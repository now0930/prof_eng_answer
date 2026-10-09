# SW-02 제어논리 Topic Pack 문제 단위 감사 — 2026-10-07

## 판정

`control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe`는 Sequence,
interlock/permissive/trip, shutdown/Cause & Effect, voting/first-out, bypass/override,
fail-safe/watchdog, restart/recovery와 PLC 구현상 주의점을 포괄하는 연결된 운전제어 문제군이다.
10개 대표 질문의 분리는 유지한다. 주제의 공통 운전논리라는 이유만으로 각 질문에 다른 하위
주제까지 답안으로 요구해서는 안 된다.

## Coverage와 필수/선택 판단

- 총 28개 Fact Anchor 중 24개가 최소 한 개 질문 pattern의 `required_anchor_ids`에 연결됨:
  24/28 = 85.7% (screen 표기 86%).
- 필수 union에 없는 4개는 `sw02_scope_operational_logic`, `sw02_state_entry_exit_actions`,
  `sw02_sw03_boundary`, `sw02_sw05_boundary`다.
- 소유범위 경계 3개는 문항 답변의 일반 필수 fact라기보다 scope control/reference이고,
  Entry/Exit action은 Sequence 세부 설계 지식이다. 대표 pattern 1은 상태전이·완료조건·이상전이
  방지를 묻지만 Entry/Exit action을 명시하지 않으므로 선택 지식으로 유지했다. Coverage 수치를
  위해 억지로 필수화하지 않았다.
- 8개 recommended outline이 기존대로 28개 Anchor를 모두 참조한다. 이는 학습용 종합 흐름이며
  개별 질문에서 모든 section을 요구하는 뜻이 아니다.

## 보완 사항

모델 답안의 10개 pattern별 required anchors는 의미상 타당해 보여 변경하지 않았다. 대신
문항 독립성을 보장하도록 다음 전역 목록을 pattern-scoped 문장으로 다시 작성했다.

- 16개 `high_score_points`
- 14개 `common_missing_points`
- 8개 `high_band_unlock_conditions`

각 항목에 적용 pattern 번호 또는 적용조건을 표시했다. SW-03(Alarm/SOE 운영정보), SW-05
(SIL·안전수명주기) 경계는 답안이 실제로 해당 소유범위로 이탈할 때만 판단하며, 경계 지식의
누락을 별도의 고득점 결손으로 보지 않는다.

이는 Topic Pack source와 검토 문서의 평가 범위 명료화다. 현재 grader runtime이 pattern별
점수 게이팅을 한다고 가정하지 않았고, A/B/C/D/E·deterministic scoring·Question Type·Router·
fatal IDs 또는 기존 test를 변경하지 않았다.

## 검증

- SW-02 focused regression `scripts/test_control_logic_sequence_interlock_permissive_trip_state_transition.py`: PASS (27 tests, including the new pattern-scope regression)
- `validate_topic_packs.py --topic-id ...`: PASS; global uniqueness 포함 2,066 anchors 검사
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS; errors 0, warnings 0
- `audit_topic_pack_atomicity.py --topic-id ...`: PASS; errors 0, warnings 0
- `validate_topic_pack_release.py --topic-id ... --require-logic-check`: PASS; generated pipeline PASS
- `git diff --check`: PASS
- 검증에서 임시 생성된 `rubrics/generated/`는 사전 snapshot으로 복원했다.

## 수정 파일과 repository 상태

- `rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/model_answer.json`
- `rubrics/topic_packs/control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe/topic_importance.json`
- 동 topic README 및 Topic Sheet
- `docs/topic_pack_reorganization_progress_20261007.md`, `docs/README.md`

작업 전부터 존재한 다른 Topic Pack 및 문서 수정은 건드리지 않았다. 전체 worktree가 이미
여러 unrelated 수정과 초안으로 dirty이므로 이번 작업은 개별 commit/push하지 않았다.
