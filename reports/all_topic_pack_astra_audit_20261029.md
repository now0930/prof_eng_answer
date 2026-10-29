# 전체 Topic Pack Astra 1차 감사 등록부 — 2026-10-29

## 범위와 판정

- 대상: 운영 source Topic Pack 89개, Master 89개, Fact Anchor 2,093개.
- 형식: validate-all 및 validate-topic-pack-release --all 통과. audit_topic_pack_atomicity.py 차단 오류 0, 검토 경고 37건.
- 내용: Astra가 두 배치로 Pack 문구를 탐색했으나 배치 감사가 사용량 제한으로 중단되었다. 아래 89개 행의 내용 상태는 모두 미완료다. 구조 PASS를 사실 검증이나 AI 승인으로 해석하지 않는다.
- Master 출처 참조 408건 중 verified 3건, unverified 405건. 이는 출처 참조 상태이며 각 Anchor의 사실 검증 결과와 동일하지 않다. 출처 참조가 없는 Topic도 있다.
- 기존 managed 승인은 그대로 두며, legacy Pack을 Astra 승인으로 소급 전환하지 않는다.

## Astra가 제기한 수정 후보

| Topic | 문제 | 다음 조치 |
| --- | --- | --- |
| flow_measurement_meter_principles_velocity_selection | 차압식 원리·환산 조건 문항의 requirement가 primary element 이름 하나만으로 충족될 수 있다. 물리 사실 오류가 아닌 문항 계약의 과대 인정 위험이다. | 사례 fixture와 허용 점수 라벨을 만든 뒤 requirement를 원리·조건으로 분리하고 Authority gate 검증. |
| control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening | Authority·Rangeability 소유자를 Topic 3으로 표기하지만 실제 canonical 소유 Topic ID와 번호가 어긋날 수 있다. | 번호 대신 control_valve_authority_rangeability_gain_installed_performance ID 사용. |
| instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification | EMI 진단 대 qualification 비교 문항이 내부 Topic ownership boundary Anchor 3개를 필수 요구로 포함한다. | 문항 직접 요구만 필수로 남기는 회귀 fixture 작성. |
| smart_positioner_diagnostics_valve_signature_predictive_maintenance | HART·Fieldbus·작업지시 문항이 내부 Topic 번호 boundary Anchor 2개를 필수 요구로 포함한다. | 동일한 문항 범위 회귀 검증 후 제외 여부 판정. |
| second_order_system_resonance_frequency_response | 유한한 공진 피크의 0<ζ<1/√2와 무감쇠 ζ=0의 특이점을 같은 일반 규칙으로 읽을 수 있다. | 식의 정규화 가정과 경계 조건을 1차 출처로 재검증하고 수정. |

위 항목은 제안이며 아직 source·generated Bank를 수정하지 않았다. 점수에 영향을 줄 수 있는 문항 계약 변경은 정상·부분·오답·경계 fixture와 기존 회귀를 먼저 확보한다. 기술 내용의 단정은 출처 확인 전 보류한다.

## Topic별 상태

형식 PASS는 JSON·참조·generated 계약 검사 결과다. 내용 미완료는 Anchor별 기술 사실·출처·오답 경계의 독립 검증이 끝나지 않았다는 뜻이다.

| # | Topic ID | 기존 승인 방식 | Master 출처 수 | 형식 | 내용 |
| ---: | --- | --- | ---: | --- | --- |
| 1 | analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting | human | 2 | PASS | 미완료 |
| 2 | balanced_trim_unbalanced_trim_structure_sealing_applications | legacy | 7 | PASS | 미완료 |
| 3 | bode_frequency_response_stability_margin_bandwidth | legacy | 0 | PASS | 미완료 |
| 4 | configuration_change_release_backup_rollback_migration_obsolescence_management | legacy | 0 | PASS | 미완료 |
| 5 | control_hardware_lifecycle_panel_architecture_component_selection_production_verification | legacy | 0 | PASS | 미완료 |
| 6 | control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe | legacy | 0 | PASS | 미완료 |
| 7 | control_software_project_engineering_documents_fat_sat_commissioning_acceptance | legacy | 0 | PASS | 미완료 |
| 8 | control_system_operations_maintenance_calibration_inspection_spares_kpi | legacy | 2 | PASS | 미완료 |
| 9 | control_valve_authority_rangeability_gain_installed_performance | legacy | 10 | PASS | 미완료 |
| 10 | control_valve_cavitation_flashing_choked_flow_damage_prevention | legacy | 10 | PASS | 미완료 |
| 11 | control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening | legacy | 4 | PASS | 미완료 |
| 12 | control_valve_deadband_stiction_response_time_positioner_dynamic_performance | legacy | 1 | PASS | 미완료 |
| 13 | control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe | legacy | 15 | PASS | 미완료 |
| 14 | control_valve_gas_sizing_choked_flow_critical_pressure_ratio | legacy | 0 | PASS | 미완료 |
| 15 | control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing | legacy | 0 | PASS | 미완료 |
| 16 | control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim | legacy | 0 | PASS | 미완료 |
| 17 | control_valve_positioner_ip_converter_booster_accessories_calibration | legacy | 21 | PASS | 미완료 |
| 18 | control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions | legacy | 3 | PASS | 미완료 |
| 19 | control_valve_selection_process_pressure_temperature_flow_media_lifecycle | legacy | 0 | PASS | 미완료 |
| 20 | control_valve_severe_service_high_low_flow_temperature_cryogenic_particles | legacy | 0 | PASS | 미완료 |
| 21 | control_valve_sizing_cv_kv_reynolds_liquid_selection | legacy | 2 | PASS | 미완료 |
| 22 | control_valve_types_globe_rotary_body_actuator_selection | legacy | 13 | PASS | 미완료 |
| 23 | differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error | legacy | 2 | PASS | 미완료 |
| 24 | displacer_level_buoyancy_torque_tube_density_interface_calibration | human | 2 | PASS | 미완료 |
| 25 | dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation | human | 0 | PASS | 미완료 |
| 26 | electronics_error_noise_drift_tolerance_aging_power_mitigation | legacy | 0 | PASS | 미완료 |
| 27 | emerging_technology_quantum_computing_instrumentation_control_applications_readiness_limits | legacy | 0 | PASS | 미완료 |
| 28 | feedback_system_closed_loop_sensitivity_steady_state_error | legacy | 4 | PASS | 미완료 |
| 29 | fiber_optic_link_modes_dispersion_loss_otdr_diagnostics | human | 2 | PASS | 미완료 |
| 30 | final_control_element_sil_sis_esd_valve_partial_stroke_test | legacy | 2 | PASS | 미완료 |
| 31 | flow_measurement_meter_principles_velocity_selection | human | 1 | PASS | 미완료 |
| 32 | fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection | human | 0 | PASS | 미완료 |
| 33 | functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh | legacy | 8 | PASS | 미완료 |
| 34 | hazardous_area_explosion_protection_intrinsic_safety_equipment_selection | legacy | 2 | PASS | 미완료 |
| 35 | hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards | legacy | 0 | PASS | 미완료 |
| 36 | hazop_lopa_ipl_risk_reduction_sil_target_allocation | legacy | 0 | PASS | 미완료 |
| 37 | hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture | legacy | 0 | PASS | 미완료 |
| 38 | historian_mes_it_ot_integration_industrial_data_quality_realtime_processing | legacy | 0 | PASS | 미완료 |
| 39 | hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management | legacy | 0 | PASS | 미완료 |
| 40 | humidity_measurement_capacitive_resistive_dew_point_selection_compensation | legacy | 0 | PASS | 미완료 |
| 41 | industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle | legacy | 0 | PASS | 미완료 |
| 42 | industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread | legacy | 4 | PASS | 미완료 |
| 43 | industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience | legacy | 8 | PASS | 미완료 |
| 44 | industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection | legacy | 18 | PASS | 미완료 |
| 45 | instrument_signal_transmission_line_reflection_termination | human | 2 | PASS | 미완료 |
| 46 | instrumentation_control_software_lifecycle_v_model_traceability_verification_validation | legacy | 4 | PASS | 미완료 |
| 47 | instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification | legacy | 2 | PASS | 미완료 |
| 48 | instrumentation_installation_wiring_impulse_tubing_inspection_codes | legacy | 5 | PASS | 미완료 |
| 49 | instrumentation_power_grounding_shielding_ups_ground_loop_emc | legacy | 18 | PASS | 미완료 |
| 50 | instrumentation_production_management_planning_quality_cost_resources | legacy | 0 | PASS | 미완료 |
| 51 | instrumentation_project_management_basic_design_cost_schedule_documents_acceptance | legacy | 12 | PASS | 미완료 |
| 52 | instrumentation_system_design_basis_codes_standards_specification_deviation_management | legacy | 0 | PASS | 미완료 |
| 53 | lead_lag_compensator_phase_margin_steady_state_error | legacy | 13 | PASS | 미완료 |
| 54 | lqr_optimal_state_feedback_riccati_weighting_design | legacy | 0 | PASS | 미완료 |
| 55 | lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error | legacy | 0 | PASS | 미완료 |
| 56 | nyquist_stability_criterion_gain_phase_margin | legacy | 20 | PASS | 미완료 |
| 57 | open_channel_weir_flume_head_discharge_submergence_selection | human | 1 | PASS | 미완료 |
| 58 | optical_laser_photoelectric_noncontact_measurement_tof_triangulation | legacy | 0 | PASS | 미완료 |
| 59 | ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response | legacy | 5 | PASS | 미완료 |
| 60 | passive_sensor_resistive_capacitive_inductive_transduction | legacy | 2 | PASS | 미완료 |
| 61 | physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control | legacy | 8 | PASS | 미완료 |
| 62 | pid_controller_tuning_sequence_gain_effects | legacy | 4 | PASS | 미완료 |
| 63 | pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative | legacy | 9 | PASS | 미완료 |
| 64 | piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration | legacy | 0 | PASS | 미완료 |
| 65 | plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability | legacy | 10 | PASS | 미완료 |
| 66 | power_electronics_converters_motor_drive_control | human | 0 | PASS | 미완료 |
| 67 | pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error | legacy | 16 | PASS | 미완료 |
| 68 | pressure_transmitter_force_balance_null_detection | human | 0 | PASS | 미완료 |
| 69 | process_control_loop_architecture_cascade_ratio_feedforward_override_split_range | legacy | 0 | PASS | 미완료 |
| 70 | radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error | legacy | 6 | PASS | 미완료 |
| 71 | root_locus_stability_gain_design | legacy | 5 | PASS | 미완료 |
| 72 | routh_hurwitz_stability_criterion_gain_range | legacy | 0 | PASS | 미완료 |
| 73 | rtd_temperature_sensor_principle_pt100_wiring_compensation | legacy | 10 | PASS | 미완료 |
| 74 | safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis | legacy | 0 | PASS | 미완료 |
| 75 | second_order_lag_response_by_damping_ratio | legacy | 2 | PASS | 미완료 |
| 76 | second_order_system_modeling_electromechanical_analogy | human | 6 | PASS | 미완료 |
| 77 | second_order_system_resonance_frequency_response | legacy | 11 | PASS | 미완료 |
| 78 | sil_target_determination_risk_reduction_and_lifecycle | legacy | 4 | PASS | 미완료 |
| 79 | sis_sil_safety_software_independence_systematic_failure_verification_validation | legacy | 6 | PASS | 미완료 |
| 80 | smart_positioner_diagnostics_valve_signature_predictive_maintenance | legacy | 3 | PASS | 미완료 |
| 81 | speed_rotation_measurement_encoder_proximity_tachometer_selection_error | legacy | 0 | PASS | 미완료 |
| 82 | state_feedback_reference_tracking_prefilter_integral_action | legacy | 14 | PASS | 미완료 |
| 83 | state_space_controllability_observability_pole_placement | legacy | 33 | PASS | 미완료 |
| 84 | strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error | legacy | 0 | PASS | 미완료 |
| 85 | temperature_measurement_error_heat_transfer | legacy | 5 | PASS | 미완료 |
| 86 | thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization | legacy | 2 | PASS | 미완료 |
| 87 | thermocouple_temperature_sensor_seebeck_reference_junction_compensation | legacy | 26 | PASS | 미완료 |
| 88 | ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error | legacy | 0 | PASS | 미완료 |
| 89 | vibratory_gyroscope_coriolis_angular_rate_sensing | ai | 1 | PASS | 미완료 |

## 수정 이력

- 2026-10-29: 89개 Pack의 형식·통합 검증을 완료하고, Astra의 확정적 발견 5건을 검토 후보로 등록했다. Pack 소스의 일괄 수정·일괄 승인은 하지 않았다.
- 다음 감사에서 Topic별 출처 대조, Anchor별 판정, 질문 범위 및 회귀 증거를 채워 상태를 갱신한다. 출처 부족은 정확성 승인 대신 별도 보류로 기록한다.
