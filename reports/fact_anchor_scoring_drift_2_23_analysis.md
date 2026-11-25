# 두 기술 문안의 143건 재생 채점 영향 분석

## 범위와 재현 고정값

이 분석은 PR #47 HEAD `243562b351fc567bf3cd687b3da65d454c699557`의 결정론적 채점 경로에서 수행한 격리 비교다. 개인 답안 원문은 비공개 입력 경로에서만 사용했고, 이 문서에는 답안 본문이나 원문 excerpt를 싣지 않는다. 기준 재생 결과는 143건이며 SHA-256 `a2825370ef80f61b2d5c3fa55a765ad811f7a8401e6e8590a41e9d663ab16693`로 기존 `actual-final-143.jsonl`과 바이트 단위로 일치했다. 후보는 동일 코드 SHA에서 두 Anchor의 `statement`, `claim`, 첫 accepted explanation만 제안 문안으로 바꾼 격리본이며 Generated 6개는 공식 `scripts/build_generated_rubrics.py`로 재생성했다. 후보 출력 SHA-256 `1a4faae39f46ce2ae6dce8ef693fcc61039a9f8b97e9e286cfe3b6fb865a3423`; 격리 후보 Fact Anchor SHA-256 `7d96e9897b41ad82c92b4be9e5e0d5a511c5bd68f02542e72a3d43b5139d0082`. 입력·결과는 공개 저장소에 추가하지 않았다.

대상: `deenergized_energized_test_condition`, `partial_stroke_test_risk_controls`. 동일 143개 입력에서 후보에 따라 **B가 바뀐 사례 23/143**를 전부 기록한다. 사례 ID는 공개 텍스트 없이 cohort/Anchor/case-kind 조합으로 익명화했다. span은 답안의 0-based `[start:end)` 위치만 나타낸다.

## 실측 요약

| 지표 | 실측 |
|---|---:|
| 영향 받은 사례 | 23 / 143 |
| Requirement state 변경 | 0 / 23 (23건 모두 MISSING 유지) |
| B 변화 | 16건 증가, 7건 감소; 총 변화 +2.25점(사례별 B 합) |
| 최종 total_score 변화 | 14건: +0.60 5건, +0.25 5건, −0.60 2건, −0.30 2건; 9건은 score floor로 최종 점수 변화 없음 |
| A / C / D / E 변화 | 각각 0건 |
| Routing / verdict / ceiling / Fatal / resolution review 변화 | 각각 0건 |
| 근거 span | 16건 새 span, 7건 기존 span 제거; Requirement state는 모두 MISSING |

## 사례별 차이

| Case ID | 영향 받은 Requirement | span 이전 → 후보 | B 이전 → 후보 (Δ) | total 이전 → 후보 (Δ) |
|---|---|---|---:|---:|
| `frozen/fail_action_vs_safe_state/case-4` | `deenergized_energized_test_condition` (MISSING→MISSING) | `∅` → `0:74` | 1.80 → 2.40 (+0.60) | 8.40 → 9.00 (+0.60) |
| `frozen/imperfect_test_residual_risk/case-1` | `partial_stroke_test_risk_controls` (MISSING→MISSING) | `∅` → `0:95` | 2.00 → 2.25 (+0.25) | 8.00 → 8.25 (+0.25) |
| `frozen/imperfect_test_residual_risk/case-2` | `partial_stroke_test_risk_controls` (MISSING→MISSING) | `∅` → `0:63` | 1.50 → 1.75 (+0.25) | 11.00 → 11.25 (+0.25) |
| `frozen/imperfect_test_residual_risk/case-3` | `partial_stroke_test_risk_controls` (MISSING→MISSING) | `∅` → `0:36` | 1.00 → 1.25 (+0.25) | 7.00 → 7.00 (+0.00) |
| `frozen/imperfect_test_residual_risk/case-4` | `partial_stroke_test_risk_controls` (MISSING→MISSING) | `∅` → `0:73` | 1.50 → 1.75 (+0.25) | 11.50 → 11.75 (+0.25) |
| `frozen/response_time_process_safety_time/case-3` | `deenergized_energized_test_condition` (MISSING→MISSING) | `0:44` → `∅` | 2.40 → 1.80 (-0.60) | 11.90 → 11.30 (-0.60) |
| `frozen/response_time_process_safety_time/case-4` | `deenergized_energized_test_condition` (MISSING→MISSING) | `0:71` → `∅` | 2.40 → 1.80 (-0.60) | 11.90 → 11.30 (-0.60) |
| `frozen/response_time_process_safety_time/case-5` | `deenergized_energized_test_condition` (MISSING→MISSING) | `0:69` → `∅` | 1.80 → 1.20 (-0.60) | 7.30 → 7.00 (-0.30) |
| `frozen/response_time_process_safety_time/case-6` | `deenergized_energized_test_condition` (MISSING→MISSING) | `0:50` → `∅` | 1.80 → 1.20 (-0.60) | 7.30 → 7.00 (-0.30) |
| `new/fail_action_vs_safe_state/case-1-positive` | `deenergized_energized_test_condition` (MISSING→MISSING) | `∅` → `0:80` | 2.40 → 3.00 (+0.60) | 12.40 → 13.00 (+0.60) |
| `new/fail_action_vs_safe_state/case-2-positive` | `deenergized_energized_test_condition` (MISSING→MISSING) | `∅` → `0:57` | 2.40 → 3.00 (+0.60) | 13.10 → 13.70 (+0.60) |
| `new/fail_action_vs_safe_state/case-3-positive` | `deenergized_energized_test_condition` (MISSING→MISSING) | `∅` → `0:65` | 1.80 → 2.40 (+0.60) | 7.30 → 7.90 (+0.60) |
| `new/fail_action_vs_safe_state/case-5-negative` | `deenergized_energized_test_condition` (MISSING→MISSING) | `∅` → `0:38` | 1.20 → 1.80 (+0.60) | 4.50 → 4.50 (+0.00) |
| `new/imperfect_test_residual_risk/case-1-positive` | `partial_stroke_test_risk_controls` (MISSING→MISSING) | `∅` → `0:62` | 1.00 → 1.25 (+0.25) | 7.00 → 7.00 (+0.00) |
| `new/imperfect_test_residual_risk/case-2-positive` | `partial_stroke_test_risk_controls` (MISSING→MISSING) | `∅` → `0:86` | 1.25 → 1.50 (+0.25) | 11.25 → 11.50 (+0.25) |
| `new/imperfect_test_residual_risk/case-4-negative` | `partial_stroke_test_risk_controls` (MISSING→MISSING) | `∅` → `0:47` | 0.75 → 1.00 (+0.25) | 4.50 → 4.50 (+0.00) |
| `new/response_time_process_safety_time/case-2-positive` | `deenergized_energized_test_condition` (MISSING→MISSING) | `0:79` → `∅` | 1.20 → 0.60 (-0.60) | 4.50 → 4.50 (+0.00) |
| `new/response_time_process_safety_time/case-5-negative` | `deenergized_energized_test_condition` (MISSING→MISSING) | `0:45` → `∅` | 0.60 → 0.00 (-0.60) | 4.50 → 4.50 (+0.00) |
| `prior/fail_action_vs_safe_state/negative` | `deenergized_energized_test_condition` (MISSING→MISSING) | `∅` → `0:50` | 0.60 → 1.20 (+0.60) | 4.50 → 4.50 (+0.00) |
| `prior/fail_action_vs_safe_state/positive` | `deenergized_energized_test_condition` (MISSING→MISSING) | `∅` → `0:68` | 1.80 → 2.40 (+0.60) | 8.40 → 9.00 (+0.60) |
| `prior/imperfect_test_residual_risk/negative` | `partial_stroke_test_risk_controls` (MISSING→MISSING) | `∅` → `0:35` | 0.50 → 0.75 (+0.25) | 4.50 → 4.50 (+0.00) |
| `prior/imperfect_test_residual_risk/positive` | `partial_stroke_test_risk_controls` (MISSING→MISSING) | `∅` → `0:63` | 1.50 → 1.75 (+0.25) | 12.00 → 12.25 (+0.25) |
| `prior/response_time_process_safety_time/negative` | `deenergized_energized_test_condition` (MISSING→MISSING) | `0:42` → `∅` | 0.60 → 0.00 (-0.60) | 4.50 → 4.50 (+0.00) |

## 원인 및 기술적/채점 해석

변화는 사실 관계 판정에서 나오지 않았다. 두 제안 문장의 용어 집합이 해당 Topic의 lexical Anchor term matching을 바꿨고, 문장 span이 생기거나 사라졌다. `grading/evidence/fact_anchor_evidence_adapter.py`의 `_terms`와 `evaluate_fact_anchor_requirements`는 lexical span을 저장한다. `grading/scoring/deterministic_score_engine.py`의 `_scoring_groups`는 `MISSING` 상태여도 `evidence_text`, `source_span` 또는 claim ID가 있으면 `grounded_attempt`로 보고 `coverage_status=PARTIAL`을 주며, B는 그 coverage ratio로 계산한다. 즉, 문장 후보는 Claim 관계 상태를 바꾸지 않고 B의 시도 커버리지만 움직였다.

이 23건 중 “공정 fail action/safe-state 답변에 테스트 요구의 B를 더 준 7건”과 “PST 응답시간 답변에서 테스트 요구 근거를 제거해 B를 낮춘 7건”, “잔여 고장모드 답변에 online PST control 요구의 B를 더 준 9건”은 서로 다른 평가 방향이다. 일부 답안은 인접 주제를 실제로 다뤄 B의 시도 점수가 합리적일 수도 있다. 반면 universal 오답 2건도 후보 span을 얻어 B가 올라간 점, residual-risk 설명이 PST-control 요구와 동일하지 않은 점은 단순 lexical grounding으로 정당화되지 않는다. 따라서 현재 증거로 23건 중 어느 것도 기술적 정오에 따른 점수 교정이라고 확정하지 않는다. 가장 보수적 결론은 **span 민감도에 따른 미확정 B drift**다.

## 결론 및 처리

- 두 문안은 기존 문구로 되돌린 채 보류한다. 이번 후보 실험 worktree는 PR branch에 반영하지 않았다.
- 정본 문장을 바꾼다는 이유만으로 B 변화가 부당하다고 일반화하지 않는다. 다만 이 재현에서는 상태, 관계, 오류 판단이 그대로인데 span만 달라졌다. 23건 모두 개별 증거 의미를 보기 전에는 정당한 교정으로 승인할 수 없다.
- 기존 scorer 변경 또는 전역 lexical rule 추가는 수행하지 않았다. score projection 결함 여부를 확정하려면 B “attempt coverage”의 근거 기준을 소유자가 별도 검토해야 한다. 이번 기술 정합성 요청에서 채점기 구조를 바꾸지 않는다.
- 적용 전 상태와 최종 PR #47 branch 상태는 143건 재생 SHA가 동일하다. 즉 제안은 미적용이고 기존 결과 영향은 없다.

