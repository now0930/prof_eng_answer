from __future__ import annotations

import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO
    / "calibration"
    / "sil_target_operations_overgrading_regression.json"
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

REQUIRED_FINDINGS = {
    "target_pfd_frequency_multiplication_dimension_error",
    "demand_mode_confused_with_fault_detection",
    "pst_claimed_to_reduce_mttr",
    "certificate_interval_treated_as_minimum_test_interval",
}


def load_fixture() -> dict[str, object]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_fixture_identity_and_scope() -> None:
    fixture = load_fixture()
    assert fixture["schema_version"] == (
        "sil_target_operations_overgrading_regression.v1"
    )
    assert fixture["regression_id"] == (
        "SIL-TARGET-OPERATIONS-OVERGRADING-01"
    )
    assert fixture["source_session_id"] == "20260831_131321_5960502198"
    assert fixture["question_type"] == "IMPLEMENTATION_EVALUATION"
    assert fixture["question"].startswith("SIL 결정 방법")


def test_original_and_corrected_pair_freezes_relation_direction() -> None:
    fixture = load_fixture()
    original = str(fixture["original_answer"])
    corrected = str(fixture["corrected_answer"])

    assert "PFD_avg <= F_H,max × F_D" in original
    assert "고장 즉시 고장을 확인" in original
    assert "PST 등 자동화된 점검 프로그램으로 MTTR을 축소" in original
    assert "인증 수준보다 짧게 점검할 이유는 없다" in original

    assert "PFD_avg <= F_target / (F_D × product(P_i))" in corrected
    assert "고장 검출시점이 아니라 요구빈도와 운전모드" in corrected
    assert "수리시간 MTTR을 자동으로 줄이지 않으며" in corrected
    assert "제품 인증주기가 아니라 실제 SIF 계산" in corrected


def test_original_contract_has_exact_eight_demand_states() -> None:
    fixture = load_fixture()
    original = fixture["expected"]["original"]
    statuses = original["demand_status"]

    assert list(statuses) == EXPECTED_AXES
    assert len(statuses) == 8
    assert sum(value == "incorrect" for value in statuses.values()) == 3
    assert sum(value == "partial" for value in statuses.values()) == 4
    assert sum(value == "missing" for value in statuses.values()) == 1
    assert "present" not in statuses.values()


def test_original_contract_blocks_overgrading() -> None:
    fixture = load_fixture()
    original = fixture["expected"]["original"]

    assert set(original["required_finding_ids"]) == REQUIRED_FINDINGS
    assert original["requirements_full_credit_allowed"] is False
    assert original["strong_verdict_allowed"] is False
    assert original["passing_score_allowed"] is False
    assert original["maximum_total_score"] == 14.5
    assert original["confidence_ceiling"] == "medium"
    assert original["manual_review_required_when_question_boundary_unknown"] is True

    forbidden = "\n".join(original["forbidden_feedback_elements"])
    assert "100%" in forbidden
    assert "strong" in forbidden
    assert "정확" in forbidden


def test_topic_ownership_and_pairwise_monotonicity_contract() -> None:
    fixture = load_fixture()
    topics = fixture["expected_topics"]
    corrected = fixture["expected"]["corrected"]

    assert topics["primary"] == (
        "sil_target_determination_risk_reduction_and_lifecycle"
    )
    assert (
        "final_control_element_sil_sis_esd_valve_partial_stroke_test"
        in topics["forbidden_primary"]
    )
    assert len(topics["supporting"]) == 4
    assert set(corrected["forbidden_finding_ids"]) == REQUIRED_FINDINGS
    assert corrected["minimum_score_delta_over_original"] == 2.0
    assert corrected["must_rank_above_original"] is True


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    assert len(tests) == 5
    for name, test in tests:
        test()
        print(f"PASS {name}")
    print("SIL_TARGET_OPERATIONS_CONTRACT_RESULT=PASS")
    print(f"SIL_TARGET_OPERATIONS_CONTRACT_TEST_COUNT={len(tests)}")


if __name__ == "__main__":
    main()
