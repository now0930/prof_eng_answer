# prof_eng_answer

`prof_eng_answer`는 산업계측제어기술사 2~4교시 논술형 답안을 Telegram Bot으로 입력받아, 25점 문항 기준으로 채점하고 보완 방향을 제시하는 답안 평가 시스템이다.

루트 README는 빠른 실행, 검증, 핵심 구조, 문서 위치만 안내한다. 세부 설계와 운영 규칙은 `docs/` 하위 문서에서 관리한다.

---

## 빠른 실행

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

---

## 빠른 검증

로컬에서 기본 검증은 아래 명령 하나로 수행한다.

```bash
cd ~/hermes/workspace/prof_eng_answer
PROMOTE_GENERATED=0 scripts/validate_release.sh
```

generated rubric bank를 실제 파일에 반영해야 할 때만 promote 모드로 실행한다.

```bash
PROMOTE_GENERATED=1 scripts/validate_release.sh
```

문서만 수정했을 때는 최소한 아래를 확인한다.

```bash
git diff --check
git diff --stat
git status --short --branch
```

---

## 채점 구조

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

채점기는 단순 키워드 채점기가 아니라 다음 layer를 함께 사용한다.

| Layer | 역할 |
|---|---|
| LLM semantic grading | Gemini 또는 fallback provider를 통한 의미 평가 |
| A/B/C/D/E scoring model | 25점 문항 기준의 계층형 점수 평가 |
| Rater profile | 교수, 기술사, 기업 임원 관점의 layer별 평가 |
| Question Type lens | 문제 유형별 C/D 평가 방향 보정 |
| Model Answer Bank | 고득점 답안의 구조와 전개 기준 |
| Fact Anchor Bank | topic별 핵심 fact coverage 기준 |
| Topic Importance | 핵심 topic의 난이도와 출제 중요도 |
| Difficulty Strategy | 문항 난이도와 선택 전략 판단 |
| Logic Check | topic별 핵심 이론 오류 검증과 fatal cap 판단 |
| Bot Output Formatter | Telegram 사용자에게 보여줄 결과 정리 |

---

## Question Type

현재 active question type은 `rubrics/question_types/default.json` 기준으로 관리한다.

| Active Type | 한국어명 | 주요 의미 |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | 원리, 동작, 계산, 설계, 수식, 모델 해석 |
| `DIAGNOSIS_ACTION` | 진단·대책형 | 문제점, 원인, 영향, 대책, 개선방안 |
| `COMPARE_SELECTION` | 비교·선정형 | 비교, 종류, 분류, 장단점, 선정 기준 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | 적용, 사례, 절차, 시험, 교정, 평가 |

상세 기준은 `docs/question_type_taxonomy.md`에서 관리한다.

---

## Rubric Bank 구조

현재 rubric은 legacy bank와 topic pack 기반 generated bank를 함께 지원한다.

| 구분 | 위치 | 역할 |
|---|---|---|
| Legacy Rubric Bank | `rubrics/*/*.json` | 기존 runtime rubric bank |
| Topic Pack Source | `rubrics/topic_packs/<topic_id>/` | 사람이 관리하는 topic source of truth |
| Generated Rubric Bank | `rubrics/generated/*.generated.json` | topic pack source를 합친 build output |

운영 기본값은 generated bank 기준으로 관리한다.

```bash
python3 scripts/check_rubric_bank_paths.py
```

Topic Pack source의 기본 파일은 다음과 같다.

| 파일 | 역할 |
|---|---|
| `README.md` | 사람이 검토할 topic 설명서 |
| `fact_anchor.json` | topic별 핵심 fact coverage source |
| `model_answer.json` | topic별 고득점 답안 구조 source |
| `topic_importance.json` | 난이도, 중요도, high-band unlock 조건 source |
| `logic_check.json` | fatal/warn 이론 오류 source |
| `topic_status.json` | topic 상태와 hash 관리 |

---

## Logic Check 요약

Logic Check는 단순 누락이나 표현 부족을 잡는 기능이 아니다. 정답과 직접 충돌하는 핵심 이론 오류를 검출하고, 필요한 경우 최종 score cap을 적용하기 위한 topic truth gate다.

핵심 원칙은 다음과 같다.

| 구분 | 의미 |
|---|---|
| Fact Anchor | 무엇을 썼는가, 즉 정답 요소 coverage |
| Logic Check | 맞게 썼는가, 즉 정답과 충돌하는 핵심 오류 |
| Difficulty Ceiling | 난이도와 fatal 오류에 따른 최종 점수 상한 |
| D/E Claim Trust | Logic Check topic 기반 D/E 주장의 이론적 신뢰도 metadata |

상세 기준은 `docs/logic_check_profiles_readme.md`와 `docs/rubric_authoring_guide.md`에서 관리한다.

---

## Topic Pack workflow

새 topic은 README나 JSON을 바로 runtime에 넣지 않는다. 아래 흐름을 따른다.

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
python3 scripts/rubric_manager.py create-topic-pack --topic-id <topic_id>

python3 scripts/generate_topic_sheet_from_readme.py \
  --topic-id <topic_id> \
  --model gemini-2.5-flash \
  --overwrite

python3 scripts/generate_topic_pack_from_sheet.py \
  --topic-id <topic_id> \
  --sheet docs/topic_sheets/<topic_id>.md \
  --model gemini-2.5-flash

python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated
python3 scripts/rubric_manager.py smoke-topic-pack --topic-id <topic_id>
```

상세 절차는 `docs/topic_pack_workflow.md`에서 관리한다.

---

## 주요 코드 파일

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
| `difficulty_strategy.py` | 난이도와 문항 선택 전략 판단 |
| `difficulty_score_ceiling.py` | 분량, 난이도, fatal 오류 기반 점수 상한 적용 |
| `logic_check_evaluator.py` | Logic Check 적용 여부 판단과 결과 병합 |
| `logic_llm_verifier.py` | JSON profile 기반 이론 오류 검증 |
| `rubric_bank_paths.py` | legacy/generated rubric bank 경로 선택 |
| `grade_output_summarizer.py` | 사용자 출력 요약과 formatting |
| `scripts/rubric_manager.py` | rubric/topic pack 관리 통합 CLI |
| `scripts/validate_release.sh` | release 전 통합 검증 |

---

## 문서 위치

`docs/README.md`는 문서 인덱스와 문서별 책임 범위를 관리한다.

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

## README 유지 원칙

1. 루트 README는 프로젝트 소개, 실행, 검증, 핵심 구조, 문서 링크만 유지한다.
2. 세부 설계와 작성 규칙은 `docs/` 하위 문서로 분리한다.
3. 과거 migration log와 긴 검증 로그는 README에 누적하지 않는다.
4. README와 `docs/README.md`는 append 방식이 아니라 필요 시 완전 재작성한다.
5. 문서와 코드가 충돌하면 현재 Python 코드와 JSON Rubric Bank를 우선한다.
