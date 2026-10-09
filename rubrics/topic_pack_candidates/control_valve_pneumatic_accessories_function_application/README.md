# 제어밸브 공압 부속기기의 기능과 적용

## Problem Unit

> 제어밸브 공압 구동계에 사용하는 Filter Regulator, Volume Booster, Lock-up Relay,
> Quick Exhaust, Volume Tank 및 Solenoid Valve의 기능을 설명하고, 유량 증대·압력 유지·
> 급속 배기 기능의 차이와 선정·적용 시 주의사항을 설명하시오.

- 근거: 기존 Topic Pack의 anchor로부터 구성한 지식원천 기반 예상문제.
- 기출·출제빈도는 확인하지 않았다.
- Question type: `PRINCIPLE_INTERPRETATION` / Difficulty: `FIELD_APPLICATION`.
- 현재 상태: managed draft, `human_review_required`; runtime/generated에는 미반영.

## 답안 중심

1. Instrument air의 conditioning부터 pilot, actuator chamber, hold/switching, exhaust까지
   공압 에너지 경로를 그린다.
2. 각 accessory의 입력·출력 및 주기능을 구분한다.
3. Booster가 flow capacity를 높이는 것, lock-up이 설정 조건에서 압력을 hold하는 것,
   quick exhaust가 chamber를 local vent하는 것을 비교한다.
4. Supply quality/pressure, actuator volume, tubing·fittings, leakage, load와 required
   response를 기능·선정 판단에 연결한다.
5. 실제 fail action은 solenoid port/energization, actuator spring, 전체 schematic과
   process safety requirement로 검증해야 함을 밝힌다.

## Ownership

- Traditional positioner feedback/I/P principle: `control_valve_positioner_ip_converter_booster_accessories_calibration`.
- Booster bypass·hunting·dynamic tuning: `control_valve_deadband_stiction_response_time_positioner_dynamic_performance`.
- Actuator thrust·spring/bench-set sizing: `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`.
- Post-maintenance calibration/test/troubleshooting/return-to-service: `control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing`.
- Split-range process architecture: `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`.
- Solenoid SIS/ESD, safe state, PST/proof-test and SIL credit: `final_control_element_sil_sis_esd_valve_partial_stroke_test`.
- Package selection, procurement, FAT/SAT and commissioning acceptance: `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`.

## Draft note

Fact Anchor의 기술 근거는 기존 `control_valve_positioner_ip_converter_booster_accessories_calibration`
source에서 이관 후보로 추적했다. 같은 지식을 기존 Pack에서 실제로 제거/이관하기 전까지 이
신규 Pack을 promote하지 않는다. source 문서 판본·페이지·도식은 아직 별도 검증되지 않았다.
