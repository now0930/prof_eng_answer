# AI·Codex 실행 계약: WordPress URL → 비공개 DB → Topic Pack

> **문서 성격: 구현된 URL 수집 실행기 + 아직 분리된 승인·Fact 검증 계약.** URL 하나로 수집·검색은 실행되지만, 기술적 판단/링크 승인·Master 출처 승인·채점 승격까지 자동으로 완료되지는 않습니다.
> 사람용 방향은 [WordPress URL 지속 운영 정책](wordpress_url_continuous_workflow.md)입니다.
>
> **우선순위:** `AGENTS.md`와 현재 코드·실제 DB 상태 → 이 계약 → [링크 판정 정책](wordpress_topic_pack_linking_policy.md) → [Master/View](wordpress_topic_pack_view_contract.md) → 과거 보고서. 충돌을 발견하면 원인·영향을 보고하며 권한을 임의로 넓히지 마세요.

## 1. 한 문장 불변 목표

한 URL의 **출처 식별·변경 추적 → Topic 소유 범위에 따른 연결 → 비공개 학습 출처 제공**을 완성하고, **검증을 거친 Fact만 승인 절차로 채점 자료에 반영**합니다. 기존 Topic의 재사용과 기술 사실의 신뢰성을 우선합니다.

## 2. 현재 구현 지도 — 반드시 실제 코드 확인

| 단계 | 현재 코드·자료 | 실제 동작 / 주의 |
| --- | --- | --- |
| URL 통합 실행 | `scripts/wordpress_url_workflow.py` | 지정된 자사 HTTPS 게시글 permalink 1건의 REST 수집·비공개 백업·변경 추적·OCR·Topic 후보·개별 보고, **자동 승인 금지** |
| 수집·DB | `scripts/wordpress_catalog.py` | 기존 카테고리 동기화 및 데이터·OCR 핵심 함수 재사용. `--category-url`은 **게시글 URL 입력용이 아님**. 기본 DB: `data/wordpress_sources.sqlite3` |
| PDF/이미지 | 동일 파일 `--ocr --ocr-images` | 자사 자료만 추출·Tesseract OCR. 결과·오류·버전 관리. OCR 성공 ≠ Fact 검증 |
| 후보 검색 | `scripts/match_wordpress_posts_to_topic_packs.py` | `--post-id` 선택 가능, 모든 기존 Topic의 README·선별 source JSON 대조, 비공개 검색 캐시. 최대 12개 후보는 검색 결과일 뿐 전수 의미 판정 아님 |
| 링크 판정 | `wordpress_catalog.review_topic_link()` 및 `--review-topic-link` | `approved/pending_review/rejected`. 새 승인에는 명시적 reviewer와 evidence가 필요합니다. 카탈로그 CLI에서는 `--reviewed-by`와 `--link-evidence`를 사용합니다. 기존 동일 결정의 재실행은 승인 기록을 변경하지 않습니다. |
| Master 출처 제안 | `study/source_update.py`, `--preview-proposal`, `--approve-proposal ID --approved-by NAME` | Topic link 승인 뒤 source proposal 생성. Master revision·source identity 검증과 별도 명시 승인 필요 |
| 비공개 학습 bundle | `scripts/build_wordpress_topic_packs.py` | 승인된 Topic link와 자사 source만 `data/wordpress_topic_packs/<topic_id>.json`에 생성. 개별 필터 `--topic-id`, `--post-id` 지원 |
| Training/Review | `study/wordpress_topic_pack.py`, `study/topic_views.py`, `study/learning_runtime.py` | 유효한 Master 출처·해시 계약에 맞는 학습 참조; 실제 `/review`와 점수 중립 자료. `Grading View`는 운영 채점 엔진 직접 입력이 아님 |
| 콘텐츠 변경 | `study/content_update.py`, `wordpress_catalog.py`의 content proposal CLI | `pending_approval`→ 승인→후보·검증→명시적 적용. source revision·before-value·hash 검사 필수 |
| canonical Topic | `rubrics/topic_packs/<topic_id>/`, `scripts/rubric_manager.py` | 신규/수정은 Topic Sheet·Fact 적격성·승인·hash·focused validation을 통과 |
| 운영 bank | `rubrics/generated/` | 빌더 산출물. 직접 편집·WordPress OCR 자동 주입 금지 |
| 운영 코드 검증 | `scripts/release_candidate.py validate` | 전체 **오프라인 pytest**. 과거 Accuracy/Authority/Stability·유료 qualification은 배포 필수 아님 |

상세 계약: [WordPress OCR](wordpress_topic_pack_ocr.md), [전체 후보 검색](wordpress_topic_full_catalog_retrieval.md), [링크 판정](wordpress_topic_pack_linking_policy.md), [Fact 적격성](fact_anchor_eligibility_policy.md), [Topic 작성·승인](topic_pack_workflow.md), [비공개 백업](private_runtime_backup.md).

## 3. URL 처리 상태기계 — 보고용, DB 신규 필드 아님

아래 레이블은 **작업 보고의 단계 이름**입니다. 기존 SQLite의 `status` enum이나 마이그레이션 요구사항이 아닙니다.

| 보고 단계 | 진입 조건 | 종료 조건 |
| --- | --- | --- |
| IDENTIFIED | URL 제공 | 게시글 ID·정규화 주소·기준 버전 확인 |
| SOURCE_CAPTURED | 글이 카탈로그에 존재 | 수집 결과·OCR 상태·해시·오류 기록 |
| TOPIC_REVIEWED | 비교 가능한 출처 확보 | 후보별 근거·부분 기여·소유권·승인/보류/거절 기록 |
| SOURCE_LINKED | 링크 승인 | Master 출처 승인 완료 또는 미승인 이유 명시 |
| LEARNING_READY | 유효한 Master 참조 및 bundle 확보 | 비공개 학습 소비 경로 확인 |
| FACT_TRIAGED | 기존 Fact와 기술적 대조 | 중복·보완·충돌·신규·보류 분류 및 근거 |
| CONTENT_APPLIED | 별도 내용 승인·실제 변경 필요 | 승인 기록·hash·회귀 증거 확보, 아니면 NOT_REQUIRED |
| CLOSED_OR_BLOCKED | 처리 결과 정리 | 완료/보류·재시도 조건·다음 조치 보고 |

**단계 건너뛰기 금지:** 링크 승인, Master source reference 승인, Fact 진위 확인, 채점 콘텐츠 반영은 독립 게이트입니다. 글이 연결되지 않았어도 Fact 검토 제안은 가능하나 그 제안이 자동 적용됐다고 기록하지 않습니다.

## 4. 실행 절차

### A. 시작 전 불변조건

1. 현재 브랜치 HEAD, 실제 실행 환경, DB 존재·경로, Topic manifest 및 연결 상태를 확인합니다.
2. **읽기 전용으로** 동일 post ID/URL과 저장된 hash·source 상태·기존 승인 연결을 조회합니다. 먼저 데이터 수정부터 하지 않습니다.
3. 새 수집·승인으로 DB/파일을 변경한다면 [비공개 백업/복원](private_runtime_backup.md)을 수행하고 복원 가능성을 검증합니다. `PRAGMA quick_check`만으로 전 파일 동기 백업을 증명하지 않습니다.
4. 개별 URL은 **`scripts/wordpress_url_workflow.py URL`**로 처리합니다. 자사 HTTPS `/wordpress/<slug>/`와 설정된 기술사 카테고리를 API로 재확인합니다. `--category-url`은 게시글 주소 입력용이 아닙니다. 사이트 범위 밖의 글·퍼머링크 변경은 자동 수집/치환하지 않습니다.
5. 원문 본문은 수정하지 않으며, 미검증 OCR 결과를 근거 없이 보정하지 않습니다. 외부 URL의 PDF·이미지를 새로 OCR하지 않습니다.

### B. 수집·후보 탐색

명령은 **실행 예**이며 요청이 왔다고 자동 수행되는 기능이 아닙니다. 비공개 서버의 설정·의존 도구·DB 경로부터 확인합니다.

```bash
# 신규/수정 URL: REST 수집 → SQLite 외부 백업(기존 DB) → 게시글 범위 OCR
# → 전체 기존 Topic 검색 shortlist → 비공개 상태 보고
python3 scripts/wordpress_url_workflow.py "https://now0930.pe.kr/wordpress/자기회로/"

# 이미 수집된 글: 원문/DB 갱신 없이 기존 후보·상태 재확인
python3 scripts/wordpress_url_workflow.py "https://now0930.pe.kr/wordpress/자기회로/" --offline

# 자사 미디어를 다시 내려받아 hash 확인할 때만 (비용·시간 주의)
python3 scripts/wordpress_url_workflow.py "https://now0930.pe.kr/wordpress/자기회로/" --refresh-assets

# 카테고리 전체 대량 동기화가 필요하면 기존 명령을 별도 사용
python3 scripts/wordpress_catalog.py --ocr --ocr-images
```

새 실행기는 실서버의 Tesseract(한국어·영어) 및 Poppler 설치를 확인합니다. 없으면 OCR을 미완료/경고로 보고하며, PDF·이미지를 검증된 Fact처럼 다루지 않습니다. **동일 hash와 메타데이터면 본문을 다시 쓰지 않고**, 기존 승인 연결을 보존합니다. 리포트는 공개 Git이 무시하는 `data/wordpress_url_intake/`에 0600 권한으로 새 파일을 만듭니다. SQLite 백업 기본 위치는 `~/hermes/private_backups/prof_eng_answer/wordpress_url_intake/`이며 DB 쓰기 전에 실행됩니다.

- 글이 신규인지, 동일 URL/ID의 버전 변경인지, 미변경인지 hash로 분류합니다.
- post 본문과 자사 PDF/이미지 OCR은 근거 성격이 다르므로 분리해서 대조합니다. OCR의 출처 URL·페이지·방법·빈 텍스트·에러를 보고합니다.
- 자사 자료 요청에서 외부 리다이렉트는 따라가기 전에 차단합니다. 기존 DB의 백업은 SQLite `quick_check`를 통과한 뒤 확정합니다. 개별 OCR 실패는 재시도할 수 있도록 기록되며, 이미 커밋한 수집 데이터를 자동 복원하지 않습니다.
- 검색 상위 결과만 보고 종료하지 않습니다. candidate 누락 가능성을 인정하고 필요한 경우 **전체 Topic owner 범위**를 확인합니다.
- URL·post ID가 확인되지 않으면 **BLOCKED: SOURCE_NOT_FOUND**로 남기고 성공 판정을 하지 않습니다.

### C. 링크 검토·적용

한 글이 여러 Topic에 부분 기여할 수 있습니다. 후보마다 (post ID, Topic ID, source locator, 구체적 기여, ownership, 충돌·불확실성, reviewer, 시간)을 남깁니다.

- **Approve**: 본문·자사 OCR에 실질 기술 설명이 있고 해당 Topic의 하위 소유 범위에 직접 기여하는 근거가 있음.
- **Defer**: 본문 부족, OCR 불명확, scope 경쟁, 기술 오류·근거 미해결. DB 링크 상태를 임의 승인하지 않음.
- **Reject**: 그 **특정** post–Topic 조합이 명백히 범위 밖임. 글 전체의 가치를 거절하는 뜻 아님.

통합 실행기는 **명시적 리뷰 인자**를 받은 경우에만 기존 `review_topic_link()`를 호출합니다. 먼저 원문·Topic README를 대조하고 reviewer와 구체적인 원문 위치를 결정한 뒤 실행합니다.

```bash
python3 scripts/wordpress_url_workflow.py "https://now0930.pe.kr/wordpress/자기회로/" \
  --offline --topic-id ACTUAL_TOPIC_ID --decision approve \
  --reviewer ACTUAL_REVIEWER --evidence "게시글 제2절, 측정 원리의 수식과 Topic 범위 대조"
```

`ACTUAL_TOPIC_ID`·`ACTUAL_REVIEWER`는 자리표시자입니다. 검토자·근거를 적는 것은 **자동 의미 검증이 아니며**, 확정 근거가 없으면 승인하지 않고 보류합니다. 기존 승인/거절을 다른 판정으로 덮어쓰는 시도는 차단합니다. DB가 변경되는 경우에는 별도 비공개 백업을 먼저 생성합니다.

### D. Master·학습 출처

링크 승인만으로 Master의 `sources[]`가 확정되는 것은 아닙니다.

```bash
# 출처 제안 미리보기 (파일을 바꾸지 않음)
python3 scripts/wordpress_catalog.py --preview-pending-proposals

# 적법한 승인·revision·source hash 검증 후 개별 적용
python3 scripts/wordpress_catalog.py \
  --approve-proposal PROPOSAL_ID --approved-by APPROVER_ID

# 승인된 링크에 해당하는 비공개 학습 source bundle만 생성
python3 scripts/build_wordpress_topic_packs.py \
  --topic-id example_topic_id --post-id 123
```

`--approved-by`는 실제 승인 식별자만 사용합니다. 테스트용 `PROPOSAL_ID`, `APPROVER_ID`, `example_topic_id`를 실제 값처럼 실행하지 않습니다. bundle을 만든 뒤에도 Master source URL/version/hash 일치를 확인하고 학습 기능에서 접근 가능한 상태인지 별도로 검증합니다. 채점용 bank는 이 단계에서 **변경 0**이어야 합니다.

통합 실행기는 대상 Topic의 승인된 게시글을 모두 포함해 기존 자료를 유지합니다. 동일한 bundle은 파일과 생성 시각을 그대로 두고 `stats.unchanged_topics`로 집계합니다. 위 `--post-id` 명령은 범위를 제한한 산출물로 기존 Topic bundle을 교체하므로 정상 증분 갱신에는 사용하지 않습니다.

### E. Fact 검토·반영

1. 기존 Topic의 `README.md`, `fact_anchor.json`, `model_answer.json`, `logic_check.json`, `question_demand_axes.json`(존재 시)을 실제로 읽습니다.
2. WordPress의 각 주장에 대해 물리법칙·검증 가능한 산업 표준/공식 기술문서·한정 조건을 대조합니다. WordPress 자체는 사용자 설명 자료이지 외부 독립 검증의 대체물이 아닙니다.
3. 각 Fact를 `already_supported / extend_existing / correct_existing / new_candidate / hold`로 분류합니다. **이 이름들은 보고용 분류이며 Registry 상태 enum이 아닙니다.**
4. 단순 중복은 생성 금지. 지나치게 세부적인 제품·현장 특수 주장은 일반 채점 Fact로 승격하지 않습니다. 독립적인 새 Topic은 기존 owner의 범위로 처리할 수 없을 때만 검토합니다.
5. 실제 내용 변경이 필요한 경우 **content proposal**을 만들고 현재 Master revision, 원본 source hash, 변경 전 값·대상·근거를 묶어 별도 검증을 진행합니다. 예: `--list-content-proposals`, `--approve-content-proposal ID --reviewed-by NAME`, `--prepare-content-candidate ID`, `--validate-content-candidate ID`, `--apply-content-candidate ID --applied-by NAME`. 순서를 건너뛰거나 승인되지 않은 후보를 적용하지 않습니다.
6. AI 위임 검토는 [AGENTS](../AGENTS.md)의 **실제 AI 모델 ID·review-method·근거 보고서** 기준을 따릅니다. AI의 검토 권한과 content proposal의 명시적 승인/적용 권한을 혼동하지 않습니다.
7. Topic source가 바뀌면 관련 focused test, hash·generated 정합성, 전체 오프라인 pytest(배포용)를 수행합니다. 유료 provider Gate, 폐지된 10회 전용 재채점을 새 필수조건으로 만들지 않습니다.

## 5. 방향 이탈 감시 — 매 단계 반드시 YES/NO

| 검사 | YES인 경우에만 계속 | NO라면 |
| --- | --- | --- |
| 이번 작업이 현재 URL·관련 Topic의 가치에 직접 기여하는가? | 범위 유지 | 별도 backlog에 격리 |
| 기존 Topic owner와 Fact를 먼저 조회했는가? | 연결·내용 검토 가능 | 신규 Topic/Fact 생성 중단 |
| 검색 추천 대신 출처 locator·실질 기여 근거를 확인했는가? | 승인 검토 가능 | `defer` |
| 링크 승인과 Fact의 진위/채점 적격성을 구별했는가? | 다음 게이트 가능 | 콘텐츠 반영 중단 |
| reviewer·revision·hash·before-value·backup·rollback이 추적 가능한가? | 쓰기 허용 검토 | 비공개 DB·canonical 쓰기 중단 |
| OCR/원문·개인 데이터·자격정보의 Git 유출 가능성이 없는가? | 문서·코드 커밋 가능 | 공개 아티팩트 작성 중단 |
| 코드 변경이 실제로 필요하며 기존 프로그램 범위를 유지하는가? | focused test 후 수행 | 새 개발 제안으로 분리 |
| 실행하지 않은 단계·테스트를 완료로 표시하지 않았는가? | 결과 보고 | 보고 수정 후 계속 |

**우선순위:** P0 보안·백업·중복 방지 → P1 수집/OCR 신뢰도 → P2 기존 Topic 연결 → P3 학습용 Master/source 최신화 → P4 기술 Fact 검증·선별 반영 → P5 사용량 증거가 있는 자동화. P5가 P0~P4를 대체하지 않습니다.

## 6. 반복 실행·멱등성·차단 조건

- 동일 post/source hash 및 기존 approved link에서는 **중복 승인·새 Fact·중복 Master 제안 생성 금지**. 기존 파이프라인의 idempotency 검사를 다시 확인합니다.
- 게시글 수정 시 변경된 source와 연결된 Topic부터 재검토합니다. 기존 승인 이력을 덮어쓰지 않습니다.
- source fetch/OCR 실패는 `sync_errors`로 남기고 재시도를 계획합니다. 실패를 성공 또는 `rejected`로 바꾸지 않습니다.
- Master revision 불일치·원문 hash 변경·승인 경계 불확실·복원 불가·비공개 노출 우려는 **BLOCKED**. 자동 재승인하거나 게이트를 완화하지 않습니다.
- `/review`는 사용자가 Topic을 지정하는 **수동 복습**입니다. 주소 등록으로 날짜별 자동 큐가 즉시 만들어진다고 설명하지 않습니다.
- **단일 URL 실행기(수집·OCR·retrieval·단계 보고)는 구현됨.** 정기 스케줄러, AI 자동 링크 판단·Fact 검증, 실제 비공개 서버 배포 및 봇 재시작은 별도 작업입니다.

## 7. 매 URL 결과 보고 계약

실행기는 `wordpress-url-workflow-v1` JSON을 비공개 `data/wordpress_url_intake/`에 기록합니다. 아래는 **사람용 보고 템플릿**으로, `fact_triage`는 자동 승인·개별 기술 검증이 아닌 미검증 상태를 표시합니다. 개인 원문·OCR 전문·세션 원본을 공개 보고서에 넣지 않습니다.

```text
URL / post_id / source_version_or_hash:
현재 브랜치 / 실행 환경 확인:
수집: 신규 | 변경 | 동일 | 실패 | 미실행
OCR: PDF/이미지 성공·실패·미실행 및 사유
Topic link: approved / pending_review / rejected (각 근거 locator)
Master source: applied / pending_approval / not_required / blocked
Training source: ready / pending / not_checked
Fact: already_supported / extend_existing / correct_existing / new_candidate / hold
Canonical Topic 수정: 파일·승인 기록·source hash·검증 결과 또는 변경 없음
백업/무결성: 실제 실행·미실행·실패
프로그램 테스트: 실제 명령 / pass·fail·skip / 미실행
다음 작업 1순위 및 blocker:
```

### 완료 판정

- **기본 출처 처리 완료:** 출처 버전·OCR 상태가 기록되고, Topic 후보마다 처리/보류 이유가 남아 있음.
- **학습 연결 완료:** 승인된 링크·Master 참조·비공개 bundle·실제 소비 경로가 검증됨. 미승인 시에는 이 완료를 주장하지 않음.
- **채점 내용 변경 완료:** 별도 Fact 검증·적법한 승인·source/generated 정합성·테스트가 확인된 경우에만 사용.
- **단순히 관련 Fact가 없거나 수정이 불필요한 경우:** `NOT_REQUIRED`로 종료할 수 있으며, 이 상황을 실패나 누락으로 세지 않음.
- **어느 단계든 미실행이면** 전체를 `COMPLETE`라고 부르지 않고 실제 완료 단계와 blocker를 기록.

## 8. 통합 실행기 구현 현황과 남은 개선

| 우선순위 | 개선 대상 | 완료 조건 |
| --- | --- | --- |
| 1 | **구현: 단일 URL → post ID·버전** | 고정 호스트/카테고리 검증, 동일 URL 인식, 실패 시 BLOCKED |
| 2 | **구현: 근거 있는 링크 결정 CLI** | `--offline --topic-id --decision --reviewer --evidence`, 기존 판정 덮어쓰기 금지. 근거 자체는 반드시 별도 의미 검토 |
| 3 | **구현: URL별 비공개 상태 JSON** | OCR/검색/기존 링크·Master proposal·학습 bundle 상태와 다음 조치 구분 |
| 4 | **구현 일부: 변경 URL 증분 처리** | 본문 해시·수정 정보 기반 무변경 스킵, 미디어 hash 재검사는 `--refresh-assets` 선택. 과거 승인 보존 |
| 5 | **미구현: 자동 의미 판단·Fact 외부 검증·주기 실행** | 현재 승인·검증 경계를 보존하고 별도 개발·테스트 필요 |

선행 단계의 동작 증거가 없는데 새 아키텍처·대형 검색 엔진·자동 생성 Topic·채점 방식 개편으로 옮겨가지 않습니다. 반드시 현재 코드 기반의 최소 변경을 우선합니다.

## 9. 검증·감사 명령의 기준

관련 변경 유형별 focused regression:

```bash
python3 scripts/test_match_wordpress_posts_to_topic_packs.py
python3 scripts/test_wordpress_topic_pack_ocr.py
python3 scripts/test_wordpress_topic_link_review_application.py
python3 scripts/test_wordpress_review_integration.py
python3 -m pytest -q tests/test_wordpress_url_workflow.py
```

실제 코드·canonical 반영이 배포 대상이라면 기존 정책에 따른 **전체 오프라인 pytest**:

```bash
python3 -B scripts/release_candidate.py validate
```

DB 쓰기 없는 문서 변경만으로 위 테스트를 실행했다고 주장하지 않습니다. 결과 보고에는 **실제 실행 여부·통과·실패·건너뜀**을 명시합니다. 라이브 API/provider 검증은 별도 선택형이며, 운영 봇을 직접 재시작하거나 현재 `main`을 변경하지 않습니다.
