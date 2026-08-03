# 제어밸브의 Authority·Rangeability·Installed Gain 및 공정 성능

## Topic ID

`control_valve_authority_rangeability_gain_installed_performance`

## Question type

Primary: `PRINCIPLE_INTERPRETATION`

Supported secondary: `CALC_DESIGN`

## 핵심 범위

- Valve Authority의 의미, 식과 system boundary
- Pressure-drop redistribution
- Low Authority와 installed characteristic distortion
- Oversizing, low normal travel와 local gain sensitivity
- Inherent gain과 installed gain
- Process gain과 loop gain
- Conditional equal-percentage gain compensation
- Rated와 installed rangeability
- Process turndown
- Minimum controllable flow
- Minimum·normal·maximum operating-point validation
- Installed flow와 gain curve 검증

## 경계

- Unbalanced force와 actuator sizing은 Topic 1이다.
- Characteristic 형상 비교는 Topic 2이다.
- Deadband·stiction·response time은 Topic 3이다.
- Valve body와 actuator 종류는 Topic 4이다.
- Cv·Kv와 liquid sizing은 Topic 6이다.
- Gas sizing은 Topic 7이다.
- Cavitation·flashing은 Topic 8이다.
- Balanced·unbalanced trim은 Topic 10이다.
- Positioner와 accessories는 Topic 11이다.
- 전체 valve package workflow는 Topic 16이다.

## 수식 경계

단순 직렬 배관계의 design-point Authority를 사용한다.

Pump curve, static head, bypass와 parallel branch가 있는 계통은
system boundary와 available pressure를 별도로 정의한다.

특정 Authority 숫자나 gain band를 모든 계통의 보편 규격으로 사용하지 않는다.

## Logic Check 정책

- Fact Anchor: 28개
- Fatal misconception: 16개
- Major conditional claim: 6개
- Deterministic verdict: disabled
- LLM semantic profile: enabled
- Direct score application: disabled
- Direct D/E effect: none

## Source

- `gemini_script/20260803_topic05_authority_rangeability_gain_requirements.md`
- `docs/topic_sheets/control_valve_authority_rangeability_gain_installed_performance.md`
- Control Valve Handbook Chapter 2

## 작성 상태

Source JSON authored and source-level validation pending generated-bank build.
