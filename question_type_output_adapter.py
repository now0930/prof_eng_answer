"""Attach v2 question_type guidance to grading output.

This module does not change scores. It only adds a broad answer-development
lens and sub-criteria for C fact explanation and D field judgement.
"""

from __future__ import annotations

from typing import Any

from question_type_taxonomy import (
    detect_question_type_from_text,
    get_question_type_profile,
    normalize_question_type,
)


def _find_existing_question_type(grade: dict[str, Any]) -> str | None:
    candidates = [
        grade.get("question_type"),
        grade.get("detected_question_type"),
    ]

    analysis = grade.get("analysis")
    if isinstance(analysis, dict):
        candidates.extend([
            analysis.get("question_type"),
            analysis.get("detected_question_type"),
        ])

    semantic = grade.get("semantic_evaluation")
    if isinstance(semantic, dict):
        candidates.extend([
            semantic.get("question_type"),
            semantic.get("detected_question_type"),
        ])

    for value in candidates:
        if value:
            return str(value)

    return None


def attach_question_type_v2_to_grade(
    grade: dict[str, Any],
    question_text: str | None = None,
    existing_question_type: str | None = None,
) -> dict[str, Any]:
    """Attach v2 question_type profile to grade.

    The function is intentionally non-scoring. It does not change total_score,
    subsection scores, caps, or difficulty strategy.
    """
    if not isinstance(grade, dict):
        return grade

    legacy_or_existing = existing_question_type or _find_existing_question_type(grade)

    if legacy_or_existing:
        question_type = normalize_question_type(legacy_or_existing)
        legacy_question_type = str(legacy_or_existing).strip().upper()
    else:
        question_type = detect_question_type_from_text(question_text or "")
        legacy_question_type = None

    profile = get_question_type_profile(question_type)

    grade["question_type"] = question_type
    grade["question_type_v2"] = {
        "question_type": question_type,
        "legacy_question_type": legacy_question_type,
        "name_ko": profile.get("name_ko"),
        "intent": profile.get("intent"),
        "c_fact_focus": profile.get("c_fact_focus", []),
        "d_field_judgement_focus": profile.get("d_field_judgement_focus", []),
        "sub_criteria": profile.get("sub_criteria", []),
        "note": (
            "question_type은 별도 점수체계가 아니라 C항목 Fact 설명과 "
            "D항목 현장 판단을 보완하는 lens입니다."
        ),
    }

    return grade
