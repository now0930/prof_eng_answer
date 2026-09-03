from __future__ import annotations

import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from logic_check_evaluator import evaluate_logic_checks
from sil_relation_integrity import (
    SIL_RELATION_INTEGRITY_MARKER,
    SIL_TARGET_TOPIC_ID,
    evaluate_sil_relation_integrity,
)
from verdict_consistency import (
    enforce_final_decision_consistency,
)


FIXTURE = REPO / "calibration" / (
    "sil_target_operations_overgrading_regression.json"
)


def fixture() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def rule_ids(result: dict[str, object]) -> set[str]:
    return {
        str(row.get("rule_id") or "")
        for row in result.get("findings", [])
        if isinstance(row, dict)
    }


def test_original_regression_detects_frequency_product() -> None:
    result = evaluate_sil_relation_integrity(
        fixture()["original_answer"]
    )

    assert result["status"] == "fatal"
    assert result["fatal_error_detected"] is True
    assert rule_ids(result) == {
        "fatal_target_pfd_frequency_product"
    }
    finding = result["findings"][0]
    assert finding["error_class"] == (
        "DIMENSION_AND_RELATION_DIRECTION"
    )
    assert finding["evidence_trust_tier"] == "DETERMINISTIC"
    assert finding["recommended_ceiling"] == 14.5


def test_corrected_regression_is_valid() -> None:
    result = evaluate_sil_relation_integrity(
        fixture()["corrected_answer"]
    )

    assert result["status"] == "valid"
    assert result["fatal_error_detected"] is False
    assert result["findings"] == []
    recognized = {
        row["relation_id"]
        for row in result["recognized_correct_relations"]
    }
    assert "target_pfd_tolerable_over_residual" in recognized


def test_ocr_and_latex_frequency_products_are_equivalent() -> None:
    variants = (
        "PFD_avg <= F_H,max * F_D",
        "PFD_avg ≤ F_H,max × F_D",
        r"PFD_{avg} \leq F_{target} \times F_D",
    )
    for answer in variants:
        result = evaluate_sil_relation_integrity(answer)
        assert rule_ids(result) == {
            "fatal_target_pfd_frequency_product"
        }, (answer, result)


def test_relation_direction_errors_are_distinct() -> None:
    cases = {
        "PFDavg <= F_residual/F_target": (
            "fatal_target_pfd_inverse_ratio"
        ),
        "RRF_required = F_target/F_residual": (
            "fatal_required_rrf_inverse_ratio"
        ),
        "PFDavg >= F_target/F_residual": (
            "fatal_target_pfd_wrong_inequality"
        ),
    }
    for answer, expected in cases.items():
        result = evaluate_sil_relation_integrity(answer)
        assert rule_ids(result) == {expected}, (answer, result)


def test_correct_risk_event_equation_is_not_pfd_product_error() -> None:
    answer = (
        "F_H = F_D * product(P_i) * PFD_avg이고, 따라서 "
        "PFD_avg <= F_target/(F_D * product(P_i))이다."
    )
    result = evaluate_sil_relation_integrity(answer)

    assert result["status"] == "valid"
    assert result["findings"] == []


def test_explicit_wrong_example_is_suppressed() -> None:
    answer = (
        "잘못된 식: PFDavg <= F_target * F_D. "
        "올바른 식은 PFDavg <= F_target/F_residual이다."
    )
    result = evaluate_sil_relation_integrity(answer)

    assert result["status"] == "valid"
    assert result["findings"] == []
    suppressed = result["corrective_examples_suppressed"]
    assert len(suppressed) == 1
    assert suppressed[0]["suppressed_rule_ids"] == [
        "fatal_target_pfd_frequency_product"
    ]


def test_missing_formula_has_no_penalty() -> None:
    result = evaluate_sil_relation_integrity(
        "위험분석 후 목표 SIL을 정하고 운전 중 재검증한다."
    )

    assert result["status"] == "not_evaluated"
    assert result["findings"] == []
    assert result["score_policy"]["missing_formula_penalty"] is False


def test_logic_check_integration_detects_original_and_accepts_corrected() -> None:
    data = fixture()
    grade = {"logic_check_topic_id": SIL_TARGET_TOPIC_ID}

    original = evaluate_logic_checks(data["original_answer"], grade)
    corrected = evaluate_logic_checks(data["corrected_answer"], grade)

    assert original["topic_id"] == SIL_TARGET_TOPIC_ID
    assert original["fatal_error_detected"] is True
    assert original["mode"] == "fatal"
    assert original["score_policy"]["recommended_ceiling"] == 14.5
    assert rule_ids(original) == {
        "fatal_demand_mode_by_fault_detection",
        "fatal_pst_replaces_full_test_or_reduces_mttr",
        "fatal_certificate_interval_as_operating_minimum",
        "fatal_target_pfd_frequency_product"
    }
    assert original["sil_relation_integrity_evaluation"]["marker"] == (
        SIL_RELATION_INTEGRITY_MARKER
    )

    assert corrected["fatal_error_detected"] is False
    assert corrected["mode"] == "pass"
    assert corrected["sil_relation_integrity_evaluation"]["status"] == (
        "valid"
    )


def test_fatal_relation_reaches_final_decision_invariants() -> None:
    data = fixture()
    logic = evaluate_logic_checks(
        data["original_answer"],
        {"logic_check_topic_id": SIL_TARGET_TOPIC_ID},
    )
    result = enforce_final_decision_consistency(
        {
            "logic_check_evaluation": logic,
            "verdict": "strong",
            "official_pass_met": True,
            "practical_target_met": True,
            "high_score_met": True,
            "question_type_coverage": {
                "overall_coverage": "strong",
            },
        }
    )

    assert result["strong_verdict_allowed"] is False
    assert result["requirements_full_credit_allowed"] is False
    assert result["passing_score_allowed"] is False
    assert result["official_pass_met"] is False
    assert result["practical_target_met"] is False
    assert result["high_score_met"] is False
    assert result["verdict"] == "검증된 핵심 기술 오류 보완 필요"
    assert result["question_type_coverage"]["full_credit_allowed"] is False
    consistency = result["final_decision_consistency"]
    assert consistency["logic_fatal"] is True
    assert consistency["fatal_error"] is True
    assert consistency["numeric_score_changed"] is False


def test_neighbor_topic_does_not_run_sil_relation_checker() -> None:
    result = evaluate_logic_checks(
        "PFDavg <= F_target * F_D",
        {
            "logic_check_topic_id": (
                "functional_safety_reliability_modeling_fta_markov_"
                "rbd_ccf_pfd_pfh"
            )
        },
    )

    evaluation = result["sil_relation_integrity_evaluation"]
    assert evaluation["applicable"] is False
    assert evaluation["status"] == "not_applicable"


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    for name, test in tests:
        test()
        print(f"PASS: {name}")
    print(f"PASS: {len(tests)}/{len(tests)} SIL relation checks")


if __name__ == "__main__":
    main()
