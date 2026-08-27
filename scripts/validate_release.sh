#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PROMOTE_GENERATED="${PROMOTE_GENERATED:-1}"
RUN_SMOKE_TOPIC_PACKS="${RUN_SMOKE_TOPIC_PACKS:-0}"
RUN_GRADING_REPRODUCIBILITY="${RUN_GRADING_REPRODUCIBILITY:-0}"

TOPIC_IDS=(
  "pid_controller_tuning_sequence_gain_effects"
  "second_order_system_resonance_frequency_response"
)

TRANSIENT_REPORTS=(
  "reports/fact_anchor_quality_audit.csv"
  "reports/fact_anchor_quality_audit.md"
  "reports/model_fact_relationship_audit.csv"
  "reports/model_fact_relationship_audit.md"
  "reports/model_answer_relationship_validation.csv"
  "reports/model_answer_relationship_validation.md"
  "reports/model_answer_relationship_minor_analysis.csv"
  "reports/model_answer_relationship_minor_analysis.md"
  "reports/model_answer_relationship_priority_minors.md"
  "reports/rubric_audit_summary.md"
)

REPORT_SNAPSHOT_DIR="$(
  mktemp -d \
    "${TMPDIR:-/tmp}/prof_eng_answer_validation_reports.XXXXXX"
)"
REPORT_SNAPSHOT_MANIFEST="${REPORT_SNAPSHOT_DIR}/existing.txt"

snapshot_transient_reports() {
  local report
  local snapshot_path

  : > "${REPORT_SNAPSHOT_MANIFEST}"

  for report in "${TRANSIENT_REPORTS[@]}"; do
    if [[ -f "${report}" ]]; then
      snapshot_path="${REPORT_SNAPSHOT_DIR}/files/${report}"
      mkdir -p "$(dirname "${snapshot_path}")"
      cp -p -- "${report}" "${snapshot_path}"
      printf '%s\n' "${report}" >> "${REPORT_SNAPSHOT_MANIFEST}"
    fi
  done
}

restore_transient_reports() {
  local report
  local snapshot_path

  if [[ -z "${REPORT_SNAPSHOT_DIR:-}" ]] ||
     [[ ! -d "${REPORT_SNAPSHOT_DIR}" ]]; then
    return 0
  fi

  for report in "${TRANSIENT_REPORTS[@]}"; do
    rm -f -- "${report}"
  done

  if [[ -f "${REPORT_SNAPSHOT_MANIFEST}" ]]; then
    while IFS= read -r report; do
      [[ -n "${report}" ]] || continue

      snapshot_path="${REPORT_SNAPSHOT_DIR}/files/${report}"
      mkdir -p "$(dirname "${report}")"
      cp -p -- "${snapshot_path}" "${report}"
    done < "${REPORT_SNAPSHOT_MANIFEST}"
  fi

  rm -rf -- "${REPORT_SNAPSHOT_DIR}"
}

snapshot_transient_reports
trap restore_transient_reports EXIT

echo "===== py_compile: core entrypoints ====="
python3 -m py_compile \
  bot.py \
  grade_output_summarizer.py \
  logic_check_evaluator.py \
  grade_score_reconciler.py \
  grading_agents.py \
  originality_grader.py \
  rubric_registry.py \
  rubric_bank_paths.py \
  scripts/rubric_manager.py \
  scripts/validate_topic_pack_release.py \
  scripts/validate_release_test_coverage.py \
  scripts/validate_model_answer_relationships.py \
  scripts/rubric_audit/report_priority_minor_relationships.py \
  scripts/rubric_audit/audit_fact_anchor_quality.py \
  scripts/rubric_audit/build_rubric_work_pack.py \
  scripts/test_restored_rubric_audit_tools.py \
  scripts/test_rubric_content_crud.py \
  scripts/rubric_audit/deep_model_fact_relationship_audit.py \
  scripts/test_model_answer_relationship_validator.py \
  scripts/test_priority_minor_reporter.py \
  scripts/test_deep_model_fact_relationship_auditor.py \
  scripts/test_release_test_coverage_validator.py \
  scripts/smoke_topic_pack.py

echo
echo "===== router / coverage / Hybrid-Multi release regressions ====="
(
  RELEASE_REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
  export PYTHONPATH="${RELEASE_REPO_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
  python3 scripts/test_assisted_routing.py
  python3 scripts/test_assisted_routing_phase10_integration.py
  python3 scripts/test_coverage_feedback_aggregator.py
  python3 scripts/test_coverage_feedback_event.py
  python3 scripts/test_coverage_feedback_exact_fingerprint_contract.py
  python3 scripts/test_coverage_feedback_persistence.py
  python3 scripts/test_coverage_feedback_persistence_diagnostics.py
  python3 scripts/test_coverage_feedback_report.py
  python3 scripts/test_coverage_feedback_retention.py
  python3 scripts/test_hybrid_demand_scope_guard.py
  python3 scripts/test_hybrid_demand_scope_prompt.py
  python3 scripts/test_hybrid_general_demand_text_enrichment.py
  python3 scripts/test_hybrid_general_evidence_consumer.py
  python3 scripts/test_hybrid_general_grading_context.py
  python3 scripts/test_hybrid_general_grading_prompt.py
  python3 scripts/test_hybrid_originality_numeric_scope.py
  python3 scripts/test_multi_topic_demand_scope_prompt.py
  python3 scripts/test_multi_topic_evidence_consumer.py
  python3 scripts/test_multi_topic_grading_context.py
  python3 scripts/test_multi_topic_grading_phase10_integration.py
  python3 scripts/test_multi_topic_question_contract_hash_repair.py
  python3 scripts/test_question_demand_shadow.py
  python3 scripts/test_question_demand_evidence_shadow.py
  python3 scripts/test_question_demand_b_score_connection_v2.py
  python3 scripts/test_semantic_router_default_transport.py
  python3 scripts/test_semantic_router_gemini_transport.py
  python3 scripts/test_semantic_router_general_mode_contract.py
  python3 scripts/test_semantic_router_shadow.py
)
echo "RELEASE_ROUTER_HYBRID_MULTI_COVERAGE_TESTS=PASS"

echo "----- host regression: question-only routing candidates -----"
PYTHONPATH=. python3 -B scripts/test_question_only_routing_candidates.py

echo "===== release test coverage validation ====="
python3 scripts/validate_release_test_coverage.py

echo
echo "===== release-test coverage validator regression ====="
python3 -m unittest scripts.test_release_test_coverage_validator

echo
echo "===== thermocouple source semantic integrity regression ====="
python3 scripts/test_thermocouple_source_semantic_integrity.py

echo
echo "===== formatter regression tests ====="
python3 -m unittest scripts.test_grade_output_formatter

echo
echo "===== logic_check evaluator regression tests ====="
python3 -m unittest scripts.test_logic_check_evaluator

echo
echo "===== model-answer relationship validator regression ====="
python3 -m unittest scripts.test_model_answer_relationship_validator

echo
echo "===== priority-minor reporter regression ====="
python3 -m unittest scripts.test_priority_minor_reporter

echo
echo "===== deep Model Answer ↔ Fact Anchor auditor regression ====="
python3 -m unittest scripts.test_deep_model_fact_relationship_auditor

echo "===== restored rubric audit tools regression ====="
python3 -m unittest scripts.test_restored_rubric_audit_tools

echo
echo "===== rubric content CRUD integration regression ====="
python3 scripts/test_rubric_content_crud.py

echo
echo "===== rubric quality audit ====="
python3 scripts/rubric_audit/run_rubric_audit.py

echo
echo "===== rubric validation: validate-all ====="
python3 scripts/rubric_manager.py validate-all

echo
if [[ "${PROMOTE_GENERATED}" == "1" ]]; then
  echo "===== topic pack release validation: promote generated ====="
  python3 scripts/rubric_manager.py validate-topic-pack-release \
    --promote-generated \
    --skip-smoke
else
  echo "===== topic pack release validation: no promote ====="
  python3 scripts/rubric_manager.py validate-topic-pack-release \
    --skip-smoke
fi

echo
echo "===== optional smoke topic packs ====="
mkdir -p data/sessions

if [[ "${RUN_SMOKE_TOPIC_PACKS}" != "1" ]]; then
  echo "SKIP: smoke-topic-pack is opt-in. Set RUN_SMOKE_TOPIC_PACKS=1 to run it locally."
elif find data/sessions -mindepth 1 -maxdepth 1 -type d | grep -q .; then
  for topic_id in "${TOPIC_IDS[@]}"; do
    echo
    echo "----- smoke-topic-pack: ${topic_id} -----"
    python3 scripts/rubric_manager.py smoke-topic-pack \
      --topic-id "${topic_id}" \
      --require-logic-check
  done
else
  echo "SKIP: smoke-topic-pack requires at least one usable base session under data/sessions."
  echo "      Run smoke locally after creating a grading session, or pass --base-session manually."
fi

echo
echo "===== cleanup transient validation reports ====="
restore_transient_reports
trap - EXIT

echo
echo
echo
echo "===== active JSON parser contract regression ====="
PYTHONPATH=. python3 scripts/test_json_parser_contract.py

echo "===== requirement coverage regression ====="
python3 scripts/test_requirement_coverage.py

echo
echo "===== explicit requirement cap regression ====="
python3 scripts/test_explicit_requirement_cap.py

echo
echo "===== originality and final score metadata regression ====="
python3 -m unittest scripts.test_score_metadata_originality_consistency

echo
echo "===== bot logging regression ====="
python3 scripts/test_bot_logging.py

echo
echo "===== score flow guard regression ====="
python3 scripts/test_score_flow_guards.py

echo "===== ascii-only answer volume regression ====="
python3 scripts/test_ascii_answer_volume.py

echo
echo "===== model answer router regression ====="
python3 scripts/test_model_answer_router.py
echo
echo "===== control valve characteristic topic regression ====="
python3 scripts/test_control_valve_characteristics_topic.py

echo
echo "===== topic importance scope validation regression ====="
python3 scripts/test_topic_importance_scope_validation.py

echo
echo "===== whitespace check ====="
git diff --check

echo
echo "VALIDATION OK"

echo
echo "===== control valve deadband stiction response topic regression ====="
python3 scripts/test_control_valve_deadband_stiction_response_topic.py

echo
echo "===== control valve body and actuator topic regression ====="
python3 scripts/test_control_valve_types_body_actuator_topic.py

echo
echo "===== control valve authority and installed-gain topic regression ====="
python3 scripts/test_control_valve_authority_rangeability_gain_topic.py

echo
echo "===== control valve liquid sizing topic regression ====="
python3 scripts/test_control_valve_sizing_cv_kv_reynolds_topic.py

echo
echo "===== control valve gas sizing and choked flow topic regression ====="
python3 scripts/test_control_valve_gas_sizing_choked_flow_topic.py

echo
echo "===== control valve cavitation flashing and liquid choked flow topic regression ====="
python3 scripts/test_control_valve_cavitation_flashing_choked_flow_topic.py

echo
echo "===== control valve aerodynamic hydrodynamic noise topic regression ====="
python3 scripts/test_control_valve_noise_aerodynamic_hydrodynamic_topic.py

echo
echo "===== control valve balanced and unbalanced trim topic regression ====="
python3 scripts/test_control_valve_balanced_unbalanced_trim_topic.py

echo
echo "===== control valve positioner IP booster accessories topic regression ====="
python3 scripts/test_control_valve_positioner_ip_booster_accessories_topic.py

echo
echo "===== smart positioner diagnostics valve signature predictive maintenance topic regression ====="
python3 scripts/test_control_valve_smart_positioner_diagnostics_topic.py

echo
echo "===== control valve seat leakage shutoff class packing fugitive emissions topic regression ====="
python3 scripts/test_control_valve_seat_leakage_packing_emissions_topic.py

echo
echo "===== control valve severe service high low flow temperature cryogenic particle topic regression ====="
python3 scripts/test_control_valve_severe_service_topic.py

echo
echo "===== final control element SIL SIS ESD valve partial stroke test topic regression ====="
python3 scripts/test_final_control_element_sil_sis_esd_pst_topic.py

echo
echo "===== control valve integrated selection process and lifecycle topic regression ====="
python3 scripts/test_control_valve_selection_process_lifecycle_topic.py

echo
echo "===== control valve maintenance inspection overhaul testing topic regression ====="
python3 -B scripts/test_control_valve_maintenance_inspection_overhaul_testing_topic.py
echo
RELEASE_REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${RELEASE_REPO_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
echo "===== additional release host regression matrix ====="

echo "----- host regression: configuration change release backup rollback migration obsolescence management -----"
python3 -B scripts/test_configuration_change_release_backup_rollback_migration_obsolescence_management.py

echo "----- host regression: control logic sequence interlock permissive trip state transition -----"
python3 -B scripts/test_control_logic_sequence_interlock_permissive_trip_state_transition.py

echo "----- host regression: control software project fat sat commissioning acceptance -----"
python3 -B scripts/test_control_software_project_fat_sat_commissioning_acceptance.py

echo "----- host regression: control valve correctness bridge -----"
python3 -B scripts/test_control_valve_correctness_bridge.py

echo "----- host regression: control valve formula checker -----"
python3 -B scripts/test_control_valve_formula_checker.py

echo "----- host regression: control valve type logic regressions -----"
python3 -B scripts/test_control_valve_type_logic_regressions.py

echo "----- host regression: cross topic calibration corpus -----"
python3 -B scripts/test_cross_topic_calibration_corpus.py

echo "----- host regression: deterministic llm sampling -----"
python3 -B scripts/test_deterministic_llm_sampling.py

echo "----- host regression: expert calibration dataset -----"
python3 -B scripts/test_expert_calibration_dataset.py

echo "----- host regression: export expert calibration record -----"
python3 -B scripts/test_export_expert_calibration_record.py

echo "----- host regression: final verified coverage and session isolation -----"
python3 -B scripts/test_final_verified_coverage_and_session_isolation.py

echo "----- host regression: gemini semantic calibration regressions -----"
python3 -B scripts/test_gemini_semantic_calibration_regressions.py

echo "----- host regression: general evidence contract -----"
python3 -B scripts/test_general_evidence_contract.py

echo "----- host regression: general grading runtime e2e -----"
python3 -B scripts/test_general_grading_runtime_e2e.py

echo "----- host regression: generate expert calibration report -----"
python3 -B scripts/test_generate_expert_calibration_report.py

echo "----- host regression: generic formula integrity -----"
python3 -B scripts/test_generic_formula_integrity.py

echo "----- host regression: historian mes it ot cross lane ownership repair -----"
python3 -B scripts/test_historian_mes_it_ot_cross_lane_ownership_repair.py

echo "----- host regression: historian mes it ot data integration topic -----"
python3 -B scripts/test_historian_mes_it_ot_data_integration_topic.py

echo "----- host regression: hmi scada alarm setpoint soe operator information -----"
python3 -B scripts/test_hmi_scada_alarm_setpoint_soe_operator_information.py

echo "----- host regression: industrial ai ml model lifecycle topic -----"
python3 -B scripts/test_industrial_ai_ml_model_lifecycle_topic.py

echo "----- host regression: industrial network realtime determinism time synchronization fault recovery resilience -----"
python3 -B scripts/test_industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience.py

echo "----- host regression: industrial wired wireless communication fieldbus ethernet interoperability selection -----"
python3 -B scripts/test_industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection.py

echo "----- host regression: instrumentation control software lifecycle v model -----"
python3 -B scripts/test_instrumentation_control_software_lifecycle_v_model.py

echo "----- host regression: layer evidence guard -----"
python3 -B scripts/test_layer_evidence_guard.py

echo "----- host regression: ot cybersecurity defense in depth allowlisting supply chain incident response -----"
python3 -B scripts/test_ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response.py

echo "----- host regression: physical ai cross lane ownership repair -----"
python3 -B scripts/test_physical_ai_cross_lane_ownership_repair.py

echo "----- host regression: physical ai robot sensor fusion safety topic -----"
python3 -B scripts/test_physical_ai_robot_sensor_fusion_safety_topic.py

echo "----- host regression: pid piping instrumentation diagram symbols tags loops control narrative -----"
python3 -B scripts/test_pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative.py

echo "----- host regression: plan a requirement coverage regressions -----"
# Parallel Topic expansion focused regressions (15)
python3 -B scripts/test_instrumentation_power_grounding_shielding_ups_ground_loop_emc_topic.py
python3 -B scripts/test_instrumentation_installation_wiring_impulse_tubing_inspection_codes_topic.py
python3 -B scripts/test_instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification_topic.py
python3 -B scripts/test_control_hardware_lifecycle_panel_architecture_component_selection_production_verification_topic.py
python3 -B scripts/test_electronics_error_noise_drift_tolerance_aging_power_mitigation_topic.py
python3 -B tests/test_hazardous_area_explosion_protection_intrinsic_safety_equipment_selection_topic_pack.py
python3 -B tests/test_instrumentation_system_design_basis_codes_standards_specification_deviation_management_topic_pack.py
python3 -B tests/test_pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error_topic_pack.py
python3 -B tests/test_speed_rotation_measurement_encoder_proximity_tachometer_selection_error_topic_pack.py
python3 -B tests/test_humidity_measurement_capacitive_resistive_dew_point_selection_compensation_topic_pack.py
python3 -B scripts/test_optical_laser_photoelectric_noncontact_measurement_topic.py
python3 -B scripts/test_control_system_operations_maintenance_calibration_inspection_spares_kpi.py
python3 -B scripts/test_instrumentation_project_management_basic_design_cost_schedule_documents_acceptance.py
python3 -B scripts/test_instrumentation_production_management_planning_quality_cost_resources.py
python3 -B scripts/test_industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread.py
# Post-expansion static backlog focused regressions (2)
python3 -B tests/test_hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards_topic_pack.py
python3 -B tests/test_emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits_topic_pack.py

python3 -B scripts/test_plan_a_requirement_coverage_regressions.py

echo "----- host regression: plan b semantic layer ownership regressions -----"
python3 -B scripts/test_plan_b_semantic_layer_ownership_regressions.py

echo "----- host regression: plan c topic aware fact cap regressions -----"
python3 -B scripts/test_plan_c_topic_aware_fact_cap_regressions.py

echo "----- host regression: plc dcs scada remote io architecture redundancy topic -----"
python3 -B scripts/test_plc_dcs_scada_remote_io_architecture_redundancy_topic.py

echo "----- host regression: post release control valve live regressions -----"
python3 -B scripts/test_post_release_control_valve_live_regressions.py

echo "----- host regression: process control loop architecture cascade ratio feedforward override split range -----"
python3 -B scripts/test_process_control_loop_architecture_cascade_ratio_feedforward_override_split_range.py

echo "----- host regression: question contract -----"
python3 -B scripts/test_question_contract.py

echo "----- host regression: question demand contract -----"
python3 -B scripts/test_question_demand_contract.py
python3 -B scripts/test_question_type_de_policy.py

echo "----- host regression: qtype golden complete contract -----"
python3 -B scripts/validate_qtype_golden_set.py --require-complete
python3 -B scripts/test_qtype_golden_contract.py
python3 -B scripts/test_qtype_golden_runner.py
python3 -B scripts/run_qtype_golden_regression.py --require-complete

echo "----- host regression: review expert calibration record -----"
python3 -B scripts/test_review_expert_calibration_record.py

echo "----- host regression: sis sil safety software topic -----"
python3 -B scripts/test_sis_sil_safety_software_topic.py

echo "----- host regression: mcdc vmodel sil overgrading regression -----"
python3 -B scripts/test_mcdc_vmodel_sil_overgrading_regression.py

echo "----- host regression: topic classification policy -----"
python3 -B scripts/test_topic_classification_policy.py

echo "----- host regression: topic pack contract and tool -----"
python3 -B -m unittest \
  scripts.test_topic_pack_contract \
  scripts.test_topic_pack_tool

echo "----- host regression: topic pack validator multischema -----"
python3 -B scripts/test_topic_pack_validator_multischema.py

echo "----- host regression: verdict recommendation consistency -----"
python3 -B scripts/test_verdict_recommendation_consistency.py

echo "----- host regression: verified defect reconciliation -----"
python3 -B scripts/test_verified_defect_reconciliation.py

echo "----- host regression: verified defect single owner guard -----"
python3 -B scripts/test_verified_defect_single_owner_guard.py

# RELEASE_DEDICATED_TEST: scripts/test_grading_reproducibility.py
echo
echo "===== dedicated grading reproducibility P0 gate ====="
if [[ "${RUN_GRADING_REPRODUCIBILITY}" == "1" ]]; then
  (
    repro_dir="$(mktemp -d "${TMPDIR:-/tmp}/prof_eng_answer_repro.XXXXXX")"
    trap 'rm -rf -- "${repro_dir}"' EXIT
    python3 -B scripts/test_grading_reproducibility.py \
      --runs 10 \
      --output-json "${repro_dir}/grading_reproducibility.json" \
      --output-md "${repro_dir}/grading_reproducibility.md"
  )
else
  echo "SKIP: dedicated reproducibility gate is opt-in. Set RUN_GRADING_REPRODUCIBILITY=1 to run exact 10-run P0 validation."
fi
# NATIVE_SEMANTIC_EVIDENCE_SCORING_V1_RELEASE_GUARD
_stage7_repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
grep -Fq 'NATIVE_SEMANTIC_EVIDENCE_SCORING_V1_RUNTIME' \
  "$_stage7_repo_root/grading_agents.py"
grep -Fq 'NATIVE_SEMANTIC_OBSERVABILITY_PROJECTION_V2' \
  "$_stage7_repo_root/grade_output_summarizer.py"
grep -Fq 'QTYPE_PHASE8_CONSTRAINT_ONLY_V1' \
  "$_stage7_repo_root/grading_agents.py"
# STAGE7_PRODUCTION_EVIDENCE_SHAPE_V2_RELEASE_GUARD
_stage7_v2_repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
grep -Fq 'STAGE7_PRODUCTION_EVIDENCE_SHAPE_V2' \
  "$_stage7_v2_repo_root/grading_agents.py"
grep -Fq 'STAGE7_BUILD_PAYLOAD_NATIVE_OBSERVABILITY_V2' \
  "$_stage7_v2_repo_root/grade_output_summarizer.py"
