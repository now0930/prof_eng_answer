# 압력계측 센서의 원리, 선정 및 오차 — Bourdon·Diaphragm·Piezoresistive·DP

## 0. Topic identity

- Topic ID: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`
- Official criterion: `IC-2027-W-2-1`
- Official scope label: 압력 계측
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Historical frequency: 근거가 없어 사용하지 않음
- Grading mode: LLM semantic review 중심
- Deterministic fatal keyword rule: 사용하지 않음

## 1. 출제 의도

이 Topic은 압력센서 이름을 나열하는 문제가 아니라 **압력 기준 정의 → sensing principle → 신호변환 → 선정조건 → 설치·환경 오차 → 보정·유지보수**의 연결을 평가한다.

핵심 흐름은 다음과 같다.

`Pressure reference → Bourdon/Diaphragm/Piezoresistive/DP 원리 → Range·Process·Environment 선정 → Error source → Calibration/Protection`

## 2. 압력의 기준과 기본 관계

### 2.1 Absolute, Gauge, Differential

- Absolute pressure: 완전진공을 기준으로 한 압력
- Gauge pressure: 주변 대기압을 기준으로 한 압력
- Differential pressure: 두 지점 압력의 차

게이지압이 국소 대기압 기준이면 다음 관계를 사용한다.

`P_abs = P_gauge + P_atm`

DP transmitter는 포트 정의가 올바른 경우 통상 다음과 같이 해석한다.

`ΔP = P_H - P_L`

부호는 실제 high/low port 연결과 transmitter 설정을 함께 확인한다.

## 3. Bourdon tube

Bourdon tube는 타원형 단면의 굽은 탄성관을 사용한다.

내부압력이 증가하면 단면이 원형에 가까워지고 관은 펴지려는 방향으로 변형된다. 자유단의 변위를 linkage와 movement가 pointer 회전으로 바꾸어 압력을 표시한다.

C-shaped, spiral, helical 등의 형상이 사용된다. 형상·재질·두께에 따라 압력범위가 달라지므로 특정 범위를 모든 Bourdon gauge의 절대 한계로 암기하지 않는다.

### 3.1 장점

- 외부 전원 없이 현장 지시 가능
- 구조가 비교적 단순하고 견고
- 중·고압 영역에서 널리 사용
- 현장 점검이 직관적

### 3.2 대표 오차·대책

- 탄성 hysteresis와 creep
- linkage 마찰·backlash
- vibration과 pulsation
- process/ambient temperature
- overpressure와 pressure spike

필요에 따라 snubber, pulsation damper, siphon, remote mounting, overpressure protector를 검토한다. 보호장치는 response time과 plugging risk에도 영향을 줄 수 있다.

## 4. Diaphragm pressure element

Diaphragm은 막 양측의 압력차에 의해 변형된다.

얇고 유연한 diaphragm은 낮은 압력에서 높은 감도를 얻기 쉽다. 변위를 기계식 linkage로 읽거나 capacitive, piezoresistive, strain-based element 등으로 전기신호화할 수 있다.

### 4.1 Diaphragm sensing element와 diaphragm seal

두 용어를 동일시하지 않는다.

- Diaphragm sensing element: 압력차를 직접 변형으로 변환하는 sensing element
- Diaphragm seal: 공정유체를 계기에서 격리하고 fill fluid 등을 통해 압력을 전달하는 process interface

Seal은 부식성·점성·고형물·고온 등에서 유용할 수 있지만 fill fluid, capillary, 온도, 설치높이에 따른 추가 영향이 생길 수 있다.

## 5. Piezoresistive pressure sensor

Piezoresistive effect는 기계적 strain에 따라 저항이 변하는 현상이다.

대표적 pressure sensor는 silicon diaphragm 또는 금속 diaphragm에 결합한 piezoresistive element를 사용하고, 여러 저항을 Wheatstone bridge로 구성해 작은 저항변화를 차동 전압으로 읽는다.

작은 변화에서 bridge output은 excitation voltage와 resistance imbalance에 비례하도록 설계할 수 있으나 정확한 식은 resistor 배치와 회로에 따라 달라진다.

### 5.1 특징

- 정적 및 저주파 압력 측정 가능
- 높은 감도
- 소형화와 전자보정에 유리
- excitation과 signal conditioning 필요
- offset와 sensitivity의 온도보정 중요

Piezoelectric sensor의 charge generation 원리와 구분한다. Piezoelectric은 동적 압력·진동 측정에 강점이 있지만 정적 측정에는 구조적 제약이 있다.

## 6. Differential pressure transmitter

DP transmitter는 high-side와 low-side 두 압력을 sensing element 양쪽에 전달하여 그 차를 전기신호로 변환한다.

두 포트에 같은 line pressure를 인가하면 이상적인 differential input은 0이다.

### 6.1 Static line pressure

실제 transmitter는 큰 common-mode/static line pressure가 가해지면 sensor 구조와 range에 따라 zero 또는 span 영향이 나타날 수 있다.

따라서 다음을 확인한다.

1. Maximum working/static pressure rating
2. Static pressure zero effect
3. Static pressure span effect
4. Line-pressure calibration 또는 trim 절차

특정 model의 %값을 모든 DP transmitter의 공통 공식으로 사용하지 않는다.

### 6.2 DP level Topic과의 경계

이 Topic은 DP transmitter의 sensing 원리와 pressure application을 소유한다.

다음은 기존 `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error` Topic이 소유한다.

- Hydrostatic level 변환
- Density compensation
- Wet leg / Dry leg
- Level zero elevation/suppression 계산
- Level용 remote-seal head와 capillary 상세오차

## 7. 압력계기 선정

### 7.1 Pressure reference

Absolute, gauge, differential 중 실제 process requirement를 먼저 정한다.

### 7.2 Range

- Normal / minimum / maximum pressure
- Calibration LRV/URV
- URL/LRL
- Turndown
- Required resolution
- Required accuracy/total performance

정상 운전점이 지나치게 range 끝단에 몰리지 않도록 한다.

### 7.3 Mechanical limits

Measurement range와 다음 항목을 구분한다.

- Maximum working pressure
- Overrange/proof pressure
- Burst pressure

Pressure spike와 upset condition을 별도 검토한다.

### 7.4 Process compatibility

- Wetted material
- Corrosion
- Viscosity/solid
- Process temperature
- Process connection
- Seal/isolator
- Flushing/drain

### 7.5 Environment

- Ambient temperature
- Humidity
- Vibration
- EMC
- Ingress protection
- Hazardous area

위험장소 인증과 방폭 방식 상세는 `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection` Topic이 소유한다.

## 8. 오차 구조

### 8.1 Reference accuracy

Reference accuracy는 제조사에 따라 linearity, hysteresis, repeatability 등의 조합으로 정의될 수 있다.

따라서 datasheet 정의를 확인한다.

### 8.2 Total performance

현장에서는 다음 영향까지 함께 검토한다.

- Ambient/process temperature
- Static line pressure
- Stability/drift
- Mounting orientation
- Power supply/output loading
- Installation
- Impulse line
- Vibration/pulsation

오차항을 항상 단순 산술합한다고 단정하지 않는다. 제조사의 accuracy/total performance 정의와 통계적 결합 방식을 확인한다.

## 9. Zero, Span과 Calibration

- Zero shift: 입력 0 또는 LRV 부근의 offset 변화
- Span shift: sensitivity 또는 URV-LRV 관계의 변화

Zero trim이 모든 span·nonlinearity 오차를 해결하는 것은 아니다.

설치방향, static line pressure, remote interface와 process condition이 영향을 주면 제조사 절차에 따라 zero trim, sensor trim, rerange 또는 full calibration을 구분한다.

DP transmitter에서는 필요한 경우 실제 line pressure를 인가한 zero correction을 수행할 수 있다. 구체 절차는 모델과 range에 따라 달라진다.

## 10. Impulse line과 설치오차

도압관을 사용하는 pressure/DP 측정에서는 sensing element가 정상이어도 전달계가 문제를 만들 수 있다.

주요 원인은 다음과 같다.

1. Leak
2. Blockage
3. Gas pocket
4. Liquid head
5. Condensation/freezing
6. Unequal temperature
7. Manifold valve misalignment

Service에 맞는 slope, vent/drain, leak test, flushing과 heat tracing을 검토한다.

## 11. 기존설비 적용 시 실무 고려

Retrofit에서는 새 transmitter의 성능만 보지 않는다.

- 기존 process connection과 manifold
- 기존 impulse line 상태
- DCS/PLC input과 signal type
- Power supply
- Hazardous-area certification
- Shutdown 가능시간
- Spare와 calibration equipment
- Maintenance skill
- Lifecycle cost

법규·안전·pressure containment를 비용만으로 정당화해 무시할 수 없다. 그 외 개선항목은 risk와 shutdown, 기존 interface, lifecycle benefit을 고려해 단계적으로 적용할 수 있다.

## 12. 근거와 범위

대표적인 기술근거는 다음 원리와 일치한다.

- WIKA: Bourdon tube의 타원형 단면과 자유단 변위, diaphragm element의 압력차 변형 원리
- Honeywell/TE Connectivity: diaphragm의 piezoresistor와 Wheatstone bridge 기반 pressure sensing
- Emerson Rosemount reference manuals: DP transmitter에서 model/range에 따른 static line pressure zero/span 영향과 line-pressure 보정 절차

제품별 수치 사양은 일반 법칙으로 사용하지 않는다.

## 13. Grading boundary

이 Topic의 핵심 연결은 다음 다섯 가지다.

1. Pressure reference를 구분한다.
2. Bourdon·Diaphragm·Piezoresistive·DP의 물리원리를 설명한다.
3. Range·mechanical limit·process·environment를 기준으로 선정한다.
4. Zero/span·temperature·static pressure·installation error를 구분한다.
5. Calibration·protection·maintenance로 현장오차를 관리한다.

다음 기존 Topic과 ownership을 분리한다.

- `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`
- `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`
- `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration`
- `passive_sensor_resistive_capacitive_inductive_transduction`
- `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
- `calibration_error_accuracy_precision`
