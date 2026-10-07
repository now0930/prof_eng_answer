# Force-balance pressure transmitter 문제 단위 감사

검토일: 2026-10-07
대상: `pressure_transmitter_force_balance_null_detection`
범위: 대표 질문의 독립성, 필수 Anchor 연결, pattern별 채점범위 및 기존 pressure/DP Pack과의 소유 경계

## 판정

- Topic은 유지한다. Pattern 1은 pneumatic/electronic 구현 원리 비교, Pattern 2는 null-balance 원리의 장단점·현장적용 평가로 요구가 다르지만, 두 질문이 `force balance`와 `position-error null feedback` 공통기반을 공유한다. 별도 토픽으로 쪼갤 근거는 부족하다.
- 5개 Anchor가 두 예상문항의 required-anchor union 및 outline에 모두 연결된다. 추가 Anchor를 coverage 수치만을 위해 만들 필요가 없다.
- 핵심 정답 사실, fatal 오개념, Question Type, owner/routing, deterministic scoring은 변경하지 않았다.

## 수정

전역 `high_score_points`, `common_missing_points`, `high_band_unlock_conditions`가 구현 chain 비교와 현장 trade-off를 모든 질문에 요구할 여지가 있었다. 이를 Pattern 1과 Pattern 2에 각각 한정했다. Pattern 1은 pneumatic/electronic chain 비교, Pattern 2는 질문 맥락에 따른 진동·복잡성·전원 trade-off를 평가한다. intrinsic-safety는 명시된 적용 맥락이 있을 때만 요구한다.

두 pattern에 별도 intent를 작성하고 README와 Topic Sheet에도 채점 경계를 명시했다. 이전 압력계측 Pack은 general sensing principle의 소유자이며, 이 Pack은 force-balance/null-detector 작동 원리의 소유자다. DP manifold·bleed·정비는 해당 maintenance Pack에 남는다.

## 승인 상태

Pack은 변경 전에 `topic_status.json`에서 사람이 승인한 것으로 표시되어 있었다. 이번 source 수정으로 승인 당시 content hash와 현재 파일 해시가 달라진다. 승인 메타데이터를 새 내용에 맞춰 동기화하거나 재승인으로 표기하지 않았다. 시스템상 현재 변경분은 재검토 필요로 남겨야 한다. 기존 승인 이력을 지우지 않았다.

## 검증

- Focused regression: 3/3 PASS
- Topic Pack schema: PASS (전역 2,068개 anchor와 uniqueness 확인)
- Topic Pack quality: PASS (errors 0, warnings 0)
- Atomicity: PASS (errors 0, warnings 0)
- Scoped release: PASS; generated outputs는 validation 후 기존 snapshot으로 복원
- Approval metadata: `topic_pack_status.py` reports `status=approved`, `review_state=reviewed`, `changed=yes`. 승인 해시는 이번 수정본을 포함하지 않으므로 그대로 보존했고, 수정본을 새로 승인된 것으로 표시하지 않았다.
- 기존 Grader A/B/C/D/E, taxonomy, Router, fatal 및 deterministic scoring은 수정하지 않음

## 다음

Screen 순서에서 다음 후보는 `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`다. 상세 기록은 이번 Pack의 사람 재검토를 완료했다는 뜻이 아니며, 수정 후 stale 상태의 approval hash를 자동 승인 처리하지 않는다.
