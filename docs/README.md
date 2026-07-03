# Documentation Index

이 디렉터리는 `prof_eng_answer`의 운영 문서, 채점 설계 문서, rubric 작성 문서, Logic Check 작성 문서를 보관한다.

이 문서는 docs 디렉터리의 지도다. 프로젝트 소개, 빠른 실행, 전체 시스템 요약은 루트 `README.md`에서 관리한다.

## 1. 문서 역할 분리

| 문서 | 담당 범위 | 담당하지 않는 것 |
|---|---|---|
| `README.md` | 프로젝트 소개, 빠른 실행, 핵심 구조 요약, 기본 검증 | 세부 설계, rubric 작성 규칙, generator prompt 상세 |
| `docs/README.md` | docs 문서 인덱스, 문서별 책임 범위, 유지보수 규칙 | 루트 실행 안내의 반복, 전체 채점표 상세 반복 |
| docs 하위 세부 문서 | 각 주제의 상세 설계와 작성 기준 | 다른 문서의 긴 요약 복붙 |
| `docs/archive/` | 과거 문서와 참고 이력 | 현재 기준 문서 |

## 2. 문서 우선순위

코드와 문서가 충돌할 때는 다음 순서를 따른다.

1. 현재 Python 코드
2. 현재 JSON Rubric Bank
3. 루트 `README.md`
4. `docs/README.md`
5. docs 하위 세부 문서
6. `docs/archive/` 하위 과거 문서

오래된 구조 설명, migration 기록, 현재 코드와 충돌할 수 있는 문서는 현재 기준 문서로 사용하지 않는다. 필요한 경우 `docs/archive/` 아래로 이동한다.

## 3. 현재 기준 문서

| 문서 | 읽는 경우 | 관리 기준 |
|---|---|---|
| `operation_runbook.md` | Bot 운영, 재시작, 장애 대응이 필요할 때 | 실제 Docker Compose 서비스명과 컨테이너명 |
| `docker_compose_usage.md` | 로컬/서버 실행 방식을 확인할 때 | 현재 compose 파일과 mount 구조 |
| `grading_architecture.md` | A/B/C/D/E 25점 채점 구조를 볼 때 | `rubrics/scoring_model/default.json` |
| `question_type_taxonomy.md` | 문제 유형 기준과 legacy mapping을 볼 때 | `rubrics/question_types/default.json` |
| `difficulty_and_selection_strategy.md` | 난이도, 선택 전략, score ceiling을 볼 때 | `difficulty_strategy.py`, `difficulty_score_ceiling.py` |
| `llm_provider.md` | Gemini, CLOVA 등 provider 설정을 볼 때 | provider router와 환경 변수 |
| `rubric_authoring_guide.md` | Model Answer, Fact Anchor, Topic Importance를 작성할 때 | 각 rubric JSON schema |
| `model_answer_generator_prompt.md` | Model Answer Bank 초안을 만들 때 | model answer schema |
| `fact_anchor_generator_prompt.md` | Fact Anchor Bank 초안을 만들 때 | fact anchor schema |
| `logic_check_profiles_readme.md` | Logic Check Profile 운영 기준을 볼 때 | profile JSON과 verifier 코드 |
| `logic_check_profile_generator_prompt.md` | LLM verifier profile 초안을 만들 때 | `rubrics/logic_check_profiles/...json` |
| `logic_check_json_generator_prompt.md` | rule-based Logic Check Bank 초안을 만들 때 | `rubrics/logic_checks/...json` |
| `archive/` | 과거 판단 근거를 참고할 때 | 현재 기준으로 직접 인용하지 않음 |

## 4. 코드와 직접 연결되는 기준 파일

| 구분 | 파일 |
|---|---|
| Bot entrypoint | `bot.py` |
| Semantic grading | `grading_agents.py` |
| Provider routing | `llm_provider_router.py` |
| Scoring model | `rubrics/scoring_model/default.json` |
| Rater profile | `rubrics/raters/layered_default.json` |
| Question Type profile | `rubrics/question_types/default.json` |
| Model Answer Bank | `rubrics/model_answers/industrial_instrumentation_control.json` |
| Fact Anchor Bank | `rubrics/fact_anchors/industrial_instrumentation_control.json` |
| Topic Importance | `rubrics/topic_importance/industrial_instrumentation_control.json` |
| Logic Check Bank | `rubrics/logic_checks/industrial_instrumentation_control.json` |
| Logic Check Profile | `rubrics/logic_check_profiles/industrial_instrumentation_control.json` |

## 5. 문서별 책임 범위

### 5.1 채점 구조 문서

`grading_architecture.md`는 A/B/C/D/E layer의 의미, 배점, rater profile 연결을 관리한다.

이 문서에는 다음 내용을 둔다.

- A/B/C/D/E layer별 평가 기준
- 교수, 기술사, 기업 임원 rater 관점
- score cap과 postprocess의 위치
- Logic Check와 scoring model의 경계

### 5.2 Question Type 문서

`question_type_taxonomy.md`는 active question type과 legacy type mapping을 관리한다.

이 문서에는 다음 내용을 둔다.

- 4개 active question type
- 10개 legacy type mapping
- DEFINE과 STRUCTURE의 처리 기준
- C/D 평가 방향 보정 방식

`docs/README.md`에는 question type 표 전체를 반복하지 않는다.

### 5.3 Rubric 작성 문서

`rubric_authoring_guide.md`는 rubric JSON을 작성할 때의 공통 원칙을 관리한다.

이 문서에는 다음 내용을 둔다.

- Model Answer Bank 작성 기준
- Fact Anchor Bank 작성 기준
- Topic Importance 작성 기준
- expected structure, high score features, field application 요소의 관계

### 5.4 Logic Check 문서

Logic Check 관련 문서는 다음 기준으로 분리한다.

| 문서 | 기준 |
|---|---|
| `logic_check_profiles_readme.md` | Logic Check Profile 운영 원칙과 표·도면·수식 반영 기준 |
| `logic_check_profile_generator_prompt.md` | LLM verifier profile 생성 프롬프트 |
| `logic_check_json_generator_prompt.md` | rule-based Logic Check Bank 생성 프롬프트 |

역할 구분:

| 구분 | 역할 |
|---|---|
| Logic Check Profile | candidate evidence, truth schema, fatal conditions, safe conditions 등 LLM verifier용 지식 |
| Logic Check Bank | regex 기반 topic truth check, fatal/major/minor check, question type check, D/E claim trust metadata |
| D/E scoring | Logic Check가 직접 평가하지 않고 A/B/C/D/E scoring model이 담당 |
| D/E claim trust | Logic Check topic truth 결과를 D/E 주장 신뢰도 판단에 참고하는 metadata |

## 6. 문서 변경 후 검증

문서만 수정했을 때:

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/validate_logic_check_de_policy.py
    git diff --check
    git diff --stat
    git status --short

Logic Check 관련 문서를 수정했을 때:

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/validate_logic_check_de_policy.py
    python3 scripts/check_logic_check_de_claim_trust_regression.py
    python3 scripts/validate_logic_check_bank.py
    git diff --check

Question Type 또는 Rubric 관련 문서를 수정했을 때:

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/validate_rubric_bank_format.py
    python3 scripts/validate_rubric_bank_content.py
    python3 scripts/rubric_manager.py validate-all
    python3 scripts/rubric_manager.py validate-topic-importance
    python3 scripts/validate_question_type_profile.py
    git diff --check

## 7. 중복 방지 규칙

1. 루트 README에는 빠른 실행과 전체 구조 요약만 둔다.
2. docs README에는 문서 목록과 문서별 책임 범위만 둔다.
3. 세부 표와 긴 정책 설명은 전용 문서에 둔다.
4. 같은 표를 README와 docs README에 동시에 유지하지 않는다.
5. 검증 명령은 목적별 최소 명령만 둔다.
6. 오래된 D/E 직접 평가 구조나 deprecated prompt 표현은 다시 넣지 않는다.
7. README와 docs README는 append 방식으로 누적하지 않고 필요 시 완전 재작성한다.

## 8. commit 기준

문서 인덱스와 루트 README만 수정한 경우:

    cd ~/hermes/workspace/prof_eng_answer

    git add README.md docs/README.md
    git diff --cached --stat
    git diff --cached --check
    git commit -m "Split root and docs README responsibilities"

Logic Check 문서나 validator까지 함께 수정한 경우:

    git add README.md docs/README.md \
      docs/logic_check_profiles_readme.md \
      docs/logic_check_profile_generator_prompt.md \
      docs/logic_check_json_generator_prompt.md \
      scripts/validate_logic_check_de_policy.py

    git diff --cached --stat
    git diff --cached --check
    git commit -m "Refresh documentation structure and logic check docs"
