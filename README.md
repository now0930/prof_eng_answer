# prof_eng_answer

`prof_eng_answer`는 산업계측제어기술사 2~4교시 논술형 답안을 Telegram Bot으로 입력받아, 25점 문항 기준으로 채점하고 보완 방향을 제시하는 답안 평가 시스템이다.

이 README는 과거 문서 복구본이 아니라 현재 코드 구조와 현재 docs 디렉터리 구성을 기준으로 새로 작성한 문서다. 오래된 migration 기록, 임시 테스트 로그, 과거 README 조각은 포함하지 않는다.

## 1. 현재 시스템 개요

이 프로젝트는 단순 키워드 채점기가 아니다. 현재 구조는 다음 layer를 함께 사용한다.

| Layer | 역할 |
|---|---|
| Telegram Bot | 사용자의 답안 입력 수신과 채점 결과 출력 |
| LLM semantic grading | Gemini 또는 fallback provider를 통한 의미 평가 |
| A/B/C/D/E scoring model | 25점 문항 기준의 계층형 점수 평가 |
| Rater profile | 교수, 기술사, 기업 임원 관점의 layer별 평가 |
| Question Type lens | 문제 유형별로 C/D 평가 방향 보정 |
| Model Answer Bank | 고득점 답안의 구조와 전개 기준 |
| Fact Anchor Bank | topic별 핵심 fact coverage 기준 |
| Difficulty Strategy | 문항 난이도와 선택 전략 판단 |
| Logic Check | 핵심 이론 오류와 fatal cap 판단 |
| Bot Output Formatter | Telegram 사용자에게 보여줄 결과 정리 |

핵심 원칙은 다음과 같다.

| 구분 | 의미 |
|---|---|
| Model Answer | 고득점 답안의 구조와 서술 방향 |
| Fact Anchor | 무엇을 썼는가, 즉 정답 요소 coverage |
| Logic Check | 맞게 썼는가, 즉 정답과 충돌하는 핵심 오류 |
| Question Type | 문제 요구 방식 충족 여부 |
| Difficulty Ceiling | 난이도와 fatal 오류에 따른 최종 점수 상한 |

## 2. 실행 구조

Docker Compose 기준 서비스는 `prof-eng-answer-bot`이고 컨테이너 이름은 `prof_eng_answer_bot`이다. Compose 설정은 repository를 `/workspace/prof_eng_answer`로 mount하고, `scripts/run_prof_eng_bot.sh`를 entrypoint로 실행한다.

일반 실행:

    cd ~/hermes
    docker compose up -d prof-eng-answer-bot
    docker logs --tail=100 prof_eng_answer_bot

재시작:

    cd ~/hermes
    docker compose restart prof-eng-answer-bot
    docker logs --tail=100 prof_eng_answer_bot

로컬 검증:

    cd ~/hermes/workspace/prof_eng_answer
    python3 -m py_compile bot.py grading_agents.py difficulty_score_ceiling.py logic_check_evaluator.py logic_llm_verifier.py
    python3 scripts/rubric_manager.py validate-all
    git diff --check

## 3. 주요 코드 파일

| 파일 | 역할 |
|---|---|
| `bot.py` | Telegram Bot entrypoint, 입력 처리, 결과 출력 |
| `grading_agents.py` | LLM 기반 semantic grading orchestration |
| `gemini_grader.py` | Gemini provider 기반 채점 호출 |
| `clova_grader.py` | CLOVA provider fallback |
| `llm_provider_router.py` | LLM provider 선택과 routing |
| `grading_config.py` | scoring model, rater profile, subject rubric 설정 로딩 |
| `rubric_registry.py` | rubric JSON 로딩과 참조 |
| `model_answer_router.py` | Model Answer Bank 검색 |
| `question_type_router.py` | 문제 유형 추론 |
| `question_type_coverage_adapter.py` | question type별 coverage 평가 |
| `difficulty_strategy.py` | 난이도와 문항 선택 전략 판단 |
| `difficulty_score_ceiling.py` | 분량, 난이도, fatal 오류 기반 점수 상한 적용 |
| `logic_check_evaluator.py` | Logic Check 적용 여부 판단과 결과 병합 |
| `logic_llm_verifier.py` | JSON profile 기반 이론 오류 검증 |
| `scripts/validate_*.py` | rubric, question type, model answer, fact anchor 검증 |
| `scripts/rubric_audit/` | rubric 관계와 품질 audit |

## 4. Rubric Bank 구조

| 구분 | 파일 |
|---|---|
| Scoring Model | `rubrics/scoring_model/default.json` |
| Rater Profile | `rubrics/raters/layered_default.json` |
| Question Type Profile | `rubrics/question_types/default.json` |
| Model Answer Bank | `rubrics/model_answers/industrial_instrumentation_control.json` |
| Fact Anchor Bank | `rubrics/fact_anchors/industrial_instrumentation_control.json` |
| Topic Importance | `rubrics/topic_importance/industrial_instrumentation_control.json` |
| Logic Check Bank | `rubrics/logic_checks/industrial_instrumentation_control.json` |
| Logic Check Profile | `rubrics/logic_check_profiles/industrial_instrumentation_control.json` |

Rubric 운영 원칙:

1. 채점 정책은 가능한 JSON rubric으로 관리한다.
2. Python 코드는 routing, parsing, validation, score postprocess에 집중한다.
3. Model Answer는 답안 구조와 고득점 요소를 정의한다.
4. Fact Anchor는 topic별 핵심 fact coverage를 정의한다.
5. Logic Check는 정답과 직접 충돌하는 핵심 이론 오류만 다룬다.
6. Question Type은 A/B/C/D/E 점수체계를 대체하지 않고 C/D 평가 방향을 보정한다.

## 5. A/B/C/D/E scoring model

총점은 25점이다.

| Layer | 이름 | 배점 | 평가 초점 |
|---|---|---:|---|
| A | 배경과 문제 진입 | 4 | 배경이 문제점으로 자연스럽게 진입하는가 |
| B | 문제 요구 파악 | 5 | 출제자가 요구한 핵심 축을 잡았는가 |
| C | 유형별 Fact 기반 내용 설명 | 8 | 핵심 개념, 원리, 수식, 비교축을 정확히 설명하는가 |
| D | 현장 적용, 설계 판단, 제언 | 6 | 비용, 실현 가능성, 기존 설비 영향, 검증 방법을 고려하는가 |
| E | 연결성, 면접 방어 가능성 | 2 | 배경, 문제, fact, 대책이 논리적으로 연결되는가 |

점수 기준:

| 기준 | 점수 |
|---|---:|
| 공식 합격선 | 15 / 25 |
| 실전 목표선 | 17.5 / 25 |
| 고득점 기준 | 20 / 25 |

## 6. Question Type lens

현재 코드의 question type 체계는 `rubrics/question_types/default.json` 기준이다. 구조는 **4개 active 대분류**와 **10개 legacy type mapping**으로 나뉜다.

Question Type은 별도 채점표가 아니다. 기존 A/B/C/D/E 점수체계를 유지하면서, 문제 유형에 따라 C항목의 fact 전개와 D항목의 현장 판단 방향을 보정한다.

### 6.1 Active question type 4개

현재 profile의 active question type은 다음 4개다.

| Active Type | 한국어명 | absorbs_legacy_types | 주요 의미 |
|---|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | `PRINCIPLE`, `CALC_DESIGN` | 원리, 동작, 계산, 설계, 수식, 모델, 계측·제어 원리 해석 |
| `DIAGNOSIS_ACTION` | 진단·대책형 | `PROBLEM_SOLVE`, `CAUSE_ACTION` | 문제점, 원인, 영향, 대책, 개선방안, 고려사항 |
| `COMPARE_SELECTION` | 비교·선정형 | `COMPARE`, `STRUCTURE` | 비교, 종류, 분류, 형식, 특징, 장단점, 선정 기준 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | `PROCEDURE`, `APPLICATION`, `EVALUATION`, `STRUCTURE` | 적용, 사례, 절차, 방법, 시험, 교정, 시스템 구성, 평가, 효과 분석 |

### 6.2 Legacy question type 10개

아래 10개는 과거 또는 사용자 표현에서 사용할 수 있는 legacy type이다. 현재 profile에서는 이들을 active 대분류로 매핑한다.

| Legacy Type | 한국어명 | legacy_mapping 기준 |
|---|---|---|
| `DEFINE` | 정의·개념 설명형 | `null`, 즉 신규 체계에서 독립 active type으로 사용하지 않음 |
| `PRINCIPLE` | 원리·메커니즘형 | `PRINCIPLE_INTERPRETATION` |
| `STRUCTURE` | 구성·분류형 | 기본 매핑은 `COMPARE_SELECTION`; 단 `IMPLEMENTATION_EVALUATION`도 absorbs_legacy_types에 `STRUCTURE`를 포함 |
| `COMPARE` | 비교·선정형 | `COMPARE_SELECTION` |
| `PROBLEM_SOLVE` | 문제점·개선방안형 | `DIAGNOSIS_ACTION` |
| `CAUSE_ACTION` | 원인·대책형 | `DIAGNOSIS_ACTION` |
| `PROCEDURE` | 절차·방법론형 | `IMPLEMENTATION_EVALUATION` |
| `CALC_DESIGN` | 계산·설계형 | `PRINCIPLE_INTERPRETATION` |
| `APPLICATION` | 사례·적용형 | `IMPLEMENTATION_EVALUATION` |
| `EVALUATION` | 평가·효과 분석형 | `IMPLEMENTATION_EVALUATION` |

정확한 표현:

| 표현 | 코드 기준 판단 |
|---|---|
| active question type은 4개다 | 맞음 |
| legacy question type은 10개이며 active 4개로 매핑된다 | 맞음 |
| DEFINE은 신규 체계에서 독립 active type으로 사용한다 | 틀림 |
| STRUCTURE의 legacy_mapping 기본값은 `COMPARE_SELECTION`이다 | 맞음 |
| STRUCTURE는 독립 question_type이 아니라 fact 설명 요소로 흡수된다 | 맞음 |

## 7. Logic Check 운영

Logic Check는 단순 누락이나 표현 부족을 잡는 기능이 아니다. 정답과 직접 충돌하는 핵심 이론 오류를 검출하고, 필요한 경우 최종 점수 상한을 적용하기 위한 layer다.

현재 핵심 적용 대상은 `second_order_lag_response_by_damping_ratio` 같은 THEORY_CORE 주제다.

운영 원칙:

1. Fact Anchor는 넓게 둔다.
2. Logic Check는 깊게 둔다.
3. Logic Check 지식은 Python 코드가 아니라 JSON profile에 둔다.
4. LLM verifier는 answer에서 candidate evidence만 보고 truth_schema와 비교한다.
5. LLM 실패 또는 confidence 부족 시 fatal을 강제하지 않는다.
6. 좋은 답안에도 등장하는 표현은 safe_conditions로 오탐을 막는다.
7. THEORY_CORE fatal이면 `difficulty_score_ceiling.py`에서 최종 score cap을 적용한다.

세부 문서:

- [Logic Check JSON Profile 운영 가이드](docs/logic_check_profiles_readme.md)

## 8. 문서 구조

현재 main의 `docs/` 디렉터리에 존재하는 기준 문서는 다음과 같다.

| 문서 | 역할 |
|---|---|
| `docs/README.md` | docs 디렉터리 인덱스 |
| `docs/operation_runbook.md` | 운영, 재시작, 장애 대응 |
| `docs/docker_compose_usage.md` | Docker Compose 실행 방식 |
| `docs/grading_architecture.md` | A/B/C/D/E 채점 구조 |
| `docs/question_type_taxonomy.md` | Question Type 기준 |
| `docs/difficulty_and_selection_strategy.md` | 난이도와 문항 선택 전략 |
| `docs/llm_provider.md` | LLM provider 설정 |
| `docs/rubric_authoring_guide.md` | rubric 작성 방법 |
| `docs/model_answer_generator_prompt.md` | Model Answer Bank 초안 생성 프롬프트 |
| `docs/fact_anchor_generator_prompt.md` | Fact Anchor Bank 초안 생성 프롬프트 |
| `docs/logic_check_profiles_readme.md` | 표, 도면, 수식, 비교 구조의 Logic Check 반영 기준 |
| `docs/archive/` | 과거 문서와 참고용 이력 문서 |

## 9. 검증 명령

기본 검증:

    cd ~/hermes/workspace/prof_eng_answer

    python3 -m py_compile       bot.py       grading_agents.py       difficulty_score_ceiling.py       logic_check_evaluator.py       logic_llm_verifier.py

    python3 -m json.tool rubrics/logic_check_profiles/industrial_instrumentation_control.json >/tmp/logic_profile_check.json

    python3 scripts/validate_logic_check_bank.py
    python3 scripts/rubric_manager.py validate-all
    python3 scripts/rubric_audit/run_rubric_audit.py
    git diff --check

문서만 수정했을 때:

    git diff --check
    git diff --stat
    git status --short

## 10. Commit 절차

문서만 커밋할 때:

    cd ~/hermes/workspace/prof_eng_answer

    git add README.md docs/README.md
    git diff --cached --stat
    git diff --cached --check
    git commit -m "Rewrite README from current code structure"
    git push

문서와 Logic Check guide까지 함께 커밋할 때:

    git add README.md docs/README.md docs/logic_check_profiles_readme.md
    git diff --cached --stat
    git diff --cached --check
    git commit -m "Refresh project documentation"
    git push

## 11. README 유지 원칙

1. README는 현재 코드 기준으로 유지한다.
2. 과거 migration log를 README에 누적하지 않는다.
3. 검증 결과 reports는 README에 붙이지 않는다.
4. 상세한 운영 절차는 docs 하위 문서로 분리한다.
5. 오래된 문서는 삭제하지 않고 필요 시 `docs/archive/`로 이동한다.
6. README와 docs/README는 append 방식이 아니라 필요 시 완전 재작성한다.
