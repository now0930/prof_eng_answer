# prof_eng_answer

산업계측제어기술사 논술 답안을 Telegram으로 접수해 채점하고, 근거·오류 진단·보완 방향을 제공하는 시스템입니다. 기존 A/B/C/D/E 채점 계약을 유지하면서 결정론적 채점, Topic Pack, 학습 이력 및 복습 기능을 운영합니다.

## 핵심 기능

- `/grade` 답안 채점과 `/review <topic_id 또는 주제명>` 사용자가 고른 주제 복습
- A/B/C/D/E 총 25점 기준 채점, 요구사항·Fact·오류 근거 및 개선 피드백
- deterministic primary 채점과 Golden/release validation
- Topic Pack 기반 채점 자료와 Master → Grading, Training, Feedback View 구조
- 답안 이력, 진단, 다음 복습일 및 Review Queue 저장
- WordPress 글·첨부 출처를 Topic에 연결하는 source-reference 계약

학습 데이터베이스와 개인 운영 자료는 비공개로 관리합니다. 개인 데이터, 토큰, `.env`와 운영 DB를 Git에 추가하지 마세요.

## 전체 구조

```text
WordPress 원문·HTML·자사 PDF·자사 이미지/OCR
              │ source reference·버전·해시
              │ 변경 제안 → 검토 → 승인
              ▼
       MASTER TOPIC PACK (topic_id·revision·projection 계약)
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
 Grading   Training  Feedback/
   View      View    Diagnosis View
      │       │        │
 기존      /review   확정 점수와
 Grader    학습·복습  진단·보완 안내
      │       │        │
      └───────┼────────┘
              ▼
       Training History
              ▼
       Review Queue / 재작성
```

기존 grader, A/B/C/D/E scoring, canonical Question Type, topic routing authority, fatal handling 및 Golden/release gate가 판정의 기준입니다. 학습 계층은 adapter/projection 방식으로 연결되며 이를 대체하지 않습니다.

### View의 역할

| View | 역할 | 점수 영향 |
|---|---|---:|
| Grading View | 기존 Topic Pack과 Grader가 사용하는 호환 projection | 있음(기존 계약 내) |
| Training View | 문제·학습자료·WordPress 원문·OCR·검토 주석 제공 | 없음 |
| Feedback/Diagnosis View | 확정 채점 결과를 바탕으로 부족점·보완자료 제공 | 없음 |

`/review <topic_id 또는 주제명>`은 Training View를 소비합니다. Feedback View는 기존 `diagnosis-projection-v1` 계약을 유지하며 별도 채점 엔진이 아닙니다. 학습 이력과 Review Queue는 사용자 상태로 별도 저장하고 Master Topic Pack에 넣지 않습니다.

## 빠른 시작

Python 3.11 환경에서 저장소 루트에서 실행합니다.

```bash
cp .env.example .env
# .env에 필요한 Telegram/provider 설정 입력
python3 bot.py
```

Compose 예제를 사용하는 경우:

```bash
cp .env.example .env
cp docker-compose.example.yml docker-compose.yml
# .env 설정 후
docker compose up -d prof-eng-answer-bot
docker compose logs --tail=100 -f prof-eng-answer-bot
```

예제 Compose의 network·provider 설정은 환경에 맞게 확인하세요. 실제 운영 서버의 경로와 배포 절차는 로컬에 고정하지 말고 [`docs/operation_runbook.md`](docs/operation_runbook.md)를 따릅니다.

### Telegram 사용

`/grade`를 입력한 다음 문제와 답안을 보냅니다.

```text
/grade

문제:
문제 내용을 입력

답안:
작성한 답안
```

채점 결과와 session은 설정된 저장 경로에 기록됩니다. `/review <topic_id 또는 주제명>`으로 원하는 주제를 직접 지정합니다. 날짜에 따라 대상이 자동 변경되지 않습니다. 검색어가 여러 Topic과 일치하면 후보를 보여주며, 완료 후 `/review done <topic_id>`로 기록합니다.

## 채점·학습 데이터

- 채점 점수는 A/B/C/D/E 계약을 따릅니다. Question Type/coverage, checker, Fact/Topic 자료는 근거와 검증 제약이며 채점 계약을 임의로 바꾸지 않습니다.
- `present`, `partial`, `incorrect`, `missing`은 구분합니다. 검증된 오류를 누락으로 바꾸거나 같은 오류를 여러 항목에서 중복 감점하지 않습니다.
- Master Topic Pack은 채점·학습·진단 View의 공통 원천입니다. 실제 Topic 내용은 검토 가능한 source를 기준으로 관리합니다.
- 복습 이력은 question/topic, 시도 시각, 점수, 진단, 복습 상태와 다음 복습 시각을 보존합니다. Queue 선택 contract는 유지하지만 Telegram의 `/review`는 사용자가 요청한 Topic을 표시합니다.
- WordPress 자료는 원문 출처와 버전 정보를 연결합니다. 변경 내용을 Master에 자동 반영하지 않고 제안·승인 흐름을 사용합니다.
- Master source의 선택 필드 `training_scope`로 Training View에만 혼합/비대상 출처를 제외하거나 PDF 페이지 구간을 제한할 수 있습니다. Master 출처와 원본은 보존하고, 채점 및 Diagnosis 참조는 이 설정의 영향을 받지 않습니다.

기존 Master와 세 View의 연결 인터페이스는 구현되어 있습니다. 여러 WordPress 글을 종합하여 Topic별 학습 흐름을 구성하는 확장은 아래 계획에 따라 진행합니다. Topic 내용의 정확성은 별도 검토 대상입니다. WordPress 링크 후보는 확정 후보와 `deferred` 후보를 분리해 관리합니다. 확정 후보만 사람 승인 후 실제 Catalog/Master에 반영하고, 보류 후보는 거절로 간주하지 않습니다.

### Topic 단위 학습 구성 확장 — 진행 중

WordPress의 단편적인 글·HTML을 종합하여 하나의 Topic을 이해하는 논리적인
학습 흐름을 만듭니다. Master는 공통 지식의 ID·버전·출처와 학습 구성·채점
연결을 관리합니다. 본문은 별도 파일로 참조할 수 있습니다.

| 구성 | 책임 | 공유 방식 |
|---|---|---|
| 공통 지식 | 개념·수식·조건·예외·관계와 여러 출처 | 안정적인 `knowledge_id`로 참조 |
| 학습 구성 | 목표 → 선수지식 → 개념 → 유도 → 예제 → 적용 한계 → 자가 점검 | Training View가 순서와 설명을 제공 |
| 채점 연결 | 기존 requirement·Fact Anchor·Logic Check와 지식의 연결 | 기존 채점 권한을 유지하며 명시적으로 매핑 |
| 피드백 연결 | 미충족 요구사항에서 해당 개념·학습 절로 안내 | 확정 점수 이후 적용, 점수 영향 없음 |

지식과 출처는 공유하지만 학습 순서는 채점 순서가 아니며, 학습자료 전체가
모든 문제의 필수 평가 항목이 되지 않습니다. 원문, 종합 설명, 검토 주석을
구별하고 출처 연결·지식 검토·학습 검토·채점 승인 상태를 분리합니다.
원문 간 충돌은 보존하고 미해결 상태를 표시합니다.

현재 구현은 기존 채점 자료와 WordPress HTML을 조합하는 Training View입니다.
공통 지식층과 학습 경로, 채점 ID 매핑은 **이번 확장의 구현 대상**입니다.
기존 v1 계약에 제안된 필드를 바로 넣지 않고 호환 adapter와 버전 계약부터
검증합니다. 사용자별 이력·복습 선택은 별도 저장합니다.

전체 계획과 단계별 통과 기준은
[Topic 지식·학습 구성 작업 계획](docs/topic_learning_synthesis_plan.md)에 기록합니다.
현재 위치: **Stage 1~8 구현·로컬 검증 완료**. 운영 콘텐츠 승인·적용은 별도입니다.
후속 구현으로 작성 CLI에 `review-template`, `preview`, `apply`를 추가했습니다. 검토 기록·후보·출처·Master 해시를 확인한 최초 연결만 지원하며 실제 후보 적용은 아직 하지 않았습니다. 사용법은 [학습 초안 작성 절차](docs/topic_learning_authoring.md)를 참조하세요.
최초 연결 적용 기능 추가 후 전체 pytest 747 passed, 기존 non-promote release 스크립트와 Topic release gate가 통과했습니다. [검증 결과와 전달 상태](docs/topic_learning_synthesis_validation.md)를 참조하세요.
실제 WordPress 자료 2개를 6절의 비공개 학습 초안으로 종합하고 격리 환경에서 검증했습니다. 운영 Master에는 아직 연결하지 않았습니다.
Feedback은 확정 ledger의 미충족 요구사항을 검토된 매핑으로 학습 절에 연결합니다. Topic·출처 파일·요구사항 ID와 문장이 정확히 일치해야 하며, 과거 안내와 현재 자료의 버전이 다르면 재확인을 표시합니다.
연결된 학습 구성이 있으면 `/review`는 목표·절별 설명·조건·예외·자가 점검·출처를 순서대로 표시합니다. 초안·출처 불일치 절은 보류하고, 기존 자료만 있는 Topic은 기존 화면을 유지합니다.
여러 글의 출처 패킷 준비와 사람/LLM 작성 초안 검증은 [학습 초안 작성 절차](docs/topic_learning_authoring.md)를 따릅니다.
필드·검토 상태·버전 정책은 [공통 지식·학습 구성 계약](docs/topic_learning_synthesis_contract.md)에 정의합니다.

현재 WordPress Topic 링크 검토 기준:

- 확정 후보: 13건
- 후속 검토 보류: 166건
- DB/Master 자동 반영: 없음

검토용 결정 템플릿은 [`reports/wordpress_topic_link_manual_review_20261005_decision_template.csv`](reports/wordpress_topic_link_manual_review_20261005_decision_template.csv)이며, 결정 적용 절차는 [`docs/wordpress_topic_link_decision_application_workflow.md`](docs/wordpress_topic_link_decision_application_workflow.md)를 따릅니다.

상세 계약과 현재 구현 범위는 [`docs/learning_layer.md`](docs/learning_layer.md), Topic Pack authoring 및 approval 절차는 [`docs/topic_pack_workflow.md`](docs/topic_pack_workflow.md)를 확인하세요.

새 Topic Pack은 `rubric_manager.py add-topic`으로 draft를 만들고, 사람 검토 후 `approve-topic`으로 승인합니다. 생성 bank를 직접 편집하지 말고 상세 절차와 `validate-topic-pack-release --all` Gate를 따릅니다.

## 검증

### WordPress Source Pack·결정 계약 검증

| 계약 | 구현 | 상태 |
|---|---|---|
| WordPress Source Pack 읽기 전용 무결성·URL·first-party/OCR 검증 | `scripts/validate_wordpress_source_pack.py` | 완료 |
| Master → Grading/Training/Feedback projection | `study/master_topic_pack.py`, `study/topic_views.py` | 완료 |
| 사람 결정 CSV의 후보 키·Topic ID·근거 검증 | `scripts/validate_wordpress_decisions.py` | 완료 |
| 승인 전 dry-run | `validate_wordpress_decisions.py` 기본 실행 | 완료 |
| 실제 링크 적용 | 기존 `wordpress_catalog.py --review-topic-link` 단건 명령 | 명시적 승인 후 |
| WordPress 내용의 canonical 채점 기준 승격 | content proposal·Topic Pack 승인 workflow | 검토 후 적용 |
| WordPress Claim → canonical Fact/Logic/Model 매핑 | `schemas/wordpress_claim.schema.json`, `study/wordpress_claims.py` | 계약 구현 완료 |

읽기 전용 Source Pack 검증:

```bash
python3 scripts/validate_wordpress_source_pack.py \
  --database data/wordpress_sources.sqlite3 \
  --master-root master_topic_packs
```

사람이 입력한 결정표 검증:

```bash
python3 scripts/validate_wordpress_decisions.py \
  --source reports/wordpress_topic_link_manual_review_20261005_confirmed_only.csv \
  --decisions reports/wordpress_topic_link_manual_review_20261005_decision_template.csv
```

검증기는 DB나 Master를 변경하지 않는다. `final_decision`이 비어 있는 행은 보류로 표시되며, 실제 적용은 기존 단건 승인 명령으로만 수행한다.

### WordPress 내용 승격 작업 계획

내용은 다음 순서로만 채점 기준에 반영한다.

1. WordPress source의 URL·version·hash·locator 확인
2. `wordpress-claim-v1` Claim 작성
3. Claim의 `source_id`, excerpt, locator와 대상 `fact_anchor`·`logic_check`·`model_answer` 매핑 기록
4. `review_status=human_review_required` 상태에서 기술 사실·Topic 경계 검토
5. 기존 `content-update-proposal-v1`로 변경 제안 생성
6. 사람 승인·candidate hash 검증
7. canonical Topic Pack 반영 후 generated bank·Golden·release regression

Claim은 승인 전까지 항상 `score_effect=none`이며, WordPress OCR 원문을 직접 Grader 입력으로 사용하지 않는다.

문서만 변경한 경우:

```bash
git diff --check
```

Topic Pack source 또는 generated bank를 변경한 경우:

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release --all
python3 scripts/rubric_manager.py validate-all
```

전체 release 검증은 환경 및 시간 요구사항을 확인한 뒤 다음을 실행합니다.

```bash
PROMOTE_GENERATED=0 scripts/validate_release.sh
```

CI는 `main` push와 pull request에서 release validation을 실행하고, generated 파일을 임의로 변경하지 않았는지 확인합니다. 변경 유형별 필수 회귀·배포 검증은 [`docs/grading_quality_roadmap.md`](docs/grading_quality_roadmap.md)와 [`docs/operation_runbook.md`](docs/operation_runbook.md)에 따릅니다.

## 주요 경로

| 경로 | 용도 |
|---|---|
| `bot.py` | Telegram 명령, 세션 입력/저장 및 출력 |
| `grading_agents.py` 및 grading 모듈 | 채점 orchestration, deterministic 판정·점수·결과 구성 |
| `master_topic_packs/` | Master Topic 데이터와 projection 계약 |
| `rubrics/topic_packs/` | 채점에 사용하는 Topic Pack source |
| `rubrics/generated/` | Topic Pack에서 생성하는 runtime bank; 직접 편집 금지 |
| `study/` | Training, Diagnosis, History, Review Queue 인터페이스 |
| `data/` | 로컬 캐시·비공개 실행 자료; 내용을 확인하고 민감 데이터는 커밋하지 않음 |
| `tests/`, `scripts/test_*.py` | 회귀 및 구조 검증 |
| `scripts/rubric_manager.py` | Topic Pack 및 Rubric 관리·검증 CLI |
| `scripts/validate_release.sh` | release 통합 검증 entrypoint |
| `docs/` | 설계·운영·검토 절차의 상세 문서 |

## 문서 안내

- [문서 인덱스와 source of truth](docs/README.md)
- [운영 runbook](docs/operation_runbook.md) · [Compose 구조](docs/docker_compose_usage.md)
- [채점 아키텍처](docs/grading_architecture.md) · [Question Type taxonomy](docs/question_type_taxonomy.md)
- [Master Topic Pack 및 학습 계층](docs/learning_layer.md)
- [WordPress Source Pack과 Grading·Review·Feedback 계약](docs/wordpress_topic_pack_view_contract.md)
- [Topic Pack workflow](docs/topic_pack_workflow.md) · [Topic Pack architecture](docs/topic_pack_architecture.md)
- [채점 품질 roadmap과 release 기준](docs/grading_quality_roadmap.md)
- [Python 코드 배치 규칙](docs/python_layout.md)

## 유지 원칙

학습 종합 콘텐츠는 근거·조건·단위 확인 후 `llm_verified`로 LLM 승인할 수 있습니다.
불확실한 항목은 `human_review_required`로 보존하고 해당 절 및 의존 절의 노출을
차단합니다. LLM 승인과 사람 승인은 구분하며, 채점 기준·fatal·배점 및 채점용
Topic Pack 승인 절차에는 적용하지 않습니다. [승인 계약](docs/topic_learning_authoring.md#6-llm-승인과-사람-검토-분리)을 참고하세요.

기존 학습 문서는 새 run에서 revision을 올려 재검토할 수 있습니다. 이전 문서와
승인 이력은 보존합니다. 기존 평가 매핑도 ID와 변경 내역을 보존하며 개정할 수
있고, 매핑의 재활성화·사용 중단에는 별도 사람 검토가 필요합니다.
현재 실제 Topic 내용 검토·확대는 보류하고 구조 검증을 진행합니다.

새 진단→학습 매핑은 `prepare --include-mapping-targets`로 현재 Topic의 정식
요구사항 목록을 고정한 후 `add-mapping`으로 초안을 작성합니다. 출처 없는 ID를
추측하지 않으며, 매핑 활성화는 별도 사람 검토를 거칩니다.

1. 최상위 README에는 현재 사용자 관점의 개요와 진입 경로만 둡니다. 단계별 작업일지와 상세 정책은 `docs/` 또는 검증 report에 둡니다.
2. A/B/C/D/E, deterministic primary, 기존 Golden tests와 release gates를 임의 변경하지 않습니다.
3. Topic Pack은 `docs/topic_pack_workflow.md`의 승인·해시·검증 흐름을 따릅니다. Generated bank를 직접 수정하지 않습니다.
4. WordPress 원문과 source reference를 보존하고, Master 변경은 제안·검토·승인 후 수행합니다.
5. 개인 답안, 세션, 비공개 학습 DB, 인증정보를 공개 저장소에 올리지 않습니다.
6. 불필요한 자료는 참조처와 복구 가능성을 확인하기 전 삭제하지 않습니다.
