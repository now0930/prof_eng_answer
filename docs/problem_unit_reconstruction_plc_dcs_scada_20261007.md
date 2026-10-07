# PLC·DCS·SCADA 아키텍처 Topic Pack 문제 단위 감사 — 2026-10-07

대상: `plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability`
유형: 10개 문항 intent 및 pattern별 피드백 범위 감사

## 판정

26개 Anchor와 10개 예상문항은 PLC/DCS/SCADA 제어시스템 아키텍처와 availability engineering이라는 공통 시스템 경계 안에 있다. Screen 및 atomicity audit에서 disconnected question family 경고가 없어 Topic을 분리하거나 Anchor를 추가하지 않았다. Pattern 10만 아키텍처·RAM·CCF·시험수용을 종합하는 질문으로 유지한다.

## 발견 및 보완

- 기존 10개 pattern의 `intent`가 각각 질문 문장을 그대로 반복했다. 각 intent를 플랫폼 선정, redundancy scope, state synchronization, Remote I/O 장애, RAM, SPOF/CCF, degraded recovery, fault-injection acceptance, 비용 trade-off, 통합 설계의 답안 목적에 맞춰 구체화했다.
- 26/26 Anchor는 기존부터 적어도 한 expected pattern에서 필수로 참조되었고 question examples도 pattern과 일치했다. Required-anchor set은 변경하지 않았다.
- `high_score_points`, `common_missing_points`, `high_band_unlock_conditions`가 10개 문항에 전역 적용되는 것처럼 읽힐 수 있었다. 각 조건에 적용 문항 번호를 명시했다. RAM 식은 pattern 5/10, FAT·SAT 수용기준은 8/10 등 해당 요구가 있는 문항에서만 평가한다.
- out-of-scope Alarm·통신·SIL·프로젝트 영역을 “누락점”에 둬 불필요한 감점 근거로 오용될 수 있는 항목을 common-missing에서 제거했다. 인접 Topic 경계 설명은 README/Topic Sheet에 유지했다.
- L0–L3는 저장소 학습 계층이며 공식 분류가 아님을 Topic Sheet에 표시했다. importance note도 `CORE_MUST_PREPARE`를 편집상 우선순위로 규정하고 반복 출제빈도를 주장하지 않도록 정리했다.

## 보호한 범위

- Question Type `COMPARE_SELECTION`, Topic aliases, fatal IDs, 기존 generated anchor inventory와 release projection 계약을 변경하지 않았다.
- Fact Anchor 26개, fatal 12개, routing authority, deterministic scoring 및 A/B/C/D/E 점수 계약은 그대로다.
- 예상문제는 기존 지식 기반 문제 패턴이지 실제 기출·공식 식별자로 표현하지 않았다.

## 검증

- `scripts/test_plc_dcs_scada_remote_io_architecture_redundancy_topic.py`: 18/19 tests pass; the remaining existing inventory assertion fails because 87 source Topic directories do not match the checked-in generated manifest count of 82. The test and manifest were not altered to mask this mismatch.
- `validate_topic_packs.py --topic-id ...`: PASS
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS
- `audit_topic_pack_atomicity.py --topic-id ... --json`: PASS; disconnected family warning 없음
- `validate_topic_pack_release.py --topic-id ... --require-logic-check`: PASS; smoke 생략
- Release validator가 `rubrics/generated/`를 사전 snapshot으로 복원했다. Projection promote는 하지 않았다.
- The inventory mismatch is independent of this source edit and remains a separate generated-inventory reconciliation item.
- `git diff --check`: PASS

## 남은 검토

이번 변경은 문항별 표현 및 source 피드백 범위 정리다. 특정 PLC/DCS 제품별 절체 성능, SIL 또는 네트워크 지연 수치의 설계는 Topic 질문에 해당할 때만 별도 기술 근거와 함께 보완한다.
