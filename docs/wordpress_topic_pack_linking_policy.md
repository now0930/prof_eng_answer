# WordPress 블로그–Topic Pack 연결 정책 및 작업 지침

## 1. 목적과 용어

이 문서는 WordPress 블로그와 기존 Topic Pack 사이의 연결 의미, 판정 기준,
적용 절차를 정의한다. 기본 구조는 **여러 블로그가 여러 Topic Pack에 기여할
수 있는 다대다 관계**다.

- **블로그 연결(Topic link)**: 게시글이 해당 Topic Pack의 범위 안에서 특정
  기술 하위 주제·근거·사례를 제공한다는 검토된 관계다.
- **출처 참조(source reference)**: 승인된 블로그 연결을 바탕으로 게시글 또는
  첨부 출처를 특정 Topic의 Master 자료 목록에 제안하는 별도 관계다.
- **콘텐츠 반영(content update)**: 블로그의 주장을 canonical Topic 내용이나
  채점 기준에 반영하는 별도 변경이다.

블로그 연결 승인은 출처나 블로그 내용이 정답이라는 인증이 아니며, 블로그
본문을 Topic Pack에 복사하거나 채점·학습 자료에 자동 반영하지 않는다.
출처 참조 승인 및 canonical 콘텐츠 변경에는 각각 별도 검토와 승인이 필요하다.

## 2. 관계와 상태

관계의 기본 단위는 `(post_id, topic_id)`다. 한 게시글은 여러 Topic Pack에
연결될 수 있고, 한 Topic Pack은 여러 게시글을 받을 수 있다. 한 블로그가
Topic Pack 전체를 다루어야 연결할 수 있는 것은 아니다. 범위에 속하는
**실질적인 일부 기여**만 있어도 연결할 수 있다.

현재 카탈로그 상태의 뜻:

| 상태 | 뜻 | 게시글 연결 지표 |
|---|---|---|
| `approved` | 이 게시글이 이 Topic Pack의 일부 범위에 기여한다고 검토됨 | 연결로 셈 |
| `pending_review` | 후보 관계이며 추가 근거·판정이 필요함 | 연결로 세지 않음 |
| `rejected` | 이 특정 게시글–후보 Topic 조합은 범위에 맞지 않는다고 판정됨 | 연결로 세지 않음 |

`rejected`는 **게시글 전체의 거절이나 다른 Topic Pack과 연결 불가 판정이
아니다**. 후보 목록은 검색을 통해 발견된 조합일 뿐, 가능한 모든 Topic을
열거하거나 블로그의 지식 가치를 평가하지 않는다. 거절 후보 행 수를 블로그
연결 성과 지표로 사용하지 않는다.

연결 기여 공백은 게시글 쪽과 Topic Pack 쪽 두 축으로 관리한다.

1. **블로그 미연결 수**: `approved` 연결이 하나도 없는 게시글 수. 대기·거절
   후보만 있는 게시글과 후보 기록이 없는 게시글을 모두 포함한다. 전체 게시글
   중 미연결 비율과 대기 후보 있음·거절 후보만 있음·후보 없음의 보조 분류를
   함께 본다.
2. **블로그 기여가 기록되지 않은 Topic Pack 수**: 승인된 WordPress 게시글이
   하나도 없는 기존 Topic Pack 수. 팩별 승인 기여 게시글 수와 대기 후보 수를
   확인해 우선 검토할 영역을 찾는다.

두 지표 모두 카탈로그에 **승인 관계가 아직 기록되지 않았다**는 뜻이다.
특히 팩에 승인 기여 글이 없다고 해서 기여 가능한 블로그가 실제로 없거나,
Topic Pack의 콘텐츠 범위가 부족하다고 결론 내리지 않는다. 검색 후보가
없다는 것은 발견된 후보가 없었다는 뜻이며, 기존 82개 팩 전체에 대한 의미
검토를 대신하지 않는다. `rejected` 후보 수는 어떤 연결 성과 지표에도 쓰지
않는다.

```bash
python3 scripts/wordpress_catalog.py --topic-link-coverage
```

출력에는 전체 미연결 게시글 요약과 모든 Topic Pack별 요약이 포함된다.
팩별 `contribution_status`는 후속 조치 우선순위를 나눈다.

- `covered`: 승인된 기여 게시글이 하나 이상 있음
- `pending_candidates`: 승인 연결은 없지만 검토 대기 후보가 있음
- `rejected_candidates_only`: 승인·대기 연결은 없고 거절 후보만 있음. 다른
  팩의 연결 가능성까지 배제하지 않으므로 새 후보를 다시 찾을 수 있음
- `no_candidates`: 현재 카탈로그에 이 팩의 게시글 후보 관계가 없음. 검색 누락
  가능성을 고려해 미연결 블로그의 전체 목록과 함께 재검색·사람 검토

전체 후보 검토 또는 링크 적용 배치 후에 JSON 스냅샷을 저장하고 이전 스냅샷과
비교한다. 날짜·배치를 구분하는 새 경로를 쓰며 기존 파일은 덮어쓰지 않는다.
스케줄러는 전제하지 않으며, 생성된 스냅샷의 게시글·팩 단위 집계 추이로
관리한다.

```bash
python3 scripts/wordpress_catalog.py \
  --topic-link-coverage-json reports/wordpress_topic_link_coverage_YYYYMMDD.json
```

## 3. 연결 판정 원칙

### 승인

다음을 모두 만족하면 해당 게시글과 Topic Pack의 연결을 승인한다.

1. **범위 소유권**: 기존 Topic Pack의 README에서 해당 기술 하위 주제를
   실제로 소유하는지 확인한다. 제목이나 Topic ID만으로 판단하지 않는다.
2. **실질적 기여**: 게시글 본문 또는 확인 가능한 자사 자료에 설명, 수식,
   절차, 장치 원리, 설계 판단, 시험·운영 사례 중 하나 이상의 구체적 내용이
   있다. 단순 언급, 링크 목록, 태그, 용어 나열은 충분하지 않다.
3. **증거와 위치**: 승인 근거를 게시글 절·문장·수식 또는 자사 OCR의 문서명과
   페이지 등 확인 가능한 위치에 연결한다. 독립 근거가 여러 개 있으면 함께
   기록한다. 짧지만 좁고 명확한 하위 주제 설명은 근거 한 건만으로도 승인할
   수 있으며, 근거 개수를 기계적인 문턱으로 삼지 않는다.
4. **경계 및 사실성 확인**: 더 적합한 다른 Topic의 소유 범위를 침범하지
   않는지, 눈에 띄는 사실 오류·OCR 불확실성이 있는지 기록한다.

부분 기여 관계는 게시글이 Topic Pack의 전 범위나 모든 평가 항목을 다룬다고
주장하지 않는다. 예를 들어 압전 가속도센서의 구성과 진동 측정 원리를 설명한
글은 해당 압전 센서 팩의 일부에 기여할 수 있다. 한 게시글이 서로 다른
하위 주제를 실제로 다루면 여러 팩에 각각 연결할 수 있지만, 각 연결은
독립된 근거와 소유 범위 확인이 필요하다.

### 보류

다음 경우는 `pending_review`로 유지한다.

- 본문·첨부 전문이 없거나 지나치게 짧아 주제를 확인할 수 없음
- OCR이 불완전하거나 원문과 상충할 가능성이 있음
- 후보 Topic 간 경계가 모호하거나 사실 오류가 연결 판단을 좌우함
- 근거가 용어·제목·키워드 중복뿐임

보류는 거절이 아니다. 추가 근거를 얻기 전까지 승인 연결이 아닌 상태로
관리한다.

### 후보 조합 거절

`rejected`는 게시글 본문과 Topic 소유 범위를 확인해 **그 특정 후보 관계가
명백히 범위 밖**일 때만 사용한다. 다른 후보 팩이나 새로운 후보를 검토하는
것을 막지 않는다. 대량 후보 정리에서 검색 점수·공통 단어만으로 거절하지
않는다.

카탈로그 구현은 이미 승인·거절된 조합의 직접 덮어쓰기를 허용하지 않는다.
이견이나 새 근거가 생기면 기존 행을 임의 수정하지 말고, 원래 결정과 새
근거가 남는 별도 재검토·정정 이력을 만든다.

## 4. 재현 가능한 검토 절차

### 1단계: 읽기 전용 준비

1. 현재 DB 백업을 만들고 게시글·Topic 수, 승인·대기 관계 수, 미연결 게시글
   기준값을 기록한다.
2. 최신 로컬 게시글 본문, 발췌, 태그, 출처·첨부 메타데이터를 확인한다.
   기존에 저장된 자사 PDF·이미지 OCR은 사용할 수 있다.
3. 외부 자료는 저장된 메타데이터만 사용한다. 외부 문서를 새로 내려받거나
   OCR하지 않는다.
4. 전체 후보 검토 시 게시글별로 후보를 묶고, 이미 승인된 관계는 유지한다.
   아직 승인 연결이 없는 게시글은 retrieval 상위 목록에 없더라도 기존 82개
   Topic Pack 전체를 검색·대조한다. 검색 누락은 “적합한 Topic 없음”의 증거가
   아니다.

### 2단계: 게시글과 Topic 범위 대조

각 게시글에 대해 다음을 확인한다.

1. 게시글에서 실제로 설명하는 중심 주제와 부분 기여 하위 주제를 추린다.
2. 후보 Topic README의 핵심 범위와 ownership boundary를 확인하고, 필요하면
   관련 `fact_anchor.json`, `logic_check.json`, `model_answer.json`을 읽는다.
3. 후보 조합마다 “게시글의 어느 구체적 내용이 Topic의 어느 하위 범위에
   기여하는가?”에 답한다.
4. 같은 게시글의 나머지 후보도 서로 비교한다. 한 팩을 승인했다고 다른
   후보를 자동 승인·거절하지 않는다.
5. 결과를 `approve`, `reject`, `defer` 중 하나로 기록한다. 근거가 부족한
   경우에는 승인 수를 늘리려고 추측하지 말고 보류한다.

BM25/retrieval 점수, 순위, `matched_terms`, LLM 권고는 후보 탐색과 검토 보조
자료다. 확률이나 승인 증거가 아니며, 이들만으로 상태를 바꾸지 않는다.

### 3단계: 결정 증적

모든 적용 결정은 다음을 기록한다.

- 게시글 ID·제목·URL 및 Topic ID·제목
- 결정과 검토자 ID·시각
- 게시글의 구체적 인용 또는 절·수식·페이지 locator
- Topic README의 관련 범위와 ownership 판단
- 부분 기여인 경우 기여하는 하위 주제와 기여 한계
- OCR·사실 오류·대체 Topic·불확실성 메모
- 적용 전후 상태와 백업·입력 검토 자료의 식별정보/해시

### 4단계: 적용과 사후 확인

1. 검토 권고와 실제 최종 결정을 분리한다. CSV나 LLM 출력만으로 카탈로그를
   변경하지 않는다.
2. 승인 또는 후보 거절은 최종 결정이 명시적으로 확인된 행에만 적용한다.
   연기(`defer`)는 DB 상태를 바꾸지 않는다.
3. 기존 링크 검토 API/CLI를 사용하고 승인 시 reviewer/evidence를 제공한다.
   실패는 명시적으로 처리하며, 자동으로 성공 처리하지 않는다.
4. 승인에 따라 생성된 source-reference proposal은 별도 출처 검토·승인
   전까지 Master의 확정 출처나 학습 콘텐츠로 간주하지 않는다.
5. 작업 후 `PRAGMA quick_check`, 승인·대기·거절 관계 수, 미연결 게시글 수,
   결정 건수 및 reviewer/evidence를 대조한다. 적용 전 백업을 보존한다.
6. Topic Pack 파일이나 Master 콘텐츠를 변경하지 않았음을 확인한다. 콘텐츠를
   실제 반영하려면 별도의 Topic Pack 승인·release 절차를 따른다.

## 5. 권한 경계

| 변경 | 이 연결 절차로 허용 | 별도 절차 |
|---|---:|---|
| 게시글–Topic Pack 관계를 `approved`로 표시 | 예 | — |
| 특정 후보 관계를 `rejected`로 표시 | 예, 명백한 범위 밖일 때 | 재검토는 감사 가능한 정정 이력 필요 |
| WordPress 원문·OCR 변경 | 아니오 | WordPress 수집/동기화 정책 |
| Master `sources[]` 참조 확정 | 아니오 | source-reference proposal 검토·승인 |
| Topic Pack README/JSON, Fact Anchor, 채점 규칙 변경 | 아니오 | Topic Pack workflow, 사람 승인, release gate |
| Grading·routing·점수 변경 | 아니오 | 기존 전용 계약과 검증 |

따라서 Topic link 승인만으로 블로그 본문이 기존 Topic Pack 파일이나
Training/Grading View에 자동 노출된다고 설명해서는 안 된다. 실제 View 반영은
해당 Master source reference 및 projection 계약을 별도로 충족해야 한다.

## 6. 관련 절차와 검증

- [WordPress Topic 링크 결정 적용 절차](wordpress_topic_link_decision_application_workflow.md)
- [LLM 보조 링크 검토 지침](wordpress_topic_link_llm_review_guide.md)
- [전체 Topic 후보 검색 지침](wordpress_topic_full_catalog_retrieval.md)
- [WordPress Topic과 Review Topic 계약](wordpress_review_topic_contract.md)
- [WordPress 자료와 Grading·Review·Feedback 계약](wordpress_topic_pack_view_contract.md)

관계 상태를 변경하는 구현은 다음 focused test를 실행한다.

```bash
python3 scripts/test_wordpress_topic_link_review_application.py
python3 scripts/test_match_wordpress_posts_to_topic_packs.py
```

Topic Pack이나 Master 파일까지 변경한다면 이 링크 지침만으로 충분하지 않다.
해당 Topic Pack workflow와 release gate를 적용한다.
