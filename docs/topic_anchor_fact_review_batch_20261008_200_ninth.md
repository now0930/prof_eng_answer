# Topic Pack Fact Anchor 감사 — 아홉 번째 200개

- 감사일: 2026-10-08
- 대상: 수동 R·C·L 센서, PID 및 P&ID, 압전센서, PLC/DCS/SCADA, 압력 계측, 루프 구조, 레이더/GWR, 근궤적·Routh, RTD
- 판정: 원리·수식·정의 확인 149, 제품·표준·설치·운전조건 확인 51, 확정 오류 0, 수정 0
- 조건 확인은 사실 오류 판정이 아니라 실제 프로젝트·제품·측정범위에 따라 근거를 지정해야 하는 적용사항이다.

## 범위 집계

| Topic ID | 범위 | 개수 | 확인 | 조건 확인 |
|---|---:|---:|---:|---:|
| `passive_sensor_resistive_capacitive_inductive_transduction` | 2–14 | 13 | 13 | 0 |
| `pid_controller_tuning_sequence_gain_effects` | 1–10 | 10 | 7 | 3 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 1–24 | 24 | 19 | 5 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 1–20 | 20 | 13 | 7 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 1–26 | 26 | 13 | 13 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 1–22 | 22 | 12 | 10 |
| `pressure_transmitter_force_balance_null_detection` | 1–5 | 5 | 5 | 0 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 1–16 | 16 | 14 | 2 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 1–28 | 28 | 19 | 9 |
| `root_locus_stability_gain_design` | 1–14 | 14 | 13 | 1 |
| `routh_hurwitz_stability_criterion_gain_range` | 1–14 | 14 | 13 | 1 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 1–8 | 8 | 8 | 0 |
| **합계** |  | **200** | **149** | **51** |

## 기술 대조 요약

- 수동 센서의 저항·정전용량·인덕턴스와 재료 물성/기하 관계, 스트레인게이지 GF, Wheatstone bridge 및 신호조절 chain을 기본식과 일치 여부로 확인했다.
- PID 이상식 및 P/I/D의 일반적 효과는 통상 모델로 확인했다. 튜닝 순서, PI의 보편성, 현장 제약은 공정·구동기·노이즈에 따라 달라지므로 보편적인 고정 규칙으로 승격하지 않았다.
- P&ID와 PID controller의 의미를 분리하고, 기호·tag·line type·numbering은 적용 표준과 프로젝트 legend에 따르도록 제한한 원문을 확인했다. P&ID가 물리적 layout이나 sequence logic의 상세 대체물이 아니라는 경계도 타당하다.
- 압전센서의 직접/역압전효과, Q=dF, 전하증폭기 Vo≈−Q/Cf와 저주파 한계 및 설치·케이블·온도 영향을 확인했다. 장착·교정·대역은 센서/conditioner/DAQ 모델별 사양을 요구한다.
- PLC/DCS/SCADA 역할 설명과 고가용성 원칙을 대조했다. A=MTBF/(MTBF+MTTR)는 일정 고장·수리율의 repairable steady-state 고유가용도 가정에 한정되며, 이중화 효과는 독립고장만으로 낙관하지 않고 공통원인고장을 별도 반영해야 한다.
- 압력 기준(절대/게이지/차압), Bourdon·diaphragm·piezoresistive 원리, static 측정 가능성, DP static pressure 및 설치오차의 구분을 확인했다. range, overpressure, wetted material, hazardous area, total performance와 calibration acceptance는 실제 사양/환경 검토 항목이다.
- Cascade·ratio·feedforward·override·split-range 설명은 표준 구조와 일치한다. Cascade의 secondary loop에 고정 속도비를 요구하지 않았고, 이상 feedforward 식 −Gd/Gu는 안정성·인과성·properness 및 모델오차가 허용될 때의 목표식이라고 제한했다.
- 펄스 레이더의 왕복거리 D=v_gτ/2, FMCW 비트 주파수 관계, 이상적 거리 분해능 v_g/(2B), 유전율 경계 반사계수 및 GWR/TDR 범위를 확인했다. 반사 에코·설치 성능은 탱크와 제품 조건에 의존하며, 제조사 자료도 foam/turbulence·obstruction 영향과 설치 고려사항을 설명한다 ([Emerson Rosemount 1208C reference manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/doc-rosemount-00809-0200-7062.pdf)).
- 근궤적과 Routh-Hurwitz의 표준 판별식 및 예외처리, 안정성/이득경계와 실제 운전 이득의 구분을 확인했다. RTD Pt100의 0°C 공칭 100Ω, IEC 60751 관계식 기반 설명과 리드선 보상 가정을 확인했다 ([IEC 60751:2022](https://webstore.iec.ch/en/publication/63753)).

## 오류 및 보류

- 이번 200개에서 명백한 기술 오류는 발견되지 않아 원문을 수정하지 않았다.
- P&ID legend, tuning 수치, controller failover/availability target, pressure range·재질·위험지역, radar echo 설정, RTD tolerance class 및 교정 acceptance는 적용 현장/제품 증거 없이 일반값으로 확정할 수 없어 조건 확인으로 남겼다.

## Anchor별 등록부

| Topic ID | 순번 | Anchor ID | 판정 |
|---|---:|---|---|
| `passive_sensor_resistive_capacitive_inductive_transduction` | 2 | `sensor_mechanical_stress_strain_youngs_modulus` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 3 | `sensor_resistive_geometry_conductivity_relation` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 4 | `sensor_resistive_strain_gauge_factor` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 5 | `sensor_resistive_voltage_current_conversion` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 6 | `sensor_capacitive_geometry_permittivity_relation` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 7 | `sensor_capacitive_dynamic_current_readout` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 8 | `sensor_inductive_magnetic_circuit_permeability_relation` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 9 | `sensor_inductive_gap_eddy_current_conductivity` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 10 | `sensor_inductive_voltage_impedance_readout` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 11 | `sensor_material_property_geometry_separation` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 12 | `sensor_rcl_excitation_signal_conditioning` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 13 | `sensor_rcl_sensitivity_linearity_environment` | 확인 |
| `passive_sensor_resistive_capacitive_inductive_transduction` | 14 | `sensor_rcl_calibration_implementation_validation` | 확인 |
| `pid_controller_tuning_sequence_gain_effects` | 1 | `pid_controller_definition` | 확인 |
| `pid_controller_tuning_sequence_gain_effects` | 2 | `pid_time_domain_formula` | 확인 |
| `pid_controller_tuning_sequence_gain_effects` | 3 | `pid_s_domain_formula` | 확인 |
| `pid_controller_tuning_sequence_gain_effects` | 4 | `p_action_effect` | 확인 |
| `pid_controller_tuning_sequence_gain_effects` | 5 | `i_action_effect` | 확인 |
| `pid_controller_tuning_sequence_gain_effects` | 6 | `d_action_effect` | 확인 |
| `pid_controller_tuning_sequence_gain_effects` | 7 | `general_tuning_sequence` | 조건 확인 |
| `pid_controller_tuning_sequence_gain_effects` | 8 | `pi_controller_common_in_process_control` | 조건 확인 |
| `pid_controller_tuning_sequence_gain_effects` | 9 | `pd_controller_exists` | 확인 |
| `pid_controller_tuning_sequence_gain_effects` | 10 | `field_constraints` | 조건 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 1 | `pid_definition_scope` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 2 | `pid_not_pid_controller` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 3 | `pfd_pid_difference` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 4 | `pid_not_physical_layout` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 5 | `equipment_and_piping_representation` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 6 | `valve_function_distinction` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 7 | `instrument_tag_function_letters` | 조건 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 8 | `loop_number_identity` | 조건 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 9 | `instrument_symbol_location_convention` | 조건 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 10 | `signal_line_legend` | 조건 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 11 | `measurement_loop_chain` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 12 | `feedback_control_loop_chain` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 13 | `control_valve_pid_representation` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 14 | `alarm_trip_interlock_boundary` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 15 | `pid_control_narrative_relation` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 16 | `pid_loop_diagram_relation` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 17 | `pid_logic_diagram_relation` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 18 | `pid_instrument_index_io_relation` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 19 | `pid_line_list_spec_relation` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 20 | `legend_project_convention_priority` | 조건 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 21 | `design_review_cross_document_consistency` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 22 | `revision_moc_document_control` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 23 | `field_verification_asbuilt` | 확인 |
| `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` | 24 | `pid_lifecycle_use` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 1 | `piezoelectric_direct_effect_charge_generation` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 2 | `piezoelectric_charge_constant_q_df` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 3 | `piezoelectric_direct_inverse_effect_distinction` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 4 | `piezoelectric_equivalent_circuit_charge_capacitance_leakage` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 5 | `piezoelectric_voltage_charge_capacitance_relation` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 6 | `piezoelectric_static_limit_electrical_time_constant` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 7 | `charge_amplifier_output_feedback_capacitance` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 8 | `charge_amplifier_feedback_resistor_low_frequency_cutoff` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 9 | `piezoelectric_charge_output_iepe_distinction` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 10 | `piezoelectric_charge_voltage_sensitivity_units` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 11 | `piezoelectric_force_sensor_measurement_chain` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 12 | `piezoelectric_pressure_sensor_dynamic_chain` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 13 | `piezoelectric_accelerometer_inertial_force_chain` | 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 14 | `piezoelectric_frequency_band_flat_response_resonance` | 조건 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 15 | `piezoelectric_mounting_stiffness_torque_contact_resonance` | 조건 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 16 | `piezoelectric_cable_triboelectric_insulation_error` | 조건 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 17 | `piezoelectric_temperature_pyroelectric_thermal_shock` | 조건 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 18 | `piezoelectric_cross_axis_base_strain_mass_loading` | 조건 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 19 | `piezoelectric_signal_conditioning_filter_adc_antialias` | 조건 확인 |
| `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` | 20 | `piezoelectric_calibration_traceability_diagnostics` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 1 | `sw01_platform_role_selection` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 2 | `sw01_hierarchical_architecture` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 3 | `sw01_plc_architecture` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 4 | `sw01_dcs_architecture` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 5 | `sw01_scada_pc_role` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 6 | `sw01_remote_io_architecture` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 7 | `sw01_redundancy_scope` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 8 | `sw01_active_standby_architecture` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 9 | `sw01_power_io_server_network_redundancy` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 10 | `sw01_fault_detection_isolation` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 11 | `sw01_state_synchronization` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 12 | `sw01_bumpless_transfer` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 13 | `sw01_failover_criteria` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 14 | `sw01_degraded_mode_local_control` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 15 | `sw01_recovery_resynchronization` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 16 | `sw01_reliability_definition` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 17 | `sw01_maintainability_definition` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 18 | `sw01_availability_definition` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 19 | `sw01_availability_formula` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 20 | `sw01_series_parallel_reliability` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 21 | `sw01_single_point_failure` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 22 | `sw01_common_cause_failure` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 23 | `sw01_independence_diversity_separation` | 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 24 | `sw01_maintenance_online_test` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 25 | `sw01_selection_tradeoff` | 조건 확인 |
| `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability` | 26 | `sw01_acceptance_metrics` | 조건 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 1 | `pressure_reference_abs_gauge_dp` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 2 | `pressure_relation_equations` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 3 | `bourdon_elastic_deformation_principle` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 4 | `bourdon_forms_application` | 조건 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 5 | `bourdon_error_protection` | 조건 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 6 | `diaphragm_deflection_principle` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 7 | `diaphragm_sensor_vs_seal` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 8 | `piezoresistive_principle_bridge` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 9 | `piezoresistive_static_capability` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 10 | `piezoresistive_temperature_compensation` | 조건 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 11 | `dp_transmitter_two_port_principle` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 12 | `dp_static_line_pressure_effect` | 조건 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 13 | `dp_level_boundary` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 14 | `range_turndown_resolution_selection` | 조건 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 15 | `overrange_working_burst_pressure` | 조건 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 16 | `process_media_wetted_material_selection` | 조건 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 17 | `ambient_environment_hazardous_selection` | 조건 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 18 | `accuracy_total_performance_terms` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 19 | `zero_span_drift_calibration` | 조건 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 20 | `impulse_line_installation_error` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 21 | `pulsation_vibration_dynamic_response` | 확인 |
| `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` | 22 | `selection_lifecycle_maintainability` | 조건 확인 |
| `pressure_transmitter_force_balance_null_detection` | 1 | `force_balance_equilibrium` | 확인 |
| `pressure_transmitter_force_balance_null_detection` | 2 | `null_position_error_detection` | 확인 |
| `pressure_transmitter_force_balance_null_detection` | 3 | `pneumatic_force_balance_chain` | 확인 |
| `pressure_transmitter_force_balance_null_detection` | 4 | `electronic_force_balance_chain` | 확인 |
| `pressure_transmitter_force_balance_null_detection` | 5 | `force_balance_tradeoffs` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 1 | `process_loop_signal_chain` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 2 | `single_loop_architecture` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 3 | `cascade_structure` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 4 | `cascade_secondary_faster` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 5 | `cascade_disturbance_condition` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 6 | `ratio_control_structure` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 7 | `ratio_scaling_and_low_flow` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 8 | `feedforward_principle` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 9 | `feedforward_feedback_combination` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 10 | `override_selective_control` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 11 | `override_tracking_antiwindup` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 12 | `split_range_control` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 13 | `split_range_transition_design` | 조건 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 14 | `architecture_selection_criteria` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 15 | `loop_interaction_coordination` | 확인 |
| `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` | 16 | `field_implementation_validation` | 조건 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 1 | `radar_level_system_structure` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 2 | `radar_electromagnetic_wave_reflection` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 3 | `radar_pulse_time_of_flight` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 4 | `radar_pulse_distance_equation` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 5 | `radar_fmcw_linear_frequency_sweep` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 6 | `radar_fmcw_beat_frequency_distance` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 7 | `radar_bandwidth_range_resolution` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 8 | `radar_level_reference_calculation` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 9 | `radar_dielectric_constant_reflection` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 10 | `radar_low_dielectric_echo_margin` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 11 | `radar_antenna_beam_footprint` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 12 | `radar_frequency_antenna_tradeoff` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 13 | `radar_blocking_distance_near_field` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 14 | `radar_false_echo_multiple_reflection` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 15 | `radar_surface_foam_turbulence_slope` | 조건 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 16 | `radar_vapor_pressure_temperature_effect` | 조건 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 17 | `radar_mounting_nozzle_obstruction_error` | 조건 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 18 | `radar_antenna_buildup_condensation` | 조건 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 19 | `radar_echo_mapping_calibration_diagnostics` | 조건 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 20 | `radar_pulse_fmcw_application_selection` | 조건 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 21 | `radar_point_target_equation_scope` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 22 | `radar_echo_polarity_sign_convention` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 23 | `radar_adaptive_threshold_echo_tracking` | 조건 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 24 | `radar_upper_null_zone_overfill_coordination` | 조건 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 25 | `gwr_tdr_guided_wave_principle` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 26 | `gwr_effective_permittivity_propagation_path` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 27 | `gwr_quasi_tem_return_path` | 확인 |
| `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` | 28 | `gwr_interface_and_process_limitations` | 조건 확인 |
| `root_locus_stability_gain_design` | 1 | `closed_loop_pole_gain_relationship` | 확인 |
| `root_locus_stability_gain_design` | 2 | `root_locus_definition` | 확인 |
| `root_locus_stability_gain_design` | 3 | `root_locus_start_end_points` | 확인 |
| `root_locus_stability_gain_design` | 4 | `real_axis_segment_rule` | 확인 |
| `root_locus_stability_gain_design` | 5 | `asymptote_count_and_angles` | 확인 |
| `root_locus_stability_gain_design` | 6 | `asymptote_centroid` | 확인 |
| `root_locus_stability_gain_design` | 7 | `breakaway_break_in_points` | 확인 |
| `root_locus_stability_gain_design` | 8 | `departure_and_arrival_angles` | 확인 |
| `root_locus_stability_gain_design` | 9 | `imaginary_axis_crossing` | 확인 |
| `root_locus_stability_gain_design` | 10 | `gain_from_magnitude_condition` | 확인 |
| `root_locus_stability_gain_design` | 11 | `angle_condition` | 확인 |
| `root_locus_stability_gain_design` | 12 | `dominant_pole_design` | 확인 |
| `root_locus_stability_gain_design` | 13 | `transient_response_mapping` | 확인 |
| `root_locus_stability_gain_design` | 14 | `compensator_design_application` | 조건 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 1 | `asymptotic_stability_open_lhp` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 2 | `first_column_sign_changes_rhp_count` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 3 | `positive_coefficients_not_sufficient` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 4 | `routh_first_two_rows_layout` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 5 | `routh_recursive_row_calculation` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 6 | `zero_first_column_epsilon_limit` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 7 | `all_zero_row_auxiliary_polynomial` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 8 | `imaginary_axis_roots_stability_class` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 9 | `gain_range_first_column_inequalities` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 10 | `gain_boundary_requires_verification` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 11 | `relative_stability_axis_shift` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 12 | `time_delay_requires_approximation_or_frequency_method` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 13 | `routh_does_not_return_exact_pole_locations` | 확인 |
| `routh_hurwitz_stability_criterion_gain_range` | 14 | `field_gain_selection_requires_margin` | 조건 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 1 | `rtd_temperature_measurement_chain` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 2 | `rtd_metal_resistance_temperature_principle` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 3 | `rtd_pt100_reference_resistance_alpha_standard` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 4 | `rtd_callendar_van_dusen_characteristic` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 5 | `rtd_excitation_voltage_measurement` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 6 | `rtd_self_heating_thermal_error` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 7 | `rtd_two_wire_lead_resistance_error` | 확인 |
| `rtd_temperature_sensor_principle_pt100_wiring_compensation` | 8 | `rtd_three_wire_bridge_compensation_assumptions` | 확인 |
