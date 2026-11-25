# P1-B — 단문화 48건 기술 동등성 검토 (2026-11-25)

- Canonical baseline: `45c7d146e4673e885005c04535e65dc9b9d7c8a5`; manifest: `5a49a7daf042fc4749b9ae137c9af054ff68afae` / blob `38e90d7300ed8b2c5eda2d995a005bd3c785ea15`.
- Registry blob `69124be63df2216e5077a1d74ddfc887503bedd5` (1,524 facts). P1-A exclusion/457 join: [inventory](p1a_fact_anchor_inventory_20261125.md) at `90a441740aa428a017e0e0b07c6ad8653d588acd`.
- Scope: 48/48 individual technical-equivalence recommendations; no repeat independent review of 457. Three bounded review batches (17/12/19). Existing evidence locators and conditions read from Registry, not a fresh independent external source audit. P1-A exclusion join reused; exclusion files not independently rehashed. No Firecrawl.
- APPROVE 20, REVISE 20, HOLD 2, REJECT 6. APPROVE/REVISE are review recommendations only, not authorized canonical edits or scoring admission. REVISE text is a new non-applied draft; where added clarification is present (e.g. saturation exception, stable feedback, equal-angle pulse intervals), P1-C must explicitly validate it against recorded evidence and not treat it as a pure copy edit. HOLD/REJECT retain current canonical. All 5 changed canonical rows REJECT; both existing excluded rows HOLD. No newly approved Fact or score effect.
- P1-C: only 20 original APPROVE proposals and 20 REVISE drafts may be screened as a maximum pool; recheck actual benefit, preserve accepted/rejected explanations, fatal checks, required_anchor_ids, importance, source hashes, owner and Registry relations. No bulk apply. No new IDs/split without separate justification and approval. Existing 119 HOLD/D4/exclusion/A–E authority unchanged. Python grader, pytest, source rehash, validate-all, new Actions: NOT_RUN. Main merge/deploy NOT_RUN.

## Individual results


### 기능안전 신뢰도 모델링: FTA·Markov·RBD·CCF·PFDavg·PFH (`functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh`)

Canonical blob: `d51ce7091a3d1594420d85b6ba0b530e934b78a6`; model_answer blob: `88363564951e6629f18da6469a87965a87eec593`.

#### 1. `fsrm_markov_state_transition` — APPROVE

- 최신 정본: Markov model은 분석할 시스템의 상태와 상태 간 전이확률 또는 전이율을 정의해 상태확률의 변화를 모델링한다. 상태 집합은 분석 경계와 운전·고장거동에 맞춰 정하며, SIS 모델에서는 필요한 경우 정상/운전, 고장·검출, 수리, proof-test, bypass 또는 degraded 상태를 포함할 수 있다. 모든 모델에 공통인 고정 상태 목록이나 반드시 시간변화 전이율을 써야 한다는 뜻은 아니다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: Markov 신뢰도 모델은 분석 목적에 맞춰 정의한 상태와 상태 간 전이확률 또는 전이율로 시스템의 상태확률 변화를 분석한다.
- 판정 이유: 상태·전이확률/율·상태확률의 정의 보존. 고정 상태 목록이나 시간가변율을 요구하지 않음.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `markov_reliability_model_uses_system_states_and_transition_rates_to_track_state_probabilities@1`; status=approved; verification=verified; Registry statement: Markov model은 분석할 시스템의 상태와 상태 간 전이확률 또는 전이율을 정의해 상태확률의 변화를 모델링한다. 상태 집합은 분석 경계와 운전·고장거동에 맞춰 정하며, SIS 모델에서는 필요한 경우 정상/운전, 고장·검출, 수리, proof-test, bypass 또는 degraded 상태를 포함할 수 있다. 모든 모델에 공통인 고정 상태 목록이나 반드시 시간변화 전이율을 써야 한다는 뜻은 아니다.
- Registry 조건: state_space_matches_analysis_boundary_and_system_behavior; transition_parameters_match_the_selected_markov_formulation; sis_operating_test_repair_and_degraded_states_are_included_only_when_relevant
- 직접 요구 문항: 기능안전 시스템의 RBD, FTA와 Markov Model을 비교하고 적용 방법을 설명하시오.
- 정본 source_basis: NASA, Reliability Modeling Method, CR-188288, §2.4 (discrete-state continuous-transition models; state-dependent and time-varying transition rates are model features, not universal requirements): https://ntrs.nasa.gov/api/citations/19940028356/downloads/19940028356.pdf; NASA NTRS, A non-homogeneous Markov model for phased-mission reliability analysis (contrasts generalized time-varying/state-dependent model with standard assumptions): https://ntrs.nasa.gov/citations/19900039580
- 기존 근거 locator (재열람 아님): NASA/CR-1998-207660, Reliability Modeling Method — Markov Modeling and §4.2 single-component model (https://ntrs.nasa.gov/api/citations/19980174903/downloads/19980174903.pdf); Modelling framework for performance analysis of SIS subject to degradation due to proof tests, Reliability Engineering & System Safety — Abstract and model description (https://www.sciencedirect.com/science/article/pii/S0951832019301450)

#### 2. `fsrm_markov_complexity` — HOLD

- 최신 정본: Markov 신뢰도 모델은 구성요소 상태와 상호작용을 포함해 상태공간이 커지면 상태·전이 분석의 계산 및 검증 부담이 증가할 수 있다. 증가 정도는 모델 구조와 분석기법에 따라 달라진다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: Markov 신뢰도 모델은 상태공간이 커지면 모델 구조와 분석기법에 따라 계산·검증 부담이 증가할 수 있다.
- 판정 이유: 조건부 기술 동등성은 있으나 기존 scoring_exclusions 등재 및 직접 요구 문항 없음. 제외 유지.
- P1-C 제안: 현 정본 유지
- 중요도: important; 정본 변경 이력: NO; 제외: fact_anchor_scoring_exclusions_20261101.json; score_effect=none (이번 검토).
- Registry: `markov_state_space_growth_can_increase_analysis_burden_without_universal_growth_rate@1`; status=approved; verification=verified; Registry statement: Markov 신뢰도 모델은 구성요소 상태와 상호작용을 포함해 상태공간이 커지면 상태·전이 분석의 계산 및 검증 부담이 증가할 수 있다. 증가 정도는 모델 구조와 분석기법에 따라 달라진다.
- Registry 조건: burden_depends_on_model_structure_and_solution_method; no_universal_growth_rate_is_asserted
- 직접 요구 문항: required_anchor_ids 직접 연결 없음 (다른 경로의 채점 적격성은 미판정)
- 정본 source_basis: docs/topic_sheets/functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh.md
- 기존 근거 locator (재열람 아님): NASA, Techniques for Modeling the Reliability of Fault-Tolerant Systems with the Markov State-Space Approach, NASA-RP-1348 — State-space modeling method and model construction (https://ntrs.nasa.gov/citations/19960000862); Reliability effects of test strategies on safety-instrumented systems in different demand modes — Abstract and comparison of Markov and Petri-net modeling (https://www.sciencedirect.com/science/article/pii/S0951832013002007)

#### 3. `fsrm_model_assumption_documentation` — REVISE

- 최신 정본: 정량 SIS 신뢰도 결과에는 모델 경계·수요모드와 적용한 입력·가정을 재현할 수 있도록 기록한다. 해당 모델에 사용한 고장자료 출처 및 적용환경, 진단/coverage, proof-test 주기·coverage, 수리 가용성·시간, CCF, bypass/override 및 근사·제외조건을 포함하되, 관련 없는 항목은 무조건 계산요소로 요구하지 말고 미모델링·제외 여부를 명시한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 정량 SIS 신뢰도 분석에서는 모델 경계·수요모드와 적용한 입력·가정·제외조건을 재현 가능하게 기록한다.
- 판정 이유: 재현성만 남기면 고장자료·진단·시험·수리·CCF 등의 구체 입력과 미모델링 여부 소실.
- P1-C 제안: 정량 SIS 신뢰도 분석은 모델 경계·수요모드, 적용한 고장자료 출처·환경과 진단·시험·수리·CCF·bypass 등 관련 입력·가정 및 미모델링·제외조건을 재현 가능하게 기록한다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `sis_reliability_result_records_boundary_mode_and_applicable_model_inputs@1`; status=approved; verification=verified; Registry statement: 정량 SIS 신뢰도 결과에는 모델 경계·수요모드와 적용한 입력·가정을 재현할 수 있도록 기록한다. 해당 모델에 사용한 고장자료 출처 및 적용환경, 진단/coverage, proof-test 주기·coverage, 수리 가용성·시간, CCF, bypass/override 및 근사·제외조건을 포함하되, 관련 없는 항목은 무조건 계산요소로 요구하지 말고 미모델링·제외 여부를 명시한다.
- Registry 조건: recorded_items_are_relevant_to_the_selected_model; failure_data_and_application_conditions_are_traceable; omitted_or_unmodeled_effects_are_identified_instead_of_silently_assumed_absent
- 직접 요구 문항: Sensor, Logic Solver와 Final Element로 구성된 전체 SIF의 정량 평가 절차를 설명하시오. / 기능안전 신뢰도 계산의 입력자료, 가정, 한계와 검증 방안을 설명하시오.
- 정본 source_basis: HSE, Functional Safety Inspection Guide (SIS verification, failure data and proof-test assumptions): https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf; HSE, Process for Defining SIS Proof Testing Requirements (diagnostic coverage, proof test intervals): https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix1.pdf; HSE, Process for Implementing SIS Proof Testing (observed failure data, test intervals, repair times and monitoring against design assumptions): https://www.hse.gov.uk/foi/internalops/og/og-00054-appendix2.pdf; NASA, Reliability Modeling Method, CR-188288, §2.4 (states, assumptions and transition-rate model choices): https://ntrs.nasa.gov/api/citations/19940028356/downloads/19940028356.pdf
- 기존 근거 locator (재열람 아님): UK Health and Safety Executive, Control systems: technical measures guidance — System architecture model and SIL confirmation, lines 164-168; diagnostics/proof testing/repair, lines 316-339; overrides, lines 324-328 (https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm)


### 제어 소프트웨어 프로젝트, 설계문서, FAT·SAT·시운전 및 인수 (`control_software_project_engineering_documents_fat_sat_commissioning_acceptance`)

Canonical blob: `f45ac8eb7f0ddf263a1386582e962e7496c2179c`; model_answer blob: `4b8d1a604e43c075ecee9a6039fccf056b0aff2a`.

#### 4. `sw10_fat_sat_relation` — APPROVE

- 최신 정본: FAT와 SAT는 수행 장소와 확인 가능한 설치·통합 조건이 다른 단계다. 프로젝트에서 두 시험을 요구한다면 FAT 합격만으로 현장 SAT를 완료한 것으로 간주하지 않는다. 실제 시험 범위와 필수 여부는 승인된 프로젝트 시험계획에 따른다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: FAT와 SAT는 시험 장소와 설치·통합 검증 조건이 다르므로, 승인된 시험계획에서 둘 다 요구하면 FAT 합격으로 현장 SAT를 대체하지 않는다.
- 판정 이유: 장소·설치/통합 검증 조건과 두 시험 요구 시 FAT로 SAT를 대체하지 않는 조건 보존.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `fat_and_sat_are_distinct_complementary_test_stages@1`; status=approved; verification=verified; Registry statement: FAT와 SAT는 수행 장소와 확인 가능한 설치·통합 조건이 다른 단계다. 프로젝트에서 두 시험을 요구한다면 FAT 합격만으로 현장 SAT를 완료한 것으로 간주하지 않는다. 실제 시험 범위와 필수 여부는 승인된 프로젝트 시험계획에 따른다.
- Registry 조건: specific_overlap_depends_on_agreed_project_test_plan; this_claim_does_not_assert_that_every_contract_requires_both_tests
- 직접 요구 문항: 제어시스템 FAT와 SAT의 목적, 시험환경, 시험항목과 한계를 비교하시오. / 제어 소프트웨어 프로젝트의 문서·시험·시운전·인수 전 과정을 연계하여 설명하시오.
- 정본 source_basis: 일반 산업 계측제어 프로젝트 엔지니어링, FAT·SAT·시운전 및 인수 실무 원칙
- 기존 근거 locator (재열람 아님): ISA-105 Series of Standards, overview of IEC 62381:2024 — FAT at vendor site, SAT/site integration on location; loop checks and commissioning separately scoped (https://www.isa.org/standards-and-publications/isa-standards/isa-105-standards)

#### 5. `sw10_loop_test` — REVISE

- 최신 정본: Loop test는 해당 Loop의 현장 입력 또는 출력 종단에서 배선·I/O·스케일링·제어기·HMI까지 신호의 방향, 범위와 동작을 종단 간 확인한다. 폐루프 제어 Loop는 센서부터 제어기와 최종요소까지 확인하며, 최종요소가 없는 정보·감시 Loop는 해당 입력 종단까지 확인한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: Loop test는 현장 입력·출력 종단에서 배선·I/O·스케일링·제어기·HMI 및 해당되는 최종제어요소까지 신호 범위와 동작을 종단 간 확인한다.
- 판정 이유: 루프별 입력 또는 출력 경계, 신호 방향 및 해당되는 최종요소 조건 보존.
- P1-C 제안: Loop test는 해당 루프의 현장 입력 또는 출력 종단부터 관련 배선·I/O·스케일링·제어기·HMI 및 해당되는 최종요소까지 신호 방향·범위·동작을 종단 간 확인한다.
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `iec62382_loop_check_scope_and_boundaries@1`; status=approved; verification=verified; Registry statement: Loop test는 해당 Loop의 현장 입력 또는 출력 종단에서 배선·I/O·스케일링·제어기·HMI까지 신호의 방향, 범위와 동작을 종단 간 확인한다. 폐루프 제어 Loop는 센서부터 제어기와 최종요소까지 확인하며, 최종요소가 없는 정보·감시 Loop는 해당 입력 종단까지 확인한다.
- Registry 조건: test_extent_is_defined_by_the_loop_and_project_scope; iec_62382_defines_what_is_intended_to_be_tested_but_not_one_universal_test_method; loop_check_does_not_replace_system_commissioning
- 직접 요구 문항: Loop test와 Site integration test의 대상, 절차와 판정기준을 설명하시오.
- 정본 source_basis: 일반 산업 계측제어 프로젝트 엔지니어링, FAT·SAT·시운전 및 인수 실무 원칙
- 기존 근거 locator (재열람 아님): IEC 62382:2024, Control systems in the process industry—Electrical and instrumentation loop check — Scope and intent of loop-check procedures (https://webstore.iec.ch/en/publication/67573)


### 습도계측의 원리, 선정 및 보상 — Capacitive·Resistive·Dew Point (`humidity_measurement_capacitive_resistive_dew_point_selection_compensation`)

Canonical blob: `3582e294a75d0501e56f121d69f6afec76fc6ca8`; model_answer blob: `3b42ea7ade1168b0ef789ca06ecca2ee90c80813`.

#### 6. `relative_humidity_definition` — APPROVE

- 최신 정본: Relative humidity는 같은 온도에서 실제 수증기 분압 P_w를 포화수증기압 P_ws(T)로 나눈 비이며 RH[%] = 100·P_w/P_ws(T)로 정의한다. 포화수증기압은 온도함수이므로 RH는 온도에 강하게 의존한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 상대습도 RH[%]는 같은 온도의 실제 수증기 분압 P_w와 포화수증기압 P_ws(T)의 비율로, RH=100·P_w/P_ws(T)이다.
- 판정 이유: 동일 온도 분압비·백분율 유지; 온도 영향은 별도 RH temperature anchor에 남음.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `relative_humidity_is_vapor_pressure_ratio_at_same_temperature@1`; status=approved; verification=verified; Registry statement: For the stated humidity convention, RH[%]=100·Pw/Pws(T): actual water-vapor partial pressure divided by saturation water-vapor pressure at the same temperature.
- Registry 조건: pw_and_pws_refer_to_the_same_temperature_and_pressure_convention; relative_humidity_is_expressed_as_percent
- 직접 요구 문항: Relative humidity, absolute humidity 및 dew point를 비교하여 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): Vaisala, Humidity measurement in test chambers: questions and answers — Relative humidity definition section (https://www.vaisala.com/en/application-note/humidity-measurement-test-chambers-questions-and-answers)

#### 7. `rh_temperature_dependence` — REVISE

- 최신 정본: 수증기량이 거의 변하지 않아도 공기온도가 올라가면 P_ws(T)가 증가하여 RH가 낮아질 수 있고, 냉각하면 RH가 증가하여 100%에 접근할 수 있다. 따라서 RH sensor는 sensor temperature와 process temperature의 차이에 민감하다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 수증기량이 거의 일정할 때 공기온도 상승은 포화수증기압 증가로 RH를 낮추며, 센서와 공정의 온도 차이는 RH 측정 오차를 일으킬 수 있다.
- 판정 이유: 수증기량 일정과 분압 일정은 같지 않음. 냉각 방향과 응축 전 조건 유지.
- P1-C 제안: 수증기 분압이 거의 일정하고 수분의 추가·제거가 없을 때 온도 상승은 포화수증기압 증가로 RH를 낮추고 냉각은 RH를 높이며, 센서와 공정의 온도 차는 RH 오차를 일으킬 수 있다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `relative_humidity_varies_with_temperature_at_fixed_vapor_pressure@1`; status=approved; verification=verified; Registry statement: If water-vapor partial pressure remains approximately fixed while temperature rises, temperature-dependent saturation pressure rises and RH decreases; cooling reverses this trend toward saturation, all else equal.
- Registry 조건: water_vapor_partial_pressure_is_approximately_unchanged; temperature_remains_below_water_critical_temperature; no_condensation_or_moisture_addition_removes_or_adds_vapor
- 직접 요구 문항: Relative humidity, absolute humidity 및 dew point를 비교하여 설명하시오. / Very low humidity에서 RH 대신 dew point 측정을 고려하는 이유를 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): Derived from RH=Pw/Pws(T) and the stated temperature dependence of Pws — Relative humidity definition and temperature-dependent saturation-pressure discussion (https://www.vaisala.com/en/application-note/humidity-measurement-test-chambers-questions-and-answers)

#### 8. `absolute_humidity_definition` — REJECT

- 최신 정본: Absolute humidity는 단위 체적당 수증기 질량 ρ_v = m_v/V이며 이상기체 근사에서는 ρ_v = P_w/(R_v T)이다(T는 절대온도). Relative humidity(RH)는 같은 온도에서 수증기 분압과 포화수증기압의 비로 RH = P_w/P_ws(T) × 100%이다. 두 물리량은 서로 다르며 온도와 수증기 분압 또는 체적 변화에 따라 모두 달라질 수 있다. 변화 방향은 무엇을 일정하게 유지하는지에 따라 판단한다.
- 과거 정본: Absolute humidity는 단위 체적당 수증기 질량 ρ_v = m_v/V로 정의할 수 있으며 이상기체 근사에서는 ρ_v = P_w/(R_v T)로 연결된다. RH와 달리 같은 수증기 상태라도 온도·압력과 체적변화의 영향을 받는다.
- 과거 단문화 후보: 절대습도는 단위체적당 수증기 질량 ρ_v=m_v/V이며, 이상기체 근사에서는 ρ_v=P_w/(R_vT)로 계산한다.
- 판정 이유: 최신 보완의 절대온도 T, RH 대비 정의와 고정 변수별 의존성 삭제. Q1 비교 문항에서 핵심. 현 정본 유지.
- P1-C 제안: 현 정본 유지
- 중요도: important; 정본 변경 이력: YES; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `absolute_humidity_is_water_vapor_mass_concentration@1`; status=approved; verification=verified; Registry statement: Absolute humidity as mass concentration is ρv=mv/V; under the ideal-gas approximation for water vapor, ρv=Pw/(RvT), with absolute temperature and the specific gas constant for water vapor.
- Registry 조건: water_vapor_is_treated_as_an_ideal_gas; t_is_absolute_temperature; rho_v_is_mass_per_volume
- 직접 요구 문항: Relative humidity, absolute humidity 및 dew point를 비교하여 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): NIST, General guidelines for on-site calibration of humidity and moisture control systems; ideal-gas equation applied to water vapor — Ideal gas law discussion; derivation PV=mvRvT for water-vapor component (https://nvlpubs.nist.gov/nistpubs/Legacy/BSS/nbsbuildingscience157.pdf)

#### 9. `dew_point_definition` — APPROVE

- 최신 정본: Dew point T_d는 현재 수증기 함량과 압력조건에서 기체를 냉각할 때 liquid water condensation이 시작되는 온도다. Ambient temperature가 dew point에 가까워질수록 condensation risk가 증가한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 이슬점 T_d는 주어진 수증기 함량과 압력에서 기체를 냉각할 때 액체 물의 응축이 시작되는 온도이다.
- 판정 이유: 액체 응축 시작 조건·수분 및 압력 유지; 응축 위험 상세는 별도 condensation anchor.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `dew_point_is_saturation_temperature_for_existing_vapor_pressure@1`; status=approved; verification=verified; Registry statement: At a specified pressure, dew point is the temperature at which the existing water-vapor partial pressure reaches saturation and condensation begins on cooling; a surface at or below that dew point can condense water.
- Registry 조건: pressure_condition_is_stated; condensate_is_liquid_water_for_dew_point_terminology
- 직접 요구 문항: Relative humidity, absolute humidity 및 dew point를 비교하여 설명하시오. / Chilled-mirror hygrometer의 dew-point 측정원리와 유지보수 고려사항을 설명하시오. / 습도계측에서 dew point와 frost point 및 pressure dew point를 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): NIST, The use of dew-point temperature in humidity calculations; Vaisala, What is dew point and how to measure it — NIST dew-point definition; Vaisala definition section (https://nvlpubs.nist.gov/nistpubs/jres/74c/jresv74cn3-4p117_a1b.pdf)

#### 10. `frost_point_distinction` — APPROVE

- 최신 정본: 0°C 이하의 매우 건조한 조건에서는 응축상이 ice인지 liquid water인지에 따라 frost point와 dew point를 구분할 수 있다. Subzero moisture specification에서는 사용한 정의와 계산 기준을 확인해야 한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 영하 조건에서는 얼음 형성을 기준으로 하는 서리점과 액체 물 응축을 기준으로 하는 이슬점의 정의를 구분해야 한다.
- 판정 이유: 얼음/액체 상 구별과 영하 정의 차이 보존.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: important; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `frost_point_names_vapor_to_ice_saturation_condition@1`; status=approved; verification=verified; Registry statement: When the saturation condensate is ice rather than liquid water, the corresponding subzero saturation temperature is termed frost point; it is distinct from a theoretical dew point defined over liquid water.
- Registry 조건: condensate_phase_is_ice; dew_point_over_liquid_water_is_not_substituted_without_conversion
- 직접 요구 문항: 습도계측에서 dew point와 frost point 및 pressure dew point를 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): NIST Engineering Metrology Toolbox, Humidity calculation documentation — Humidity definitions for dew point and frost point (https://emtoolbox.nist.gov/wavelength/documentation.asp)

#### 11. `pressure_dew_point_effect` — REVISE

- 최신 정본: Dew point는 pressure condition의 영향을 받으므로 compressed gas에서는 pressure dew point와 atmospheric-equivalent dew point를 혼동하지 않는다. 압력변화 시 같은 moisture content라도 condensation condition이 달라질 수 있다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 압축기체의 이슬점은 압력에 따라 달라지므로 압력 이슬점과 대기압 환산 이슬점을 구분해야 한다.
- 판정 이유: 같은 수분 함량에서도 압력 변화에 따른 응축조건 변화의 인과를 보존.
- P1-C 제안: 압축기체는 동일한 수분 함량이라도 압력 변화에 따라 이슬점과 응축조건이 달라질 수 있으므로 압력 이슬점과 대기압 환산 이슬점을 구분한다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `pressure_changes_compressed_gas_dew_point_parameter@1`; status=approved; verification=verified; Registry statement: Dew point in compressed gas is pressure-condition dependent; a dew point measured after expansion to atmosphere is not the process-pressure dew point unless it is corrected for the pressure change.
- Registry 조건: water_content_and_process_pressure_are_tracked; atmospheric_sample_value_is_not_labeled_as_pressure_dew_point_without_correction
- 직접 요구 문항: 습도계측에서 dew point와 frost point 및 pressure dew point를 설명하시오. / Very low humidity에서 RH 대신 dew point 측정을 고려하는 이유를 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): Vaisala, What is dew point and how to measure it? — Effect of pressure on dew point; dew-point measurement steps 1–2 (https://www.vaisala.com/en/blog/2019-09/what-dew-point-and-how-measure-it)

#### 12. `capacitive_polymer_principle` — APPROVE

- 최신 정본: Capacitive humidity sensor는 porous electrode 사이의 hygroscopic polymer dielectric이 수분을 흡수·방출하면 dielectric constant가 변하고 이에 따라 capacitance가 변하는 원리를 이용한다. 이 capacitance를 전자회로가 RH 신호로 변환한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 고분자 정전용량식 습도센서는 흡습성 고분자 유전체의 수분 흡수·방출에 따른 유전율·정전용량 변화를 상대습도 신호로 변환한다.
- 판정 이유: 흡습성 고분자→유전율→정전용량→RH 원리 보존; 다공성 전극은 구현 예시.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `capacitive_humidity_sensor_polymer_dielectric_changes_with_absorbed_water@1`; status=approved; verification=verified; Registry statement: In the documented Vaisala HUMICAP capacitive sensor, a thin-film hygroscopic polymer between conductive electrodes absorbs or releases water vapor; its dielectric properties and sensor capacitance change with absorbed water, and electronics convert capacitance to a humidity reading.
- Registry 조건: claim_is_limited_to_documented_capacitive_polymer_sensor_architecture; device_electronics_convert_capacitance_to_humidity_output
- 직접 요구 문항: Capacitive humidity sensor의 원리와 temperature compensation을 설명하시오. / Capacitive, resistive, chilled-mirror 습도계측 방식을 비교하고 선정기준을 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): Vaisala HMM170 User Guide, HUMICAP technology — HUMICAP technology section (https://docs.vaisala.com/r/M212259EN-D/en-US/GUID-483A8D7D-0A10-4A90-980A-CB88E2F4CD51)

#### 13. `resistive_humidity_principle` — REVISE

- 최신 정본: Resistive humidity sensor는 습기에 민감한 sensing element의 resistance 또는 impedance 변화를 측정한다. 제조사·기술 자료의 polymer 또는 conductive-salt 구조에서는 수증기 흡수에 따른 ionic conduction 변화가 저항성 응답을 만든다. 재료별 구조와 응답특성을 모든 resistive sensor에 일반화하지 않는다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 저항식 습도센서는 감지소자의 습도에 따른 저항 또는 임피던스 변화를 이용하며, 전도 메커니즘은 재료·구조에 따라 다르다.
- 판정 이유: 고분자·전도성 염의 이온전도 예시 소실. Q3 원리 설명 및 특정 재료 한정 유지.
- P1-C 제안: 저항식 습도센서는 습도에 따른 감지소자의 저항·임피던스 변화를 이용하며, 일부 고분자·전도성 염 구조에서는 수분 흡수에 따른 이온전도 변화가 원인이다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `resistive_humidity_element_resistance_changes_with_absorbed_vapor@1`; status=approved; verification=verified; Registry statement: A resistive humidity sensor measures a resistance or impedance change in a moisture-sensitive element. In documented polymer or conductive-salt designs, absorbed water vapor changes ionic conduction and therefore the resistive response; the material construction and response characteristic are design-specific, not universal to every resistive humidity sensor.
- Registry 조건: specific_mechanism_is_limited_to_documented_polymer_or_conductive_salt_designs; response_curve_and_material_are_product_specific; no_single_material_or_response_law_is_asserted_for_all_resistive_sensors
- 직접 요구 문항: Resistive humidity sensor의 원리, 특징 및 오차를 설명하시오. / Capacitive, resistive, chilled-mirror 습도계측 방식을 비교하고 선정기준을 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): Texas Instruments, Precision Analog Applications Seminar: Remote System Monitor Applications — Humidity monitoring—resistive sensors, pp. 2-44–2-45 (https://www.ti.com/lit/pdf/slyp160); Hokuriku Electric Industry (HDK), Driving Method of Resistive Humidity Sensor Element, KRH1901003 — §4, p. 3 (https://www.hdk.co.jp/pdf/tece/appe_krh1901003.pdf)

#### 14. `psychrometric_wet_dry_bulb` — REVISE

- 최신 정본: Psychrometric method는 dry-bulb와 wetted wet-bulb의 증발냉각 차이를 이용하고, airflow·wick·water purity·pressure를 고려한 psychrometric relation으로 humidity를 구한다. Wet-bulb temperature를 dew point와 동일시하지 않는다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 건습구법은 건구·습구 온도차와 통풍·심지·물 순도·압력 조건으로 습도를 산정하며, 습구온도를 이슬점과 동일시하지 않는다.
- 판정 이유: 습구 증발냉각 원리 및 Registry의 포화시 일치 예외 유지.
- P1-C 제안: 건습구법은 습구의 증발냉각에 따른 건·습구 온도차와 통풍·심지·물 순도·압력 조건으로 습도를 산정하며, 포화 상태를 제외하면 습구온도를 이슬점과 동일시하지 않는다.
- 중요도: important; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `psychrometric_wet_bulb_is_not_dew_point_except_at_saturation@1`; status=approved; verification=verified; Registry statement: A psychrometer combines dry-bulb and wetted wet-bulb temperatures with the applicable psychrometric relation to infer humidity; wet-bulb temperature is not dew point except at saturation (100% RH).
- Registry 조건: air_pressure_and_psychrometric_convention_are_accounted_for; wet_bulb_is_not_identified_as_dew_point_except_at_saturation
- 직접 요구 문항: required_anchor_ids 직접 연결 없음 (다른 경로의 채점 적격성은 미판정)
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): NIST, General guidelines for the on-site calibration of humidity and moisture control systems in buildings — Psychrometric method and wet-bulb/dew-point discussion (https://nvlpubs.nist.gov/nistpubs/Legacy/BSS/nbsbuildingscience157.pdf)

#### 15. `condensation_sensor_temperature_error` — REVISE

- 최신 정본: Sensor surface가 주변공기보다 차가워 local RH가 높아지거나 dew point 이하로 내려가면 condensation이 발생할 수 있다. 반대로 self-heating이나 warm surface는 local RH를 낮춰 실제 process RH와 차이를 만들 수 있다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 센서 표면과 공정 기체의 온도 차는 국소 상대습도를 바꾸며, 표면 온도가 이슬점 이하로 내려가면 응축을 유발할 수 있다.
- 판정 이유: 냉각시 국소 RH 상승, 가열시 감소의 방향 소실. 분압 변화가 미미한 조건 명시.
- P1-C 제안: 수증기 분압이 거의 일정할 때 센서 표면이 공정보다 차가우면 국소 RH가 상승해 이슬점 이하에서 응축될 수 있고, 가열되면 국소 RH가 낮아져 측정 오차가 생길 수 있다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `probe_temperature_difference_can_bias_rh_or_cause_condensation@1`; status=approved; verification=verified; Registry statement: A humidity probe colder than high-RH process air can cross the local dew point and condense water; because RH uses temperature-dependent saturation pressure, a probe at a temperature different from the air can also report an RH different from process RH. A warmer probe can bias local RH downward.
- Registry 조건: sensor_temperature_differs_from_process_air; high_rh_condensation_risk_is_evaluated; reported_rh_temperature_basis_is_identified
- 직접 요구 문항: High humidity 및 condensation 환경에서 습도센서의 오차와 대책을 설명하시오. / 기존 공조/공정 습도센서를 교체할 때 선정 및 적용 고려사항을 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): Vaisala, Humidity measurement in test chambers: questions and answers — Sensor installation and temperature difference sections; RH definition (https://www.vaisala.com/en/application-note/humidity-measurement-test-chambers-questions-and-answers)

#### 16. `low_humidity_dew_point_selection` — HOLD

- 최신 정본: Very low humidity에서는 RH 값이 작고 temperature sensitivity와 RH calibration uncertainty의 영향이 커질 수 있어 dew point/frost point 또는 trace-moisture 방식이 더 적합할 수 있다. 선정은 required range와 uncertainty에 따라 결정한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 극저습도에서는 상대습도의 온도 민감도와 불확도를 고려하여 이슬점·서리점 또는 미량수분 계측이 요구 범위에 더 적합할 수 있다.
- 판정 이유: 기존 unresolved_source_holds 등재. 요구 범위·불확도 및 특정 초건조 적용 문맥 유지. 제외 해제 금지.
- P1-C 제안: 현 정본 유지
- 중요도: core; 정본 변경 이력: NO; 제외: fact_anchor_unresolved_source_holds_20261101.json; score_effect=none (이번 검토).
- Registry: `dew_point_is_preferred_measurement_parameter_in_ultra_dry_vaisala_applications@1`; status=approved; verification=verified; Registry statement: For the documented Vaisala ultra-dry applications, very low RH increases RH measurement uncertainty; the vendor identifies dew/frost point measurement as the preferred parameter for those dry processes, but the exact usable range and uncertainty remain instrument-specific.
- Registry 조건: claim_is_limited_to_documented_ultra_dry_conditions; selection_matches_required_range_and_uncertainty; no_universal_rh_threshold_is_imposed
- 직접 요구 문항: Very low humidity에서 RH 대신 dew point 측정을 고려하는 이유를 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): Vaisala, Why choose Dew point/Frost Point Temperature over Relative Humidity or PPM measurements in ultra-dry conditions? — Sections on RH uncertainty below 5% and sensor selection for ultra-dry conditions (https://www.vaisala.com/en/expert-article/why-choose-dew-pointfrost-point-temperature-over-relative-humidity-or-ppm-measurements-ultra-dry-conditions)

#### 17. `selection_environment_process` — APPROVE

- 최신 정본: 습도계기 선정은 필요한 humidity parameter/range와 process 온도·압력, condensation/contaminant 조건, installation 및 response 요구를 특정 모델의 사양·옵션에 대조한다. 제조사 자료는 application마다 요구가 다르고 모든 조건에 맞는 단일 기기가 없다고 설명한다. 구체적인 range, recovery 및 설치 제약은 제품별이며 hazardous-area 인증은 별도 적용기준으로 확인한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 습도계기는 측정 물리량·범위, 공정 온도·압력, 응축·오염, 설치·응답 및 해당되는 방폭 인증 조건을 제품별 사양과 대조해 선정한다.
- 판정 이유: 요구 범위·온압·오염·설치·응답·해당 방폭을 제품별 대조하는 핵심 유지. 인증 상세 별도 소유.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `humidity_instrument_selection_matches_application_to_model_limits@1`; status=approved; verification=verified; Registry statement: Humidity instrument selection should map the required parameter and range to the application's temperature, pressure, condensation/contamination, installation, and response requirements using the selected model's published performance and options. Vaisala states that applications have different requirements and no single instrument suits every need. Specific range, recovery, and mounting constraints remain product-specific; hazardous-area certification is checked separately against applicable requirements.
- Registry 조건: selection_is_made_against_specific_model_documentation; temperature_pressure_condensation_and_contamination_effects_are_product_and_application_scoped; no_single_universal_instrument_is_asserted; hazardous_area_certification_is_checked_separately
- 직접 요구 문항: Capacitive, resistive, chilled-mirror 습도계측 방식을 비교하고 선정기준을 설명하시오. / 기존 공조/공정 습도센서를 교체할 때 선정 및 적용 고려사항을 설명하시오.
- 정본 source_basis: docs/topic_sheets/humidity_measurement_capacitive_resistive_dew_point_selection_compensation.md
- 기존 근거 locator (재열람 아님): Vaisala, How to choose the right instrument for measuring humidity and dew point — Application requirements and sections on high humidity, low humidity, temperature/pressure, sampling, and hazardous environments (https://www.vaisala.com/en/expert-article/how-to-choose-the-right-instrument-for-measuring-humidity-and-dew-point); Vaisala, HMM170 User Guide, Selecting probe mounting location and method — Selecting probe mounting location and method (https://docs.vaisala.com/r/M212259EN-D/en-US/GUID-9669B101-33E9-4074-8E76-8F2AEB76FCEB)


### 피드백 시스템의 폐루프 구조·민감도·정상상태 오차 (`feedback_system_closed_loop_sensitivity_steady_state_error`)

Canonical blob: `44a1141bc6268715f83ddd4862122863cecaed30`; model_answer blob: `3b0da971da93fe6b1caec91704f73d5b13c1ca59`.

#### 18. `feedback_sensitivity_functions` — APPROVE

- 최신 정본: 민감도 함수는 S(s)=1/[1+L(s)], 상보 민감도 함수는 T(s)=L(s)/[1+L(s)]이며 S(s)+T(s)=1이다. S와 T는 같은 함수가 아니다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 표준 음의 피드백의 민감도 S(s)=1/[1+L(s)]와 상보 민감도 T(s)=L(s)/[1+L(s)]는 S(s)+T(s)=1을 만족한다.
- 판정 이유: 표준 음의 피드백에서 S,T와 합 관계의 수식 보존. 일반적으로 두 함수 구별.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `sensitivity_and_complementary_sensitivity_functions@1`; status=approved; verification=verified; Registry statement: S(s)=1/[1+L(s)], T(s)=L(s)/[1+L(s)]이며 S(s)+T(s)=1이다. 민감도와 상보 민감도는 서로 다른 전달함수다.
- Registry 조건: standard_feedback_definition
- 직접 요구 문항: 피드백 시스템의 폐루프 전달함수와 민감도 함수를 설명하시오. / 음의 피드백 시스템의 민감도 S와 상보 민감도 T의 의미를 설명하시오. / 폐루프 제어계에서 외란 억제, 측정 잡음 및 안정성의 상충관계를 설명하시오.
- 정본 source_basis: MathWorks `loopsens`: S=(I+L)^-1, T=L(I+L)^-1 and S+T=I.
- 기존 근거 locator (재열람 아님): 폐루프 민감도 함수의 정의 및 항등식 — S=1/(1+L); T=L/(1+L); S+T=1

#### 19. `feedback_parameter_sensitivity` — REVISE

- 최신 정본: 피드백 전달 H가 고정된 경우 순방향 전달 G의 상대 변화에 대한 폐루프 전달함수의 상대 민감도는 S(s)와 연결된다. |L|가 충분히 큰 주파수 영역에서는 |S|가 작아져 모델 변화의 영향이 감소할 수 있지만 모든 주파수에서 S를 임의로 작게 만들 수는 없다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 피드백 H가 고정된 표준 구조에서 폐루프 전달함수의 G에 대한 상대 민감도는 S=1/(1+L)이며, |L|이 큰 주파수 대역에서 작아질 수 있다.
- 판정 이유: 고정 H 조건·상대 민감도 식 및 모든 주파수에서 임의 감소 불가 한계 유지.
- P1-C 제안: H가 고정된 표준 피드백에서 폐루프 전달함수의 G에 대한 상대 민감도는 S=1/(1+L)이며, |L|이 충분히 큰 주파수에서는 |S|가 작아질 수 있으나 모든 주파수에서 임의로 낮출 수는 없다.
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `closed_loop_parameter_sensitivity@1`; status=approved; verification=verified; Registry statement: 피드백 전달 H가 고정된 경우 순방향 전달 G의 미소 상대 변화에 대한 폐루프 기준입력 전달함수 G/(1+GH)의 상대 민감도는 S=1/(1+GH)이다.
- Registry 조건: feedback_path_fixed; differentiable_transfer_function
- 직접 요구 문항: 음의 피드백 시스템의 민감도 S와 상보 민감도 T의 의미를 설명하시오. / Feedback System의 추종성, 민감도 및 정상상태 오차 개선 방법을 설명하시오.
- 정본 source_basis: MathWorks `loopsens` and MIT OpenCourseWare feedback sensitivity notes.
- 기존 근거 locator (재열람 아님): 폐루프 전달함수의 G에 대한 로그 미분 — d ln[G/(1+GH)] / d ln G = 1/(1+GH)

#### 20. `feedback_disturbance_noise_paths` — APPROVE

- 최신 정본: 단위 피드백의 표준 신호 위치에서 출력단 외란은 S를 통해 출력에 나타나고 측정 잡음은 -T를 통해 출력에 나타난다. 전달경로는 외란과 잡음의 주입 위치에 따라 달라지므로 신호 위치를 먼저 정의해야 한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 표준 단위 피드백의 출력단 외란은 S, 측정 잡음은 -T를 통해 출력에 전달되며, 다른 주입 위치에는 각 전달경로를 재정의해야 한다.
- 판정 이유: 단위 피드백·출력단 외란 S·측정 잡음 -T·주입 위치 의존성 보존.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `output_disturbance_and_measurement_noise_paths@1`; status=approved; verification=verified; Registry statement: 단위 음의 피드백에서 출력 합산점에 더해지는 외란의 전달경로는 S=1/(1+L), 측정값에 더해지는 잡음의 출력 전달경로는 −T=−L/(1+L)이다.
- Registry 조건: disturbance_added_at_output; noise_added_in_measurement_path
- 직접 요구 문항: 폐루프 제어계에서 외란 억제, 측정 잡음 및 안정성의 상충관계를 설명하시오.
- 정본 source_basis: MathWorks `loopsens` input/output sensitivity definitions and signal-injection analysis.
- 기존 근거 locator (재열람 아님): 출력외란·측정잡음 합산 위치별 단위피드백 전달경로 유도 — E=R−(Y+N); Y=GE+D

#### 21. `feedback_steady_state_error_final_value` — APPROVE

- 최신 정본: 정상상태 오차는 e_ss=lim[s→0]sE(s)로 계산할 수 있다. 단, 최종값이 존재하고 sE(s)의 모든 극이 개방 좌반평면에 있어야 한다. 우반평면 또는 허수축 극으로 발산하거나 지속 진동하면 최종값 정리를 적용하지 않는다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 정상상태 오차는 sE(s)의 모든 극이 개방 좌반평면에 있고 최종값이 존재할 때 e_ss=lim[s→0]sE(s)로 계산한다.
- 판정 이유: 최종값 존재 및 sE(s) 극 조건과 식 보존. 발산·지속 진동 금지는 해당 조건으로 판단.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `steady_state_error_final_value_theorem@1`; status=approved; verification=verified; Registry statement: 정상상태 오차는 조건을 만족할 때 e_ss=lim(s→0)sE(s)로 구한다. 최종값 정리를 쓰려면 sE(s)의 모든 극이 개방 좌반평면에 있어야 한다.
- Registry 조건: limit_exists; all_poles_of_s_times_e_in_open_left_half_plane
- 직접 요구 문항: 피드백 시스템의 시스템 형과 정상상태 오차의 관계를 설명하시오.
- 정본 source_basis: MIT OpenCourseWare 16.06 steady-state error notes and final-value theorem pole conditions.
- 기존 근거 locator (재열람 아님): 라플라스 최종값 정리의 극 조건 — lim(t→∞)e(t)=lim(s→0)sE(s) when poles of sE(s) lie in LHP

#### 22. `feedback_integral_action_tradeoff` — REVISE

- 최신 정본: 유효 루프에 상쇄되지 않은 원점 적분기를 추가하는 적분 동작은 시스템 형을 증가시켜 정상상태 오차 제거에 기여할 수 있다. 그러나 위상여유 감소, 액추에이터 포화 및 적분 windup을 유발할 수 있으므로 anti-windup과 포화 처리가 필요하다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 루프에 상쇄되지 않은 적분기를 추가하면 시스템 형이 증가하여 정상상태 오차를 줄일 수 있으나, 위상여유 감소·액추에이터 포화·windup 및 anti-windup 대책을 검토해야 한다.
- 판정 이유: 원점의 비상쇄 적분기·안정 폐루프·포화시 windup 구분.
- P1-C 제안: 안정한 단위 피드백에서 상쇄되지 않은 원점 적분기를 추가하면 시스템 형이 증가하여 정상상태 오차를 줄일 수 있으나, 위상여유 감소 및 액추에이터 포화 시 windup을 검토하고 필요한 anti-windup 대책을 적용한다.
- 중요도: important; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `feedback_integral_action_tradeoff@1`; status=approved; verification=verified; Registry statement: 표준 안정 단위 피드백에서 유효 루프에 상쇄되지 않은 원점 적분기를 추가하면 시스템 형이 증가해 해당 조건의 정상상태 오차를 줄이거나 제거할 수 있다. 적분 동작은 루프 위상여유를 줄일 수 있고, 액추에이터 포화 중 오차 적분은 windup을 일으킬 수 있어 포화가 있는 설계에서는 anti-windup 처리가 필요하다.
- Registry 조건: stable_unity_feedback_for_error_claim; integrator_not_cancelled; actuator_saturation_for_windup_claim
- 직접 요구 문항: Feedback System의 추종성, 민감도 및 정상상태 오차 개선 방법을 설명하시오.
- 정본 source_basis: MathWorks PID anti-windup guidance and classical integral-action saturation analysis.
- 기존 근거 locator (재열람 아님): 단위피드백의 원점 pole 차수와 정적 오차상수 정의로부터 유도 — L(s)=L0(s)/s^n; stable closed-loop step error and Kv relations; MathWorks, Anti-Windup Control Using PID Controller Block — Purpose; back-calculation and clamping methods (https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html)


### 압력계측 센서의 원리, 선정 및 오차 — Bourdon·Diaphragm·Piezoresistive·DP (`pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`)

Canonical blob: `a1cb1968304a7b09ff3512c8b2ed2047874c52df`; model_answer blob: `82386c7c11b9d9bb9145a1feeaf091f917c8704b`.

#### 23. `bourdon_forms_application` — REVISE

- 최신 정본: Bourdon element는 C형, spiral, helical 등으로 구성할 수 있으며 형상·재질·두께에 따라 사용 압력범위가 달라진다. 일반적으로 견고한 현장 지시와 중·고압 측정에 널리 사용된다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 부르동관은 C형·나선형·헬리컬형 등의 탄성요소 변형을 이용해 압력을 지시하며, 사용 압력범위는 형상·재질·두께에 따라 달라진다.
- 판정 이유: Q2 특징/적용에 필요한 견고한 현장 지시·중고압 일반 용례 삭제.
- P1-C 제안: 부르동관은 C형·나선형·헬리컬형 등의 탄성변형으로 압력을 지시하며 견고한 현장 지시와 중·고압에 널리 쓰이고, 사용범위는 형상·재질·두께에 따라 달라진다.
- 중요도: important; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `bourdon_tube_forms_and_ranges_are_design_specific@1`; status=approved; verification=verified; Registry statement: Bourdon pressure gauges use C-shaped, helical, or spiral tube forms. C-shaped tubes are commonly used over lower pressure ranges, while helical or spiral constructions are used in some higher-range designs; the usable range is product-specific and depends on tube geometry, material, dimensions, and construction. Select from the manufacturer's rated range and service limits rather than treating one shape-to-pressure threshold as universal.
- Registry 조건: shape_to_range_relationship_is_general_not_an_absolute_threshold; actual_range_and_material_limits_are_taken_from_the_selected_product_datasheet; process_and_operating_limits_are_checked_for_the_application
- 직접 요구 문항: Bourdon tube pressure gauge의 원리, 특징 및 오차요인을 설명하시오.
- 정본 source_basis: docs/topic_sheets/pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error.md
- 기존 근거 locator (재열람 아님): WIKA, Bourdon tube pressure gauge: functional principle — C-shaped, helical, and spiral tube construction and general application ranges (https://www.wika.com/en-gb/lp_bourdon_tube_pressure_gauge.WIKA); WIKA, Bourdon Tube Pressure Gauge Model 232.53, Datasheet 23X.53 — Range and Bourdon tube specifications (https://www.wika.com/media/Data-sheets/Pressure/Pressure-gauges/ds_23x.53_en_us.pdf)

#### 24. `diaphragm_deflection_principle` — REVISE

- 최신 정본: Diaphragm pressure element는 막 양측의 압력차가 만드는 탄성변형을 변위 또는 전기신호로 변환한다. 얇고 유연한 diaphragm은 작은 압력차에 높은 감도를 얻을 수 있다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 다이어프램 압력센서는 막 양측 압력차에 의한 탄성변형을 변위나 전기신호로 변환하며, 막의 유연성은 감도에 영향을 준다.
- 판정 이유: 유연성의 감도 영향 방향 불명확. 비교 가능한 조건과 탄성 범위를 보존.
- P1-C 제안: 다이어프램은 양면 압력차에 의한 탄성변형을 변위나 전기신호로 변환하며, 다른 조건이 유사하면 얇고 유연한 막은 작은 차압에 높은 감도를 얻을 수 있다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `diaphragm_differential_pressure_deflection_and_sensitivity@1`; status=approved; verification=verified; Registry statement: A diaphragm pressure element responds elastically to the pressure difference across its two sides; its deflection may be converted mechanically to displacement or electrically through a capacitive, piezoresistive, or other sensing structure. For otherwise comparable material, span, boundary support, and geometry in the small-deflection regime, a thinner/more compliant diaphragm generally deflects more under the same small pressure difference and can provide greater sensitivity, but design limits such as stress, linearity, overload capacity, and stability must also be met.
- Registry 조건: pressure_difference_is_applied_across_the_diaphragm_faces; elastic_response_remains_within_the_design_range; sensitivity_comparison_holds_other_geometry_material_and_support_conditions_comparable; overload_stress_linearity_and_stability_limits_are_checked
- 직접 요구 문항: Diaphragm pressure element의 원리와 적용 시 고려사항을 설명하시오. / Bourdon, Diaphragm, Piezoresistive pressure sensor를 비교하고 선정기준을 설명하시오.
- 정본 source_basis: docs/topic_sheets/pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error.md
- 기존 근거 locator (재열람 아님): WIKA, Model 106D Differential Pressure Gauge — High/low pressures applied to opposite diaphragm sides and resulting deflection (https://www.wika.com/en-in/106d.WIKA); Analog Devices, Demystifying Piezoresistive Pressure Sensors — Diaphragm fabrication, pressure deformation, piezoresistive bridge output and pressure-range design (https://www.analog.com/en/resources/technical-articles/demystifying-piezoresistive-pressure-sensors.html); Linear elastic plate-bending relation for a clamped circular plate under uniform differential pressure — Central deflection scales as w0 proportional to Δp·a^4/(E·t^3) for fixed support and Poisson ratio in small-deflection regime

#### 25. `diaphragm_sensor_vs_seal` — REVISE

- 최신 정본: 압력을 직접 감지하는 diaphragm sensing element와 공정유체를 계기에서 격리하는 diaphragm seal은 목적이 다르다. Seal은 fill fluid와 capillary를 포함할 수 있으며 자체로 모든 오차를 제거하지 않는다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 압력 감지용 다이어프램은 압력차를 검출하지만 격리용 다이어프램 실은 공정유체를 계기에서 분리하며, 실의 충전액·모세관은 별도 오차원이 될 수 있다.
- 판정 이유: 직결/원격 구성에 따른 충전액·모세관의 선택적 존재 및 오차 유지.
- P1-C 제안: 감지용 다이어프램은 압력차를 검출하고 격리용 실은 공정유체를 계기와 분리하며, 구성에 따른 충전액·모세관은 별도 오차원이 될 수 있다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `diaphragm_sensing_element_vs_remote_seal_function@1`; status=approved; verification=verified; Registry statement: A pressure-sensing diaphragm is the elastic element that responds to pressure (or differential pressure) and couples that input to a mechanical or electrical sensing method. A diaphragm seal is an isolation/pressure-transfer assembly: its process-wetted diaphragm separates the instrument from the process medium and transmits pressure through a system fill fluid; a remote assembly may use a capillary. The seal does not inherently remove all measurement error—fill-fluid temperature/density, capillary response, elevation head, and assembly properties can affect performance.
- Registry 조건: seal_configuration_may_be_direct_mounted_or_remote_with_capillary; fill_fluid_and_assembly_design_are_specified; temperature_static_head_and_response_effects_are_evaluated_for_the_actual_installation
- 직접 요구 문항: Diaphragm pressure element의 원리와 적용 시 고려사항을 설명하시오.
- 정본 source_basis: docs/topic_sheets/pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error.md
- 기존 근거 locator (재열람 아님): WIKA, Technical Information IN 00.06: Diaphragm seals and diaphragm seal systems — Definition and functionality of diaphragm seal systems (https://www.wika.com/media/Technical-information/English/ds_in0006_en_co.pdf); Emerson, Rosemount Remote Seal Systems Reference Manual, §2.3.2–2.3.3 — Fill-fluid density temperature effect; system time response and performance (https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/dp-level/documents/doc-rosemount-dp-00809-0100-4002.pdf)

#### 26. `piezoresistive_static_capability` — REVISE

- 최신 정본: Piezoresistive 방식은 외부 excitation과 signal conditioning이 필요하지만 정적 압력과 저주파 압력도 측정할 수 있다. 전하 누설 때문에 정적 측정이 어려운 piezoelectric sensor와 구분해야 한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 압저항식 압력센서는 외부 여기와 신호조정 회로를 사용하여 정압·저주파 압력까지 측정할 수 있으므로 전하 누설 영향을 받는 압전식 센서와 구분한다.
- 판정 이유: 압전식 전하 누설이 정적 측정을 어렵게 한다는 비교 결과 유지.
- P1-C 제안: 압저항식은 외부 여기·신호조정으로 정압·저주파 압력을 측정할 수 있으나, 압전식은 전하 누설·드리프트 때문에 장시간 정적 측정이 어렵다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `piezoresistive_vs_piezoelectric_static_pressure_response@1`; status=approved; verification=verified; Registry statement: A piezoresistive pressure bridge is an externally excited resistive measurement and can produce a persistent output under a static or slowly varying pressure, subject to sensor drift and conditioning limits. A charge-output piezoelectric sensor is generally better suited to dynamic pressure because charge leakage/conditioning causes drift under sustained static load; static measurability depends on pressure magnitude, duration, accuracy requirement, and electronics, so piezoelectric measurement is not categorically impossible.
- Registry 조건: piezoresistive_bridge_has_excitation_and_suitable_signal_conditioning; piezoelectric_charge_leakage_and_drift_are_evaluated_for_required_duration_and_accuracy; sensor_model_and_signal_conditioner_limits_are_checked
- 직접 요구 문항: Piezoresistive pressure sensor의 원리와 temperature compensation을 설명하시오.
- 정본 source_basis: docs/topic_sheets/pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error.md
- 기존 근거 locator (재열람 아님): Kistler, Piezoelectric pressure sensors with charge output for static pressure measurement — Static load behavior and comparison with piezoresistive sensors (https://www.kistler.com/DE/en/piezoelectric-pressure-sensors-with-charge-output-pe-for-static-pressure-measurement/C00000140); Analog Devices, Piezoresistive Sensing ICs in Portable Infusion Pumps — Bridge excitation and resistive output description (https://www.analog.com/en/resources/technical-articles/piezoresistive-sensing-ics-in-portable-infusion.html)

#### 27. `dp_transmitter_two_port_principle` — APPROVE

- 최신 정본: DP transmitter는 high-side와 low-side 두 입력의 압력차를 sensing element에 전달하여 차압을 전기신호로 변환한다. 두 포트에 동일한 압력이 인가된 상태는 이상적으로 zero differential pressure 조건이다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 차압전송기는 고압측과 저압측 압력의 차이 ΔP=P_H-P_L를 감지하여 전기신호로 변환하며, 두 포트의 압력이 같으면 이상적인 차압은 0이다.
- 판정 이유: 두 포트 차압식·동일 압력의 이상적 차압 0 유지. 출력 0 또는 정압 무영향으로 확대하지 않음.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `differential_pressure_transmitter_two_port_sensing@1`; status=approved; verification=verified; Registry statement: A differential-pressure instrument applies the high-side and low-side pressures to opposite sides of a sensing element and converts their difference to an output. In the ideal differential model, equal pressures at both ports mean zero differential input; real instruments can still exhibit zero offset or static-pressure effects, so equalization does not itself prove calibrated output is exactly zero.
- Registry 조건: high_and_low_ports_are_correctly_identified_and_connected; equal_port_pressures_define_zero_differential_input_not_necessarily_zero_output; static_pressure_and_zero_offset_are_checked_for_the_specific_device
- 직접 요구 문항: DP transmitter의 원리와 high static line pressure 영향을 설명하시오. / Impulse line을 사용하는 pressure/DP 측정의 설치오차와 대책을 설명하시오.
- 정본 source_basis: docs/topic_sheets/pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error.md
- 기존 근거 locator (재열람 아님): WIKA, Model 106D Differential Pressure Gauge — Description: high/low pressures applied on either side of diaphragm and resultant deflection (https://www.wika.com/en-in/106d.WIKA); Emerson, Rosemount 4051S Manual, §6.4 Trimming pressure signal — §6.4; zero trim conditions for differential-pressure transmitters (https://www.emerson.com/en/measurement-instrumentation/catalog/pressure-measurement/4051s-manual)

#### 28. `ambient_environment_hazardous_selection` — REVISE

- 최신 정본: 주위온도, 습도, 진동, 침수·분진, EMC, 위험장소와 설치공간은 sensor/transmitter enclosure와 인증, mounting 선정에 반영해야 한다. 방폭 상세 선정은 별도 hazardous-area Topic이 소유한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 압력센서·전송기의 외함·설치·인증은 주위온도·습도·진동·EMC·침수·분진·위험장소 등 실제 환경조건에 맞춰 선정한다.
- 판정 이유: 설치공간과 방폭 상세의 별도 Topic 소유 경계 유지.
- P1-C 제안: 압력센서·전송기의 외함·설치·인증은 주위온도·습도·진동·EMC·침수·분진·위험장소·설치공간에 맞춰 선정하며, 상세 방폭 선정은 별도 Topic에서 다룬다.
- 중요도: important; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `pressure_transmitter_environmental_and_approval_selection_is_installation_specific@1`; status=approved; verification=verified; Registry statement: Select a pressure transmitter's enclosure, mounting, and approvals against the actual installation environment and jurisdiction. Check the model's ambient/process-temperature limits, ingress/environmental protection, vibration and EMC specifications, and—where the area is classified—the applicable gas/dust classification, protection concept, temperature class, certificate conditions, and installation requirements. A general hazardous-area label or enclosure IP/NEMA rating alone does not establish suitability for every site.
- Registry 조건: environmental_limits_are_checked_for_actual_ambient_and_process_conditions; classified_area_approval_matches_local_area_classification_and_certificate_conditions; emc_vibration_ingress_and_mounting_requirements_are_checked_per_product_documentation
- 직접 요구 문항: 압력 transmitter 선정 시 range, overrange, process condition 및 environment를 설명하시오. / 기존 압력계기를 smart pressure transmitter로 교체할 때 선정·적용 고려사항을 설명하시오.
- 정본 source_basis: docs/topic_sheets/pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error.md
- 기존 근거 locator (재열람 아님): Emerson, Rosemount 3051 Pressure Transmitter Quick Start Guide, Hazardous Locations and Special Conditions for Safe Use — Hazardous-location certification, ambient temperature, grounding, cable glands, blanking plugs, and installation conditions (https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/dl-rmt-00825-0100-5007.pdf); WIKA, IS-3 Pressure Transmitter Product Information and Datasheet PE 81.58 — Product approvals, hazardous-area variants and ingress protection (https://www-prod.wika.com/en-us/is_3.WIKA); WIKA, IS-3 Pressure Transmitter Datasheet PE 81.58 — Approvals table: EMC directive and industrial-environment immunity; ATEX/IECEx area markings (https://shop.wika.com/media/Data-sheets/Pressure/Pressure-sensors/ds_pe8158_en_co.pdf)

#### 29. `accuracy_total_performance_terms` — REVISE

- 최신 정본: 압력계기의 reference accuracy는 linearity, hysteresis, repeatability 등의 일부 또는 조합일 수 있고 제조사 정의가 다를 수 있다. 실제 성능은 온도·static pressure·installation·stability 영향까지 포함한 total performance 관점으로 평가한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 압력계기의 기준정확도는 제조사별 정의에 따라 선형성·히스테리시스·반복성 등의 기여를 포함할 수 있으므로, 실제 정확도는 온도·정압·설치·안정성의 영향까지 검토한다.
- 판정 이유: reference accuracy와 total performance 용어 및 제조사별 정의 유지.
- P1-C 제안: 압력계기의 reference accuracy는 제조사 정의에 따라 선형성·히스테리시스·반복성 등을 포함할 수 있으며, 실제 성능은 온도·정압·설치·안정성 영향을 포함한 total performance 관점에서 평가한다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `pressure_reference_accuracy_and_operating_effects_are_distinct_specification_terms@1`; status=approved; verification=verified; Registry statement: A pressure transmitter's reference-accuracy specification may combine linearity, hysteresis, and repeatability under stated reference conditions; it does not by itself represent all installed measurement error. Product specifications may separately state temperature effect, static-pressure effect, vibration effect, and long-term stability, and the definitions and included terms vary by model. Evaluate expected performance using the selected model's specification and operating conditions; do not assume a universal additive total-performance formula unless the manufacturer defines one.
- Registry 조건: reference_conditions_and_included_accuracy_terms_are_read_from_datasheet; temperature_static_pressure_vibration_and_stability_effects_are_checked_separately_when_listed; combined_total_performance_formula_is_used_only_if_defined_for_the_model
- 직접 요구 문항: 압력계측의 주요 오차원인과 calibration 대책을 설명하시오.
- 정본 source_basis: docs/topic_sheets/pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error.md
- 기존 근거 locator (재열람 아님): Emerson, Rosemount 2088 Pressure Transmitter Product Data Sheet, Performance Specifications — Reference accuracy, ambient temperature effect, stability, vibration effect (https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-2088-00813-0100-4690.pdf); Emerson, Rosemount 3051N Pressure Transmitter Product Data Sheet, Performance Specifications — Reference accuracy, ambient temperature effect, drift, overpressure effect and range-down conditions (https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051N-00813-0100-4808.pdf)


### 회전속도 계측의 원리, 선정 및 오차 — Encoder·Proximity·Tachometer (`speed_rotation_measurement_encoder_proximity_tachometer_selection_error`)

Canonical blob: `caa53173881ed893e47a908ab4d30e60ea8bdc73`; model_answer blob: `3b2880741ab7ae24c08a6d2b176f4338d60fc7e8`.

#### 30. `pulse_frequency_speed_equation` — REVISE

- 최신 정본: 회전당 유효 count 수를 N_eff, 측정 pulse frequency를 f[Hz]라 하면 n[rpm] = 60f/N_eff로 계산한다. N_eff는 encoder PPR뿐 아니라 edge counting과 x1/x2/x4 decoding 정의를 반영해야 한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 회전당 유효 펄스 수 N_eff와 펄스 주파수 f[Hz]로 회전속도를 계산하면 n[rpm]=60f/N_eff이며, N_eff에는 수신기의 x1/x2/x4 에지 계수방식을 반영한다.
- 판정 이유: f를 물리 채널 펄스와 디코딩 계수율로 혼동하지 않도록 실제 계수 기준 명시.
- P1-C 제안: 실제 계수하는 유효 이벤트의 빈도 f[count/s]와 회전당 유효 계수 N_eff[count/rev]가 같은 계수 기준이면 n[rpm]=60f/N_eff이며, N_eff는 PPR 정의와 x1/x2/x4 에지 계수를 반영한다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `encoder_pulse_frequency_to_rpm_equation@1`; status=approved; verification=verified; Registry statement: If an incremental encoder produces f counted pulses per second and the configured decoding yields N_eff counted pulses per mechanical revolution, rotational speed is n=60f/N_eff rpm. N_eff must use the receiver's actual x1/x2/x4 edge-count definition; interpreting catalog PPR without the decoder convention can introduce a factor error.
- Registry 조건: f_is_counted_pulses_per_second; n_eff_is_counted_edges_per_mechanical_revolution; decoder_mode_and_catalog_ppr_definition_are_consistent
- 직접 요구 문항: 회전속도 계측에서 pulse frequency와 RPM의 관계 및 측정방법을 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): Dimensional derivation from pulse count and rotational frequency — revolutions/second = (pulses/second)/(pulses/revolution); multiply by 60 seconds/minute

#### 31. `counting_window_speed_equation` — REJECT

- 최신 정본: 고정 측정창 Δt 동안 m개의 유효 count를 세면 n = 60m/(N_eff·Δt)로 계산할 수 있다. N_eff와 Δt가 일정하면 한 count가 만드는 절대 RPM step은 60/(N_eff·Δt)로 일정하며, 저속에서는 상대 quantization error 또는 상대 분해능의 영향이 커질 수 있다.
- 과거 정본: 고정 측정창 Δt 동안 m개의 유효 count를 세면 n = 60m/(N_eff·Δt)로 계산할 수 있다. 낮은 속도에서는 한 count가 만드는 속도 step이 커져 quantization 또는 resolution error가 증가할 수 있다.
- 과거 단문화 후보: 측정창 Δt에 수신한 유효 펄스 수가 m이면 n[rpm]=60m/(N_eff·Δt)이며, 저속에서는 펄스 양자화에 의한 속도 분해능 한계가 커질 수 있다.
- 판정 이유: 최신 정본의 절대 RPM step 일정 및 저속 상대 양자화 오차 증가의 구별 삭제. Q1/Q9 핵심. 현 정본 유지.
- P1-C 제안: 현 정본 유지
- 중요도: core; 정본 변경 이력: YES; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `encoder_fixed_window_count_to_rpm_equation@1`; status=approved; verification=verified; Registry statement: If m decoded encoder edges are counted during a gate interval Δt seconds and N_eff is the decoded edge count per mechanical revolution, the gate-average speed estimate is n=60m/(N_eff·Δt) rpm. A finite gate quantizes the result in increments of 60/(N_eff·Δt) rpm per count; this is resolution/quantization, not a universal bound on all measurement error.
- Registry 조건: delta_t_is_measured_in_seconds; m_counts_decoded_edges_during_the_gate; n_eff_is_edges_per_mechanical_revolution; count_endpoint_and_gate_timing_conventions_are_defined
- 직접 요구 문항: 회전속도 계측에서 pulse frequency와 RPM의 관계 및 측정방법을 설명하시오. / 저속과 고속의 회전수 측정에서 resolution과 response time trade-off를 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): Dimensional derivation from edge count over a fixed time gate — m/N_eff = revolutions in Δt; divide by Δt for rev/s and multiply by 60 for rpm

#### 32. `period_measurement_low_speed` — REVISE

- 최신 정본: 저속에서는 연속 유효 pulse 사이의 시간 T_c를 측정하여 n = 60/(N_eff·T_c)로 계산하는 reciprocal/period 방식이 fixed-window count 방식보다 유리할 수 있다. 단, timer resolution과 jitter의 영향을 검토해야 한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 유효 펄스 사이의 주기 T_c를 측정하면 n[rpm]=60/(N_eff·T_c)이며, 저속 계측에 유리할 수 있으나 타이머 분해능과 지터를 검토한다.
- 판정 이유: 저속 고정창 방식 대비 장점과 연속 유효 펄스 조건·시간 단위 유지.
- P1-C 제안: 등각도 간격의 연속 유효 펄스 간 주기 T_c[s]를 측정하면 구간 평균속도 n[rpm]=60/(N_eff·T_c)이며, 저속에서는 고정창 계수보다 유리할 수 있으나 타이머 분해능·지터를 검토한다.
- 중요도: important; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `rotation_speed_period_measurement_formula_and_low_speed_tradeoff@1`; status=approved; verification=verified; Registry statement: When a sensor generates N_eff effective pulses per revolution and the measured interval between consecutive pulses is T_c seconds, rotational speed is n = 60/(N_eff·T_c) rpm. Period measurement can improve low-speed resolution relative to fixed-window counting because the measured interval becomes longer; timer quantization and pulse-timing jitter still bound the result.
- Registry 조건: effective_pulses_per_revolution_match_the_actual_edge_counting_mode; pulse_period_is_measured_in_seconds_between_valid_consecutive_pulses; missing_or_extra_edges_are_excluded_or_accounted_for; timer_resolution_and_timing_jitter_are_within_required_error
- 직접 요구 문항: 회전속도 계측에서 pulse frequency와 RPM의 관계 및 측정방법을 설명하시오. / 저속과 고속의 회전수 측정에서 resolution과 response time trade-off를 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): Dimensional derivation: f_pulse = 1/T_c; revolutions per second = f_pulse/N_eff; rpm = 60 × revolutions per second — n = 60/(N_eff·T_c), with T_c in seconds and N_eff in pulses/revolution

#### 33. `quadrature_direction_principle` — APPROVE

- 최신 정본: Quadrature incremental encoder는 A와 B 두 channel을 약 90 electrical degree 위상차로 출력하며 어느 channel이 선행하는지로 회전방향을 판별한다. x1/x2/x4 decoding에 따라 유효 count/rev가 달라질 수 있다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 증분형 엔코더의 A·B 직교 채널은 약 90° 전기각 위상차와 선행 채널로 방향을 판별하며, 유효 계수 수는 x1/x2/x4 복호화 방식에 따라 달라진다.
- 판정 이유: A/B 전기각 위상차·선행 채널 방향·디코딩에 따른 유효 계수 보존.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `quadrature_phase_order_encodes_direction@1`; status=approved; verification=verified; Registry statement: A quadrature incremental encoder provides A and B channels in nominally quadrature phase (90 electrical degrees); the channel lead/lag sequence indicates direction. The effective counts per revolution depend on which edges and channels the receiving counter decodes, so x1/x2/x4 mode must be reflected in N_eff.
- Registry 조건: channels_are_valid_quadrature_signals; direction_is_decoded_from_phase_order; effective_counts_per_revolution_follow_receiver_decode_mode
- 직접 요구 문항: Incremental encoder의 원리와 A/B/Z signal의 기능을 설명하시오. / Encoder의 PPR/CPR, quadrature decoding 및 maximum frequency 선정관계를 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): Danaher/Dynapar, Encoder Handbook, Absolute vs. Incremental Coding — Incremental Coding; quadrature and x1/x2/x4 decoding (https://www.dynapar.com/hubfs/uploadedFiles/_site_root/Service_and_Support/Danaher_Encoder_Handbook.pdf); Rockwell Automation, ControlLogix High-speed Counter Module Installation Instructions, 1756-UM007E-EN-P — Chapter 2, Encoder x4 mode and A/B timing diagrams (https://literature.rockwellautomation.com/idc/groups/literature/documents/um/1756-um007_-en-p.pdf)

#### 34. `index_z_channel_role` — APPROVE

- 최신 정본: Incremental encoder의 Z 또는 index channel은 일반적으로 1회전당 기준 pulse를 제공하여 homing, revolution reference 또는 count verification에 사용할 수 있다. Z pulse만으로 다회전 absolute position을 제공하는 것은 아니다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 증분형 엔코더의 Z 채널은 일반적으로 1회전당 기준 펄스를 제공해 원점 복귀·회전 기준 검증에 사용하지만, 이 펄스만으로 다회전 절대위치를 알 수는 없다.
- 판정 이유: 1회전 기준이라는 일반 조건, 원점·회전 검증 및 다회전 절대위치 한계 보존.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: important; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `encoder_index_is_reference_mark_not_multiturn_absolute_position@1`; status=approved; verification=verified; Registry statement: An incremental encoder's index/marker/Z output is typically a once-per-revolution reference pulse used for homing, locating a reference, or checking accumulated A/B counts. It is a reference mark, not by itself a code for the shaft's absolute multi-turn position; turn counting and retention require other system logic.
- Registry 조건: index_output_is_configured_for_one_reference_per_revolution; multi_turn_position_requires_counting_and_state_retention_or_other_reference
- 직접 요구 문항: Incremental encoder의 원리와 A/B/Z signal의 기능을 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): Dynapar, Incremental Encoder Technology: Benefits and Application Uses — Optional signals: Index or Z channel (https://www.dynapar.com/knowledge/encoder-basics/encoder-types/incremental-encoders/)

#### 35. `absolute_encoder_principle` — REVISE

- 최신 정본: Absolute encoder는 각 angular position에 대응하는 고유 digital word를 출력한다. 속도는 연속 position sample의 변화량과 sample interval로 계산할 수 있으며 resolution, update rate, communication latency를 함께 고려한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 절대형 엔코더는 각도 위치에 대응하는 고유 디지털 코드를 제공하며, 샘플 간 위치변화로 속도를 구할 때 분해능·갱신주기·통신지연을 고려한다.
- 판정 이유: 샘플 간 위치 변화만으로 속도 산출 불가; 시간 간격 유지.
- P1-C 제안: 절대형 엔코더는 각도별 고유 디지털 코드를 제공하며, 위치 샘플 변화량과 시간 간격으로 속도를 계산할 때 분해능·갱신주기·통신지연을 고려한다.
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `absolute_encoder_code_identifies_position_and_speed_is_sampled@1`; status=approved; verification=verified; Registry statement: An absolute encoder outputs a digital code/word associated with its absolute angular position (single-turn or multi-turn capability depends on the model). Speed can be estimated from successive position samples divided by their time interval; achievable dynamic response also depends on sampling/update rate and communication latency, not resolution alone.
- Registry 조건: single_turn_or_multiturn_range_is_checked_for_the_selected_model; speed_estimation_uses_time_stamped_or_interval_known_position_samples; update_and_communication_rates_support_required_response
- 직접 요구 문항: Incremental encoder와 absolute encoder를 비교하고 속도계측 적용을 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): Danaher/Dynapar, Encoder Handbook, Absolute vs. Incremental Coding — Absolute Coding (https://www.dynapar.com/hubfs/uploadedFiles/_site_root/Service_and_Support/Danaher_Encoder_Handbook.pdf); Dynapar, How to Calculate Encoder Resolution — Absolute encoder resolution and serial communication/data rate discussion (https://www.dynapar.com/knowledge/encoder-basics/encoder-how-to-guides/how-to-calculate-encoder-resolution)

#### 36. `encoder_frequency_limit_selection` — REJECT

- 최신 정본: Encoder와 receiving counter/PLC의 최대 output/input frequency를 확인한다. 최고 속도 n[rpm]에서 채널당 pulse/rev P_ch이면 물리 pulse frequency f_ch=n·P_ch/60 [Hz], 유효 count/rev N_eff이면 decoded count rate=n·N_eff/60 [count/s]이다. 동일 회전속도에서 물리 PPR 증가에 따라 pulse frequency가 증가하며 decoding 배율 변경은 count rate를 바꾼다. 각 장치 사양의 단위와 조건에 맞춰 선정한다.
- 과거 정본: Encoder와 receiving counter/PLC에는 최대 output/input frequency가 있으므로 최고 회전속도와 N_eff의 곱이 허용 주파수를 넘지 않도록 선정한다. 해상도를 높이면 동일 속도에서 pulse frequency도 증가한다.
- 과거 단문화 후보: 엔코더와 수신기의 허용 펄스 주파수는 최고 회전속도와 회전당 유효 계수 수 N_eff에 맞춰 선정하며, 고분해능일수록 같은 속도에서 주파수가 증가한다.
- 판정 이유: 물리 채널 주파수 f_ch=nP_ch/60[Hz]와 decoded count rate=nN_eff/60[count/s] 혼합. 최신 보완 원복 위험. 현 정본 유지.
- P1-C 제안: 현 정본 유지
- 중요도: core; 정본 변경 이력: YES; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `encoder_speed_and_decode_rate_must_fit_frequency_limits@2`; status=approved; verification=verified; Registry statement: 증분형 엔코더가 `n` rpm으로 회전하고 PPR이 채널의 회전당 신호 주기 수를 뜻할 때, 채널 출력 주파수는 `n·PPR/60` Hz이고 수신기의 유효 계수율은 `n·N_eff/60` count/s이다. 최대 회전속도와 선택한 복호 모드에서 엔코더 출력 한계, 수신기 입력 주파수·펄스폭 한계, 사양에 명시된 내부 계수 처리 한계를 각각 확인한다.
- Registry 조건: n_is_in_rpm; n_eff_is_receiver_decoded_counts_per_revolution; encoder_and_input_module_limits_are_checked_separately
- 직접 요구 문항: Encoder의 PPR/CPR, quadrature decoding 및 maximum frequency 선정관계를 설명하시오. / 저속과 고속의 회전수 측정에서 resolution과 response time trade-off를 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): Dynapar, How to Calculate Encoder Resolution — Incremental Encoder Resolution Calculation (https://www.dynapar.com/knowledge/encoder-basics/encoder-how-to-guides/how-to-calculate-encoder-resolution); Rockwell Automation, ControlLogix High-speed Counter Module Installation Instructions, 1756-UM007E-EN-P — Chapter 2, Encoder x1/x4 frequency and minimum pulse width (https://literature.rockwellautomation.com/idc/groups/literature/documents/um/1756-um007_-en-p.pdf)

#### 37. `inductive_proximity_principle` — APPROVE

- 최신 정본: Inductive proximity sensor는 sensing face의 교번 전자기장에 금속 target이 접근할 때 발생하는 eddy-current loss 또는 oscillator 변화로 target 존재를 검출한다. Gear tooth나 flag를 반복 검출하면 passage frequency에서 회전속도를 계산할 수 있다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 유도형 근접센서는 교번자계에 금속 표적이 접근할 때 생기는 와전류 손실·발진변화를 검출하며, 톱니 통과 빈도로 회전속도를 산정할 수 있다.
- 판정 이유: 금속 표적 와전류/발진 변화·톱니 통과빈도에 의한 속도 산출 보존. 환산은 별도 gear equation.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `inductive_proximity_metal_target_eddy_current_detection@1`; status=approved; verification=verified; Registry statement: A common high-frequency-oscillator inductive proximity sensor generates an alternating electromagnetic field at its sensing face; a conductive metal target entering that field induces eddy-current losses that damp the oscillator, and the sensor electronics switch the output when the change crosses its threshold. Repeated gear-tooth or flag passages can create pulses whose frequency is related to target passage rate; conversion to shaft speed requires the target count per revolution and correct pulse interpretation.
- Registry 조건: claim_applies_to_high_frequency_oscillator_inductive_sensor_type; target_is_conductive_and_within_the_sensor_operating_range; shaft_speed_conversion_uses_known_target_events_per_revolution
- 직접 요구 문항: Inductive proximity sensor를 이용한 gear-tooth 회전속도 측정원리와 오차를 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): Balluff, The basic operating principle of an inductive proximity sensor — Oscillator, electromagnetic field, eddy-current losses and output switching (https://www.balluff.com/en-gb/blog/the-basic-operating-principle-of-an-inductive-proximity-sensor); Danaher/Dynapar, Encoder Handbook, Incremental Coding — Incremental pulse counting and speed/position measurement (https://www.dynapar.com/hubfs/uploadedFiles/_site_root/Service_and_Support/Danaher_Encoder_Handbook.pdf)

#### 38. `gear_tooth_speed_equation` — REJECT

- 최신 정본: 회전당 Z개의 동일한 tooth 또는 target event가 있고 각 event당 1 pulse를 얻는다면 평균 event frequency f에 대해 n = 60f/Z이다. 실제 missing-tooth, multiple-edge counting 또는 target pattern에서는 전체 회전 평균에 회전당 유효 event 수 Z_eff를 적용한다. 비등간격 event의 국부 period로 속도를 계산할 때는 실제 각도 간격을 반영한다.
- 과거 정본: 회전당 Z개의 동일한 tooth 또는 target event가 있고 각 event당 1 pulse를 얻는다면 n = 60f/Z이다. 실제 missing-tooth, multiple-edge counting 또는 target pattern이 있으면 Z 대신 회전당 유효 event 수를 사용한다.
- 과거 단문화 후보: 회전당 검출 이벤트가 Z개이고 이벤트당 펄스가 하나이면 회전속도 n[rpm]=60f/Z이며, 누락 톱니나 다중 에지 계수 시 실제 유효 이벤트 수로 보정한다.
- 판정 이유: 전체 회전 평균에 Z_eff 적용과 비등간격 국부 period에서 실제 각도 간격 반영의 최신 보완 삭제. 현 정본 유지.
- P1-C 제안: 현 정본 유지
- 중요도: core; 정본 변경 이력: YES; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `rotation_speed_tooth_event_frequency_relation@2`; status=approved; verification=verified; Registry statement: 한 회전 또는 정수 회전에서 측정한 이벤트 평균 주파수가 `f` Hz이고 회전당 유효 이벤트 수가 `Z`이면 평균 회전속도는 `60f/Z` rpm이다. 결손치를 포함한 두 검출 에지 사이의 구간 평균 회전속도는 실제 회전각을 경과 시간으로 나누어 환산한다.
- Registry 조건: effective_event_count_per_revolution_is_correctly_defined; counted_event_frequency_is_measured_in_hertz; counting_mode_and_target_pattern_match_the_effective_event_count
- 직접 요구 문항: Inductive proximity sensor를 이용한 gear-tooth 회전속도 측정원리와 오차를 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): Dimensional derivation: f = Z·r, where r is revolutions/second; n = 60r revolutions/minute — n = 60f/Z, with f in events/second and Z in events/revolution

#### 39. `tachogenerator_voltage_speed_principle` — APPROVE

- 최신 정본: Permanent-magnet DC tachogenerator는 회전에 의해 생성되는 DC voltage가 정상 동작범위에서 회전속도에 대체로 비례하도록 설계된 analog speed transducer다. V_t ≈ K_t·n의 sensitivity로 표현할 수 있다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 영구자석형 DC 타코제너레이터의 출력전압은 규정 동작범위에서 회전속도에 대체로 비례하여 V_t≈K_t·n으로 표현할 수 있다.
- 판정 이유: 영구자석 DC 방식·규정 범위에서 근사 비례·수식 유지.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: core; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `permanent_magnet_dc_tachogenerator_voltage_tracks_speed@1`; status=approved; verification=verified; Registry statement: A permanent-magnet DC tachogenerator generates an output voltage whose magnitude is approximately proportional to shaft speed over its specified operating range; the output polarity can indicate direction for a bipolar measurement circuit. The proportionality constant, linearity, ripple, loading error and temperature behavior are device-specific and require the manufacturer's specification/calibration.
- Registry 조건: sensor_is_a_dc_tachogenerator_not_an_ac_tachometer; operation_is_within_specified_speed_and_load_range; calibration_and_device_nonidealities_are_accounted_for
- 직접 요구 문항: DC tachogenerator의 원리, 특징 및 오차요인을 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): NEMA MG 1-2016, Motors and Generators, DC Permanent-Magnet Tachometer Generators for Control Systems — Part 16, DC permanent-magnet control tachometer generator definition (https://www.normsplash.com/Samples/NEMA/155967517/ANSI-NEMA-MG-1-2016-en-3.pdf); Nidec Leroy-Somer, Engineering Guide to Position and Speed Feedback Devices for Variable Speed Drives and Servos — DC tacho-generators (https://cdn-static.nidec-netherlands.nl/media/2927-an-engineering-guide-to-position-and-speed-feedback-devices-for-variable-speed-drives-and-servos-iss2x-0704-0010-02x.pdf)

#### 40. `digital_tachometer_instrument_boundary` — APPROVE

- 최신 정본: Digital tachometer는 encoder·proximity·optical pickup 등의 pulse를 계수하거나 period를 측정해 RPM을 표시하는 instrument일 수 있다. Tachometer라는 명칭만으로 sensing principle이 tachogenerator라고 단정하지 않는다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 디지털 타코미터는 엔코더·근접센서·광학센서의 펄스 수 또는 주기를 이용해 회전속도를 표시할 수 있으므로 명칭만으로 센서 원리를 타코제너레이터로 단정하지 않는다.
- 판정 이유: 계측기와 센서 원리 경계 및 펄스 계수/주기 방식의 가능성 유지.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: important; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `digital_tachometer_can_measure_from_external_sensor_pulses@1`; status=approved; verification=verified; Registry statement: A digital tachometer is an RPM-measuring instrument, not necessarily a tachogenerator: some instruments accept external pulse inputs from an encoder or other detector and calculate/display rotational speed using a configured pulse-per-revolution value; other handheld tachometers derive RPM optically or by contact. The instrument's input type and sensing method must be identified from its manual rather than inferred from the word 'tachometer'.
- Registry 조건: statement_describes_instrument_classes_not_one_specific_model; input_and_sensor_compatibility_are_checked_in_the_instrument_manual; tachogenerator_is_a_sensor_type_not_a_synonym_for_every_tachometer
- 직접 요구 문항: DC tachogenerator의 원리, 특징 및 오차요인을 설명하시오.
- 정본 source_basis: docs/topic_sheets/speed_rotation_measurement_encoder_proximity_tachometer_selection_error.md
- 기존 근거 locator (재열람 아님): Tsuruga Electric, 4961 Tachometer Instruction Manual — Digital Tachometer Mode, P1 pulse count/revolution for rotary encoder or similar (https://www.tsuruga.co.jp/foreign/products/pdf/4961tacho_en_ex.pdf); Fluke, 931 Tachometer Users Manual — Optical (non-contact) and contact RPM measurement procedures (https://assets.fluke.com/manuals/931_____umeng0000.pdf)


### 열전대 온도센서의 원리, 기준접점 보상 및 보상도선 (`thermocouple_temperature_sensor_seebeck_reference_junction_compensation`)

Canonical blob: `5ea6a5d552f19247f20b02e356f79d25fdda35e0`; model_answer blob: `5f2bc9ac20f81de9a2e36b98321201c669d569ef`.

#### 41. `thermocouple_temperature_measurement_chain` — REJECT

- 최신 정본: 열전대 측정은 공정 온도를 측정접점의 온도로 전달하고, 측정접점과 기준접점의 온도차에 대응하는 열기전력을 측정한 뒤, 기준접점 보상과 열전대 종류별 선형화를 수행하여 온도로 환산하는 과정이다. 답안은 센서, 접점, 배선, 기준접점 센서, 신호처리기와 지시값까지의 측정 체인을 연결해야 한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 열전대는 측정접점과 기준접점의 온도에 따른 열기전력을 계측하고 기준접점 보상·열전대 형식별 선형화를 거쳐 측정접점 온도로 환산한다.
- 판정 이유: Q1/Q3 측정 체인의 공정→접점 열전달, 배선·단자·기준접점 센서·신호처리·지시 연결 소실. 현 정본 유지.
- P1-C 제안: 현 정본 유지
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `thermocouple_temperature_measurement_chain@1`; status=approved; verification=verified; Registry statement: 열전대 측정은 측정접점과 기준접점의 온도차에 대응하는 열기전력을 측정하고, 기준접점 보상과 열전대 종류별 변환을 거쳐 온도로 환산한다.
- Registry 조건: thermocouple_type_known; reference_junction_temperature_compensated
- 직접 요구 문항: 열전대의 측정원리와 기준접점 보상 방법을 설명하시오. / 열전대의 측정접점과 기준접점의 역할을 설명하시오.
- 정본 source_basis: reviewed thermocouple requirements Markdown
- 기존 근거 locator (재열람 아님): NIST, Thermocouple: Mercury Thermometer Alternatives — Thermocouples measure temperature differences (https://www.nist.gov/pml/sensor-science/thermodynamic-metrology/mercury-thermometer-alternatives/mercury-thermometer-5); NIST Monograph 175, Temperature-Electromotive Force Reference Functions and Tables Based on ITS-90 — Type-specific reference functions and tables (https://nvlpubs.nist.gov/nistpubs/Legacy/MONO/nistmonograph175.pdf)

#### 42. `thermocouple_seebeck_effect_dissimilar_conductors` — APPROVE

- 최신 정본: 서로 다른 두 도체로 폐회로를 구성하고 두 접점에 온도차가 존재하면 열기전력이 발생한다. 열전대의 출력은 단순히 금속 하나의 온도에서 발생하는 전압이 아니라, 재료 조합과 접점 온도의 함수이다. Seebeck 계수는 재료와 온도에 따라 달라지므로 열전대 출력은 전체 범위에서 완전한 직선이 아니다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 서로 다른 두 열전소자로 만든 열전대의 열기전력은 측정접점과 기준접점의 온도 및 재료 조합에 따라 달라지며, Seebeck 계수의 온도의존성 때문에 전체 범위에서 선형이 아니다.
- 판정 이유: 재료쌍과 두 온도에 따른 열기전력·Seebeck 계수 비선형성 보존. 구체 연결은 체인 anchor 유지.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `thermocouple_seebeck_effect_dissimilar_conductors@1`; status=approved; verification=verified; Registry statement: 서로 다른 열전대 재료의 열전기 특성과 접점 간 온도차가 열기전력을 결정하며, Seebeck 계수의 온도의존성 때문에 열전대 전압-온도 관계는 일반적으로 비선형이다.
- Registry 조건: temperature_gradient_present; thermoelement_pair_and_type_defined
- 직접 요구 문항: 열전대의 측정원리와 기준접점 보상 방법을 설명하시오. / Seebeck 효과와 열전대 온도 측정의 관계를 설명하시오.
- 정본 source_basis: reviewed thermocouple requirements Markdown
- 기존 근거 locator (재열람 아님): NIST Special Publication 250-35, The Calibration of Thermocouples and Thermocouple Materials — Thermocouple emf and Seebeck coefficient (https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication250-35.pdf); NIST Monograph 175, Temperature-Electromotive Force Reference Functions and Tables Based on ITS-90 — Polynomial reference functions (https://nvlpubs.nist.gov/nistpubs/Legacy/MONO/nistmonograph175.pdf)

#### 43. `thermocouple_measures_temperature_difference` — REJECT

- 최신 정본: 열전대 전압은 측정접점 온도만의 함수가 아니다. 균질한 열전대에서 열기전력 E(Th,Tc)=E0(Th)−E0(Tc)는 재료 조합과 측정접점·기준접점의 두 온도에 의존하며, Seebeck 계수가 온도에 따라 변하므로 같은 온도차라도 열기전력이 다를 수 있다. 측정접점 온도를 구하려면 기준접점 온도(또는 알려진 기준조건)와 해당 열전대의 유효 온도-열기전력 변환관계를 이용한다. 온도차 측정이라는 일반적인 설명은 ΔT만의 함수라는 단정과 구분한다.
- 과거 정본: 열전대 전압은 측정접점 온도만의 함수가 아니다. 기준접점의 온도가 변하면 동일한 측정접점 온도에서도 측정 전압이 달라진다. 따라서 열전대는 본질적으로 두 접점의 온도차에 대응하는 센서이며, 절대온도를 얻으려면 기준접점 온도를 알아야 한다.
- 과거 단문화 후보: 열전대의 기전력은 측정접점뿐 아니라 기준접점 온도에도 의존하므로 측정접점의 절대온도 환산에는 기준접점 온도 정보가 필요하다.
- 판정 이유: 최신 정본의 E(Th,Tc)=E0(Th)−E0(Tc), 같은 ΔT에서 다른 emf 가능, 알려진 기준조건·형식별 변환관계 소실. 현 정본 유지.
- P1-C 제안: 현 정본 유지
- 중요도: must; 정본 변경 이력: YES; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `thermocouple_measures_temperature_difference@2`; status=approved; verification=verified; Registry statement: 균질한 열전대 재료쌍과 지정 극성에서 측정접점과 기준접점의 온도를 각각 `T_m`, `T_r`로 하면, 순 열기전력은 해당 형식의 기준함수 차 `E(T_m) − E(T_r)`이다. 기준접점 온도가 고정된 경우 해당 형식의 유효 범위에서 온도차로 전압 변화를 설명할 수 있다.
- Registry 조건: thermocouple_material_pair_known
- 직접 요구 문항: 열전대의 측정원리와 기준접점 보상 방법을 설명하시오. / Seebeck 효과와 열전대 온도 측정의 관계를 설명하시오. / 열전대의 측정접점과 기준접점의 역할을 설명하시오.
- 정본 source_basis: reviewed thermocouple requirements Markdown
- 기존 근거 locator (재열람 아님): NIST, Thermocouple: Mercury Thermometer Alternatives — Temperature difference and reference point (https://www.nist.gov/pml/sensor-science/thermodynamic-metrology/mercury-thermometer-alternatives/mercury-thermometer-5)

#### 44. `thermocouple_reference_junction_compensation` — REVISE

- 최신 정본: 현대의 냉접점 보상은 기준접점을 실제 0°C로 유지하는 방식만을 의미하지 않는다. 일반적으로 입력 단자 주변의 온도를 별도 센서로 측정하고, 해당 기준접점 온도에 대응하는 열기전력을 계산하여 측정 열기전력과 결합한 뒤 측정접점 온도로 환산한다. CJC 센서 위치, 단자대의 등온성, 내부 온도구배와 보상 알고리즘은 오차에 영향을 준다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 열전대 냉접점 보상은 기준접점 단자 온도를 별도 센서로 측정하고 해당 열기전력으로 보정해 측정접점 온도를 계산하며, 단자 온도구배와 센서 위치는 오차원이 된다.
- 판정 이유: 전자식 CJC를 일반 방식으로 한정, 기준접점 열기전력 합성 및 등온 조건 유지.
- P1-C 제안: 전자식 냉접점 보상은 기준접점 단자 온도를 별도 센서로 측정하고 해당 온도의 열기전력을 측정 열기전력과 합성해 측정접점 온도로 환산하며, 단자 등온성·온도구배·센서 위치와 보상 알고리즘은 오차에 영향을 준다.
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `thermocouple_reference_junction_compensation@1`; status=approved; verification=verified; Registry statement: 전자식 냉접점 보상은 기준접점 온도를 측정하고 그 온도에 대응하는 열기전력을 보상하여 측정접점 온도로 환산한다. 단자대 접점들의 온도 불균일은 보상 오차를 만들 수 있다.
- Registry 조건: cjc_sensor_tracks_actual_terminal_junction_temperature; thermocouple_type_known
- 직접 요구 문항: 열전대의 측정원리와 기준접점 보상 방법을 설명하시오. / 열전대의 측정접점과 기준접점의 역할을 설명하시오. / 냉접점 보상의 필요성과 구현 방법을 설명하시오. / 열전대 transmitter의 신호처리와 선형화 과정을 설명하시오.
- 정본 source_basis: reviewed thermocouple requirements Markdown
- 기존 근거 locator (재열람 아님): National Instruments, Cold Junction Compensation and Why It Is Needed — Reference junctions created at DAQ terminals and CJC (https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000P6wvSAC&l=en-US); National Instruments, Thermocouple DAQ CJC and Voltage Correction — Measure CJC temperature and convert to voltage correction (https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000kFe3SAE&l=en-US)

#### 45. `thermocouple_law_of_intermediate_metals` — APPROVE

- 최신 정본: 열전대 회로에 제3의 금속이 삽입되더라도 그 금속과 열전대 재료 사이에 형성된 두 접점이 동일한 온도에 있으면 순 열기전력은 변하지 않는다. 따라서 단자대, 커넥터와 계측기 내부 도체를 사용할 수 있다. 다만 두 접점의 온도가 다르거나 등온 조건이 깨지면 추가 오차가 발생할 수 있다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 열전대 회로에 삽입된 제3 금속의 두 접점이 등온이면 그 금속이 순 열기전력을 바꾸지 않으나 등온 조건이 깨지면 오차가 생길 수 있다.
- 판정 이유: 추가 금속 접점의 등온 조건·순 열기전력 불변·비등온 오차 보존.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `thermocouple_law_of_intermediate_metals@1`; status=approved; verification=verified; Registry statement: 열전대 회로에 제3 금속을 삽입할 때 그 금속과 열전대 재료 사이 두 접점이 같은 온도이면 순 열기전력 변화가 상쇄된다. 두 접점 온도가 다르면 추가 열기전력이 생길 수 있다.
- Registry 조건: homogeneous_materials; isothermal_added_junctions
- 직접 요구 문항: 열전대의 중간금속 법칙과 중간온도 법칙을 설명하시오.
- 정본 source_basis: reviewed thermocouple requirements Markdown
- 기존 근거 locator (재열람 아님): Seebeck 적분식에 의한 중간금속 법칙 유도 — Added-metal contribution is the difference of two equal-temperature Seebeck integrals; NBS Special Publication 300, Precision Measurement and Calibration: Selected NBS Papers on Temperature — Thermocouple laws of successive/intermediate temperatures (https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nbsspecialpublication300v2.pdf)

#### 46. `thermocouple_law_of_intermediate_temperatures` — APPROVE

- 최신 정본: 열전대의 기준접점 온도를 변경할 때 열기전력은 중간온도 법칙에 따라 합성할 수 있다. E(T1,T3) = E(T1,T2) + E(T2,T3) 이 관계는 기준접점 보상과 표준 열기전력표 환산의 이론적 근거이다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 열전대의 중간온도 법칙은 E(T1,T3)=E(T1,T2)+E(T2,T3)로 표현되며 기준접점 보상과 기준 열기전력표 환산에 이용된다.
- 판정 이유: 중간온도 합성식과 CJC/기준표 응용 보존. 동일 형식·기준 관례의 Registry 조건 불변.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `thermocouple_law_of_intermediate_temperatures@1`; status=approved; verification=verified; Registry statement: 열전대의 기전력은 중간온도 법칙을 만족한다: E(T1,T3)=E(T1,T2)+E(T2,T3).
- Registry 조건: same_thermocouple_type_and_reference_convention; homogeneous_thermoelements
- 직접 요구 문항: 냉접점 보상의 필요성과 구현 방법을 설명하시오. / 열전대의 중간금속 법칙과 중간온도 법칙을 설명하시오.
- 정본 source_basis: reviewed thermocouple requirements Markdown
- 기존 근거 locator (재열람 아님): NBS Special Publication 300, Precision Measurement and Calibration: Selected NBS Papers on Temperature — Law of Successive or Intermediate Temperatures (https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nbsspecialpublication300v2.pdf)

#### 47. `thermocouple_nonlinearity_reference_tables_polynomial_conversion` — APPROVE

- 최신 정본: 열전대 열기전력과 온도의 관계는 비선형이다. 따라서 열전대 종류별 표준 열기전력표 또는 표준 다항식을 사용하여 전압을 온도로 환산한다. 열전대 종류가 다르면 동일한 전압-온도 변환식을 사용할 수 없다. 다항식 적용 범위와 단위를 확인해야 하며, 범위 밖 외삽은 제한해야 한다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 열전대의 비선형 열기전력은 열전대 형식별 표준 열기전력표나 다항식의 유효 온도범위·단위에 맞춰 온도로 환산해야 한다.
- 판정 이유: 비선형·형식별 표/다항식·유효 범위·단위 보존. 외삽 허용하지 않음.
- P1-C 제안: 과거 단문화 후보 (추가 승인 전 미적용)
- 중요도: must; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `thermocouple_nonlinearity_reference_tables_polynomial_conversion@1`; status=approved; verification=verified; Registry statement: 열전대 전압-온도 관계는 종류별로 비선형이며, 지정 온도범위에 맞는 NIST ITS-90 기준함수 또는 표를 사용해 환산해야 한다.
- Registry 조건: correct_thermocouple_type; within_reference_function_range
- 직접 요구 문항: 열전대의 측정원리와 기준접점 보상 방법을 설명하시오. / 열전대 transmitter의 신호처리와 선형화 과정을 설명하시오.
- 정본 source_basis: reviewed thermocouple requirements Markdown
- 기존 근거 locator (재열람 아님): NIST Monograph 175, Temperature-Electromotive Force Reference Functions and Tables Based on ITS-90 — Type-specific ITS-90 functions, tables and temperature ranges (https://nvlpubs.nist.gov/nistpubs/Legacy/MONO/nistmonograph175.pdf)

#### 48. `thermocouple_thermowell_installation_dynamic_error` — REVISE

- 최신 정본: 보호관, 삽입길이, 유속, 배관 벽면과의 열전도, 복사, 접촉상태는 측정접점이 실제 공정 온도에 도달하는 과정에 영향을 준다. 열전대 자체의 전기적 원리가 정확해도 설치가 부적절하면 열전달 오차와 응답지연이 발생한다. 보호관의 열용량이 증가하면 일반적으로 응답이 느려진다.
- 과거 정본: 최신 정본과 동일
- 과거 단문화 후보: 열전대의 열전달 오차와 응답시간은 보호관·침지길이·유속·벽면 열전도·복사·접촉상태 등 설치조건의 영향을 받는다.
- 판정 이유: 설치 변수 나열만으로는 공정 온도와 실제 접점 온도 차 및 열용량-응답 관계 소실.
- P1-C 제안: 열전대는 보호관·침지길이·유속·벽면 열전도·복사·접촉상태에 따라 공정 온도와 측정접점 온도 차 및 응답지연이 생길 수 있으며, 보호관 열용량이 증가하면 일반적으로 응답이 느려진다.
- 중요도: important; 정본 변경 이력: NO; 제외: NOT_LISTED; score_effect=none (이번 검토).
- Registry: `thermocouple_thermowell_installation_dynamic_error@1`; status=approved; verification=verified; Registry statement: 열전대 측정접점이 공정온도를 추종하는 정확도와 응답은 thermowell, 삽입 깊이, 유속과 열전달, 배관으로의 stem conduction, 복사환경 및 센서·보호관 사이의 열접촉에 영향을 받는다. 열용량이 커지고 열전달 경로가 같다면 응답시간은 일반적으로 증가한다.
- Registry 조건: sensor_installed_in_nonuniform_thermal_environment; specific_probe_and_process_geometry_considered
- 직접 요구 문항: 열전대 측정오차의 원인과 진단·개선 방법을 설명하시오. / 접지형·비접지형·노출형 열전대 접점의 특성을 설명하시오.
- 정본 source_basis: reviewed thermocouple requirements Markdown
- 기존 근거 locator (재열람 아님): Emerson, Temperature Measurement, Control Key to Plant Performance, ISA Automation Basics — p. 2; thermowell time constants under changes in process velocity, annular clearance, and fill material (https://www.emerson.com/is/content/emerson/en/corporate/news-and-events/articles/documents/temperature-measurement-control-key-to-plant-performance.pdf); Emerson, Rosemount 114C Thermowells Product Data Sheet — Thermowell length and stem profile selection; required response speed, flow drag and immersion guidance (https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/temperature/documents/doc-rosemount-00813-0200-4952.pdf); Emerson, Rosemount X-well Technology: Accuracy and Installation FAQ — FAQ: accuracy compared with standard thermowells and surface sensors (https://www.emerson.com/en/measurement-instrumentation/products/rosemount-x-well-technology-family); National Bureau of Standards, Radiation Errors in Air Ducts Under Nonisothermal Conditions Using Thermocouples, Thermistors, and a Resistance Thermometer, Building Science Series 26 — Study of radiation error in moving-air thermocouple measurements with differing duct-wall temperatures and radiation shields (https://firedoc.nist.gov/article/33cyXYQBWEcjUZEYeo5I); NIST, Guide to Secondary Thermometry: Industrial Platinum Resistance Thermometers — §4.2.1; immersion depth, sheath conduction and immersion error model (https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=932587); Lumped thermal-capacitance energy balance for a sensor/well assembly — τ≈C_th/G_th for a first-order thermal response


## Coverage / gate

- 48 unique IDs, 7 owners, 48 canonical + manifest + Registry + P1-A joins, 46 directly referenced by expected_question_patterns, 2 not directly referenced. All five newer canonical statements retained. 2 exclusions preserved. 0 canonical/Registry/Generated/approval/score changes. This report is document-only, with no new approval or deployment.
