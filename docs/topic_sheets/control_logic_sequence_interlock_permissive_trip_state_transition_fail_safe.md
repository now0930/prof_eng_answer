# SW-02 Topic Sheet

## 0. Topic identity

- Topic ID: `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`
- 한글 주제: 제어논리, Sequence, Interlock, Permissive, Trip, 상태전이 및 Fail-Safe
- Lane: `SOFTWARE_LLM_LANE_A`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `CORE_MUST_PREPARE`

## 1. 출제 의도

산업 계측제어 소프트웨어는 단순히 조건문을 연결하는 프로그램이 아니다. 실제 설비는 기동 전 조건, 운전 중 금지조건, 보호정지, 수동조작, 통신고장과 재기동 상황을 동시에 처리해야 한다. 따라서 답안은 Sequence, 상태전이, Interlock, Permissive와 Trip의 의미를 구분하고, 정상경로와 실패·복구경로를 함께 제시해야 한다.

## 2. 포함 범위

1. Sequence control
2. Step과 State
3. State transition과 Transition guard
4. Entry action, 지속동작, Exit action
5. Permissive
6. Interlock
7. Trip과 Trip latch
8. 정상 Shutdown과 보호 Shutdown
9. Cause & Effect
10. M-out-of-N Voting
11. First-out
12. Bypass와 Override
13. Fail-safe와 Safe state
14. Watchdog와 Heartbeat
15. Bad quality와 stale data
16. Command arbitration
17. Abnormal transition prevention
18. Restart와 Recovery

## 3. 제외 범위

### 3.1 SW-03으로 넘기는 범위

- HMI·SCADA architecture
- High-performance HMI
- Alarm philosophy와 rationalization
- Priority, Deadband, Delay
- Shelving과 Suppression
- Setpoint·Alarm·Trip·Interlock value list 관리
- SOE 화면·보고서
- Audit trail
- Operator authority와 Display hierarchy

SW-02는 Alarm 또는 SOE에 나타날 실제 논리 이벤트의 발생조건을 다룬다. 표시방식과 운영정보 관리는 SW-03이 담당한다.

### 3.2 SW-05로 넘기는 범위

- SIL 산정
- PFDavg와 PFH
- 안전수명주기
- 체계적 고장
- 독립성
- Safety V&V
- SIS 안전 SW 적격성

SW-02는 일반 운전논리와 보호동작 메커니즘만 담당한다.

## 4. Ownership 판단표

| 논점 | SW-02 소유 | 인접 Topic 소유 |
|---|---|---|
| Interlock 동작조건과 출력 강제 | O |  |
| Trip 상태전이와 Latch·Reset | O |  |
| First-out 최초 원인 선정 | O |  |
| SOE 화면 표시와 검색 |  | SW-03 |
| Alarm priority·Shelving |  | SW-03 |
| Operator 권한과 Audit trail |  | SW-03 |
| Voting 논리의 동작 메커니즘 | O |  |
| Voting 구조의 SIL 충족성 |  | SW-05 |
| Fail-safe 상태전환 | O |  |
| Safety lifecycle와 독립성 |  | SW-05 |

## 5. 핵심 개념

### 5.1 Sequence control

Sequence는 공정을 여러 Step 또는 State로 분할한다. 각 상태에는 다음 항목이 필요하다.

- 진입조건
- 실행출력
- 유지조건
- 완료 피드백
- 최대 허용시간
- 실패상태
- 복구 또는 안전정지 경로

Timer만 만료되었다고 실제 설비가 움직였다고 판단해서는 안 된다.

### 5.2 상태전이

```text
S(k+1) = delta[S(k), U(k), P(k), I(k), T(k), F(k)]
```

- `S(k)`: 현재 State
- `U(k)`: 운전명령
- `P(k)`: Permissive
- `I(k)`: Interlock·Inhibit
- `T(k)`: Trip
- `F(k)`: 설비 Feedback와 Timer

다음 상태는 동일한 입력에서 동일하게 결정되어야 한다. 허용되지 않은 전이는 Illegal state로 처리한다.

### 5.3 Transition guard

```text
E_transition
= Command
AND Permissive_All
AND Feedback_OK
AND NOT Trip
AND NOT Inhibit
```

전이조건은 명령만으로 구성하지 않는다. 실제 설비상태와 보호조건을 함께 확인해야 한다.

### 5.4 Permissive

Permissive는 기동 또는 특정 전이를 시작하기 위한 사전 허가조건이다.

예:

- 윤활유 압력 정상
- 냉각수 유량 정상
- 흡입밸브 위치 확인
- Downstream 설비 준비완료

보통 필수조건을 AND로 묶는다.

### 5.5 Interlock

Interlock은 위험한 조합을 금지하거나 출력을 강제하는 운전 제약이다.

예:

- Pump 운전 중 흡입밸브 Close 금지
- 두 방향 Contactor 동시 투입 금지
- 고온 시 Heater 출력 차단
- 설비 이동 중 Door open 금지

Alarm은 운전자에게 정보를 주지만 Interlock은 실제 동작을 제한한다.

### 5.6 Trip

Trip은 보호조건 성립 시 정상 Sequence보다 우선하여 설비를 미리 정한 정지상태로 이행시킨다.

일반적인 Trip 처리:

1. 원인 검출
2. Trip Event Set
3. Trip Latch 유지
4. 보호출력 실행
5. First-out 저장
6. 원인 제거 확인
7. Safe condition 확인
8. 권한 있는 Reset
9. Restart 조건 재평가

### 5.7 Shutdown

정상 Shutdown은 공정을 순차적으로 정리할 수 있다. Trip은 위험을 제한하기 위해 정상 Sequence를 중단하고 우선동작한다. 두 동작은 목적과 시간특성이 다르다.

### 5.8 Cause & Effect

Cause & Effect는 원인과 결과를 표 또는 행렬로 연결한다.

| Cause | Alarm | Interlock | Trip | Final action |
|---|---:|---:|---:|---|
| Low suction pressure | O | Start inhibit | Delay trip | Pump stop |
| High-high temperature | O | Heater cut | Immediate trip | Valve safe state |
| Communication loss | O | Mode inhibit | Conditional | Hold or stop |

Cause & Effect는 설계의도 기준문서이다. 상세 상태전이, Timer, Latch, Reset, 우선순위와 Scan 동작은 별도 논리사양이 필요하다.

### 5.9 Voting

```text
Trip_vote = 1 if sum(x_i) >= M
```

예를 들어 2oo3은 3개 채널 중 2개 이상이 Trip일 때 동작한다.

검토 항목:

- 채널 독립성
- 공통원인
- Bad quality 처리
- 불일치 Alarm
- Bypass 중 Voting 변환
- 채널 복구조건

Voting은 채널 수만 늘린다고 항상 좋아지지 않는다.

### 5.10 First-out

```text
First_Out = arg min(t_i)
```

연쇄적으로 여러 Trip 신호가 발생할 때 가장 먼저 발생한 유효 원인을 보존한다. 최종 잔류신호나 Alarm 우선순위가 아니다.

### 5.11 Bypass와 Override

| 구분 | Bypass | Override |
|---|---|---|
| 목적 | 입력 또는 보호경로 우회 | 정상 명령보다 우선하는 강제명령 |
| 주요 위험 | 보호기능 감소 | 예상하지 못한 출력 강제 |
| 필수 통제 | 승인, 표시, 시간제한, 대체조치 | 권한, 범위, 우선순위, 해제조건 |
| 복구 | 원상복귀와 기능확인 | 강제 해제와 정상 소유권 반환 |

### 5.12 Fail-safe

Fail-safe는 고장 시 위험을 최소화하는 상태와 동작이다.

가능한 Safe state:

- Fail-close
- Fail-open
- Fail-last 또는 Hold
- Controlled stop
- 단계적 Depressurization
- 제한운전

모든 설비가 Fail-close인 것은 아니다.

### 5.13 Watchdog

```text
Watchdog_Expired
= Current_Time - Last_Heartbeat > Timeout
```

Watchdog 대상:

- PLC Task
- Controller redundancy
- Remote I/O
- Network connection
- Smart device heartbeat

Timeout 후에는 단순 Alarm뿐 아니라 Hold, Controlled stop 또는 Safe action 정책이 필요하다.

### 5.14 Trip latch와 Reset

```text
Q_trip(k+1)
= Trip_Event
OR [Q_trip(k) AND NOT Reset_Valid]
```

```text
Reset_Valid
= Cause_Clear
AND Safe_Condition
AND Authorized
AND Reset_Edge
```

원인이 남아 있는 상태에서 Reset을 허용해서는 안 된다.

### 5.15 이상전이 방지

- Allowed transition matrix
- Mutual exclusion
- One-hot state
- Transition-in-progress lock
- Timeout
- Feedback discrepancy
- Debounce와 Hysteresis
- Illegal-state fallback
- 단일 출력 소유자
- Trip 우선순위

### 5.16 Scan, Edge와 Memory

PLC Scan에서는 Level과 Edge를 구분한다.

- Level: 조건이 참인 동안 계속 참
- Rising edge: False에서 True로 변한 1회 이벤트
- One-shot: 한 Scan 또는 한 실행주기만 참
- Latch: Reset 전까지 상태 유지

Set과 Reset이 동시에 성립할 가능성이 있으면 우선순위를 명시한다.

### 5.17 Command arbitration

권장 우선순위 예:

```text
Trip or Emergency action
> Safety-critical Interlock
> Controlled shutdown
> Maintenance Override
> Manual command
> Automatic Sequence command
```

실제 우선순위는 프로젝트 요구사항으로 확정한다. 한 출력은 한 시점에 하나의 논리 소유자만 가져야 한다.

### 5.18 Restart와 Recovery

Restart 시 확인사항:

1. Cold start와 Warm restart 구분
2. 출력 초기화 정책
3. 실제 밸브·모터·접점 상태 재수집
4. 메모리 State와 현장상태 비교
5. State reconciliation
6. Trip latch 보존
7. Permissive 재확인
8. 자동재개 또는 운영자 승인 결정
9. 부분정전과 통신복구 시나리오 검증

## 6. 대표 오답과 판정

| 대표 오답 | 판정 | 정정 |
|---|---|---|
| Permissive와 Trip은 같다 | Fatal | 사전 허가와 보호정지를 구분 |
| Interlock은 Alarm만 발생 | Fatal | 금지 또는 강제동작 수행 |
| Trip 원인이 없어지면 즉시 Auto reset | Fatal | Latch와 Reset valid 필요 |
| 모든 Fail-safe는 Fail-close | Fatal | 공정별 Safe state |
| Voting은 채널이 많을수록 항상 안전 | Fatal | 독립성·공통원인 검토 |
| Timer 만료가 실제 완료 피드백 | Fatal | 실제 Feedback 확인 |
| Restart 시 이전 Step 그대로 복원 | Fatal | State reconciliation |
| Bypass 승인과 시간제한 누락 | Major | 관리통제 추가 |
| First-out 누락 | Warn 또는 Major | 문항 요구 시 최초 원인 보존 설명 |
| HMI 화면과 Alarm priority 위주 답안 | Scope drift | SW-03으로 이동 |
| SIL 계산 위주 답안 | Scope drift | SW-05로 이동 |

## 7. False positive 기준

1. 문항이 Alarm 관리 중심이면 SW-03이다.
2. 문항이 SIL 산정 중심이면 SW-05이다.
3. 특정 밸브의 Fail-close 사례는 허용한다.
4. 비위험 설비의 조건부 Auto restart는 허용할 수 있다.
5. Cause & Effect를 중요 설계문서라고 한 것은 정답이다.
6. Bypass가 필요할 수 있다는 설명 자체는 정답이다.
7. First-out과 SOE를 함께 설명해도 소유범위를 구분하면 정답이다.
8. 단순 누락은 Fatal이 아니다.

## 8. Model Answer 예시 구조

### 8.1 배경

공정 자동화는 정상운전뿐 아니라 기동 전 조건, 운전 중 금지조건, 고장 시 보호정지와 복구를 일관되게 처리해야 한다. 이를 위해 Sequence, 상태전이, Interlock, Permissive와 Trip을 계층적으로 설계한다.

### 8.2 핵심 내용

Sequence는 State와 Transition으로 구성한다. 전이는 명령, Permissive, 정상 Feedback, `NOT Trip`, `NOT Inhibit`가 모두 성립할 때 허용한다. Permissive는 사전 허가조건이다. Interlock은 위험한 조합을 금지하거나 출력을 강제한다. Trip은 보호조건 발생 시 정상 Sequence보다 우선하여 정지상태로 이행한다.

Cause & Effect는 원인과 결과의 설계 의도를 제시한다. Voting은 M-out-of-N 구조로 판정하되 독립성과 공통원인을 검토한다. First-out은 연쇄 Trip의 최초 원인을 보존한다. Bypass와 Override는 목적이 다르므로 권한, 표시, 시간제한과 해제조건을 분리한다.

Fail-safe는 공정별 Safe state로 정의한다. Watchdog, Bad quality와 stale data는 Hold, Controlled stop, Trip 또는 Degraded mode로 연결한다. Restart 시에는 실제 상태를 재수집하고 State reconciliation과 Permissive 재확인을 수행한다.

### 8.3 결론

고득점 답안은 용어 나열이 아니라 조건, 우선순위, 출력, 피드백, 실패와 복구를 상태전이로 연결해야 한다. 또한 HMI·Alarm 관리는 SW-03, SIL과 안전수명주기는 SW-05로 구분해야 한다.

## 9. Topic Importance

이 Topic은 PLC·DCS 응용, Cause & Effect, 시운전, 트러블슈팅과 안전정지 문제의 공통 기반이다. 실무 적용성이 높고 다양한 문제와 결합되므로 `CORE_MUST_PREPARE`로 분류한다.

## 10. Routing alias

- `제어논리 Sequence Interlock Permissive Trip`
- `시퀀스 상태전이 인터록 퍼미시브 트립`
- `Sequence control state transition interlock permissive trip`
- `운전 제어논리와 상태전이`
- `Interlock Permissive Trip 차이`
- `인터록 퍼미시브 트립 차이`
- `Cause & Effect Voting First-out`
- `원인 결과표 Voting First-out`
- `Bypass Override 제어논리`
- `바이패스 오버라이드 명령 우선순위`
- `Fail-safe Watchdog Restart Recovery`
- `Fail safe watchdog 재기동 복구논리`
- `Sequence abnormal transition prevention`
- `시퀀스 이상전이 방지`
- `Trip latch reset logic`
- `트립 래치 리셋 조건`
- `Manual Auto Local Remote command arbitration`
- `수동 자동 로컬 리모트 명령 중재`
- `PLC sequence feedback timeout one-shot latch`
- `상태전이표 mutual exclusion illegal state recovery`

## 11. Focused regression cases

### Positive routing cases

1. Sequence 상태전이와 Interlock·Trip 설계
2. Permissive와 Trip 차이
3. Cause & Effect, Voting과 First-out
4. Bypass·Override 및 명령 우선순위
5. Watchdog와 Restart recovery
6. Feedback Timeout과 Illegal state 방지

### Negative boundary cases

1. Alarm priority, Deadband, Shelving과 Suppression
2. High-performance HMI와 Display hierarchy
3. SOE 보고서와 Operator audit trail
4. SIL 산정, PFDavg와 PFH
5. Safety lifecycle, independence와 Safety V&V
6. PLC·DCS architecture와 redundancy만 묻는 문제

## 12. Source JSON 설계

- `fact_anchor.json`: Anchor 28개, Fatal 16개
- `logic_check.json`: 명시적 반대 주장용 deterministic fatal, LLM major·warn 및 false-positive 기준
- `model_answer.json`: 대표 질문 10개, 8단계 Outline, compound routing alias
- `topic_importance.json`: DESIGN_EVALUATION, CORE_MUST_PREPARE

## 13. Topic-local 검증

- JSON 문법
- Topic Pack quality/schema
- focused unittest
- trailing whitespace와 EOF
- 변경 파일 ownership
- generated 및 공통 Python 불변

## 14. Topic-local 커밋과 통합 단계 이관

Topic-local 검증이 성공하면 SW-02 파일과 SW-02 전용 실행 스크립트만 별도 로컬 커밋한다. Topic 작업 중에는 원격 push를 수행하지 않는다.

다음은 최종 main 통합 단계로 넘긴다.

- generated rebuild
- cross-topic duplicate 검사
- 전체 Router 회귀
- validate-all
- release validation
- container smoke
- main commit
- main push
