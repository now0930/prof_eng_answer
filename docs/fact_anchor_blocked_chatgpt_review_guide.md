# ChatGPT 검토 지시문 — 채점 차단 Fact Anchor 436건

## 입력 파일

- 전체: [`../reports/fact_anchor_blocked_436_chatgpt_20261104.csv`](../reports/fact_anchor_blocked_436_chatgpt_20261104.csv)
- 분할: `../reports/fact_anchor_blocked_436_chatgpt_batches_20261104/batch_01.csv`부터 `batch_09.csv`까지. 각 파일은 최대 50행이다.

파일은 저장소의 Fact Registry, Topic Pack, 기존 감사와 실행용 차단 목록만 투영한다. 개인 답안, 세션 이력, 인증 정보, 운영 DB는 포함하지 않는다. 다만 사용자의 비공개 운영 원칙에 따라 **생성된 CSV 자체는 `.gitignore`로 공개 커밋에서 제외한다**. 다른 환경에서는 아래 생성 명령을 다시 실행해야 한다. ChatGPT에는 **분할 파일을 하나씩** 첨부하고 아래 지시문을 사용한다. 9개 파일을 모두 검토한 뒤 결과 CSV를 비공개로 보관한다. 이 단계는 검토 제안이며 채점 차단을 자동 해제하지 않는다.

## ChatGPT에 붙여 넣을 지시문

```text
첨부한 CSV의 모든 행을 독립적으로 검토하라. 산업계측제어기술사 채점용 Fact Anchor의 일반 채점 자격을 판단하는 작업이다. 기존 Registry의 verified/approved 표기, 기존 출처 목록, 다른 LLM의 판정만으로 사실 검증을 완료했다고 판단하지 말라.

원칙:
1. fact_id/topic_id/anchor_id/current_statement_sha256/block_group/block_reason은 절대 수정하지 말라. 행을 누락하거나 합치지 말라.
2. current_topic_statement와 current_registry_statement의 차이, 적용 조건, 단위·수식, 과도한 일반화, 중복 채점 여부를 확인하라.
3. 물리법칙·공식 표준·학술 원문·공식 기술문서 등 1차 근거의 해당 위치를 직접 확인하라. 기존 링크가 있다는 사실만으로 승인하지 말라. 출처에 접근할 수 없으면 HOLD_EVIDENCE로 표기하라.
4. 일반적으로 옳은 핵심 사실만 GENERAL_CANDIDATE로 제안하라. 제조사·모델 특화 사례, 특정 관할/판본에만 적용되는 요건, 지엽적 예시, 중복 채점 요소는 일반 필수 Fact로 승격하지 말라.
5. 문구 일부만 옳으면 REVISE_CANDIDATE를 제안하고, proposed_statement에 검증된 최소 명제와 적용 조건을 쓴다. 현재 채점 가능 여부와 기술적 진위는 구분하라.
6. 출처 URL·판/절/페이지나 식 번호, 그 출처가 문구의 어느 부분을 직접 지지하는지 기록하라. 불확실하면 HOLD_EVIDENCE로 두고 추측하지 말라.
7. 질문별 채점 적합성을 별도로 생각하라. 일반 채점 후보라는 뜻은 모든 문제의 필수 답안 요소라는 뜻이 아니다.
8. 자동 채점 기준, 점수, fatal 규칙, Topic Pack 원문을 직접 수정하지 말라. 승인 권한은 후속 검증 절차에 있다.

chatgpt_decision은 다음 중 하나만 사용하라:
GENERAL_CANDIDATE, REVISE_CANDIDATE, SCOPED_ONLY, NONCORE, DUPLICATE, HOLD_EVIDENCE, INCORRECT.

출력: 입력 CSV의 모든 원본 열을 순서와 값 그대로 유지하고, 빈 검토 열(chatgpt_decision, proposed_statement, applicable_conditions, verified_source_url, source_locator, source_support_explanation, reviewer_model, reviewed_at, review_notes)만 채운 CSV 파일로 반환하라. 행 개수와 각 decision의 개수를 함께 보고하라. 확인하지 못한 항목을 임의로 승인하지 말라.
```

## 파일 생성·정합성 확인

```bash
python3 scripts/export_blocked_fact_review_packet.py --write
python3 scripts/export_blocked_fact_review_packet.py
```

입력 스냅샷은 전체 **436행** = 수정 대기 80 + 출처/승격 보류 80 + 일반 채점 제외 276이다. 분할 파일은 9개(50행 × 8, 36행 × 1)다. 각 행에 `current_statement_sha256`을 넣어 이후 Topic Pack 원문이 바뀌면 구판 검토 결과를 그대로 적용하지 않도록 한다.

ChatGPT 결과는 **제안**이다. 반영 전에는 Fact ID별 현재 원문·출처·질문 계약을 다시 대조하고, Topic Pack 관리 명령으로 생성물을 갱신한 뒤 관련 pytest, `validate-all`, 전체 Release Gate를 통과해야 한다. 보류 항목은 그때까지 차단 상태를 유지한다.

돌려받은 CSV의 형식과 원본 불변성을 검사하려면 다음을 실행한다.

```bash
python3 scripts/validate_blocked_fact_review.py <ChatGPT가_반환한_batch_01_CSV> --batch 1
# 436행 전체를 한 파일로 받았다면: --all
```

`FORMAT_VALID_ONLY`는 행·열·원본 문구·출처 기입 형식만 확인한다. 기술적 사실을 검증하거나 채점 차단을 해제하는 명령이 아니다.
