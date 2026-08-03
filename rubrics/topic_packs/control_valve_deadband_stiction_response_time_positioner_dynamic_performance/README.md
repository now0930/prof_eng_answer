# 제어밸브의 데드밴드·스틱션·응답시간 및 포지셔너 동특성

## Topic ID

`control_valve_deadband_stiction_response_time_positioner_dynamic_performance`

## Question type

`DIAGNOSIS_ACTION`

보조 문제 형식은 `PRINCIPLE_INTERPRETATION`이다.

## 핵심 범위

- Final Control Element와 공정변동성
- Deadband, Backlash와 Hysteresis
- Static friction, Stiction과 Stick-Slip
- PV cycling과 limit cycle
- Dead time과 Dynamic time
- Small-step, Large-step와 Reversal test
- Step sensitivity
- Positioner feedback와 gain trade-off
- Pneumatic supply, tubing과 relay capacity
- Volume booster와 hunting
- 개선 전후 검증

## 경계

- Actuator thrust, unbalance force와 fail-safe spring sizing은 Topic 1이다.
- Inherent·Installed와 Linear·Equal Percentage·Quick Opening은 Topic 2이다.
- I/P converter, split range와 detailed bench calibration은 별도 Positioner Topic이다.
- Valve signature와 predictive maintenance는 별도 Diagnostics Topic이다.
- Valve authority, rangeability와 quantitative installed gain은 별도 Topic이다.
- Cv·Kv와 liquid/gas sizing은 별도 Sizing Topic이다.

## Logic Check 정책

- Fatal misconception: 14개
- Major conditional claim: 5개
- Deterministic verdict: disabled
- LLM semantic profile: enabled
- Direct score application: disabled
- Direct D/E effect: none

## Source

- `gemini_script/20260803_topic03_deadband_stiction_response_positioner_requirements.md`
- `docs/topic_sheets/control_valve_deadband_stiction_response_time_positioner_dynamic_performance.md`
- Valve Handbook Chapter 2 summary
- Control-valve dynamic performance and positioner application guidance

## 작성 상태

Source JSON authored and source-level validation pending generated-bank build.
