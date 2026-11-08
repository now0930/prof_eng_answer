# 기술사 채점 Fact의 제외·범위제한·중복통합 후보 (2026-11-01)

## 적용 기준과 주의사항

- Registry의 인용 근거가 있는 사실이라도 **일반산업 필수 채점 Fact가 아닌 경우** 분리한다. 제품·기관 사례가 진실이라는 것과 보편적인 기술사 정답 요건은 다르다.
- **이는 수정 제안 명세**이며 이 문서만으로 실제 승인/삭제가 이루어졌다고 주장하지 않는다. Source Topic Pack·각 질문의 요구·Logic Check·Rubric·Fixture·검증 CLI·회귀 테스트가 준비된 후에만 변경한다.
- 현재 Queue 1,290개의 A~K 최신 판정에서 우선 검토 대상 **276건**: 일반 채점 비핵심 190; 규격/관할 한정 66; 문구 수정 3; 중복 통합 17. 다음 표는 독립적 사실 원문인증을 뜻하지 않는다.

| Fact ID | 우선 조치 | 최근 검토 상태 | 근거 검토 기록 |
|---|---|---|---|
| `aerodynamic_noise_prediction_uses_geometry_and_service_case_inputs` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `bare_valve_liquid_choked_pressure_drop_limit` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_fp_accounts_for_directly_attached_fittings` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_fr_depends_on_reynolds_and_valve_style_inputs` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_gas_choked_pressure_ratio_limit_uses_specific_heat_factor_and_xt` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_gas_mass_flow_density_equation_structure` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_gas_sizing_no_attached_fittings_sets_fp_one_and_xtp_equal_xt` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_gas_sizing_y_bounds_are_one_to_two_thirds_at_choke` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_gas_sizing_y_expansion_factor_subcritical_relation` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_gas_standard_volume_equation_structure_uses_selected_gas_property_basis` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_leakage_class_uses_class_specific_normalization_basis` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `control_valve_leakage_requirements_cite_applicable_standard_edition` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `control_valve_liquid_turbulence_can_generate_hydrodynamic_noise` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `control_valve_noise_prediction_method_and_reference_condition_must_be_identified` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `control_valve_reynolds_equation_uses_style_and_passage_modifiers` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_selection_fr_below_one_increases_required_cv` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_sizing_uses_valve_specific_reynolds_equation` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_xt_is_bare_valve_choked_pressure_drop_ratio_parameter` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_xtp_adjusts_choked_pressure_drop_ratio_for_attached_fittings` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `epa_method_21_type_ii_ambient_background_comparison` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `epa_method_21_voc_leak_screening_instrument_performance` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fci_70_2_defined_test_conditions_seat_leakage_benchmark` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fci_70_2_seat_leakage_results_are_class_medium_and_method_specific` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_fl_is_rated_liquid_pressure_recovery_factor` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `fitting_adjusted_liquid_choked_pressure_drop_limit` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `flp_combines_valve_and_attached_fitting_recovery` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `fp_corrects_attached_piping_fitting_effect` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `gas_attached_fittings_modify_fp_and_choked_ratio_factor` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `gas_choked_limit_caps_sizing_ratio_and_expansion_factor` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `gas_expansion_factor_accounts_for_compressible_expansion` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `gas_pressure_drop_ratio_uses_upstream_absolute_pressure` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `gas_specific_heat_factor_is_gamma_over_1_4` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `hazardous_area_design_competence_considers_suitability_risk_and_function` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `hazardous_ex_e_protection_levels_have_distinct_fault_assumptions` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `iec60534_9_reproducible_configuration_reporting_and_application_kpis` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `isa_binary_logic_diagram_documents_interlock_and_sequence_logic` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `isa_instrument_tag_letters_and_number_encode_identity` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `isa95_level3_level4_exchange_scope_is_implementation_specific` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `isa95_level3_level4_functional_boundary_and_information_exchange` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `iso14224_equipment_id_function_location_and_reliability_taxonomy` | 규격/관할 한정 | `STANDARD_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `iso14224_failure_data_categories_and_site_specific_rca_boundary` | 규격/관할 한정 | `STANDARD_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `iso14224_maintenance_data_covers_actions_resources_consequences_and_downtime` | 규격/관할 한정 | `STANDARD_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `iso14224_maintenance_plan_structured_tasks_activities_procedures_resources_duration` | 규격/관할 한정 | `STANDARD_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `iso14224_mttr_repair_vs_mttres_restoration_boundary` | 규격/관할 한정 | `STANDARD_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `iso14224_reliability_maintenance_data_quality_and_standard_format` | 규격/관할 한정 | `STANDARD_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `iso55001_system_continual_improvement_value_and_decision_balance` | 규격/관할 한정 | `STANDARD_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `liquid_critical_pressure_ratio_factor_ff_depends_on_pv_pc` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `liquid_sizing_uses_actual_or_choked_limit_whichever_is_lower` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `liquid_valve_pc_is_thermodynamic_critical_pressure` | 규격/관할 한정 | `STANDARD_FORMULA` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `mcdc_deactivated_code_is_configuration_scoped_inactive_code` | 규격/관할 한정 | `STANDARD_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_f.md) |
| `mcdc_full_criterion_includes_entry_exit_and_independence_obligations` | 규격/관할 한정 | `STANDARD_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_f.md) |
| `misra_guidelines_are_coding_rules_not_dynamic_unit_test_tools` | 규격/관할 한정 | `STANDARD_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_f.md) |
| `occupational_noise_criteria_are_jurisdiction_and_duration_scoped` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `osha_psm_mechanical_integrity_deficiency_correction_scope` | 규격/관할 한정 | `REGULATION_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `osha_psm_operating_procedure_currency_and_training_records` | 규격/관할 한정 | `REGULATION_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `osha_psm_scoped_management_of_change_requirements` | 규격/관할 한정 | `REGULATION_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `osha_scoped_hazardous_energy_control_and_psm_maintenance_work_practices` | 규격/관할 한정 | `REGULATION_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `pid_instrument_symbol_conveys_accessibility_per_convention` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `pid_symbol_interpretation_uses_standard_and_project_legend` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `production_equipment_resource_availability_and_maintenance_scope_boundary` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `production_finite_capacity_schedule_respects_resource_and_sequence_constraints` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `production_management_scope_follows_iso22400_mom_activities_and_local_goals` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `production_schedule_kpi_defines_freeze_period_and_completion_basis` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `spc_control_chart_signals_are_distinct_from_specification_and_customer_disposition` | 규격/관할 한정 | `STANDARD_EDITION_CLAUSE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `special_service_valve_sealing_uses_service_specific_test_and_design_scope` | 규격/관할 한정 | `SCOPED_STANDARD_OR_REGULATION` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `sw06_moc_is_scoped_to_psm_covered_changes_and_ot_guidance` | 규격/관할 한정 | `REGULATION_SCOPE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `control_valve_min_normal_max_flow_are_evaluated_separately` | 문구 수정 | `CORRECT_REQUIRED` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `cryogenic_control_valve_extension_bonnet_protects_packing_from_cold_zone` | 문구 수정 | `NARROW_OR_CORRECT` | [보고서](fact_anchor_chat_review_20261101.md) |
| `liquid_valve_sizing_requires_process_fluid_and_operating_case_inputs` | 문구 수정 | `CORRECT_REQUIRED` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `actuator_online_monitoring_detects_selected_faults` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_f.md) |
| `asset_administration_shell_standardizes_asset_identification_and_submodel_structure_without_guaranteeing_completeness` | 일반 채점 비핵심 | `SPECIALIST_SCOPE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `aveva_historian_history_trend_event_compression_query_functions` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `balanced_plug_seal_is_secondary_pressure_boundary` | 일반 채점 비핵심 | `MODEL_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `balanced_trim_balance_hole_blockage_impairs_pressure_communication` | 일반 채점 비핵심 | `MODEL_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `bryson_rule_is_initial_normalization_heuristic` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_e.md) |
| `butterfly_valve_compact_large_size_and_trim_dependent_control_scope` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `cage_guided_balanced_trim_functions` | 일반 채점 비핵심 | `MODEL_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `cavitation_onset_and_damage_coefficients_are_valve_specific` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `cavitation_trim_effectiveness_can_change_with_travel_and_geometry` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `collaborative_robot_safety_is_application_specific` | 일반 채점 비핵심 | `SPECIALIST_SCOPE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `configured_lock_in_last_assembly_can_retain_actuator_pressure_on_supply_loss` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `control_range_is_declared_installed_gain_acceptance_interval` | 일반 채점 비핵심 | `VENDOR_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `control_valve_end_connection_maintenance_and_service_tradeoffs` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `control_valve_flashing_damage_mitigation_is_application_specific` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_selection_repeats_after_selected_style_fl_update` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_sliding_stem_rotary_motion_classification` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `digital_thread_links_traceable_information_across_product_lifecycle` | 일반 채점 비핵심 | `SPECIALIST_SCOPE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `digital_twin_fidelity_is_fit_for_purpose_and_validation_scope_dependent` | 일반 채점 비핵심 | `SPECIALIST_SCOPE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `dod_sd22_dmsms_resolution_categories_and_complexity` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `dod_sd22_software_license_life_of_need_examples` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `double_ported_globe_capacity_force_balance_and_seat_leakage_limit` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `dp_level_volume_output_requires_geometry_mapping` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `dp_level_wet_leg_zero_elevation` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `dp_remote_seal_response_and_fill_fluid_selection_factors` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `dvc6200_sis_relay_capacity_and_tubing_requirements_are_variant_specific` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `dvc6200_sis_tuning_response_adjustment_is_assembly_specific` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `emerson_gas_pilot_pressure_spike_snubber_dampens_transients` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `encoder_speed_feedback_selection_must_match_receiver_limits` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `erp_enterprise_business_planning_and_resource_domain_distinct_from_mes_execution` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `ethercat_datagram_processing_esi_mapping_and_configured_topology` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `ethernet_ip_uses_cip_objects_profiles_and_scanner_adapter_connections` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `extension_bonnet_temperature_length_and_orientation_are_application_specific` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fieldvue_as_left_signature_can_become_product_specific_comparison_baseline` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fieldvue_in_service_monitoring_and_offline_signature_are_distinct` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_2625_volume_booster_one_to_one_pressure_following` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_3570_action_change_bypass_isolation_and_recheck` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_3570_positioner_adjustment_conditions` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_3570_positioner_spring_and_relay_adjustments` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_3582_cam_and_linkage_alignment_affect_calibration_starting_travel` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_3582_direct_reverse_action_describes_input_to_actuator_pressure_direction` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_3582_supply_medium_debris_and_connection_leak_controls` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_3582_zero_and_travel_adjustments_interact_and_require_low_end_recheck` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_3582i_combines_electropneumatic_converter_with_pneumatic_positioner` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_3582i_signal_conversion_positioning_and_stem_feedback_chain` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_585c_fail_close_spring_must_provide_required_seat_force` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_585c_fail_open_spring_must_complete_required_opening_travel` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_67cf_filter_regulator_filters_particles_separates_condensate_and_reduces_pressure` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_685sr_sizing_requires_available_thrust_to_meet_valve_load` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_actuator_sizing_sums_loads_for_service_case` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_balanced_trim_reduces_static_unbalance_not_all_loads` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_balanced_trim_residual_load_seal_friction_shutoff_and_balance_hole_maintenance` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_bellows_bonnet_seals_stem_and_has_pressure_temperature_cycle_bounds` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_bench_set_is_actuator_spring_adjustment_reference` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_boiler_feedwater_plug_tip_erosion_reduces_shutoff` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_catalog_12_fci_70_2_factory_test_condition_limits` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_eh_eha_thermal_cycle_seat_ring_distortion_control` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_enviro_seal_live_loading_sustains_packing_load_and_reduces_adjustment` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_force_equations_include_stem_pressure_area` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_handbook_defines_hunting_and_positioner_instability_symptom` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_handbook_reports_direction_specific_valve_response_time` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_hp_hpa_cseal_overtravel_can_reduce_seat_load_and_damage_trim` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_multiport_selector_well_test_routing_scope` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_positioner_feedback_and_actuator_linkage_lost_motion_are_distinct` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_positioner_ip_booster_package_checks_are_model_specific` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_pressure_direction_depends_on_flow_and_plug_action` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_pressure_tends_direction_is_configuration_specific` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_rotary_actuator_selection_uses_valve_torque` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_seat_load_is_separate_actuator_force_requirement` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_sliding_stem_actuator_force_components` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_sliding_stem_packing_friction_and_selection_factors` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_sliding_stem_packing_system_selection_and_arrangements` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_sourcebook_rotary_packing_motion_comparison` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `fisher_unbalance_force_pressure_area_equations` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_v500_eccentric_plug_cam_action_and_erosive_service_scope` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `fisher_vbl_booster_bypass_separates_large_and_small_signal_operation` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `foundation_fieldbus_function_block_support_and_host_compatibility_are_feature_specific` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `foundation_fieldbus_function_blocks_device_management_and_segment_engineering` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `gao_jfmip_parallel_operation_transition_test_and_costs` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `garlock_packing_consolidation_can_reduce_gland_load_and_needs_conditioned_adjustment` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `garlock_packing_installation_controls_compression_and_follower_alignment` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `garlock_stem_runout_and_misalignment_create_uneven_packing_wear` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `garlock_stem_surface_damage_increases_packing_leakage_and_wear` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `gas_required_cv_iteration_uses_selected_product_xt` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `gas_sizing_outputs_feed_aerodynamic_noise_review` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `gate_model_applies_quantum_operations_before_classical_measurement` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `globe_valve_guide_method_alignment_side_load_and_wear_scope` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `gwr_interface_distance_accounts_for_upper_layer_delay` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `gwr_interface_measurement_has_process_and_probe_limits` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `hhs_data_conversion_cutover_preparation_and_backup_example` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `hhs_data_conversion_execution_mode_planning_choices` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `hhs_data_conversion_mapping_test_and_reconciliation_practice` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `hhs_data_conversion_post_conversion_validation_scope` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `hse_offshore_sis_maintenance_test_deferral_risk_management_guidance` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `hsr_duplicates_frames_in_both_ring_directions_and_nodes_forward_and_discard` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `impulse_line_freezing_plugs_and_isolates_transmitter` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `industrial_robot_system_and_application_boundaries_are_distinct` | 일반 채점 비핵심 | `SPECIALIST_SCOPE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `ipgse_frequency_and_event_timing_are_diagnostic_clues_not_causation` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `ipgse_ground_loop_mitigation_uses_signal_path_not_pe_lifting` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `ipgse_noise_diagnosis_uses_spectrum_setup_and_component_isolation` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `ipgse_noise_mitigation_preserves_before_after_measurement_evidence` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `ipgse_power_supply_redundancy_is_limited_by_shared_upstream_paths` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `ipgse_shield_termination_depends_on_coupling_and_bonding_context` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `isa100_11a_wireless_roles_and_host_application_integration` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `isa95_cross_system_equipment_and_material_identifiers_need_mapping_and_versioned_recipe_context` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `isa95_level_three_mom_supports_production_operations_execution_and_tracking` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `isa95_models_enterprise_control_interfaces_not_single_protocol` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `lvdt_excitation_carrier_bandwidth_and_device_limits` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `maintenance_reliability_kpi_catalog_and_definitions_are_scoped` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `markov_state_space_growth_can_increase_analysis_burden_without_universal_growth_rate` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_f.md) |
| `masoneilan_overtravel_correction_and_fisher_dvc2000_seat_load_cutoff` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `mlops_integrates_versioned_ml_build_test_deploy_and_monitor_workflows` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `model_version_lineage_requires_explicit_run_data_and_deployment_metadata` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nasa_lesson_limited_shelf_life_spares_identify_replace_expired` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `nasa_npr_4100_1f_shelf_life_type_and_test_controls` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `nist_80082r3_dmz_prevents_direct_corporate_ot_traffic` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_firewall_adjacent_authorized_communications` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_ot_acl_rbac_abac_access_control_models` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_ot_asset_inventory_documentation_scope` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_ot_incident_response_plan_contents` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_ot_log_event_identity_source_outcome_fields` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_ot_remote_session_account_and_monitoring_controls` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_ot_removable_media_policy_handling_and_disposal` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_ot_risk_management_boundary_asset_dataflow_tasks` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_ot_software_firmware_authenticity_checks` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_ot_supplier_authenticity_and_review` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_ot_tabletop_dr_recovery_testing_and_lessons` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `nist_80082r3_unidirectional_gateway_hardware_one_way_ot_boundary` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `opc_ua_information_models_encode_object_types_and_relationship_semantics` | 일반 채점 비핵심 | `SPECIALIST_SCOPE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `opcua_namespaces_and_node_ids_scope_identifiers_browse_names_are_not_unique_ids` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `opcua_status_change_datachange_trigger` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `ot_zone_conduit_grouping_and_boundary_enforcement` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `pid_compact_v3_implementation_behavior_is_platform_specific` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `port_guided_plug_alignment_and_high_pressure_drop_vibration_condition` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `profibus_pa_profile_bus_power_dp_pa_segment_design` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `profinet_io_cyclic_acyclic_diagnostics_and_gsdml_device_model` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_classical_input_state_preparation_can_limit_algorithmic_advantage` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_computing_uses_qubit_states_for_problem_specific_computation` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_entanglement_creates_nonclassical_correlations_without_faster_than_light_signaling` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_error_mitigation_and_error_correction_are_distinct_methods` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_hardware_noise_includes_gate_readout_and_decoherence_effects` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_hybrid_workflow_assigns_classical_and_quantum_subtasks` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_measurement_returns_probability_weighted_classical_outcomes` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_measurement_shots_and_classical_aggregation_belong_in_end_to_end_accuracy_and_latency` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_sensing_is_measurement_and_quantum_computing_is_computation` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_superposition_is_coherent_state_not_classical_random_mixture` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `quantum_workload_capability_depends_on_quality_connectivity_depth_and_logical_resources` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `qubit_state_uses_complex_amplitudes_and_measurement_yields_classical_bit` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `radar_interface_field_phase_and_displayed_echo_polarity_are_distinct` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `radar_level_from_empty_distance_minus_measured_distance` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `radar_minimum_distance_blocking_zone_model_specific` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `radar_nozzle_clearance_and_surface_alignment` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `radar_threshold_window_false_echo_and_history_tracking` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `relative_phase_controls_constructive_and_destructive_quantum_interference` | 일반 채점 비핵심 | `SPECIALIST_OPTIONAL_NOT_GENERIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `robot_localization_estimates_pose_from_sensors_with_method_dependent_uncertainty` | 일반 채점 비핵심 | `SPECIALIST_SCOPE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `rosemount_1159_capillary_length_increases_response_time` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `rosemount_1159_static_head_zero_error_and_rezero` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `rosemount_2051_three_valve_zero_check_isolation_side_sequence` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `rosemount_2051_three_valve_zero_check_return_sequence` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `rosemount_3051shp_mwp_misvalving_output_shift` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `rosemount_3100_ultrasonic_setup_and_echo_diagnostics` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `rosemount_5408_upper_null_zone_suppresses_measurement_and_api2350_cat3_independence` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `rosemount_balanced_vs_tuned_remote_seal_temperature_effects` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `rosemount_impulse_piping_pressure_transfer_error_modes` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `rosemount_remote_seal_temperature_effect_mechanisms_scoped` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `rtd_channel_fault_checks_are_topology_and_device_dependent` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_b.md) |
| `rtd_transmitter_connection_signal_conditioning` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_b.md) |
| `segmented_v_notch_ball_capacity_characteristic_and_seal_scope` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `siemens_safety_integrated_fblock_reuse_requires_signature_and_version_recheck` | 일반 채점 비핵심 | `VENDOR_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_f.md) |
| `sif_final_element_package_can_include_actuator_solenoid_and_support` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_f.md) |
| `simulation_credibility_is_limited_to_intended_use_and_validated_domain` | 일반 채점 비핵심 | `SPECIALIST_SCOPE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `state_estimator_inference_is_limited_by_model_and_sensor_observability` | 일반 채점 비핵심 | `SPECIALIST_SCOPE_PENDING` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `stream_event_time_watermark_and_lateness_handling` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `sw02_bypassability_is_configured_and_selected_with_role_controls_in_plantpax` | 일반 채점 비핵심 | `MODEL_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `sw02_first_out_simultaneous_scan_behavior_is_vendor_specific` | 일반 채점 비핵심 | `MODEL_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `sw02_sfc_action_lifecycle_and_output_retention` | 일반 채점 비핵심 | `MODEL_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `sw02_trip_response_preempts_sequence_in_documented_safety_example` | 일반 채점 비핵심 | `MODEL_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `sw06_change_request_records_scope_priority_impact_and_closure` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `sw06_release_package_is_identified_approved_and_auditable` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `sw06_software_release_delivery_records_and_as_built` | 일반 채점 비핵심 | `AGENCY_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `sw06_vendor_lockin_lifecycle_risk` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `thermocouple_junction_construction_response_isolation` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_b.md) |
| `thermocouple_loop_diagnostics_are_device_and_symptom_specific` | 일반 채점 비핵심 | `SUPPLEMENT_ONLY` | [보고서](fact_anchor_chat_review_20261101_batch_b.md) |
| `ultrasonic_application_selection_is_model_and_path_condition_specific` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `ultrasonic_installation_alignment_nozzle_and_obstruction_controls` | 일반 채점 비핵심 | `VENDOR_REFERENCE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_j.md) |
| `valmet_control_valve_breakaway_friction_decreases_after_motion_starts` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `valve_erosive_service_trim_material_options_are_construction_specific` | 일반 채점 비핵심 | `VENDOR_EXAMPLE_NONCORE` | [보고서](fact_anchor_chat_review_20261101_batch_k.md) |
| `vendor_product_lifecycle_status_and_ot_change_control_for_obsolescence` | 일반 채점 비핵심 | `VENDOR_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `vendor_product_version_scoped_compatibility_checks_for_migration` | 일반 채점 비핵심 | `VENDOR_EXAMPLE` | [보고서](fact_anchor_chat_review_20261101_batch_d.md) |
| `wirelesshart_mesh_gateway_network_manager_and_device_join_architecture` | 일반 채점 비핵심 | `SOURCE_OR_PROTOCOL_SPECIFIC` | [보고서](fact_anchor_chat_review_20261101_batch_i.md) |
| `backpressure_reduces_vena_contracta_cavitation_risk_conditionally` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `balanced_trim_assessment_uses_residual_unbalance_area_seat_load_and_application` | 중복 통합 | `CONSOLIDATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `balanced_trim_pressure_communication_path` | 중복 통합 | `CONSOLIDATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `balanced_trim_seal_leakage_is_separate_internal_path` | 중복 통합 | `CONSOLIDATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `control_valve_gas_choked_flow_does_not_increase_with_further_downstream_pressure_reduction` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_gas_choked_flow_is_a_nonzero_limiting_flow_condition` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_gas_pressure_drop_ratio_increases_as_downstream_pressure_falls` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_gas_sizing_uses_absolute_upstream_temperature` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `control_valve_positioner_uses_position_feedback_to_modulate_actuator_pressure` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `control_valve_pressure_force_sign_depends_on_loaded_areas_and_axis` | 중복 통합 | `CONSOLIDATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `control_valve_stiction_has_stationary_and_slip_jump_travel_phases` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `control_valve_unbalance_area_not_always_seat_area` | 중복 통합 | `CONSOLIDATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `fisher_hunting_possible_control_system_or_positioner_instability` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_h.md) |
| `ideal_full_balance_is_not_universal_actual_state` | 중복 통합 | `CONSOLIDATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_c.md) |
| `liquid_choked_flow_remains_finite_nonzero_capacity` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `liquid_valve_phase_change_pressure_variables` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |
| `lower_liquid_recovery_factor_increases_cavitation_susceptibility` | 중복 통합 | `DUPLICATE_CANDIDATE` | [보고서](fact_anchor_chat_review_20261101_batch_g.md) |

## 변경 시 필수 불변조건

- 지엽적 내용을 제거해도 **물리식, 표준에서 일반적으로 요구하는 안전원리, 계측기의 기본 기능과 원인·결과 관계**는 남긴다.
- 일률적 조건(모든 경우의 3개 운전점·고정 Travel band·표준 Annex 예시를 법적 의무로 승격)은 문장을 수정한 후에만 채점한다.
- 동일 개념을 여러 Anchor로 중복 가산하지 않고 필요하면 한 Core + 다양한 답변 허용 조건으로 통합한다.
- `source=blog` 정책, Topic ID, A~C 결정론적 채점 계약, D~E 판단 보조 계약, 기존 사용자 미커밋 파일을 보호한다.
- 원본 Registry/Generated를 이 보고서로 직접 갱신하지 않는다.
