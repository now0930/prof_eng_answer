# Golden Review: sil_target_operations_issue1

상태: `APPROVED`

근거:

- `calibration/sil_target_operations_overgrading_regression.json`
- `rubrics/topic_packs/sil_target_determination_risk_reduction_and_lifecycle/question_demand_axes.json`
- `rubrics/topic_packs/sil_target_determination_risk_reduction_and_lifecycle/logic_check.json`

## 요구 상태 제안

| 요구 ID | 현재 | 제안 | 근거 |
|---|---|---|---|
| system_scope_and_sil_role | PARTIAL | PARTIAL | SIS·SIF 관계는 언급했으나 SIL의 SIF별 위험 시나리오 할당이 불완전함 |
| risk_scenario_and_tolerable_target | PARTIAL | PARTIAL | 허용위험은 언급했으나 시나리오·safe state·결정방법 경계가 부족함 |
| existing_ipl_and_independence | MISSING | MISSING | IPL 적격성·독립성·중복 credit 설명이 없음 |
| required_rrf_and_target_sil | WRONG | WRONG | PFDavg 목표식을 빈도 곱으로 제시하여 차원과 방향이 틀림 |
| demand_mode_metric_selection | WRONG | WRONG | demand mode를 요구빈도가 아닌 고장 검출시점으로 구분함 |
| quantitative_verification_dimension | WRONG | WRONG | 전체 SIF 정량검증·target/achieved 구분이 없고 핵심 식이 틀림 |
| proof_test_diagnostics_reliability | PARTIAL | WRONG | 시험주기, PST와 MTTR의 역할을 직접 답했으나 핵심 판단이 틀림 |
| operations_moc_security_ai_lifecycle | PARTIAL | PARTIAL | AI·보안·형상관리는 다뤘으나 SRS·bypass·독립 V&V·재검증 연결이 부족함 |

## Finding ID·심각도 제안

| 현재 ID | 정규 rule ID | 현재 | 제안 |
|---|---|---:|---:|
| target_pfd_frequency_multiplication_dimension_error | fatal_target_pfd_frequency_product | fatal | fatal |
| demand_mode_confused_with_fault_detection | fatal_demand_mode_by_fault_detection | major | fatal |
| pst_claimed_to_reduce_mttr | fatal_pst_replaces_full_test_or_reduces_mttr | major | fatal |
| certificate_interval_treated_as_minimum_test_interval | fatal_certificate_interval_as_operating_minimum | major | fatal |

심각도 제안은 Topic Pack의 검증 규칙과 일치시킨 것이다. 네 항목 모두 문제의 핵심
결정·운영 판단을 반대로 만들 수 있으므로 major/fatal 탐지 평가에서는 positive label로 유지한다.

## 점수·판정 제안

- score range: `10.0–14.5` 유지
- passing: `false` 유지
- strong: `false` 유지
- confidence ceiling: `medium` 유지

## 승인 기록

- reviewer: `workspace_owner`
- reviewed_at: `2026-09-02T05:24:26+09:00`
- method: `user_approval`
- decision: 승인
- notes: Golden JSONL을 `reviewed`로 전환한다.
