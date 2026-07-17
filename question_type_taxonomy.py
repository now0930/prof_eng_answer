"""Question type taxonomy for professional engineer answer grading.

The v2 taxonomy uses broad answer-development lenses instead of short-answer
style labels. The question_type does not replace A/B/C/D/E scoring. It guides
B requirement completeness, C fact explanation, and D field judgement.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
TAXONOMY_PATH = ROOT / "rubrics" / "question_types" / "v2_professional_engineer.json"


@lru_cache(maxsize=1)
def load_question_type_taxonomy() -> dict[str, Any]:
    with TAXONOMY_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def valid_question_types() -> list[str]:
    data = load_question_type_taxonomy()
    return list(data.get("types", {}).keys())


def legacy_question_type_mapping() -> dict[str, str | None]:
    data = load_question_type_taxonomy()
    return dict(data.get("legacy_mapping", {}))


def normalize_question_type(question_type: str | None) -> str:
    """Return the v2 question type.

    Legacy types are accepted during migration.
    DEFINE is intentionally removed. If it appears, use fallback.
    """
    data = load_question_type_taxonomy()
    fallback = data.get("fallback_type", "PRINCIPLE_INTERPRETATION")

    if not question_type:
        return fallback

    qt = str(question_type).strip().upper()

    if qt in data.get("types", {}):
        return qt

    mapped = data.get("legacy_mapping", {}).get(qt)
    if mapped:
        return mapped

    return fallback


def get_question_type_profile(question_type: str | None) -> dict[str, Any]:
    data = load_question_type_taxonomy()
    qt = normalize_question_type(question_type)
    profile = dict(data["types"][qt])
    profile["question_type"] = qt
    return profile


def question_type_sub_criteria(question_type: str | None) -> list[str]:
    return list(get_question_type_profile(question_type).get("sub_criteria", []))


def question_type_c_focus(question_type: str | None) -> list[str]:
    return list(get_question_type_profile(question_type).get("c_fact_focus", []))


def question_type_d_focus(question_type: str | None) -> list[str]:
    return list(get_question_type_profile(question_type).get("d_field_judgement_focus", []))


def detect_question_type_from_text(question_text: str) -> str:
    """Detect a V2 type with demand verbs taking precedence."""
    import re

    text = (question_text or "").lower()
    data = load_question_type_taxonomy()

    priority = [
        "DIAGNOSIS_ACTION",
        "COMPARE_SELECTION",
        "IMPLEMENTATION_EVALUATION",
        "PRINCIPLE_INTERPRETATION",
    ]

    scores: dict[str, int] = {
        question_type: 0
        for question_type in priority
    }

    selection_context = bool(
        re.search(
            (
                r"선정\s*(?:시|할\s*때|과정에서|단계에서|"
                r"에\s*있어|을\s*위한)"
            ),
            text,
        )
    )

    explicit_compare_demand = any(
        expression in text
        for expression in [
            "비교",
            "차이점",
            "장단점",
            "대비",
            "선정하시오",
            "선정하여",
            "선정하고",
            "선택하시오",
            "선택하여",
        ]
    )

    explicit_principle_demand = any(
        expression in text
        for expression in [
            "개념 설명",
            "개념을 설명",
            "원리 설명",
            "원리를 설명",
            "설계 기준 제시",
            "설계기준 제시",
            "기준을 제시",
            "해석하시오",
        ]
    )

    explicit_diagnosis_demand = any(
        expression in text
        for expression in [
            "원인과 대책",
            "발생원인과 대책",
            "문제점과 개선",
            "문제점",
            "개선방안",
        ]
    )

    explicit_implementation_demand = any(
        expression in text
        for expression in [
            "절차를 설명",
            "시험 방법",
            "평가 방법",
            "적용 사례",
            "구성도를",
            "구현 방법",
        ]
    )

    for question_type in priority:
        signals = (
            data["types"][question_type]
            .get("selection_signals", [])
        )

        for signal in signals:
            normalized_signal = str(signal).lower()

            if (
                question_type == "COMPARE_SELECTION"
                and normalized_signal in {
                    "선정",
                    "선택",
                }
                and selection_context
                and not explicit_compare_demand
            ):
                continue

            if normalized_signal in text:
                scores[question_type] += 1

    if explicit_diagnosis_demand:
        scores["DIAGNOSIS_ACTION"] += 5

    if explicit_compare_demand:
        scores["COMPARE_SELECTION"] += 5

    if explicit_implementation_demand:
        scores["IMPLEMENTATION_EVALUATION"] += 5

    if explicit_principle_demand:
        scores["PRINCIPLE_INTERPRETATION"] += 7

    if selection_context and not explicit_compare_demand:
        scores["COMPARE_SELECTION"] = min(
            scores["COMPARE_SELECTION"],
            1,
        )

    if any(
        keyword in text
        for keyword in [
            "원리",
            "전달함수",
            "상태방정식",
            "응답특성",
            "안정도",
            "계산",
            "구하시오",
        ]
    ):
        scores["PRINCIPLE_INTERPRETATION"] += 2

    best = max(
        priority,
        key=lambda question_type: scores[
            question_type
        ],
    )

    if scores[best] <= 0:
        return data.get(
            "fallback_type",
            "PRINCIPLE_INTERPRETATION",
        )

    return best
