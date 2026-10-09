# 제어밸브 공압 부속기기의 기능과 적용

## 1. Topic metadata

- Topic ID: `control_valve_pneumatic_accessories_function_application`
- Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `HIGH`
- 상태: 초안. 사람의 기술 검토 전이며, 과거 기출 확인도 하지 않음.

## 2. Problem Unit / 근거 유형

### 대표 예상 문제

> **제어밸브 공압 구동계에 사용하는 Filter Regulator, Volume Booster, Lock-up Relay,
> Quick Exhaust, Volume Tank 및 Solenoid Valve의 기능을 설명하고, 유량 증대·압력 유지·
> 급속 배기 기능의 차이와 선정·적용 시 주의사항을 설명하시오.**

- 근거 유형: 기존 Topic Pack의 지식 원천을 바탕으로 한 예상문제 구성.
- 기출 회차·빈도·공식 출제 분류는 확인하지 않았으며 주장하지 않는다.
- 응집 근거: 각 부품이 pneumatic supply/output/actuator chamber의 conditioning,
  fill/vent, holding/switching 기능을 담당하며, 문제는 공압 에너지 경로 안에서 기능과
  구성상 trade-off를 비교한다.
- 범위 제한: 이 Pack은 accessory의 기능·공압 경로·일반 적용조건을 다룬다. 포지셔너의
  내부 feedback 원리, detailed zero/span calibration, fail-safe spring sizing, SIS proof-test
  credit은 소유하지 않는다.

## 3. Scope and ownership

### 포함

- Filter Regulator: instrument-air conditioning과 downstream pressure regulation.
- Volume Booster: pilot pressure를 추종하는 relay/flow-capacity function; actuator fill/vent
  capacity와 stroke response의 관계.
- Lock-up Relay: 지정된 조건에서 chamber pressure를 hold할 수 있는 기능과 package
  dependency.
- Quick Exhaust: actuator chamber의 local rapid vent와 booster와의 기능 차이.
- Volume Tank: pneumatic energy storage와 capacity/response trade-off.
- Solenoid Valve: electrical command에 따른 pneumatic path switching의 일반 기능.
- Accessory flow path, supply quality, actuator volume, tubing/fitting, leakage 및 failure
  state가 기능에 미치는 영향.

### 소유권 경계

- 전통 positioner/I/P 내부 구조 및 travel feedback: `control_valve_positioner_ip_converter_booster_accessories_calibration`.
- Booster bypass, sensitivity, hunting 및 dynamic tuning: `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`.
- Actuator thrust, spring force, bench-set range 및 fail-safe sizing: `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`.
- SIF/ESD solenoid architecture, safe state, PST/proof test, SIL/PFDavg/PFH credit: `final_control_element_sil_sis_esd_valve_partial_stroke_test`.
- Package accessory selection, datasheet, vendor bid, FAT/SAT/commissioning acceptance: `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`.
- Positioner 교정 후 maintenance test·return-to-service, field failure diagnosis: `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing`.
- Process-level split-range control and transition: `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`.

## 4. Demand-to-knowledge coverage

| 요구 축 | 필요한 지식·답안 근거 | 후보 Fact Anchor ID (초안) | outline 위치 |
|---|---|---|---|
| Pneumatic energy path | Supply conditioning에서 accessory, actuator chamber, vent까지의 path 구분 | `pneumatic_accessory_energy_path` | 1 |
| Accessory별 기능 | filter/regulate, pressure-following flow boost, conditional hold, local vent, stored air, electrical switching 구분 | `pneumatic_accessory_filter_regulator_conditioning`, `pneumatic_accessory_volume_booster_flow_capacity`, `pneumatic_accessory_lockup_conditional_holding`, `pneumatic_accessory_quick_exhaust_vent`, `pneumatic_accessory_volume_tank_storage_tradeoff`, `pneumatic_accessory_solenoid_path_switching` | 2–3 |
| 핵심 기능 비교 | Flow-capacity increase ≠ steady pressure amplification; hold ≠ fail-close; rapid exhaust ≠ booster; solenoid switching ≠ final fail action | `pneumatic_accessory_volume_booster_flow_capacity`, `pneumatic_accessory_lockup_conditional_holding`, `pneumatic_accessory_quick_exhaust_vent`, `pneumatic_accessory_solenoid_path_switching` | 3–4 |
| 선정·응답조건 | Supply pressure/quality, actuator volume, tubing length/diameter, fittings, load, required response와 stability | `pneumatic_accessory_supply_capacity_conditions`, `pneumatic_accessory_volume_tank_storage_tradeoff` | 4 |
| Failure·시험 경계 | Loss-of-air/power/signals 및 package-specific response를 검증하되, safe-state/SIL credit은 별도 safety owner로 이관 | `pneumatic_accessory_fail_action_configuration_boundary` | 5 |

아래 JSON Pack의 ID는 이 초안에 새로 발급한 고유 ID다. 기존 Positioner Pack의 원 anchor를
참조·재구성했다는 provenance는 각 `source_basis`와 revision note에 남겼다. 이는 원 Pack에서
소유권을 이전하거나 기존 anchor를 삭제했다는 뜻이 아니며, 검토·승인 전까지 기존 라우팅과
채점 기준은 그대로 유지한다.

## 5. Recommended answer outline

1. Supply-air/accessory/actuator chamber/vent의 pneumatic path를 개략화한다.
2. Accessory별 입력·출력·기능을 구분한다.
3. Booster와 quick exhaust의 fill/vent capacity, lock-up의 conditional holding 기능을 비교한다.
4. Volume tank, filter regulator, tubing 및 actuator volume의 selection/response trade-off를 제시한다.
5. Solenoid switching과 mechanical/spring fail action을 구별하고 loss-of-utility condition은 actual package diagram으로 검증한다고 맺는다.

## 6. Fatal / warn / false-positive guidance

### 잠재적 핵심 오개념 (기존 source rule에서 옮길 후보)

- Volume booster는 steady-state pressure를 임의 비율로 증폭한다고 단정.
- Quick exhaust valve와 volume booster가 동일 기능이라고 설명.
- Lock-up relay 작동만으로 모든 조건에서 fail-close가 보장된다고 단정.
- Solenoid의 energized/de-energized 상태만으로 실제 valve fail action이 결정된다고 단정.
- Volume tank는 dynamic response나 usable stored-air capacity에 영향을 주지 않는다고 설명.
- Filter regulator가 공급압을 상류 supply보다 높인다고 설명.

### 조건부 주의

- Booster 성능·bypass setting은 exact model, supply, actuator volume, tubing, load와 stability에 의존한다.
- Lock-up 동작 및 보존압은 device 설정과 전체 pneumatic schematic에 의존한다.
- Volume tank의 usable capacity는 initial/minimum pressure, actuator volume, leakage, temperature 및 required hold time에 의존한다.
- Solenoid porting/energization logic은 actual schematic, de-energized requirement 및 safety design basis로 판단한다.
- Accessory 누락·간략화만으로 오답/fatal 처리하지 않는다.

## 7. Provenance and limitations

초안 근거 후보:

- 기존 Pack `control_valve_positioner_ip_converter_booster_accessories_calibration`의 Fact Anchor와 Topic Sheet.
- 기존 Pack이 인용한 Control Valve Handbook의 positioner/I/P/booster/accessory sections 및 Control Valve Primer의 pneumatic accessory sections.
- 특정 판본·페이지·그림·WordPress source 위치는 아직 원문 대조하지 않았다. 그러므로 이 문서는 technical approval이 아니다.

## 8. Human review checklist

- [ ] accessory pneumatic path가 제조사 도식과 맞는가?
- [ ] pressure-following booster 설명이 기기별 variation을 과도하게 일반화하지 않는가?
- [ ] lock-up/quick exhaust/volume tank의 응답·고장동작 설명이 적용조건을 명시하는가?
- [ ] solenoid와 SIS/ESD ownership이 분명한가?
- [ ] 모든 요구가 고유 Fact Anchor, outline 및 source location에 연결됐는가?
- [ ] Router alias와 기존 Positioner/Topic 3/Topic 15/Topic 16 경계가 검사됐는가?
