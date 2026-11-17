# S7 B7 독립 검토 packet 사용 절차

**사람용 요약:** 이 packet은 5개 기술 주제의 답안 표현을 독립 검토자에게 검토받기 위한 연구 자료입니다. 답안 문장과 Stage A/B 결과는 작성자가 만든 probe이며 정답 라벨이 아닙니다. 검토가 끝나기 전에는 정확도나 의미 매칭 성능을 계산하지 않습니다.

## 구현 및 자료 경로

- Stage A/B 구현: [`grading/evidence/s7_answer_claim_shadow.py`](../grading/evidence/s7_answer_claim_shadow.py)
- 회귀: [`tests/test_s7_answer_claim_shadow.py`](../tests/test_s7_answer_claim_shadow.py)
- 검토 자료: [`calibration/s7_b7_expert_review_packet_v1.json`](../calibration/s7_b7_expert_review_packet_v1.json)
- 정본 Registry 입력은 기존 [`approved_fact_registry.py`](../grading/evidence/approved_fact_registry.py)의 검증 절차를 사용합니다.

원본 packet은 5개 Fact별 8개, 총 40개의 작성자 생성 probe를 담고 있으며 변경하지 않습니다. 전수 감사에서 정규화한 답안 문자열 기준 3개 exact-duplicate group이 발견되어 고유 답안은 37개입니다. 추가로 의미가 겹칠 가능성이 있는 두 쌍을 확인했으나 조건 범위 차이일 수 있어 exact duplicate에서 제외하지 않았습니다. 원본의 `stage_a_extracted_claims`와 `stage_b_comparison_status`는 작성자 예측이며 검토자 자료에 전달하지 않습니다. Registry의 `verification_refs`는 원본 Fact 참고 자료일 뿐 각 probe의 독립 정답 근거가 아닙니다.

원본 probe 분류 중 명확한 mismatch 3건을 기록했습니다: nominal seat 면적에 대한 독립성 문장을 관계 역전으로 분류한 사례, 서로 모순되지 않는 configuration-baseline 문장 두 개를 모순 사례로 분류한 사례, 필수 조건이 0개인 V-Model에 조건 누락 probe label을 붙인 사례입니다. partial/quoted/Nyquist scope 중 일부는 의미가 모호해 mismatch로 단정하지 않고 전문가 판정 대상으로 표시했습니다. 자세한 case별 감사와 ID 대응표는 로컬 전용 `tmp/s7_b7_blind_review/author_audit_and_key.json`에 있습니다.

검토자 전달용 자료는 원본 보존과 분리해 로컬 전용 `tmp/s7_b7_blind_review/blinded_packet.json`에 만들었습니다. 37개의 고유 답안에 무작위 ID를 부여하고, 각 답안에 비교 Fact의 원문 주장·조건 ID·출처 locator를 포함합니다. `case_kind`, `probe_note`, Stage A/B 예측은 제외했습니다. 별도 판정 서식은 `tmp/s7_b7_blind_review/review_results.json`이며 모든 결과는 `PENDING`입니다. 무작위 ID 대응표와 작성자 감사 정보는 reviewer에게 전달하지 않습니다. 이 blind copy는 metadata-blind이며 답안 문장 자체가 원본 공개 packet과 겹칠 수 있으므로 reviewer에게는 이 파일만 전달하고 원본 저장소 링크를 함께 주지 않는 방식으로 사용해야 합니다.

원본 packet의 모든 항목은 `data_origin=AUTHOR_AUTHORED_PROBE_NOT_GOLD`, `review_status=PENDING`이며 `independent_reviewer_label`, `reviewer_evidence`, `reviewer_id`가 비어 있습니다. 블라인드 판정 서식도 reviewer 결과가 입력되기 전까지 동일하게 PENDING입니다. 두 자료 모두 운영 채점기에서 읽지 않습니다.

## 검토 계약

독립 검토자는 각 답안을 원문 Fact의 범위·조건·기술 근거와 대조하고, 필요하면 인용된 원자료의 구체 위치를 `reviewer_evidence`에 기록합니다. 작성자 자신이나 이전 모델 출력의 라벨을 독립 검토로 간주하지 않습니다.

검토는 서로 다른 단위로 기록합니다: (1) 전체 답안이 Fact를 충분히 뒷받침하는지, (2) 답안에서 검토자가 직접 식별한 각 Claim과 Fact 관계, (3) 필수 조건 충족 여부, (4) 문장이 작성자의 주장인지 인용·부정·정정인지. Fact가 여러 관계를 포함하면 각 관계를 따로 기록합니다. 일부 Claim이 맞아도 답안에 모순 Claim이 함께 있으면 전체 답안을 완전 지지로 표시하지 않습니다.

`overall_answer_label`은 `FULLY_SUPPORTED_WITHIN_FACT_SCOPE`, `PARTIALLY_SUPPORTED_OR_INCOMPLETE`, `MIXED_OR_CONTRADICTED`, `NO_ASSERTION`, `UNRESOLVED` 중 하나를 사용합니다. 각 Claim의 `independent_reviewer_label`은 다음 값 중 하나를 사용합니다.

- `EQUIVALENT_WITHIN_SCOPE`: 답안이 원본 관계와 적용 범위를 충분히 표현함.
- `PARTIAL_OR_CONDITION_OMITTED`: 일부는 맞지만 필요한 적용 조건이나 관계 일부가 누락됨.
- `CONTRADICTED`: 답안이 원본과 반대되거나 직접 모순됨.
- `NOT_ASSERTED_QUOTED_OR_REJECTED`: 문장이 인용·부정·정정 등으로 작성자의 주장이 아님.
- `UNRESOLVED`: 근거 또는 문맥이 부족해 판단할 수 없음.

검토 시 `review_status`를 `REVIEWED`로 바꾸려면 reviewer identity, 근거 인용, 판단 이유를 함께 기록해야 합니다. 서로 다른 검토자의 판단이 충돌하면 별도 조정 기록이 완료될 때까지 `PENDING`으로 둡니다. 이 문서는 검토를 수행하거나 라벨을 부여하지 않습니다.

별도 결과 파일을 갱신할 때 reviewer identity와 locator가 포함된 근거가 없으면 `REVIEWED`로 바꾸지 않습니다. 자동 추출 결과, 작성자 probe note, 모델 판정은 reviewer evidence로 인정하지 않습니다.

## 평가 지표 경계

- **Stage A 추출 범위/누락:** 독립 검토자가 답안에서 직접 열거한 Claim을 기준으로, 추출 Claim의 span·관계·assertion context를 대조합니다. Stage A precision/recall은 각각 검토 확인 추출 수/전체 추출 수와 검토 확인 추출 수/독립 확인 Claim 수로 정의하되, 독립 Claim 목록이 완료되기 전에는 계산하지 않습니다. 작성자 probe 분류를 분모나 정답으로 쓰지 않습니다.
- **독립 Claim–Fact 관계:** 검토자가 Fact statement·조건·출처에 근거해 개별 관계와 전체 답안 verdict를 따로 기록합니다. verified-equivalent, partial, contradicted, unresolved 관계 수를 구분하며 임의로 하나의 accuracy 수치로 합치지 않습니다.
- **False acceptance / false rejection:** 독립 라벨이 있는 표본에서 실제 matcher가 ACCEPT한 관계 중 전문가가 동등하지 않다고 판정한 비율과, 전문가가 동등하다고 판정했으나 matcher가 거부한 비율을 각각 계산할 수 있습니다. 현재 Stage B는 전부 `NOT_ESTABLISHED` 또는 `ABSTAIN`이고 semantic acceptance가 없으므로 두 오류율은 **측정 불가**입니다. `NOT_ESTABLISHED`를 false rejection이나 정확한 부정 판정으로 세지 않습니다.

## 해석 경계

- Stage B는 호출자가 명시한 Topic/Fact scope를 검증해 감사행을 만들지만, 검토된 의미 crosswalk가 없어 관계 상태는 `NOT_ESTABLISHED`입니다. `source_match_proven=false`, `accuracy_status=NOT_ESTABLISHED`, `score_admission=DISABLED`, `score_effect=none`은 고정입니다.
- 검토자가 `EQUIVALENT_WITHIN_SCOPE`를 기록하더라도 이는 연구용 라벨입니다. 코드 crosswalk 승인, Fact 승격, 점수 변경 권한을 주지 않습니다.
- 현 Stage B는 채점 승인 결과를 출력하지 않으므로, 이 packet만으로 false-acceptance/false-rejection 비율을 계산하지 않습니다. 두 지표는 향후 별도 승인된 예측 규칙과 독립 라벨을 함께 검증한 뒤에만 산출할 수 있습니다. 현 상태의 `NOT_ESTABLISHED`는 의미 불일치가 아니라 보류입니다.
- V-Model Registry 관계의 필수 조건 수는 0입니다. 조건 누락 label을 적용하지 않습니다.
- Nyquist의 contour 관계와 `L(s)` mapping 관계는 별도 Stage A Claim입니다. 검토 근거도 관계별로 구분합니다.
- 원문 답안이나 개인 데이터는 packet에 추가하지 않습니다. 현재 40개 문장은 공개 연구용으로 작성한 synthetic probe입니다.

## 현재 검토 상태

독립 검토자 라벨은 **0건**입니다. 블라인드 자료 37건은 전부 `PENDING`이고 B7은 OPEN으로 유지합니다. 본 packet 생성이나 case 감사는 독립 검증 완료 또는 정확도 결과가 아닙니다.

## 로컬 검토 자료 무결성 검사

로컬 전용 blind packet과 reviewer 결과 서식은 저장소에 포함하지 않습니다. 접근 제한된 `tmp/s7_b7_blind_review/` 자료에 다음 검증기를 실행할 수 있습니다.

```bash
python3 -B scripts/validate_s7_b7_review_results.py
```

검증기는 공개 원본 packet의 고정 SHA-256, 40개/5개 Fact별 분포, exact duplicate 제외에 따른 37개 고유 답안, private 1:1 blind ID 교차표, 승인 Registry의 Fact·Topic·관계·조건·출처 일치, reviewer 결과의 ID·span·조건·근거 구조를 검사합니다. 표준 출력은 집계 수와 고정된 오류 코드만 포함하며 답안·reviewer 정보·ID 교차표는 출력하지 않습니다. exit code 1은 입력 거부를 뜻합니다. 운영 채점 경로에서는 이 검증기를 호출하지 않습니다.

`REVIEWED` 결과에는 reviewer identity(자기 기재이며 코드가 신원을 인증하지 않음), ISO timestamp, 전체 답안 판정, Claim별 라벨·정확한 답안 span·이유, Fact 조건별 상태·이유, assertion context, 문서명·정확한 locator·근거 이유가 필요합니다. Claim span은 Python 문자열 offset으로 원문과 정확히 일치해야 합니다. V-Model의 조건 집합은 빈 목록 그대로 유지합니다. 복수 reviewer 판정이 다르면 `PENDING` 또는 `CONFLICT`만 허용하며, 별도 adjudication 없이 `REVIEWED`로 종결하지 않습니다. `PENDING`에는 reviewer 라벨을 넣을 수 없습니다.

2026-11-17 무결성 검사 결과: 원본 40건, exact duplicate 3개(3 group), blind unique 37건; 가능한 의미 중복 2쌍은 exact duplicate에서 제외했습니다. 작성자 probe 분류 불일치 집계는 3건입니다. 이 중 nominal seat 면적 관계를 말하지 않은 문장을 관계 역전으로 분류한 사례 1건, 서로 모순되지 않는 형상 기준선 설명을 contradiction으로 분류한 사례 1건, 필수 조건이 0개인 V-Model에 조건 누락 label을 붙인 사례 1건입니다. 독립 reviewer 라벨은 0건이고 37건 모두 `PENDING`입니다. 이 검사는 packet·구조 무결성만 확인하며 기술적 정답이나 reviewer 신원을 판정하지 않습니다.
