# D4 공통 관계 비교: 복수 Claim 연구 경로

이 경로는 답안에서 추출된 모델 제안을 검토용으로 비교합니다. 후보와 오류 묶음은 사실 검증이나 점수 변경을 뜻하지 않습니다. 승인 Registry와 원문 span이 정확해도 문맥과 의미가 입증되는 것은 아닙니다.

## 입력과 결과

`grading/evidence/d4_common_relation.py:evaluate_claim_batch(answer, proposals)`는 호출자가 제공한 복수 Claim과 Fact ID 목록을 기존 공통 구성요소 비교기로 평가합니다. 각 항목은 `claim_id`, 기존 비교기의 `claim`, `fact_ids`, `cause_span`을 명시합니다. `cause_span`은 원문의 `{start, end, text}` 또는 `null`입니다. Claim ID나 Fact ID 중복은 거부하고 동일한 Claim–Fact 제안의 중복 후보는 제외합니다. 지원되지 않는 Fact나 Registry가 일치하지 않으면 보류합니다.

반대 구성요소 후보의 원문 원인 span, scope 및 조건 근거가 정확히 같을 때 `PROPOSED_SAME_CAUSE` 묶음을 반환합니다. 이는 모델이 제안한 원인 위치를 바탕으로 한 묶음이며 동일한 오류 원인이라는 검증이나 감점 계산이 아닙니다. 비교 행은 모두 보존합니다. 서로 다른 scope·조건 근거·원인 span은 합치지 않습니다. 미확인 문맥과 인용·반박은 기존 비교기의 보류 정책을 따릅니다.

`python3 -B scripts/replay_d4_claim_batch.py --input <private.json> --output <new-private.json>`으로 ChatGPT가 별도 생성한 구조화 제안을 읽을 수 있습니다. 입력 최상위 필드는 `answer`, `proposals`입니다. 결과 파일은 새 파일로만 생성되고 권한은 0600이며 답안 전문과 근거 문자열을 포함하지 않습니다. 이 명령은 ChatGPT나 다른 모델을 호출하지 않습니다.

기존 `scripts/replay_d4_common_relation.py`는 기본적으로 지원 Fact의 제안이 하나라도 빠지면 실패합니다. 목록만 재생할 때 명시적으로 `--allow-missing-proposals`를 지정하면 누락 행을 `MISSING`/`UNRESOLVED`로 남깁니다. 이 옵션은 누락된 Claim을 생성하거나 의미 검증을 대체하지 않습니다.

`audit_full_registry()`는 pinned 전체 Registry의 해시, 중복 ID, 관계 필드 및 기록된 승인·출처와 기존 프로파일의 원본 일치를 점검합니다. 기록된 승인 상태를 세는 검사는 Fact의 기술적 정확성이나 점수 적격성을 재승인하지 않습니다. 모든 결과는 `score_admission=DISABLED`, `score_effect=none`, `source_match_proven=false`입니다.
