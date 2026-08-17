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

## Bench set–positioner 작업순서

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
