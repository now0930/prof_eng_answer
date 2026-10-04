# WordPress Topic과 Review Topic 계약

## 1. 핵심 정의

`WordPress Topic`과 `Review Topic`은 같은 객체가 아니다.

- **WordPress Topic**: WordPress 게시글·HTML·자사 PDF·자사 이미지/OCR 출처를
  `topic_id`에 연결해 보관하는 출처 집합이다. 내용의 정답성이나 채점 권한을
  갖지 않는다.
- **Review Topic**: 사용자가 복습 대상으로 선택한 기존 Master Topic이다.
  별도 지식 원천이 아니라 `topic_id`로 Master와 Training View를 조회하는
  실행 단위다.

따라서 현재 구조에서는 `review_topic_id`를 새로 만들지 않고
`review_topic_id == topic_id`로 고정한다. WordPress 게시글 하나가 여러
Topic에 연결될 수 있고, 한 Topic도 여러 게시글·자료를 가질 수 있다.

## 2. 전체 흐름

```text
WordPress post/asset/OCR
        │ source_id, URL, version, hash
        ▼
WordPress Source Pack
        │ 승인된 source reference
        ▼
Master Topic Pack(topic_id, revision)
        ├── Grading View  ── 기존 Grader 권한
        ├── Training View  ── Review Topic 화면
        └── Feedback View  ── 확정 점수와 결합
                                  │
                           Training History
                                  │
                            다음 복습 요청
```

## 3. 식별자와 관계 계약

| 객체 | 식별자 | 관계 | 권한 |
|---|---|---|---|
| WordPress 게시글 | `post_id` | 여러 `topic_id`에 연결 가능 | 원문·출처 보존 |
| WordPress 자료 | `source_id` | 하나의 게시글에 속하고 하나 이상의 Topic에서 참조 가능 | URL·버전·해시 보존 |
| Master Topic | `topic_id` | canonical Topic 1개 | View 구성·revision 관리 |
| Review Topic | `topic_id` | Master Topic과 1:1 조회 | 사용자가 선택한 복습 문맥 |
| 학습 시도 | `question_id`, `attempted_at` | 하나의 `topic_id`에 귀속 | 사용자 상태 저장 |

필수 관계 불변식:

1. Review Topic 조회 결과의 `topic_id`는 Master 파일의 `topic_id`와 같아야 한다.
2. Training View의 WordPress 자료는 해당 Master의 `sources[]`에 이미 연결된
   `source_id`만 노출한다.
3. `source_id`·URL·버전·콘텐츠 해시가 일치하지 않으면 자료를 `stale` 또는
   `unavailable`로 처리하고 복습 내용으로 확정하지 않는다.
4. WordPress 연결·Review Topic 선택·복습 이력 저장은 Grading View의
   deterministic scoring을 호출하거나 변경하지 않는다.
5. 한 WordPress 자료가 여러 Topic에 연결되어도 각 Topic의 범위·소유권 검토를
   별도로 기록한다.

## 4. WordPress Topic 계약

```json
{
  "topic_id": "<master-topic-id>",
  "sources": [
    {
      "source_id": "wp-source-...",
      "post_id": 123,
      "source_type": "wordpress_html|first_party_pdf|first_party_image|ocr",
      "wordpress_url": "https://example/wordpress/post/",
      "source_url": "https://example/asset.pdf",
      "title": "...",
      "version": "2026-10-05",
      "content_sha256": "...",
      "locator": {"page": 3, "section": "..."},
      "extraction_method": "html|llm_ocr|manual_ocr|none",
      "verification_status": "unverified|pending_review|approved|stale"
    }
  ]
}
```

`approved`는 출처 연결이 확인되었다는 뜻이지, 해당 내용이 canonical
grading fact라는 뜻이 아니다. 내용이 Fact Anchor·fatal rule·question pattern
등으로 승격되려면 별도의 content update proposal과 기존 release gate가
필요하다.

## 5. Review Topic 계약

Review Topic은 다음 입력을 받아 읽기 전용 화면을 만든다.

```json
{
  "topic_id": "<master-topic-id>",
  "learner_id": "<learner>",
  "selected_at": "2026-10-05T01:00:00+09:00",
  "training_revision": 3,
  "training_view": "training-projection-v1"
}
```

출력은 `Training View`와 과거 `Training History`를 조합한다.

- 문제 예시·학습 내용·승인된 source reference를 표시한다.
- 미검토 OCR과 주석은 `검토 대기`, `score_effect: none`으로 표시한다.
- 마지막 시도에서 생성된 진단은 Feedback View를 통해 참고자료로 표시한다.
- 복습 완료는 Master를 수정하지 않고 별도 History에 저장한다.

현재 복습 선택은 날짜 기반 자동 변경이 아니라 사용자가 요청한
`topic_id` 또는 Topic 제목을 기준으로 한다. 하루 2문제 Queue는 향후 이
계약 위에 `weak_topic`·`long_unreviewed_topic` 등의 선정 정책을 추가한다.

## 6. View별 허용·금지 범위

| View | WordPress 자료 사용 | 점수/판정 변경 | 저장 대상 |
|---|---|---:|---|
| Grading | source reference도 직접 채점 입력으로 사용하지 않음 | 불가 | 기존 Grader 결과 |
| Training/Review | 연결·해시가 확인된 원문/OCR 참고자료 | 불가 | Training History 별도 |
| Feedback/Diagnosis | 확정 grade와 연결된 안내·추천자료 | 불가 | feedback snapshot 별도 |
| Master | source reference와 projection만 관리 | 직접 계산하지 않음 | 승인된 proposal만 |

## 7. 변경 및 승인 계약

```text
WordPress 변경
  → source version/hash 비교
  → 관련 topic_id 탐색
  → source-reference proposal 생성
  → 사용자 승인 후 Master sources 갱신

내용을 채점 기준으로 반영하려는 경우
  → content update proposal
  → before/proposed 값·근거·영향 View 기록
  → 사람 검토
  → Topic Pack 재생성
  → Golden/release gate
  → 명시적 적용
```

출처 연결 승인만으로 Grading View가 바뀌어서는 안 된다. 제안이 거절되거나
보류되어도 기존 Master·Grader·복습 이력은 유지한다.

## 8. 계약 검증 기준

- `topic_id`가 Master와 Review 요청에서 일치하는가
- WordPress `source_id`, URL, version, hash가 일치하는가
- Review Topic이 Training View만 읽고 원문을 수정하지 않는가
- Feedback이 `score_effect: none`을 유지하는가
- Training History가 Master JSON에 기록되지 않는가
- Grading Projection과 기존 deterministic/fatal/Golden 계약이 동일한가
- source 변경은 proposal·approval 없이 canonical 파일을 변경하지 않는가

이 계약의 목적은 WordPress 자료를 학습에 적극 활용하면서도, 검토되지 않은
OCR·원문·LLM 의견이 기존 채점 권한으로 우회 승격되는 것을 막는 것이다.
