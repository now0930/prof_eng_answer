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

- Non-choked liquid Cv·Kv와 Reynolds correction: Topic 6
- Gas·steam compressible choked sizing: Topic 7
- Hydrodynamic·aerodynamic noise prediction: Topic 9
- Balanced·unbalanced trim: Topic 10
- Hardfacing·severe-service material: Topic 14
- 전체 valve-package workflow: Topic 16

## Source

- `docs/topic_sheets/control_valve_cavitation_flashing_choked_flow_damage_prevention.md`
- Control Valve Handbook liquid sizing and cavitation/flashing sections
- Control Valve Primer cavitation and flashing sections
- `gemini_script/20260804_topic08_cavitation_flashing_requirements.md`

Source JSON authored. Generated-bank build and focused regression are separate stages.
