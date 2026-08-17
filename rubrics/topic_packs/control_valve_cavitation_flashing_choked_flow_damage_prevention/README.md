# 제어밸브의 캐비테이션·플래싱·액체 초크 유동 및 손상 방지

## Topic ID

`control_valve_cavitation_flashing_choked_flow_damage_prevention`

## Question type

Primary: `PRINCIPLE_INTERPRETATION`

Supported secondary: `COMPARE_SELECTION`

Supported tertiary: `DIAGNOSIS_ACTION`

## 핵심 범위

- `P1 → Pvc → P2` liquid pressure profile
- Absolute pressure와 operating-temperature `Pv`
- Thermodynamic critical pressure `Pc`
- Liquid critical-pressure-ratio factor `FF`
- Pressure-recovery factor `FL`
- Piping geometry factor `FP`
- Combined recovery factor `FLP`
- Bare-valve·fitting-adjusted liquid choked limit
- Cavitation·flashing classification
- Choked·vapor formation·damage axis separation
- Cavitation prevention과 flashing mitigation
- Minimum·normal·maximum 및 startup·shutdown
- Vendor result와 hand calculation crosscheck

## Logic Check 정책

- Fact Anchor: 36
- Fatal misconception: 20
- Major conditional claim: 8
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Non-choked liquid Cv·Kv와 Reynolds correction: `control_valve_sizing_cv_kv_reynolds_liquid_selection`
- Gas·steam compressible choked sizing: `control_valve_gas_sizing_choked_flow_critical_pressure_ratio`
- Hydrodynamic·aerodynamic noise prediction: `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`
- Balanced·unbalanced trim 구조: `balanced_trim_unbalanced_trim_structure_sealing_applications`
- Hardfacing·severe-service material: `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`
- 전체 valve-package workflow: `control_valve_selection_process_pressure_temperature_flow_media_lifecycle`
- 손상된 trim의 분해점검·수리·교체 절차는 향후 Valve Maintenance 전문 Topic으로 hand-off할 계획이며, 현재는 active routing 대상으로 사용하지 않는다.

## 핵심 판정 가드

- 압력은 absolute basis로 통일하고 `P1 → Pvc → P2`를 operating-temperature `Pv`와 비교한다.
- `Pvc < Pv`이고 `P2 > Pv`이면 기포가 붕괴할 수 있어 cavitation 가능성이 있다.
- `Pvc < Pv`이고 `P2 ≤ Pv`이면 하류에서도 증기가 유지되어 flashing으로 분류한다.
- Choked flow 발생 여부와 cavitation·flashing 손상 정도는 같은 축으로 단정하지 않는다.
- Anti-cavitation trim은 staged pressure reduction으로 cavitation 위험을 낮출 수 있지만 지속 flashing 자체를 제거하는 일반 해법은 아니다.
- Minimum·normal·maximum뿐 아니라 startup·shutdown·upset case를 함께 확인한다.

## Source

- `docs/topic_sheets/control_valve_cavitation_flashing_choked_flow_damage_prevention.md`
- Control Valve Handbook liquid sizing and cavitation/flashing sections
- Control Valve Primer cavitation and flashing sections
- 적용 표준·제조사 sizing 식은 압력 기준, 단위, `FL`·`FP`·`FLP` 정의와 적용 판본을 교차검증한다.
- `gemini_script/20260804_topic08_cavitation_flashing_requirements.md`

Source JSON authored. Generated-bank build and focused regression are separate stages.
