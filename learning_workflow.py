"""Additive bridge from existing grading/diagnosis output to study history."""

from __future__ import annotations

from typing import Any

from review_queue import build_review_queue
from training_history import TrainingAttempt, TrainingHistoryStore


class LearningWorkflowError(ValueError):
    pass


def record_result_and_build_queue(
    history: TrainingHistoryStore,
    *,
    question_id: str,
    topic_id: str,
    attempted_at: str,
    grade_result: dict[str, Any],
    diagnosis: dict[str, Any],
    queue_candidates: list[dict[str, Any]],
    generated_at: str,
    next_review_at: str | None = None,
) -> dict[str, Any]:
    """Persist a completed grade/diagnosis and return the next daily queue.

    This is an adapter only: it consumes the existing final score and never
    recalculates, adjusts, or writes any grading fields.
    """
    if not isinstance(grade_result, dict):
        raise LearningWorkflowError("grade_result must be an object")
    score = grade_result.get("final_total_score", grade_result.get("total_score"))
    if score is None:
        raise LearningWorkflowError("grade_result has no finalized score")
    try:
        queue = build_review_queue(queue_candidates, generated_at=generated_at)
        saved = history.save(TrainingAttempt(
            question_id=question_id,
            topic_id=topic_id,
            attempted_at=attempted_at,
            score=score,
            diagnosis=diagnosis,
            review_status="scheduled" if next_review_at else "new",
            next_review_at=next_review_at,
        ))
    except (TypeError, ValueError) as exc:
        raise LearningWorkflowError(str(exc)) from exc
    return {"training_attempt": saved, "review_queue": queue}
