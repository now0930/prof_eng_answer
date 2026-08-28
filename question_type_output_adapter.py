"""Attach v2 question_type guidance to grading output.

This module does not change scores. It only adds a broad answer-development
lens and sub-criteria for C fact explanation and D field judgement.
"""

from __future__ import annotations

from typing import Any

from question_type_router import (
    detect_question_type as detect_canonical_question_type,
)
from question_type_taxonomy import (
    get_question_type_profile,
    normalize_question_type,
    valid_question_types,
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



def _question_type_from_contract(
    question_contract: dict[str, Any] | None,
) -> str | None:
    # Return a validated canonical type from Question Contract.
    if not isinstance(question_contract, dict):
        return None

    version = str(
        question_contract.get("version") or ""
    ).strip()

    if (
        version
        and version != "question_contract_v1"
    ):
        return None

    block = question_contract.get("question_type")
    if not isinstance(block, dict):
        block = {}

    type_id = str(block.get("id") or "").strip().upper()
    lens = str(
        question_contract.get("lens") or ""
    ).strip().upper()

    if type_id and lens and type_id != lens:
        return None

    candidate = type_id or lens

    if candidate not in set(valid_question_types()):
        return None

    return candidate


def attach_question_type_v2_to_grade(
    grade: dict[str, Any],
    question_text: str | None = None,
    existing_question_type: str | None = None,
    question_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    # Attach canonical Question Type profile without changing scores.
    if not isinstance(grade, dict):
        return grade

    legacy_or_existing = (
        existing_question_type
        or _find_existing_question_type(grade)
    )
    normalized_question_text = str(
        question_text or ""
    ).strip()

    embedded_contract = grade.get("question_contract")
    effective_contract = (
        question_contract
        if isinstance(question_contract, dict)
        else (
            embedded_contract
            if isinstance(embedded_contract, dict)
            else None
        )
    )
    contract_question_type = (
        _question_type_from_contract(
            effective_contract
        )
    )

    if contract_question_type:
        question_type = contract_question_type
        canonical_owner = (
            "question_contract.question_type.id"
        )
        contract_block = (
            effective_contract.get("question_type")
            if isinstance(effective_contract, dict)
            else {}
        )
        if not isinstance(contract_block, dict):
            contract_block = {}
        canonical_source = str(
            contract_block.get("source")
            or "question_contract"
        ).strip()
        canonical_confidence = str(
            contract_block.get("confidence")
            or ""
        ).strip()
        matched_rules = list(
            contract_block.get("matched_rules")
            or []
        )

    elif normalized_question_text:
        canonical_evaluation = (
            detect_canonical_question_type(
                normalized_question_text
            )
        )
        question_type = normalize_question_type(
            canonical_evaluation.get(
                "question_type"
            )
        )
        canonical_owner = str(
            canonical_evaluation.get(
                "canonical_owner"
            )
            or (
                "question_type_router."
                "detect_question_type"
            )
        )
        canonical_source = str(
            canonical_evaluation.get("source")
            or "deterministic_rule"
        )
        canonical_confidence = str(
            canonical_evaluation.get(
                "confidence"
            )
            or ""
        )
        matched_rules = list(
            canonical_evaluation.get(
                "matched_rules"
            )
            or []
        )

    elif legacy_or_existing:
        question_type = normalize_question_type(
            legacy_or_existing
        )
        canonical_owner = (
            "legacy_question_type_fallback"
        )
        canonical_source = "legacy_fallback"
        canonical_confidence = ""
        matched_rules = []

    else:
        question_type = normalize_question_type(
            None
        )
        canonical_owner = "taxonomy_fallback"
        canonical_source = "fallback"
        canonical_confidence = ""
        matched_rules = []

    legacy_question_type = (
        str(legacy_or_existing).strip().upper()
        if legacy_or_existing
        else None
    )

    profile = get_question_type_profile(
        question_type
    )

    grade["question_type"] = question_type
    grade["question_type_name"] = profile.get(
        "name_ko"
    )
    grade["question_type_v2"] = {
        "question_type": question_type,
        "legacy_question_type": (
            legacy_question_type
        ),
        "name_ko": profile.get("name_ko"),
        "intent": profile.get("intent"),
        "c_fact_focus": profile.get(
            "c_fact_focus",
            [],
        ),
        "d_field_judgement_focus": profile.get(
            "d_field_judgement_focus",
            [],
        ),
        "sub_criteria": profile.get(
            "sub_criteria",
            [],
        ),
        "canonical_owner": canonical_owner,
        "canonical_source": canonical_source,
        "canonical_confidence": (
            canonical_confidence
        ),
        "matched_rules": matched_rules,
        "note": (
            "question_type은 별도 점수체계가 아니라 "
            "C항목 Fact 설명과 D항목 현장 판단을 "
            "보완하는 lens입니다."
        ),
    }

    return grade
