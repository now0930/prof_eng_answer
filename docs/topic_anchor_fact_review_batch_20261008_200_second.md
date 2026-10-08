# Topic Pack Fact Anchor 감사 — 추가 200개

- 감사일: 2026-10-08
- 범위: 9개 Topic Pack의 총 200개 Anchor
- 결과: 확인 134, 적용조건 확인 66, 확정 오류 0, 원문 수정 0
- `적용조건 확인`은 사실 오류 판정이 아니라, 용어·제품별 관행·프로젝트별 수용기준을 표준 요구와 혼동하지 않도록 조건을 확인해야 한다는 뜻이다.
- 기존 저장소에 다수의 사용자 미커밋 변경이 있어 원본 JSON과 생성 bank는 수정하지 않았다.

## 범위 집계

| Topic ID | Anchor 범위 | 합계 | 확인 | 적용조건 확인 |
|---|---:|---:|---:|---:|
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | 22–31 | 10 | 7 | 3 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | 1–10 | 10 | 8 | 2 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | 1–36 | 36 | 26 | 10 |
| `bode_frequency_response_stability_margin_bandwidth` | 1–14 | 14 | 10 | 4 |
| `bubbler_level_measurement_purge_backpressure_diagnostics` | 1–6 | 6 | 2 | 4 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | 1–40 | 40 | 32 | 8 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | 1–35 | 35 | 29 | 6 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | 1–28 | 28 | 16 | 12 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | 1–21 | 21 | 4 | 17 |
| **합계** |  | **200** | **134** | **66** |

## 적용조건 확인 Anchor

- HMI/SOE: `sw03_audit_trail`, `sw03_operator_authority`, `sw03_human_error_prevention`
- 4–20 mA: `acl_active_source_output`, `acl_passive_sink_output` (source/sink 명칭과 카드 결선 정의를 제품 회로도에서 확인)
- 밸브 trim: `control_valve_balanced_unbalanced_scope`, `effective_unbalanced_area`, `residual_effective_area`, `force_reduction_ratio_conditional`, `cage_guided_balanced_plug_structure`, `balance_seal_loading`, `pressure_equalization_transient`, `clean_high_dp_large_size_application`, `dirty_slurry_particulate_limit`, `high_temperature_cryogenic_seal_limit`
- Bode: `multiple_or_missing_crossovers`, `closed_loop_bandwidth`, `margin_transient_response_approximation`, `compensator_and_field_validation`
- Bubbler: `bubbler_pressure_reference`, `bubbler_flow_friction_bias`, `bubbler_failure_diagnosis`, `bubbler_material_process_compatibility`
- Configuration/change: `sw06_moc_trigger_and_scope`, `sw06_risk_based_approval_authority`, `sw06_irreversible_change_forward_recovery`, `sw06_backup_scope_and_consistency`, `sw06_backup_integrity_separation_retention`, `sw06_restore_test_recovery_evidence`, `sw06_disaster_recovery_objectives`, `sw06_migration_strategy_selection`
- Hardware lifecycle: `chl_design_review`, `chl_verification_plan`, `chl_verification_vs_validation`, `chl_environmental_qualification_boundary`, `chl_production_test_coverage`, `chl_change_impact`
- 제어논리: `sw02_transition_guard`, `sw02_voting_logic`, `sw02_shutdown_classes`, `sw02_fail_safe`, `sw02_watchdog`, `sw02_command_arbitration`, `sw02_signal_quality`, `sw02_restart_recovery`, `sw02_scan_edge_memory`, `sw02_debounce_hysteresis`, `sw02_manual_mode_boundary`, `sw02_sw05_boundary`
- 프로젝트 문서·시험: `sw10_scope_project_execution`, `sw10_sw04_boundary`, `sw10_sw02_boundary`, `sw10_sw03_boundary`, `sw10_feasibility`, `sw10_scope_baseline`, `sw10_schedule_dependencies`, `sw10_cost_change_control`, `sw10_control_philosophy`, `sw10_urs`, `sw10_frs`, `sw10_fds`, `sw10_sds`, `sw10_document_hierarchy_traceability`, `sw10_io_list`, `sw10_tag_list`, `sw10_alarm_list`

그 외 Anchor는 일반 원리·정의 또는 조건부/권고 문구가 명시된 사실로 대조했다. 특히 4–20 mA Active/Passive는 업계 용례가 혼용될 수 있어 장치의 source/sink 전기회로를 먼저 확인해야 하고, URS/FRS/FDS/SDS의 상세 문서명·계층은 프로젝트 절차에 따라 달라질 수 있다. FAT/SAT/SIT와 loop-check/commissioning은 표준상 범위를 같은 시험으로 합쳐 해석하지 않았다.

## 공식·기술 근거

- Configuration baseline과 변경통제: ISO 10007은 제품·서비스 lifecycle의 configuration management 지침이며, NIST SP 800-128은 baseline을 공식 합의된 기준으로 정의하고 변경 제안·구현·시험·검토를 관리한다. [ISO 10007:2017](https://www.iso.org/standard/70400.html), [NIST SP 800-128](https://csrc.nist.gov/pubs/sp/800/128/upd1/final)
- 제어시스템 FAT/SAT/SIT와 loop check: ISA-105 자료는 FAT/SAT/SIT와 loop check의 목적·경계를 구분하고, FAT/SAT 문서만으로 현장 loop check나 commissioning을 대체하지 않는다고 안내한다. [ISA-105](https://www.isa.org/standards-and-publications/isa-105-standards)
- 밸브 작동력: Emerson Control Valve Handbook은 unbalance force를 net pressure differential × net unbalance area로 설명하고 balanced valve에도 작은 residual unbalance area가 존재하며 manufacturer data를 사용한다고 명시한다. [Control Valve Handbook](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/products/eccentric-plug-valves/documents/D101881X012.pdf)
- Bode 정의: MIT 자료는 주파수응답 크기의 dB 표현과 gain/phase margin의 교차주파수 기준을 설명한다. 폐루프 bandwidth와 transient response 경향은 적용되는 전달함수/응답형태를 전제한다. [MIT gain/phase margin tutorial](https://web.mit.edu/2.010/www_f00/psets/hw3_dir/tutor3_dir/tut3_g.html), [MIT OCW control lecture](https://ocw.mit.edu/courses/2-004-systems-modeling-and-control-ii-fall-2007/resources/lecture32/)
- 4–20 mA / bubbler: ISA는 2-wire loop-powered 기기가 한 쌍의 선으로 전원과 신호를 공유한다고 설명한다. Yokogawa는 bubbler의 배압이 liquid head에 비례하고 낮은 purge 유량으로 tube 마찰 압력강하 영향을 줄여야 함을 설명한다. [ISA two-wire transmitters](https://www.isa.org/intech-home/2016/january-february/departments/two-wire-flow-transmitters-keep-up-with-technology), [Yokogawa bubbler application note](https://www.yokogawa.com/us/library/resources/application-notes/rotameters-and-bubble-tube-purge-for-level-measurement/)
- 확인 범위는 공개된 표준 요약/기술 안내로 일반 사실을 대조한 것이며, 유료 규격의 모든 조항이나 제조사별 제품 조합에 대한 적합성 인증을 뜻하지 않는다.

## Anchor별 등록부

아래 등록부는 이번 배치의 각 Anchor를 원본 `fact_anchor.json` ID로 추적한다.

| Topic ID | Anchor ID | 판정 |
|---|---|---|
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_time_sync_resolution` | 확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_historian_vs_soe` | 확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_first_out_relation` | 확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_audit_trail` | 적용조건 확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_operator_authority` | 적용조건 확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_human_error_prevention` | 적용조건 확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_data_quality_display` | 확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_abnormal_situation_management` | 확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_sw02_boundary` | 확인 |
| `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management` | `sw03_sw04_sw10_boundary` | 확인 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | `acl_current_loop_principle` | 확인 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | `acl_live_zero_fault_discrimination` | 확인 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | `acl_two_wire_loop_powered` | 확인 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | `acl_active_source_output` | 적용조건 확인 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | `acl_passive_sink_output` | 적용조건 확인 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | `acl_source_sink_compatibility` | 확인 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | `acl_compliance_voltage_load_budget` | 확인 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | `acl_resistor_voltage_measurement` | 확인 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | `acl_calibrator_isolation_workflow` | 확인 |
| `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` | `acl_closed_loop_verification` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `control_valve_balanced_unbalanced_scope` | 적용조건 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `trim_pressure_boundary_terms` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `unbalanced_trim_direct_pressure_loading` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `effective_unbalanced_area` | 적용조건 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `nominal_seat_area_boundary` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `unbalanced_force_equation` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `force_direction_sign_convention` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `balanced_trim_pressure_communication` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `balance_hole_passage_function` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `balanced_trim_residual_force` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `residual_effective_area` | 적용조건 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `ideal_full_balance_boundary` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `force_reduction_ratio_conditional` | 적용조건 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `cage_guided_balanced_plug_structure` | 적용조건 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `balance_seal_function` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `balance_seal_loading` | 적용조건 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `balance_seal_friction` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `breakaway_running_friction_boundary` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `balance_seal_leakage_path` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `seat_leakage_path_boundary` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `pressure_equalization_transient` | 적용조건 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `passage_plugging_dynamic_imbalance` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `flow_direction_geometry_dependency` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `seat_load_shutoff_margin_boundary` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `actuator_sizing_topic1_handoff` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `dynamic_friction_topic3_handoff` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `body_cage_guide_topic4_handoff` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `low_noise_trim_topic9_boundary` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `leakage_packing_topic13_boundary` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `severe_service_material_topic14_boundary` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `clean_high_dp_large_size_application` | 적용조건 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `dirty_slurry_particulate_limit` | 적용조건 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `high_temperature_cryogenic_seal_limit` | 적용조건 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `fluid_compatibility_seal_degradation` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `operating_case_force_matrix` | 확인 |
| `balanced_trim_unbalanced_trim_structure_sealing_applications` | `vendor_cutaway_force_table_crosscheck` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `open_loop_closed_loop_roles` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `log_frequency_and_decibel` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `pole_zero_magnitude_slopes` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `phase_contribution_nonminimum_phase` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `positive_gain_shift` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `gain_phase_crossover_frequencies` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `phase_margin_calculation` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `gain_margin_calculation` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `multiple_or_missing_crossovers` | 적용조건 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `closed_loop_bandwidth` | 적용조건 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `margin_transient_response_approximation` | 적용조건 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `delay_and_nonminimum_phase_limits` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `sensitivity_robustness_noise_tradeoff` | 확인 |
| `bode_frequency_response_stability_margin_bandwidth` | `compensator_and_field_validation` | 적용조건 확인 |
| `bubbler_level_measurement_purge_backpressure_diagnostics` | `bubbler_backpressure_principle` | 확인 |
| `bubbler_level_measurement_purge_backpressure_diagnostics` | `bubbler_pressure_reference` | 적용조건 확인 |
| `bubbler_level_measurement_purge_backpressure_diagnostics` | `bubbler_flow_friction_bias` | 적용조건 확인 |
| `bubbler_level_measurement_purge_backpressure_diagnostics` | `bubbler_flow_monitoring` | 확인 |
| `bubbler_level_measurement_purge_backpressure_diagnostics` | `bubbler_failure_diagnosis` | 적용조건 확인 |
| `bubbler_level_measurement_purge_backpressure_diagnostics` | `bubbler_material_process_compatibility` | 적용조건 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_configuration_item_scope` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_configuration_identification_relationship` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_baseline_approved_reference` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_version_control_status_accounting` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_as_built_consistency` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_moc_trigger_and_scope` | 적용조건 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_change_request_problem_objective` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_impact_analysis_multidisciplinary` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_risk_based_approval_authority` | 적용조건 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_change_implementation_plan` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_pre_change_backup_restore_readiness` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_release_package_content` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_release_control_authorized_artifact` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_risk_based_regression` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_release_acceptance_and_asbuilt_update` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_rollback_preplanned_criteria` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_restore_rollback_distinction` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_irreversible_change_forward_recovery` | 적용조건 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_backup_scope_and_consistency` | 적용조건 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_backup_integrity_separation_retention` | 적용조건 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_restore_test_recovery_evidence` | 적용조건 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_disaster_recovery_objectives` | 적용조건 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_migration_discovery_dependency_inventory` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_compatibility_matrix` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_data_configuration_transformation_validation` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_migration_strategy_selection` | 적용조건 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_parallel_operation_controls` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_cutover_freeze_gonogo` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_post_cutover_stabilization_decommission` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_legacy_system_risk_based_management` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_obsolescence_proactive_process` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_obsolescence_mitigation_options` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_spare_lifecycle_management` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_vendor_lockin_lifecycle_risk` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_license_entitlement_continuity` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_firmware_compatibility_control` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_documentation_training_knowledge_retention` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_emergency_change_retrospective_control` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_sw04_boundary` | 확인 |
| `configuration_change_release_backup_rollback_migration_obsolescence_management` | `sw06_sw09_boundary` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_scope_chain` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_requirement_traceability` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_architecture_partitioning` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_interface_definition` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_power_budget` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_power_protection` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_component_selection_multicriteria` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_derating_rule` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_tolerance_stack_boundary` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_obsolescence_availability` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_thermal_design` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_panel_layout` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_grounding_emc_boundary` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_field_installation_boundary` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_io_selection` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_communication_interface` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_connector_terminal_selection` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_prototype_not_production` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_design_review` | 적용조건 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_verification_plan` | 적용조건 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_verification_vs_validation` | 적용조건 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_prototype_design_verification` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_environmental_qualification_boundary` | 적용조건 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_dfm_dfa` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_bom_configuration` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_incoming_material_control` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_work_instruction_process_control` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_production_test_coverage` | 적용조건 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_eol_test` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_test_fixture_control` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_nonconformance_rework` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_fat_boundary` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_software_lifecycle_boundary` | 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_change_impact` | 적용조건 확인 |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | `chl_release_gate` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_scope_operational_logic` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_sequence_definition` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_state_transition_model` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_transition_guard` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_state_entry_exit_actions` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_permissive_definition` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_interlock_definition` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_trip_definition` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_shutdown_classes` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_cause_effect` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_voting_logic` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_first_out` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_bypass` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_override` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_fail_safe` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_watchdog` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_feedback_confirmation_timeout` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_trip_latch_reset` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_abnormal_transition_prevention` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_command_arbitration` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_signal_quality` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_restart_recovery` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_degraded_mode` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_scan_edge_memory` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_debounce_hysteresis` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_manual_mode_boundary` | 적용조건 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_sw03_boundary` | 확인 |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | `sw02_sw05_boundary` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_scope_project_execution` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_sw04_boundary` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_sw02_boundary` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_sw03_boundary` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_feasibility` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_scope_baseline` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_schedule_dependencies` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_cost_change_control` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_control_philosophy` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_urs` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_frs` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_fds` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_sds` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_document_hierarchy_traceability` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_io_list` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_tag_list` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_alarm_list` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_interlock_list` | 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_cause_effect` | 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_logic_diagram` | 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_test_specification` | 확인 |

## 결론

확정 오류가 없어 원문 수정은 하지 않았다. 기존 작업 트리에 미커밋 변경이 있고, 전체 Pack validation은 현재 6개 관리형 Pack의 사람 승인 상태/승인 해시 불일치로 차단되어 있다. 따라서 승인·해시를 자동 보정하거나 생성 bank를 promote하지 않았다. 당시 진행 메모의 분모 2,073은 후속 전수 대조에서 실제 원본 인벤토리와 불일치한 것으로 확인됐다. 전체 완료 집계는 최종 감사 보고서의 2,068개 기준을 따른다.
