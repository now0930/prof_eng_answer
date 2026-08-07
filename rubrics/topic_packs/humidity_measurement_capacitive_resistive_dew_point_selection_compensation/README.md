# 습도계측의 원리, 선정 및 보상 — Capacitive·Resistive·Dew Point

- Topic ID: `humidity_measurement_capacitive_resistive_dew_point_selection_compensation`
- Official criterion: `IC-2027-W-2-1`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Historical frequency: 근거가 없어 사용하지 않음

## Scope

이 Topic은 RH·absolute humidity·dew/frost point의 물리적 차이와 capacitive/resistive/chilled-mirror 습도계측의 원리, temperature/condensation 보상 및 선정오차를 다룬다.

핵심 흐름:

`Water vapor → RH / Dew point → Capacitive / Resistive / Chilled mirror → Temperature & Condensation → Selection → Calibration`

## Core equations / definitions

- `RH[%] = 100 × P_w / P_ws(T)`
- `ρ_v = m_v / V`
- 이상기체 근사: `ρ_v = P_w / (R_v T)`
- Dew point: condensation onset temperature at the stated pressure

## Core distinctions

- Relative humidity ≠ Absolute humidity
- RH is temperature dependent
- Dew point ≠ RH percentage
- Dew point ≠ Wet-bulb temperature
- Capacitive humidity sensor ≠ Resistive humidity sensor
- Chilled mirror ≠ polymer RH sensor
- Sensor-local RH ≠ actual process RH when the sensor is heated
- Pressure dew point ≠ automatically atmospheric dew point

## Ownership boundary

다음 상세내용은 기존 Topic이 소유한다.

- Passive resistive/capacitive/inductive transduction 일반론:
  `passive_sensor_resistive_capacitive_inductive_transduction`
- RTD temperature sensor:
  `rtd_temperature_sensor_principle_pt100_wiring_compensation`
- Thermistor:
  `thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization`
- Thermocouple:
  `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`
- Calibration/accuracy/precision metrology 일반론:
  `calibration_error_accuracy_precision`
- Hazardous-area protection/certification:
  `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`

## Grading direction

고득점 답안은 humidity sensor 이름만 나열하지 않는다.

먼저 RH, absolute humidity, dew/frost point를 구분하고 capacitive polymer dielectric과 resistive hygroscopic impedance 원리를 설명해야 한다. 이후 sensor temperature, condensation, hysteresis, drift, contamination과 pressure를 실제 선정·보상·calibration으로 연결한다.

제품별 RH accuracy, exact range, recovery time, warmed-probe heater temperature와 calibration interval을 일반 법칙으로 사용하지 않는다.
