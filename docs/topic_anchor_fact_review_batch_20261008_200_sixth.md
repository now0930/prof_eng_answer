# Topic Pack Fact Anchor 감사 — 여섯 번째 200개

- 감사일: 2026-10-08
- 대상: 양자컴퓨팅 산업 적용 잔여분, feedback/fiber, SIS final element, 기능안전 모델, GWR·방폭·위험환경, HAZOP/LOPA, HIPPS
- 판정: 일반 원리/정의 확인 84, 적용조건·표준·설비 자료 확인 116, 명백한 내용/구조 오류 1건 수정
- “조건 확인”은 오류/사용자 승인 대기 표시가 아니라, 수치·요구 성능·적용성을 해당 시스템/표준/설비 자료와 대조해야 한다는 뜻이다.

## 범위 집계

| Topic ID | 범위 | 개수 | 확인 | 조건 확인 |
|---|---:|---:|---:|---:|
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 9–27 | 19 | 5 | 14 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 1–11 | 11 | 7 | 4 |
| `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics` | 1–6 | 6 | 5 | 1 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 1–48 | 48 | 14 | 34 |
| `float_level_measurement_buoyancy_guidance_tape_errors` | 1–5 | 5 | 4 | 1 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 1–26 | 26 | 9 | 17 |
| `guided_wave_radar_level_measurement_tdr_interface_application` | 1–4 | 4 | 2 | 2 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 1–22 | 22 | 8 | 14 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 1–26 | 26 | 10 | 16 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 1–24 | 24 | 15 | 9 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 1–9 | 9 | 5 | 4 |
| **합계** |  | **200** | **84** | **116** |

## 확정 오류 및 수정

HAZOP/LOPA Pack의 hazop_lopa_required_rrf Anchor에서 claim은 RRF 정의였지만 statement 뒤에 PFDavg/PFH demand-mode 설명과 SIL 명칭 설명이 덧붙어 claim·statement가 불일치했다. 해당 부가 문장은 Anchor 내용 범위를 벗어나므로 제거하고 statement를 기존 claim과 일치시켰다. RRF 수식상의 의미는 유지했다. 한 항목만 수정했다: [fact_anchor.json](/home/now0930/codex/pro_engineer/prof_eng_answer_work/rubrics/topic_packs/hazop_lopa_ipl_risk_reduction_sil_target_allocation/fact_anchor.json).

검증: JSON 파싱 및 claim/statement 정합성 PASS, 해당 Pack release validation PASS, 품질 errors 0 / warnings 0, generated pipeline PASS. Validator가 임시 generated 결과를 복원했다.

## 기술 대조 요약

- 기능안전 수명주기, SIS/SIF 경계, PFDavg/PFH 모드 구분, 진단/Proof Test coverage, 전체 SIF 기여는 IEC 61511의 프로세스 산업 적용 범위와 대조했다. 제품 인증 하나만으로 전체 SIF 달성을 보증하지 않는 점도 구분했다. [IEC 61511-1](https://webstore.iec.ch/en/publication/24241)
- LOPA/HAZOP 논리는 scenario 경계, initiating event/conditional modifier, IPL 독립성 및 중복 credit, residual risk, target SIL과 achieved SIL 차이를 확인했다. RRF 정의와 저수요 target PFDavg 관계는 역방향으로 기재되지 않았다. 구체 수용기준과 값은 사업장 위험기준 및 표준 판본에 종속된다.
- Zone/EPL, Ex d/e/i/p/m/t, 본질안전 entity compatibility는 기기 인증과 system-level loop assessment를 구분했다. 인증서의 특수조건과 실제 설치조건은 함께 확인한다.
- HIPPS는 과압 원인을 차단하는 SIF로서 relief 장치의 방출 기능과 구별했다. 허용 architecture, 시험요건, relief 설계 대체 여부를 보편 규칙으로 단정하지 않았다. [API Standards Plan—HIPPS](https://www.api.org/products-and-services/standards/standards-plan), [API pressure-relief overview](https://www.api.org/products-and-services/training/calendar/equity-technical-institute-thepressure-relieving-systems)
- 양자컴퓨팅 Anchor는 하이브리드 적용, 문제별 baseline 비교, 측정/샘플링 및 noise 한계를 반영했다. 양자 우위를 보편적으로 보장하는 문장은 확인되지 않았다. [NIST Quantum Computing Explained](https://www.nist.gov/quantum-information-science/quantum-computing-explained)
- 광섬유 dispersion, insertion loss/OTDR 역할과 feedback S/T 전달함수·최종값 정리는 각 개념의 정의와 명시된 가정으로 확인했다.
- 개별 플랜트 설계승인이나 현행 규격 적합성 판정은 본 감사 범위가 아니다. 설치, 매체, 모델·인증 조건이 필요한 항목은 조건 확인으로 표시했다.

## 검토 메모

- claim에 반하는 명백한 기술 사실 오류는 발견하지 못했다. 다만 위의 Anchor 문장 혼입 1건은 claim을 바꾸지 않고 정리했다.
- 조건 확인은 작업 중단이나 승인 요청이 아니라, 적용 플랜트의 SRS, 위험기준, 인증서, 도면, 제조사 매뉴얼과 표준 판본이 있어야 적용성을 확정할 수 있다는 뜻이다.

## Anchor별 등록부

| Topic ID | 순번 | Anchor ID | 판정 |
|---|---:|---|---|
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 9 | `etc_hybrid_quantum_classical` | 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 10 | `etc_problem_fit_first` | 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 11 | `etc_optimization_candidate` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 12 | `etc_estimation_candidate` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 13 | `etc_offline_supervisory_boundary` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 14 | `etc_data_encoding_bottleneck` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 15 | `etc_output_sampling_bottleneck` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 16 | `etc_noise_decoherence` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 17 | `etc_error_mitigation_correction_boundary` | 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 18 | `etc_scale_quality_tradeoff` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 19 | `etc_latency_determinism` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 20 | `etc_plc_dcs_boundary` | 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 21 | `etc_quantum_sensing_boundary` | 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 22 | `etc_readiness_maturity` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 23 | `etc_classical_baseline_benchmark` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 24 | `etc_pilot_verification` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 25 | `etc_tco_skills_integration` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 26 | `etc_security_governance` | 조건 확인 |
| `emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits` | 27 | `etc_emerging_technology_framework` | 조건 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 1 | `feedback_negative_loop_structure` | 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 2 | `feedback_closed_loop_transfer` | 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 3 | `feedback_sensitivity_functions` | 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 4 | `feedback_parameter_sensitivity` | 조건 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 5 | `feedback_disturbance_noise_paths` | 조건 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 6 | `feedback_steady_state_error_final_value` | 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 7 | `feedback_system_type_error_constants` | 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 8 | `feedback_type_error_relationship` | 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 9 | `feedback_integral_action_tradeoff` | 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 10 | `feedback_stability_bandwidth_tradeoff` | 조건 확인 |
| `feedback_system_closed_loop_sensitivity_steady_state_error` | 11 | `feedback_field_design_validation` | 조건 확인 |
| `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics` | 1 | `fiber_total_internal_reflection` | 확인 |
| `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics` | 2 | `fiber_mode_dispersion_relation` | 확인 |
| `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics` | 3 | `single_mode_residual_dispersion` | 확인 |
| `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics` | 4 | `insertion_loss_test_role` | 확인 |
| `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics` | 5 | `otdr_distance_and_event_role` | 확인 |
| `fiber_optic_link_modes_dispersion_loss_otdr_diagnostics` | 6 | `otdr_limit_and_acceptance` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 1 | `final_element_role_in_sif` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 2 | `system_sif_sil_context_boundary` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 3 | `safe_state_process_hazard_basis` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 4 | `deenergize_to_trip_energy_philosophy` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 5 | `final_element_subsystem_boundary` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 6 | `valve_actuator_solenoid_architecture` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 7 | `utility_supply_and_shared_dependencies` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 8 | `trip_signal_and_output_chain` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 9 | `dangerous_failure_modes` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 10 | `safe_failure_and_spurious_trip` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 11 | `hidden_stuck_failure` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 12 | `seat_leakage_as_safety_requirement` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 13 | `actuator_force_margin_handoff` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 14 | `fail_action_vs_safe_state` | 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 15 | `failure_rate_partition_dd_du_sd_su` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 16 | `low_demand_pfdavg_contribution` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 17 | `high_continuous_demand_pfh_contribution` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 18 | `series_subsystem_pfd` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 19 | `final_element_budget_allocation` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 20 | `diagnostic_coverage_definition` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 21 | `proof_test_coverage_definition` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 22 | `pst_coverage_definition` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 23 | `pst_detectable_failure_set` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 24 | `pst_not_full_proof_test` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 25 | `full_stroke_proof_test_scope` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 26 | `test_interval_and_repair_time` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 27 | `imperfect_test_residual_risk` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 28 | `proof_test_procedure_repeatability` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 29 | `response_time_process_safety_time` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 30 | `component_response_time_sum` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 31 | `worst_case_trip_time` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 32 | `deenergized_energized_test_condition` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 33 | `bypass_override_inhibit_controls` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 34 | `impairment_alarm_and_permit` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 35 | `restoration_independent_verification` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 36 | `common_cause_beta_factor_context` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 37 | `redundancy_independence_boundary` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 38 | `shared_air_power_environment` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 39 | `partial_stroke_test_risk_controls` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 40 | `pst_interval_and_online_demand_exposure` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 41 | `diagnostic_credit_validation` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 42 | `valve_signature_pst_handoff` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 43 | `proof_test_records_traceability` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 44 | `fmeca_fmeda_vendor_data_assumptions` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 45 | `systematic_capability_software_procedure` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 46 | `maintenance_moc_spares` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 47 | `acceptance_criteria_and_srs_traceability` | 조건 확인 |
| `final_control_element_sil_sis_esd_valve_partial_stroke_test` | 48 | `lifecycle_closed_loop_reverification` | 조건 확인 |
| `float_level_measurement_buoyancy_guidance_tape_errors` | 1 | `float_buoyancy_position` | 확인 |
| `float_level_measurement_buoyancy_guidance_tape_errors` | 2 | `float_density_immersion` | 확인 |
| `float_level_measurement_buoyancy_guidance_tape_errors` | 3 | `float_guidance_turbulence` | 확인 |
| `float_level_measurement_buoyancy_guidance_tape_errors` | 4 | `float_tape_motion_transfer` | 확인 |
| `float_level_measurement_buoyancy_guidance_tape_errors` | 5 | `float_method_boundary` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 1 | `fsrm_rbd_success_path` | 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 2 | `fsrm_rbd_series_parallel` | 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 3 | `fsrm_fta_top_event` | 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 4 | `fsrm_minimal_cut_set` | 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 5 | `fsrm_markov_state_transition` | 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 6 | `fsrm_markov_complexity` | 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 7 | `fsrm_model_purpose_boundary` | 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 8 | `fsrm_low_demand_pfdavg` | 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 9 | `fsrm_high_continuous_demand_pfh` | 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 10 | `fsrm_demand_mode_metric_selection` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 11 | `fsrm_one_oo_one_low_demand_approximation` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 12 | `fsrm_approximation_conditions` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 13 | `fsrm_rrf_relationship` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 14 | `fsrm_voting_tradeoff` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 15 | `fsrm_hft_not_sil_guarantee` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 16 | `fsrm_ccf_redundancy_impact` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 17 | `fsrm_beta_factor` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 18 | `fsrm_ccf_reduction_measures` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 19 | `fsrm_diagnostic_vs_proof_coverage` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 20 | `fsrm_proof_test_purpose` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 21 | `fsrm_proof_test_interval_exposure` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 22 | `fsrm_partial_test_boundary` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 23 | `fsrm_complete_sif_boundary` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 24 | `fsrm_component_certificate_limit` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 25 | `fsrm_hardware_systematic_boundary` | 조건 확인 |
| `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` | 26 | `fsrm_model_assumption_documentation` | 조건 확인 |
| `guided_wave_radar_level_measurement_tdr_interface_application` | 1 | `gwr_tdr_probe_guided_reflection` | 확인 |
| `guided_wave_radar_level_measurement_tdr_interface_application` | 2 | `gwr_surface_interface_permittivity_path` | 확인 |
| `guided_wave_radar_level_measurement_tdr_interface_application` | 3 | `gwr_probe_return_path_quasi_tem_boundary` | 조건 확인 |
| `guided_wave_radar_level_measurement_tdr_interface_application` | 4 | `gwr_process_probe_application_limits` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 1 | `hazardous_area_classification_release_likelihood` | 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 2 | `gas_zone_0_1_2_meaning` | 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 3 | `dust_zone_20_21_22_meaning` | 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 4 | `zone_epl_mapping` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 5 | `ex_marking_selection_chain` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 6 | `gas_dust_group_compatibility` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 7 | `temperature_class_surface_temperature` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 8 | `protection_method_risk_matching` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 9 | `flameproof_ex_d_principle` | 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 10 | `increased_safety_ex_e_principle` | 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 11 | `intrinsic_safety_ex_i_principle` | 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 12 | `pressurization_ex_p_principle` | 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 13 | `encapsulation_and_dust_enclosure_principle` | 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 14 | `intrinsic_safety_levels_ia_ib_ic` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 15 | `is_system_components` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 16 | `entity_voltage_current_power_compatibility` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 17 | `entity_capacitance_inductance_cable` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 18 | `zener_barrier_galvanic_isolator_selection` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 19 | `is_wiring_segregation_identification` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 20 | `certificate_special_conditions_control_drawing` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 21 | `ex_environmental_suitability_independent_check` | 조건 확인 |
| `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` | 22 | `inspection_maintenance_documentation` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 1 | `hec_hazardous_environment_scope` | 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 2 | `hec_hazard_scenario_chain` | 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 3 | `hec_required_safe_state_context` | 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 4 | `hec_fail_safe_not_universal_deenergize` | 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 5 | `hec_loss_of_power_strategy` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 6 | `hec_residual_stored_energy` | 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 7 | `hec_loss_of_communication_strategy` | 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 8 | `hec_local_autonomous_protection` | 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 9 | `hec_sensor_selection_diagnostics` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 10 | `hec_redundancy_common_cause` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 11 | `hec_final_element_safe_action` | 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 12 | `hec_permissive_interlock_trip_roles` | 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 13 | `hec_bypass_override_management` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 14 | `hec_rail_hazard_context` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 15 | `hec_rail_uncertain_authority_response` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 16 | `hec_power_generation_hazard_context` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 17 | `hec_power_shutdown_auxiliaries` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 18 | `hec_building_hazard_context` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 19 | `hec_building_fire_smoke_scenario` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 20 | `hec_environmental_application_controls` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 21 | `hec_alarm_operator_action_boundary` | 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 22 | `hec_verification_loss_scenarios` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 23 | `hec_maintenance_proof_moc` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 24 | `hec_legacy_retrofit_risk_priority` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 25 | `hec_requirement_traceability` | 조건 확인 |
| `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards` | 26 | `hec_ownership_boundary` | 조건 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 1 | `hazop_lopa_hazop_role` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 2 | `hazop_lopa_lopa_scenario_boundary` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 3 | `hazop_lopa_consequence_without_credited_protection` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 4 | `hazop_lopa_initiating_event_frequency` | 조건 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 5 | `hazop_lopa_enabling_and_conditional_modifiers` | 조건 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 6 | `hazop_lopa_lopa_frequency_equation` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 7 | `hazop_lopa_tolerable_event_frequency` | 조건 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 8 | `hazop_lopa_ipl_definition` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 9 | `hazop_lopa_ipl_independence` | 조건 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 10 | `hazop_lopa_ipl_specificity` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 11 | `hazop_lopa_ipl_dependability_auditability` | 조건 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 12 | `hazop_lopa_no_double_counting` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 13 | `hazop_lopa_common_cause_dependency` | 조건 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 14 | `hazop_lopa_bpcs_ipl_credit` | 조건 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 15 | `hazop_lopa_alarm_operator_ipl` | 조건 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 16 | `hazop_lopa_proposed_safeguard_not_creditable` | 조건 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 17 | `hazop_lopa_residual_frequency_after_existing_ipls` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 18 | `hazop_lopa_required_rrf` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 19 | `hazop_lopa_pfdavg_rrf_relation` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 20 | `hazop_lopa_sil_band_mapping` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 21 | `hazop_lopa_target_vs_achieved_sil` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 22 | `hazop_lopa_sif_allocation_boundary` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 23 | `hazop_lopa_srs_handoff` | 확인 |
| `hazop_lopa_ipl_risk_reduction_sil_target_allocation` | 24 | `hazop_lopa_scenario_aggregation_moc` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 1 | `hipps_definition` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 2 | `hipps_not_relief_device` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 3 | `hipps_application_boundary` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 4 | `hipps_sif_end_to_end_boundary` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 5 | `hipps_trip_setpoint_margin` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 6 | `hipps_process_safety_time` | 조건 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 7 | `hipps_two_out_of_three_sensing` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 8 | `hipps_two_out_of_three_limits` | 확인 |
| `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture` | 9 | `hipps_degraded_voting_mode` | 조건 확인 |
