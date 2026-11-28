# P1-C — 최소 정본 변경 후보 확정 (2026-11-25)

- Baseline main: `45c7d146e4673e885005c04535e65dc9b9d7c8a5`; P1-B: `2b66a4d4cd5a2322aa2849abb62b970ad72ecd47` / blob `58f3c0dca0bb42c8393a7246d2a214bf3d16fa55`.
- [Review-only candidate JSON](p1c_minimal_anchor_change_candidates_20261125.json) blob `d088aa133640e7853a7830a4a7d1f8d5ee6eb44e`. 48 unique dispositions: P1-B 40개 pool 중 8개 준비, 32개 현행 유지, 이전 REJECT 6/HOLD 2 유지. 후보는 4 Topic, 신규 ID 0, 정본 적용 0, 승인 0, score_effect=none. 이 JSON은 보고서 데이터이며 runtime schema/loader 입력이 아니다.
- 기준: 단축률이 아닌 독립적으로 설명 가능한 사실의 적용 조건, 변수 단위, 예외, 과도한 일반화 방지 등 실제 변경 가치. 32개 유지 이유는 JSON dispositions에 개별 기록. P1-B 승인 권고는 소유자의 명시적 적용 승인으로 해석하지 않음.
- 검토: 4 Topic의 fact_anchor/model_answer/logic_check 정본을 main에서 읽고 8건의 기존 Registry 조건·기존 verification_refs·accepted/rejected 설명·grading_notes·required_anchor_ids와 대조. 외부 원문 재열람은 NOT_RUN. P1-A/B의 48개 제외/소유/기술 검토 이력 재사용. 별도 신규 독립 457 전수 검토 없음.

## 1. 확정 후보 (적용 전)

### 1. `rh_temperature_dependence`

- 기존: 수증기량이 거의 변하지 않아도 공기온도가 올라가면 P_ws(T)가 증가하여 RH가 낮아질 수 있고, 냉각하면 RH가 증가하여 100%에 접근할 수 있다. 따라서 RH sensor는 sensor temperature와 process temperature의 차이에 민감하다.
- 후보: 수증기 분압을 거의 일정하게 유지하는 응축 전 조건에서 공기온도가 올라가면 P_ws(T)가 증가하여 RH가 낮아지고, 냉각하면 RH가 증가하여 100%에 접근한다. RH sensor는 sensor temperature와 process temperature의 차이에 민감하다.
- 변경 실익: 수증기량 일정과 분압 일정의 혼동 제거; 포화 이전의 변화 방향과 센서 온도 조건 유지.
- 기존 근거 및 기술 판단: RH=100 P_w/P_ws(T): P_w 고정, P_ws 증가 → RH 감소; 냉각 중 응축이 시작되면 같은 분압 가정으로 계속 외삽하지 않는다.
- 대조 답안 기대 (수기 설계, 실행 결과 아님): 수증기 분압 고정 조건의 가열·냉각 설명은 허용; 수증기 질량만 고정하면 모든 압력·체적 조건에서 동일하다는 주장은 허용하지 않음.
- Registry: `relative_humidity_varies_with_temperature_at_fixed_vapor_pressure@1` / water_vapor_partial_pressure_is_approximately_unchanged; temperature_remains_below_water_critical_temperature; no_condensation_or_moisture_addition_removes_or_adds_vapor
- 직접 연결 문항: Relative humidity, absolute humidity 및 dew point를 비교하여 설명하시오. / Very low humidity에서 RH 대신 dew point 측정을 고려하는 이유를 설명하시오.
- 기존 문장 exact-copy 위치: fact_anchor=/anchors/2/statement, /anchors/2/accepted_explanations/0, /anchors/2/claim, /anchors/2/description, /core_facts/2; logic_check=/llm_profile/truth_schema/2; model_answer=없음

### 2. `psychrometric_wet_dry_bulb`

- 기존: Psychrometric method는 dry-bulb와 wetted wet-bulb의 증발냉각 차이를 이용하고, airflow·wick·water purity·pressure를 고려한 psychrometric relation으로 humidity를 구한다. Wet-bulb temperature를 dew point와 동일시하지 않는다.
- 후보: Psychrometric method는 dry-bulb와 wetted wet-bulb의 증발냉각 차이를 이용하고, airflow·wick·water purity·pressure를 고려한 psychrometric relation으로 humidity를 구한다. Wet-bulb temperature와 dew point는 포화 상태(100% RH)를 제외하면 서로 다르다.
- 변경 실익: 기존 문장의 무조건 동일시 금지 표현에 Registry의 명시적 포화 예외 반영.
- 기존 근거 및 기술 판단: Registry verification_refs는 RH=100%에서 wet bulb와 dew point의 일치를 명시한다. 적용 가능한 정상 평형 건습구 관계 기준.
- 대조 답안 기대 (수기 설계, 실행 결과 아님): 불포화 상태에서 습구온도=이슬점 단정은 부적합; 포화 상태의 일치 설명은 허용. 직접 required_anchor_ids 연결 없음, 신규 문항 연결 금지.
- Registry: `psychrometric_wet_bulb_is_not_dew_point_except_at_saturation@1` / air_pressure_and_psychrometric_convention_are_accounted_for; wet_bulb_is_not_identified_as_dew_point_except_at_saturation
- 직접 연결 문항: 없음; 문항 scope 추가 금지
- 기존 문장 exact-copy 위치: fact_anchor=/anchors/15/statement, /anchors/15/accepted_explanations/0, /anchors/15/claim, /anchors/15/description, /core_facts/15; logic_check=/llm_profile/truth_schema/15; model_answer=없음

### 3. `feedback_parameter_sensitivity`

- 기존: 피드백 전달 H가 고정된 경우 순방향 전달 G의 상대 변화에 대한 폐루프 전달함수의 상대 민감도는 S(s)와 연결된다. |L|가 충분히 큰 주파수 영역에서는 |S|가 작아져 모델 변화의 영향이 감소할 수 있지만 모든 주파수에서 S를 임의로 작게 만들 수는 없다.
- 후보: 음의 피드백에서 H가 고정된 경우 폐루프 기준입력 전달함수 G/(1+GH)의 G에 대한 미소 상대 민감도는 S(s)=1/[1+G(s)H(s)]이다(L=GH). |L|가 충분히 큰 주파수 영역에서는 |S|가 작아져 모델 변화의 영향이 감소할 수 있지만 모든 주파수에서 S를 임의로 작게 만들 수는 없다.
- 변경 실익: 모호한 'S와 연결된다'를 Registry가 이미 검증한 정확한 관계로 명확화; 미소 상대 변화·고정 H 보존.
- 기존 근거 및 기술 판단: F=G/(1+GH), (G/F)∂F/∂G=1/(1+GH), F와 분모가 정의되는 상대 민감도 영역에서 성립.
- 대조 답안 기대 (수기 설계, 실행 결과 아님): 고정 H에서 S 식 제시는 허용; H도 동시에 변하는 모든 경우 같은 민감도 또는 모든 주파수 완전 제거 단정은 부적합.
- Registry: `closed_loop_parameter_sensitivity@1` / feedback_path_fixed; differentiable_transfer_function
- 직접 연결 문항: 음의 피드백 시스템의 민감도 S와 상보 민감도 T의 의미를 설명하시오. / Feedback System의 추종성, 민감도 및 정상상태 오차 개선 방법을 설명하시오.
- 기존 문장 exact-copy 위치: fact_anchor=/anchors/3/statement, /anchors/3/claim, /anchors/3/description, /core_facts/3; logic_check=/llm_profile/truth_schema/3; model_answer=없음

### 4. `feedback_integral_action_tradeoff`

- 기존: 유효 루프에 상쇄되지 않은 원점 적분기를 추가하는 적분 동작은 시스템 형을 증가시켜 정상상태 오차 제거에 기여할 수 있다. 그러나 위상여유 감소, 액추에이터 포화 및 적분 windup을 유발할 수 있으므로 anti-windup과 포화 처리가 필요하다.
- 후보: 유효 루프에 상쇄되지 않은 원점 적분기를 추가하면 시스템 형이 증가하고, 안정한 단위 피드백에서 해당 입력에 대한 정상상태 오차 감소 또는 제거에 기여할 수 있다. 위상여유 감소와 액추에이터 포화를 검토하고, 포화 중 적분 windup을 방지하기 위해 필요한 anti-windup과 포화 처리를 적용한다.
- 변경 실익: 기존 오차 개선 주장의 안정성·입력 범위 및 windup의 포화 조건 명시.
- 기존 근거 및 기술 판단: Registry 기존 stable unity feedback, uncancelled integrator, actuator saturation 조건과 error-constant 및 anti-windup 근거를 그대로 따름.
- 대조 답안 기대 (수기 설계, 실행 결과 아님): 상쇄되지 않은 원점 극·안정 폐루프 조건의 오차 개선 가능성 허용; 상쇄/안정성과 무관한 항상 개선 또는 포화 중 windup 불가 주장 부적합.
- Registry: `feedback_integral_action_tradeoff@1` / stable_unity_feedback_for_error_claim; integrator_not_cancelled; actuator_saturation_for_windup_claim
- 직접 연결 문항: Feedback System의 추종성, 민감도 및 정상상태 오차 개선 방법을 설명하시오.
- 기존 문장 exact-copy 위치: fact_anchor=/anchors/8/statement, /anchors/8/claim, /anchors/8/description; logic_check=/llm_profile/truth_schema/8; model_answer=없음

### 5. `diaphragm_deflection_principle`

- 기존: Diaphragm pressure element는 막 양측의 압력차가 만드는 탄성변형을 변위 또는 전기신호로 변환한다. 얇고 유연한 diaphragm은 작은 압력차에 높은 감도를 얻을 수 있다.
- 후보: Diaphragm pressure element는 막 양측의 압력차가 만드는 탄성변형을 변위 또는 전기신호로 변환한다. 재질·지지·형상(두께 제외) 등 다른 조건이 유사하고 소변형 탄성 범위이면 얇고 유연한 diaphragm은 작은 압력차에 높은 감도를 얻을 수 있다.
- 변경 실익: 두께 하나만으로 감도가 정해진다는 일반화 방지; 원래의 비교 방향 유지.
- 기존 근거 및 기술 판단: Registry 기록의 소변형 원형판 예 w0∝Δp·a^4/(E·t^3), 반경·재질·지지 고정일 때의 비교; 실제 설계 한계는 별도.
- 대조 답안 기대 (수기 설계, 실행 결과 아님): 비교 조건이 같은 얇은 막의 높은 감도 가능성 허용; 재질·형상·지지와 무관하게 두께만으로 감도 결정 단정 부적합.
- Registry: `diaphragm_differential_pressure_deflection_and_sensitivity@1` / pressure_difference_is_applied_across_the_diaphragm_faces; elastic_response_remains_within_the_design_range; sensitivity_comparison_holds_other_geometry_material_and_support_conditions_comparable; overload_stress_linearity_and_stability_limits_are_checked
- 직접 연결 문항: Diaphragm pressure element의 원리와 적용 시 고려사항을 설명하시오. / Bourdon, Diaphragm, Piezoresistive pressure sensor를 비교하고 선정기준을 설명하시오.
- 기존 문장 exact-copy 위치: fact_anchor=/anchors/5/statement, /anchors/5/accepted_explanations/0, /anchors/5/claim, /anchors/5/description, /core_facts/5; logic_check=/llm_profile/truth_schema/5; model_answer=없음

### 6. `dp_transmitter_two_port_principle`

- 기존: DP transmitter는 high-side와 low-side 두 입력의 압력차를 sensing element에 전달하여 차압을 전기신호로 변환한다. 두 포트에 동일한 압력이 인가된 상태는 이상적으로 zero differential pressure 조건이다.
- 후보: DP transmitter는 high-side와 low-side 두 입력의 압력차 ΔP=P_H−P_L를 sensing element에 전달하여 전기신호로 변환한다. 두 포트의 압력이 같으면 이상적인 차압 입력은 0이지만 실제 출력의 영점 오차나 정압 영향까지 없다는 뜻은 아니다.
- 변경 실익: 동일 포트압=차압 입력 0과 실제 출력 영점 보증을 구분; P1-B 수용안에 이미 Registry가 명시한 제한만 반영.
- 기존 근거 및 기술 판단: Registry의 pressure difference/zero offset/static pressure 구분 및 zero trim locator.
- 대조 답안 기대 (수기 설계, 실행 결과 아님): 동일 포트압에서 차압 입력 0 허용; 실제 전송기 출력이 반드시 영점이거나 정압 영향이 없다는 단정은 부적합. 4–20 mA의 출력값을 0 mA로 오인하지 않음.
- Registry: `differential_pressure_transmitter_two_port_sensing@1` / high_and_low_ports_are_correctly_identified_and_connected; equal_port_pressures_define_zero_differential_input_not_necessarily_zero_output; static_pressure_and_zero_offset_are_checked_for_the_specific_device
- 직접 연결 문항: DP transmitter의 원리와 high static line pressure 영향을 설명하시오. / Impulse line을 사용하는 pressure/DP 측정의 설치오차와 대책을 설명하시오.
- 기존 문장 exact-copy 위치: fact_anchor=/anchors/10/statement, /anchors/10/accepted_explanations/0, /anchors/10/claim, /anchors/10/description, /core_facts/10; logic_check=/llm_profile/truth_schema/10; model_answer=없음

### 7. `pulse_frequency_speed_equation`

- 기존: 회전당 유효 count 수를 N_eff, 측정 pulse frequency를 f[Hz]라 하면 n[rpm] = 60f/N_eff로 계산한다. N_eff는 encoder PPR뿐 아니라 edge counting과 x1/x2/x4 decoding 정의를 반영해야 한다.
- 후보: 회전당 유효 count 수를 N_eff[count/rev], 같은 계수 기준에서 실제 계수하는 이벤트 빈도를 f[count/s]라 하면 n[rpm] = 60f/N_eff로 계산한다. N_eff는 encoder PPR 정의와 edge counting 및 x1/x2/x4 decoding을 반영해야 한다.
- 변경 실익: 분자·분모의 계수 기준 통일, 물리 채널 주파수와 decoded count rate 혼동 방지.
- 기존 근거 및 기술 판단: f/N_eff = rev/s; ×60 s/min = rpm. Registry의 counted pulses per second 및 decoder convention 근거.
- 대조 답안 기대 (수기 설계, 실행 결과 아님): 채널 100 pulse/rev, x4, 1000 rpm이면 1666.7 physical pulse/s와 6666.7 count/s; N_eff=400에는 후자를 사용. 다른 기준 혼합 부적합.
- Registry: `encoder_pulse_frequency_to_rpm_equation@1` / f_is_counted_pulses_per_second; n_eff_is_counted_edges_per_mechanical_revolution; decoder_mode_and_catalog_ppr_definition_are_consistent
- 직접 연결 문항: 회전속도 계측에서 pulse frequency와 RPM의 관계 및 측정방법을 설명하시오.
- 기존 문장 exact-copy 위치: fact_anchor=/anchors/1/statement, /anchors/1/accepted_explanations/0, /anchors/1/claim, /anchors/1/description, /core_facts/1; logic_check=/llm_profile/truth_schema/1; model_answer=없음

### 8. `period_measurement_low_speed`

- 기존: 저속에서는 연속 유효 pulse 사이의 시간 T_c를 측정하여 n = 60/(N_eff·T_c)로 계산하는 reciprocal/period 방식이 fixed-window count 방식보다 유리할 수 있다. 단, timer resolution과 jitter의 영향을 검토해야 한다.
- 후보: 저속에서는 등각도 간격의 연속 유효 pulse 사이의 시간 T_c[s]를 측정하여 구간 평균속도 n[rpm] = 60/(N_eff·T_c)로 계산하는 reciprocal/period 방식이 fixed-window count 방식보다 유리할 수 있다. 단, timer resolution과 jitter의 영향을 검토해야 한다.
- 변경 실익: 시간 단위와 등각도 간격 전제 명시, 비등간격 국부 period 오용 방지.
- 기존 근거 및 기술 판단: 회전당 N_eff개의 등각도 이벤트에서 Δθ=2π/N_eff, n=60/(N_eff T_c); 비등간격의 실제 각도 간격 원리는 최신 gear_tooth_speed_equation과 일치. Registry의 valid consecutive pulses/missing-extra edge 조건과 연계.
- 대조 답안 기대 (수기 설계, 실행 결과 아님): 등각도 연속 이벤트 구간 평균식 허용; 결손치 간격을 정상 간격으로 취급하거나 timer/jitter 한계가 없다는 주장 부적합.
- Registry: `rotation_speed_period_measurement_formula_and_low_speed_tradeoff@1` / effective_pulses_per_revolution_match_the_actual_edge_counting_mode; pulse_period_is_measured_in_seconds_between_valid_consecutive_pulses; missing_or_extra_edges_are_excluded_or_accounted_for; timer_resolution_and_timing_jitter_are_within_required_error
- 직접 연결 문항: 회전속도 계측에서 pulse frequency와 RPM의 관계 및 측정방법을 설명하시오. / 저속과 고속의 회전수 측정에서 resolution과 response time trade-off를 설명하시오.
- 기존 문장 exact-copy 위치: fact_anchor=/anchors/3/statement, /anchors/3/accepted_explanations/0, /anchors/3/claim, /anchors/3/description, /core_facts/3; logic_check=/llm_profile/truth_schema/3; model_answer=없음

## 2. 적용 계약 및 안전 경계

실제 adapter `grading/evidence/fact_anchor_evidence_adapter.py` main 기준 L79–81, L173–175, L585–600에서 statement/accepted_explanations 및 statement/claim을 token, 질문 범위, reference text, requirement text에 사용한다. 따라서 단순 문구 변경도 채점 회귀 위험이 있다. 기존 승인 적용 기록 `reports/fact_anchor_approval_application_20261125.md` L34, L49–54를 적용 절차의 선례로 참조했다.

- 정확 복제 위치 총 37개 fact_anchor 필드, 8개 logic_check truth_schema 필드, 0개 model_answer 필드. 문장 복제의 동기화 대상 *후보*이며 일괄 문자열 치환 허가 아님. 적용 시 파일 SHA/기존 값/owner/ID를 재검증하고 동일 복제만 공식 절차에 따라 정렬한다. 비동일 accepted/rejected explanations, fatal wrong claims, 중요도, keywords/core_terms, 기존 deterministic checks/문항 범위, Registry relation/conditions/revision/approval/hash는 유지. 기존 Registry 문장 자체 수정 불필요로 판단했으며 변경 필요 발견 시 별도 승인. 8개 모두 legacy Topic; managed approval 승격 금지. Generated/ledger는 공식 builder 및 기존 정책으로만 재생성, 수동 변경 금지.
- 소유자 명시 승인 전 source/Registry/Generated/ledger 변경 금지. 119 HOLD/D4/4계층 exclusion/A–E 권한/배점 불변. #33/#34/#35/#48 소유 경계 유지. P2-A는 별도 비채점 계약 매핑으로 진행 가능하나 P1-C 후보를 승인 Fact로 사용하지 않는다.
- 별도 승인 이후 집중 대조 답안 및 기존 요구/오답 조건, protected 143 answer byte-identical replay, 전체 pytest, validate-all, Generated freshness, Release Candidate 및 동일 SHA Actions. 차이 발생 시 승인/적용 게이트 차단 후 원인분석; 기대값을 억지로 수정하지 않는다. source hash/ledger 갱신 여부와 구체 명령은 기존 workflow로 확정. 현재 Python/pytest/validate-all/143 replay/Actions/실제 source hash 재계산 모두 NOT_RUN. 수기 대조는 실행 시험이 아니다. Firecrawl 미사용.

## 3. 48개 최종 처분

| Anchor ID | P1-B | P1-C | 이유 |
|---|---|---|---|
| `fsrm_markov_state_transition` | APPROVE | KEEP_CANONICAL | SIS 상태 예시와 고정 목록/시간변화율 비필수 설명은 기능안전 비교 답안에 유용. 단축 이득보다 범위 손실 큼. |
| `fsrm_markov_complexity` | HOLD | PRESERVE_HOLD | 기존 제외/보류 유지. |
| `fsrm_model_assumption_documentation` | REVISE | KEEP_CANONICAL | 진단 coverage, proof-test 주기·coverage, 수리 가용성·시간 및 override 등 구체 입력을 유지하는 편이 안전. |
| `sw10_fat_sat_relation` | APPROVE | KEEP_CANONICAL | FAT/SAT 조건과 승인 시험계획이 이미 명확. 문장 압축만 필요하지 않음. |
| `sw10_loop_test` | REVISE | KEEP_CANONICAL | 폐루프 최종요소/감시 루프 예외의 명시가 기존 문장에 더 분명. |
| `relative_humidity_definition` | APPROVE | KEEP_CANONICAL | 정의식과 온도의존성 연결은 학습상 유익. 다른 Anchor 중복만으로 삭제하지 않음. |
| `rh_temperature_dependence` | REVISE | PREPARE_CANDIDATE | 수증기량 일정과 분압 일정의 혼동 제거; 포화 이전의 변화 방향과 센서 온도 조건 유지. |
| `absolute_humidity_definition` | REJECT | KEEP_CANONICAL | P1-B 거절 결정 유지, 최신 기술 보완 및 문항 범위 보존. |
| `dew_point_definition` | APPROVE | KEEP_CANONICAL | 정의와 응축 위험 연결 유지. 압축 실익 없음. |
| `frost_point_distinction` | APPROVE | KEEP_CANONICAL | 영하 사양의 정의·계산 기준 확인 조건 유지. |
| `pressure_dew_point_effect` | REVISE | KEEP_CANONICAL | 압력과 응축 인과가 이미 두 문장에 표현됨. |
| `capacitive_polymer_principle` | APPROVE | KEEP_CANONICAL | 전극/전자회로 포함 변환 원리가 이미 명확. 번역·축약만으로 변경하지 않음. |
| `resistive_humidity_principle` | REVISE | KEEP_CANONICAL | 이온전도 사례와 재료별 일반화 금지 조건이 이미 명시됨. |
| `psychrometric_wet_dry_bulb` | REVISE | PREPARE_CANDIDATE | 기존 문장의 무조건 동일시 금지 표현에 Registry의 명시적 포화 예외 반영. |
| `condensation_sensor_temperature_error` | REVISE | KEEP_CANONICAL | 기존 문장 자체가 냉각/가열 방향과 self-heating을 명시; 분압 조건은 7번과 Registry로 보완됨. 추가 변경 실익 부족. |
| `low_humidity_dew_point_selection` | HOLD | PRESERVE_HOLD | 기존 제외/보류 유지. |
| `selection_environment_process` | APPROVE | KEEP_CANONICAL | 제품별 recovery/설치 제약 및 인증 별도 적용기준 보존 가치가 더 큼. |
| `feedback_sensitivity_functions` | APPROVE | KEEP_CANONICAL | 표준 음의 피드백 범위는 기존 질문·Registry에서 정의되어 있고 식 및 S/T 구별 명확. 단순 축약 불필요. |
| `feedback_parameter_sensitivity` | REVISE | PREPARE_CANDIDATE | 모호한 'S와 연결된다'를 Registry가 이미 검증한 정확한 관계로 명확화; 미소 상대 변화·고정 H 보존. |
| `feedback_disturbance_noise_paths` | APPROVE | KEEP_CANONICAL | 신호 주입 위치를 먼저 정의하라는 기존 조건 명확. |
| `feedback_steady_state_error_final_value` | APPROVE | KEEP_CANONICAL | 최종값 정리의 불가 사례를 남겨 오답 경계 보존. |
| `feedback_integral_action_tradeoff` | REVISE | PREPARE_CANDIDATE | 기존 오차 개선 주장의 안정성·입력 범위 및 windup의 포화 조건 명시. |
| `bourdon_forms_application` | REVISE | KEEP_CANONICAL | 형상·압력범위 및 적용이 이미 명확; 재표현 효과 제한. |
| `diaphragm_deflection_principle` | REVISE | PREPARE_CANDIDATE | 두께 하나만으로 감도가 정해진다는 일반화 방지; 원래의 비교 방향 유지. |
| `diaphragm_sensor_vs_seal` | REVISE | KEEP_CANONICAL | 감지와 격리, 선택적 구성 및 오차 비제거 명시됨. |
| `piezoresistive_static_capability` | REVISE | KEEP_CANONICAL | 외부 여기와 정적 측정 비교 이미 충분; 드리프트 추가 문구는 별도 실익 부족. |
| `dp_transmitter_two_port_principle` | APPROVE | PREPARE_CANDIDATE | 동일 포트압=차압 입력 0과 실제 출력 영점 보증을 구분; P1-B 수용안에 이미 Registry가 명시한 제한만 반영. |
| `ambient_environment_hazardous_selection` | REVISE | KEEP_CANONICAL | 설치공간과 Topic 소유 경계 명확. |
| `accuracy_total_performance_terms` | REVISE | KEEP_CANONICAL | 제조사 정의 및 reference accuracy/total performance 구별 명확. |
| `pulse_frequency_speed_equation` | REVISE | PREPARE_CANDIDATE | 분자·분모의 계수 기준 통일, 물리 채널 주파수와 decoded count rate 혼동 방지. |
| `counting_window_speed_equation` | REJECT | KEEP_CANONICAL | P1-B 거절 결정 유지, 최신 기술 보완 및 문항 범위 보존. |
| `period_measurement_low_speed` | REVISE | PREPARE_CANDIDATE | 시간 단위와 등각도 간격 전제 명시, 비등간격 국부 period 오용 방지. |
| `quadrature_direction_principle` | APPROVE | KEEP_CANONICAL | A/B 방향과 회전당 유효 계수 정의가 이미 명확. |
| `index_z_channel_role` | APPROVE | KEEP_CANONICAL | 기준 펄스와 다회전 절대위치 한계 이미 명확. |
| `absolute_encoder_principle` | REVISE | KEEP_CANONICAL | 현재 정본에 sample interval이 명시되어 있음. |
| `encoder_frequency_limit_selection` | REJECT | KEEP_CANONICAL | P1-B 거절 결정 유지, 최신 기술 보완 및 문항 범위 보존. |
| `inductive_proximity_principle` | APPROVE | KEEP_CANONICAL | 톱니와 flag 적용 범위 보존. 번역·축약 실익 없음. |
| `gear_tooth_speed_equation` | REJECT | KEEP_CANONICAL | P1-B 거절 결정 유지, 최신 기술 보완 및 문항 범위 보존. |
| `tachogenerator_voltage_speed_principle` | APPROVE | KEEP_CANONICAL | 아날로그 속도 변환 및 비례식 모두 명확. |
| `digital_tachometer_instrument_boundary` | APPROVE | KEEP_CANONICAL | 계측기와 센서 경계의 기존 명시 충분. |
| `thermocouple_temperature_measurement_chain` | REJECT | KEEP_CANONICAL | P1-B 거절 결정 유지, 최신 기술 보완 및 문항 범위 보존. |
| `thermocouple_seebeck_effect_dissimilar_conductors` | APPROVE | KEEP_CANONICAL | 두 도체/접점 온도차 및 비선형 설명 유지 가치 있음. |
| `thermocouple_measures_temperature_difference` | REJECT | KEEP_CANONICAL | P1-B 거절 결정 유지, 최신 기술 보완 및 문항 범위 보존. |
| `thermocouple_reference_junction_compensation` | REVISE | KEEP_CANONICAL | 실제 0°C 유지만 의미하지 않는다는 CJC 오개념 방지 문장 유지. |
| `thermocouple_law_of_intermediate_metals` | APPROVE | KEEP_CANONICAL | 등온의 정확한 접점 및 단자대 활용 설명 보존. |
| `thermocouple_law_of_intermediate_temperatures` | APPROVE | KEEP_CANONICAL | 중간온도 법칙과 적용 근거 명확. |
| `thermocouple_nonlinearity_reference_tables_polynomial_conversion` | APPROVE | KEEP_CANONICAL | 형식별 변환식·외삽 금지의 명시적 경계 보존. |
| `thermocouple_thermowell_installation_dynamic_error` | REVISE | KEEP_CANONICAL | 설치 조건·공정 온도와 접점 차 및 열용량-응답 인과 이미 명확. |

P1-C 후보 선별·문서화 종결, 실제 변경 승인/적용 및 검증은 미완료. Issue #40 OPEN / Draft PR #49 유지. 다음 단계 P2-A.
