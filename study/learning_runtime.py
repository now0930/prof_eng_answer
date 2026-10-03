"""Application integration for persisted grades and learner review queues."""

from __future__ import annotations

from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import Any

from grading.scoring.grading_identity import build_grading_identity
from .master_topic_pack import load_legacy_topic_sources, load_master_topic_pack
from .review_queue import build_review_queue
from .training_history import TrainingAttempt, TrainingHistoryStore


WEAK_SCORE_THRESHOLD = 15.0
LONG_UNREVIEWED_DAYS = 30
DEFAULT_REVIEW_INTERVAL_DAYS = 30


class LearningRuntimeError(ValueError):
    pass


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed


def _question_id(question_text: str, sid: str) -> str:
    normalized = str(question_text or "").strip()
    identity = normalized if normalized else f"session:{sid}"
    return build_grading_identity(identity, "").question_hash


def diagnosis_from_grade(grade: dict[str, Any]) -> dict[str, Any]:
    """Keep concise, structured learning feedback from the final grade."""
    ledger = grade.get("canonical_evaluation_ledger")
    ledger_summary = ledger.get("summary") if isinstance(ledger, dict) else None
    return {
        "summary": str(
            grade.get("overall_summary")
            or grade.get("summary")
            or grade.get("overall_comment")
            or ""
        ),
        "weaknesses": grade.get("weaknesses") if isinstance(grade.get("weaknesses"), list) else [],
        "improvement_points": grade.get("improvement_points") if isinstance(grade.get("improvement_points"), list) else [],
        "missing_keywords": grade.get("missing_keywords") if isinstance(grade.get("missing_keywords"), list) else [],
        "layer_scores": grade.get("breakdown") if isinstance(grade.get("breakdown"), list) else [],
        "question_type": grade.get("question_type"),
        "demand_status_counts": ledger_summary.get("status_counts") if isinstance(ledger_summary, dict) else {},
        "fatal_findings": [
            item for item in grade.get("verified_defects", [])
            if isinstance(item, dict) and str(item.get("severity", "")).lower() in {"fatal", "major"}
        ] if isinstance(grade.get("verified_defects"), list) else [],
        "verdict": grade.get("verdict") or grade.get("score_status"),
    }


def _topic_masters(master_directory: str | Path) -> dict[str, dict[str, Any]]:
    directory = Path(master_directory)
    result = {}
    for path in sorted(directory.glob("*.json")):
        master = load_master_topic_pack(path)
        result[master["topic_id"]] = master
    return result


def _master_question(
    master: dict[str, Any],
    repository_root: str | Path,
) -> tuple[str | None, str]:
    sources = load_legacy_topic_sources(repository_root, master)
    model_answer = sources.get("model_answer", {})
    examples = model_answer.get("question_examples")
    if not isinstance(examples, list) or not examples:
        patterns = model_answer.get("expected_question_patterns")
        examples = [
            row.get("pattern") for row in patterns
            if isinstance(row, dict) and isinstance(row.get("pattern"), str)
        ] if isinstance(patterns, list) else []
    question_text = next((item.strip() for item in examples if isinstance(item, str) and item.strip()), "")
    return (_question_id(question_text, "") if question_text else None), question_text


def _review_candidates(
    attempts: list[dict[str, Any]],
    masters: dict[str, dict[str, Any]],
    unattempted_reviews: dict[str, dict[str, str]],
    *,
    now: datetime,
    repository_root: str | Path,
) -> list[dict[str, Any]]:
    by_topic: dict[str, dict[str, Any]] = {}
    for attempt in attempts:
        prior = by_topic.get(attempt["topic_id"])
        if prior is not None and _parse_time(attempt["attempted_at"]) <= _parse_time(prior["attempted_at"]):
            continue
        by_topic[attempt["topic_id"]] = attempt

    candidates: list[dict[str, Any]] = []
    weak_rows = sorted(
        (
            row for row in by_topic.values()
            if float(row["score"]) < WEAK_SCORE_THRESHOLD
            and (not row.get("next_review_at") or _parse_time(row["next_review_at"]) <= now)
        ),
        key=lambda row: (float(row["score"]), row["topic_id"]),
    )
    for row in weak_rows:
        candidates.append({"topic_id": row["topic_id"], "reason": "weak_topic", "question_id": row["question_id"], "question_text": row.get("question_text", "")})

    recently_changed = []
    long_unreviewed = []
    for topic_id, row in by_topic.items():
        master = masters.get(topic_id)
        if master is not None:
            attempt_at = _parse_time(row["attempted_at"])
            last_review = row.get("last_reviewed_at")
            baseline = max(attempt_at, _parse_time(last_review)) if last_review else attempt_at
            changed_after_attempt = []
            for source in master.get("sources", []):
                updated_at = source.get("updated_at") if isinstance(source, dict) else None
                if isinstance(updated_at, str):
                    try:
                        source_time = _parse_time(updated_at)
                    except ValueError:
                        continue
                    if baseline < source_time <= now:
                        changed_after_attempt.append(source_time)
            if changed_after_attempt:
                recently_changed.append((max(changed_after_attempt), topic_id, row))

        next_review = row.get("next_review_at")
        next_due = _parse_time(next_review) if next_review else None
        attempted_at = _parse_time(row["attempted_at"])
        if (next_due is not None and next_due <= now) or (
            next_due is None and attempted_at <= now - timedelta(days=LONG_UNREVIEWED_DAYS)
        ):
            long_unreviewed.append((attempted_at, topic_id, row))

    for _, topic_id, row in sorted(recently_changed, key=lambda item: (-item[0].timestamp(), item[1])):
        candidates.append({"topic_id": topic_id, "reason": "recently_changed_topic", "question_id": row["question_id"], "question_text": row.get("question_text", "")})
    for _, topic_id, row in sorted(long_unreviewed, key=lambda item: (item[0], item[1])):
        candidates.append({"topic_id": topic_id, "reason": "long_unreviewed_topic", "question_id": row["question_id"], "question_text": row.get("question_text", "")})

    for topic_id in sorted(set(masters) - set(by_topic)):
        master = masters[topic_id]
        review = unattempted_reviews.get(topic_id)
        if review is not None and _parse_time(review["next_review_at"]) > now:
            continue
        question_id, question_text = _master_question(master, repository_root)
        reason = "long_unreviewed_topic" if review is not None else "new_topic"
        candidates.append({"topic_id": topic_id, "reason": reason, "question_id": question_id, "question_text": question_text})
    return candidates


def create_daily_review_queue(
    history: TrainingHistoryStore,
    *,
    learner_id: str,
    master_directory: str | Path,
    generated_at: str,
) -> tuple[dict[str, Any], dict[str, str]]:
    """Return the current two-item queue and its topic-title lookup."""
    now = _parse_time(generated_at)
    masters = _topic_masters(master_directory)
    queue_date = now.date().isoformat()
    existing_queue = history.get_daily_queue(learner_id, queue_date)
    titles = {topic_id: master["title_ko"] for topic_id, master in masters.items()}
    if existing_queue is not None:
        return existing_queue, titles
    attempts = history.list_attempts(learner_id=learner_id)
    unattempted_reviews = history.list_unattempted_topic_reviews(learner_id)
    repository_root = Path(master_directory).resolve().parent
    candidates = _review_candidates(
        attempts, masters, unattempted_reviews, now=now, repository_root=repository_root
    )
    queue = build_review_queue(candidates, generated_at=generated_at)
    queue = history.save_daily_queue(learner_id, queue_date, queue)
    return queue, titles


def record_completed_grade(
    history: TrainingHistoryStore,
    *,
    learner_id: str,
    sid: str,
    grade: dict[str, Any],
    submission_normalization: dict[str, Any],
    master_directory: str | Path,
    session_directory: str | Path,
    attempted_at: str | None = None,
) -> dict[str, Any]:
    """Persist one final grade, then snapshot the next queue beside its session."""
    if not isinstance(grade, dict):
        raise LearningRuntimeError("grade must be an object")
    score = grade.get("final_total_score")
    if score is None:
        score = grade.get("total_score")
    topic_id = grade.get("topic_id") or grade.get("inferred_topic_id")
    if not isinstance(topic_id, str) or not topic_id.strip():
        raise LearningRuntimeError("grade has no routed topic_id")
    if score is None:
        raise LearningRuntimeError("grade has no final score")
    question_text = str(submission_normalization.get("question_text") or "")
    timestamp = attempted_at or datetime.now().astimezone().isoformat(timespec="seconds")
    question_id = _question_id(question_text, sid)
    attempt = history.save(TrainingAttempt(
        learner_id=str(learner_id),
        question_id=question_id,
        topic_id=topic_id,
        attempted_at=timestamp,
        score=score,
        diagnosis=diagnosis_from_grade(grade),
        question_text=question_text,
        session_id=sid,
    ))
    queue, titles = create_daily_review_queue(
        history,
        learner_id=str(learner_id),
        master_directory=master_directory,
        generated_at=timestamp,
    )
    snapshot = {
        "history_status": "saved",
        "attempt_id": attempt["attempt_id"],
        "queue": queue,
        "topic_titles": titles,
    }
    directory = Path(session_directory)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "learning_history.json"
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(target)
    return snapshot


def complete_topic_review(
    history: TrainingHistoryStore,
    *,
    learner_id: str,
    topic_id: str,
    reviewed_at: str | None = None,
    interval_days: int = DEFAULT_REVIEW_INTERVAL_DAYS,
) -> dict[str, Any]:
    timestamp = reviewed_at or datetime.now().astimezone().isoformat(timespec="seconds")
    try:
        next_review_at = (_parse_time(timestamp) + timedelta(days=interval_days)).isoformat(timespec="seconds")
    except ValueError as exc:
        raise LearningRuntimeError(str(exc)) from exc
    try:
        if history.list_attempts(learner_id=learner_id, topic_id=topic_id):
            return history.review_latest_for_topic(
                learner_id,
                topic_id,
                last_reviewed_at=timestamp,
                next_review_at=next_review_at,
            )
        return history.schedule_unattempted_topic_review(
            learner_id,
            topic_id,
            last_reviewed_at=timestamp,
            next_review_at=next_review_at,
        )
    except ValueError as exc:
        raise LearningRuntimeError(str(exc)) from exc
