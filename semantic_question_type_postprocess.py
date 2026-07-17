"""Postprocess semantic grader output for question_type coverage.

Gemini/CLOVA wrappers may return either:

1. Direct parsed semantic result:
   {"layers": [...], "question_type_coverage": {...}}

2. Provider envelope:
   {"ok": true, "parsed": {"layers": [...]}}

This module ensures question_type_coverage is available in the semantic result.
Fallback coverage is marked as unknown and must not be used for score adjustment.
"""

from __future__ import annotations

from typing import Any

from question_type_taxonomy import normalize_question_type
from semantic_question_type_prompt import empty_question_type_coverage


def _mark_semantic_coverage(coverage: dict[str, Any]) -> dict[str, Any]:
    coverage["question_type"] = normalize_question_type(coverage.get("question_type"))
    coverage.setdefault("coverage_source", "semantic_grader")
    return coverage


def _make_fallback_coverage(
    question_text: str | None = None,
    existing_question_type: str | None = None,
) -> dict[str, Any]:
    fallback = empty_question_type_coverage(
        question_text=question_text,
        existing_question_type=existing_question_type,
    )

    fallback["overall_coverage"] = "unknown"
    fallback["coverage_source"] = "fallback_missing_semantic_field"
    fallback["sub_criteria_coverage"] = []
    fallback["missing_sub_criteria"] = []
    fallback["c_fact_focus_coverage"] = {
        "covered": [],
        "missing": [],
    }
    fallback["d_field_judgement_focus_coverage"] = {
        "covered": [],
        "missing": [],
    }
    fallback["scoring_hint"] = (
        "semantic grader가 question_type_coverage 필드를 반환하지 않아 "
        "fallback coverage를 생성했습니다. 이 값은 점수 보정에 사용하지 않습니다."
    )
    return fallback


def _canonicalize_semantic_question_type(
    coverage: dict[str, Any],
    question_text: str | None,
    existing_question_type: str | None,
) -> dict[str, Any]:
    if not isinstance(coverage, dict):
        return coverage

    semantic_type = coverage.get("question_type")

    if not semantic_type or not question_text:
        return coverage

    try:
        from question_type_taxonomy import (
            detect_question_type_from_text,
            normalize_question_type,
        )

        semantic_normalized = normalize_question_type(
            str(semantic_type)
        )
        detected_type = detect_question_type_from_text(
            question_text
        )
    except Exception:
        return coverage

    existing_raw = str(
        existing_question_type or ""
    ).strip().upper()

    canonical_v2_types = {
        "COMPARE_SELECTION",
        "DIAGNOSIS_ACTION",
        "IMPLEMENTATION_EVALUATION",
        "PRINCIPLE_INTERPRETATION",
    }

    existing_normalized = None

    if existing_raw in canonical_v2_types:
        existing_normalized = normalize_question_type(
            existing_raw
        )

    lowered_question = question_text.lower()

    explicit_compare_demand = any(
        expression in lowered_question
        for expression in [
            "비교",
            "차이점",
            "장단점",
            "대비",
            "선정하시오",
            "선정하여",
            "선정하고",
            "선택하시오",
        ]
    )

    contextual_selection = any(
        expression in lowered_question
        for expression in [
            "선정시",
            "선정 시",
            "선정할 때",
            "선정 과정에서",
            "선정에 있어",
            "선정을 위한",
        ]
    )

    principle_demand = any(
        expression in lowered_question
        for expression in [
            "개념 설명",
            "개념을 설명",
            "원리 설명",
            "원리를 설명",
            "설계 기준 제시",
            "설계기준 제시",
            "기준을 제시",
        ]
    )

    canonical_type = None
    reason = None

    if (
        existing_normalized
        and existing_normalized == detected_type
        and semantic_normalized != detected_type
    ):
        canonical_type = detected_type
        reason = (
            "Phase 9 and taxonomy demand signals agree"
        )

    elif (
        semantic_normalized == "COMPARE_SELECTION"
        and detected_type
        == "PRINCIPLE_INTERPRETATION"
        and contextual_selection
        and principle_demand
        and not explicit_compare_demand
    ):
        canonical_type = detected_type
        reason = (
            "Selection is context; explanation and "
            "design criteria are the actual demands"
        )

    if not canonical_type:
        return coverage

    normalized = dict(coverage)
    normalized["canonicalized_from"] = (
        semantic_normalized
    )
    normalized["question_type"] = canonical_type
    normalized["canonicalization_reason"] = reason

    return normalized


def ensure_question_type_coverage(
    result: dict[str, Any],
    question_text: str | None = None,
    existing_question_type: str | None = None,
) -> dict[str, Any]:
    if not isinstance(result, dict):
        return result

    parsed = result.get("parsed")

    if isinstance(parsed, dict):
        coverage = parsed.get(
            "question_type_coverage"
        )

        if (
            isinstance(coverage, dict)
            and coverage.get("question_type")
        ):
            coverage = _mark_semantic_coverage(
                coverage
            )
            coverage = (
                _canonicalize_semantic_question_type(
                    coverage,
                    question_text,
                    existing_question_type,
                )
            )

            parsed["question_type_coverage"] = coverage
            parsed["question_type"] = coverage[
                "question_type"
            ]
            result["question_type_coverage"] = coverage
            result["question_type"] = coverage[
                "question_type"
            ]
            return result

        fallback = _make_fallback_coverage(
            question_text=question_text,
            existing_question_type=(
                existing_question_type
                or parsed.get("question_type")
                or result.get("question_type")
            ),
        )

        parsed["question_type_coverage"] = fallback
        parsed["question_type"] = fallback[
            "question_type"
        ]
        result["question_type_coverage"] = fallback
        result["question_type"] = fallback[
            "question_type"
        ]
        return result

    coverage = result.get("question_type_coverage")

    if (
        isinstance(coverage, dict)
        and coverage.get("question_type")
    ):
        coverage = _mark_semantic_coverage(coverage)
        coverage = _canonicalize_semantic_question_type(
            coverage,
            question_text,
            existing_question_type,
        )

        result["question_type_coverage"] = coverage
        result["question_type"] = coverage[
            "question_type"
        ]
        return result

    fallback = _make_fallback_coverage(
        question_text=question_text,
        existing_question_type=(
            existing_question_type
            or result.get("question_type")
        ),
    )

    result["question_type_coverage"] = fallback
    result["question_type"] = fallback[
        "question_type"
    ]

    return result
