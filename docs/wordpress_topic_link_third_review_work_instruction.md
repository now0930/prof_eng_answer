# WordPress–Topic 링크 3차 검토 작업 지시서

## 목적

개선 검토표에서도 승인 권고가 45건으로 과다했고, 일부 `high` 승인이 단순 키워드 또는 일반 연관성에 의존했다. 본문에 “직접 전개되지 않음”이라고 적힌 글도 승인된 사례가 있었다.

이번 검토는 승인 건수를 맞추는 작업이 아니다. **Topic의 중심 기술 내용을 게시글이 실제로 설명하는지 입증하는 작업**이다.

## 입력 및 보호 대상

다음 자료를 읽기 전용으로 사용한다: 원본 후보 CSV, 1·2차·개선 LLM CSV, 게시글 본문·자사 OCR CSV, Topic README·fact anchor.

다음은 절대 수정하지 않는다.

- WordPress DB, Master Topic Pack, canonical Topic Pack
- 원본·1차·2차·개선 CSV
- 실제 Topic 링크 승인/거절 상태
- Grader 및 release gate

## 승인 권고의 필수 조건

`recommend_approve`는 다음 6개 조건을 모두 만족해야 한다.

1. 게시글 중심 목적이 후보 Topic 핵심 범위와 일치한다.
2. Topic 고유 개념이 본문에서 2개 이상 확인된다.
3. 서로 독립적인 기술 근거가 2개 이상 있다. 예: 정의+수식, 장치 원리+계산 절차, 시험 항목+적용 판단.
4. 각 근거에 본문 위치 또는 명확한 문장·절·수식이 있다.
5. Topic README의 ownership boundary를 침해하지 않는다.
6. 본문에 해당 Topic을 부정하거나 제외하는 문장이 없다.

“키워드가 2개 이상”인 것만으로는 독립적인 근거 2개를 충족하지 않는다.

## 승인 금지 조건

아래 중 하나라도 해당하면 승인하지 않는다.

- 본문에 “직접 전개되지 않음”, “참조만 함”, “추가 학습 필요”라고 명시됨
- 제목만 일치하고 본문 설명이 없음
- 일반 계측·제어·소프트웨어·안전 개념을 세부 Topic에 연결함
- 다른 Topic이 명백히 소유하는 중심 주제임
- 외부 PDF의 제목·URL만 있고 본문 근거가 없음
- OCR 문장이 불완전하여 기술 의미를 확인할 수 없음
- 상위 개념과 하위 구현 개념을 구분하지 않음

## 반드시 별도 확인할 오탐 조합

| 게시글 유형 | 잘못된 승인 예 |
|---|---|
| HART/FIMS·산업통신 | 양자컴퓨팅, Historian, Configuration 자동 연결 |
| Pitot·일반 유량 측정 | Control Valve gas sizing 또는 초음파 ToF 자동 연결 |
| Safety Critical Chapter 2 | Control Valve gas sizing 또는 MC/DC 자동 연결 |
| Safety Critical Chapter 4 | MC/DC 자동 연결. MC/DC 실제 설명 여부 확인 |
| 일반 Wheatstone bridge | Strain Gauge 자동 연결. strain/load-cell 적용 확인 |
| 일반 온도 센서 | Thermistor 자동 연결. NTC/PTC 특성 확인 |
| 일반 진동 측정 | LVDT 또는 초음파 자동 연결. 변환기 원리 확인 |
| SIS/안전계측 | Control Valve 유지보수 자동 연결. 정비 절차 확인 |
| 제어밸브 소음·캐비테이션 | 모든 밸브 선정 Topic에 중복 승인 |

## 부정 근거 우선 원칙

본문에 “직접 다루지 않는다”, “참조만 한다”, “상세 내용은 별도 Topic이다”, “본문 범위에 포함하지 않는다”, “예시로만 언급한다”, “링크만 제공한다”가 있으면 승인 근거보다 우선한다. 이 경우 `manual_review` 또는 `recommend_reject`로 분류한다.

## 권고 및 신뢰도 기준

- `recommend_approve`: 직접 일치 + 독립 근거 2개 이상 + 범위 충돌 없음
- `recommend_reject`: 중심 주제가 명백히 다른 Topic이거나 후보 범위 밖임
- `manual_review`: 인접 주제, OCR 불완전, 여러 Topic 가능, 근거 부족
- `high`: 독립 근거 2개 이상을 정확한 위치와 함께 제시하고 부정 근거가 없음
- `medium`: 관련성은 있으나 경계 또는 자료 품질에 불확실성이 있음
- `low`: 제목·태그·짧은 발췌 또는 OCR 의존성이 큼

근거가 일반 문장뿐이면 `medium` 이하로 낮춘다.

## 근거 작성 형식

`post_id=..., 본문 위치=..., 근거 A=..., 근거 B=..., Topic 범위=..., 경계 확인=..., 결론=...`

근거 A와 B는 서로 다른 기술 사실이어야 한다. 같은 문장의 단어 2개를 A/B로 나누지 않는다.

## 출력 파일

입력 행·열을 모두 보존하고 다음 열을 추가한다.

- `third_llm_recommendation`
- `third_llm_confidence`
- `third_llm_topic_id`
- `third_llm_evidence`
- `third_llm_scope_match` (`direct`, `adjacent`, `out_of_scope`, `insufficient`)
- `third_llm_notes`
- `comparison_to_previous` (`retain`, `downgrade`, `upgrade`, `disagree`)

승인 권고가 아니면 `third_llm_topic_id`는 공란으로 둔다.

## 검증 조건

1. 입력 179행과 출력 179행이 동일하다.
2. `(post_id, link_status, candidate_topic_id)`가 정확히 보존된다.
3. 원본 열은 변경되지 않는다.
4. 승인 권고 1건마다 독립 근거 A/B가 모두 존재한다.
5. 승인 권고는 `direct + high + candidate_topic_id 일치`여야 한다.
6. `manual_review`와 `recommend_reject`는 Topic ID가 비어 있어야 한다.
7. 부정 근거가 있는 승인 권고가 0건이어야 한다.
8. 기존 DB·Master·Topic Pack의 해시와 수정시각이 변경되지 않아야 한다.
9. 기존 review CSV validation을 실행한다.

## 최종 보고

승인·거절·보류 건수, 2차 및 개선 결과와의 불일치 건수, 승인 건별 근거 A/B, 부정 근거로 제외한 행, 사람이 최종 판단할 행, DB·Master 미변경 여부를 보고한다.

이 결과는 권고 자료이며, 사람의 명시적 승인 전에는 실제 링크나 Master에 반영하지 않는다.
