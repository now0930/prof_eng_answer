# S7 B7 독립 검토 packet 사용 절차

**사람용 요약:** 이 packet은 5개 기술 주제의 답안 표현을 독립 검토자에게 검토받기 위한 연구 자료입니다. 답안 문장과 Stage A/B 결과는 작성자가 만든 probe이며 정답 라벨이 아닙니다. 검토가 끝나기 전에는 정확도나 의미 매칭 성능을 계산하지 않습니다.

## 구현 및 자료 경로

- Stage A/B 구현: [`grading/evidence/s7_answer_claim_shadow.py`](../grading/evidence/s7_answer_claim_shadow.py)
- 회귀: [`tests/test_s7_answer_claim_shadow.py`](../tests/test_s7_answer_claim_shadow.py)
- 검토 자료: [`calibration/s7_b7_expert_review_packet_v1.json`](../calibration/s7_b7_expert_review_packet_v1.json)
- 정본 Registry 입력은 기존 [`approved_fact_registry.py`](../grading/evidence/approved_fact_registry.py)의 검증 절차를 사용합니다.

현재 packet은 5개 Fact별로 8개, 총 40개의 작성자 생성 probe를 담습니다. 각 항목의 `stage_a_extracted_claims`와 `stage_b_comparison_status`는 현재 코드를 사용해 계산한 실행 기록입니다. Registry의 기존 `verification_refs`는 원본 Fact의 참고 자료이며 해당 답안 표현을 독립 검토했다는 뜻은 아닙니다.

모든 항목은 `data_origin=AUTHOR_AUTHORED_PROBE_NOT_GOLD`, `review_status=PENDING`이며 `independent_reviewer_label`, `reviewer_evidence`, `reviewer_id`는 비어 있습니다. 이 자료는 운영 채점기에서 읽지 않습니다.

## 검토 계약

독립 검토자는 각 답안을 원문 Fact의 범위·조건·기술 근거와 대조하고, 필요하면 인용된 원자료의 구체 위치를 `reviewer_evidence`에 기록합니다. 작성자 자신이나 이전 모델 출력의 라벨을 독립 검토로 간주하지 않습니다.

`independent_reviewer_label`은 다음 값 중 하나를 사용합니다.

- `EQUIVALENT_WITHIN_SCOPE`: 답안이 원본 관계와 적용 범위를 충분히 표현함.
- `PARTIAL_OR_CONDITION_OMITTED`: 일부는 맞지만 필요한 적용 조건이나 관계 일부가 누락됨.
- `CONTRADICTED`: 답안이 원본과 반대되거나 직접 모순됨.
- `NOT_ASSERTED_QUOTED_OR_REJECTED`: 문장이 인용·부정·정정 등으로 작성자의 주장이 아님.
- `UNRESOLVED`: 근거 또는 문맥이 부족해 판단할 수 없음.

검토 시 `review_status`를 `REVIEWED`로 바꾸려면 reviewer identity, 근거 인용, 판단 이유를 함께 기록해야 합니다. 서로 다른 검토자의 판단이 충돌하면 별도 조정 기록이 완료될 때까지 `PENDING`으로 둡니다. 이 문서는 검토를 수행하거나 라벨을 부여하지 않습니다.

## 해석 경계

- Stage B는 호출자가 명시한 Topic/Fact scope를 검증해 감사행을 만들지만, 검토된 의미 crosswalk가 없어 관계 상태는 `NOT_ESTABLISHED`입니다. `source_match_proven=false`, `accuracy_status=NOT_ESTABLISHED`, `score_admission=DISABLED`, `score_effect=none`은 고정입니다.
- 검토자가 `EQUIVALENT_WITHIN_SCOPE`를 기록하더라도 이는 연구용 라벨입니다. 코드 crosswalk 승인, Fact 승격, 점수 변경 권한을 주지 않습니다.
- 현 Stage B는 채점 승인 결과를 출력하지 않으므로, 이 packet만으로 false-acceptance/false-rejection 비율을 계산하지 않습니다. 두 지표는 향후 별도 승인된 예측 규칙과 독립 라벨을 함께 검증한 뒤에만 산출할 수 있습니다. 현 상태의 `NOT_ESTABLISHED`는 의미 불일치가 아니라 보류입니다.
- V-Model Registry 관계의 필수 조건 수는 0입니다. 조건 누락 label을 적용하지 않습니다.
- Nyquist의 contour 관계와 `L(s)` mapping 관계는 별도 Stage A Claim입니다. 검토 근거도 관계별로 구분합니다.
- 원문 답안이나 개인 데이터는 packet에 추가하지 않습니다. 현재 40개 문장은 공개 연구용으로 작성한 synthetic probe입니다.

## 현재 검토 상태

독립 검토자 라벨은 **0/40**입니다. B7은 OPEN으로 유지하며, 본 packet의 생성은 독립 검증 완료나 정확도 결과가 아닙니다.
