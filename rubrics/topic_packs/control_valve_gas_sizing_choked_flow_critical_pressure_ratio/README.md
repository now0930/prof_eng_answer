# 제어밸브의 가스·증기 사이징, 팽창계수 및 초크 유동

## Topic ID

`control_valve_gas_sizing_choked_flow_critical_pressure_ratio`

## Question type

Primary: `CALC_DESIGN`

Supported secondary: `PRINCIPLE_INTERPRETATION`

Supported tertiary: `COMPARE_SELECTION`

## 핵심 범위

- Standard·actual volumetric flow와 mass flow 구분
- Absolute pressure와 absolute temperature
- Pressure-drop ratio `x=(P1-P2)/P1`
- Gas property `M`, `Gg`, `rho1`, `gamma`, `Z1`
- `Fgamma`, `xT`, `FP`, `xTP`
- Expansion factor `Y`
- Subcritical·choked flow
- Required Cv와 rated trim capacity
- Selected-travel `xT/xTP` 반복 계산
- Minimum·normal·maximum 및 fail-open flow
- Steam phase와 Topic 9 aerodynamic-noise hand-off

## Logic Check 정책

- Fact Anchor: 34
- Fatal misconception: 19
- Major conditional claim: 8
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Non-choked liquid sizing과 Reynolds correction: Topic 6
- Liquid cavitation·flashing·liquid choked: Topic 8
- Aerodynamic noise와 low-noise trim: Topic 9
- Balanced·unbalanced trim: Topic 10
- Severe-service material: Topic 14
- 전체 valve package workflow: Topic 16

## Source

- `docs/topic_sheets/control_valve_gas_sizing_choked_flow_critical_pressure_ratio.md`
- Control Valve Handbook Chapter 5
- Control Valve Primer Chapter 5
- `gemini_script/20260804_topic07_gas_sizing_requirements.md`

Source JSON authored. Generated-bank build and focused regression are separate stages.
