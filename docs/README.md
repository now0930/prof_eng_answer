# Documentation Index

이 디렉터리는 `prof_eng_answer`의 운영 문서와 rubric 작성 문서를 보관한다.

이 문서는 과거 문서 조각을 이어 붙인 파일이 아니라, 현재 코드 구조와 현재 docs 디렉터리 구성을 기준으로 새로 작성한 문서 인덱스다.

## 1. 문서 우선순위

코드와 문서가 충돌할 때는 다음 순서를 따른다.

1. 현재 Python 코드
2. 현재 JSON Rubric Bank
3. 루트 `README.md`
4. `docs/README.md`
5. docs 하위 세부 문서
6. `docs/archive/` 하위 과거 문서

오래된 구조 설명, migration 기록, 현재 코드와 충돌할 수 있는 문서는 현재 기준 문서로 사용하지 않는다. 필요한 경우 `docs/archive/` 아래로 이동한다.

## 2. 현재 기준 문서

현재 main의 `docs/` 디렉터리에 존재하는 기준 문서는 다음과 같다.

| 문서 | 역할 |
|---|---|
| `operation_runbook.md` | Bot 운영, 재시작, 장애 대응 |
| `docker_compose_usage.md` | Docker Compose 기반 실행 방식 |
| `grading_architecture.md` | A/B/C/D/E 25점 채점 구조 |
| `question_type_taxonomy.md` | Question Type 기준과 분류 원칙 |
| `difficulty_and_selection_strategy.md` | 문항 난이도와 선택 전략 |
| `llm_provider.md` | Gemini, CLOVA 등 LLM provider 설정 |
| `rubric_authoring_guide.md` | Model Answer, Fact Anchor, Topic Importance 작성 방법 |
| `model_answer_generator_prompt.md` | Model Answer Bank 초안 생성 프롬프트 |
| `fact_anchor_generator_prompt.md` | Fact Anchor Bank 초안 생성 프롬프트 |
| `logic_check_profiles_readme.md` | 표, 도면, 수식, 비교 구조의 Logic Check 반영 기준 |
| `logic_check_profile_generator_prompt.md` | Logic Check Profile JSON 초안 생성 프롬프트 |
| `logic_check_json_generator_prompt.md` | Logic Check Bank JSON 초안 생성 프롬프트 |
| `archive/` | 과거 문서와 참고용 이력 문서 |

## 3. 코드와 직접 연결되는 기준 파일

| 구분 | 파일 |
|---|---|
| Bot entrypoint | `bot.py` |
| Semantic grading | `grading_agents.py` |
| Scoring model | `rubrics/scoring_model/default.json` |
| Rater profile | `rubrics/raters/layered_default.json` |
| Question Type profile | `rubrics/question_types/default.json` |
| Model Answer Bank | `rubrics/model_answers/industrial_instrumentation_control.json` |
| Fact Anchor Bank | `rubrics/fact_anchors/industrial_instrumentation_control.json` |
| Topic Importance | `rubrics/topic_importance/industrial_instrumentation_control.json` |
| Logic Check Bank | `rubrics/logic_checks/industrial_instrumentation_control.json` |
| Logic Check Profile | `rubrics/logic_check_profiles/industrial_instrumentation_control.json` |

## 4. Question Type 문서화 기준

현재 `rubrics/question_types/default.json` 기준으로 question type은 4개 active 대분류와 10개 legacy mapping으로 구성된다.

### 4.1 Active question type 4개

| Active Type | 한국어명 | absorbs_legacy_types |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | `PRINCIPLE`, `CALC_DESIGN` |
| `DIAGNOSIS_ACTION` | 진단·대책형 | `PROBLEM_SOLVE`, `CAUSE_ACTION` |
| `COMPARE_SELECTION` | 비교·선정형 | `COMPARE`, `STRUCTURE` |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | `PROCEDURE`, `APPLICATION`, `EVALUATION`, `STRUCTURE` |

### 4.2 Legacy question type 10개

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

문서에 “10개 active type”이라고 쓰지 않는다. 정확한 표현은 “10개 legacy type을 4개 active type으로 매핑한다”이다.

## 5. 문서별 유지 원칙

| 문서 유형 | 유지 원칙 |
|---|---|
| 운영 runbook | 실제 Docker Compose와 컨테이너 이름 기준으로 유지 |
| 채점 구조 문서 | `rubrics/scoring_model/default.json` 기준으로 유지 |
| Question Type 문서 | `rubrics/question_types/default.json` 기준으로 유지 |
| Rubric 작성 문서 | Model Answer Bank와 Fact Anchor Bank schema 기준으로 유지 |
| Logic Check 문서 | `logic_check_profiles` JSON과 evaluator 코드 기준으로 유지 |
| Archive 문서 | 참고용으로만 유지하고 현재 기준으로 인용하지 않음 |

## 6. Logic Check 문서 작성 기준

Logic Check 관련 문서는 다음 기준으로 분리한다.

| 문서 | 기준 |
|---|---|
| `logic_check_profiles_readme.md` | Logic Check Profile 운영 원칙과 표·도면·수식 반영 기준 |
| `logic_check_profile_generator_prompt.md` | `rubrics/logic_check_profiles/...json`에 넣을 LLM verifier profile 생성 프롬프트 |
| `logic_check_json_generator_prompt.md` | `rubrics/logic_checks/...json`에 넣을 rule bank 생성 프롬프트 |

역할 구분:

| 구분 | 역할 |
|---|---|
| Logic Check Profile | candidate evidence, truth schema, fatal/safe condition 등 LLM verifier용 지식 |
| Logic Check Bank | regex 기반 fatal/major/minor check, question type check, D/E feedback check |

## 7. README 관리 원칙

루트 README는 다음 내용을 중심으로 유지한다.

1. 프로젝트 목적
2. 실행 구조
3. 주요 Python 모듈
4. Rubric Bank 구조
5. A/B/C/D/E scoring model
6. Question Type lens
7. Logic Check 운영 구조
8. 문서 인덱스
9. 검증 명령
10. commit 절차

루트 README에는 과거 migration log나 긴 검증 로그를 누적하지 않는다.

## 8. 검증 명령

기본 검증:

```bash
cd ~/hermes/workspace/prof_eng_answer

python3 -m py_compile \
  bot.py \
  grading_agents.py \
  difficulty_score_ceiling.py \
  logic_check_evaluator.py \
  logic_llm_verifier.py

python3 -m json.tool rubrics/logic_check_profiles/industrial_instrumentation_control.json >/tmp/logic_profile_check.json
python3 scripts/validate_logic_check_bank.py
python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_audit/run_rubric_audit.py
git diff --check
```

문서 변경 후 확인:

```bash
grep -n 'logic_check_profile_generator_prompt\|logic_check_json_generator_prompt' README.md docs/README.md
grep -n 'PRINCIPLE_INTERPRETATION\|DEFINE\|legacy question type\|STRUCTURE' README.md docs/README.md
grep -n 'logic_check_profiles_readme.md' README.md docs/README.md

git diff --check
git diff --stat
```
