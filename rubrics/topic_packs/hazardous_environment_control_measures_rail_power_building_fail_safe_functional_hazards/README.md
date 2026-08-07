# 철도·발전·건축 등 비폭발 위험환경의 Fail-Safe 제어요소, Safe State 및 검증

## Topic ID

`hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards`

## Official criterion

- `IC-2027-W-4-2`
- 가스, 정유, 철도, 발전, 건축 등 위험 환경에서 고려해야 할 제어요소 및 대책
- 본 Topic은 기존 방폭 Topic이 남긴 **철도·발전·건축 등 비폭발 위험환경 residual scope**를 직접 소유한다.

## Classification

- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `CORE_MUST_PREPARE`
- Historical frequency: 근거가 없어 사용하지 않음

## Core answer flow

1. 위험환경과 hazard·initiating event를 정의한다.
2. Consequence를 기준으로 required safe state를 정의한다.
3. 전원·통신·센서·제어논리·최종요소의 failure mode를 연결한다.
4. Rail·power generation·building 환경별 제어요소와 대책을 구분한다.
5. Cause-and-Effect와 failure/loss scenario로 실제 safe response를 검증한다.
6. Bypass·MOC·functional/proof test·revalidation을 lifecycle로 연결한다.
7. 기존설비 retrofit에서는 risk·cost·downtime·legacy interface를 함께 고려한다.

## Core facts

- Fail-safe는 모든 출력을 OFF하는 것과 동일하지 않다.
- Required safe state는 hazard와 운전상태에 따라 달라진다.
- 전원상실에서는 필요한 안전기능의 유지시간과 잔류에너지를 함께 고려한다.
- 통신상실에서는 timeout·watchdog·status로 stale data를 식별하고 safe response를 정한다.
- Redundancy는 common cause failure를 자동 제거하지 않는다.
- Final element fail action은 process/hazard별로 정한다.
- Rail은 movement·speed·position·authority uncertainty를 다룬다.
- Power generation은 주에너지원 차단과 필요한 cooling·lubrication 등 auxiliary 유지의 sequence를 다룬다.
- Building fire/smoke control은 scenario에 따라 fan·damper 목표상태가 달라질 수 있다.
- Normal I/O check와 failure/loss scenario verification은 다르다.

## Application-specific scope

### Rail / Railway

속도·위치·진로권한·통신 신뢰성이 상실될 때 기존 명령을 무기한 유지하지 않는다. 적용 시스템의 안전원칙에 따라 movement inhibition, speed restriction, controlled braking 또는 local protected mode를 검토한다.

### Power generation

고온·고압 유체, 회전체, 연료와 전기에너지의 차단뿐 아니라 coast-down·잔열·윤활·냉각·purge 등 안전정지 완료에 필요한 auxiliary function의 유지시간을 함께 검토한다.

### Building / Facility

화재·연기·피난·HVAC·댐퍼·승강기·비상전원을 시나리오로 연결한다. 팬·댐퍼의 safe state는 화재구획과 smoke-control cause-and-effect에 따라 달라질 수 있다.

## Ownership boundary

- `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
  - Zone/EPL/Ex marking, 방폭방식, intrinsic-safety entity/barrier/wiring 상세
- `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`
  - EMC/EMI·온습도·진동 qualification 시험계획과 acceptance evidence 상세
- `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
  - power architecture, grounding, shielding, UPS 일반설계 깊이
- `sis_sil_safety_software_independence_systematic_failure_verification_validation`
  - SIL/SIS lifecycle·독립성·systematic failure 검증 깊이
- `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`
  - sequence/interlock/permissive/trip 상태전이 논리 자체의 상세

본 Topic은 위 영역을 중복 상세화하지 않고 **비폭발 위험환경의 hazard-specific safe state와 적용 제어대책**에 집중한다.

## Verification and retrofit

- Loss of power, loss of communication, sensor failure, final element stuck, bypass, restart scenario를 검증한다.
- Cause-and-Effect, FAT/SAT, functional test 또는 동등한 evidence를 사용한다.
- 변경 후에는 MOC와 필요한 revalidation을 수행한다.
- Legacy retrofit은 현재 fail action·logic·wiring·power·shutdown window와 cost를 확인하고 위험도 높은 gap부터 단계화한다.

## Standards orientation

특정 표준 판년·시험레벨·숫자를 모든 산업에 공통 정답으로 사용하지 않는다. Applicable law, sector code/standard, owner requirement와 design basis를 확인하고 최신 유효 요구사항에 trace한다.
