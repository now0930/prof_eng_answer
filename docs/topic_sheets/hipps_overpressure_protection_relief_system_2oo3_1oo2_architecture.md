# HIPPS 과압보호시스템의 구조, Voting Architecture 및 Relief System 비교

## 1. Topic metadata

- Topic ID: `hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture`
- Question type: `COMPARE_SELECTION`
- Difficulty: `THEORY_CORE`
- Selection importance: `CORE_MUST_PREPARE`
- Authoring method: 공식 Topic Pack 생성 후 직접 검토·작성

## 2. 정의와 목적

HIPPS는 High Integrity Pressure Protection System이다.

고압원에서 저압측 설비로 유입되는 에너지를 Sensor, Logic Solver와 Shutdown Valve로 차단하여 설계압력 초과를 예방한다.

HIPPS는 Relief Valve의 다른 이름이 아니다.

Relief Device는 과압 시 유체를 배출하여 압력을 제한한다.

HIPPS는 과압을 일으키는 유입 자체를 차단한다.

## 3. 적용경계

대표 적용경계는 고압 공급원과 더 낮은 설계압력을 가진 downstream 배관·용기·공정설비 사이이다.

적용성은 다음을 확인한다.

- 과압 initiating cause
- downstream design pressure와 허용압력
- pressure rise rate
- 차단 가능한 유입원
- 잔여열원과 trapped liquid expansion
- Relief 또는 flare disposal capability
- Code와 사업장 risk criterion

## 4. 전체 SIF 구조

HIPPS는 다음 전체 경로로 평가한다.

`Pressure Sensor → Voting/Logic Solver → Solenoid 또는 Pilot → Actuator → Shutdown Valve → Safe State`

전원, 공기·유압 공급, process tap, root valve, position feedback, alarm, reset와 bypass도 기능경계에 포함한다.

## 5. Trip setpoint와 Process Safety Time

Trip setpoint는 보호대상의 허용압력보다 낮아야 한다.

다음 여유를 반영한다.

- Sensor accuracy와 drift
- deadband와 scan delay
- voting과 logic execution time
- solenoid·pilot response
- actuator와 valve stroke time
- valve closure 중 pressure overshoot

총 응답시간은 Process Safety Time보다 짧아야 한다.

## 6. 2oo3 Sensor Voting

2oo3는 세 채널 중 두 채널이 trip 조건을 만족할 때 안전동작을 요구한다.

장점:

- 단일 Sensor false high에 의한 spurious trip 억제
- 단일 채널 고장 상태에서도 일정한 voting capability 유지
- channel discrepancy와 diagnostics 활용

한계:

- common process tap과 root valve
- shared power와 cabinet environment
- 동일 모델·교정절차·software
- logic solver와 maintenance common cause

따라서 채널 수만으로 SIL을 보장하지 않는다.

## 7. Degraded voting

한 채널을 bypass하거나 fault isolation하면 원래 2oo3 구조가 유지되지 않는다.

전환정책에 따라 1oo2 또는 2oo2가 될 수 있다.

- 1oo2: 안전동작 민감도는 높지만 spurious trip 가능성이 증가할 수 있다.
- 2oo2: spurious trip은 줄지만 위험고장 허용도가 악화될 수 있다.

Degraded mode, 허용시간, 보상조치와 복구조건을 SRS에 명시한다.

## 8. 1oo2 Final Element

직렬 Shutdown Valve 두 대 중 어느 하나의 폐쇄만으로 요구 유량차단과 Safe State를 달성하면 기능적 1oo2로 평가할 수 있다.

그러나 다음 요구에서는 단순 1oo2 가정이 성립하지 않을 수 있다.

- double block 요구
- 특정 leakage class
- zero-energy isolation
- 두 방향 압력차 조건
- bypass 또는 equalizing path
- 한 Valve closure만으로 pressure rise가 멈추지 않는 공정

Architecture 표기는 실제 안전기능 성공조건을 기준으로 정한다.

## 9. Final Element 동작경로

Final Element는 Valve body만이 아니다.

다음을 함께 검증한다.

- actuator torque와 thrust
- spring return 또는 accumulator
- solenoid/pilot valve
- air·hydraulic supply
- tubing과 restriction
- position feedback
- seat leakage
- closing profile과 stroke time

Fail close 표기만으로 실제 성능을 대체하지 않는다.

## 10. Closure Time, Surge와 Leakage

빠른 폐쇄는 pressure rise를 제한하지만 surge와 pressure wave를 만들 수 있다.

따라서 다음을 동시에 만족해야 한다.

1. Process Safety Time 안에 요구 차단량 도달
2. transient pressure가 보호설비와 upstream system의 허용한계 이하
3. valve·actuator와 배관의 dynamic load 수용
4. closure 후 leakage가 residual pressure criterion 만족

## 11. PFDavg와 SIL 검증

Target SIL은 위험분석이 요구한 무결성이다.

Achieved SIL은 설계된 HIPPS가 실제로 달성한 무결성이다.

전체 PFDavg에는 다음을 포함한다.

- Sensor subsystem
- Logic Solver
- Final Element
- common cause
- diagnostic coverage
- proof test interval과 coverage
- repair time
- bypass exposure
- human error와 systematic capability

개별 인증기기의 SIL 표시는 전체 SIF 검증을 대체하지 않는다.

## 12. BPCS와 독립성

HIPPS를 IPL로 credit하려면 initiating cause와 BPCS로부터 독립적이어야 한다.

다음을 검토한다.

- process tap과 Sensor
- power와 utility
- logic hardware와 software
- shutdown valve와 actuator
- communication path
- maintenance team과 procedure
- test equipment와 calibration reference

## 13. HIPPS와 Relief System 비교

| 구분 | HIPPS | Relief System |
|---|---|---|
| 기능 | 고압원 유입 차단 | 과압 유체 배출 |
| 성격 | 예방형 계장 SIF | 완화형 기계 보호 |
| 핵심 성능 | Isolation integrity, response time | Set pressure, relieving capacity |
| 주요 의존 | Sensor·Logic·Valve·Utility | Valve·rupture disc·discharge path |
| 환경영향 | 정상 trip 시 방출 감소 가능 | flare·vent·containment 필요 |
| 대표 위험 | common cause, fail-to-close, spurious trip | fail-to-open, undersizing, backpressure |
| 운영관리 | proof test, voting, bypass, SRS | inspection, set pressure, discharge system |

두 방법은 상호배타적이지 않다.

## 14. Relief 대체와 병행 선정

HIPPS가 Relief Load를 줄이거나 특정 Relief Device를 대체할 수 있는지는 다음을 검토한다.

- 적용 Code와 법규
- 모든 credible overpressure scenario
- fire, thermal expansion와 blocked-in condition
- reaction 또는 residual heat source
- HIPPS independence와 achieved integrity
- flare 또는 discharge system availability
- environmental impact
- maintenance competence와 spare strategy
- false trip 생산손실
- lifecycle cost와 legacy integration

필요하면 HIPPS와 Relief Device를 병행한다.

## 15. SRS와 운영관리

SRS에는 다음을 정의한다.

- initiating cause와 protected equipment
- pressure measurement range
- trip setpoint와 voting
- safe state와 valve sequence
- process safety time와 maximum closure time
- alarm, latch, reset와 restart permissive
- sensor/valve bypass와 degraded mode
- proof test와 partial stroke test 경계
- acceptance criterion
- MOC와 revalidation 조건

## 16. 인접 Topic handoff

- 목표 SIL 산정: `hazop_lopa_ipl_risk_reduction_sil_target_allocation`
- Final Element·PST 상세: `final_control_element_sil_sis_esd_valve_partial_stroke_test`
- SIS software lifecycle: `sis_sil_safety_software_independence_systematic_failure_verification_validation`
- 본 Topic은 위 세부영역을 재소유하지 않는다.

## 17. 기술사 답안 권장 흐름

1. HIPPS 정의와 Relief와의 차이를 제시한다.
2. 전체 SIF 구조를 도식화한다.
3. Trip setpoint와 Process Safety Time을 설명한다.
4. 2oo3 Sensor와 degraded mode를 설명한다.
5. 조건부 1oo2 Final Element를 설명한다.
6. PFDavg, SIL과 독립성을 검증한다.
7. Relief System과 비교하여 선정기준을 제시한다.
8. SRS, 시험, bypass와 MOC로 결론낸다.

## 18. Human review checklist

- [ ] HIPPS와 Relief Device를 구분했는가
- [ ] 전체 SIF 경계를 제시했는가
- [ ] Setpoint margin과 Process Safety Time이 있는가
- [ ] 2oo3의 common cause와 degraded mode가 있는가
- [ ] 1oo2 적용조건과 예외가 있는가
- [ ] Closure Time, Surge와 Leakage를 검토했는가
- [ ] Target SIL과 Achieved SIL을 구분했는가
- [ ] Code와 잔여 과압원을 검토했는가
- [ ] Proof Test, Bypass, SRS와 MOC가 있는가
- [ ] Generated bank를 직접 수정하지 않았는가
