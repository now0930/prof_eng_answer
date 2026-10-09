# WordPress–Topic 링크 2차 LLM 검토 개선 작업 지시서

## 1. 목적

기존 2차 LLM 검토는 179건의 행·키와 CSV 구조는 보존했지만, 1차보다 승인 권고가 13건에서 46건으로 증가했고, 인접 주제를 `high / recommend_approve`로 분류하는 사례가 확인되었다.

이번 작업의 목적은 승인 수를 늘리는 것이 아니라, **게시글의 중심 기술 내용이 Topic Pack의 소유범위와 직접 일치하는지 검증 가능한 근거로 판정하는 것**이다.

## 2. 절대 변경 금지

- WordPress SQLite DB
- Master Topic Pack 및 canonical Topic Pack
- A/B/C/D/E 채점 계약, deterministic scoring, routing authority
- 원본 후보 CSV
- 1차 및 2차 검토 CSV
- 실제 Topic 링크 승인·거절 상태

결과는 새 CSV와 별도 요약 파일로만 저장한다. 권고는 사람이 최종 승인하기 전까지 데이터베이스에 적용하지 않는다.

## 3. 입력 자료

다음 자료를 함께 읽는다.

1. 원본 후보 CSV: `wordpress_topic_link_manual_review_20261005_master33.csv`
2. 1차 검토 CSV: `wordpress_topic_link_manual_review_20261005_master33_llm_final.csv`
3. 2차 검토 CSV: `wordpress_topic_link_manual_review_20261005_second_llm.csv`
4. 후보 게시글 본문 CSV
5. 후보 출처 및 자사 OCR 텍스트 CSV
6. 게시글–출처 연결 CSV
7. 후보 Topic 범위 CSV
8. 필요한 경우 저장소의 해당 Topic `README.md`, `fact_anchor.json`, `logic_check.json`

외부 자료(`first_party=0`)는 URL·제목 등 메타데이터만 사용한다. 외부 PDF를 새로 다운로드하거나 OCR하지 않는다.

## 4. 판정 절차

각 행에 대해 아래 순서로 판단한다.

### 4.1 게시글 중심 주제 추출

- 제목만 보지 말고 `content_text` 전체에서 반복되는 핵심 개념, 수식, 절차, 장치, 시험방법을 확인한다.
- 게시글의 중심 목적과 단순 언급을 구분한다.
- 링크된 자사 PDF·이미지 OCR은 게시글 내용을 보강하는 근거로 사용하되, OCR 오류 가능성을 기록한다.

### 4.2 Topic 소유범위 확인

- README의 핵심 범위와 경계(ownership boundary)를 먼저 확인한다.
- Topic의 대표 문제, fact anchor, 제외 범위를 확인한다.
- 공통 단어 하나 또는 상위 개념이 같다는 이유만으로 승인하지 않는다.

### 4.3 직접 일치 기준

`recommend_approve`는 다음 조건을 모두 만족할 때만 허용한다.

1. 게시글의 중심 기술 주제가 Topic의 핵심 범위 안에 있다.
2. 본문에서 Topic 고유 개념이 2개 이상 확인된다.
3. 확인 가능한 구체적 근거가 있다. 예: 절 제목, 수식, 장치 원리, 계산 절차, 시험 항목.
4. 더 적합한 다른 Topic이 명백하지 않다.
5. 근거를 게시글 또는 OCR 텍스트의 위치와 함께 설명할 수 있다.

한 항목이라도 부족하면 `manual_review` 또는 `recommend_reject`로 판정한다.

### 4.4 거절과 보류 구분

- `recommend_reject`: 본문 중심 주제가 명백히 다른 분야이거나, Topic 경계에서 제외한 내용임이 확인될 때만 사용한다.
- `manual_review`: 인접 주제, 일반 개론, OCR 불완전, 본문 부족, 두 Topic 모두 가능한 경우에 사용한다.
- 검색 점수·matched_terms·제목 유사도만으로 거절하지 않는다.

## 5. 신뢰도 보정 규칙

- `high`: 구체적인 직접 근거 2개 이상과 범위 일치가 확인된 경우에만 사용한다.
- `medium`: 관련성은 있으나 범위 경계 또는 자료 완전성에 불확실성이 있는 경우.
- `low`: 제목·키워드·짧은 발췌만 있거나 OCR 신뢰성이 낮은 경우.

다음 조합은 금지한다.

- 구체적 근거가 없는 `high`
- `manual_review` 또는 `recommend_reject`인데 `llm_topic_id`를 채움
- 인접 주제를 직접 일치로 표현한 `recommend_approve`
- 같은 게시글의 여러 후보를 본문 확인 없이 일괄 승인

## 6. 특히 재검토할 오탐 유형

- Routh/Nyquist와 Bode/주파수응답을 같은 Topic으로 자동 승인하는 경우
- 일반 진동·유속·레이더·GWR 글을 초음파 ToF Topic으로 승인하는 경우
- 일반 온도센서 글을 Thermistor Topic으로 승인하는 경우
- 일반 Wheatstone bridge 글을 Strain Gauge Topic으로 승인하는 경우
- 일반 안전계측 글을 제어밸브 유지보수 Topic으로 승인하는 경우
- 일반 소프트웨어/통신/AI 글을 MC/DC, Historian, Configuration Topic으로 승인하는 경우
- 제어밸브 일반 특성·캐비테이션·소음·가스 사이징을 세부 Topic에 중복 승인하는 경우

이 유형들은 해당 세부 개념이 본문에서 실제로 전개되는지 확인하고, 그렇지 않으면 보류한다.

## 7. 출력 형식

원본의 모든 열과 행을 그대로 복사하고 다음 열만 추가한다.

- `improved_recommendation`: `recommend_approve`, `recommend_reject`, `manual_review`
- `improved_confidence`: `high`, `medium`, `low`
- `improved_topic_id`: 승인 권고일 때만 원본 후보 Topic ID
- `evidence_quote_or_locator`: 게시글 제목·절·수식·OCR 위치 등 구체적 근거
- `scope_match`: `direct`, `adjacent`, `out_of_scope`, `insufficient`
- `improvement_notes`: 1·2차 판단과 다른 이유 또는 추가 확인사항

근거는 다음 형식으로 작성한다.

`post_id=..., 본문 절/개념=..., Topic README 범위=..., 직접 일치 판단=...`

“키워드가 일치한다”, “관련성이 높다”만 단독 근거로 쓰지 않는다.

## 8. 기존 1·2차 결과와 비교

각 행의 판단을 1차·2차 결과와 비교하고 다음 중 하나를 기록한다.

- `retain_first`: 1차가 더 구체적이고 보수적임
- `retain_second`: 2차가 구체적 근거를 추가로 제시함
- `downgrade_to_manual`: 1차 또는 2차 승인 근거가 부족함
- `reject_false_positive`: 승인 후보가 Topic 경계를 명백히 벗어남
- `agree`: 세 검토가 같은 방향임

2차의 `high` 표기 자체를 근거로 삼지 말고, 본문 근거를 다시 확인한다.

## 9. 검증 조건

작업 종료 전 다음을 확인한다.

1. 입력 179행과 출력 179행이 동일하다.
2. `(post_id, link_status, candidate_topic_id)` 키가 정확히 보존된다.
3. 원본 열은 한 글자도 변경되지 않는다.
4. 승인 권고에는 구체적 근거가 2개 이상 있다.
5. `high` 승인 권고에는 `scope_match=direct`가 있어야 한다.
6. `manual_review`에는 `improved_topic_id`가 비어 있어야 한다.
7. DB와 Master 파일의 해시·수정시각이 작업 전후 동일하다.
8. 기존 deterministic 및 Golden 테스트를 실행한다.

## 10. 최종 보고

다음 항목을 보고한다.

- 전체 건수
- 승인·거절·보류 건수
- 1차·2차와의 불일치 건수
- `high` 승인 건수와 각 근거 목록
- 거절에서 보류로 변경한 건수
- 보류에서 승인으로 변경한 건수
- 사람이 최종 확인해야 할 주요 행
- DB/Master 미변경 확인

최종 결과는 권고 자료일 뿐이며, 소유자의 명시적 승인 전에는 실제 링크나 Topic을 변경하지 않는다.
