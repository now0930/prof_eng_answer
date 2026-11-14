"""Review guardrails for sentence simplification, not technical approval.

Preserve existing Fact IDs and indispensable conditions. This proves only
source representation and read-only safety; expert/source review is separate.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads(
    (ROOT / "calibration/fact_anchor_simplification_review_20261114.json").read_text(
        encoding="utf-8"
    )
)
BEFORE = {
    (item["topic_id"], item["anchor_id"]): item
    for item in MANIFEST["entries"]
}

SIMPLIFIED = {
    "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh": {
        "fsrm_markov_state_transition",
        "fsrm_markov_complexity",
        "fsrm_model_assumption_documentation",
    },
    "control_software_project_engineering_documents_fat_sat_commissioning_acceptance": {
        "sw10_fat_sat_relation",
        "sw10_loop_test",
    },
    "humidity_measurement_capacitive_resistive_dew_point_selection_compensation": {
        "relative_humidity_definition",
        "rh_temperature_dependence",
        "absolute_humidity_definition",
        "dew_point_definition",
        "frost_point_distinction",
        "pressure_dew_point_effect",
        "capacitive_polymer_principle",
        "resistive_humidity_principle",
        "psychrometric_wet_dry_bulb",
        "condensation_sensor_temperature_error",
        "low_humidity_dew_point_selection",
        "selection_environment_process",
    },
    "feedback_system_closed_loop_sensitivity_steady_state_error": {
        "feedback_sensitivity_functions",
        "feedback_parameter_sensitivity",
        "feedback_disturbance_noise_paths",
        "feedback_steady_state_error_final_value",
        "feedback_integral_action_tradeoff",
    },
    "pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error": {
        "bourdon_forms_application",
        "diaphragm_deflection_principle",
        "diaphragm_sensor_vs_seal",
        "piezoresistive_static_capability",
        "dp_transmitter_two_port_principle",
        "ambient_environment_hazardous_selection",
        "accuracy_total_performance_terms",
    },
    "speed_rotation_measurement_encoder_proximity_tachometer_selection_error": {
        "pulse_frequency_speed_equation",
        "counting_window_speed_equation",
        "period_measurement_low_speed",
        "quadrature_direction_principle",
        "index_z_channel_role",
        "absolute_encoder_principle",
        "encoder_frequency_limit_selection",
        "inductive_proximity_principle",
        "gear_tooth_speed_equation",
        "tachogenerator_voltage_speed_principle",
        "digital_tachometer_instrument_boundary",
    },
    "thermocouple_temperature_sensor_seebeck_reference_junction_compensation": {
        "thermocouple_temperature_measurement_chain",
        "thermocouple_seebeck_effect_dissimilar_conductors",
        "thermocouple_measures_temperature_difference",
        "thermocouple_reference_junction_compensation",
        "thermocouple_law_of_intermediate_metals",
        "thermocouple_law_of_intermediate_temperatures",
        "thermocouple_nonlinearity_reference_tables_polynomial_conversion",
        "thermocouple_thermowell_installation_dynamic_error",
    },
}

REQUIRED_BOUNDARIES = {
    ("functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh", "fsrm_markov_state_transition"):
        ("분석 목적", "전이확률 또는 전이율"),
    ("functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh", "fsrm_model_assumption_documentation"):
        ("모델 경계", "수요모드", "제외조건"),
    ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_fat_sat_relation"):
        ("시험계획", "둘 다 요구", "SAT"),
    ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_loop_test"):
        ("현장", "종단", "해당되는 최종제어요소"),
    ("humidity_measurement_capacitive_resistive_dew_point_selection_compensation", "relative_humidity_definition"):
        ("P_w", "P_ws(T)", "100"),
    ("humidity_measurement_capacitive_resistive_dew_point_selection_compensation", "absolute_humidity_definition"):
        ("단위체적", "이상기체 근사", "R_vT"),
    ("humidity_measurement_capacitive_resistive_dew_point_selection_compensation", "frost_point_distinction"):
        ("영하", "얼음", "액체"),
    ("humidity_measurement_capacitive_resistive_dew_point_selection_compensation", "pressure_dew_point_effect"):
        ("압력", "대기압 환산"),
    ("humidity_measurement_capacitive_resistive_dew_point_selection_compensation", "selection_environment_process"):
        ("해당되는 방폭 인증", "제품별 사양"),
    ("feedback_system_closed_loop_sensitivity_steady_state_error", "feedback_parameter_sensitivity"):
        ("H가 고정", "S=1/(1+L)"),
    ("feedback_system_closed_loop_sensitivity_steady_state_error", "feedback_disturbance_noise_paths"):
        ("단위 피드백", "출력단 외란", "측정 잡음", "다른 주입 위치"),
    ("feedback_system_closed_loop_sensitivity_steady_state_error", "feedback_steady_state_error_final_value"):
        ("모든 극", "개방 좌반평면", "최종값"),
    ("feedback_system_closed_loop_sensitivity_steady_state_error", "feedback_integral_action_tradeoff"):
        ("상쇄되지 않은", "포화", "anti-windup"),
    ("pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error", "piezoresistive_static_capability"):
        ("외부 여기", "정압", "압전식"),
    ("pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error", "dp_transmitter_two_port_principle"):
        ("P_H-P_L", "두 포트", "0"),
    ("pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error", "accuracy_total_performance_terms"):
        ("제조사별 정의", "온도", "정압", "설치"),
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "pulse_frequency_speed_equation"):
        ("60f/N_eff", "x1/x2/x4"),
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "counting_window_speed_equation"):
        ("60m/(N_eff·Δt)", "저속", "양자화"),
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "period_measurement_low_speed"):
        ("60/(N_eff·T_c)", "지터"),
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "quadrature_direction_principle"):
        ("A·B", "90°", "x1/x2/x4"),
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "index_z_channel_role"):
        ("1회전당", "다회전 절대위치"),
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "gear_tooth_speed_equation"):
        ("60f/Z", "실제 유효 이벤트"),
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "tachogenerator_voltage_speed_principle"):
        ("영구자석형", "규정 동작범위", "K_t·n"),
    ("thermocouple_temperature_sensor_seebeck_reference_junction_compensation", "thermocouple_seebeck_effect_dissimilar_conductors"):
        ("재료 조합", "기준접점", "비선형"),
    ("thermocouple_temperature_sensor_seebeck_reference_junction_compensation", "thermocouple_reference_junction_compensation"):
        ("별도 센서", "단자 온도구배", "측정접점"),
    ("thermocouple_temperature_sensor_seebeck_reference_junction_compensation", "thermocouple_law_of_intermediate_metals"):
        ("제3 금속", "등온", "순 열기전력"),
    ("thermocouple_temperature_sensor_seebeck_reference_junction_compensation", "thermocouple_law_of_intermediate_temperatures"):
        ("E(T1,T3)=E(T1,T2)+E(T2,T3)", "기준접점"),
    ("thermocouple_temperature_sensor_seebeck_reference_junction_compensation", "thermocouple_nonlinearity_reference_tables_polynomial_conversion"):
        ("형식별", "유효 온도범위", "단위"),
    ("thermocouple_temperature_sensor_seebeck_reference_junction_compensation", "thermocouple_thermowell_installation_dynamic_error"):
        ("침지길이", "유속", "설치조건"),
}


@pytest.mark.parametrize("topic", sorted(SIMPLIFIED))
def test_only_source_bound_single_sentence_statement_is_revised(topic):
    path = ROOT / "rubrics" / "topic_packs" / topic / "fact_anchor.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = {str(a.get("anchor_id") or a.get("id")): a for a in data["anchors"]}
    assert data["topic_id"] == topic
    assert SIMPLIFIED[topic] <= rows.keys()
    assert MANIFEST["schema_version"] == "fact_anchor_simplification_review.v1"
    assert MANIFEST["review_status"] == "PENDING_TECHNICAL_REVIEW"
    assert MANIFEST["score_effect"] == "none"
    assert len(BEFORE) == MANIFEST["changed_anchor_count"] == 48
    assert set(BEFORE) == {
        (topic_id, aid)
        for topic_id, anchors in SIMPLIFIED.items()
        for aid in anchors
    }
    for aid in SIMPLIFIED[topic]:
        row = rows[aid]
        statement = row["statement"]
        baseline = BEFORE[(topic, aid)]
        assert baseline["review_status"] == "PENDING_TECHNICAL_REVIEW"
        assert statement == baseline["simplified_statement"]
        assert statement != baseline["previous_statement"]
        assert statement.endswith((".", "다."))
        assert len(re.findall(r"[.!?。](?=\s|$)", statement)) == 1
        assert not row.get("review_status") == "approved"  # approval is not inferred
        assert baseline["previous_statement"] in row.get(
            "accepted_explanations", []
        ), "original Fact wording must remain available for manual review"
        for alias in ("expected", "claim", "description"):
            if alias in row:
                assert row[alias] == statement
        for term in REQUIRED_BOUNDARIES.get((topic, aid), ()):
            assert term in statement


def test_managed_displacer_source_requires_separate_review_and_reapproval():
    topic = "displacer_level_buoyancy_torque_tube_density_interface_calibration"
    folder = ROOT / "rubrics/topic_packs" / topic
    status = json.loads((folder / "topic_status.json").read_text(encoding="utf-8"))
    anchors = json.loads((folder / "fact_anchor.json").read_text(encoding="utf-8"))
    assert status["status"] == "approved"
    assert status["review_method"] == "human"
    raw_bytes = (folder / "fact_anchor.json").read_bytes()
    blob = b"blob " + str(len(raw_bytes)).encode("ascii") + b"\x00" + raw_bytes
    assert hashlib.sha1(blob).hexdigest() == (
        "23ae898870b6dd2e1e71f3ead09038688ba6fc3a"
    )
    for aid in (
        "displacer_buoyancy",
        "displacer_signal_chain",
        "displacer_interface_density_difference",
        "displacer_wet_dry_calibration",
    ):
        row = next(a for a in anchors["anchors"] if a["anchor_id"] == aid)
        assert len(re.findall(r"[.!?。](?=\s|$)", row["statement"])) >= 2
    # Approved source stays untouched until authorized managed review.


def test_source_simplification_has_no_scoring_admission():
    from grading.evidence.fact_anchor_sentence_view import project_fact_anchor_sentences

    view = project_fact_anchor_sentences(SIMPLIFIED)
    assert view["score_effect"] == "none"
    assert view["score_admission"] == "DISABLED"
    by_pair = {(r["owner_topic_id"], r["fact_id"]): r for r in view["rows"]}
    assert sum(map(len, SIMPLIFIED.values())) == 48
    assert all(
        by_pair[(topic, aid)]["style_status"] == "SINGLE_STATEMENT"
        for topic, anchors in SIMPLIFIED.items()
        for aid in anchors
    )
