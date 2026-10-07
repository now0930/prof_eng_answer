# 최종제어요소의 SIL·SIS·ESD 밸브와 부분행정시험

## Topic ID

`final_control_element_sil_sis_esd_valve_partial_stroke_test`

## Question type

Primary: `IMPLEMENTATION_EVALUATION`

Supported secondary: `PRINCIPLE_INTERPRETATION`

Supported tertiary: `CALC_DESIGN`, `PROCEDURE`

## 핵심 범위

- SIF에서 Final Element subsystem의 역할과 boundary
- Safe State, fail action와 de-energize-to-trip
- ESD valve·actuator·solenoid·utility architecture
- Dangerous·safe·spurious·hidden failure mode
- PFDavg·PFH와 subsystem risk budget
- Diagnostic Coverage와 Proof Test Coverage
- Partial Stroke Test와 Full Stroke Proof Test
- Response time과 Process Safety Time
- Bypass·override·impairment·restoration
- Redundancy, common cause와 shared utility
- FMEDA·acceptance evidence·proof-test records
- Maintenance, MOC와 lifecycle revalidation

## 문항별 평가 범위

10개 예상문항은 final-element functional-safety라는 공통 소유범위의 하위 문제다. Pattern 1/4는 boundary·architecture, Pattern 2/7은 PST/proof-test, Pattern 3은 reliability calculation, Pattern 5/8은 safe action/response time, Pattern 6/9는 failure/impairment, Pattern 10은 lifecycle evidence를 묻는다. `model_answer.json`의 패턴별 Anchor와 점수 적용 표시를 따르며, 한 답안에 전체 48 Anchor를 공통 요구하지 않는다.

## Logic Check 정책

- Fact Anchor: 48
- Fatal misconception: 24
- Major conditional claim: 12
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Actuator force·spring sizing: Topic 1
- Deadband·stiction·generic response: Topic 3
- Valve body·actuator taxonomy: Topic 4
- Cavitation·flashing: Topic 8
- Balanced trim·seal mechanics: Topic 10
- Positioner·I/P·booster calibration: Topic 11
- Valve signature·predictive diagnostics: Topic 12
- Seat leakage·packing·emissions: Topic 13
- Severe-service mechanical suitability: Topic 14
- Complete package selection과 enterprise lifecycle: Topic 16

## Source

- `docs/topic_sheets/final_control_element_sil_sis_esd_valve_partial_stroke_test.md`
- Applicable IEC 61508·IEC 61511 concepts and project SRS
- Control Valve Handbook final-control-element and shutdown-valve sections
- Vendor FMEDA, proof-test and PST manuals subject to application assumptions
- Adjacent Topic 1·3·4·8·10·11·12·13·14 source packs
- `gemini_script/20260806_topic15_final_element_sis_esd_pst_requirements.md`

Source JSON authored. Generated-bank build와 focused regression은 별도 단계에서 수행한다.
