# Prof Eng Answer

산업계측제어기술사 답안 채점 Telegram Bot입니다.

이 프로젝트는 기술사 답안을 다음 기준으로 평가합니다.

- 문제 의도 파악
- Fact 기반 기술 설명
- 문제점, 리스크, 적용상 쟁점 진단
- 개선방안, 설계 판단, 현장 제언
- 답안 연결성 및 면접 방어 가능성

기본 채점 구조는 A/B/C/D/E 25점 체계입니다.

| 항목 | 배점 | 의미 |
|---|---:|---|
| A | 4 | 배경과 문제 진입 |
| B | 5 | 문제 요구 파악 |
| C | 8 | 유형별 Fact 기반 내용 설명 |
| D | 6 | 현장 적용, 설계 판단, 제언 |
| E | 2 | 연결성, 면접 방어 가능성 |

---

## 빠른 실행

운영 환경에서는 상위 `~/hermes/docker-compose.yml`에서 실행합니다.

```bash

cd ~/hermes
docker compose up -d
docker compose ps
```

정상 상태:

```text

hermes_agent          Up
prof_eng_answer_bot   Up
```

로그 확인:

```bash

tail -n 120 ~/hermes/workspace/prof_eng_answer/logs/prof_eng_answer.log
```

봇만 재시작:

```bash

cd ~/hermes
docker compose restart prof-eng-answer-bot
```

---

## Docker 자동 실행 구조

운영 환경은 두 컨테이너로 분리합니다.

| 서비스 | 역할 |
|---|---|
| `hermes` | Hermes agent 기본 컨테이너 |
| `prof-eng-answer-bot` | Telegram 채점 Bot 자동 실행 컨테이너 |

`prof-eng-answer-bot`은 Docker 시작 시 자동으로 `bot.py`를 실행합니다.

실행 스크립트:

```text

scripts/run_prof_eng_bot.sh
```

중복 polling을 막기 위해 `hermes_agent` 안에서 수동으로 `nohup python bot.py`를 실행하지 않습니다.

---

## 환경변수

운영 환경변수는 상위 디렉터리의 `.env`에서 관리합니다.

```text

~/hermes/.env
```

주요 변수:

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
| `DIFFICULTY_CEILING_MODE` | `warn` 또는 `strict` |
| `QUESTION_TYPE_COVERAGE_SCORE_MODE` | question_type coverage 보정 모드. `warn`, `strict`, `off` |

`.env`는 Git에 올리지 않습니다.

---

## LLM Provider

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

## 채점 Pipeline

현재 주요 순서는 다음과 같습니다.

```text

1. 기본 채점자별 분석
2. Gemini 또는 CLOVA semantic grader 적용
3. phase2 layered scoring 적용
4. phase20 difficulty strategy 출력
5. phase21 difficulty ceiling 적용
```

정상 로그 예시:

```text

[agent] phase2 layered scoring applied: ...
[agent] phase20 final difficulty strategy applied: ...
[agent] phase21 final difficulty ceiling evaluated: ...
```

중요한 순서:

```text

phase2 -> phase20 -> phase21
```

---

## 난이도와 점수 Ceiling

문제 난이도는 기존 A/B/C/D/E 점수를 대체하지 않습니다.  
채점 엄격도, 고득점 가능성, 선택 전략 평가에 보조로 사용합니다.

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

`warn` 모드는 cap 후보만 계산하고 실제 점수는 바꾸지 않습니다.

실제 점수를 제한하려면:

```env

DIFFICULTY_CEILING_MODE=strict
```

`strict` 모드에서는 ceiling을 초과한 점수를 실제로 제한합니다.

제어이론 문제는 선택 자체로 가산점을 주지 않습니다.  
정확히 풀었을 때만 16.5~17.5점 상위 band가 열립니다.

---

## 문항 선택 전략

기술사 시험은 여러 문제 중 일부를 선택해 답안을 작성합니다.  
따라서 Bot은 개별 답안 점수와 문항 선택 전략을 분리합니다.

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

## 주요 파일

| 파일 | 역할 |
|---|---|
| `bot.py` | Telegram Bot 진입점 |
| `grading_agents.py` | 채점 pipeline |
| `difficulty_strategy.py` | 문제 난이도와 선택 중요도 분류 |
| `difficulty_output_adapter.py` | phase20 난이도 설명 출력 |
| `difficulty_score_ceiling.py` | phase21 ceiling 계산 및 strict 적용 |
| `scripts/run_prof_eng_bot.sh` | Docker 자동 실행 스크립트 |
| `rubrics/difficulty_profiles/default.json` | 난이도 Profile 정의 |
| `rubrics/topic_importance/industrial_instrumentation_control.json` | topic별 난이도와 선택 중요도 |
| `rubrics/exam_selection/default.json` | 시험 문항 선택 전략 기준 |

---

## 검증 명령

Python 문법 확인:

```bash

python3 -m py_compile \
  bot.py \
  grading_agents.py \
  difficulty_strategy.py \
  difficulty_output_adapter.py \
  difficulty_score_ceiling.py
```

난이도 전략 검증:

```bash

python3 scripts/validate_difficulty_strategy.py
```

Docker 상태 확인:

```bash

cd ~/hermes
docker compose ps
```

Bot 프로세스 중복 확인:

```bash

docker exec prof_eng_answer_bot bash -lc 'pgrep -af "python.*bot.py" || true'
docker exec hermes_agent bash -lc 'pgrep -af "python.*bot.py" || true'
```

---


---

## Question Type v2

2~4교시 답안 채점에서는 단답식 `DEFINE` 유형을 사용하지 않습니다.  
대신 C항목 Fact 설명과 D항목 현장 판단을 보강하기 위해 4개 question_type lens를 사용합니다.

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

## 상세 문서

| 문서 | 설명 |
|---|---|
| `docs/grading_architecture.md` | A/B/C/D/E 채점 구조 |
| `docs/llm_provider.md` | Gemini, CLOVA provider 구조 |
| `docs/rubric_authoring_guide.md` | Rubric, Question Type, Model Answer 작성 |
| `docs/difficulty_and_selection_strategy.md` | 난이도, ceiling, 문항 선택 전략 |
| `docs/docker_compose_usage.md` | Docker compose 운영 방식 |
| `docs/question_type_taxonomy.md` | question_type v2, sub_criteria, coverage 보정 방식 |

## 문서

현재 구조와 운영 절차는 `docs` 디렉터리에 정리한다.

| 문서 | 목적 |
|---|---|
| `docs/README.md` | 문서 인덱스 |
| `docs/operation_runbook.md` | 운영 점검, 재시작, 장애 대응 |
| `docs/docker_compose_usage.md` | Docker Compose 운영 방식 |
| `docs/grading_architecture.md` | A/B/C/D/E 채점 구조와 pipeline |
| `docs/question_type_taxonomy.md` | Question Type v2 taxonomy와 coverage |
| `docs/difficulty_and_selection_strategy.md` | Difficulty Profile, ceiling, 문항 선택 전략 |
| `docs/llm_provider.md` | Gemini/CLOVA provider 설정 |
| `docs/rubric_authoring_guide.md` | Rubric, Fact Anchor, Model Answer 작성법 |

운영 중 문제가 생기면 먼저 `docs/operation_runbook.md`를 확인한다.

