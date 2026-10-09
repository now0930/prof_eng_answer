# 제어밸브 포지셔너·I/P 변환기·부스터·부속기기 및 교정

## Topic ID

`control_valve_positioner_ip_converter_booster_accessories_calibration`

## Question type

Primary: `PRINCIPLE_INTERPRETATION`

Supported secondary: `STRUCTURE`

Supported tertiary: `PROCEDURE`

## 핵심 범위

- Command→I/P→positioner→actuator→travel feedback chain
- Position error와 negative feedback
- Pneumatic positioner force-balance·nozzle-flapper·relay
- Electropneumatic positioner와 separate I/P 구조
- 4–20 mA·3–15 psi current-pressure mapping
- Direct·reverse action과 actuator·fail action 분리
- Feedback linkage·cam alignment
- Zero·span·multipoint upstroke·downstroke calibration
- Split-range local normalization
- Volume booster pressure-follower·flow-capacity 기능
- Filter regulator·lock-up·quick exhaust·solenoid·volume tank
- Bench set·endpoint·loop test
- Loss-of-signal·air·power와 accessory failure response
- As-found·as-left와 vendor crosscheck

## Problem-unit 기준 재정렬 (2026-10-06)

### 중심 Problem Unit

> **전통적인 공압식 및 전기공압식 밸브 포지셔너의 구조와 작동 원리를 설명하고,
> 설정 신호와 밸브 이동량 사이의 피드백 동작 및 I/P 변환기의 역할을 설명하시오.**

이 문장은 확인된 과거 기출이 아니라, 기존 기술 지식으로 구성한 **출제 가능 문제**다.
현재 근거 유형은 지식원천 기반 추론이며, 특정 회차·출제 빈도 또는 공식 출제기준의
확정 문항으로 주장하지 않는다.

| 문제 요구 | 답안에 연결할 지식 | Fact Anchor |
|---|---|---|
| 전통 포지셔너의 목적과 신호 경로 | Command/reference, positioner, actuator, travel feedback의 역할과 경계 | `command_ip_positioner_actuator_feedback_chain`, `positioner_travel_feedback_controller` |
| 공압식 구조·작동 | nozzle-flapper/force-balance/relay의 조건부 구성, feedback element와 출력 변화 | `pneumatic_positioner_force_balance_mechanism`, `travel_feedback_linkage_cam_alignment` |
| 피드백 동작 | reference와 measured travel의 차이를 correction으로 줄이는 negative-feedback 관계 | `position_error_negative_feedback`, `positioner_travel_feedback_controller` |
| 전기공압 구성과 I/P 역할 | integrated electropneumatic positioner와 separate I/P 구분; I/P는 current-to-pressure 변환기이며 travel sensor/controller가 아님 | `electropneumatic_positioner_separate_ip_boundary`, `ip_converter_current_pressure_transduction` |
| 신호 범위 예시 | 명시된 conventional 4–20 mA / 3–15 psi 조건에서 정규화와 endpoint 관계 | `normalized_current_command`, `ip_linear_pressure_mapping`, `conventional_4_20ma_3_15psi_endpoints`, `ip_supply_air_dependency` |
| 동작 방향과 실제 밸브 동작의 구분 | Positioner direct/reverse, actuator air/spring action, valve fail action을 같은 용어로 취급하지 않음 | `positioner_direct_reverse_action`, `actuator_action_fail_action_separation` |

중심 문제의 답안 골격은 **구성/신호 경로 → 공압 변환부와 feedback linkage → 오차와
negative feedback → I/P의 위치 → action/fail 동작 구분 → 핵심 적용조건**이다. 수치
계산은 문제에서 범위를 주었을 때만 하며, accessory catalog, full calibration 절차,
split-range 설계, 고장진단 전체를 한 답안의 필수요구로 강제하지 않는다.

### 관련 문제와 현재 호환 경계

현행 `model_answer.json`에는 위 중심 문제 외에도 calibration, split-range, booster,
pneumatic accessories, fault diagnosis와 integrated loop test를 묻는 별도 문제 후보가
함께 보존되어 있다. 이들은 동일 문항의 표현 변형으로 간주할 수 없다. 기존 focused
regression은 40 Anchor·10 patterns 및 일부 router 결과를 고정하고 있으므로, 이 단계에서
삭제·이동하지 않고 아래와 같이 compatibility candidates로 분류한다.

- **중심 문제의 변형:** 전체 signal chain, pneumatic force-balance/nozzle-flapper 원리,
  conventional I/P mapping.
- **독립 문제 후보:** direct/reverse와 fail-action 조합, booster/accessory 기능 비교,
  split-range mapping, zero/span 및 up/down calibration, bench-set·loop-test 순서,
  loss-of-signal/air/power fault diagnosis, 기록·통합검증.
- **공압 부속기기 이관 초안:** 기능 비교 문제의 별도 Pack 초안
  `control_valve_pneumatic_accessories_function_application`을 managed workflow로 작성했다.
  현재 draft / human_review_required이며 이 기존 Pack의 anchors, expected patterns, aliases,
  generated manifest, runtime route는 이관·삭제하지 않았다. 사람 검토와 명시적 owner migration
  전까지 accessory 관련 legacy 범위는 호환용으로 남으며, 두 Pack을 동시에 운영 채점하는 것은
  금지한다.
- **기존 owner handoff:** dynamic hunting/stiction은 Topic 3, actuator force·bench set은
  Topic 1, smart diagnostics는 Topic 12, SIS/ESD/PST는 Topic 15, package lifecycle은 Topic 16.

따라서 현재는 **문서상 중심 Problem Unit을 명확히 한 1단계 수정**이다. JSON expected
patterns와 Router consumer의 문제 단위 분리·승계는 아직 완료되지 않았다. 해당 변화를
적용하기 전에는 각 독립 질문의 현재 owner, aliases, grader/training/diagnosis 소비와
회귀를 함께 이관해야 한다.

## 별도 PROCEDURE 문제 후보: Bench set–positioner 작업순서

이 절은 중심 포지셔너 구조·작동 문제의 필수 답안이 아니라, 별도 현장 절차 문제 후보의
참고자료다.

일반적인 작업순서는 다음과 같다. 실제 작업에서는 제조사 매뉴얼, actuator 형식,
valve action과 현장 절차를 우선한다.

1. 밸브·actuator의 기계 상태와 안전조건을 확인한다.
2. Actuator 단독 bench set과 spring range를 확인한다.
3. Valve와 actuator를 결합하고 seat endpoint·travel·mechanical stop을 설정한다.
4. Positioner를 설치하고 feedback linkage·lever·cam을 정렬한다.
5. Positioner action과 actuator·valve action의 조합을 확인한다.
6. Zero·span을 반복 조정한다.
7. 0·25·50·75·100% 상승·하강 다점에서 travel과 hysteresis를 확인한다.
8. Command·current·pressure·travel의 loop test를 수행한다.
9. Signal·air·power 상실 시 fail action과 accessory 동작을 확인한다.
10. As-found·as-left, 설정값과 합격 결과를 기록한다.

Ownership은 분리한다.

- Actuator 힘 평형, spring force와 독립 bench set 산정은 Topic 1이 소유한다.
- 본 Topic은 검증된 bench setting을 인수한 뒤 coupling·endpoint·positioner 설치,
  calibration·loop test·fail-action 및 as-left 기록을 소유한다.

## Logic Check 정책

- Fact Anchor: 40
- Fatal misconception: 22
- Major conditional claim: 10
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Direct score application: disabled
- Direct D/E effect: none

## 경계

- Actuator thrust·bench force·fail-safe spring: Topic 1
- Deadband·stiction·response time·hunting·booster dynamic tuning: Topic 3
- Actuator type와 general mechanical structure: Topic 4
- Balanced trim·balance-seal friction: Topic 10
- Smart diagnostics·valve signature·predictive maintenance: Topic 12
- SIS·ESD·solenoid architecture·PST: Topic 15
- Full valve-package·datasheet·lifecycle workflow: Topic 16

## Source

- `docs/topic_sheets/control_valve_positioner_ip_converter_booster_accessories_calibration.md`
- Control Valve Handbook positioner, I/P converter, booster and accessories sections
- 사용자 정리: `https://now0930.pe.kr/wordpress/%ed%8f%ac%ec%a7%80%ec%85%94%eb%84%88-benchset-%ec%88%9c%ec%84%9c/`
- Control Valve Primer valve-positioner and pneumatic accessory sections
- Topic 1, Topic 3, Topic 4 and Topic 10 source packs
- `gemini_script/20260804_topic11_positioner_ip_booster_requirements.md`

Source JSON authored. Generated-bank build and focused regression are separate stages.
