"""Regression for the reviewed source-owned requirements, not a new score gate."""

import json
from pathlib import Path

import pytest

from grading.evidence.fact_anchor_evidence_adapter import evaluate_fact_anchor_requirements
from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring

ROOT = Path(__file__).resolve().parents[1]
FINAL = "final_control_element_sil_sis_esd_valve_partial_stroke_test"
SPEED = "speed_rotation_measurement_encoder_proximity_tachometer_selection_error"
HUMIDITY = "humidity_measurement_capacitive_resistive_dew_point_selection_compensation"
SW = "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"
TC = "thermocouple_temperature_sensor_seebeck_reference_junction_compensation"

CASES = [
    (FINAL, "fail_action_vs_safe_state", ("개방, 폐쇄, 유지", "SRS")),
    (FINAL, "imperfect_test_residual_risk", ("overhaul/mission time", "100%")),
    (FINAL, "response_time_process_safety_time", (
        "해당 위험 시나리오의 Process Safety Time(PST) 내에 요구 Safe State",
        "SRS 또는 추적 가능한 설계 시간 예산에 별도로 할당된 경우 해당 할당값을 검증한다",
    )),
    (FINAL, "redundancy_independence_boundary", ("common cause failure", "완전 독립")),
    (SPEED, "encoder_frequency_limit_selection", ("f_ch=n·P_ch/60", "count/s")),
    (SPEED, "counting_window_speed_equation", ("절대 RPM step", "상대 quantization")),
    (SPEED, "incremental_encoder_principle", ("미계측 축 이동", "homing")),
    (SPEED, "gear_tooth_speed_equation", ("전체 회전 평균", "실제 각도 간격")),
    (HUMIDITY, "absolute_humidity_definition", ("m_v/V", "P_w/P_ws(T)")),
    (SW, "sw04_hil", ("SiL 또는 HIL", "Virtual Commissioning")),
    (TC, "thermocouple_measures_temperature_difference", ("E0(Th)−E0(Tc)", "두 온도")),
]


def load(topic, filename):
    return json.loads((ROOT / "rubrics" / "topic_packs" / topic / filename).read_text(encoding="utf-8"))


@pytest.mark.parametrize("topic,anchor_id,markers", CASES)
def test_corrected_reference_is_used_by_requirement_evaluator(topic, anchor_id, markers):
    fact = load(topic, "fact_anchor.json")
    model = load(topic, "model_answer.json")
    anchor = next(a for a in fact["anchors"] if a["anchor_id"] == anchor_id)
    statement = anchor["statement"]
    assert all(marker in statement for marker in markers)
    assert not excluded_from_scoring(topic_id=topic, anchor_id=anchor_id)
    pattern = next(
        p for p in model["expected_question_patterns"]
        if anchor_id in p["required_anchor_ids"]
    )
    result = evaluate_fact_anchor_requirements(
        question_text=pattern["pattern"], answer_text=statement, topic_ids=[topic]
    )
    row = next(r for r in result["requirements"] if r["requirement_id"] == anchor_id)
    assert row["requirement_text"] == statement
    assert row["status"] in {"SATISFIED", "PARTIAL"}
    assert result["provider_calls"] == 0


def test_fixed_window_fatal_correction_does_not_claim_absolute_step_increases():
    fact = load(SPEED, "fact_anchor.json")
    logic = load(SPEED, "logic_check.json")
    rule_id = "speed_fatal_fixed_window_no_low_speed_error"
    a = next(r for r in fact["fatal_wrong_claims"] if r["id"] == rule_id)
    b = next(r for r in logic["llm_profile"]["fatal_conditions"] if r["id"] == rule_id)
    assert a["wrong_claim"] == b["wrong_claim"]
    assert "상대 양자화" in a["wrong_claim"]
    assert a["correct_rule"] == b["correct_rule"]
    assert "절대 RPM step은 일정" in a["correct_rule"]


def test_hil_fatal_rule_retains_actual_hardware_boundary():
    fact = load(SW, "fact_anchor.json")
    logic = load(SW, "logic_check.json")
    rule_id = "sw04_fatal_hil_requires_real_plant"
    a = next(r for r in fact["fatal_wrong_claims"] if r["id"] == rule_id)
    b = next(r for r in logic["llm_profile"]["fatal_conditions"] if r["id"] == rule_id)
    assert a["wrong_claim"] == b["wrong_claim"]
    assert "실제 생산설비" in a["wrong_claim"]
    assert "SiL 또는 HIL" in a["correct_rule"]
    assert "SiL 또는 HIL" in b["correct_rule"]
