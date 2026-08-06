# SW-03 Topic Sheet

## 1. Topic 식별

- Topic ID: `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management`
- 한글 주제: HMI·SCADA·Alarm·Setpoint·Trip·Interlock·SOE 및 운전정보 관리
- Lane: `SOFTWARE_LLM_LANE_A`
- 소유범위: 운전자에게 제공되는 공정정보, Alarm, Setpoint, SOE, 권한과 운전정보 관리
- 제외범위: Interlock·Trip의 상태전이 실행논리, SIL 산정, 일반 SW V&V, 프로젝트 FAT·SAT 수행

## 2. 핵심 문제의식

제어시스템이 정확한 제어논리를 보유해도 운전자가 현재 공정상태와 정보의 신뢰도를 이해하지 못하면 적절한 판단과 조치를 수행하기 어렵다. SW-03은 HMI와 SCADA를 단순 화면 또는 데이터 수집 장치로 보지 않는다. 공정상태를 인지하고, 비정상 징후를 발견하며, Alarm을 진단하고, 권한에 따라 조치한 뒤, SOE와 Audit trail로 결과를 추적하는 운전정보 체계로 다룬다.

## 3. 포함 범위

1. HMI와 SCADA의 역할 및 구조
2. 서버·통신 장애, Failover와 데이터 품질 표시
3. High-performance HMI와 화면계층
4. Alarm definition, philosophy와 rationalization
5. Alarm priority, Acknowledge와 Return-to-normal
6. Deadband, Delay, Shelving과 Suppression
7. Alarm flood, Chattering, Standing alarm과 KPI
8. Setpoint·Alarm·Trip·Interlock 값 관리
9. SOE, 시각동기, Historian과 First-out
10. Audit trail, 운전자 권한과 Human error 방지
11. Abnormal situation management

## 4. 제외 범위와 ownership

### 4.1 SW-02 경계

SW-03는 Alarm, Setpoint, SOE, 화면표시와 운전자 권한을 소유한다. Interlock과 Trip의 실제 상태전이, Latch·Reset, Cause & Effect 실행논리, Fail-safe와 Restart는 SW-02가 소유한다.

### 4.2 SW-04 경계

SW-03는 운전정보의 기능과 운영정책을 다룬다. Requirement traceability, Unit·Integration·System test, Static·Dynamic analysis와 일반 SW V&V는 SW-04가 소유한다.

### 4.3 SW-10 경계

SW-03는 Setpoint list, Alarm list와 Interlock value의 내용·관리원칙을 다룬다. 프로젝트 문서 인도, FAT·SAT, Loop test, Commissioning와 Acceptance 절차는 SW-10이 소유한다.

### 4.4 SW-05·SW-08 경계

SIL, PFDavg, PFH, Safety lifecycle와 독립성은 SW-05가 소유한다. SCADA 통신보안, 네트워크 분리와 접근통제 아키텍처는 보안 Topic이 소유한다. SW-03는 운전자 역할과 화면조작 권한만 다룬다.

## 5. HMI·SCADA 구조

HMI는 운전자가 공정상태를 보고 명령을 입력하는 인터페이스이다. SCADA는 원격 설비와 제어기의 데이터를 수집하고 감시, 명령, Alarm, 이력과 보고기능을 제공하는 상위 감시체계이다.

구조 설명에는 다음 흐름이 포함되어야 한다.

```text
Sensor·Actuator
→ PLC·DCS·RTU
→ Control network
→ SCADA server·Alarm server·Historian
→ HMI client·Engineering station
→ Operator action·Audit
```

서버 이중화 자체만으로 신뢰성이 확보되는 것은 아니다. 통신단절, Failover 진행상태, Bad·Uncertain·Stale quality, 수동대체값과 재연결 후 데이터 일치성을 화면에서 구분해야 한다.

## 6. High-performance HMI

High-performance HMI의 목적은 화려한 화면이 아니라 빠른 상황인식이다.

- 정상상태는 낮은 시각적 강조를 사용한다.
- Alarm과 비정상 상태는 제한된 색상과 기호로 강조한다.
- 현재값만 아니라 정상범위, 편차, 변화방향과 Trend를 함께 제공한다.
- 화면 이동 후에도 설비 위치, 운전모드, 선택대상과 관련 Alarm의 맥락을 유지한다.
- Command와 Feedback을 다른 표시로 구분한다.
- Bad·Stale quality를 정상 최신값처럼 표시하지 않는다.

화면계층 예시는 다음과 같다.

| Level | 목적 | 핵심 정보 |
|---|---|---|
| Level 1 | 공정 전체 Overview | 생산상태, 주요 제약, 이상 위치 |
| Level 2 | Unit·Area | 장치군 상태, 주요 Alarm과 Trend |
| Level 3 | 상세 운전 | Loop, Valve, Motor, Sequence 상태 |
| Level 4 | 진단·정비 | 상세 신호, 품질, 이력, 장치진단 |

## 7. Alarm의 정의와 Lifecycle

Alarm은 비정상 상태를 알리고 운전자가 정해진 시간 안에 판단 또는 조치를 하도록 요구한다. 조치가 필요하지 않은 Event, Status와 Notification은 Alarm으로 만들지 않는다.

Alarm 상태는 Process condition과 Acknowledgement를 분리해서 이해해야 한다.

```text
Condition normal
→ Alarm active and unacknowledged
→ Alarm active and acknowledged
→ Condition returned to normal
→ Alarm cleared according to configured acknowledgement policy
```

Acknowledge는 운전자가 Alarm을 인지했다는 기록이다. 원인 제거, Process condition 해제 또는 설비복구를 의미하지 않는다.

## 8. Alarm philosophy와 rationalization

Alarm philosophy는 조직 전체에 적용하는 상위 정책이다. 역할, 우선순위, 표시, 색상, Acknowledge, Shelving, Suppression, KPI, 변경관리와 검토주기를 정한다.

Alarm rationalization은 각 Alarm 후보를 검토하는 활동이다.

| 항목 | 검토내용 |
|---|---|
| 원인 | 어떤 비정상 상태가 발생했는가 |
| 결과 | 조치하지 않으면 무엇이 발생하는가 |
| 조치 | 운전자가 어떤 행동을 해야 하는가 |
| 응답시간 | 조치가 유효한 최대시간은 얼마인가 |
| 우선순위 | 결과와 응답시간을 어떻게 반영하는가 |
| 설정 | Alarm value, Deadband와 Delay는 무엇인가 |
| 상태관리 | Shelving 또는 Suppression 허용조건은 무엇인가 |
| 근거 | 승인자, 문서와 변경이력은 무엇인가 |

## 9. Alarm priority

Priority는 측정값의 절대크기로 정하지 않는다.

```text
Priority = f(Consequence severity, Maximum operator response time)
```

결과가 심각하고 허용 응답시간이 짧을수록 높은 우선순위가 필요하다. 동일한 Priority는 표시, 음향, 대응절차와 교육에서 일관된 의미를 가져야 한다.

## 10. Deadband와 Delay

High alarm의 개념적 관계는 다음과 같다.

```text
발생:
PV ≥ SP_H 상태가 T_on 이상 지속

복귀:
PV ≤ SP_H - DB_H 상태가 T_off 이상 지속
```

- Deadband는 발생 임계값과 복귀 임계값 사이의 값 차이이다.
- Delay는 조건이 유지되어야 하는 시간이다.
- Deadband는 경계부 노이즈에 효과적이다.
- Delay는 짧은 일시변동에 효과적이다.
- 두 값이 너무 크면 실제 Alarm을 늦추거나 가릴 수 있다.

## 11. Shelving과 Suppression

| 구분 | Shelving | Suppression |
|---|---|---|
| 적용주체 | 권한 있는 운전자 | 설계된 자동논리 |
| Trigger | 알려진 일시적 사유 | 설비상태·운전모드·논리조건 |
| 기간 | 제한시간 | 조건이 참인 동안 |
| 기록 | 사용자, 사유, 시작, 만료 | Suppression 조건과 적용상태 |
| 핵심위험 | 무기한 은폐 | 잘못된 조건설계로 필요한 Alarm 누락 |

Shelving은 Alarm 정의와 이력을 삭제하지 않는다. Suppression은 운전자가 편의상 임의로 숨기는 기능이 아니다.

## 12. Alarm flood와 KPI

Alarm flood는 짧은 시간에 Alarm이 집중되어 운전자의 인지, 진단과 대응을 방해하는 상태이다. Chattering은 같은 Alarm이 반복 발생·해제되는 현상이다. Standing alarm은 장기간 Active 상태로 남아 정상 배경처럼 인식되는 Alarm이다.

개선순서는 다음과 같다.

```text
원인설비와 신호품질 개선
→ 불필요 Alarm 제거
→ Rationalization 재검토
→ Deadband·Delay 조정
→ 상태기반 Suppression
→ 화면·절차 개선
→ KPI 재평가
```

KPI 수치는 현장 Alarm philosophy에 따라 정한다. 시간당 발생률, Peak rate, Flood 구간, Standing·Chattering alarm, 우선순위 분포와 Shelving 사용현황을 추적한다.

## 13. Setpoint·Alarm·Trip·Interlock 값

| 값 | 목적 | 일반 소유 |
|---|---|---|
| 운전 Setpoint | 목표 운전값 | 운전·공정 제어 |
| Alarm value | 운전자 조치 촉구 | Alarm 관리 |
| Trip value | 자동 보호정지 | 보호논리 |
| Interlock value | 동작허용·금지 조건 | 실행 제어논리 |

상승방향 위험변수에서는 정상운전범위, Alarm과 Trip 사이에 운전자 응답과 공정동특성을 고려한 여유를 둘 수 있다. 그러나 상대순서는 위험방향과 논리에 따라 달라지므로 모든 공정에 하나의 숫자순서를 강제하면 안 된다.

Setpoint list에는 Tag, 기능, 값, 단위, 방향, Deadband·Delay, 적용모드, 근거, 승인자, 변경이력과 관련 보호기능 참조를 포함한다.

## 14. SOE, Historian, First-out과 Audit trail

SOE event는 다음 정보로 표현할 수 있다.

```text
e_i = (Source timestamp, Signal source, Old state, New state, Quality)
```

SOE의 선후관계를 신뢰하려면 장치의 시각동기, Timestamp 생성위치, 정확도, 분해능, 통신지연과 Time quality를 관리해야 한다.

| 기능 | 기록대상 | 주목적 |
|---|---|---|
| Historian | 공정값과 Trend | 장기 추세·성능 분석 |
| SOE | 이산 상태변화 | 사건 선후관계 분석 |
| First-out | 최초 유효 원인 | 빠른 초기원인 지시 |
| Audit trail | 사용자 행위와 변경 | 권한·책임·변경 추적 |

## 15. 운전자 권한과 Human error 방지

권한은 역할기반 최소권한으로 설계한다. 중요 Setpoint 변경, Shelving, Suppression 승인과 보호관련 조작은 재확인, 이중승인 또는 별도 권한이 필요할 수 있다.

Human error 방지를 위해 다음을 제공한다.

- 현재 Local·Remote와 Manual·Auto 상태
- 명령 소유권과 조작가능 여부
- Interlock·Permissive 불만족 사유
- 조작대상과 예상결과의 명확한 표시
- 중요조작 확인과 취소 경로
- Command 전송과 실제 Feedback 분리
- Timeout, 불일치와 Bad quality 표시
- 복구와 Rollback 절차

## 16. Abnormal situation management

```text
Detect
→ Diagnose
→ Respond
→ Recover
→ Review
```

Overview와 Trend로 이상을 조기에 발견한다. Alarm, SOE와 공정맥락으로 원인을 진단한다. 권한과 절차에 따라 대응한다. 실제 Feedback과 품질을 확인하며 복구한다. 사후에는 Alarm KPI, SOE와 Audit trail로 반복원인을 개선한다.

## 17. 대표 Fatal 오류

1. 모든 Event를 Alarm으로 구성한다.
2. Alarm, Trip과 Interlock을 같은 기능으로 본다.
3. Acknowledge가 공정원인을 해제한다고 본다.
4. Priority를 측정값 크기만으로 정한다.
5. Deadband와 Delay를 같은 기능으로 본다.
6. Shelving이 Alarm 이력을 삭제한다고 본다.
7. Suppression과 Shelving를 동일시한다.
8. Shelving를 무기한 유지한다.
9. 네 종류의 값을 서로 바꾸어 사용한다.
10. 시각동기 없이 SOE 순서를 신뢰한다.
11. Historian이 SOE를 항상 대체한다고 본다.
12. Audit trail과 SOE를 동일시한다.
13. 밝은 색을 많이 쓸수록 좋은 HMI라고 본다.
14. 모든 값을 무제한 변경하도록 허용한다.
15. HMI 명령이 현장동작 완료를 증명한다고 본다.
16. 모든 Alarm의 Priority를 높여 Flood를 해결한다.

## 18. Warn 수준 부족사항

- HMI·SCADA 구성요소만 나열하고 정보신뢰성을 누락함
- 색상만 설명하고 화면계층과 Trend를 누락함
- Rationalization에서 운전자 조치와 응답시간을 누락함
- Deadband, Delay, Shelving과 Suppression의 차이를 누락함
- Setpoint list의 근거, 권한과 변경이력을 누락함
- SOE에서 시각동기와 Time quality를 누락함
- 권한에서 Audit trail과 중요조작 확인을 누락함
- 비정상상황의 복구와 사후검토를 누락함

## 19. False positive 방지

직접적인 반대 단정문만 Fatal 후보로 본다. Alarm이 Trip을 유발할 수 있다는 설명은 두 기능을 동일시한 것이 아니다. Shelving이 화면에서 숨긴다는 설명도 이력 삭제 주장과 다르다. High-performance HMI는 색상을 전혀 사용하지 않는 방식이 아니라 제한된 의미로 사용하는 방식이다.

## 20. Model Answer 권장 흐름

1. 운전정보 관리의 목적과 ownership
2. HMI·SCADA 구조와 정보신뢰성
3. High-performance HMI와 화면계층
4. Alarm 철학·합리화·우선순위
5. Alarm 상태와 nuisance 관리
6. Setpoint·Alarm·Trip·Interlock 값 관리
7. SOE·Historian·First-out·Audit trail
8. 권한·Human error·비정상상황 대응

## 21. 대표 출제문제

1. HMI와 SCADA의 구조, 기능 및 신뢰성 설계기준을 설명하시오.
2. High-performance HMI의 설계원칙과 화면계층을 설명하시오.
3. Alarm philosophy와 Alarm rationalization의 목적 및 절차를 설명하시오.
4. Alarm priority, Deadband와 Delay의 선정기준을 설명하시오.
5. Alarm Shelving과 Suppression의 차이와 관리방안을 설명하시오.
6. Setpoint, Alarm value, Trip value와 Interlock value의 차이 및 관리기준을 설명하시오.
7. SOE의 원리와 시각동기, Historian 및 First-out과의 관계를 설명하시오.
8. 운전정보 시스템의 Audit trail과 운전자 권한 관리방안을 설명하시오.
9. Alarm flood와 Chattering의 문제점 및 개선방안을 설명하시오.
10. HMI·SCADA를 이용한 Abnormal situation management 방안을 설명하시오.

## 22. Focused regression 범위

- Topic ID와 schema contract
- Anchor ID 중복과 필수 의미군
- Fatal·Major·False-positive count
- Model Answer의 Anchor 참조 무결성
- 넓은 단일 Routing alias 배제
- SW-02·SW-04·SW-10 경계
- Alarm Active·Acknowledge 관계
- Deadband·Delay 논리
- Priority 결정요소
- SOE Timestamp와 시각동기
- 직접 오답 패턴과 명시적 정정문 구분
