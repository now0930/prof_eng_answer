# Topic Pack Fact Anchor 감사 — 네 번째 200개

- 감사일: 2026-10-08
- 대상: 제어밸브 가스 sizing 잔여분, 정비·소음·공압 부속기기·포지셔너·누설·패키지 선정
- 판정: 일반 원리/정의 확인 89, 적용조건·표준·제조사·프로젝트 자료 확인 111, 확정 오류 0, 원본 수정 0
- “조건 확인”은 사실 오류나 사용자 검토 요청이 아니라, 수치·허용치·실제 적합성은 해당 설비 조건/구매사양/현행 표준/제조사 자료에 따라 정해야 한다는 뜻이다.
- 확정된 오류를 찾지 못했으며, 원본 Fact Anchor는 수정하지 않았다. 미커밋 사용자 변경이 많은 상태를 보존했다.

## 범위 집계

| Topic ID | 범위 | 개수 | 확인 | 조건 확인 |
|---|---:|---:|---:|---:|
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | 30–34 | 5 | 1 | 4 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 1–20 | 20 | 12 | 8 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 1–38 | 38 | 25 | 13 |
| `control_valve_pneumatic_accessories_function_application` | 1–9 | 9 | 4 | 5 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 1–40 | 40 | 25 | 15 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 1–48 | 48 | 18 | 30 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 1–40 | 40 | 4 | 36 |
| **합계** |  | **200** | **89** | **111** |

## 기술 대조 요약

- 밸브 sizing, 가스 choked flow 및 noise는 IEC 60534/ISA-75 계열의 적용 범위와 제조사 계산방법을 구분했다. 가스 choked condition은 흐름이 멈춘다는 뜻이 아니며, sizing 계수·압력 기준·유동 case를 임의의 보편 상수로 치환하면 안 된다. [Emerson Control Valve Handbook](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), [ISA-75 standards](https://www.isa.org/standards-and-publications/isa-standards/isa-75-standards)
- 소음 기본량은 sound power와 관측점 sound pressure를 구분하고, 서로 독립인 source의 dB 합산은 에너지량 기준으로 한다. 실외 SPL 예측, octave spectrum, noise trim 성능 및 직업 노출 한계는 측정 위치·환경·적용 표준·제조사 방법에 의존한다. [ISA-75.17](https://www.isa.org/products/isa-75-17-1989-control-valve-aerodynamic-noise-pre), [ISA-75 noise measurement and prediction committee](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa75-07)
- Volume booster, quick exhaust, lock-up 및 solenoid는 각 공압 경로·포트 구성에서 서로 다른 기능을 한다. 액추에이터의 최종 fail position은 개별 부속기기 이름만으로 결정할 수 없고 package schematic, spring/action, 누설 및 supply condition을 확인해야 한다. [Emerson Control Valve Handbook—Accessories](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), [Fisher VBL Volume Booster](https://www.emerson.com/en/final-control/products/fisher-vbl)
- Positioner는 명령과 실제 travel의 차이를 feedback으로 줄이는 기기이며, I/P converter 자체를 position controller로 혼동하지 않았다. Conventional 4–20 mA/3–15 psi 매핑은 그 range를 채택한 경우에만 적용하고, action·cam·calibration·fail response는 해당 모델/배선/공압도면과 대조해야 한다. [Emerson Control Valve Handbook](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf)
- Seat leakage class는 시험 조건과 허용량을 구분하는 분류이며 external packing/fugitive emission과 동일한 acceptance가 아니다. 특정 class의 허용 누설률, 시험 medium·압력·온도 및 emission qualification은 표준 판본과 구매사양에서 확인한다. [Emerson Control Valve Handbook—seat leakage classifications](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), [Emerson Control Valve Sourcebook](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf)
- 정비·패키지 선정 Anchor는 안전격리, as-found/as-left, 추적성, 요구조건 통합 같은 일반적인 공학 관리원칙으로 확인했다. 특정 작업허가, 치수 공차, 시험 압력/hold time, 재료 호환, 압력등급, 법규, SIL 요구 및 수용기준은 프로젝트/기기별 문서가 있어야 최종 확정 가능하다.

## 오류 및 보류 사항

- 이번 200개에서 문헌/기본 원리와 명백히 모순되는 확정 오류는 발견하지 못했다.
- 조건 확인 항목은 정보가 불충분하다는 이유로 오류로 표시하지 않았다. 해당 항목의 값이나 적합성을 특정 설비에 적용하려면 설비자료·구매사양·공식 표준 판본·제조사 모델 자료가 필요하다.
- 검토 전용/사람 승인 대기 중인 별도 Release Pack 상태는 변경하지 않았다.

## Anchor별 감사 등록부

정확히 원본에서 읽은 200개 Anchor ID를 기록했다. 판정은 해당 Pack 내부 순번 기준이다.

| Topic ID | 순번 | Anchor ID | 판정 |
|---|---:|---|---|
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | 30 | `minimum_normal_maximum_gas_cases` | 조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | 31 | `fail_open_maximum_flow_case` | 조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | 32 | `steam_vapor_property_boundary` | 조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | 33 | `aerodynamic_noise_handoff` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | 34 | `vendor_hand_calculation_crosscheck_gas` | 조건 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 1 | `maintenance_scope_boundary` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 2 | `work_permit_isolation_depressurization` | 조건 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 3 | `as_found_condition_record` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 4 | `symptom_failure_mode_triage` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 5 | `external_cause_elimination` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 6 | `controlled_removal_marking` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 7 | `disassembly_sequence_traceability` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 8 | `cleaning_contamination_control` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 9 | `trim_stem_guide_body_inspection` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 10 | `dimensional_acceptance_criteria` | 조건 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 11 | `repair_replace_lapping_decision` | 조건 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 12 | `packing_gasket_seal_restoration` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 13 | `reassembly_alignment_torque` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 14 | `seat_endpoint_travel_restoration` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 15 | `pressure_boundary_test` | 조건 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 16 | `seat_leakage_test` | 조건 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 17 | `stroke_friction_hysteresis_test` | 조건 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 18 | `fail_action_accessory_function_test` | 조건 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 19 | `root_cause_evidence_handoff` | 확인 |
| `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing` | 20 | `return_to_service_as_left_record` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 1 | `control_valve_noise_scope` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 2 | `process_flow_vs_accessory_noise` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 3 | `source_path_receiver_hierarchy` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 4 | `sound_power_level_definition` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 5 | `sound_pressure_level_definition` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 6 | `decibel_logarithmic_scale` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 7 | `independent_source_logarithmic_sum` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 8 | `identical_source_doubling` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 9 | `pressure_amplitude_doubling` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 10 | `overall_spectrum_octave_distinction` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 11 | `a_weighting_dba_meaning` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 12 | `sound_power_pressure_boundary` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 13 | `aerodynamic_turbulent_jet_noise` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 14 | `aerodynamic_expansion_shock_noise` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 15 | `gas_choked_regime_noise_input` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 16 | `gas_outlet_velocity_mach_geometry` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 17 | `topic7_aerodynamic_noise_handoff` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 18 | `hydrodynamic_turbulence_noise` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 19 | `cavitation_bubble_collapse_noise` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 20 | `flashing_two_phase_noise` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 21 | `topic8_hydrodynamic_noise_handoff` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 22 | `acoustic_power_pipe_radiation_path` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 23 | `pipe_transmission_loss_dependency` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 24 | `external_spl_observation_condition` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 25 | `prediction_standard_vendor_method` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 26 | `multi_hole_jet_division` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 27 | `multi_stage_pressure_ratio_velocity_control` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 28 | `diffuser_pressure_drop_distribution` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 29 | `silencer_insulation_enclosure_path_treatment` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 30 | `valve_size_capacity_velocity_tradeoff` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 31 | `low_noise_trim_capacity_rangeability_tradeoff` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 32 | `plugging_erosion_maintenance_tradeoff` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 33 | `operating_case_noise_matrix` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 34 | `multiple_source_parallel_bypass_combination` | 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 35 | `field_measurement_background_correction` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 36 | `prediction_measurement_gap_diagnosis` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 37 | `occupational_limit_local_standard` | 조건 확인 |
| `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` | 38 | `vendor_crosscheck_noise` | 조건 확인 |
| `control_valve_pneumatic_accessories_function_application` | 1 | `pneumatic_accessory_energy_path` | 확인 |
| `control_valve_pneumatic_accessories_function_application` | 2 | `pneumatic_accessory_filter_regulator_conditioning` | 확인 |
| `control_valve_pneumatic_accessories_function_application` | 3 | `pneumatic_accessory_volume_booster_flow_capacity` | 확인 |
| `control_valve_pneumatic_accessories_function_application` | 4 | `pneumatic_accessory_lockup_conditional_holding` | 조건 확인 |
| `control_valve_pneumatic_accessories_function_application` | 5 | `pneumatic_accessory_quick_exhaust_vent` | 확인 |
| `control_valve_pneumatic_accessories_function_application` | 6 | `pneumatic_accessory_volume_tank_storage_tradeoff` | 조건 확인 |
| `control_valve_pneumatic_accessories_function_application` | 7 | `pneumatic_accessory_solenoid_path_switching` | 조건 확인 |
| `control_valve_pneumatic_accessories_function_application` | 8 | `pneumatic_accessory_supply_capacity_conditions` | 조건 확인 |
| `control_valve_pneumatic_accessories_function_application` | 9 | `pneumatic_accessory_fail_action_configuration_boundary` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 1 | `control_valve_positioner_accessory_scope` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 2 | `command_ip_positioner_actuator_feedback_chain` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 3 | `positioner_travel_feedback_controller` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 4 | `position_error_negative_feedback` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 5 | `pneumatic_positioner_force_balance_mechanism` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 6 | `electropneumatic_positioner_separate_ip_boundary` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 7 | `ip_converter_current_pressure_transduction` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 8 | `normalized_current_command` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 9 | `ip_linear_pressure_mapping` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 10 | `conventional_4_20ma_3_15psi_endpoints` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 11 | `ip_supply_air_dependency` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 12 | `positioner_direct_reverse_action` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 13 | `actuator_action_fail_action_separation` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 14 | `travel_feedback_linkage_cam_alignment` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 15 | `positioner_zero_span_travel_calibration` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 16 | `multipoint_upstroke_downstroke_verification` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 17 | `split_range_local_mapping` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 18 | `volume_booster_flow_capacity_function` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 19 | `booster_pressure_follower_boundary` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 20 | `booster_bypass_hunting_topic3_handoff` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 21 | `filter_regulator_supply_conditioning` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 22 | `lockup_relay_supply_failure_holding` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 23 | `quick_exhaust_rapid_vent_function` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 24 | `solenoid_on_off_pneumatic_switching` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 25 | `volume_tank_energy_storage_response_tradeoff` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 26 | `tubing_output_capacity_pressure_drop` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 27 | `bench_set_calibration_boundary` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 28 | `seat_endpoint_overtravel_mechanical_stop` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 29 | `command_pressure_travel_loop_test` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 30 | `hysteresis_deadband_stiction_topic3_handoff` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 31 | `air_quality_leakage_nozzle_restriction_failure` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 32 | `loss_signal_air_power_failure_response` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 33 | `operating_pressure_case_calibration_validity` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 34 | `maintenance_bypass_manual_operation_boundary` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 35 | `as_found_as_left_traceability` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 36 | `vendor_action_cam_relay_setting_crosscheck` | 조건 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 37 | `smart_diagnostics_topic12_handoff` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 38 | `sis_esd_pst_topic15_handoff` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 39 | `package_workflow_topic16_handoff` | 확인 |
| `control_valve_positioner_ip_converter_booster_accessories_calibration` | 40 | `final_signal_pressure_travel_fail_action_verification` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 1 | `internal_external_leakage_boundary` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 2 | `shutoff_class_purpose_scope` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 3 | `class_test_condition_dependency` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 4 | `shop_test_field_service_boundary` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 5 | `soft_metal_seat_tradeoff` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 6 | `single_double_seat_leakage_paths` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 7 | `balanced_trim_additional_leakage_path` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 8 | `seat_contact_geometry` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 9 | `seat_load_contact_stress_relation` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 10 | `insufficient_seat_load_leakage` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 11 | `excessive_seat_load_damage` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 12 | `pressure_direction_sealing` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 13 | `gas_liquid_test_medium_difference` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 14 | `test_pressure_temperature_duration_stabilization` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 15 | `volumetric_mass_bubble_basis` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 16 | `size_normalization_basis` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 17 | `ideal_gas_reference_conversion` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 18 | `bubble_count_conversion` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 19 | `seat_damage_erosion_wire_drawing` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 20 | `cavitation_flashing_damage_handoff` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 21 | `foreign_material_contamination` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 22 | `thermal_distortion_hot_leakage` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 23 | `misalignment_stem_guide_wear` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 24 | `surface_finish_lapping_hardness_coating` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 25 | `special_service_sealing_boundary` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 26 | `stem_shaft_packing_leakage_paths` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 27 | `packing_material_ring_arrangement` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 28 | `gland_geometry_compression` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 29 | `packing_leakage_friction_tradeoff` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 30 | `packing_consolidation_relaxation` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 31 | `live_loaded_packing_function` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 32 | `bellows_backup_packing_boundary` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 33 | `low_emission_qualification_field_boundary` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 34 | `fugitive_emission_source_monitoring` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 35 | `concentration_mass_emission_boundary` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 36 | `screening_bagging_quantification_methods` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 37 | `packing_adjustment_replacement_inspection` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 38 | `as_found_as_left_leakage` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 39 | `seat_packing_acceptance_separation` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 40 | `orientation_thermal_cycle_history` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 41 | `specification_test_lifecycle_workflow` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 42 | `measurement_calibration_detection_uncertainty` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 43 | `false_pass_false_fail_background` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 44 | `standard_edition_exact_citation` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 45 | `vendor_purchase_spec_alignment` | 조건 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 46 | `topic1_topic3_topic10_boundary` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 47 | `topic11_topic12_topic14_boundary` | 확인 |
| `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | 48 | `topic15_topic16_standard_boundary` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 1 | `selection_process_ownership` | 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 2 | `governing_document_hierarchy` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 3 | `process_design_basis_traceability` | 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 4 | `tag_service_boundary` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 5 | `stakeholder_requirement_integration` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 6 | `requirement_classification_mandatory_preferred` | 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 7 | `operating_case_matrix` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 8 | `minimum_normal_maximum_cases` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 9 | `startup_shutdown_upset_cleaning_cases` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 10 | `pressure_reference_consistency` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 11 | `temperature_envelope_and_thermal_transient` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 12 | `flow_basis_and_uncertainty` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 13 | `fluid_phase_composition_properties` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 14 | `solids_fouling_corrosion_contaminant` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 15 | `control_objective_and_loop_dynamics` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 16 | `rangeability_turndown_travel_distribution` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 17 | `shutoff_leakage_fail_action` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 18 | `safety_environmental_regulatory_requirements` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 19 | `response_time_and_availability_requirement` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 20 | `specialist_calculation_handoff` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 21 | `liquid_gas_sizing_cross_check` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 22 | `authority_installed_characteristic_cross_check` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 23 | `cavitation_flashing_noise_velocity_cross_check` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 24 | `severe_service_and_material_cross_check` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 25 | `final_element_sis_esd_cross_check` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 26 | `selection_matrix_tradeoff` | 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 27 | `uncertainty_margin_and_double_margin` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 28 | `valve_body_flow_path_selection` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 29 | `trim_characteristic_and_flow_direction` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 30 | `pressure_temperature_rating_and_class` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 31 | `material_compatibility_and_corrosion` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 32 | `seat_packing_gasket_emissions` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 33 | `actuator_thrust_torque_supply_minimum` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 34 | `fail_action_spring_and_stored_energy` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 35 | `positioner_solenoid_booster_accessory_package` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 36 | `installation_orientation_piping_load_accessibility` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 37 | `datasheet_completeness_and_units` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 38 | `requisition_scope_and_guarantees` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 39 | `vendor_bid_technical_comparison` | 조건 확인 |
| `control_valve_selection_process_pressure_temperature_flow_media_lifecycle` | 40 | `deviation_exception_risk_register` | 조건 확인 |
