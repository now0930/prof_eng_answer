#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "rubrics" / "topic_packs"

THEORY_TOPICS = {
    "bode_frequency_response_stability_margin_bandwidth",
    "control_valve_authority_rangeability_gain_installed_performance",
    "feedback_system_closed_loop_sensitivity_steady_state_error",
    "historian_mes_it_ot_integration_industrial_data_quality_realtime_processing",
    "industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle",
    "lead_lag_compensator_phase_margin_steady_state_error",
    "lqr_optimal_state_feedback_riccati_weighting_design",
    "nyquist_stability_criterion_gain_phase_margin",
    "physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control",
    "pid_controller_tuning_sequence_gain_effects",
    "plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability",
    "process_control_loop_architecture_cascade_ratio_feedforward_override_split_range",
    "root_locus_stability_gain_design",
    "routh_hurwitz_stability_criterion_gain_range",
    "second_order_lag_response_by_damping_ratio",
    "second_order_system_resonance_frequency_response",
    "sis_sil_safety_software_independence_systematic_failure_verification_validation",
    "state_feedback_reference_tracking_prefilter_integral_action",
    "state_space_controllability_observability_pole_placement",
}

APPLICATION_TOPICS = {
    "balanced_trim_unbalanced_trim_structure_sealing_applications",
    "control_valve_cavitation_flashing_choked_flow_damage_prevention",
    "control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening",
    "control_valve_deadband_stiction_response_time_positioner_dynamic_performance",
    "control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe",
    "control_valve_gas_sizing_choked_flow_critical_pressure_ratio",
    "control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim",
    "control_valve_positioner_ip_converter_booster_accessories_calibration",
    "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions",
    "control_valve_selection_process_pressure_temperature_flow_media_lifecycle",
    "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles",
    "control_valve_sizing_cv_kv_reynolds_liquid_selection",
    "control_valve_types_globe_rotary_body_actuator_selection",
    "differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error",
    "electronics_error_noise_drift_tolerance_aging_power_mitigation",
    "final_control_element_sil_sis_esd_valve_partial_stroke_test",
    "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection",
    "humidity_measurement_capacitive_resistive_dew_point_selection_compensation",
    "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification",
    "instrumentation_installation_wiring_impulse_tubing_inspection_codes",
    "instrumentation_power_grounding_shielding_ups_ground_loop_emc",
    "lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error",
    "optical_laser_photoelectric_noncontact_measurement_tof_triangulation",
    "passive_sensor_resistive_capacitive_inductive_transduction",
    "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration",
    "pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error",
    "radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error",
    "rtd_temperature_sensor_principle_pt100_wiring_compensation",
    "smart_positioner_diagnostics_valve_signature_predictive_maintenance",
    "speed_rotation_measurement_encoder_proximity_tachometer_selection_error",
    "strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error",
    "temperature_measurement_error_heat_transfer",
    "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization",
    "thermocouple_temperature_sensor_seebeck_reference_junction_compensation",
    "ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error",
}

DESIGN_TOPICS = {
    "configuration_change_release_backup_rollback_migration_obsolescence_management",
    "control_hardware_lifecycle_panel_architecture_component_selection_production_verification",
    "control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe",
    "control_software_project_engineering_documents_fat_sat_commissioning_acceptance",
    "control_system_operations_maintenance_calibration_inspection_spares_kpi",
    "hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management",
    "industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread",
    "industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience",
    "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection",
    "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation",
    "instrumentation_production_management_planning_quality_cost_resources",
    "instrumentation_project_management_basic_design_cost_schedule_documents_acceptance",
    "instrumentation_system_design_basis_codes_standards_specification_deviation_management",
    "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response",
    "pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative",
}

ALLOWED_SELECTION_IMPORTANCE = {
    "CORE_MUST_PREPARE",
    "HIGH",
    "NORMAL",
}

EXPECTED_DIFFICULTY_COUNTS = {
    "THEORY_CORE": 19,
    "FIELD_APPLICATION": 35,
    "DESIGN_EVALUATION": 15,
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    actual_topics = {
        path.name
        for path in PACK_ROOT.iterdir()
        if path.is_dir()
    }

    classified_topics = (
        THEORY_TOPICS
        | APPLICATION_TOPICS
        | DESIGN_TOPICS
    )

    assert len(actual_topics) == 69
    assert actual_topics == classified_topics

    assert not (THEORY_TOPICS & APPLICATION_TOPICS)
    assert not (THEORY_TOPICS & DESIGN_TOPICS)
    assert not (APPLICATION_TOPICS & DESIGN_TOPICS)

    actual_by_difficulty = {
        "THEORY_CORE": set(),
        "FIELD_APPLICATION": set(),
        "DESIGN_EVALUATION": set(),
    }

    for topic_id in sorted(actual_topics):
        importance = load_json(
            PACK_ROOT / topic_id / "topic_importance.json"
        )

        difficulty = importance.get("difficulty")
        selection_importance = importance.get("selection_importance")

        assert difficulty in actual_by_difficulty, (
            topic_id,
            difficulty,
        )
        assert selection_importance in ALLOWED_SELECTION_IMPORTANCE, (
            topic_id,
            selection_importance,
        )

        actual_by_difficulty[difficulty].add(topic_id)

    assert actual_by_difficulty["THEORY_CORE"] == THEORY_TOPICS
    assert (
        actual_by_difficulty["FIELD_APPLICATION"]
        == APPLICATION_TOPICS
    )
    assert (
        actual_by_difficulty["DESIGN_EVALUATION"]
        == DESIGN_TOPICS
    )

    for difficulty, expected_count in EXPECTED_DIFFICULTY_COUNTS.items():
        assert len(actual_by_difficulty[difficulty]) == expected_count

    print(f"theory_topic_count={len(THEORY_TOPICS)}")
    print(f"application_topic_count={len(APPLICATION_TOPICS)}")
    print(f"design_topic_count={len(DESIGN_TOPICS)}")
    print(f"classified_topic_count={len(classified_topics)}")
    print(
        "selection_importance_values="
        + ",".join(sorted(ALLOWED_SELECTION_IMPORTANCE))
    )


if __name__ == "__main__":
    main()
