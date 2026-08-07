# 압력계측 센서의 원리, 선정 및 오차 — Bourdon·Diaphragm·Piezoresistive·DP

- Topic ID: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`
- Official criterion: `IC-2027-W-2-1`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Historical frequency: 근거가 없어 사용하지 않음

## Scope

이 Topic은 압력 reference와 Bourdon·Diaphragm·Piezoresistive·DP pressure sensing의 원리, 선정과 오차를 다룬다.

핵심 흐름:

`Absolute/Gauge/DP → Mechanical/Electrical sensing → Range & Process selection → Static/Temperature/Installation error → Calibration & Protection`

## Core distinctions

- Absolute pressure ≠ Gauge pressure ≠ Differential pressure
- Bourdon tube: elastic deformation → mechanical displacement → pointer
- Diaphragm: pressure difference → membrane deflection
- Diaphragm sensing element ≠ Diaphragm seal
- Piezoresistive: strain → resistance change → Wheatstone bridge output
- Piezoresistive static measurement ≠ Piezoelectric dynamic emphasis
- DP: `ΔP = P_H - P_L`
- Measurement range ≠ Maximum working pressure ≠ Burst pressure
- Reference accuracy ≠ Field total performance
- Zero shift ≠ Span shift

## Ownership boundary

다음 상세내용은 기존 Topic이 소유한다.

- Hydrostatic DP level, density compensation, wet/dry leg, level remote-seal head:
  `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`
- Wheatstone bridge/load-cell 상세와 strain-gauge temperature compensation:
  `strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error`
- Piezoelectric dynamic force/pressure/acceleration과 charge amplifier:
  `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration`
- Passive resistive/capacitive/inductive transduction 일반론:
  `passive_sensor_resistive_capacitive_inductive_transduction`
- Hazardous-area protection/certification 상세:
  `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
- Accuracy/precision/calibration metrology 일반론:
  `calibration_error_accuracy_precision`

## Grading direction

고득점 답안은 센서 종류만 나열하지 않는다.

압력 reference를 정한 뒤 각 sensing principle을 물리적으로 설명하고, range·mechanical pressure limit·process compatibility·environment를 선정기준으로 연결해야 한다. 이후 temperature, static line pressure, zero/span drift, impulse line, pulsation/vibration 오차와 calibration·protection 대책을 제시해야 한다.

DP transmitter의 static line pressure zero/span effect는 model과 range에 따라 달라질 수 있으므로 특정 제품의 수치값을 일반공식처럼 사용하지 않는다.

Existing plant에서는 process connection, manifold, impulse line 상태, DCS/PLC interface, shutdown, spare, calibration equipment와 lifecycle cost까지 고려한다.
