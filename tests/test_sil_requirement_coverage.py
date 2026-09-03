from __future__ import annotations

import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from logic_check_evaluator import evaluate_logic_checks
import gemini_grader
from question_demand_contract import build_question_demand_contract
from question_type_coverage_adapter import (
    attach_question_type_coverage_feedback,
)
from sil_relation_integrity import SIL_TARGET_TOPIC_ID


FIXTURE = REPO / "calibration" / (
    "sil_target_operations_overgrading_regression.json"
)
EXPECTED_AXES = [
    "system_scope_and_sil_role",
    "risk_scenario_and_tolerable_target",
    "existing_ipl_and_independence",
    "required_rrf_and_target_sil",
    "demand_mode_metric_selection",
    "quantitative_verification_dimension",
    "proof_test_diagnostics_reliability",
    "operations_moc_security_ai_lifecycle",
]


def fixture() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def coverage_rows(
    statuses: dict[str, str],
) -> list[dict[str, object]]:
    return [
        {
            "requirement_id": requirement_id,
            "requirement": requirement_id,
            "status": statuses[requirement_id],
            "mentioned": statuses[requirement_id] != "missing",
            "evidence": (
                "fixture evidence"
                if statuses[requirement_id] != "missing"
                else ""
            ),
            "is_core": True,
        }
        for requirement_id in EXPECTED_AXES
    ]


def test_issue_question_owns_exact_eight_demand_axes() -> None:
    data = fixture()
    contract = build_question_demand_contract(data["question"])

    assert contract["topic_pack_demand_axes_applied"] is True
    assert contract["topic_pack_demand_axes"]["topic_id"] == (
        SIL_TARGET_TOPIC_ID
    )
    assert contract["primary_lens"] == "IMPLEMENTATION_EVALUATION"
    assert [
        row["requirement_id"]
        for row in contract["requirements"]
    ] == EXPECTED_AXES


def test_neighbor_hazop_question_keeps_neighbor_demand_axes() -> None:
    contract = build_question_demand_contract(
        "화학 플랜트 반응기 과압력 위험에 대해 기존 보호장치를 "
        "평가하고 SIS 아키텍처와 목표 SIL을 설명하시오."
    )

    assert contract["topic_pack_demand_axes"]["topic_id"] == (
        "hazop_lopa_ipl_risk_reduction_sil_target_allocation"
    )
    assert contract["requirements"][0]["requirement_id"] == (
        "scenario_definition_and_cause"
    )


def test_prompt_separates_mentioned_from_correct_status() -> None:
    data = fixture()
    prompt = gemini_grader.build_gemini_grading_prompt(
        question_text=data["question"],
        answer_text=data["original_answer"],
        scoring_model={},
        subject_rubric={},
        rater_profile={},
        volume={},
        fact_eval={},
        connection_eval={},
    )

    assert "mentioned는 답안이 해당 요구를 실제로 다뤘는지만" in prompt
    assert "present는 단순 언급이 아니라" in prompt
    assert "mentioned=true, status=wrong" in prompt
    assert "mention coverage와 correctness coverage를 혼동하지" in prompt
    for requirement_id in EXPECTED_AXES:
        assert f'"requirement_id": "{requirement_id}"' in prompt


def test_projection_rejects_mention_status_contradiction() -> None:
    data = fixture()
    contract = build_question_demand_contract(data["question"])
    statuses = {axis: "present" for axis in EXPECTED_AXES}
    rows = coverage_rows(statuses)
    rows[0]["status"] = "missing"
    rows[0]["mentioned"] = True
    result = {
        "parsed": {
            "question_type_coverage": {
                "explicit_requirement_coverage": {
                    "requirements": rows,
                }
            }
        }
    }

    assert not gemini_grader._stage35e2_projection_matches_contract(
        result,
        contract,
    )


def test_fixture_statuses_separate_mention_from_correctness() -> None:
    data = fixture()
    statuses = data["expected"]["original"]["demand_status"]
    grade = {
        "question_type_coverage": {
            "question_type": "IMPLEMENTATION_EVALUATION",
            "overall_coverage": "strong",
            "explicit_requirement_coverage": {
                "requirements": coverage_rows(statuses),
            },
        }
    }

    result = attach_question_type_coverage_feedback(grade)
    summary = result["question_type_coverage_summary"]

    assert summary["sub_criteria_total"] == 8
    assert summary["sub_criteria_partial"] == 4
    assert summary["sub_criteria_wrong"] == 3
    assert summary["sub_criteria_missing"] == 1
    assert summary["mention_coverage_percent"] == 87.5
    assert summary["correctness_coverage_percent"] == 25.0
    assert summary["full_correct_coverage"] is False


def test_fatal_formula_overrides_false_present_by_exact_demand_ref() -> None:
    data = fixture()
    statuses = {axis: "present" for axis in EXPECTED_AXES}
    logic = evaluate_logic_checks(
        data["original_answer"],
        {"logic_check_topic_id": SIL_TARGET_TOPIC_ID},
    )
    grade = {
        "logic_check_evaluation": logic,
        "question_type_coverage": {
            "question_type": "IMPLEMENTATION_EVALUATION",
            "overall_coverage": "strong",
            "explicit_requirement_coverage": {
                "requirements": coverage_rows(statuses),
            },
        },
    }

    result = attach_question_type_coverage_feedback(grade)
    coverage = result["question_type_coverage"]
    rows = coverage["explicit_requirement_coverage"]["requirements"]
    by_id = {row["requirement_id"]: row for row in rows}

    for requirement_id in (
        "required_rrf_and_target_sil",
        "demand_mode_metric_selection",
        "quantitative_verification_dimension",
        "proof_test_diagnostics_reliability",
        "operations_moc_security_ai_lifecycle",
    ):
        row = by_id[requirement_id]
        assert row["status"] == "wrong"
        assert row["demand_state"] == "WRONG"
        assert row["mentioned"] is True
        assert row["fatal_logic_reclassification"]["finding_ids"]
        assert (
            f"demand_ref:{requirement_id}"
            in row["fatal_logic_reclassification"]["matched_tokens"]
        )

    summary = result["question_type_coverage_summary"]
    assert summary["mention_coverage_percent"] == 100.0
    assert summary["correctness_coverage_percent"] == 37.5
    assert summary["full_correct_coverage"] is False
    assert coverage["overall_coverage"] == "weak"
    assert coverage["full_credit_allowed"] is False
    assert coverage["coverage_status_semantics"] == {
        "version": "mention_correctness_separation_v1",
        "mention_is_correctness": False,
        "present_requires_correctness": True,
        "wrong_can_be_mentioned": True,
    }


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    for name, test in tests:
        test()
        print(f"PASS: {name}")
    print(f"PASS: {len(tests)}/{len(tests)} SIL coverage checks")


if __name__ == "__main__":
    main()
