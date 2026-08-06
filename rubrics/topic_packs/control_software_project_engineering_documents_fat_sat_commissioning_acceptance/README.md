# 제어 소프트웨어 프로젝트, 설계문서, FAT·SAT·시운전 및 인수

## Topic ID

`control_software_project_engineering_documents_fat_sat_commissioning_acceptance`

## 목적

이 Topic Pack은 산업계측제어기술사 답안에서 제어 소프트웨어 프로젝트의 문서와 시험단계를 단순 나열하지 않고 요구사항, 설계, FAT·SAT, 현장시험, 시운전, 성능시험, 인수와 인계를 하나의 추적 가능한 폐루프로 설명하는지를 평가한다.

## 소유범위

- Feasibility, Scope, Schedule, Cost
- Control philosophy, URS, FRS, FDS, SDS
- I/O·Tag·Alarm·Interlock list, Cause & Effect, Logic diagram
- Test specification, FAT, SAT, Loop test, Site integration test
- Commissioning, Performance test, Acceptance
- Punch list, As-built, Handover, 구성·백업·복구

## 경계

- 일반 SW lifecycle·V-Model·V&V는 SW-04
- Interlock·Trip의 실제 논리 메커니즘은 SW-02
- Alarm philosophy·SOE 운전정보 원리는 SW-03
- SW-10은 프로젝트 산출물과 현장 검증·계약 인수를 소유한다.

## 채점 핵심

1. URS→FRS→FDS→SDS→시험의 양방향 추적
2. FAT와 SAT의 환경·검출결함·한계 비교
3. Loop·Site integration·Commissioning의 대상과 순서
4. 정량 Performance test와 Acceptance 조건
5. Punch closure·As-built·Handover·backup 증적
6. 변경영향·baseline 갱신·재시험 폐루프

## 파일

- `fact_anchor.json`: 핵심 사실과 fatal wrong claims
- `logic_check.json`: deterministic 보조패턴과 LLM 의미검사 계약
- `model_answer.json`: 대표 문제, 답안 구조와 routing 정보
- `topic_importance.json`: 난이도와 고득점 조건
- `docs/topic_sheets/control_software_project_engineering_documents_fat_sat_commissioning_acceptance.md`: 상세 설계서
- `scripts/test_control_software_project_fat_sat_commissioning_acceptance.py`: focused regression

## 검증 경계

이 Topic-local 단계에서는 JSON, source schema, Topic quality, focused test, diff와 Lane ownership만 검증한다. generated rebuild와 전체 release 검증은 main 통합 단계에서 수행한다.
