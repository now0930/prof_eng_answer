# 제어밸브 고유·설치 유량특성과 Linear·Equal Percentage·Quick Opening Topic Sheet

## 1. Topic metadata

- topic_id: `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`
- title_ko: 제어밸브 고유·설치 유량특성과 Linear·Equal Percentage·Quick Opening
- question_type: `COMPARE_SELECTION`
- supported_question_form: `PRINCIPLE_INTERPRETATION`
- difficulty: `FIELD_APPLICATION`
- selection_importance: `NORMAL`
- roadmap_priority: `★★★★★`
- grading_mode: `LLM_ONLY`
- deterministic_checks: disabled
- candidate_extraction_rules: empty
- semantic_review: ChatGPT manual review
- local_llm_validation: skipped

### 1.1 Topic purpose

이 Topic은 제어밸브의 travel과 flow coefficient 또는 flow 사이 관계를 평가한다.

다음을 핵심으로 한다.

- Inherent Flow Characteristic와 Installed Flow Characteristic의 구분
- Linear, Equal Percentage 및 Quick Opening 비교
- system pressure-drop redistribution에 의한 installed curve 변형
- pump curve, static head 및 system resistance 영향
- 부하범위와 제어 목적에 따른 characteristic 선정
- manufacturer data와 현장검증

### 1.2 Representative questions

1. 제어밸브의 Inherent Flow Characteristic와 Installed Flow Characteristic를 비교하시오.
2. Linear, Equal Percentage 및 Quick Opening 특성을 비교하고 적용 기준을 설명하시오.
3. 제어밸브 고유 유량특성이 실제 배관에서 설치 유량특성으로 변형되는 원인을 설명하시오.
4. Equal Percentage 특성이 넓은 부하범위의 공정에 자주 적용되는 이유를 설명하시오.
5. Linear trim이 실제 배관에서도 항상 linear flow를 보장하지 않는 이유를 설명하시오.
6. Quick Opening Characteristic의 곡선 형상과 적용 분야를 설명하시오.
7. pump curve, static head 및 system resistance가 Installed Characteristic에 미치는 영향을 설명하시오.
8. 공정 운전범위와 제어 목적에 따른 제어밸브 유량특성 선정절차를 설명하시오.
9. Linear, Equal Percentage 및 Quick Opening 곡선을 그리고 동일 travel 변화에 대한 용량 변화를 비교하시오.
10. 제어밸브 유량특성에 관한 제시 설명의 타당성을 검토하시오.

### 1.3 Scope boundary

Topic 1 참조 전용:

- fluid force
- unbalance force
- friction
- actuator sizing
- Fail-Safe spring
- seat load
- worst-case force verification

Topic 3 이관:

- Valve Authority 상세 정의·식·목표범위
- Rangeability 계산과 Turndown 구분
- installed valve gain 정량 계산
- process gain과 loop gain 결합
- oversizing과 authority 저하의 종합평가

Topic 4 이관:

- Cv·Kv 정의와 변환
- liquid sizing
- Reynolds correction
- valve size selection

Topic 6 이관:

- cavitation
- flashing
- liquid choked flow
- damage prevention

Topic 8 이관:

- Balanced·Unbalanced trim 구조
- residual unbalance
- seal friction과 leakage trade-off

Topic 11 이관:

- stiction
- deadband
- hysteresis
- resolution
- mechanical nonlinearity

## 2. Core correct facts

### 2.1 기본 변수와 정규화

- `x = l / l_rated`
- `y = Cv / Cv_rated`
- `l`: 현재 valve travel
- `l_rated`: rated travel
- `Cv`: 현재 flow coefficient
- `Cv_rated`: rated flow coefficient
- 특성곡선은 일반적으로 normalized travel과 relative capacity의 관계로 비교한다.
- seat 근처와 실제 trim에서는 이상곡선과 차이가 있을 수 있다.

### 2.2 Inherent Flow Characteristic

- 밸브 전후 차압과 유체 조건을 일정한 기준조건으로 유지한다.
- valve travel과 flow coefficient 또는 이에 비례하는 flow의 관계다.
- 밸브와 trim 자체의 기준 특성이다.
- 실제 배관 저항, pump curve 및 static head를 포함한 시스템 결합곡선이 아니다.
- 제조사 trim curve와 valve characteristic 설명의 기준이다.

### 2.3 Installed Flow Characteristic

- 실제 배관계에 설치된 상태에서 valve travel과 실제 flow 사이의 관계다.
- 밸브 inherent characteristic와 system characteristic의 결합 결과다.
- 운전점에 따라 valve differential pressure가 달라질 수 있다.
- system resistance, pump curve, static head 및 pressure source가 영향을 준다.
- 일정 valve differential pressure가 유지되는 제한조건에서는 inherent curve에 가까울 수 있다.
- 모든 실제 배관에서 inherent curve와 동일하다고 단정할 수 없다.

### 2.4 Linear Characteristic

이상적 관계:

`y ≈ y0 + (1-y0)x`

최소용량을 무시한 이상식:

`y ≈ x`

- 동일 travel 증가마다 `Cv`가 같은 절대량만큼 증가한다.
- 일정 valve differential pressure에서는 flow 변화도 이를 더 직접적으로 따른다.
- actual installed flow가 모든 운전점에서 travel에 정비례한다고 보장하지 않는다.
- 비교적 일정한 valve differential pressure와 제한된 부하범위에서 적합할 수 있다.

### 2.5 Equal Percentage Characteristic

미분적 의미:

`dCv / Cv = k dx`

이상적 정규화식의 한 표현:

`y = R^(x-1)`

기울기:

`dy/dx = ln(R) · y`

- 동일 travel 증가마다 현재 `Cv`에 대해 동일한 비율로 증가한다.
- 저개도에서는 절대 증가량이 작다.
- 고개도에서는 절대 증가량이 크다.
- 넓은 부하범위에서 low-flow resolution과 high-flow capacity를 함께 확보하는 데 유리할 수 있다.
- 감소하는 valve differential pressure 또는 변하는 공정 민감도를 부분적으로 보상할 수 있다.
- 모든 시스템에서 installed curve를 자동으로 linear하게 만들지는 않는다.
- `R`은 이 Topic에서 curve shape를 설명하는 파라미터다.
- Rangeability 상세 정의와 설계는 Topic 3이 담당한다.

### 2.6 Quick Opening Characteristic

- 초기 travel에서 큰 `Cv` 증가가 발생한다.
- 이후 travel 증가에 따른 추가 capacity 증가는 작아진다.
- 저개도에서 curve slope가 크고 고개도에서 평탄해진다.
- 빠른 초기 flow 확보가 중요한 On-Off, bypass, batch fill 또는 차단 성격의 서비스에 자주 적용한다.
- 정밀 연속제어의 일반 기본 선택으로 단정하지 않는다.
- 구조적으로 중간개도 운전이 불가능하다고 단정하지 않는다.

### 2.7 Flow와 valve differential pressure

비압축성·비초크 조건의 정성적 관계:

`Q ∝ Cv(x) √(ΔPv(x) / SG)`

- `Q`: flow
- `Cv(x)`: travel에 따른 flow coefficient
- `ΔPv(x)`: 운전점별 valve differential pressure
- `SG`: specific gravity
- 이 식은 installed curve distortion을 설명하기 위한 최소 관계다.
- unit constant, viscosity, Reynolds correction 및 sizing은 Topic 4로 넘긴다.

### 2.8 Pressure-drop redistribution

개념적 pressure balance:

`ΔP_available(Q) = ΔPv(Q) + ΔPsystem(Q)`

난류 system loss 근사:

`ΔPsystem ≈ KQ²`

- flow 증가 시 system loss가 증가한다.
- pump 또는 pressure source가 제공하는 available pressure도 운전점에 따라 변할 수 있다.
- valve에 남는 differential pressure는 감소하거나 다른 형태로 변할 수 있다.
- 실제 flow는 inherent `Cv` curve와 valve differential pressure의 결합 결과다.
- 따라서 installed curve는 inherent curve와 다를 수 있다.

### 2.9 Pump curve와 static head

- centrifugal pump head는 일반적으로 flow 증가에 따라 감소한다.
- static head는 flow와 무관한 pressure requirement로 작용할 수 있다.
- pipe friction loss는 flow와 함께 증가한다.
- 이 조합이 운전점별 available pressure와 valve differential pressure를 정한다.
- friction-dominated system과 static-head-dominated system은 installed distortion 양상이 다를 수 있다.
- characteristic selection은 pump/system curve와 예상 operating points로 확인한다.

### 2.10 Linear installed distortion

- Linear inherent trim도 flow 증가와 함께 valve differential pressure가 감소하면 installed flow가 항상 linear하지 않다.
- 낮은 valve pressure share에서는 저개도 flow response가 상대적으로 커지고 고개도 추가 flow가 압축될 수 있다.
- 정확한 정량 평가는 Valve Authority 및 Installed Gain Topic에서 수행한다.

### 2.11 Equal Percentage partial compensation

- Equal Percentage의 증가하는 inherent slope는 고개도에서 감소하는 valve differential pressure 영향을 부분적으로 보상할 수 있다.
- 넓은 부하범위에서 installed sensitivity를 비교적 균일하게 만들 수 있다.
- 이 효과는 system condition에 의존한다.
- Equal Percentage가 항상 linear installed flow 또는 constant loop gain을 보장하지 않는다.

### 2.12 Conditional application mapping

일반적 경향:

- Linear: valve differential pressure가 비교적 일정한 throttling service
- Equal Percentage: 부하범위가 넓거나 valve differential pressure가 크게 변하는 throttling service
- Quick Opening: 빠른 초기 capacity가 필요한 On-Off 또는 bypass 성격

주의:

- heat exchanger라는 장치명만으로 characteristic를 확정하지 않는다.
- 모든 flow-control loop에 Linear를 자동 적용하지 않는다.
- 모든 throttling loop에 Equal Percentage를 자동 적용하지 않는다.
- manufacturer valve data와 hydraulic system analysis로 확인한다.

### 2.13 Selection and verification

특성 선정 시 다음을 검토한다.

- minimum, normal 및 maximum flow
- valve differential pressure at operating points
- pump 또는 pressure-source characteristic
- static head
- pipe and equipment resistance
- process load range
- required control precision
- low-travel sensitivity
- high-travel capacity
- throttling 또는 On-Off 목적
- manufacturer inherent characteristic
- expected installed curve
- commissioning flow response

### 2.14 Planned Fact Anchor IDs

1. `control_valve_inherent_characteristic_definition`
2. `control_valve_installed_characteristic_definition`
3. `control_valve_inherent_installed_distinction`
4. `control_valve_normalized_travel_relative_capacity`
5. `control_valve_flow_valve_dp_dependency_boundary`
6. `control_valve_linear_characteristic_definition`
7. `control_valve_equal_percentage_characteristic_definition`
8. `control_valve_equal_percentage_exponential_relation`
9. `control_valve_equal_percentage_absolute_increment`
10. `control_valve_quick_opening_characteristic_definition`
11. `control_valve_inherent_constant_pressure_drop_condition`
12. `control_valve_installed_pressure_drop_redistribution`
13. `control_valve_system_resistance_flow_squared_relation`
14. `control_valve_pump_curve_installed_characteristic_effect`
15. `control_valve_static_head_installed_characteristic_effect`
16. `control_valve_linear_installed_distortion`
17. `control_valve_equal_percentage_partial_compensation`
18. `control_valve_characteristic_selection_criteria`
19. `control_valve_application_mapping_is_conditional`
20. `control_valve_installed_local_slope_topic_boundary`
21. `control_valve_manufacturer_curve_system_model_verification`
22. `control_valve_commissioning_characteristic_verification`

## 3. Acceptable answer expressions

- 고유 유량특성은 일정한 valve differential pressure에서 travel과 relative `Cv`의 관계다.
- 설치 유량특성은 실제 배관에서 travel과 actual flow의 관계다.
- Inherent는 valve/trim characteristic이고 Installed는 valve와 system의 combined characteristic다.
- Linear는 동일 stroke 증가마다 `Cv`가 같은 절대량 증가한다.
- Equal Percentage는 동일 stroke 증가마다 현재 `Cv`의 같은 percentage가 증가한다.
- Equal Percentage는 low travel에서 절대 변화가 작고 high travel에서 크다.
- Quick Opening은 초기 stroke에서 큰 capacity를 확보하고 이후 증가가 완만해진다.
- actual flow는 `Cv`뿐 아니라 valve differential pressure에도 의존한다.
- pipe loss가 증가하면 valve에 배분되는 differential pressure가 달라진다.
- Linear inherent trim도 installed flow가 항상 linear하지는 않다.
- Equal Percentage는 changing differential pressure를 부분적으로 보상할 수 있다.
- Equal Percentage가 installed curve를 항상 linear하게 보장하는 것은 아니다.
- valve differential pressure가 거의 일정하면 Installed가 Inherent에 가까워질 수 있다.
- heat exchanger에는 Equal Percentage가 자주 적용되지만 system analysis가 필요하다.
- Quick Opening은 On-Off 또는 bypass 성격에 일반적으로 적합하다.
- 최종 characteristic는 pump curve, static head, system resistance 및 operating range를 함께 보고 선정한다.
- manufacturer data와 predicted installed curve를 검토한다.
- commissioning에서 valve travel과 flow response를 확인한다.

## 4. Fatal wrong claims

### 4.1 `control_valve_inherent_installed_same_concept`

Claim:

Inherent Characteristic와 Installed Characteristic는 동일한 개념이다.

Reason:

전자는 일정 기준조건의 valve/trim characteristic이고 후자는 실제 system combined characteristic다.

False-positive guard:

같지 않다고 반박하거나 일정 valve differential pressure에서만 근사적으로 가까울 수 있다고 설명하면 검출하지 않는다.

### 4.2 `control_valve_inherent_includes_system_resistance`

Claim:

Inherent Characteristic는 pipe resistance와 pump curve를 포함한 field curve다.

Reason:

system 영향을 포함하는 관계는 Installed Characteristic다.

### 4.3 `control_valve_installed_is_constant_dp_bench_curve`

Claim:

Installed Characteristic는 valve 단독으로 differential pressure를 일정하게 유지하여 측정한 curve다.

Reason:

이 설명은 Inherent Characteristic의 기준조건이다.

### 4.4 `control_valve_equal_percentage_equal_absolute_increment`

Claim:

Equal Percentage는 동일 travel마다 flow 또는 `Cv`가 같은 절대량 증가한다.

Reason:

같은 percentage로 증가하며 absolute increment는 high travel에서 더 커진다.

False-positive guard:

같은 절대량이 아니라 같은 비율이라고 대조하면 검출하지 않는다.

### 4.5 `control_valve_equal_percentage_linear_with_travel`

Claim:

Equal Percentage는 travel에 정비례하는 Linear characteristic다.

Reason:

이상적 Equal Percentage는 exponential relation이고 Linear와 구분된다.

### 4.6 `control_valve_equal_percentage_largest_low_travel_increment`

Claim:

Equal Percentage의 동일 travel당 absolute flow 증가가 low travel에서 가장 크다.

Reason:

low travel에서는 absolute increment가 작고 high travel에서 커진다.

### 4.7 `control_valve_linear_always_installed_linear`

Claim:

Linear trim이면 실제 pipe system에서도 travel과 flow가 항상 linear다.

Reason:

operating-point valve differential pressure 변화가 installed curve를 왜곡한다.

False-positive guard:

valve differential pressure가 거의 일정한 제한조건에서 가까워질 수 있다고 설명하면 안전하다.

### 4.8 `control_valve_quick_opening_precision_control_default`

Claim:

Quick Opening은 precision continuous control에 가장 적합한 일반 characteristic다.

Reason:

초기 큰 capacity가 필요한 On-Off 또는 bypass 성격에 일반적으로 적합하다.

False-positive guard:

특수 service에서 제한적으로 modulation할 수 있다고 조건부로 설명하면 자동 fatal로 보지 않는다.

### 4.9 `control_valve_system_pressure_distribution_no_effect`

Claim:

system pressure distribution, pipe resistance와 pump curve는 valve characteristic에 영향을 주지 않는다.

Reason:

이 요소들이 valve differential pressure를 바꾸어 Installed Characteristic를 결정한다.

### 4.10 `control_valve_variable_dp_no_installed_distortion`

Claim:

운전점에 따라 valve differential pressure가 변해도 inherent curve가 actual flow에 그대로 나타난다.

Reason:

flow는 `Cv`와 valve differential pressure의 결합 결과다.

### 4.11 `control_valve_trim_only_determines_installed_curve`

Claim:

Installed Characteristic는 trim shape만으로 결정된다.

Reason:

trim과 system resistance, pump/static head 및 operating condition의 combined result다.

### 4.12 `control_valve_linear_guarantees_constant_process_gain`

Claim:

Linear trim은 모든 operating range에서 constant process gain 또는 loop gain을 보장한다.

Reason:

valve inherent slope와 entire process gain은 다른 개념이며 operating point에 따라 변한다.

Boundary:

정량 gain·authority 분석은 Topic 3이 담당한다.

## 5. Warn-level weak claims

- Inherent와 Installed를 이름만 나열하고 기준조건을 비교하지 않는다.
- Linear, Equal Percentage 및 Quick Opening의 curve shape만 나열한다.
- Equal Percentage의 percentage 의미를 설명하지 않는다.
- Equal Percentage의 low/high travel absolute increment를 누락한다.
- Quick Opening의 service 목적을 설명하지 않는다.
- valve differential pressure 변화와 installed distortion을 연결하지 않는다.
- pump curve와 static head를 누락한다.
- application mapping을 제시하지만 condition과 exception을 설명하지 않는다.
- manufacturer curve와 system model 검증을 누락한다.
- actual commissioning 확인을 누락한다.
- Topic 3 용어를 언급하지만 Topic 2 인과관계를 설명하지 않는다.

Major 또는 conditional error 후보:

- 모든 control service에서 Equal Percentage가 항상 최적이라고 일반화한다.
- Quick Opening은 어떠한 중간개도 운전도 구조적으로 불가능하다고 절대화한다.
- 모든 heat exchanger에는 system condition과 무관하게 Equal Percentage만 사용해야 한다고 설명한다.

## 6. False positive cautions

- “Equal Percentage는 같은 절대량이 아니라 같은 비율로 증가한다”는 정답이다.
- “Linear inherent라도 installed flow가 항상 linear인 것은 아니다”는 정답이다.
- “Quick Opening은 precision control보다 On-Off service에 일반적으로 적합하다”는 정답이다.
- “valve differential pressure가 거의 일정하면 Installed가 Inherent에 가까울 수 있다”는 정답이다.
- “Equal Percentage가 installed curve를 linear에 가깝게 만들 수 있으나 항상 보장하지 않는다”는 정답이다.
- 오답을 인용한 뒤 `틀리다`, `아니다`, `혼동하면 안 된다`고 반박한 문장은 safe다.
- `R`을 curve parameter로 정의하고 후속 equation에서 재사용하는 것은 safe다.
- simplified incompressible relation임을 명시하고 `Q ∝ Cv√ΔP`를 사용하는 것은 safe다.
- 특수 service에서 Quick Opening modulation 가능성을 조건부로 언급하는 것은 fatal이 아니다.
- Valve Authority와 Rangeability를 Topic 3 경계로 언급하는 것은 routing evidence로 과대평가하지 않는다.
- 표나 curve sketch의 위치만으로 fatal을 확정하지 않는다.
- axis label, curve label, body explanation과 equation을 함께 확인한다.

## 7. Regex candidate patterns

deterministic checks는 disabled로 유지한다.

아래 pattern은 semantic evidence candidate 추출 참고용이다.

- `(?i)(inherent|고유).*(installed|설치).*(같|동일)`
- `(?i)(equal percentage|등비|등퍼센트).*(같은|동일).*(절대량|유량)`
- `(?i)(equal percentage|등비|등퍼센트).*(선형|정비례)`
- `(?i)(linear|선형).*(actual|실제|installed|설치).*(항상|모든).*(선형|정비례)`
- `(?i)(quick opening|퀵 오프닝).*(precision|정밀|연속제어).*(최적|가장 적합)`
- `(?i)(pipe resistance|배관 저항|system resistance|pump curve|static head).*(영향.*없|무관)`
- `(?i)(installed|설치).*(trim|트림).*(만으로|오직).*(결정)`
- `(?i)(equal percentage|등비|등퍼센트).*(항상|모든).*(최적|적합)`
- `(?i)(quick opening|퀵 오프닝).*(중간개도).*(불가능|절대)`

Regex hit만으로 fatal을 확정하지 않는다.

negation, quotation, contrastive expression, conditional phrase와 surrounding claim을 확인한다.

## 8. fact_anchor.json generation guidance

### 8.1 Structure

기존 canonical Topic Pack과 같은 key order를 사용한다.

Root:

- `schema_version`
- `topic_id`
- `title_ko`
- `question_type_hint`
- `anchors`
- `fatal_wrong_claims`
- `safe_expressions`
- `revision_notes`
- `topic_label`
- `core_facts`

각 anchor:

- `id`
- `anchor_id`
- `statement`
- `importance`
- `keywords`
- `core_terms`
- `accepted_explanations`
- `rejected_explanations`
- `grading_notes`
- `source_basis`
- `claim`
- `description`

### 8.2 Anchor count and importance

- total anchors: 22
- `must` 후보: 1, 2, 3, 6, 7, 10, 11, 12, 16, 17, 18
- 나머지: `important`
- optional anchor는 두지 않는다.
- `id`와 `anchor_id`는 동일하게 작성한다.
- anchor ID는 repository 전체에서 unique해야 한다.

### 8.3 Formula handling

- Linear equation은 idealized relation임을 명시한다.
- Equal Percentage equation에서 `R`의 의미를 curve parameter 범위로 제한한다.
- `Q ∝ Cv√ΔPv`는 incompressible nonchoked qualitative relation으로 제한한다.
- unit constants와 full sizing equation은 Topic 4로 넘긴다.
- formula variable definition을 함께 둔다.
- defined variable reuse를 오류로 보지 않는다.

### 8.4 Coverage boundary

Fact Anchor는 올바른 content presence를 평가한다.

fatal logic, score cap 및 false-positive rule은 logic_check에서 관리한다.

## 9. logic_check.json generation guidance

### 9.1 Deterministic section

- `enabled`: false
- `topic_name`: Topic 2 title
- `question_type`: `COMPARE_SELECTION`
- `difficulty_profile`: `FIELD_APPLICATION`
- `topic_aliases`: 좁은 valve-characteristic phrase만 사용
- `fatal_checks`: schema-compatible object list
- `major_checks`: conditional overgeneralization 중심
- `question_type_checks`: compare and selection coverage 보조
- `next_practice_points`: definition, curve comparison, system distortion, selection
- `de_claim_trust`: D/E 직접 점수반영 금지 계약 유지

Broad keyword hit만으로 fatal을 발생시키지 않는다.

### 9.2 LLM profile

- `truth_schema`: 22 Fact Anchor와 일관된 truth
- `fatal_conditions`: 12개
- `major_checks`: 3개 conditional error
- `safe_conditions`: contrastive and conditional correct claims
- `candidate_extraction`: empty rules
- `false_positive_cautions`: negation, quote, formula variable reuse, table/curve context
- `output_contract`: current canonical schema 유지
- `cap_policy`: verified fatal correctness error에만 적용
- `score_policy`: C canonical owner

### 9.3 Single-owner policy

- requirement coverage: B
- verified correctness: C
- design and field depth: D
- defensibility and connection: E
- same misconception에 B/C 중복 deduction 금지
- Logic Check의 D/E 직접 scoring 금지

## 10. model_answer.json generation guidance

### 10.1 Metadata

- schema: `topic_pack.model_answer.v1`
- question_type: `COMPARE_SELECTION`
- rich question patterns: 10
- recommended outline sections: 7

### 10.2 Expected question patterns

Pattern 1:
Inherent와 Installed 비교

Required anchors:
- `control_valve_inherent_characteristic_definition`
- `control_valve_installed_characteristic_definition`
- `control_valve_inherent_installed_distinction`
- `control_valve_inherent_constant_pressure_drop_condition`
- `control_valve_installed_pressure_drop_redistribution`

Pattern 2:
Linear, Equal Percentage 및 Quick Opening 비교

Required anchors:
- `control_valve_linear_characteristic_definition`
- `control_valve_equal_percentage_characteristic_definition`
- `control_valve_equal_percentage_absolute_increment`
- `control_valve_quick_opening_characteristic_definition`

Pattern 3:
Installed distortion

Required anchors:
- `control_valve_flow_valve_dp_dependency_boundary`
- `control_valve_installed_pressure_drop_redistribution`
- `control_valve_system_resistance_flow_squared_relation`
- `control_valve_linear_installed_distortion`

Pattern 4:
Equal Percentage selection

Required anchors:
- `control_valve_equal_percentage_exponential_relation`
- `control_valve_equal_percentage_absolute_increment`
- `control_valve_equal_percentage_partial_compensation`
- `control_valve_application_mapping_is_conditional`

Pattern 5:
Quick Opening application

Required anchors:
- `control_valve_quick_opening_characteristic_definition`
- `control_valve_application_mapping_is_conditional`
- `control_valve_characteristic_selection_criteria`

Pattern 6:
pump curve and static head

Required anchors:
- `control_valve_pump_curve_installed_characteristic_effect`
- `control_valve_static_head_installed_characteristic_effect`
- `control_valve_installed_pressure_drop_redistribution`

Pattern 7:
Characteristic selection procedure

Required anchors:
- `control_valve_characteristic_selection_criteria`
- `control_valve_application_mapping_is_conditional`
- `control_valve_manufacturer_curve_system_model_verification`
- `control_valve_commissioning_characteristic_verification`

Pattern 8:
Curve drawing and interpretation

Required anchors:
- `control_valve_normalized_travel_relative_capacity`
- `control_valve_linear_characteristic_definition`
- `control_valve_equal_percentage_characteristic_definition`
- `control_valve_quick_opening_characteristic_definition`

Pattern 9:
Linear installed misconception

Required anchors:
- `control_valve_inherent_constant_pressure_drop_condition`
- `control_valve_installed_pressure_drop_redistribution`
- `control_valve_linear_installed_distortion`

Pattern 10:
Topic 2 and Topic 3 boundary

Required anchors:
- `control_valve_installed_local_slope_topic_boundary`
- `control_valve_characteristic_selection_criteria`
- `control_valve_manufacturer_curve_system_model_verification`

### 10.3 Recommended outline

1. 유량특성의 정의와 axes
2. Inherent와 Installed 비교
3. Linear, Equal Percentage 및 Quick Opening
4. flow, `Cv`와 valve differential pressure
5. pump curve, static head 및 system resistance
6. 조건부 selection criteria
7. manufacturer model과 commissioning verification

### 10.4 Routing aliases

권장:

- 제어밸브 고유 유량특성
- 제어밸브 설치 유량특성
- inherent flow characteristic
- installed flow characteristic
- equal percentage valve characteristic
- linear valve characteristic
- quick opening valve characteristic
- 밸브 특성곡선 비교
- 등비 유량특성
- 등퍼센트 유량특성
- 선형 유량특성
- 퀵 오프닝 특성
- valve travel relative flow characteristic
- installed flow curve distortion

금지:

- control valve
- 제어밸브
- flow
- 유량
- linear
- installed
- gain
- performance
- authority
- rangeability
- Cv
- Kv
- sizing
- balanced trim
- unbalanced trim
- stiction
- deadband

### 10.5 Routing field points

- constant valve differential pressure inherent curve
- actual system installed flow curve
- equal absolute `Cv` increment
- equal percentage `Cv` increment
- pressure-drop redistribution
- pump curve and static head
- system resistance
- conditional process application
- manufacturer curve and commissioning verification

## 11. topic_importance.json generation guidance

- schema: `topic_pack.topic_importance.v1`
- difficulty: `FIELD_APPLICATION`
- selection_importance: `NORMAL`
- question_type: `COMPARE_SELECTION`
- grading mode note: `LLM_ONLY`
- deterministic checks note: disabled

High-band unlock conditions:

1. Inherent와 Installed를 정확히 구분한다.
2. Linear, Equal Percentage 및 Quick Opening을 비교한다.
3. Equal Percentage의 percentage 의미와 absolute increment를 설명한다.
4. `Q`, `Cv` 및 valve differential pressure 관계를 연결한다.
5. pressure-drop redistribution과 system resistance를 설명한다.
6. pump curve와 static head를 고려한다.
7. application mapping을 conditional하게 제시한다.
8. Topic 3과 Topic 4의 정량범위를 침범하지 않는다.
9. manufacturer data와 installed curve를 검증한다.
10. fatal misconception이 없다.

`★★★★★`는 작업 우선순위이며 runtime `selection_importance`를 대체하지 않는다.

## 12. Human review checklist

### 12.1 Correctness

- [ ] Inherent와 Installed가 정확히 구분되었는가?
- [ ] constant valve differential pressure 조건이 Inherent에 연결되었는가?
- [ ] Linear가 equal absolute `Cv` increment로 설명되었는가?
- [ ] Equal Percentage가 equal relative increment로 설명되었는가?
- [ ] Equal Percentage의 low/high travel absolute increment가 올바른가?
- [ ] Quick Opening curve shape가 올바른가?
- [ ] `Q ∝ Cv√ΔPv`의 condition이 명시되었는가?
- [ ] pressure-drop redistribution 인과가 올바른가?
- [ ] pump curve와 static head가 구분되었는가?
- [ ] Linear installed always-linear misconception을 배제했는가?
- [ ] Equal Percentage compensation을 guarantee로 과장하지 않았는가?

### 12.2 Boundary

- [ ] Topic 1 힘·액추에이터 내용을 재작성하지 않았는가?
- [ ] Topic 3 authority·rangeability·gain 정량설계를 이관했는가?
- [ ] Topic 4 Cv·Kv sizing을 이관했는가?
- [ ] Topic 6 cavitation·flashing을 이관했는가?
- [ ] Topic 8 balanced trim 상세를 이관했는가?
- [ ] Topic 11 stiction·deadband 상세를 이관했는가?

### 12.3 Grading and routing

- [ ] Fact Anchor 후보 22개가 unique한가?
- [ ] fatal 12개와 major 3개가 분리되었는가?
- [ ] safe conditions가 contrastive correct claims를 보호하는가?
- [ ] regex는 candidate evidence에만 사용하는가?
- [ ] broad routing aliases가 배제되었는가?
- [ ] Topic 1 direct routing을 침범하지 않는가?
- [ ] authority·rangeability 질문을 Topic 2로 억지 흡수하지 않는가?
- [ ] general linear-system 질문과 충돌하지 않는가?
- [ ] Question Type lens가 question text only 원칙을 지키는가?
- [ ] C canonical owner와 B/C deduplication이 유지되는가?

### 12.4 Authoring flow

- [ ] README와 source JSON은 다음 단계에서만 작성하는가?
- [ ] generated bank를 직접 수정하지 않는가?
- [ ] LLM JSON generation을 실행하지 않는가?
- [ ] local LLM validation을 실행하지 않는가?
- [ ] host validation 후에만 builder를 실행하는가?
- [ ] user review 전 commit하지 않는가?
