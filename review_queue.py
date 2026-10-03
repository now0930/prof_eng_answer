"""Daily review queue contract and deterministic starter selector."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable
from uuid import uuid4


QUEUE_REASONS = {
    "weak_topic",
    "long_unreviewed_topic",
    "recently_changed_topic",
    "new_topic",
}
_RETENTION_REASONS = {"long_unreviewed_topic", "recently_changed_topic", "new_topic"}


class ReviewQueueError(ValueError):
    pass


def build_review_queue(
    candidates: Iterable[dict[str, Any]],
    *,
    generated_at: str,
    daily_target: int = 2,
    queue_id: str | None = None,
) -> dict[str, Any]:
    """Pick at most two distinct Topics: one weak and one retention candidate.

    Selection is intentionally small and stable. Ranking policy can evolve
    without changing the queue record contract.
    """
    if daily_target != 2:
        raise ReviewQueueError("daily_target is fixed at 2 for this contract")
    try:
        parsed_time = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise ReviewQueueError("generated_at must be ISO-8601") from exc
    if parsed_time.tzinfo is None:
        raise ReviewQueueError("generated_at must include a timezone")

    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ReviewQueueError("candidate must be an object")
        topic_id = candidate.get("topic_id")
        reason = candidate.get("reason")
        question_id = candidate.get("question_id")
        question_text = candidate.get("question_text")
        if not isinstance(topic_id, str) or len(topic_id) < 8:
            raise ReviewQueueError("candidate topic_id is invalid")
        if reason not in QUEUE_REASONS:
            raise ReviewQueueError("candidate reason is invalid")
        if question_id is not None and (not isinstance(question_id, str) or not question_id.strip()):
            raise ReviewQueueError("question_id must be a non-empty string or null")
        if question_text is not None and not isinstance(question_text, str):
            raise ReviewQueueError("question_text must be a string")
        identity = (topic_id, reason)
        if identity in seen:
            continue
        seen.add(identity)
        normalized.append({"topic_id": topic_id, "reason": reason, "question_id": question_id, "question_text": question_text or ""})

    weak = next((item for item in normalized if item["reason"] == "weak_topic"), None)
    retention = next((item for item in normalized if item["reason"] in _RETENTION_REASONS and (weak is None or item["topic_id"] != weak["topic_id"])), None)
    chosen: list[tuple[dict[str, Any], str]] = []
    if weak is not None:
        chosen.append((weak, "weakness"))
    if retention is not None:
        chosen.append((retention, "retention"))
    if len(chosen) < daily_target:
        chosen_topics = {item["topic_id"] for item, _ in chosen}
        for item in normalized:
            if item["topic_id"] in chosen_topics:
                continue
            chosen.append((item, "weakness" if not chosen else "retention"))
            chosen_topics.add(item["topic_id"])
            if len(chosen) == daily_target:
                break

    return {
        "queue_id": queue_id or str(uuid4()),
        "generated_at": parsed_time.isoformat(),
        "daily_target": daily_target,
        "items": [
            {
                "topic_id": item["topic_id"],
                "reason": item["reason"],
                "slot": slot,
                "question_id": item["question_id"],
                "question_text": item["question_text"],
            }
            for item, slot in chosen
        ],
    }
