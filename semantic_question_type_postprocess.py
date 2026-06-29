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


def ensure_question_type_coverage(
    result: dict[str, Any],
    question_text: str | None = None,
    existing_question_type: str | None = None,
) -> dict[str, Any]:
    if not isinstance(result, dict):
        return result

    # Case 1: provider envelope with parsed dict.
    parsed = result.get("parsed")
    if isinstance(parsed, dict):
        coverage = parsed.get("question_type_coverage")

        if isinstance(coverage, dict) and coverage.get("question_type"):
            coverage = _mark_semantic_coverage(coverage)
            parsed["question_type_coverage"] = coverage
            parsed["question_type"] = coverage["question_type"]
            result["question_type_coverage"] = coverage
            result["question_type"] = coverage["question_type"]
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
        parsed["question_type"] = fallback["question_type"]
        result["question_type_coverage"] = fallback
        result["question_type"] = fallback["question_type"]
        return result

    # Case 2: direct parsed semantic result.
    coverage = result.get("question_type_coverage")

    if isinstance(coverage, dict) and coverage.get("question_type"):
        coverage = _mark_semantic_coverage(coverage)
        result["question_type_coverage"] = coverage
        result["question_type"] = coverage["question_type"]
        return result

    fallback = _make_fallback_coverage(
        question_text=question_text,
        existing_question_type=existing_question_type or result.get("question_type"),
    )

    result["question_type_coverage"] = fallback
    result["question_type"] = fallback["question_type"]
    return result
