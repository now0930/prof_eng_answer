# prof_eng_answer

`prof_eng_answer`는 산업계측제어기술사 **2~4교시 논술형 답안**을 Telegram으로 입력받아, 25점 문항 기준으로 채점하고 핵심 오류와 보완 방향을 제시하는 답안 평가 시스템입니다.

단순 키워드 포함 여부가 아니라 문제 요구 해석, Fact 정확성, 현장 적용 판단, 논리 연결성, 문제 유형별 요구 충족도와 핵심 이론 오류를 함께 평가합니다.

> 이 README는 프로젝트 소개, 빠른 실행, 핵심 정책과 검증 방법을 안내합니다. 세부 설계와 운영 기준은 [`docs/README.md`](docs/README.md)에서 찾을 수 있습니다.

---

## 1. 주요 기능

- Telegram `/grade` 명령 기반 답안 채점
- Gemini semantic grader와 CLOVA fallback
- Ollama 기반 보조 분석
- A/B/C/D/E 25점 계층형 채점
- 교수·기술사·기업 임원 관점의 3인 채점자 가중 합성
- Question Type v2 기반 문제 유형별 평가 lens
- Fact Anchor 기반 핵심 사실 평가
- Model Answer Bank 기반 답안 구조 참조
- Logic Check 기반 핵심 이론 오류 검증
- Difficulty Strategy와 score ceiling 평가
- 문제문에 명시된 핵심 요구의 실제 누락 hard cap
- Topic Pack 기반 Rubric source 관리와 generated bank 생성
- Telegram 결과 요약과 세션별 평가 결과 저장
- release validation과 Rubric Audit

---

## 2. 채점 구조

총점은 25점입니다.

| Layer | 이름 | 배점 | 평가 초점 |
|---|---|---:|---|
| A | 문제 진입·답안 구조 | 3 | 배경과 핵심 쟁점을 간결하게 제시하고 전개 구조가 명확한가 |
| B | 문제 요구 해석·완전성 | 6 | 요구동사와 세부 요구를 정확히 해석하고 직접 답했는가 |
| C | 유형별 Fact 기반 내용 설명 | 8 | 핵심 개념, 원리, 수식과 비교축을 정확히 설명하는가 |
| D | 현장 적용·설계 판단·제언 | 6 | 비용, 실현 가능성, 기존 설비 영향과 검증 방법을 고려하는가 |
| E | 연결성·면접 방어 가능성 | 2 | 배경, 요구, Fact와 판단이 논리적으로 연결되는가 |
| **합계** |  | **25** |  |

기준 점수:

| 기준 | 점수 |
|---|---:|
| 공식 합격선 | 15 / 25 |
| 실전 목표선 | 17.5 / 25 |
| 고득점 기준 | 20 / 25 |

Question Type, Fact Anchor, Model Answer, Logic Check와 Difficulty Strategy는 A/B/C/D/E 점수 체계를 대체하지 않고 평가 근거와 최종 정합성을 보완합니다.

---

## 3. 2026-07 반영 정책

### 3.1 `incorrect`와 `missing` 분리

명시적 요구와 Question Type 세부 기준은 다음 네 상태로 구분합니다.

| 상태 | 의미 | 처리 |
|---|---|---|
| `present` | 정확하고 충분하게 답함 | 정상 인정 |
| `partial` | 직접 답했지만 설명이 부족함 | 부분 인정 |
| `incorrect` | 직접 답했지만 핵심 사실이 틀림 | Fact·Logic 평가에서 제한 |
| `missing` | 요구에 실질적으로 답하지 않음 | 조건 충족 시 누락 hard cap 대상 |

`incorrect`는 오답이고 `missing`은 미응답입니다. 직접 답했지만 틀린 내용은 누락 hard cap을 발생시키지 않습니다.

Telegram 출력에서도 오답과 누락을 분리합니다.

```text
- 상태: 충족 0 · 부분 0 · 오답 5 · 누락 2
- 오답 응답: principle_mechanism, result_meaning ...
- 누락: background_need, formula_model_variables
- 명시적 핵심 요구 오답 응답: 감쇠비에 따른 과도응답 특성 설명
```

### 3.2 명시적 요구사항 hard cap

hard cap은 다음 조건을 모두 만족하는 **실제 핵심 요구 누락**에만 적용합니다.

- semantic grader가 생성한 coverage
- 요구사항 source가 `question_text`
- 추출 신뢰도가 `high`
- 문제문에서 직접 요구한 핵심 항목
- 상태가 `missing`

`partial`과 `incorrect`는 hard cap 대상이 아닙니다.

| 실제 누락 상태 | B항목 상한 | 총점 상한 |
|---|---:|---:|
| 핵심 요구 1개 누락 | 3.5 / 6 | 17.0 / 25 |
| 핵심 요구 2개 이상 누락 | 2.0 / 6 | 14.0 / 25 |
| 핵심 요구 전체 누락 | 1.5 / 6 | 12.5 / 25 |

### 3.3 Question Type coverage 보정

`QUESTION_TYPE_COVERAGE_SCORE_MODE`는 다음과 같이 동작합니다.

| 모드 | 동작 |
|---|---|
| `warn` | 보정 후보만 기록하고 표시하며 점수는 변경하지 않음 |
| `strict` | 유효한 보정 후보가 현재 점수보다 낮을 때 실제 점수에 반영 |
| `off` | coverage 점수 보정 비활성 |

기본값은 `warn`입니다. coverage 보정은 최대 `0.75 / 25`의 약한 보조 정책이며, 명시적 요구사항 hard cap이 발동한 경우 중복 적용하지 않습니다.

### 3.4 Logic fatal과 numeric cap 분리

Logic Check의 `fatal`은 **핵심 이론 오류 판정**입니다. fatal이 검출됐다는 이유만으로 numeric cap이 실제 적용된 것은 아닙니다.

`DIFFICULTY_CEILING_MODE=strict`에서도 권장 cap이 현재 점수보다 낮아 실제 점수를 제한할 때만 `cap_applied=true`가 됩니다.

```text
판정: THEORY_CORE 핵심 이론 오류

총평: 핵심 이론 오류가 확인되었습니다.
현재 점수가 권장 ceiling보다 낮아 추가적인 수치 cap은 적용되지 않았습니다.
```

실제로 점수를 제한한 경우에만 다음 표현을 사용합니다.

```text
예상 점수대: 10점 cap 적용
판정: THEORY_CORE 핵심 이론 오류 cap 적용
```

### 3.5 최종 Question Type 정합성

semantic grader가 최종 선택한 Question Type은 grade root와 Telegram 출력에 동일하게 반영합니다.

```text
question_type=PRINCIPLE_INTERPRETATION
question_type_name=원리·해석형
```

Model Answer의 `question_type`은 참고 답안의 메타데이터이며 최종 semantic Question Type을 덮어쓰지 않습니다.

---

## 4. 빠른 실행

### 4.1 운영 중인 Hermes Compose

운영 Compose 기준 service는 `prof-eng-answer-bot`, container는 `prof_eng_answer_bot`입니다.

```bash
cd ~/hermes

docker compose up -d prof-eng-answer-bot
docker logs --tail=100 -f prof_eng_answer_bot
```

재시작:

```bash
cd ~/hermes

docker compose restart prof-eng-answer-bot
docker logs --tail=100 -f prof_eng_answer_bot
```

상태 확인:

```bash
docker compose ps
docker inspect -f '{{.State.Running}}' prof_eng_answer_bot
```

### 4.2 저장소의 standalone 예제

```bash
cd ~/hermes/workspace/prof_eng_answer

cp .env.example .env
cp docker-compose.example.yml docker-compose.yml

vim .env
docker compose up -d prof-eng-answer-bot
docker logs --tail=100 -f prof_eng_answer_bot
```

예제 Compose는 외부 Docker network `ai_net`을 사용합니다. network가 없다면 한 번만 생성합니다.

```bash
docker network create ai_net
```

상세 운영 절차는 [`docs/operation_runbook.md`](docs/operation_runbook.md), Compose 구조는 [`docs/docker_compose_usage.md`](docs/docker_compose_usage.md)를 참조합니다.

---

## 5. 환경변수

기본 provider 설정은 `.env.example`을 복사해 사용합니다.

```dotenv
# Telegram
TELEGRAM_BOT_TOKEN=

# Gemini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.1-flash-lite

# Ollama
OLLAMA_URL=http://ollama:11434
OLLAMA_MODEL=

# Provider routing
LLM_PROVIDER=auto
LLM_PRIMARY=gemini
LLM_FALLBACK=clova

# CLOVA
CLOVA_API_KEY=
CLOVA_REQUEST_ID=prof-eng-answer-local
CLOVA_MODEL=HCX-003
CLOVA_HOST=https://clovastudio.stream.ntruss.com
CLOVA_ENDPOINT=/v1/chat-completions/HCX-003
```

선택 가능한 runtime 정책:

```dotenv
# Rubric bank
RUBRIC_BANK_MODE=generated

# Question Type coverage: warn | strict | off
QUESTION_TYPE_COVERAGE_SCORE_MODE=warn

# Difficulty ceiling: warn | strict
DIFFICULTY_CEILING_MODE=warn
```

Provider 선택:

| 값 | 의미 |
|---|---|
| `LLM_PROVIDER=auto` | Gemini primary, CLOVA fallback |
| `LLM_PROVIDER=gemini` | Gemini만 사용 |
| `LLM_PROVIDER=clova` | CLOVA만 사용 |

세부 provider 설정은 [`docs/llm_provider.md`](docs/llm_provider.md)를 참조합니다.

---

## 6. Telegram 사용

Bot에서 `/grade`를 입력한 뒤 문제와 답안을 전송합니다.

```text
/grade
2차 시스템의 감쇠비(ζ)에 따른 과도응답 특성을 설명하시오.

1. 개요
...

2. 감쇠비별 응답 특성
...

3. 현장 적용 시 고려사항
...

끝.
```

결과에는 다음 항목이 포함될 수 있습니다.

- 최종 점수와 예상 점수대
- 합격선·실전 목표선·고득점 기준 달성 여부
- 핵심 판정 근거와 항목별 근거
- Logic Check 결과
- Question Type 요구사항 충족도
- 명시적 요구의 오답·누락 구분
- 보완 방향
- 저장된 session 경로

세션 결과는 다음 위치에 저장됩니다.

```text
data/sessions/<session_id>/
```

`grade.json`, 입력 원문과 단계별 평가 snapshot 등이 저장될 수 있습니다.

---

## 7. 처리 흐름

```text
Telegram /grade
  → bot.py
  → grading_agents.py
  → LLM provider routing
  → semantic grading
  → A/B/C/D/E layer scoring
  → 3인 rater weighted scoring
  → Fact Anchor / Model Answer
  → Question Type classification and coverage
  → explicit requirement evaluation
  → Logic Check
  → Difficulty Strategy and ceiling
  → final score reconciliation
  → Telegram output formatter
  → data/sessions/<session_id>/ 저장
```

세부 설계는 [`docs/grading_architecture.md`](docs/grading_architecture.md)를 참조합니다.

---

## 8. Rubric Bank와 Topic Pack

Rubric은 legacy bank와 Topic Pack 기반 generated bank를 지원합니다.

| 구분 | 위치 | 역할 |
|---|---|---|
| Legacy Rubric Bank | `rubrics/*/*.json` | 기존 통합 Rubric |
| Topic Pack Source | `rubrics/topic_packs/<topic_id>/` | 사람이 관리하는 source of truth |
| Generated Rubric Bank | `rubrics/generated/*.generated.json` | Topic Pack source를 합친 runtime output |

새 topic의 기본 흐름:

```text
Topic Pack README
  → Topic Sheet 후보
  → 사람 검토
  → source JSON candidate
  → generated bank
  → smoke 및 Telegram 재채점
```

작성 기준은 [`docs/rubric_authoring_guide.md`](docs/rubric_authoring_guide.md), 실행 절차는 [`docs/topic_pack_workflow.md`](docs/topic_pack_workflow.md)를 참조합니다.

---

## 9. 검증

### 9.1 전체 release validation

generated bank를 변경하지 않고 검증:

```bash
cd ~/hermes/workspace/prof_eng_answer

PROMOTE_GENERATED=0 \
RUN_SMOKE_TOPIC_PACKS=0 \
bash scripts/validate_release.sh
```

generated bank를 실제 파일에 반영해야 할 때만 promote를 활성화합니다.

```bash
PROMOTE_GENERATED=1 \
RUN_SMOKE_TOPIC_PACKS=0 \
bash scripts/validate_release.sh
```

### 9.2 Release test coverage

```bash
python3 scripts/validate_release_test_coverage.py
```

정상 marker:

```text
ALL RELEASE TEST MODULES COVERED
```

### 9.3 Rubric Audit

```bash
python3 scripts/rubric_audit/run_rubric_audit.py
```

### 9.4 핵심 회귀 테스트

```bash
python3 scripts/test_explicit_requirement_cap.py
python3 scripts/test_requirement_coverage.py
python3 scripts/test_score_flow_guards.py
python3 scripts/test_grade_output_formatter.py
```

주요 검증 대상:

- `incorrect`와 `missing` 분리
- 실제 누락에만 hard cap 적용
- coverage `warn` 모드의 점수 보존
- coverage `strict` 모드의 제한적 점수 반영
- Logic fatal과 실제 numeric cap의 출력 분리
- 최종 score range와 pass flag 정합성
- Question Type과 한국어 이름 동기화

### 9.5 문서만 수정했을 때

```bash
git diff --check
git diff --stat
git status --short --branch
```

LLM prompt, provider integration, container mount·dependency 또는 배포 runtime을 변경한 경우 host 검증과 함께 container 검증을 수행합니다.

---

## 10. 문서

문서 인덱스와 책임 범위는 [`docs/README.md`](docs/README.md)에서 관리합니다.

| 목적 | 문서 |
|---|---|
| 운영, 재시작, 장애 대응 | [`docs/operation_runbook.md`](docs/operation_runbook.md) |
| Docker Compose | [`docs/docker_compose_usage.md`](docs/docker_compose_usage.md) |
| 채점 구조와 score flow | [`docs/grading_architecture.md`](docs/grading_architecture.md) |
| Question Type | [`docs/question_type_taxonomy.md`](docs/question_type_taxonomy.md) |
| 난이도와 ceiling | [`docs/difficulty_and_selection_strategy.md`](docs/difficulty_and_selection_strategy.md) |
| LLM provider | [`docs/llm_provider.md`](docs/llm_provider.md) |
| Rubric 작성 | [`docs/rubric_authoring_guide.md`](docs/rubric_authoring_guide.md) |
| Topic Pack workflow | [`docs/topic_pack_workflow.md`](docs/topic_pack_workflow.md) |
| Logic Check 운영 | [`docs/logic_check_profiles_readme.md`](docs/logic_check_profiles_readme.md) |

---

## 11. 주요 파일

| 파일 | 역할 |
|---|---|
| `bot.py` | Telegram 입력 처리와 결과 출력 |
| `grading_agents.py` | semantic grading orchestration |
| `question_type_coverage_adapter.py` | coverage 정규화와 상태 집계 |
| `explicit_requirement_cap.py` | 명시적 핵심 요구의 실제 누락 hard cap |
| `question_type_coverage_score_adjuster.py` | coverage 보정 후보 계산과 strict 적용 |
| `logic_check_evaluator.py` | 핵심 이론 오류 평가 병합 |
| `difficulty_score_ceiling.py` | difficulty ceiling 평가와 strict 적용 |
| `grade_score_reconciler.py` | 최종 점수·cap·score range 정합성 |
| `grade_output_summarizer.py` | Telegram 요약과 deterministic fallback |
| `scripts/rubric_manager.py` | Rubric과 Topic Pack 관리 |
| `scripts/validate_release.sh` | release 전 통합 검증 |

---

## 12. 유지 원칙

1. 루트 README에는 프로젝트 소개, 실행, 핵심 정책과 기본 검증만 유지합니다.
2. 세부 설계, 운영 절차와 authoring 규칙은 `docs/`에서 관리합니다.
3. 과거 migration log와 긴 검증 로그를 README에 누적하지 않습니다.
4. `incorrect`와 `missing`을 같은 누락 상태로 설명하지 않습니다.
5. `warn`을 실제 점수 변경으로 설명하지 않습니다.
6. Logic fatal, recommended cap과 actually applied cap을 구분합니다.
7. 문서와 runtime이 충돌하면 현재 코드, Rubric source와 검증 결과를 확인합니다.
