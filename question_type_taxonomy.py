"""Question type taxonomy for professional engineer answer grading.

The v2 taxonomy uses broad answer-development lenses instead of short-answer
style labels. The question_type does not replace A/B/C/D/E scoring. It only
guides C fact explanation and D field judgement.
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
    """Lightweight rule-based detector for v2 question types.

    This is intentionally conservative. LLM/prompt logic may refine it later.
    """
    text = (question_text or "").lower()
    data = load_question_type_taxonomy()

    # Priority matters. Diagnosis and comparison should not be swallowed by
    # generic principle keywords.
    priority = [
        "DIAGNOSIS_ACTION",
        "COMPARE_SELECTION",
        "IMPLEMENTATION_EVALUATION",
        "PRINCIPLE_INTERPRETATION",
    ]

    scores: dict[str, int] = {k: 0 for k in priority}

    for qt in priority:
        signals = data["types"][qt].get("selection_signals", [])
        for sig in signals:
            if str(sig).lower() in text:
                scores[qt] += 1

    # Strong compound patterns.
    if any(k in text for k in ["원인과 대책", "발생원인과 대책", "문제점", "개선방안"]):
        scores["DIAGNOSIS_ACTION"] += 3

    if any(k in text for k in ["비교", "차이점", "장단점", "선정"]):
        scores["COMPARE_SELECTION"] += 3

    if any(k in text for k in ["절차", "교정", "시험", "평가", "적용 사례", "구성도"]):
        scores["IMPLEMENTATION_EVALUATION"] += 3

    if any(k in text for k in ["원리", "전달함수", "상태방정식", "응답특성", "안정도", "계산", "구하시오"]):
        scores["PRINCIPLE_INTERPRETATION"] += 2

    best = max(priority, key=lambda k: scores[k])
    if scores[best] <= 0:
        return data.get("fallback_type", "PRINCIPLE_INTERPRETATION")

    return best
