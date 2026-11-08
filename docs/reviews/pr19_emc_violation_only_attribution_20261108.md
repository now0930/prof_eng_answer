# PR19 — EMC 오류 규칙의 기술적 채점 귀속 분리 (2026-11-08)

## 감사 발견

이중 HOLD 가상 평가에서 EMC 모델답안은 14.25점(검토된 Golden 13–19점)으로 들어왔으나,
6개 오류 규칙이 의미적으로 다른 채점 Anchor를 `WRONG`으로 덮어썼다. 예:

- `EMC_GROUND_LOOP_RESISTANCE_ONLY`가 EMI 결합경로 Anchor를 `WRONG` 처리하여,
  답안에 존재하는 정확한 `emc_coupling_paths_check` 근거가 가려짐.
- `EMC_REDUNDANCY_IGNORES_CCF`가 전원품질 측정 Anchor를 `WRONG` 처리함.
- `EMC_SHIELD_REPLACES_PE` 및 `EMC_SINGLE_POINT_UNIVERSAL`가 source/path/victim 진단 Anchor를 `WRONG` 처리함.
- `EMC_SINGLE_COUNTERMEASURE_UNIVERSAL`가 EMI 결합 방식의 분류를 `WRONG` 처리함.
- `EMC_REWIRE_BEFORE_EVIDENCE`는 before/after 검증과 관련되지만 조치 전 근거 확보 요구로 직접 귀속.

## 수정 정책

`violation_only` 머신 요구사항은 **이미 독립적으로 검출된 결정론적 기술오류가 있을 때만** `WRONG`을 생성한다.
오류가 없는 답안에는 해당 머신 요구사항 자체가 생성되지 않으며, 이를 긍정 점수나 Fact 증거로 취급할 수 없다.
`violation_only`의 `required_fact_ids`는 반드시 빈 배열이고 `minimum_match_count`는 0이어야 한다.

| 기술오류 | 직접 귀속되는 Anchor |
|---|---|
| `EMC_SINGLE_POINT_UNIVERSAL` | `ipgse_single_multi_point_conditional` |
| `EMC_SHIELD_REPLACES_PE` | `ipgse_shield_not_pe` |
| `EMC_REDUNDANCY_IGNORES_CCF` | `ipgse_redundant_supply_boundary` |
| `EMC_GROUND_LOOP_RESISTANCE_ONLY` | `ipgse_ground_loop_safe_mitigation` |
| `EMC_SINGLE_COUNTERMEASURE_UNIVERSAL` | `ipgse_source_path_victim_mitigation` |
| `EMC_REWIRE_BEFORE_EVIDENCE` | `ipgse_evidence_before_rewire` |

기존 3개 Fatal은 유지. 모두 9개 불변식의 Fatal/Major 분류와 25점 만점, Golden, 합격선은 변경하지 않는다.
네 개 긍정 Anchor와 워크플로 Anchor 총 5개의 실제 HOLD는 유지하며, 그림자 채점은 승격 근거가 아니다.

## 남은 검토

근거 문장이 없는 상태에서 `SATISFIED`를 받는 어휘 기반 recall floor가 간헐적으로 나타난다.
이번 패치는 **잘못된 기술오류–채점 항목 귀속만** 해결한다. 어휘 기반 부분점수는 별도 회귀검증 및 범위 한정 없이 변경하지 않는다.
