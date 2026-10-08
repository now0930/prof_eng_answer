# Topic Pack Fact Anchor 감사 — 열 번째 200개

- 감사일: 2026-10-08
- 대상: RTD, MC/DC, 표준 2차계/공진, Sight Glass, SIL 목표결정, SIS/SIL 소프트웨어, 스마트 포지셔너 진단, 회전속도 센서, 상태공간 제어
- 판정: 일반 원리·식 확인 149, 적용·제품·표준조건 확인 51, 기술 주장 불일치 3건 정정
- 조건 확인은 오류 유보가 아니라 특정 제품, 프로젝트, 표준 적용범위 또는 현장 승인에 따라 근거를 채워야 한다는 의미다.

## 범위 집계

| Topic ID | 범위 | 개수 | 확인 | 조건 확인 |
|---|---:|---:|---:|---:|
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 9–14 | 6 | 6 | 0 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 1–33 | 33 | 32 | 1 |
| `second_order_lag_response_by_damping_ratio` | 1–8 | 8 | 8 | 0 |
| `second_order_system_resonance_frequency_response` | 1–5 | 5 | 5 | 0 |
| `sight_glass_level_gauge_communicating_vessels_interface` | 1–5 | 5 | 4 | 1 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 1–16 | 16 | 7 | 9 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 1–34 | 34 | 22 | 12 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 1–44 | 44 | 26 | 18 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 1–22 | 22 | 14 | 8 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 1–14 | 14 | 13 | 1 |
| `state_space_controllability_observability_pole_placement` | 1–13 | 13 | 12 | 1 |
| **합계** |  | **200** | **149** | **51** |

## 기술 대조 및 수정

- RTD 4선 Kelvin 측정, 리드선 보상 방식의 trade-off, transmitter 입력 처리, thermowell/stem conduction, 교정 불확도와 fault diagnostics를 확인했다. IEC 60751은 산업용 백금 RTD의 저항-온도 관계 및 성능 요구를 규정한다 ([IEC 60751:2022](https://webstore.iec.ch/en/publication/63753)); 클래스와 허용오차는 적용 specification을 확인해야 한다.
- MC/DC는 각 조건의 독립적인 Boolean Decision 영향 증거다. Statement/Decision/Condition coverage와 구별되고, 100% MC/DC가 요구사항 완전성이나 시스템 SIL 전체 달성을 보장하지 않는다는 경계도 타당하다. 적용대상·기준은 산업별 안전계획을 따르며 NASA 기준 또는 항공 DO-178C를 산업제어 전반에 자동 적용하지 않는다 ([NASA-STD-8739.8B](https://standards.nasa.gov/sites/default/files/standards/NASA/B/NASA-STD-87398RevB.pdf), [FAA AC 20-115D](https://www.faa.gov/airports/resources/advisory_circulars/index.cfm/go/document.information/documentNumber/20-115D), [IEC 61508-3](https://webstore.iec.ch/en/publication/5517)).
- 표준 2차계의 감쇠비 분류, 주파수응답 크기, 공진주파수와 감쇠진동수의 차이를 확인했다. 단위이득 표준모델 및 선형·시간불변 가정 안의 식으로 읽어야 한다.
- Sight Glass의 용기-게이지 정수압 평형 및 상·하부 연결 원리를 확인했다. 게이지 종류별 압력·온도·재질 한계는 개별 설계사양이 필요하다.
- SIL target 결정은 scenario와 tolerable risk 간 비교, RRF=F_residual/F_tolerable, low-demand PFDavg target ≤ F_tolerable/F_residual 관계 및 achieved SIL 검증의 분리를 포함해 확인했다. LOPA credit, conditional modifier, proof-test coverage, mode 구분과 조직 risk criteria는 scenario/표준 가정에 종속된다.
- SIS/SIL에서는 SIL이 개별 SIF에 귀속되고 end-to-end SIF, systematic/random failure 구분, V&V, 독립성, certified product 범위, PFD/PFH mode, 추적성과 변경관리를 확인했다.
- 스마트 포지셔너 진단의 서명/추세 산식은 제공된 조건·정의 범위에서 확인했다. 실제 variable dictionary, baseline 조건, 센서 정확도, 장치 상태코드와 제조사별 signature 해석은 해당 기기의 manual 기준으로 확인해야 한다.
- RPM/count/period 식 및 encoder, proximity, magnetic pickup, tachogenerator의 작동원리를 확인했다. PPR/CPR 정의, edge decoding, 주파수한계, target geometry와 receiver electrical interface는 특정 센서/PLC 모델의 조건이다.
- 상태공간 pole placement, reference prefilter와 integral augmentation의 역할 및 PBH/controllability/observability 조건을 확인했다. (N_r) 식은 본문에 적힌 SISO, D=0, 안정한 (A-BK), 가역 DC gain 가정에 한정한다.

### 확정 수정

SIS/SIL Pack의 마지막 세 Anchor는 accepted explanation이 주장하는 항목과 statement가 서로 달랐다. 특히 단위시험/MISRA Anchor가 무관한 Random Hardware Failure 문장을 주장하고, V-model Anchor에는 근거 없는 bracket 표지가 붙어 있었다. 동일 Pack의 intended scope와 accepted explanation을 따라 핵심 사실은 유지하면서 주장문·claim·description을 일치시켰다.

- `random_hardware_failure__unit_test_not_random_hardware_integrity`: 단위시험과 random hardware failure 무결성 입증의 차이를 명시.
- `random_hardware_failure_unit_test_not_random_hardware_integrity__misra_not_unit_test_tool`: MISRA 코딩규칙/정적분석과 단위시험 도구의 차이를 명시.
- `sis_mcdc_structural_coverage_boundary__vmodel_does_not_guarantee_sil`: V-model이 수명주기 구조이지 SIL 달성 보증이 아니라는 점과 MC/DC 경계를 명시.

이 수정 후 JSON 파싱, Topic Pack quality 및 release 검증이 PASS했다. 87개 Pack/2,068 anchors 전체 생성 pipeline도 PASS했으며, validator가 생성 결과를 원상 복구했다.

## Anchor별 등록부

| Topic ID | 순번 | Anchor ID | 판정 |
|---|---:|---|---|
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 9 | `rtd_four_wire_kelvin_measurement` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 10 | `rtd_wiring_method_selection_tradeoff` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 11 | `rtd_transmitter_connection_signal_conditioning` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 12 | `rtd_installation_thermowell_dynamic_response` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 13 | `rtd_calibration_tolerance_uncertainty` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 14 | `rtd_fault_diagnostics_environment_validation` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 1 | `mcdc_purpose` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 2 | `mcdc_structural_vs_requirements_coverage` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 3 | `mcdc_statement_coverage` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 4 | `mcdc_decision_coverage` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 5 | `mcdc_condition_coverage` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 6 | `mcdc_definition` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 7 | `mcdc_independent_effect_pair` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 8 | `mcdc_unique_cause` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 9 | `mcdc_masking` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 10 | `mcdc_multiple_condition_coverage` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 11 | `mcdc_n_plus_one_limit` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 12 | `mcdc_short_circuit` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 13 | `mcdc_coupled_conditions` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 14 | `mcdc_masked_inactive_condition` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 15 | `mcdc_requirements_based_testing_first` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 16 | `mcdc_coverage_analysis_workflow` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 17 | `mcdc_uncovered_code_disposition` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 18 | `mcdc_dead_code` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 19 | `mcdc_deactivated_code` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 20 | `mcdc_defensive_code` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 21 | `mcdc_source_object_coverage` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 22 | `mcdc_compiler_optimization` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 23 | `mcdc_instrumentation_effect` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 24 | `mcdc_coverage_tool_qualification` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 25 | `mcdc_static_analysis_relation` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 26 | `mcdc_dynamic_analysis_relation` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 27 | `mcdc_control_data_flow_complement` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 28 | `mcdc_target_environment` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 29 | `mcdc_regression_change` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 30 | `mcdc_one_hundred_percent_limit` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 31 | `mcdc_industrial_application_boundary` | 조건 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 32 | `mcdc_safety_plc_boundary` | 확인 |
| `safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis` | 33 | `mcdc_lifecycle_vv_boundary` | 확인 |
| `second_order_lag_response_by_damping_ratio` | 1 | `so2_standard_transfer_function` | 확인 |
| `second_order_lag_response_by_damping_ratio` | 2 | `so2_damping_ratio_definition` | 확인 |
| `second_order_lag_response_by_damping_ratio` | 3 | `so2_pole_response_relationship` | 확인 |
| `second_order_lag_response_by_damping_ratio` | 4 | `so2_underdamped_response` | 확인 |
| `second_order_lag_response_by_damping_ratio` | 5 | `so2_critical_damping_response` | 확인 |
| `second_order_lag_response_by_damping_ratio` | 6 | `so2_overdamped_response` | 확인 |
| `second_order_lag_response_by_damping_ratio` | 7 | `so2_zero_negative_damping` | 확인 |
| `second_order_lag_response_by_damping_ratio` | 8 | `so2_design_tradeoff` | 확인 |
| `second_order_system_resonance_frequency_response` | 1 | `F1` | 확인 |
| `second_order_system_resonance_frequency_response` | 2 | `F2` | 확인 |
| `second_order_system_resonance_frequency_response` | 3 | `F3` | 확인 |
| `second_order_system_resonance_frequency_response` | 4 | `F4` | 확인 |
| `second_order_system_resonance_frequency_response` | 5 | `F5` | 확인 |
| `sight_glass_level_gauge_communicating_vessels_interface` | 1 | `sight_glass_pressure_equilibrium` | 확인 |
| `sight_glass_level_gauge_communicating_vessels_interface` | 2 | `sight_glass_upper_lower_connections` | 확인 |
| `sight_glass_level_gauge_communicating_vessels_interface` | 3 | `sight_glass_interface_connections` | 확인 |
| `sight_glass_level_gauge_communicating_vessels_interface` | 4 | `sight_glass_indication_faults` | 확인 |
| `sight_glass_level_gauge_communicating_vessels_interface` | 5 | `sight_glass_service_limits` | 조건 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 1 | `sis_sif_sil_scope` | 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 2 | `hazard_scenario_boundary` | 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 3 | `tolerable_risk_alarp` | 조건 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 4 | `method_selection` | 조건 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 5 | `initiating_frequency_modifiers` | 조건 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 6 | `existing_ipl_independence` | 조건 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 7 | `residual_frequency_before_sif` | 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 8 | `required_rrf_relation` | 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 9 | `target_pfd_relation` | 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 10 | `sil_band_mapping` | 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 11 | `demand_mode_metric_selection` | 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 12 | `achieved_sil_verification` | 조건 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 13 | `proof_test_pst_role` | 조건 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 14 | `srs_lifecycle_handoff` | 조건 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 15 | `operations_moc_revalidation` | 조건 확인 |
| `sil_target_determination_risk_reduction_and_lifecycle` | 16 | `cyber_ai_safety_boundary` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 1 | `sis_sif_relation` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 2 | `sil_property_of_safety_function` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 3 | `sif_end_to_end_boundary` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 4 | `risk_to_srs_flow` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 5 | `srs_functional_integrity_requirements` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 6 | `application_program_role` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 7 | `software_safety_lifecycle` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 8 | `random_hardware_failure` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 9 | `systematic_failure` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 10 | `systematic_not_simple_rate` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 11 | `verification_definition` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 12 | `validation_definition` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 13 | `functional_test_boundary` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 14 | `proof_test_relation` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 15 | `independence_purpose` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 16 | `separation_shared_resources` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 17 | `common_cause_dependency` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 18 | `diversity_tradeoff` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 19 | `certified_product_scope` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 20 | `safety_manual_constraints` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 21 | `proven_in_use_evidence` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 22 | `tool_qualification_basis` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 23 | `library_validation_control` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 24 | `bidirectional_traceability` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 25 | `modification_revalidation` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 26 | `bypass_override_controls` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 27 | `audit_role` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 28 | `competence_management` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 29 | `pfd_pfh_mode_boundary` | 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 30 | `quantitative_assumptions` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 31 | `sis_mcdc_structural_coverage_boundary` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 32 | `random_hardware_failure__unit_test_not_random_hardware_integrity` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 33 | `random_hardware_failure_unit_test_not_random_hardware_integrity__misra_not_unit_test_tool` | 조건 확인 |
| `sis_sil_safety_software_independence_systematic_failure_verification_validation` | 34 | `sis_mcdc_structural_coverage_boundary__vmodel_does_not_guarantee_sil` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 1 | `smart_positioner_diagnostic_scope` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 2 | `diagnostic_signal_data_chain` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 3 | `online_monitoring_offline_test_boundary` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 4 | `static_dynamic_signature_boundary` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 5 | `device_status_event_configuration_history` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 6 | `data_quality_time_sync_units` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 7 | `vendor_variable_dictionary_verification` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 8 | `as_left_reference_signature` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 9 | `comparable_context_baseline` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 10 | `command_travel_error_signed` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 11 | `full_span_travel_error` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 12 | `up_down_hysteresis_signature` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 13 | `actuator_pressure_open_close_band` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 14 | `pressure_band_friction_proxy` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 15 | `process_force_confounding` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 16 | `supply_pressure_regulator_droop` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 17 | `ip_zero_span_drift_trend` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 18 | `relay_pilot_fill_vent_health` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 19 | `pneumatic_air_consumption_leakage` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 20 | `feedback_sensor_drift_noise_dropout` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 21 | `cycle_count_definition` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 22 | `accumulated_travel_direction_reversal` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 23 | `stroke_time_response_trend` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 24 | `endpoint_seat_contact_mechanical_stop` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 25 | `packing_stem_shaft_resistance_trend` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 26 | `trim_balance_seal_friction_handoff` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 27 | `baseline_residual_context` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 28 | `percent_change_domain` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 29 | `rate_of_change_time_domain` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 30 | `threshold_persistence_deadband` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 31 | `multi_evidence_failure_isolation` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 32 | `diagnostic_confidence_data_quality` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 33 | `false_positive_negative_context` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 34 | `detection_confirmation_boundary` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 35 | `detect_verify_diagnose_priority_workflow` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 36 | `time_condition_predictive_maintenance_compare` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 37 | `degradation_trend_lead_time` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 38 | `maintenance_priority_consequence` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 39 | `hart_fieldbus_asset_integration` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 40 | `offline_test_process_risk` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 41 | `as_found_as_left_work_order_feedback` | 조건 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 42 | `topic1_topic3_topic11_boundary` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 43 | `topic13_topic15_topic16_boundary` | 확인 |
| `smart_positioner_diagnostics_valve_signature_predictive_maintenance` | 44 | `final_closed_loop_diagnostic_verification` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 1 | `speed_angular_frequency_relation` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 2 | `pulse_frequency_speed_equation` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 3 | `counting_window_speed_equation` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 4 | `period_measurement_low_speed` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 5 | `incremental_encoder_principle` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 6 | `quadrature_direction_principle` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 7 | `index_z_channel_role` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 8 | `absolute_encoder_principle` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 9 | `encoder_resolution_ppr_cpr_definition` | 조건 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 10 | `encoder_frequency_limit_selection` | 조건 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 11 | `inductive_proximity_principle` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 12 | `gear_tooth_speed_equation` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 13 | `magnetic_pickup_variable_reluctance` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 14 | `proximity_airgap_target_error` | 조건 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 15 | `tachogenerator_voltage_speed_principle` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 16 | `tachogenerator_direction_loading_error` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 17 | `digital_tachometer_instrument_boundary` | 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 18 | `selection_speed_range_low_high` | 조건 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 19 | `selection_direction_position_resolution` | 조건 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 20 | `mechanical_mounting_coupling_error` | 조건 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 21 | `electrical_interface_noise_error` | 조건 확인 |
| `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` | 22 | `lifecycle_maintainability_selection` | 조건 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 1 | `state_tracking_design_objective` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 2 | `state_tracking_feedback_law_closed_loop` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 3 | `state_tracking_pole_placement_tracking_distinction` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 4 | `state_tracking_prefilter_steady_state_derivation` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 5 | `state_tracking_prefilter_existence_model_dependence` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 6 | `state_tracking_integral_internal_model_principle` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 7 | `state_tracking_augmented_system_formulation` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 8 | `state_tracking_augmented_controllability_stabilizability` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 9 | `state_tracking_prefilter_integral_role_separation` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 10 | `state_tracking_disturbance_reference_performance` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 11 | `state_tracking_observer_separation_principle` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 12 | `state_tracking_saturation_anti_windup` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 13 | `state_tracking_robustness_noise_gain_tradeoff` | 확인 |
| `state_feedback_reference_tracking_prefilter_integral_action` | 14 | `state_tracking_implementation_validation` | 조건 확인 |
| `state_space_controllability_observability_pole_placement` | 1 | `state_space_model_and_dimensions` | 확인 |
| `state_space_controllability_observability_pole_placement` | 2 | `transfer_function_realization_relation` | 확인 |
| `state_space_controllability_observability_pole_placement` | 3 | `eigenvalue_pole_minimal_realization` | 확인 |
| `state_space_controllability_observability_pole_placement` | 4 | `controllability_matrix_rank` | 확인 |
| `state_space_controllability_observability_pole_placement` | 5 | `pbh_controllability_stabilizability` | 확인 |
| `state_space_controllability_observability_pole_placement` | 6 | `observability_matrix_rank` | 확인 |
| `state_space_controllability_observability_pole_placement` | 7 | `pbh_observability_detectability` | 확인 |
| `state_space_controllability_observability_pole_placement` | 8 | `state_feedback_closed_loop` | 확인 |
| `state_space_controllability_observability_pole_placement` | 9 | `pole_placement_conditions` | 확인 |
| `state_space_controllability_observability_pole_placement` | 10 | `ackermann_and_numerical_limits` | 조건 확인 |
| `state_space_controllability_observability_pole_placement` | 11 | `observer_error_dynamics` | 확인 |
| `state_space_controllability_observability_pole_placement` | 12 | `separation_principle_conditions` | 확인 |
| `state_space_controllability_observability_pole_placement` | 13 | `reference_tracking_integral_action` | 확인 |
