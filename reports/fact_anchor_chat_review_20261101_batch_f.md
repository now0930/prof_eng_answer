# Fact Anchor 안전계장·신뢰성·MC/DC — Batch F (2026-11-01)

## 범위·판정

- 작업 브랜치 `codex/essay-boundary-calibration-20261028`. 현행 Queue 내 SIS/안전소프트웨어 29, 신뢰도 22, Final Element 27, SIL 할당 14, MC/DC 31, 총 **123개 Fact ID**에 일반 원리·물리/확률 모델·표준 적용범위 검토.
- 결과: CONDITIONAL_CORE 90; CORE_SUPPORTED 25; STANDARD_SCOPE 3; CORE_CONDITIONAL 1; SUPPLEMENT_ONLY 3; VENDOR_EXAMPLE 1. 본 자료만으로 Registry 승인 상태나 기존 1,265건 미확인 기록 변경하지 않는다.
- `CORE_SUPPORTED`: 여러 신뢰 가능한 공개 원문 또는 직접 검증 가능한 논리; `CONDITIONAL_CORE`: 요구 모드·SRS·공통원인·해석 모델·산업표준 범위와 함께 유지; `VENDOR_EXAMPLE`/`STANDARD_SCOPE`/`SUPPLEMENT_ONLY`: 전 산업 기술사 필수 Fact로 사용하지 않음.
- 법/표준 단어가 있다는 이유만으로 인증하지 않고, 각각의 원문 문장에 포함된 단서와 요구/위험분석 경계를 유지한다.

## Fact ID별 판단

| Fact ID | 권고 | 기술사 채점·적용 조건 |
|---|---|---|
| `sil_target_band_after_metric` | `CONDITIONAL_CORE` | CCPS LOPA·HSE/IEC 기능안전: 위험시나리오별 목표 설정과 SIF 달성검증을 구분 |
| `sil_sis_sif_scope` | `CONDITIONAL_CORE` | CCPS LOPA·HSE/IEC 기능안전: 위험시나리오별 목표 설정과 SIF 달성검증을 구분 |
| `sil_hazard_scenario_boundary` | `CONDITIONAL_CORE` | CCPS LOPA·HSE/IEC 기능안전: 위험시나리오별 목표 설정과 SIF 달성검증을 구분 |
| `sil_tolerable_risk_alarp` | `CONDITIONAL_CORE` | 허용위험/ALARP 판단은 관할·산업·법적 기준에 따르며 고정 허용빈도 없음 |
| `sil_method_selection` | `CORE_SUPPORTED` | Risk Graph·LOPA 등은 가능한 배정방법; 어느 하나 보편 의무 아님 |
| `sil_initiating_frequency_modifiers` | `CONDITIONAL_CORE` | CCPS LOPA·HSE/IEC 기능안전: 위험시나리오별 목표 설정과 SIF 달성검증을 구분 |
| `sil_existing_ipl_independence` | `CONDITIONAL_CORE` | CCPS LOPA·HSE/IEC 기능안전: 위험시나리오별 목표 설정과 SIF 달성검증을 구분 |
| `sil_residual_frequency_before_sif` | `CONDITIONAL_CORE` | CCPS LOPA·HSE/IEC 기능안전: 위험시나리오별 목표 설정과 SIF 달성검증을 구분 |
| `sil_required_rrf_relation` | `CONDITIONAL_CORE` | CCPS LOPA·HSE/IEC 기능안전: 위험시나리오별 목표 설정과 SIF 달성검증을 구분 |
| `sil_target_pfd_relation` | `CONDITIONAL_CORE` | CCPS LOPA·HSE/IEC 기능안전: 위험시나리오별 목표 설정과 SIF 달성검증을 구분 |
| `sil_demand_mode_metric_selection` | `CONDITIONAL_CORE` | CCPS LOPA·HSE/IEC 기능안전: 위험시나리오별 목표 설정과 SIF 달성검증을 구분 |
| `sil_achieved_sil_verification` | `CORE_SUPPORTED` | 대상 SIL과 설계 검증 SIL은 독립, 전체 SIF 수명주기 증거 필요 |
| `sil_is_discrete_integrity_level_of_safety_function` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `hazard_risk_analysis_allocates_sif_requirements_and_sil` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `safety_software_is_managed_through_lifecycle_activities` | `CONDITIONAL_CORE` | V&V·운영/변경관리 기본원리. 특정 lifecycle 문서세트 전부를 무조건 필수화 금지 |
| `srs_lifecycle_handoff_process_independently_verified` | `CONDITIONAL_CORE` | CCPS LOPA·HSE/IEC 기능안전: 위험시나리오별 목표 설정과 SIF 달성검증을 구분 |
| `sis_operational_maintenance_modification_records_and_review` | `CONDITIONAL_CORE` | 운영/정비/변경 기록은 적용 안전기준과 수명주기 절차 범위로 판단 |
| `mcdc_full_coverage_is_not_complete_requirements_or_sil_evidence` | `CORE_SUPPORTED` | 100% 구조적 MC/DC가 요구사항 올바름·SIL 달성 보증하지 않음 |
| `mcdc_structural_criterion_targets_independent_condition_effect` | `CORE_SUPPORTED` | 독립 Boolean 조건의 Decision 영향 입증이 MC/DC 핵심 |
| `mcdc_full_criterion_includes_entry_exit_and_independence_obligations` | `STANDARD_SCOPE` | NASA/DO-178B 문맥의 Entry/Exit·Decision/Condition/독립효과 요건, 일반 PLC에 자동 적용 안 됨 |
| `statement_coverage_executes_each_executable_statement_only` | `CORE_SUPPORTED` | Statement Coverage와 Decision/Condition Coverage 구분 |
| `decision_coverage_exercises_decision_true_and_false_not_condition_effect` | `CORE_SUPPORTED` | 각 Decision의 True/False만으로 각 Condition 독립 영향 입증 불가 |
| `condition_coverage_exercises_each_condition_outcome_not_decision_effect` | `CORE_SUPPORTED` | 조건값 T/F와 전체 Decision 독립 영향이 서로 다른 요구 |
| `mcdc_structural_and_requirement_coverage_are_complementary` | `CORE_SUPPORTED` | 구조적 시험과 요구사항 시험은 보완적, 상호 대체 아님 |
| `mcdc_mcc_exercises_all_condition_combinations` | `CORE_CONDITIONAL` | MCC는 실현 가능한 조합 전체. 조합 수/실행조건 제약을 인정 |
| `mcdc_independence_pair_changes_decision_via_target_effect` | `CORE_SUPPORTED` | 독립영향 Pair로 특정 조건이 Decision 출력을 바꿈을 입증 |
| `mcdc_inactive_boolean_branch_masks_other_condition_effect` | `CORE_SUPPORTED` | AND 거짓/OR 참 조건이 다른 영향 마스킹하는 Boolean 원리 |
| `mcdc_deactivated_code_is_configuration_scoped_inactive_code` | `STANDARD_SCOPE` | Deactivated Code의 공식 정의/처리는 적용 안전소프트웨어 규격마다 다름 |
| `mcdc_structural_coverage_complements_requirements_based_tests` | `CORE_SUPPORTED` | MC/DC는 Requirement Test의 대체물이 아님 |
| `mcdc_unique_cause_pair_holds_other_conditions_fixed` | `CONDITIONAL_CORE` | Unique Cause와 Masking MC/DC 구별 |
| `mcdc_masking_allows_non_target_changes_when_effect_masked` | `CONDITIONAL_CORE` | 비대상 조건 변화는 결과에 영향이 마스킹됨을 입증해야 함 |
| `mcdc_n_plus_one_test_count_is_not_universal` | `CORE_SUPPORTED` | N+1은 가능한 단순구조의 사례이지 무조건 최소 Test 개수 아님 |
| `mcdc_condition_coupling_can_invalidate_unique_cause_pairs` | `CONDITIONAL_CORE` | 조건이 종속되면 Unique Cause 짝 불가능 가능성 |
| `sis_software_systematic_failure_needs_lifecycle_controls` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_verification_phase_deliverable_definition` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_proof_test_detects_unrevealed_dangerous_failures` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_shared_resources_create_common_cause_dependency` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_common_cause_dependency_independence_assessment` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_pfdavg_pfh_demand_mode_measure_boundary` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_random_hardware_failure_degradation_definition` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_systematic_failure_definition_and_sources` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_validation_meets_safety_requirements_specification` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_srs_function_and_integrity_requirements_detail` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_safety_application_program_implements_specified_logic` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_control_system_validation_precedes_overall_validation` | `CONDITIONAL_CORE` | FAT와 설치 후 전체 안전 검증을 구별하되 단계 이름과 순서의 예외 고려 |
| `sis_override_and_maintenance_bypass_controls` | `CONDITIONAL_CORE` | 우회와 안전상태 위험을 통제하지만 만능 동일 승인·시간 제한 양식 금지 |
| `sis_functional_safety_assessment_independent_evidence_review` | `CONDITIONAL_CORE` | 독립성 요구의 역할·수준은 IEC 61511 적용범위와 조직·SIL에 따름 |
| `sis_safety_lifecycle_traceability_record` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `sis_modification_control_and_safety_verification` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `final_element_valve_actuator_utility_scope` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `final_element_safe_action_process_dependent` | `CORE_SUPPORTED` | 안전상태는 공정 요구별; Fail-open/Fail-close 보편 정답 금지 |
| `deenergize_trip_requires_application_safe_action_check` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `protective_system_required_utility_scope_and_integrity` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `partial_stroke_exercise_is_not_full_proof_test` | `CORE_SUPPORTED` | HSE는 PST/Actuator Exercise가 full proof test와 동등하지 않음을 명시 |
| `proof_test_frequency_detection_and_repair_time_effect` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `proof_test_procedure_acceptance_and_safe_execution` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `sis_override_and_post_maintenance_restoration_controls` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `sis_proof_test_expected_trip_and_end_to_end_scope` | `CONDITIONAL_CORE` | 실제 Trip/End-to-End 시험과 예외조치는 위험·운전 제약에 따라 설계 |
| `maintenance_bypass_equivalent_safety_controls` | `CONDITIONAL_CORE` | 우회 시 보상조치는 실제 SIF 위험에 따라 정의, 모든 조치 목록 일률화 금지 |
| `shared_dependencies_and_environment_affect_independence` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `actuator_online_monitoring_detects_selected_faults` | `SUPPLEMENT_ONLY` | Stroke-Time/Brake/End-switch 진단 예시는 기종별; 모든 상태를 판단 가능하다고 강제 금지 |
| `sis_modification_and_spares_controls` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `repair_performance_monitored_against_design_criteria` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `mcdc_applicability_and_target_follow_safety_classification_and_plan` | `CORE_SUPPORTED` | 안전분류·해당 산업표준·계획 없이는 모든 PLC에 MC/DC 강제하지 않음 |
| `functional_safety_audit_reviews_lifecycle_and_management_processes` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `safety_related_competence_uses_role_evidence_and_assessment` | `CONDITIONAL_CORE` | IEC 61508/61511/HSE 안전수명주기의 SIF 경계·안전 요구·무결성·독립성 원리. 상세 SIL/시험은 실제 적용 표준·설비별 검증 |
| `misra_guidelines_are_coding_rules_not_dynamic_unit_test_tools` | `STANDARD_SCOPE` | MISRA 준수 및 정적분석의 역할은 타당하지만 MISRA를 모든 PLC의 강제 규칙으로 확대 금지 |
| `functional_safety_diversity_is_ccf_measure_not_guarantee_and_has_complexity_tradeoff` | `CONDITIONAL_CORE` | 다양성은 공통원인을 줄일 수 있으나 무조건 제거하지 않음 |
| `iec_61508_tool_qualification_considers_safety_impact_and_error_detection` | `CONDITIONAL_CORE` | 도구 오검출 위험·후속 검출가능성을 고려하되 표준의 도구 등급/절차는 해당 적용 조항에 따름 |
| `safety_manual_assumptions_and_proof_test_requirements_enter_sif_design` | `CONDITIONAL_CORE` | 선정된 실제 인증제품 Safety Manual·실제 시험조건을 참조 |
| `proven_in_use_software_requires_versioned_scope_profile_and_fault_history` | `CONDITIONAL_CORE` | Proven-in-use 사용가능성은 개별 표준·운영이력과 환경 유사성에 의존, 단순 장기운영만으로 충족하지 않음 |
| `functional_safety_pfd_approximation_states_demand_diagnostic_test_repair_and_ccf_assumptions` | `CONDITIONAL_CORE` | PFD 근사는 시스템 구조·시험/수리/독립성 조건을 특정해야 함 |
| `v_model_organizes_software_verification_but_does_not_establish_sif_sil` | `CORE_SUPPORTED` | V Model 채택 자체가 SIL 달성을 인증하지 않음 |
| `siemens_safety_integrated_fblock_reuse_requires_signature_and_version_recheck` | `VENDOR_EXAMPLE` | Siemens F-block signature/version 업무 규칙을 모든 SIS의 필수 Fact로 요구하지 않음 |
| `fault_tree_analysis_decomposes_defined_top_event_with_boolean_logic` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `minimal_cut_set_is_minimal_basic_event_combination_causing_top_event` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `safety_function_failure_metric_depends_on_demand_mode` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `low_demand_sif_integrity_uses_average_probability_of_failure_on_demand` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `high_or_continuous_demand_sif_integrity_uses_dangerous_failure_rate` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `diagnostic_coverage_and_proof_test_coverage_are_distinct_detection_mechanisms` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `proof_testing_targets_dangerous_failures_not_found_by_online_diagnostics` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `longer_proof_test_interval_increases_latent_failure_exposure_under_constant_rate_model` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `partial_proof_test_leaves_uncovered_failure_modes_for_full_test_or_modeling` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `rbd_represents_system_success_logic_through_functional_paths` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `series_and_parallel_rbd_paths_encode_different_success_conditions` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `markov_reliability_model_uses_system_states_and_transition_rates_to_track_state_probabilities` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `markov_state_space_growth_can_increase_analysis_burden_without_universal_growth_rate` | `SUPPLEMENT_ONLY` | 상태공간 폭발은 해석 복잡도 설명이며 고정 증가율·필수 정량채점 근거 아님 |
| `common_cause_failures_reduce_redundancy_benefit_under_independence_assumption` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `physical_separation_independent_utilities_and_diversity_are_ccf_mitigation_measures` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `low_demand_risk_reduction_factor_is_inverse_of_pfdavg_under_defined_sif_metric` | `CONDITIONAL_CORE` | PFDavg 기준 저요구 모드에서만 RRF≈1/PFDavg로 다룸 |
| `hft_and_voting_architecture_alone_do_not_demonstrate_achieved_sil` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `certified_subsystem_sil_does_not_automatically_establish_complete_sif_integrity` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `random_hardware_failure_calculation_does_not_replace_systematic_and_lifecycle_evidence` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `beta_factor_model_partitions_total_rate_into_independent_and_common_cause_contributions` | `CONDITIONAL_CORE` | β-model은 공통원인 단순화 모델, 어느 구조에도 보편 정확한 값 아님 |
| `pfdavg_approximation_requires_explicit_model_assumptions_and_scope` | `CORE_SUPPORTED` | λDU, 시험 간격, 공통원인, 진단, 수리 조건 없이 PFDavg 숫자 인증 금지 |
| `mcdc_coverage_analysis_traces_artifacts_and_disposes_uncovered_structure` | `CONDITIONAL_CORE` | 미커버 영역은 요구·코드·테스트 불일치 원인을 조사, 처리절차는 적용 규격에 따름 |
| `uncovered_structural_code_is_analyzed_and_its_disposition_recorded` | `CONDITIONAL_CORE` | Dead/Deactivated/미시험 경로는 각각 구분 후 정당화/수정, 고정 처분 일률화 금지 |
| `static_analysis_complements_but_does_not_supply_execution_coverage_evidence` | `CORE_SUPPORTED` | 정적분석으로 실제 실행된 MC/DC 증거를 대체할 수 없음 |
| `sis_voting_architecture_changes_dangerous_failure_and_spurious_trip_tradeoffs` | `CONDITIONAL_CORE` | FTA/RBD/Markov 신뢰성 모델의 논리·확률관계. 독립성·고장률·상태경계 가정 없이는 실제 SIL 확정 불가 |
| `unneeded_dead_code_is_removed_or_its_residual_risk_justified` | `CONDITIONAL_CORE` | Dead Code 처리는 안전등급/변경위험/수명주기에 의존 |
| `source_object_coverage_equivalence_is_analyzed_when_generated_code_changes_structure` | `CONDITIONAL_CORE` | Source와 Object 동등성 증거는 해당 표준/컴파일러/도구 안전영향에 따름 |
| `coverage_tool_assurance_depends_on_tool_use_and_unverified_output_risk` | `CONDITIONAL_CORE` | Coverage Tool이 잘못된 증거 제공 시 영향 평가/검증 필요 |
| `compiler_generated_object_structure_can_differ_from_source_decision_structure` | `CONDITIONAL_CORE` | 최적화·Compiler 버전에 따라 Source/Object 경로 일치 보장 불가 |
| `coverage_instrumentation_can_add_runtime_overhead_and_change_observed_execution` | `CORE_SUPPORTED` | 계측 오버헤드/Probe Effect는 물리적 실행시간/메모리 영향 |
| `short_circuit_evaluation_can_mask_unexecuted_boolean_conditions` | `CORE_SUPPORTED` | 단락평가로 Boolean 조건 일부가 미평가될 수 있음 |
| `coverage_test_environment_represents_target_hardware_and_timing_conditions` | `CONDITIONAL_CORE` | 시험환경과 실제 Target 차이는 영향 평가해야 하나 모든 시험이 실물 Hardware 필수는 아님 |
| `structural_mcdc_coverage_is_one_vv_evidence_not_a_lifecycle_substitute` | `CORE_SUPPORTED` | 구조적 커버리지로 생애주기 V&V 전체 대체 불가 |
| `safety_error_handling_behavior_is_requirement_traced_and_tested` | `CONDITIONAL_CORE` | Error Handling 요구를 명세/검증하지만 모든 Defensive Code가 동일 SRS 형식은 아님 |
| `mcdc_decision_coverage_does_not_replace_other_data_timing_and_boundary_analyses` | `CORE_SUPPORTED` | Boolean Coverage로 Overflow·Timing·Data Coupling 전부 검증할 수 없음 |
| `software_changes_trigger_regression_and_coverage_impact_review` | `CONDITIONAL_CORE` | 코드/Compiler 변경 시 영향범위 회귀와 커버리지 검토, 불변 영역 전수 재수행 의무 아님 |
| `final_element_safe_failure_and_spurious_trip_consequences_are_distinct` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `sif_final_element_package_can_include_actuator_solenoid_and_support` | `SUPPLEMENT_ONLY` | ESD 제품 구성·Accessory 목록은 설계별 참고; 센서·로직·최종요소 경계가 Core |
| `dormant_sis_valves_can_hide_sticking_degradation` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `sif_seat_leakage_acceptance_depends_on_required_safety_function` | `CORE_SUPPORTED` | Seat Leakage 의무는 SRS의 목적(격리 등)에 따른다 |
| `low_demand_final_element_uses_pfdavg_measure` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `high_demand_or_continuous_final_element_uses_pfh_measure` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `diagnostic_coverage_is_detected_dangerous_failure_fraction` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `proof_test_coverage_is_tested_fraction_of_relevant_failures` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `pst_detects_only_architecture_and_procedure_covered_fault_modes` | `CONDITIONAL_CORE` | PST 진단가능 고장집합은 실제 구성과 동작 시험범위에 따라 다름 |
| `partial_testing_leaves_unrevealed_failure_modes_for_full_proof_test` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `online_valve_test_bypass_can_leave_sif_unprotected` | `CORE_SUPPORTED` | 시험 중 우회는 기능을 저해할 수 있어 위험·조치 관리 |
| `systematic_capability_is_not_proved_by_random_failure_probability_alone` | `CONDITIONAL_CORE` | HSE 보호계통 지침의 최종요소/진단/Proof Test 원리. 실제 Failure Mode·기능·제약별 시험 |
| `sif_acceptance_criteria_trace_to_defined_safety_requirements` | `CORE_SUPPORTED` | 시험 합격기준을 SRS 안전 기능요구와 추적 |

## 특히 주의할 범용화 오류

1. **SIL:** SIL은 기능/시나리오의 안전 무결성 요구에 배정; 센서 인증·PLC 모델 등급·하드웨어 중복만으로 전체 SIF의 SIL 달성 주장을 금지. 저요구 `PFDavg`는 무차원, 고요구 `PFH`는 시간 역수 — 두 물리량을 수치로 직접 비교할 수 없다.
2. **Proof/PST:** HSE는 Partial Stroke/Actuator Exercise를 Full Proof Test와 구별. 시험 후 잔류 위험고장모드/진단 커버리지를 명시하지 않은 PST 효과의 보편적인 PFD 감소율을 승인하지 않음.
3. **CCF/의존성:** 독립 채널·정비·공통 전원·현장 탭·진단 기능을 고려하지 않고 Reliability 블록을 독립이라고 가정하지 않음.
4. **MC/DC:** MC/DC 100%가 명세의 타당성·실행환경·하드웨어 결함·SIL을 보증하지 않음. NASA SWE-219의 100% 안전중요 소프트웨어 요구는 **NASA 해당 프로그램**에 적용되며 일반 PLC 전체의 무조건 의무가 아님. Masking/Unique-Cause는 정의가 다른 방식이며 `n+1` 테스트 수 보편 규칙 아님.
5. **제조사 절차:** Siemens F-block 서명/버전 비교는 특정 안전 라이브러리 가이드 내용으로서 제품 범위를 넘지 않는다.

## 외부 공식 근거 및 한계

- [HSE 기능안전과 SIS 수명주기](https://www.hse.gov.uk/eci/functional.htm), [HSE 보호계통 설계·독립성·Proof Testing·PST와 Modification](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm). 산업·관할 적용 범위를 명시.
- [CCPS/AIChE LOPA 공식 원리](https://ccps.aiche.org/resources/tools/lopa), [TÜV SÜD IEC 61508 PFDavg/PFH SIL 구간](https://www.tuvsud.com/ko-kr/services/functional-safety/iec-61508) (표준 전체 문구의 재현이 아니라 공개 요약에 대한 대조).
- [NASA SWE-219 MC/DC 안전중요 소프트웨어 지침](https://swehb.nasa.gov/spaces/SWEHBVD/pages/105709626/SWE-219%2B-%2BCode%2BCoverage%2Bfor%2BSafety%2BCritical%2BSoftware), [NASA Multi-condition / Unique Cause·Masking](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695692/7.21%2B-%2BMulti-condition%2BSoftware%2BRequirements), [NIST MC/DC 정의](https://csrc.nist.gov/glossary/term/Modified_condition_decision_coverage), [NASA NTRS 원문 서지](https://ntrs.nasa.gov/citations/20010057789).
- 원본 IEC 61508/61511의 상세 절/항을 전체 구매·열람하지 않았으므로 규격 세부 절 번호와 권한 기반 mandatory 결론은 보고서에서 내리지 않음.

## 변경·검증 상태

- 보고서만 새로 추가. Registry/Topic Packs/Logic/Generated/운영 체크아웃 미변경.
- 실제 변경 시 Topic Pack 요구축과 안전중요 채점 테스트를 보존하고, CLI 생성·집중 테스트·release gate·`validate-all` 필요. 이 Chat 환경에서는 실행하지 않음.
