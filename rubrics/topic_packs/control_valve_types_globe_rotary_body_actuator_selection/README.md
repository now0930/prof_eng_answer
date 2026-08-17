# 제어밸브 본체 형식과 액추에이터 종류 및 선정

## Topic ID

`control_valve_types_globe_rotary_body_actuator_selection`

## Question type

`COMPARE_SELECTION`

보조 문제 형식은 `PRINCIPLE_INTERPRETATION`이다.

## 핵심 범위

- Sliding-stem과 rotary valve
- Single-port, angle, guided, cage-guided, double-port와 three-way valve
- Sanitary valve
- Butterfly, segmented·V-notch ball, eccentric plug와 full-port ball
- End connection, bonnet, plug guiding과 reduced-capacity trim
- Spring-diaphragm, piston, rack-and-pinion, electric와 manual actuator
- Body motion과 actuator force·torque matching
- Fail-safe, power source, installation, maintenance와 lifecycle selection

## 경계

- 정량 unbalance force와 actuator sizing은 Topic 1이다.
- Valve characteristic는 Topic 2이다.
- Deadband·stiction·response time은 Topic 3이다.
- Authority·rangeability는 Topic 5이다.
- Cv·Kv sizing은 Topic 6이다.
- Balanced·unbalanced trim 상세는 Topic 10이다.
- Positioner·I/P·booster는 Topic 11이다.
- Seat leakage와 fugitive emissions는 Topic 13이다.
- Severe service 상세는 Topic 14이다.
- 전체 valve package workflow는 Topic 16이다.

## Historical alias handling

과거 자료에서 다음 명칭이 나타나면 이 Topic으로 라우팅한다.

- `control_valve_body_trim_selection`
- `control_valve_actuator_types_selection`

현재 Source Topic Pack에는 위 명칭의 별도 Legacy Topic을 유지하지 않는다.
본 Topic이 제어밸브 본체 형식과 actuator 종류·비교·선정의 주 소유권을 가진다.

## Logic Check 정책

- Fact Anchor: 28개
- Fatal misconception: 16개
- Major conditional claim: 6개
- Deterministic verdict: disabled
- LLM semantic profile: enabled
- Direct score application: disabled
- Direct D/E effect: none

## Source

- `gemini_script/20260803_topic04_valve_body_actuator_selection_requirements.md`
- `docs/topic_sheets/control_valve_types_globe_rotary_body_actuator_selection.md`
- Control Valve Handbook Chapter 3

## 작성 상태

Source JSON authored and source-level validation pending generated-bank build.
