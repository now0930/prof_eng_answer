# 사실 기반 채점 입력 계약 v1

이 계약은 기존 채점기 위에 추가되는 **비활성·점수 중립 입력층**이다. 기존
`rubrics/topic_packs/`, `rubrics/generated/`, A/B/C/D/E, fatal 및 Question Type의
판정권을 옮기지 않는다. 구현은 `grading/evidence/fact_grounded_contracts.py`, 형식
카탈로그는 `schemas/fact_grounded_contract_v1.schema.json`이다.

| 레코드 | 식별·근거 | 허용하는 일 | 금지하는 일 |
|---|---|---|---|
| Fact | `fact_id`, `topic_id`, 관계·조건, 원문 위치·출처 버전·SHA-256, 검토 상태 | 승인된 사실을 질문의 참조 후보로 제공 | 사실 자체의 배점·fatal·문항 필수 여부 지정 |
| Question contract | 문제 SHA-256, 각 요구의 원문 span·행위·사실 ID, 지식 snapshot SHA-256 | 특정 문항이 무엇을 요구하는지 기록 | 미승인 사실 참조, 답안에 따라 요구사항 변경 |
| Interpretation candidate | 질문/답안 원문의 정확한 span·텍스트, 관계·극성·조건, 생성기 버전 | 의미 해석 *후보* 제안 | 점수·충족 상태·오류 심각도·fatal·합격 여부 판정 |
| Evaluation snapshot | 질문·답안·승인 사실·문제 계약·후보·온톨로지·룰브릭·정책 해시 | 재현 가능한 입력 식별 | 후보를 증거로 승인하거나 점수를 확정 |

동일한 `fact_id`를 Master의 출처 참조와 향후 Training/Grading/Feedback
projection에 사용한다. 현 단계에서는 `legacy_anchor_index`가 기존 Fact Anchor의
ID와 파일 해시만 읽는다. 기존 Anchor 문구를 새로 승인된 WordPress 사실로 간주하지
않으며 기존 채점 실행 경로도 변경하지 않는다.
`validate_view_fact_refs`는 세 View가 동일한 승인 사실 ID 공간을 참조하도록 검사하지만,
각 View가 그 사실을 실제로 소비하는 경로는 다음 Stage의 구현 대상이다.

`candidate`, `conflict` 상태의 Fact는 질문의 확정 사실 참조가 될 수 없다. 질문의
`knowledge_snapshot_sha256`가 실제 Fact 묶음과 다르면 snapshot을 만들지 않는다.
후보의 원문 span과 텍스트가 정확히 일치하지 않거나 점수/상태 필드가 들어오면 거부한다.
이는 **형식·출처·권한 검증**일 뿐 의미적 참/거짓 검증은 아니다. 원문에 나타난
잘못된 주장도 유효한 후보일 수 있으며, Stage 4~5의 관계·조건 검증 전에는 절대
`SATISFIED`로 승격하지 않는다.

Fact의 `score_effect=none`은 WordPress 출처나 LLM 후보가 점수 정책을 직접
수정하지 않는다는 뜻이다. 기존 사람 승인/hash 절차는 그대로 유지한다. 운영 DB,
개인 답안, WordPress OCR 전문은 이 공개 계약 파일과 테스트 fixture에 넣지 않는다.

검증: `python3 -m pytest -q tests/test_fact_grounded_contract_v1.py`.
