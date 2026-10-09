# 추가형 학습 레이어

학습 레이어는 기존 Topic Pack 레지스트리를 기반으로 구축됩니다. 이 레이어는
grader의 A/B/C/D/E 계약, 결정적 검사, 라우팅, 치명적 오류 처리, 표준 Question
Types, Golden 사례 또는 릴리스 게이트를 변경하지 않습니다.

```text
WordPress 게시물 / PDF / 이미지 / HTML
        │ 동기화, 버전 관리, OCR/텍스트 추출
        ▼
SQLite 소스 카탈로그 ── 게시물↔Topic 후보 연결 ── 사람 검토
                                                    │
                                           소스 참조 제안
                                                    │
                                                사용자 승인
                                                    ▼
Master Topic Pack (Topic 식별 정보, 레거시 참조, 승인된 소스)
        ├── Grading View ──► 기존 Topic Pack ──► 결정적/의미 기반 grader
        ├── Training View ─► 연습 문제, 개요, 사실, 학습 목표
        └── Feedback View ─► 최종 채점 + 진단 가이드 ─► 학습자 피드백
                                                        │
                                              SQLite 학습 이력
                                                        ▲
학습자 ── `/review <topic_id or title>` ──► 선택한 Topic 학습 자료
```

세 가지 View는 현재 Topic Pack 내용을 읽기 전용으로 투영한 별개의 뷰입니다.
Master는 Topic 식별 정보, 프로젝션 계약, 승인된 소스 참조를 관리하며, 별도의
채점 규칙 데이터베이스가 아닙니다. Feedback View는 `diagnosis` 프로젝션을
학습자에게 제공하는 용도이며, 확정된 점수나 판정을 바꾸면 안 됩니다.

## 계약 및 코드

- Master 레코드: `master_topic_packs/<topic_id>.json`
- Master 스키마: `schemas/master_topic_pack.schema.json`
- 프로젝션 어댑터: `study/master_topic_pack.py`
- 학습 이력: `study/training_history.py` 및 `schemas/training_history.schema.json`
- 선택적 큐 선택 계약: `study/review_queue.py` 및 `schemas/review_queue.schema.json`
- 채점 결과 브리지: `study/learning_workflow.py`
- 운영 grade 이력 저장: `study/learning_runtime.py`. `bot.py`가 `grade.json`을
  확정한 뒤 호출됩니다.
- WordPress 참조 및 승인 제안: `study/source_update.py`
- 선별된 Topic 콘텐츠 변경 제안 계약:
  `study/content_update.py` 및 `schemas/content_update_proposal.schema.json`
- 선별 콘텐츠 제안의 저장 및 검토: WordPress 카탈로그 데이터베이스의 별도
  `content_update_proposals` 테이블
- WordPress 카테고리 수집, 소스 카탈로그, 미디어 버전 추적, 로컬 PDF 텍스트
  추출/OCR 및 검토 명령: `scripts/wordpress_catalog.py`
- 로컬 생성 카탈로그: `data/wordpress_sources.sqlite3` (무시 대상 런타임 데이터이며,
  설정된 카테고리 URL에서 다시 생성할 수 있습니다.)

## View의 사용처와 소유권

| View | 계약 및 대상 사용자 | 현재 연결 상태 |
| --- | --- | --- |
| Grading | `project_grading()` / `grading_compatibility_payload()`는 기존 채점 소스 파일을 수정하거나 변환하지 않고 제공합니다. 기존 Topic Pack과 라우팅이 계속 기준이 됩니다. | 현재 프로젝션은 계약/통합 테스트에서 검증되며, 운영 채점 경로에서는 호출되지 않습니다. 실제 어댑터 경계에서 호환성이 입증될 때까지 의도적으로 이렇게 유지합니다. |
| Training | `project_training()`은 질문 패턴, 예시, 개요, 사실 앵커, 고득점 포인트, 학습 목표, 해시로 고정된 WordPress HTML, 선택적인 선별 worked example을 제공합니다. 선별 보조 자료에는 소스 근거와 명시적인 검토 상태가 포함되며, 이 입력은 어느 것도 정규 채점 사실이 아닙니다. | `/review <topic_id or title>`는 날짜를 기준으로 삼지 않고 사용자가 선택한 Topic을 확인한 다음 질문, 개요, 사실, 소스 기반 보조 자료를 표시합니다. |
| Feedback | `project_diagnosis()`는 앵커, 치명적 오개념, 결정적 검사, `score_effect: none`인 가이드, 일치하는 선별 학습 보조 자료의 참조를 제공합니다. | 확정된 시도 기록에는 기존의 grade 기반 진단과 추가 `topic_guidance` 페이로드가 저장됩니다. 사용자가 선택한 리뷰는 저장된 이전 약점과 Topic 가이드를 별도로 보여 주며, 어느 쪽도 채점에 다시 반영되지 않습니다. |

운영 순서는 다음과 같습니다. 현재와 똑같이 grade를 확정하고, Training 및 Feedback
View를 읽기 전용 페이로드로 만들고, 최종 점수와 구조화된 피드백을 저장한 다음,
학습자가 리뷰할 Topic을 선택하도록 합니다. 선택적 큐 계약은 Telegram 리뷰
선택기가 아닙니다. Grading View를 별도의 채점 구현으로 만들어서는 안 됩니다.
향후 grader 어댑터를 전환하려면 별도의 동등성 및 회귀 검증 단계가 필요합니다.

### Learning-runtime View 어댑터: 구현 완료

제한된 어댑터 단계는 `study/learning_runtime.py`에 구현되어 있으며,
`bot.py`의 채점 및 점수 확정 경로와 분리되어 있습니다.

1. `_master_question()`은 Training View를 통해 프롬프트와 예시를 읽고, 기존의
   질문 선택 결과를 유지합니다. 프로젝션을 사용할 수 없으면 레거시 소스를
   사용합니다. 기존 선택 우선순위를 보존하기 위해 프로젝션은
   `question_examples`를 제공합니다.
2. `record_completed_grade()`는 확정된 grade에서 저장할 진단을 도출한 뒤,
   Diagnosis View의 가이드를 별도의 점수 중립적 `topic_guidance` 필드에
   첨부합니다. 이 어댑터는 점수를 계산하거나 판정을 바꾸거나 자체 신호를
   치명적 오류로 승격할 수 없습니다.
3. Master/View 데이터가 없거나 형식이 잘못되어도 grade 이력 저장은 차단되지
   않습니다. 채점과 정규 grader는 변경되지 않습니다.

#### 이 어댑터 경계의 회귀 게이트 (향후 변경 시 필수)

- **Training 어댑터 동등성:** 대표적인 Master Topic에서 선택된 질문 ID/텍스트가
  어댑터 도입 전 레거시 동작과 동일해야 합니다. 예시/패턴이 비어 있는 경우와
  대체 동작도 테스트합니다.
- **Feedback 격리:** 어댑터 사용 전후의 grade를 비교하여 `final_total_score`,
  `total_score`, `verdict`, `score_status` 및 기존의 모든 grade 필드가 그대로인지
  확인합니다. 가이드의 `score_effect == "none"`도 확인합니다.
- **저장 호환성:** 기존 이력 필드와 SQLite 스키마를 계속 읽을 수 있어야 합니다.
  피드백 추가 필드는 선택 사항이어야 하며 기존 행도 계속 불러올 수 있어야 합니다.
- **통합 실패 격리:** View 데이터가 없거나 유효하지 않아도 확정된 grade 응답이
  차단되거나 이미 저장된 grade가 손상되어서는 안 됩니다.
- Master 스키마/프로젝션/Training 진단/이력/큐/통합 테스트, bot 학습 이력 통합
  테스트와 기존 Grader 결정적 검사, 치명적 오류, 표준 라우팅, Golden 및 릴리스
  게이트 테스트를 실행합니다. 어댑터를 수용하기 위해 기존 게이트를 수정하거나
  완화해서는 안 됩니다.

이 구현은 `scripts/test_learning_runtime.py`,
`scripts/test_bot_learning_history_integration.py`,
`tests/test_master_view_private_end_to_end.py` 및 기존 전체 릴리스 검증으로
검증됩니다. 향후 Grading View 또는 운영 채점 경로를 변경하는 것은 별도 범위이며,
그에 대한 자체 동등성 및 회귀 검증 단계가 필요합니다.

## WordPress 변경 제안 라이프사이클

1. WordPress 게시물과 자사 미디어를 소스 카탈로그에 동기화합니다. 상위 게시물 URL,
   정확한 에셋 URL, 소스 ID, 버전/해시, 타임스탬프, 추출 텍스트를 기록합니다.
   PDF 바이너리는 카탈로그 밖에 두고 OCR 텍스트는 로컬에 저장합니다.
2. 제목, 요약, 태그를 바탕으로 게시물과 Topic의 연결 후보를 생성합니다. 점수는
   순위를 정하기 위한 참고값일 뿐입니다. 각 매핑은 사람이 승인하거나 거부합니다.
3. 승인된 각 Topic/소스 쌍에 대해 소스 참조 제안을 대기열에 넣습니다. Topic에
   Master가 아직 없으면 `waiting_for_master` 상태로 두고, Master가 있으면 현재
   Master revision을 기준으로 `pending_approval` 상태를 사용합니다.
4. `--preview-proposal ID`는 보류 중인 제안 하나를 현재 Master와 대조하고,
   `--preview-pending-proposals`는 대기 중인 제안 전체를 확인합니다. 둘 다 파일을
   쓰지 않고 변경 전후의 참조를 표시합니다. 명시적으로 승인하면 소스 참조를
   추가하거나 교체하고 Master revision을 증가시킵니다. 카탈로그 승인과 원자적인
   Master 교체는 롤백 및 커밋 결과가 모호한 경우의 조정 절차로 보호됩니다. 다른
   보류 제안은 새 기준에 맞게 갱신되지만, 각각 별도의 승인이 여전히 필요합니다.
   적용된 참조도 내용과 위치를 확인할 때까지 `unverified` 상태로 유지됩니다.
5. 소스가 변경되면 `source_change_events`에 이전/새 버전 또는 해시를 기록하고,
   승인된 연결이 있는 Topic에 대한 제안을 생성합니다. 승인된 Topic 연결이 없는
   이벤트는 `pending_topic_review` 상태로 유지됩니다.

소스 참조 제안이 승인되고 새 `updated_at`이 Master에 기록된 뒤에만 Topic이
`recently_changed_topic` 리뷰 대상이 될 수 있습니다. 승인되지 않은 카탈로그
이벤트나 제안은 학습자의 큐 또는 Training/Feedback View를 변경하지 않습니다.
카탈로그에서 Master로 이어지는 승인 경계와 그에 따른 리뷰 후보 신호는
`scripts/test_wordpress_review_integration.py`에서 검증합니다.

사람이 매핑을 검토할 때 `--export-topic-link-review PATH`는 승인된 연결, 보류 중인
후보 연결, 연결되지 않은 게시물을 담은 저장소 내 CSV 스냅샷을 생성합니다. 기존
파일을 덮어쓰지 않습니다. 각 행에는 게시물 제목/URL/요약/태그, 후보 Topic 및
어휘 기반 근거, 연결된 에셋 메타데이터가 포함됩니다. 이 내보내기는 카탈로그를
수정하지 않습니다. 검토 후에도 각 매핑은
`--review-topic-link POST_ID TOPIC_ID approve|reject`로 개별 적용해야 합니다.
LLM을 보조 수단으로 쓰는 추천 전용 검토 절차는
`docs/wordpress_topic_link_llm_review_guide.md`에 설명되어 있습니다. 이 절차는
자동 승인이나 Master/Topic 편집을 명시적으로 금지합니다.

현재 이 라이프사이클은 정규 사실이나 채점 규칙이 아니라 소스 참조를 갱신합니다.
Training View는 이미 연결된 비공개 WordPress 소스 묶음에서 추출한 원문을 콘텐츠
해시 및 `unverified` 상태와 함께 학습 자료로 노출할 수 있습니다. 이 텍스트를
요약하거나 정규화하거나 채점/진단 사실로 승격하지는 않습니다. 중요한 WordPress
콘텐츠 변경으로 선별된 Topic 내용이 조용히 바뀌어서는 안 됩니다. 이후 콘텐츠
정리 제안은 영향을 받는 Fact/섹션을 지정하고 소스 차이와 근거를 제시하며, 정규
Topic 내용을 변경하기 전에 승인을 받아야 합니다. 이렇게 하면 소스 기반 학습 자료
접근과 지식 콘텐츠 변경을 분리할 수 있습니다. 선별된 worked example은
`study/learning_materials/`에 두고 Master에서 연결해야 합니다. 근거 해시와 위치
정보, 점수 중립 필드 및 명시적인 검토 상태를 포함해야 하며,
`rubrics/topic_packs/`나 생성된 bank에는 기록하지 않습니다.

콘텐츠 제안 전용 계약은 소스 참조 업데이트와 별개입니다. 이 계약은 Master
revision, 대상 소스 키/레코드/필드, 변경 전 텍스트와 제안 텍스트, 소스
ID/URL/버전/해시, 위치 정보와 근거 발췌문을 고정하고 영향을 받는 View를
도출합니다. 명시적인 승인/거부는 처리자와 시간 정보와 함께 기록됩니다. 승인된
변경은 기준 revision, 연결된 근거, 대상의 유일성, 변경 전 값이 여전히 일치할
때만 메모리 내 후보로 변환할 수 있습니다. `--prepare-content-candidate ID`는
결과를 해시 manifest가 포함된 격리된 저장소 내 후보 묶음에 기록합니다. Master나
정규 Topic 파일은 덮어쓰지 않습니다. 정규 반영에는
`--apply-content-candidate ID --applied-by NAME`을 사용합니다.
`candidate_ready` 카탈로그 레코드가 있어야 하며 후보 묶음, 현재 revision, 대상의
변경 전 값을 다시 확인한 뒤 반영 처리자와 시간을 기록합니다.
`--validate-content-candidate ID`는 정규 파일이나 제안 상태를 변경하지 않고 사전
검증을 수행합니다. 대상, 변경 전후 값, 근거, 영향을 받는 View, 소스 근거, 나중에
반영할 때 교체될 파일을 출력합니다. 파일 교체가 실패하면 반영 과정은 롤백을
시도합니다. 어느 명령도 회귀/릴리스 게이트를 실행하지 않습니다. 실제 제안을
반영하기 전후에 해당 게이트를 실행해야 하며, 해당 콘텐츠 제안에 대한 사용자의
명시적 승인 없이 반영해서는 안 됩니다.

보류 중인 제안은 소스 참조 제안과 독립적으로 저장하고 검토할 수 있습니다.
`--list-content-proposals`는 제안 목록을 표시합니다.
`--approve-content-proposal ID --reviewed-by NAME`은 승인만 기록하고,
`--reject-content-proposal ID --reviewed-by NAME`은 거부만 기록합니다. 승인 시
현재 Master revision과 연결된 소스의 식별 정보/URL을 확인합니다. 정규 Topic
파일을 쓰거나 현재 제공 중인 View를 변경하지 않습니다. 승인된 제안만 후보 묶음을
생성할 수 있으며, 생성 후 카탈로그에서 `candidate_ready` 상태로 표시됩니다.

이력 데이터베이스 경로는 호출자가 지정합니다. 각 시도에는 질문과 Topic 식별 정보,
시도 시각, 최종 점수, 구조화된 진단, 리뷰 상태, 마지막 리뷰 시각 및 다음 리뷰
시각이 저장됩니다. 큐 계약은 기본적으로 서로 다른 Topic에서 각각 하나씩 약점
항목과 복습 항목을 사용합니다. 선택 후보는 호출자가 제공하므로 순위 정책은 저장
방식과 독립적으로 발전할 수 있습니다.

Telegram 리뷰는 날짜가 아니라 사용자가 선택합니다. `/review <topic_id or title>`을
사용하면 어떤 Master Topic이든 요청할 수 있습니다. 정확한 Topic ID와 제목이
우선되며, 유일하게 일치하는 부분 문자열도 허용됩니다. 일치 항목이 모호하면
학습자가 선택할 수 있도록 해당 항목을 나열합니다. `/review done <topic_id>`는
해당 Topic이 선택적 큐에 있었는지와 관계없이 유효한 Master Topic의 리뷰 완료를
기록합니다. 같은 Topic에 `/review`를 반복해도 일일 큐를 소모하거나 순환시키지
않습니다.

`review_queue` 스키마와 선택기는 나중에 사용할 선택적 계약으로 유지되지만,
Telegram의 `/review` 명령은 일일 큐 스냅샷을 만들거나 읽지 않습니다. 채점은
시도 기록과 점수 중립적 진단만 저장하며, 부수 효과로 날짜별 큐를 만들지 않습니다.

학습자가 채점된 답안을 제출하기 전에도 새 Topic을 리뷰 완료로 표시할 수 있습니다.
리뷰 시각은 점수가 있는 시도와 별도로 저장되므로 리뷰만으로 점수나 진단을
만들어내지 않습니다. `next_review_at`은 과거의 일정 관리 메타데이터로 남으며,
수동 Topic 선택을 제어하지 않습니다.

Telegram 어댑터는 `chat_id`를 학습자 범위로 사용합니다. Topic이 라우팅된 모든
성공적인 grade는 `grade.json`을 기록한 뒤 저장됩니다. 이력 쓰기에 실패하면
로그에 기록되며 grade를 변경하거나 차단하지 않습니다. `/review <topic_id or
title>`은 선택한 Topic의 Training View와 이전의 점수 중립적 가이드를 그대로
표시하고, `/review done <topic_id>`는 수동 리뷰와 그 시각 정보를 기록합니다.
Telegram 명령은 날짜 기반 후보 순위를 사용하지 않습니다.

카탈로그 동기화와 소스 변경 감지는 구현되어 있지만 Master 레코드에 자동으로
쓰는 기능은 비활성화되어 있습니다. 승인된 Topic 매핑에 연결된 변경은
`pending_approval` 소스 참조 제안을 생성합니다. 이를 적용하려면 승인자 식별
정보와 현재 Master revision이 일치해야 합니다.

첫 번째 카탈로그 수집은 `scripts/wordpress_catalog.py`에 설정된 Industrial
Instrumentation/Control Engineer 카테고리를 대상으로 합니다. 카테고리의 모든
게시물과 PDF, 이미지, HTML, Overleaf 링크를 색인화합니다. 후보 Topic 연결은 제목,
요약, 태그를 바탕으로 생성되며 `pending_review` 상태를 유지합니다. 어휘 점수는
순위를 돕기 위한 값이지 보정된 확률이 아닙니다. 후보는 Master에 자동 복사되지
않습니다. 후보 연결을 승인하면 별도의 소스 업데이트 제안이 대기열에 들어갑니다.
그 제안을 적용하려면 승인자를 명시해야 합니다. 기존 Master 레코드가 없는
게시물은 `waiting_for_master` 상태로 대기합니다.

카탈로그는 소스 URL, WordPress 미디어 식별자와 수정 시각, 게시물 텍스트, 콘텐츠
해시, 추출된 PDF 텍스트를 저장하지만 미디어 바이너리는 저장하지 않습니다.
여기서 자사(first-party) 도메인은 `now0930.pe.kr` 및 그 하위 도메인을 뜻합니다.
이 도메인의 PDF만 다운로드/OCR 후보가 됩니다. 자사 PDF에서는 디지털로 포함된
텍스트를 페이지별로 추출합니다. 사용할 수 있는 내장 텍스트가 없는 페이지는
로컬에서 렌더링한 뒤 한국어 및 영어 언어 데이터를 사용하는 Tesseract로
인식합니다. 외부 PDF 링크는 메타데이터로만 보존하며 다운로드하거나 OCR 처리하지
않습니다. `python3 scripts/wordpress_catalog.py --ocr`를 실행하면 카탈로그를
동기화하고 처리가 대기 중인 자사 PDF를 처리합니다. Debian/Ubuntu에서는 먼저
`tesseract-ocr`, `tesseract-ocr-kor`, `tesseract-ocr-eng`, `poppler-utils`를
설치합니다. 검토 및 승인 절차에는 `--list-pending`,
`--review-topic-link POST_ID TOPIC_ID approve|reject`,
`--approve-proposal ID --approved-by NAME`을 사용합니다. 매칭되지 않은 게시물도
같은 `--review-topic-link` 명령으로 직접 선택한 Topic ID를 승인할 수 있습니다.
