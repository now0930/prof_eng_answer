# Prof Eng Answer

`prof_eng_answer`는 산업계측제어기술사 답안을 Telegram으로 입력받아, 기술사 시험 관점에서 채점하고 보완 방향을 제시하는 채점 Bot입니다.

이 프로젝트의 핵심 목적은 단순 키워드 매칭이 아니라 다음을 함께 평가하는 것입니다.

- 문제 의도 파악
- Fact 기반 기술 설명 수준
- 현장 적용성
- 설계·운영 판단
- 답안 구조와 면접 방어 가능성
- 모범답안 Bank와 Fact Anchor 기준 충족 여부
- 문제 유형별 요구사항 충족 여부
- 문항 난이도와 선택 전략

기본 채점 구조는 A/B/C/D/E 25점 체계입니다.

| 항목 | 배점 | 의미 |
|---|---:|---|
| A | 4 | 배경과 문제 진입 |
| B | 5 | 문제 요구 파악 |
| C | 8 | 유형별 Fact 기반 내용 설명 |
| D | 6 | 현장 적용, 설계 판단, 제언 |
| E | 2 | 연결성, 면접 방어 가능성 |

---

## 1. 빠른 실행

운영 환경에서는 상위 `~/hermes/docker-compose.yml`에서 실행합니다.

```bash
cd ~/hermes
docker compose up -d
docker compose ps
```

정상 상태 예시:

```text
hermes_agent Up
prof_eng_answer_bot Up
```

로그 확인:

```bash
tail -n 120 ~/hermes/workspace/prof_eng_answer/logs/prof_eng_answer.log
```

Bot만 재시작:

```bash
cd ~/hermes
docker compose restart prof-eng-answer-bot
```

중복 polling을 막기 위해 `hermes_agent` 안에서 수동으로 `nohup python bot.py`를 실행하지 않습니다.

---

## 2. 주요 파일

| 파일 | 역할 |
|---|---|
| `bot.py` | Telegram Bot 진입점 |
| `grading_agents.py` | 채점 pipeline |
| `gemini_grader.py` | Gemini semantic grader |
| `clova_grader.py` | CLOVA fallback grader |
| `model_answer_router.py` | 문제와 모범답안 topic 매칭 |
| `question_type_router.py` | question_type 분류 |
| `difficulty_strategy.py` | 문제 난이도와 선택 중요도 분류 |
| `difficulty_score_ceiling.py` | 난이도 기반 ceiling 후보 계산 |
| `rubrics/model_answers/industrial_instrumentation_control.json` | 모범답안 Bank |
| `rubrics/fact_anchors/industrial_instrumentation_control.json` | Fact Anchor Bank |
| `rubrics/question_types/default.json` | question_type 정의 |
| `scripts/import_review_design.py` | review design markdown을 bank JSON으로 반영 |
| `scripts/rubric_manager.py` | rubric 관련 명령 실행 |
| `scripts/validate_model_answer_bank.py` | 모범답안 Bank 단독 검증 |
| `scripts/validate_fact_anchor_bank.py` | Fact Anchor Bank 단독 검증 |
| `scripts/validate_model_fact_consistency.py` | 모범답안 Bank와 Fact Anchor Bank 간 정합성 검증 |

---

## 3. 채점 Pipeline

현재 주요 순서는 다음과 같습니다.

```text
1. Telegram /grade 입력
2. 문제와 답안 파싱
3. LLM provider 선택
4. Gemini 또는 CLOVA semantic grader 실행
5. Python rule 기반 A/B/C/D/E 점수 후처리
6. 3인 채점자 layer 평가 반영
7. Fact Anchor Bank 참조
8. Model Answer Bank 참조
9. Question Type v2 coverage 평가
10. Difficulty Profile과 ceiling 후보 계산
11. Telegram formatter 구성
12. send_message boundary cleanup
13. 최종 채점 결과 출력
```

중요한 순서:

```text
phase2 -> phase20 -> phase21
```

---

## 4. 환경변수

운영 환경변수는 상위 디렉터리의 `.env`에서 관리합니다.

```text
~/hermes/.env
```

| 변수 | 설명 |
|---|---|
| `TELEGRAM_BOT_TOKEN` 또는 `BOT_TOKEN` | Telegram Bot token |
| `OLLAMA_URL` | Ollama API URL |
| `OLLAMA_MODEL` | 로컬 분석 모델 |
| `GEMINI_API_KEY` | Gemini API key |
| `GEMINI_MODEL` | Gemini 채점 모델 |
| `LLM_PROVIDER` | `auto`, `gemini`, `clova` |
| `LLM_PRIMARY` | 기본 LLM provider |
| `LLM_FALLBACK` | fallback LLM provider |
| `CLOVA_API_KEY` | Naver CLOVA Studio API key |
| `CLOVA_MODEL` | CLOVA 모델명 |
| `DIFFICULTY_CEILING_MODE` | `warn`, `strict`, `off` |
| `QUESTION_TYPE_COVERAGE_SCORE_MODE` | `warn`, `strict`, `off` |

`.env`는 Git에 올리지 않습니다.

---

## 5. LLM Provider

Telegram에서 provider를 선택할 수 있습니다.

```text
/provider
/provider auto
/provider gemini
/provider clova
/provider reset
```

| 모드 | 의미 |
|---|---|
| `auto` | Gemini 우선, 실패 시 CLOVA fallback |
| `gemini` | Gemini만 사용 |
| `clova` | CLOVA만 사용 |

---

## 6. Question Type v2

2~4교시 답안 채점에서는 단답식 `DEFINE` 유형을 사용하지 않습니다. 대신 C항목 Fact 설명과 D항목 현장 판단을 보강하기 위해 4개 question_type lens를 사용합니다.

| question_type | 의미 |
|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·동작·계산·설계·수식 해석형 |
| `DIAGNOSIS_ACTION` | 문제·원인·영향·대책·개선 실행형 |
| `COMPARE_SELECTION` | 비교·분류·선정 판단형 |
| `IMPLEMENTATION_EVALUATION` | 적용·절차·방법·평가형 |

coverage 결과는 기본적으로 `warn` 모드에서 보정 후보만 표시합니다.

```env
QUESTION_TYPE_COVERAGE_SCORE_MODE=warn
```

실제 약한 보정을 적용하려면 다음을 사용합니다.

```env
QUESTION_TYPE_COVERAGE_SCORE_MODE=strict
```

자세한 내용은 `docs/question_type_taxonomy.md`를 참고합니다.

---

## 7. 모범답안 Bank

모범답안 Bank는 정답 문장 매칭용이 아닙니다. 답안 전개 구조, 고득점 요소, 저득점 패턴, 현장 적용 포인트를 제공하여 semantic grader와 Python rule 판단을 보강합니다.

본체 파일:

```text
rubrics/model_answers/industrial_instrumentation_control.json
```

대표 필드:

| 필드 | 의미 |
|---|---|
| `id` | 모범답안 고유 ID |
| `topic_id` | 주제 식별자. Fact Anchor Bank와 연결되는 핵심 key |
| `question_type` | 4개 Question Type v2 중 하나 |
| `title` | 사람이 읽는 제목 |
| `topic_aliases` | 검색·라우팅용 alias |
| `question_examples` | 출제 가능 문장 |
| `expected_structure` | 답안 전개 순서 |
| `model_answer_outline` | 모범답안 흐름 |
| `high_score_features` | 고득점 요소 |
| `low_score_patterns` | 저득점 패턴 |
| `field_connection_points` | 현장 적용 포인트 |
| `revision_notes` | 작성 의도와 수정 이력 |

### 7.1 모범답안 추가

새 topic을 추가할 때는 원칙적으로 모범답안 Bank와 Fact Anchor Bank를 함께 추가합니다.

1. topic_id를 먼저 정합니다.
2. `rubrics/model_answers/industrial_instrumentation_control.json`의 `answers`에 새 객체를 추가합니다.
3. 같은 `topic_id`를 `rubrics/fact_anchors/industrial_instrumentation_control.json`의 `topics`에도 추가합니다.
4. 검증을 실행합니다.

권장 명명 규칙:

```text
id = <topic_id>_<question_type>_v1
```

예:

```text
second_order_system_resonance_frequency_response_PRINCIPLE_INTERPRETATION_v1
```

단, 과거 legacy 항목은 `legacy_question_type`이 남아 있을 수 있으므로 기존 ID를 무리하게 바꾸지 않습니다.

검증:

```bash
python3 scripts/validate_model_answer_bank.py
python3 scripts/validate_fact_anchor_bank.py
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
git diff --check
```

### 7.2 모범답안 수정

수정할 때는 같은 `id`와 `topic_id`를 유지합니다.

수정 대상:

- `title`
- `topic_aliases`
- `question_examples`
- `expected_structure`
- `model_answer_outline`
- `high_score_features`
- `low_score_patterns`
- `field_connection_points`
- `revision_notes`

수정 후 반드시 다음을 확인합니다.

```bash
python3 scripts/validate_model_answer_bank.py
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
```

### 7.3 모범답안 삭제

모범답안을 삭제할 때는 topic 단위 영향도를 먼저 확인합니다.

삭제 기준:

| 상황 | 처리 |
|---|---|
| 같은 `topic_id`의 다른 모범답안이 남아 있음 | 해당 model answer만 삭제 가능 |
| 같은 `topic_id`의 모범답안이 모두 삭제됨 | Fact Anchor topic도 삭제할지 검토 |
| Fact Anchor만 남고 model answer가 없음 | 정합성 오류 또는 보류 topic으로 간주 |

삭제 후 확인:

```bash
python3 scripts/validate_model_fact_consistency.py
```

---

## 8. Fact Anchor Bank

Fact Anchor Bank는 topic별 핵심 사실 기준입니다. 모범답안의 문장 흐름과 달리, Fact Anchor는 채점 시 반드시 확인해야 하는 기술 fact의 최소 기준을 정의합니다.

본체 파일:

```text
rubrics/fact_anchors/industrial_instrumentation_control.json
```

대표 필드:

| 필드 | 의미 |
|---|---|
| `topic_id` | 주제 식별자. Model Answer Bank와 연결되는 핵심 key |
| `name` | 사람이 읽는 topic 이름 |
| `triggers` | 문제 매칭용 핵심 검색어 |
| `aliases` | topic 유사 표현 |
| `anchors` | 사실 기준 목록 |
| `anchors[].id` | anchor ID. 보통 `F1`, `F2` 형식 |
| `anchors[].name` | anchor 이름 |
| `anchors[].expected` | 반드시 설명되어야 할 사실 기준 |
| `anchors[].core_terms` | 핵심 용어 |
| `anchors[].support_terms` | 보조 용어 |

### 8.1 Fact Anchor 추가

새 topic을 만들 때는 `topics`에 새 객체를 추가합니다.

기본 원칙:

- `topic_id`는 model answer의 `topic_id`와 동일해야 합니다.
- `anchors`는 보통 4~5개로 구성합니다.
- 각 anchor는 하나의 fact 판단 기준만 담습니다.
- `expected`는 채점자가 의미 판단할 수 있을 정도로 문장형으로 작성합니다.

추가 후 검증:

```bash
python3 scripts/validate_fact_anchor_bank.py
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
```

### 8.2 Fact Anchor 수정

수정할 수 있는 항목:

- `name`
- `triggers`
- `aliases`
- `anchors[].name`
- `anchors[].expected`
- `anchors[].core_terms`
- `anchors[].support_terms`

수정 시 주의사항:

- `topic_id`는 기존 model answer와 연결되므로 함부로 바꾸지 않습니다.
- anchor의 `expected`는 단순 키워드가 아니라 채점 가능한 사실 문장이어야 합니다.
- `core_terms`는 너무 넓게 넣지 말고 해당 anchor를 식별할 수 있는 핵심어 중심으로 둡니다.

### 8.3 Fact Anchor 삭제

Fact Anchor topic을 삭제할 때는 같은 `topic_id`의 model answer가 남아 있는지 먼저 확인합니다.

| 상황 | 처리 |
|---|---|
| model answer가 남아 있음 | Fact Anchor 삭제 금지 |
| model answer가 모두 삭제됨 | Fact Anchor 삭제 가능 |
| 임시로 제외하고 싶음 | 삭제보다 `revision_notes` 또는 별도 review queue에서 관리 권장 |

삭제 후 검증:

```bash
python3 scripts/validate_model_fact_consistency.py
```

---

## 9. Model Answer Bank와 Fact Anchor Bank의 관계

두 파일은 `topic_id`를 기준으로 연결됩니다.

```text
model_answers.answers[].topic_id
        ==
fact_anchors.topics[].topic_id
```

핵심 관계는 다음과 같습니다.

| 관계 | 설명 |
|---|---|
| 1개 Fact Anchor topic | 하나의 기술 주제에 대한 사실 기준 |
| 1개 이상 Model Answer | 같은 topic을 여러 question_type 답안 구조로 설명 가능 |
| `topic_id` | 두 파일 사이의 primary key 역할 |
| `question_type` | Model Answer에만 존재. Fact Anchor에는 두지 않음 |
| `topic_aliases` | Model Answer routing 보조 |
| `triggers`, `aliases` | Fact Anchor matching 보조 |

예를 들어 `cv_valve_flow_coefficient`는 하나의 Fact Anchor topic을 가지면서, 정의형·계산설계형 등 여러 Model Answer를 가질 수 있습니다. 이때 모든 Model Answer는 같은 `topic_id`를 공유하고, 같은 Fact Anchor 기준을 참조합니다.

정합성 원칙:

1. 모든 model answer의 `topic_id`는 Fact Anchor Bank에 존재해야 합니다.
2. 모든 Fact Anchor topic은 최소 1개 이상의 model answer와 연결되는 것이 원칙입니다.
3. 한 topic에 여러 model answer가 있어도 됩니다. 단, `question_type`별 의도가 구분되어야 합니다.
4. Fact Anchor는 기술 fact 기준이고, Model Answer는 답안 구조 기준입니다.
5. 두 파일의 alias가 완전히 같을 필요는 없지만, 같은 topic을 가리켜야 합니다.
6. 새 topic 추가는 두 파일을 함께 추가합니다.
7. 기존 topic에 question_type만 추가할 때는 model answer만 추가할 수 있습니다. 이 경우 기존 Fact Anchor topic이 반드시 있어야 합니다.
8. topic 삭제는 model answer를 먼저 삭제하고, 연결된 model answer가 없을 때 Fact Anchor topic을 삭제합니다.

---

## 10. review design importer 사용

`review_design.md`는 고정 파일명이 아니라 review 결과 markdown의 일반 이름입니다. 실제 파일은 보통 다음 경로에 있습니다.

```text
wordpress_docs/review_designs/batch_011_design_4topics.md
wordpress_docs/review_designs/batch_012_design_2topics.md
wordpress_docs/review_designs/batch_013_design_4topics.md
wordpress_docs/review_designs/batch_014_design_1topic.md
```

목록 확인:

```bash
find wordpress_docs/review_designs -type f -name '*design*.md' | sort
```

import 실행:

```bash
python3 scripts/import_review_design.py wordpress_docs/review_designs/batch_014_design_1topic.md
```

주의사항:

- importer는 review design markdown을 JSON 형식으로 반영하는 도구입니다.
- importer가 기술적 사실 정확성을 보장하지는 않습니다.
- import 후 반드시 validate와 diff 확인을 수행합니다.
- importer 안에 topic별 `META`를 누적하지 않습니다. 한글 인코딩 깨짐을 막기 위해 metadata는 markdown과 JSON bank에 둡니다.

---

## 11. 검증 명령

Python 문법 확인:

```bash
python3 -m py_compile \
  bot.py \
  grading_agents.py \
  difficulty_strategy.py \
  difficulty_output_adapter.py \
  difficulty_score_ceiling.py \
  scripts/import_review_design.py \
  scripts/validate_model_fact_consistency.py
```

Rubric 단독 검증:

```bash
python3 scripts/validate_model_answer_bank.py
python3 scripts/validate_fact_anchor_bank.py
python3 scripts/validate_question_type_profile.py
```

Model Answer와 Fact Anchor 간 정합성 검증:

```bash
python3 scripts/validate_model_fact_consistency.py
```

전체 검증:

```bash
python3 scripts/rubric_manager.py validate-all
```

commit 전 확인:

```bash
git diff --check
git status --short
```

---

## 12. `validate_model_fact_consistency.py`가 검증하는 것

`scripts/validate_model_fact_consistency.py`는 두 JSON 파일의 형식적 정합성을 확인합니다.

검증 항목:

- JSON 파싱 가능 여부
- model answer `id` 중복 여부
- model answer `topic_id` 누락 여부
- model answer `question_type` 허용값 여부
- fact topic `topic_id` 중복 여부
- fact anchor `anchors` 존재 여부
- anchor `id`, `name`, `expected`, `core_terms` 기본 형식 여부
- model answer에는 있는데 fact anchor에는 없는 topic
- fact anchor에는 있는데 model answer에는 없는 topic
- topic별 model answer 개수 요약
- topic별 fact anchor 개수 요약

기본 실행:

```bash
python3 scripts/validate_model_fact_consistency.py
```

warning까지 실패로 처리:

```bash
python3 scripts/validate_model_fact_consistency.py --strict
```

정상 예시:

```text
VALID
model answers: 47
fact topics: 47
shared topics: 47
```

오류 예시:

```text
INVALID
ERROR: model topic missing in fact anchors: some_topic_id
ERROR: fact topic has no model answer: old_topic_id
```

---

## 13. 난이도와 점수 Ceiling

문제 난이도는 기존 A/B/C/D/E 점수를 대체하지 않습니다. 채점 엄격도, 고득점 가능성, 선택 전략 평가에 보조로 사용합니다.

| Profile | 의미 | 기본 ceiling |
|---|---|---:|
| `BASIC_CONCEPT` | 정의, 개념, 구성 중심 | 15.00 |
| `FIELD_APPLICATION` | 현장 적용, 선정, 개선방안 중심 | 15.75 |
| `DESIGN_EVALUATION` | 설계, 평가, 효과 분석 중심 | 16.50 |
| `THEORY_CORE` | 제어이론, 2차 시스템, 안정도 등 핵심 이론 | 17.50 |

기본 모드:

```env
DIFFICULTY_CEILING_MODE=warn
```

`warn` 모드는 cap 후보만 계산하고 실제 점수는 바꾸지 않습니다. 실제 점수를 제한하려면 다음을 사용합니다.

```env
DIFFICULTY_CEILING_MODE=strict
```

---

## 14. 문항 선택 전략

기술사 시험은 여러 문제 중 일부를 선택해 답안을 작성합니다. 따라서 Bot은 개별 답안 점수와 문항 선택 전략을 분리합니다.

핵심 원칙:

```text
쉬운 문제 = 안정 점수형, ceiling 낮음
제어이론 문제 = 고위험·고보상형
제어이론 선택 자체 = 가산점 없음
제어이론 정확 풀이 = 고득점 band unlock
제어이론 회피 = 개별 감점이 아니라 선택 전략 risk
```

제어이론, feedback system, 2차 시스템, 안정도, 과도응답 계열은 `CORE_MUST_PREPARE`로 관리합니다.

---

## 15. 업데이트 작업 표준 절차

모범답안 또는 Fact Anchor를 수정한 뒤에는 아래 순서를 따릅니다.

```bash
cd ~/hermes/workspace/prof_eng_answer

python3 scripts/validate_model_answer_bank.py
python3 scripts/validate_fact_anchor_bank.py
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all

grep -nE 'Ã|Â|�' rubrics/model_answers/industrial_instrumentation_control.json || echo 'OK: model answer mojibake 없음'
grep -nE 'Ã|Â|�' rubrics/fact_anchors/industrial_instrumentation_control.json || echo 'OK: fact anchor mojibake 없음'
grep -nE 'Ã|Â|�' scripts/import_review_design.py || echo 'OK: importer mojibake 없음'

git diff --check
git status --short
```

문제가 없으면 commit합니다.

```bash
git add README.md scripts/validate_model_fact_consistency.py rubrics/model_answers/industrial_instrumentation_control.json rubrics/fact_anchors/industrial_instrumentation_control.json
git commit -m "Update rubric bank documentation and consistency validation"
```

---

## 16. 상세 문서

| 문서 | 설명 |
|---|---|
| `docs/grading_architecture.md` | A/B/C/D/E 채점 구조 |
| `docs/llm_provider.md` | Gemini, CLOVA provider 구조 |
| `docs/rubric_authoring_guide.md` | Rubric, Question Type, Model Answer 작성 |
| `docs/difficulty_and_selection_strategy.md` | 난이도, ceiling, 문항 선택 전략 |
| `docs/docker_compose_usage.md` | Docker compose 운영 방식 |
| `docs/question_type_taxonomy.md` | question_type v2, sub_criteria, coverage 보정 방식 |
