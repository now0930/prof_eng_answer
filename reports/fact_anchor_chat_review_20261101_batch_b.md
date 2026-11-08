# Fact Anchor 기술사 적합성·근거 대조 — Batch B (2026-11-01)

## 기준과 판정 효력

- 작업 브랜치: `codex/essay-boundary-calibration-20261028`. 기준 행: `reports/remaining_fact_current_queue_20261030.csv`에 있는 Fact ID. 현행 `Registry=1,520`과 역사적 `1,272건: 제거 2·유지 5·미확인 1,265` 수치는 유지.
- 이번 개별 검토 ID: **56건**. 판정 현황: HOLD_SPECIFIC_CLAUSE 4; CORE_CONDITIONAL 23; CORE_SUPPORTED 25; SUPPLEMENT_ONLY 4.
- 이 보고서는 **채점 적합성 및 공개 1차/공식 자료와의 범위 대조**이다. `CORE_SUPPORTED`도 종전 승인 등록이나 source 변경을 자동 뜻하지 않는다. 출처가 단지 스펙 범위 설명인 경우 표준 세부조항을 직접 인증하지 않는다.
- `SUPPLEMENT_ONLY`: 사실일 수 있으나 기종·프로젝트별 세부 사례는 필수 정답에서 제외하는 권고. `HOLD_SPECIFIC_CLAUSE`: 공개된 규격 소개로 입증 못 하는 구체 조항이므로 채점 근거로 사용 금지. `CORE_CONDITIONAL`: 필수 원리는 유지하되 적용 조건을 질문 요구범위와 일치시킨다.
- 이 단계는 **보고서 추가만 허용**. Registry, Topic Pack, Logic, 생성물, `verified` 상태, 배점은 그대로다. 제거/등급 조정은 사용자 승인이 없어도 기술 근거, 평가 요구축, 로컬 CLI 생성 및 회귀 검증이 마련되기 전까지 실행하지 않는다.

## 개별 검토 — 원문 Fact ID별

| Fact ID | 채점 권고 | 기술 판단·제한 조건 |
|---|---|---|
| `iec62382_control_stroke_intermediate_points_and_hysteresis_checks` | `HOLD_SPECIFIC_CLAUSE` | 공개 IEC 초록으로 Annex A.4의 25/50/75% 수치/왕복 시험을 직접 검증 불가; 일반 의무로 승격 금지 |
| `iec62382_loop_check_exercises_individual_and_combined_loop_components` | `CORE_CONDITIONAL` | Loop Check 범위는 IEC 초록에서 확인되지만 모든 부품을 한 번의 시험으로 함께 확인한다는 고유 정의는 본문 추가 대조 필요 |
| `iec62382_actuator_failure_simulation_verifies_configured_reaction` | `HOLD_SPECIFIC_CLAUSE` | Annex A.4 고유 예시를 유료 원문 없이 확인 불가; fail position은 설치 요구에 따름 |
| `iec62382_end_to_end_loop_check_is_not_sis_validation` | `HOLD_SPECIFIC_CLAUSE` | Loop Check와 SIS Validation은 개념상 별도이나 'IEC 62382가 명시적으로 SIS 검증을 제외'한다는 조항은 공개 초록에서 미확인 |
| `hazop_lopa_lopa_frequency_equation` | `CORE_CONDITIONAL` | 독립성·같은 시나리오·조건부 확률을 확인한 경우 시작 빈도와 IPL PFD의 곱을 사용 |
| `hazop_lopa_ipl_definition` | `CORE_SUPPORTED` | 특정 시나리오에서 결과 방지·완화 기능과 독립성, 검증 가능성이 확인된 보호계층 |
| `hazop_lopa_ipl_independence` | `CORE_SUPPORTED` | 시작 사건 및 다른 보호계층으로부터의 독립성, 공통원인·공유 설비 검토 필요 |
| `hazop_lopa_required_rrf` | `CORE_CONDITIONAL` | 동일 종점·시간단위에서 기존 보호 후 빈도/허용 빈도; 허용빈도 0 또는 정의 누락 사례 제외 |
| `hazop_lopa_pfdavg_rrf_relation` | `CORE_CONDITIONAL` | 저요구 모드 및 유효 위험감소 배정 가정에서 PFDavg 목표와 RRF의 역수 관계 |
| `hazop_lopa_sil_band_mapping` | `CORE_SUPPORTED` | SIL1 1e-2~1e-1, SIL2 1e-3~1e-2, SIL3 1e-4~1e-3 (상한 미포함) |
| `hazop_lopa_target_vs_achieved_sil` | `CORE_SUPPORTED` | 위험평가에서 요구 SIL을 정의하고 설계된 SIF의 검증 성능·구조·시스템적 능력을 별도로 확인 |
| `hazop_lopa_sif_allocation_boundary` | `CORE_CONDITIONAL` | 센서·로직·최종요소, 안전상태·응답시간 등 해당 SIF의 기능경계 정의; 모든 예시 필드의 무조건 필수화 금지 |
| `hazop_lopa_hazop_role` | `CORE_SUPPORTED` | HAZOP은 Deviation/원인/결과/보호수단 식별; 목표 SIL 계산과 구별 |
| `hazop_lopa_initiating_event_frequency` | `CORE_SUPPORTED` | 시나리오와 관측·통계 적용 경계를 명시한 시작사건 발생빈도 |
| `hazop_lopa_enabling_and_conditional_modifiers` | `CORE_CONDITIONAL` | CCPS가 시나리오 적합성·위험기준·데이터 및 이중계산 금지를 명시 |
| `hazop_lopa_ipl_dependability_auditability` | `CORE_SUPPORTED` | IPL에는 신뢰성과 감사가능성이 요구되고 정비·시험 등의 근거를 유지 |
| `hazop_lopa_consequence_without_credited_protection` | `CORE_SUPPORTED` | 보호계층 효과의 순환 포함/중복 계산을 피해야 함 |
| `hazop_lopa_tolerable_event_frequency` | `CORE_CONDITIONAL` | 허용 위험기준은 승인된 사업장/규제 기준을 따른다; 보편적 수치 없음 |
| `hazop_lopa_ipl_specificity` | `CORE_SUPPORTED` | 일반적 교육·좋은 설계 자체는 특정 시나리오의 독립 IPL 성능 증명이 아님 |
| `hazop_lopa_no_double_counting` | `CORE_SUPPORTED` | 공유 센서·로직·최종요소/유틸리티의 종속성이 있으면 IPL PFD를 독립적으로 중복 곱하지 않음 |
| `hazop_lopa_common_cause_dependency` | `CORE_SUPPORTED` | 공통전원·탭·소프트웨어·정비 등 공통원인/종속성 검토 |
| `hazop_lopa_bpcs_ipl_credit` | `CORE_CONDITIONAL` | BPCS가 원인/공통 기능이면 IPL 중복 credit 제한; 입증된 독립 보호만 적용 |
| `hazop_lopa_alarm_operator_ipl` | `CORE_CONDITIONAL` | 경보+작업자 대응의 충분한 시간, 인지·조치능력, 독립·감사가능성 확인; 일률 시간기준 금지 |
| `hazop_lopa_residual_frequency_after_existing_ipls` | `CORE_SUPPORTED` | 기존 IPL 적용 후 잔여 위험을 동일 허용기준과 비교 |
| `hazop_lopa_no_additional_sif_when_ratio_below_one` | `CORE_CONDITIONAL` | 특정 시나리오가 위험기준 만족하더라도 다른 시나리오/ALARP/별도 의무는 남음 |
| `thermocouple_temperature_measurement_chain` | `CORE_SUPPORTED` | 두 재료 기전력과 기준접점 정보를 이용한 온도 환산 |
| `thermocouple_seebeck_effect_dissimilar_conductors` | `CORE_SUPPORTED` | 재료별 온도의존 Seebeck 특성으로 전압-온도 비선형 |
| `thermocouple_measures_temperature_difference` | `CORE_SUPPORTED` | 절대온도 추정에 기준접점 온도 필요 |
| `thermocouple_reference_junction_compensation` | `CORE_SUPPORTED` | 기준접점 온도에 대응하는 전압 보정; 단자 온도 불균일 시 오차 |
| `thermocouple_law_of_intermediate_temperatures` | `CORE_CONDITIONAL` | 동일 재료쌍/균질성에서 E(T1,T3)=E(T1,T2)+E(T2,T3) 성립 |
| `thermocouple_nonlinearity_reference_tables_polynomial_conversion` | `CORE_SUPPORTED` | 열전대 종류와 온도 범위에 대응하는 ITS-90 기준함수·표 사용 |
| `rtd_pt100_reference_resistance_alpha_standard` | `CORE_CONDITIONAL` | Pt100 0°C의 공칭 100Ω; α≈0.00385/°C. 0.003851은 근삿값이며 다른 규격 RTD와 구분 |
| `rtd_callendar_van_dusen_characteristic` | `CORE_SUPPORTED` | 0°C 위 2차, 아래 C(T−100)T³ 항 추가; 표준·적용 온도 범위·계수 확인 |
| `rtd_excitation_voltage_measurement` | `CORE_SUPPORTED` | 외부 여기 전류/전압 기반 R=V/I; 도선·자기발열 오차 확인 |
| `rtd_self_heating_thermal_error` | `CORE_SUPPORTED` | P=I²R Joule 발열과 주변 열전달로 자기발열 오차 발생 |
| `rtd_two_wire_lead_resistance_error` | `CORE_SUPPORTED` | 2선 경로 저항 합산과 양의 RTD 온도계수에서 온도 상승 방향 오차 |
| `rtd_three_wire_bridge_compensation_assumptions` | `CORE_SUPPORTED` | 3선 회로의 보상은 특정 배선회로와 도선저항 균형을 전제; 잔류오차 존재 |
| `rtd_four_wire_kelvin_measurement` | `CORE_SUPPORTED` | Force/Sense 분리와 고입력 임피던스로 전류 리드 전압강하 영향을 줄임 |
| `thermocouple_extension_compensating_wire_polarity` | `CORE_CONDITIONAL` | 극성·보상선 종류·허용 온도 범위가 중요한 일반 원리; 특정 합금 제품 나열 금지 |
| `rtd_measurement_chain_passive_sensor` | `CORE_SUPPORTED` | RTD는 저항값이 온도에 따라 변하는 수동 소자이며 외부 여기가 필요 |
| `rtd_metal_resistance_temperature_principle` | `CORE_SUPPORTED` | 금속 저항 온도의존성을 이용하며 백금 재료의 안정성·사용 범위는 사용 조건에 따름 |
| `rtd_transmitter_connection_signal_conditioning` | `SUPPLEMENT_ONLY` | 특정 장치의 진단·절연·통신 기능은 일반 센서 원리와 분리 |
| `rtd_wiring_method_selection_tradeoff` | `CORE_CONDITIONAL` | 요구 정확도·비용·리드저항·회로 구성에 따라 2/3/4선 선택; 항상 4선이 의무 아님 |
| `thermocouple_junction_construction_response_isolation` | `SUPPLEMENT_ONLY` | 접지/비접지/노출의 응답·잡음 영향은 구조·직경·유체환경에 좌우; 절대 응답속도 순위 의무 금지 |
| `thermocouple_thermowell_installation_dynamic_error` | `CORE_CONDITIONAL` | 열접촉·삽입·열전달·열용량이 응답과 오차에 영향; 개별 보호관/기하 조건은 보조 |
| `thermocouple_signal_conditioning_noise_grounding` | `CORE_CONDITIONAL` | 작은 전압에 잡음/접지 영향, CJC·증폭·선형화 기본 기능; 특정 제품 진단/통신은 선택적 |
| `rtd_channel_fault_checks_are_topology_and_device_dependent` | `SUPPLEMENT_ONLY` | 진단 기능·고장 검출 지원 범위는 제품 고유; 모든 장치의 필수 기능이나 정답 나열로 채점 금지 |
| `lopa_scenario_outputs_trace_into_srs_function_and_integrity_requirements` | `CORE_CONDITIONAL` | LOPA 위험감소 요구와 SRS 상세 기능요건을 구분; 상세 항목 모두를 LOPA 직접 산출물로 요구하지 않음 |
| `shared_sif_scenarios_and_assumption_changes_require_reassessment` | `CORE_CONDITIONAL` | 하나의 SIF 공유 시 누적 수요와 위험감소 검토; 변경 영향이 있으면 관련 검증·문서 갱신, 모든 변경에 전면 재평가 강제 금지 |
| `rtd_calibration_uncertainty_depends_on_reference_bath_readout_and_sensor_application_effects` | `CORE_CONDITIONAL` | 교정 소급성·온도원·측정불확도·삽입·자기발열 등 실제 유의한 항목만 평가; 모든 정해진 교정점 수 의무 아님 |
| `thermocouple_loop_diagnostics_are_device_and_symptom_specific` | `SUPPLEMENT_ONLY` | 증상별 진단은 유용하지만 제품별 단선감지 등 세부 기능을 필수 Fact에서 제외 |
| `thermocouple_type_and_probe_construction_selection_scope` | `CORE_CONDITIONAL` | 열전대 형식·온도 범위·환경을 함께 검토; 형식만으로 모든 사용 조건 결정 불가 |
| `thermocouple_calibration_uncertainty_is_method_specific` | `CORE_CONDITIONAL` | 교정법·온도원·기준·접점·열기전력 등 실제 관련 불확도만 반영; 고정 목록 암기 불필요 |
| `maintenance_program_separates_routine_inspection_and_functional_checks` | `CORE_CONDITIONAL` | 외관/배선 점검과 동작/기능검증의 목적 구분. 구체 절차·시험항목은 설비 및 적용 사업장 기준에 따름 |
| `iec62382_control_stroke_up_down_detects_hysteresis_only` | `HOLD_SPECIFIC_CLAUSE` | Annex A.4 고유 서술 미확인; 왕복 stroke 차이를 stiction 단독 원인으로 진단할 수는 없음 |
| `iec62382_loop_check_scope_and_boundaries` | `CORE_CONDITIONAL` | IEC의 공개 범위는 설치/배선 검사 후 냉간 시운전 전 Loop Check; 모든 공정 제어 loop 물리적 전 구간의 동시시험 의무는 아님 |

## 근거 범위 (공개 원문)

1. **LOPA (23건)** — [CCPS/AIChE LOPA 기본 정의·속성](https://ccps.aiche.org/resources/tools/lopa), [CCPS 조건부 수정인자 사용 제한](https://ccps.aiche.org/resources/tools/lopa/when-when-not-use-enabling-conditions-conditional-modifiers), [ISA: LOPA 위험빈도·SIL 계산](https://www.isa.org/intech-home/2016/january-february/features/safety-instrumented-system-sil-calculation), [ISA: 복수 수요 시나리오 및 IPL 독립성](https://www.isa.org/intech-home/2022/december-2022/departments/creating-a-lopa-project-report). SIL PFDavg 밴드는 [TÜV SÜD IEC 61508 요약](https://www.tuvsud.com/ko-kr/services/functional-safety/iec-61508)·[ADI 기능안전 자료](https://www.analog.com/en/resources/analog-dialogue/raqs/raq-issue-226.html)로 교차 대조. **IEC 61508/61511 전체 조항 자체를 열람한 것은 아님**.
2. **RTD (13건)** — [IEC 60751:2022 공개 적용범위](https://webstore.iec.ch/en/publication/63753), [NI RTD·Callendar–Van Dusen 기술 설명](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000x1rnCAA), [NI 2/3/4-wire 차이](https://www.ni.com/docs/en-US/bundle/ni-dmm/page/resistance-temperature-detector-rtds_7.html). Pt100/α 값은 **근삿값**이며 특정 제조사 교정 계수와 구별.
3. **열전대 (13건)** — [NIST 열전대 물리원리](https://www.nist.gov/pml/sensor-science/thermodynamic-metrology/mercury-thermometer-alternatives/mercury-thermometer-5), [NI CJC 설명](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000P6wvSAC&l=en-US), [NI CJC 계산](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000kHQNSA2&l=en-US). 온도계수·접점 보정의 열기전력 합산과 비선형 보정은 물리 관계를 중심으로 평가; 특정 부속품·모듈 스펙은 참고.
4. **IEC 62382 및 Loop Check (7건)** — [IEC 62382:2024 공식 Scope](https://webstore.iec.ch/en/publication/67573). 공개 소개는 loop check의 공사·시험 범위와 프로젝트별 적응을 확인하지만 Annex A.4 원문, 25/50/75% 점검점, SIS validation 명시 제외 조항은 확인하지 못함. 이를 규격 고유 의무로 인용한 네 개 Fact는 명시적 `HOLD_SPECIFIC_CLAUSE`.

## 실행·추적 경계

- 이전 보고서 `reports/fact_anchor_chat_review_20261101.md`의 첫 배치 20건과 **중복하지 않는 추가 검토 56건**.
- 원본 registry를 바꾸지 않았으므로 원래 Queue의 `UNREVIEWED`를 임의로 변경하지 않았다. 근거 대조의 효력은 이 Chat 검토 보고서에 한정.
- 다음 우선순위: P0의 일반 원리 위주 ① 균압 Trim ② OT 변경/형상 관리 ③ loop check 고유 표준조항. 기존 선별 모델 결과는 채점 Fact 인증 근거로 사용 금지.
- 로컬 pytest·`validate-all`·`validate_release.sh` 미실행. `main`, 운영 checkout, 컨테이너 변경 없음.
