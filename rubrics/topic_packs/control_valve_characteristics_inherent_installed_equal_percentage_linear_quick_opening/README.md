# 제어밸브 고유·설치 유량특성과 Linear·Equal Percentage·Quick Opening

## Topic metadata

- Topic ID: `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`
- Question type: `COMPARE_SELECTION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Roadmap priority: `★★★★★`
- Grading mode: `LLM_ONLY`
- Deterministic checks: disabled

## Scope

제어밸브의 기준 유량특성과 실제 system에서 나타나는 설치 유량특성을 구분하고,
Linear, Equal Percentage 및 Quick Opening의 곡선과 선정기준을 평가한다.

- normalized valve travel과 relative flow coefficient
- Inherent Flow Characteristic
- Installed Flow Characteristic
- Linear Characteristic
- Equal Percentage Characteristic
- Quick Opening Characteristic
- valve differential pressure와 actual flow
- pressure-drop redistribution
- system resistance
- pump curve와 static head
- conditional application mapping
- manufacturer curve와 commissioning verification

## Boundary

- actuator force, friction와 Fail-Safe spring: Topic 1 참조
- Valve Authority, Rangeability와 quantitative gain: Topic 3
- Cv·Kv와 liquid sizing: Topic 4
- cavitation, flashing와 choked liquid flow: Topic 6
- Balanced·Unbalanced trim 상세: Topic 8
- stiction, deadband와 hysteresis 상세: Topic 11

## Source inventory

- Fact Anchors: 22
- Fatal misconception contracts: 12
- Major conditional-error contracts: 3
- Rich question patterns: 10
- Recommended Outline sections: 7

## Grading policy

Logic Check는 Topic 신뢰도와 B/C 진단에 사용한다.

Fatal 오류가 확인되면 Topic trust를 `limited`로 본다.

Verified correctness 오류의 canonical owner는 C이며 같은 오류를 B와 C에서 중복 감점하지 않는다.

Logic Check 결과는 D/E 점수에 직접 반영하지 않는다.
