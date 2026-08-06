# 계측제어 소프트웨어 수명주기, V-Model, 추적성, 검증 및 확인

## Topic ID

`instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`

## 목적

이 Topic Pack은 일반 계측제어 소프트웨어의 요구사항, 아키텍처, 상세설계, 구현, 시험, 추적성, 결함·변경관리와 승인 증적을 V-Model의 하나의 흐름으로 평가한다.

## 포함 범위

- Requirement specification과 시험 가능한 acceptance criteria
- System architecture와 Software architecture
- Detailed design과 Coding standard
- Unit test, Integration test와 System test
- Verification과 Validation
- Requirement Traceability Matrix의 양방향 추적
- Static analysis, Dynamic analysis와 Regression test
- Simulation, HIL과 Fault injection
- Defect management, Change impact와 Configuration baseline
- Review, Approval, Exit criteria와 V&V evidence

## ownership 경계

- SW-04 소유: 일반 계측제어 SW lifecycle, V-Model, 추적성, 개발단계별 V&V
- SW-05 이관: SIS Safety Integrity, 독립성, 체계적 고장 통제와 Safety V&V
- SW-10 이관: 프로젝트 문서 인도, FAT·SAT·Loop test·시운전·Acceptance·Handover
- SW-03 이관: HMI·SCADA Alarm·SOE와 운전자 정보관리
- SW-02 이관: Sequence·Interlock·Trip의 실제 상태전이와 Fail-safe 운전논리

## 핵심 논리관계

```text
Verification = 산출물이 해당 단계 명세와 설계기준에 맞는가
Validation   = 통합 시스템이 의도된 사용목적과 사용자 요구를 충족하는가

RTM:
Requirement
  ↔ Architecture
  ↔ Detailed design
  ↔ Code
  ↔ Test case
  ↔ Test result

V-Model 대응:
Requirement / intended use ↔ System test / Validation
System·SW architecture     ↔ Integration test
Detailed design / module   ↔ Unit test
```

단위시험 통과는 통합시험과 시스템시험을 대체하지 않는다. 정적분석은 비실행 분석이고 동적분석은 실행기반 분석이다. 회귀시험은 변경된 기능뿐 아니라 영향받는 기존 기능과 인터페이스를 확인한다.

## 대표 오답

- Verification과 Validation은 같은 활동이다.
- V-Model에서는 코딩 후 시험을 처음 계획한다.
- 한 방향 RTM만으로 양방향 추적성이 완성된다.
- 단위시험 통과가 통합·시스템시험을 대체한다.
- 정적분석은 프로그램을 실행한다.
- 회귀시험은 새 기능만 확인한다.
- Simulation은 현장과 항상 완전히 동일하다.
- HIL은 반드시 실제 생산설비를 가동해야 한다.
- 시험 실패 시 expected result를 실제 결과로 바꾸면 된다.
- 일반 SW V&V만으로 SIS SIL 충족이 자동 증명된다.

## 파일

- `fact_anchor.json`: 31개 Fact Anchor와 16개 Fatal 오답
- `logic_check.json`: deterministic aid, LLM truth schema, Major와 false-positive 기준
- `model_answer.json`: 대표 문제 10개, 답안구조 8개와 Routing 정보
- `topic_importance.json`: 난이도와 선택 중요도
- `docs/topic_sheets/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation.md`: 상세 Topic Sheet
- `scripts/test_instrumentation_control_software_lifecycle_v_model.py`: focused regression

## 검증 경계

Topic-local 단계에서는 JSON, source schema, Topic quality, focused test, Python compile, whitespace, `git diff --check`와 Lane A ownership만 검증한다. Generated rebuild, 전체 Router 회귀, cross-topic duplicate, validate-all, release validation와 container smoke는 최종 통합 단계로 넘긴다.
