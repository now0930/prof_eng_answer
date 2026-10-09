# SW-06 형상·변경·복구 Topic Pack 문제 단위 재구성

갱신: 2026-10-07
Topic ID: `configuration_change_release_backup_rollback_migration_obsolescence_management`

## 판정과 범위

40 Anchor를 가진 Pack은 11개 예상문항으로 이루어진 넓은 SW-06 운영 수명주기 문제 family다. 전수 atomicity audit은 error 0, `LARGE_ANCHOR_INVENTORY` warning 1을 냈다. 내용은 운영 형상/MOC/Release, Backup·복구, Migration·Cutover, Legacy·Obsolescence 및 종속성 관리의 여러 질문 유형으로 갈린다. 이들은 공통적으로 운영 중 승인 형상과 운전연속성을 관리하지만 단일 시험문제 하나의 필수 답안으로 합쳐서는 안 된다.

이번 단계에서는 기존 Topic ID, canonical router, `question_demand_axes.json`의 별도 activation/owner 계약을 바꾸지 않았다. 11개를 서로 구분되는 예상문항으로 명확히 표현하고 pattern-local requirements를 적용했다. 이후 Stage 6의 owner/view 영향분석에서 하위 pack 분리가 기존 router 및 question-demand contract를 바꿔야 하는지 다시 판정한다. 이 검토 전까지 분리 후보를 승인된 새 topic처럼 만들지 않는다.

## 확인 결과와 수정

- Source에는 11 expected patterns가 있었지만 README/Topic Sheet/question_examples에는 10개만 있었고 여러 `pattern` 값도 질문이 아니라 “묻는 문제”라는 설명이었다. 11개 모두 직접 답할 수 있는 기술사형 질문 문장으로 통일하고 question_examples와 pattern 목록을 일치시켰다.
- Required Anchor union은 39/40 (97.5%). 유일한 미포함 Anchor인 `sw06_irreversible_change_forward_recovery`는 변경이 비가역적인 경우의 대책으로서 모든 Backup/Rollback 질문에서 필수라고 볼 수 없어 선택 지식으로 유지했다.
- 기존 outline은 backup scope 및 DR objectives Anchor가 빠져 있었다. 두 Anchor를 학습 outline에 추가해 40/40 연결로 맞췄다.
- Pattern 1에는 문서·교육 갱신 Anchor를 추가하고, 긴급변경 사후 검토 Anchor는 전용 Pattern 10에만 남겼다. MOC 질문 Pattern 3에서도 긴급변경 상세를 필수화하지 않았다.
- 고득점, common-missing, LLM major checks 및 high-band unlock 조건 모두 적용 pattern 번호를 명시했다. 해당 pattern 밖의 누락은 문제에서 요구하지 않은 한 오류·감점 근거가 아니다.
- 종합 모범답안은 전체 학습 reference임을 README/Topic Sheet에 표시했다. 모든 문항에서 종합답안 전체를 다시 쓰게 하는 요구는 두지 않았다.
- 기존 4-clause question demand bridge는 유지했다. 이는 all activation term groups(PLC/DCS, release, backup, rollback, regression)가 함께 있는 경우에만 별도 canonical requirements를 제공하며 이번 문제패턴들의 일반 공통조건으로 확장하지 않는다.
- SW-04 개발 V&V와 SW-09 사이버사고 대응 구분은 Pattern 11에서만 직접 평가한다. 다른 문항에서 이 경계 설명을 생략했다는 사실만으로 결함 처리하지 않는다.

## Source/version 확인 메모

- [ISO 10007:2017](https://www.iso.org/standard/70400.html): configuration management guidance. 발행 중인 현행 edition이며 ISO catalog상 개정 단계가 진행 중이다.
- [IEC 62402:2019](https://webstore.iec.ch/en/publication/59531): Obsolescence management requirements and guidance.
- [NIST SP 800-82 Rev.3](https://csrc.nist.gov/pubs/sp/800/82/r3/final): final publication/reference used in the pack.
- [NIST SP 800-82 Rev.4 initial public draft](https://csrc.nist.gov/pubs/sp/800/82/r4/ipd): 2026-09-21 published draft; not a final replacement as of this audit.
- [NIST SP 1339](https://csrc.nist.gov/pubs/sp/1339/final): final OT Backup Quick Start Guide, June 2026; supports integration of backups with change/recovery practices and recurring restore testing.

Edition/status checks are source maintenance information, not grading requirements. They were checked against official ISO, IEC and NIST catalog pages on 2026-10-07.

## 변경하지 않은 계약

- A/B/C/D/E, deterministic score/fatal handling, Question Type and topic routing authority.
- Topic ID and classification, Fact Anchor IDs, 20 fatal IDs, 12 major-check count and C-only affected layer.
- Existing `question_demand_axes.json`, generated rubric banks, common router and release gate definitions.
- SW-06 broad owner taxonomy pending the planned Stage 6 analysis.

## 검증

- Focused SW-06 tests: PASS 42/42.
- Topic Pack source schema: PASS (87 packs and 2,066 global anchors checked).
- Topic Pack quality: PASS (0 errors, 0 warnings).
- Topic Pack atomicity: PASS with 0 errors and one remaining `LARGE_ANCHOR_INVENTORY` warning (40 anchors).
- Scoped generated release: PASS; generated pipeline/quality passed and six generated banks were restored to their pre-validation snapshot.
- No full repository regression or commit in this turn; unrelated worktree changes remain.
- Focused/release logs: `/tmp/sw06_topic_release_20261007.log` (focused test output was returned directly in the run).
