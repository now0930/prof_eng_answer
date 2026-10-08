# Anchor 사실 검증 배치 200 (2026-10-08)

## 범위와 판정 기준

이번 배치는 미검토 재고에서 기능안전 소프트웨어, MC/DC, ESD 최종요소, HIPPS, OT 보안, 산업 AI의 순서로 **정확히 200개**를 선택했다. Topic Pack 원문은 각 링크된 `fact_anchor.json`에서 확인한다. 아래 표의 `확인`은 근거 자료가 문장의 주장을 지지한다는 뜻이고, `적용조건`은 표준/기기/현장 조건이 달라 일률 규정으로 사용할 수 없다는 경계를 확인했다는 뜻이다. `수정`은 이번 배치에서 source를 바로잡았다. 법규 또는 특정 표준의 의무 조항이라는 뜻으로 확대하지 않는다.

| Topic Pack | Anchor 수 | 확인 | 적용조건 | 수정 | 추가근거 |
|---|---:|---:|---:|---:|---:|
| SIS 안전 소프트웨어 | 34 | 34 | 0 | 0 | 0 |
| MC/DC 구조 커버리지 | 33 | 28 | 4 | 1 | 0 |
| ESD 최종요소·PST | 48 | 43 | 5 | 0 | 0 |
| HIPPS | 25 | 22 | 3 | 0 | 0 |
| OT 사이버보안 | 40 | 38 | 1 | 0 | 1 |
| 산업 AI·예지보전 | 20 | 19 | 1 | 0 | 0 |
| **합계** | **200** | **185** | **13** | **1** | **1** |

## 1. SIS 안전 소프트웨어 (34)

근거: [IEC 61511-1 미리보기][iec61511], [HSE 기능안전 lifecycle][hsefs], [HSE SIS 운영·제어시스템][hsecontrol]. IEC 미리보기는 일부 조항만 노출하므로, 전체 규범 조항을 확인했다고 주장하지 않는다.

| Anchor ID | 판정 | 대조 메모 |
|---|---|---|
| `sis_sif_relation` | 확인 | SIS가 하나 이상의 SIF를 구현하는 관계 확인. |
| `sil_property_of_safety_function` | 확인 | SIL은 안전기능의 무결성 수준이며 제품명 자체가 아님. |
| `sif_end_to_end_boundary` | 확인 | 센서부터 최종요소까지 기능경계를 확인. |
| `risk_to_srs_flow` | 확인 | H&RA에서 SIF 기능·무결성 요구 도출 및 SRS 인계 확인. |
| `srs_functional_integrity_requirements` | 확인 | SRS에서 안전기능과 무결성 요구를 구분해 명세. |
| `application_program_role` | 확인 | Application Program이 SRS의 논리기능을 구현한다는 의미 확인. |
| `software_safety_lifecycle` | 확인 | 안전 소프트웨어가 설계부터 변경·운영까지 lifecycle에서 관리됨. |
| `random_hardware_failure` | 확인 | 무작위 하드웨어 고장은 시간에 따른 고장확률/률로 다루는 구분 확인. |
| `systematic_failure` | 확인 | 요구·설계·소프트웨어·도구·설치·변경 결함이 체계고장 원인이 될 수 있음. |
| `systematic_not_simple_rate` | 확인 | 체계고장을 하드웨어 무작위 고장률 계산만으로 충분히 다루지 못함. |
| `verification_definition` | 확인 | 산출물을 단계 입력 요구와 대조하는 verification 의미 확인. |
| `validation_definition` | 확인 | 통합 SIS가 사용환경에서 SRS를 만족하는지 확인하는 validation 의미 확인. |
| `functional_test_boundary` | 확인 | 기능시험은 특정 기능 시험이며 전체 safety validation과 같지 않음. |
| `proof_test_relation` | 확인 | Proof test와 소프트웨어 validation은 다른 증거·활동임. |
| `independence_purpose` | 확인 | 독립 검토·분리의 조직 및 기술적 목적 확인. 특정 표준 수준은 SIL·scope에 따름. |
| `separation_shared_resources` | 확인 | 공유 센서·전원·네트워크·도구 등은 SIS/BPCS 분리 후에도 dependency가 될 수 있음. |
| `common_cause_dependency` | 확인 | 공통원인·종속성은 독립채널 가정을 손상시킬 수 있음. |
| `diversity_tradeoff` | 확인 | Diversity는 일부 CCF를 줄일 수 있지만 설계 복잡성과 새 체계오류를 추가할 수 있음. |
| `certified_product_scope` | 확인 | 인증은 명시된 범위·조건과 Safety Manual 가정 안에서만 증거가 됨. |
| `safety_manual_constraints` | 확인 | Safety Manual 제한과 사용가정을 SIF 설계에 반영해야 함. |
| `proven_in_use_evidence` | 확인 | Proven-in-use 주장은 기기/version·사용이력·결함기록·환경 대표성에 의존. |
| `tool_qualification_basis` | 확인 | 도구 오류 영향과 후속검출 가능성으로 qualification 수준을 정함. |
| `library_validation_control` | 확인 | Library/function block의 version·검증범위·parameter·변경을 통제. |
| `bidirectional_traceability` | 확인 | 요구·설계·프로그램·시험·결과의 추적성 확인. |
| `modification_revalidation` | 확인 | 변경 영향분석, 승인, regression 및 필요한 범위의 revalidation과 as-built 갱신. |
| `bypass_override_controls` | 확인 | 우회는 승인·표시·기간·보상조치·기록·복구 확인으로 관리. |
| `audit_role` | 확인 | Audit은 lifecycle 활동과 관리체계의 수행을 점검. |
| `competence_management` | 확인 | 역할별 역량은 교육·경험·책임·평가 근거로 관리. |
| `pfd_pfh_mode_boundary` | 확인 | 저요구 PFDavg와 고요구/연속 PFH의 mode boundary 확인. |
| `quantitative_assumptions` | 확인 | PFD 계산에서 mode, 진단, 시험, 수리, CCF 및 독립성 가정을 명시. |
| `sis_mcdc_structural_coverage_boundary` | 확인 | SW-05 일반 lifecycle와 MC/DC 상세 Topic의 ownership 구분 확인. |
| `random_hardware_failure__unit_test_not_random_hardware_integrity` | 확인 | Unit test는 software 결함검출이며 무작위 하드웨어 무결성의 대체증거가 아님. |
| `random_hardware_failure_unit_test_not_random_hardware_integrity__misra_not_unit_test_tool` | 확인 | MISRA는 코딩 지침이며 정적 분석 등으로 준수를 확인; 동적 단위시험 도구 자체가 아님. |
| `sis_mcdc_structural_coverage_boundary__vmodel_does_not_guarantee_sil` | 확인 | V-model 사용 자체가 SIL 달성을 보장하지 않는다는 경계 확인. |

## 2. MC/DC 구조 커버리지 (33)

근거: [FAA AC 20-115D][faa], [NASA MC/DC 설명][nasamcdc]. FAA 문서는 항공 소프트웨어에 적용되는 수용 가능한 방법이므로, 이 근거를 다른 산업의 일률 의무로 확대하지 않는다.

| Anchor ID | 판정 | 대조 메모 |
|---|---|---|
| `mcdc_purpose` | 확인 | 조건별 독립 영향에 대한 구조 커버리지 목적 확인. |
| `mcdc_structural_vs_requirements_coverage` | 확인 | 코드구조 커버리지와 요구사항 검증은 상호보완. |
| `mcdc_statement_coverage` | 확인 | Statement coverage는 실행문 실행을 확인하며 개별 조건 독립영향을 보장하지 않음. |
| `mcdc_decision_coverage` | 확인 | Branch/decision 결과 true와 false 확인만으로 각 조건 영향까지 보장되지 않음. |
| `mcdc_condition_coverage` | 확인 | 개별 조건의 true/false 실행이 decision 결과 독립영향과 같지 않음. |
| `mcdc_definition` | 수정 | MC/DC 정의와 전체 구조커버리지의 entry/exit 목표를 분리하도록 source를 수정했다. |
| `mcdc_independent_effect_pair` | 확인 | 대상 조건 변경이 결과를 바꾸는 pair 및 다른 조건의 영향 고정/마스킹 의미 확인. |
| `mcdc_unique_cause` | 확인 | 대상 조건만 바꾸는 unique-cause 방식 확인. |
| `mcdc_masking` | 확인 | 비대상 조건의 값변화가 결과에 영향을 못 주도록 마스킹하는 방식 확인. |
| `mcdc_multiple_condition_coverage` | 확인 | 전체 조합 시험과 MC/DC는 서로 다른 기준이며 조합 수 증가 확인. |
| `mcdc_n_plus_one_limit` | 적용조건 | 단순 논리의 n+1 시험점은 흔한 구성법이지 일반 보장이 아님. |
| `mcdc_short_circuit` | 확인 | Short-circuit 평가 시 실행된 조건과 계측증거를 반영해야 함. |
| `mcdc_coupled_conditions` | 확인 | 종속·반복 조건은 unique-cause 독립변경을 막을 수 있음. |
| `mcdc_masked_inactive_condition` | 확인 | AND/OR의 masking 상태를 pair 선정에 반영. |
| `mcdc_requirements_based_testing_first` | 확인 | 요구 기반 시험을 구조 기반 미실행 분석이 대체하지 않음. |
| `mcdc_coverage_analysis_workflow` | 확인 | 추적 후 report·gap 분석·보완 또는 승인된 정당화 절차 확인. |
| `mcdc_uncovered_code_disposition` | 확인 | 미실행 원인별 처분과 승인·재시험 증거 필요. |
| `mcdc_dead_code` | 확인 | 실제 도달불가·무요구 dead code는 제거와 영향/회귀 확인 대상. |
| `mcdc_deactivated_code` | 확인 | 다른 승인 구성에서 실행 가능한 비활성 코드의 구성·요구·시험 추적 확인. |
| `mcdc_defensive_code` | 확인 | 방어 동작도 derived requirement·오류경로 시험과 safe-state 근거 필요. |
| `mcdc_source_object_coverage` | 적용조건 | Object coverage/equivalence 분석은 표준·개발방식·요구 증거에 따라 결정. |
| `mcdc_compiler_optimization` | 확인 | Compiler option/version 및 object 생성 추적이 source-test 대응에 중요. |
| `mcdc_instrumentation_effect` | 확인 | 계측에 따른 timing·memory·scheduling 영향 및 대표성 확인. |
| `mcdc_coverage_tool_qualification` | 적용조건 | Tool qualification은 오류영향과 독립 검출수단의 충분성에 따라 요구수준 결정. |
| `mcdc_static_analysis_relation` | 확인 | Static analysis는 MC/DC 실행시험을 대체하지 않음. |
| `mcdc_dynamic_analysis_relation` | 확인 | Dynamic test는 실제 실행/계측증거이나 oracle·요구추적은 별도. |
| `mcdc_control_data_flow_complement` | 확인 | Boolean MC/DC로 초기화·data coupling·timing·race 등이 자동 커버되지는 않음. |
| `mcdc_target_environment` | 적용조건 | Target 대표성은 보장수단이며 Host 시험은 차이분석·보완증거가 필요할 수 있음. |
| `mcdc_regression_change` | 확인 | 논리·compiler·tool·library·configuration 변경은 영향범위 regression과 report 갱신 대상. |
| `mcdc_one_hundred_percent_limit` | 확인 | 100% MC/DC는 요구완전성·알고리즘·timing·SIL 전체를 단독 입증하지 않음. |
| `mcdc_industrial_application_boundary` | 확인 | 적용범위는 산업 표준·계획·개발 scope로 결정하며 모든 PLC/HMI에 일률 적용되지 않음. |
| `mcdc_safety_plc_boundary` | 확인 | 인증범위와 Safety Manual이 내부 firmware 증거와 application validation 경계를 정함. |
| `mcdc_lifecycle_vv_boundary` | 확인 | MC/DC는 구조 커버리지 증거 중 하나이며 추적성/V&V를 대체하지 않음. |

## 3. ESD 최종요소와 PST (48)

근거: [IEC 61511-1 미리보기][iec61511], [HSE 제어시스템][hsecontrol], [HSE proof-test 지침][proof1], [HSE 부분시험 예시][proof3], [HSE 기능안전 검사 지침][hseguide]. Vendor 수치·coverage는 해당 제품·구성·시험조건에 종속된다.

| Anchor ID | 판정 | 대조 메모 |
|---|---|---|
| `final_element_role_in_sif` | 확인 | 최종요소는 SIF의 공정 action을 실행하는 하위시스템. |
| `system_sif_sil_context_boundary` | 확인 | Topic ownership을 최종요소 검증에 한정. |
| `safe_state_process_hazard_basis` | 확인 | Fail-close/open는 process hazard 기준을 대체하지 않음. |
| `deenergize_to_trip_energy_philosophy` | 확인 | De-energize-trip이 모든 process에서 자동으로 안전한 것은 아님. |
| `final_element_subsystem_boundary` | 확인 | Output부터 요구된 공정결과 달성까지 구성품·interface 반영. |
| `valve_actuator_solenoid_architecture` | 확인 | Valve/actuator/solenoid/indication/utility 및 failure mode 분리 확인. |
| `utility_supply_and_shared_dependencies` | 확인 | 전원·공압·유압·배기·환경은 dependency/CCF 경계에 포함. |
| `trip_signal_and_output_chain` | 확인 | Logic 출력에서 process outcome까지 end-to-end 추적. |
| `dangerous_failure_modes` | 확인 | 이동불가·방향/시간/격리 미달 등은 duty-specific dangerous failure가 될 수 있음. |
| `safe_failure_and_spurious_trip` | 확인 | Safe failure와 nuisance trip의 운영·secondary consequence 구분. |
| `hidden_stuck_failure` | 확인 | 잠복 고장 및 proof-test 진단 필요 확인. |
| `seat_leakage_as_safety_requirement` | 확인 | 허용 누설은 SRS/process hazard에 따라 요구됨. |
| `actuator_force_margin_handoff` | 확인 | 기계설계 자체와 SIF acceptance 연결의 Topic boundary 확인. |
| `fail_action_vs_safe_state` | 확인 | 기계 fail-action과 공정 safe state는 별도 정의. |
| `failure_rate_partition_dd_du_sd_su` | 확인 | Mode·diagnostic 가정과 failure-rate 구분 일치 필요. |
| `low_demand_pfdavg_contribution` | 확인 | 단순식은 low demand·시험·coverage 등의 가정 아래 적용. |
| `high_continuous_demand_pfh_contribution` | 확인 | 고요구/연속 PFH와 저요구 PFD 식을 혼용하지 않음. |
| `series_subsystem_pfd` | 확인 | 직렬 SIF subsystem 조합과 독립성·근사 가정 확인. |
| `final_element_budget_allocation` | 확인 | Component SIL label 대신 전체 SIF의 budget 기여 평가. |
| `diagnostic_coverage_definition` | 확인 | DC를 관련 dangerous failure detection으로 정의하고 latency/action 고려. |
| `proof_test_coverage_definition` | 확인 | PTC는 DU failure mode와 test step 증거 관계. |
| `pst_coverage_definition` | 적용조건 | PST coverage는 vendor 값 단독 채택 불가; 해당 configuration·failure set 확인. |
| `pst_detectable_failure_set` | 적용조건 | 검출 가능한 sticking/actuator/feedback failure는 PST architecture·procedure에 따라 다름. |
| `pst_not_full_proof_test` | 확인 | Partial test가 full travel·seat leakage 등 모든 mode를 증명하지 않음. |
| `full_stroke_proof_test_scope` | 적용조건 | 실제 시험범위는 SRS·failure mode·안전한 시험절차에 맞춰 정의. |
| `test_interval_and_repair_time` | 확인 | PFD는 시험·진단·수리·복구의 가정에 좌우됨. |
| `imperfect_test_residual_risk` | 확인 | 불완전 coverage의 잔여 DU와 mission time 반영. |
| `proof_test_procedure_repeatability` | 확인 | 시험 전제·수용기준·복구·독립확인 기록의 재현성. |
| `response_time_process_safety_time` | 확인 | SRS/process safety time 제약과 worst-case margin. |
| `component_response_time_sum` | 확인 | 간단한 serial screening과 dynamic package 측정의 구분. |
| `worst_case_trip_time` | 확인 | 실제 worst credible 조건에서 시간 승인 확인. |
| `deenergized_energized_test_condition` | 확인 | Manual stroke만으로 전기·utility trip chain 전체를 증명하지 않음. |
| `bypass_override_inhibit_controls` | 확인 | 우회·inhibit 시 위험저감 감소와 보상조치 관리. |
| `impairment_alarm_and_permit` | 확인 | 시험·불능 중 impairment를 알리고 위험기반 임시대책 적용. |
| `restoration_independent_verification` | 확인 | 시험 후 normal state와 bypass 제거 확인. |
| `common_cause_beta_factor_context` | 확인 | Beta-factor는 방법 중 하나이며 값은 현장 근거 필요. |
| `redundancy_independence_boundary` | 확인 | Redundancy credit은 독립성·CCF 평가가 필요. |
| `shared_air_power_environment` | 확인 | Shared utility·환경·정비 오류가 동시고장을 야기할 수 있음. |
| `partial_stroke_test_risk_controls` | 적용조건 | PST 위험과 permissive/abort/복구대책은 밸브·공정·PST 설계에 맞춤. |
| `pst_interval_and_online_demand_exposure` | 확인 | PST 간격의 위험저감과 운영부담 trade-off 확인; 최적점은 현장별. |
| `diagnostic_credit_validation` | 확인 | 진단 credit은 detectable set·latency·repair·test interaction 근거 필요. |
| `valve_signature_pst_handoff` | 확인 | Topic ownership은 본 repository의 cross-topic 계약으로 확인. |
| `proof_test_records_traceability` | 확인 | 시험 결과·고장·수리·복구 추적은 운영 증거로 필요. |
| `fmeca_fmeda_vendor_data_assumptions` | 확인 | FMEDA 적용성은 제품·환경·구성·시험가정에 종속. |
| `systematic_capability_software_procedure` | 확인 | PFD 숫자만으로 systematic capability가 증명되지 않음. |
| `maintenance_moc_spares` | 적용조건 | 단순 like-for-like 조치와 안전기능/설계가정 영향 변경을 MOC impact assessment로 구분해야 함. 원문은 재검증을 일률 요구하는지 해석에 주의. |
| `acceptance_criteria_and_srs_traceability` | 확인 | acceptance 기준·test condition·측정 불확도 및 SRS 추적. |
| `lifecycle_closed_loop_reverification` | 확인 | 운전 고장·시험 자료를 failure assumption과 lifecycle 개선으로 환류. |

## 4. HIPPS (25)

근거: [HSE loss-of-containment/IPS 지침][hseips], [HSE 제어시스템][hsecontrol], [HSE relief system 지침][relief], [IEC 61511-1 미리보기][iec61511]. HIPPS 적용이 압력용기 relief 법규/코드 요구를 보편적으로 대체한다는 뜻은 아니다.

| Anchor ID | 판정 | 대조 메모 |
|---|---|---|
| `hipps_definition` | 확인 | HIPPS/IPS의 위험상태 방지·차단 기능 확인. |
| `hipps_not_relief_device` | 확인 | Instrumented isolation과 압력 방출은 원리·failure mode가 다름. |
| `hipps_application_boundary` | 확인 | 낮은 압력 정격 설비를 보호하는 overpressure scenario 적용 예. |
| `hipps_sif_end_to_end_boundary` | 확인 | Sensor–logic–final element 및 utility/test/bypass까지 기능경계. |
| `hipps_trip_setpoint_margin` | 확인 | Setpoint는 계기오차·transient·closing response margin 포함. 수치는 scenario별. |
| `hipps_process_safety_time` | 확인 | 총 응답시간을 PST와 비교해야 함. |
| `hipps_two_out_of_three_sensing` | 확인 | 2oo3 voting의 대표적인 availability/false trip trade-off. |
| `hipps_two_out_of_three_limits` | 확인 | 공유 tap·utility·환경·정비 등 CCF가 단순 channel 수 이점을 제한. |
| `hipps_degraded_voting_mode` | 확인 | Bypass/fault channel 때 degraded logic을 SRS에 정의해야 함. |
| `hipps_one_out_of_two_final_elements` | 확인 | 단일 밸브만으로 요구 유량차단이 이뤄지는 경우에 한해 1oo2 성공구조 해석 가능. |
| `hipps_one_out_of_two_condition` | 확인 | Double-block/누설 요구가 둘 다 필요하면 성공 논리 재정의. |
| `hipps_architecture_not_universal` | 확인 | 2oo3+1oo2는 예이며 risk·demand·spurious trip·maintenance로 선정. |
| `hipps_logic_solver_role` | 확인 | Voting·latch·output·fault/reset 행동은 SRS에 따라야 함. |
| `hipps_final_element_chain` | 확인 | Valve만이 아닌 actuator·pilot·utility·feedback을 포함해 검증. |
| `hipps_fail_safe_energy` | 확인 | Power/utility 상실 때 요구 safe-state 도달 여부 확인. |
| `hipps_closure_time_and_surge` | 확인 | Closing profile은 PST와 surge/water hammer 등 공정영향을 같이 검토. |
| `hipps_tight_shutoff_and_leakage` | 확인 | Shutoff class·누설·downstream pressure criteria는 SRS와 scenario별. |
| `hipps_pfdavg_allocation` | 확인 | 센서·로직·최종요소·CCF·진단·시험으로 전체 SIF PFDavg 검토. |
| `hipps_target_vs_achieved_sil` | 확인 | 요구 Target과 검증된 Achieved를 구분. |
| `hipps_independence_from_bpcs` | 확인 | IPL credit 전 initiating cause/공유 요소와 독립성 평가. |
| `hipps_relief_system_comparison` | 확인 | 방출형 relief와 유입 차단 HIPPS의 기능축을 구분. |
| `hipps_relief_replacement_boundary` | 적용조건 | 대체성은 관할 code·법규·시나리오와 잔여 과압원 검토에 한정. 보편 대체 규칙 아님. |
| `hipps_coexistence_and_selection` | 적용조건 | 병행 여부·경제성은 위험·법규·방출결과와 현장 운영조건에 따라 결정. |
| `hipps_proof_test_and_bypass` | 확인 | 부분시험/full test 구간·우회 관리 및 복구를 운영에서 보장. |
| `hipps_srs_moc_revalidation` | 적용조건 | SRS 변경은 영향분석을 거쳐 안전 요구에 영향을 주는 경우 관련 SRS/검증 단계 갱신. |

## 5. OT 사이버보안 (40)

근거: [NIST SP 800-82 Rev.3][nist82], [ISA/IEC 62443-3-2 공개 미리보기][isa62443], [CISA OT 보안 자료][cisa]. NIST Rev.4는 2026-09-21 공개 초안이므로 이번 판정은 최종 Rev.3와 ISA/IEC 공개 범위에 기초한다. NIST/ISA의 권고를 모든 관할의 법정 최소요건으로 표현하지 않는다.

| Anchor ID | 판정 | 대조 메모 |
|---|---|---|
| `sw09_security_objectives` | 확인 | OT 보안은 safety·availability·reliability 영향을 함께 고려. |
| `sw09_asset_inventory` | 확인 | OT asset/account/path의 식별과 최신 inventory 권고 확인. |
| `sw09_criticality_classification` | 확인 | Criticality와 영향평가로 우선순위·대응을 정함. |
| `sw09_risk_assessment` | 확인 | Threat/vulnerability/consequence·safeguard·residual risk의 risk-based 평가. |
| `sw09_system_under_consideration` | 확인 | SUC 범위와 trust/data boundary 정의. |
| `sw09_zone_conduit` | 확인 | Zone/conduit의 위험기반 partition 및 통신제한. |
| `sw09_segmentation` | 확인 | Segment는 lateral movement와 blast radius를 줄이되 제어요구를 고려. |
| `sw09_industrial_dmz` | 확인 | IT/OT 중계와 직접 경로 축소는 architecture-dependent design pattern. |
| `sw09_firewall_policy` | 확인 | Default deny·최소 허용은 권고; legacy/process별 검증과 예외가 필요. |
| `sw09_unidirectional_gateway` | 확인 | 단방향 요구에는 유용하나 반환통신과 운영요구 별도 설계. |
| `sw09_ids_ips_monitoring` | 확인 | 탐지/차단 보조수단과 process-safe tuning 필요. |
| `sw09_allowlisting` | 확인 | 승인 실행목록과 업데이트/비상변경 통제 권고. |
| `sw09_least_privilege` | 확인 | 최소권한·기간·review 원칙 확인. |
| `sw09_authentication` | 확인 | 사용자·장치·서비스 식별 및 계정관리 원칙. |
| `sw09_authorization` | 확인 | 인증 후 resource/action 제한과 duties separation. |
| `sw09_remote_access` | 확인 | 원격접속 승인·범위·기간·경로 통제 권고. |
| `sw09_jump_server` | 확인 | 중계 호스트 강화·credential 분리·session 관리 권고. |
| `sw09_mfa` | 확인 | MFA는 account takeover 위험을 낮추지만 다른 authorization controls 대체 아님. |
| `sw09_secure_remote_session` | 적용조건 | 암호화·승인·최소권한·감사로그는 risk-based 통제. 모든 장치/작업에서 동일한 session recording을 일률 요구하지 않음. |
| `sw09_patch_management` | 확인 | Patch 우선순위에 exploit·safety·availability·시험·rollback 포함. |
| `sw09_vulnerability_management` | 확인 | 식별부터 검증·완화·예외·종결 증거까지 관리. |
| `sw09_legacy_compensating_control` | 확인 | Patch/MFA 미지원 자산에는 위험기반 compensating control 고려. |
| `sw09_secure_configuration_baseline` | 확인 | 승인 baseline과 drift 확인의 목적·내용 확인. |
| `sw09_security_change_control` | 확인 | 보안 변경도 access/rule/log/rollback/exception 영향평가. |
| `sw09_supply_chain_risk` | 확인 | Supplier/component/update/service dependency를 공급망 위험으로 관리. |
| `sw09_supplier_assurance` | 확인 | 지원·취약점 disclosure·provenance·EOL 책임은 공급계약으로 증거화. |
| `sw09_sbom` | 확인 | SBOM은 성분 식별이며 exploitability/config/runtime/authenticity 검증 대체 아님. |
| `sw09_software_firmware_integrity` | 확인 | Trusted source·서명/hash·전송·version·rollback 및 설치 검증. |
| `sw09_removable_media` | 확인 | 승인·검사·기록·격리·폐기 통제 권고. |
| `sw09_logging` | 확인 | 보안·설정·접속 event에 식별/결과 기록을 연결. |
| `sw09_time_synchronization_forensics` | 확인 | 공통 시각과 clock 상태는 사건순서 분석에 중요. |
| `sw09_detection_triage` | 확인 | 여러 신호 correlation 후 severity·scope·safety impact 판단. |
| `sw09_incident_response_plan` | 확인 | 역할·연락·권한·안전조정·증거처리 사전정의. |
| `sw09_containment_eradication` | 확인 | 확산 차단과 persistence 제거를 운전안전 영향과 함께 계획. |
| `sw09_trusted_recovery` | 확인 | 검증된 baseline·backup·credential·staged restore의 recovery sequence. |
| `sw09_backup_recovery_security` | 확인 | Offline/immutable·분리credential·restore test는 권고수단이며 threat model에 맞춤. |
| `sw09_business_continuity` | 확인 | 수동/감소운전·통신대안·안전정지·회복 우선순위 계획. |
| `sw09_safety_coordination` | 확인 | Cyber 대응에서 승인 없이 SIS를 우회/비활성화하지 않고 safety authority와 조정. |
| `sw09_exercise_metrics` | 추가근거 | MTTD/MTTC는 조직별 start/stop 정의가 다를 수 있다. 원문의 incident 선언 또는 탐지 시점 중 기준을 하나 정하고 timestamp source를 규정해야 지표 비교 가능. |
| `sw09_lifecycle_decommissioning` | 확인 | 폐기 때 자격증명·인증서·경로·데이터·inventory 제거/갱신. |

## 6. 산업 AI·예지보전 (20)

근거: [NIST AI RMF 1.0 Core][airmf], [NIST AI RMF Measure][airmfmeasure], [scikit-learn metrics][skmetrics], [시계열 분할 문서][timesplit]. NIST AI RMF는 자발적 위험관리 프레임워크이고 구체적인 성능지표 선택은 작업·위험·현장에 맞춘다.

| Anchor ID | 판정 | 대조 메모 |
|---|---|---|
| `ai_ml_dl_hierarchy` | 확인 | AI/ML/DL의 상하위 개념 관계 확인. |
| `supervised_learning` | 확인 | Label 데이터로 input-target mapping을 학습. |
| `unsupervised_learning` | 확인 | Label 없이 structure/cluster/normal pattern을 찾을 수 있지만 현장평가 필요. |
| `task_type_selection` | 확인 | 분류/연속값 예측/시간예측은 target과 decision에 맞춤. |
| `anomaly_detection_score_threshold` | 확인 | Anomaly score·threshold는 이상도이며 root-cause 확정이 아님. |
| `predictive_maintenance_scope` | 확인 | 예측정비는 정비 의사결정을 지원하고 고장 제거 보장은 아님. |
| `remaining_useful_life_uncertainty` | 확인 | RUL은 고장기준·조건에 대한 추정이며 uncertainty 필요. |
| `process_optimization_boundary` | 확인 | Optimization은 안전제약·승인·supervisory 경계에 종속. |
| `feature_engineering_context` | 확인 | Feature는 예측 시점의 가용정보로 만들어 미래정보 누출 방지. |
| `representative_data` | 확인 | 데이터의 현장 대표성·Label·결측·운전조건 확인. |
| `train_validation_test_separation` | 확인 | 학습·선택·최종시험 데이터 역할 분리. |
| `chronological_group_split` | 확인 | 시계열/설비 Episode 혼합 leakage 방지; split 방법은 데이터 구조에 맞춤. |
| `data_leakage` | 확인 | 예측시점 이후 정보나 중복사건 혼입으로 시험성능이 낙관 편향될 수 있음. |
| `class_imbalance` | 확인 | 희소 고장에서는 Accuracy 단독 한계; PR·비용 등 추가 평가. |
| `confusion_matrix` | 확인 | TP/FP/TN/FN은 binary classification 결과를 구분. |
| `precision_metric` | 확인 | Precision = TP/(TP+FP). |
| `recall_metric` | 확인 | Recall = TP/(TP+FN). |
| `f1_metric` | 확인 | F1은 precision/recall의 조화평균이며 operation cost 대체 아님. |
| `false_alarm_miss_tradeoff` | 확인 | Threshold 조정으로 miss와 false alarm trade-off를 운전비용에 맞춤. |
| `decision_cost_and_lead_time` | 적용조건 | Model metric 외에도 lead time·actionability·downtime·확인부하를 업무 목적에 맞춰 평가. |

## 수정 및 미확정 사항

이번 배치에서 확인된 수정 1건은 `mcdc_definition`이다. 전체 MC/DC coverage 기준과 MC/DC criterion의 정의를 분리했다. OT `sw09_exercise_metrics`는 MTTC 시계 시작점을 일관되게 정할 추가 근거가 필요해 source를 고치지 않았다. 최종요소의 `maintenance_moc_spares`, HIPPS의 relief replacement/SRS 변경, OT 접속기록 방식 등은 영향도와 표준·site 조건이 달라 위험기반 적용으로 표시했다.

## 누적 진행

이전 검토 67개에 이번 200개를 더해 **267 / 2,073개**가 Anchor별로 기록되었다. 현재 미검토는 **1,806개**다. 이 배치의 source 수정은 MC/DC 한 건이며 generated bank는 공식 builder로 다시 생성한다.

[iec61511]: https://webstore.iec.ch/en/iec_catalog/product/preview/?id=L3B1Yi9wZGYvcHJldmlldy9pbmZvX2llYzYxNTExLTF7ZWQyLjB9Yi5wZGY%3D
[hsefs]: https://www.hse.gov.uk/eci/functional.htm
[hsecontrol]: https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm
[proof1]: https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf
[proof3]: https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix3.pdf
[hseguide]: https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf
[faa]: https://www.faa.gov/airports/resources/advisory_circulars/index.cfm/go/document.information/documentNumber/20-115D
[nasamcdc]: https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695692/7.21%2B-%2BMulti-condition+Software+Requirements
[hseips]: https://www.hse.gov.uk/offshore/assets/docs/inspection-of-loss-of-containment.pdf
[relief]: https://www.hse.gov.uk/comah/sragtech/techmeasventsyst.htm
[nist82]: https://csrc.nist.gov/pubs/sp/800/82/r3/final
[isa62443]: https://www.isa.org/getmedia/661c718f-8e64-446d-acf9-2c6286db1b33/isa-62443-3-2-preview.pdf
[cisa]: https://www.cisa.gov/topics/industrial-control-systems
[airmf]: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
[airmfmeasure]: https://airc.nist.gov/airmf-resources/playbook/measure/
[skmetrics]: https://scikit-learn.org/stable/modules/model_evaluation.html
[timesplit]: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
