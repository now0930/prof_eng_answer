# 회전속도 계측의 원리, 선정 및 오차 — Encoder·Proximity·Tachometer

## 0. Topic identity

- Topic ID: `speed_rotation_measurement_encoder_proximity_tachometer_selection_error`
- Official criterion: `IC-2027-W-2-1`
- Official scope label: 속도·회전수 계측
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Historical frequency: 근거가 없어 사용하지 않음
- Grading mode: LLM semantic review 중심
- Deterministic fatal keyword rule: 사용하지 않음

## 1. 출제 의도

이 Topic은 encoder·proximity·tachometer의 이름을 나열하는 문제가 아니다.

핵심 흐름은 다음과 같다.

`회전 → pulse/voltage 변환 → frequency/time 측정 → RPM 계산 → direction/resolution 선정 → mounting/electrical error 관리`

## 2. 회전속도와 기본 관계

회전속도 n[rpm]과 각속도 ω[rad/s]는 다음 관계를 갖는다.

`ω = 2πn / 60`

Pulse 방식에서는 **1회전당 controller가 실제로 세는 유효 count 수 N_eff**가 중요하다.

Pulse frequency가 f[Hz]이면,

`n = 60f / N_eff`

고정 측정창 Δt 동안 m count를 세면,

`n = 60m / (N_eff·Δt)`

연속 count 사이의 period가 T_c이면,

`n = 60 / (N_eff·T_c)`

N_eff는 단순 catalog PPR과 항상 동일하다고 가정하지 않는다. PPR/CPR 정의, rising/falling edge, quadrature x1/x2/x4 decoding을 확인한다.

## 3. Incremental encoder

Incremental encoder는 shaft 회전에 따라 반복 pulse train을 만든다.

- Optical type: code disk/scale와 photodetector
- Magnetic type: magnetic pole/pattern과 magnetic sensor

Pulse count는 relative position, pulse frequency는 speed에 사용한다.

전원 제거 후 controller의 누적 count가 사라지면 incremental encoder 자체만으로 absolute multi-turn position을 복원하지 못한다.

### 3.1 A/B quadrature

A와 B는 약 90 electrical degree 위상차를 갖는다.

어느 channel이 lead/lag하는지 비교하여 rotation direction을 판별한다.

- x1: 한 기준 edge만 count
- x2: 두 edge 또는 두 channel 활용
- x4: A/B의 rising/falling edge 모두 활용

정확한 decoding 의미는 controller 문서를 확인한다.

### 3.2 Z / Index

Z 또는 index는 일반적으로 1 revolution reference pulse다.

주 용도:

- Homing
- Revolution reference
- Pulse count verification

Z 하나를 multi-turn absolute position과 동일시하지 않는다.

## 4. Absolute encoder

Absolute encoder는 각 angular position에 대응하는 unique digital word를 출력한다.

Single-turn 또는 multi-turn 정보를 제공할 수 있으며, speed는 successive position sample의 차이를 sample interval로 나누어 계산할 수 있다.

Speed feedback에는 다음을 함께 본다.

- Position resolution(bits)
- Update rate
- Communication latency
- Wrap-around handling
- Maximum shaft speed

## 5. Resolution: PPR, CPR, Effective Count

Encoder resolution은 제조사에 따라 PPR, CPR 또는 bit로 표기된다.

같은 PPR이라도 controller가 quadrature edge를 몇 배로 count하는지에 따라 유효 count/rev가 달라질 수 있다.

따라서 답안에서는 다음을 구분한다.

1. Encoder catalog resolution
2. Output cycle/pulse definition
3. Controller decode mode
4. Effective counts per revolution, N_eff

고해상도는 저속 resolution에 유리할 수 있으나 같은 RPM에서 pulse frequency를 증가시킨다.

`f = n·N_eff / 60`

따라서 encoder output frequency와 PLC/high-speed counter input frequency의 허용범위를 확인한다.

## 6. 저속·고속 측정방식

### 6.1 Fixed counting window

일정 시간창에서 pulse 수를 세는 방식이다.

장점:
- 구현이 단순
- 고속에서 많은 count를 얻기 쉬움

문제:
- 저속에서는 count 수가 작아져 1 count가 만드는 RPM step이 커짐
- update time과 resolution 사이 trade-off

### 6.2 Period / Reciprocal measurement

pulse 간 시간을 timer로 측정한다.

장점:
- 저속에서 적은 pulse로도 속도 추정 가능

문제:
- timer resolution
- edge jitter
- signal noise
- 매우 고속에서 짧은 period 측정한계

## 7. Proximity / Gear-tooth speed sensing

### 7.1 Inductive proximity

Inductive proximity sensor는 sensing face의 교번 electromagnetic field에 metal target이 접근할 때 eddy-current loss 또는 oscillator 상태가 변하는 원리를 사용한다.

Gear tooth, bolt, flag 등 반복 target을 pulse로 검출할 수 있다.

회전당 Z개의 동일한 유효 event가 있고 1 event당 1 pulse를 얻으면,

`n = 60f / Z`

Missing tooth, unequal pattern 또는 multiple-edge counting이 있으면 Z 대신 실제 effective events/rev를 사용한다.

### 7.2 Variable-reluctance magnetic pickup

Ferromagnetic tooth가 pole piece를 지나가면 magnetic reluctance와 flux가 변하고 Faraday induction에 의해 voltage pulse가 발생한다.

특징:

- Passive pickup
- 별도 excitation이 필요 없는 구조 가능
- Speed가 높을수록 signal amplitude가 커지는 경향
- Air gap 증가 시 signal이 약해질 수 있음
- 매우 낮은 speed 또는 zero speed 검출에는 제약 가능

Inductive proximity switch와 VR pickup의 동작원리를 동일시하지 않는다.

## 8. Proximity 설치오차

Proximity speed sensing은 다음에 영향을 받는다.

- Air gap
- Target material
- Target size/thickness
- Tooth geometry
- Shaft runout/eccentricity
- Mounting vibration
- Sensor switching frequency
- Cable/noise
- Target damage 또는 missing tooth

Nominal sensing distance만 보지 말고 assured operating/release distance와 실제 target 조건을 확인한다.

## 9. Tachometer / Tachogenerator

### 9.1 DC tachogenerator

Permanent-magnet DC tachogenerator는 회전에 의해 speed-proportional DC voltage를 만든다.

정상범위에서 근사적으로,

`V_t ≈ K_t·n`

여기서 K_t는 tachogenerator sensitivity다.

회전방향이 반전되면 일반적인 DC tacho는 output polarity도 반전될 수 있다.

대표 오차:

- Linearity
- Temperature coefficient
- Brush/commutator ripple
- Loading
- Bearing/coupling 상태
- Calibration drift

K_t와 허용오차 수치를 모든 제품의 공통값으로 암기하지 않는다.

### 9.2 Digital tachometer

Digital tachometer는 별도의 pulse sensor를 입력으로 사용할 수 있다.

- Encoder pulse
- Proximity pulse
- Optical target pulse

따라서 tachometer라는 명칭만으로 transducer 원리가 tachogenerator라고 단정하지 않는다.

## 10. 선정 기준

### 10.1 Speed range

- Starting/creeping speed
- Normal speed
- Maximum speed
- Overspeed
- Acceleration
- Required response time

저속에서는 pulse scarcity와 VR amplitude를, 고속에서는 frequency limit와 mechanical speed limit를 확인한다.

### 10.2 측정기능

- Speed only
- Direction
- Relative position
- Absolute position
- Homing/index
- Overspeed detection

Speed만 필요하면 one-channel pickup도 가능하지만 direction/position이 필요하면 quadrature 또는 absolute encoder가 유리할 수 있다.

### 10.3 Resolution and bandwidth

필요한 angular resolution과 speed resolution을 정하고 controller update period와 control bandwidth를 함께 본다.

해상도만 높이고 receiver frequency limit를 초과하지 않는다.

### 10.4 Mechanical installation

- Shaft diameter
- Solid/hollow shaft
- Coupling
- Radial/axial load
- Runout
- Misalignment
- Torsional vibration
- Maximum mechanical RPM
- IP/environment

### 10.5 Electrical interface

- Supply voltage
- HTL/TTL/RS-422 등 output
- Sink/source interface
- Differential/single-ended
- PLC high-speed counter
- Cable length
- Shield/ground
- Receiver threshold
- Isolation

## 11. 대표 오차와 진단

### 11.1 Count / Timer error

- Fixed-window quantization
- Timer resolution
- Clock accuracy
- Edge jitter
- Missed/double pulse

### 11.2 Encoder signal error

- Duty/symmetry
- A/B phase error
- Index alignment
- Frequency limit exceed
- Electrical noise

### 11.3 Mechanical error

- Coupling slip
- Loose mounting
- Runout/eccentricity
- Shaft vibration
- Misalignment
- Excess shaft load

### 11.4 Proximity error

- Air-gap drift
- Tooth geometry
- Target damage
- Sensor contamination
- Switching-frequency limit

### 11.5 Tachogenerator error

- Linearity
- Temperature
- Brush/commutator ripple
- Loading
- Calibration drift

## 12. 기존설비 적용 시 실무 고려

Retrofit에서는 새 sensor의 resolution만 비교하지 않는다.

- 기존 shaft/coupling modification
- Guard와 설치공간
- Sensor bracket 강성
- Air-gap adjustment
- 기존 PLC high-speed input
- Input voltage/interface
- Cable 재사용 가능성
- Shutdown 시간
- Spare
- Calibration/diagnostic equipment
- Maintenance skill
- Lifecycle cost

법규·기계적 안전·위험장소 요구사항은 비용만으로 무시할 수 없다. 그 외 개선은 risk와 shutdown, 기존 interface, lifecycle benefit을 고려해 단계적으로 적용한다.

## 13. 근거와 범위

대표 기술근거는 다음 원리와 일치한다.

- Dynapar: incremental encoder의 PPR/resolution, A/B quadrature direction, Z/index reference, maximum frequency와 RPM/PPR 관계
- Pepperl+Fuchs: inductive proximity의 target/air-gap 의존성과 speed sensing 적용
- Baumer / Johannes Hübner Giessen: permanent-magnet DC tachogenerator의 speed-proportional voltage 원리

제품별 PPR, sensing distance, maximum RPM, K_t와 정확도 수치는 일반 법칙으로 사용하지 않는다.

## 14. Grading boundary

이 Topic의 핵심 연결은 다음이다.

1. RPM·angular velocity·pulse frequency 관계를 설명한다.
2. Encoder incremental/absolute와 quadrature/index를 구분한다.
3. Proximity/gear-tooth/VR pickup의 pulse 발생원리를 설명한다.
4. Tachogenerator의 speed-proportional voltage 원리를 설명한다.
5. Low/high speed, resolution, frequency limit와 mounting/electrical error를 연결한다.

다음 기존 Topic과 ownership을 분리한다.

- `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error`
- `passive_sensor_resistive_capacitive_inductive_transduction`
- `physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control`
- `calibration_error_accuracy_precision`
- `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
- `industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience`
