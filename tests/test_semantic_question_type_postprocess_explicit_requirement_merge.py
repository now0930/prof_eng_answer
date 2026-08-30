from __future__ import annotations

import copy

from semantic_question_type_postprocess import (
    ensure_question_type_coverage,
)


def _coverage() -> dict[str, object]:
    return {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "sub_criteria_coverage": [
            {
                "criterion": "background_need",
                "status": "partial",
            }
        ],
        "overall_coverage": "partial",
    }


def _explicit(
    label: str = "source-owned-demand",
) -> dict[str, object]:
    return {
        "requirements": [
            {
                "requirement_id": label,
                "requirement": label,
                "status": "partial",
                "weight": 1.0,
            }
        ],
        "weighted_coverage_ratio": 0.5,
    }


def test_parsed_sibling_is_promoted() -> None:
    payload = {
        "parsed": {
            "question_type_coverage": _coverage(),
            "explicit_requirement_coverage": _explicit(),
        }
    }

    result = ensure_question_type_coverage(payload)
    merged = result["question_type_coverage"]

    assert merged["explicit_requirement_coverage"] == _explicit()
    assert (
        result["parsed"]["question_type_coverage"]
        is result["question_type_coverage"]
    )
    assert len(merged["sub_criteria_coverage"]) == 1


def test_root_sibling_is_promoted() -> None:
    payload = {
        "question_type_coverage": _coverage(),
        "explicit_requirement_coverage": _explicit(),
    }

    result = ensure_question_type_coverage(payload)

    assert (
        result["question_type_coverage"][
            "explicit_requirement_coverage"
        ]
        == _explicit()
    )


def test_valid_nested_value_has_precedence() -> None:
    nested = _explicit("nested")
    coverage = _coverage()
    coverage["explicit_requirement_coverage"] = nested
    payload = {
        "parsed": {
            "question_type_coverage": coverage,
            "explicit_requirement_coverage": _explicit(
                "sibling"
            ),
        }
    }

    result = ensure_question_type_coverage(payload)

    assert (
        result["question_type_coverage"][
            "explicit_requirement_coverage"
        ]["requirements"][0]["requirement_id"]
        == "nested"
    )


def test_invalid_nested_uses_valid_sibling() -> None:
    coverage = _coverage()
    coverage["explicit_requirement_coverage"] = {
        "requirements": "invalid"
    }
    payload = {
        "parsed": {
            "question_type_coverage": coverage,
            "explicit_requirement_coverage": _explicit(
                "valid-sibling"
            ),
        }
    }

    result = ensure_question_type_coverage(payload)

    assert (
        result["question_type_coverage"][
            "explicit_requirement_coverage"
        ]["requirements"][0]["requirement_id"]
        == "valid-sibling"
    )


def test_invalid_sibling_is_not_fabricated() -> None:
    payload = {
        "parsed": {
            "question_type_coverage": _coverage(),
            "explicit_requirement_coverage": {
                "requirements": "invalid"
            },
        }
    }

    result = ensure_question_type_coverage(payload)

    assert (
        "explicit_requirement_coverage"
        not in result["question_type_coverage"]
    )


def test_promoted_value_is_deep_copied() -> None:
    sibling = _explicit("before")
    payload = {
        "parsed": {
            "question_type_coverage": _coverage(),
            "explicit_requirement_coverage": sibling,
        }
    }

    result = ensure_question_type_coverage(payload)
    promoted = result["question_type_coverage"][
        "explicit_requirement_coverage"
    ]

    assert promoted is not sibling
    assert promoted["requirements"] is not sibling["requirements"]

    sibling["requirements"][0]["requirement_id"] = "after"
    assert (
        promoted["requirements"][0]["requirement_id"]
        == "before"
    )


def test_operation_is_idempotent() -> None:
    payload = {
        "parsed": {
            "question_type_coverage": _coverage(),
            "explicit_requirement_coverage": _explicit(),
        }
    }

    once = ensure_question_type_coverage(
        copy.deepcopy(payload)
    )
    twice = ensure_question_type_coverage(
        copy.deepcopy(once)
    )

    assert once == twice


def test_fallback_preserves_source_owned_explicit_demands() -> None:
    payload = {
        "parsed": {
            "explicit_requirement_coverage": _explicit(
                "fallback-demand"
            )
        }
    }

    result = ensure_question_type_coverage(
        payload,
        existing_question_type=(
            "PRINCIPLE_INTERPRETATION"
        ),
    )

    assert (
        result["question_type_coverage"][
            "explicit_requirement_coverage"
        ]["requirements"][0]["requirement_id"]
        == "fallback-demand"
    )
    assert (
        result["question_type_coverage"][
            "coverage_source"
        ]
        == "fallback_missing_semantic_field"
    )
