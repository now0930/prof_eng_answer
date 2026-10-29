# 선별 Fact 재검증 결과 — 2026-10-29

## 범위와 판정

승인 Registry 1,524행 중 선별한 225행(P0 4, P1 138, SAMPLE 83)을 모두 Fact ID별로 검토했다. SAMPLE에서 경보 shelving 관련 문구가 근거 범위를 넘는 사례가 나와 동일 Topic의 DEFER 8행을 추가로 검토했다. 총 **233행 검토**이며, DEFER의 나머지 1,291행은 사실 검증 완료로 간주하지 않는다.

| 최종 판정 | 선별 225행 | 추가 8행 | 의미 |
| --- | ---: | ---: | --- |
| VERIFIED_AS_IS | 188 | 5 | 제시한 조건과 확인 가능한 근거 범위에서 유지 가능 |
| CORRECT_STATEMENT_OR_CONDITION | 5 | 1 | Fact 문구·적용 조건 정정 필요 |
| EVIDENCE_ONLY_FIX | 12 | 2 | 주장 자체보다 인용 위치·메타데이터·유도 설명·Anchor 연결 보완 필요 |
| RECLASSIFY_INTERNAL | 2 | 0 | 기술 사실이 아닌 저장소 내부 연결 계약으로 분리 필요 |
| HOLD | 18 | 0 | 원문 접근 불가 또는 주장 전체를 직접 뒷받침할 근거 미확인 |

이 수치는 **검토 범위와 판정의 집계**다. 188행을 운영 승격하거나 기존 승인 상태를 변경했다는 뜻은 아니다. 점수, Topic Pack, Fact Registry, 생성 Bank는 이 검증 단계에서 수정하지 않았다. 특히 HOLD 18행은 원문을 확보하거나 주장 범위를 줄이기 전까지 재승인 근거로 사용하지 않는다.

## 우선 수정 후보

- `second_order_overdamped_response`: “임계감쇠보다 느림”은 지배극의 긴 꼬리 등 비교 지표를 명시해야 한다.
- `second_order_resonance_frequency_condition`: 유한한 공진 피크는 `0 < ζ < 1/√2`; `ζ=0`은 이상적 특이점으로 구별한다.
- `closed_loop_minus_three_db_bandwidth`: 정확한 반전력점은 `−3.0103 dB`; 관용적 `−3 dB`와 구별한다.
- `state_tracking_integral_augmented_state_matrices`: `u`와 `r`의 입력 행렬을 별도로 써 차원 모호성을 없앤다.
- `alarm_shelving_is_temporary_operator_controlled_suppression`, `alarm_rationalization_reviews_shelving_eligibility`: 출처가 보여 주는 운영 관행과 모든 시스템에 요구되는 필수사항을 구별한다.

두 배치에서 겹친 `two_layer_interface_dp_equation_under_submerged_tap_conditions`는 수식 자체가 맞지만 Registry의 중간 압력 유도 설명이 틀려 `EVIDENCE_ONLY_FIX`로 판정했다. 기존 Fact 승인을 취소하거나 Pack 수식을 바꾸는 판정은 아니다. 검토 기록의 상충은 집계기에서 이 Fact ID 하나에 명시적으로 해소했다.

출처 보완에는 `liquid_in_glass_thermometer_calibration_is_immersion_condition_specific`의 Anchor 연결 누락, HMI/SCADA 문서번호·근거 범위, 일부 깨진 PDF 링크 및 표준 원문 위치가 포함된다. `HOLD`는 [P0/P1 첫 40행](fact_recheck_p0_p1_first40_20261029.md)과 [P1 나머지](fact_recheck_p1_rest_20261029.md)에 항목별 사유가 있다. [SAMPLE 및 동일 Topic 추가 8행](fact_recheck_sample_20261029.md)에서 미탐 유형을 확인할 수 있다.

## 다음 적용 원칙

1. 문구·조건 정정 6행과 출처·연결 보완 14행을 개별 변경 제안으로 분리하고, 관련 Pack/Registry의 단일 소유자를 확인한다.
2. 내부 계약 2행은 engineering Fact 점수 근거에서 분리하는 방안을 검토한다.
3. HOLD 18행은 접근 가능한 1차 자료나 재현 가능한 유도로 해소하기 전까지 현 상태를 유지한다.
4. SAMPLE에서 미탐이 확인됐으므로, 다음 선별에서는 같은 유형의 포괄 체크리스트·필수성 주장과 인용 범위 불일치 신호를 보강한다. 1,291행 전체를 검증 완료로 표시하지 않는다.

검토 범위·중복 판정·동일 Topic 확장은 `python3 -B scripts/validate_selected_fact_recheck_coverage.py`로 확인한다. 검토 문서는 공개 가능한 Fact ID와 1차 출처만 포함하며 개인 답안·세션·WordPress 비공개 DB는 포함하지 않는다.

## 실행 검증

- 선별 커버리지 검사: 225/225 및 추가 8행 확인, PASS.
- `python3 -B -m unittest scripts/test_triage_approved_fact_recheck.py`: 4건 PASS.
- `python3 -B scripts/rubric_manager.py validate-all`: PASS.
- `PROMOTE_GENERATED=0 scripts/validate_release.sh`: PASS. 10회 채점 재현성 P0 gate는 기본 설정대로 opt-in SKIP이며, 이 사실 검토의 완료 근거로 사용하지 않았다.
