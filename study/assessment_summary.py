"""Score-neutral whole-exam summary; never changes individual grades."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import isfinite


def summarize_assessment(
    grades: Sequence[Mapping[str, object]], *, expected_questions: int = 4,
    pass_percent: float = 60.0,
) -> dict[str, object]:
    """Judge the 60/100 target only after every question is present and scored.

    The caller must supply one grade per question with a stable question_id.
    This is a study target, not a claim about any official exam decision.
    """
    if expected_questions < 1 or not 0 < pass_percent <= 100:
        raise ValueError("invalid_assessment_contract")
    seen: set[str] = set()
    points = 0.0
    maximum = 0.0
    rows: list[dict[str, object]] = []
    for grade in grades:
        if (grade.get("resolution_review") or {}).get("required"):
            raise ValueError("provisional_grade_requires_review")
        question_id = str(grade.get("question_id") or "").strip()
        score = grade.get("total_score")
        max_score = grade.get("max_score", 25.0)
        if not question_id or question_id in seen:
            raise ValueError("missing_or_duplicate_question_id")
        if (
            isinstance(score, bool) or not isinstance(score, (int, float))
            or isinstance(max_score, bool) or not isinstance(max_score, (int, float))
            or not isfinite(score) or not isfinite(max_score)
            or max_score <= 0 or not 0 <= score <= max_score
        ):
            raise ValueError("invalid_grade_score")
        seen.add(question_id)
        points += score
        maximum += max_score
        rows.append({"question_id": question_id, "score": score, "max_score": max_score})
    if len(rows) > expected_questions:
        raise ValueError("too_many_questions")
    complete = len(rows) == expected_questions
    percent = round(points / maximum * 100, 2) if maximum else None
    return {
        "complete": complete,
        "scored_questions": len(rows),
        "expected_questions": expected_questions,
        "points": round(points, 2),
        "maximum": round(maximum, 2),
        "percent_so_far": percent,
        "target_percent": pass_percent,
        "target_met": bool(complete and percent is not None and percent >= pass_percent),
        "decision": (
            "TARGET_MET" if complete and percent is not None and percent >= pass_percent
            else "BELOW_TARGET" if complete else "INCOMPLETE"
        ),
        "questions": rows,
    }
