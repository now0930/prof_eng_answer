from __future__ import annotations

import copy

import question_type_coverage_adapter as adapter
import verified_defect_reconciliation as owner


def _base_grade() -> dict:
    return {
        "score": 14.5,
        "total_score": 14.5,
        "final_score": 14.5,
        "improvement_points": [
            "기존 개선점",
        ],
        "strategy_warnings": [
            "기존 경고",
        ],
        "question_type_coverage": {
            "question_type": (
                "PRINCIPLE_INTERPRETATION"
            ),
            "name_ko": "원리·해석형",
            "explicit_requirement_coverage": {
                "requirements": [
                    {
                        "requirement": "원리",
                        "status": "present",
                        "evidence": "설명",
                    },
                    {
                        "requirement": "해석",
                        "status": "incorrect",
                        "evidence": "오류",
                    },
                    {
                        "requirement": "현장 판단",
                        "status": "incorrect",
                        "evidence": "오류",
                    },
                ],
            },
            "coverage_counts": {
                "present": 1,
                "incorrect": 2,
                "total": 3,
            },
        },
        "question_type_coverage_summary": {
            "sub_criteria_total": 0,
            "sub_criteria_present": 0,
            "sub_criteria_incorrect": 0,
        },
        "parsed": {
            "question_type_coverage": {
                "question_type": (
                    "PRINCIPLE_INTERPRETATION"
                ),
                "coverage_counts": {
                    "present": 1,
                    "incorrect": 2,
                    "total": 3,
                },
            },
        },
        "verified_defect_reconciliation": {
            "marker": (
                "VERIFIED_DEFECT_RECONCILIATION_V1"
            ),
            "score_effect": "none",
        },
    }


def test_stage25g5e2_stable_unique_preserves_order():
    rows = [
        "a",
        "b",
        "a",
        {"id": 1},
        "c",
        "b",
    ]
    result = (
        owner
        ._stage25g5e2_stable_unique_strings(
            rows
        )
    )
    assert result == [
        "a",
        "b",
        {"id": 1},
        "c",
    ]


def test_stage25g5e2_nonlist_and_nondict_passthrough():
    assert (
        owner
        ._stage25g5e2_stable_unique_strings(
            "not-a-list"
        )
        == "not-a-list"
    )
    assert (
        owner
        ._stage25g5e2_finalize_feedback_fixed_point(
            "not-a-dict"
        )
        == "not-a-dict"
    )


def test_stage25g5e2_finalizer_reaches_fixed_point_once():
    warning = (
        "question_type 세부 요구 충족도가 낮습니다"
        "(원리·해석형). 단답식 키워드보다 C항목 "
        "Fact 설명과 D항목 현장 판단을 보강해야 합니다."
    )

    original_previous_step = (
        owner
        ._reconcile_verified_defects_with_coverage_identity
    )
    original_attach = (
        adapter.attach_question_type_coverage_feedback
    )

    def fake_previous_step(grade):
        return copy.deepcopy(grade)

    def fake_attach(grade):
        output = copy.deepcopy(grade)
        points = output.setdefault(
            "improvement_points",
            [],
        )
        points.append(warning)
        warnings = output.setdefault(
            "strategy_warnings",
            [],
        )
        warnings.append(warning)
        output[
            "question_type_coverage_summary"
        ] = {
            "sub_criteria_total": 0,
            "sub_criteria_present": 0,
            "sub_criteria_incorrect": 0,
        }
        return output

    owner._reconcile_verified_defects_with_coverage_identity = (
        fake_previous_step
    )
    adapter.attach_question_type_coverage_feedback = (
        fake_attach
    )

    try:
        grade = _base_grade()
        once = (
            owner
            .reconcile_verified_defects_with_coverage(
                grade
            )
        )
        twice = (
            owner
            .reconcile_verified_defects_with_coverage(
                once
            )
        )
    finally:
        owner._reconcile_verified_defects_with_coverage_identity = (
            original_previous_step
        )
        adapter.attach_question_type_coverage_feedback = (
            original_attach
        )

    assert once == twice
    assert once["improvement_points"] == [
        "기존 개선점",
        warning,
    ]
    assert once["strategy_warnings"] == [
        "기존 경고",
        warning,
    ]
    assert (
        once["parsed"]["question_type_coverage"]
        == once["question_type_coverage"]
    )
    summary = once[
        "question_type_coverage_summary"
    ]
    assert summary["sub_criteria_total"] == 3
    assert summary["sub_criteria_present"] == 1
    assert summary["sub_criteria_incorrect"] == 2
    assert once["final_score"] == 14.5
