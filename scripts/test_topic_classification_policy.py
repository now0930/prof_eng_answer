#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "rubrics" / "topic_packs"
CREATE_SCRIPT = ROOT / "scripts" / "create_topic_pack.py"

THEORY_TOPICS = {
    "bode_frequency_response_stability_margin_bandwidth",
    "feedback_system_closed_loop_sensitivity_steady_state_error",
    "lead_lag_compensator_phase_margin_steady_state_error",
    "lqr_optimal_state_feedback_riccati_weighting_design",
    "nyquist_stability_criterion_gain_phase_margin",
    "pid_controller_tuning_sequence_gain_effects",
    "root_locus_stability_gain_design",
    "routh_hurwitz_stability_criterion_gain_range",
    "second_order_lag_response_by_damping_ratio",
    "second_order_system_resonance_frequency_response",
    "state_feedback_reference_tracking_prefilter_integral_action",
    "state_space_controllability_observability_pole_placement",
}

APPLICATION_TOPICS = {
    "differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error",
    "lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error",
    "passive_sensor_resistive_capacitive_inductive_transduction",
    "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration",
    "radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error",
    "rtd_temperature_sensor_principle_pt100_wiring_compensation",
    "strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error",
    "temperature_measurement_error_heat_transfer",
    "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization",
    "thermocouple_temperature_sensor_seebeck_reference_junction_compensation",
    "ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8")
    )

    assert isinstance(value, dict), path
    return value


def main() -> None:
    actual_topics = {
        path.name
        for path in PACK_ROOT.iterdir()
        if path.is_dir()
    }

    assert actual_topics == (
        THEORY_TOPICS | APPLICATION_TOPICS
    )

    core_topics: set[str] = set()
    field_topics: set[str] = set()

    for topic_id in sorted(actual_topics):
        importance = load_json(
            PACK_ROOT
            / topic_id
            / "topic_importance.json"
        )

        difficulty = importance.get(
            "difficulty"
        )
        priority = importance.get(
            "selection_importance"
        )

        if priority == "CORE_MUST_PREPARE":
            core_topics.add(topic_id)

        if difficulty == "FIELD_APPLICATION":
            field_topics.add(topic_id)

        if topic_id in THEORY_TOPICS:
            assert difficulty == "THEORY_CORE"
            assert priority == "CORE_MUST_PREPARE"

        if topic_id in APPLICATION_TOPICS:
            assert difficulty == "FIELD_APPLICATION"
            assert priority == "NORMAL"

    assert core_topics == THEORY_TOPICS
    assert field_topics == APPLICATION_TOPICS

    create_text = CREATE_SCRIPT.read_text(
        encoding="utf-8"
    )

    assert (
        create_text.count(
            'default="FIELD_APPLICATION"'
        )
        == 1
    )

    assert (
        create_text.count(
            'default="NORMAL"'
        )
        == 1
    )

    print(
        f"theory_topic_count="
        f"{len(THEORY_TOPICS)}"
    )
    print(
        f"application_topic_count="
        f"{len(APPLICATION_TOPICS)}"
    )
    print(
        f"core_must_prepare_count="
        f"{len(core_topics)}"
    )
    print(
        f"field_application_count="
        f"{len(field_topics)}"
    )
    print(
        "PASS: CORE_MUST_PREPARE IS LIMITED "
        "TO CONTROL THEORY"
    )
    print(
        "PASS: APPLICATION TOPICS ARE "
        "FIELD_APPLICATION / NORMAL"
    )
    print(
        "PASS: NEW TOPIC DEFAULTS ARE "
        "FIELD_APPLICATION / NORMAL"
    )


if __name__ == "__main__":
    main()
