# RTD 온도센서·Pt100·측정전류·배선보상 원리

## 1. Topic 기본정보

- Topic ID: `rtd_temperature_sensor_principle_pt100_wiring_compensation`
- 이전 Topic ID: `rtd_pt100_wire_connection_compensation`
- 문제 유형: `PRINCIPLE_INTERPRETATION`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: `LLM_ONLY`
- 결정론적 검사: 비활성화
- 작성 기준일: 2026-07-12

## 2. Refactor 목적

기존 Topic은 Pt100의 2선식·3선식·4선식 배선보상 비교에 초점이
맞춰져 있었다.

새 Topic은 RTD를 하나의 온도센서로 설명한다.

다음 항목을 하나의 인과관계로 통합한다.

- 금속 저항의 온도 의존성
- Pt100의 기준저항과 표준 특성
- Callendar–Van Dusen 관계
- 측정전류와 전압 검출
- 자기발열
- 2선식·3선식·4선식 배선보상
- transmitter와 배선 구성
- 설치·응답·교정·진단

배선보상은 독립된 주제가 아니라 RTD 측정 정확도를 확보하기 위한
하위 설계요소로 편입한다.

## 3. 세 온도센서 Topic의 경계

온도센서는 다음 세 Topic으로 분리한다.

### RTD

본 Topic에서 다룬다.

- 금속 저항 온도계수
- Pt100
- Callendar–Van Dusen 식
- 여기전류
- 자기발열
- 2선식·3선식·4선식
- 리드선 저항 보상
- 설치·교정·진단

### Thermocouple

별도 Topic으로 작성한다.

- Seebeck effect
- 측정접점과 기준접점
- 냉접점 보상
- 열전대 종류
- 보상도선과 연장도선
- 극성 및 이종금속 접속오차

### Thermistor

별도 Topic으로 작성한다.

- NTC와 PTC
- Beta 식
- Steinhart–Hart 식
- 비선형화와 선형화
- 자기발열
- 제한된 측정범위와 높은 감도

본 Topic에서 Thermocouple과 Thermistor는 RTD의 경계를 설명하기
위한 간단한 비교 외에는 상세 평가하지 않는다.

## 4. RTD의 통합 측정 사슬

RTD 계측의 전체 변환 사슬은 다음과 같다.

    공정온도
    -> 감온부 온도
    -> 금속 저항 변화
    -> 측정전류에 의한 전압 변화
    -> 배선보상·증폭·선형화
    -> 표시·제어용 온도값

이를 식으로 표현하면 다음과 같다.

    T_process
    -> T_sensor
    -> R(T)
    -> V = I_exc R(T)
    -> T_indicated

RTD는 열전대처럼 자체 열기전력을 발생하지 않는다.

저항을 읽기 위한 외부 여기전류가 필요하다.

## 5. Fact Anchor 요구사항

### A01 — `rtd_temperature_measurement_chain`

RTD는 공정온도가 감온부로 전달되고, 금속소자의 저항 변화가
측정전류와 신호조절회로를 통해 전압 및 온도값으로 변환되는
수동형 저항 온도센서다.

필수 내용:

- 공정온도와 감온부 온도를 구분한다.
- 온도에서 저항, 전압, 표시온도로 이어지는 변환 사슬을 설명한다.
- RTD가 자체 열기전력을 발생하지 않음을 설명한다.
- 외부 여기전류와 신호조절이 필요함을 설명한다.
- 센서소자와 transmitter 또는 계측채널을 구분한다.

### A02 — `rtd_metal_resistance_temperature_principle`

RTD는 금속의 전기저항이 온도에 따라 변하는 성질을 이용한다.

금속 도체의 기본 저항은 다음과 같다.

    R = rho l / A

- `rho`: 비저항
- `l`: 도체 길이
- `A`: 전류 통과 단면적

RTD에서는 온도에 따른 비저항 변화가 주된 측정원리다.

필수 내용:

- 금속의 저항 온도계수를 설명한다.
- 형상 변화보다 비저항의 온도의존성이 주된 설계요소임을 설명한다.
- 백금이 안정성·재현성·내식성 때문에 널리 사용됨을 설명한다.
- 저항형 변형센서와 RTD의 측정목적을 구분한다.

### A03 — `rtd_pt100_reference_resistance_alpha_standard`

Pt100은 기준온도 0℃에서 공칭저항이 100 Ω인 백금 RTD다.

대표 산업용 Pt100은 다음 온도계수로 정의된다.

    alpha
    =
    (R_100 - R_0) / (100 R_0)

대표적인 표준 특성은 다음과 같다.

    alpha approximately 0.00385 per degree Celsius

필수 내용:

- `Pt`는 백금 재료를 의미한다.
- `100`은 0℃의 공칭저항을 의미한다.
- 모든 RTD가 Pt100인 것은 아님을 설명한다.
- Pt500, Pt1000과 다른 alpha 특성이 존재할 수 있음을 설명한다.
- 실제 허용오차는 등급과 표준에 따라 달라짐을 설명한다.

### A04 — `rtd_callendar_van_dusen_characteristic`

Pt100의 저항-온도 관계는 전 온도범위에서 완전한 직선이 아니다.

0℃ 이상에서는 다음 형태를 사용할 수 있다.

    R_t
    =
    R_0
    [
      1
      + A t
      + B t^2
    ]

0℃ 미만에서는 추가항을 포함한다.

    R_t
    =
    R_0
    [
      1
      + A t
      + B t^2
      + C (t - 100) t^3
    ]

필수 내용:

- Callendar–Van Dusen 관계를 설명한다.
- 단순 선형식은 제한된 범위의 근사임을 설명한다.
- 온도에서 저항 또는 저항에서 온도를 구할 때 선형화가 필요할 수
  있음을 설명한다.
- 계수와 적용범위는 센서 표준 및 제작특성에 따라 관리함을 설명한다.

### A05 — `rtd_excitation_voltage_measurement`

RTD는 외부 측정전류를 흘리고 저항 양단의 전압을 측정하여 저항을
구한다.

    V_RTD = I_exc R_RTD

    R_RTD = V_RTD / I_exc

필수 내용:

- 정전류 여기 또는 bridge 측정을 설명한다.
- 여기전류의 정확도와 안정도가 측정오차에 영향을 줌을 설명한다.
- ratiometric 측정으로 여기변동 영향을 줄일 수 있음을 설명한다.
- instrumentation amplifier와 A/D 변환의 역할을 설명한다.
- 신호 크기와 노이즈·분해능의 관계를 설명한다.

### A06 — `rtd_self_heating_thermal_error`

측정전류는 RTD에서 전력을 발생시킨다.

    P = I_exc^2 R_RTD

발생한 열이 주변으로 충분히 방출되지 않으면 감온부 온도가 실제
공정온도보다 높아지는 자기발열 오차가 발생한다.

    Delta T_self
    approximately
    P / D

- `D`: 방산상수 또는 dissipation constant

필수 내용:

- 여기전류 증가 시 신호는 커지지만 자기발열도 증가함을 설명한다.
- 유체 유속, 설치구조와 주변 열전달이 방산상수에 영향을 줌을
  설명한다.
- 저전류·펄스여기·보정 등 완화방법을 설명한다.
- 자기발열과 공정의 실제 온도상승을 구분한다.

### A07 — `rtd_two_wire_lead_resistance_error`

2선식 RTD에서는 두 리드선 저항이 감온저항에 직렬로 더해진다.

    R_measured
    =
    R_RTD
    + R_L1
    + R_L2

필수 내용:

- 리드선 저항이 양의 온도오차를 만들 수 있음을 설명한다.
- 배선길이, 굵기와 주변온도가 리드선 저항에 영향을 줌을 설명한다.
- 짧은 배선 또는 낮은 정확도 요구에서 사용할 수 있음을 설명한다.
- transmitter를 감온부 근처에 설치하면 리드선 영향을 줄일 수 있음을
  설명한다.
- 2선식이 리드선 저항을 자동 제거하지 않음을 설명한다.

### A08 — `rtd_three_wire_bridge_compensation_assumptions`

3선식 RTD는 bridge 또는 차동측정에서 두 리드선 저항이 서로 같다는
가정을 이용하여 리드선 저항의 1차 영향을 상쇄한다.

대표 가정은 다음과 같다.

    R_L1 approximately R_L2

필수 내용:

- 3선식 보상은 동일 리드저항 가정에 의존함을 설명한다.
- 도체 재질, 길이, 굵기와 온도조건을 맞춰야 함을 설명한다.
- 리드선 불평형은 잔류오차를 만든다는 점을 설명한다.
- 3선식이 모든 조건에서 완전 보상하는 것은 아님을 설명한다.
- 산업용 transmitter에서 널리 쓰이는 이유를 설명한다.

### A09 — `rtd_four_wire_kelvin_measurement`

4선식 RTD는 두 선으로 측정전류를 공급하고 다른 두 선으로 감온부
전압을 측정하는 Kelvin 방식이다.

고입력 임피던스 전압측정에서는 sense lead 전류가 매우 작으므로
리드선 전압강하의 영향을 크게 줄일 수 있다.

필수 내용:

- force lead와 sense lead의 역할을 구분한다.
- 전압측정 입력 임피던스가 충분히 높아야 함을 설명한다.
- 정밀 교정과 기준온도 측정에 적합함을 설명한다.
- 배선비용과 단자 수가 증가함을 설명한다.
- 4선식도 접촉열기전력·누설·노이즈 등 모든 오차를 제거하는 것은
  아님을 설명한다.

### A10 — `rtd_wiring_method_selection_tradeoff`

2선식·3선식·4선식은 정확도, 배선거리, 비용, 설치공간과 유지보수
조건에 따라 선정한다.

필수 비교:

| 항목 | 2선식 | 3선식 | 4선식 |
|---|---|---|---|
| 배선 수 | 적음 | 중간 | 많음 |
| 리드선 보상 | 없음 | 동일저항 가정의 1차 보상 | Kelvin 측정 |
| 정확도 | 낮음 | 산업용으로 양호 | 가장 우수 |
| 비용 | 낮음 | 중간 | 높음 |
| 대표 적용 | 짧은 배선 | 일반 공정 | 정밀·교정 |

필수 내용:

- 정확도만으로 배선방식을 선정하지 않는다.
- transmitter 위치와 배선거리를 함께 고려한다.
- 현장 유지보수성과 단자오류 가능성을 고려한다.
- 요구 불확도에 맞춰 경제적으로 선정한다.

### A11 — `rtd_transmitter_connection_signal_conditioning`

RTD transmitter는 여기전류 공급, 배선방식 판별, 선형화, 절연,
진단과 4–20 mA 또는 디지털 신호 변환을 수행할 수 있다.

필수 내용:

- head-mounted transmitter와 remote transmitter를 구분한다.
- 2/3/4선식 입력 설정이 실제 배선과 일치해야 함을 설명한다.
- 4–20 mA 변환 후에는 장거리 전송에서 RTD 리드선 저항이 아닌
  current-loop 특성이 적용됨을 설명한다.
- 절연·접지·차폐와 공통모드 노이즈를 고려한다.
- sensor matching 또는 transmitter trimming을 설명한다.

### A12 — `rtd_installation_thermowell_dynamic_response`

RTD의 표시온도는 감온소자뿐 아니라 보호관, thermowell, 삽입길이,
배관 유속과 열전도 조건의 영향을 받는다.

필수 내용:

- 공정온도와 감온부 온도 사이의 열전달 지연을 설명한다.
- 보호관 질량과 두께가 응답시간을 증가시킬 수 있음을 설명한다.
- 삽입길이 부족과 stem conduction이 설치오차를 만들 수 있음을
  설명한다.
- 유속, 접촉상태와 열전달계수의 영향을 설명한다.
- 진동·압력·부식 조건에 따른 보호구조를 고려한다.

### A13 — `rtd_calibration_tolerance_uncertainty`

RTD는 기준온도계 및 안정된 온도원을 사용하여 다점교정할 수 있다.

필수 내용:

- 기준저항과 저항-온도 곡선을 검증한다.
- 센서 허용오차와 계측기 오차를 구분한다.
- 리드선, 여기전류, 자기발열과 설치오차를 불확도에 포함한다.
- ice point, dry block, liquid bath 등의 교정방법을 설명한다.
- 표준 등급, 추적성, 교정성적서와 재교정 주기를 고려한다.

### A14 — `rtd_fault_diagnostics_environment_validation`

RTD 계측채널은 단선, 단락, 접촉저항, 절연저하, 수분침투, 배선방식
오설정과 drift를 진단하고 검증해야 한다.

필수 내용:

- 단선 시 고저항 또는 over-range 진단을 설명한다.
- 단락 시 저저항 또는 under-range 진단을 설명한다.
- 3선식 리드 불평형과 단자 접촉불량을 점검한다.
- 절연저항 저하와 접지루프의 영향을 설명한다.
- 정적 정확도와 동적 응답을 모두 검증한다.
- 설치 후 loop check와 현장 비교검증을 수행한다.

## 6. Fatal Wrong Claim 요구사항

### F01 — `rtd_fatal_self_generated_voltage`

잘못된 주장:

RTD는 온도에 비례하는 전압을 자체적으로 발생하므로 외부
측정전류가 필요하지 않다.

정확한 기준:

RTD는 온도에 따라 저항이 변하는 수동형 센서이며, 저항을 읽기 위한
외부 여기전류 또는 bridge 측정이 필요하다.

### F02 — `rtd_fatal_pt100_means_hundred_at_any_temperature`

잘못된 주장:

Pt100의 100은 모든 온도에서 저항이 항상 100 Ω이라는 의미다.

정확한 기준:

Pt100은 0℃에서 공칭저항이 100 Ω인 백금 RTD이며 저항은 온도에 따라
변한다.

### F03 — `rtd_fatal_perfect_linear_all_temperature`

잘못된 주장:

Pt100은 전 온도범위에서 완전히 선형이므로 하나의 1차식만 사용하면
항상 정확하다.

정확한 기준:

Pt100은 비선형성을 가지며 정밀 변환에는 적용범위에 맞는
Callendar–Van Dusen 관계 또는 표준표를 사용한다.

### F04 — `rtd_fatal_excitation_current_no_self_heating`

잘못된 주장:

RTD 측정전류는 신호 크기만 증가시키며 센서 온도와 측정오차에는
영향을 주지 않는다.

정확한 기준:

측정전류는 `I^2R` 열을 발생시켜 자기발열 오차를 만들 수 있으므로
신호 크기와 발열 사이의 상충관계를 고려한다.

### F05 — `rtd_fatal_two_wire_removes_lead_error`

잘못된 주장:

2선식 RTD는 두 리드선을 사용하므로 리드선 저항이 자동으로
상쇄된다.

정확한 기준:

2선식에서는 두 리드선 저항이 RTD 저항에 직렬로 더해져 측정오차를
만든다.

### F06 — `rtd_fatal_three_wire_perfect_unconditional`

잘못된 주장:

3선식 RTD는 리드선 길이와 저항이 달라도 모든 조건에서 리드선
오차를 완전히 제거한다.

정확한 기준:

3선식은 대응 리드선 저항이 같다는 가정에 의존하며 불평형이 있으면
잔류오차가 발생한다.

### F07 — `rtd_fatal_four_wire_removes_all_error`

잘못된 주장:

4선식 RTD는 배선 수가 많으므로 자기발열, 설치오차, 노이즈와
센서 drift까지 모든 오차를 제거한다.

정확한 기준:

4선식은 주로 리드선 저항 영향을 줄이지만 다른 센서·회로·설치
오차는 별도로 관리해야 한다.

### F08 — `rtd_fatal_wiring_accuracy_only_selection`

잘못된 주장:

RTD 배선방식은 정확도가 가장 높은 4선식만 선택하면 되며 비용,
배선거리, transmitter 위치와 유지보수는 고려할 필요가 없다.

정확한 기준:

2/3/4선식은 요구 불확도, 거리, 비용, 설치조건과 유지보수성을 함께
고려하여 선정한다.

## 7. 권장 답안 구조

### O01 — RTD 온도계측의 변환 사슬

공정온도, 감온부, 저항 변화, 측정전류, 전압과 표시온도의 관계를
설명한다.

참조 Anchor:

- `rtd_temperature_measurement_chain`
- `rtd_metal_resistance_temperature_principle`

### O02 — Pt100 기준과 저항-온도 특성

Pt100의 명칭, 기준저항, 온도계수와 Callendar–Van Dusen 관계를
설명한다.

참조 Anchor:

- `rtd_pt100_reference_resistance_alpha_standard`
- `rtd_callendar_van_dusen_characteristic`

### O03 — 여기전류와 자기발열

정전류 또는 bridge 측정, 신호 크기와 자기발열의 상충관계를
설명한다.

참조 Anchor:

- `rtd_excitation_voltage_measurement`
- `rtd_self_heating_thermal_error`

### O04 — 2선식 리드선 오차

2선식 등가저항과 배선길이·온도에 따른 리드선 오차를 설명한다.

참조 Anchor:

- `rtd_two_wire_lead_resistance_error`

### O05 — 3선식과 4선식 보상

3선식의 동일저항 가정과 4선식 Kelvin 측정의 차이를 설명한다.

참조 Anchor:

- `rtd_three_wire_bridge_compensation_assumptions`
- `rtd_four_wire_kelvin_measurement`

### O06 — 배선방식과 transmitter 선정

정확도, 거리, 비용, 유지보수에 따른 배선방식과 transmitter 구성을
설명한다.

참조 Anchor:

- `rtd_wiring_method_selection_tradeoff`
- `rtd_transmitter_connection_signal_conditioning`

### O07 — 설치와 동적 응답

thermowell, 삽입길이, 유속과 열전도에 따른 응답지연 및 설치오차를
설명한다.

참조 Anchor:

- `rtd_installation_thermowell_dynamic_response`

### O08 — 교정·불확도·고장진단

교정, 허용오차, 불확도, 단선·단락·절연과 loop 검증을 설명한다.

참조 Anchor:

- `rtd_calibration_tolerance_uncertainty`
- `rtd_fault_diagnostics_environment_validation`

## 8. 고득점 해제조건

### H01 — RTD 측정 사슬

온도에서 저항, 여기전류, 전압과 표시온도까지의 변환단계를 명확히
구분한다.

### H02 — Pt100과 Callendar–Van Dusen

Pt100의 명칭과 기준저항을 설명하고 전 온도범위 완전선형이라는
오개념을 피한다.

### H03 — 측정전류와 자기발열

여기전류 증가에 따른 신호 향상과 `I^2R` 자기발열의 상충관계를
설명한다.

### H04 — 2선식 오차

리드선 저항이 RTD 저항에 직렬로 더해지는 2선식 오차를 식으로
설명한다.

### H05 — 3선식 보상조건

3선식 보상이 동일 리드저항 가정에 의존하고 불평형 시 잔류오차가
발생함을 설명한다.

### H06 — 4선식 Kelvin 측정

force와 sense lead를 구분하고 4선식이 리드선 오차만 주로 줄인다는
한계를 설명한다.

### H07 — 설치·응답·선정

배선방식뿐 아니라 transmitter 위치, thermowell, 삽입길이, 응답시간,
비용과 유지보수를 함께 고려한다.

### H08 — 교정과 현장 진단

다점교정, 불확도, 추적성, 단선·단락·절연저하와 loop check를 종합
설명한다.

## 9. Source Topic Pack 작성 계약

후속 Refactor는 다음 작업을 수행한다.

1. Topic Pack 디렉터리 변경

   - 이전:
     `rubrics/topic_packs/rtd_pt100_wire_connection_compensation`
   - 변경:
     `rubrics/topic_packs/rtd_temperature_sensor_principle_pt100_wiring_compensation`

2. Source 파일 5개 수정

   - `README.md`
   - `fact_anchor.json`
   - `logic_check.json`
   - `model_answer.json`
   - `topic_importance.json`

3. 직접 참조 수정

   - `scripts/test_model_answer_router.py`

4. generated bank 6개 재생성

5. 기존 Topic ID 제거 및 새 Topic ID 단일 반영 검증

필수 수량:

- Fact Anchor: 14개
- Fatal Wrong Claim: 8개
- 권장 답안 구조: 8개
- 고득점 해제조건: 8개

추가 원칙:

- 문제 유형은 `PRINCIPLE_INTERPRETATION`로 변경한다.
- 난이도는 `THEORY_CORE`를 유지한다.
- 선택 중요도는 `CORE_MUST_PREPARE`를 유지한다.
- 평가 방식은 `LLM_ONLY`를 유지한다.
- 결정론적 검사는 비활성화한다.
- candidate extraction rule은 비워 둔다.
- 배선보상은 RTD 원리의 하위 구성요소로 포함한다.
- Thermocouple과 Thermistor의 상세 내용은 포함하지 않는다.
- 이전 Topic ID는 generated bank와 runtime 참조에서 제거한다.
- Git 이력 보존을 위해 기존 Source 파일을 새 디렉터리로 이동한 뒤
  내용을 수정한다.
