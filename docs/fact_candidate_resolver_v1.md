# 답안 해석 후보의 보류 전파 계약

`grading/evidence/fact_candidate_resolver.py`는 기존 Grader와 분리된 **비활성**
검증층이다. 질문 계약의 fact 범위, 승인 Fact snapshot, 답안 원문 span, 후보 간 충돌,
긍정·부정과 인용·반박 문맥을 확인한다. 누락된 답안 구간이나 해석 실패가 있으면
`extraction_complete=false`와 `unresolved_spans`를 반환한다. 이 결과는 점수,
fatal, `SATISFIED`/`WRONG` 판정이 아니다.
질문 자체의 모든 요구가 `resolved`가 아니면 답안이 비어 있어도
`extraction_complete=false`로 남긴다.

LLM 후보가 승인 Fact와 같은 subject/predicate/object를 제시하더라도 원문이 실제로
그 뜻인지 별도로 확인하지 않으면 채택하지 않는다. `independently_verified_candidate_ids`
가 비어 있으면 어떤 제안도 `accepted`로 나오지 않는다. 현재 구현에는 이 독립 의미
검증기가 없으며 synthetic 테스트에서만 검증 ID를 주입한다. 따라서 운영 채점 경로에
연결해서는 안 된다. 검증기가 실패해도 기존 LLM 채점 경로로 자동 전환하지 않는다.

기존 `deterministic_primary_grader.py`는 추출 결과에 미해결 문장이 있어도
`extraction_complete=True`를 evaluator에 넘긴다. 이 실제 경로 수정은 출력·저장·
점수 보류 계약과 충분한 정상/반례 회귀가 준비될 때 별도 Stage 4 완료 작업으로 남긴다.
현재는 기존 점수와 release gate를 보호하기 위해 해당 운영 코드를 바꾸지 않았다.

집중 테스트: `python3 -m pytest -q tests/test_fact_candidate_resolver.py`.
