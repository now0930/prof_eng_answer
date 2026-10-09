# Topic Pack Fact Anchor 감사 — 일곱 번째 200개

- 감사일: 2026-10-08
- 대상: HIPPS 잔여분, 습도·AI·전송선로, SW lifecycle, 환경/EMC, 계장 설치·접지, 생산관리
- 판정: 일반 원리/정의 확인 137, 적용조건·프로젝트/제품 근거 확인 63, 기술 오류 0, 구조·용어 혼입 2건 최소 수정
- 조건 확인은 오류/승인 대기 의미가 아니라, 제품·설비·프로젝트별 수치와 수행 적합성을 적용 근거로 확정해야 한다는 뜻이다.

## 범위 집계

| Topic ID | 범위 | 개수 | 확인 | 조건 확인 |
|---|---:|---:|---:|---:|
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 10–25 | 16 | 6 | 10 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 1–22 | 22 | 10 | 12 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 1–20 | 20 | 16 | 4 |
| `instrument_signal_transmission_line_reflection_termination` | 1–5 | 5 | 3 | 2 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 1–33 | 33 | 26 | 7 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 1–32 | 32 | 21 | 11 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 1–33 | 33 | 26 | 7 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 1–29 | 29 | 23 | 6 |
| `instrumentation_production_management_planning_quality_cost_resources` | 1–10 | 10 | 6 | 4 |
| **합계** |  | **200** | **137** | **63** |

## 발견 사항 및 최소 수정

1. HAZOP/LOPA의 hazop_lopa_required_rrf statement에 다른 개념의 demand-mode 및 SIL 용어 설명이 뒤에 붙어 claim과 statement가 불일치했다. 부가 문구를 제거하고 기존 claim에 맞췄다. 자세한 원인과 검증은 [여섯 번째 감사 보고서](topic_anchor_fact_review_batch_20261008_200_sixth.md)에 있다.
2. SW lifecycle의 sw04_hil 설명에서 SIL을 Software-in-the-loop 약어로 사용해 Safety Integrity Level 약어와 충돌할 수 있었다. 설명은 유지하고 혼동되는 약어만 풀어 썼다. 해당 Pack release validation PASS, quality errors 0 / warnings 0, generated pipeline PASS.
두 수정 모두 사실의 의미를 임의 변경하지 않고 claim과 약어의 혼입만 정리했다.

## 기술 대조 요약

- HIPPS/SIF 요구, SIL 수명주기, proof-test 및 system boundary는 IEC 61511의 프로세스 산업 적용범위와 대조했다. [IEC 61511-1](https://webstore.iec.ch/en/publication/24241). HIPPS는 과압원 차단, relief는 압력 방출이라는 기능 차이를 확인했으며 실제 법규·Code의 대체 허용 여부는 별도 확인 대상으로 남겼다. [API HIPPS standards listing](https://www.api.org/products-and-services/standards/standards-plan)
- 상대습도, dew/frost point 및 습도센서 원리는 상태량 정의와 측정 원리를 확인했다. 압력 dew point, 온도보상, sensor range와 calibration interval은 제품·압력·측정범위가 필요하다.
- Industrial AI metric/data leakage, transmission line reflection, software V&V 및 환경시험의 기본 원리는 정합성이 있었다. 실제 test profiles, acceptance thresholds, installation/cable separation, grounding/UPS topology 및 production planning 수치는 규격·제품·사업장별 조건을 반영해야 한다.
- 이번 batch의 Anchor IDs와 원본 순번을 등록부에서 대조했다. 별도 플랜트 설계 승인이나 표준 적합성 인증은 수행하지 않았다.

## Anchor별 등록부

| Topic ID | 순번 | Anchor ID | 판정 |
|---|---:|---|---|
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 10 | `hipps_one_out_of_two_final_elements` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 11 | `hipps_one_out_of_two_condition` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 12 | `hipps_architecture_not_universal` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 13 | `hipps_logic_solver_role` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 14 | `hipps_final_element_chain` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 15 | `hipps_fail_safe_energy` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 16 | `hipps_closure_time_and_surge` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 17 | `hipps_tight_shutoff_and_leakage` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 18 | `hipps_pfdavg_allocation` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 19 | `hipps_target_vs_achieved_sil` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 20 | `hipps_independence_from_bpcs` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 21 | `hipps_relief_system_comparison` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 22 | `hipps_relief_replacement_boundary` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 23 | `hipps_coexistence_and_selection` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 24 | `hipps_proof_test_and_bypass` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 25 | `hipps_srs_moc_revalidation` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 1 | `humidity_water_vapor_partial_pressure` | 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 2 | `relative_humidity_definition` | 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 3 | `rh_temperature_dependence` | 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 4 | `absolute_humidity_definition` | 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 5 | `dew_point_definition` | 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 6 | `frost_point_distinction` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 7 | `pressure_dew_point_effect` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 8 | `capacitive_polymer_principle` | 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 9 | `capacitive_sensor_temperature_compensation` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 10 | `capacitive_sensor_hysteresis_drift` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 11 | `resistive_humidity_principle` | 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 12 | `resistive_sensor_ac_measurement` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 13 | `resistive_sensor_limits` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 14 | `chilled_mirror_principle` | 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 15 | `chilled_mirror_maintenance` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 16 | `psychrometric_wet_dry_bulb` | 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 17 | `condensation_sensor_temperature_error` | 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 18 | `high_humidity_warmed_probe` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 19 | `low_humidity_dew_point_selection` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 20 | `selection_environment_process` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 21 | `calibration_traceability_field_check` | 조건 확인 |
| `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` | 22 | `humidity_lifecycle_maintainability_selection` | 조건 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 1 | `ai_ml_dl_hierarchy` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 2 | `supervised_learning` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 3 | `unsupervised_learning` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 4 | `task_type_selection` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 5 | `anomaly_detection_score_threshold` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 6 | `predictive_maintenance_scope` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 7 | `remaining_useful_life_uncertainty` | 조건 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 8 | `process_optimization_boundary` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 9 | `feature_engineering_context` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 10 | `representative_data` | 조건 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 11 | `train_validation_test_separation` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 12 | `chronological_group_split` | 조건 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 13 | `data_leakage` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 14 | `class_imbalance` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 15 | `confusion_matrix` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 16 | `precision_metric` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 17 | `recall_metric` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 18 | `f1_metric` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 19 | `false_alarm_miss_tradeoff` | 확인 |
| `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` | 20 | `decision_cost_and_lead_time` | 조건 확인 |
| `instrument_signal_transmission_line_reflection_termination` | 1 | `transmission_line_applicability` | 확인 |
| `instrument_signal_transmission_line_reflection_termination` | 2 | `reflection_coefficient_relation` | 확인 |
| `instrument_signal_transmission_line_reflection_termination` | 3 | `reflection_waveform_effects` | 확인 |
| `instrument_signal_transmission_line_reflection_termination` | 4 | `termination_and_topology` | 조건 확인 |
| `instrument_signal_transmission_line_reflection_termination` | 5 | `waveform_diagnostic_procedure` | 조건 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 1 | `sw04_scope_general_lifecycle` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 2 | `sw04_sw05_boundary` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 3 | `sw04_sw10_boundary` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 4 | `sw04_v_model_definition` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 5 | `sw04_requirements_specification` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 6 | `sw04_system_architecture` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 7 | `sw04_software_architecture` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 8 | `sw04_detailed_design` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 9 | `sw04_coding_standard` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 10 | `sw04_configuration_baseline` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 11 | `sw04_unit_test` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 12 | `sw04_integration_test` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 13 | `sw04_system_test` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 14 | `sw04_verification_definition` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 15 | `sw04_validation_definition` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 16 | `sw04_verification_validation_relationship` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 17 | `sw04_rtm_bidirectional` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 18 | `sw04_static_analysis` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 19 | `sw04_dynamic_analysis` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 20 | `sw04_regression_test` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 21 | `sw04_simulation` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 22 | `sw04_hil` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 23 | `sw04_fault_injection` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 24 | `sw04_test_specification` | 조건 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 25 | `sw04_coverage_exit_criteria` | 조건 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 26 | `sw04_defect_management` | 조건 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 27 | `sw04_change_impact` | 조건 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 28 | `sw04_review_approval` | 조건 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 29 | `sw04_test_environment` | 조건 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 30 | `sw04_lifecycle_feedback` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 31 | `sw04_evidence_and_auditability` | 조건 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 32 | `sw04_mcdc_detailed_coverage_boundary` | 확인 |
| `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` | 33 | `vmodel_no_sil_guarantee__mcdc_adjacent_boundary` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 1 | `ieeq_scope_chain` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 2 | `ieeq_requirement_traceability` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 3 | `ieeq_emc_emi_distinction` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 4 | `ieeq_emission_immunity_distinction` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 5 | `ieeq_emc_test_categories` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 6 | `ieeq_test_setup_representative` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 7 | `ieeq_operating_mode_worst_case` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 8 | `ieeq_pretest_baseline` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 9 | `ieeq_in_test_monitoring` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 10 | `ieeq_acceptance_criteria_predefined` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 11 | `ieeq_temperature_operating_storage` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 12 | `ieeq_temperature_transition_boundary` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 13 | `ieeq_humidity_failure_mechanisms` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 14 | `ieeq_condensation_condition` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 15 | `ieeq_humidity_recovery_check` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 16 | `ieeq_vibration_sine_random` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 17 | `ieeq_vibration_mounting` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 18 | `ieeq_vibration_functional_monitor` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 19 | `ieeq_post_vibration_inspection` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 20 | `ieeq_combined_environment_interaction` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 21 | `ieeq_measurement_instrument_control` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 22 | `ieeq_uncertainty_margin` | 조건 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 23 | `ieeq_failure_evidence_capture` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 24 | `ieeq_failure_root_cause` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 25 | `ieeq_corrective_action_retest` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 26 | `ieeq_qualification_vs_field_troubleshooting` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 27 | `ieeq_topic2_boundary` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 28 | `ieeq_topic4_boundary` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 29 | `ieeq_topic5_boundary` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 30 | `ieeq_standard_edition_policy` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 31 | `ieeq_traceable_report` | 확인 |
| `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | 32 | `ieeq_change_control_requalification` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 1 | `iiwic_scope_chain` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 2 | `iiwic_document_hierarchy` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 3 | `iiwic_install_per_approved_drawings` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 4 | `iiwic_accessibility_maintainability` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 5 | `iiwic_environment_installation_protection` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 6 | `iiwic_cable_route_mechanical_protection` | 조건 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 7 | `iiwic_cable_separation_execution` | 조건 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 8 | `iiwic_bend_radius_tension` | 조건 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 9 | `iiwic_gland_entry_integrity` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 10 | `iiwic_terminal_quality` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 11 | `iiwic_wire_identification` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 12 | `iiwic_spare_core_treatment` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 13 | `iiwic_shield_execution_boundary` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 14 | `iiwic_intrinsic_safety_segregation_execution` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 15 | `iiwic_impulse_line_general` | 조건 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 16 | `iiwic_impulse_slope_service_specific` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 17 | `iiwic_liquid_service_principle` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 18 | `iiwic_gas_service_principle` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 19 | `iiwic_steam_service_principle` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 20 | `iiwic_dp_pair_symmetry` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 21 | `iiwic_tubing_fittings_integrity` | 조건 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 22 | `iiwic_root_manifold_drain_vent` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 23 | `iiwic_support_thermal_vibration` | 조건 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 24 | `iiwic_cleanliness_pressure_boundary` | 조건 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 25 | `iiwic_installation_inspection_sequence` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 26 | `iiwic_continuity_insulation_boundary` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 27 | `iiwic_punch_classification` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 28 | `iiwic_fat_sat_boundary` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 29 | `iiwic_design_basis_boundary` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 30 | `iiwic_pid_document_boundary` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 31 | `iiwic_hazardous_area_boundary` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 32 | `iiwic_topic1_boundary` | 확인 |
| `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | 33 | `iiwic_asbuilt_final_acceptance` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 1 | `ipgse_scope_chain` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 2 | `ipgse_pe_signal_reference_boundary` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 3 | `ipgse_bonding_impedance_frequency` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 4 | `ipgse_single_multi_point_conditional` | 조건 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 5 | `ipgse_ground_loop_mechanism` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 6 | `ipgse_ground_loop_safe_mitigation` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 7 | `ipgse_common_differential_mode` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 8 | `ipgse_shield_not_pe` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 9 | `ipgse_shield_termination_frequency` | 조건 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 10 | `ipgse_cable_separation_coupling` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 11 | `ipgse_emi_coupling_paths` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 12 | `ipgse_source_path_victim_mitigation` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 13 | `ipgse_filter_entry_bonding` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 14 | `ipgse_spd_coordination` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 15 | `ipgse_power_quality_scope` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 16 | `ipgse_dc_supply_distribution` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 17 | `ipgse_redundant_supply_boundary` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 18 | `ipgse_ups_function_boundary` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 19 | `ipgse_ups_sizing_factors` | 조건 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 20 | `ipgse_ups_bypass_grounding` | 조건 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 21 | `ipgse_symptom_frequency_correlation` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 22 | `ipgse_measurement_reference_safety` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 23 | `ipgse_diagnostic_workflow` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 24 | `ipgse_evidence_before_rewire` | 조건 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 25 | `ipgse_topic2_boundary` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 26 | `ipgse_topic3_boundary` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 27 | `ipgse_topic4_boundary` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 28 | `ipgse_topic5_boundary` | 확인 |
| `instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 29 | `ipgse_final_verification` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 1 | `production_management_objective_scope` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 2 | `production_demand_order_plan_translation` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 3 | `production_horizon_master_detailed_schedule` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 4 | `production_takt_cycle_time_boundary` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 5 | `production_capacity_available_time_rate` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 6 | `production_bottleneck_throughput_constraint` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 7 | `production_line_balancing_workload` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 8 | `production_finite_capacity_schedule_dispatch` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 9 | `production_changeover_sequence_batch_tradeoff` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 10 | `production_wip_flow_lead_time` | 확인 |
