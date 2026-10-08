# Topic Pack Fact Anchor 감사 — 추가 200개

- 감사일: 2026-10-08
- 대상: 프로젝트 FAT/SAT 및 유지보수, 제어밸브 성능·유동·마찰, 밸브 액추에이터 force, 가스 sizing
- 판정: 일반 사실 확인 133, 적용조건/모델 확인 67, 확정 오류 0, 원본 수정 0
- 적용조건 확인은 기술 오류를 뜻하지 않는다. 설계점·표준 equation form·제조사 계수·프로젝트 문서 규약에 좌우되는 부분을 식별했다.
- 미커밋 사용자 변경이 많은 상태여서 원본 Pack을 수정하지 않았다.

## 범위 집계

| Topic ID | 범위 | 개수 | 확인 | 조건 확인 |
|---|---:|---:|---:|---:|
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | 22–34 | 13 | 5 | 8 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | 1–26 | 26 | 14 | 12 |
| `control_valve_authority_rangeability_gain_installed_performance` | 1–28 | 28 | 23 | 5 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | 1–36 | 36 | 24 | 12 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | 1–22 | 22 | 17 | 5 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | 1–24 | 24 | 15 | 9 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | 1–22 | 22 | 13 | 9 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | 1–29 | 29 | 22 | 7 |
| **합계** |  | **200** | **133** | **67** |

## 조건/모델 확인 Anchor

- FAT/SAT: `sw10_fat`, `sw10_fat_limit`, `sw10_sat`, `sw10_fat_sat_relation`, `sw10_loop_test`, `sw10_site_integration_test`, `sw10_commissioning`, `sw10_as_built_handover`
- 유지보수: `maintenance_strategy_corrective_preventive_condition_predictive`, `maintenance_criticality_risk_prioritization`, `maintenance_plan_task_interval_basis`, `failure_coding_rca_bad_actor_feedback`, `calibration_interval_risk_history`, `calibration_as_found_as_left_oot`, `inspection_program_routine_functional_loop`, `deferred_maintenance_risk_control`, `spares_criticality_classification`, `spares_stock_policy_reorder_leadtime`, `spares_obsolescence_substitution_moc`, `kpi_mtbf_definition_boundary`
- Authority/gain: `authority_simple_series_formula`, `authority_system_boundary_definition`, `authority_not_fixed_universal_target`, `valve_process_gain_compensation`, `equal_percentage_compensation_is_conditional`
- Cavitation/flashing: `fl_direction_and_cavitation_susceptibility`, `fl_style_trim_travel_dependency`, `cavitation_inception_development_damage_levels`, `cavitation_damage_mechanism`, `flashing_damage_mechanism`, `cavitation_classification`, `flashing_classification`, `pressure_drop_staging_prevention`, `increase_downstream_pressure_prevention`, `anti_cavitation_trim_not_flashing_cure`, `vendor_crosscheck_liquid_phase_change`, `flashing_service_geometry_location`
- Inherent/installed characteristics: `control_valve_system_resistance_flow_squared_relation`, `control_valve_pump_curve_installed_characteristic_effect`, `control_valve_static_head_installed_characteristic_effect`, `control_valve_application_mapping_is_conditional`, `control_valve_commissioning_characteristic_verification`
- Positioner/dynamics: `oscillation_requires_differential_diagnosis`, `response_time_dead_dynamic_separation`, `small_step_test_control_resolution`, `large_step_test_pneumatic_capacity`, `reversal_test_deadband_hysteresis`, `step_sensitivity_not_resolution_only`, `positioner_gain_speed_stability_tradeoff`, `pneumatic_supply_tubing_spool_capacity`, `volume_booster_flow_capacity_feedback_condition`
- Force/sizing: `control_valve_pressure_force_surface_integration`, `control_valve_unbalance_force_effective_area_approximation`, `control_valve_dynamic_flow_force_momentum_side_load`, `control_valve_breakaway_running_friction_hysteresis`, `control_valve_pneumatic_actuator_force_effective_area`, `control_valve_spring_preload_rate_travel_force`, `control_valve_bench_set_operating_range_difference`, `control_valve_actuator_sizing_worst_case_conditions`, `control_valve_balanced_trim_tradeoff_maintenance`
- Gas sizing: `standard_condition_definition_required`, `gas_property_input_selection`, `compressibility_factor_meaning`, `heat_capacity_ratio_factor`, `valve_pressure_drop_ratio_factor_meaning`, `piping_geometry_factor_gas_service`, `xTP_fitting_adjusted_factor`, `unit_constant_equation_dependency`

## 기술 대조 및 주의점

- FAT/SAT/SIT/loop check는 표준·프로젝트 scope를 따라 분리했다. ISA-105 안내는 FAT/SAT가 loop check와 commissioning을 자동 포함하거나 대신하지 않는다고 명시한다. [ISA-105](https://www.isa.org/standards-and-publications/isa-105-standards)
- 유지보수 데이터·failure taxonomy의 근거는 ISO 14224의 적용 산업(석유·천연가스·석유화학) 범위 안에서 인용하고, 이 표준을 모든 업종의 의무사항으로 일반화하지 않았다. MTBF 추정은 고장 정의, 운전시간, 모델 가정에 의존한다. [ISO 14224](https://www.iso.org/standard/64076.html), [NIST reliability data analysis](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm)
- 밸브의 inherent/installed 특성, authority, balanced-trim residual force와 pressure force는 제조사 설계자료 및 운전점에 달린다. Emerson handbook은 압력 불평형력의 기본형을 `net pressure differential × net unbalance area`로 설명하고 balanced valve에도 잔류 면적이 존재한다고 명시한다. [Emerson Control Valve Handbook](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valve-handbook)
- 액체 cavitation/flashing 구분은 vena-contracta pressure가 vapor pressure 아래로 내려간 뒤 downstream pressure가 회복되는지 여부에 따라 구분했다. choked liquid flow는 일정 조건에서 하류압력 감소에도 유량 증가가 제한되는 현상이지 유량 정지를 뜻하지 않는다. [Valmet liquid flow manual](https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/), [Emerson severe-liquid-flow handbook](https://documentation.emersonprocess.com/intradoc-cgi/groups/public/documents/book/d103540x012.pdf)
- 가스 sizing의 `x`, `xT/xTP`, `Fγ`, `Y`, `FP`, `Z`, flow basis와 unit constant는 ANSI/ISA-75.01.01 / IEC 60534-2-1 계열 equation form과 선택 단위에 종속된다. vendor 계수는 해당 valve/trim의 자료를 사용해야 한다. [Emerson standardized valve sizing](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d351798x012_02.pdf)
- Positioner 진단은 friction, deadband 및 instrument-air 문제를 함께 보아야 한다. positioner가 mechanical backlash, 마찰 또는 actuator force 부족을 물리적으로 제거한다는 뜻으로 해석하지 않았다. [Emerson valve diagnostics](https://www.emerson.com/en/final-control/catalog/products-and-software/valve-software/control-valve-diagnostics)

## Anchor별 등록부

다음 표는 감사대상 200개를 원본 Anchor ID와 1:1로 기록한다.

| Topic ID | Anchor ID | 판정 |
|---|---|---|
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_fat` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_fat_limit` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_sat` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_fat_sat_relation` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_loop_test` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_site_integration_test` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_commissioning` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_performance_test` | 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_acceptance` | 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_punch_list` | 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_as_built_handover` | 적용조건 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_configuration_backup` | 확인 |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | `sw10_change_punch_closure` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `om_asset_register_system_boundary` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `maintenance_strategy_corrective_preventive_condition_predictive` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `maintenance_criticality_risk_prioritization` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `maintenance_plan_task_interval_basis` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `work_order_history_closed_loop` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `failure_coding_rca_bad_actor_feedback` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `calibration_program_traceability` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `calibration_interval_risk_history` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `calibration_as_found_as_left_oot` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `calibration_reference_standard_control` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `inspection_program_routine_functional_loop` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `inspection_findings_defect_priority_closeout` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `deferred_maintenance_risk_control` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `spares_criticality_classification` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `spares_stock_policy_reorder_leadtime` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `spares_preservation_shelf_life_rotation` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `spares_obsolescence_substitution_moc` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `kpi_mtbf_definition_boundary` | 적용조건 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `kpi_mttr_definition_boundary` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `kpi_intrinsic_availability_equation` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `kpi_pm_compliance_backlog_schedule` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `kpi_gaming_single_metric_tradeoff` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `maintenance_data_quality_cmms_taxonomy` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `maintenance_roles_competence_permit_restoration` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `maintenance_configuration_backup_change_handoff` | 확인 |
| `control_system_operations_maintenance_calibration_inspection_spares_kpi` | `om_continuous_improvement_pdca_lifecycle_cost` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `valve_authority_physical_meaning` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `authority_simple_series_formula` | 적용조건 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `authority_system_boundary_definition` | 적용조건 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `pressure_drop_redistribution_with_flow` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `low_authority_installed_characteristic_distortion` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `authority_not_fixed_universal_target` | 적용조건 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `oversizing_low_normal_travel` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `oversizing_reduces_effective_valve_drop` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `oversizing_increases_local_gain_sensitivity` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `inherent_gain_constant_pressure_drop` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `installed_gain_actual_system_slope` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `installed_gain_operating_point_dependency` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `installed_gain_differs_from_inherent_gain` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `process_gain_operating_point_dependency` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `loop_gain_component_product` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `valve_process_gain_compensation` | 적용조건 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `equal_percentage_compensation_is_conditional` | 적용조건 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `gain_variation_affects_control_performance` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `control_range_gain_acceptance_concept` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `rangeability_controllable_cv_ratio` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `rangeability_not_travel_ratio` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `installed_rangeability_flow_ratio` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `installed_rangeability_differs_from_rated` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `process_turndown_distinct_from_rangeability` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `minimum_controllable_flow_limits` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `seat_leakage_not_minimum_control_flow` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `min_normal_max_operating_point_validation` | 확인 |
| `control_valve_authority_rangeability_gain_installed_performance` | `gain_curve_installed_curve_final_verification` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `liquid_pressure_profile_scope` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `absolute_pressure_basis_liquid_phase_change` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `vapor_pressure_operating_temperature` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `thermodynamic_critical_pressure_meaning` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `vena_contracta_minimum_pressure` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `vapor_formation_condition` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `downstream_pressure_recovery` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `pressure_recovery_factor_fl_meaning` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `fl_direction_and_cavitation_susceptibility` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `fl_style_trim_travel_dependency` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `critical_pressure_ratio_factor_ff` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `bare_valve_liquid_choked_limit` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `piping_geometry_factor_fp_liquid` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `combined_recovery_factor_flp` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `fitting_adjusted_liquid_choked_limit` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `effective_liquid_sizing_pressure_drop` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `liquid_choked_flow_capacity_limit` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `liquid_choked_flow_not_zero` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `cavitation_classification` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `flashing_classification` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `cavitation_flashing_commonality` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `cavitation_flashing_difference` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `cavitation_inception_development_damage_levels` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `cavitation_damage_mechanism` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `flashing_damage_mechanism` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `choked_vapor_damage_axes_separated` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `liquid_phase_change_operating_cases` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `increase_downstream_pressure_prevention` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `reduce_liquid_temperature_prevention` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `reduce_total_pressure_drop_prevention` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `pressure_drop_staging_prevention` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `higher_fl_low_recovery_selection` | 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `flashing_service_geometry_location` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `anti_cavitation_trim_not_flashing_cure` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `vendor_crosscheck_liquid_phase_change` | 적용조건 확인 |
| `control_valve_cavitation_flashing_choked_flow_damage_prevention` | `topic9_topic14_handoff` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_inherent_characteristic_definition` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_installed_characteristic_definition` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_inherent_installed_distinction` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_normalized_travel_relative_capacity` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_flow_valve_dp_dependency_boundary` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_linear_characteristic_definition` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_equal_percentage_characteristic_definition` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_equal_percentage_exponential_relation` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_equal_percentage_absolute_increment` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_quick_opening_characteristic_definition` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_inherent_constant_pressure_drop_condition` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_installed_pressure_drop_redistribution` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_system_resistance_flow_squared_relation` | 적용조건 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_pump_curve_installed_characteristic_effect` | 적용조건 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_static_head_installed_characteristic_effect` | 적용조건 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_linear_installed_distortion` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_equal_percentage_partial_compensation` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_characteristic_selection_criteria` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_application_mapping_is_conditional` | 적용조건 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_installed_local_slope_topic_boundary` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_manufacturer_curve_system_model_verification` | 확인 |
| `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` | `control_valve_commissioning_characteristic_verification` | 적용조건 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `final_control_element_variability_path` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `deadband_definition_direction_reversal` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `deadband_not_dead_time` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `backlash_mechanical_clearance` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `hysteresis_direction_dependent_output` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `static_friction_starting_force` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `stiction_stick_then_jump` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `stick_slip_repeated_motion` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `stiction_limit_cycle_path` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `oscillation_requires_differential_diagnosis` | 적용조건 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `response_time_dead_dynamic_separation` | 적용조건 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `opening_closing_response_asymmetry` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `small_step_test_control_resolution` | 적용조건 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `large_step_test_pneumatic_capacity` | 적용조건 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `reversal_test_deadband_hysteresis` | 적용조건 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `step_sensitivity_not_resolution_only` | 적용조건 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `positioner_closed_loop_position_feedback` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `positioner_cannot_remove_mechanical_backlash` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `positioner_cannot_replace_actuator_thrust` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `positioner_gain_speed_stability_tradeoff` | 적용조건 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `pneumatic_supply_tubing_spool_capacity` | 적용조건 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `volume_booster_flow_capacity_feedback_condition` | 적용조건 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `hunting_multicausal_diagnosis` | 확인 |
| `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | `improvement_verify_same_test_and_process_result` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_moving_assembly_free_body_diagram` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_pressure_force_surface_integration` | 적용조건 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_unbalance_force_effective_area_approximation` | 적용조건 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_pressure_tends_to_open_close_direction` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_flow_direction_trim_geometry_dependency` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_stem_area_pressure_force` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_balanced_trim_residual_unbalance` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_dynamic_flow_force_momentum_side_load` | 적용조건 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_packing_friction` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_guide_friction_side_load` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_breakaway_running_friction_hysteresis` | 적용조건 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_friction_opposes_motion_not_actuator` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_seat_load_shutoff_class` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_pneumatic_actuator_force_effective_area` | 적용조건 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_spring_preload_rate_travel_force` | 적용조건 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_bench_set_operating_range_difference` | 적용조건 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_fail_close_force_balance` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_fail_open_force_balance` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_actuator_sizing_worst_case_conditions` | 적용조건 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_rotary_valve_torque_boundary` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_stiction_deadband_diagnostics` | 확인 |
| `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_balanced_trim_tradeoff_maintenance` | 적용조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `compressible_control_valve_sizing_scope` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `flow_basis_standard_actual_mass_distinction` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `standard_condition_definition_required` | 적용조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `absolute_pressure_required` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `absolute_temperature_required` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `pressure_drop_ratio_definition` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `pressure_ratio_direction` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `gas_property_input_selection` | 적용조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `compressibility_factor_meaning` | 적용조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `heat_capacity_ratio_factor` | 적용조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `valve_pressure_drop_ratio_factor_meaning` | 적용조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `xT_valve_style_trim_travel_dependency` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `piping_geometry_factor_gas_service` | 적용조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `xTP_fitting_adjusted_factor` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `no_fitting_reference_condition` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `choked_pressure_ratio_limit` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `sizing_ratio_minimum_selection` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `expansion_factor_physical_meaning` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `expansion_factor_subcritical_relation` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `expansion_factor_bounds` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `subcritical_flow_behavior` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `choked_flow_physical_meaning` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `choked_flow_not_zero_flow` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `choked_flow_downstream_independence` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `standard_volume_formula_structure` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `mass_flow_formula_structure` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `unit_constant_equation_dependency` | 적용조건 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `required_vs_rated_gas_coefficient` | 확인 |
| `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` | `selected_travel_xT_iteration` | 확인 |

## 결론

이번 배치에서는 수식·정의의 확정 오류를 찾지 못했다. 오히려 앵커가 authority, flow regime, vendor factor, measurement basis와 commissioning test scope를 조건부로 표현하고 있어 무조건적 수치/보장을 추가하지 않았다. 당시 진행 메모의 분모 2,073은 후속 전수 대조에서 실제 원본 인벤토리와 불일치한 것으로 확인됐다. 전체 완료 집계는 최종 감사 보고서의 2,068개 기준을 따른다. 전체 release validation은 별도 workflow-managed 승인/hash 게이트에 종속된다.
