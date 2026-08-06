# HMI·SCADA·Alarm·Setpoint·Trip·Interlock·SOE 및 운전정보 관리

## Topic ID

`hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management`

## 목적

이 Topic Pack은 HMI·SCADA, High-performance HMI, Alarm lifecycle, Alarm rationalization, Setpoint 관리, SOE, Audit trail, 운전자 권한과 비정상상황 대응을 하나의 운전정보 관리 체계로 평가한다.

## 포함 범위

- HMI·SCADA 구조와 데이터 품질
- High-performance HMI와 화면계층
- Alarm philosophy와 rationalization
- Priority, Acknowledge, Deadband와 Delay
- Shelving, Suppression, Alarm flood와 KPI
- Setpoint·Alarm·Trip·Interlock 값 관리
- SOE, Historian, First-out과 Audit trail
- Operator authority와 Human error prevention
- Abnormal situation management

## ownership 경계

- SW-03 소유: 운전자 정보, Alarm, Setpoint, SOE, Audit와 권한
- SW-02 이관: Trip·Interlock 실행논리, 상태전이, Latch·Reset와 Fail-safe
- SW-04 이관: V-Model, 추적성, 일반 SW Verification·Validation
- SW-10 이관: 프로젝트 문서 인도, FAT·SAT, 시운전와 Acceptance
- SW-05 이관: SIL, PFDavg·PFH와 Safety lifecycle

## 핵심 논리관계

```text
Alarm = abnormal condition requiring timely operator action
Priority = f(consequence severity, allowable response time)
High alarm active: PV ≥ SP_H for T_on
High alarm clear: PV ≤ SP_H - DB_H for T_off
SOE event = timestamp + source + state transition + quality
```

Acknowledge는 운전자 인지기록이며 Alarm condition 해제가 아니다. Deadband는 값 기반 이력폭이고 Delay는 시간 기반 필터이다. Shelving은 제한시간의 운전자 임시조치이고 Suppression은 설계된 상태조건에 따른 자동제외이다.

## 대표 오답

- 모든 Event는 Alarm이다.
- Alarm, Trip과 Interlock은 같은 기능이다.
- Acknowledge가 원인을 해제한다.
- Deadband와 Delay는 같은 기능이다.
- Shelving이 Alarm 이력을 삭제한다.
- 시각동기 없이도 SOE 순서는 항상 정확하다.
- Historian, SOE와 Audit trail은 같은 기록이다.
- 밝은 색을 많이 쓰는 HMI가 더 우수하다.
- HMI 명령 전송이 현장동작 완료를 증명한다.

## 파일

- `fact_anchor.json`: 31개 Fact Anchor와 16개 Fatal 오답
- `logic_check.json`: deterministic aid, LLM truth schema, Major와 false-positive 조건
- `model_answer.json`: 대표 문제 10개, 답안구조 8개와 Routing 정보
- `topic_importance.json`: 난이도와 선택 중요도
- `docs/topic_sheets/hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management.md`: 상세 Topic Sheet
- `scripts/test_hmi_scada_alarm_setpoint_soe_operator_information.py`: focused regression

## 검증 경계

Topic-local authoring 단계에서는 JSON, source schema, Topic quality, focused test, whitespace, `git diff --check`와 Lane A ownership만 검증한다. Generated rebuild, 전체 Router 회귀, cross-topic duplicate, validate-all, release validation와 container smoke는 최종 통합 단계로 넘긴다.
