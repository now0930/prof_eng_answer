# Topic Pack Fact Anchor 감사 — 여덟 번째 200개

- 감사일: 2026-10-08
- 대상: 생산/프로젝트/설계기준, Lead-Lag·LQR·Nyquist, LVDT/RVDT, 광학 측정, OT 보안
- 판정: 기본 원리/정의 확인 168, 설비·표준·성능/운영조건 확인 32, 확정 오류 0, 원문 수정 0
- 조건 확인은 사실 오류를 뜻하지 않는다. 실제 규격·측정범위·기기 모델·사업장 risk decision을 적용 근거와 함께 결정할 항목이다.

## 범위 집계

| Topic ID | 범위 | 개수 | 확인 | 조건 확인 |
|---|---:|---:|---:|---:|
| `instrumentation_production_management_planning_quality_cost_resources` | 11–28 | 18 | 9 | 9 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 1–28 | 28 | 25 | 3 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 1–22 | 22 | 19 | 3 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 1–14 | 14 | 12 | 2 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 1–14 | 14 | 11 | 3 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 1–22 | 22 | 18 | 4 |
| `nyquist_stability_criterion_gain_phase_margin` | 1–14 | 14 | 13 | 1 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 1–27 | 27 | 22 | 5 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 1–40 | 40 | 38 | 2 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 1–1 | 1 | 1 | 0 |
| **합계** |  | **200** | **168** | **32** |

## 기술 대조 요약

- 생산계획/원가/OEE 계열은 KPI의 공정경계와 분모 정의가 필요하다는 점을 반영했다. OEE의 A×P×Q 형태만으로 납기·원가·안전 전부를 대표한다고 보지 않았다.
- 프로젝트와 Design Basis에서는 규격판/관할/계약의 적용성 및 deviation 승인 절차가 중요하며, “최신판이 언제나 자동 우선”이라고 일반화하지 않았다.
- Lead/Lag와 LQR 수식은 전달함수 극점·영점의 배치, 연속/이산 Riccati의 구분, stabilizing solution·stabilizability/detectability 조건, 비용 가중치가 hard input constraints를 보장하지 않는 점을 대조했다.
- Nyquist 표준음의 피드백 임계점은 −1이며, 개루프 RHP 극점 P와 폐루프 RHP 극점 Z를 함께 고려한다. 원문은 clockwise-positive N을 정의하고 N=Z−P로 일관되게 썼다. 허수축 극점 contour indentation과 복수 crossover 경고도 포함한다.
- LVDT 차동출력은 두 2차 전압의 차이며 이상 null에서 각 2차 전압이 0이라고 하지 않는다. 출력 진폭과 위상 방향, 센서 원시 AC null residual과 복조 후 DC offset을 구분했다.
- Optical ToF d=cΔt/2는 co-located reflective direct ToF의 왕복거리 조건, iToF는 위상 래핑, optical triangulation은 보정 기하에 한정해 서술했다. 수광 intensity만으로 거리 절대값을 추정한다는 오류는 없다.
- OT cybersecurity는 availability·safety·integrity를 IT 기밀성보다 무시하지 않는 OT context로 다루며, zones/conduits, risk assessment, lifecycle 및 system-owner/shared-responsibility 관점과 일치한다. [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final), [ISA/IEC 62443 series](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards). NIST는 Rev. 4 initial public draft 상태를 안내하므로, 이 감사는 Rev. 3 final과 공개된 62443 범위에 기댔고 특정 최신 강제요건을 단정하지 않았다.
- 이 등록부의 200개 source ID 및 순번은 원본과 대조했다. 이 보고서는 특정 공장 설계승인 또는 현장 보안 적합성 인증이 아니다.

## 오류 및 보류

- 확정된 기술 오류는 이번 대상에서 발견되지 않아 Pack 내용 수정은 없다.
- OT 보안 정책의 구체 통제, MTTD/MTTC 기준점과 SLA, 프로젝트 원가/OEE 정의, 계기 calibration/acceptance, 표준판 적용은 owner·관할·시스템별 근거가 있어야 한다. 이들은 조건 확인으로 기록했다.

## Anchor별 등록부

| Topic ID | 순번 | Anchor ID | 판정 |
|---|---:|---|---|
| `instrumentation_production_management_planning_quality_cost_resources` | 11 | `production_material_requirement_availability` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 12 | `production_manpower_skill_shift` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 13 | `production_equipment_resource_availability` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 14 | `production_quality_plan_ctq_spec` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 15 | `production_fpy_yield_scrap_rework` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 16 | `production_process_quality_feedback` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 17 | `production_defect_containment_traceability` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 18 | `production_cost_structure` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 19 | `production_standard_actual_cost_variance` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 20 | `production_unit_cost_volume_yield` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 21 | `production_energy_consumables_cost` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 22 | `production_oee_apq_formula_boundary` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 23 | `production_throughput_cycle_lead_wip_kpi` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 24 | `production_schedule_adherence_delivery_kpi` | 조건 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 25 | `production_mes_data_handoff` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 26 | `production_erp_mes_role_boundary` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 27 | `production_daily_management_visual_control` | 확인 |
| `instrumentation_production_management_planning_quality_cost_resources` | 28 | `production_pdca_tradeoff_improvement` | 조건 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 1 | `project_lifecycle_stage_gate` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 2 | `project_scope_boundary_interface` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 3 | `project_design_basis_requirements` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 4 | `project_wbs_responsibility_raci` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 5 | `project_schedule_milestone_dependency_critical_path` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 6 | `project_progress_measurement_forecast` | 조건 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 7 | `project_cost_estimate_basis_quantity_rate_contingency` | 조건 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 8 | `project_cost_baseline_commitment_actual_forecast` | 조건 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 9 | `project_risk_register_mitigation` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 10 | `project_change_control_scope_cost_schedule` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 11 | `project_document_control_revision_transmittal` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 12 | `project_master_deliverable_register` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 13 | `instrument_index_master_tag_register` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 14 | `instrument_datasheet_process_mechanical_interface` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 15 | `instrument_document_set_loop_hookup_cable_jb` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 16 | `io_list_software_project_handoff` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 17 | `instrument_quantity_mto_boq` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 18 | `procurement_requisition_rfq_tbe_po` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 19 | `vendor_document_review_integration` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 20 | `vendor_inspection_acceptance_handoff` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 21 | `construction_installation_readiness` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 22 | `construction_qa_qc_itp_hold_witness` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 23 | `mechanical_completion_punch_systemization` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 24 | `precommissioning_loop_readiness_handoff` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 25 | `project_acceptance_criteria_evidence` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 26 | `asbuilt_handover_document_dossier` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 27 | `operations_maintenance_handover_boundary` | 확인 |
| `instrumentation_project_management_basic_design_cost_schedule_documents_acceptance` | 28 | `project_closeout_lessons_learned` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 1 | `design_basis_purpose` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 2 | `governing_requirements_register` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 3 | `code_standard_spec_distinction` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 4 | `applicability_edition_jurisdiction` | 조건 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 5 | `hierarchy_precedence_conflict` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 6 | `process_design_conditions` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 7 | `measurement_performance_requirements` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 8 | `environment_hazardous_safety_requirements` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 9 | `architecture_reliability_maintainability` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 10 | `interfaces_utilities_communication` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 11 | `documentation_set_consistency` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 12 | `instrument_identification_standardization` | 조건 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 13 | `specification_datasheet_verifiable_requirements` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 14 | `vendor_bid_deviation_list` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 15 | `technical_bid_evaluation_traceability` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 16 | `deviation_definition_controlled_departure` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 17 | `deviation_impact_risk_assessment` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 18 | `deviation_approval_authority` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 19 | `deviation_disposition_closure` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 20 | `change_control_moc_boundary` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 21 | `as_built_handover_baseline` | 확인 |
| `instrumentation_system_design_basis_codes_standards_specification_deviation_management` | 22 | `lifecycle_traceability_verification_acceptance` | 조건 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 1 | `lead_lag_design_objective` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 2 | `lead_lag_lead_pole_zero_geometry` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 3 | `lead_lag_lead_maximum_phase_relation` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 4 | `lead_lag_lead_center_frequency_magnitude` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 5 | `lead_lag_lead_phase_margin_design_sequence` | 조건 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 6 | `lead_lag_lead_bandwidth_noise_effort_tradeoff` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 7 | `lead_lag_lag_pole_zero_geometry` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 8 | `lead_lag_lag_steady_state_error_improvement` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 9 | `lead_lag_lag_crossover_phase_loss` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 10 | `lead_lag_lag_gain_ratio_error_constant` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 11 | `lead_lag_combined_design` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 12 | `lead_lag_root_locus_frequency_consistency` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 13 | `lead_lag_plant_robustness_limits` | 확인 |
| `lead_lag_compensator_phase_margin_steady_state_error` | 14 | `lead_lag_implementation_validation` | 조건 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 1 | `state_lqr_design_objective_cost` | 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 2 | `state_lqr_weight_matrix_conditions` | 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 3 | `state_lqr_care_stabilizing_solution` | 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 4 | `state_lqr_optimal_gain_closed_loop` | 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 5 | `state_lqr_existence_stabilizability_detectability` | 조건 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 6 | `state_lqr_q_weight_state_tradeoff` | 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 7 | `state_lqr_r_weight_control_tradeoff` | 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 8 | `state_lqr_common_scaling_invariance` | 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 9 | `state_lqr_state_input_normalization_bryson` | 조건 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 10 | `state_lqr_pole_placement_distinction` | 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 11 | `state_lqr_tracking_prefilter_lqi` | 조건 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 12 | `state_lqr_saturation_constraints_limit` | 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 13 | `state_lqr_continuous_discrete_riccati_distinction` | 확인 |
| `lqr_optimal_state_feedback_riccati_weighting_design` | 14 | `state_lqr_robustness_observer_implementation_validation` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 1 | `lvdt_differential_transformer_structure` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 2 | `lvdt_primary_ac_excitation` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 3 | `lvdt_secondary_series_opposition` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 4 | `lvdt_core_position_mutual_inductance` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 5 | `lvdt_differential_output_es1_es2` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 6 | `lvdt_null_position_voltage_balance` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 7 | `lvdt_output_amplitude_displacement` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 8 | `lvdt_output_phase_direction` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 9 | `lvdt_linear_measurement_range` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 10 | `lvdt_null_residual_voltage` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 11 | `lvdt_demodulated_zero_offset` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 12 | `lvdt_phase_sensitive_demodulation` | 조건 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 13 | `lvdt_low_pass_dc_output` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 14 | `lvdt_excitation_frequency_voltage_sensitivity` | 조건 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 15 | `lvdt_core_alignment_eccentricity_error` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 16 | `lvdt_temperature_coil_resistance_error` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 17 | `lvdt_magnetic_saturation_nonlinearity` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 18 | `lvdt_cable_shield_grounding_error` | 조건 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 19 | `lvdt_dynamic_response_frequency_bandwidth` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 20 | `rvdt_rotary_angle_measurement` | 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 21 | `lvdt_calibration_traceability_diagnostics` | 조건 확인 |
| `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error` | 22 | `lvdt_vs_strain_gauge_displacement_principle` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 1 | `closed_loop_characteristic_equation` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 2 | `nyquist_contour_and_mapping` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 3 | `argument_principle_pnz_relation` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 4 | `critical_point_minus_one` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 5 | `open_loop_rhp_poles_count` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 6 | `closed_loop_rhp_poles_count` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 7 | `stable_open_loop_special_case` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 8 | `imaginary_axis_pole_indentation` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 9 | `conjugate_symmetry` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 10 | `gain_margin_definition` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 11 | `phase_margin_definition` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 12 | `multiple_crossover_interpretation` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 13 | `time_delay_phase_effect` | 확인 |
| `nyquist_stability_criterion_gain_phase_margin` | 14 | `field_robustness_validation` | 조건 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 1 | `optical_noncontact_measurement_chain` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 2 | `photoelectric_conversion_principle` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 3 | `photoelectric_through_beam_mode` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 4 | `photoelectric_retroreflective_mode` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 5 | `photoelectric_diffuse_reflective_mode` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 6 | `photoelectric_intensity_boundary` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 7 | `optical_direct_tof_round_trip` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 8 | `optical_direct_tof_distance_equation` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 9 | `optical_indirect_tof_phase_principle` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 10 | `optical_itof_phase_ambiguity` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 11 | `laser_triangulation_principle` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 12 | `laser_triangulation_detector_coordinate` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 13 | `laser_triangulation_calibration` | 조건 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 14 | `triangulation_range_resolution_tradeoff` | 조건 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 15 | `surface_reflectivity_color_effect` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 16 | `specular_transparent_surface_error` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 17 | `ambient_light_filtering` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 18 | `laser_speckle_effect` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 19 | `alignment_occlusion_geometry` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 20 | `tof_timing_jitter_resolution` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 21 | `detector_saturation_dynamic_range` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 22 | `multipath_mixed_pixel_error` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 23 | `calibration_reference_traceability` | 조건 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 24 | `accuracy_resolution_repeatability_boundary` | 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 25 | `wavelength_material_selection` | 조건 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 26 | `optical_method_selection_tradeoff` | 조건 확인 |
| `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` | 27 | `optical_vs_ultrasonic_tof_comparison` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 1 | `sw09_security_objectives` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 2 | `sw09_asset_inventory` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 3 | `sw09_criticality_classification` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 4 | `sw09_risk_assessment` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 5 | `sw09_system_under_consideration` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 6 | `sw09_zone_conduit` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 7 | `sw09_segmentation` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 8 | `sw09_industrial_dmz` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 9 | `sw09_firewall_policy` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 10 | `sw09_unidirectional_gateway` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 11 | `sw09_ids_ips_monitoring` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 12 | `sw09_allowlisting` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 13 | `sw09_least_privilege` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 14 | `sw09_authentication` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 15 | `sw09_authorization` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 16 | `sw09_remote_access` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 17 | `sw09_jump_server` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 18 | `sw09_mfa` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 19 | `sw09_secure_remote_session` | 조건 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 20 | `sw09_patch_management` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 21 | `sw09_vulnerability_management` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 22 | `sw09_legacy_compensating_control` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 23 | `sw09_secure_configuration_baseline` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 24 | `sw09_security_change_control` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 25 | `sw09_supply_chain_risk` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 26 | `sw09_supplier_assurance` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 27 | `sw09_sbom` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 28 | `sw09_software_firmware_integrity` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 29 | `sw09_removable_media` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 30 | `sw09_logging` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 31 | `sw09_time_synchronization_forensics` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 32 | `sw09_detection_triage` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 33 | `sw09_incident_response_plan` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 34 | `sw09_containment_eradication` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 35 | `sw09_trusted_recovery` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 36 | `sw09_backup_recovery_security` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 37 | `sw09_business_continuity` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 38 | `sw09_safety_coordination` | 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 39 | `sw09_exercise_metrics` | 조건 확인 |
| `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` | 40 | `sw09_lifecycle_decommissioning` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 1 | `sensor_passive_transduction_chain` | 확인 |
