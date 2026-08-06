# 제어논리, Sequence, Interlock, Permissive, Trip, 상태전이 및 Fail-Safe

## Topic identity

- SW 번호: `SW-02`
- Topic ID: `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`
- Lane: `SOFTWARE_LLM_LANE_A`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `CORE_MUST_PREPARE`

## 1. 목적

이 Topic Pack은 PLC·DCS 기반 운전 제어논리를 단순 키워드가 아니라 상태와 조건의 관계로 평가한다. 핵심은 Sequence를 Step 나열로 설명하는 데 있지 않다. 현재 상태, 전이조건, 출력동작, 피드백 확인, Timeout, 보호 우선순위와 복구경로를 하나의 결정론적 논리로 연결해야 한다.

## 2. 포함 범위

- Sequence control과 Step·State 모델
- State transition, Transition guard, Entry·Exit action
- Permissive, Interlock, Trip, Shutdown
- Cause & Effect
- M-out-of-N Voting과 First-out
- Bypass와 Override
- Fail-safe와 Safe state
- Watchdog, Heartbeat, Bad quality와 stale data
- Trip latch와 Reset valid
- Manual·Auto, Local·Remote 명령 우선순위
- Timeout, Feedback confirmation, Debounce, Hysteresis
- Restart, Recovery, State reconciliation
- Abnormal transition prevention과 Degraded mode

## 3. 제외 범위

다음은 SW-02의 핵심 채점범위가 아니다.

- HMI 화면계층, High-performance HMI
- Alarm philosophy, rationalization, priority, Deadband, Delay, Shelving, Suppression
- Setpoint list, Alarm value, Trip value, Interlock value 관리
- SOE 화면·보고서 운영, Audit trail, Operator authority
- SIL 산정, PFDavg, PFH
- 안전수명주기, 체계적 고장 통제, 독립성
- Safety V&V와 안전 SW 적격성

## 4. Ownership 경계

### SW-03과의 경계

SW-02는 Interlock·Trip·Sequence의 실제 동작논리와 상태전이를 소유한다. SW-03은 그 결과를 운전자에게 전달하는 HMI·SCADA, Alarm 관리, Setpoint, SOE, Audit trail과 권한을 소유한다.

First-out은 최초 원인을 선정하는 메커니즘까지 SW-02이다. First-out 또는 SOE를 화면에 표시하고 검색·보고하는 운영기능은 SW-03이다.

### SW-05와의 경계

SW-02는 Fail-safe, Trip, Voting과 Bypass의 운전논리 메커니즘을 다룬다. SW-05는 해당 기능의 SIL 산정, 안전수명주기, 독립성, 체계적 고장 통제와 Safety V&V를 다룬다. 모든 Interlock을 SIS로 간주하지 않는다.

## 5. 핵심 논리 관계

### 5.1 상태전이

```text
S(k+1) = delta(S(k), Command, Permissive, Interlock, Trip, Feedback, Timer)
```

동일한 현재 상태와 입력에는 동일한 다음 상태가 결정되어야 한다.

### 5.2 전이 허가

```text
Transition_Enable
= Command
AND Permissive_All
AND Feedback_OK
AND NOT Trip
AND NOT Inhibit
```

여기서 `Permissive_All = p1 AND p2 AND ... AND pn`이다.

### 5.3 Voting

```text
Trip_vote = 1, when sum(x_i) >= M for N channels
```

`M-out-of-N` 숫자만으로 성능이 보장되지 않는다. 채널 독립성, 공통원인, 진단과 불일치 처리가 필요하다.

### 5.4 Trip latch

```text
Trip_Latched(k+1)
= Trip_Event
OR [Trip_Latched(k) AND NOT Reset_Valid]
```

Set-dominant가 기본이다. `Reset_Valid`는 원인 제거, 안전조건, 권한과 Reset edge를 모두 확인해야 한다.

### 5.5 First-out

```text
First_Out = arg min(t_i), for valid initiating causes
```

후속 연쇄신호가 아니라 최초의 유효 원인을 고정한다.

### 5.6 Watchdog

```text
Watchdog_Expired = Current_Time - Last_Heartbeat > Timeout
```

Timeout 후 동작은 Hold, Controlled stop, Safe action 또는 제한운전 중 공정에 적합한 정책으로 정한다.

## 6. 대표 출제문제

1. Sequence control의 상태전이, 단계완료 조건 및 비정상 전이 방지방법을 설명하시오.
2. Interlock, Permissive 및 Trip의 차이와 적용방법을 설명하시오.
3. 공정 Shutdown 논리와 Cause & Effect 작성 시 고려사항을 설명하시오.
4. 2oo3 Voting과 First-out 논리의 원리 및 설계 유의사항을 설명하시오.
5. Bypass와 Override의 차이, 위험요인 및 관리방안을 설명하시오.
6. Fail-safe와 Watchdog의 개념을 설명하고 고장 시 제어논리를 제시하시오.
7. 제어시스템 Restart 및 Recovery 논리의 설계기준을 설명하시오.
8. PLC Sequence에서 Timer, Feedback, Edge 및 Latch 적용 시 주의사항을 설명하시오.
9. Manual·Auto, Local·Remote 운전모드의 명령 우선순위와 보호논리를 설명하시오.
10. 상태전이표를 이용한 이상전이 방지 및 복구방안을 설명하시오.

## 7. 대표 Fatal 오류

- Permissive와 Trip을 같은 기능으로 설명
- Interlock을 Alarm 표시만 하는 기능으로 설명
- Trip 원인 소멸 즉시 무조건 Auto reset
- Bypass를 승인·표시·시간제한 없이 유지
- Fail-safe를 모든 설비의 Fail-close로 일반화
- Voting 채널을 늘리면 항상 안전하다고 설명
- First-out을 마지막 신호 또는 Alarm 우선순위로 설명
- Watchdog를 표시기능으로만 설명
- Restart 시 이전 출력과 Step을 조건 확인 없이 복원
- Cause & Effect만으로 실행논리가 완성된다고 설명
- Timer 만료를 설비 완료 피드백으로 대체
- Override와 Bypass를 같은 기능으로 설명
- 정상 Shutdown과 Trip을 동일시
- 모든 Interlock을 SIS·SIL 기능으로 간주
- Manual mode에서 보호 Interlock과 Trip을 전부 무효화
- Bad quality와 stale data를 정상 신호로 간주

## 8. Warn 또는 Major 수준 부족사항

- State와 Step은 언급했으나 진입·완료·실패·복구 조건이 없음
- Permissive·Interlock·Trip의 시점과 우선순위 비교가 없음
- Trip latch와 Reset valid가 없음
- Feedback confirmation과 Timeout의 역할을 구분하지 않음
- Bypass·Override의 권한과 복구통제가 없음
- Restart 상태 일치화가 없음
- Bad quality와 통신복구 정책이 없음
- HMI·Alarm 또는 SIL 설명으로 주제가 이동함

## 9. False positive 방지

- `Trip` 또는 `Interlock` 단어 하나만으로 이 Topic을 선택하지 않는다.
- Alarm priority·Shelving·SOE 표시가 중심이면 SW-03이다.
- SIL·PFDavg·Safety lifecycle이 중심이면 SW-05이다.
- 특정 설비의 Fail-close 사례는 허용한다. 모든 설비에 대한 절대 주장일 때만 Fatal이다.
- 위험이 낮은 보조설비의 조건부 Auto reset도 상태검증과 설계근거가 있으면 허용한다.
- Bypass를 정비수단으로 언급한 것 자체는 오류가 아니다. 관리통제 유무를 평가한다.

## 10. Model Answer 권장 구조

1. 배경과 제어논리 계층
2. Sequence와 상태전이 모델
3. Permissive·Interlock·Trip·Shutdown 비교
4. Cause & Effect·Voting·First-out
5. Bypass·Override·명령 우선순위
6. Fail-safe·Watchdog·신호품질
7. 이상전이 방지와 Scan 기반 구현
8. Restart·Recovery와 현장 적용 결론

## 11. Focused regression 계약

Focused test는 다음을 확인한다.

- source JSON 4개의 Topic ID와 schema
- Anchor 28개와 Fatal 16개의 유일성
- Model Answer의 모든 Anchor reference 유효성
- SW-03·SW-05 ownership 경계 존재
- broad alias인 `PLC`, `SCADA`, `Alarm`, `Trip`, `Interlock`, `SIS` 단독 사용 금지
- 상태전이, Voting, Trip latch, Watchdog, Restart 논리 회귀
- generated bank와 공통 Router를 변경하지 않았는지 ownership 검사

## 12. Topic-local 완료 기준

- Topic Sheet 생성
- README와 source JSON 4개 생성
- focused test 생성 및 통과
- JSON 문법 검증 통과
- Topic Pack quality/schema 검증 통과
- git diff whitespace 검증 통과
- 새 변경경로가 SW-02 허용경로와 정확히 일치
- generated, 공통 Python, 기존 Topic 불변
- SW-02 Topic-local 로컬 커밋 생성
- 원격 push 미실행
