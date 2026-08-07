# 철도·발전·건축 등 비폭발 위험환경의 Fail-Safe 제어요소, Safe State 및 검증

## 0. Topic identity

- Topic ID: `hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards`
- Official criterion: `IC-2027-W-4-2`
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `CORE_MUST_PREPARE`
- Historical frequency: 근거가 없어 사용하지 않음
- Current criterion status before this Topic: `PARTIAL`

## 1. Authoring objective

기존 `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`은 가스·정유의 폭발위험 영역을 강하게 소유한다.

그러나 공식 criterion은 철도·발전·건축 등을 포함한 위험환경 전반의 제어요소와 대책을 요구한다.

따라서 본 Topic은 다음 residual scope를 직접 소유한다.

- 철도·발전·건축 등 비폭발 위험환경
- Required safe state와 fail-safe
- 전원·통신·센서·제어·최종제어요소 상실 시 대응
- Environmental hazard와 functional hazard의 구분
- Hazard identification → safe state → sensing/control/final element → verification
- Existing facility retrofit의 cost·downtime·legacy compatibility

## 2. 핵심 개념 — Hazard에서 Safe State까지

위험환경 제어설계는 장치목록보다 hazard scenario에서 시작한다.

`Hazard → Initiating event → Consequence → Required safe state → Detection → Logic → Final element → Verification`

Required safe state는 설비마다 다르다.

- 정지 또는 차단
- 감속 또는 controlled braking
- 격리와 residual energy 제거
- 일정 시간 cooling·lubrication·purge 유지
- Fire/smoke scenario에 맞는 fan·damper 위치
- Local protected mode 또는 제한운전

따라서 `Fail-safe = 무조건 모든 전원 OFF`로 정의하지 않는다.

## 3. Loss of Power

전원상실에서는 다음을 순서대로 판단한다.

1. 어떤 기능이 반드시 살아 있어야 하는가.
2. 얼마 동안 유지해야 하는가.
3. Backup power가 필요한가.
4. Backup이 고갈되면 최종 safe state가 무엇인가.
5. 전원 OFF 후 남는 압력·관성·열·공압·유압 등의 residual energy는 무엇인가.
6. 실제 shutdown sequence가 이를 만족하는지 어떻게 시험할 것인가.

UPS·battery·redundant power는 수단이며 safe state 자체가 아니다.

## 4. Loss of Communication

통신상실에서는 정상값과 stale/invalid data를 구분한다.

- timeout
- watchdog
- heartbeat
- quality/status
- local diagnostic

상위 SCADA나 network가 상실되어도 필요한 보호기능은 가능한 한 local control layer에서 유지한다.

Hold-last-value는 hazard와 허용시간이 명확할 때만 사용할 수 있다. 무기한 유지가 fail-safe인 것은 아니다.

## 5. Sensor, Logic, Final Element

### Sensor

- response time
- range·accuracy
- 환경적합성
- self-diagnostic
- plausibility
- testability
- 설치위치

### Redundancy

이중화는 single failure tolerance를 높일 수 있다.

그러나 common cause failure를 자동 제거하지 않는다.

- 공통전원
- 공통 cable route
- 동일 환경
- 동일 software
- 동일 sensing principle

필요하면 separation·diversity·independent path·diagnostics를 조합한다.

### Logic

- Permissive: 시작·전이 허용조건
- Interlock: 위험·부적절 동작 억제
- Trip: 위험조건에서 보호동작 수행
- Bypass/Override: 권한·시간제한·표시·보완대책·복구확인 필요

### Final element

Safe position은 hazard별로 정한다.

- valve fail-open / fail-close / fail-in-place
- brake apply / release
- damper position
- contactor trip
- motor coast / controlled stop

필요한 spring·accumulator·gravity·stored energy와 실제 position feedback까지 확인한다.

## 6. Rail / Railway hazardous environment

주요 hazard 축은 다음과 같다.

- 이동체와 충돌위험
- speed·position uncertainty
- movement authority uncertainty
- braking
- door/platform interface
- traction/electrical energy
- communication loss
- 사람 접근

위치·속도·진로권한 신뢰성이 상실되면 기존 명령을 무기한 유지하지 않는다.

적용 시스템의 안전원칙에 따라 다음을 검토한다.

- movement inhibition
- speed restriction
- controlled braking
- local protected mode

구체적인 rail signaling 규격의 단일 동작을 보편정답으로 강제하지 않는다.

## 7. Power-generation hazardous environment

주요 hazard 축은 다음과 같다.

- high-pressure / high-temperature fluid
- fuel
- rotating machinery
- electrical energy
- residual heat
- auxiliary systems

Trip의 목적은 단순 전체 OFF가 아니다.

주에너지원은 차단하되 안전정지 과정에서 다음 기능이 일정 시간 필요할 수 있다.

- cooling
- lubrication
- seal support
- purge
- coast-down support

따라서 main trip과 auxiliary power/shutdown sequence를 함께 설계·검증한다.

## 8. Building / Facility hazardous environment

주요 hazard 축은 다음과 같다.

- fire
- smoke
- egress
- HVAC
- damper
- elevator
- emergency power
- flooding
- occupancy

Fire/smoke control의 fan·damper 목표상태는 fire compartment와 smoke-control scenario에 따라 달라질 수 있다.

Cause-and-Effect에서 다음을 정의한다.

- detection input
- logic condition
- fan/damper/door/elevator command
- feedback
- alarm
- failure response
- reset/recovery

모든 HVAC를 단일 상태로 만드는 것을 보편 fail-safe로 보지 않는다.

## 9. Environmental hazard와 Functional hazard

Environmental hazard는 temperature, humidity, vibration, impact, dust, water, corrosion, EMI 등 외부 stress가 계측·제어기능을 약화시키는 축이다.

Functional hazard는 sensor failure, stale data, wrong logic, stuck final element, power/communication loss처럼 제어기능 자체의 실패가 위험상태를 만드는 축이다.

두 축은 서로 연결될 수 있지만 동일개념은 아니다.

환경 qualification 시험 깊이는 `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`이 소유한다.

## 10. Verification

정상운전 I/O check만으로 fail-safe를 검증하지 않는다.

대표 scenario:

- loss of power
- loss of communication
- sensor failure
- implausible sensor
- final element stuck
- bypass active
- restart after recovery

검증수단:

- Cause-and-Effect review
- FAT
- SAT
- functional test
- proof test
- simulated failure
- actual position/status feedback
- recovery verification

## 11. Lifecycle and MOC

운영 중 다음 evidence를 관리한다.

- functional/proof test
- bypass/override history
- alarm/trip history
- failure finding
- corrective action

Logic, setpoint, sensor, final element, network 또는 power path가 변경되면 MOC와 필요한 revalidation을 수행한다.

## 12. Legacy retrofit

기존설비에는 다음 제약이 있다.

- 기존 relay/PLC logic
- existing wiring
- current fail action
- power source
- spare availability
- shutdown window
- operating procedure
- modification cost

개선은 위험도가 높은 gap부터 단계화한다.

단기에는 alarm·diagnostic·bypass control·testability 개선이 가능할 수 있다.

중장기에는 final element, independent power/path, local protection과 control architecture를 개조할 수 있다.

Cost와 downtime을 줄이더라도 interim risk control과 최종 완료기준을 명확히 한다.

## 13. Ownership boundary

본 Topic의 IN:

- rail/railway hazardous operating environment
- power-generation hazardous operating environment
- building/facility hazardous operating environment
- required safe state
- fail-safe on power/control/communication loss
- environmental hazard versus functional hazard
- application-specific control measures
- failure-scenario verification
- legacy retrofit

본 Topic의 OUT:

- `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
  - Zone/EPL/Ex marking, intrinsic-safety entity/barrier/wiring 상세
- `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`
  - qualification test plan, severity, monitoring, acceptance evidence 상세
- `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
  - grounding/shielding/UPS 일반설계 상세
- `sis_sil_safety_software_independence_systematic_failure_verification_validation`
  - SIL/SIS lifecycle·systematic failure·independence 상세
- `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`
  - sequence/state transition 논리 자체의 상세

## 14. 기술사 답안 권장 흐름

1. 위험환경을 폭발·비폭발 hazard로 구분한다.
2. Hazard scenario와 required safe state를 정의한다.
3. 전원·통신·sensor·logic·final element의 failure response를 설명한다.
4. Rail·power generation·building 사례를 각각 연결한다.
5. Cause-and-Effect와 failure scenario verification을 제시한다.
6. Lifecycle MOC와 bypass 관리를 제시한다.
7. Legacy retrofit의 cost·downtime·compatibility를 개선방안에 포함한다.

## 15. Coverage gate

이 Topic source를 생성했다고 `IC-2027-W-4-2`를 즉시 COVERED로 승격하지 않는다.

Focused validation, release registration, generated rebuild, integration validation 및 ChatGPT semantic re-audit를 모두 통과한 뒤 coverage를 다시 판정한다.
