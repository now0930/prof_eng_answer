# Thermistor 온도센서의 NTC·PTC 특성, 측정회로 및 선형화

## 1. 문서 목적

이 문서는 산업계측제어기술사 답안 채점 Bot에 Thermistor 온도센서 Topic을 추가하기 위한 요구사항을 정의한다.

Source Pack JSON은 이 문서에서 합의한 사실 기준을 직접 반영한다. 외부 LLM을 사용하여 Source JSON을 생성하지 않는다.

## 2. Topic 메타데이터

- Topic ID: `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization`
- 제목: Thermistor 온도센서의 NTC·PTC 특성, 측정회로 및 선형화
- 문제 유형: `PRINCIPLE_INTERPRETATION`
- 이론 깊이: `FIELD_APPLICATION`
- 준비 우선순위: `NORMAL`
- 채점 방식: `LLM_ONLY`
- deterministic checks: 비활성화
- candidate extraction rules: 빈 객체

## 3. Topic 경계

### 3.1 포함 범위

Thermistor의 반도체 저항-온도 원리, NTC 및 PTC 특성, B-상수와 Steinhart-Hart 식, 측정회로, ADC 변환, 자기발열, 열시정수, 오차, 교정과 고장진단을 포함한다.

### 3.2 제외 범위

RTD와 Pt100의 금속 저항온도계수, 2선식·3선식·4선식 리드선 보상은 RTD 전용 Topic으로 유지한다.

열전대의 Seebeck 효과, 측정접점·기준접점, CJC와 연장도선·보상도선은 열전대 전용 Topic으로 유지한다.

Thermistor, RTD와 열전대의 비교 문제는 질문의 중심축을 분석하여 비교 Topic 또는 복수 후보로 처리한다.

## 4. 핵심 사실 Anchor

### 1. `thermistor_temperature_measurement_chain`

- 기준 주장: Thermistor 온도 측정은 감온 소자의 저항 변화, 여기 및 측정회로, ADC 변환, 저항-온도 환산과 보정으로 구성된다.
- 설명: Thermistor 자체의 저항만 읽는 것이 아니라 전압분배기, 브리지 또는 정전류 회로로 저항을 전기신호로 변환한다. 이후 ADC 코드에서 저항을 계산하고 소자별 곡선식이나 표준표를 사용하여 온도로 환산한다.
- 핵심어: 감온 소자, 저항 측정, 측정회로, ADC, 저항-온도 환산, 보정

### 2. `thermistor_semiconductor_resistance_temperature_principle`

- 기준 주장: Thermistor는 반도체 세라믹 또는 고분자 재료의 전하 운반자와 전도 메커니즘이 온도에 따라 변하는 저항형 온도센서이다.
- 설명: 금속 RTD와 달리 Thermistor는 반도체 재료의 온도 의존성이 크다. 따라서 작은 온도 변화에도 저항이 크게 변하여 감도가 높지만 비선형성과 사용온도 범위의 제약을 함께 고려해야 한다.
- 핵심어: 반도체 세라믹, 저항형 센서, 온도 의존성, 고감도, 비선형

### 3. `thermistor_ntc_negative_temperature_coefficient`

- 기준 주장: NTC Thermistor는 일반적으로 온도가 상승하면 저항이 감소하는 음의 온도계수 특성을 갖는다.
- 설명: 온도 상승으로 열적으로 활성화되는 전하 운반자가 증가하면서 전도도가 커지고 저항이 감소한다. NTC는 온도 측정, 온도 보상과 돌입전류 제한 등에 사용되지만 적용 목적에 따라 소자 구조와 정격이 다르다.
- 핵심어: NTC, 음의 온도계수, 온도 상승, 저항 감소, 전도도 증가

### 4. `thermistor_ntc_beta_equation`

- 기준 주장: NTC의 제한된 온도범위에서는 B-상수 식으로 저항과 절대온도의 관계를 근사할 수 있다.
- 설명: 대표식은 R(T)=R0·exp[B·(1/T−1/T0)]이며 T와 T0는 kelvin 단위이다. B 값과 기준저항 R0는 소자별 사양값이므로 다른 형식의 Thermistor에 임의로 공통 적용하면 안 된다.
- 핵심어: B-상수, Beta equation, R(T), 절대온도, kelvin, R25

### 5. `thermistor_steinhart_hart_linearization`

- 기준 주장: 넓은 온도범위 또는 높은 정확도가 필요하면 Steinhart-Hart 식, 다항식, 표준표나 다점 보정을 사용하여 비선형성을 보상한다.
- 설명: 일반적인 Steinhart-Hart 식은 1/T=A+B·ln(R)+C·[ln(R)]³ 형태이다. 계수는 해당 소자 또는 교정 데이터에서 구해야 하며 B-상수 단일 근사보다 넓은 범위에서 정확도를 높일 수 있다.
- 핵심어: Steinhart-Hart, ln(R), 비선형 보상, 다점 보정, 표준 저항표

### 6. `thermistor_ptc_positive_temperature_coefficient_switching`

- 기준 주장: PTC Thermistor는 온도가 상승하면 저항이 증가하며, 재료에 따라 특정 전이온도 부근에서 저항이 급격히 증가하는 스위칭 특성을 이용한다.
- 설명: 세라믹 PTC는 전이온도 부근의 급격한 저항 증가를 과전류 보호, 모터 보호와 자기조절 히터에 활용한다. PTC의 전 범위를 하나의 선형 온도계수로 취급해서는 안 된다.
- 핵심어: PTC, 양의 온도계수, 전이온도, 스위칭, 과전류 보호, 자기조절 히터

### 7. `thermistor_voltage_divider_bridge_current_measurement`

- 기준 주장: Thermistor 저항은 전압분배기, 브리지 또는 정전류 여기회로를 이용하여 측정 가능한 전압으로 변환한다.
- 설명: 전압분배기의 기준저항은 관심 온도범위의 Thermistor 저항과 ADC 입력범위를 고려해 선정한다. 브리지는 작은 변화를 민감하게 검출할 수 있으며 정전류 방식은 V=IR로 저항을 구하지만 자기발열을 제한해야 한다.
- 핵심어: 전압분배기, 브리지, 정전류, 기준저항, V=IR

### 8. `thermistor_adc_reference_ratiometric_conversion`

- 기준 주장: ADC 기준전압과 센서 여기전압을 함께 사용하는 비율측정 방식은 전원 변동의 영향을 줄일 수 있다.
- 설명: 분압회로의 공급전압을 ADC 기준전압으로 같이 사용하면 ADC 코드가 저항비에 주로 의존하므로 공급전압 변동이 상쇄된다. 다만 기준저항 공차, ADC 양자화, 입력 누설과 기준전압 잡음은 별도 오차로 관리해야 한다.
- 핵심어: ADC, 기준전압, 비율측정, ratiometric, 양자화, 기준저항 공차

### 9. `thermistor_self_heating_dissipation_constant`

- 기준 주장: Thermistor에 인가한 측정전력은 자기발열을 발생시켜 소자온도를 공정온도보다 높이고 측정오차를 만들 수 있다.
- 설명: 소모전력은 P=I²R 또는 P=V²/R로 계산한다. 방산정수 δ가 온도를 1℃ 높이는 데 필요한 전력이라면 정상상태 자기발열은 대략 ΔT=P/δ로 평가한다. 여기전류, 듀티비와 열결합 조건을 제한해야 한다.
- 핵심어: 자기발열, P=I²R, P=V²/R, 방산정수, ΔT=P/δ, 여기전류

### 10. `thermistor_thermal_time_constant_installation`

- 기준 주장: Thermistor의 열시정수와 설치조건은 온도 변화에 대한 동적 응답과 지연오차를 결정한다.
- 설명: 열시정수는 계단 온도 변화 후 최종 변화량의 약 63.2%에 도달하는 시간으로 표현한다. 소자 크기, 봉지재, 보호관, 유체속도, 삽입깊이와 접촉상태가 열전달과 응답속도를 바꾼다.
- 핵심어: 열시정수, 63.2%, 봉지재, 보호관, 열결합, 동적오차

### 11. `thermistor_tolerance_interchangeability_calibration`

- 기준 주장: Thermistor 정확도는 기준저항 공차, B 값 또는 곡선계수 공차, 회로 오차와 교정 불확도의 영향을 함께 받는다.
- 설명: R25 공차만으로 전체 온도범위 정확도를 보장할 수 없다. B 값 또는 Steinhart-Hart 계수의 편차와 기준저항, ADC, 교정표준기의 불확도를 합성해야 한다. 고정밀 적용은 개별 소자 다점 교정 또는 교환성 등급을 사용한다.
- 핵심어: R25 공차, B 값 공차, 교환성, 다점 교정, 불확도

### 12. `thermistor_operating_range_material_selection_stability`

- 기준 주장: Thermistor는 요구 온도범위, 감도, 장기 안정성, 사용분위기와 패키지에 맞춰 선정해야 한다.
- 설명: NTC와 PTC는 재료 및 구조에 따라 저항값, 곡선, 허용온도, 정격전력과 안정성이 다르다. 고온, 습기, 열충격과 장기 사용은 저항 드리프트를 유발할 수 있으므로 데이터시트의 허용범위와 신뢰성 조건을 확인해야 한다.
- 핵심어: 사용온도 범위, 재료, 패키지, 정격전력, 장기 안정성, 드리프트

### 13. `thermistor_wiring_contact_moisture_noise_effects`

- 기준 주장: 배선저항, 접촉저항, 누설, 습기와 전기잡음은 Thermistor 측정회로의 저항 및 전압 계산에 오차를 만든다.
- 설명: 고저항 NTC 회로는 누설전류와 PCB 오염에 민감할 수 있고, 저저항 PTC나 정밀 측정에서는 배선 및 접촉저항도 중요하다. 차폐, 필터링, 절연, 적절한 배선과 방습·세정 설계를 적용한다.
- 핵심어: 배선저항, 접촉저항, 누설전류, 습기, 차폐, 필터링

### 14. `thermistor_fault_diagnostics_open_short_range_fail_safe`

- 기준 주장: Thermistor 입력은 단선, 단락, 범위이탈과 ADC 포화 상태를 구분하고 안전한 고장대응을 수행해야 한다.
- 설명: 분압회로에서 단선과 단락은 서로 다른 ADC 극한값으로 나타날 수 있다. 정상 저항범위와 변화율, 이중센서 비교, pull-up 또는 pull-down 진단을 이용하며 고장 시에는 설비를 안전상태로 전환하거나 대체값 사용을 제한한다.
- 핵심어: 단선, 단락, 범위이탈, ADC 포화, Fail-safe, 진단

## 5. Fatal 오개념

### 1. `thermistor_fatal_ntc_resistance_increases_with_temperature`

- 잘못된 주장: NTC Thermistor는 온도가 상승하면 저항이 증가한다.
- 교정 기준: NTC는 일반적으로 온도가 상승하면 저항이 감소하는 음의 온도계수 소자이다.
- 심각도: fatal
- 영향 계층: B, C, D

### 2. `thermistor_fatal_ptc_perfect_linear_all_range`

- 잘못된 주장: PTC Thermistor의 저항은 전 온도범위에서 항상 일정한 비율로 선형 증가한다.
- 교정 기준: PTC의 저항-온도 특성은 재료와 구조에 따라 비선형이며, 세라믹 PTC는 전이온도 부근에서 급격한 저항 증가를 보일 수 있다.
- 심각도: fatal
- 영향 계층: B, C, D

### 3. `thermistor_fatal_self_generating_voltage_sensor`

- 잘못된 주장: Thermistor는 온도에 비례하는 전압을 스스로 발생하는 자기발전형 센서이다.
- 교정 기준: Thermistor는 외부 여기회로로 저항 변화를 측정하는 수동 저항형 센서이며 열기전력을 자체 발생하지 않는다.
- 심각도: fatal
- 영향 계층: B, C, D

### 4. `thermistor_fatal_self_heating_no_measurement_error`

- 잘못된 주장: Thermistor의 측정전류에 의한 자기발열은 온도 측정값에 영향을 주지 않는다.
- 교정 기준: 측정전력은 소자온도를 상승시켜 오차를 만들 수 있으므로 여기전류, 듀티비, 방산정수와 열결합 조건을 관리해야 한다.
- 심각도: fatal
- 영향 계층: B, C, D

### 5. `thermistor_fatal_beta_equation_linear_all_range`

- 잘못된 주장: B-상수 식은 Thermistor의 전 온도범위에서 완전한 직선 관계를 나타낸다.
- 교정 기준: B-상수 식은 절대온도와 저항의 지수 관계를 제한된 범위에서 근사한다. 넓은 범위에는 Steinhart-Hart 식, 표준표 또는 다점 보정이 필요하다.
- 심각도: fatal
- 영향 계층: B, C, D

### 6. `thermistor_fatal_ntc_ptc_same_sensor_polarity_only`

- 잘못된 주장: NTC와 PTC는 전기적 극성만 반대로 연결하는 동일한 Thermistor이다.
- 교정 기준: NTC와 PTC는 온도계수의 방향, 재료, 저항-온도 곡선과 주요 적용목적이 다르며 단순한 극성 차이가 아니다.
- 심각도: fatal
- 영향 계층: B, C, D

### 7. `thermistor_fatal_circuit_adc_wiring_no_error`

- 잘못된 주장: 기준저항, ADC 기준전압, 배선과 접촉저항은 Thermistor 온도 오차에 영향을 주지 않는다.
- 교정 기준: 기준저항 공차, ADC 오차, 배선·접촉저항, 누설과 전원·기준전압 잡음은 저항 및 온도 환산 오차를 만든다.
- 심각도: fatal
- 영향 계층: B, C, D

### 8. `thermistor_fatal_all_devices_same_curve_beta`

- 잘못된 주장: 모든 Thermistor는 동일한 저항표와 동일한 B-상수를 사용한다.
- 교정 기준: Thermistor의 기준저항, B 값, Steinhart-Hart 계수와 저항-온도 곡선은 형식 및 제조사양에 따라 다르다.
- 심각도: fatal
- 영향 계층: B, C, D

## 6. 답안 구성

1. Thermistor의 정의와 반도체 저항형 온도센서라는 측정원리를 제시한다.
2. NTC의 온도 상승 시 저항 감소와 고감도·비선형 특성을 설명한다.
3. PTC의 온도 상승 시 저항 증가와 전이온도 부근 스위칭 특성을 설명한다.
4. B-상수 식과 Steinhart-Hart 식의 적용범위 차이를 설명한다.
5. 전압분배기·브리지·정전류 회로와 ADC 저항 환산을 설명한다.
6. 자기발열, 방산정수와 열시정수에 따른 정적·동적 오차를 설명한다.
7. 공차·교정·배선·습기·설치와 장기 안정성 문제를 설명한다.
8. 단선·단락 진단, Fail-safe 및 적용별 선정기준을 제시한다.

## 7. 고득점 요소

1. NTC와 PTC를 단순 명칭이 아니라 저항-온도 곡선과 재료 특성으로 구분한다.
2. B-상수 식에서 온도를 kelvin으로 사용하고 근사 적용범위를 명시한다.
3. Steinhart-Hart 식의 계수가 소자 또는 교정 데이터에 종속됨을 설명한다.
4. 기준저항과 ADC 기준전압을 포함한 비율측정 회로의 오차상쇄 원리를 설명한다.
5. P=I²R과 ΔT≈P/δ를 사용해 자기발열 오차를 정량적으로 연결한다.
6. 열시정수 63.2% 정의와 보호관·열접촉의 동적 영향까지 설명한다.
7. R25·B 값 공차, ADC, 기준저항과 교정 불확도를 하나의 오차사슬로 연결한다.
8. 단선·단락·범위이탈 진단과 안전상태 전환을 현장 적용 관점에서 제시한다.

## 8. High-band 요구사항

1. 원리, 회로, 환산식, 오차, 설치와 진단을 하나의 측정사슬로 일관되게 설명한다.
2. NTC·PTC·RTD·열전대의 물리적 원리를 혼동하지 않는다.
3. 비선형성을 단순 단점으로 나열하지 않고 B 식과 Steinhart-Hart 보상으로 연결한다.
4. 정확도와 응답속도의 상충관계를 소자 크기, 열결합과 필터링으로 설명한다.
5. 자기발열을 여기전류·방산정수·측정 듀티비와 연결하여 개선안을 제시한다.
6. 부품 공차와 환경영향을 교정·회로설계·설치관리로 나누어 대응한다.
7. 비교형 문제에서도 Thermistor 고유 원리와 적용 한계를 중심축으로 유지한다.
8. 현장 적용 시 비용, 교환성, 유지보수성과 Fail-safe를 함께 고려한다.

## 9. Data-driven routing

### 9.1 Routing aliases

- 서미스터
- Thermistor
- NTC
- PTC
- NTC Thermistor
- PTC Thermistor
- 음의 온도계수
- 양의 온도계수
- B-상수
- Beta constant
- Steinhart-Hart
- 저항-온도 특성
- 자기발열
- 방산정수
- 열시정수
- 전압분배기
- 비율측정

- 전이온도
- 저항 증가
- 스위칭 특성
- 과전류 보호
- 자기조절 히터

### 9.2 Routing field points

1. R25, B 값 또는 Steinhart-Hart 계수, 저항 공차, 사용온도와 패키지 조건을 확인하여 소자를 선정한다.
2. 전압분배기 기준저항과 ADC 입력범위를 관심 온도구간에 맞추고, 가능하면 센서 여기전압과 ADC 기준전압을 공유하는 비율측정을 적용한다.
3. 여기전류와 측정 듀티비를 제한하고 P=I²R 및 방산정수로 자기발열 오차를 검토한다.
4. 소자 크기, 봉지재, 보호관, 삽입깊이와 열접촉 상태가 열시정수와 동적오차에 미치는 영향을 확인한다.
5. 단선·단락·범위이탈과 ADC 포화를 진단하고, 습기·누설·배선·접촉저항 및 전기잡음에 대한 Fail-safe 설계를 적용한다.

### 9.3 Question examples

1. Thermistor 온도센서의 원리와 NTC 및 PTC 특성을 설명하시오.
2. NTC Thermistor의 저항-온도 특성과 B-상수 식을 설명하시오.
3. Thermistor의 Steinhart-Hart 선형화 방법을 설명하시오.
4. NTC Thermistor 측정용 전압분배기와 ADC 변환을 설명하시오.
5. Thermistor 측정에서 자기발열 오차와 방산정수를 설명하시오.
6. Thermistor의 열시정수와 설치조건에 따른 동적오차를 설명하시오.
7. PTC Thermistor의 전이온도와 스위칭 보호 특성을 설명하시오.
8. Thermistor의 R25 공차, B 값 공차와 교정 방법을 설명하시오.
9. Thermistor 입력의 단선·단락 진단과 Fail-safe 설계를 설명하시오.
10. Thermistor 측정회로의 기준저항, ADC 기준전압 및 배선 오차를 설명하시오.
11. NTC와 PTC Thermistor를 비교하고 적용분야를 설명하시오.
12. Thermistor와 RTD를 비교하되 Thermistor의 비선형성과 자기발열을 중심으로 설명하시오.
13. Thermistor, RTD 및 열전대의 측정원리와 적용 특성을 비교하시오.

## 10. 정합성 요구사항

Source fact anchor의 14개 Anchor와 8개 fatal claim은 Generated fact bank에서 ID와 핵심 문장이 보존되어야 한다.

Source model answer의 routing aliases와 routing field points는 Generated model answer의 topic aliases와 field connection points에 동일하게 반영되어야 한다.

Thermistor 직접 질문은 본 Topic으로 라우팅되어야 한다. RTD 전용, 열전대 전용 질문은 본 Topic 후보를 유지하면 안 된다.

Thermistor 비교 질문에서는 질문의 중심이 Thermistor이면 본 Topic을 primary 또는 유효 후보로 유지해야 한다.

## 11. LLM 의미 검증 기준

정상 답안은 NTC·PTC 방향, B-상수 식, Steinhart-Hart, 측정회로와 자기발열을 사실에 맞게 연결해야 한다.

의도적 오답은 정의된 fatal claim 중 하나 이상을 명시적으로 주장할 때 해당 fatal ID를 검출할 수 있어야 한다.

RTD 또는 열전대만 설명한 답안은 Thermistor 답안으로 정합하다고 평가하면 안 된다.

LLM 의미 검증은 ChatGPT가 수행한다. 로컬 검증 스크립트에서는 LLM 호출을 제외하고 Source/Generated 구조, routing과 회귀 테스트를 검증한다.

## 12. Revision notes

- `created_from_reviewed_thermistor_requirements`
- `separated_from_rtd_pt100_wiring_compensation_topic`
- `separated_from_thermocouple_seebeck_cjc_topic`
- `focused_on_ntc_ptc_measurement_self_heating_and_linearization`
- `deterministic_checks_disabled`
- `candidate_extraction_rules_empty`
- `added_data_driven_routing_aliases_and_field_points`
