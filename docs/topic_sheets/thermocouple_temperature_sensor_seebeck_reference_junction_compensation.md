# 열전대 온도센서 원리·기준접점 보상·보상도선 Topic Pack 요구사항

## 1. Topic 기본 정보

- Topic ID: `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`
- 한글 제목: 열전대 온도센서의 원리, 기준접점 보상 및 보상도선
- 대표 영문명: Thermocouple temperature sensor, Seebeck effect, reference-junction compensation
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `THEORY_CORE`
- Selection importance: `CORE_MUST_PREPARE`
- Evaluation method: `LLM_ONLY`
- Deterministic checks: 비활성화
- Candidate extraction rules: 비워 둔다.
- 독립 Topic 여부: 독립 Topic
- 관련 비교 Topic: `temperature_sensor_thermocouple_rtd`
- 관련 RTD Topic: `rtd_temperature_sensor_principle_pt100_wiring_compensation`
- 향후 관련 Topic: thermistor NTC/PTC 독립 Topic

## 2. 작성 목적

이 Topic은 열전대의 기본 원리를 단순히 “두 금속에서 전압이 발생한다”는 수준으로 설명하지 않는다.

다음의 전체 측정 체인을 하나의 논리로 설명하도록 요구한다.

공정 온도
→ 측정접점 온도
→ 측정접점과 기준접점의 온도차
→ 열기전력 발생
→ 기준접점 온도 측정
→ 냉접점 보상
→ 열전대 종류별 비선형 변환
→ 지시 온도

답안은 열전대를 RTD와 구분해야 한다.

- RTD는 외부 여자전류를 인가하여 저항을 측정한다.
- 열전대는 서로 다른 도체와 접점 온도차에 의해 열기전력을 발생한다.
- RTD의 2선식·3선식·4선식 보상과 열전대의 냉접점 보상은 서로 다른 원리이다.
- 열전대 보상도선은 단순히 저항이 낮은 전선이 아니다.
- 열전대가 직접 나타내는 물리량은 한 접점의 절대온도가 아니라 측정접점과 기준접점의 온도차에 대응하는 열기전력이다.

## 3. Topic 경계

### 3.1 이 Topic에 포함하는 범위

1. 열전대 측정 체인
2. Seebeck 효과
3. 서로 다른 두 도체와 열전기 회로
4. 측정접점과 기준접점
5. 냉접점 보상
6. 중간금속의 법칙
7. 중간온도의 법칙
8. 열전대 종류와 적용 범위
9. 연장도선과 보상도선
10. 극성과 접속 오류
11. 열기전력의 비선형성과 표준 열기전력표
12. 다항식 또는 표준 변환에 의한 선형화
13. 접지형·비접지형·노출형 측정접점
14. 보호관과 설치 조건
15. 응답속도와 열전달 오차
16. transmitter와 signal conditioner
17. 노이즈·접지·절연
18. 교정·허용오차·불확도·열화
19. 단선·극성 반전·CJC 오류 진단
20. 열전대 종류 선정과 기존 설비 적용 판단

### 3.2 이 Topic에서 제외하는 범위

1. RTD의 Pt100 저항-온도 관계
2. RTD의 Callendar–Van Dusen 식
3. RTD의 2선식·3선식·4선식 리드선 보상
4. RTD 여자전류와 자기발열의 상세 계산
5. thermistor의 NTC·PTC 특성
6. thermistor의 β 식과 Steinhart–Hart 식
7. thermistor의 열폭주
8. 열전대와 RTD를 동등한 비중으로 비교하는 선정형 답안
9. 적외선·써모파일 비접촉 온도센서
10. 보호관 재질 선정만을 독립적으로 다루는 Topic

열전대와 RTD의 비교가 문제의 주된 요구이면 기존 비교 Topic을 사용한다.

이 Topic은 열전대 자체의 원리와 측정회로, 보상, 설치 및 진단을 중심으로 한다.

## 4. 대표 문제 예시

1. 열전대의 측정원리와 기준접점 보상 방법을 설명하시오.
2. Seebeck 효과와 열전대 온도 측정의 관계를 설명하시오.
3. 열전대의 측정접점과 기준접점의 역할을 설명하시오.
4. 냉접점 보상의 필요성과 구현 방법을 설명하시오.
5. 열전대의 중간금속 법칙과 중간온도 법칙을 설명하시오.
6. 열전대 연장도선과 보상도선의 차이 및 사용상 주의사항을 설명하시오.
7. 열전대 종류별 특성과 선정 기준을 설명하시오.
8. 열전대 측정오차의 원인과 진단·개선 방법을 설명하시오.
9. 접지형·비접지형·노출형 열전대 접점의 특성을 설명하시오.
10. 열전대 transmitter의 신호처리와 선형화 과정을 설명하시오.

## 5. 필수 Fact Anchor

### 5.1 `thermocouple_temperature_measurement_chain`

열전대 측정은 공정 온도를 측정접점의 온도로 전달하고, 측정접점과 기준접점의 온도차에 대응하는 열기전력을 측정한 뒤, 기준접점 보상과 열전대 종류별 선형화를 수행하여 온도로 환산하는 과정이다.

답안은 센서, 접점, 배선, 기준접점 센서, 신호처리기와 지시값까지의 측정 체인을 연결해야 한다.

### 5.2 `thermocouple_seebeck_effect_dissimilar_conductors`

서로 다른 두 도체로 폐회로를 구성하고 두 접점에 온도차가 존재하면 열기전력이 발생한다.

열전대의 출력은 단순히 금속 하나의 온도에서 발생하는 전압이 아니라, 재료 조합과 접점 온도의 함수이다.

Seebeck 계수는 재료와 온도에 따라 달라지므로 열전대 출력은 전체 범위에서 완전한 직선이 아니다.

### 5.3 `thermocouple_measures_temperature_difference`

열전대 전압은 측정접점 온도만의 함수가 아니다.

기준접점의 온도가 변하면 동일한 측정접점 온도에서도 측정 전압이 달라진다.

따라서 열전대는 본질적으로 두 접점의 온도차에 대응하는 센서이며, 절대온도를 얻으려면 기준접점 온도를 알아야 한다.

### 5.4 `thermocouple_reference_junction_compensation`

현대의 냉접점 보상은 기준접점을 실제 0°C로 유지하는 방식만을 의미하지 않는다.

일반적으로 입력 단자 주변의 온도를 별도 센서로 측정하고, 해당 기준접점 온도에 대응하는 열기전력을 계산하여 측정 열기전력과 결합한 뒤 측정접점 온도로 환산한다.

CJC 센서 위치, 단자대의 등온성, 내부 온도구배와 보상 알고리즘은 오차에 영향을 준다.

### 5.5 `thermocouple_law_of_intermediate_metals`

열전대 회로에 제3의 금속이 삽입되더라도 그 금속과 열전대 재료 사이에 형성된 두 접점이 동일한 온도에 있으면 순 열기전력은 변하지 않는다.

따라서 단자대, 커넥터와 계측기 내부 도체를 사용할 수 있다.

다만 두 접점의 온도가 다르거나 등온 조건이 깨지면 추가 오차가 발생할 수 있다.

### 5.6 `thermocouple_law_of_intermediate_temperatures`

열전대의 기준접점 온도를 변경할 때 열기전력은 중간온도 법칙에 따라 합성할 수 있다.

E(T1,T3) = E(T1,T2) + E(T2,T3)

이 관계는 기준접점 보상과 표준 열기전력표 환산의 이론적 근거이다.

### 5.7 `thermocouple_type_material_range_atmosphere_selection`

K, J, T, E, N, R, S, B형은 재료 조합, 감도, 사용온도 범위, 산화·환원 분위기 적합성, 안정성, 가격이 서로 다르다.

열전대 종류는 최고온도만으로 선택하지 않는다.

다음 요소를 함께 검토한다.

- 공정 온도 범위
- 산화·환원·진공·부식 분위기
- 요구 정확도와 감도
- 장기 안정성과 drift
- 보호관과 절연재
- 기존 배선과 transmitter 입력 형식
- 유지보수성과 비용

### 5.8 `thermocouple_extension_compensating_wire_polarity`

연장도선은 지정된 온도 범위에서 해당 열전대와 동일하거나 유사한 열기전력 특성을 갖도록 제작한다.

보상도선은 특정 제한 온도 범위에서 원 열전대의 열기전력 특성을 근사하는 별도 합금일 수 있다.

둘 다 단순 저저항 전선이 아니다.

종류, 극성, 허용온도, 접속 위치와 커넥터 재질을 확인해야 한다.

극성이 반대로 연결되면 온도 변화 방향이 반대로 나타나거나 큰 측정오차가 발생한다.

### 5.9 `thermocouple_nonlinearity_reference_tables_polynomial_conversion`

열전대 열기전력과 온도의 관계는 비선형이다.

따라서 열전대 종류별 표준 열기전력표 또는 표준 다항식을 사용하여 전압을 온도로 환산한다.

열전대 종류가 다르면 동일한 전압-온도 변환식을 사용할 수 없다.

다항식 적용 범위와 단위를 확인해야 하며, 범위 밖 외삽은 제한해야 한다.

### 5.10 `thermocouple_junction_construction_response_isolation`

측정접점 구조는 접지형, 비접지형, 노출형으로 구분할 수 있다.

- 접지형은 보호관과 접점이 전기적으로 연결되어 응답이 빠르지만 ground loop와 노이즈에 취약할 수 있다.
- 비접지형은 전기적 절연성이 좋지만 열저항 증가로 응답이 느릴 수 있다.
- 노출형은 응답이 가장 빠르지만 기계적·화학적 보호가 약하다.

선정 시 응답속도, 절연, 노이즈, 공정 유체와 안전을 함께 고려한다.

### 5.11 `thermocouple_thermowell_installation_dynamic_error`

보호관, 삽입길이, 유속, 배관 벽면과의 열전도, 복사, 접촉상태는 측정접점이 실제 공정 온도에 도달하는 과정에 영향을 준다.

열전대 자체의 전기적 원리가 정확해도 설치가 부적절하면 열전달 오차와 응답지연이 발생한다.

보호관의 열용량이 증가하면 일반적으로 응답이 느려진다.

### 5.12 `thermocouple_signal_conditioning_noise_grounding`

열전대 출력은 보통 mV 수준이므로 증폭기 입력 offset, 공통모드 전압, EMI, 접지전위차와 절연저하의 영향을 받기 쉽다.

신호처리기는 다음 기능을 수행할 수 있다.

- 저수준 차동전압 측정
- 냉접점 온도 측정
- 열전대 종류별 선형화
- 단선 감지
- 필터링
- 절연
- 4–20 mA 또는 digital signal 변환

차폐와 접지는 설치환경과 주파수 특성을 고려하여 적용해야 한다.

### 5.13 `thermocouple_calibration_tolerance_uncertainty_drift`

열전대의 허용오차는 열전대 종류, 등급과 온도범위에 따라 다르다.

교정은 기준 온도계와 dry block 또는 bath, 고정점 등을 이용할 수 있다.

전체 불확도에는 다음 요소가 포함될 수 있다.

- 열전대 자체 허용오차
- 열화와 불균질성
- 기준접점 보상 오차
- 계측기 전압 측정 오차
- 표준 변환 오차
- 보호관과 설치에 의한 열전달 오차
- 기준기의 불확도
- 반복성

고온·오염·산화 환경에서는 재료 조성 변화와 drift를 고려해야 한다.

### 5.14 `thermocouple_fault_diagnostics_open_polarity_cjc_validation`

열전대 loop 진단은 단선 여부만 확인해서는 부족하다.

다음 항목을 확인해야 한다.

- 열전대 종류 설정
- 극성
- 연장도선·보상도선 종류
- 단자대 접속
- CJC 센서 위치와 값
- 단선 또는 접촉불량
- 접지와 절연저항
- 노이즈
- 보호관 내부 단락
- 열화와 drift
- transmitter range와 단위
- 실제 공정 온도와 기준기 비교

진단은 센서, 배선, 기준접점 보상, transmitter와 설치조건을 분리하여 수행한다.

## 6. Fatal Wrong Claims

### 6.1 `thermocouple_fatal_absolute_temperature_self_generated_voltage`

잘못된 주장:

열전대는 측정접점의 절대온도에 비례하는 전압을 자체 발생한다.

정확한 기준:

열전대 출력은 측정접점과 기준접점의 온도차 및 재료 조합에 따른 열기전력이다. 절대온도를 구하려면 기준접점 온도 보상이 필요하다.

### 6.2 `thermocouple_fatal_reference_junction_no_effect`

잘못된 주장:

기준접점의 온도는 측정 결과에 영향을 주지 않으므로 냉접점 보상이 필요 없다.

정확한 기준:

기준접점 온도가 변하면 측정 전압도 변한다. 기준접점 온도를 실제로 유지하거나 측정하여 보상해야 한다.

### 6.3 `thermocouple_fatal_cjc_fixed_voltage_subtraction`

잘못된 주장:

냉접점 보상은 모든 열전대 신호에서 일정한 전압을 빼는 것이다.

정확한 기준:

기준접점 온도와 열전대 종류에 대응하는 비선형 열기전력을 계산하여 측정값과 합성해야 한다.

### 6.4 `thermocouple_fatal_every_intermediate_metal_creates_error`

잘못된 주장:

열전대 회로에 다른 금속을 접속하면 항상 추가 열기전력이 발생하여 사용할 수 없다.

정확한 기준:

중간금속의 두 접점이 동일 온도에 있으면 순 열기전력은 변하지 않는다. 등온 조건이 깨질 때 오차가 발생할 수 있다.

### 6.5 `thermocouple_fatal_copper_wire_always_equivalent`

잘못된 주장:

열전대 배선은 일반 동선을 사용해도 항상 동일하다.

정확한 기준:

일반 동선을 사용하면 기준접점 위치가 이동하거나 추가 접점 온도차에 따른 오차가 생길 수 있다. 지정된 연장도선 또는 보상도선과 적절한 접속조건을 사용해야 한다.

### 6.6 `thermocouple_fatal_compensating_wire_low_resistance_only`

잘못된 주장:

보상도선은 전압강하를 줄이기 위해 저항이 낮은 전선을 사용하는 것이다.

정확한 기준:

보상도선은 제한된 온도범위에서 특정 열전대와 유사한 열기전력 특성을 갖도록 설계된 합금 도선이다.

### 6.7 `thermocouple_fatal_all_types_same_voltage_table`

잘못된 주장:

열전대 종류가 달라도 동일한 mV-온도표를 사용할 수 있다.

정확한 기준:

각 열전대 종류는 재료 조합과 열기전력 특성이 다르므로 종류별 표준표와 다항식을 사용해야 한다.

### 6.8 `thermocouple_fatal_perfect_linear_and_polarity_irrelevant`

잘못된 주장:

열전대 출력은 전 범위에서 완전한 직선이며 극성은 측정값에 영향을 주지 않는다.

정확한 기준:

열전대 출력은 비선형이고 종류별 선형화가 필요하다. 극성 반전은 신호 방향과 온도 환산에 중대한 오류를 발생시킨다.

## 7. 권장 답안 구조

1. 열전대의 정의와 전체 측정 체인
2. Seebeck 효과와 온도차 측정 원리
3. 측정접점·기준접점과 냉접점 보상
4. 중간금속·중간온도 법칙
5. 열전대 종류와 선정 기준
6. 연장도선·보상도선·극성
7. 비선형 선형화와 signal conditioning
8. 설치·교정·오차·진단 및 결론

## 8. High-band Unlock Conditions

고득점 band를 허용하려면 다음 조건을 모두 충족해야 한다.

1. 열전대가 절대온도가 아니라 접점 온도차에 대응하는 열기전력을 발생한다는 점을 설명한다.
2. Seebeck 효과와 서로 다른 도체의 역할을 설명한다.
3. 측정접점과 기준접점을 구분하고 냉접점 보상 절차를 설명한다.
4. 중간금속 법칙과 중간온도 법칙을 적용 조건과 함께 설명한다.
5. 연장도선과 보상도선의 목적, 재질, 극성 및 허용온도를 설명한다.
6. 열전대 종류별 비선형 특성과 종류별 표준 변환의 필요성을 설명한다.
7. 접점 구조, 보호관과 설치조건을 응답속도·절연·노이즈와 연결한다.
8. 교정, 불확도, drift, 단선·극성·CJC 오류 진단을 포함한다.

하나 이상의 핵심 원리를 반대로 설명하거나 Fatal Wrong Claim에 해당하면 high-band를 허용하지 않는다.

## 9. 답안 평가 원칙

### 9.1 인정할 설명

표현이 요구사항과 동일하지 않아도 다음 의미가 정확하면 인정한다.

- 열전대는 온도차에 따른 열기전력을 이용한다.
- 기준접점 온도를 알고 보상해야 측정접점 온도를 구할 수 있다.
- CJC는 기준접점 온도에 해당하는 열기전력을 계산하여 환산하는 과정이다.
- 중간금속 법칙은 삽입 금속의 두 접점이 등온일 때 성립한다.
- 중간온도 법칙은 열기전력의 구간 합성에 사용한다.
- 보상도선은 열기전력 특성을 근사하는 전용 합금 도선이다.
- 열전대 종류별 전압-온도 특성이 다르다.
- 설치, 접점 구조와 보호관이 동특성과 측정오차에 영향을 준다.

### 9.2 부족한 답안

다음과 같은 답안은 낮게 평가한다.

- Seebeck 효과라는 용어만 제시하고 측정접점·기준접점을 설명하지 않음
- 냉접점 보상을 단순한 영점조정으로 설명함
- 열전대 종류를 나열하지만 선정기준이 없음
- 보상도선을 단순한 저저항 배선으로 설명함
- 설치와 보호관에 따른 응답지연을 누락함
- 비선형성과 종류별 표준표를 누락함
- 단선만 진단하고 CJC·극성·절연·노이즈를 누락함
- RTD 3선식 보상과 열전대 냉접점 보상을 혼동함

### 9.3 LLM 평가 원칙

- 키워드 출현 여부만으로 평가하지 않는다.
- 원리, 조건, 인과관계와 현장 적용성을 의미 기반으로 평가한다.
- 동일한 문장을 요구하지 않는다.
- 표준에 맞는 다른 식과 설명도 의미가 정확하면 인정한다.
- 결정론적 문자열 규칙으로 Fatal 여부를 확정하지 않는다.
- Candidate extraction 규칙은 두지 않는다.
- deterministic check의 enabled 값은 false로 유지한다.

## 10. Topic Alias 후보

다음 표현을 Topic routing 후보로 사용한다.

- 열전대
- thermocouple
- Seebeck effect
- Seebeck
- 제벡 효과
- 열기전력
- thermoelectric voltage
- 측정접점
- hot junction
- measuring junction
- 기준접점
- reference junction
- cold junction
- 냉접점
- 냉접점 보상
- cold junction compensation
- CJC
- 중간금속의 법칙
- law of intermediate metals
- 중간온도의 법칙
- law of intermediate temperatures
- 연장도선
- extension wire
- 보상도선
- compensating wire
- 열전대 극성
- K type thermocouple
- J type thermocouple
- T type thermocouple
- E type thermocouple
- N type thermocouple
- R type thermocouple
- S type thermocouple
- B type thermocouple
- 접지형 열전대
- 비접지형 열전대
- 노출형 열전대

다음 단독 표현만으로는 이 Topic을 강하게 선택하지 않는다.

- RTD
- Pt100
- 3선식
- 4선식
- Callendar–Van Dusen
- thermistor
- NTC
- PTC
- 적외선 온도계
- thermopile

## 11. Cross-topic Contamination 방지

### 11.1 RTD와의 구분

이 Topic에서 다음 내용을 열전대 원리로 설명하면 안 된다.

- 외부 여자전류로 센서 저항을 측정한다.
- Pt100은 0°C에서 100Ω이다.
- 3선식 브리지로 리드저항을 상쇄한다.
- 4선식 Kelvin 측정으로 리드저항 영향을 제거한다.
- Callendar–Van Dusen 식으로 온도를 환산한다.

### 11.2 Thermistor와의 구분

이 Topic에서 다음 내용을 열전대 원리로 설명하면 안 된다.

- NTC와 PTC의 저항 특성
- β 식
- Steinhart–Hart 식
- thermistor의 분압 회로
- thermistor의 열폭주

### 11.3 기존 비교 Topic과의 관계

`temperature_sensor_thermocouple_rtd`는 열전대와 RTD의 비교·선정 문제에 사용한다.

새 Topic은 열전대 자체의 원리·기준접점 보상·보상도선·설치·오차·진단을 깊게 평가한다.

기존 비교 Topic을 삭제하거나 새 Topic으로 rename하지 않는다.

## 12. Source Pack 작성 요구사항

다음 단계에서 아래 파일을 직접 작성한다.

- `rubrics/topic_packs/thermocouple_temperature_sensor_seebeck_reference_junction_compensation/README.md`
- `rubrics/topic_packs/thermocouple_temperature_sensor_seebeck_reference_junction_compensation/fact_anchor.json`
- `rubrics/topic_packs/thermocouple_temperature_sensor_seebeck_reference_junction_compensation/logic_check.json`
- `rubrics/topic_packs/thermocouple_temperature_sensor_seebeck_reference_junction_compensation/model_answer.json`
- `rubrics/topic_packs/thermocouple_temperature_sensor_seebeck_reference_junction_compensation/topic_importance.json`

Source JSON은 사람이 확정한 이 요구사항 Markdown을 기준으로 직접 작성한다.

Gemini 또는 다른 LLM이 Source JSON을 자동 생성하게 하지 않는다.

## 13. Source JSON 수량 계약

- Fact Anchor: 14개
- Fact Fatal Wrong Claim: 8개
- Logic truth schema: 14개
- Logic fatal condition: 8개
- Recommended outline: 8개
- High-band unlock condition: 8개
- Deterministic fatal check: 0개
- Deterministic major check: 0개
- Deterministic question-type check: 0개
- Candidate extraction rule: 0개

## 14. 정확한 Anchor ID

1. `thermocouple_temperature_measurement_chain`
2. `thermocouple_seebeck_effect_dissimilar_conductors`
3. `thermocouple_measures_temperature_difference`
4. `thermocouple_reference_junction_compensation`
5. `thermocouple_law_of_intermediate_metals`
6. `thermocouple_law_of_intermediate_temperatures`
7. `thermocouple_type_material_range_atmosphere_selection`
8. `thermocouple_extension_compensating_wire_polarity`
9. `thermocouple_nonlinearity_reference_tables_polynomial_conversion`
10. `thermocouple_junction_construction_response_isolation`
11. `thermocouple_thermowell_installation_dynamic_error`
12. `thermocouple_signal_conditioning_noise_grounding`
13. `thermocouple_calibration_tolerance_uncertainty_drift`
14. `thermocouple_fault_diagnostics_open_polarity_cjc_validation`

## 15. 정확한 Fatal ID

1. `thermocouple_fatal_absolute_temperature_self_generated_voltage`
2. `thermocouple_fatal_reference_junction_no_effect`
3. `thermocouple_fatal_cjc_fixed_voltage_subtraction`
4. `thermocouple_fatal_every_intermediate_metal_creates_error`
5. `thermocouple_fatal_copper_wire_always_equivalent`
6. `thermocouple_fatal_compensating_wire_low_resistance_only`
7. `thermocouple_fatal_all_types_same_voltage_table`
8. `thermocouple_fatal_perfect_linear_and_polarity_irrelevant`

## 16. Revision Notes 요구사항

Source Pack의 revision notes에는 최소한 다음 항목을 포함한다.

- `created_from_reviewed_thermocouple_requirements_markdown`
- `separated_from_temperature_sensor_thermocouple_rtd_comparison_topic`
- `separated_from_rtd_pt100_wiring_compensation_topic`
- `focused_on_seebeck_reference_junction_cjc_and_compensating_wire`
- `thermistor_ntc_ptc_kept_as_independent_future_topic`
- `deterministic_checks_disabled`
- `candidate_extraction_rules_empty`

## 17. 완료 조건

이 요구사항 단계는 다음 조건을 만족하면 완료한다.

1. 새 요구사항 Markdown 파일만 추가한다.
2. 기존 파일을 수정하지 않는다.
3. Source JSON은 아직 작성하지 않는다.
4. generated bank를 변경하지 않는다.
5. staging하지 않는다.
6. 정확한 Anchor ID 14개를 포함한다.
7. 정확한 Fatal ID 8개를 포함한다.
8. Question type을 `PRINCIPLE_INTERPRETATION`으로 고정한다.
9. `LLM_ONLY`와 deterministic checks 비활성화를 명시한다.
10. 기존 열전대·RTD 비교 Topic을 유지한다고 명시한다.
11. RTD와 thermistor의 Topic 경계를 명확히 한다.
12. 다음 단계에서 이 문서를 기준으로 Source Pack JSON을 직접 작성한다.

## 18. Data-driven Topic 라우팅 필드

- `model_answer.json.routing_aliases`는 열전대 Topic 후보를 식별하는 전용 라우팅 메타데이터이다.
- `model_answer.json.routing_field_points`는 열전대 현장 적용성을 보완하는 전용 라우팅 메타데이터이다.
- 두 필드가 없으면 generated builder가 fallback을 사용하므로 다른 Topic의 값이 혼입되지 않도록 명시적으로 관리한다.
- deterministic 채점은 계속 비활성화한다.
