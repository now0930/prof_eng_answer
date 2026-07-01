# prof_eng_answer

`prof_eng_answer`는 산업계측제어기술사 답안을 Telegram으로 입력받아, 기술사 시험 관점에서 채점하고 보완 방향을 제시하는 답안 평가 Bot이다.

이 저장소의 문서는 **현재 Python 코드와 JSON Rubric Bank를 우선 기준**으로 한다. 오래된 설계 설명이나 migration 기록이 현재 코드와 충돌하면, 운영 판단은 코드와 active JSON 설정을 따른다.

## 1. 빠른 운영 기준

| 항목 | 현재 기준 |
|---|---|
| Repository 위치 | `~/hermes/workspace/prof_eng_answer` |
| 컨테이너 내부 경로 | `/workspace/prof_eng_answer` |
| Compose 실행 위치 | `~/hermes` |
| Bot 컨테이너 | `prof_eng_answer_bot` |
| Bot 실행 진입점 | `python -u bot.py` |
| Telegram 명령 | `/grade`, `/provider`, `/new`, `/status`, `/rubric`, `/help` |
| 기본 provider 정책 | `auto`: Gemini 우선, CLOVA fallback |
| 로컬 보조 모델 | Ollama `OLLAMA_MODEL` |
| 최종 Telegram 포맷터 | `bot.py::format_result()` |
| 최종 송신 정리 | `bot.py::send_message()` boundary |

운영 절차는 `docs/operation_runbook.md`를 우선한다.

## 2. 현재 채점 흐름

```text
Telegram /grade 입력
→ bot.py가 세션과 입력 저장
→ grading_agents.run_agent_pipeline() 호출
→ 로컬 보조 모델(Ollama) 1차 분석 시도
→ Gemini 또는 CLOVA semantic grader 적용
→ Python rule 기반 A/B/C/D/E 25점 재산정
→ 3인 채점자 layer 가중 합성
→ Fact Anchor / Model Answer Bank 참조
→ Question Type v2 coverage attach
→ Difficulty Profile 및 ceiling 평가
→ bot.py format_result()로 Telegram 출력 구성
→ send_message() boundary cleanup 후 전송
```

LLM 의미 평가는 최종 점수를 단독 결정하지 않는다. 최종 출력 점수는 Python 후처리에서 volume cap, Question Type coverage, Difficulty ceiling, fallback, 출력 정합성을 함께 반영한다.

## 3. A/B/C/D/E 25점 구조

| 항목 | 배점 | 평가 내용 |
|---|---:|---|
| A | 4 | 배경과 문제 진입 |
| B | 5 | 문제 요구 파악 |
| C | 8 | 유형별 Fact 기반 내용 설명 |
| D | 6 | 현장 적용·설계 판단·제언 |
| E | 2 | 연결성·면접 방어 가능성 |
| 합계 | 25 | 전체 답안 점수 |

| 기준선 | 점수 |
|---|---:|
| 공식 합격선 | 15 |
| 실전 목표선 | 17.5 |
| 고득점 기준 | 20 |

## 4. 3인 채점자 layer

Bot은 답안을 하나의 단일 관점으로만 보지 않고, 세 채점자 관점을 layer별로 합성한다.

| 채점자 | 주요 관점 |
|---|---|
| 교수 채점자 | 원리, 개념 정확성, 체계성, 이론적 설명 |
| 기술사 채점자 | 현장 절차, 적용 조건, 리스크, 검증 기준 |
| 기업 임원 채점자 | 비용, 유지보수성, 기존 설비 영향, 실현 가능성 |

Telegram 출력에서 3인 단순 평균과 가중 점수가 보일 수 있다. Difficulty ceiling이 적용된 경우, 가중 점수는 **ceiling 적용 전 점수**로 표시하고 최종 점수는 별도로 표시한다.

## 5. Question Type v2

Question Type은 A/B/C/D/E 점수를 대체하지 않는다. C항목의 fact 전개 방향과 D항목의 현장 판단 방향을 정하는 lens이다.

| question_type | 한국어명 | 핵심 방향 |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | 원리, 메커니즘, 수식, 계산, 결과 해석 |
| `DIAGNOSIS_ACTION` | 진단·대책형 | 문제, 원인, 영향, 대책, 검증 |
| `COMPARE_SELECTION` | 비교·선정형 | 비교축, 장단점, 적용 조건, 선정 판단 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | 대상, 구성, 절차, 평가 지표, 운영 개선 |

`DEFINE`은 신규 question type으로 사용하지 않는다. 기존 migration 기록에는 남을 수 있으나 신규 항목은 위 4개 중 하나를 사용한다.

## 6. Difficulty Profile

Difficulty Profile은 고득점 가능성, 문항 선택 전략, ceiling 후보를 설명하는 보조 lens이다.

| Profile | 의미 |
|---|---|
| `BASIC_CONCEPT` | 정의, 개념, 구성 중심 |
| `FIELD_APPLICATION` | 현장 적용, 선정, 개선방안 중심 |
| `DESIGN_EVALUATION` | 설계, 평가, 효과 분석 중심 |
| `THEORY_CORE` | 제어이론, 2차 시스템, 안정도 등 핵심 이론 |

`DIFFICULTY_CEILING_MODE`는 `warn`, `strict`, `off`를 지원한다. 운영 환경에서 `strict`이면 cap이 실제 점수에 적용된다.

## 7. 핵심 파일

| 구분 | 경로 | 역할 |
|---|---|---|
| Bot entrypoint | `bot.py` | Telegram polling, 명령 처리, 출력 포맷 |
| Pipeline | `grading_agents.py` | 채점 pipeline 중심 |
| Provider router | `llm_provider_router.py` | Gemini/CLOVA provider 선택 |
| Provider settings | `llm_provider_settings.py` | chat별 provider 설정 저장 |
| Gemini grader | `gemini_grader.py` | Gemini semantic grading |
| CLOVA grader | `clova_grader.py` | CLOVA semantic grading |
| Difficulty strategy | `difficulty_strategy.py` | Difficulty Profile 분류 |
| Difficulty output | `difficulty_output_adapter.py` | difficulty 설명 attach |
| Difficulty ceiling | `difficulty_score_ceiling.py` | ceiling 후보 계산과 strict 적용 |
| Question Type taxonomy | `question_type_taxonomy.py` | v2 taxonomy loader/detector |
| Question Type coverage | `question_type_coverage_adapter.py` | coverage 출력 보강 |
| Model Answer router | `model_answer_router.py` | Model Answer Bank 참조 |
| Rubric registry | `rubric_registry.py` | Rubric 파일 로딩 |
| Rubric manager | `scripts/rubric_manager.py` | Rubric 관리 CLI |

## 8. Rubric JSON Bank

| JSON | 역할 | 일반 수정 여부 |
|---|---|---|
| `rubrics/model_answers/industrial_instrumentation_control.json` | topic/question_type별 답안 구조 | 수정 대상 |
| `rubrics/fact_anchors/industrial_instrumentation_control.json` | topic별 핵심 fact 기준 | 수정 대상 |
| `rubrics/topic_importance/industrial_instrumentation_control.json` | 주제 중요도와 문항 선택 전략 | 제한적 수정 |
| `rubrics/question_types/default.json` | Question Type v2 4개 lens | 보통 수정하지 않음 |
| `rubrics/difficulty_profiles/default.json` | Difficulty Profile 정의 | 보통 수정하지 않음 |
| `rubrics/scoring_model/default.json` | A/B/C/D/E 배점과 cap rule | 정책 변경 시 수정 |
| `rubrics/raters/layered_default.json` | 3인 채점자 관점 | 정책 변경 시 수정 |
| `rubrics/active_profile.json` | active config root | 보통 수정하지 않음 |

## 9. 문서 구조

| 문서 | 단일 책임 |
|---|---|
| `docs/README.md` | 문서 인덱스와 우선순위 |
| `docs/operation_runbook.md` | 운영 점검, 재시작, 장애 대응 |
| `docs/docker_compose_usage.md` | Docker Compose 사용법 |
| `docs/grading_architecture.md` | 채점 pipeline과 점수 구조 |
| `docs/question_type_taxonomy.md` | Question Type v2 taxonomy |
| `docs/difficulty_and_selection_strategy.md` | Difficulty, ceiling, 문항 선택 전략 |
| `docs/llm_provider.md` | Gemini/CLOVA/Ollama provider 구조 |
| `docs/rubric_authoring_guide.md` | Rubric Bank 수정·검증 절차 |
| `scripts/rubric_audit/README.md` | rubric audit 도구 설명 |

`docs/migration_plan.md`, `docs/structure_review.md`는 현재 실행 기준 문서가 아니라 reference/archive 성격으로 본다.

## 10. 검증 명령

일반 검증:

```bash
cd ~/hermes/workspace/prof_eng_answer
python3 -m py_compile \
  bot.py \
  grading_agents.py \
  gemini_grader.py \
  clova_grader.py \
  difficulty_strategy.py \
  difficulty_output_adapter.py \
  difficulty_score_ceiling.py \
  question_type_taxonomy.py \
  question_type_coverage_adapter.py \
  question_type_coverage_score_adjuster.py \
  semantic_question_type_prompt.py \
  semantic_question_type_postprocess.py
python3 scripts/rubric_manager.py validate-all
git diff --check
git status --short
```

Rubric audit:

```bash
python3 scripts/rubric_audit/run_rubric_audit.py
```

Audit 통과 기준:

```text
Fact Anchor MAJOR = 0
Model Answer relationship MAJOR = 0
validate-all = OK
priority MINOR = 0
```

일반 `MINOR`는 advisory로 유지할 수 있다. `MINOR`를 0으로 만들기 위해 Model Answer를 과도하게 늘리거나 validator에 과적합하지 않는다.
