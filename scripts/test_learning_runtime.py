from __future__ import annotations

import copy
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from study.learning_runtime import (
    _master_question,
    _question_id,
    _review_candidates,
    complete_topic_review,
    create_daily_review_queue,
    record_completed_grade,
    review_material_for_topic,
)
from study.master_topic_pack import load_legacy_topic_sources, load_master_topic_pack
from study.training_history import TrainingAttempt, TrainingHistoryStore


def test_grade_history_and_manual_completion_cycle() -> None:
    topics = sorted((ROOT / "master_topic_packs").glob("*.json"))
    assert len(topics) >= 3
    master_one_topic = topics[0].stem
    # Projection-backed question selection must preserve the legacy source
    # precedence and selected text for every available Master fixture.
    for topic_path in topics:
        master = load_master_topic_pack(topic_path)
        model_answer = load_legacy_topic_sources(ROOT, master).get("model_answer", {})
        legacy_examples = model_answer.get("question_examples")
        if not isinstance(legacy_examples, list) or not legacy_examples:
            patterns = model_answer.get("expected_question_patterns")
            legacy_examples = [
                row.get("pattern") for row in patterns
                if isinstance(row, dict) and isinstance(row.get("pattern"), str)
            ] if isinstance(patterns, list) else []
        legacy_text = next((item.strip() for item in legacy_examples if isinstance(item, str) and item.strip()), "")
        assert _master_question(master, ROOT) == (
            _question_id(legacy_text, "") if legacy_text else None,
            legacy_text,
        )
    attempted_at = "2026-10-03T10:00:00+09:00"
    with tempfile.TemporaryDirectory(prefix="learning-runtime-") as directory:
        base = Path(directory)
        history = TrainingHistoryStore(base / "history.sqlite3")
        output = record_completed_grade(
            history,
            learner_id="telegram-chat-100",
            sid="session-1",
            grade={"topic_id": master_one_topic, "final_total_score": 12.0, "breakdown": []},
            submission_normalization={"question_text": "Define the topic and give an application."},
            master_directory=ROOT / "master_topic_packs",
            session_directory=base / "session-1",
            attempted_at=attempted_at,
        )
        assert output["history_status"] == "saved"
        assert "queue" not in output
        assert history.get_daily_queue("telegram-chat-100", "2026-10-03") is None
        assert len(history.list_attempts(learner_id="telegram-chat-100")) == 1
        assert history.list_attempts(learner_id="telegram-chat-100")[0]["question_text"] == "Define the topic and give an application."
        stored_diagnosis = history.list_attempts(learner_id="telegram-chat-100")[0]["diagnosis"]
        assert stored_diagnosis["topic_guidance"]["score_effect"] == "none"
        assert stored_diagnosis["topic_guidance"]["topic_id"] == master_one_topic
        assert len(history.list_attempts(learner_id="another-chat")) == 0
        assert (base / "session-1" / "learning_history.json").is_file()

        # The optional queue contract remains available, but grading no longer
        # creates a date-bound queue as a side effect.
        first_queue, _ = create_daily_review_queue(
            history,
            learner_id="telegram-chat-100",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-03T10:00:00+09:00",
        )
        assert len(first_queue["items"]) == 2
        same_day_queue, _ = create_daily_review_queue(
            history,
            learner_id="telegram-chat-100",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-03T23:00:00+09:00",
        )
        assert same_day_queue == first_queue

        completion_time = "2026-10-04T10:00:00+09:00"
        reviewed = complete_topic_review(
            history,
            learner_id="telegram-chat-100",
            topic_id=master_one_topic,
            reviewed_at=completion_time,
        )
        assert reviewed["review_status"] == "scheduled"
        assert reviewed["next_review_at"].startswith("2026-11-03")

        queue, _ = create_daily_review_queue(
            history,
            learner_id="telegram-chat-100",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-04T10:01:00+09:00",
        )
        assert all(item["topic_id"] != master_one_topic for item in queue["items"])


def test_review_queue_uses_due_history_and_keeps_learners_separate() -> None:
    topics = sorted((ROOT / "master_topic_packs").glob("*.json"))
    topic_id = topics[0].stem
    with tempfile.TemporaryDirectory(prefix="learning-runtime-due-") as directory:
        history = TrainingHistoryStore(Path(directory) / "history.sqlite3")
        history.save(TrainingAttempt(
            learner_id="alice",
            question_id="q-alice",
            topic_id=topic_id,
            attempted_at="2026-08-01T10:00:00+09:00",
            score=18,
            diagnosis={},
            review_status="scheduled",
            next_review_at="2026-09-01T10:00:00+09:00",
        ))
        queue_alice, _ = create_daily_review_queue(
            history,
            learner_id="alice",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-03T10:00:00+09:00",
        )
        queue_bob, _ = create_daily_review_queue(
            history,
            learner_id="bob",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-03T10:00:00+09:00",
        )
        assert any(item["topic_id"] == topic_id for item in queue_alice["items"])
        alice_candidates = _review_candidates(
            history.list_attempts(learner_id="alice"),
            {master["topic_id"]: master for master in (load_master_topic_pack(path) for path in topics)},
            history.list_unattempted_topic_reviews("alice"),
            now=datetime.fromisoformat("2026-10-03T10:00:00+09:00"),
            repository_root=ROOT,
        )
        assert any(
            item["topic_id"] == topic_id and item["reason"] == "long_unreviewed_topic"
            for item in alice_candidates
        )
        bob_topic = next(item for item in queue_bob["items"] if item["topic_id"] == topic_id)
        assert bob_topic["reason"] == "new_topic"


def test_unattempted_topic_completion_survives_until_due() -> None:
    with tempfile.TemporaryDirectory(prefix="learning-runtime-new-topic-") as directory:
        history = TrainingHistoryStore(Path(directory) / "history.sqlite3")
        first_queue, _ = create_daily_review_queue(
            history,
            learner_id="new-learner",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-03T10:00:00+09:00",
        )
        topic_id = first_queue["items"][0]["topic_id"]
        reviewed = complete_topic_review(
            history,
            learner_id="new-learner",
            topic_id=topic_id,
            reviewed_at="2026-10-03T10:30:00+09:00",
        )
        assert reviewed["next_review_at"].startswith("2026-11-02")
        history.complete_daily_queue_item("new-learner", "2026-10-03", topic_id)
        assert history.list_attempts(learner_id="new-learner") == []
        tomorrow, _ = create_daily_review_queue(
            history,
            learner_id="new-learner",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-04T10:00:00+09:00",
        )
        assert all(item["topic_id"] != topic_id for item in tomorrow["items"])
        due, _ = create_daily_review_queue(
            history,
            learner_id="new-learner",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-11-03T10:00:00+09:00",
        )
        assert any(
            item["topic_id"] == topic_id and item["reason"] == "long_unreviewed_topic"
            for item in due["items"]
        )


def test_source_change_is_acknowledged_after_review() -> None:
    master = copy.deepcopy(load_master_topic_pack(sorted((ROOT / "master_topic_packs").glob("*.json"))[0]))
    topic_id = master["topic_id"]
    master["sources"].append({"updated_at": "2026-10-01T10:00:00+09:00"})
    attempt = {
        "topic_id": topic_id,
        "question_id": "q1",
        "question_text": "Explain this topic.",
        "attempted_at": "2026-09-01T10:00:00+09:00",
        "last_reviewed_at": "2026-10-02T10:00:00+09:00",
        "next_review_at": "2026-11-01T10:00:00+09:00",
        "score": 18.0,
    }
    before = _review_candidates(
        [attempt], {topic_id: master}, {}, now=datetime.fromisoformat("2026-10-03T10:00:00+09:00"),
        repository_root=ROOT,
    )
    assert not any(item["reason"] == "recently_changed_topic" for item in before)
    master["sources"][0]["updated_at"] = "2026-10-03T09:00:00+09:00"
    after = _review_candidates(
        [attempt], {topic_id: master}, {}, now=datetime.fromisoformat("2026-10-03T10:00:00+09:00"),
        repository_root=ROOT,
    )
    assert any(item["reason"] == "recently_changed_topic" for item in after)


def test_missing_master_keeps_grade_diagnosis_persistable() -> None:
    topic_id = "missing_master_topic"
    with tempfile.TemporaryDirectory(prefix="learning-runtime-no-master-") as directory:
        base = Path(directory)
        master_directory = base / "master_topic_packs"
        master_directory.mkdir()
        history = TrainingHistoryStore(base / "history.sqlite3")
        snapshot = record_completed_grade(
            history,
            learner_id="learner-without-master",
            sid="session-no-master",
            grade={
                "topic_id": topic_id,
                "final_total_score": 14.0,
                "verdict": "below",
                "weaknesses": ["application"],
            },
            submission_normalization={"question_text": "Explain the topic."},
            master_directory=master_directory,
            session_directory=base / "session",
            attempted_at="2026-10-03T10:00:00+09:00",
        )
        row = history.list_attempts(learner_id="learner-without-master")[0]
        assert snapshot["history_status"] == "saved"
        assert row["score"] == 14.0
        assert row["diagnosis"]["weaknesses"] == ["application"]
        assert "topic_guidance" not in row["diagnosis"]


def test_review_material_supports_legacy_history_without_view_feedback() -> None:
    master_path = sorted((ROOT / "master_topic_packs").glob("*.json"))[0]
    topic_id = master_path.stem
    with tempfile.TemporaryDirectory(prefix="review-material-legacy-history-") as directory:
        history = TrainingHistoryStore(Path(directory) / "history.sqlite3")
        history.save(TrainingAttempt(
            learner_id="legacy-learner",
            question_id="legacy-question",
            topic_id=topic_id,
            attempted_at="2026-09-01T10:00:00+09:00",
            score=16,
            diagnosis={"weaknesses": ["legacy weakness"]},
        ))
        material = review_material_for_topic(
            history,
            learner_id="legacy-learner",
            topic_id=topic_id,
            master_directory=ROOT / "master_topic_packs",
        )
        assert material["training"]["topic_id"] == topic_id
        assert material["feedback"] is None
        assert material["prior_diagnosis"]["weaknesses"] == ["legacy weakness"]


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"LEARNING_RUNTIME_TESTS={len(tests)}_PASS")
