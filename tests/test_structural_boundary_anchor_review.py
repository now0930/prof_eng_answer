import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_structural_boundaries_are_separately_reviewed_and_target_packs_exist():
    report = json.loads((ROOT / "reports/full_topic_fact_source_audit_20261010.json").read_text())
    totals = report["totals"]
    baseline_reviews = totals["structural_boundary_reviews"]
    additional = json.loads((ROOT / "reports/structural_boundary_anchor_review_20261012.json").read_text())
    additional_reviews = additional["reviews"]
    reviews = baseline_reviews + additional_reviews

    assert totals["anchors"] == 2073
    assert additional["review_status"] == "structural_scope_confirmed_not_technical_fact"
    assert len(additional_reviews) == 47
    assert len(reviews) == 51
    assert len({(row.get("source_topic_id", additional.get("source_topic_id")), row["anchor_id"]) for row in reviews}) == 51
    assert totals["factual_anchor_count"] == 2069  # source-audit snapshot predates 3 reclassifications
    assert totals["structural_boundary_anchor_count"] == 4

    reviewed_ids = set()
    for row in reviews:
        row_source_topic_id = row.get("source_topic_id", additional.get("source_topic_id"))
        row_status = row.get("review_status", additional.get("review_status"))
        assert row_status == "structural_scope_confirmed_not_technical_fact"
        source_path = ROOT / "rubrics/topic_packs" / row_source_topic_id / "fact_anchor.json"
        assert source_path.is_file()
        source_pack = json.loads(source_path.read_text())
        source_anchor_ids = {anchor["anchor_id"] for anchor in source_pack["anchors"]}
        assert row["anchor_id"] in source_anchor_ids
        review_key = (row_source_topic_id, row["anchor_id"])
        assert review_key not in reviewed_ids
        reviewed_ids.add(review_key)

        targets = [
            {"target_topic_id": row["target_topic_id"], "target_anchor_ids": row.get("target_anchor_ids", [])},
            *row.get("additional_targets", []),
        ]
        for target in targets:
            target_path = ROOT / "rubrics/topic_packs" / target["target_topic_id"] / "fact_anchor.json"
            assert target_path.is_file()
            target_pack = json.loads(target_path.read_text())
            assert target_pack["topic_id"] == target["target_topic_id"]
            target_anchor_ids = {anchor["anchor_id"] for anchor in target_pack["anchors"]}
            for target_anchor_id in target.get("target_anchor_ids", []):
                assert target_anchor_id in target_anchor_ids

    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    registered_anchors = {(row["topic_id"], row["legacy_anchor_id"]) for row in registry["facts"] if row.get("legacy_anchor_id")}
    reviewed_anchors = {
        (row.get("source_topic_id", additional.get("source_topic_id")), row["anchor_id"])
        for row in reviews
    }
    assert reviewed_anchors.isdisjoint(registered_anchors)


def test_newly_verified_mixed_handoffs_have_independent_sources_and_no_score_effect():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    facts = {
        (row["topic_id"], row.get("legacy_anchor_id")): row
        for row in registry["facts"]
    }
    expected = {
        (
            "balanced_trim_unbalanced_trim_structure_sealing_applications",
            "dynamic_friction_topic3_handoff",
        ),
        (
            "balanced_trim_unbalanced_trim_structure_sealing_applications",
            "low_noise_trim_topic9_boundary",
        ),
        (
            "control_valve_severe_service_high_low_flow_temperature_cryogenic_particles",
            "hardfacing_coating_ceramic",
        ),
    }
    for key in expected:
        fact = facts[key]
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert fact["verification_refs"]
        pack_path = ROOT / "rubrics/topic_packs" / key[0] / "fact_anchor.json"
        pack = json.loads(pack_path.read_text())
        anchor = next(row for row in pack["anchors"] if row["anchor_id"] == key[1])
        assert fact["statement"] == anchor["statement"]
        if "claim" in anchor:
            assert fact["statement"] == anchor["claim"]


def test_pack_scope_anchor_is_structural_not_a_technical_fact():
    report = json.loads((ROOT / "reports/structural_boundary_anchor_review_20261012.json").read_text())
    scope_reviews = report.get("scope_reviews", [])
    assert len(scope_reviews) == 18
    row = next(item for item in scope_reviews if item["anchor_id"] == "sw02_scope_operational_logic")
    assert row["review_status"] == "structural_scope_confirmed_not_technical_fact"
    source_path = ROOT / "rubrics/topic_packs" / row["source_topic_id"] / "fact_anchor.json"
    source_pack = json.loads(source_path.read_text())
    assert row["anchor_id"] in {anchor["anchor_id"] for anchor in source_pack["anchors"]}
    assert row["target_topic_id"] == row["source_topic_id"]
    assert set(row["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in source_pack["anchors"]}
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    registered = {(fact["topic_id"], fact["legacy_anchor_id"]) for fact in registry["facts"] if fact.get("legacy_anchor_id")}
    assert (row["source_topic_id"], row["anchor_id"]) not in registered

    assert row["anchor_id"] == "sw02_scope_operational_logic"
    assert set(row["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in source_pack["anchors"]}
    assert (row["source_topic_id"], row["anchor_id"]) not in registered
    maintenance_scope = next(item for item in scope_reviews if item["anchor_id"] == "maintenance_scope_boundary")
    maintenance_pack = json.loads((ROOT / "rubrics/topic_packs" / maintenance_scope["source_topic_id"] / "fact_anchor.json").read_text())
    assert set(maintenance_scope["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in maintenance_pack["anchors"]}
    assert (maintenance_scope["source_topic_id"], maintenance_scope["anchor_id"]) not in registered
    selection_scope = next(item for item in scope_reviews if item["anchor_id"] == "selection_process_ownership")
    selection_pack = json.loads((ROOT / "rubrics/topic_packs" / selection_scope["source_topic_id"] / "fact_anchor.json").read_text())
    assert set(selection_scope["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in selection_pack["anchors"]}
    assert (selection_scope["source_topic_id"], selection_scope["anchor_id"]) not in registered
    positioner_scope = next(item for item in scope_reviews if item["anchor_id"] == "smart_positioner_diagnostic_scope")
    positioner_pack = json.loads((ROOT / "rubrics/topic_packs" / positioner_scope["source_topic_id"] / "fact_anchor.json").read_text())
    assert set(positioner_scope["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in positioner_pack["anchors"]}
    assert (positioner_scope["source_topic_id"], positioner_scope["anchor_id"]) not in registered
    final_scope = next(item for item in scope_reviews if item["anchor_id"] == "system_sif_sil_context_boundary")
    final_pack = json.loads((ROOT / "rubrics/topic_packs" / final_scope["source_topic_id"] / "fact_anchor.json").read_text())
    assert set(final_scope["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in final_pack["anchors"]}
    assert (final_scope["source_topic_id"], final_scope["anchor_id"]) not in registered
    project_scope = next(item for item in scope_reviews if item["anchor_id"] == "sw10_scope_project_execution")
    project_pack = json.loads((ROOT / "rubrics/topic_packs" / project_scope["source_topic_id"] / "fact_anchor.json").read_text())
    assert set(project_scope["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in project_pack["anchors"]}
    assert (project_scope["source_topic_id"], project_scope["anchor_id"]) not in registered
    hardware_scopes = {item["anchor_id"] for item in scope_reviews if item["source_topic_id"] == "control_hardware_lifecycle_panel_architecture_component_selection_production_verification"}
    assert hardware_scopes == {"chl_scope_chain", "chl_tolerance_stack_boundary", "chl_grounding_emc_boundary", "chl_field_installation_boundary", "chl_environmental_qualification_boundary", "chl_fat_boundary", "chl_software_lifecycle_boundary"}
    install_scopes = {item["anchor_id"] for item in scope_reviews if item["source_topic_id"] == "instrumentation_installation_wiring_impulse_tubing_inspection_codes"}
    assert install_scopes == {"iiwic_scope_chain", "iiwic_shield_execution_boundary", "iiwic_fat_sat_boundary"}
    sw04_scope = next(item for item in scope_reviews if item["anchor_id"] == "sw04_scope_general_lifecycle")
    sw04_pack = json.loads((ROOT / "rubrics/topic_packs" / sw04_scope["source_topic_id"] / "fact_anchor.json").read_text())
    assert sw04_scope["target_topic_id"] == sw04_scope["source_topic_id"]
    assert set(sw04_scope["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in sw04_pack["anchors"]}
    sw03_scope = next(item for item in scope_reviews if item["anchor_id"] == "sw03_scope_operator_information")
    sw03_pack = json.loads((ROOT / "rubrics/topic_packs" / sw03_scope["source_topic_id"] / "fact_anchor.json").read_text())
    assert sw03_scope["target_topic_id"] == sw03_scope["source_topic_id"]
    assert set(sw03_scope["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in sw03_pack["anchors"]}


def test_positioner_scope_label_does_not_hide_its_technical_claim():
    topic_id = "control_valve_positioner_ip_converter_booster_accessories_calibration"
    anchor_id = "control_valve_positioner_accessory_scope"
    pack = json.loads((ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text())
    anchor = next(item for item in pack["anchors"] if item["anchor_id"] == anchor_id)
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    fact = next(item for item in registry["facts"] if item.get("legacy_anchor_id") == anchor_id)
    assert "Fisher 846" in fact["statement"]
    assert "failure response" in fact["statement"]
    assert fact["verification_status"] == "verified"
    assert len(fact["verification_refs"]) == 3
    assert anchor["accepted_explanations"]


def test_eem_metrology_boundary_remains_unresolved_without_a_concrete_owner():
    report = json.loads((ROOT / "reports/structural_boundary_anchor_review_20261012.json").read_text())
    unresolved = report["unresolved_scope_reviews"]
    assert len(unresolved) == 1
    row = unresolved[0]
    assert row["anchor_id"] == "eem_metrology_boundary"
    source = json.loads((ROOT / "rubrics/topic_packs" / row["source_topic_id"] / "fact_anchor.json").read_text())
    assert row["anchor_id"] in {anchor["anchor_id"] for anchor in source["anchors"]}
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    registered = {(fact["topic_id"], fact.get("legacy_anchor_id")) for fact in registry["facts"] if fact.get("legacy_anchor_id")}
    assert (row["source_topic_id"], row["anchor_id"]) not in registered


def test_mcdc_safety_plc_compound_claim_stays_unresolved_without_full_support():
    report = json.loads((ROOT / "reports/unresolved_technical_anchor_reviews_20261012.json").read_text())
    expected = {
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_hmi_scada_architecture"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_architecture_redundancy_quality"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_high_performance_hmi"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_display_hierarchy"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_color_context_navigation"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_alarm_delay"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_alarm_performance_kpi"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_setpoint_value_classes"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_setpoint_governance"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_alarm_trip_interlock_boundary"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_soe_definition"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_time_sync_resolution"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_historian_vs_soe"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_first_out_relation"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_audit_trail"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_operator_authority"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_human_error_prevention"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_data_quality_display"),
        ("hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management", "sw03_abnormal_situation_management"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_smart_factory_scope"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_layered_architecture_device_edge_platform_cloud"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_ot_control_boundary"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_edge_gateway_functions"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_workload_placement_latency_bandwidth_cost"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_offline_degraded_mode"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_data_contract_timestamp_quality_context"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_asset_namespace_identifier"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_asset_model_version_lifecycle"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_digital_thread_traceability_links"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_digital_twin_handoff"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_api_event_interface_contract"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_edge_device_onboarding_identity"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_device_edge_fleet_management"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_remote_update_rollback"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_observability_logs_metrics_traces"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_security_zero_trust_least_privilege"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_data_privacy_residency_governance"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_scalability_capacity_multi_site"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_availability_resilience_rto_rpo"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_value_use_case_kpi_architecture"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_incremental_brownfield_migration"),
        ("industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread", "iiot_lifecycle_governance_pdca"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "severe_service_combined_risk_definition"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "operating_case_envelope"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "process_fluid_geometry_consequence_chain"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "installed_rangeability_handoff"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "microflow_trim_geometry"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "packing_gasket_seat_coating_temperature"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "thermal_cycling_heat_soak"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "actuator_positioner_heat_isolation"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "icing_condensation_insulation_interface"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "fibrous_sticky_polymerizing_plugging"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "valve_geometry_solids_passage"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "purge_flushing_cleanout"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "orientation_flow_direction_self_cleaning"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "high_viscosity_non_newtonian_sizing"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "multiphase_entrained_gas_uncertainty"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "seat_packing_material_tradeoff"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "actuator_breakaway_thermal_friction_handoff"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "min_normal_max_transient_cases"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "fouling_wear_clearance_trend"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "inspection_monitoring_trim_replacement"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "specification_material_sizing_workflow"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "vendor_qualification_purchaser_acceptance"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "maintainability_spares_turnaround"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "lifecycle_cost_energy_service_life"),
        ("control_valve_severe_service_high_low_flow_temperature_cryogenic_particles", "repair_reverification_worst_case"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_lifecycle_stage_gate"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_scope_boundary_interface"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_design_basis_requirements"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_wbs_responsibility_raci"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_schedule_milestone_dependency_critical_path"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_progress_measurement_forecast"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_cost_estimate_basis_quantity_rate_contingency"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_cost_baseline_commitment_actual_forecast"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_risk_register_mitigation"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_change_control_scope_cost_schedule"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_document_control_revision_transmittal"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_master_deliverable_register"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "instrument_index_master_tag_register"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "instrument_datasheet_process_mechanical_interface"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "instrument_document_set_loop_hookup_cable_jb"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "io_list_software_project_handoff"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "instrument_quantity_mto_boq"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "procurement_requisition_rfq_tbe_po"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "vendor_document_review_integration"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "vendor_inspection_acceptance_handoff"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "construction_installation_readiness"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "construction_qa_qc_itp_hold_witness"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "mechanical_completion_punch_systemization"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "precommissioning_loop_readiness_handoff"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_acceptance_criteria_evidence"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "asbuilt_handover_document_dossier"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "operations_maintenance_handover_boundary"),
        ("instrumentation_project_management_basic_design_cost_schedule_documents_acceptance", "project_closeout_lessons_learned"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_requirements_specification"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_system_architecture"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_software_architecture"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_detailed_design"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_coding_standard"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_configuration_baseline"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_static_analysis"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_dynamic_analysis"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_regression_test"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_simulation"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_hil"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_fault_injection"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_test_specification"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_coverage_exit_criteria"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_defect_management"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_change_impact"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_review_approval"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_test_environment"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_lifecycle_feedback"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "sw04_evidence_and_auditability"),
        ("instrumentation_control_software_lifecycle_v_model_traceability_verification_validation", "vmodel_no_sil_guarantee__mcdc_adjacent_boundary"),
        ("safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis", "mcdc_safety_plc_boundary"),
        ("control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions", "orientation_thermal_cycle_history"),
        ("control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions", "specification_test_lifecycle_workflow"),
        ("control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe", "sw02_scan_edge_memory"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_in_test_monitoring"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_humidity_recovery_check"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_humidity_failure_mechanisms"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_rs485_multidrop"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_modbus_rtu"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_conformance_vs_interoperability"),
        ("industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle", "data_leakage"),
        ("industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle", "ai_ml_dl_hierarchy"),
        ("industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle", "human_review_fallback"),
        ("industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle", "process_optimization_boundary"),
        ("industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle", "decision_cost_and_lead_time"),
        ("industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle", "regression_and_champion_challenger"),
        ("control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe", "sw02_shutdown_classes"),
        ("control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe", "sw02_override"),
        ("control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe", "sw02_watchdog"),
        ("control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe", "sw02_trip_latch_reset"),
        ("control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe", "sw02_abnormal_transition_prevention"),
        ("control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe", "sw02_command_arbitration"),
        ("control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe", "sw02_signal_quality"),
        ("control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe", "sw02_restart_recovery"),
        ("control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe", "sw02_degraded_mode"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_scope_chain"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_operating_mode_worst_case"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_pretest_baseline"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_vibration_functional_monitor"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_post_vibration_inspection"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_combined_environment_interaction"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_failure_evidence_capture"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_failure_root_cause"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_corrective_action_retest"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_traceable_report"),
        ("instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification", "ieeq_change_control_requalification"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_problem_fit_first"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_optimization_candidate"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_estimation_candidate"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_offline_supervisory_boundary"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_latency_determinism"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_plc_dcs_boundary"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_readiness_maturity"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_classical_baseline_benchmark"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_pilot_verification"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_tco_skills_integration"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_security_governance"),
        ("emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits", "etc_emerging_technology_framework"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_communication_requirements"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_selection_multicriteria"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_copper_media"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_fiber_media"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_topology_selection"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_termination_grounding"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_gateway_role"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_protocol_conversion"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_interoperability_levels"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_commissioning_workflow"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_addressing_naming"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_diagnostics_maintenance"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_installed_base_transition"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_lifecycle_compatibility"),
        ("industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection", "sw07_vendor_tool_dependency"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "work_permit_isolation_depressurization"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "as_found_condition_record"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "symptom_failure_mode_triage"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "external_cause_elimination"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "controlled_removal_marking"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "disassembly_sequence_traceability"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "cleaning_contamination_control"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "trim_stem_guide_body_inspection"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "dimensional_acceptance_criteria"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "repair_replace_lapping_decision"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "packing_gasket_seal_restoration"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "reassembly_alignment_torque"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "seat_endpoint_travel_restoration"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "pressure_boundary_test"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "stroke_friction_hysteresis_test"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "fail_action_accessory_function_test"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "root_cause_evidence_handoff"),
        ("control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing", "return_to_service_as_left_record"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "physical_ai_definition"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "sensor_complementarity"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "calibration_coordinate_frame"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "fusion_uncertainty"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "common_cause_and_fault_detection"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "state_estimation"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "slam_relation"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "world_model"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "digital_twin_synchronization"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "robot_planning_hierarchy"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "closed_loop_ai"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "edge_on_device_ai"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "latency_deadline_budget"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "autonomous_manufacturing"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "human_robot_collaboration"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "safety_envelope"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "safe_state_fallback_degraded_mode"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "supervisory_control_human_override"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "functional_safety_separation"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "operational_design_domain_validation"),
        ("physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control", "runtime_monitoring_change_control"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "governing_document_hierarchy"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "process_design_basis_traceability"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "tag_service_boundary"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "stakeholder_requirement_integration"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "requirement_classification_mandatory_preferred"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "operating_case_matrix"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "minimum_normal_maximum_cases"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "startup_shutdown_upset_cleaning_cases"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "pressure_reference_consistency"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "temperature_envelope_and_thermal_transient"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "flow_basis_and_uncertainty"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "fluid_phase_composition_properties"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "solids_fouling_corrosion_contaminant"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "control_objective_and_loop_dynamics"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "rangeability_turndown_travel_distribution"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "shutoff_leakage_fail_action"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "safety_environmental_regulatory_requirements"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "response_time_and_availability_requirement"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "specialist_calculation_handoff"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "liquid_gas_sizing_cross_check"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "authority_installed_characteristic_cross_check"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "cavitation_flashing_noise_velocity_cross_check"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "severe_service_and_material_cross_check"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "final_element_sis_esd_cross_check"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "selection_matrix_tradeoff"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "uncertainty_margin_and_double_margin"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "valve_body_flow_path_selection"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "trim_characteristic_and_flow_direction"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "seat_packing_gasket_emissions"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "actuator_thrust_torque_supply_minimum"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "fail_action_spring_and_stored_energy"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "positioner_solenoid_booster_accessory_package"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "installation_orientation_piping_load_accessibility"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "datasheet_completeness_and_units"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "requisition_scope_and_guarantees"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "vendor_bid_technical_comparison"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "deviation_exception_risk_register"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "vendor_sizing_assumption_validation"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "document_and_configuration_control"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "inspection_test_plan_and_hold_points"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "material_certification_nde_traceability"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "fat_functional_performance_acceptance"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "sat_loop_stroke_response_leakage"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "commissioning_installed_performance_verification"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "as_built_baseline_and_handover"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "reliability_availability_maintainability"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "spare_parts_interchangeability_obsolescence"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "lifecycle_cost_energy_downtime"),
        ("control_valve_selection_process_pressure_temperature_flow_media_lifecycle", "field_feedback_moc_revalidation"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "static_dynamic_signature_boundary"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "device_status_event_configuration_history"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "data_quality_time_sync_units"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "comparable_context_baseline"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "process_force_confounding"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "supply_pressure_regulator_droop"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "ip_zero_span_drift_trend"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "relay_pilot_fill_vent_health"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "pneumatic_air_consumption_leakage"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "feedback_sensor_drift_noise_dropout"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "cycle_count_definition"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "stroke_time_response_trend"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "endpoint_seat_contact_mechanical_stop"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "packing_stem_shaft_resistance_trend"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "trim_balance_seal_friction_handoff"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "percent_change_domain"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "threshold_persistence_deadband"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "multi_evidence_failure_isolation"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "diagnostic_confidence_data_quality"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "false_positive_negative_context"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "detection_confirmation_boundary"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "detect_verify_diagnose_priority_workflow"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "time_condition_predictive_maintenance_compare"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "degradation_trend_lead_time"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "maintenance_priority_consequence"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "hart_fieldbus_asset_integration"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "offline_test_process_risk"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "as_found_as_left_work_order_feedback"),
        ("smart_positioner_diagnostics_valve_signature_predictive_maintenance", "final_closed_loop_diagnostic_verification"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "final_element_subsystem_boundary"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "trip_signal_and_output_chain"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "dangerous_failure_modes"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "actuator_force_margin_handoff"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "fail_action_vs_safe_state"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "failure_rate_partition_dd_du_sd_su"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "final_element_budget_allocation"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "response_time_process_safety_time"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "component_response_time_sum"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "worst_case_trip_time"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "deenergized_energized_test_condition"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "common_cause_beta_factor_context"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "redundancy_independence_boundary"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "partial_stroke_test_risk_controls"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "pst_interval_and_online_demand_exposure"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "valve_signature_pst_handoff"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "proof_test_records_traceability"),
        ("final_control_element_sil_sis_esd_valve_partial_stroke_test", "fmeca_fmeda_vendor_data_assumptions"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_feasibility"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_scope_baseline"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_schedule_dependencies"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_cost_change_control"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_control_philosophy"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_urs"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_frs"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_fds"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_sds"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_document_hierarchy_traceability"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_io_list"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_tag_list"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_alarm_list"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_interlock_list"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_cause_effect"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_logic_diagram"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_test_specification"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_site_integration_test"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_performance_test"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_acceptance"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_punch_list"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_as_built_handover"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_configuration_backup"),
        ("control_software_project_engineering_documents_fat_sat_commissioning_acceptance", "sw10_change_punch_closure"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_architecture_partitioning"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_interface_definition"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_power_budget"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_power_protection"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_component_selection_multicriteria"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_obsolescence_availability"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_thermal_design"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_panel_layout"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_io_selection"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_communication_interface"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_connector_terminal_selection"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_prototype_not_production"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_design_review"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_prototype_design_verification"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_dfm_dfa"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_incoming_material_control"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_work_instruction_process_control"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_production_test_coverage"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_eol_test"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_test_fixture_control"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_nonconformance_rework"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_change_impact"),
        ("control_hardware_lifecycle_panel_architecture_component_selection_production_verification", "chl_release_gate"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_document_hierarchy"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_install_per_approved_drawings"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_accessibility_maintainability"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_environment_installation_protection"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_cable_route_mechanical_protection"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_cable_separation_execution"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_bend_radius_tension"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_gland_entry_integrity"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_terminal_quality"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_wire_identification"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_spare_core_treatment"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_tubing_fittings_integrity"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_root_manifold_drain_vent"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_support_thermal_vibration"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_cleanliness_pressure_boundary"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_installation_inspection_sequence"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_continuity_insulation_boundary"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_punch_classification"),
        ("instrumentation_installation_wiring_impulse_tubing_inspection_codes", "iiwic_asbuilt_final_acceptance"),
    }
    rows = {(row["topic_id"], row["anchor_id"]): row for row in report["reviews"]}
    assert expected <= set(rows)
    assert len(rows) == 491
    for row in rows.values():
        if row["review_status"] == "verified_promoted_to_fact_registry":
            assert row["anchor_id"] == "sw08_congestion_buffering"
            assert row["registry_action"] == "registered_verified_score_neutral"
            continue
        if row["anchor_id"] == "ai_ml_dl_hierarchy":
            assert row["review_status"] == "unresolved_claim_needs_scope_correction"
        elif row["anchor_id"] == "sw02_override":
            assert row["review_status"] == "unresolved_claim_needs_correction"
        elif row["anchor_id"] == "sw02_abnormal_transition_prevention":
            assert row["review_status"] == "unresolved_evidence_insufficient"
        elif row["topic_id"] == "smart_positioner_diagnostics_valve_signature_predictive_maintenance" and row["anchor_id"] == "percent_change_domain":
            assert row["review_status"] == "unresolved_claim_needs_scope_correction"
        elif row["topic_id"] == "smart_positioner_diagnostics_valve_signature_predictive_maintenance" and row["anchor_id"] in {"static_dynamic_signature_boundary", "data_quality_time_sync_units", "relay_pilot_fill_vent_health", "cycle_count_definition", "trim_balance_seal_friction_handoff", "threshold_persistence_deadband", "multi_evidence_failure_isolation", "diagnostic_confidence_data_quality", "detect_verify_diagnose_priority_workflow", "time_condition_predictive_maintenance_compare", "maintenance_priority_consequence", "hart_fieldbus_asset_integration", "offline_test_process_risk", "as_found_as_left_work_order_feedback", "final_closed_loop_diagnostic_verification"}:
            assert row["review_status"] == "unresolved_scope_overgeneralization"
        elif row["topic_id"] == "final_control_element_sil_sis_esd_valve_partial_stroke_test" and row["anchor_id"] in {"final_element_subsystem_boundary", "dangerous_failure_modes", "actuator_force_margin_handoff", "worst_case_trip_time", "deenergized_energized_test_condition", "partial_stroke_test_risk_controls", "valve_signature_pst_handoff", "proof_test_records_traceability"}:
            assert row["review_status"] == "unresolved_scope_overgeneralization"
        elif row["topic_id"] == "control_software_project_engineering_documents_fat_sat_commissioning_acceptance" and row["anchor_id"] in {"sw10_feasibility", "sw10_scope_baseline", "sw10_schedule_dependencies", "sw10_cost_change_control", "sw10_control_philosophy", "sw10_frs", "sw10_fds", "sw10_sds", "sw10_document_hierarchy_traceability", "sw10_io_list", "sw10_tag_list", "sw10_alarm_list", "sw10_interlock_list", "sw10_cause_effect", "sw10_logic_diagram", "sw10_test_specification", "sw10_performance_test", "sw10_acceptance", "sw10_punch_list", "sw10_as_built_handover", "sw10_configuration_backup", "sw10_change_punch_closure"}:
            assert row["review_status"] == "unresolved_scope_overgeneralization"
        elif row["topic_id"] == "control_software_project_engineering_documents_fat_sat_commissioning_acceptance":
            assert row["review_status"] == "unresolved_evidence_insufficient"
        elif row["topic_id"] == "control_hardware_lifecycle_panel_architecture_component_selection_production_verification" and row["anchor_id"] in {"chl_thermal_design", "chl_prototype_not_production"}:
            assert row["review_status"] == "unresolved_evidence_insufficient"
        elif row["topic_id"] == "control_hardware_lifecycle_panel_architecture_component_selection_production_verification":
            assert row["review_status"] == "unresolved_scope_overgeneralization"
        elif row["topic_id"] == "instrumentation_installation_wiring_impulse_tubing_inspection_codes" and row["anchor_id"] in {"iiwic_tubing_fittings_integrity", "iiwic_cleanliness_pressure_boundary", "iiwic_continuity_insulation_boundary"}:
            assert row["review_status"] == "unresolved_evidence_insufficient"
        elif row["topic_id"] == "instrumentation_installation_wiring_impulse_tubing_inspection_codes":
            assert row["review_status"] == "unresolved_scope_overgeneralization"
        elif row["topic_id"] == "final_control_element_sil_sis_esd_valve_partial_stroke_test":
            assert row["review_status"] == "unresolved_evidence_insufficient"
        elif row["anchor_id"] in {"human_review_fallback", "process_optimization_boundary", "regression_and_champion_challenger", "sw02_shutdown_classes", "sw02_watchdog", "sw02_trip_latch_reset", "sw02_command_arbitration", "sw02_signal_quality", "sw02_restart_recovery", "sw02_degraded_mode", "ieeq_scope_chain", "ieeq_operating_mode_worst_case", "ieeq_pretest_baseline", "ieeq_combined_environment_interaction", "ieeq_corrective_action_retest", "ieeq_change_control_requalification", "etc_offline_supervisory_boundary", "etc_plc_dcs_boundary", "etc_security_governance", "etc_emerging_technology_framework", "sw07_communication_requirements", "sw07_topology_selection", "sw07_termination_grounding", "sw07_commissioning_workflow", "sw07_addressing_naming", "sw07_lifecycle_compatibility", "work_permit_isolation_depressurization", "as_found_condition_record", "controlled_removal_marking", "disassembly_sequence_traceability", "cleaning_contamination_control", "trim_stem_guide_body_inspection", "repair_replace_lapping_decision", "packing_gasket_seal_restoration", "reassembly_alignment_torque", "seat_endpoint_travel_restoration", "fail_action_accessory_function_test", "return_to_service_as_left_record", "physical_ai_definition", "sensor_complementarity", "calibration_coordinate_frame", "common_cause_and_fault_detection", "world_model", "digital_twin_synchronization", "robot_planning_hierarchy", "closed_loop_ai", "edge_on_device_ai", "autonomous_manufacturing", "human_robot_collaboration", "safety_envelope", "safe_state_fallback_degraded_mode", "supervisory_control_human_override", "operational_design_domain_validation", "runtime_monitoring_change_control", "governing_document_hierarchy", "process_design_basis_traceability", "stakeholder_requirement_integration", "requirement_classification_mandatory_preferred", "startup_shutdown_upset_cleaning_cases", "temperature_envelope_and_thermal_transient", "solids_fouling_corrosion_contaminant", "shutoff_leakage_fail_action", "safety_environmental_regulatory_requirements", "response_time_and_availability_requirement", "specialist_calculation_handoff", "cavitation_flashing_noise_velocity_cross_check", "severe_service_and_material_cross_check", "final_element_sis_esd_cross_check", "selection_matrix_tradeoff", "valve_body_flow_path_selection", "trim_characteristic_and_flow_direction", "seat_packing_gasket_emissions", "fail_action_spring_and_stored_energy", "positioner_solenoid_booster_accessory_package", "installation_orientation_piping_load_accessibility", "datasheet_completeness_and_units", "requisition_scope_and_guarantees", "vendor_bid_technical_comparison", "deviation_exception_risk_register", "document_and_configuration_control", "inspection_test_plan_and_hold_points", "material_certification_nde_traceability", "fat_functional_performance_acceptance", "sat_loop_stroke_response_leakage", "commissioning_installed_performance_verification", "as_built_baseline_and_handover", "spare_parts_interchangeability_obsolescence", "lifecycle_cost_energy_downtime", "field_feedback_moc_revalidation"}:
            assert row["review_status"] == "unresolved_scope_overgeneralization"
        else:
            assert row["review_status"] == "unresolved_evidence_insufficient"
        assert row["registry_action"] == "not_registered_not_verified"
        assert row["sources_checked"]
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    assert all(not any(fact.get("topic_id") == topic and fact.get("legacy_anchor_id") == anchor for fact in registry["facts"]) for topic, anchor in expected)


def test_hardware_lifecycle_scope_handoffs_are_valid_pack_references():
    report = json.loads((ROOT / "reports/structural_boundary_anchor_review_20261012.json").read_text())
    rows = [row for row in report["scope_reviews"] if row["source_topic_id"] == "control_hardware_lifecycle_panel_architecture_component_selection_production_verification"]
    assert len(rows) == 7
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    registered = {(fact["topic_id"], fact.get("legacy_anchor_id")) for fact in registry["facts"] if fact.get("legacy_anchor_id")}
    for row in rows:
        source = json.loads((ROOT / "rubrics/topic_packs" / row["source_topic_id"] / "fact_anchor.json").read_text())
        assert row["anchor_id"] in {anchor["anchor_id"] for anchor in source["anchors"]}
        assert (row["source_topic_id"], row["anchor_id"]) not in registered
        target = json.loads((ROOT / "rubrics/topic_packs" / row["target_topic_id"] / "fact_anchor.json").read_text())
        assert set(row["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in target["anchors"]}


def test_installation_scope_handoffs_are_valid_pack_references():
    report = json.loads((ROOT / "reports/structural_boundary_anchor_review_20261012.json").read_text())
    rows = [row for row in report["scope_reviews"] if row["source_topic_id"] == "instrumentation_installation_wiring_impulse_tubing_inspection_codes"]
    assert {row["anchor_id"] for row in rows} == {"iiwic_scope_chain", "iiwic_shield_execution_boundary", "iiwic_fat_sat_boundary"}
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    registered = {(fact["topic_id"], fact.get("legacy_anchor_id")) for fact in registry["facts"] if fact.get("legacy_anchor_id")}
    for row in rows:
        source = json.loads((ROOT / "rubrics/topic_packs" / row["source_topic_id"] / "fact_anchor.json").read_text())
        assert row["anchor_id"] in {anchor["anchor_id"] for anchor in source["anchors"]}
        assert (row["source_topic_id"], row["anchor_id"]) not in registered
        target = json.loads((ROOT / "rubrics/topic_packs" / row["target_topic_id"] / "fact_anchor.json").read_text())
        assert set(row["target_anchor_ids"]) <= {anchor["anchor_id"] for anchor in target["anchors"]}


def test_anchor_audit_inventory_partitions_all_2073_without_overlap():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    fact_pairs = {(fact["topic_id"], fact["legacy_anchor_id"]) for fact in registry["facts"] if fact.get("legacy_anchor_id")}
    base = json.loads((ROOT / "reports/full_topic_fact_source_audit_20261010.json").read_text())
    extra = json.loads((ROOT / "reports/structural_boundary_anchor_review_20261012.json").read_text())
    boundaries = {
        (row.get("source_topic_id", extra.get("source_topic_id")), row["anchor_id"])
        for row in base["totals"]["structural_boundary_reviews"] + extra["reviews"]
    }
    scope = {(row["source_topic_id"], row["anchor_id"]) for row in extra["scope_reviews"]}
    unresolved_scope = {(row["source_topic_id"], row["anchor_id"]) for row in extra["unresolved_scope_reviews"]}
    anchors = set()
    for pack_path in (ROOT / "rubrics/topic_packs").glob("*/fact_anchor.json"):
        pack = json.loads(pack_path.read_text())
        anchors.update((pack["topic_id"], anchor["anchor_id"]) for anchor in pack["anchors"])
    unresolved_technical = anchors - fact_pairs - boundaries - scope - unresolved_scope
    detailed_reviews = json.loads((ROOT / "reports/unresolved_technical_anchor_reviews_20261012.json").read_text())
    detailed_unresolved = {(row["topic_id"], row["anchor_id"]) for row in detailed_reviews["reviews"] if row["review_status"].startswith("unresolved_")}
    assert len(anchors) == 2073
    assert len(fact_pairs) == 1513
    assert len(boundaries) == 51
    assert len(scope) == 18
    assert len(unresolved_scope) == 1
    assert len(unresolved_technical) == 490
    assert detailed_unresolved == unresolved_technical
    groups = [fact_pairs, boundaries, scope, unresolved_scope, unresolved_technical]
    assert all(left.isdisjoint(right) for i, left in enumerate(groups) for right in groups[i + 1 :])
