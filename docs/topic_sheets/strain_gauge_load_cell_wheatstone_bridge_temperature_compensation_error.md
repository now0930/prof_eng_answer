# 스트레인 게이지와 로드셀의 원리, 휘트스톤 브리지, 온도보상 및 오차

## 1. 문서 목적

이 문서는 산업계측제어기술사 답안 채점 Bot에 스트레인 게이지·로드셀 Topic을 추가하기 위한 요구사항을 정의한다.

Source Pack JSON은 이 문서에서 합의한 사실 기준을 직접 반영한다. 외부 LLM으로 Source JSON을 생성하지 않는다.

## 2. Topic 메타데이터

- Topic ID: `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`
- 제목: 스트레인 게이지와 로드셀의 원리, 휘트스톤 브리지, 온도보상 및 오차
- 문제 유형: `PRINCIPLE_INTERPRETATION`
- 이론 깊이: `FIELD_APPLICATION`
- 준비 우선순위: `NORMAL`
- 채점 방식: `LLM_ONLY`
- deterministic checks: 비활성화
- candidate extraction: 빈 객체

## 3. Topic 경계

수동형 센서 일반 Topic은 저항형·용량형·유도형 변환의 공통원리를 유지한다. 본 Topic은 스트레인 게이지의 게이지율, 브리지 구성과 로드셀의 하중-변형률-mV/V 측정사슬을 중심으로 한다.

Thermistor와 RTD의 저항-온도 특성은 온도센서 Topic으로 유지한다.

압전형 힘센서의 전하 발생원리는 본 Topic에서 제외한다.

## 4. 핵심 사실 Anchor

### 1. `strain_gauge_resistance_change_principle`

- 기준 주장: 금속 스트레인 게이지는 피측정체의 변형을 길이, 단면적 및 비저항 변화에 따른 전기저항 변화로 변환한다.
- 설명: 기본 저항식은 R=ρL/A이다. 축방향 인장 시 길이는 증가하고 단면적은 감소하므로 저항이 증가하며, 압축 시에는 반대 방향으로 변한다. 금속의 압저항 효과에 따른 비저항 변화도 함께 포함된다.
- 핵심어: R=ρL/A, 길이 변화, 단면적 변화, 비저항 변화, 압저항 효과

### 2. `strain_gauge_factor_definition`

- 기준 주장: 게이지율은 기계적 변형률에 대한 상대 저항변화의 비로 GF=(ΔR/R)/ε로 정의한다.
- 설명: 여기서 ε=ΔL/L이며 무차원이다. 따라서 작은 변형률에서 ΔR/R≈GF·ε로 표현할 수 있다. 금속 스트레인 게이지의 게이지율은 기하학적 효과와 압저항 효과를 모두 포함한다.
- 핵심어: 게이지율, Gauge factor, GF=(ΔR/R)/ε, 변형률, 상대 저항변화

### 3. `strain_poisson_transverse_effect`

- 기준 주장: 축방향 변형률은 포아송비에 따른 횡방향 변형률을 발생시키며, 이 효과가 스트레인 게이지의 단면적 변화와 게이지율에 기여한다.
- 설명: 선형 탄성범위에서 횡변형률은 εt=-ν·εl로 나타낸다. 금속 게이지의 상대 저항변화는 근사적으로 ΔR/R=(1+2ν)ε+Δρ/ρ로 설명할 수 있다.
- 핵심어: 포아송비, 횡변형률, εt=-ν·εl, 단면수축, Δρ/ρ

### 4. `wheatstone_bridge_balance_output`

- 기준 주장: 휘트스톤 브리지는 네 저항의 비가 평형조건을 만족할 때 차동 출력이 0이 되고, 게이지 저항 변화에 따라 불평형 전압이 발생한다.
- 설명: 대표적인 평형조건은 R1/R2=R3/R4이다. 브리지 출력은 두 중간점 전압의 차이며, 작은 저항 변화에서는 변형률에 거의 비례하는 차동신호로 사용할 수 있다.
- 핵심어: Wheatstone bridge, R1/R2=R3/R4, 평형, 차동 출력, 불평형 전압

### 5. `quarter_bridge_sensitivity_temperature`

- 기준 주장: Quarter bridge는 한 개의 활성 게이지를 사용하며, 작은 변형률에서 출력 크기는 대략 Vo/Vex≈GF·ε/4이다.
- 설명: 부호는 게이지가 연결된 브리지 팔과 인장·압축 방향에 따라 달라진다. 구성이 단순하지만 게이지 및 리드선의 온도 변화와 배선저항 영향을 상대적으로 크게 받으므로 보상회로가 필요하다.
- 핵심어: Quarter bridge, 한 개 활성 게이지, Vo/Vex≈GF·ε/4, 리드선 영향, 온도오차

### 6. `half_bridge_sensitivity_compensation`

- 기준 주장: Half bridge는 두 개의 게이지를 사용한다. 두 활성 게이지를 출력이 합산되도록 배치하면 Quarter bridge보다 감도가 높아지고, 활성·더미 구성은 주로 온도보상을 제공한다.
- 설명: 동일 크기의 인장·압축 변형을 받는 두 활성 게이지를 출력이 합산되도록 배치하면 작은 변형률에서 Vo/Vex≈GF·ε/2가 된다. 활성 게이지 한 개와 무변형 더미 게이지를 사용하면 공통 온도변화는 상쇄하지만 기계적 감도는 1차 근사에서 Vo/Vex≈GF·ε/4이다.
- 핵심어: Half bridge, 두 활성 게이지, Vo/Vex≈GF·ε/2, 활성·더미 게이지, Vo/Vex≈GF·ε/4, 온도보상

### 7. `full_bridge_sensitivity_compensation`

- 기준 주장: Full bridge는 네 개의 활성 게이지를 사용하며, 인장과 압축 게이지를 출력이 합산되도록 배치하면 가장 높은 감도와 우수한 공통 온도보상을 얻을 수 있다.
- 설명: 이상적인 대칭 배치와 작은 변형률에서는 출력 크기가 대략 Vo/Vex≈GF·ε가 된다. 실제 감도는 탄성체 형상, 게이지 위치, 배선 방향과 횡감도에 따라 달라진다.
- 핵심어: Full bridge, 네 개 활성 게이지, Vo/Vex≈GF·ε, 최대 감도, 공통 온도보상

### 8. `load_cell_force_strain_voltage_chain`

- 기준 주장: 스트레인 게이지식 로드셀은 하중을 탄성체의 변형으로 바꾸고, 게이지 저항변화와 브리지 불평형 전압을 거쳐 전기신호로 변환한다.
- 설명: 측정사슬은 힘·하중→탄성체 응력→변형률→ΔR/R→브리지 출력의 순서이다. 탄성체는 정격하중에서 선형 탄성범위에 있도록 설계되며, 게이지 위치는 인장과 압축 변형이 크게 나타나는 곳에 선정한다.
- 핵심어: 로드셀, 탄성체, 하중, 변형률, 브리지 출력

### 9. `load_cell_excitation_ratiometric_output`

- 기준 주장: 로드셀의 브리지 출력은 여자전압에 비례하며 일반적으로 정격하중에서의 감도를 mV/V 단위로 표시한다.
- 설명: 예를 들어 정격감도 2 mV/V의 로드셀에 10 V를 인가하면 정격하중 출력은 이상적으로 약 20 mV이다. 여자전압을 ADC 기준과 공유하는 비율측정은 여자전압 변동의 영향을 줄일 수 있다.
- 핵심어: 여자전압, mV/V, 정격감도, 비율측정, ratiometric

### 10. `instrumentation_amplifier_adc_signal_chain`

- 기준 주장: 로드셀의 작은 차동 브리지 출력은 계측증폭기에서 증폭한 뒤 필터링하고 ADC로 변환한다.
- 설명: 계측증폭기는 높은 입력임피던스와 공통모드 제거비, 낮은 오프셋과 드리프트가 필요하다. 증폭이득은 정격 mV/V 출력과 ADC 입력범위를 고려하여 정하며, 영점 조정과 저역통과 필터를 함께 적용한다.
- 핵심어: 계측증폭기, 차동신호, CMRR, 오프셋, ADC, 필터링

### 11. `temperature_zero_span_compensation`

- 기준 주장: 온도 변화는 게이지 저항, 접착층, 탄성체 열팽창과 탄성계수를 변화시켜 로드셀의 영점과 감도에 오차를 만든다.
- 설명: 더미 게이지는 동일한 온도와 재료변화를 받되 기계적 변형은 받지 않도록 배치하여 온도에 의한 저항변화를 상쇄한다. 자기온도보상 게이지, 대칭 브리지, 보상저항 및 소프트웨어 보정으로 영점과 span을 보상한다.
- 핵심어: 영점 온도영향, 감도 온도영향, 더미 게이지, 자기온도보상, span 보상

### 12. `creep_hysteresis_nonlinearity_repeatability`

- 기준 주장: 크리프, 히스테리시스, 비직선성과 반복성은 서로 다른 로드셀 성능오차이며 각각의 시험조건과 정의로 평가해야 한다.
- 설명: 크리프는 일정 하중과 환경에서 시간이 지나며 출력이 변하는 현상이다. 히스테리시스는 같은 하중에서 증가·감소 경로의 출력이 다른 현상이다. 비직선성은 교정직선과의 편차이며 반복성은 동일 조건 반복측정의 산포이다.
- 핵심어: 크리프, 히스테리시스, 비직선성, 반복성, 교정오차

### 13. `installation_eccentric_load_overload`

- 기준 주장: 로드셀은 정해진 하중축과 지지조건으로 설치해야 하며, 편심하중, 측하중, 모멘트와 과부하는 출력오차와 영구변형을 유발할 수 있다.
- 설명: 하중 도입부의 정렬, 수평, 체결토크, 부착면 강성 및 기계적 스토퍼를 관리해야 한다. 스트레인 게이지 직접 부착 시에는 표면처리, 접착층 두께, 방향 정렬과 방습 밀봉이 변형 전달과 장기 안정성에 영향을 준다.
- 핵심어: 편심하중, 측하중, 과부하, 접착, 정렬, 기계적 스토퍼

### 14. `wiring_shield_ground_fault_diagnostics`

- 기준 주장: 스트레인 게이지와 로드셀 배선은 리드선저항, 전자기잡음과 접지루프를 관리하고 단선·단락·브리지 불평형 고장을 진단해야 한다.
- 설명: Quarter bridge는 3선식 보상으로 리드선저항 영향을 줄일 수 있고, 정밀 로드셀은 excitation sense를 포함한 6선식을 사용할 수 있다. 트위스트 페어, 차폐, 단일점 접지와 입력 범위진단을 적용한다.
- 핵심어: 3선식 보상, 6선식 로드셀, sense 선, 차폐, 단일점 접지, 단선·단락 진단

## 5. Fatal 오개념

### 1. `strain_gauge_fatal_self_generating_voltage`

- 잘못된 주장: 스트레인 게이지는 외부 여기 없이 변형에 비례하는 전압을 스스로 발생한다.
- 교정 기준: 스트레인 게이지는 변형에 따라 저항이 변하는 수동 저항형 센서이므로 외부 여자 및 브리지 측정회로가 필요하다.
- 심각도: fatal
- 영향 계층: B, C, D

### 2. `strain_gauge_fatal_gauge_factor_inverse_definition`

- 잘못된 주장: 게이지율은 변형률을 상대 저항변화로 나눈 GF=ε/(ΔR/R)이다.
- 교정 기준: 게이지율은 상대 저항변화를 변형률로 나눈 GF=(ΔR/R)/ε로 정의한다.
- 심각도: fatal
- 영향 계층: B, C, D

### 3. `wheatstone_bridge_fatal_balance_maximum_output`

- 잘못된 주장: 휘트스톤 브리지는 평형상태에서 최대 차동출력을 발생한다.
- 교정 기준: 이상적인 휘트스톤 브리지는 평형조건에서 차동출력이 0이며, 저항 변화에 따른 불평형으로 출력이 발생한다.
- 심각도: fatal
- 영향 계층: B, C, D

### 4. `bridge_fatal_quarter_half_full_identical`

- 잘못된 주장: Quarter, Half, Full bridge는 게이지 수만 다를 뿐 감도와 온도보상 능력이 모두 동일하다.
- 교정 기준: 활성 게이지 수와 배치에 따라 감도는 대략 GFε/4, GFε/2, GFε로 달라지며 온도보상과 굽힘·축력 분리 능력도 서로 다르다.
- 심각도: fatal
- 영향 계층: B, C, D

### 5. `load_cell_fatal_output_independent_of_excitation`

- 잘못된 주장: 로드셀 출력은 여자전압과 관계없는 고정 절대전압이다.
- 교정 기준: 저항 브리지형 로드셀 출력은 여자전압에 비례하며 감도는 보통 mV/V로 표시한다.
- 심각도: fatal
- 영향 계층: B, C, D

### 6. `dummy_gauge_fatal_active_load_measurement`

- 잘못된 주장: 더미 게이지는 하중변형을 직접 측정하는 활성 게이지이다.
- 교정 기준: 더미 게이지는 활성 게이지와 같은 온도조건을 받되 측정변형은 받지 않도록 배치하여 온도에 의한 저항변화를 상쇄한다.
- 심각도: fatal
- 영향 계층: B, C, D

### 7. `load_cell_fatal_creep_equals_hysteresis`

- 잘못된 주장: 크리프와 히스테리시스는 같은 원인과 같은 시험으로 정의되는 동일한 오차이다.
- 교정 기준: 크리프는 일정 하중에서 시간에 따른 출력변화이고, 히스테리시스는 동일 하중에서 증가·감소 경로에 따른 출력차이이다.
- 심각도: fatal
- 영향 계층: B, C, D

### 8. `load_cell_fatal_installation_no_error`

- 잘못된 주장: 편심하중, 과부하, 접착상태와 설치방향은 로드셀 및 스트레인 게이지 출력오차에 영향을 주지 않는다.
- 교정 기준: 하중축 정렬, 편심·측하중, 과부하, 표면처리, 접착과 게이지 방향은 변형 전달, 영점, 감도, 선형성과 장기 안정성에 직접 영향을 준다.
- 심각도: fatal
- 영향 계층: B, C, D

## 6. 권장 답안 구성

1. 스트레인 게이지를 변형에 따른 저항변화를 이용하는 수동 저항형 센서로 정의한다.
2. R=ρL/A, 변형률과 게이지율 GF=(ΔR/R)/ε를 설명한다.
3. 휘트스톤 브리지의 평형조건과 차동 불평형 출력을 설명한다.
4. Quarter·Half·Full bridge의 감도와 온도보상 차이를 비교한다.
5. 로드셀의 하중→탄성체→변형률→저항변화→mV/V 출력 사슬을 설명한다.
6. 여자전압, 계측증폭기, 필터와 ADC의 신호처리 구조를 설명한다.
7. 온도영향, 크리프, 히스테리시스, 비직선성과 반복성 오차를 설명한다.
8. 편심하중·과부하·접착·배선·차폐·접지와 고장진단 대책을 제시한다.

## 7. 고득점 요소

1. 게이지율 정의를 정확히 제시하고 기하학적 효과와 압저항 효과를 연결한다.
2. 포아송비와 횡변형률이 단면적 변화 및 게이지율에 미치는 영향을 설명한다.
3. 브리지 평형조건과 작은 변형률에서 Quarter, 두 활성 Half, 활성·더미 Half와 Full bridge의 출력 근사조건을 구분한다.
4. 로드셀 감도를 mV/V와 여자전압의 곱으로 실제 출력전압에 연결한다.
5. 더미 게이지와 자기온도보상, 대칭 브리지의 역할을 구분한다.
6. 크리프·히스테리시스·비직선성·반복성을 서로 다른 시험개념으로 구분한다.
7. 계측증폭기의 CMRR·오프셋·드리프트와 ADC 입력범위를 정량 설계에 연결한다.
8. 편심·측하중, 과부하, 접착과 방습을 설치 및 수명관리 대책으로 연결한다.

## 8. High-band 요구사항

1. 기계적 하중에서 디지털 값까지의 측정사슬을 단절 없이 설명한다.
2. 게이지율과 브리지 감도식을 정의 및 가정조건과 함께 정확히 제시한다.
3. Quarter, 두 활성 Half, 활성·더미 Half와 Full bridge를 감도조건과 보상성능으로 비교한다.
4. 여자전압 변동과 mV/V 출력을 비율측정 및 ADC 기준전압으로 연결한다.
5. 영점 온도영향과 span 온도영향을 구분하고 하드웨어·소프트웨어 보상을 제시한다.
6. 정적오차, 시간의존 오차 및 설치오차를 구분하여 개선방법을 제시한다.
7. 기존 수동형 센서 일반 Topic과 중복하지 않고 로드셀 고유 측정사슬을 중심으로 답한다.
8. 정확도뿐 아니라 비용, 교정성, 과부하 보호, 유지보수와 Fail-safe를 함께 고려한다.

## 9. Data-driven routing

### 9.1 Routing aliases

- 스트레인 게이지
- 변형률 게이지
- strain gauge
- strain gage
- 로드셀
- load cell
- 휘트스톤 브리지
- Wheatstone bridge
- 게이지율
- gauge factor
- Quarter bridge
- Half bridge
- Full bridge
- 더미 게이지
- dummy gauge
- mV/V
- 브리지 출력
- 계측증폭기
- instrumentation amplifier
- 크리프
- 히스테리시스
- 편심하중

### 9.2 Routing field points

1. 피측정 하중범위, 정격용량, 안전과부하, 탄성체 형상과 게이지 배치를 기준으로 로드셀 구조를 선정한다.
2. Quarter·Half·Full bridge의 감도, 온도보상, 배선복잡도와 원가를 비교하여 브리지 구성을 결정한다.
3. 정격 mV/V 출력과 여자전압을 기준으로 계측증폭기 이득, ADC 입력범위, 필터와 비율측정 구조를 설계한다.
4. 영점·span 온도영향, 크리프, 히스테리시스, 비직선성과 반복성을 교정·보상 및 유지보수 계획에 반영한다.
5. 하중축 정렬, 편심·측하중, 과부하 방지, 접착·방습, 차폐·접지와 단선·단락 진단을 현장 설치기준에 포함한다.

### 9.3 Question examples

1. 스트레인 게이지의 저항변화 원리와 게이지율을 설명하시오.
2. 스트레인 게이지의 게이지율과 포아송비의 관계를 설명하시오.
3. 휘트스톤 브리지의 평형조건과 스트레인 게이지 출력원리를 설명하시오.
4. Quarter, Half, Full bridge의 구성, 감도와 온도보상을 비교하시오.
5. 스트레인 게이지식 로드셀의 하중-변형률-전압 변환과정을 설명하시오.
6. 로드셀의 mV/V 정격감도와 여자전압의 관계를 설명하시오.
7. 로드셀 신호용 계측증폭기와 ADC 설계 시 고려사항을 설명하시오.
8. 스트레인 게이지의 더미 게이지 및 자기온도보상 방법을 설명하시오.
9. 로드셀의 영점 및 감도 온도영향과 보상방법을 설명하시오.
10. 로드셀의 크리프, 히스테리시스, 비직선성과 반복성을 설명하시오.
11. 로드셀의 편심하중, 측하중과 과부하에 대한 설치대책을 설명하시오.
12. 스트레인 게이지의 리드선 보상, 차폐, 접지와 고장진단을 설명하시오.
13. 스트레인 게이지식 로드셀과 압전식 힘센서의 측정특성을 비교하시오.

## 10. Source/Generated 계약

Source의 14개 Anchor와 8개 fatal claim은 Generated bank에서 ID와 claim·correction 계약이 보존되어야 한다.

Source routing aliases, field points와 question examples는 Generated model answer에 동일하게 반영되어야 한다.

스트레인 게이지 또는 로드셀 직접 질문은 본 Topic으로 라우팅되어야 한다. Thermistor·RTD·열전대 전용 질문은 본 Topic 후보를 유지하면 안 된다.

## 11. 의미 검증 원칙

정상 답안은 GF=(ΔR/R)/ε, 브리지 평형출력 0, Quarter·Half·Full 감도 차이, mV/V와 여자전압 관계를 정확히 설명해야 한다.

크리프와 히스테리시스, 영점 및 span 온도영향, 편심·측하중과 과부하를 서로 구분해야 한다.

LLM 의미 검증은 ChatGPT가 직접 수행한다. 로컬 검증 스크립트에서는 독립 LLM 및 Ollama 호출을 모두 제외한다.

## 12. Revision notes

- `created_from_reviewed_strain_gauge_load_cell_requirements`
- `separated_from_general_passive_sensor_transduction_topic`
- `separated_from_temperature_resistive_sensor_topics`
- `focused_on_gauge_factor_bridge_load_cell_signal_chain_and_error`
- `deterministic_checks_disabled`
- `candidate_extraction_rules_empty`
- `added_data_driven_routing_aliases_and_field_points`
- `manual_semantic_review_by_chatgpt`
- `all_local_llm_calls_skipped`

- `removed_temperature_sensor_template_contamination`

- `corrected_question_pattern_anchor_mapping`

- `clarified_active_dummy_half_bridge_sensitivity`
