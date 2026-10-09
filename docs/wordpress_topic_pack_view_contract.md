# WordPress Topic Pack과 Grading·Review·Feedback 계약

## 1. 목적

WordPress는 개인 지식의 원천이며, 기존 Grader의 채점 기준 자체가 아니다. WordPress 자료를 Master와 세 View에 연결하되, 원문·OCR의 불완전성이나 미검토 내용이 채점 점수에 영향을 주지 않도록 계층과 권한을 분리한다.

## 2. 전체 관계

```text
WordPress 글·HTML·자사 PDF·자사 이미지/OCR
              │
              │ 출처 식별·버전·해시·검토 상태
              ▼
       WordPress Source Pack
              │ source reference 승인
              ▼
       MASTER TOPIC PACK
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
 Grading   Training  Feedback/Diagnosis
   View      View           View
 호환 검증  /review    확정 점수 기반 안내

별도 채점 경로: Topic Pack source → generated bank → 기존 Grader → 확정 점수
학습 상태: 확정 점수·/review → Training History / Review Queue
```

Grading View는 현재 운영 Grader의 입력 경로가 아니다. WordPress 원문·OCR을
Master에 연결하는 것과 채점용 Topic Pack source로 승인하는 것은 별도 절차다.

## 3. 계층별 권한

| 계층 | 역할 | 채점 점수 변경 | 쓰기 권한 |
|---|---|---:|---|
| WordPress Source Pack | 원문·HTML·PDF·이미지·OCR와 출처 메타데이터 보존 | 불가 | 수집·동기화만 |
| Master Topic Pack | Topic ID·버전·legacy source·View projection·source reference의 통합 계약 | 직접 계산하지 않음 | 승인된 제안만 |
| Grading View | 기존 canonical Topic Pack을 Grader가 읽는 호환 projection | 기존 계약 범위에서만 | 없음 |
| Training/Review View | 학습자료·원문·OCR·미확정 주석 제공 | 불가 | 학습 이력은 별도 저장 |
| Feedback/Diagnosis View | 확정 점수와 진단 차원에 따른 보완 안내 | 불가 | 피드백 snapshot만 별도 저장 |
| Training History/Review Queue | 사용자의 시도·복습 상태·선정 대상 관리 | 불가 | 사용자 상태 저장 |

## 4. WordPress Source Pack 계약

출처 레코드는 최소 다음 필드를 보존한다.

```text
source_id
source_type
wordpress_url
source_url
title
version
page
section
updated_at
content_sha256
extraction_method
verification_status
```

규칙:

- `first_party=1`인 자사 자료의 기존 추출/OCR만 사용한다.
- 외부 PDF는 URL·제목 등 메타데이터만 보존하고 자동 OCR·채점 반영을 하지 않는다.
- 출처 연결은 기술적 정답 승인과 다르다.
- URL·버전·해시가 Master reference와 다르면 View는 `stale` 또는 `unavailable`로 처리한다.
- 원문 변경은 Master 자동 수정이 아니라 변경 제안으로 전환한다.

## 5. Master Topic Pack 계약

Master는 원문 전체를 복사하지 않고 다음을 관리한다.

```text
topic_id
revision
legacy_topic_pack.source_root
legacy_topic_pack.source_files
projections.grading
projections.training
projections.diagnosis
sources[]
source_update_policy
```

필수 불변식:

1. Grading projection의 authority는 `existing_topic_pack`이다.
2. Grading projection은 기존 `fact_anchor`, `logic_check`, `model_answer`, `topic_importance`를 가리킨다.
3. WordPress source reference만 추가해도 canonical grading fact는 바뀌지 않는다.
4. `sources=[]`는 출처 미연결 상태로 허용한다.
5. source 변경은 `proposal_only + approval_required` 계약을 따른다.
6. Master revision·source hash·proposal 상태가 일치하지 않으면 적용을 중단한다.

## 6. Grading View 계약

Grading View는 새 채점기가 아니다. 기존 Grader가 사용하던 Topic Pack source를 읽기 전용으로 projection한다.

입력:

- canonical Topic Pack source JSON
- 기존 Question Type taxonomy
- 기존 routing authority
- 기존 deterministic scoring·fatal·Golden 계약

금지:

- WordPress 원문·OCR을 직접 점수 계산 입력으로 사용
- LLM 권고 CSV를 사실·정답·fatal rule로 사용
- Training View 주석이나 Feedback 내용을 점수에 반영
- source reference 승인만으로 Fact Anchor를 자동 생성

채점 기준을 바꾸려면 WordPress 자료에서 별도 content proposal을 만들고, Topic Sheet·source JSON을 사람이 검토한 뒤 `approve-topic`과 release validation을 통과해야 한다.

## 7. Training/Review View 계약

Training View는 WordPress source가 Master에 연결되고 버전·URL·해시가 일치할 때만 학습 참고자료로 노출한다.

허용:

- 게시글·HTML·자사 PDF/OCR 발췌
- source URL·페이지·섹션·버전
- 미확정 주석과 검토 상태
- 문제·학습자료·복습 안내

금지:

- 원문을 canonical fact로 표시
- 미확정 주석을 정답 또는 오답으로 승격
- 학습자료만으로 채점 점수 변경
- 원문 전체를 Grading result 또는 diagnosis snapshot에 복사

`/review <topic_id 또는 주제명>`은 Training View를 소비한다. 복습 완료·점수·진단은 Master가 아니라 Training History에 저장한다.

## 8. Feedback/Diagnosis View 계약

Feedback View는 이미 확정된 채점 결과를 입력으로 받고, 부족점과 보완 방향을 제공한다.

```text
final_grade + diagnosis projection + approved navigation references
                    ↓
             feedback guidance
```

불변식:

- `score_effect: none`
- Feedback은 점수·판정·fatal을 재계산하지 않는다.
- WordPress source는 추천자료·탐색 링크로만 노출한다.
- 미검토 원문·주석은 “검토 대기”로 표시한다.
- 오래된 feedback snapshot은 당시 Master/source revision을 보존한다.

## 9. 내용 승격 계약

WordPress 내용을 채점 기준으로 승격하는 경우에만 다음 절차를 적용한다.

```text
WordPress source/OCR
 → Topic scope·ownership 확인
 → content update proposal
 → Fact/Model/Logic/Importance 후보 작성
 → 사람 검토
 → candidate bundle·hash 검증
 → approve-topic 또는 명시적 content approval
 → generated bank 재생성
 → Golden/release regression
 → 배포
```

다음은 자동 승격하지 않는다.

- 제목·태그·lexical score 일치
- LLM의 `recommend_approve`
- OCR 텍스트만 존재
- source reference가 승인됨
- Training/Feedback View에서 자주 사용됨

## 10. 검토 상태

```text
unverified
  → candidate
  → human_review
  → approved_source_reference
  → (별도 내용 검토 후) canonical_content_candidate
  → applied
```

`deferred`는 거절이 아니라 후속 검토 상태다. 현재 확실하지 않은 후보는 Master·Grader에 반영하지 않고 보류한다.

## 11. 검증 계약

최소 검증 항목:

- Master schema validation
- source URL/version/hash consistency
- Grading Projection compatibility
- Training Projection validation
- Diagnosis/Feedback Projection validation
- source change proposal atomicity
- WordPress source-material identity check
- 기존 deterministic regression·Golden·release gate
- Training History persistence 및 Review Queue contract

어느 View의 보조 자료가 실패해도 확정 채점·점수 저장·기존 routing을 차단하지 않는다.

## 12. 현재 운영 원칙

- 형식 구조는 완료되어 있다.
- WordPress 내용은 먼저 Training/Feedback 참고자료로 사용한다.
- 확실한 출처 연결만 별도 승인 후보로 관리한다.
- 내용 정확성이 확인되기 전에는 Grading View를 변경하지 않는다.
- 기존 Grader와 deterministic primary authority를 항상 보존한다.
