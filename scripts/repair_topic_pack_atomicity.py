#!/usr/bin/env python3
"""Repair reviewed Topic Pack contamination and scope legacy question patterns.

This is an explicit migration, not a production-time inference path.  It projects
the authoritative Fact Anchor statements into duplicate model/logic mirrors and
converts legacy string questions into anchor-scoped contracts.  Run without
``--write`` to preview the exact assignments.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "rubrics" / "topic_packs"
P0_TOPICS = {
    "control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing",
    "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization",
    "nyquist_stability_criterion_gain_phase_margin",
    "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration",
}
TOKEN_RE = re.compile(r"[0-9a-z가-힣]+")
STOP = {
    "the", "and", "또는", "및", "의", "를", "을", "이", "가", "에서", "으로",
    "설명하시오", "구하시오", "비교하시오", "제시하시오", "방법", "관계", "시",
}

# Reviewed question-to-anchor contracts.  Index order is locked to the source
# question order and validated before any file is written.  Keeping this map in
# the migration makes the semantic decision inspectable and reproducible.
CURATED_QUESTION_CONTRACTS: dict[str, list[list[str]]] = {
    "bode_frequency_response_stability_margin_bandwidth": [
        ["open_loop_closed_loop_roles", "log_frequency_and_decibel", "pole_zero_magnitude_slopes", "gain_phase_crossover_frequencies", "phase_margin_calculation", "gain_margin_calculation"],
        ["open_loop_closed_loop_roles", "gain_phase_crossover_frequencies", "phase_margin_calculation", "gain_margin_calculation"],
        ["gain_phase_crossover_frequencies", "phase_margin_calculation", "gain_margin_calculation"],
        ["open_loop_closed_loop_roles", "gain_phase_crossover_frequencies", "closed_loop_bandwidth"],
        ["positive_gain_shift", "gain_phase_crossover_frequencies", "phase_margin_calculation", "compensator_and_field_validation"],
        ["compensator_and_field_validation", "phase_margin_calculation", "sensitivity_robustness_noise_tradeoff"],
        ["delay_and_nonminimum_phase_limits", "phase_margin_calculation", "compensator_and_field_validation"],
        ["multiple_or_missing_crossovers", "phase_margin_calculation", "gain_margin_calculation"],
    ],
    "control_software_project_engineering_documents_fat_sat_commissioning_acceptance": [
        ["sw10_feasibility", "sw10_scope_baseline", "sw10_schedule_dependencies", "sw10_cost_change_control"],
        ["sw10_urs", "sw10_frs", "sw10_fds", "sw10_sds", "sw10_document_hierarchy_traceability"],
        ["sw10_io_list", "sw10_tag_list", "sw10_alarm_list", "sw10_interlock_list", "sw10_cause_effect"],
        ["sw10_test_specification", "sw10_fat", "sw10_fat_limit", "sw10_sat", "sw10_fat_sat_relation"],
        ["sw10_test_specification", "sw10_loop_test", "sw10_site_integration_test"],
        ["sw10_commissioning", "sw10_test_specification", "sw10_configuration_backup"],
        ["sw10_performance_test", "sw10_acceptance", "sw10_test_specification"],
        ["sw10_punch_list", "sw10_as_built_handover"],
        ["sw10_change_punch_closure", "sw10_configuration_backup", "sw10_test_specification"],
        ["sw10_scope_project_execution", "sw10_document_hierarchy_traceability", "sw10_fat_sat_relation", "sw10_commissioning", "sw10_acceptance", "sw10_as_built_handover"],
    ],
    "feedback_system_closed_loop_sensitivity_steady_state_error": [
        ["feedback_negative_loop_structure", "feedback_closed_loop_transfer", "feedback_sensitivity_functions"],
        ["feedback_negative_loop_structure", "feedback_sensitivity_functions", "feedback_parameter_sensitivity"],
        ["feedback_steady_state_error_final_value", "feedback_system_type_error_constants", "feedback_type_error_relationship"],
        ["feedback_disturbance_noise_paths", "feedback_sensitivity_functions", "feedback_stability_bandwidth_tradeoff"],
        ["feedback_parameter_sensitivity", "feedback_type_error_relationship", "feedback_integral_action_tradeoff", "feedback_field_design_validation"],
    ],
    "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation": [
        ["sw04_scope_general_lifecycle", "sw04_v_model_definition", "sw04_requirements_specification", "sw04_unit_test", "sw04_integration_test", "sw04_system_test"],
        ["sw04_verification_definition", "sw04_validation_definition", "sw04_verification_validation_relationship"],
        ["sw04_requirements_specification", "sw04_rtm_bidirectional", "sw04_evidence_and_auditability"],
        ["sw04_unit_test", "sw04_integration_test", "sw04_system_test", "sw04_test_specification"],
        ["sw04_static_analysis", "sw04_dynamic_analysis", "sw04_regression_test"],
        ["sw04_requirements_specification", "sw04_test_specification", "sw04_coverage_exit_criteria"],
        ["sw04_simulation", "sw04_hil", "sw04_fault_injection", "sw04_test_environment"],
        ["sw04_defect_management", "sw04_change_impact", "sw04_regression_test", "sw04_lifecycle_feedback"],
        ["sw04_software_architecture", "sw04_detailed_design", "sw04_review_approval"],
        ["sw04_configuration_baseline", "sw04_review_approval", "sw04_evidence_and_auditability", "sw04_verification_validation_relationship"],
        ["sw04_v_model_definition", "sw04_verification_validation_relationship", "sw04_mcdc_detailed_coverage_boundary", "vmodel_no_sil_guarantee__mcdc_adjacent_boundary"],
    ],
    "lead_lag_compensator_phase_margin_steady_state_error": [
        ["lead_lag_lead_pole_zero_geometry", "lead_lag_lag_pole_zero_geometry", "lead_lag_lead_maximum_phase_relation", "lead_lag_lag_steady_state_error_improvement"],
        ["lead_lag_lead_maximum_phase_relation", "lead_lag_lead_center_frequency_magnitude", "lead_lag_lead_phase_margin_design_sequence"],
        ["lead_lag_lag_pole_zero_geometry", "lead_lag_lag_steady_state_error_improvement", "lead_lag_lag_gain_ratio_error_constant"],
        ["lead_lag_combined_design", "lead_lag_design_objective", "lead_lag_lead_bandwidth_noise_effort_tradeoff", "lead_lag_lag_crossover_phase_loss"],
        ["lead_lag_root_locus_frequency_consistency", "lead_lag_plant_robustness_limits", "lead_lag_implementation_validation"],
    ],
    "lqr_optimal_state_feedback_riccati_weighting_design": [
        ["state_lqr_design_objective_cost", "state_lqr_weight_matrix_conditions", "state_lqr_care_stabilizing_solution", "state_lqr_optimal_gain_closed_loop"],
        ["state_lqr_q_weight_state_tradeoff", "state_lqr_r_weight_control_tradeoff", "state_lqr_state_input_normalization_bryson"],
        ["state_lqr_existence_stabilizability_detectability", "state_lqr_care_stabilizing_solution"],
        ["state_lqr_pole_placement_distinction", "state_lqr_tracking_prefilter_lqi"],
        ["state_lqr_continuous_discrete_riccati_distinction", "state_lqr_saturation_constraints_limit", "state_lqr_robustness_observer_implementation_validation"],
    ],
    "nyquist_stability_criterion_gain_phase_margin": [
        ["closed_loop_characteristic_equation", "nyquist_contour_and_mapping", "argument_principle_pnz_relation", "critical_point_minus_one", "open_loop_rhp_poles_count", "closed_loop_rhp_poles_count"],
        ["nyquist_contour_and_mapping", "argument_principle_pnz_relation", "critical_point_minus_one", "open_loop_rhp_poles_count", "closed_loop_rhp_poles_count", "conjugate_symmetry"],
        ["closed_loop_characteristic_equation", "critical_point_minus_one", "argument_principle_pnz_relation", "field_robustness_validation"],
        ["imaginary_axis_pole_indentation", "multiple_crossover_interpretation", "conjugate_symmetry"],
        ["gain_margin_definition", "phase_margin_definition", "multiple_crossover_interpretation", "time_delay_phase_effect", "field_robustness_validation"],
    ],
    "passive_sensor_resistive_capacitive_inductive_transduction": [
        ["sensor_resistive_geometry_conductivity_relation", "sensor_resistive_voltage_current_conversion", "sensor_capacitive_geometry_permittivity_relation", "sensor_capacitive_dynamic_current_readout", "sensor_inductive_magnetic_circuit_permeability_relation", "sensor_inductive_voltage_impedance_readout"],
        ["sensor_material_property_geometry_separation", "sensor_resistive_geometry_conductivity_relation", "sensor_capacitive_geometry_permittivity_relation", "sensor_inductive_gap_eddy_current_conductivity"],
        ["sensor_mechanical_stress_strain_youngs_modulus", "sensor_material_property_geometry_separation", "sensor_resistive_geometry_conductivity_relation", "sensor_capacitive_geometry_permittivity_relation", "sensor_inductive_magnetic_circuit_permeability_relation"],
        ["sensor_resistive_voltage_current_conversion", "sensor_capacitive_dynamic_current_readout", "sensor_inductive_voltage_impedance_readout", "sensor_rcl_excitation_signal_conditioning"],
        ["sensor_rcl_sensitivity_linearity_environment", "sensor_rcl_calibration_implementation_validation", "sensor_passive_transduction_chain"],
    ],
    "pid_controller_tuning_sequence_gain_effects": [
        ["pid_controller_definition", "p_action_effect", "i_action_effect", "d_action_effect", "general_tuning_sequence"],
        ["p_action_effect", "i_action_effect", "d_action_effect", "general_tuning_sequence", "field_constraints"],
        ["i_action_effect", "d_action_effect", "field_constraints"],
        ["p_action_effect", "i_action_effect", "d_action_effect", "general_tuning_sequence"],
    ],
    "process_control_loop_architecture_cascade_ratio_feedforward_override_split_range": [
        ["process_loop_signal_chain", "single_loop_architecture", "loop_interaction_coordination", "architecture_selection_criteria"],
        ["cascade_structure", "cascade_secondary_faster", "cascade_disturbance_condition"],
        ["ratio_control_structure", "ratio_scaling_and_low_flow", "feedforward_principle", "feedforward_feedback_combination"],
        ["feedforward_principle", "feedforward_feedback_combination", "field_implementation_validation"],
        ["override_selective_control", "override_tracking_antiwindup"],
        ["split_range_control", "split_range_transition_design"],
        ["cascade_structure", "ratio_control_structure", "feedforward_principle", "override_selective_control", "split_range_control", "architecture_selection_criteria"],
        ["single_loop_architecture", "loop_interaction_coordination", "architecture_selection_criteria", "field_implementation_validation"],
    ],
    "root_locus_stability_gain_design": [
        ["closed_loop_pole_gain_relationship", "root_locus_definition", "root_locus_start_end_points", "real_axis_segment_rule", "asymptote_count_and_angles", "gain_from_magnitude_condition"],
        ["closed_loop_pole_gain_relationship", "root_locus_start_end_points", "real_axis_segment_rule", "imaginary_axis_crossing", "gain_from_magnitude_condition"],
        ["real_axis_segment_rule", "asymptote_count_and_angles", "asymptote_centroid", "breakaway_break_in_points", "imaginary_axis_crossing"],
        ["dominant_pole_design", "transient_response_mapping", "angle_condition", "gain_from_magnitude_condition"],
        ["compensator_design_application", "angle_condition", "gain_from_magnitude_condition"],
    ],
    "routh_hurwitz_stability_criterion_gain_range": [
        ["asymptotic_stability_open_lhp", "first_column_sign_changes_rhp_count", "routh_first_two_rows_layout", "routh_recursive_row_calculation"],
        ["routh_first_two_rows_layout", "routh_recursive_row_calculation", "first_column_sign_changes_rhp_count", "asymptotic_stability_open_lhp"],
        ["gain_range_first_column_inequalities", "gain_boundary_requires_verification", "field_gain_selection_requires_margin"],
        ["zero_first_column_epsilon_limit", "all_zero_row_auxiliary_polynomial", "imaginary_axis_roots_stability_class"],
        ["relative_stability_axis_shift", "gain_range_first_column_inequalities", "gain_boundary_requires_verification"],
    ],
    "rtd_temperature_sensor_principle_pt100_wiring_compensation": [
        ["rtd_temperature_measurement_chain", "rtd_metal_resistance_temperature_principle", "rtd_pt100_reference_resistance_alpha_standard", "rtd_callendar_van_dusen_characteristic"],
        ["rtd_two_wire_lead_resistance_error", "rtd_three_wire_bridge_compensation_assumptions", "rtd_four_wire_kelvin_measurement", "rtd_wiring_method_selection_tradeoff"],
        ["rtd_excitation_voltage_measurement", "rtd_self_heating_thermal_error", "rtd_wiring_method_selection_tradeoff", "rtd_fault_diagnostics_environment_validation"],
    ],
    "second_order_lag_response_by_damping_ratio": [
        ["so2_standard_transfer_function", "so2_damping_ratio_definition", "so2_pole_response_relationship", "so2_underdamped_response", "so2_critical_damping_response", "so2_overdamped_response"],
        ["so2_damping_ratio_definition", "so2_pole_response_relationship", "so2_underdamped_response", "so2_critical_damping_response", "so2_overdamped_response"],
        ["so2_underdamped_response", "so2_critical_damping_response", "so2_overdamped_response"],
        ["so2_damping_ratio_definition", "so2_pole_response_relationship", "so2_zero_negative_damping"],
        ["so2_underdamped_response", "so2_design_tradeoff", "so2_pole_response_relationship"],
    ],
    "second_order_system_resonance_frequency_response": [
        ["F1", "F2", "F3"],
        ["F2", "F3"],
        ["F3", "F4", "F5"],
    ],
    "state_feedback_reference_tracking_prefilter_integral_action": [
        ["state_tracking_design_objective", "state_tracking_prefilter_steady_state_derivation", "state_tracking_integral_internal_model_principle", "state_tracking_prefilter_integral_role_separation"],
        ["state_tracking_feedback_law_closed_loop", "state_tracking_prefilter_steady_state_derivation", "state_tracking_prefilter_existence_model_dependence"],
        ["state_tracking_integral_internal_model_principle", "state_tracking_augmented_system_formulation", "state_tracking_augmented_controllability_stabilizability"],
        ["state_tracking_prefilter_steady_state_derivation", "state_tracking_prefilter_existence_model_dependence", "state_tracking_prefilter_integral_role_separation", "state_tracking_disturbance_reference_performance"],
        ["state_tracking_observer_separation_principle", "state_tracking_saturation_anti_windup", "state_tracking_implementation_validation"],
    ],
    "state_space_controllability_observability_pole_placement": [
        ["state_space_model_and_dimensions", "transfer_function_realization_relation", "eigenvalue_pole_minimal_realization"],
        ["state_space_model_and_dimensions", "controllability_matrix_rank", "pbh_controllability_stabilizability"],
        ["state_space_model_and_dimensions", "observability_matrix_rank", "pbh_observability_detectability"],
        ["pbh_controllability_stabilizability", "pbh_observability_detectability"],
        ["state_feedback_closed_loop", "pole_placement_conditions", "ackermann_and_numerical_limits"],
        ["observer_error_dynamics", "pbh_observability_detectability", "separation_principle_conditions"],
        ["state_feedback_closed_loop", "observer_error_dynamics", "separation_principle_conditions"],
        ["reference_tracking_integral_action", "implementation_tradeoffs_validation", "separation_principle_conditions"],
    ],
    "temperature_measurement_error_heat_transfer": [
        ["temperature_heat_transfer_error_paths", "temperature_heat_resistance_model", "temperature_error_reduction_measures"],
        ["temperature_heat_transfer_error_paths", "temperature_stem_conduction_immersion_error", "temperature_heat_resistance_model"],
        ["temperature_stem_conduction_immersion_error", "temperature_installation_selection_conditions", "temperature_error_reduction_measures"],
    ],
    "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization": [
        ["thermistor_temperature_measurement_chain", "thermistor_semiconductor_resistance_temperature_principle", "thermistor_ntc_negative_temperature_coefficient", "thermistor_ptc_positive_temperature_coefficient_switching"],
        ["thermistor_ntc_beta_equation", "thermistor_steinhart_hart_linearization", "thermistor_tolerance_interchangeability_calibration"],
        ["thermistor_voltage_divider_bridge_current_measurement", "thermistor_adc_reference_ratiometric_conversion", "thermistor_self_heating_dissipation_constant", "thermistor_thermal_time_constant_installation", "thermistor_wiring_contact_moisture_noise_effects", "thermistor_fault_diagnostics_open_short_range_fail_safe"],
    ],
    "thermocouple_temperature_sensor_seebeck_reference_junction_compensation": [
        ["thermocouple_temperature_measurement_chain", "thermocouple_seebeck_effect_dissimilar_conductors", "thermocouple_measures_temperature_difference", "thermocouple_reference_junction_compensation", "thermocouple_nonlinearity_reference_tables_polynomial_conversion"],
        ["thermocouple_seebeck_effect_dissimilar_conductors", "thermocouple_measures_temperature_difference"],
        ["thermocouple_temperature_measurement_chain", "thermocouple_measures_temperature_difference", "thermocouple_reference_junction_compensation"],
        ["thermocouple_reference_junction_compensation", "thermocouple_law_of_intermediate_temperatures"],
        ["thermocouple_law_of_intermediate_metals", "thermocouple_law_of_intermediate_temperatures"],
        ["thermocouple_extension_compensating_wire_polarity", "thermocouple_fault_diagnostics_open_polarity_cjc_validation"],
        ["thermocouple_type_material_range_atmosphere_selection", "thermocouple_junction_construction_response_isolation"],
        ["thermocouple_calibration_tolerance_uncertainty_drift", "thermocouple_fault_diagnostics_open_polarity_cjc_validation", "thermocouple_thermowell_installation_dynamic_error", "thermocouple_signal_conditioning_noise_grounding"],
        ["thermocouple_junction_construction_response_isolation", "thermocouple_thermowell_installation_dynamic_error"],
        ["thermocouple_signal_conditioning_noise_grounding", "thermocouple_nonlinearity_reference_tables_polynomial_conversion", "thermocouple_reference_junction_compensation"],
    ],
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def _dump(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _tokens(value: Any) -> set[str]:
    if isinstance(value, dict):
        text = " ".join(str(item) for item in value.values())
    elif isinstance(value, list):
        text = " ".join(str(item) for item in value)
    else:
        text = str(value or "")
    result = {
        token for token in TOKEN_RE.findall(text.casefold())
        if len(token) >= 2 and token not in STOP
    }
    # Korean eojeol endings make word-only overlap brittle. Character trigrams
    # are used only to rank anchors inside the already selected owner Topic.
    compact = "".join(char for char in text.casefold() if "가" <= char <= "힣")
    result.update(f"ko:{compact[i:i + 3]}" for i in range(max(0, len(compact) - 2)))
    return result


def _anchor_id(anchor: dict[str, Any]) -> str:
    return str(anchor.get("id") or anchor.get("anchor_id") or "").strip()


def _rank_anchors(pattern: str, anchors: list[dict[str, Any]]) -> list[str]:
    question_tokens = _tokens(pattern)
    ranked: list[tuple[float, str]] = []
    for anchor in anchors:
        anchor_id = _anchor_id(anchor)
        corpus = {
            "id": anchor_id.replace("_", " "),
            "statement": anchor.get("statement", ""),
            "keywords": anchor.get("keywords", []),
            "core_terms": anchor.get("core_terms", []),
            "description": anchor.get("description", ""),
        }
        anchor_tokens = _tokens(corpus)
        overlap = question_tokens & anchor_tokens
        score = sum(2.0 if token.startswith("ko:") else 3.0 for token in overlap)
        score /= max(1.0, len(question_tokens) ** 0.5 * len(anchor_tokens) ** 0.35)
        ranked.append((score, anchor_id))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    if not ranked or ranked[0][0] <= 0:
        raise ValueError(f"no anchor vocabulary match for question: {pattern}")
    best = ranked[0][0]
    selected = [anchor_id for score, anchor_id in ranked if score >= best * 0.58][:4]
    if len(selected) < min(2, len(ranked)):
        selected = [anchor_id for _, anchor_id in ranked[:2]]
    return selected


def _fatal_projection(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _safe_projection(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for row in value:
        if isinstance(row, str) and row.strip():
            result.append(row)
        elif isinstance(row, dict):
            text = row.get("statement") or row.get("claim") or row.get("correct_rule")
            if isinstance(text, str) and text.strip():
                result.append(text)
    return result


def _repair_p0(topic_id: str, fact: dict[str, Any], model: dict[str, Any], logic: dict[str, Any]) -> None:
    anchors = [row for row in fact.get("anchors", []) if isinstance(row, dict)]
    statements = [str(row.get("statement") or "").strip() for row in anchors]
    statements = [row for row in statements if row]
    title = str(model.get("title_ko") or fact.get("title_ko") or logic.get("title") or topic_id)

    if topic_id == "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization":
        title = "Thermistor 온도센서의 NTC·PTC 특성, 측정회로 및 선형화"
        fact["title_ko"] = title
        fact["topic_label"] = title
        fact["safe_expressions"] = statements
        for anchor in anchors:
            statement = str(anchor.get("statement") or "").strip()
            description = str(anchor.get("description") or "").strip()
            anchor["accepted_explanations"] = [
                item for item in (statement, description) if item
            ]
            anchor["rejected_explanations"] = [
                "용어만 나열하고 Thermistor의 저항-온도 원리, 회로조건 또는 오차 인과관계를 설명하지 않는다."
            ]
            anchor["source_basis"] = (
                "reviewed Thermistor NTC·PTC measurement, linearization, "
                "self-heating and diagnostics requirements"
            )
        current_patterns = model.get("expected_question_patterns", [])
        if any(
            isinstance(row, str) or "rtd" in str(row).casefold() or "pt100" in str(row).casefold()
            for row in current_patterns
        ):
            model["expected_question_patterns"] = [
                "Thermistor 온도센서의 측정원리와 NTC·PTC 특성을 설명하시오.",
                "NTC Thermistor의 B-상수 식과 Steinhart-Hart 선형화 방법을 설명하시오.",
                "Thermistor 측정회로의 자기발열, 열시정수, 배선오차 및 고장진단을 설명하시오.",
            ]
        model["common_missing_points"] = [
            "NTC와 PTC의 저항-온도 방향 및 적용범위를 구분하지 않음",
            "B-상수 식과 Steinhart-Hart 식의 적용범위를 구분하지 않음",
            "전압분배기·기준저항·ADC의 변환사슬을 생략함",
            "측정전력에 의한 자기발열과 방산정수를 생략함",
            "열시정수, 설치, 배선·접촉·습기 및 단선·단락 진단을 생략함",
        ]

    if topic_id == "nyquist_stability_criterion_gain_phase_margin":
        current_patterns = model.get("expected_question_patterns", [])
        if any(
            isinstance(row, str) or any(
                term in str(row).casefold()
                for term in ("한 행 전체가 0", "실수부가 -α", "routh", "루스")
            )
            for row in current_patterns
        ):
            model["expected_question_patterns"] = [
                "Nyquist 안정도 판별법의 원리와 판별 절차를 설명하시오.",
                "주어진 개루프 전달함수의 Nyquist 궤적을 작성하고 안정 여부를 판별하시오.",
                "폐루프 특성방정식에 포함된 제어기 이득 K의 안정 범위를 Nyquist 선도로 구하시오.",
                "Nyquist 판별에서 허수축 극점의 우회와 복수 crossover 처리 방법을 설명하시오.",
                "Nyquist 선도에서 이득·위상여유와 시간지연을 고려한 강인성 조건을 설명하시오.",
            ]
        for key in ("routing_aliases", "topic_aliases"):
            aliases = model.get(key)
            if isinstance(aliases, list):
                model[key] = [
                    alias for alias in aliases
                    if not any(term in str(alias).casefold() for term in (
                        "routh", "루스", "첫 열", "0인 행", "zero row", "axis shift",
                    ))
                ]
        missing = model.get("common_missing_points")
        if isinstance(missing, list):
            model["common_missing_points"] = [
                item for item in missing
                if not any(term in str(item).casefold() for term in ("routh", "첫 행", "둘째 행"))
            ]

    if topic_id in {
        "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization",
        "control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing",
    }:
        fact["safe_expressions"] = statements

    fact["core_facts"] = statements
    fact["title_ko"] = title
    if "topic_label" in fact:
        fact["topic_label"] = title

    model["title_ko"] = title
    if "id" in model:
        model["id"] = f"{topic_id}_{model.get('question_type', 'UNKNOWN')}_v1"
    if "title" in model:
        model["title"] = title

    profile = logic.setdefault("llm_profile", {})
    profile["display_name"] = title
    profile["truth_schema"] = statements
    profile["fatal_conditions"] = _fatal_projection(fact.get("fatal_wrong_claims"))
    profile["safe_conditions"] = _safe_projection(fact.get("safe_expressions"))
    key_terms: list[str] = [title, topic_id]
    key_terms.extend(str(row) for row in model.get("routing_aliases", []) if str(row).strip())
    for anchor in anchors:
        key_terms.append(_anchor_id(anchor))
        key_terms.extend(str(row) for row in anchor.get("core_terms", []) if str(row).strip())
    profile["candidate_extraction"] = {
        "key_terms": list(dict.fromkeys(key_terms)),
        "rules": [],
    }
    logic["title"] = title
    if "topic_label" in logic:
        logic["topic_label"] = title
    deterministic = logic.get("deterministic_checks")
    if isinstance(deterministic, dict):
        deterministic["topic_name"] = title
        deterministic["topic_aliases"] = list(model.get("routing_aliases", []))


def _sync_legacy_model_mirrors(topic_id: str, model: dict[str, Any]) -> None:
    patterns = model.get("expected_question_patterns", [])
    questions = [
        row if isinstance(row, str) else str(row.get("pattern") or "")
        for row in patterns
    ]
    questions = [row for row in questions if row]
    if "question_examples" in model or topic_id in P0_TOPICS:
        model["question_examples"] = questions
    if "topic_aliases" in model:
        model["topic_aliases"] = list(model.get("routing_aliases", []))
    if "expected_structure" in model:
        model["expected_structure"] = model.get("recommended_outline", [])
    if "high_score_features" in model:
        model["high_score_features"] = model.get("high_score_points", [])
    if "low_score_patterns" in model:
        model["low_score_patterns"] = model.get("common_missing_points", [])
    if "field_connection_points" in model:
        model["field_connection_points"] = model.get("routing_field_points", [])


def migrate(*, write: bool) -> dict[str, Any]:
    assignments: list[dict[str, Any]] = []
    changed_files: list[str] = []
    for pack_dir in sorted(path for path in PACK_ROOT.iterdir() if path.is_dir()):
        paths = {name: pack_dir / name for name in (
            "fact_anchor.json", "model_answer.json", "logic_check.json"
        )}
        fact = _load(paths["fact_anchor.json"])
        model = _load(paths["model_answer.json"])
        logic = _load(paths["logic_check.json"])
        before = {name: json.dumps(value, ensure_ascii=False, sort_keys=True) for name, value in (
            ("fact_anchor.json", fact), ("model_answer.json", model), ("logic_check.json", logic)
        )}

        if pack_dir.name in P0_TOPICS:
            _repair_p0(pack_dir.name, fact, model, logic)

        anchors = [row for row in fact.get("anchors", []) if isinstance(row, dict)]
        patterns = model.get("expected_question_patterns")
        if isinstance(patterns, list):
            curated = CURATED_QUESTION_CONTRACTS.get(pack_dir.name)
            string_count = sum(isinstance(row, str) for row in patterns)
            if string_count and curated is None:
                raise ValueError(f"missing reviewed question contract map: {pack_dir.name}")
            if curated is not None and len(curated) != len(patterns):
                raise ValueError(
                    f"question contract count drift for {pack_dir.name}: "
                    f"expected {len(curated)}, found {len(patterns)}"
                )
            known_anchor_ids = {_anchor_id(row) for row in anchors}
            converted: list[Any] = []
            for index, pattern in enumerate(patterns):
                if not isinstance(pattern, str):
                    if curated is not None and isinstance(pattern, dict):
                        revised = dict(pattern)
                        revised["required_anchor_ids"] = list(curated[index])
                        converted.append(revised)
                    else:
                        converted.append(pattern)
                    continue
                anchor_ids = list(curated[index]) if curated is not None else _rank_anchors(pattern, anchors)
                unknown_refs = set(anchor_ids) - known_anchor_ids
                if not anchor_ids or unknown_refs:
                    raise ValueError(
                        f"invalid reviewed contract for {pack_dir.name}[{index}]: "
                        f"unknown={sorted(unknown_refs)}"
                    )
                converted.append({"pattern": pattern, "required_anchor_ids": anchor_ids})
                assignments.append({
                    "topic_id": pack_dir.name,
                    "pattern": pattern,
                    "required_anchor_ids": anchor_ids,
                })
            model["expected_question_patterns"] = converted

        if pack_dir.name in P0_TOPICS:
            _sync_legacy_model_mirrors(pack_dir.name, model)
        values = {
            "fact_anchor.json": fact,
            "model_answer.json": model,
            "logic_check.json": logic,
        }
        for name, value in values.items():
            after = json.dumps(value, ensure_ascii=False, sort_keys=True)
            if after != before[name]:
                changed_files.append(str(paths[name].relative_to(ROOT)))
                if write:
                    _dump(paths[name], value)

    return {
        "version": "topic_pack_atomicity_repair_v1",
        "mode": "write" if write else "preview",
        "p0_topics": sorted(P0_TOPICS),
        "converted_question_count": len(assignments),
        "changed_files": sorted(set(changed_files)),
        "assignments": assignments,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="apply the reviewed migration")
    args = parser.parse_args()
    print(json.dumps(migrate(write=args.write), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
