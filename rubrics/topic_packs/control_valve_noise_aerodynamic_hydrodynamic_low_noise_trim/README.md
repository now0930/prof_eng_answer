# 제어밸브의 공력·수력 소음, 소음 예측 및 저소음 트림

## Topic ID

`control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`

## Question type

Primary: `PRINCIPLE_INTERPRETATION`

Supported secondary: `CALC_DESIGN`

Supported tertiary: `COMPARE_SELECTION`

## 핵심 범위

- Process-flow noise와 accessory noise 구분
- Source·path·receiver hierarchy
- Sound power level과 sound pressure level
- dB logarithmic addition
- Overall spectrum, octave band와 dBA
- Aerodynamic turbulent jet·expansion·shock noise
- Hydrodynamic turbulence·cavitation·flashing noise
- Topic 7 gas-sizing handoff
- Topic 8 liquid-regime handoff
- Internal acoustic power와 pipe transmission loss
- External SPL과 observation condition
- Multi-hole·multi-path·multi-stage low-noise trim
- Diffuser·silencer·insulation·enclosure
- Capacity·rangeability·plugging·maintenance tradeoff
- Operating-case matrix와 field verification

## Logic Check 정책

- Fact Anchor: 38
- Fatal misconception: 21
- Major conditional claim: 9
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Gas capacity, choked regime, xT·xTP·Y: Topic 7
- Cavitation·flashing·liquid-choked classification: Topic 8
- Balanced·unbalanced trim 구조: Topic 10
- Positioner·I/P·booster accessory 구조: Topic 11
- Severe-service material·hardfacing: Topic 14
- 전체 valve-package workflow: Topic 16

## Source

- `docs/topic_sheets/control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim.md`
- Control Valve Handbook aerodynamic-noise, hydrodynamic-noise and noise-abatement sections
- Control Valve Primer valve-noise sections
- Topic 7 and Topic 8 source packs
- `gemini_script/20260804_topic09_noise_requirements.md`

Source JSON authored. Generated-bank build and focused regression are separate stages.
