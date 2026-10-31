# Fact Anchor 산업공통성·기관별 적용범위 — Batch D (2026-11-01)

## 범위

- 작업 브랜치 `codex/essay-boundary-calibration-20261028`, 현행 `remaining_fact_current_queue_20261030.csv` 내 구성변경/백업 36건, Installed Valve 26건, 유지보수/교정 24건 — 총 **86개 Fact**.
- 상태 분포: CORE_CONDITIONAL 35; CORE_SUPPORTED 12; CORE_PHYSICS 8; AGENCY_EXAMPLE 13; VENDOR_EXAMPLE 3; STANDARD_SCOPE 7; REGULATION_SCOPE 5; SUPPLEMENT_ONLY 2; REMOVE_FROM_GENERIC_SCORING 1.
- 앞선 Chat 검토에 이미 언급된 ID **16건**을 포함한 재판정이므로 이번 배치의 고유 추가 검토는 **70건**으로 보수적으로 계산. 중복 확인 못 한 경우 성과를 부풀리지 않는다.
- `CORE_*`는 물리·측정·일반적 엔지니어링 원리로 채점에 적합한 후보. `REGULATION_SCOPE`/`STANDARD_SCOPE`는 해당 관할·산업에만 유효한 사실. `VENDOR_EXAMPLE`/`AGENCY_EXAMPLE`은 거짓이라고 선언하지 않으며 **일반 기술사 필수 채점에서 제외하는 후보**. `REMOVE_FROM_GENERIC_SCORING`도 제품 진위는 별도 검토하고 Core에서 내리는 제안일 뿐 실제 삭제는 아니다.

## Fact ID 개별 검토

| Fact ID | 판정 | 판단 범위와 기술사 채점 처리 |
|---|---|---|
| `calibration_reference_standard_uncertainty_traceability_control` | `CORE_CONDITIONAL` | 교정 기준의 불확도·소급성·상태 확인 필요; 정확도 고정 비율 강제 금지 |
| `calibration_interval_depends_on_requirements_stability_history_and_use` | `CORE_SUPPORTED` | NIST는 보편 교정주기 미제시, 안정성·요구 정확도·사용환경 고려 |
| `calibration_as_found_as_left_and_oot_impact_assessment` | `CORE_CONDITIONAL` | As-found/as-left 비교와 OOT 영향평가는 해당 품질 시스템/규정에 맞춤 |
| `mtbf_operating_time_per_confirmed_failure` | `CORE_PHYSICS` | 수리가능 자산의 정의한 고장 집계에 따른 MTBF=누적 운전시간/유효 고장횟수 |
| `inherent_availability_mtbf_mttr_two_state_model` | `CORE_PHYSICS` | 단순 2상태 수리가능 계통의 Ai=MTBF/(MTBF+MTTR); 예방·물류 지연 제외 |
| `backup_integrity_separation_and_retention_controls` | `CORE_CONDITIONAL` | 백업 주기·분리·보존·무결성 검사는 자산/위험/복구목표별로 정한다 |
| `restore_testing_and_recovery_evidence` | `CORE_CONDITIONAL` | 정기 복원훈련으로 백업의 실제 복구가능성 확인; 기간·빈도는 위험별 |
| `disaster_recovery_objectives_and_resources` | `CORE_CONDITIONAL` | RTO/RPO와 우선순위, 복구자원 정의는 일반 DR 원리; 수치 일률화 금지 |
| `obsolescence_management_is_lifecycle_process` | `CORE_CONDITIONAL` | 단종은 수명주기 위험으로 관리; IEC 62402의 세부 절차는 표준 본문 추가 확인 |
| `configuration_baseline_is_approved_point_in_time_reference` | `CORE_PHYSICS` | Baseline은 승인된 시점 형상의 기준; 현재 형상과 자동 동일함을 뜻하지 않음 |
| `version_control_is_not_complete_configuration_management` | `CORE_SUPPORTED` | 버전관리만으로 CI 식별·승인·변경상태·감사 전체를 대체하지 못함 |
| `valve_authority_is_defined_for_declared_operating_condition` | `CORE_CONDITIONAL` | Authority는 정의한 경계·유량점에서의 밸브 차압 비율; 규약 확인 |
| `simple_series_valve_authority_ratio_requires_fixed_boundary` | `CORE_CONDITIONAL` | 정의된 직렬 계통에서 a=ΔPv/(ΔPv+ΔPrest), 분모 경계 고정 |
| `authority_comparison_requires_complete_hydraulic_boundary` | `CORE_SUPPORTED` | Pump·정수두·배관까지 경계를 일치해야 Authority 비교 가능 |
| `valve_and_pipe_pressure_drops_redistribute_with_flow` | `CORE_PHYSICS` | 관로 손실은 유량에 따라 달라져 밸브/계통 차압 배분이 변화 |
| `low_authority_can_distort_installed_curve_conditionally` | `CORE_CONDITIONAL` | 낮은 Authority에서 Installed 특성 왜곡 가능. 항상 성능 불합격은 아님 |
| `valve_authority_has_no_universal_acceptance_threshold` | `CORE_SUPPORTED` | 모든 설비의 공통 Authority 합격 임계값 없음 |
| `oversized_valve_can_operate_at_low_travel` | `CORE_CONDITIONAL` | 과대용량 밸브는 일부 운전점에서 낮은 Travel 사용 가능 |
| `oversized_valve_can_have_high_low_flow_installed_gain` | `CORE_CONDITIONAL` | 저유량 부근 Installed Gain 변화 가능; 밸브/계통에 따라 다름 |
| `inherent_valve_gain_is_local_slope_under_constant_dp` | `CORE_PHYSICS` | 고유특성 Gain은 ΔP 일정 조건에서 유량/Travel 곡선의 국소 기울기 |
| `installed_valve_gain_is_actual_flow_travel_slope` | `CORE_PHYSICS` | 설치특성 Gain은 실제 계통 Flow/Travel 곡선 국소 기울기 |
| `installed_valve_gain_varies_over_process_operating_range` | `CORE_CONDITIONAL` | 설치 Gain은 비선형/압력 분배 변화에 따라 운전점 의존 |
| `installed_gain_need_not_equal_inherent_gain` | `CORE_SUPPORTED` | 시스템 차압 변화가 고유 곡선과 설치 곡선을 구별 |
| `equal_percentage_is_only_conditional_process_compensation` | `CORE_CONDITIONAL` | Equal Percentage 특성의 설치 보상은 조건부; 최적성 보편화 금지 |
| `installed_gain_variation_can_change_loop_sensitivity` | `CORE_PHYSICS` | 밸브 Gain 변화는 선형화한 제어 Loop Gain 변화를 유발 |
| `inherent_rangeability_is_controllable_cv_ratio_under_stated_tolerance` | `CORE_CONDITIONAL` | 고유 Rangeability는 규정한 공차 내 Cv 최대/최소 비 |
| `rangeability_is_not_a_travel_ratio` | `CORE_SUPPORTED` | Rangeability는 Travel 비가 아닌 Cv 또는 제어가능 유량비 |
| `installed_rangeability_depends_on_installed_controllability_limits` | `CORE_CONDITIONAL` | 설치 Rangeability는 제어성능 기준·계통 조건에 따라 평가 |
| `installed_rangeability_can_differ_from_catalog_rangeability` | `CORE_SUPPORTED` | 설치 범위와 Catalog 고유 범위는 일치 보장 안 됨 |
| `process_turndown_and_valve_rangeability_are_different_quantities` | `CORE_SUPPORTED` | 공정 유량 요구 비와 밸브 제어능력 비 구별 |
| `installed_valve_cases_should_cover_min_normal_max_flow` | `CORE_CONDITIONAL` | 실제 규정된 운전점 중심; 최소/정상/최대 3개를 모든 상황에 강제 금지 |
| `valve_selection_final_check_uses_installed_curve_and_gain` | `CORE_CONDITIONAL` | 설치 조건 유량·Travel·Gain을 목표 성능에 대조 |
| `sw06_ci_identification_scope_and_examples` | `CORE_CONDITIONAL` | CI의 세부 대상과 관계는 조직·형상관리계획이 결정 |
| `sw06_change_authority_proportionate_to_impact_and_criticality` | `CORE_CONDITIONAL` | 변경 영향·중요도에 비례한 검토/승인. 특정 승인 단계 수 강제하지 않음 |
| `sw06_configuration_identification_tracks_ci_attributes_and_relationships` | `CORE_CONDITIONAL` | 재구성·영향분석에 필요한 속성 식별; 모든 프로젝트에 동일 필드 필수 아님 |
| `sw06_change_request_records_scope_priority_impact_and_closure` | `AGENCY_EXAMPLE` | NASA SWE-113 고유 문서 항목은 일반 채점 필수 목록에서 제외 |
| `sw06_release_package_is_identified_approved_and_auditable` | `AGENCY_EXAMPLE` | NASA SWE-085 release package 필드와 권한은 기관 절차 사례 |
| `sw06_software_release_delivery_records_and_as_built` | `AGENCY_EXAMPLE` | NASA SWE-077/085 기록요건은 NASA 프로젝트 범위로 한정 |
| `ot_backup_restore_scope_includes_recovery_dependencies` | `CORE_CONDITIONAL` | 복구 시 필요한 소프트웨어·설정·라이선스·도구·의존성은 적용 자산별 확인 |
| `control_process_gain_is_local_to_operating_conditions` | `CORE_CONDITIONAL` | 비선형 공정의 Gain은 운전점에서 정의한 입력·출력 기준의 국소 변화비 |
| `linearized_control_loop_gain_is_cascade_product` | `CORE_PHYSICS` | 고정 운전점에서 선형화된 직렬 Block Gain의 곱; 우회/비선형/병렬 경로 제외 |
| `closed_seat_leakage_is_distinct_from_minimum_controllable_flow` | `CORE_SUPPORTED` | 완전 닫힘 Seat 누설과 제어 가능한 최소 유량은 다른 정의 |
| `control_range_is_declared_installed_gain_acceptance_interval` | `VENDOR_EXAMPLE` | Emerson/Fisher의 normalized Installed Gain 0.5~2.0 등은 출처 전용 합격 범위 |
| `minimum_controllable_flow_is_distinct_from_seat_leakage_and_contextual` | `CORE_CONDITIONAL` | 최소 제어 가능 Flow의 의미는 조건·허용 편차에 따라 달라짐 |
| `maintenance_types_distinguish_corrective_preventive_condition_based_and_predictive` | `CORE_CONDITIONAL` | 예방/사후/상태기반/예측 정비의 개념 구분, 표준 분류를 모든 상황의 필수 조합으로 강제 금지 |
| `iso14224_maintenance_plan_structured_tasks_activities_procedures_resources_duration` | `STANDARD_SCOPE` | ISO 14224 용어정의는 석유·가스·석유화학 데이터 교환 문맥; 전 산업 의무 목록 아님 |
| `metrological_traceability_chain_uncertainty_and_interval_are_purpose_dependent` | `CORE_SUPPORTED` | 소급성은 측정결과의 속성, 문서화된 끊김 없는 교정사슬·불확도 필요 |
| `asset_maintenance_risk_prioritization_considers_likelihood_consequence_and_defined_criteria` | `CORE_CONDITIONAL` | 안전/환경/가동 영향과 가능성을 고려한 우선순위. 가중치 일률화 금지 |
| `iso14224_equipment_id_function_location_and_reliability_taxonomy` | `STANDARD_SCOPE` | ISO 14224는 석유·가스·석유화학 RM 데이터 범위이며 특정 자산 ID/Taxonomy 일률 적용 금지 |
| `iso14224_maintenance_data_covers_actions_resources_consequences_and_downtime` | `STANDARD_SCOPE` | ISO 14224 분야별 데이터 범주; 전 산업 필수 CMMS 필드 아님 |
| `iso14224_failure_data_categories_and_site_specific_rca_boundary` | `STANDARD_SCOPE` | 고장 데이터/Failure Mode는 해당 표준 범위; RCA 의무 발생기준은 별도 |
| `osha_scoped_hazardous_energy_control_and_psm_maintenance_work_practices` | `REGULATION_SCOPE` | 미국 OSHA 1910.147/PSM 적용 공정과 작업범위로 제한 |
| `iso14224_mttr_repair_vs_mttres_restoration_boundary` | `STANDARD_SCOPE` | MTTR/MTTRes의 용어 구별은 특정 표준 정의에 맞춰 사용. 단일 MTTR 정의 강제 금지 |
| `hse_offshore_sis_maintenance_test_deferral_risk_management_guidance` | `AGENCY_EXAMPLE` | 영국 Offshore HSE 연기관리/승인 절차는 현장·관할 적용; 모든 설비 강제 금지 |
| `osha_psm_mechanical_integrity_deficiency_correction_scope` | `REGULATION_SCOPE` | OSHA PSM §(j)(5) 적용 장비의 허용한계 밖 결함 조치로 한정 |
| `nist_ot_configuration_change_control_and_backup_management_guidance` | `CORE_CONDITIONAL` | NIST OT 변경시험/백업 권고, SP1339의 복원훈련; 모든 작업 전후 백업 의무 아님 |
| `iso55001_system_continual_improvement_value_and_decision_balance` | `STANDARD_SCOPE` | ISO 55001 자산관리시스템 대상에 적용. 모든 KPI/교정 주기의 정량적 의무 아님 |
| `iso14224_reliability_maintenance_data_quality_and_standard_format` | `STANDARD_SCOPE` | ISO14224 범주와 데이터 표준화는 특정 산업 적용, 모든 데이터 분석 결과 정확성 보증 아님 |
| `sw06_as_built_documentation_and_ot_backup_reconciliation` | `CORE_CONDITIONAL` | As-built와 승인 형상 대조, 백업의 시점/버전 관리; 현재 운영상태와 무조건 동일 아님 |
| `sw06_ot_backup_scope_is_asset_and_recovery_objective_specific` | `CORE_CONDITIONAL` | 백업 데이터와 설정의 범위는 자산·복구목표 기준; 고정한 I/O 등 필드 강제 금지 |
| `sw06_moc_is_scoped_to_psm_covered_changes_and_ot_guidance` | `REGULATION_SCOPE` | OSHA PSM은 적용 공정/교체 예외와 해당 변경에만 적용 |
| `nist_sp80082_ot_inventory_for_migration_discovery` | `CORE_CONDITIONAL` | 실제 OT Asset/Configuration 재고를 Migration 기준으로 활용; 필수 필드 차등 |
| `hhs_data_conversion_mapping_test_and_reconciliation_practice` | `AGENCY_EXAMPLE` | HHS 데이터 변환 상세 단계는 IT 가이드 예시; 매핑·정합성 검증 핵심만 채점 |
| `hhs_data_conversion_execution_mode_planning_choices` | `AGENCY_EXAMPLE` | HHS의 Parallel/One-time 선택 방식은 실행 사례 |
| `hhs_data_conversion_cutover_preparation_and_backup_example` | `AGENCY_EXAMPLE` | HHS 사전 백업/모의전환 항목 고정 나열은 보편 의무 아님 |
| `hhs_data_conversion_post_conversion_validation_scope` | `AGENCY_EXAMPLE` | HHS 상세 지침의 문구·중복 데이터 처리 예시는 특정 프로젝트 맥락 |
| `osha_psm_scoped_management_of_change_requirements` | `REGULATION_SCOPE` | 29 CFR 1910.119(l)의 MOC/Replacement-in-kind 예외는 Covered Process에만 적용 |
| `vendor_product_version_scoped_compatibility_checks_for_migration` | `VENDOR_EXAMPLE` | Rockwell PCDC/Siemens Migration Checker는 제조사별 도구 사례; 호환성 검토 원리만 Core |
| `sw06_change_impact_review_is_requirement_and_dependency_scoped` | `CORE_CONDITIONAL` | 기술/안전/인터페이스 영향은 적용 법·위험·기능 의존관계에 맞춤 |
| `sw06_change_execution_plan_is_requirement_and_risk_scoped` | `CORE_CONDITIONAL` | 시험·배포·복구계획은 변경 위험·사업장 절차별 구성 |
| `sw06_restore_and_rollback_are_distinct_recovery_concepts` | `CORE_SUPPORTED` | 백업 Restore와 이전 승인 형상 Rollback은 달라야 할 개념 |
| `sw06_regression_test_selection_is_change_impact_and_risk_scoped` | `CORE_SUPPORTED` | 변경 영향범위와 위험에 맞춘 회귀시험; 전체 기능 전수시험의 무조건적 요구 금지 |
| `sw06_rollback_requirements_are_change_and_procedure_scoped` | `CORE_CONDITIONAL` | Rollback이 실제 가능한 경우 대상·조건·상태 명시. 모든 변경에서 동일 절차 강제 금지 |
| `critical_spare_classification_uses_asset_risk_consequence_and_lead_time` | `CORE_CONDITIONAL` | 중요 예비품 판단은 고장 결과·리드타임·대체성·중요도 등 위험기반 |
| `nasa_lesson_limited_shelf_life_spares_identify_replace_expired` | `AGENCY_EXAMPLE` | NASA 우주 임무 Shelf-life 사례는 일반 OT 예비품 규정 아님 |
| `vendor_product_lifecycle_status_and_ot_change_control_for_obsolescence` | `VENDOR_EXAMPLE` | NI 생애주기 단계는 제품별 참고. 단종 대응·변경관리 원리만 추출 |
| `maintenance_program_separates_routine_inspection_and_functional_checks` | `CORE_CONDITIONAL` | 외관 점검과 기능시험의 목표·증거가 다름; 횟수·구체 항목은 위험별 |
| `maintenance_reliability_kpi_catalog_and_definitions_are_scoped` | `SUPPLEMENT_ONLY` | 다양한 KPI 목록은 참고, 목표·분모·데이터 규칙 정의가 핵심 |
| `sw06_legacy_system_risk_based_management` | `CORE_CONDITIONAL` | Legacy 교체/보완/격리 판단은 기능·수명·보안·지원 위험을 함께 검토 |
| `sw06_vendor_lockin_lifecycle_risk` | `SUPPLEMENT_ONLY` | 벤더 Lock-in/라이선스/도구 가용성은 설계 의사결정 고려사항이나 필수 세부항목 고정 금지 |
| `osha_psm_operating_procedure_currency_and_training_records` | `REGULATION_SCOPE` | OSHA 적용 공정의 서면 절차/연례 확인 및 교육기록 규칙으로 한정 |
| `nasa_npr_4100_1f_shelf_life_type_and_test_controls` | `AGENCY_EXAMPLE` | NASA Type I/II 보존기간 분류를 일반 OT 기술사 필수 사실에서 제외 |
| `dod_sd22_dmsms_resolution_categories_and_complexity` | `AGENCY_EXAMPLE` | DoD DMSMS resolution 목록을 모든 산업의 단종 전략 필수 열거로 오인 금지 |
| `dod_sd22_software_license_life_of_need_examples` | `AGENCY_EXAMPLE` | DoD의 License downgrade/지원 연장 사례는 참고만 |
| `oracle_zdm_post_switchover_fallback_condition_example` | `REMOVE_FROM_GENERIC_SCORING` | Oracle ZDM switchover 후 redo 송신의 특정 조건은 보편 제어·계장 Fact로서 채점 부적합. 참·거짓/제품 버전은 별도 확인 |
| `gao_jfmip_parallel_operation_transition_test_and_costs` | `AGENCY_EXAMPLE` | GAO/JFMIP 구·신 시스템 병행시험의 이점/중복비용은 IT Migration 사례. 일반 원리만 유지 |

## 검토 근거·표준의 정확한 적용 경계

- [NIST 교정주기 공식 FAQ](https://www.nist.gov/calibrations/recommended-calibration-interval): 고정 교정주기 부재, 불확도·환경·안정성·요구 정확도에 맞춰 선정.
- [NIST 측정 소급성 공식 FAQ](https://www.nist.gov/metrology/metrological-traceability): 소급성은 측정 **결과**의 성질이며 문서화된 연속 교정과 각 단계 불확도 필요.
- [NIST SP1339(2026) 발행기관 공식 페이지](https://csrc.nist.gov/pubs/sp/1339/final): OT 백업을 변경관리에 통합하고 생성·시험·복구훈련 권고. [NIST OT SP800-82 Rev3](https://csrc.nist.gov/pubs/sp/800/82/r3/final); 최신 Rev4는 2026-09-21 현재 **Draft**로 Rev3가 확정본([NIST 공개 목록](https://csrc.nist.gov/Projects/operational-technology-security/publications)).
- [OSHA 29 CFR 1910.119 공식 원문](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119): §(j) Mechanical Integrity, §(l) MOC, §(f) Operation; **미국 Covered Process** 외부로 보편 법적 의무를 확대 금지.
- [ISO 14224:2016 공식 범위](https://www.iso.org/standard/64076.html): 석유·천연가스·석유화학의 장비 신뢰성·정비 데이터 수집 및 교환. 모든 설비의 CMMS·KPI 상세 필수 기준 아님.
- [Emerson/Fisher Control Valve Handbook 공식 페이지](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/control-valve-handbook): 제어밸브 고유/설치특성, 액추에이터, Hydraulic boundary 및 Flow/Travel 설명. 보편적 Authority 합격값 또는 Gain 0.5~2.0 의무는 아님.
- **기관·제품 고유 사례:** NASA SWE, HHS EPLC, DoD SD-22, NASA Shelf-life, Oracle ZDM, GAO/JFMIP, NI lifecycle는 각 출처의 제도·프로그램·버전 범위. 유료/비공개 표준의 상세 조항까지 원문 확인한 것으로 기록하지 않는다.

## 중복·삭제 후보와 변경 통제

1. `oracle_zdm_post_switchover_fallback_condition_example`: **일반 채점 Fact에서 제외 우선 후보**. Oracle 전용 시스템 전환 내부 조건은 OT 전반의 물리/표준 원리가 아님. Oracle 진위는 삭제 근거가 아니라 채점 범위 적합성 문제.
2. `dod_sd22_software_license_life_of_need_examples`, `nasa_npr_4100_1f_shelf_life_type_and_test_controls`, `sw06_release_package_is_identified_approved_and_auditable`, `vendor_product_version_scoped_compatibility_checks_for_migration`: 일반 위험·호환성·복구 원리만 Core에 보존하고 기관별 서식·분류·도구명은 보조자료로 이동할 후보.
3. `installed_rangeability_can_differ_from_catalog_rangeability`, `installed_gain_need_not_equal_inherent_gain`, `installed_valve_gain_varies_over_process_operating_range`: 원리상 사실이나 실제 Topic Pack의 개별 배점이 중복되는지 대조 후 조정. **지금은 삭제하지 않음**.
4. 이 보고서의 결과를 기존 Queue나 Registry의 `verified` 상태 변경으로 계산하지 않음. 최종 삭제/채점 수정은 관련 Topic Pack source·Logic·모범답안·생성물 CLI·회귀 테스트까지 함께 처리.

## 검증 환경

- GitHub 문서 보고서만 새로 추가. 로컬 checkout, 사용자 미커밋 두 파일, operating checkout, container 변경 없음.
- 로컬 pytest/Release Gate/validate-all 미실행. 모델의 일반원리 선별 점수로 재승인하거나 삭제하지 않음.
