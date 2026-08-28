#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from difficulty_output_adapter import (
    attach_difficulty_strategy_to_grade,
)
from explicit_requirement_cap import (
    _walk_find_question_type_coverage
    as cap_walk,
    evaluate_explicit_requirement_hard_cap,
)
from question_type_coverage_adapter import (
    _walk_find_question_type_coverage
    as adapter_walk,
    attach_question_type_coverage_feedback,
)
from question_type_coverage_score_adjuster import (
    _walk_find_question_type_coverage
    as adjustment_walk,
    evaluate_question_type_coverage_score_adjustment,
)
from question_type_output_adapter import (
    attach_question_type_v2_to_grade,
)
from question_type_router import (
    detect_question_type,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, "
            f"actual={actual!r}"
        )


def contract(question_type):
    return {
        "version": "question_contract_v1",
        "lens": question_type,
        "question_type": {
            "id": question_type,
            "confidence": "high",
            "status": "locked",
            "locked": True,
            "source": "deterministic_rule",
            "matched_rules": [
                "focused_regression"
            ],
        },
        "contract_hash": "focused-regression",
    }


def unknown_coverage(question_type):
    return {
        "question_type": question_type,
        "name_ko": question_type,
        "overall_coverage": "unknown",
        "coverage_source": (
            "question_only_type_owner_mismatch_guard"
        ),
        "sub_criteria_coverage": [],
        "missing_sub_criteria": [],
        "c_fact_focus_coverage": {
            "covered": [],
            "missing": [],
        },
        "d_field_judgement_focus_coverage": {
            "covered": [],
            "missing": [],
        },
    }


def semantic_missing_coverage(question_type):
    return {
        "question_type": question_type,
        "name_ko": question_type,
        "overall_coverage": "poor",
        "coverage_source": "semantic_grader",
        "sub_criteria_coverage": [
            {
                "criterion": "required axis",
                "status": "missing",
            }
        ],
        "explicit_requirement_coverage": {
            "source": "question_text",
            "extraction_confidence": "high",
            "requirements": [
                {
                    "requirement": "required axis",
                    "status": "missing",
                    "is_core": True,
                    "evidence": "",
                }
            ],
        },
        "c_fact_focus_coverage": {
            "covered": [],
            "missing": ["required axis"],
        },
        "d_field_judgement_focus_coverage": {
            "covered": [],
            "missing": [],
        },
    }


def test_router_delegation_matrix():
    questions = [
        "두 방식의 차이점과 선정 기준을 설명하시오.",
        "고장 발생 원인과 대책을 설명하시오.",
        "구현 절차와 평가 방법을 설명하시오.",
        "PID 제어의 동작 원리를 설명하시오.",
    ]

    for question in questions:
        expected = detect_question_type(
            question
        )["question_type"]
        grade = {
            "total_score": 13.52,
            "final_total_score": 13.52,
        }
        result = attach_question_type_v2_to_grade(
            grade,
            question_text=question,
        )
        assert_equal(
            result["question_type"],
            expected,
            f"router delegation: {question}",
        )
        assert_equal(
            result["question_type_v2"][
                "canonical_owner"
            ],
            "question_type_router.detect_question_type",
            "router owner",
        )
        assert_equal(
            result["total_score"],
            13.52,
            "router delegation score invariant",
        )


def test_contract_precedes_redetection_and_legacy():
    diagnosis_question = (
        "고장 발생 원인과 대책을 설명하시오."
    )
    router_type = detect_question_type(
        diagnosis_question
    )["question_type"]
    assert_equal(
        router_type,
        "DIAGNOSIS_ACTION",
        "regression precondition",
    )

    grade = {
        "question_type": "DIAGNOSIS_ACTION",
        "total_score": 13.52,
        "final_total_score": 13.52,
    }
    result = attach_question_type_v2_to_grade(
        grade,
        question_text=diagnosis_question,
        question_contract=contract(
            "COMPARE_SELECTION"
        ),
    )

    assert_equal(
        result["question_type"],
        "COMPARE_SELECTION",
        "contract precedence",
    )
    assert_equal(
        result["question_type_v2"][
            "question_type"
        ],
        "COMPARE_SELECTION",
        "v2 contract persistence",
    )
    assert_equal(
        result["question_type_v2"][
            "legacy_question_type"
        ],
        "DIAGNOSIS_ACTION",
        "legacy provenance",
    )
    assert_equal(
        result["question_type_v2"][
            "canonical_owner"
        ],
        "question_contract.question_type.id",
        "contract owner",
    )
    assert_equal(
        result["total_score"],
        13.52,
        "contract persistence score invariant",
    )


def test_difficulty_adapter_contract_handoff():
    result = attach_difficulty_strategy_to_grade(
        {
            "question_type": "DIAGNOSIS_ACTION",
            "total_score": 13.52,
            "final_total_score": 13.52,
            "breakdown": [],
        },
        question_text=(
            "고장 발생 원인과 대책을 설명하시오."
        ),
        question_contract=contract(
            "COMPARE_SELECTION"
        ),
    )
    assert_equal(
        result["question_type"],
        "COMPARE_SELECTION",
        "difficulty adapter contract handoff",
    )
    assert_equal(
        result["question_type_v2"][
            "canonical_owner"
        ],
        "question_contract.question_type.id",
        "final pipeline canonical owner preservation",
    )
    assert_equal(
        result["question_type_v2"][
            "canonical_source"
        ],
        "deterministic_rule",
        "final pipeline canonical source preservation",
    )
    assert_equal(
        result["question_type_v2"][
            "canonical_confidence"
        ],
        "high",
        "final pipeline canonical confidence preservation",
    )
    assert_equal(
        result["question_type_v2"][
            "legacy_question_type"
        ],
        "DIAGNOSIS_ACTION",
        "final pipeline legacy provenance preservation",
    )
    assert_equal(
        result["question_type_v2"][
            "matched_rules"
        ],
        ["focused_regression"],
        "final pipeline matched rules preservation",
    )
    assert_equal(
        result["total_score"],
        13.52,
        "difficulty adapter score invariant",
    )


def test_reference_only_coverage_exclusion():
    root = unknown_coverage(
        "COMPARE_SELECTION"
    )
    legacy = semantic_missing_coverage(
        "DIAGNOSIS_ACTION"
    )
    payload = {
        "legacy_grade_reference": {
            "question_type_coverage": legacy,
        },
        "model_answer_reference": {
            "question_type_coverage": legacy,
        },
        "question_type_coverage": root,
    }

    for name, walker in [
        ("adapter", adapter_walk),
        ("adjustment", adjustment_walk),
        ("cap", cap_walk),
    ]:
        selected = walker(deepcopy(payload))
        assert_equal(
            selected["question_type"],
            "COMPARE_SELECTION",
            f"{name} root precedence",
        )

        reference_only = walker(
            {
                "legacy_grade_reference": {
                    "question_type_coverage": legacy,
                },
                "model_answer_reference": {
                    "question_type_coverage": legacy,
                },
            }
        )
        assert_equal(
            reference_only,
            None,
            f"{name} reference exclusion",
        )


def test_score_and_cap_use_active_root_only():
    root = unknown_coverage(
        "COMPARE_SELECTION"
    )
    legacy = semantic_missing_coverage(
        "DIAGNOSIS_ACTION"
    )
    grade = {
        "total_score": 13.52,
        "final_total_score": 13.52,
        "question_type_coverage": root,
        "legacy_grade_reference": {
            "question_type_coverage": legacy,
        },
    }

    adjustment = (
        evaluate_question_type_coverage_score_adjustment(
            deepcopy(grade)
        )
    )
    assert_equal(
        adjustment["question_type"],
        "COMPARE_SELECTION",
        "adjustment active root type",
    )
    assert_equal(
        adjustment["applied"],
        False,
        "adjustment warn invariant",
    )
    assert_equal(
        adjustment["adjusted_score"],
        13.52,
        "adjustment score invariant",
    )

    cap = evaluate_explicit_requirement_hard_cap(
        deepcopy(grade)
    )
    assert_equal(
        cap["triggered"],
        False,
        "legacy missing requirement excluded",
    )
    assert_equal(
        cap["adjusted_score"],
        13.52,
        "cap score invariant",
    )


def test_mismatch_guard_reconciles_to_root():
    grade = {
        "question_type": "COMPARE_SELECTION",
        "total_score": 13.52,
        "final_total_score": 13.52,
        "question_type_coverage": (
            semantic_missing_coverage(
                "DIAGNOSIS_ACTION"
            )
        ),
    }
    result = (
        attach_question_type_coverage_feedback(
            grade
        )
    )

    assert_equal(
        result["question_type"],
        "COMPARE_SELECTION",
        "mismatch root owner",
    )
    assert_equal(
        result["question_type_coverage"][
            "question_type"
        ],
        "COMPARE_SELECTION",
        "mismatch coverage reconciliation",
    )
    assert_equal(
        result["question_type_coverage"][
            "overall_coverage"
        ],
        "unknown",
        "mismatch type-specific invalidation",
    )
    assert_equal(
        result["question_type_coverage"][
            "coverage_source"
        ],
        "question_only_type_owner_mismatch_guard",
        "mismatch guard source",
    )
    assert_equal(
        result["total_score"],
        13.52,
        "mismatch score invariant",
    )


def test_runtime_callsite_passes_contract():
    source = Path(
        "grading_agents.py"
    ).read_text(encoding="utf-8")
    required = (
        'question_contract=locals().get(\n'
        '                "question_contract"\n'
        "            ),"
    )
    if required not in source:
        raise AssertionError(
            "grading_agents does not pass "
            "Question Contract to output adapter"
        )


def main():
    tests = [
        test_router_delegation_matrix,
        test_contract_precedes_redetection_and_legacy,
        test_difficulty_adapter_contract_handoff,
        test_reference_only_coverage_exclusion,
        test_score_and_cap_use_active_root_only,
        test_mismatch_guard_reconciles_to_root,
        test_runtime_callsite_passes_contract,
    ]

    for test in tests:
        test()

    print(
        "RESULT=PASS\n"
        "TESTS=7_OF_7_PASS\n"
        "CONTRACT_PRECEDENCE=PASS\n"
        "ROUTER_DELEGATION=PASS\n"
        "LEGACY_REFERENCE_EXCLUSION=PASS\n"
        "SCORE_INVARIANCE=PASS"
    )


if __name__ == "__main__":
    main()
