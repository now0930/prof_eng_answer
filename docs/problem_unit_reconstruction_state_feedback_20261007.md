# 상태피드백 기준입력 추종 Topic Pack 문제 단위 감사 — 2026-10-07

## 판정

`state_feedback_reference_tracking_prefilter_integral_action`은 상태피드백 안정화와 기준입력
추종, DC prefilter, integral servo, 두 방법의 비교, observer/포화/구현 검증을 잇는 문제군이다.
다섯 대표 질문을 별도 pattern으로 유지한다. 서로 다른 설계문제를 한 답안의 보편 필수 목록으로
합치지 않는다.

## Coverage 및 Anchor 조정

- 초기 14개 Anchor 중 required union은 12개(85.7%, 감사 screen 반올림 86%)였다.
- `state_tracking_pole_placement_tracking_distinction`을 패턴 1(기준입력 추종·정상상태 오차
  보상)에 연결했다. 해당 질문에서 안정화용 pole placement와 추종 정확도를 혼동하면 핵심 요구를
  잘못 설명하게 된다.
- `state_tracking_robustness_noise_gain_tradeoff`를 패턴 5(observer 기반 추종에서 saturation,
  anti-windup과 검증항목)에 연결했다. 노이즈, 제어입력 및 강인성은 이 검증 질문에 직접 관련된다.
- required union은 14/14가 되었다. 나머지 패턴에 위 두 항목을 공통 필수요건으로 더하지 않았다.
- 8개 recommended outline은 14개 Anchor 모두를 이미 참조하며 누락/미해결 참조가 없다.

## 범위 조정

14개 `high_score_points`, 12개 `common_missing_points`, 8개 high-band unlock 조건을 각각
패턴 번호로 제한했다. 핵심 적용은 다음과 같다.

| 패턴 | 필수 평가 초점 |
|---|---|
| 1 | 안정화와 기준입력 추종 구분, 정상상태 오차보상의 큰 틀 |
| 2 | SISO·D=0 등 적용조건 아래 `N_r` 정상상태 유도와 존재성 |
| 3 | 적분 내부모델, 확대상태 구성 및 가제어성/안정화 가능성 |
| 4 | Prefilter와 integral feedback의 역할, 기준입력과 외란 경로 비교 |
| 5 | Observer 전제, saturation/anti-windup, 노이즈·강인성·이산 구현 검증 |

따라서 패턴 2에서 적분 확대행렬을 쓰지 않았거나 패턴 3에서 `N_r`을 유도하지 않았다는 이유만으로
감점하지 않는다. Fatal은 해당 오개념 주장이 실제 답안에 있을 때만 적용한다. 이는 source Pack과
Topic Sheet의 계약 명료화이고 runtime pattern score gate를 새로 구현한 것은 아니다.

## 검증 결과

- `scripts/test_state_feedback_reference_tracking_scope.py`: PASS (3 tests)
- `validate_topic_packs.py --topic-id ...`: PASS; global uniqueness 포함 2,066 Anchor 검사
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS; errors 0, warnings 0
- `audit_topic_pack_atomicity.py --topic-id ...`: PASS; errors 0, warnings 0
- `validate_topic_pack_release.py --topic-id ... --require-logic-check`: PASS; generated pipeline PASS
- `git diff --check`: PASS
- 검증이 임시 생성한 `rubrics/generated/` 산출물은 사전 snapshot으로 복원했다.

## 변경 파일

- `rubrics/topic_packs/state_feedback_reference_tracking_prefilter_integral_action/model_answer.json`
- `rubrics/topic_packs/state_feedback_reference_tracking_prefilter_integral_action/topic_importance.json`
- 해당 Topic Pack README와 Topic Sheet
- `scripts/test_state_feedback_reference_tracking_scope.py`
- `docs/topic_pack_reorganization_progress_20261007.md`, `docs/README.md`

Grader A/B/C/D/E·deterministic score·Question Type/Router·fatal IDs·Golden tests·release gates는
수정하지 않았다. 작업 전부터 존재한 기타 worktree 변경은 보존했다.
