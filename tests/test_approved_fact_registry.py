import json
from pathlib import Path

import pytest

from grading.evidence.approved_fact_registry import load_approved_fact_registry
from grading.evidence.fact_grounded_contracts import FactGroundedContractError


ROOT = Path(__file__).resolve().parents[1]


def test_registry_has_only_explicitly_delegated_approved_facts():
    registry = load_approved_fact_registry(ROOT)
    assert len(registry["facts"]) == 1520
    assert len({row["topic_id"] for row in registry["facts"]}) == 84
    linked = [row for row in registry["facts"] if row.get("legacy_anchor_id")]
    assert len({(row["topic_id"], row["legacy_anchor_id"]) for row in linked}) == 1518
    assert "repository_sw_topic_contract_separates_transport_data_integration_and_model_use" not in {
        row["fact_id"] for row in registry["facts"]
    }
    assert "rockwell_5590_firmware_logix_designer_compatibility_example" not in {
        row["fact_id"] for row in registry["facts"]
    }

    resolution = json.loads((ROOT / "reports/displacer_anchor_verification_20261019.json").read_text())
    assert resolution["status"] == "verified" and resolution["score_effect"] == "none"
    assert len(resolution["reviews"]) == 7
    displacer = {row["legacy_anchor_id"]: row for row in linked if row["topic_id"] == "displacer_level_buoyancy_torque_tube_density_interface_calibration"}
    assert set(displacer) == {row["anchor_id"] for row in resolution["reviews"]}
    for row in resolution["reviews"]:
        fact = displacer[row["anchor_id"]]
        assert fact["fact_id"] == row["fact_id"]
        assert {ref["authority_id"] for ref in fact["verification_refs"]} == set(row["authority_ids"])
        assert all(ref["url"].startswith("https://") and ref["locator"] for ref in fact["verification_refs"])
    standalone = next(row for row in registry["facts"] if row["fact_id"] == "liquid_in_glass_thermometer_calibration_is_immersion_condition_specific")
    assert "legacy_anchor_id" not in standalone
    assert ("temperature_measurement_error_heat_transfer", "temperature_error_reduction_measures") in {
        (row["topic_id"], row.get("legacy_anchor_id")) for row in registry["facts"]
    }
    assert registry["approval_record"]["reviewer_id"] == "codex_with_user_delegation"
    assert all(row["score_effect"] == "none" for row in registry["facts"])
    assert all(row["verification_status"] == "verified" for row in registry["facts"])


def test_severe_service_thermal_growth_and_dirty_trim_facts_are_conditioned():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    facts = {row.get("legacy_anchor_id"): row for row in registry["facts"] if row["topic_id"] == topic_id}
    thermal = facts["differential_growth_binding_leakage"]
    assert thermal["verification_status"] == "verified"
    assert thermal["score_effect"] == "none"
    assert "effects_depend_on_material_pair_temperature_geometry_and_constraint" in thermal["relation"]["conditions"]
    assert "D352003X012.pdf" in thermal["verification_refs"][0]["url"]
    dirty_trim = facts["cage_multihole_particle_sensitivity"]
    assert dirty_trim["verification_status"] == "verified"
    assert dirty_trim["score_effect"] == "none"
    assert "the_anchor_requires_review_of_risk_not_a_claim_that_all_multihole_trims_plug" in dirty_trim["relation"]["conditions"]
    assert "D101881X012.pdf" in dirty_trim["verification_refs"][0]["url"]


def test_iiot_information_model_and_digital_thread_facts_are_source_bounded():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    topic_id = "industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread"
    facts = {row.get("legacy_anchor_id"): row for row in registry["facts"] if row["topic_id"] == topic_id}
    expected = {
        "iiot_syntactic_semantic_interoperability",
        "iiot_information_model_asset_relationship",
        "iiot_aas_open_model_optional",
        "iiot_digital_thread_definition",
    }
    assert expected <= set(facts)
    for anchor_id in expected:
        fact = facts[anchor_id]
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"]


def test_alarm_management_definitions_are_conditioned_by_isa_18_lifecycle():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    topic_id = "hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management"
    facts = {row.get("legacy_anchor_id"): row for row in registry["facts"] if row["topic_id"] == topic_id}
    expected = {
        "sw03_alarm_definition",
        "sw03_alarm_philosophy",
        "sw03_alarm_rationalization",
        "sw03_alarm_shelving",
        "sw03_alarm_suppression",
        "sw03_alarm_flood_chattering",
    }
    assert expected <= set(facts)
    for anchor_id in expected:
        fact = facts[anchor_id]
        assert fact["verification_status"] == "verified"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"]


def test_smart_positioner_diagnostics_facts_are_bounded_to_evidence_and_conditions():
    registry = load_approved_fact_registry(ROOT)
    facts = {
        row.get("legacy_anchor_id"): row
        for row in registry["facts"]
        if row["topic_id"] == "smart_positioner_diagnostics_valve_signature_predictive_maintenance"
    }
    expected = {
        "online_monitoring_offline_test_boundary",
        "diagnostic_signal_data_chain",
        "vendor_variable_dictionary_verification",
        "as_left_reference_signature",
        "pressure_band_friction_proxy",
    }
    assert expected <= set(facts)
    for anchor_id in expected:
        assert facts[anchor_id]["verification_status"] == "verified"
        assert facts[anchor_id]["review_status"] == "approved"
        assert facts[anchor_id]["score_effect"] == "none"
        assert facts[anchor_id]["verification_refs"]
    assert "this_fact_is_scoped_to_documented_fieldvue_valvelink_capabilities" in facts["online_monitoring_offline_test_boundary"]["relation"]["conditions"]
    assert "variable_availability_is_model_and_diagnostic_tier_dependent" in facts["diagnostic_signal_data_chain"]["relation"]["conditions"]
    assert "the_estimate_is_not_a_unique_root_cause_diagnosis" in facts["pressure_band_friction_proxy"]["relation"]["conditions"]


def test_industrial_ml_supervised_and_unsupervised_definitions_are_conditioned():
    registry = load_approved_fact_registry(ROOT)
    facts = {
        row["legacy_anchor_id"]: row
        for row in registry["facts"]
        if row["topic_id"] == "industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle"
    }
    assert {"supervised_learning", "unsupervised_learning", "task_type_selection", "anomaly_detection_score_threshold", "predictive_maintenance_scope", "remaining_useful_life_uncertainty", "feature_engineering_context", "representative_data", "class_imbalance", "false_alarm_miss_tradeoff", "explainability_limits", "model_version_traceability", "production_monitoring", "drift_types", "mlops_lifecycle", "deployment_environment", "retraining_trigger"} <= set(facts)
    assert "forecasting_is_supervised_only_when_future_targets_are_defined_in_training_examples" in facts["supervised_learning"]["relation"]["conditions"]
    assert "operational_or_causal_interpretation_requires_domain_validation" in facts["unsupervised_learning"]["relation"]["conditions"]
    assert "forecasting_target_refers_to_future_values_relative_to_prediction_time" in facts["task_type_selection"]["relation"]["conditions"]
    assert "an_outlier_label_does_not_establish_a_physical_fault_cause" in facts["anomaly_detection_score_threshold"]["relation"]["conditions"]
    assert "prediction_is_decision_support_not_a_guarantee_of_failure_prevention" in facts["predictive_maintenance_scope"]["relation"]["conditions"]
    assert "failure_threshold_represents_a_defined_functional_or_end_of_life_condition" in facts["remaining_useful_life_uncertainty"]["relation"]["conditions"]
    assert "feature_window_ends_no_later_than_the_prediction_information_cutoff" in facts["feature_engineering_context"]["relation"]["conditions"]
    assert "the_anchor_examples_are_not_a_universal_exhaustive_required_list" in facts["representative_data"]["relation"]["conditions"]
    assert "class_weighting_and_sampling_are_candidate_methods_not_guaranteed_improvements" in facts["class_imbalance"]["relation"]["conditions"]
    assert "utility_and_operating_constraints_are_application_specific" in facts["false_alarm_miss_tradeoff"]["relation"]["conditions"]
    assert "trustworthiness_characteristics_are_distinct_and_require_their_own_evaluation" in facts["explainability_limits"]["relation"]["conditions"]
    assert "features_threshold_code_and_runtime_environment_are_logged_if_not_automatically_captured" in facts["model_version_traceability"]["relation"]["conditions"]
    assert "monitoring_metrics_are_selected_for_system_context_and_risk" in facts["production_monitoring"]["relation"]["conditions"]
    assert "terminology_varies_across_the_drift_and_dataset_shift_literature" in facts["drift_types"]["relation"]["conditions"]
    assert "the_exact_maturity_level_and_components_depend_on_system_context" in facts["mlops_lifecycle"]["relation"]["conditions"]
    assert "input_schema_preprocessing_and_prediction_api_are_checked_for_the_actual_serving_path" in facts["deployment_environment"]["relation"]["conditions"]
    assert "trigger_selection_and_frequency_depend_on_data_availability_use_case_risk_and_retraining_cost" in facts["retraining_trigger"]["relation"]["conditions"]


def test_smart_positioner_definition_and_calculation_anchors_are_verified_without_claiming_causal_diagnosis():
    registry = load_approved_fact_registry(ROOT)
    facts = {row.get("legacy_anchor_id"): row for row in registry["facts"] if row["topic_id"] == "smart_positioner_diagnostics_valve_signature_predictive_maintenance"}
    expected = {
        "command_travel_error_signed",
        "full_span_travel_error",
        "up_down_hysteresis_signature",
        "baseline_residual_context",
        "rate_of_change_time_domain",
        "accumulated_travel_direction_reversal",
        "actuator_pressure_open_close_band",
    }
    assert expected <= set(facts)
    for anchor_id in expected:
        fact = facts[anchor_id]
        assert fact["verification_status"] == "verified"
        assert fact["score_effect"] == "none"
        assert len(fact["verification_refs"]) == 1
        assert fact["verification_refs"][0]["authority_type"] == "calculation"
    assert 50 - 47 == 3
    assert 100 * (50 - 47) / (100 - 0) == 3
    assert abs(52 - 48) == 4
    assert 1.3 - 1.0 == pytest.approx(0.3)
    assert (5 - 2) / (4 - 1) == 1
    samples = [0, 10, 4, 8]
    assert sum(abs(curr - prev) for prev, curr in zip(samples, samples[1:])) == 20
    assert abs(120 - 108) == 12
    assert "percent_change_domain" not in facts  # denominator convention needs separate review

    pack = json.loads((ROOT / "rubrics/topic_packs/smart_positioner_diagnostics_valve_signature_predictive_maintenance/fact_anchor.json").read_text())
    anchors = {row["anchor_id"]: row for row in pack["anchors"]}
    for anchor_id in expected:
        assert facts[anchor_id]["statement"] == anchors[anchor_id]["statement"]


def test_simple_repairable_system_availability_formula_matches_two_state_derivation():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == "sw01_availability_formula")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "redundant_standby_structure_is_not_included" in fact["relation"]["conditions"]
    assert "scheduled_or_administrative_downtime_is_not_included" in fact["relation"]["conditions"]
    mtbf, mttr = 1000.0, 10.0
    failure_rate, repair_rate = 1 / mtbf, 1 / mttr
    assert repair_rate / (failure_rate + repair_rate) == pytest.approx(mtbf / (mtbf + mttr))


def test_series_parallel_reliability_uses_independence_and_preserves_common_cause_boundary():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == "sw01_series_parallel_reliability")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "common_cause_failure_is_modeled_separately_when_independence_does_not_hold" in fact["relation"]["conditions"]
    r1, r2 = 0.9, 0.8
    assert r1 * r2 == pytest.approx(0.72)
    assert 1 - (1 - r1) * (1 - r2) == pytest.approx(0.98)


def test_reliability_definition_is_time_bounded_and_distinct_from_availability():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == "sw01_reliability_definition")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    evidence = fact["verification_refs"][0]
    assert evidence["authority_id"] == "NIST_IR_8323R1_RELIABILITY_GLOSSARY_DEFINITION"
    assert evidence["url"] == "https://doi.org/10.6028/NIST.IR.8323r1"
    assert "specified time period" in evidence["supports_claim"]
    assert "availability" in fact["relation"]["conditions"][-1]


def test_maintainability_anchor_is_supported_as_contextual_restoration_characteristic():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == "sw01_maintainability_definition")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    refs = {row["authority_id"] for row in fact["verification_refs"]}
    assert refs == {
        "IEC_60300_3_10_2025_MAINTAINABILITY_DESCRIPTION_AND_MEASUREMENT",
        "IEC_60300_3_10_2025_STANDARD_TEXT_SAMPLE",
    }
    assert "accessibility_fault_finding_and_modular_replacement_are_influencing_design_or_process_factors_not_an_exhaustive_list" in fact["relation"]["conditions"]


def test_availability_definition_preserves_metric_context_and_failure_restoration_effects():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == "sw01_availability_definition")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "instantaneous_probability_and_uptime_fraction_are_distinct_measures_not_interchangeable_without_context" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_61703_2016_AVAILABILITY_MEASURES_SCOPE",
        "IEC_60300_3_10_2025_AVAILABILITY_READINESS_AND_UPTIME_RATIO",
    }


def test_common_cause_failure_definition_and_non_exhaustive_examples_are_nrc_supported():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability"
    fact = next(row for row in registry["facts"] if row["topic_id"] == topic_id and row.get("legacy_anchor_id") == "sw01_common_cause_failure")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["relation"]["conditions"] == [
        "failure_or_degradation_affects_two_or_more_components_within_the_analysis_time_window",
        "examples_are_possible_coupling_factors_not_an_exhaustive_or_universal_list",
        "software_common_cause_applies_when_a_shared_latent_defect_or_same_program_affects_multiple_channels",
        "redundancy_does_not_by_itself_eliminate_shared_cause_risk",
    ]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "NRC_AL_98_04_COMMON_CAUSE_EVENT_DEFINITION",
        "NRC_RIS_99_03_CCF_COUPLING_FACTOR_EXAMPLES",
        "NRC_NUREG_1793_CHAPTER_19_SOFTWARE_COMMON_MODE",
        "NRC_ITEM_A30_REDUNDANT_DC_POWER_INDEPENDENCE",
    }
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw01_common_cause_failure")
    assert fact["statement"] == anchor["statement"]


def test_communication_layering_distinguishes_network_medium_from_protocol_and_information_model():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    fact = next(row for row in registry["facts"] if row["topic_id"] == topic_id and row.get("legacy_anchor_id") == "sw07_layered_view")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["relation"]["conditions"] == [
        "the_layer_list_is_an_analysis_framework_and_not_a_single_mandatory_stack_shared_by_all_protocols",
        "protocols_mapped_to_the_same_physical_or_ethernet_network_do_not_automatically_share_application_semantics",
        "profiles_and_information_models_define_protocol_specific_capabilities_and_data_meaning",
        "interoperation_requires_compatible_protocol_support_or_an_explicit_mapping",
    ]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "MODBUS_APPLICATION_PROTOCOL_V1_1B3_LAYER_POSITION",
        "MODBUS_TCP_MESSAGING_IMPLEMENTATION_GUIDE",
        "OPCUA_PART1_SPECIFICATION_LAYERS_PROFILES_INFORMATION_MODELS",
    }
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw07_layered_view")
    assert fact["statement"] == anchor["statement"]


def test_fieldbus_and_opcua_role_facts_are_protocol_scoped_and_source_backed():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    facts = {
        row["legacy_anchor_id"]: row
        for row in registry["facts"]
        if row["topic_id"] == topic_id and row.get("legacy_anchor_id") in {"sw07_fieldbus_concept", "sw07_opcua_role_boundary"}
    }
    assert set(facts) == {"sw07_fieldbus_concept", "sw07_opcua_role_boundary"}
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchors = {row["anchor_id"]: row for row in pack["anchors"]}
    for anchor_id, fact in facts.items():
        assert fact["statement"] == anchors[anchor_id]["statement"] == anchors[anchor_id]["claim"]
        assert fact["verification_status"] == "verified"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"]
    assert "not_every_fieldbus_has_the_same_device_configuration_or_asset_management_functions" in facts["sw07_fieldbus_concept"]["relation"]["conditions"]
    assert "deterministic_timing_depends_on_the_selected_profile_transport_network_and_system_configuration" in facts["sw07_opcua_role_boundary"]["relation"]["conditions"]


def test_device_profile_claim_is_bounded_to_profile_specific_cross_vendor_capabilities():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    fact = next(row for row in registry["facts"] if row["topic_id"] == topic_id and row.get("legacy_anchor_id") == "sw07_device_profile")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["relation"]["conditions"] == [
        "the_profile_defines_class_specific_process_data_parameters_functions_and_diagnostics",
        "mandatory_and_optional_features_are_profile_and_version_specific",
        "interoperability_is_within_the_profile_scope_and_supported_host_features_not_all_vendor_option_combinations",
        "device_profile_does_not_replace_protocol_or_network_conformance",
    ]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "PI_PROFINET_FIELD_DEVICES_APPLICATION_PROFILE_DEFINITION",
        "PI_PROFIdrive_PROFILE_CONFORMANCE_TEST_SCOPE",
    }
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw07_device_profile")
    assert fact["statement"] == anchor["statement"]


def test_classifier_probability_calibration_is_relevant_to_cost_sensitive_thresholds():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle"
    fact = next(row for row in registry["facts"] if row["topic_id"] == topic_id and row.get("legacy_anchor_id") == "calibration_and_uncertainty")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "decision_threshold_depends_on_error_costs_and_consequences_not_calibration_alone" in fact["relation"]["conditions"]
    calibration, derivation = fact["verification_refs"]
    assert calibration["authority_id"] == "SKLEARN_PROBABILITY_CALIBRATION_GUIDE"
    assert derivation["authority_type"] == "calculation"
    c_fp, c_fn, estimated_p, actual_p = 7.0, 3.0, 0.8, 0.5
    threshold = c_fp / (c_fp + c_fn)
    assert threshold == pytest.approx(0.7)
    assert estimated_p >= threshold
    assert (1 - actual_p) * c_fp == pytest.approx(3.5)
    assert actual_p * c_fn == pytest.approx(1.5)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "calibration_and_uncertainty")
    assert fact["statement"] == anchor["statement"]


def test_train_validation_test_roles_preserve_held_out_generalization_assessment():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle"
    fact = next(row for row in registry["facts"] if row["topic_id"] == topic_id and row.get("legacy_anchor_id") == "train_validation_test_separation")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "test_data_remains_untouched_by_model_selection_and_is_reserved_for_final_generalization_assessment" in fact["relation"]["conditions"]
    assert "a_fixed_validation_set_is_not_mandatory_when_cross_validation_is_used_for_selection" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "SKLEARN_CROSS_VALIDATION_MODEL_SELECTION_TRAIN_VALIDATION_TEST",
        "SKLEARN_COMMON_PITFALLS_PREPROCESSING_LEAKAGE",
    }
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "train_validation_test_separation")
    assert fact["statement"] == anchor["statement"]


def test_time_series_group_split_conditions_follow_temporal_and_group_dependence():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle"
    fact = next(row for row in registry["facts"] if row["topic_id"] == topic_id and row.get("legacy_anchor_id") == "chronological_group_split")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "grouped_split_keeps_samples_from_the_same_dependent_group_out_of_both_training_and_test_folds" in fact["relation"]["conditions"]
    assert "the_exact_split_strategy_depends_on_the_intended_deployment_and_generalization_question" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "SKLEARN_TIME_SERIES_CROSS_VALIDATION_DEPENDENCE",
        "SKLEARN_GROUP_CROSS_VALIDATION_DEPENDENT_SAMPLES",
    }
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "chronological_group_split")
    assert fact["statement"] == anchor["statement"]


def test_alarm_deadband_uses_hysteresis_to_reduce_chatter_without_fixed_value_claim():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management"
    anchor_id = "sw03_alarm_deadband"
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ROCKWELL_PROCESS_OBJECTS_ALARM_DEADBAND_NOISY_SIGNAL",
        "EMERSON_OPM2000R_ALARM_DEADBAND_CLEAR_THRESHOLD",
        "ISA_TR18_2_5_DEADBAND_ALARM_STATE_HYSTERESIS",
    }


def test_alarm_priority_uses_consequence_and_allowable_response_time():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management"
    anchor_id = "sw03_alarm_priority"
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_ALARM_RATIONALIZATION_PRIORITY_MATRIX_INPUTS",
        "ISA_TR18_2_2_CONSEQUENCE_RESPONSE_TIME_PRIORITIZATION_METHOD",
        "ISA_ALARM_RATIONALIZATION_DOCUMENTS_CONSEQUENCE_RESPONSE_ACTION",
    }


def test_alarm_acknowledgement_does_not_clear_process_condition():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management"
    anchor_id = "sw03_alarm_state_acknowledgement"
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ROCKWELL_FACTORYTALK_ACKNOWLEDGEMENT_DOES_NOT_CORRECT_CONDITION",
        "ROCKWELL_SLC_ACTIVE_ACKNOWLEDGED_ALARM_REMAINS_ACTIVE_UNTIL_CLEAR",
        "EMERSON_ROSEMOUNT_MON2020_ACTIVE_ACK_STATE_AND_CONDITION_CLEAR",
    }


def test_ml_precision_definition_is_supported_by_official_scikit_learn_docs():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle"
    anchor_id = "precision_metric"
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "SCIKIT_LEARN_PRECISION_SCORE_TP_OVER_TP_FP",
        "SCIKIT_LEARN_MODEL_EVALUATION_BINARY_PRECISION",
    }


@pytest.mark.parametrize(
    ("anchor_id", "expected_authorities"),
    [
        ("recall_metric", {"SCIKIT_LEARN_RECALL_SCORE_TP_OVER_TP_FN", "SCIKIT_LEARN_MODEL_EVALUATION_RECALL_AND_FALSE_NEGATIVES"}),
        ("confusion_matrix", {"SCIKIT_LEARN_BINARY_CONFUSION_MATRIX_OUTCOMES", "SCIKIT_LEARN_CONFUSION_MATRIX_API"}),
        ("f1_metric", {"SCIKIT_LEARN_F1_HARMONIC_MEAN_FORMULA", "SCIKIT_LEARN_MODEL_EVALUATION_METRIC_SELECTION_AND_CONTEXT"}),
    ],
)
def test_ml_classification_metric_facts_match_pack_and_official_docs(anchor_id, expected_authorities):
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle"
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == expected_authorities


def test_environment_temperature_qualification_matches_current_iec_60068_scope():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification"
    anchor_id = "ieeq_temperature_operating_storage"
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_60068_1_2013_TEST_TAILORING_AND_SEVERITY",
        "IEC_60068_2_2_2025_DRY_HEAT_DISSIPATING_STABILITY_USE_STORAGE",
        "IEC_60068_2_1_2025_COLD_HEAT_DISSIPATING_STABILITY_USE_STORAGE",
    }


def test_environment_test_severity_is_traceable_to_intended_use_requirements():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification"
    anchor_id = "ieeq_requirement_traceability"
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_60068_1_2013_TEST_TAILORING_AND_INTENDED_CONDITIONS",
        "IEC_60068_2_2_2025_SPECIMEN_USE_AND_TEST_REPORT_REQUIREMENTS",
    }


def test_vibration_mounting_controls_representative_service_constraints():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification"
    anchor_id = "ieeq_vibration_mounting"
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_60068_2_47_2005_SPECIMEN_MOUNTING_DYNAMIC_TESTS",
        "IEC_60068_2_47_2005_STANDARD_TEXT_PREVIEW_MOUNTING_CABLE_FIXTURE",
        "IEC_60068_2_6_2007_VIBRATION_FIXING_AND_MEASURING_POINTS",
    }


def test_mcdc_industrial_scope_is_classification_dependent_not_universal():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
    anchor_id = "mcdc_industrial_application_boundary"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_61508_3_2010_SCOPE_AND_GRADED_SOFTWARE_MEASURES",
        "NASA_SWE_189_COVERAGE_SELECTION_BY_CLASSIFICATION",
    }


def test_modbus_tcp_mapping_and_configuration_are_specified_by_official_protocol_docs():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_modbus_tcp"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "MODBUS_APPLICATION_PROTOCOL_V1_1B3_TRANSPORT_AND_VENDOR_MAPPING",
        "MODBUS_TCP_MESSAGING_GUIDE_V1_0B_MBAP_UNIT_ID_CONNECTIONS",
    }


def test_hart_overlay_and_device_data_exchange_match_fieldcomm_specifications():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_hart_overlay"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FIELDCOMM_HART_TECHNOLOGY_EXPLAINED_DUAL_CHANNELS",
        "FIELDCOMM_HART_COMMAND_SPECIFICATION_CONFIGURATION_AND_VARIABLE_ACCESS",
    }


def test_hart_multidrop_behavior_is_revision_and_device_specific():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_hart_multidrop"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FIELDCOMM_HART_APPLICATION_GUIDE_R7_1_MULTIDROP",
        "EMERSON_BIFFI_HART_MULTIDROP_MODE_MANUAL",
    }


def test_opc_ua_address_space_services_and_information_model_match_opc_foundation_specs():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_opcua"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "OPC_FOUNDATION_OPC_10000_1_PLATFORM_INDEPENDENT_INFORMATION_MODELS",
        "OPC_FOUNDATION_OPC_10000_3_OBJECT_METHOD_EVENT_MODEL",
        "OPC_FOUNDATION_OPC_10000_4_METHOD_MONITOREDITEM_SUBSCRIPTION_SERVICES",
    }


def test_profibus_pa_profile_bus_power_and_segment_design_are_conditioned_by_pi_sources():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_profibus_pa"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "PROFIBUS_PI_SYSTEM_DESCRIPTION_PA_PROFILE_MBP_AND_DP_PA_COUPLING",
        "PROFIBUS_PI_DESIGN_GUIDELINE_PA_SEGMENT_TERMINATION",
    }


def test_foundation_fieldbus_function_blocks_and_segment_design_match_fieldcomm_guides():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_foundation_fieldbus"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FIELDCOMM_FOUNDATION_FIELD_BUS_TECHNOLOGY_FUNCTION_BLOCKS_DD_DIAGNOSTICS",
        "FIELDCOMM_FOUNDATION_FIELD_BUS_SYSTEM_ENGINEERING_GUIDELINE_SEGMENTS",
    }


def test_foundation_function_block_claim_is_limited_by_host_and_device_support():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_foundation_fieldbus_function_blocks"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FIELDCOMM_FOUNDATION_FUNCTION_BLOCK_APPLICATION_STANDARDIZATION",
        "FIELDCOMM_FOUNDATION_SYSTEM_ENGINEERING_GUIDELINES_BLOCK_HOST_COMPATIBILITY",
    }


def test_serial_communication_separates_framing_interface_and_protocol_addressing():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_serial_communication"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "NI_SERIAL_PORT_COMMUNICATION_FRAMING_AND_INTERFACE_VARIANTS",
        "SIEMENS_SERIAL_TRANSMISSION_DUPLEX_AND_PHYSICAL_DRIVER_SETTINGS",
        "MODBUS_ORG_SERIAL_LINE_RTU_ADDRESS_AND_FRAME_FIELDS",
    }


def test_ethernet_ip_cip_layers_and_scanner_adapter_support_match_odva_guides():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_ethernetip_cip"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ODVA_ETHERNETIP_CIP_OBJECTS_PROFILES_TCPIP_MAPPING",
        "ODVA_ETHERNETIP_SCANNER_ADAPTER_IO_CONNECTION_AND_EDS",
    }


def test_profinet_cyclic_acyclic_diagnostics_and_gsdml_roles_match_pi_documents():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_profinet"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "PI_PROFINET_SYSTEM_DESCRIPTION_CYCLIC_ACYCLIC_ALARMS_GSDML",
        "PI_PROFINET_GSDML_SPEC_AND_CONFORMANCE_CLASS_TESTING",
    }


def test_ethercat_frame_processing_mapping_and_esi_are_device_topology_specific():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_ethercat"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ETG_ETHER_CAT_TECHNOLOGY_FRAME_PROCESSING_AND_TOPOLOGY",
        "ETG_ETHER_CAT_ESI_OFFLINE_CONFIGURATION_PROCESS_DATA",
    }


def test_wirelesshart_mesh_gateway_manager_join_and_host_integration_are_scoped():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_wirelesshart"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FIELDCOMM_WIRELESSHART_MESH_CORE_COMPONENTS_AND_HOST_GATEWAY",
        "FIELDCOMM_WIRELESSHART_SYSTEM_ENGINEERING_GATEWAY_ACCESS_POINT_HOST",
        "FIELDCOMM_WIRELESSHART_JOIN_PROVISIONING_REQUIREMENTS",
    }


def test_asme_b16_34_rating_scope_is_limited_to_the_standardized_valve_construction():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "control_valve_selection_process_pressure_temperature_flow_media_lifecycle"
    anchor_id = "pressure_temperature_rating_and_class"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "ASME_B16_34_2025_OFFICIAL_SCOPE"


def test_wireless_power_lifecycle_has_supported_operational_boundaries():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_wireless_power_lifecycle"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FIELDCOMM_WIRELESSHART_UPDATE_RATE_BATTERY_AND_NETWORK_CAPACITY",
        "FIELDCOMM_WIRELESSHART_DEVICE_POWER_BUDGET_BATTERY_CHEMISTRY_AND_REPLACEMENT",
        "EMERSON_ROSEMOUNT_648_WIRELESS_BATTERY_REFERENCE_CONDITIONS_AND_ROUTING",
    }


def test_wireless_site_survey_covers_rf_environment_and_installed_link_validation():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_wireless_site_survey"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "NIST_AMS_300_4_INDUSTRIAL_WIRELESS_FACTORY_SURVEY_AND_RF_LINK_VALIDATION",
        "FIELDCOMM_WIRELESSHART_SITE_WALKDOWN_AND_COHABITATION_PLANNING",
    }


def test_device_description_formats_are_distinct_ecosystem_specific_integration_artifacts():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_device_description"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FIELDCOMM_EDDL_DEVICE_PARAMETER_FUNCTION_AND_MENU_DESCRIPTION",
        "PI_GSDML_DEVICE_ID_STRUCTURE_COMMUNICATION_PROCESS_DATA_PARAMETERS_DIAGNOSIS",
        "ODVA_CIP_EDS_CONNECTION_AND_PARAMETER_CONFIGURATION",
        "ETG_ETHER_CAT_ESI_OFFLINE_CONFIGURATION_PROCESS_DATA",
    }


def test_min_normal_max_travel_and_control_objective_claim_remains_unresolved_pending_direct_evidence():
    topic_id = "control_valve_selection_process_pressure_temperature_flow_media_lifecycle"
    anchor_id = "minimum_normal_maximum_cases"
    registry = load_approved_fact_registry(ROOT)
    assert (topic_id, anchor_id) not in {
        (row["topic_id"], row.get("legacy_anchor_id")) for row in registry["facts"]
    }
    review = ROOT / "docs/topic_anchor_evidence_followup_20261012_min_normal_max_cases.md"
    assert review.is_file()
    text = review.read_text()
    assert "미검증으로 유지" in text
    assert "required travel" in text
    assert "control objective" in text


def test_isa100_roles_host_integration_and_physical_role_separation_match_sources():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
    anchor_id = "sw07_isa10011a"
    fact = next(
        row for row in registry["facts"]
        if row.get("legacy_anchor_id") == anchor_id and row["topic_id"] == topic_id
    )
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ISA_ISA100_11A_SCOPE_SYSTEM_MANAGEMENT_GATEWAY",
        "YOKOGAWA_ISA100_11A_NETWORK_ROLES_AND_HOST_INTEGRATION",
        "ISA100_11A_ARCHITECTURE_ROLE_SEPARATION_STANDARD_TEXT",
    }


def test_control_valve_low_temperature_review_is_code_and_component_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_low_temperature_service_checks_material_toughness_and_temperature_limit"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "low_temperature_toughness_brittle_fracture")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    conditions = " ".join(fact["relation"]["conditions"])
    assert "not_a_single_universal_rating_for_all_control_valves" in conditions
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ASME_B31_3_PROCESS_PIPING_LOW_TEMPERATURE_SCOPE",
        "ASME_BPVC_MDMT_TOUGHNESS_REQUIREMENTS_OVERVIEW",
        "MSS_SP_134_CRYOGENIC_VALVE_MATERIAL_DESIGN_TEST_SCOPE",
    }


def test_cryogenic_control_valve_extension_bonnet_is_service_sized():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "cryogenic_control_valve_extension_bonnet_protects_packing_from_cold_zone"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "extended_bonnet_packing_isolation")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_CRYOGENIC_EXTENSION_BONNET"
    assert "required_extension_length_and_orientation_depend_on_service_temperature_insulation_and_valve_design" in fact["relation"]["conditions"]


def test_control_valve_thermal_expansion_clearance_is_temperature_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_thermal_expansion_requires_design_temperature_clearance_review"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "thermal_expansion_clearance")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_CVX_THERMAL_TRIM_GROWTH",
        "EMERSON_SEMPELL_STEM_THERMAL_EXPANSION_COMPENSATION",
    }


def test_particle_service_characterization_is_property_and_service_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "slurry_service_characterization_includes_particle_and_carrier_fluid_properties"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "particle_characterization")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "METSO_SLURRY_PROCESS_PARTICLE_CHARACTERIZATION_PARAMETERS",
        "SPRINGER_2022_SOLID_PARTICLE_EROSION_CHARACTERIZATION_REVIEW",
        "NIST_PARTICLE_SIZE_CHARACTERIZATION_SETTLING_AND_CHEMISTRY",
    }
    assert "not_a_universal_erosion_parameter" in " ".join(fact["relation"]["conditions"])


def test_control_valve_high_local_velocity_kinetic_energy_is_not_erosion_rate():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_local_flow_velocity_increases_kinetic_energy_density_and_can_raise_impingement"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "high_flow_kinetic_energy_density")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "MIT_FLUID_KINETIC_ENERGY_DENSITY",
        "WEAR_1997_PARTICLE_IMPACT_ANGLE_EROSION_EXPERIMENTS",
        "VALMET_CONTROL_VALVE_HIGH_VELOCITY_FLASHING_IMPINGEMENT_EROSION",
    }
    assert "does_not_determine_damage_rate_or_location" in " ".join(fact["relation"]["conditions"])


def test_control_valve_downstream_geometry_can_shift_local_damage_and_noise():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_outlet_geometry_and_downstream_piping_shift_local_flow_effects"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "downstream_piping_outlet_effect")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_ATTACHED_FITTINGS_REDUCERS",
        "VALMET_FLOW_CONTROL_MANUAL_DOWNSTREAM_CAVITATION_FLASHING_LOCATION",
        "VALMET_MANIFOLD_DESIGN_FLOW_PROFILE_DISTURBANCE",
        "VALMET_CONTROL_VALVE_VELOCITY_EROSION_NOISE_VIBRATION",
    }
    assert "not_a_universal_prediction_of_peak_location_or_severity" in " ".join(fact["relation"]["conditions"])


def test_microflow_plugging_risk_and_filtering_are_service_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "microflow_passages_require_solids_and_polymer_buildup_risk_review"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "low_flow_plugging_sensitivity")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "SAMSON_TYPE_3510_MICROFLOW_SOLIDS_FILTER_WARNING",
        "VALMET_POLYMERIZATION_CONTROL_VALVE_BUILDUP_APPLICATION_REPORT",
        "VALMET_MULTI_PHASE_SLURRY_PLUGGING_RISK",
    }
    assert "filtration_is_not_universal" in " ".join(fact["relation"]["conditions"])


def test_cavitation_flashing_noise_handoff_has_topic_owners_and_conditional_risk():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_severe_service_risk_includes_cavitation_flashing_and_noise"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "cavitation_flashing_noise_handoff")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert (ROOT / "rubrics/topic_packs/control_valve_cavitation_flashing_choked_flow_damage_prevention").is_dir()
    assert (ROOT / "rubrics/topic_packs/control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim").is_dir()
    assert "not_a_claim_that_all_cavitation_flashing_or_noise_cases_cause_failure" in " ".join(fact["relation"]["conditions"])


def test_control_valve_high_flow_velocity_checks_local_area_and_flow_regime():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_high_flow_velocity_depends_on_local_flow_area_and_volumetric_condition"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "high_flow_velocity_area_relation")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "MISSISSIPPI_STATE_ENGINEERING_FUNDAMENTALS_CONTINUITY_EQUATION",
        "VALMET_FLOW_CONTROL_MANUAL_LIQUID_FLOW_AREA_AND_VENA_CONTRACTA",
        "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_REDUCER_FITTINGS",
    }


def test_control_valve_low_reynolds_flow_uses_applicable_sizing_correction():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_low_reynolds_flow_requires_nonturbulent_sizing_correction"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "low_reynolds_laminar_correction")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_60534_2_1_NON_TURBULENT_FLOW_CORRECTIONS",
        "VALMET_FLOW_CONTROL_MANUAL_REYNOLDS_FACTOR_NON_TURBULENT_FLOW",
    }


def test_control_valve_minimum_controllable_flow_is_application_installed():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_minimum_flow_is_installed_controllability_not_catalog_c_minimum"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "low_flow_minimum_controllable_flow")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "VALMET_CONTROL_VALVE_RANGEABILITY_INHERENT_AND_INSTALLED",
        "VALMET_INSTALLED_FLOW_CHARACTERISTIC_PROCESS_PIPELINE_DEPENDENCE",
        "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_RANGEABILITY_DEFINITION",
    }


def test_cryogenic_control_valve_differential_contraction_is_design_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "cryogenic_valve_differential_contraction_changes_mating_clearance_and_sealing_alignment"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "cryogenic_thermal_contraction")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "NASA_SP_8097_CRYOGENIC_VALVE_THERMAL_TRANSIENT_ALIGNMENT",
        "NASA_CRYOGENIC_CONTROL_VALVE_DIFFERENTIAL_CTE_SEAT_BODY",
        "EMERSON_FISHER_CRYOGENIC_CONTROL_VALVE_DESIGN",
    }


def test_trapped_cryogenic_liquid_cavity_pressure_requires_design_specific_relief():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "trapped_cryogenic_liquid_can_overpressure_enclosed_cavity_when_warmed"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "trapped_liquid_cavity_pressure")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "VALMET_JAMESBURY_BALL_VALVE_CAVITY_PRESSURE_RELIEF_B100",
        "VALMET_JAMESBURY_6FRF_TRAPPED_FLUID_TEMPERATURE_PRESSURE",
        "LAWRENCE_BERKELEY_LAB_CRYOGENIC_TRAPPED_FLUID_RELIEF",
    }


def test_cryogenic_flashing_claim_is_limited_to_phase_conditions():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "cryogenic_fluid_phase_state_can_change_with_heat_leak_and_pressure_reduction"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "cryogenic_vaporization_two_phase")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "VALMET_CONTROL_VALVE_FLASHING_PHASE_CONDITION",
        "LBNL_CRYOGENIC_HEAT_INPUT_BOILOFF_AND_PRESSURE",
        "IEC_60534_2_1_FLUID_PHASE_SIZING_SCOPE",
    }


def test_high_temperature_valve_material_review_is_condition_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_high_temperature_requires_material_strength_and_degradation_review"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "high_temperature_material_strength_oxidation")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ASME_B16_34_PRESSURE_TEMPERATURE_MATERIAL_RATINGS",
        "EMERSON_FISHER_HIGH_TEMPERATURE_CONTROL_VALVE_MATERIAL_SELECTION",
        "NATIONAL_BOARD_HIGH_TEMPERATURE_SCALE_CREEP_OXIDATION",
    }


def test_erosion_corrosion_mechanisms_are_distinguished_and_interaction_is_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "erosion_corrosion_distinguishes_mechanical_and_chemical_loss_with_interaction"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "corrosion_erosion_corrosion")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ASTM_G40_WEAR_EROSION_SCOPE_AND_MECHANICAL_INTERACTION",
        "AMPP_CORROSION_CHEMICAL_ELECTROCHEMICAL_DEFINITION",
        "ASTM_G119_WEAR_CORROSION_SYNERGISM",
    }


def test_slurry_erosion_claim_identifies_parameters_without_universalizing_rates():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "slurry_erosion_depends_on_particle_impact_and_material_parameters"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "slurry_erosion_impingement")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "JMRT_2021_SLURRY_EROSION_IMPACT_PARAMETER_EXPERIMENTS",
        "SAGE_2023_SLURRY_EROSION_PARAMETER_REVIEW",
        "ASTM_G40_MECHANICAL_IMPINGEMENT_EROSION_TERMINOLOGY",
    }


def test_high_flow_erosion_and_vibration_are_condition_dependent():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "high_velocity_can_promote_valve_erosion_and_condition_dependent_flow_vibration_fatigue"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "high_flow_erosion_vibration")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "VALMET_FLOW_CONTROL_MANUAL_VELOCITY_EROSION_CAVITATION_FLASHING",
        "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_FLASHING_EROSION_VELOCITY",
        "ZIADA_2001_HIGH_PRESSURE_PIPING_FLOW_VIBRATION_FATIGUE_CASE",
        "JAEA_HIGH_FLOW_VELOCITY_PIPING_VIBRATION_AND_FATIGUE_LIMIT",
    }


def test_network_latency_definition_matches_one_way_delay_components():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "one_way_network_latency_accumulates_transmission_propagation_and_node_processing_delays"
    )
    topic_id = "industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw08_latency_definition")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IETF_RFC_7928_END_TO_END_DELAY_COMPONENTS",
        "ITU_T_Y2617_PACKET_DELAY_COMPONENTS_AND_SUM",
    }


def test_industrial_cycle_time_claim_separates_application_cycle_and_frame_transfer():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "industrial_cycle_time_distinguishes_periodic_application_and_network_cycles_from_frame_transfer"
    )
    topic_id = "industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw08_cycle_time_definition")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEEE_8021_60802_CYCLE_APPLICATION_NETWORK_TRANSFER_PHASE_USE_CASE",
        "SIEMENS_PROFINET_CYCLIC_UPDATE_SEND_CLOCK_RELATION",
    }


def test_process_response_time_covers_configured_input_to_output_path():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "industrial_process_response_time_spans_input_detection_to_output_action"
    )
    topic_id = "industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw08_response_time_definition")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "SIEMENS_S71500_PROCESS_RESPONSE_TIME_COMPONENTS",
        "SIEMENS_SIRIUS_ACT_EVENT_TO_SENSOR_ACTUATOR_REACTION_TIME",
        "SIEMENS_PROFINET_ISOCHRONOUS_INPUT_PROCESS_OUTPUT_RESPONSE",
    }


def test_hardware_derating_uses_part_and_project_specific_limits():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "hardware_derating_reduces_part_stress_with_application_specific_limits"
    )
    topic_id = "control_hardware_lifecycle_panel_architecture_component_selection_production_verification"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "chl_derating_rule")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert [ref["authority_id"] for ref in fact["verification_refs"]] == [
        "NASA_EEE_INST_002_PART_SPECIFIC_DERATING"
    ]


def test_liquid_valve_hydraulic_power_is_not_misrepresented_as_damage_prediction():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_liquid_hydraulic_power_is_only_a_damage_screening_proxy"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "high_flow_hydraulic_power")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "UF_HYDRAULIC_POWER_PRESSURE_FLOW_RELATION",
        "FISHER_CONTROL_VALVE_HANDBOOK_FLASHING_CAVITATION_DAMAGE_FACTORS",
        "FISHER_CAVITROL_PRESSURE_STAGING_AND_CAVITATION",
    }


def test_staged_pressure_drop_is_conditioned_on_trim_geometry_and_service():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_staged_pressure_drop_is_geometry_dependent_energy_management"
    )
    topic_id = "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "staged_pressure_reduction_distribution")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FISHER_DST_G_STAGED_PRESSURE_DROP_LOWER_ENERGY_JETS",
        "FISHER_CAVITROL_STAGING_AND_STAGE_FLOW_AREA",
    }


def test_quantum_entanglement_claim_preserves_no_signaling_boundary():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "quantum_entanglement_creates_nonclassical_correlations_without_faster_than_light_signaling"
    )
    topic_id = "emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "etc_entanglement_role")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "NIST_BELL_TEST_ENTANGLEMENT_NONLOCAL_CORRELATIONS",
        "NIST_NO_SIGNALLING_ENTANGLEMENT_LIMIT",
    }


def test_quantum_output_sampling_claim_includes_precision_and_postprocessing_cost():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "quantum_measurement_shots_and_classical_aggregation_belong_in_end_to_end_accuracy_and_latency"
    )
    topic_id = "emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "etc_output_sampling_bottleneck")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IBM_QUANTUM_ESTIMATOR_SHOTS_PRECISION_AND_STANDARD_ERROR",
        "IBM_QUANTUM_FINITE_SAMPLING_ERROR_AND_SHOT_COST",
        "IBM_QUANTUM_MEASUREMENT_RESULTS_CLASSICAL_REGISTER",
    }


def test_quantum_computing_definition_is_limited_to_problem_specific_advantage():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "quantum_computing_uses_qubit_states_for_problem_specific_computation"
    )
    pack = json.loads(
        (ROOT / "rubrics/topic_packs" / fact["topic_id"] / "fact_anchor.json").read_text()
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {row["authority_id"] for row in fact["verification_refs"]} == {
        "IBM_QUANTUM_LEARNING_QUBITS_GATES_CIRCUITS",
        "IBM_QUANTUM_LEARNING_APPLICATION_FIT",
    }


def test_digital_twin_fidelity_is_fit_for_purpose_and_validation_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "digital_twin_fidelity_is_fit_for_purpose_and_validation_scope_dependent")
    pack = json.loads((ROOT / "rubrics/topic_packs" / fact["topic_id"] / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "digital_twin_fidelity")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {row["authority_id"] for row in fact["verification_refs"]} == {
        "PEER_REVIEWED_DT_FIT_FOR_PURPOSE_FRAMEWORK",
        "NIST_DIGITAL_TWIN_REQUIREMENTS_VALIDATION_MAINTENANCE",
        "NIST_AM_DIGITAL_TWIN_DATA_FIDELITY",
    }


def test_synthetic_robot_data_claim_is_limited_to_domain_gap_validation():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "synthetic_robot_data_can_cover_rare_cases_but_requires_sim_to_real_validation")
    pack = json.loads((ROOT / "rubrics/topic_packs" / fact["topic_id"] / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "synthetic_data_domain_gap")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {row["authority_id"] for row in fact["verification_refs"]} == {
        "SCIENTIFIC_REPORTS_HYBRID_REAL_SYNTHETIC_ROBOTIC_HAZARDS",
        "FRONTIERS_ROBOT_DOMAIN_RANDOMIZATION_SIM_TO_REAL",
        "ANNUAL_REVIEWS_ROBOTICS_REALITY_GAP",
        "NIST_ROBOTICS_SIM_FIDELITY_REAL_DATA",
    }


def test_robot_localization_claim_is_frame_and_uncertainty_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "robot_localization_estimates_pose_from_sensors_with_method_dependent_uncertainty")
    pack = json.loads((ROOT / "rubrics/topic_packs" / fact["topic_id"] / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "localization")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {row["authority_id"] for row in fact["verification_refs"]} == {
        "WILEY_ROBOT_LOCALIZATION_INTRODUCTION",
        "SE_ROBOT_LOCALIZATION_MAPPING_UNCERTAINTY",
        "ROS_REP_105_MOBILE_PLATFORM_FRAMES",
    }


def test_state_estimation_claim_preserves_observability_limits():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "state_estimator_inference_is_limited_by_model_and_sensor_observability")
    pack = json.loads((ROOT / "rubrics/topic_packs" / fact["topic_id"] / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "observability_limits")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {row["authority_id"] for row in fact["verification_refs"]} == {
        "PEER_REVIEWED_ROBOT_OBSERVABILITY_SENSOR_PLACEMENT",
        "PEER_REVIEWED_UNOBSERVABLE_NONLINEAR_STATE_ESTIMATION",
        "IFAC_OBSERVABILITY_BASED_INERTIAL_SENSOR_PLACEMENT_ROBOTS",
        "PEER_REVIEWED_RGBD_INERTIAL_MOTION_OBSERVABILITY",
    }


def test_quantum_topic_verified_facts_match_their_current_anchor_and_have_evidence():
    registry = load_approved_fact_registry(ROOT)
    expected = {
        "etc_quantum_computing_definition",
        "etc_qubit_vs_classical_bit",
        "etc_superposition_role",
        "etc_measurement_readout",
        "etc_interference_role",
        "etc_gate_model",
        "etc_noise_decoherence",
        "etc_error_mitigation_correction_boundary",
        "etc_annealing_boundary",
        "etc_hybrid_quantum_classical",
        "etc_data_encoding_bottleneck",
        "etc_scale_quality_tradeoff",
        "etc_quantum_sensing_boundary",
    }
    facts = {
        row["legacy_anchor_id"]: row
        for row in registry["facts"]
        if row["topic_id"] == "emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits"
        and row.get("legacy_anchor_id") in expected
    }
    assert set(facts) == expected
    pack = json.loads(
        (ROOT / "rubrics/topic_packs" / "emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits" / "fact_anchor.json").read_text()
    )
    anchors = {row["anchor_id"]: row for row in pack["anchors"]}
    for anchor_id, fact in facts.items():
        assert fact["statement"] == anchors[anchor_id]["statement"] == anchors[anchor_id]["claim"]
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"]


@pytest.mark.parametrize(
    ("fact_id", "anchor_id", "authorities"),
    [
        ("dlr_uses_supervisor_and_ring_nodes_with_beacon_or_announce_fault_recovery", "sw08_dlr", {"ODVA_DLR_GUIDELINES"}),
        ("prp_duplicates_frames_across_two_lans_and_discards_later_copy", "sw08_prp", {"IEC_62439_3_2021", "SIEMENS_PRP_PROTOCOL_MANUAL"}),
        ("hsr_duplicates_frames_in_both_ring_directions_and_nodes_forward_and_discard", "sw08_hsr", {"IEC_62439_3_2021", "SIEMENS_HSR_PRP_GUIDELINES"}),
        ("packet_delay_variation_is_distinct_from_mean_latency_and_reported_with_distribution_metrics", "sw08_jitter_definition", {"IETF_RFC_3393", "IETF_RFC_8238"}),
        ("frame_preemption_suspends_preemptable_frames_for_time_critical_traffic", "sw08_tsn_preemption", {"IEEE_802_1QBU_FRAME_PREEMPTION", "IEEE_802_1QBU_FRAGMENTING_OVERVIEW"}),
        ("throughput_is_a_rate_metric_distinct_from_latency_and_jitter", "sw08_throughput_distinction", {"IETF_RFC_1242", "IETF_RFC_8239"}),
        ("ptp_synchronizes_distributed_clocks_but_does_not_alone_guarantee_deadlines", "sw08_ptp_purpose", {"IEC_61588_2021", "IEEE_802_1AS_TIME_SYNC", "IEEE_802_1QBV_SCHEDULED_TRAFFIC"}),
        ("tsn_is_a_family_of_complementary_ieee_802_1_mechanisms_used_with_profiles_and_end_to_end_configuration", "sw08_tsn_toolbox", {"IEEE_802_1_TSN_STANDARDS_FAMILY", "IEEE_802_1QCI_PER_STREAM_POLICING", "IEEE_802_1QCA_PATH_RESERVATION", "IEC_IEEE_60802_TSN_PROFILE", "IEEE_802_1QAT_STREAM_RESERVATION"}),
        ("ptp_architecture_selects_clock_roles_timing_source_and_holdover_behavior", "sw08_ptp_clock_architecture", {"IEC_61588_2021_CLOCK_SYNC", "CISCO_PTP_CLOCK_ARCHITECTURE_AND_BMCA", "CISCO_PTP_HOLDOVER_CLOCK_CLASS", "CISCO_PTP_BMCA_AND_HOLDOVER_TIMER"}),
        ("ieee_802_1qbv_gate_schedule_design_accounts_for_guard_band_cycle_and_clock_accuracy", "sw08_tsn_qbv", {"IEEE_802_1QBV_SCHEDULED_TRAFFIC", "IEEE_802_1AS_TIME_SYNC", "IEEE_802_1_TSN_GUARD_BAND_TUTORIAL", "TSN_QBV_CYCLIC_SCHEDULE_GUARD_BAND_RESEARCH"}),
        ("clock_synchronization_alone_does_not_establish_deterministic_network_behavior", "sw08_sync_not_determinism", {"IEEE_802_1AS_TIME_SYNC", "IEEE_802_1QBV_SCHEDULED_TRAFFIC", "IEEE_802_1QCI_PER_STREAM_POLICING"}),
    ],
)
def test_industrial_redundancy_facts_match_anchor_and_primary_references(fact_id, anchor_id, authorities):
    topic_id = "industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor_id
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert authorities <= {row["authority_id"] for row in fact["verification_refs"]}


def test_mrp_anchor_with_manager_client_role_claim_is_bounded_to_iec_scope():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience"
    fact = next(row for row in registry["facts"] if row.get("topic_id") == topic_id and row.get("legacy_anchor_id") == "sw08_mrp")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert any(row["authority_id"] == "IEC_62439_2_2021_MRP_RECOVERY" for row in fact["verification_refs"])
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw08_mrp")
    assert "ring manager와 ring client가 상태를 감시" in anchor["statement"]
    assert fact["statement"] == anchor["statement"]


@pytest.mark.parametrize(
    ("fact_id", "anchor_id"),
    [
        ("fault_tree_analysis_decomposes_defined_top_event_with_boolean_logic", "fsrm_fta_top_event"),
        ("minimal_cut_set_is_minimal_basic_event_combination_causing_top_event", "fsrm_minimal_cut_set"),
        ("safety_function_failure_metric_depends_on_demand_mode", "fsrm_demand_mode_metric_selection"),
        ("low_demand_sif_integrity_uses_average_probability_of_failure_on_demand", "fsrm_low_demand_pfdavg"),
        ("high_or_continuous_demand_sif_integrity_uses_dangerous_failure_rate", "fsrm_high_continuous_demand_pfh"),
        ("low_demand_1oo1_pfdavg_is_proportional_to_du_rate_and_test_interval_under_full_test_assumptions", "fsrm_one_oo_one_low_demand_approximation"),
        ("diagnostic_coverage_and_proof_test_coverage_are_distinct_detection_mechanisms", "fsrm_diagnostic_vs_proof_coverage"),
        ("proof_testing_targets_dangerous_failures_not_found_by_online_diagnostics", "fsrm_proof_test_purpose"),
        ("longer_proof_test_interval_increases_latent_failure_exposure_under_constant_rate_model", "fsrm_proof_test_interval_exposure"),
        ("partial_proof_test_leaves_uncovered_failure_modes_for_full_test_or_modeling", "fsrm_partial_test_boundary"),
        ("rbd_represents_system_success_logic_through_functional_paths", "fsrm_rbd_success_path"),
        ("series_and_parallel_rbd_paths_encode_different_success_conditions", "fsrm_rbd_series_parallel"),
        ("markov_reliability_model_uses_system_states_and_transition_rates_to_track_state_probabilities", "fsrm_markov_state_transition"),
        ("markov_state_space_growth_can_increase_analysis_burden_without_universal_growth_rate", "fsrm_markov_complexity"),
        ("common_cause_failures_reduce_redundancy_benefit_under_independence_assumption", "fsrm_ccf_redundancy_impact"),
        ("physical_separation_independent_utilities_and_diversity_are_ccf_mitigation_measures", "fsrm_ccf_reduction_measures"),
        ("fta_rbd_and_markov_models_use_distinct_failure_success_and_state_representations", "fsrm_model_purpose_boundary"),
        ("low_demand_risk_reduction_factor_is_inverse_of_pfdavg_under_defined_sif_metric", "fsrm_rrf_relationship"),
        ("hft_and_voting_architecture_alone_do_not_demonstrate_achieved_sil", "fsrm_hft_not_sil_guarantee"),
        ("complete_sif_reliability_evaluation_includes_all_required_elements_and_utilities", "fsrm_complete_sif_boundary"),
        ("certified_subsystem_sil_does_not_automatically_establish_complete_sif_integrity", "fsrm_component_certificate_limit"),
        ("random_hardware_failure_calculation_does_not_replace_systematic_and_lifecycle_evidence", "fsrm_hardware_systematic_boundary"),
        ("beta_factor_model_partitions_total_rate_into_independent_and_common_cause_contributions", "fsrm_beta_factor"),
        ("pfdavg_approximation_requires_explicit_model_assumptions_and_scope", "fsrm_approximation_conditions"),
        ("sis_reliability_result_records_boundary_mode_and_applicable_model_inputs", "fsrm_model_assumption_documentation"),
        ("sis_voting_architecture_changes_dangerous_failure_and_spurious_trip_tradeoffs", "fsrm_voting_tradeoff"),
    ],
)
def test_functional_safety_reliability_fact_matches_anchor(fact_id, anchor_id):
    topic_id = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor_id
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["verification_refs"]
    assert fact["score_effect"] == "none"


@pytest.mark.parametrize(
    ("fact_id", "anchor_id"),
    [
        ("mcdc_coverage_analysis_traces_artifacts_and_disposes_uncovered_structure", "mcdc_coverage_analysis_workflow"),
        ("uncovered_structural_code_is_analyzed_and_its_disposition_recorded", "mcdc_uncovered_code_disposition"),
        ("static_analysis_complements_but_does_not_supply_execution_coverage_evidence", "mcdc_static_analysis_relation"),
    ],
)
def test_mcdc_fact_matches_pack_anchor(fact_id, anchor_id):
    topic_id = "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor_id
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["verification_refs"]
    assert fact["score_effect"] == "none"


def test_temperature_error_controls_fact_matches_narrowed_pack_anchor():
    topic_id = "temperature_measurement_error_heat_transfer"
    fact_id = "contact_temperature_error_controls_depend_on_immersion_gradients_and_use_conditions"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "temperature_error_reduction_measures")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert len(fact["verification_refs"]) == 2
    assert fact["score_effect"] == "none"


def test_instrumental_drift_fact_matches_vim_scoped_pack_anchor():
    topic_id = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
    fact_id = "instrumental_drift_is_time_change_not_measurand_or_influence_change"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "eem_drift_definition")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert len(fact["verification_refs"]) == 2
    assert fact["score_effect"] == "none"


def test_analog_signal_chain_error_budget_fact_matches_scoped_anchor():
    topic_id = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
    fact_id = "analog_measurement_signal_chain_error_budget_uses_common_reference_point"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "eem_scope_chain")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert len(fact["verification_refs"]) == 2
    assert fact["score_effect"] == "none"


def test_analog_daq_diagnosis_fact_matches_narrowed_pack_anchor():
    topic_id = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
    fact_id = "analog_daq_unexpected_offset_noise_isolated_by_input_and_path_checks"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "eem_diagnosis_chain")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert len(fact["verification_refs"]) == 2
    assert fact["score_effect"] == "none"


def test_measuring_system_verification_fact_matches_scoped_anchor():
    topic_id = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
    fact_id = "measuring_system_verification_compares_indications_under_use_conditions"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "eem_residual_verification")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert len(fact["verification_refs"]) == 2
    assert fact["score_effect"] == "none"


def test_fisher_seat_load_and_overtravel_fact_matches_scoped_anchor():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    fact_id = "fisher_hp_hpa_cseal_overtravel_can_reduce_seat_load_and_damage_trim"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "excessive_seat_load_damage")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert len(fact["verification_refs"]) == 2
    assert fact["score_effect"] == "none"


def test_valve_as_found_as_left_fact_uses_general_comparable_test_basis():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    fact_id = "valve_as_found_as_left_results_require_comparable_test_basis"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "as_found_as_left_leakage")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert len(fact["verification_refs"]) == 3
    assert fact["score_effect"] == "none"
    assert "시험기준의 비교 가능성" in fact["statement"]
    assert "특정 제조사" in anchor["grading_notes"]
    assert "engineering inference" in fact["verification_refs"][2]["supports_claim"]


@pytest.mark.parametrize(
    ("fact_id", "anchor_id"),
    [
        ("functional_safety_audit_reviews_lifecycle_and_management_processes", "audit_role"),
        ("safety_related_competence_uses_role_evidence_and_assessment", "competence_management"),
        (
            "misra_guidelines_are_coding_rules_not_dynamic_unit_test_tools",
            "random_hardware_failure_unit_test_not_random_hardware_integrity__misra_not_unit_test_tool",
        ),
        (
            "functional_safety_diversity_is_ccf_measure_not_guarantee_and_has_complexity_tradeoff",
            "diversity_tradeoff",
        ),
        (
            "iec_61508_tool_qualification_considers_safety_impact_and_error_detection",
            "tool_qualification_basis",
        ),
        (
            "certified_sis_subsystem_evidence_is_limited_to_scope_and_constraints",
            "certified_product_scope",
        ),
        (
            "safety_manual_assumptions_and_proof_test_requirements_enter_sif_design",
            "safety_manual_constraints",
        ),
        (
            "proven_in_use_software_requires_versioned_scope_profile_and_fault_history",
            "proven_in_use_evidence",
        ),
        (
            "functional_safety_pfd_approximation_states_demand_diagnostic_test_repair_and_ccf_assumptions",
            "quantitative_assumptions",
        ),
        (
            "software_module_unit_test_is_not_random_hardware_integrity_evidence",
            "random_hardware_failure__unit_test_not_random_hardware_integrity",
        ),
        (
            "v_model_organizes_software_verification_but_does_not_establish_sif_sil",
            "sis_mcdc_structural_coverage_boundary__vmodel_does_not_guarantee_sil",
        ),
        (
            "siemens_safety_integrated_fblock_reuse_requires_signature_and_version_recheck",
            "library_validation_control",
        ),
    ],
)
def test_sis_sil_software_management_fact_matches_anchor(fact_id, anchor_id):
    topic_id = "sis_sil_safety_software_independence_systematic_failure_verification_validation"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor_id
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["verification_refs"]
    assert fact["score_effect"] == "none"


@pytest.mark.parametrize(
    ("fact_id", "anchor_id"),
    [
        ("control_valve_leakage_requirements_cite_applicable_standard_edition", "standard_edition_exact_citation"),
        ("valve_vendor_purchase_and_acceptance_specs_align_leakage_test_basis", "vendor_purchase_spec_alignment"),
    ],
)
def test_control_valve_leakage_fact_matches_anchor(fact_id, anchor_id):
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor_id
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["verification_refs"]
    assert fact["score_effect"] == "none"


def test_analog_mitigation_fact_rejects_universal_order_and_matches_anchor():
    topic_id = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
    fact_id = "analog_measurement_mitigation_depends_on_chain_and_leaves_residual_uncertainty"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "eem_mitigation_hierarchy")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "does not prescribe a universal mitigation order" in fact["verification_refs"][0]["supports_claim"]


def test_voltage_reference_aging_fact_matches_narrowed_pack_anchor():
    topic_id = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
    fact_id = "voltage_reference_long_term_drift_can_limit_accuracy_before_catastrophic_failure"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "eem_aging_reliability_boundary")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert len(fact["verification_refs"]) == 3
    assert fact["score_effect"] == "none"


def test_error_mitigation_fact_matches_topology_scoped_pack_anchor():
    topic_id = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
    fact_id = "analog_error_mitigation_methods_are_topology_and_error_term_specific"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "eem_auto_zero_ratiometric")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert len(fact["verification_refs"]) == 4
    assert fact["score_effect"] == "none"


def test_pcb_noise_mitigation_fact_matches_topology_scoped_pack_anchor():
    topic_id = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
    fact_id = "pcb_noise_mitigation_is_topology_specific"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "eem_layout_local_mitigation")
    assert fact["topic_id"] == topic_id
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert len(fact["verification_refs"]) == 3
    assert fact["score_effect"] == "none"


def test_cv_kv_foundation_facts_match_pack_and_have_independent_evidence():
    topic_id = "control_valve_sizing_cv_kv_reynolds_liquid_selection"
    registry = load_approved_fact_registry(ROOT)
    facts = [row for row in registry["facts"] if row["topic_id"] == topic_id]
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchors = {row["id"]: row for row in pack["anchors"]}
    expected = {
        "control_valve_cv_is_flow_capacity_not_travel_or_line_size": "cv_flow_capacity_physical_meaning",
        "control_valve_cv_kv_conversion_is_approximate_unit_conversion": "cv_kv_conversion_relation",
        "control_valve_sizing_equation_requires_consistent_units": "unit_system_consistency",
        "control_valve_required_coefficient_increases_with_specific_gravity": "specific_gravity_direction",
    }
    for fact_id, anchor_id in expected.items():
        fact = next(row for row in facts if row["fact_id"] == fact_id)
        assert fact["legacy_anchor_id"] == anchor_id
        assert fact["statement"] == anchors[anchor_id]["statement"] == anchors[anchor_id]["claim"]
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"]
    kv_fact_ids = {row["fact_id"] for row in facts}
    assert "control_valve_kv_reference_definition_verified" not in kv_fact_ids


def test_hazardous_area_classification_selection_facts_are_anchor_bound():
    topic_id = "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection"
    registry = load_approved_fact_registry(ROOT)
    facts = [row for row in registry["facts"] if row["topic_id"] == topic_id]
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchors = {row["id"]: row for row in pack["anchors"]}
    expected = {
        "hazardous_location_classification_uses_atmosphere_likelihood_and_duration": "hazardous_area_classification_release_likelihood",
        "hazardous_gas_zones_are_defined_by_frequency_and_duration": "gas_zone_0_1_2_meaning",
        "hazardous_dust_zones_use_separate_frequency_duration_and_epl_scheme": "dust_zone_20_21_22_meaning",
        "hazardous_area_zone_to_epl_minimum_mapping_gas_and_dust": "zone_epl_mapping",
        "hazardous_area_design_competence_considers_suitability_risk_and_function": "protection_method_risk_matching",
        "hazardous_equipment_selection_checks_all_marking_and_use_conditions": "ex_marking_selection_chain",
        "hazardous_ex_d_contains_internal_explosion_without_claiming_no_ignition": "flameproof_ex_d_principle",
        "hazardous_ex_e_protection_levels_have_distinct_fault_assumptions": "increased_safety_ex_e_principle",
        "hazardous_ex_i_limits_circuit_energy_under_normal_and_abnormal_conditions": "intrinsic_safety_ex_i_principle",
        "hazardous_ex_equipment_environmental_suitability_is_checked_separately": "ex_environmental_suitability_independent_check",
        "hazardous_area_installation_requires_documented_inspection_and_maintenance": "inspection_maintenance_documentation",
        "hazardous_ex_m_encapsulation_and_ex_t_dust_enclosure_are_distinct_principles": "encapsulation_and_dust_enclosure_principle",
        "hazardous_equipment_group_must_be_compatible_with_gas_or_dust_subdivision": "gas_dust_group_compatibility",
        "hazardous_equipment_temperature_marking_is_checked_against_ignition_and_ambient_conditions": "temperature_class_surface_temperature",
        "hazardous_ex_p_uses_purge_overpressure_and_protective_supervision": "pressurization_ex_p_principle",
        "hazardous_intrinsic_safety_levels_ia_ib_ic_have_distinct_fault_assessment": "intrinsic_safety_levels_ia_ib_ic",
        "hazardous_intrinsic_safety_is_an_interconnected_associated_apparatus_cable_system": "is_system_components",
        "hazardous_entity_u_i_p_output_must_not_exceed_field_device_input": "entity_voltage_current_power_compatibility",
        "hazardous_entity_cable_capacitance_and_inductance_are_within_co_lo_limits": "entity_capacitance_inductance_cable",
        "hazardous_zener_and_isolated_barriers_differ_by_grounding_and_galvanic_isolation": "zener_barrier_galvanic_isolator_selection",
        "hazardous_is_wiring_separation_identification_and_shield_grounding_are_design_scoped": "is_wiring_segregation_identification",
    }
    for fact_id, anchor_id in expected.items():
        fact = next(row for row in facts if row["fact_id"] == fact_id)
        assert fact["legacy_anchor_id"] == anchor_id
        assert fact["statement"] == anchors[anchor_id]["statement"] == anchors[anchor_id]["claim"]
        assert fact["verification_status"] == "verified"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"]


def test_hazardous_certificate_and_control_drawing_fact_has_scoped_primary_evidence():
    topic_id = "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection"
    fact_id = "hazardous_certificate_conditions_control_drawing_and_installation_rules_are_distinct"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "certificate_special_conditions_control_drawing")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IECEX_OD_011_2_X_SUFFIX_AND_CABLE_GLAND_BOUNDARY",
        "IECEX_OD_017_CONTROL_DRAWING_CONNECTION_AND_INSTALLATION_INFORMATION",
        "IEC_60079_14_2024_INSTALLATION_SCOPE",
    }


def test_hazardous_ex_e_fact_preserves_eb_ec_fault_assumption_boundary():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "hazardous_ex_e_protection_levels_have_distinct_fault_assumptions")
    assert fact["legacy_anchor_id"] == "increased_safety_ex_e_principle"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_60079_7_2015_AMD1_2017_PROTECTION_LEVELS",
        "NSW_GOVERNMENT_EX_E_ADDITIONAL_MEASURES_AND_EB_EC",
    }


def test_control_valve_reynolds_number_uses_documented_valve_sizing_inputs():
    topic_id = "control_valve_sizing_cv_kv_reynolds_liquid_selection"
    fact_id = "control_valve_sizing_uses_valve_specific_reynolds_equation"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "valve_reynolds_number_meaning")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "FISHER_CATALOG12_VALVE_REYNOLDS_EQUATION_AND_INPUTS"


def test_control_valve_reduced_trim_uses_its_standard_fr_relation():
    topic_id = "control_valve_sizing_cv_kv_reynolds_liquid_selection"
    fact_id = "control_valve_reynolds_correction_uses_separate_reduced_trim_relation"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "small_flow_trim_special_review")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    ref = fact["verification_refs"][0]
    assert ref["authority_id"] == "IEC_60534_2_1_2011_ANNEX_A7_FULL_AND_REDUCED_TRIM_FR"
    assert ref["locator"] == "Annex A.7 and equations (A.6)–(A.8b)"
    assert "full_size_trim_applies_when_c_rated_over_d_squared_n18_is_greater_than_or_equal_to_0_016" in fact["relation"]["conditions"]
    assert "reduced_trim_applies_when_c_rated_over_d_squared_n18_is_less_than_0_016" in fact["relation"]["conditions"]


def test_liquid_sizing_crosscheck_is_limited_to_same_documented_basis():
    topic_id = "control_valve_sizing_cv_kv_reynolds_liquid_selection"
    fact_id = "liquid_sizing_crosscheck_reuses_same_process_and_equation_basis"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "vendor_hand_calculation_crosscheck")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 2
    assert "actual_pressure_drop_across_the_valve_is_used_not_unallocated_system_pressure_drop" in fact["relation"]["conditions"]
    assert "a_difference_triggers_review_of_inputs_assumptions_and_equation_not_automatic_vendor_error" in fact["relation"]["conditions"]


def test_aerodynamic_noise_prediction_is_case_specific_without_universal_matrix():
    topic_id = "control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim"
    fact_id = "aerodynamic_noise_prediction_uses_geometry_and_service_case_inputs"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "operating_case_noise_matrix")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert all(ref["authority_type"] == "official_documentation" for ref in fact["verification_refs"])
    assert "no_universal_fixed_operating_case_matrix_is_claimed_for_every_installation" in fact["relation"]["conditions"]


def test_control_valve_positioner_uses_actual_position_feedback():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "control_valve_positioner_uses_position_feedback_to_modulate_actuator_pressure"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "positioner_closed_loop_position_feedback")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_VALVE_POSITIONER_FEEDBACK_AND_ACTUATOR_PRESSURE",
        "EMERSON_FISHER_3710_3720_POSITIONER_FORCE_BALANCE_FEEDBACK",
    }


def test_stiction_limit_cycle_claim_is_conditional_and_distinguishes_deadband():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "stiction_can_induce_conditional_limit_cycles_deadband_is_not_universal"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "stiction_limit_cycle_path")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "CHOUDHURY_SHAH_THORNHILL_2005_MODELLING_VALVE_STICTION"
    assert "limit_cycle_requires_interaction_with_the_closed_loop_process_and_controller_dynamics_and_is_not_guaranteed_for_every_loop" in fact["relation"]["conditions"]
    assert "pure_deadband_or_backlash_does_not_universally_produce_limit_cycles_in_pi_loops_without_a_plant_integrator" in fact["relation"]["conditions"]


def test_valve_response_time_separates_dead_time_and_dynamic_time():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "control_valve_response_time_separates_dead_time_and_dynamic_time"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "response_time_dead_dynamic_separation")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_DEAD_TIME_DYNAMIC_TIME"


def test_small_step_response_is_not_inferred_from_full_stroke_time():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "small_step_response_assesses_control_region_not_full_stroke_speed"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "small_step_test_control_resolution")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_60534_9_2007_STEP_RESPONSE_TEST_SCOPE",
        "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_SMALL_SIGNAL_VS_STROKING_TIME",
    }


def test_full_stroke_time_is_not_a_pneumatic_fault_diagnosis():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "full_stroke_test_measures_directional_total_travel_time_only"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "large_step_test_pneumatic_capacity")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_FULL_STROKE_TIME_TEST",
        "IEC_60534_9_2007_STEP_RESPONSE_TEST_SCOPE",
    }


def test_positioner_tuning_tradeoff_is_limited_to_documented_dvc6200_sis_guidance():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "dvc6200_sis_tuning_response_adjustment_is_assembly_specific"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "positioner_gain_speed_stability_tradeoff")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_DVC6200_SIS_RESPONSE_TUNING_GUIDANCE"
    assert "no_universal_gain_or_air_consumption_relation_is_inferred_for_other_positioners" in fact["relation"]["conditions"]


def test_dvc6200_sis_relay_capacity_and_tubing_requirements_are_variant_specific():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "dvc6200_sis_relay_capacity_and_tubing_requirements_are_variant_specific"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "pneumatic_supply_tubing_spool_capacity")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_DVC6200_SIS_RELAY_CAPACITY_AND_TUBING_SPECIFICATIONS"
    assert "manual_does_not_establish_a_universal_quantitative_relation_between_tubing_length_or_inside_diameter_and_response_time" in fact["relation"]["conditions"]


def test_fisher_handbook_hunting_claim_is_limited_to_documented_instability_symptom():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "fisher_handbook_defines_hunting_and_positioner_instability_symptom"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "oscillation_requires_differential_diagnosis")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_HUNTING_AND_LOOP_INSTABILITY"
    assert "this_handbook_statement_does_not_identify_the_cause_of_every_field_oscillation_or_exclude_other_causes" in fact["relation"]["conditions"]


def test_fisher_actuator_thrust_example_is_service_and_model_specific():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "fisher_685sr_sizing_requires_available_thrust_to_meet_valve_load"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "positioner_cannot_replace_actuator_thrust")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_685SR_REQUIRED_VS_AVAILABLE_THRUST_SIZING"
    assert "example_force_values_are_not_universal_sizing_constants" in fact["relation"]["conditions"]


def test_fisher_handbook_directional_response_values_are_assembly_specific():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "fisher_handbook_reports_direction_specific_valve_response_time"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "opening_closing_response_asymmetry")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_DIRECTIONAL_RESPONSE_EXAMPLE"
    assert "the_example_does_not_establish_universal_causes_or_asymmetry_magnitude" in fact["relation"]["conditions"]


def test_iec60534_4_dead_band_test_is_distinct_from_hysteresis():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "iec60534_4_dead_band_test_measures_signal_change_on_reversal"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "reversal_test_deadband_hysteresis")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "IEC_60534_4_2021_DEAD_BAND_TEST_AND_HYSTERESIS_DEFINITIONS"
    assert "hysteresis_is_defined_separately_as_direction_sequence_dependent_output" in fact["relation"]["conditions"]


def test_iec60534_9_separates_valve_resolution_from_instrument_resolution():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "iec60534_9_distinguishes_valve_resolution_from_instrument_resolution"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "step_sensitivity_not_resolution_only")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "IEC_60534_9_2007_VALVE_AND_INSTRUMENT_RESOLUTION"
    assert "instrument_resolution_should_be_no_greater_than_one_third_of_valve_resolution_and_preferably_one_tenth" in fact["relation"]["conditions"]


def test_fisher_positioner_feedback_and_actuator_lost_motion_are_separate_functions():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "fisher_positioner_feedback_and_actuator_linkage_lost_motion_are_distinct"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "positioner_cannot_remove_mechanical_backlash")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_3660_POSITIONER_FEEDBACK_MECHANISM",
        "EMERSON_FISHER_1052_ACTUATOR_LINKAGE_LOST_MOTION_REDUCTION",
        "EMERSON_FISHER_1052_ACTUATOR_PRODUCT_DESCRIPTION",
    }
    assert "manufacturer_sources_do_not_claim_positioner_adjustment_physically_eliminates_all_mechanical_clearance" in fact["relation"]["conditions"]


def test_iec60534_9_comparison_claim_separates_standard_tests_from_process_kpis():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "iec60534_9_reproducible_configuration_reporting_and_application_kpis"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "improvement_verify_same_test_and_process_result")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "IEC_60534_9_2007_TEST_CONFIGURATION_AND_PROCESS_VARIABLES"
    assert "quality_energy_and_air_consumption_are_application_selected_kpis_not_a_universal_iec_required_list" in fact["relation"]["conditions"]


def test_fisher_vbl_bypass_separates_large_and_small_signal_behavior():
    topic_id = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    fact_id = "fisher_vbl_booster_bypass_separates_large_and_small_signal_operation"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "volume_booster_flow_capacity_feedback_condition")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_VBL_VOLUME_BOOSTER_MANUAL_D103317X012"
    assert "behavior_is_not_generalized_to_every_volume_booster_design" in fact["relation"]["conditions"]


def test_fisher_packing_facts_match_scoped_manufacturer_evidence():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    registry = load_approved_fact_registry(ROOT)
    facts = [row for row in registry["facts"] if row["topic_id"] == topic_id]
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchors = {row["id"]: row for row in pack["anchors"]}
    expected = {
        "fisher_sourcebook_rotary_packing_motion_comparison": (
            "stem_shaft_packing_leakage_paths",
            "EMERSON_FISHER_CONTROL_VALVE_SOURCEBOOK_ROTARY_PACKING_MOTION",
        ),
        "fisher_sliding_stem_packing_system_selection_and_arrangements": (
            "packing_material_ring_arrangement",
            "EMERSON_FISHER_SLIDING_STEM_PACKING_BULLETIN_2026",
        ),
    }
    for fact_id, (anchor_id, authority_id) in expected.items():
        fact = next(row for row in facts if row["fact_id"] == fact_id)
        assert fact["legacy_anchor_id"] == anchor_id
        assert fact["statement"] == anchors[anchor_id]["statement"] == anchors[anchor_id]["claim"]
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert authority_id in {ref["authority_id"] for ref in fact["verification_refs"]}


def test_fisher_thermal_cycle_claim_matches_eh_eha_product_scope():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    fact_id = "fisher_eh_eha_thermal_cycle_seat_ring_distortion_control"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "thermal_distortion_hot_leakage")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_EH_EHA_TEMPERATURE_CYCLE_SEAT_RING_DESIGN",
        "EMERSON_FISHER_STEAM_CONDITIONING_DIFFERENTIAL_THERMAL_EXPANSION",
    }


def test_epa_method_21_claim_is_limited_to_voc_fugitive_screening():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    fact_id = "epa_method_21_voc_leak_screening_instrument_performance"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "measurement_calibration_detection_uncertainty")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    evidence = fact["verification_refs"][0]
    assert evidence["authority_id"] == "EPA_40_CFR_METHOD_21_CURRENT_INSTRUMENT_PERFORMANCE"
    assert evidence["locator"] == "§§8.1.1.2, 8.1.2–8.1.3, 8.3.1.1"


def test_epa_method_21_background_claim_is_limited_to_type_ii_screening():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    fact_id = "epa_method_21_type_ii_ambient_background_comparison"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "false_pass_false_fail_background")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["locator"] == "§8.3.2, Type II—No Detectable Emission"


def test_special_service_scope_fact_keeps_fire_cryo_and_product_evidence_distinct():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    fact_id = "special_service_valve_sealing_uses_service_specific_test_and_design_scope"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "special_service_sealing_boundary")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ISO_10497_2022_FIRE_TEST_SCOPE_AND_CRITERIA",
        "ISO_21011_2008_CRYOGENIC_VALVE_SCOPE",
        "EMERSON_FISHER_EH_EHA_TEMPERATURE_CYCLE_SEAT_RING_DESIGN",
    }


def test_flashing_noise_anchor_is_limited_to_prediction_method_scope():
    topic_id = "control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim"
    fact_id = "flashing_control_valve_noise_prediction_scope_is_limited"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "flashing_two_phase_noise")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_60534_8_4_2015_HYDRODYNAMIC_NOISE_SCOPE",
        "IEC_60534_8_4_2015_STANDARD_TEXT_PREVIEW",
        "EMERSON_FISHER_SOURCEBOOK_FLASHING_NOISE_PREDICTION_LIMIT",
    }
def test_fisher_bellows_anchor_is_limited_to_documented_product_envelope():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    fact_id = "fisher_bellows_bonnet_seals_stem_and_has_pressure_temperature_cycle_bounds"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "bellows_backup_packing_boundary")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    ref = fact["verification_refs"][0]
    assert ref["authority_id"] == "FISHER_ENVIRO_SEAL_BELLOWS_PRODUCT_BULLETIN_2019"
    assert "claim_is_limited_to_fisher_enviro_seal_bellows_bonnet_documentation" in fact["relation"]["conditions"]


def test_fci_seat_leakage_media_and_reporting_basis_are_class_specific():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    fact_id = "fci_70_2_seat_leakage_results_are_class_medium_and_method_specific"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "gas_liquid_test_medium_difference")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FISHER_CATALOG12_ANSI_FCI70_2_CLASS_MEDIA_AND_LEAKAGE_BASIS",
        "ANSI_FCI_70_2_2021_STANDARD_IDENTITY",
    }


def test_fisher_live_loaded_packing_claim_does_not_assert_maintenance_free():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    fact_id = "fisher_enviro_seal_live_loading_sustains_packing_load_and_reduces_adjustment"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "live_loaded_packing_function")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert "claim_does_not_assert_all_live_loaded_packing_is_maintenance_free_or_universal_constant_load" in fact["relation"]["conditions"]


def test_emerson_feedwater_seat_erosion_fact_preserves_application_boundary():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    fact_id = "fisher_boiler_feedwater_plug_tip_erosion_reduces_shutoff"
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "seat_damage_erosion_wire_drawing")
    assert fact["legacy_anchor_id"] == anchor["id"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_PROTECTED_INSIDE_SEAT_BOILER_FEEDWATER_CASE"
    assert "the_case_does_not_generalize_every_erosion_or_seat_damage_mechanism" in fact["relation"]["conditions"]


def test_garlock_packing_facts_are_scoped_to_documented_installation_and_service_guidance():
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    expected = {
        "garlock_stem_runout_and_misalignment_create_uneven_packing_wear": "misalignment_stem_guide_wear",
        "garlock_stem_surface_damage_increases_packing_leakage_and_wear": "surface_finish_lapping_hardness_coating",
        "garlock_packing_installation_controls_compression_and_follower_alignment": "gland_geometry_compression",
        "garlock_packing_consolidation_can_reduce_gland_load_and_needs_conditioned_adjustment": "packing_consolidation_relaxation",
    }
    registry = load_approved_fact_registry(ROOT)
    facts = {row["fact_id"]: row for row in registry["facts"] if row["topic_id"] == topic_id}
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchors = {row["id"]: row for row in pack["anchors"]}
    for fact_id, anchor_id in expected.items():
        fact = facts[fact_id]
        assert fact["legacy_anchor_id"] == anchor_id
        assert fact["statement"] == anchors[anchor_id]["statement"] == anchors[anchor_id]["claim"]
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"][0]["authority_id"].startswith("GARLOCK_LOW_EMISSION_PACKING_OWNER_MANUAL_")

def test_control_valve_piping_and_complex_fluid_facts_are_anchor_bound():
    topic_id = "control_valve_sizing_cv_kv_reynolds_liquid_selection"
    registry = load_approved_fact_registry(ROOT)
    facts = [row for row in registry["facts"] if row["topic_id"] == topic_id]
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8"))
    anchors = {row["id"]: row for row in pack["anchors"]}
    expected = {
        "control_valve_fp_accounts_for_directly_attached_fittings": "piping_geometry_factor_meaning",
        "control_valve_fp_below_one_reduces_assembly_capacity": "piping_factor_reduces_effective_capacity",
        "control_valve_fp_depends_on_valve_and_attached_geometry": "piping_factor_geometry_dependency",
        "iec_liquid_sizing_scope_excludes_complex_nonnewtonian_and_slurry_services": "complex_fluid_separate_method",
        "control_valve_nonturbulent_trigger_high_viscosity_low_flow_or_low_dp": "viscosity_low_reynolds_trigger",
        "control_valve_selection_fr_below_one_increases_required_cv": "reynolds_factor_correction_direction",
        "control_valve_fr_depends_on_reynolds_and_valve_style_inputs": "reynolds_correction_not_arbitrary_constant",
        "control_valve_selection_repeats_after_selected_style_fl_update": "reynolds_correction_iteration",
        "control_valve_required_and_rated_coefficients_are_distinct": "required_vs_rated_coefficient",
        "control_valve_body_size_and_trim_capacity_are_not_identical": "body_size_vs_trim_capacity",
        "control_valve_min_normal_max_flow_are_evaluated_separately": "minimum_normal_maximum_sizing_points",
        "control_valve_required_capacity_maps_through_selected_characteristic_to_travel": "selected_characteristic_travel_mapping",
        "control_valve_oversizing_can_reduce_low_flow_control_performance": "oversized_valve_selection_consequence",
        "kv_reference_definition_is_water_flow_at_one_bar_with_source_specific_temperature": "kv_reference_definition_metric_units",
        "liquid_valve_sizing_requires_process_fluid_and_operating_case_inputs": "liquid_sizing_input_data",
        "control_valve_reynolds_equation_uses_style_and_passage_modifiers": "valve_style_modifier_dependency",
        "control_valve_corrected_required_capacity_is_checked_against_selected_rated_capacity": "corrected_required_vs_available_trim",
        "control_valve_undersized_capacity_may_fail_maximum_flow_case": "undersized_valve_selection_consequence",
        "liquid_sizing_screens_cavitation_flashing_and_choked_flow_with_pressure_data": "cavitation_flashing_choked_screening",
        "normal_control_valve_travel_target_is_application_specific": "normal_operating_travel_is_conditional",
    }
    for fact_id, anchor_id in expected.items():
        fact = next(row for row in facts if row["fact_id"] == fact_id)
        assert fact["legacy_anchor_id"] == anchor_id
        assert fact["statement"] == anchors[anchor_id]["statement"] == anchors[anchor_id]["claim"]
        assert fact["verification_status"] == "verified"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"]


def test_sw02_state_transition_model_is_verified_with_explicit_determinism_boundary():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "sw02_state_transition_is_deterministic_function_when_all_state_inputs_are_defined")
    pack = json.loads((ROOT / "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw02_state_transition_model")
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert any(ref["authority_id"] == "PLCOPEN_SOFTWARE_CONSTRUCTION_GUIDELINES_STATE_TRANSITIONS" for ref in fact["verification_refs"])
    assert any("determinism_is_a_design_property" in condition for condition in fact["relation"]["conditions"])


def test_sw02_fail_safe_is_application_defined_and_not_universally_deenergized():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "sw02_fail_safe_action_is_application_defined_safe_state")
    pack = json.loads((ROOT / "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw02_fail_safe")
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} >= {
        "HSE_FUNCTIONAL_SAFETY_SAFE_STATE",
        "HSE_CONTROL_SYSTEMS_FAIL_SAFE_TRIPPED_STATE",
        "HSE_ELECTRICAL_SYSTEM_SAFE_STATE_POWER_MAY_BE_NEEDED",
    }
    assert "neither_fail_closed_nor_deenergize_is_universally_safe" in fact["relation"]["conditions"]


def test_sw02_cause_effect_matrix_is_not_runtime_sequential_logic():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "sw02_cause_effect_matrix_documents_relations_not_runtime_sequence_logic")
    pack = json.loads((ROOT / "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw02_cause_effect")
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    evidence = fact["verification_refs"][0]
    assert evidence["authority_id"] == "IEC_62881_2018_CAUSE_EFFECT_MATRIX_SCOPE"
    assert "PLC/DCS" in evidence["supports_claim"]
    assert "matrix_is_not_by_itself_the_implemented_plc_dcs_application_logic" in fact["relation"]["conditions"]


def test_sw02_debounce_and_hysteresis_include_detection_tradeoffs():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "sw02_debounce_hysteresis_reduce_chatter_with_response_time_tradeoff")
    pack = json.loads((ROOT / "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw02_debounce_hysteresis")
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    authorities = {ref["authority_id"] for ref in fact["verification_refs"]}
    assert "ROCKWELL_SEQUENCE_OF_EVENTS_INPUT_CHATTER_DETECTION" in authorities
    assert "SIEMENS_S7_1200_DIGITAL_INPUT_FILTER_TIMES" in authorities
    assert "ADI_COMPARATOR_HYSTERESIS_NOISE_BOUNCE" in authorities
    assert "SIEMENS_G120_SAFETY_INPUT_DEBOUNCE_RESPONSE_TIME" in authorities
    assert "pulse_rejection_and_filter_delay_are_included_in_input_detection_and_protective_response_assessment" in fact["relation"]["conditions"]


def test_mcdc_full_coverage_does_not_stand_in_for_requirements_timing_or_sil_evidence():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "mcdc_full_coverage_is_not_complete_requirements_or_sil_evidence")
    pack = json.loads((ROOT / "rubrics/topic_packs/safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "mcdc_one_hundred_percent_limit")
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    authorities = {ref["authority_id"] for ref in fact["verification_refs"]}
    assert authorities >= {
        "NASA_SWE066_100_PERCENT_COVERAGE_LIMITS",
        "NASA_NPR_7150_2D_SAFETY_CRITICAL_SOFTWARE_REQUIREMENTS",
        "IEC_61511_1_SIS_LIFECYCLE_SCOPE",
    }
    assert "requirements_correctness_and_completeness_are_validated_separately" in fact["relation"]["conditions"]


def test_sw02_manual_mode_preserves_required_hazard_preventing_interlocks():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "sw02_manual_control_does_not_remove_hazard_preventing_protection")
    pack = json.loads((ROOT / "rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw02_manual_mode_boundary")
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    evidence = fact["verification_refs"][0]
    assert evidence["authority_id"] == "HSE_CONTROL_SYSTEMS_MANUAL_SEQUENCE_PROTECTIVE_INTERLOCK_BOUNDARY"
    assert "prevent hazardous actions" in evidence["supports_claim"]
    assert "any_protection_override_is_separately_authorized_and_managed_under_application_safety_requirements" in fact["relation"]["conditions"]


def test_asme_b16_34_fact_is_limited_to_standard_scope():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "asme_b16_34_2025_valve_scope_and_pressure_temperature_ratings")
    topic = json.loads((ROOT / "rubrics/topic_packs/control_valve_selection_process_pressure_temperature_flow_media_lifecycle/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in topic["anchors"] if row["id"] == "pressure_temperature_rating_and_class")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert "the_scope_does_not_make_b16_34_a_universal_rating_standard_for_all_pipe_or_flange_components" in fact["relation"]["conditions"]
    assert fact["verification_refs"][0]["authority_id"] == "ASME_B16_34_2025_OFFICIAL_SCOPE"


def test_emerson_noise_trim_capacity_claim_is_design_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "emerson_noise_trim_capacity_noise_design_specificity")
    pack = json.loads((ROOT / "rubrics/topic_packs/control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "low_noise_trim_capacity_rangeability_tradeoff")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 2
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"


def test_performance_measure_gaming_claim_is_general_and_not_maintenance_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "gao_performance_measure_alignment_balance_and_gaming_risk")
    pack = json.loads((ROOT / "rubrics/topic_packs/control_system_operations_maintenance_calibration_inspection_spares_kpi/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "kpi_gaming_single_metric_tradeoff")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 3


def test_emerson_body_material_claim_stays_within_handbook_scope():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "emerson_body_material_pressure_temperature_corrosion_erosion_tradeoff")
    topic = json.loads((ROOT / "rubrics/topic_packs/control_valve_selection_process_pressure_temperature_flow_media_lifecycle/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in topic["anchors"] if row["id"] == "material_compatibility_and_corrosion")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "the_example_does_not_define_a_universal_material_checklist_for_trim_stem_seat_fasteners_or_all_fluid_chemistries" in fact["relation"]["conditions"]


def test_fci_seat_leakage_benchmark_claim_is_limited_to_defined_test_conditions():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "fci_70_2_defined_test_conditions_seat_leakage_benchmark")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "shutoff_class_purpose_scope")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "FCI_70_2_OFFICIAL_INFORMATIONAL_SHEET"
    assert "claim_is_limited_to_fci_statement_about_defined_test_conditions_and_maximum_allowable_seat_leakage" in fact["relation"]["conditions"]


def test_control_valve_internal_and_external_leakage_paths_are_distinguished():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_internal_seat_and_external_atmospheric_leakage_paths")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "internal_external_leakage_boundary")
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "plug and seat" in fact["verification_refs"][0]["supports_claim"]
    authorities = {ref["authority_id"] for ref in fact["verification_refs"]}
    assert authorities == {
        "SAMSON_T8000_6_CONTROL_VALVE_INTERNAL_EXTERNAL_LEAKAGE_PATHS",
        "EMERSON_CONTROL_VALVE_HANDBOOK_STEM_AND_ROTARY_SHAFT_PACKING",
    }
    assert "manufacturer_documented_body_gasket_and_flanged_joint_paths_are_examples_of_external_paths_not_an_exhaustive_list_for_every_valve_design" in fact["relation"]["conditions"]


def test_local_fugitive_concentration_is_distinct_from_mass_emission_rate():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_local_concentration_is_not_mass_emission_rate")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "concentration_mass_emission_boundary")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "US_EPA_METHOD_21_LOCAL_CONCENTRATION_SCREENING",
        "US_EPA_EQUIPMENT_LEAKS_HIGH_FLOW_MASS_RATE",
    }
    assert "mass_emission_rate_requires_a_flow_basis_and_the_emitted_species_concentration_or_mass_fraction_under_the_method_used" in fact["relation"]["conditions"]


def test_standardized_shutoff_test_does_not_predict_field_leakage_across_conditions():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_shop_test_does_not_predict_field_leakage_across_service_conditions")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "shop_test_field_service_boundary")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    authorities = {ref["authority_id"] for ref in fact["verification_refs"]}
    assert authorities == {
        "EMERSON_FISHER_SOURCEBOOK_SHUTOFF_SERVICE_LEAKAGE_FACTORS",
        "IEC_60534_4_FACTORY_SEAT_LEAKAGE_TEST_LIMIT",
        "EMERSON_FISHER_DIRTY_SERVICE_TRIM_PARTICULATE_SEAT_PROTECTION",
        "EMERSON_FISHER_HIGH_CYCLE_SHUTOFF_TESTING",
    }
    assert "the_claim_does_not_quantify_a_universal_leakage_shift_or_predict_a_specific_installed_valve" in fact["relation"]["conditions"]


def test_balanced_trim_reduces_unbalance_but_has_a_separate_sealed_clearance_path():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "balanced_plug_reduces_unbalance_but_retains_separate_cage_clearance_leakage_path")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "balanced_trim_additional_leakage_path")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_BALANCED_PLUG_FORCE_AND_PISTON_RING_SECONDARY_PATH",
        "EMERSON_FISHER_EH_BORE_SEAL_SECONDARY_PATH",
    }
    assert "the_anchor_says_the_path_can_exist_and_does_not_claim_every_balanced_trim_has_measurable_leakage" in fact["relation"]["conditions"]


def test_soft_and_metal_seat_tradeoffs_are_application_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "soft_and_metal_seats_have_application_specific_leakage_and_service_tradeoffs")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "soft_metal_seat_tradeoff")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    authorities = {ref["authority_id"] for ref in fact["verification_refs"]}
    assert authorities == {
        "EMERSON_FISHER_SOFT_SEAT_SHUTOFF_AND_MATERIAL_LIMITS",
        "EMERSON_FISHER_SOFT_SEAT_TEMPERATURE_AND_ANTIEXTRUSION_LIMITS",
        "EMERSON_FISHER_METAL_SEAT_EROSIVE_SERVICE_AND_HIGH_TEMPERATURE",
        "IEC_60534_4_SEAT_LEAKAGE_CLASS_AND_SURFACE_CONDITION",
    }
    assert "the_anchor_does_not_assert_that_all_soft_seats_leak_less_or_all_metal_seats_are_more_durable" in fact["relation"]["conditions"]


def test_ideal_gas_leakage_reference_conversion_uses_absolute_state_variables():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ideal_gas_leakage_reference_conversion_uses_absolute_pressure_and_temperature")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "ideal_gas_reference_conversion")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "NIST_IDEAL_GAS_EQUATION_OF_STATE"
    assert "the_simple_conversion_assumes_ideal_gas_behavior_or_equal_compressibility_factors_at_the_two_states" in fact["relation"]["conditions"]


def test_foreign_material_can_damage_seating_surfaces_or_prevent_control_valve_shutoff():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_foreign_material_can_damage_seat_or_prevent_shutoff")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "foreign_material_contamination")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_FOREIGN_MATERIAL_SHUTOFF",
        "EMERSON_FISHER_HP_CONTROL_VALVE_PARTICLE_AND_SERVICE_LIMITS",
    }


def test_control_valve_leakage_acceptance_names_class_specific_normalization_basis():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_leakage_class_uses_class_specific_normalization_basis")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "size_normalization_basis")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_CLASS_LEAKAGE_NORMALIZATION",
        "IEC_60534_4_CLASS_MEDIUM_PROCEDURE_AND_LEAKAGE_BASIS",
    }
    assert "the_applied_standard_and_class_define_the_governing_normalization_basis_not_a_free_choice_of_nominal_size_seat_diameter_or_capacity" in fact["relation"]["conditions"]


def test_leakage_reporting_uses_method_specific_volume_mass_or_bubble_rate():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "leakage_reporting_basis_is_method_specific_volume_mass_or_bubble_count")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "volumetric_mass_bubble_basis")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ISO_15848_1_EXTERNAL_LEAK_RATE_MASS_OR_VOLUME",
        "EMERSON_FISHER_CLASS_VI_VOLUME_AND_CALIBRATED_BUBBLE_ALTERNATIVE",
        "IEC_60534_4_SEAT_LEAKAGE_METHOD_SPECIFICATION",
    }


def test_bubble_count_conversion_is_calibrated_and_method_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "bubble_count_conversion_requires_a_calibrated_bubble_volume_and_test_condition")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "bubble_count_conversion")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_CLASS_VI_BUBBLE_DEVICE_GEOMETRY",
        "IEC_60534_4_CLASS_VI_GAS_TEST_AND_STABILIZATION",
    }


def test_seat_leakage_test_state_is_recorded_without_inventing_fixed_hold_time():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "seat_leakage_test_records_defined_pressure_temperature_and_stabilized_observation")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "test_pressure_temperature_duration_stabilization")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "hold_duration_is_determined_by_flow_stabilization_and_measurement_accuracy_not_a_single_universal_time" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_60534_4_TEST_PRESSURE_MEDIUM_TEMPERATURE_AND_STABILIZATION",
        "EMERSON_FISHER_CLASS_LEAKAGE_TEST_CONDITIONS",
    }


def test_seat_contact_geometry_claim_is_limited_to_supported_alignment_and_fit():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_seat_contact_geometry_alignment_and_contact_width")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "seat_contact_geometry")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "specific_contact_geometry_and_width_are_trim_design_and_manufacturer_procedure_dependent_not_a_universal_dimension_or_acceptance_limit" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_PLUG_SEAT_ALIGNMENT",
        "EMERSON_FISHER_SEAT_CONTACT_LAPPING",
        "EMERSON_FISHER_CSEAL_SEATING_SURFACE",
    }


def test_seat_load_contact_stress_claim_limits_average_stress_and_design_scope():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_seat_load_contact_stress_is_geometry_and_service_dependent")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "seat_load_contact_stress_relation")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "nominal_average_stress_is_force_divided_by_the_defined_contact_area_but_actual_local_contact_stress_distribution_is_not_assumed_uniform" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_SEAT_LOAD_AND_CONTACT_AREA",
        "FISHER_SOURCEBOOK_SEAT_LOAD_PRESSURE_UNBALANCE",
        "UIUC_INTRODUCTORY_SOLID_MECHANICS_STRESS",
    }


def test_insufficient_seat_load_claim_is_a_possible_failure_not_a_universal_law():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "insufficient_control_valve_seat_load_can_fail_shutoff_leakage_target")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "insufficient_seat_load_leakage")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "the_claim_is_a_possible_failure_mechanism_not_a_universal_quantitative_leakage_law_or_a_claim_that_more_force_always_improves_field_performance" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FISHER_HPNS_BORE_SEAL_SEATING_FORCE",
        "FISHER_SOURCEBOOK_PRESSURE_UNBALANCE_AND_SEAT_LOAD",
        "FISHER_SEAT_SURFACE_CONDITION_AND_SHUTOFF",
    }


def test_pressure_direction_claim_requires_design_specific_reverse_case_evaluation():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_sealing_and_actuator_load_depend_on_pressure_direction")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "pressure_direction_sealing")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "the_claim_requires_evaluation_of_the_actual_normal_and_reverse_pressure_cases_but_does_not_assert_that_reverse_pressure_always_worsens_leakage" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FISHER_ACTUATOR_SIZING_REVERSE_FLOW",
        "FISHER_HANDBOOK_PRESSURE_UNBALANCE_FORCE",
        "FISHER_26000_PRESSURE_ASSISTED_SEATING",
    }


def test_double_ported_trim_requires_both_seats_contact_and_total_leak_test():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "single_and_double_ported_valves_have_distinct_seat_interfaces_and_leak_paths")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "single_double_seat_leakage_paths")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "the_claim_does_not_assign_a_universal_leak_class_or_identical_leakage_to_all_double_seat_designs" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "FISHER_HANDBOOK_DOUBLE_PORTED_VALVE",
        "FISHER_HS_DOUBLE_PORT_SEAT_ALIGNMENT_AND_LEAKAGE",
    }


def test_cavitation_flashing_damage_is_verified_without_duplicating_topic_8_ownership():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "cavitation_and_flashing_can_damage_control_valve_trim_scope_handoff")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "cavitation_flashing_damage_handoff")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    topic8 = ROOT / "rubrics/topic_packs/control_valve_cavitation_flashing_choked_flow_damage_prevention/fact_anchor.json"
    assert topic8.is_file()
    assert "the_seat_leakage_topic_only_records_the_damage_handoff_and_does_not_replace_topic_8_mechanism_or_prevention_analysis" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FLASHING_DAMAGE_SEAT_TRIM",
        "FISHER_HANDBOOK_CAVITATION_TRIM_DAMAGE",
    }


def test_fugitive_emission_monitoring_anchor_distinguishes_source_ambient_and_screening_scope():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "fugitive_emission_survey_separates_leak_source_ambient_and_method_conditions")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "fugitive_emission_source_monitoring")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "method_21_is_a_screening_and_leak_classification_method_not_a_direct_mass_emission_rate_measurement" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "US_EPA_METHOD_21_SOURCE_POINT_AMBIENT_BOUNDARY",
        "US_EPA_METHOD_21_OFFICIAL_PAGE",
    }


def test_screening_and_bagging_quantification_are_distinct_and_method_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "fugitive_screening_and_bagging_require_distinct_measurement_setups")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "screening_bagging_quantification_methods")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert "screening_values_support_comparison_or_correlation_only_within_compatible_instrument_calibration_species_and_measurement_conditions" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "US_EPA_METHOD_21_SCREENING_NOT_MASS_RATE",
        "US_EPA_EQUIPMENT_LEAK_BAGGING_PROTOCOL",
    }


def test_packing_compression_tradeoff_is_scoped_to_supported_failure_mechanisms():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_packing_compression_leakage_friction_wear_and_actuator_force_tradeoff")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "packing_leakage_friction_tradeoff")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "SAMSON_T8000_6_PACKING_COMPRESSION_FRICTION_AND_ACTUATOR_FORCE",
        "EMERSON_657_ACTUATOR_PACKING_FRICTION_DEADBAND",
        "EMERSON_A11_EXCESSIVE_PACKING_TIGHTENING_WEAR_FRICTION",
    }
    assert "the_claim_is_about_adjustable_packing_and_does_not_assume_leakage_decreases_monotonically_with_compression" in fact["relation"]["conditions"]


def test_packing_leakage_repair_tracks_both_sliding_stem_and_rotary_manual_boundaries():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_packing_leakage_adjustment_replacement_surface_inspection")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "packing_adjustment_replacement_inspection")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_D_DA_SLIDING_STEM_PACKING_LEAKAGE_MAINTENANCE",
        "EMERSON_8540_ROTARY_PACKING_LEAKAGE_MAINTENANCE",
    }
    assert "adjustment_is_limited_to_the_packing_design_and_manufacturer_specified_load_or_torque" in fact["relation"]["conditions"]


def test_packing_leakage_maintenance_is_conditioned_on_model_specific_manual_limits():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_packing_leakage_adjustment_replacement_surface_inspection")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_D_DA_SLIDING_STEM_PACKING_LEAKAGE_MAINTENANCE",
        "EMERSON_8540_ROTARY_PACKING_LEAKAGE_MAINTENANCE",
    }
    assert "avoid_over_tightening_because_it_can_damage_parts_increase_friction_or_accelerate_packing_wear" in fact["relation"]["conditions"]


def test_iso_15848_type_qualification_is_not_a_field_performance_guarantee():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "iso_15848_type_test_does_not_certify_field_packing_performance")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "low_emission_qualification_field_boundary")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "ISO_15848_1_2015_TYPE_TEST_QUALIFICATION_SCOPE"
    assert "the_standard_scope_includes_external_leakage_of_stem_or_shaft_seals_and_body_joints_but_excludes_end_connection_joints_corrosion_effects_and_radiation" in fact["relation"]["conditions"]


def test_seat_leakage_and_external_packing_emission_have_distinct_test_contracts():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "iec_seat_leakage_and_fugitive_packing_acceptance_are_distinct_tests")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "seat_packing_acceptance_separation")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "IEC_60534_4_SEAT_AND_PACKING_TEST_SEPARATION",
        "ISO_15848_1_EXTERNAL_SEAL_EMISSION_METHOD_AND_QUANTITY",
    }
    assert "the_applicable_contract_or_regulation_selects_the_governing_standard_and_acceptance_limits_no_single_unit_or_limit_is_universal" in fact["relation"]["conditions"]


def test_fisher_catalog_class_table_is_limited_to_factory_test_conditions():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "fisher_catalog_12_fci_70_2_factory_test_condition_limits")
    topic_id = "control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "class_test_condition_dependency")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_CATALOG_12_SECTION_2_LEAKAGE_SPECIFICATIONS"
    assert "the_catalog_example_does_not_establish_other_test_variables_as_universal_requirements" in fact["relation"]["conditions"]


def test_nist_ot_security_objectives_anchor_is_limited_to_nist_guidance():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_security_requirements_prioritize_availability_safety_context")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_security_objectives")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "NIST_SP_800_82R3_OT_SECURITY_OBJECTIVES_AND_SAFETY_PERFORMANCE"
    assert "nist_says_availability_is_generally_the_greatest_concern_for_ot_not_that_it_always_supersedes_other_objectives" in fact["relation"]["conditions"]


def test_nist_ot_asset_inventory_claim_is_scoped_to_documented_examples():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_asset_inventory_documentation_scope")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_asset_inventory")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "NIST_SP_800_82R3_OT_ASSET_MANAGEMENT"
    assert "the_source_does_not_make_the_anchor_list_an_exhaustive_mandatory_universal_asset_schema" in fact["relation"]["conditions"]


def test_nist_ot_security_objectives_anchor_matches_fact_anchor_and_logic():
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_security_objectives")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert "process continuity" not in anchor["statement"].lower()


def test_nist_ot_asset_inventory_anchor_matches_fact_anchor_and_logic():
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_asset_inventory")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert "exhaustive" not in anchor["statement"].lower()


def test_nist_ot_risk_assessment_fact_matches_scope_and_source():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_risk_assessment_threat_vulnerability_impact_likelihood")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_risk_assessment")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert "the_claim_does_not_assert_a_universal_numeric_risk_formula_or_specific_residual_risk_acceptance_plan" in fact["relation"]["conditions"]


def test_nist_ot_system_context_fact_does_not_overclaim_iec_62443_terms():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_risk_management_boundary_asset_dataflow_tasks")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_system_under_consideration")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert "the_source_does_not_use_iec_62443_system_under_consideration_or_trust_boundary_as_synonyms_for_these_tasks" in fact["relation"]["conditions"]


def test_iec_62443_3_2_zone_conduit_claim_matches_published_scope_only():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ot_zone_conduit_grouping_and_boundary_enforcement")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_zone_conduit")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "IEC_62443_3_2_2020_OFFICIAL_SCOPE"
    assert "the_claim_does_not_assert_that_zones_and_conduits_are_synonymous_with_trust_boundaries_or_policy_enforcement_devices" in fact["relation"]["conditions"]


def test_nist_ot_segmentation_claim_preserves_performance_and_adjacent_firewall_scope():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_network_segmentation_basis_performance_safety")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_segmentation")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert "the_claim_does_not_assert_that_this_is_an_exhaustive_segmentation_taxonomy_or_that_every_site_requires_identical_physical_partitions" in fact["relation"]["conditions"]


def test_nist_ot_dmz_claim_excludes_universal_intermediary_service_list():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_dmz_prevents_direct_corporate_ot_traffic")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_industrial_dmz")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert "the_claim_does_not_require_historian_relay_patch_staging_or_remote_access_broker_as_universal_dmz_services" in fact["relation"]["conditions"]


def test_nist_data_diode_fact_preserves_hardware_one_way_limit():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_unidirectional_gateway_hardware_one_way_ot_boundary")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_unidirectional_gateway")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert "the_claim_does_not_assert_that_one_way_devices_fit_every_ot_communication_or_maintenance_requirement" in fact["relation"]["conditions"]


def test_nist_allowlisting_anchor_is_limited_to_host_execution_control():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_application_allowlisting_restricts_host_execution")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_allowlisting")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert "the_claim_does_not_assert_update_emergency_change_or_learning_mode_procedures_as_nist_requirements_here" in fact["relation"]["conditions"]


def test_nist_ot_patch_management_anchor_matches_nist_recommendations():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_patch_sandbox_window_recovery_plan")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_patch_management")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert "the_claim_does_not_assert_a_universal_vulnerability_scoring_or_patch_priority_algorithm" in fact["relation"]["conditions"]


def test_nist_ot_firewall_claim_does_not_overstate_default_deny_or_policy_fields():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_firewall_adjacent_authorized_communications")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_firewall_policy")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert "the_claim_does_not_assert_a_universal_default_deny_rule_field_schema_owner_or_expiration_format" in fact["relation"]["conditions"]


def test_nist_ot_logging_claim_is_capability_and_event_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_log_event_identity_source_outcome_fields")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_logging")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert "the_claim_does_not_require_every_ot_device_to_log_all_process_and_recovery_event_categories" in fact["relation"]["conditions"]


def test_nist_ot_time_sync_claim_avoids_specific_protocol_overclaim():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_device_clock_sync_and_timestamp_consistency")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_time_synchronization_forensics")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert "the_claim_does_not_assert_a_specific_protocol_or_universal_timezone_policy" in fact["relation"]["conditions"]


def test_sw06_ot_migration_inventory_claim_matches_nist_scope():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "nist_sp80082_ot_inventory_for_migration_discovery"
    )
    topic_id = "configuration_change_release_backup_rollback_migration_obsolescence_management"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw06_migration_discovery_dependency_inventory")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "NIST_SP80082R3_OT_ASSET_INVENTORY_INTERCONNECTION_AND_CHANGE"
    assert any("not_an_exhaustive_mandatory_migration_checklist_for_all_sites" in value for value in fact["relation"]["conditions"])
    assert "현장별 추가 확인" in anchor["statement"]


def test_sw06_compatibility_check_is_vendor_and_version_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "vendor_product_version_scoped_compatibility_checks_for_migration"
    )
    topic_id = "configuration_change_release_backup_rollback_migration_obsolescence_management"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw06_compatibility_matrix")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 3
    assert "the_examples_do_not_establish_a_universal_exhaustive_matrix_field_list_for_all_ot_migrations" in fact["relation"]["conditions"]
    assert "보편 matrix에 넣어야 한다는 뜻은 아니다" in fact["statement"]


def test_daily_production_management_claim_is_practice_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "daily_production_visual_review_and_action_followup_practice"
    )
    topic_id = "instrumentation_production_management_planning_quality_cost_resources"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "production_daily_management_visual_control")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "NIST_HONEYWELL_FM_AND_T_BALDRIGE_DAILY_OPERATIONS_CASE",
        "LEI_DAILY_MANAGEMENT_VISUAL_CONTROL_AND_ACTION_ACCOUNTABILITY",
        "LEI_MEETING_ACTION_OWNER_DUE_DATE_FOLLOWUP",
    }
    assert "the_sources_describe_practice_and_a_case_not_universal_mandatory_metrics_or_meeting_frequency" in fact["relation"]["conditions"]


def test_critical_spare_fact_is_asset_risk_and_lead_time_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "critical_spare_classification_uses_asset_risk_consequence_and_lead_time"
    )
    topic_id = "control_system_operations_maintenance_calibration_inspection_spares_kpi"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "spares_criticality_classification")
    assert fact["topic_id"] == topic_id
    assert fact["statement"] == anchor["statement"] == anchor["claim"] == anchor["description"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 3
    assert "the_sources_support_risk_factors_and_examples_but_not_one_universal_classification_algorithm" in fact["relation"]["conditions"]


def test_spare_reorder_point_claim_is_scoped_to_documented_inventory_examples():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "spare_reorder_point_accounts_for_demand_lead_time_safety_and_repair_cycle"
    )
    topic_id = "control_system_operations_maintenance_calibration_inspection_spares_kpi"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "spares_stock_policy_reorder_leadtime")
    statement = anchor["statement"]
    assert fact["statement"] == statement == anchor["claim"] == anchor["description"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "GAO_09_103_NAVY_SPARE_INVENTORY_REORDER_POINT",
        "DOE_OIG_24_30_WAPA_LOCAL_CRITICAL_SPARE_REORDER_POINTS",
    }
    assert "the_sources_do_not_establish_a_universal_moq_commonality_or_min_max_rule" in fact["relation"]["conditions"]
    logic = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "logic_check.json").read_text())
    assert statement in logic["llm_profile"]["truth_schema"]
    assert statement in logic["llm_profile"]["safe_conditions"]


def test_limited_shelf_life_spares_claim_is_scoped_to_nasa_lesson():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "nasa_lesson_limited_shelf_life_spares_identify_replace_expired"
    )
    topic_id = "control_system_operations_maintenance_calibration_inspection_spares_kpi"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "spares_preservation_shelf_life_rotation")
    statement = anchor["statement"]
    assert fact["statement"] == statement == anchor["claim"] == anchor["description"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "NASA_LLIS_724_LIMITED_SHELF_LIFE_SPARES"
    assert "this_source_does_not_establish_firmware_license_fifo_or_rotation_checks_for_all_instrument_spares" in fact["relation"]["conditions"]
    logic = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "logic_check.json").read_text())
    assert statement in logic["llm_profile"]["truth_schema"]
    assert statement in logic["llm_profile"]["safe_conditions"]


def test_obsolescence_claim_is_vendor_lifecycle_and_ot_change_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "vendor_product_lifecycle_status_and_ot_change_control_for_obsolescence"
    )
    topic_id = "control_system_operations_maintenance_calibration_inspection_spares_kpi"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "spares_obsolescence_substitution_moc")
    statement = anchor["statement"]
    assert fact["statement"] == statement == anchor["claim"] == anchor["description"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "NI_HARDWARE_PRODUCT_LIFECYCLE_POLICIES",
        "NIST_SP_800_82R3_OT_CONFIGURATION_CHANGE_CONTROL",
    }
    assert "the_sources_do_not_define_one_universal_substitution_checklist_or_sequence" in fact["relation"]["conditions"]
    logic = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "logic_check.json").read_text())
    assert statement in logic["llm_profile"]["truth_schema"]
    assert statement in logic["llm_profile"]["safe_conditions"]


def test_sw06_data_conversion_claim_is_scoped_to_hhs_guide():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "hhs_data_conversion_mapping_test_and_reconciliation_practice"
    )
    topic_id = "configuration_change_release_backup_rollback_migration_obsolescence_management"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw06_data_configuration_transformation_validation")
    statement = anchor["statement"]
    assert fact["statement"] == statement == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "HHS_EPLC_DATA_CONVERSION_PRACTICES_GUIDE_V1"
    assert "the_guide_is_it_data_conversion_practice_guidance_not_a_universal_ot_standard" in fact["relation"]["conditions"]
    logic = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "logic_check.json").read_text())
    assert statement in logic["llm_profile"]["truth_schema"]


def test_sw06_migration_mode_claim_is_scoped_to_hhs_project_planning_example():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "hhs_data_conversion_execution_mode_planning_choices"
    )
    topic_id = "configuration_change_release_backup_rollback_migration_obsolescence_management"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw06_migration_strategy_selection")
    statement = anchor["statement"]
    assert fact["statement"] == statement == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "HHS_EPLC_DATA_CONVERSION_PRACTICES_GUIDE_V1"
    assert "these_are_project_specific_planning_choices_not_a_universal_ot_migration_method_or_optimization_formula" in fact["relation"]["conditions"]
    logic = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "logic_check.json").read_text())
    assert statement in logic["llm_profile"]["truth_schema"]


def test_sw06_cutover_preparation_claim_is_scoped_to_hhs_it_guide():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "hhs_data_conversion_cutover_preparation_and_backup_example"
    )
    topic_id = "configuration_change_release_backup_rollback_migration_obsolescence_management"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw06_cutover_freeze_gonogo")
    statement = anchor["statement"]
    assert fact["statement"] == statement == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "HHS_EPLC_DATA_CONVERSION_PRACTICES_GUIDE_V1"
    assert "this_does_not_define_universal_ot_freeze_approval_contact_go_no_go_or_process_safety_checklists" in fact["relation"]["conditions"]
    logic = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "logic_check.json").read_text())
    assert statement in logic["llm_profile"]["truth_schema"]


def test_sw06_post_conversion_claim_is_limited_to_data_validation_scope():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "hhs_data_conversion_post_conversion_validation_scope"
    )
    topic_id = "configuration_change_release_backup_rollback_migration_obsolescence_management"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw06_post_cutover_stabilization_decommission")
    statement = anchor["statement"]
    assert fact["statement"] == statement == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "HHS_EPLC_DATA_CONVERSION_PRACTICES_GUIDE_V1"
    assert "legacy_control_system_retention_or_decommission_criteria_are_not_defined_by_this_guide" in fact["relation"]["conditions"]
    logic = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "logic_check.json").read_text())
    assert statement in logic["llm_profile"]["truth_schema"]


def test_sw06_emergency_change_claim_is_scoped_to_osha_psm_moc():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "osha_psm_scoped_management_of_change_requirements"
    )
    topic_id = "configuration_change_release_backup_rollback_migration_obsolescence_management"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw06_emergency_change_retrospective_control")
    statement = anchor["statement"]
    assert fact["statement"] == statement == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "OSHA_1910_119_L_MANAGEMENT_OF_CHANGE"
    assert "the_regulation_does_not_create_a_general_emergency_change_exemption_or_universal_ot_backup_checklist" in fact["relation"]["conditions"]
    logic = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "logic_check.json").read_text())
    assert statement in logic["llm_profile"]["truth_schema"]


def test_control_valve_noise_assessment_scope_is_scoped_and_evidenced():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_noise_assessment_integrates_mechanism_path_mitigation_and_verification"
    )
    pack_path = ROOT / "rubrics/topic_packs/control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim/fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "control_valve_noise_scope")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 6
    conditions = set(fact["relation"]["conditions"])
    assert "this_is_an_engineering_assessment_framework_not_a_claim_that_one_standard_mandates_a_fixed_universal_workflow" in conditions
    assert "aerodynamic_and_hydrodynamic_noise_methods_apply_to_different_flow_mechanisms_and_have_distinct_scope" in conditions
    assert "field_measurement_is_used_for_validation_when_required_or_appropriate_and_is_not_assumed_to_be_part_of_every_prediction" in conditions


def test_control_valve_noise_source_path_receiver_accounting_is_scoped_and_evidenced():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_noise_source_path_receiver_accounting"
    )
    pack_path = ROOT / "rubrics/topic_packs/control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim/fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "source_path_receiver_hierarchy")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 3
    conditions = set(fact["relation"]["conditions"])
    assert "source_path_receiver_is_a_system_analysis_framework_not_a_universal_sequence_of_mandatory_controls" in conditions
    assert "overlapping_or_interacting_treatments_are_not_assumed_to_have_independent_additive_attenuation" in conditions


def test_control_valve_noise_vendor_crosscheck_is_method_and_case_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_noise_vendor_result_crosscheck_fields"
    )
    pack_path = ROOT / "rubrics/topic_packs/control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim/fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "vendor_crosscheck_noise")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 3
    conditions = set(fact["relation"]["conditions"])
    assert "crosscheck_fields_are_required_as_applicable_to_the_selected_method_and_service_not_as_a_universal_vendor_report_template" in conditions
    assert "aerodynamic_and_hydrodynamic_results_use_distinct_methods_and_are_not_interchanged" in conditions


def test_control_valve_noise_trim_dirty_service_review_is_service_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_noise_trim_dirty_service_compatibility_review"
    )
    pack_path = ROOT / "rubrics/topic_packs/control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim/fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "plugging_erosion_maintenance_tradeoff")
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 3
    conditions = set(fact["relation"]["conditions"])
    assert "this_is_a_selection_and_design_review_requirement_not_a_claim_that_every_small_passage_or_multistage_trim_will_plug_or_erode" in conditions
    assert "dirty_service_trim_examples_do_not_establish_that_a_noise_attenuation_trim_has_the_same_geometry_or_particulate_rating" in conditions


def test_maintenance_inspection_and_functional_check_fact_is_scoped_and_evidenced():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "maintenance_program_separates_routine_inspection_and_functional_checks"
    )
    pack_path = ROOT / "rubrics/topic_packs/control_system_operations_maintenance_calibration_inspection_spares_kpi/fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(
        row for row in pack["anchors"]
        if row["anchor_id"] == "inspection_program_routine_functional_loop"
    )
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {
        "ISA_IEC_62382_LOOP_CHECK_SCOPE_2026",
        "OSHA_1910_119_APP_C_MECHANICAL_INTEGRITY_INSPECTION_TEST_SCOPE",
        "NASA_RCM_AUTOMATIC_VALVE_INSPECTION_AND_OPERATION_CHECK",
    } == {row["authority_id"] for row in fact["verification_refs"]}


def test_maintenance_kpi_catalog_and_contextual_definitions_are_evidenced():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "maintenance_reliability_kpi_catalog_and_definitions_are_scoped"
    )
    pack_path = ROOT / "rubrics/topic_packs/control_system_operations_maintenance_calibration_inspection_spares_kpi/fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(
        row for row in pack["anchors"]
        if row["anchor_id"] == "kpi_pm_compliance_backlog_schedule"
    )
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert {row["authority_id"] for row in fact["verification_refs"]} == {
        "SMRP_BEST_PRACTICES_METRIC_CATALOG_AND_METHOD",
        "DOE_FEMP_OM_GUIDE_MAINTENANCE_METRIC_FORMULAS",
    }


def test_sw06_as_built_and_ot_backup_claim_is_scoped_and_evidenced():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "sw06_as_built_documentation_and_ot_backup_reconciliation"
    )
    assert fact["legacy_anchor_id"] == "sw06_as_built_consistency"
    assert fact["verification_status"] == "verified"
    assert len(fact["verification_refs"]) == 3
    assert "backup_is_a_time_specific_recovery_copy_and_is_not_assumed_identical_to_current_online_state" in fact["relation"]["conditions"]
    pack_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/fact_anchor.json"
    logic_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/logic_check.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    logic = json.loads(logic_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]
    assert fact["statement"] in logic["llm_profile"]["truth_schema"]


def test_sw06_backup_scope_is_asset_specific_and_nist_sourced():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "sw06_ot_backup_scope_is_asset_and_recovery_objective_specific"
    )
    assert fact["legacy_anchor_id"] == "sw06_backup_scope_and_consistency"
    assert fact["verification_status"] == "verified"
    assert any(ref["authority_id"] == "NIST_SP_1339_OT_BACKUP_QUICK_START" for ref in fact["verification_refs"])
    assert "backup_scope_and_frequency_are_defined_per_asset_and_risk_not_as_one_universal_file_list" in fact["relation"]["conditions"]
    pack_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]


def test_sw06_moc_claim_separates_psm_requirement_from_ot_guidance():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "sw06_moc_is_scoped_to_psm_covered_changes_and_ot_guidance"
    )
    assert fact["legacy_anchor_id"] == "sw06_moc_trigger_and_scope"
    authorities = {ref["authority_id"] for ref in fact["verification_refs"]}
    assert "OSHA_29_CFR_1910_119_L_PSM_MOC" in authorities
    assert "NIST_SP_800_82R3_OT_CHANGE_DOCUMENT_TEST_APPROVE" in authorities
    assert "replacement_in_kind_is_excluded_from_the_psm_moc_requirement" in fact["relation"]["conditions"]
    pack_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/fact_anchor.json"
    logic_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/logic_check.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    logic = json.loads(logic_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]
    assert fact["statement"] in logic["llm_profile"]["truth_schema"]


def test_sw06_change_impact_review_is_requirement_and_dependency_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "sw06_change_impact_review_is_requirement_and_dependency_scoped"
    )
    assert fact["legacy_anchor_id"] == "sw06_impact_analysis_multidisciplinary"
    assert len(fact["verification_refs"]) == 3
    assert "candidate_impact_elements_are_not_an_identical_mandatory_checklist_for_every_change" in fact["relation"]["conditions"]
    pack_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/fact_anchor.json"
    logic_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/logic_check.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    logic = json.loads(logic_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]
    assert fact["statement"] in logic["llm_profile"]["truth_schema"]


def test_sw06_change_plan_is_not_a_universal_fixed_checklist():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "sw06_change_execution_plan_is_requirement_and_risk_scoped"
    )
    assert fact["legacy_anchor_id"] == "sw06_change_implementation_plan"
    assert "no_universal_identical_execution_plan_checklist_is_claimed" in fact["relation"]["conditions"]
    pack_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/fact_anchor.json"
    logic_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/logic_check.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    logic = json.loads(logic_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]
    assert fact["statement"] in logic["llm_profile"]["truth_schema"]


def test_sw06_regression_testing_is_scoped_and_source_bounded():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "sw06_regression_test_selection_is_change_impact_and_risk_scoped"
    )
    assert fact["legacy_anchor_id"] == "sw06_risk_based_regression"
    assert len(fact["verification_refs"]) == 2
    assert "no_identical_fixed_test_list_is_claimed_for_every_ot_change" in fact["relation"]["conditions"]
    pack_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/fact_anchor.json"
    logic_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/logic_check.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    logic = json.loads(logic_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]
    assert fact["statement"] in logic["llm_profile"]["truth_schema"]


def test_sw06_rollback_requirements_are_not_a_universal_checklist():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "sw06_rollback_requirements_are_change_and_procedure_scoped"
    )
    assert fact["legacy_anchor_id"] == "sw06_rollback_preplanned_criteria"
    assert len(fact["verification_refs"]) == 2
    assert "not_every_change_is_asserted_to_be_reversible_or_to_require_rollback" in fact["relation"]["conditions"]
    pack_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/fact_anchor.json"
    logic_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/logic_check.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    logic = json.loads(logic_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]
    assert fact["statement"] in logic["llm_profile"]["truth_schema"]


def test_sw06_restore_and_rollback_are_distinct_but_can_be_combined():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "sw06_restore_and_rollback_are_distinct_recovery_concepts"
    )
    assert fact["legacy_anchor_id"] == "sw06_restore_rollback_distinction"
    assert len(fact["verification_refs"]) == 2
    pack_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/fact_anchor.json"
    logic_path = ROOT / "rubrics/topic_packs/configuration_change_release_backup_rollback_migration_obsolescence_management/logic_check.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    logic = json.loads(logic_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]
    assert fact["statement"] in logic["llm_profile"]["truth_schema"]


    acoustic_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim"}
    assert {"acoustic_power_pipe_radiation_path", "multi_hole_jet_division", "silencer_insulation_enclosure_path_treatment", "multi_stage_pressure_ratio_velocity_control", "aerodynamic_turbulent_jet_noise", "cavitation_bubble_collapse_noise", "aerodynamic_expansion_shock_noise", "gas_choked_regime_noise_input", "gas_outlet_velocity_mach_geometry", "external_spl_observation_condition", "process_flow_vs_accessory_noise", "field_measurement_background_correction", "prediction_standard_vendor_method", "hydrodynamic_turbulence_noise", "occupational_limit_local_standard", "valve_size_capacity_velocity_tradeoff"} <= set(acoustic_facts)
    assert all(acoustic_facts[key]["score_effect"] == "none" for key in ("acoustic_power_pipe_radiation_path", "multi_hole_jet_division", "silencer_insulation_enclosure_path_treatment", "multi_stage_pressure_ratio_velocity_control"))
    absolute_temperature = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_gas_sizing_uses_absolute_upstream_temperature"
    )
    assert absolute_temperature["legacy_anchor_id"] == "absolute_temperature_required"
    assert len(absolute_temperature["verification_refs"]) == 2
    assert absolute_temperature["score_effect"] == "none"
    optical_ultrasonic = next(row for row in registry["facts"] if row["fact_id"] == "optical_vs_ultrasonic_tof_comparison")
    assert optical_ultrasonic["legacy_anchor_id"] == "optical_vs_ultrasonic_tof_comparison"
    assert len(optical_ultrasonic["verification_refs"]) == 5
    assert "tank_ullage_gas_sound_speed_conditions_are_limited_to_gas_type_temperature_and_vapor_pressure" in optical_ultrasonic["relation"]["conditions"]
    assert optical_ultrasonic["score_effect"] == "none"
    multipath = next(row for row in registry["facts"] if row["fact_id"] == "multipath_mixed_pixel_error")
    assert multipath["legacy_anchor_id"] == "multipath_mixed_pixel_error"
    assert len(multipath["verification_refs"]) == 2
    assert "the_error_is_scene_and_sensor_dependent_and_no_universal_direction_or_magnitude_is_claimed" in multipath["relation"]["conditions"]
    assert multipath["score_effect"] == "none"
    specular_transparent = next(row for row in registry["facts"] if row["fact_id"] == "specular_transparent_surface_error")
    assert specular_transparent["legacy_anchor_id"] == "specular_transparent_surface_error"
    assert len(specular_transparent["verification_refs"]) == 2
    assert "no_universal_error_direction_or_behavior_is_claimed_across_optical_sensor_types" in specular_transparent["relation"]["conditions"]
    assert specular_transparent["score_effect"] == "none"
    calibration = next(row for row in registry["facts"] if row["fact_id"] == "laser_triangulation_calibration_and_recalibration_are_condition_dependent")
    assert calibration["legacy_anchor_id"] == "calibration_reference_traceability"
    assert len(calibration["verification_refs"]) == 3
    assert "no_universal_fixed_recalibration_interval_or_lens_contamination_claim_is_made" in calibration["relation"]["conditions"]
    assert calibration["score_effect"] == "none"
    optical_pack_dir = ROOT / "rubrics/topic_packs/optical_laser_photoelectric_noncontact_measurement_tof_triangulation"
    optical_pack = json.loads((optical_pack_dir / "fact_anchor.json").read_text(encoding="utf-8"))
    optical_anchor = next(row for row in optical_pack["anchors"] if row["id"] == "multipath_mixed_pixel_error")
    assert optical_anchor["statement"] == multipath["statement"]
    specular_anchor = next(row for row in optical_pack["anchors"] if row["id"] == "specular_transparent_surface_error")
    assert specular_anchor["statement"] == specular_transparent["statement"]
    calibration_anchor = next(row for row in optical_pack["anchors"] if row["id"] == "calibration_reference_traceability")
    assert calibration_anchor["statement"] == calibration["statement"]
    assert calibration_anchor["claim"] == calibration["statement"]
    optical_logic = json.loads((optical_pack_dir / "logic_check.json").read_text(encoding="utf-8"))
    assert multipath["statement"] in optical_logic["llm_profile"]["safe_conditions"]
    assert calibration["statement"] in optical_logic["llm_profile"]["truth_schema"]
    received_signal = next(row for row in registry["facts"] if row["fact_id"] == "optical_range_received_signal_low_level_noise_and_saturation_limits")
    assert received_signal["legacy_anchor_id"] == "detector_saturation_dynamic_range"
    assert len(received_signal["verification_refs"]) == 3
    assert "no_generic_noise_floor_value_or_universal_snr_threshold_is_claimed" in received_signal["relation"]["conditions"]
    assert received_signal["score_effect"] == "none"
    received_signal_anchor = next(row for row in optical_pack["anchors"] if row["id"] == "detector_saturation_dynamic_range")
    assert received_signal_anchor["statement"] == received_signal["statement"]
    assert received_signal_anchor["claim"] == received_signal["statement"]
    assert received_signal["statement"] in optical_logic["llm_profile"]["truth_schema"]
    wavelength = next(row for row in registry["facts"] if row["fact_id"] == "photoelectric_target_response_depends_on_wavelength_and_material")
    assert wavelength["legacy_anchor_id"] == "wavelength_material_selection"
    assert len(wavelength["verification_refs"]) == 2
    assert "no_single_visible_or_infrared_wavelength_is_claimed_best_for_all_targets" in wavelength["relation"]["conditions"]
    assert wavelength["score_effect"] == "none"
    wavelength_anchor = next(row for row in optical_pack["anchors"] if row["id"] == "wavelength_material_selection")
    assert wavelength_anchor["statement"] == wavelength["statement"]
    assert wavelength_anchor["claim"] == wavelength["statement"]
    assert wavelength["statement"] in optical_logic["llm_profile"]["truth_schema"]
    optical_selection = next(row for row in registry["facts"] if row["fact_id"] == "optical_method_selection_is_application_specific")
    assert optical_selection["legacy_anchor_id"] == "optical_method_selection_tradeoff"
    assert len(optical_selection["verification_refs"]) == 3
    assert "no_sensor_method_is_claimed_optimal_for_every_range_target_and_environment" in optical_selection["relation"]["conditions"]
    assert optical_selection["score_effect"] == "none"
    optical_selection_anchor = next(row for row in optical_pack["anchors"] if row["id"] == "optical_method_selection_tradeoff")
    assert optical_selection_anchor["statement"] == optical_selection["statement"]
    assert optical_selection_anchor["claim"] == optical_selection["statement"]
    assert optical_selection["statement"] in optical_logic["llm_profile"]["truth_schema"]
    finite_schedule = next(row for row in registry["facts"] if row["fact_id"] == "production_finite_capacity_schedule_respects_resource_and_sequence_constraints")
    assert finite_schedule["legacy_anchor_id"] == "production_finite_capacity_schedule_dispatch"
    assert len(finite_schedule["verification_refs"]) == 3
    assert finite_schedule["score_effect"] == "none"
    wip_flow = next(row for row in registry["facts"] if row["fact_id"] == "production_wip_buffer_and_flow_time_relationship_is_contextual")
    assert wip_flow["legacy_anchor_id"] == "production_wip_flow_lead_time"
    assert len(wip_flow["verification_refs"]) == 3
    assert wip_flow["score_effect"] == "none"
    equipment_availability = next(row for row in registry["facts"] if row["fact_id"] == "production_equipment_resource_availability_and_maintenance_scope_boundary")
    assert equipment_availability["legacy_anchor_id"] == "production_equipment_resource_availability"
    assert len(equipment_availability["verification_refs"]) == 2
    assert "no_universal_maintenance_strategy_or_mtbf_mttr_target_is_claimed" in equipment_availability["relation"]["conditions"]
    assert equipment_availability["score_effect"] == "none"
    ford_quality_plan = next(row for row in registry["facts"] if row["fact_id"] == "ford_iatf_supplier_quality_plan_control_plan_scope")
    assert ford_quality_plan["legacy_anchor_id"] == "production_quality_plan_ctq_spec"
    assert len(ford_quality_plan["verification_refs"]) == 2
    assert "no_universal_ctq_label_sampling_plan_or_control_plan_template_is_claimed" in ford_quality_plan["relation"]["conditions"]
    assert ford_quality_plan["score_effect"] == "none"
    spc_quality_feedback = next(row for row in registry["facts"] if row["fact_id"] == "spc_control_chart_signals_are_distinct_from_specification_and_customer_disposition")
    assert spc_quality_feedback["legacy_anchor_id"] == "production_process_quality_feedback"
    assert len(spc_quality_feedback["verification_refs"]) == 3
    assert "control_limits_are_process_behavior_limits_not_product_acceptance_specifications" in spc_quality_feedback["relation"]["conditions"]
    assert spc_quality_feedback["score_effect"] == "none"
    defect_containment = next(row for row in registry["facts"] if row["fact_id"] == "production_nonconforming_output_containment_uses_scoped_traceability")
    assert defect_containment["legacy_anchor_id"] == "production_defect_containment_traceability"
    assert len(defect_containment["verification_refs"]) == 3
    assert "no_universal_mandatory_field_list_or_single_disposition_is_claimed" in defect_containment["relation"]["conditions"]
    assert defect_containment["score_effect"] == "none"
    lvdt_residual = next(row for row in registry["facts"] if row["fact_id"] == "lvdt_null_residual_signal_causes_and_spectrum")
    assert lvdt_residual["legacy_anchor_id"] == "lvdt_null_residual_voltage"
    assert len(lvdt_residual["verification_refs"]) == 1
    assert "do_not_conflate_leakage_resistance_with_magnetic_leakage_flux" in lvdt_residual["relation"]["conditions"]
    assert lvdt_residual["score_effect"] == "none"
    lvdt_saturation = next(row for row in registry["facts"] if row["fact_id"] == "lvdt_excessive_primary_excitation_saturation_harmonics_nonlinearity")
    assert lvdt_saturation["legacy_anchor_id"] == "lvdt_magnetic_saturation_nonlinearity"
    assert len(lvdt_saturation["verification_refs"]) == 2
    assert "no_universal_excitation_threshold_or_general_demodulation_error_is_claimed" in lvdt_saturation["relation"]["conditions"]
    assert lvdt_saturation["score_effect"] == "none"
    lvdt_traceability = next(row for row in registry["facts"] if row["fact_id"] == "lvdt_characterization_and_result_traceability_requirements")
    assert lvdt_traceability["legacy_anchor_id"] == "lvdt_calibration_traceability_diagnostics"
    assert len(lvdt_traceability["verification_refs"]) == 2
    assert "metrological_traceability_applies_to_the_measurement_result_not_to_an_instrument_alone" in lvdt_traceability["relation"]["conditions"]
    assert lvdt_traceability["score_effect"] == "none"
    lvdt_anchor = next(
        row
        for row in json.loads(
            (ROOT / "rubrics/topic_packs/lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error/fact_anchor.json").read_text(encoding="utf-8")
        )["anchors"]
        if row["id"] == "lvdt_null_residual_voltage"
    )
    assert "누설저항" in lvdt_anchor["statement"]
    assert "누설자속" not in lvdt_anchor["statement"]
    lvdt_saturation_anchor = next(
        row
        for row in json.loads(
            (ROOT / "rubrics/topic_packs/lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error/fact_anchor.json").read_text(encoding="utf-8")
        )["anchors"]
        if row["id"] == "lvdt_magnetic_saturation_nonlinearity"
    )
    assert lvdt_saturation_anchor["statement"] == lvdt_saturation["statement"]
    assert "복조오차" not in lvdt_saturation_anchor["statement"]
    lvdt_traceability_anchor = next(
        row
        for row in json.loads(
            (ROOT / "rubrics/topic_packs/lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error/fact_anchor.json").read_text(encoding="utf-8")
        )["anchors"]
        if row["id"] == "lvdt_calibration_traceability_diagnostics"
    )
    assert lvdt_traceability_anchor["statement"] == lvdt_traceability["statement"]
    assert "frequency response test" not in lvdt_traceability_anchor["statement"]
    lvdt_alignment = next(row for row in registry["facts"] if row["fact_id"] == "lvdt_alignment_and_radial_sensitivity_depend_on_core_construction")
    assert lvdt_alignment["legacy_anchor_id"] == "lvdt_core_alignment_eccentricity_error"
    assert len(lvdt_alignment["verification_refs"]) == 2
    assert "no_universal_zero_shift_hysteresis_or_repeatability_error_is_attributed_to_all_radial_offset" in lvdt_alignment["relation"]["conditions"]
    assert lvdt_alignment["score_effect"] == "none"
    structure_selection = next(row for row in registry["facts"] if row["fact_id"] == "process_control_structure_selection_multicriteria")
    assert structure_selection["legacy_anchor_id"] == "architecture_selection_criteria"
    assert len(structure_selection["verification_refs"]) == 3
    assert structure_selection["score_effect"] == "none"
    pid_scope = next(row for row in registry["facts"] if row["fact_id"] == "pid_diagram_scope_and_documentation_function")
    assert pid_scope["legacy_anchor_id"] == "pid_definition_scope"
    assert len(pid_scope["verification_refs"]) == 3
    assert pid_scope["score_effect"] == "none"
    pfd_pid = next(row for row in registry["facts"] if row["fact_id"] == "pfd_and_pid_purpose_and_detail_distinction")
    assert pfd_pid["legacy_anchor_id"] == "pfd_pid_difference"
    assert len(pfd_pid["verification_refs"]) == 3
    assert pfd_pid["score_effect"] == "none"
    pid_layout = next(row for row in registry["facts"] if row["fact_id"] == "pid_is_functional_schematic_not_physical_location_drawing")
    assert pid_layout["legacy_anchor_id"] == "pid_not_physical_layout"
    assert len(pid_layout["verification_refs"]) == 2
    assert pid_layout["score_effect"] == "none"
    tag_identity = next(row for row in registry["facts"] if row["fact_id"] == "isa_instrument_tag_letters_and_number_encode_identity")
    assert tag_identity["legacy_anchor_id"] == "instrument_tag_function_letters"
    assert len(tag_identity["verification_refs"]) == 2
    loop_identity = next(row for row in registry["facts"] if row["fact_id"] == "isa_loop_number_groups_devices_for_function")
    assert loop_identity["legacy_anchor_id"] == "loop_number_identity"
    assert len(loop_identity["verification_refs"]) == 2
    pid_equipment = next(row for row in registry["facts"] if row["fact_id"] == "pid_major_equipment_piping_and_field_instrumentation_content")
    assert pid_equipment["legacy_anchor_id"] == "equipment_and_piping_representation"
    pid_symbols = next(row for row in registry["facts"] if row["fact_id"] == "pid_instrument_symbol_conveys_accessibility_per_convention")
    assert pid_symbols["legacy_anchor_id"] == "instrument_symbol_location_convention"
    pid_valve = next(row for row in registry["facts"] if row["fact_id"] == "pid_control_valve_body_actuator_positioner_representation")
    assert pid_valve["legacy_anchor_id"] == "control_valve_pid_representation"
    pid_line = next(row for row in registry["facts"] if row["fact_id"] == "isa_instrument_line_styles_encode_connection_type")
    assert pid_line["legacy_anchor_id"] == "signal_line_legend"
    pid_measure = next(row for row in registry["facts"] if row["fact_id"] == "pid_measurement_loop_functional_path")
    assert pid_measure["legacy_anchor_id"] == "measurement_loop_chain"
    pid_feedback = next(row for row in registry["facts"] if row["fact_id"] == "pid_feedback_loop_measure_controller_final_element_chain")
    assert pid_feedback["legacy_anchor_id"] == "feedback_control_loop_chain"
    pid_valve_types = next(row for row in registry["facts"] if row["fact_id"] == "p_and_id_valves_have_distinct_functions_not_all_are_control_valves")
    assert pid_valve_types["legacy_anchor_id"] == "valve_function_distinction"
    assert len(pid_valve_types["verification_refs"]) == 4
    pid_loop_diagram = next(row for row in registry["facts"] if row["fact_id"] == "loop_diagram_carries_installation_and_wiring_detail_beyond_pid")
    assert pid_loop_diagram["legacy_anchor_id"] == "pid_loop_diagram_relation"
    assert len(pid_loop_diagram["verification_refs"]) == 2
    pid_logic = next(row for row in registry["facts"] if row["fact_id"] == "isa_binary_logic_diagram_documents_interlock_and_sequence_logic")
    assert pid_logic["legacy_anchor_id"] == "pid_logic_diagram_relation"
    assert len(pid_logic["verification_refs"]) == 2
    alarm_logic = next(row for row in registry["facts"] if row["fact_id"] == "pid_shows_selected_alarm_and_interlock_functions_not_full_logic_detail")
    assert alarm_logic["legacy_anchor_id"] == "alarm_trip_interlock_boundary"
    assert len(alarm_logic["verification_refs"]) == 2
    control_narrative = next(row for row in registry["facts"] if row["fact_id"] == "control_narrative_complements_pid_with_operating_logic_description")
    assert control_narrative["legacy_anchor_id"] == "pid_control_narrative_relation"
    assert len(control_narrative["verification_refs"]) == 2
    legend_convention = next(row for row in registry["facts"] if row["fact_id"] == "pid_symbol_interpretation_uses_standard_and_project_legend")
    assert legend_convention["legacy_anchor_id"] == "legend_project_convention_priority"
    assert len(legend_convention["verification_refs"]) == 2
    instrument_index = next(row for row in registry["facts"] if row["fact_id"] == "instrument_tag_identity_is_cross_referenced_in_project_documents")
    assert instrument_index["legacy_anchor_id"] == "pid_instrument_index_io_relation"
    assert len(instrument_index["verification_refs"]) == 2
    config_review = next(row for row in registry["facts"] if row["fact_id"] == "configuration_review_checks_documented_design_against_physical_configuration")
    assert config_review["legacy_anchor_id"] == "design_review_cross_document_consistency"
    assert len(config_review["verification_refs"]) == 2
    walkdown = next(row for row in registry["facts"] if row["fact_id"] == "pid_walkdown_can_verify_as_found_configuration_and_feed_as_built_records")
    assert walkdown["legacy_anchor_id"] == "field_verification_asbuilt"
    assert len(walkdown["verification_refs"]) == 2
    pid_moc = next(row for row in registry["facts"] if row["fact_id"] == "process_change_requires_document_review_and_pid_revision_where_affected")
    assert pid_moc["legacy_anchor_id"] == "revision_moc_document_control"
    assert len(pid_moc["verification_refs"]) == 1
    pid_lifecycle = next(row for row in registry["facts"] if row["fact_id"] == "pid_is_process_safety_information_for_hazard_analysis_and_operations")
    assert pid_lifecycle["legacy_anchor_id"] == "pid_lifecycle_use"
    assert len(pid_lifecycle["verification_refs"]) == 1
    standard_bonnet = next(row for row in registry["facts"] if row["fact_id"] == "globe_valve_bonnet_closes_pressure_boundary_and_houses_packing")
    assert standard_bonnet["legacy_anchor_id"] == "standard_bonnet_pressure_boundary"
    assert len(standard_bonnet["verification_refs"]) == 2
    balanced_scope = next(row for row in registry["facts"] if row["fact_id"] == "balanced_trim_assessment_uses_residual_unbalance_area_seat_load_and_application")
    assert balanced_scope["legacy_anchor_id"] == "control_valve_balanced_unbalanced_scope"
    assert balanced_scope["score_effect"] == "none"
    assert len(balanced_scope["verification_refs"]) == 2
    motion_class = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_sliding_stem_rotary_motion_classification")
    assert motion_class["legacy_anchor_id"] == "sliding_stem_rotary_motion_classification"
    assert motion_class["score_effect"] == "none"
    actuator_match = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_actuator_output_matches_valve_motion")
    assert actuator_match["legacy_anchor_id"] == "actuator_output_matches_valve_motion"
    assert actuator_match["source_refs"] == []
    assert actuator_match["score_effect"] == "none"
    rack_pinion = next(row for row in registry["facts"] if row["fact_id"] == "rack_pinion_actuator_rotary_output_application_and_sizing")
    assert rack_pinion["legacy_anchor_id"] == "rack_pinion_rotary_torque_conversion"
    assert len(rack_pinion["verification_refs"]) == 2
    assert rack_pinion["score_effect"] == "none"
    butterfly = next(row for row in registry["facts"] if row["fact_id"] == "butterfly_valve_compact_large_size_and_trim_dependent_control_scope")
    assert butterfly["legacy_anchor_id"] == "butterfly_compact_high_capacity"
    assert len(butterfly["verification_refs"]) == 3
    assert butterfly["score_effect"] == "none"
    full_port_ball = next(row for row in registry["facts"] if row["fact_id"] == "full_port_ball_low_restriction_pigging_and_throttling_scope")
    assert full_port_ball["legacy_anchor_id"] == "full_port_ball_low_restriction_scope"
    assert len(full_port_ball["verification_refs"]) == 1
    assert full_port_ball["score_effect"] == "none"
    multiport = next(row for row in registry["facts"] if row["fact_id"] == "fisher_multiport_selector_well_test_routing_scope")
    assert multiport["legacy_anchor_id"] == "multiport_selector_flow_routing"
    assert len(multiport["verification_refs"]) == 2
    assert multiport["score_effect"] == "none"
    end_connections = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_end_connection_maintenance_and_service_tradeoffs")
    assert end_connections["legacy_anchor_id"] == "end_connection_threaded_flanged_welded"
    assert len(end_connections["verification_refs"]) == 1
    assert end_connections["score_effect"] == "none"
    electric_actuator = next(row for row in registry["facts"] if row["fact_id"] == "electric_valve_actuator_output_duty_supply_and_fail_safe_selection")
    assert electric_actuator["legacy_anchor_id"] == "electric_actuator_motor_gear_control"
    assert len(electric_actuator["verification_refs"]) == 3
    assert electric_actuator["score_effect"] == "none"
    hydraulic_actuator = next(row for row in registry["facts"] if row["fact_id"] == "hydraulic_actuator_force_stiffness_and_stored_energy_scope")
    assert hydraulic_actuator["legacy_anchor_id"] == "hydraulic_actuator_force_and_stored_energy_fail_safe"
    assert len(hydraulic_actuator["verification_refs"]) == 4
    assert hydraulic_actuator["score_effect"] == "none"
    double_ported = next(row for row in registry["facts"] if row["fact_id"] == "double_ported_globe_capacity_force_balance_and_seat_leakage_limit")
    assert double_ported["legacy_anchor_id"] == "double_port_capacity_force_balance_limit"
    assert len(double_ported["verification_refs"]) == 2
    assert double_ported["score_effect"] == "none"
    guide_methods = next(row for row in registry["facts"] if row["fact_id"] == "globe_valve_guide_method_alignment_side_load_and_wear_scope")
    assert guide_methods["legacy_anchor_id"] == "plug_guiding_alignment_and_side_load"
    assert len(guide_methods["verification_refs"]) == 3
    assert guide_methods["score_effect"] == "none"
    segmented_v_notch = next(row for row in registry["facts"] if row["fact_id"] == "segmented_v_notch_ball_capacity_characteristic_and_seal_scope")
    assert segmented_v_notch["legacy_anchor_id"] == "segmented_v_notch_ball_throttling"
    assert len(segmented_v_notch["verification_refs"]) == 3
    assert segmented_v_notch["score_effect"] == "none"
    cage_guided = next(row for row in registry["facts"] if row["fact_id"] == "cage_guides_plug_and_enables_flow_characterization")
    assert cage_guided["legacy_anchor_id"] == "cage_guided_alignment_and_flow_path"
    assert len(cage_guided["verification_refs"]) == 3
    assert cage_guided["score_effect"] == "none"
    eccentric_plug = next(row for row in registry["facts"] if row["fact_id"] == "fisher_v500_eccentric_plug_cam_action_and_erosive_service_scope")
    assert eccentric_plug["legacy_anchor_id"] == "eccentric_plug_noncontact_rotation"
    assert len(eccentric_plug["verification_refs"]) == 3
    assert eccentric_plug["score_effect"] == "none"
    extension_bonnet = next(row for row in registry["facts"] if row["fact_id"] == "extension_bonnet_temperature_length_and_orientation_are_application_specific")
    assert extension_bonnet["legacy_anchor_id"] == "extension_bonnet_temperature_isolation"
    assert len(extension_bonnet["verification_refs"]) == 3
    assert extension_bonnet["score_effect"] == "none"
    valve_selection = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_actuator_selection_multifactor_service_fit_and_lifecycle_scope")
    assert valve_selection["legacy_anchor_id"] == "body_actuator_selection_multi_criteria"
    assert len(valve_selection["verification_refs"]) == 5
    assert valve_selection["score_effect"] == "none"
    humidity_selection = next(row for row in registry["facts"] if row["fact_id"] == "humidity_sensor_selection_maintenance_integration_and_lifecycle_factors")
    assert humidity_selection["legacy_anchor_id"] == "humidity_lifecycle_maintainability_selection"
    assert len(humidity_selection["verification_refs"]) == 3
    assert humidity_selection["score_effect"] == "none"
    zone_conduit = next(row for row in registry["facts"] if row["fact_id"] == "ot_zone_conduit_grouping_and_boundary_enforcement")
    assert zone_conduit["legacy_anchor_id"] == "sw09_zone_conduit"
    assert zone_conduit["source_refs"] == []
    assert len(zone_conduit["verification_refs"]) == 1
    assert zone_conduit["score_effect"] == "none"
    source_free = next(row for row in registry["facts"] if row["fact_id"] == "nyquist_negative_feedback_characteristic_equation")
    assert source_free["source_refs"] == []
    assert source_free["verification_refs"][0]["authority_type"] == "calculation"
    positioner_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "control_valve_positioner_ip_converter_booster_accessories_calibration"}
    assert positioner_facts["ip_converter_current_pressure_transduction"]["verification_status"] == "verified"
    assert positioner_facts["conventional_4_20ma_3_15psi_endpoints"]["verification_status"] == "verified"
    assert positioner_facts["positioner_travel_feedback_controller"]["verification_status"] == "verified"
    assert positioner_facts["volume_booster_flow_capacity_function"]["verification_status"] == "verified"
    assert "not a universal steady-state pressure amplifier" in positioner_facts["volume_booster_flow_capacity_function"]["statement"]
    assert positioner_facts["normalized_current_command"]["verification_refs"][0]["authority_type"] == "calculation"
    assert positioner_facts["ip_linear_pressure_mapping"]["verification_refs"][0]["authority_type"] == "calculation"
    booster_ratio = next(row for row in registry["facts"] if row["fact_id"] == "fisher_2625_volume_booster_one_to_one_pressure_following")
    assert booster_ratio["legacy_anchor_id"] == "booster_pressure_follower_boundary"
    assert booster_ratio["verification_status"] == "verified"
    assert booster_ratio["verification_refs"][0]["authority_type"] == "official_documentation"
    assert any("not_generalized_to_other_booster_designs" in condition for condition in booster_ratio["relation"]["conditions"])
    tank_fact = next(row for row in registry["facts"] if row["fact_id"] == "volume_tank_stored_air_mass_and_fill_time_tradeoff")
    assert tank_fact["legacy_anchor_id"] == "volume_tank_energy_storage_response_tradeoff"
    assert tank_fact["verification_refs"][0]["authority_type"] == "calculation"
    assert "no_fixed_actuator_holding_time_is_guaranteed_by_tank_volume_alone" in tank_fact["relation"]["conditions"]
    tubing_fact = next(row for row in registry["facts"] if row["fact_id"] == "pneumatic_actuator_line_capacity_and_fill_response")
    assert tubing_fact["legacy_anchor_id"] == "tubing_output_capacity_pressure_drop"
    assert tubing_fact["verification_status"] == "verified"
    assert "no_universal_tubing_size_or_stroke_time_is_asserted" in tubing_fact["relation"]["conditions"]
    as_found = next(row for row in registry["facts"] if row["fact_id"] == "positioner_calibration_as_found_as_left_recording_scope")
    assert as_found["legacy_anchor_id"] == "as_found_as_left_traceability"
    assert as_found["verification_status"] == "verified"
    assert any(ref["authority_id"].startswith("NIST_") for ref in as_found["verification_refs"])
    iec62382_ids = {
        "iec62382_control_stroke_intermediate_points_and_hysteresis_checks",
        "iec62382_loop_check_exercises_individual_and_combined_loop_components",
        "iec62382_actuator_failure_simulation_verifies_configured_reaction",
        "iec62382_end_to_end_loop_check_is_not_sis_validation",
    }
    iec62382_facts = {row["fact_id"]: row for row in registry["facts"] if row["fact_id"] in iec62382_ids}
    assert set(iec62382_facts) == iec62382_ids
    assert all(row["verification_status"] == "verified" for row in iec62382_facts.values())
    assert all(row["verification_refs"][0]["authority_type"] == "standard" for row in iec62382_facts.values())
    dp_level_facts = {
        row["legacy_anchor_id"]: row for row in registry["facts"]
        if row["topic_id"] == "differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error"
    }
    endpoint_fact = dp_level_facts["dp_level_calibration_lrv_urv"]
    assert endpoint_fact["verification_status"] == "verified"
    assert endpoint_fact["source_refs"] == []
    assert any(ref["authority_type"] == "calculation" for ref in endpoint_fact["verification_refs"])
    assert "only_pressure_heads_present_in_actual_installation_are_included" in endpoint_fact["relation"]["conditions"]
    overpressure_fact = dp_level_facts["dp_level_overpressure_and_static_pressure_effect"]
    assert overpressure_fact["verification_status"] == "verified"
    assert overpressure_fact["source_refs"] == []
    assert overpressure_fact["verification_refs"][0]["authority_type"] == "official_documentation"
    assert "claim_is_limited_to_rosemount_3051shp_manual" in overpressure_fact["relation"]["conditions"]
    assert "no_universal_transmitter_damage_threshold_is_claimed" in overpressure_fact["relation"]["conditions"]
    selection_fact = dp_level_facts["dp_level_selection_against_radar_gwr"]
    assert selection_fact["verification_status"] == "verified"
    assert selection_fact["source_refs"] == []
    assert len(selection_fact["verification_refs"]) == 3
    assert "no_universal_technology_superiority_is_claimed" in selection_fact["relation"]["conditions"]
    radar_facts = {
        row["legacy_anchor_id"]: row for row in registry["facts"]
        if row["topic_id"] == "radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error"
    }
    assert radar_facts["radar_pulse_time_of_flight"]["verification_refs"][0]["authority_type"] == "official_documentation"
    assert radar_facts["radar_level_reference_calculation"]["verification_status"] == "verified"
    assert radar_facts["radar_level_reference_calculation"]["source_refs"] == []
    assert "d_and_e_use_the_same_reference_point" in radar_facts["radar_level_reference_calculation"]["relation"]["conditions"]
    assert radar_facts["radar_electromagnetic_wave_reflection"]["verification_refs"][0]["authority_type"] == "official_documentation"
    assert radar_facts["radar_fmcw_linear_frequency_sweep"]["verification_refs"][0]["authority_type"] == "official_documentation"
    assert radar_facts["radar_dielectric_constant_reflection"]["verification_refs"][0]["authority_type"] == "calculation"
    assert "lossless_nonmagnetic_dielectric" in radar_facts["radar_dielectric_constant_reflection"]["relation"]["conditions"]
    assert len(radar_facts["radar_fmcw_beat_frequency_distance"]["verification_refs"]) == 2
    assert "ideal_linear_frequency_sweep" in radar_facts["radar_fmcw_beat_frequency_distance"]["relation"]["conditions"]
    assert len(radar_facts["gwr_tdr_guided_wave_principle"]["verification_refs"]) == 4
    assert "claim_is_about_guided_radar_not_free_space_fmcw" in radar_facts["gwr_tdr_guided_wave_principle"]["relation"]["conditions"]
    assert len(radar_facts["radar_echo_mapping_calibration_diagnostics"]["verification_refs"]) == 4
    assert "false_echo_mapping_must_not_mask_true_level_echo" in radar_facts["radar_echo_mapping_calibration_diagnostics"]["relation"]["conditions"]
    assert len(radar_facts["radar_antenna_beam_footprint"]["verification_refs"]) == 3
    assert "footprint_depends_on_beam_angle_and_range" in radar_facts["radar_antenna_beam_footprint"]["relation"]["conditions"]
    assert len(radar_facts["radar_pulse_distance_equation"]["verification_refs"]) == 3
    assert "high_pressure_polar_vapor_effect_is_gas_and_process_specific" in radar_facts["radar_pulse_distance_equation"]["relation"]["conditions"]
    assert len(radar_facts["radar_bandwidth_range_resolution"]["verification_refs"]) == 5
    assert "range_resolution_is_two_reflector_separation_capability" in radar_facts["radar_bandwidth_range_resolution"]["relation"]["conditions"]
    assert len(radar_facts["radar_low_dielectric_echo_margin"]["verification_refs"]) == 4
    assert "no_single_dielectric_cutoff_is_generalized_to_all_radar_models" in radar_facts["radar_low_dielectric_echo_margin"]["relation"]["conditions"]
    assert len(radar_facts["radar_mounting_nozzle_obstruction_error"]["verification_refs"]) == 3
    assert "nozzle_dimensions_are_antenna_model_specific" in radar_facts["radar_mounting_nozzle_obstruction_error"]["relation"]["conditions"]
    assert len(radar_facts["radar_antenna_buildup_condensation"]["verification_refs"]) == 4
    assert "no_universal_antenna_material_or_heating_requirement_is_claimed" in radar_facts["radar_antenna_buildup_condensation"]["relation"]["conditions"]
    assert len(radar_facts["radar_false_echo_multiple_reflection"]["verification_refs"]) == 2
    assert "multiple_reflection_is_not_claimed_to_occur_in_every_tank" in radar_facts["radar_false_echo_multiple_reflection"]["relation"]["conditions"]
    assert len(radar_facts["radar_vapor_pressure_temperature_effect"]["verification_refs"]) == 2
    assert len(radar_facts["radar_point_target_equation_scope"]["verification_refs"]) == 1
    assert "fourth_power_case_is_limited_to_small_reflector_relative_to_beam" in radar_facts["radar_point_target_equation_scope"]["relation"]["conditions"]
    assert len(radar_facts["radar_frequency_antenna_tradeoff"]["verification_refs"]) == 3
    assert "fmcw_two_target_range_resolution_depends_on_swept_bandwidth_not_carrier_frequency_alone" in radar_facts["radar_frequency_antenna_tradeoff"]["relation"]["conditions"]
    assert len(radar_facts["radar_surface_foam_turbulence_slope"]["verification_refs"]) == 3
    assert len(radar_facts["radar_adaptive_threshold_echo_tracking"]["verification_refs"]) == 3
    assert "no_single_peak_rule_or_universal_adaptive_threshold_algorithm_is_claimed" in radar_facts["radar_adaptive_threshold_echo_tracking"]["relation"]["conditions"]
    assert radar_facts["radar_echo_polarity_sign_convention"]["verification_status"] == "verified"
    assert "physical_field_phase_reversal_is_distinct_from_processed_echo_plot_polarity" in radar_facts["radar_echo_polarity_sign_convention"]["relation"]["conditions"]
    chl_facts = {
        row["legacy_anchor_id"]: row for row in registry["facts"]
        if row["topic_id"] == "control_hardware_lifecycle_panel_architecture_component_selection_production_verification"
    }
    assert chl_facts["chl_requirement_traceability"]["verification_status"] == "verified"
    assert "requirement_categories_and_tool_are_project_specific" in chl_facts["chl_requirement_traceability"]["relation"]["conditions"]
    assert chl_facts["chl_verification_plan"]["verification_refs"][0]["authority_type"] == "official_documentation"
    assert chl_facts["chl_verification_vs_validation"]["verification_status"] == "verified"
    assert chl_facts["chl_bom_configuration"]["verification_status"] == "verified"
    assert "no_universal_bom_or_firmware_dependency_field_list_is_asserted" in chl_facts["chl_bom_configuration"]["relation"]["conditions"]
    sw02_facts = {
        row["legacy_anchor_id"]: row for row in registry["facts"]
        if row["topic_id"] == "control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe"
    }
    assert sw02_facts["sw02_sequence_definition"]["verification_status"] == "verified"
    assert sw02_facts["sw02_permissive_definition"]["verification_status"] == "verified"
    assert "no_universal_and_expression_or_condition_list_is_asserted" in sw02_facts["sw02_permissive_definition"]["relation"]["conditions"]
    assert sw02_facts["sw02_interlock_definition"]["verification_status"] == "verified"
    assert sw02_facts["sw02_trip_definition"]["verification_status"] == "verified"
    assert "no_universal_manual_reset_or_trip_state_is_asserted" in sw02_facts["sw02_trip_definition"]["relation"]["conditions"]
    assert sw02_facts["sw02_feedback_confirmation_timeout"]["verification_status"] == "verified"
    assert "timeout_detects_late_or_missing_completion_but_does_not_identify_root_cause" in sw02_facts["sw02_feedback_confirmation_timeout"]["relation"]["conditions"]
    assert sw02_facts["sw02_state_entry_exit_actions"]["verification_status"] == "verified"
    assert "initialization_processing_termination_are_documented_simatic_sfc_phases_not_mandatory_for_every_step" in sw02_facts["sw02_state_entry_exit_actions"]["relation"]["conditions"]
    for anchor_id in (
        "electropneumatic_positioner_separate_ip_boundary",
        "ip_supply_air_dependency",
        "filter_regulator_supply_conditioning",
        "quick_exhaust_rapid_vent_function",
        "solenoid_on_off_pneumatic_switching",
        "pneumatic_positioner_force_balance_mechanism",
        "positioner_direct_reverse_action",
        "positioner_zero_span_travel_calibration",
        "command_ip_positioner_actuator_feedback_chain",
        "travel_feedback_linkage_cam_alignment",
    ):
        assert positioner_facts[anchor_id]["verification_status"] == "verified"
    assert "nozzle/flapper" in positioner_facts["pneumatic_positioner_force_balance_mechanism"]["statement"]
    assert "actuator diaphragm-casing pressure" in positioner_facts["positioner_direct_reverse_action"]["statement"]
    assert "repeat the zero adjustment" in positioner_facts["positioner_zero_span_travel_calibration"]["statement"]
    assert "stem travel is fed back mechanically through the cam" in positioner_facts["command_ip_positioner_actuator_feedback_chain"]["statement"]
    assert "universal quantitative linearity error" in positioner_facts["travel_feedback_linkage_cam_alignment"]["statement"]
    assert "water-vapor removal are not implied" in positioner_facts["filter_regulator_supply_conditioning"]["statement"]
    gas_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "control_valve_gas_sizing_choked_flow_critical_pressure_ratio"}
    assert set(gas_facts) == {
        "flow_basis_standard_actual_mass_distinction",
        "standard_condition_definition_required",
        "absolute_pressure_required",
        "absolute_temperature_required",
        "compressibility_factor_meaning",
        "valve_pressure_drop_ratio_factor_meaning",
        "pressure_ratio_direction",
        "xTP_fitting_adjusted_factor",
        "no_fitting_reference_condition",
        "choked_pressure_ratio_limit",
        "expansion_factor_subcritical_relation",
        "expansion_factor_bounds",
        "subcritical_flow_behavior",
        "standard_volume_formula_structure",
        "mass_flow_formula_structure",
        "gas_property_input_selection",
        "compressible_control_valve_sizing_scope",
        "xT_valve_style_trim_travel_dependency",
        "required_vs_rated_gas_coefficient",
        "minimum_normal_maximum_gas_cases",
        "steam_vapor_property_boundary",
        "vendor_hand_calculation_crosscheck_gas",
        "aerodynamic_noise_handoff",
        "choked_flow_not_zero_flow",
        "choked_flow_downstream_independence",
        "pressure_drop_ratio_definition",
        "heat_capacity_ratio_factor",
        "piping_geometry_factor_gas_service",
        "sizing_ratio_minimum_selection",
        "expansion_factor_physical_meaning",
        "choked_flow_physical_meaning",
        "unit_constant_equation_dependency",
        "selected_travel_xT_iteration",
        "fail_open_maximum_flow_case",
    }
    fail_open = gas_facts["fail_open_maximum_flow_case"]
    assert "maximum_upstream_and_minimum_downstream_pressures_must_be_credible_and_coincident" in fail_open["relation"]["conditions"]
    assert fail_open["score_effect"] == "none"
    assert all(row["score_effect"] == "none" for row in gas_facts.values())
    assert all(row["verification_refs"] for row in gas_facts.values())
    process_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "process_control_loop_architecture_cascade_ratio_feedforward_override_split_range"}
    assert set(process_facts) == {
        "architecture_selection_criteria",
        "cascade_structure",
        "cascade_secondary_faster",
        "cascade_disturbance_condition",
        "override_selective_control",
        "override_tracking_antiwindup",
        "split_range_control",
        "ratio_control_structure",
        "feedforward_principle",
        "feedforward_feedback_combination",
        "process_loop_signal_chain",
        "single_loop_architecture",
        "split_range_transition_design",
        "ratio_scaling_and_low_flow",
        "loop_interaction_coordination",
        "field_implementation_validation",
    }
    assert all(row["score_effect"] == "none" for row in process_facts.values())
    assert all(row["verification_refs"] for row in process_facts.values())
    humidity_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "humidity_measurement_capacitive_resistive_dew_point_selection_compensation"}
    assert set(humidity_facts) == {
        "humidity_water_vapor_partial_pressure",
        "relative_humidity_definition",
        "rh_temperature_dependence",
        "absolute_humidity_definition",
        "dew_point_definition",
        "frost_point_distinction",
        "pressure_dew_point_effect",
        "capacitive_polymer_principle",
        "capacitive_sensor_temperature_compensation",
        "capacitive_sensor_hysteresis_drift",
        "resistive_humidity_principle",
        "resistive_sensor_ac_measurement",
        "resistive_sensor_limits",
        "selection_environment_process",
        "chilled_mirror_maintenance",
        "chilled_mirror_principle",
        "psychrometric_wet_dry_bulb",
        "condensation_sensor_temperature_error",
        "high_humidity_warmed_probe",
        "low_humidity_dew_point_selection",
        "calibration_traceability_field_check",
        "humidity_lifecycle_maintainability_selection",
    }
    assert all(row["score_effect"] == "none" for row in humidity_facts.values())
    assert all(row["verification_refs"] for row in humidity_facts.values())
    lvdt_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error"}
    assert set(lvdt_facts) == {
        "lvdt_differential_transformer_structure",
        "lvdt_primary_ac_excitation",
        "lvdt_secondary_series_opposition",
        "lvdt_differential_output_es1_es2",
        "lvdt_null_position_voltage_balance",
        "lvdt_output_amplitude_displacement",
        "lvdt_output_phase_direction",
        "lvdt_linear_measurement_range",
        "lvdt_null_residual_voltage",
        "lvdt_core_alignment_eccentricity_error",
        "lvdt_phase_sensitive_demodulation",
        "lvdt_low_pass_dc_output",
        "lvdt_dynamic_response_frequency_bandwidth",
        "lvdt_core_position_mutual_inductance",
        "lvdt_temperature_coil_resistance_error",
        "rvdt_rotary_angle_measurement",
        "lvdt_vs_strain_gauge_displacement_principle",
        "lvdt_demodulated_zero_offset",
        "lvdt_cable_shield_grounding_error",
        "lvdt_excitation_frequency_voltage_sensitivity",
        "lvdt_magnetic_saturation_nonlinearity",
        "lvdt_calibration_traceability_diagnostics",
    }
    assert "ten_to_one_minimum_is_attributed_to_the_cited_ni_guidance" in lvdt_facts["lvdt_excitation_frequency_voltage_sensitivity"]["relation"]["conditions"]
    assert all(row["score_effect"] == "none" for row in lvdt_facts.values())
    assert all(row["verification_refs"] for row in lvdt_facts.values())
    valve_type_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "control_valve_types_globe_rotary_body_actuator_selection"}
    assert set(valve_type_facts) == {
        "sliding_stem_rotary_motion_classification",
        "single_port_globe_throttling_structure",
        "angle_valve_flow_direction_change",
        "cage_guided_alignment_and_flow_path",
        "three_way_mixing_diverting_function",
        "sanitary_valve_cleanability_drainability",
        "high_performance_butterfly_eccentric_sealing",
        "bellows_seal_bonnet_emission_barrier",
        "reduced_capacity_trim_match_required_flow",
        "spring_diaphragm_actuator_force_and_fail_safe",
        "piston_actuator_high_force_and_speed",
        "manual_actuator_local_operation_limit",
        "actuator_output_matches_valve_motion",
        "rack_pinion_rotary_torque_conversion",
        "butterfly_compact_high_capacity",
        "full_port_ball_low_restriction_scope",
        "multiport_selector_flow_routing",
        "end_connection_threaded_flanged_welded",
        "electric_actuator_motor_gear_control",
        "hydraulic_actuator_force_and_stored_energy_fail_safe",
        "double_port_capacity_force_balance_limit",
        "plug_guiding_alignment_and_side_load",
        "segmented_v_notch_ball_throttling",
        "eccentric_plug_noncontact_rotation",
        "extension_bonnet_temperature_isolation",
        "standard_bonnet_pressure_boundary",
        "post_guided_plug_alignment",
        "port_guided_plug_alignment",
        "body_actuator_selection_multi_criteria",
    }
    assert all(row["score_effect"] == "none" for row in valve_type_facts.values())
    assert all(row["verification_refs"] for row in valve_type_facts.values())
    manifold_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation"}
    assert set(manifold_facts) == {
        "manifold_normal_state",
        "dp_pressure_test_reference",
        "process_isolation_fill_fluid",
        "pulsation_damping_tradeoff",
        "bleed_vent_service_location",
        "manifold_isolation_sequence",
        "manifold_return_sequence",
    }
    assert all(row["score_effect"] == "none" for row in manifold_facts.values())
    assert all(row["verification_refs"] for row in manifold_facts.values())
    manifold_normal = next(row for row in registry["facts"] if row["fact_id"] == "dp_3valve_manifold_normal_measurement_configuration")
    assert len(manifold_normal["verification_refs"]) == 2
    assert any(ref["authority_id"] == "EMERSON_ROSEMOUNT_3051S_THREE_VALVE_NORMAL_OPERATION" for ref in manifold_normal["verification_refs"])
    ultrasonic_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error"}
    assert set(ultrasonic_facts) == {
        "ultrasonic_round_trip_distance_equation",
        "ultrasonic_sound_speed_medium_dependence",
        "ultrasonic_air_temperature_compensation",
        "ultrasonic_piezoelectric_transduction",
        "ultrasonic_pulse_echo_time_of_flight",
        "ultrasonic_sensor_crosstalk",
        "ultrasonic_target_reflectivity_orientation",
        "ultrasonic_beam_angle_footprint",
        "ultrasonic_level_measurement_reference",
        "ultrasonic_false_echo_multiple_reflection",
        "ultrasonic_echo_amplitude_validity",
        "ultrasonic_mounting_nozzle_obstruction_error",
        "ultrasonic_foam_vapor_turbulence_error",
        "ultrasonic_dead_zone_ringdown",
        "ultrasonic_sensor_system_structure",
        "ultrasonic_frequency_range_resolution_tradeoff",
        "ultrasonic_attenuation_max_range",
        "ultrasonic_repetition_rate_response_averaging",
        "ultrasonic_calibration_echo_mapping_diagnostics",
        "ultrasonic_application_limits_comparison",
    }
    assert all(row["score_effect"] == "none" for row in ultrasonic_facts.values())
    assert all(row["verification_refs"] for row in ultrasonic_facts.values())
    maintenance_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing"}
    assert set(maintenance_facts) == {"seat_leakage_test"}
    assert "does not define acceptance conditions for other trims" in maintenance_facts["seat_leakage_test"]["statement"]
    assert maintenance_facts["seat_leakage_test"]["score_effect"] == "none"
    force_facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe"}
    assert set(force_facts) == {
        "control_valve_moving_assembly_free_body_diagram",
        "control_valve_unbalance_force_effective_area_approximation",
        "control_valve_pressure_tends_to_open_close_direction",
        "control_valve_stem_area_pressure_force",
        "control_valve_balanced_trim_residual_unbalance",
        "control_valve_seat_load_shutoff_class",
        "control_valve_pneumatic_actuator_force_effective_area",
        "control_valve_spring_preload_rate_travel_force",
        "control_valve_bench_set_operating_range_difference",
        "control_valve_actuator_sizing_worst_case_conditions",
        "control_valve_stiction_deadband_diagnostics",
        "control_valve_pressure_force_surface_integration",
        "control_valve_flow_direction_trim_geometry_dependency",
        "control_valve_fail_open_force_balance",
        "control_valve_fail_close_force_balance",
        "control_valve_rotary_valve_torque_boundary",
        "control_valve_friction_opposes_motion_not_actuator",
        "control_valve_dynamic_flow_force_momentum_side_load",
        "control_valve_breakaway_running_friction_hysteresis",
        "control_valve_packing_friction",
        "control_valve_balanced_trim_tradeoff_maintenance",
        "control_valve_guide_friction_side_load",
    }
    assert all(row["verification_refs"] and row["score_effect"] == "none" for row in force_facts.values())
    speed_fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == "mechanical_mounting_coupling_error")
    assert speed_fact["verification_status"] == "verified"
    assert len(speed_fact["verification_refs"]) == 2
    assert "universal coupling-slip or torsional-vibration" in speed_fact["statement"]


def test_sw06_release_control_fact_is_scoped_to_supported_project_guidance():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "sw06_release_control_identifies_approved_versioned_scope_and_checks_delivery_copy"
    )
    assert fact["legacy_anchor_id"] == "sw06_release_control_authorized_artifact"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "claim_is_scoped_to_nasa_swe_085_guidance_and_applicable_project_requirements" in fact["relation"]["conditions"]
    assert any(
        ref["authority_id"] == "NASA_SWEHB_SWE_085_RELEASE_MANAGEMENT_VER_D"
        and "verifying delivered copies against the master" in ref["supports_claim"]
        for ref in fact["verification_refs"]
    )


def test_maintenance_type_anchor_uses_current_scoped_iso_definitions():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "maintenance_types_distinguish_corrective_preventive_condition_based_and_predictive"
    )
    assert fact["legacy_anchor_id"] == "maintenance_strategy_corrective_preventive_condition_predictive"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "preventive_maintenance_is_not_limited_to_fixed_time_or_usage_intervals" in fact["relation"]["conditions"]
    assert any(
        ref["authority_id"] == "ISO_14224_2016_CURRENT_MAINTENANCE_TERMINOLOGY"
        and "§3.77" in ref["supports_claim"]
        for ref in fact["verification_refs"]
    )


def test_maintenance_plan_anchor_matches_iso_14224_definition_without_universal_interval():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "iso14224_maintenance_plan_structured_tasks_activities_procedures_resources_duration"
    )
    assert fact["legacy_anchor_id"] == "maintenance_plan_task_interval_basis"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert any(
        ref["authority_id"] == "ISO_14224_2016_CURRENT_MAINTENANCE_PLAN_DEFINITION"
        and "§3.54" in ref["locator"]
        for ref in fact["verification_refs"]
    )


def test_calibration_anchor_distinguishes_traceability_from_fitness_and_fixed_interval():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "metrological_traceability_chain_uncertainty_and_interval_are_purpose_dependent"
    )
    assert fact["legacy_anchor_id"] == "calibration_program_traceability"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert any(ref["authority_id"] == "NIST_POLICY_ON_METROLOGICAL_TRACEABILITY" for ref in fact["verification_refs"])
    assert any(ref["authority_id"] == "NIST_RECOMMENDED_CALIBRATION_INTERVAL" for ref in fact["verification_refs"])


def test_maintenance_criticality_fact_avoids_universal_factor_list():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "asset_maintenance_risk_prioritization_considers_likelihood_consequence_and_defined_criteria"
    )
    assert fact["legacy_anchor_id"] == "maintenance_criticality_risk_prioritization"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "no_universal_instrumentation_criticality_factor_list_or_weighting_is_claimed" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ISO_31000_2018_RISK_MANAGEMENT_FRAMEWORK",
        "ISO_55001_2024_ASSET_DECISION_CRITERIA",
    }


def test_asset_register_fact_is_limited_to_iso14224_taxonomy_and_identification_scope():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "iso14224_equipment_id_function_location_and_reliability_taxonomy"
    )
    assert fact["legacy_anchor_id"] == "om_asset_register_system_boundary"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "complete_asset_register_fields_may_include_additional_operator_specific_information" in fact["relation"]["conditions"]


def test_iso14224_work_order_anchor_is_limited_to_standardized_data_categories():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "iso14224_maintenance_data_covers_actions_resources_consequences_and_downtime"
    )
    assert fact["legacy_anchor_id"] == "work_order_history_closed_loop"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "maintenance_data_categories_do_not_imply_a_universal_work_order_process" in fact["relation"]["conditions"]
    assert any(
        ref["authority_id"] == "ISO_14224_2016_MAINTENANCE_DATA_CATEGORIES_AND_SCOPE"
        and "downtime" in ref["supports_claim"]
        for ref in fact["verification_refs"]
    )


def test_iso14224_maintenance_data_quality_anchor_is_scoped_and_nonprescriptive():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "iso14224_reliability_maintenance_data_quality_and_standard_format"
    )
    assert fact["legacy_anchor_id"] == "maintenance_data_quality_cmms_taxonomy"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "standard_scope_is_petroleum_natural_gas_and_petrochemical_industries" in fact["relation"]["conditions"]
    assert "standard_does_not_require_a_named_cmms_or_eam_product_or_all_operator_specific_work_order_fields" in fact["relation"]["conditions"]
    assert any(ref["authority_id"] == "ISO_14224_2016_CURRENT_SCOPE_DATA_CATEGORIES_AND_QUALITY" for ref in fact["verification_refs"])
    assert any(ref["authority_id"] == "ISO_TC67_OTC_28705_MS_ISO14224_DATA_QUALITY_IMPLEMENTATION" for ref in fact["verification_refs"])


def test_iso55001_continual_improvement_anchor_does_not_universalize_local_maintenance_loop():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "iso55001_system_continual_improvement_value_and_decision_balance"
    )
    assert fact["legacy_anchor_id"] == "om_continuous_improvement_pdca_lifecycle_cost"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "continual_improvement_requirement_applies_at_asset_management_system_level" in fact["relation"]["conditions"]
    assert "no_universal_instrument_maintenance_kpi_oot_spares_review_loop_or_mandated_actions_are_claimed" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ISO_55001_2024_ASSET_MANAGEMENT_SYSTEM_REQUIREMENTS",
        "ISO_TC251_ISO55001_2024_DECISION_AND_IMPROVEMENT_GUIDANCE",
        "ISO_55000_2024_ASSET_LIFECYCLE_VALUE_PRINCIPLES",
    }


def test_nist_ot_change_and_backup_fact_does_not_create_universal_maintenance_checklist():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "nist_ot_configuration_change_control_and_backup_management_guidance"
    )
    assert fact["legacy_anchor_id"] == "maintenance_configuration_backup_change_handoff"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "no_universal_baseline_check_or_backup_for_every_maintenance_task_is_claimed" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "NIST_SP_800_82_REV_3_OT_CONFIGURATION_AND_BACKUP_CONTROLS",
        "NIST_SP_1339_OT_BACKUP_QUICK_START_GUIDE_2026",
    }


def test_osha_maintenance_work_control_fact_is_scoped_and_score_neutral():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "osha_scoped_hazardous_energy_control_and_psm_maintenance_work_practices"
    )
    assert fact["legacy_anchor_id"] == "maintenance_roles_competence_permit_restoration"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "osha_1910_147_applies_to_servicing_or_maintenance_with_hazardous_energy_exposure_scope" in fact["relation"]["conditions"]
    assert "no_universal_work_permit_sis_bypass_approval_or_functional_test_checklist_is_claimed" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "OSHA_29_CFR_1910_147_CONTROL_OF_HAZARDOUS_ENERGY",
        "OSHA_29_CFR_1910_119_PSM_SAFE_WORK_PRACTICES_AND_MAINTENANCE_TRAINING",
    }
    pack_path = ROOT / "rubrics/topic_packs" / fact["topic_id"] / "fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]


def test_osha_psm_deficiency_correction_fact_is_scoped_and_score_neutral():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "osha_psm_mechanical_integrity_deficiency_correction_scope"
    )
    assert fact["legacy_anchor_id"] == "inspection_findings_defect_priority_closeout"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "acceptable_limits_are_defined_by_the_process_safety_information" in fact["relation"]["conditions"]
    assert "no_universal_risk_priority_formula_work_order_format_or_retest_sequence_is_claimed" in fact["relation"]["conditions"]
    assert fact["verification_refs"][0]["authority_id"] == "OSHA_29_CFR_1910_119_PSM_MECHANICAL_INTEGRITY_AND_DEFICIENCY_CORRECTION"
    pack_path = ROOT / "rubrics/topic_packs" / fact["topic_id"] / "fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]


def test_iso14224_failure_data_anchor_does_not_claim_to_prescribe_rca_method():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "iso14224_failure_data_categories_and_site_specific_rca_boundary"
    )
    assert fact["legacy_anchor_id"] == "failure_coding_rca_bad_actor_feedback"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "failure_data_categories_include_cause_and_consequence_and_standardized_format" in fact["relation"]["conditions"]
    assert "standard_does_not_define_methods_for_analyzing_or_applying_reliability_maintenance_data" in fact["relation"]["conditions"]
    assert fact["verification_refs"][0]["authority_id"] == "ISO_14224_2016_FAILURE_DATA_CATEGORIES_AND_SCOPE"
    pack_path = ROOT / "rubrics/topic_packs" / fact["topic_id"] / "fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]


def test_hse_offshore_sis_deferral_guidance_is_not_generalized_to_all_maintenance():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "hse_offshore_sis_maintenance_test_deferral_risk_management_guidance"
    )
    assert fact["legacy_anchor_id"] == "deferred_maintenance_risk_control"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "scope_is_offshore_sis_component_maintenance_repair_and_testing_deferrals" in fact["relation"]["conditions"]
    assert "guidance_does_not_impose_one_universal_due_date_interim_safeguard_or_approval_regime_on_all_maintenance" in fact["relation"]["conditions"]
    assert fact["verification_refs"][0]["locator"] == "p. 30, Deferrals and Success Criteria"
    pack_path = ROOT / "rubrics/topic_packs" / fact["topic_id"] / "fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]


def test_iso_mttr_and_mttres_are_distinguished_in_fact_contract():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "iso14224_mttr_repair_vs_mttres_restoration_boundary"
    )
    assert fact["legacy_anchor_id"] == "kpi_mttr_definition_boundary"
    assert fact["review_status"] == "approved"
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "iso_tr_12489_mttres_includes_detection_pre_repair_delay_active_repair_and_time_until_available_for_return_to_operation" in fact["relation"]["conditions"]
    assert "mttr_and_mttres_are_not_interchangeable_across_standard_conventions" in fact["relation"]["conditions"]
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ISO_TR_12489_2013_REPAIR_AND_RESTORATION_TIME_TAXONOMY",
        "ISO_14224_2016_MTTR_MTTRES_DEFINITIONS",
    }
    pack_path = ROOT / "rubrics/topic_packs" / fact["topic_id"] / "fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == fact["legacy_anchor_id"])
    assert anchor["statement"] == fact["statement"] == anchor["claim"]


def test_registry_rejects_wrong_root():
    with pytest.raises(FactGroundedContractError):
        load_approved_fact_registry(Path("/tmp"))


def test_dp_remote_seal_fact_and_anchor_keep_liquid_fill_approximation_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "dp_level_remote_seal_pressure_transfer_architecture_and_limits")
    assert fact["verification_status"] == "verified"
    assert "not literally incompressible" in fact["statement"]
    pack = json.loads((ROOT / "rubrics/topic_packs/differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "dp_level_remote_seal_structure")
    assert "비압축성 충전액" not in anchor["statement"]
    assert anchor["statement"] == anchor["claim"] == anchor["description"]


def test_rosemount_1159_capillary_response_fact_is_product_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "rosemount_1159_capillary_length_increases_response_time")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "모든 remote-seal 설계의 정량 예측식으로 일반화하지 않는다" in fact["statement"]
    assert fact["verification_refs"][0]["authority_type"] == "official_documentation"
    pack = json.loads((ROOT / "rubrics/topic_packs/differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "dp_level_capillary_response_time")
    assert anchor["statement"] == fact["statement"]
    assert anchor["claim"] == anchor["description"] == anchor["statement"]


def test_two_layer_interface_equation_keeps_hydrostatic_assumptions_explicit():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "two_layer_interface_dp_equation_under_submerged_tap_conditions")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "both_taps_remain_submerged" in fact["relation"]["conditions"]
    assert "interface_height_is_between_lower_and_upper_taps" in fact["relation"]["conditions"]
    assert "P_lower=P_g" in fact["verification_refs"][0]["locator"]
    pack = json.loads((ROOT / "rubrics/topic_packs/differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "dp_level_interface_compensated_taps")
    assert anchor["statement"] == fact["statement"]
    assert anchor["claim"] == anchor["description"] == anchor["statement"]


def test_dp_level_remote_seal_and_impulse_line_facts_are_scoped_to_sources():
    registry = load_approved_fact_registry(ROOT)
    expected = {
        "dp_level_remote_seal_fill_fluid_head": "remote_seal_signed_fill_fluid_static_head",
        "dp_level_remote_seal_temperature_error": "rosemount_remote_seal_temperature_effect_mechanisms_scoped",
        "dp_level_capillary_length_symmetry": "rosemount_balanced_vs_tuned_remote_seal_temperature_effects",
        "dp_level_tank_geometry_volume_conversion": "dp_level_volume_output_requires_geometry_mapping",
        "dp_level_impulse_line_blockage_leak_bubble": "rosemount_impulse_piping_pressure_transfer_error_modes",
        "dp_level_impulse_line_freezing_and_heat_tracing": "impulse_line_freezing_plugs_and_isolates_transmitter",
        "dp_level_transmitter_mounting_elevation_error": "rosemount_1159_static_head_zero_error_and_rezero",
    }
    facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error"}
    pack = json.loads((ROOT / "rubrics/topic_packs/differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error/fact_anchor.json").read_text(encoding="utf-8"))
    anchors = {row["anchor_id"]: row for row in pack["anchors"]}
    for anchor_id, fact_id in expected.items():
        fact = facts[anchor_id]
        anchor = anchors[anchor_id]
        assert fact["fact_id"] == fact_id
        assert fact["verification_status"] == "verified"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"]
        assert fact["statement"] == anchor["statement"] == anchor["claim"] == anchor["description"]
    assert "head-temperature effect는 남는다" in facts["dp_level_capillary_length_symmetry"]["statement"]
    assert "모든 적용의 무조건적 최적해가 아니다" in facts["dp_level_capillary_length_symmetry"]["statement"]


def test_control_valve_vendor_crosscheck_fact_is_conditional_and_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_liquid_sizing_vendor_result_independent_crosscheck")
    assert fact["verification_status"] == "verified"
    assert fact["legacy_anchor_id"] == "vendor_crosscheck_liquid_phase_change"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "only when" in fact["statement"]
    assert "not an independent validation" in fact["statement"]
    assert fact["verification_refs"][0]["authority_id"] == "EMERSON_FISHER_CONTROL_VALVE_SOURCEBOOK_OIL_GAS_LIQUID_SIZING"
    pack = json.loads((ROOT / "rubrics/topic_packs/control_valve_cavitation_flashing_choked_flow_damage_prevention/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "vendor_crosscheck_liquid_phase_change")
    assert anchor["statement"]


def test_balance_seal_loading_fact_is_product_specific_not_universal():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "balanced_trim_seal_loading_is_construction_and_condition_specific")
    assert fact["verification_status"] == "verified"
    assert fact["legacy_anchor_id"] == "balance_seal_loading"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "one universal seal-load equation" in fact["statement"]
    assert {row["authority_type"] for row in fact["verification_refs"]} == {"official_documentation"}
    pack = json.loads((ROOT / "rubrics/topic_packs/balanced_trim_unbalanced_trim_structure_sealing_applications/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "balance_seal_loading")
    assert "preload" in anchor["statement"] and "wear" in anchor["statement"]


def test_balanced_trim_actuator_force_benefit_is_case_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "balanced_trim_force_advantage_is_case_specific_in_high_dp_or_large_valves")
    assert fact["verification_status"] == "verified"
    assert fact["legacy_anchor_id"] == "clean_high_dp_large_size_application"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "not a guarantee of a smaller actuator or zero force" in fact["statement"]
    assert len(fact["verification_refs"]) == 2
    pack = json.loads((ROOT / "rubrics/topic_packs/balanced_trim_unbalanced_trim_structure_sealing_applications/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "clean_high_dp_large_size_application")
    assert "조건부로" in anchor["statement"]


def test_vendor_force_seal_and_maintenance_data_are_model_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "balanced_trim_selection_should_be_reconciled_with_vendor_force_and_seal_data")
    assert fact["verification_status"] == "verified"
    assert fact["legacy_anchor_id"] == "vendor_cutaway_force_table_crosscheck"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "selected model and revision" in fact["statement"]
    assert len(fact["verification_refs"]) == 2
    pack = json.loads((ROOT / "rubrics/topic_packs/balanced_trim_unbalanced_trim_structure_sealing_applications/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "vendor_cutaway_force_table_crosscheck")
    assert "Vendor cutaway" in anchor["statement"]


def test_extreme_temperature_balanced_seal_checks_are_model_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "balanced_trim_extreme_temperature_seal_checks_are_model_specific")
    assert fact["verification_status"] == "verified"
    assert fact["legacy_anchor_id"] == "high_temperature_cryogenic_seal_limit"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "does not imply a common limit" in fact["statement"]
    assert len(fact["verification_refs"]) == 3
    pack = json.loads((ROOT / "rubrics/topic_packs/balanced_trim_unbalanced_trim_structure_sealing_applications/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "high_temperature_cryogenic_seal_limit")
    assert "clearance" in anchor["statement"] and "leakage" in anchor["statement"]


def test_elastomer_seal_degradation_modes_are_conditional_not_universal():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "balanced_trim_elastomer_seal_compatibility_and_failure_modes_are_condition_specific")
    assert fact["verification_status"] == "verified"
    assert fact["legacy_anchor_id"] == "fluid_compatibility_seal_degradation"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "applies_only_if_the_selected_seal_component_is_elastomeric" in fact["relation"]["conditions"]
    assert "do_not_generalize_these_mechanisms_to_ptfe_graphite_metallic_or_all_balance_seal_constructions" in fact["relation"]["conditions"]
    assert fact["verification_refs"][0]["authority_id"] == "PARKER_PRAEDIFA_O_RING_HANDBOOK_CONDITION_SPECIFIC_SEAL_SELECTION"
    pack = json.loads((ROOT / "rubrics/topic_packs/balanced_trim_unbalanced_trim_structure_sealing_applications/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "fluid_compatibility_seal_degradation")
    assert "탄성체 seal" in anchor["statement"]
    assert "일반화하지 않는다" in anchor["statement"]


def test_particulate_blockage_is_passage_and_model_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "balanced_trim_particulate_blockage_risk_is_passage_and_model_specific")
    assert fact["verification_status"] == "verified"
    assert fact["legacy_anchor_id"] == "dirty_slurry_particulate_limit"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "do_not_infer_universal_slurry_particle_limit_blockage_rate_or_seal_wear_rule" in fact["relation"]["conditions"]
    assert {row["authority_id"] for row in fact["verification_refs"]} == {
        "FISHER_HP_HPA_MANUAL_PARTICULATE_PASSAGES_BALANCE_HOLES",
        "EMERSON_FISHER_DIRTY_SERVICE_TRIM_PARTICULATE_CASE",
    }
    pack = json.loads((ROOT / "rubrics/topic_packs/balanced_trim_unbalanced_trim_structure_sealing_applications/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "dirty_slurry_particulate_limit")
    assert "모든 slurry" in anchor["statement"]
    assert "일반화하지 않는다" in anchor["statement"]


def test_operating_case_force_review_is_limited_to_defined_cases_and_selected_configuration():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "balanced_trim_defined_case_force_review_is_configuration_specific")
    assert fact["verification_status"] == "verified"
    assert fact["legacy_anchor_id"] == "operating_case_force_matrix"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert "startup_or_shutdown_are_included_when_present_in_design_basis_not_universal_required_cases" in fact["relation"]["conditions"]
    assert {row["authority_id"] for row in fact["verification_refs"]} == {
        "FISHER_SPECIFICATION_MANAGER_SERVICE_CONDITION_FIELDS",
        "FISHER_SOURCEBOOK_ACTUATOR_FORCE_CASES",
    }
    pack = json.loads((ROOT / "rubrics/topic_packs/balanced_trim_unbalanced_trim_structure_sealing_applications/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "operating_case_force_matrix")
    assert "모든 설비에 공통 필수라고 가정하지 않는다" in anchor["statement"]


def test_mcdc_definition_and_lower_coverage_distinctions_are_nasa_supported():
    registry = load_approved_fact_registry(ROOT)
    by_anchor = {
        row["legacy_anchor_id"]: row
        for row in registry["facts"]
        if row["topic_id"] == "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
    }
    expected = {
        "mcdc_purpose",
        "mcdc_definition",
        "mcdc_statement_coverage",
        "mcdc_decision_coverage",
        "mcdc_condition_coverage",
    }
    assert expected <= by_anchor.keys()
    for anchor_id in expected:
        fact = by_anchor[anchor_id]
        assert fact["verification_status"] == "verified"
        assert fact["score_effect"] == "none"
        assert fact["source_refs"] == []
        assert fact["verification_refs"]
    pack = json.loads((ROOT / "rubrics/topic_packs/safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis/fact_anchor.json").read_text(encoding="utf-8"))
    definition = next(row for row in pack["anchors"] if row["anchor_id"] == "mcdc_definition")
    assert "각 진입점·종료점 실행" in definition["statement"]
    assert "MC/DC 정의와 구분한다" not in definition["statement"]


def test_bode_closed_loop_transfer_distinguishes_general_and_unity_feedback():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "bode_open_closed_loop_transfer_relations")
    assert fact["verification_status"] == "verified"
    assert fact["legacy_anchor_id"] == "open_loop_closed_loop_roles"
    assert fact["source_refs"] == []
    assert fact["score_effect"] == "none"
    assert any(row["authority_type"] == "calculation" for row in fact["verification_refs"])
    pack = json.loads((ROOT / "rubrics/topic_packs/bode_frequency_response_stability_margin_bandwidth/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "open_loop_closed_loop_roles")
    assert "G(s)/(1+G(s)H(s))" in anchor["statement"]
    assert "H(s)=1일 때에만" in anchor["statement"]


def test_control_valve_deadband_hysteresis_backlash_static_friction_scope():
    registry = load_approved_fact_registry(ROOT)
    by_anchor = {
        row["legacy_anchor_id"]: row
        for row in registry["facts"]
        if row["topic_id"] == "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    }
    expected = {
        "deadband_definition_direction_reversal",
        "backlash_mechanical_clearance",
        "hysteresis_direction_dependent_output",
        "static_friction_starting_force",
    }
    assert expected <= by_anchor.keys()
    assert by_anchor["stiction_stick_then_jump"]["verification_status"] == "verified"
    for anchor_id in expected:
        fact = by_anchor[anchor_id]
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert fact["source_refs"] == []
        assert fact["verification_refs"]


def test_ultrasonic_round_trip_distance_anchor_has_direct_manufacturer_support():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ultrasonic_echo_distance_uses_round_trip_time_over_two")
    assert fact["verification_status"] == "verified"
    assert fact["source_refs"] == []
    assert fact["score_effect"] == "none"
    pack = json.loads((ROOT / "rubrics/topic_packs/ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "ultrasonic_round_trip_distance_equation")
    assert "d=ct/2" in anchor["statement"]
    assert "왕복" in anchor["statement"]


@pytest.mark.parametrize(
    ("fact_id", "anchor_id"),
    [
        ("ultrasonic_distance_conversion_uses_medium_sound_speed", "ultrasonic_sound_speed_medium_dependence"),
        ("ultrasonic_air_temperature_changes_uncompensated_range", "ultrasonic_air_temperature_compensation"),
    ],
)
def test_ultrasonic_sound_speed_conditions_are_manufacturer_supported(fact_id, anchor_id):
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    assert fact["verification_status"] == "verified"
    assert fact["source_refs"] == []
    assert fact["score_effect"] == "none"
    pack = json.loads((ROOT / "rubrics/topic_packs/ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert anchor["statement"]


@pytest.mark.parametrize(
    ("fact_id", "anchor_id"),
    [
        ("ultrasonic_transducer_piezoelectric_transmit_receive", "ultrasonic_piezoelectric_transduction"),
        ("ultrasonic_pulse_echo_measures_emission_to_echo_return_time", "ultrasonic_pulse_echo_time_of_flight"),
        ("ultrasonic_nearby_sensor_crosstalk_risk", "ultrasonic_sensor_crosstalk"),
        ("ultrasonic_target_geometry_surface_affects_echo_detection", "ultrasonic_target_reflectivity_orientation"),
        ("ultrasonic_beam_footprint_expands_with_range", "ultrasonic_beam_angle_footprint"),
        ("ultrasonic_level_is_bottom_reference_minus_surface_distance", "ultrasonic_level_measurement_reference"),
        ("ultrasonic_internal_obstruction_and_multipath_false_echoes", "ultrasonic_false_echo_multiple_reflection"),
        ("ultrasonic_echo_size_is_diagnostic_not_distance_basis", "ultrasonic_echo_amplitude_validity"),
        ("ultrasonic_installation_alignment_nozzle_and_obstruction_controls", "ultrasonic_mounting_nozzle_obstruction_error"),
        ("ultrasonic_process_conditions_can_degrade_echo_measurement", "ultrasonic_foam_vapor_turbulence_error"),
        ("ultrasonic_monostatic_ringdown_and_blanking_create_dead_zone", "ultrasonic_dead_zone_ringdown"),
        ("ultrasonic_sensor_signal_chain_is_partitioned_by_function", "ultrasonic_sensor_system_structure"),
        ("ultrasonic_frequency_tradeoff_resolution_directivity_attenuation_range", "ultrasonic_frequency_range_resolution_tradeoff"),
        ("ultrasonic_maximum_range_depends_on_link_budget_and_target", "ultrasonic_attenuation_max_range"),
    ],
)
def test_ultrasonic_operating_principle_and_interference_facts_have_manufacturer_support(fact_id, anchor_id):
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    assert fact["verification_status"] == "verified"
    assert fact["source_refs"] == []
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"]
    pack = json.loads((ROOT / "rubrics/topic_packs/ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert anchor["statement"]


@pytest.mark.parametrize(
    ("fact_id", "anchor_id"),
    [
        ("gear_tooth_speed_sensor_target_geometry_and_gap_are_device_limited", "proximity_airgap_target_error"),
        ("dc_tachogenerator_direction_load_temperature_ripple_and_mounting_effects", "tachogenerator_direction_loading_error"),
        ("speed_sensor_selection_must_cover_operating_envelope_and_dynamic_limits", "selection_speed_range_low_high"),
        ("encoder_speed_feedback_selection_must_match_receiver_limits", "lifecycle_maintainability_selection"),
    ],
)
def test_speed_measurement_facts_have_manufacturer_support(fact_id, anchor_id):
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    assert fact["verification_status"] == "verified"
    assert fact["source_refs"] == []
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"]
    pack = json.loads((ROOT / "rubrics/topic_packs/speed_rotation_measurement_encoder_proximity_tachometer_selection_error/fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert anchor["statement"]


def test_speed_composite_fact_anchors_are_scoped_to_verified_evidence():
    registry = load_approved_fact_registry(ROOT)
    facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == "speed_rotation_measurement_encoder_proximity_tachometer_selection_error"}
    pack = json.loads((ROOT / "rubrics/topic_packs/speed_rotation_measurement_encoder_proximity_tachometer_selection_error/fact_anchor.json").read_text(encoding="utf-8"))
    anchors = {row["anchor_id"]: row for row in pack["anchors"]}

    proximity = anchors["proximity_airgap_target_error"]["statement"]
    assert "operating air gap" in proximity
    assert "보편적인 dropout 한계는 단정하지 않는다" in proximity
    assert "pulse amplitude·duty·dropout이 달라질 수 있으므로" not in proximity
    assert facts["proximity_airgap_target_error"]["verification_status"] == "verified"

    tacho = anchors["tachogenerator_direction_loading_error"]["statement"]
    assert "특정 TDP 모델" in tacho
    assert "모델별 data sheet" in tacho
    assert "linearity와 zero에 영향을" not in tacho
    assert facts["tachogenerator_direction_loading_error"]["verification_status"] == "verified"

    selection = anchors["selection_speed_range_low_high"]["statement"]
    assert "sensor·signal-conditioning·receiver 전체 사양" in selection
    assert "보편적 RPM 임계값은 없다" in selection
    assert facts["selection_speed_range_low_high"]["verification_status"] == "verified"

    mounting = anchors["mechanical_mounting_coupling_error"]["statement"]
    assert "제품별" in mounting
    assert "coupling slip이나 보편적인 torsional-vibration 오류를 주장하지 않는다" in mounting
    assert facts["mechanical_mounting_coupling_error"]["verification_status"] == "verified"


def test_independent_fact_verification_is_not_blocked_by_wordpress_source_state(tmp_path):
    source_registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in source_registry["facts"] if row["source_refs"])
    registry = {**source_registry, "facts": [fact]}
    registry_dir = tmp_path / "grading" / "evidence"
    registry_dir.mkdir(parents=True)
    (registry_dir / "approved_fact_registry.json").write_text(json.dumps(registry), encoding="utf-8")
    master_dir = tmp_path / "master_topic_packs"
    master_dir.mkdir()
    (master_dir / f"{fact['topic_id']}.json").write_text(
        json.dumps({"topic_id": fact["topic_id"], "sources": []}), encoding="utf-8"
    )

    loaded = load_approved_fact_registry(tmp_path)
    assert loaded["facts"][0]["verification_status"] == "verified"


@pytest.mark.parametrize(
    ("fact_id", "anchor_id"),
    [
        ("optical_noncontact_measurement_emission_interaction_reception_processing_chain", "optical_noncontact_measurement_chain"),
        ("photoelectric_receiver_converts_received_light_change_to_electrical_output", "photoelectric_conversion_principle"),
        ("through_beam_photoelectric_sensing_uses_opposed_emitter_receiver", "photoelectric_through_beam_mode"),
        ("retroreflective_photoelectric_sensing_uses_return_reflector_path", "photoelectric_retroreflective_mode"),
        ("diffuse_photoelectric_sensing_uses_target_scattered_light", "photoelectric_diffuse_reflective_mode"),
        ("diffuse_photoelectric_intensity_and_distance_setting_principle_boundary", "photoelectric_intensity_boundary"),
        ("direct_tof_measures_optical_pulse_round_trip_delay", "optical_direct_tof_round_trip"),
        ("indirect_tof_uses_modulated_light_phase_delay", "optical_indirect_tof_phase_principle"),
        ("laser_triangulation_maps_reflected_spot_position_to_range", "laser_triangulation_principle"),
        ("laser_triangulation_detector_coordinate_encodes_target_depth", "laser_triangulation_detector_coordinate"),
        ("laser_triangulation_distance_mapping_depends_on_device_geometry_and_calibration", "laser_triangulation_calibration"),
        ("laser_triangulation_speckle_perturbs_spot_localization_on_rough_surfaces", "laser_speckle_effect"),
        ("single_frequency_itof_phase_wraps_and_multifrequency_unwraps_range", "optical_itof_phase_ambiguity"),
    ],
)
def test_optical_measurement_facts_are_independently_sourced_and_non_scoring(fact_id, anchor_id):
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    assert fact["legacy_anchor_id"] == anchor_id
    assert fact["verification_status"] == "verified"
    assert fact["source_refs"] == []
    assert fact["verification_refs"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/optical_laser_photoelectric_noncontact_measurement_tof_triangulation/fact_anchor.json").read_text(encoding="utf-8")
    )
    assert any(anchor["anchor_id"] == anchor_id and anchor["statement"] for anchor in pack["anchors"])


@pytest.mark.parametrize(
    ("fact_id", "anchor_id"),
    [
        ("rosemount_5408_upper_null_zone_suppresses_measurement_and_api2350_cat3_independence", "radar_upper_null_zone_overfill_coordination"),
        ("magnetrol_706_single_rod_installation_and_nozzle_reflection_effects", "gwr_quasi_tem_return_path"),
    ],
)
def test_radar_level_facts_are_scope_limited_and_non_scoring(fact_id, anchor_id):
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    assert fact["legacy_anchor_id"] == anchor_id
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert fact["verification_refs"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    assert anchor["statement"] == fact["statement"]


def test_protective_earth_and_signal_reference_fact_is_independently_sourced_and_non_scoring():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_protective_earth_and_signal_reference_ground_distinction")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_pe_signal_reference_boundary"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "OSHA_ELECTRICAL_EQUIPMENT_GROUNDING_FAULT_CURRENT_PATH",
        "NI_CHASSIS_EARTH_SIGNAL_GROUND_TERMINOLOGY",
    }
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "보호접지" in anchor["statement"]
    assert "임의 해제해서는 안 된다" in anchor["statement"]


def test_ground_loop_mechanism_fact_is_independently_sourced_and_non_scoring():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_ground_loop_multiple_paths_potential_difference_current_disturbance")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_ground_loop_mechanism"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 1
    assert fact["verification_refs"][0]["authority_id"] == "ANALOG_DEVICES_GROUND_LOOP_SIGNAL_CORRUPTION"
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "전위차" in anchor["statement"]
    assert "순환전류" in anchor["statement"]


def test_ground_loop_mitigation_preserves_pe_and_scopes_shield_termination():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_ground_loop_mitigation_uses_signal_path_not_pe_lifting")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_ground_loop_safe_mitigation"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 3
    assert "single_end_shield_grounding_is_only_the_cited_capacitive_coupling_example_not_a_universal_rule" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "절연·차동입력·적절한 차폐 접속" in anchor["statement"]
    assert "PE 같은 안전 접지를 제거" in anchor["statement"]


def test_vfd_and_signal_cable_separation_fact_is_coupling_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_vfd_motor_and_signal_cable_separation_reduces_coupling")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_cable_separation_coupling"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert "minimum_separation_distance_is_not_universal_and_follows_the_applicable_drive_and_site_requirements" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "VFD" in anchor["statement"]
    assert "평행구간 최소화" in anchor["statement"]
    assert "90" in fact["statement"]


def test_emi_coupling_paths_fact_has_source_path_victim_evidence():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_emi_source_path_victim_and_coupling_types")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_emi_coupling_paths"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "conducted" in anchor["statement"]
    assert "radiated" in anchor["statement"]
    assert "source-path-victim" in anchor["statement"]


def test_common_differential_mode_fact_scopes_filter_and_receiver_limits():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_common_differential_noise_requires_mode_specific_mitigation")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_common_differential_mode"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 4
    assert "common_mode_rejection_is_limited_by_device_common_mode_range_and_frequency_dependent_cmrr" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "differential-mode와 common-mode" in anchor["statement"]
    assert "CMRR, 절연, 필터와 본딩" in anchor["statement"]


def test_ups_function_fact_scopes_backup_and_optional_isolation_features():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_ups_continuity_and_galvanic_isolation_is_configuration_specific")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_ups_function_boundary"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert "galvanic_isolation_is_present_only_when_the_applicable_isolation_transformer_or_equivalent_design_is_provided" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "요구된 시간 동안" in anchor["statement"]
    assert "galvanic-isolation 문제를 자동으로 제거" in anchor["statement"]


def test_redundant_power_supply_fact_accounts_for_shared_primary_feed():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_power_supply_redundancy_is_limited_by_shared_upstream_paths")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_redundant_supply_boundary"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert "a_common_component_is_a_potential_shared_failure_path_not_a_quantified_failure_probability_without_reliability_data" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "공통 입력전원" in anchor["statement"]
    assert "완전한 이중화가 아니다" in anchor["statement"]


def test_power_quality_diagnostic_fact_limits_temporal_correlation_claim():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_power_quality_diagnostics_correlate_disturbance_events_and_transfer_timing")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_power_quality_scope"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 3
    assert "a_temporal_match_is_diagnostic_evidence_not_proof_of_causation" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "sag, swell, interruption" in anchor["statement"]
    assert "증상 시간대와 연계" in anchor["statement"]


def test_dc_supply_distribution_fact_is_load_and_installation_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_dc_distribution_capacity_drop_selectivity_and_return_path_review")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_dc_supply_distribution"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 4
    assert "design_values_and_protection_choices_are_installation_and_component_specific" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "distribution voltage drop" in anchor["statement"]
    assert "common return impedance" in anchor["statement"]


def test_emc_source_path_victim_fact_is_a_diagnostic_framework_not_universal_fix():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_emc_source_path_victim_model_guides_layered_mitigation")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_source_path_victim_mitigation"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 3
    assert "a_single_filter_or_grounding_change_is_not_assumed_sufficient_without_retesting_the_affected_system" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "source의 발생 저감" in anchor["statement"]
    assert "단일 필터나 단일 접지 변경" in anchor["statement"]


def test_grounding_topology_fact_rejects_universal_star_ground_prescription():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_grounding_topology_is_current_path_and_system_specific")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_single_multi_point_conditional"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert "the_single_board_star_ground_example_is_not_generalized_to_all_multiboard_or_facility_grounding_systems" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "어느 한 방식이 모든 계장 시스템에 항상 우월하지 않다" in anchor["statement"]


def test_signal_cable_shield_fact_preserves_specific_power_cable_pe_exception():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_signal_cable_shield_is_not_assumed_pe_or_load_return")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_shield_not_pe"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 3
    assert "a_shield_or_armor_used_as_pe_is_a_specific_exception_for_a_cable_designed_and_verified_for_that_role" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "기본적으로 보호접지 도체" in anchor["statement"]
    assert "적용 안전기준의 고장전류" in anchor["statement"]


def test_shield_termination_fact_keeps_examples_application_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_shield_termination_depends_on_coupling_and_bonding_context")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_shield_termination_frequency"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert "neither_termination_method_is_a_universal_rule" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "one-end 또는 both-end/360-degree termination" in anchor["statement"]
    assert "주파수와 본딩 조건" in anchor["statement"]


def test_emi_filter_installation_fact_uses_vendor_scoped_recommendations():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_emi_filter_installation_controls_bypass_coupling_and_bond_impedance")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_filter_entry_bonding"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 3
    assert "manufacturer_instructions_and_system_emc_test_results_control_the_final_layout" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "enclosure power entry 가까이에" in anchor["statement"]
    assert "unfiltered input과 filtered output 배선을 분리" in anchor["statement"]


def test_spd_fact_scopes_coordination_and_connection_lead_effects():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_spd_coordination_and_short_low_impedance_connections_limit_residual_surge_voltage")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_spd_coordination"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 3
    assert "numeric_lead_length_and_coordination_limits_are_not_generalized_beyond_their_stated_standard_and_product_context" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "전원·신호 경로의 SPD" in anchor["statement"]
    assert "접속 리드의 임피던스" in anchor["statement"]


def test_ups_sizing_fact_limits_load_and_battery_margins_to_vendor_context():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_ups_sizing_checks_load_power_dynamics_runtime_and_battery_conditions")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_ups_sizing_factors"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 4
    assert "no_universal_capacity_margin_or_battery_correction_factor_is_asserted" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "W와 VA" in anchor["statement"]
    assert "battery aging" in anchor["statement"]


def test_ups_neutral_bonding_fact_is_topology_specific_and_safety_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_ups_neutral_ground_bonding_depends_on_topology_and_transfer_paths")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_ups_bypass_grounding"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 3
    assert "all_changes_follow_the_exact_ups_manual_site_single_line_and_local_code_and_are_performed_by_qualified_personnel" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "normal·battery·bypass" in anchor["statement"]
    assert "neutral을 임의 결선" in anchor["statement"]


def test_frequency_and_timing_fact_uses_signatures_as_candidate_evidence_only():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_frequency_and_event_timing_are_diagnostic_clues_not_causation")
    assert fact["topic_id"] == "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
    assert fact["legacy_anchor_id"] == "ipgse_symptom_frequency_correlation"
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 4
    assert "event_timestamp_correlation_is_diagnostic_evidence_not_causation" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "50/60 Hz 성분" in anchor["statement"]
    assert "인과 증명으로 취급하지 않는다" in anchor["statement"]


def test_measurement_reference_common_mode_and_probe_ratings_are_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_measurement_reference_ground_common_mode_and_ratings_checked_before_connection")
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert {row["authority_id"] for row in fact["verification_refs"]} == {
        "NI_FIELD_WIRING_COMMON_MODE_GROUND_LOOP",
        "FLUKE_MEASUREMENT_TOOL_SELECTION_SAFETY",
    }
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "입력 공통모드 범위" in anchor["statement"]
    assert "계측기·프로브 정격" in anchor["statement"]
    assert "보호접지" not in anchor["statement"]


def test_high_frequency_bonding_claim_is_application_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_high_frequency_bonding_geometry_controls_impedance")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert any("not_universal_dimensions" in condition for condition in fact["relation"]["conditions"])
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "고주파 본딩" in anchor["statement"]
    assert "보호요건" in anchor["statement"]


def test_noise_diagnosis_distinguishes_candidate_source_path_victim():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_noise_diagnosis_separates_source_path_and_victim")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert "actual_cause_is_established_from_the_specific_setup_and_measurement_evidence" in fact["relation"]["conditions"]
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "결합경로(coupling path)" in anchor["statement"]
    assert "실제 원인은 측정" in anchor["statement"]


def test_analog_noise_workflow_is_scoped_to_documented_ni_daq_methods():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_noise_diagnosis_uses_spectrum_setup_and_component_isolation")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 1
    assert any("not_a_universal_mandated_sequence" in condition for condition in fact["relation"]["conditions"])
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "FFT 등으로 주파수 특징" in anchor["statement"]
    assert "한 번에 하나씩 분리·비교" in anchor["statement"]


def test_noise_mitigation_keeps_baseline_evidence_and_safety_boundary():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_noise_mitigation_preserves_before_after_measurement_evidence")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert any("not_proof_of_causation" in condition for condition in fact["relation"]["conditions"])
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "같은 측정 구성·운전상태" in anchor["statement"]
    assert "보호접지를 임의 해제하지 않는다" in anchor["statement"]


def test_post_mitigation_verification_is_safe_and_application_specific():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "ipgse_mitigation_followup_compares_measurement_to_baseline_and_spec")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 1
    assert any("not_a_universal_formal_acceptance_requirement" in c for c in fact["relation"]["conditions"])
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "계측기 사양을 재확인" in anchor["statement"]
    assert "안전한 시험절차" in anchor["statement"]


def test_grounding_pack_cross_topic_boundaries_are_structurally_resolved():
    boundaries = {
        "ipgse_topic2_boundary": ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", ("cable", "tubing", "installation")),
        "ipgse_topic3_boundary": ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", ("emc", "temperature", "vibration")),
        "ipgse_topic4_boundary": ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", ("hardware", "panel", "component")),
        "ipgse_topic5_boundary": ("electronics_error_noise_drift_tolerance_aging_power_mitigation", ("noise", "drift", "tolerance")),
    }
    source_pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_power_grounding_shielding_ups_ground_loop_emc/fact_anchor.json").read_text(encoding="utf-8")
    )
    source_anchors = {row["anchor_id"]: row for row in source_pack["anchors"]}
    for anchor_id, (target_topic, expected_terms) in boundaries.items():
        anchor = source_anchors[anchor_id]
        assert target_topic in anchor["statement"]
        target_dir = ROOT / "rubrics/topic_packs" / target_topic
        assert (target_dir / "fact_anchor.json").is_file()
        target_text = (target_dir / "README.md").read_text(encoding="utf-8").lower()
        target_text += (target_dir / "fact_anchor.json").read_text(encoding="utf-8").lower()
        assert all(term in target_text for term in expected_terms)


def test_pid_line_list_spec_and_nozzle_crosscheck_is_project_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "pid_line_list_spec_and_nozzle_relations_checked_when_project_uses_them")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 3
    assert "autodesk_plant_3d_is_an_implementation_example_not_a_universal_project_requirement" in fact["relation"]["conditions"]
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "사용하는 경우" in anchor["statement"]
    assert "승인된 project design basis" in anchor["statement"]


def test_production_energy_intensity_accounts_for_relevant_variables():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "production_energy_intensity_uses_enpi_baseline_and_relevant_variables")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 3
    assert "simple_energy_intensity_is_not_always_a_fair_efficiency_comparison_when_product_mix_or_other_relevant_variables_change" in fact["relation"]["conditions"]
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_production_management_planning_quality_cost_resources/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "EnPI와 기준선" in anchor["statement"]
    assert "peak·idle loss" not in anchor["statement"]


def test_production_schedule_kpi_definitions_are_reproducible_and_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "production_schedule_kpi_defines_freeze_period_and_completion_basis")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert "late_order_cause_categories_are_locally_defined_not_a_universal_iso_taxonomy" in fact["relation"]["conditions"]
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_production_management_planning_quality_cost_resources/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "freeze 시점" in anchor["statement"]
    assert "구현 예" in anchor["statement"]


def test_production_management_scope_matches_iso22400_without_universal_goal_order():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "production_management_scope_follows_iso22400_mom_activities_and_local_goals")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert len(fact["verification_refs"]) == 2
    assert "the_standard_does_not_prescribe_one_universal_priority_order_for_safety_quality_delivery_and_cost_goals" in fact["relation"]["conditions"]
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/instrumentation_production_management_planning_quality_cost_resources/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == fact["legacy_anchor_id"])
    assert "organization-specific" not in anchor["statement"]
    assert "규제요건에 맞춘다" in anchor["statement"]


def test_active_triangulation_uncertainty_fact_is_geometry_scoped_and_non_scoring():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row
        for row in registry["facts"]
        if row["fact_id"] == "active_triangulation_distance_uncertainty_depends_on_geometry"
    )
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["legacy_anchor_id"] == "triangulation_range_resolution_tradeoff"
    assert len(fact["verification_refs"]) == 2
    assert "far_field_approximation_requires_distance_much_greater_than_focal_length" in fact["relation"]["conditions"]
    pack = json.loads(
        (ROOT / "rubrics/topic_packs/optical_laser_photoelectric_noncontact_measurement_tof_triangulation/fact_anchor.json").read_text(encoding="utf-8")
    )
    anchor = next(row for row in pack["anchors"] if row["id"] == fact["legacy_anchor_id"])
    assert "제품의 성능 보증값은 아니다" in anchor["statement"]
    assert "δd≈d²·δu/(f·b)" in anchor["statement"]


def test_optical_return_signal_occlusion_and_timing_facts_are_source_scoped():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "optical_laser_photoelectric_noncontact_measurement_tof_triangulation"
    expected = {
        "surface_reflectivity_color_effect": "direct_tof_target_surface_changes_return_pulse_amplitude",
        "alignment_occlusion_geometry": "active_triangulation_shadowing_occultation_and_baseline_tradeoff",
        "tof_timing_jitter_resolution": "direct_tof_timing_uncertainty_propagates_to_distance_uncertainty",
    }
    facts = {
        row["legacy_anchor_id"]: row
        for row in registry["facts"]
        if row["topic_id"] == topic_id and row["legacy_anchor_id"] in expected
    }
    assert set(facts) == set(expected)
    for anchor_id, fact_id in expected.items():
        fact = facts[anchor_id]
        assert fact["fact_id"] == fact_id
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert len(fact["verification_refs"]) == 1
        assert fact["verification_refs"][0]["authority_type"] == "official_documentation"


def test_metrology_terms_and_tof_filtering_are_verified_with_scoped_sources():
    registry = load_approved_fact_registry(ROOT)
    topic_id = "optical_laser_photoelectric_noncontact_measurement_tof_triangulation"
    expected = {
        "accuracy_resolution_repeatability_boundary": "vim_distinguishes_resolution_repeatability_and_accuracy",
        "ambient_light_filtering": "hamamatsu_direct_tof_uses_wavelength_centered_filter_for_background",
    }
    facts = {
        row["legacy_anchor_id"]: row
        for row in registry["facts"]
        if row["topic_id"] == topic_id and row["legacy_anchor_id"] in expected
    }
    assert set(facts) == set(expected)
    for anchor_id, fact_id in expected.items():
        fact = facts[anchor_id]
        assert fact["fact_id"] == fact_id
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"]


def test_control_valve_deadband_and_dead_time_use_distinct_measurement_definitions():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_deadband_signal_range_is_distinct_from_dead_time_interval")
    topic_dir = ROOT / "rubrics/topic_packs/control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
    pack = json.loads((topic_dir / "fact_anchor.json").read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["id"] == "deadband_not_dead_time")
    logic = json.loads((topic_dir / "logic_check.json").read_text(encoding="utf-8"))
    assert fact["legacy_anchor_id"] == "deadband_not_dead_time"
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert len(fact["verification_refs"]) == 2
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_CH1_DEADBAND",
        "EMERSON_FISHER_CONTROL_VALVE_HANDBOOK_CH2_DEAD_TIME",
    }
    assert "deadband_is_measured_after_input_direction_reversal_and_requires_specified_input_and_output_variables" in fact["relation"]["conditions"]
    assert fact["score_effect"] == "none"
    assert fact["statement"] in logic["llm_profile"]["truth_schema"]
    stiction = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_stiction_static_friction_can_cause_stick_jump_motion")
    stiction_anchor = next(row for row in pack["anchors"] if row["id"] == "stiction_stick_then_jump")
    assert stiction["legacy_anchor_id"] == "stiction_stick_then_jump"
    assert stiction["statement"] == stiction_anchor["statement"] == stiction_anchor["claim"]
    assert len(stiction["verification_refs"]) == 2
    assert "cause_diagnosis_requires_the_specific_valve_positioner_actuator_and_test_context" in stiction["relation"]["conditions"]
    assert stiction["score_effect"] == "none"
    assert stiction["statement"] in logic["llm_profile"]["truth_schema"]
    stick_slip = next(row for row in registry["facts"] if row["fact_id"] == "control_valve_stiction_has_stationary_and_slip_jump_travel_phases")
    stick_slip_anchor = next(row for row in pack["anchors"] if row["id"] == "stick_slip_repeated_motion")
    assert stick_slip["legacy_anchor_id"] == "stick_slip_repeated_motion"
    assert stick_slip["statement"] == stick_slip_anchor["statement"] == stick_slip_anchor["claim"]
    assert len(stick_slip["verification_refs"]) == 2
    assert "one_slip_jump_alone_does_not_establish_a_repeating_cycle_or_process_variable_oscillation" in stick_slip["relation"]["conditions"]
    assert stick_slip["score_effect"] == "none"
    assert stick_slip["statement"] in logic["llm_profile"]["truth_schema"]


def test_control_valve_pipe_transmission_loss_fact_is_frequency_and_scope_limited():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_pipe_transmission_loss_depends_on_geometry_material_frequency_and_fluid_service"
    )
    pack_path = ROOT / "rubrics/topic_packs/control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim/fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "pipe_transmission_loss_dependency")
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 2
    assert "the_cited_iec_60534_8_3_method_is_limited_to_steel_and_steel_alloy_pipes_and_its_documented_applicability" in fact["relation"]["conditions"]


def test_control_valve_diffuser_fact_is_capacity_and_service_scoped():
    registry = load_approved_fact_registry(ROOT)
    fact = next(
        row for row in registry["facts"]
        if row["fact_id"] == "control_valve_diffuser_pressure_drop_capacity_erosion_and_noise_must_be_evaluated"
    )
    pack_path = ROOT / "rubrics/topic_packs/control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim/fact_anchor.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "diffuser_pressure_drop_distribution")
    assert fact["legacy_anchor_id"] == anchor["anchor_id"]
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert len(fact["verification_refs"]) == 2
    assert "fixed_diffuser_or_attenuator_capacity_and_intermediate_pressure_are_sized_for_the_governing_flow_case" in fact["relation"]["conditions"]
    assert "diffuser_flow_velocity_and_erosion_controls_depend_on_impurities_wet_steam_and_other_service_conditions" in fact["relation"]["conditions"]


def test_nist_ot_incident_response_plan_fact_is_limited_to_section_3_3_8():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_incident_response_plan_contents")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_incident_response_plan")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["locator"] == "§3.3.8, pp. 41–42"
    assert "the_source_does_not_establish_that_this_list_is_exhaustive_for_every_organization" in fact["relation"]["conditions"]


def test_nist_ot_recovery_continuity_fact_is_limited_to_recovery_objectives():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_recovery_objectives_and_continuity_plans")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_business_continuity")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["locator"] == "§3.3.9, pp. 42–43"
    assert "the_source_does_not_require_every_site_to_use_identical_manual_operation_or_alternate_communications_procedures" in fact["relation"]["conditions"]


def test_nist_ot_criticality_anchor_uses_organizational_goal_and_loss_impact_basis():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_ir8179_criticality_prioritizes_by_goal_importance_and_loss_impact")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_criticality_classification")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "NIST_IR_8179_CRITICALITY_ANALYSIS_PROCESS_MODEL"
    assert "the_claim_does_not_prescribe_a_universal_fixed_factor_list_or_numeric_scoring_formula" in fact["relation"]["conditions"]


def test_nist_ot_recovery_fact_is_limited_to_supported_recovery_capability():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_recovery_preincident_state_backups_and_plan_tests")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_trusted_recovery")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["locator"].startswith("§3.3.9")
    assert "the_claim_does_not_require_a_specific_credential_reset_staged_restore_or_heightened_monitoring_sequence" in fact["relation"]["conditions"]


def test_nist_ot_backup_plan_fact_does_not_make_optional_storage_controls_mandatory():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nist_80082r3_ot_risk_based_backup_plan_and_immutable_storage")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_backup_recovery_security")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["locator"] == "Appendix E, §§E.3.1–E.3.2, pp. 210–211"
    assert "immutable_storage_is_presented_as_an_option_for_additional_integrity_not_a_mandatory_control" in fact["relation"]["conditions"]


def _assert_nist_ot_supply_chain_fact(fact_id: str, anchor_id: str, authority_id: str):
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == authority_id
    return fact


def test_nist_ot_supply_chain_risks_are_identified_without_universal_contract_checklist():
    fact = _assert_nist_ot_supply_chain_fact(
        "nist_80082r3_ot_supply_chain_risks_contracts_assessments_response",
        "sw09_supply_chain_risk",
        "NIST_SP_800_82R3_OT_SUPPLY_CHAIN_RISK",
    )
    assert "§6.1.5" in fact["verification_refs"][0]["locator"]
    assert "the_claim_does_not_require_a_universal_supplier_substitution_strategy_or_fixed_contract_clause_set" in fact["relation"]["conditions"]


def test_nist_ot_supplier_assurance_is_limited_to_authenticity_and_supplier_review():
    fact = _assert_nist_ot_supply_chain_fact(
        "nist_80082r3_ot_supplier_authenticity_and_review",
        "sw09_supplier_assurance",
        "NIST_SP_800_82R3_OT_SUPPLIER_ASSURANCE",
    )
    assert "serial number" in fact["statement"]
    assert "the_source_does_not_define_a_universal_secure_development_or_vulnerability_disclosure_contract_clause_list" in fact["relation"]["conditions"]


def test_nist_sbom_claim_is_limited_to_component_dependency_and_vulnerability_context():
    fact = _assert_nist_ot_supply_chain_fact(
        "nist_80082r3_sbom_components_dependencies_vulnerability_impact",
        "sw09_sbom",
        "NIST_SP_800_82R3_SBOM_GUIDANCE",
    )
    assert "§6.1.5" in fact["verification_refs"][0]["locator"]
    assert "the_claim_does_not_assert_that_an_sbom_alone_proves_exploitability_runtime_exposure_or_product_security" in fact["relation"]["conditions"]


def test_nist_ot_software_firmware_authenticity_excludes_unsupported_properties():
    fact = _assert_nist_ot_supply_chain_fact(
        "nist_80082r3_ot_software_firmware_authenticity_checks",
        "sw09_software_firmware_integrity",
        "NIST_SP_800_82R3_OT_SOFTWARE_FIRMWARE_AUTHENTICITY",
    )
    assert "Appendix F, SI-7(15)" in fact["verification_refs"][0]["locator"]
    assert "the_claim_does_not_assert_secure_transfer_compatibility_or_rollback_protection_as_covered_by_these_citations" in fact["relation"]["conditions"]


def _assert_nist_ot_access_fact(fact_id: str, anchor_id: str, authority_id: str):
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == fact_id)
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == anchor_id)
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_status"] == "verified" and fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == authority_id
    return fact


def test_nist_ot_least_privilege_is_limited_to_job_required_scope():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_least_privilege_and_separation_of_duties", "sw09_least_privilege", "NIST_SP_800_82R3_OT_LEAST_PRIVILEGE")
    assert "§6.2.1.1" in fact["verification_refs"][0]["locator"]
    assert "the_claim_does_not_require_a_universal_privilege_review_interval_or_privileged_activity_monitoring_rule" in fact["relation"]["conditions"]


def test_nist_ot_authentication_fact_covers_identity_and_credential_lifecycle():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_identity_management_credentials_and_lifecycle", "sw09_authentication", "NIST_SP_800_82R3_OT_IDENTITY_MANAGEMENT")
    assert "issuance·revocation·update" in fact["statement"]
    assert "the_claim_does_not_assert_lockout_thresholds_or_exception_handling_as_defined_requirements_in_this_section" in fact["relation"]["conditions"]


def test_nist_ot_authorization_fact_distinguishes_acl_rbac_and_abac():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_acl_rbac_abac_access_control_models", "sw09_authorization", "NIST_SP_800_82R3_OT_ACCESS_CONTROL_MODELS")
    assert "§6.2.1.1" in fact["verification_refs"][0]["locator"]
    assert "not_a_required_combined_stack" in fact["relation"]["conditions"][1]


def test_nist_ot_remote_access_is_business_justified_and_restricted():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_remote_access_justification_scope_and_revoke", "sw09_remote_access", "NIST_SP_800_82R3_OT_REMOTE_ACCESS")
    assert "business need" in fact["statement"]
    assert "§6.2.10" in fact["verification_refs"][0]["locator"]


def test_nist_ot_mfa_is_remote_access_best_practice_not_universal_mandate():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_mfa_remote_access_with_environmental_constraints", "sw09_mfa", "NIST_SP_800_82R3_OT_MFA")
    assert "accepted best practice" in fact["statement"]
    assert "the_claim_does_not_assert_mfa_is_mandatory_for_every_ot_account_or_that_it_substitutes_for_authorization_or_session_controls" in fact["relation"]["conditions"]


def test_nist_ot_ids_ips_monitoring_includes_baselining_tuning_and_failure_mode():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_ids_ips_monitoring_and_sensor_tuning", "sw09_ids_ips_monitoring", "NIST_SP_800_82R3_OT_NETWORK_MONITORING")
    assert "정상 통신 기준선" in fact["statement"]
    assert "the_claim_does_not_assert_ids_or_ips_prevent_all_attacks_or_require_automatic_blocking" in fact["relation"]["conditions"]


def test_nist_ot_vulnerability_scanning_requires_impact_assessment_before_production():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_vulnerability_scanning_with_impact_controls", "sw09_vulnerability_management", "NIST_SP_800_82R3_OT_VULNERABILITY_SCANNING")
    assert "오프라인 사전시험" in fact["statement"]
    assert "the_claim_does_not_assert_every_scan_must_be_active_or_that_discovery_alone_completes_vulnerability_management" in fact["relation"]["conditions"]


def test_nist_ot_detection_process_requires_tested_roles_and_contextual_alert_interpretation():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_detection_process_and_network_baseline", "sw09_detection_triage", "NIST_SP_800_82R3_OT_DETECTION_PROCESS")
    assert "적시에 식별" in fact["statement"]
    assert "the_claim_does_not_assert_a_specific_cross_domain_correlation_set_or_fixed_response_time" in fact["relation"]["conditions"]


def test_nist_ot_containment_is_selected_after_process_and_safety_risk_assessment():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_incident_containment_with_process_risk_assessment", "sw09_containment_eradication", "NIST_SP_800_82R3_OT_INCIDENT_CONTAINMENT")
    assert "공정 성능·안전 영향" in fact["statement"]
    assert "the_claim_does_not_require_blind_disconnect_or_assert_a_universal_containment_action" in fact["relation"]["conditions"]


def test_nist_ot_remote_session_anchor_avoids_unsupported_logging_mandates():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_remote_session_account_and_monitoring_controls", "sw09_secure_remote_session", "NIST_SP_800_82R3_OT_REMOTE_SESSION_CONTROLS")
    assert "기본 자격증명 변경·비활성화" in fact["statement"]
    assert "the_claim_does_not_assert_universal_full_session_recording_concurrent_session_limits_or_inactivity_timeouts" in fact["relation"]["conditions"]


def test_nist_ot_compensating_controls_require_equivalence_risk_and_documentation():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_compensating_controls_risk_documentation", "sw09_legacy_compensating_control", "NIST_SP_800_82R3_OT_COMPENSATING_CONTROLS")
    assert "동등하거나 비교 가능한 보호" in fact["statement"]
    assert "the_claim_does_not_make_segmentation_or_any_single_safeguard_a_universal_replacement" in fact["relation"]["conditions"]


def test_nist_ot_removable_media_anchor_limits_claim_to_policy_and_handling():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_removable_media_policy_handling_and_disposal", "sw09_removable_media", "NIST_SP_800_82R3_OT_MEDIA_PROTECTION")
    assert "비인가 이동식 매체 사용을 허용하지 않으며" in fact["statement"]
    assert "the_claim_does_not_assert_scanning_station_hash_quarantine_or_write_protection_as_universal_requirements_in_this_section" in fact["relation"]["conditions"]


def test_nist_ot_configuration_baseline_requires_predeployment_change_testing():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_baseline_configuration_and_predeployment_change_testing", "sw09_secure_configuration_baseline", "NIST_SP_800_82R3_OT_CONFIGURATION_MANAGEMENT")
    assert "승인된 기준 구성" in fact["statement"]
    assert "the_claim_does_not_assert_a_universal_configuration_schema_or_automatic_drift_detection_requirement" in fact["relation"]["conditions"]


def test_nist_ot_configuration_change_control_aligns_with_organizational_moc():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_configuration_management_aligned_with_moc", "sw09_security_change_control", "NIST_SP_800_82R3_OT_MOC_ALIGNMENT")
    assert "MOC(Management of Change)" in fact["statement"]
    assert "the_claim_does_not_require_specific_security_change_review_fields_or_a_named_sw06_workflow" in fact["relation"]["conditions"]


def test_nist_ot_asset_disposal_protects_critical_data_and_media():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_asset_disposal_and_critical_data_sanitization", "sw09_lifecycle_decommissioning", "NIST_SP_800_82R3_OT_ASSET_DISPOSAL")
    assert "수명 종료 시 자산 폐기 프로그램" in fact["statement"]
    assert "the_claim_does_not_assert_removal_of_every_account_certificate_license_backup_or_supplier_path_as_a_requirement_in_this_source_passage" in fact["relation"]["conditions"]


def test_nist_ot_safety_security_coordination_avoids_universal_airgap_claim():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_safety_system_separation_risk_and_control_impact", "sw09_safety_coordination", "NIST_SP_800_82R3_OT_SAFETY_SYSTEMS")
    assert "독립적으로 구현되기도 하지만" in fact["statement"]
    assert "the_claim_does_not_assert_that_all_safety_systems_must_be_physically_air_gapped_or_that_nist_requires_a_specific_safety_approval_workflow" in fact["relation"]["conditions"]


def test_nist_ot_tabletop_dr_testing_does_not_invent_universal_metrics():
    fact = _assert_nist_ot_access_fact("nist_80082r3_ot_tabletop_dr_recovery_testing_and_lessons", "sw09_exercise_metrics", "NIST_SP_800_82R3_OT_TABLETOP_AND_RESPONSE_IMPROVEMENT")
    assert "tabletop exercise" in fact["statement"]
    assert "the_claim_does_not_define_mttd_or_containment_time_formula_or_universal_required_exercise_metrics" in fact["relation"]["conditions"]


def test_nistir_7966_jump_server_claim_is_ssh_specific_not_universal_ot_design():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row["fact_id"] == "nistir_7966_approved_jump_server_ssh_trust_and_key_lifecycle")
    topic_id = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
    pack_dir = ROOT / "rubrics/topic_packs" / topic_id
    pack = json.loads((pack_dir / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == "sw09_jump_server")
    logic = json.loads((pack_dir / "logic_check.json").read_text())["llm_profile"]
    assert fact["statement"] == anchor["statement"] == anchor["claim"]
    assert anchor["statement"] in logic["truth_schema"]
    assert fact["verification_refs"][0]["authority_id"] == "NISTIR_7966_SSH_JUMP_SERVER"
    assert "claim_is_limited_to_nistir_7966_ssh_access_management_guidance_not_a_universal_ot_architecture_requirement" in fact["relation"]["conditions"]


def test_sw08_congestion_fact_is_verified_with_deadline_scope_preserved():
    registry = load_approved_fact_registry(ROOT)
    fact = next(row for row in registry["facts"] if row.get("legacy_anchor_id") == "sw08_congestion_buffering")
    assert fact["verification_status"] == "verified"
    assert fact["score_effect"] == "none"
    assert fact["verification_refs"][0]["authority_id"] == "IETF_RFC_7567_QUEUE_ARRIVAL_DELAY_BUFFER_SIZE"
    assert "buffer_sizing_absorbs_expected_bursts_but_does_not_by_itself_prove_an_application_deadline" in fact["relation"]["conditions"]
