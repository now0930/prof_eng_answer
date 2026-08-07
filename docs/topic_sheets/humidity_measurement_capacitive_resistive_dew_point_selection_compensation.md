# 습도계측의 원리, 선정 및 보상 — Capacitive·Resistive·Dew Point

## 0. Topic identity

- Topic ID: `humidity_measurement_capacitive_resistive_dew_point_selection_compensation`
- Official criterion: `IC-2027-W-2-1`
- Official scope label: 습도 계측
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Historical frequency: 근거가 없어 사용하지 않음
- Grading mode: LLM semantic review 중심
- Deterministic fatal keyword rule: 사용하지 않음

## 1. 출제 의도

이 Topic은 습도센서 종류를 나열하는 문제가 아니다.

핵심 흐름은 다음과 같다.

`Water vapor state → RH / Absolute humidity / Dew point → Capacitive / Resistive / Chilled mirror principle → Temperature compensation → Condensation / Hysteresis / Drift → Selection / Calibration`

## 2. 습도 물리량

### 2.1 Water-vapor partial pressure

공기 중 수증기는 partial pressure `P_w`로 표현할 수 있다.

같은 온도에서 가능한 최대 수증기분압을 saturation vapor pressure `P_ws(T)`로 본다.

### 2.2 Relative Humidity

Relative humidity는 다음과 같이 정의한다.

`RH[%] = 100 × P_w / P_ws(T)`

핵심은 `P_ws`가 **temperature function**이라는 점이다.

수증기량이 거의 일정해도:

- 공기를 가열하면 `P_ws(T)`가 증가하여 RH가 감소할 수 있다.
- 공기를 냉각하면 RH가 증가하고 saturation에 접근한다.

따라서 RH sensor의 온도는 측정오차와 직접 연결된다.

### 2.3 Absolute Humidity

Absolute humidity는 단위체적당 수증기 질량으로 정의할 수 있다.

`ρ_v = m_v / V`

이상기체 근사에서는,

`ρ_v = P_w / (R_v T)`

RH와 absolute humidity를 동일한 물리량으로 취급하지 않는다.

## 3. Dew Point와 Frost Point

Dew point `T_d`는 현재 moisture content와 pressure에서 공기를 냉각할 때 liquid water condensation이 시작되는 온도다.

Ambient temperature가 dew point에 가까워질수록 condensation risk가 커진다.

### 3.1 Frost point

0°C 이하에서는 응축상이 ice인 경우 frost point라는 표현을 사용한다.

Subzero dry gas에서는 dew point/frost point 정의와 instrument output convention을 확인한다.

### 3.2 Pressure dew point

Compressed air/gas에서는 measurement pressure를 명확히 한다.

Pressure가 바뀌면 동일한 water-vapor amount라도 condensation condition이 달라질 수 있으므로 pressure dew point와 atmospheric-equivalent dew point를 혼동하지 않는다.

## 4. Capacitive Humidity Sensor

대표적인 capacitive RH sensor는 porous electrode 사이에 hygroscopic polymer dielectric을 둔다.

수분이 polymer에 흡수되면 dielectric constant가 변하고 capacitance가 변한다.

`Water absorption → ε_r change → C change → electronics → RH`

정확한 capacitance 식과 polymer constant는 sensor geometry와 material에 따라 달라진다.

### 4.1 Temperature compensation

Capacitive RH measurement에는 temperature 영향이 두 경로로 들어온다.

1. RH 정의 자체의 `P_ws(T)`
2. Polymer/electronics의 temperature coefficient

따라서 colocated temperature sensor와 factory calibration coefficient를 이용한 compensation이 중요하다.

### 4.2 Error source

- Hysteresis
- Long-term drift
- Chemical contamination
- Dust/filter loading
- Condensation
- Sensor self-heating
- Response time

제품별 recovery와 chemical resistance를 확인한다.

## 5. Resistive Humidity Sensor

Resistive humidity sensor는 hygroscopic material의 water uptake에 따른 electrical resistance 또는 impedance 변화를 이용한다.

가능한 sensing material:

- Polymer
- Salt/electrolytic film
- Ceramic

`Water adsorption → ionic/electronic conduction change → R/Z change`

재료와 구조에 따라 AC excitation으로 impedance를 측정하여 polarization과 electrode degradation을 줄이는 경우가 있다.

AC frequency와 circuit 조건은 제조사 사양을 따른다.

### 5.1 대표 제한

- Nonlinearity
- Temperature dependence
- High-RH recovery
- Condensation
- Contamination
- Aging/drift

Capacitive 방식과 resistive 방식을 동일한 transduction principle로 설명하지 않는다.

## 6. Chilled-Mirror Dew-Point Hygrometer

Chilled mirror는 dew point의 정의 자체에 가까운 직접적 측정을 한다.

1. Gas sample을 mirror 위로 흘린다.
2. Mirror를 냉각한다.
3. Reflected light 변화를 감지한다.
4. Condensation onset 또는 evaporation-condensation equilibrium을 제어한다.
5. Mirror temperature를 dew/frost point로 읽는다.

### 6.1 장점

- 높은 accuracy/reference measurement에 유리
- Sensor material의 empirical RH calibration에 덜 의존

### 6.2 제한

- Mirror contamination
- Optical fouling
- Cleaning 필요
- Sampling system 영향
- Frost/dew phase 판별
- Cost와 maintenance

## 7. Psychrometric Method

Dry-bulb와 wet-bulb의 온도차를 이용한다.

Wet bulb는 물이 증발하면서 냉각되는 equilibrium temperature다.

영향요인:

- Air velocity
- Wick condition
- Water purity
- Radiation
- Pressure

**Wet-bulb temperature를 dew point와 동일시하지 않는다.**

## 8. Condensation과 Sensor Temperature

습도센서의 실제 표면온도가 중요하다.

### 8.1 Sensor가 차가운 경우

Sensor surface가 ambient보다 차가우면 local RH가 높아지고 dew point 아래에서는 condensation이 생길 수 있다.

### 8.2 Sensor가 따뜻한 경우

Self-heating 또는 warmed sensor는 local RH를 낮출 수 있다.

따라서 local sensor RH와 actual process RH를 구분한다.

### 8.3 Warmed probe

High humidity에서 condensation risk가 큰 경우 sensor head를 dew point보다 높게 유지하는 warmed probe 기술을 사용할 수 있다.

이 경우 actual RH 계산에는 별도의 ambient/process temperature가 필요하다.

## 9. Low-Humidity Measurement

Very low humidity에서는 RH 값 자체가 작고 temperature error의 상대적 영향이 커질 수 있다.

따라서 다음 방식이 더 적합할 수 있다.

- Dew point
- Frost point
- Trace moisture
- ppm moisture

선정은 required range, uncertainty, pressure와 contamination 조건으로 결정한다.

## 10. 선정 기준

### 10.1 Measurand

- RH
- Dew/frost point
- Absolute humidity
- Trace moisture

측정하고 싶은 물리량부터 구분한다.

### 10.2 Range / Accuracy

- Normal RH
- High humidity
- Very dry gas
- Required uncertainty
- Response time
- Long-term stability

### 10.3 Process condition

- Temperature
- Pressure
- Air velocity
- Condensation
- Chemical vapor
- Dust/oil
- Cleanliness
- Sampling line

### 10.4 Installation

- Duct insertion depth
- Representative location
- Thermal gradient
- Wall/pipe conduction
- Airflow
- Filter
- Cable/interface
- Enclosure

### 10.5 Hazardous area

Hazardous-area protection/certification 상세는 별도 Topic이 소유한다.

## 11. 대표 오차와 보상

### 11.1 Temperature error

- RH definition
- Sensor material temperature coefficient
- Self-heating
- Thermal gradient

대책:

- Colocated temperature measurement
- Temperature compensation
- Proper thermal placement

### 11.2 Hysteresis

Adsorption와 desorption path가 다를 수 있다.

Calibration에서 상승/하강 humidity history를 고려한다.

### 11.3 Drift

- Polymer aging
- Chemical exposure
- Contamination
- Electronics drift

대책:

- Periodic calibration
- Filter/protection
- Replaceable probe
- Field check

### 11.4 Condensation

Condensation 후 recovery time과 contaminated condensate 영향을 고려한다.

필요한 경우 warmed probe, proper location, heating 또는 dew-point margin을 사용한다.

## 12. Calibration

가능한 reference:

- Humidity generator
- Reference hygrometer
- Salt solution
- Chilled-mirror reference

Field check와 full calibration을 구분한다.

중요 조건:

- Equilibration time
- Temperature stability
- Chamber uniformity
- Traceability
- Multiple points
- As-found / As-left record

한 점 field check가 모든 hysteresis와 drift를 제거한다고 보지 않는다.

## 13. 기존설비 적용 시 실무 고려

Retrofit에서는 sensor accuracy만 비교하지 않는다.

- Existing duct/process location
- Airflow
- Condensation history
- Chemical exposure
- Existing cable
- 4-20 mA / voltage / digital interface
- DCS/PLC scaling
- Calibration access
- Shutdown
- Spare
- Replaceable filter/probe
- Lifecycle cost

법규·안전·위험장소 요구사항은 비용만으로 무시할 수 없다.

## 14. 근거와 범위

대표 기술근거는 다음 원리와 일치한다.

- Vaisala: `RH = P_w/P_ws(T)` 정의, dew point와 pressure/temperature/condensation 영향, chilled-mirror 원리, high-humidity warmed-probe 적용
- Sensirion: hygroscopic polymer dielectric의 water absorption/desorption에 따른 capacitance 변화와 integrated temperature measurement
- Honeywell/Vaisala 자료: moisture-sensitive resistive material의 resistance/impedance 변화와 capacitive polymer 방식의 구분

제품별 RH accuracy, exact sensing range, recovery time, heater temperature, calibration interval과 chemical-resistance 수치는 일반 법칙으로 사용하지 않는다.

## 15. Grading boundary

이 Topic의 핵심 연결은 다음이다.

1. RH, absolute humidity, dew/frost point를 구분한다.
2. Capacitive sensor의 dielectric-capacitance 변환을 설명한다.
3. Resistive sensor의 hygroscopic resistance/impedance 변환을 설명한다.
4. Chilled-mirror dew-point principle을 설명한다.
5. Temperature, condensation, hysteresis, drift를 선정·보상·calibration과 연결한다.

다음 기존 Topic과 ownership을 분리한다.

- `passive_sensor_resistive_capacitive_inductive_transduction`
- `rtd_temperature_sensor_principle_pt100_wiring_compensation`
- `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization`
- `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`
- `calibration_error_accuracy_precision`
- `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
