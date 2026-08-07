# 회전속도 계측의 원리, 선정 및 오차 — Encoder·Proximity·Tachometer

- Topic ID: `speed_rotation_measurement_encoder_proximity_tachometer_selection_error`
- Official criterion: `IC-2027-W-2-1`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Historical frequency: 근거가 없어 사용하지 않음

## Scope

이 Topic은 shaft/rotational speed를 pulse 또는 analog voltage로 변환하는 원리와 실제 RPM 계산, 선정 및 오차를 다룬다.

핵심 흐름:

`Rotation → Encoder/Proximity/Tacho transduction → Frequency/Period → RPM → Direction/Resolution → Installation & Interface error`

## Core equations

- `ω = 2πn/60`
- `n = 60f/N_eff`
- `n = 60m/(N_eff·Δt)`
- `n = 60/(N_eff·T_c)`
- Gear tooth: `n = 60f/Z`
- DC tachogenerator: `V_t ≈ K_t·n`

## Core distinctions

- PPR/CPR catalog definition ≠ controller effective count/rev in every case
- Incremental encoder ≠ Absolute encoder
- A/B quadrature direction ≠ Z/index reference
- Fixed-window count ≠ Period/reciprocal measurement
- Inductive proximity ≠ Variable-reluctance magnetic pickup
- Tachogenerator ≠ 모든 digital tachometer
- Resolution increase ≠ unlimited maximum speed

## Ownership boundary

다음 상세내용은 기존 Topic이 소유한다.

- LVDT/RVDT displacement/angle transformer:
  `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error`
- Resistive/capacitive/inductive transduction 일반론:
  `passive_sensor_resistive_capacitive_inductive_transduction`
- Robot sensor fusion/digital twin application:
  `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`
- Accuracy/precision/calibration metrology 일반론:
  `calibration_error_accuracy_precision`
- Hazardous-area certification:
  `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
- Network-wide time synchronization/determinism:
  `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience`

## Grading direction

고득점 답안은 encoder, proximity, tachometer의 장단점만 나열하지 않는다.

회전→pulse/voltage 변환원리를 설명하고 N_eff/PPR 정의를 확인한 다음 speed equation을 적용해야 한다. 이어 low/high-speed resolution, maximum input/output frequency, direction/position requirement, air gap/runout/misalignment와 electrical interface를 선정·오차관리로 연결한다.

제품별 PPR, maximum RPM, sensing distance와 tachogenerator K_t 수치를 일반공식처럼 암기하지 않는다.
