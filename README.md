# prof_eng_answer

`prof_eng_answer`는 산업계측제어기술사 2~4교시 논술형 답안을 Telegram Bot으로 입력받아, 25점 문항 기준으로 채점하고 보완 방향을 제시하는 답안 평가 시스템이다.

이 문서는 repository의 루트 안내서다. 목적은 다음 세 가지다.

1. 시스템이 무엇을 하는지 빠르게 설명한다.
2. Bot 실행과 검증 방법을 바로 제공한다.
3. 세부 설계 문서가 어디에 있는지 연결한다.

상세한 채점 구조, question type, rubric 작성법, Logic Check 작성법은 `docs/` 하위 문서에서 관리한다.

## 1. 빠른 실행

Docker Compose 기준 서비스 이름은 `prof-eng-answer-bot`이고 컨테이너 이름은 `prof_eng_answer_bot`이다.

실행:

    cd ~/hermes
    docker compose up -d prof-eng-answer-bot
    docker logs --tail=100 prof_eng_answer_bot

재시작:

    cd ~/hermes
    docker compose restart prof-eng-answer-bot
    docker logs --tail=100 prof_eng_answer_bot

로컬 기본 검증:

    cd ~/hermes/workspace/prof_eng_answer

    python3 -m py_compile \
      bot.py \
      grading_agents.py \
      difficulty_score_ceiling.py \
      logic_check_evaluator.py \
      logic_llm_verifier.py

    python3 scripts/validate_logic_check_de_policy.py
    python3 scripts/check_logic_check_de_claim_trust_regression.py
    python3 scripts/validate_logic_check_bank.py
    python3 scripts/rubric_manager.py validate-all
    python3 scripts/rubric_manager.py validate-topic-importance
    python3 scripts/validate_question_type_profile.py
    git diff --check

## 2. 시스템 개요

이 프로젝트는 단순 키워드 채점기가 아니다. 현재 채점 흐름은 다음 layer를 함께 사용한다.

| Layer | 역할 |
|---|---|
| Telegram Bot | 사용자의 답안 입력 수신과 채점 결과 출력 |
| LLM semantic grading | Gemini 또는 fallback provider를 통한 의미 평가 |
| A/B/C/D/E scoring model | 25점 문항 기준의 계층형 점수 평가 |
| Rater profile | 교수, 기술사, 기업 임원 관점의 layer별 평가 |
| Question Type lens | 문제 유형별 C/D 평가 방향 보정 |
| Model Answer Bank | 고득점 답안의 구조와 전개 기준 |
| Fact Anchor Bank | topic별 핵심 fact coverage 기준 |
| Topic Importance | 고빈도·고변별 topic 가중 판단 |
| Difficulty Strategy | 문항 난이도와 선택 전략 판단 |
| Logic Check | 핵심 이론 오류, fatal cap, D/E claim trust 판단 |
| Bot Output Formatter | Telegram 사용자에게 보여줄 결과 정리 |

핵심 원칙:

| 구분 | 의미 |
|---|---|
| Model Answer | 고득점 답안의 구조와 서술 방향 |
| Fact Anchor | 무엇을 썼는가, 즉 정답 요소 coverage |
| Logic Check | 맞게 썼는가, 즉 정답과 충돌하는 핵심 오류 |
| Question Type | 문제 요구 방식 충족 여부 |
| Difficulty Ceiling | 난이도와 fatal 오류에 따른 최종 점수 상한 |

## 3. 채점 기준 요약

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

상세 기준은 `docs/grading_architecture.md`에서 관리한다.

## 4. 현재 Question Type 요약

현재 `rubrics/question_types/default.json` 기준 question type은 4개 active 대분류와 10개 legacy type mapping으로 구성된다.

| Active Type | 한국어명 | 주요 의미 |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | 원리, 동작, 계산, 설계, 수식, 모델 해석 |
| `DIAGNOSIS_ACTION` | 진단·대책형 | 문제점, 원인, 영향, 대책, 개선방안 |
| `COMPARE_SELECTION` | 비교·선정형 | 비교, 종류, 분류, 장단점, 선정 기준 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | 적용, 사례, 절차, 시험, 교정, 평가 |

상세 기준은 `docs/question_type_taxonomy.md`에서 관리한다.

## 5. Logic Check 운영 요약

Logic Check는 단순 누락이나 표현 부족을 잡는 기능이 아니다. 정답과 직접 충돌하는 핵심 이론 오류를 검출하고, 필요한 경우 최종 점수 상한을 적용하기 위한 안전장치다.

현재 원칙:

1. Logic Check는 topic truth gate다.
2. Logic Check finding의 `affected_layers`는 A/B/C까지만 사용한다.
3. D/E 점수는 Logic Check가 직접 감점·가점하지 않는다.
4. D/E와의 연결은 `de_claim_trust` metadata로만 표현한다.
5. fatal 오류가 있으면 `difficulty_score_ceiling.py`에서 최종 score cap을 적용한다.
6. LLM verifier 실패 또는 confidence 부족 시 fatal을 강제하지 않는다.

관련 문서:

| 문서 | 역할 |
|---|---|
| `docs/logic_check_profiles_readme.md` | Logic Check Profile 운영 가이드 |
| `docs/logic_check_profile_generator_prompt.md` | LLM verifier profile 생성 프롬프트 |
| `docs/logic_check_json_generator_prompt.md` | Logic Check Bank 생성 프롬프트 |

## 6. 주요 코드 파일

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

## 7. Rubric Bank 구조

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

운영 원칙:

1. 채점 정책은 가능한 JSON rubric으로 관리한다.
2. Python 코드는 routing, parsing, validation, score postprocess에 집중한다.
3. Model Answer는 답안 구조와 고득점 요소를 정의한다.
4. Fact Anchor는 topic별 핵심 fact coverage를 정의한다.
5. Logic Check는 정답과 직접 충돌하는 핵심 이론 오류만 다룬다.
6. Question Type은 A/B/C/D/E 점수체계를 대체하지 않고 C/D 평가 방향을 보정한다.

형식 검증:

    python3 scripts/validate_rubric_bank_format.py

내용 검증:

    python3 scripts/validate_rubric_bank_content.py

## 8. 문서 위치

`docs/README.md`는 문서 인덱스와 문서별 책임 범위를 관리한다.

자주 보는 문서:

| 목적 | 문서 |
|---|---|
| 전체 문서 목록 | `docs/README.md` |
| 운영, 재시작, 장애 대응 | `docs/operation_runbook.md` |
| Docker Compose 실행 | `docs/docker_compose_usage.md` |
| A/B/C/D/E 채점 구조 | `docs/grading_architecture.md` |
| Question Type 기준 | `docs/question_type_taxonomy.md` |
| 난이도와 문항 선택 전략 | `docs/difficulty_and_selection_strategy.md` |
| LLM provider 설정 | `docs/llm_provider.md` |
| Rubric 작성 | `docs/rubric_authoring_guide.md` |
| Logic Check 운영 | `docs/logic_check_profiles_readme.md` |

## 9. README 유지 원칙

1. 루트 README는 프로젝트 소개, 실행, 검증, 핵심 구조 요약만 유지한다.
2. 세부 설계와 작성 규칙은 `docs/` 하위 문서로 분리한다.
3. 과거 migration log와 긴 검증 로그는 README에 누적하지 않는다.
4. README와 `docs/README.md`는 append 방식이 아니라 필요 시 완전 재작성한다.
5. 문서와 코드가 충돌하면 현재 Python 코드와 JSON Rubric Bank를 우선한다.
