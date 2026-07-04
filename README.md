# prof_eng_answer

`prof_eng_answer`는 산업계측제어기술사 2~4교시 논술형 답안을 Telegram Bot으로 입력받아, 25점 문항 기준으로 채점하고 보완 방향을 제시하는 답안 평가 시스템이다.

이 README는 repository의 루트 안내서다. 세부 설계, rubric 작성법, topic pack 운영, Logic Check 작성 기준은 `docs/` 하위 문서에서 관리한다.

---

## 1. 빠른 실행

Docker Compose 기준 서비스 이름은 `prof-eng-answer-bot`이고, 컨테이너 이름은 `prof_eng_answer_bot`이다.

```bash
cd ~/hermes
docker compose up -d prof-eng-answer-bot
docker logs --tail=100 prof_eng_answer_bot
```

재시작:

```bash
cd ~/hermes
docker compose restart prof-eng-answer-bot
docker logs --tail=100 prof_eng_answer_bot
```

로컬 기본 검증:

```bash
cd ~/hermes/workspace/prof_eng_answer

python3 -m py_compile \
  bot.py \
  grading_agents.py \
  difficulty_score_ceiling.py \
  logic_check_evaluator.py \
  logic_llm_verifier.py

python3 scripts/rubric_manager.py validate-all
git diff --check
```

Topic Pack 기반 generated bank까지 검증할 때:

```bash
python3 scripts/rubric_manager.py validate-generated-pipeline
python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated
```

---

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
| Topic Importance | 핵심 topic의 난이도와 출제 중요도 |
| Difficulty Strategy | 문항 난이도와 선택 전략 판단 |
| Logic Check | topic별 핵심 이론 오류 검증과 fatal cap 판단 |
| D/E Claim Trust | Logic Check 결과를 D/E 주장 신뢰도 metadata로 연결 |
| Bot Output Formatter | Telegram 사용자에게 보여줄 결과 정리 |

핵심 원칙은 다음과 같다.

| 구분 | 의미 |
|---|---|
| Model Answer | 고득점 답안의 구조와 서술 방향 |
| Fact Anchor | 무엇을 썼는가, 즉 정답 요소 coverage |
| Logic Check | 맞게 썼는가, 즉 정답과 충돌하는 핵심 오류 |
| Question Type | 문제 요구 방식 충족 여부 |
| Difficulty Ceiling | 난이도와 fatal 오류에 따른 최종 점수 상한 |
| D/E Claim Trust | Logic Check topic 기반 D/E 주장의 이론적 신뢰도 metadata |

---

## 3. 채점 기준 요약

총점은 25점이다.

| Layer | 이름 | 배점 | 평가 초점 |
|---|---|---:|---|
| A | 배경과 문제 진입 | 4 | 배경이 문제점으로 자연스럽게 진입하는가 |
| B | 문제 요구 파악 | 5 | 출제자가 요구한 핵심 축을 잡았는가 |
| C | 유형별 Fact 기반 내용 설명 | 8 | 핵심 개념, 원리, 수식, 비교축을 정확히 설명하는가 |
| D | 현장 적용, 설계 판단, 제언 | 6 | 비용, 실현 가능성, 기존 설비 영향, 검증 방법을 고려하는가 |
| E | 연결성, 면접 방어 가능성 | 2 | 배경, 문제, fact, 대책이 논리적으로 연결되는가 |

| 기준 | 점수 |
|---|---:|
| 공식 합격선 | 15 / 25 |
| 실전 목표선 | 17.5 / 25 |
| 고득점 기준 | 20 / 25 |

D/E 점수는 A/B/C/D/E scoring model에서 산정한다. Logic Check는 D/E를 직접 감점·가점하지 않고, 해당 topic 기반 현장 적용 주장과 결론 주장의 신뢰도를 metadata로 제공한다.

---

## 4. Question Type 요약

현재 question type은 `rubrics/question_types/default.json` 기준으로 관리한다. active question type은 4개이고, legacy type 10개는 active type으로 매핑된다.

| Active Type | 한국어명 | 주요 의미 |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | 원리, 동작, 계산, 설계, 수식, 모델 해석 |
| `DIAGNOSIS_ACTION` | 진단·대책형 | 문제점, 원인, 영향, 대책, 개선방안 |
| `COMPARE_SELECTION` | 비교·선정형 | 비교, 종류, 분류, 장단점, 선정 기준 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | 적용, 사례, 절차, 시험, 교정, 평가 |

Question Type은 A/B/C/D/E 점수 체계를 대체하지 않는다. 문제 유형에 따라 C항목의 fact 전개 방식과 D항목의 현장 판단 방향을 보정한다.

상세 기준은 `docs/question_type_taxonomy.md`에서 관리한다.

---

## 5. Rubric Bank 구조

현재 rubric은 legacy bank와 topic pack 기반 generated bank를 함께 지원한다.

### 5.1 Legacy Rubric Bank

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

### 5.2 Topic Pack Source

`rubrics/topic_packs/<topic_id>/`는 사람이 관리하는 topic source of truth이다.

| 파일 | 역할 |
|---|---|
| `README.md` | 사람이 검토할 topic 설명서 |
| `fact_anchor.json` | topic별 핵심 fact coverage source |
| `model_answer.json` | topic별 고득점 답안 구조 source |
| `topic_importance.json` | 난이도, 중요도, high-band unlock 조건 source |
| `logic_check.json` | fatal/warn 이론 오류 source |
| `topic_status.json` | topic 상태와 hash 관리 |

### 5.3 Generated Rubric Bank

`rubrics/generated/`는 runtime에서 읽기 쉽게 topic pack source를 합친 build output이다.

| 파일 | 역할 |
|---|---|
| `fact_anchors.generated.json` | generated fact anchor bank |
| `model_answers.generated.json` | generated model answer bank |
| `topic_importance.generated.json` | generated topic importance bank |
| `logic_checks.generated.json` | generated logic check bank |
| `logic_check_profiles.generated.json` | generated LLM verifier profile bank |
| `topic_pack_manifest.generated.json` | generated topic manifest |

`RUBRIC_BANK_MODE=generated`이면 generated bank를 사용하고, `RUBRIC_BANK_MODE=legacy`이면 legacy bank를 사용한다. 운영 기본값은 generated bank 기준으로 관리한다.

확인:

```bash
python3 scripts/check_rubric_bank_paths.py
```

---

## 6. Logic Check 운영 요약

Logic Check는 단순 누락이나 표현 부족을 잡는 기능이 아니다. 정답과 직접 충돌하는 핵심 이론 오류를 검출하고, 필요한 경우 최종 score cap을 적용하기 위한 topic truth gate다.

운영 원칙:

1. Fact Anchor는 coverage를 넓게 본다.
2. Logic Check는 정답과 충돌하는 오류를 깊게 본다.
3. Logic Check 지식은 Python 코드가 아니라 JSON bank와 profile에 둔다.
4. LLM verifier는 answer에서 candidate evidence를 추출하고 truth schema와 비교한다.
5. LLM 실패 또는 confidence 부족 시 fatal을 강제하지 않는다.
6. 좋은 답안에도 등장할 수 있는 표현은 safe condition 또는 false positive caution으로 보호한다.
7. THEORY_CORE fatal이면 `difficulty_score_ceiling.py`에서 최종 score cap을 적용한다.
8. Logic Check finding의 `affected_layers`는 원칙적으로 A/B/C까지만 사용한다.
9. D/E와의 연결은 `de_claim_trust` metadata로 표현한다.

예: `second_order_lag_response_by_damping_ratio`에서 다음 오류는 fatal cap 대상이다.

- `ζ=1`을 과감쇠 또는 overdamped로 분류
- 과감쇠 또는 overdamped를 중근으로 설명
- 안정한 2차계 극점식을 `s = +ζωn ± jωd`처럼 양의 실수부로 표기
- 좌반평면과 우반평면의 안정성 관계를 반대로 설명

---

## 7. Topic Pack 추가 workflow

새 topic은 README나 JSON을 바로 runtime에 넣는 방식으로 관리하지 않는다. 아래 순서를 따른다.

```text
Topic Pack README
  → Topic Sheet 후보 생성
  → 사람이 Topic Sheet 검토
  → schema-locked JSON candidate 생성
  → topic pack quality/release 검증
  → generated bank promote
  → smoke/Telegram 재채점 확인
```

대표 명령:

```bash
# 1. topic pack 생성
python3 scripts/rubric_manager.py create-topic-pack \
  --topic-id <topic_id>

# 2. 사람이 topic README 작성
vim rubrics/topic_packs/<topic_id>/README.md

# 3. README에서 Topic Sheet 후보 생성
python3 scripts/generate_topic_sheet_from_readme.py \
  --topic-id <topic_id> \
  --model gemini-2.5-flash \
  --overwrite

# 4. 사람이 Topic Sheet 검토
vim docs/topic_sheets/<topic_id>.md

# 5. Topic Sheet에서 schema-locked JSON 생성
python3 scripts/generate_topic_pack_from_sheet.py \
  --topic-id <topic_id> \
  --sheet docs/topic_sheets/<topic_id>.md \
  --model gemini-2.5-flash

# 6. 검증 및 generated promote
python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated

# 7. smoke 확인
python3 scripts/rubric_manager.py smoke-topic-pack --topic-id <topic_id>
```

토픽 추가 상세 절차는 `docs/topic_pack_workflow.md`에서 관리한다.

---

## 8. 표와 다이어그램 처리 원칙

답안의 ASCII 표, 비교표, 도식, s-plane 그림, block diagram은 그 자체가 정답 또는 오답이 아니다. 채점기는 표와 다이어그램에서 **claim**을 추출해서 평가한다.

| 대상 | Fact Anchor 처리 | Logic Check 처리 |
|---|---|---|
| 비교표 | 올바른 구분, 용어, 수식, 비교축을 fact evidence로 인정 | 표 안의 잘못된 mapping은 fatal/warn 후보 |
| 다이어그램 | diagram이 말하는 극점 위치, 방향, 신호 흐름을 fact evidence로 인정 | 좌/우반평면 안정성 반전, 부호 오류 등은 fatal 후보 |
| 수식 전개 | 최종 수식과 정의를 fact evidence로 인정 | 정답과 충돌하는 최종식은 fatal 후보 |
| ASCII 그림 | 위치 자체보다 주변 라벨과 설명 문장을 함께 해석 | 그림만으로 fatal 처리하지 않고 claim이 명시될 때 적용 |
| dead time 설명 | 보조 설명으로 인정 가능 | 핵심 topic을 대체하면 major/warn 또는 topic miss 후보 |

중요한 기준:

- Fact Anchor는 “무엇을 언급했는가”를 본다.
- Logic Check는 “그 언급이 맞는가”를 본다.
- 표의 셀 배치만으로 fatal 처리하지 않는다.
- 표의 셀·라벨·본문 설명이 함께 정답과 충돌하면 Logic Check 대상이 된다.
- 다이어그램은 그림 자체가 아니라 그림에서 주장하는 극점 위치, 부호, 안정성, causal relation을 평가한다.

상세 기준은 `docs/rubric_authoring_guide.md`와 `docs/logic_check_profiles_readme.md`에서 관리한다.

---

## 9. 주요 코드 파일

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
| `rubric_bank_paths.py` | legacy/generated rubric bank 경로 선택 |
| `scripts/rubric_manager.py` | rubric/topic pack 관리 통합 CLI |
| `scripts/generate_topic_sheet_from_readme.py` | README에서 Topic Sheet 후보 생성 |
| `scripts/generate_topic_pack_from_sheet.py` | Topic Sheet에서 schema-locked JSON candidate 생성 |
| `scripts/build_generated_rubrics.py` | topic pack source를 generated bank로 build |
| `scripts/validate_*.py` | rubric, question type, model answer, fact anchor 검증 |

---

## 10. 문서 위치

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
| Topic Pack 추가 workflow | `docs/topic_pack_workflow.md` |
| Logic Check 운영 | `docs/logic_check_profiles_readme.md` |

---

## 11. 검증 명령

전체 기본 검증:

```bash
cd ~/hermes/workspace/prof_eng_answer

python3 -m py_compile \
  bot.py \
  grading_agents.py \
  difficulty_score_ceiling.py \
  logic_check_evaluator.py \
  logic_llm_verifier.py

python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_manager.py validate-generated-pipeline
python3 scripts/rubric_manager.py validate-topic-pack-release
python3 scripts/validate_question_type_profile.py
git diff --check
```

Topic Pack 변경 후:

```bash
python3 scripts/rubric_manager.py validate-topic-pack-quality
python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated
python3 scripts/rubric_manager.py smoke-topic-pack --topic-id <topic_id>
```

문서만 수정했을 때:

```bash
git diff --check
git diff --stat
git status --short
```

---

## 12. README 유지 원칙

1. 루트 README는 프로젝트 소개, 실행, 검증, 핵심 구조 요약만 유지한다.
2. 세부 설계와 작성 규칙은 `docs/` 하위 문서로 분리한다.
3. 과거 migration log와 긴 검증 로그는 README에 누적하지 않는다.
4. README와 `docs/README.md`는 append 방식이 아니라 필요 시 완전 재작성한다.
5. 문서와 코드가 충돌하면 현재 Python 코드와 JSON Rubric Bank를 우선한다.
