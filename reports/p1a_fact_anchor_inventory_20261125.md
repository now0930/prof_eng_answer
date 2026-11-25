# P1-A — 최신 Fact Anchor Inventory 및 457/48 연결 감사 (2026-11-25)

기준 main: `45c7d146e4673e885005c04535e65dc9b9d7c8a5`, tree `d06a43d7b36323b587e52086c495f12dcc8e9442`. Owner [#40](https://github.com/now0930/prof_eng_answer/issues/40), 문서·감사 PR [#49](https://github.com/now0930/prof_eng_answer/pull/49).

**판정: P1-A 구조 집계 완료 / AUDIT_ONLY / score_admission=DISABLED / score_effect=none.** 457건 기술 검토는 #42에서 종결된 이력을 보존하며, 단문화 후보의 기술 동등성과 적용 여부는 P1-B/C에서 별도 판단한다. 정본, Registry, 승인 Ledger, Generated, 제외 정책과 운영 점수는 변경하지 않는다.

## 1. 읽기 전용 검사 방법

- 고정 main Git tree의 `rubrics/topic_packs/*/fact_anchor.json` 89개와 `topic_status.json` 12개를 실제 Git blob으로 읽었다. 7회 분할 조회로 정본 2,096개 owner/Anchor ID/statement를 [Generated Fact Anchor bank](../rubrics/generated/fact_anchors.generated.json) blob `06108f815b5a802573e493504656b77f1de8bc49`와 직접 비교했다. 각 정본 파일의 Topic owner, ID 중복, ID별 문장 및 건수 차이 모두 0. 이후 교집합 및 텍스트 집계는 일치 확인한 bank의 투영에 대해 수행했다.
- [Registry](../grading/evidence/approved_fact_registry.json) blob `69124be63df2216e5077a1d74ddfc887503bedd5` 1,524행 전체를 실제 JSON으로 읽었다. 정본과는 `(topic_id, legacy_anchor_id)` 정확 조인만 적용했다. 일반 file 조회가 4MB 파일에 빈 응답을 반환하여 Git blob 조회로 대체했다.
- [동결 457 후보](fact_atomicity_triage/) batch_01–07 7개 원본과 [D4 종료 SHA의 48 후보](https://github.com/now0930/prof_eng_answer/blob/5a49a7daf042fc4749b9ae137c9af054ff68afae/calibration/fact_anchor_simplification_review_20261114.json) blob `38e90d7300ed8b2c5eda2d995a005bd3c785ea15`를 다시 읽어 정확한 owner/ID로 비교했다.
- [기존 제외 함수](../grading/evidence/fact_anchor_scoring_exclusions.py)의 네 계층 JSON을 직접 읽었다. anchor key 및 연결 Registry fact ID 차단을 비교했다. 실제 Python 함수 호출, 후보 hold statement SHA-256 재계산 및 새 전체 pytest/Actions는 NOT_RUN. 마지막 검증된 main Actions [45582704118](https://github.com/now0930/prof_eng_answer/actions/runs/45582704118)는 별도 과거 실행 증거다.
- 처음 한 번의 대량 API 호출은 호출 수 제한으로 완료되지 않아 분할 조회했다. 완료 집계에는 실제 응답으로 확인한 자료만 사용한다.

## 2. 집계 결과

| 집계 항목 | 전체 | 역사적 457 | 단문화 48 |
|---|---:|---:|---:|
| Anchor 수 | 2096 | 457 | 48 |
| 관리형 Topic 소속 | 86 | 8 | 0 |
| Registry 정확 owner/legacy-ID 연결 | 1522 | 429 | 48 |
| 연결된 Registry 중 문장 완전 일치 | 614 | 218 | 5 |
| 연결됐으나 문장 완전 불일치 | 908 | 211 | 43 |
| 정확 Registry 조인 없음 | 574 | 28 | 0 |
| 기존 제외 계층에 등재 | 539 | 188 | 2 |
| 제외 계층 미등재 | 1557 | 269 | 46 |
| 복문 휴리스틱 | 457 | 457 | 48 |
| 조건 cue | 775 | 289 | 31 |
| 250 Unicode codepoint 이상 | 102 | 90 | 2 |
| 식·단위 표기 cue | 188 | 53 | 12 |
| 예외·범위 cue | 102 | 47 | 8 |

- 89 Topic 중 관리형 12개 / legacy 77개. 관리형의 12개 상태 파일 모두 owner 일치, approved/reviewed, approved_source_hash 존재, review_method human 10 / ai 2. 개별 hash 재계산은 이번 감사 범위가 아니다. 86/2,010 Anchor의 관리형/legacy 분류는 구조 분류이며 개별 기술적 승인과 동일하지 않다.
- 2,096 고유 `(topic_id, anchor_id)` 및 Anchor ID 문자열 교차 Topic 중복 0. 공백 정규화와 대소문자 무시 비교 기준 동일 Topic/다른 Topic exact statement 중복 각각 0 그룹. 의미 중복의 부재까지 뜻하지 않는다.
- 정본 anchor 객체의 `source_basis`가 비어 있거나 없는 행 120개, `importance` 필드가 비어 있거나 없는 행 66개. 이는 필드 형식 차이의 실측값이며 실제 출처 부재나 배점 부재로 간주하지 않는다. managed source sheet, Topic-level importance/required/weight, Registry provenance를 개별 검토 없이 자동 수정하지 않는다.
- 복문/조건은 기존 `scripts/audit_fact_anchor_claim_inventory.py`의 패턴과 동일. 250자, 식·단위(=,≈,∝,≤,≥,±,√, LaTeX frac, rpm/Hz/kHz/Pa/kPa/MPa/mA/kg/mm/dB), 예외·범위(예외, 제외, 항상, 반드시, 일반적으로, 한정, 단정, unless/except/always)는 본 감사용 휴리스틱. 필수 조건·단위·예외 누락은 이 수치만으로 판정할 수 없으며 P1-B에서 후보별 검토한다.

## 3. 기존 승인 및 제외 관계

| 구분 | 건수 | 의미 |
|---|---:|---|
| Registry 전체 행 / 고유 fact_id | 1,524 / 1,524 | 기존 승인 데이터 |
| Registry 정확 owner/legacy-ID 키 | 1,523 | legacy_anchor_id 미지정 1개 포함 |
| 정본에 연결된 Registry 행 | 1,523 | 1개 Anchor에 2개 Fact 연결 |
| Registry 연결 정본 Anchor | 1,522 | 2,096개 중 exact owner/legacy ID join |
| 연결 없는 정본 Anchor | 574 | Registry 미연결 ≠ 미승인 또는 오류 |
| Registry revision 1 / 2 | 1,507 / 17 | 승인 반영 결과 유지 |
| approved / verified / score_effect=none | 1,524 / 1,524 / 1,524 | 신규 Claim 채점 권한 없음 |
| 채점 제외 기본 계층 | 276 | 기존 exclusion |
| 독립 재검토 hold | 80 | 기존 hold |
| 미해결 출처 hold | 80 | 기존 hold |
| 1656 후보 hold | 103 | 기존 hold |
| 4계층 합집합 | 539 | 중복 키 0 / 정본 미대응 0 / Registry fact-id 단독 추가 차단 0 |
| 제외 계층 미등재 | 1,557 | 실제 출제/채점 적격성 보증 아님 |

Registry 미연결 행 1개: `liquid_in_glass_thermometer_calibration_is_immersion_condition_specific` (temperature_measurement_error_heat_transfer; legacy_anchor_id 없음). 별도 Fact의 정상적인 소유 범위일 수 있으므로 orphan 오류로 판정하지 않는다. 다중 연결 키 1개: `balanced_trim_unbalanced_trim_structure_sealing_applications/unbalanced_trim_direct_pressure_loading`에 `unbalanced_trim_pressure_differential_loads_plug`, `unbalanced_trim_static_pressure_force` 두 Fact가 대응한다. 동일 ID 중복은 아니며, 의미/권한 매핑은 P2-A에서 확인한다.

## 4. 457건과 48건의 관계

- 동결 457행 모두 고유 ID이며 현재 main에서 누락 0. 동결 문장과 다른 정본 30건은 이전 기술 검토·승인 반영과 일치하는 건수다(이전 종결 보고의 30건을 재승인한 것은 아님). 나머지 427건 문장 동일. 기존 #42 판정과 이력은 수정하지 않는다.
- 48개 고유 후보 전부 457 집합에 포함(48/48). 457 중 후보 아닌 409건. 전체 2,096 중 역사적 457 외 1,639건. 48건 전부 legacy Topic이며 Registry exact owner/legacy ID 연결이 존재한다.
- 후보 48건 모두 `PENDING_TECHNICAL_REVIEW / CANDIDATE_ONLY_NOT_APPLIED`. 현재 정본과 previous_statement 일치 43, 양쪽 후보 문장과 다른 정본 5, simplified_statement와 완전 일치 0. 48건 중 제외 2건(마르코프 복잡도, 초저습도 이슬점 선택), 미등재 46. 기존 제외 상태를 유지한다.
- 달라진 5개 정본: `absolute_humidity_definition`, `counting_window_speed_equation`, `encoder_frequency_limit_selection`, `gear_tooth_speed_equation`, `thermocouple_measures_temperature_difference`. 최신 승인·기술 보완을 우선하여 과거 단문화 문장으로 되돌리지 않는다.

## 5. Topic별 구조 집계

| Topic ID | 유형 | Anchor | 457 | 48 | Registry 연결 | 제외 | 복문 | 조건 cue | 장문 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting | managed | 10 | 0 | 0 | 10 | 1 | 0 | 0 | 0 |
| balanced_trim_unbalanced_trim_structure_sealing_applications | legacy | 36 | 5 | 0 | 32 | 19 | 5 | 5 | 2 |
| bode_frequency_response_stability_margin_bandwidth | legacy | 14 | 1 | 0 | 14 | 3 | 1 | 6 | 0 |
| configuration_change_release_backup_rollback_migration_obsolescence_management | legacy | 40 | 23 | 0 | 37 | 20 | 23 | 21 | 13 |
| control_hardware_lifecycle_panel_architecture_component_selection_production_verification | legacy | 35 | 0 | 0 | 5 | 6 | 0 | 7 | 7 |
| control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe | legacy | 28 | 2 | 0 | 15 | 10 | 2 | 16 | 0 |
| control_software_project_engineering_documents_fat_sat_commissioning_acceptance | legacy | 34 | 2 | 2 | 6 | 11 | 2 | 17 | 0 |
| control_system_operations_maintenance_calibration_inspection_spares_kpi | legacy | 26 | 19 | 0 | 26 | 17 | 19 | 17 | 9 |
| control_valve_authority_rangeability_gain_installed_performance | legacy | 28 | 0 | 0 | 28 | 6 | 0 | 12 | 0 |
| control_valve_cavitation_flashing_choked_flow_damage_prevention | legacy | 36 | 5 | 0 | 35 | 19 | 5 | 6 | 1 |
| control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening | legacy | 22 | 1 | 0 | 22 | 2 | 1 | 10 | 1 |
| control_valve_deadband_stiction_response_time_positioner_dynamic_performance | legacy | 24 | 17 | 0 | 24 | 13 | 17 | 12 | 9 |
| control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe | legacy | 22 | 3 | 0 | 22 | 16 | 3 | 7 | 0 |
| control_valve_gas_sizing_choked_flow_critical_pressure_ratio | legacy | 34 | 0 | 0 | 34 | 22 | 0 | 8 | 0 |
| control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing | legacy | 20 | 0 | 0 | 1 | 2 | 0 | 4 | 0 |
| control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim | legacy | 38 | 3 | 0 | 36 | 11 | 3 | 6 | 1 |
| control_valve_positioner_ip_converter_booster_accessories_calibration | legacy | 40 | 21 | 0 | 36 | 26 | 21 | 16 | 7 |
| control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions | legacy | 48 | 19 | 0 | 43 | 24 | 19 | 19 | 9 |
| control_valve_selection_process_pressure_temperature_flow_media_lifecycle | legacy | 52 | 2 | 0 | 2 | 4 | 2 | 21 | 2 |
| control_valve_severe_service_high_low_flow_temperature_cryogenic_particles | legacy | 48 | 2 | 0 | 23 | 11 | 2 | 7 | 1 |
| control_valve_sizing_cv_kv_reynolds_liquid_selection | legacy | 32 | 3 | 0 | 32 | 9 | 3 | 12 | 0 |
| control_valve_types_globe_rotary_body_actuator_selection | legacy | 29 | 1 | 0 | 29 | 10 | 1 | 11 | 0 |
| differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error | legacy | 28 | 27 | 0 | 28 | 10 | 27 | 16 | 7 |
| displacer_level_buoyancy_torque_tube_density_interface_calibration | managed | 7 | 4 | 0 | 7 | 2 | 4 | 2 | 0 |
| dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation | managed | 7 | 2 | 0 | 7 | 4 | 2 | 0 | 0 |
| electronics_error_noise_drift_tolerance_aging_power_mitigation | legacy | 36 | 8 | 0 | 31 | 6 | 8 | 20 | 5 |
| emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits | legacy | 27 | 0 | 0 | 15 | 15 | 0 | 5 | 0 |
| feedback_system_closed_loop_sensitivity_steady_state_error | legacy | 11 | 9 | 5 | 11 | 2 | 9 | 5 | 0 |
| fiber_optic_link_modes_dispersion_loss_otdr_diagnostics | managed | 6 | 0 | 0 | 6 | 0 | 0 | 1 | 0 |
| final_control_element_sil_sis_esd_valve_partial_stroke_test | legacy | 48 | 42 | 0 | 29 | 7 | 42 | 18 | 0 |
| flow_measurement_meter_principles_velocity_selection | managed | 16 | 0 | 0 | 13 | 0 | 0 | 7 | 0 |
| fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection | managed | 8 | 0 | 0 | 8 | 2 | 0 | 3 | 0 |
| functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh | legacy | 26 | 3 | 3 | 26 | 1 | 3 | 10 | 0 |
| hazardous_area_explosion_protection_intrinsic_safety_equipment_selection | legacy | 22 | 4 | 0 | 22 | 2 | 4 | 16 | 0 |
| hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards | legacy | 26 | 2 | 0 | 0 | 1 | 2 | 11 | 1 |
| hazop_lopa_ipl_risk_reduction_sil_target_allocation | legacy | 25 | 2 | 0 | 25 | 9 | 2 | 11 | 0 |
| hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture | legacy | 25 | 0 | 0 | 0 | 0 | 0 | 8 | 0 |
| historian_mes_it_ot_integration_industrial_data_quality_realtime_processing | legacy | 29 | 0 | 0 | 29 | 13 | 0 | 2 | 0 |
| hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management | legacy | 31 | 2 | 0 | 9 | 3 | 2 | 11 | 0 |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | legacy | 22 | 15 | 12 | 22 | 4 | 15 | 10 | 2 |
| industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle | legacy | 30 | 0 | 0 | 24 | 4 | 0 | 7 | 0 |
| industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread | legacy | 29 | 0 | 0 | 4 | 6 | 0 | 6 | 2 |
| industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience | legacy | 40 | 2 | 0 | 19 | 3 | 2 | 12 | 0 |
| industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection | legacy | 40 | 0 | 0 | 20 | 12 | 0 | 6 | 0 |
| instrument_signal_transmission_line_reflection_termination | managed | 5 | 0 | 0 | 5 | 0 | 0 | 1 | 0 |
| instrumentation_control_software_lifecycle_v_model_traceability_verification_validation | legacy | 33 | 2 | 0 | 8 | 4 | 2 | 12 | 1 |
| instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification | legacy | 32 | 3 | 0 | 15 | 3 | 3 | 16 | 0 |
| instrumentation_installation_wiring_impulse_tubing_inspection_codes | legacy | 33 | 0 | 0 | 7 | 7 | 0 | 13 | 0 |
| instrumentation_power_grounding_shielding_ups_ground_loop_emc | legacy | 29 | 7 | 0 | 25 | 22 | 7 | 15 | 0 |
| instrumentation_production_management_planning_quality_cost_resources | legacy | 28 | 11 | 0 | 28 | 10 | 11 | 13 | 3 |
| instrumentation_project_management_basic_design_cost_schedule_documents_acceptance | legacy | 28 | 0 | 0 | 0 | 5 | 0 | 9 | 0 |
| instrumentation_system_design_basis_codes_standards_specification_deviation_management | legacy | 22 | 2 | 0 | 0 | 0 | 2 | 16 | 0 |
| lead_lag_compensator_phase_margin_steady_state_error | legacy | 14 | 3 | 0 | 14 | 2 | 3 | 3 | 0 |
| lqr_optimal_state_feedback_riccati_weighting_design | legacy | 14 | 4 | 0 | 14 | 1 | 4 | 4 | 0 |
| lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error | legacy | 22 | 12 | 0 | 22 | 6 | 12 | 11 | 0 |
| nyquist_stability_criterion_gain_phase_margin | legacy | 14 | 0 | 0 | 14 | 2 | 0 | 1 | 0 |
| open_channel_weir_flume_head_discharge_submergence_selection | managed | 5 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| optical_laser_photoelectric_noncontact_measurement_tof_triangulation | legacy | 27 | 15 | 0 | 27 | 4 | 15 | 16 | 5 |
| ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response | legacy | 40 | 39 | 0 | 40 | 15 | 39 | 16 | 1 |
| passive_sensor_resistive_capacitive_inductive_transduction | legacy | 14 | 3 | 0 | 14 | 0 | 3 | 3 | 0 |
| physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control | legacy | 30 | 5 | 0 | 9 | 6 | 5 | 12 | 3 |
| pid_controller_tuning_sequence_gain_effects | legacy | 10 | 0 | 0 | 10 | 1 | 0 | 4 | 0 |
| pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative | legacy | 24 | 1 | 0 | 24 | 4 | 1 | 7 | 1 |
| piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration | legacy | 20 | 0 | 0 | 20 | 3 | 0 | 5 | 0 |
| plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability | legacy | 26 | 0 | 0 | 6 | 0 | 0 | 11 | 0 |
| power_electronics_converters_motor_drive_control | managed | 7 | 0 | 0 | 7 | 0 | 0 | 5 | 0 |
| pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error | legacy | 22 | 10 | 7 | 21 | 2 | 10 | 12 | 0 |
| pressure_transmitter_force_balance_null_detection | managed | 5 | 0 | 0 | 5 | 3 | 0 | 0 | 0 |
| process_control_loop_architecture_cascade_ratio_feedforward_override_split_range | legacy | 19 | 7 | 0 | 19 | 3 | 7 | 13 | 0 |
| radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error | legacy | 28 | 13 | 0 | 28 | 12 | 13 | 15 | 1 |
| root_locus_stability_gain_design | legacy | 14 | 0 | 0 | 14 | 2 | 0 | 3 | 0 |
| routh_hurwitz_stability_criterion_gain_range | legacy | 14 | 0 | 0 | 14 | 1 | 0 | 4 | 0 |
| rtd_temperature_sensor_principle_pt100_wiring_compensation | legacy | 14 | 0 | 0 | 14 | 5 | 0 | 4 | 0 |
| safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis | legacy | 33 | 1 | 0 | 32 | 5 | 1 | 18 | 0 |
| second_order_lag_response_by_damping_ratio | legacy | 9 | 3 | 0 | 9 | 0 | 3 | 0 | 0 |
| second_order_system_modeling_electromechanical_analogy | managed | 5 | 0 | 0 | 5 | 3 | 0 | 0 | 0 |
| second_order_system_resonance_frequency_response | legacy | 5 | 3 | 0 | 5 | 0 | 3 | 2 | 0 |
| sil_target_determination_risk_reduction_and_lifecycle | legacy | 16 | 11 | 0 | 16 | 6 | 11 | 9 | 2 |
| sis_sil_safety_software_independence_systematic_failure_verification_validation | legacy | 34 | 5 | 0 | 33 | 11 | 5 | 6 | 0 |
| smart_positioner_diagnostics_valve_signature_predictive_maintenance | legacy | 44 | 0 | 0 | 12 | 6 | 0 | 4 | 0 |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | legacy | 22 | 22 | 11 | 22 | 2 | 22 | 15 | 5 |
| state_feedback_reference_tracking_prefilter_integral_action | legacy | 14 | 4 | 0 | 14 | 2 | 4 | 9 | 0 |
| state_space_controllability_observability_pole_placement | legacy | 14 | 0 | 0 | 14 | 2 | 0 | 1 | 0 |
| strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error | legacy | 14 | 1 | 0 | 14 | 2 | 1 | 3 | 0 |
| temperature_measurement_error_heat_transfer | legacy | 5 | 1 | 0 | 5 | 1 | 1 | 3 | 0 |
| thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization | legacy | 14 | 0 | 0 | 14 | 3 | 0 | 9 | 0 |
| thermocouple_temperature_sensor_seebeck_reference_junction_compensation | legacy | 14 | 14 | 8 | 14 | 2 | 14 | 12 | 1 |
| ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error | legacy | 20 | 2 | 0 | 20 | 3 | 2 | 6 | 0 |
| vibratory_gyroscope_coriolis_angular_rate_sensing | managed | 5 | 2 | 0 | 2 | 0 | 2 | 3 | 0 |

## 6. P1-B 고정 입력 — 48건 개별 조인

아래 48행은 모두 457 이력에 포함된다. 기술적 동등성 판정은 NOT_RUN. `NOT_LISTED`는 4개 기존 제외 계층 미등재이며 승인이나 점수 권한을 의미하지 않는다.

| Topic ID | Anchor ID | 정본 vs previous | 정본 vs simplified | Registry Fact ID @ revision | 정본·Registry 문장 일치 | 기존 제외 계층 |
|---|---|---|---|---|---|---|
| functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh | fsrm_markov_state_transition | EQUAL | DIFFERENT | markov_reliability_model_uses_system_states_and_transition_rates_to_track_state_probabilities@1 | EQUAL | NOT_LISTED |
| functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh | fsrm_markov_complexity | EQUAL | DIFFERENT | markov_state_space_growth_can_increase_analysis_burden_without_universal_growth_rate@1 | EQUAL | fact_anchor_scoring_exclusions_20261101.json |
| functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh | fsrm_model_assumption_documentation | EQUAL | DIFFERENT | sis_reliability_result_records_boundary_mode_and_applicable_model_inputs@1 | EQUAL | NOT_LISTED |
| control_software_project_engineering_documents_fat_sat_commissioning_acceptance | sw10_fat_sat_relation | EQUAL | DIFFERENT | fat_and_sat_are_distinct_complementary_test_stages@1 | EQUAL | NOT_LISTED |
| control_software_project_engineering_documents_fat_sat_commissioning_acceptance | sw10_loop_test | EQUAL | DIFFERENT | iec62382_loop_check_scope_and_boundaries@1 | EQUAL | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | relative_humidity_definition | EQUAL | DIFFERENT | relative_humidity_is_vapor_pressure_ratio_at_same_temperature@1 | DIFFERENT | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | rh_temperature_dependence | EQUAL | DIFFERENT | relative_humidity_varies_with_temperature_at_fixed_vapor_pressure@1 | DIFFERENT | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | absolute_humidity_definition | DIFFERENT | DIFFERENT | absolute_humidity_is_water_vapor_mass_concentration@1 | DIFFERENT | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | dew_point_definition | EQUAL | DIFFERENT | dew_point_is_saturation_temperature_for_existing_vapor_pressure@1 | DIFFERENT | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | frost_point_distinction | EQUAL | DIFFERENT | frost_point_names_vapor_to_ice_saturation_condition@1 | DIFFERENT | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | pressure_dew_point_effect | EQUAL | DIFFERENT | pressure_changes_compressed_gas_dew_point_parameter@1 | DIFFERENT | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | capacitive_polymer_principle | EQUAL | DIFFERENT | capacitive_humidity_sensor_polymer_dielectric_changes_with_absorbed_water@1 | DIFFERENT | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | resistive_humidity_principle | EQUAL | DIFFERENT | resistive_humidity_element_resistance_changes_with_absorbed_vapor@1 | DIFFERENT | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | psychrometric_wet_dry_bulb | EQUAL | DIFFERENT | psychrometric_wet_bulb_is_not_dew_point_except_at_saturation@1 | DIFFERENT | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | condensation_sensor_temperature_error | EQUAL | DIFFERENT | probe_temperature_difference_can_bias_rh_or_cause_condensation@1 | DIFFERENT | NOT_LISTED |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | low_humidity_dew_point_selection | EQUAL | DIFFERENT | dew_point_is_preferred_measurement_parameter_in_ultra_dry_vaisala_applications@1 | DIFFERENT | fact_anchor_unresolved_source_holds_20261101.json |
| humidity_measurement_capacitive_resistive_dew_point_selection_compensation | selection_environment_process | EQUAL | DIFFERENT | humidity_instrument_selection_matches_application_to_model_limits@1 | DIFFERENT | NOT_LISTED |
| feedback_system_closed_loop_sensitivity_steady_state_error | feedback_sensitivity_functions | EQUAL | DIFFERENT | sensitivity_and_complementary_sensitivity_functions@1 | DIFFERENT | NOT_LISTED |
| feedback_system_closed_loop_sensitivity_steady_state_error | feedback_parameter_sensitivity | EQUAL | DIFFERENT | closed_loop_parameter_sensitivity@1 | DIFFERENT | NOT_LISTED |
| feedback_system_closed_loop_sensitivity_steady_state_error | feedback_disturbance_noise_paths | EQUAL | DIFFERENT | output_disturbance_and_measurement_noise_paths@1 | DIFFERENT | NOT_LISTED |
| feedback_system_closed_loop_sensitivity_steady_state_error | feedback_steady_state_error_final_value | EQUAL | DIFFERENT | steady_state_error_final_value_theorem@1 | DIFFERENT | NOT_LISTED |
| feedback_system_closed_loop_sensitivity_steady_state_error | feedback_integral_action_tradeoff | EQUAL | DIFFERENT | feedback_integral_action_tradeoff@1 | DIFFERENT | NOT_LISTED |
| pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error | bourdon_forms_application | EQUAL | DIFFERENT | bourdon_tube_forms_and_ranges_are_design_specific@1 | DIFFERENT | NOT_LISTED |
| pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error | diaphragm_deflection_principle | EQUAL | DIFFERENT | diaphragm_differential_pressure_deflection_and_sensitivity@1 | DIFFERENT | NOT_LISTED |
| pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error | diaphragm_sensor_vs_seal | EQUAL | DIFFERENT | diaphragm_sensing_element_vs_remote_seal_function@1 | DIFFERENT | NOT_LISTED |
| pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error | piezoresistive_static_capability | EQUAL | DIFFERENT | piezoresistive_vs_piezoelectric_static_pressure_response@1 | DIFFERENT | NOT_LISTED |
| pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error | dp_transmitter_two_port_principle | EQUAL | DIFFERENT | differential_pressure_transmitter_two_port_sensing@1 | DIFFERENT | NOT_LISTED |
| pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error | ambient_environment_hazardous_selection | EQUAL | DIFFERENT | pressure_transmitter_environmental_and_approval_selection_is_installation_specific@1 | DIFFERENT | NOT_LISTED |
| pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error | accuracy_total_performance_terms | EQUAL | DIFFERENT | pressure_reference_accuracy_and_operating_effects_are_distinct_specification_terms@1 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | pulse_frequency_speed_equation | EQUAL | DIFFERENT | encoder_pulse_frequency_to_rpm_equation@1 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | counting_window_speed_equation | DIFFERENT | DIFFERENT | encoder_fixed_window_count_to_rpm_equation@1 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | period_measurement_low_speed | EQUAL | DIFFERENT | rotation_speed_period_measurement_formula_and_low_speed_tradeoff@1 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | quadrature_direction_principle | EQUAL | DIFFERENT | quadrature_phase_order_encodes_direction@1 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | index_z_channel_role | EQUAL | DIFFERENT | encoder_index_is_reference_mark_not_multiturn_absolute_position@1 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | absolute_encoder_principle | EQUAL | DIFFERENT | absolute_encoder_code_identifies_position_and_speed_is_sampled@1 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | encoder_frequency_limit_selection | DIFFERENT | DIFFERENT | encoder_speed_and_decode_rate_must_fit_frequency_limits@2 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | inductive_proximity_principle | EQUAL | DIFFERENT | inductive_proximity_metal_target_eddy_current_detection@1 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | gear_tooth_speed_equation | DIFFERENT | DIFFERENT | rotation_speed_tooth_event_frequency_relation@2 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | tachogenerator_voltage_speed_principle | EQUAL | DIFFERENT | permanent_magnet_dc_tachogenerator_voltage_tracks_speed@1 | DIFFERENT | NOT_LISTED |
| speed_rotation_measurement_encoder_proximity_tachometer_selection_error | digital_tachometer_instrument_boundary | EQUAL | DIFFERENT | digital_tachometer_can_measure_from_external_sensor_pulses@1 | DIFFERENT | NOT_LISTED |
| thermocouple_temperature_sensor_seebeck_reference_junction_compensation | thermocouple_temperature_measurement_chain | EQUAL | DIFFERENT | thermocouple_temperature_measurement_chain@1 | DIFFERENT | NOT_LISTED |
| thermocouple_temperature_sensor_seebeck_reference_junction_compensation | thermocouple_seebeck_effect_dissimilar_conductors | EQUAL | DIFFERENT | thermocouple_seebeck_effect_dissimilar_conductors@1 | DIFFERENT | NOT_LISTED |
| thermocouple_temperature_sensor_seebeck_reference_junction_compensation | thermocouple_measures_temperature_difference | DIFFERENT | DIFFERENT | thermocouple_measures_temperature_difference@2 | DIFFERENT | NOT_LISTED |
| thermocouple_temperature_sensor_seebeck_reference_junction_compensation | thermocouple_reference_junction_compensation | EQUAL | DIFFERENT | thermocouple_reference_junction_compensation@1 | DIFFERENT | NOT_LISTED |
| thermocouple_temperature_sensor_seebeck_reference_junction_compensation | thermocouple_law_of_intermediate_metals | EQUAL | DIFFERENT | thermocouple_law_of_intermediate_metals@1 | DIFFERENT | NOT_LISTED |
| thermocouple_temperature_sensor_seebeck_reference_junction_compensation | thermocouple_law_of_intermediate_temperatures | EQUAL | DIFFERENT | thermocouple_law_of_intermediate_temperatures@1 | DIFFERENT | NOT_LISTED |
| thermocouple_temperature_sensor_seebeck_reference_junction_compensation | thermocouple_nonlinearity_reference_tables_polynomial_conversion | EQUAL | DIFFERENT | thermocouple_nonlinearity_reference_tables_polynomial_conversion@1 | DIFFERENT | NOT_LISTED |
| thermocouple_temperature_sensor_seebeck_reference_junction_compensation | thermocouple_thermowell_installation_dynamic_error | EQUAL | DIFFERENT | thermocouple_thermowell_installation_dynamic_error@1 | DIFFERENT | NOT_LISTED |

## 7. P1-A 종결과 다음 작업

- 구조 집계 및 457/48의 ID·owner·승인/제외 관계 확인 완료. P1-B는 48개 후보의 현재 정본·기존 문장·단문화 문장 및 출처·질문 scope를 비교하여 유지/수정권고/보류/거절을 판정한다. 실제 승인·적용은 P1-C 이후 별도 절차다.
- 위 908개 전체 문장 불일치, 574개 미연결, 120/66개 필드 차이 및 다중 매핑을 신규 전수 수정 큐로 자동 생성하지 않는다. 특히 기존 457 검토를 다시 반복하지 않는다.
- 119 HOLD, D4, 4개 exclusion overlay, 기존 Registry/Ledger, A~E 권한·배점 및 운영 불변. Machine Contract/ontology 관계 계약은 P2-A에서 다룬다. PR #49 Draft, main 병합/배포 없음. 새 문서 SHA의 전체 pytest 및 Actions는 NOT_RUN. Firecrawl 미사용.
