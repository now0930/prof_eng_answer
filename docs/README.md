# Documentation Index

이 디렉터리는 `prof_eng_answer`의 운영 문서, 채점 설계 문서, rubric 작성 문서, Topic Pack authoring 문서, Logic Check 작성 문서를 보관한다.

이 문서는 docs 디렉터리의 지도다. 프로젝트 소개, 빠른 실행, 전체 시스템 요약은 루트 `README.md`에서 관리한다.

---

## 1. 문서 역할 분리

| 문서 | 담당 범위 | 담당하지 않는 것 |
|---|---|---|
| 루트 `README.md` | 프로젝트 소개, 빠른 실행, 핵심 구조 요약, 기본 검증 | 세부 설계, rubric 작성 규칙, generator prompt 상세 |
| `docs/README.md` | docs 문서 인덱스, 문서별 책임 범위, 유지보수 규칙 | 루트 실행 안내의 반복, 전체 채점표 상세 반복 |
| docs 하위 세부 문서 | 각 주제의 상세 설계와 작성 기준 | 다른 문서의 긴 요약 복붙 |
| `docs/archive/` | 과거 문서와 참고 이력 | 현재 기준 문서 |

---

## 2. 문서 우선순위

코드와 문서가 충돌할 때는 다음 순서를 따른다.

1. 현재 Python 코드
2. 현재 JSON Rubric Bank
3. Topic Pack source JSON
4. generated rubric bank
5. 루트 `README.md`
6. `docs/README.md`
7. docs 하위 세부 문서
8. `docs/archive/` 하위 과거 문서

오래된 구조 설명, migration 기록, 현재 코드와 충돌할 수 있는 문서는 현재 기준 문서로 사용하지 않는다. 필요한 경우 `docs/archive/` 아래로 이동한다.

---

## 3. 현재 기준 문서

| 문서 | 읽는 경우 | 관리 기준 |
|---|---|---|
| `operation_runbook.md` | Bot 운영, 재시작, 장애 대응이 필요할 때 | 실제 Docker Compose 서비스명과 컨테이너명 |
| `docker_compose_usage.md` | 로컬/서버 실행 방식을 확인할 때 | 현재 compose 파일과 mount 구조 |
| `grading_architecture.md` | A/B/C/D/E 25점 채점 구조를 볼 때 | `rubrics/scoring_model/default.json` |
| `question_type_taxonomy.md` | 문제 유형 기준과 legacy mapping을 볼 때 | `rubrics/question_types/default.json` |
| `difficulty_and_selection_strategy.md` | 난이도, 선택 전략, score ceiling을 볼 때 | `difficulty_strategy.py`, `difficulty_score_ceiling.py` |
| `llm_provider.md` | Gemini, CLOVA 등 provider 설정을 볼 때 | provider router와 환경 변수 |
| `rubric_authoring_guide.md` | Model Answer, Fact Anchor, Topic Importance, Logic Check source를 작성할 때 | topic pack source JSON schema |
| `topic_pack_workflow.md` | 새 topic 추가, README→Topic Sheet→JSON→generated promote 흐름을 볼 때 | `scripts/generate_topic_sheet_from_readme.py`, `scripts/generate_topic_pack_from_sheet.py`, `scripts/rubric_manager.py` |
| `logic_check_profiles_readme.md` | Logic Check Profile 운영 기준과 표·도면·수식 반영 기준을 볼 때 | profile JSON과 verifier 코드 |
| `logic_check_profile_generator_prompt.md` | LLM verifier profile 초안을 만들 때 | `rubrics/logic_check_profiles/*.json` |
| `logic_check_json_generator_prompt.md` | rule-based Logic Check Bank 초안을 만들 때 | `rubrics/logic_checks/*.json` 또는 topic pack `logic_check.json` |
| `topic_sheets/` | Topic Sheet 후보와 검토 완료본을 보관할 때 | 사람이 검토한 Markdown input |
| `archive/` | 과거 판단 근거를 참고할 때 | 현재 기준으로 직접 인용하지 않음 |

---

## 4. 코드와 직접 연결되는 기준 파일

### 4.1 Runtime entry / orchestration

| 구분 | 파일 |
|---|---|
| Bot entrypoint | `bot.py` |
| Semantic grading | `grading_agents.py` |
| Model Answer routing | `model_answer_router.py` |
| Question Type routing | `question_type_router.py` |
| Difficulty strategy | `difficulty_strategy.py` |
| Difficulty score ceiling | `difficulty_score_ceiling.py` |
| Logic Check evaluator | `logic_check_evaluator.py` |
| Logic LLM verifier | `logic_llm_verifier.py` |
| Rubric bank path resolver | `rubric_bank_paths.py` |

### 4.2 Legacy Rubric Bank

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

### 4.3 Topic Pack Source

| 구분 | 파일/디렉터리 |
|---|---|
| Topic Pack 원천 | `rubrics/topic_packs/<topic_id>/` |
| Topic Pack README | `rubrics/topic_packs/<topic_id>/README.md` |
| Fact Anchor source | `rubrics/topic_packs/<topic_id>/fact_anchor.json` |
| Model Answer source | `rubrics/topic_packs/<topic_id>/model_answer.json` |
| Topic Importance source | `rubrics/topic_packs/<topic_id>/topic_importance.json` |
| Logic Check source | `rubrics/topic_packs/<topic_id>/logic_check.json` |
| Topic 상태/hash | `rubrics/topic_packs/<topic_id>/topic_status.json` |

### 4.4 Generated Rubric Bank

| 구분 | 파일 |
|---|---|
| Fact Anchors | `rubrics/generated/fact_anchors.generated.json` |
| Model Answers | `rubrics/generated/model_answers.generated.json` |
| Topic Importance | `rubrics/generated/topic_importance.generated.json` |
| Logic Checks | `rubrics/generated/logic_checks.generated.json` |
| Logic Check Profiles | `rubrics/generated/logic_check_profiles.generated.json` |
| Topic Pack Manifest | `rubrics/generated/topic_pack_manifest.generated.json` |

`rubrics/topic_packs/`는 사람이 관리하는 source of truth이고, `rubrics/generated/`는 runtime에서 읽기 쉽게 합친 build output이다.

---

## 5. Legacy / Generated 평가 모드

Rubric bank 경로는 `rubric_bank_paths.py`에서 선택한다.

```text
RUBRIC_BANK_MODE=generated
  → rubrics/generated/*.generated.json 사용

RUBRIC_BANK_MODE=legacy
  → 기존 industrial_instrumentation_control.json 사용
```

운영 원칙:

```text
기본 평가:
  generated topic bank

기존 전체 범위 fallback:
  RUBRIC_BANK_MODE=legacy

topic pack 개발/검증:
  generated와 legacy를 smoke에서 비교
```

확인:

```bash
python3 scripts/check_rubric_bank_paths.py
RUBRIC_BANK_MODE=generated python3 scripts/check_rubric_bank_paths.py
RUBRIC_BANK_MODE=legacy python3 scripts/check_rubric_bank_paths.py
```

---

## 6. 문서별 책임 범위

### 6.1 채점 구조 문서

`grading_architecture.md`는 A/B/C/D/E layer의 의미, 배점, rater profile 연결을 관리한다.

이 문서에는 다음 내용을 둔다.

- A/B/C/D/E layer별 평가 기준
- 교수, 기술사, 기업 임원 rater 관점
- score cap과 postprocess의 위치
- Logic Check와 scoring model의 경계

---

### 6.2 Question Type 문서

`question_type_taxonomy.md`는 active question type과 legacy type mapping을 관리한다.

이 문서에는 다음 내용을 둔다.

- 4개 active question type
- 10개 legacy type mapping
- DEFINE과 STRUCTURE의 처리 기준
- C/D 평가 방향 보정 방식

`docs/README.md`에는 question type 표 전체를 반복하지 않는다.

---

### 6.3 Rubric 작성 문서

`rubric_authoring_guide.md`는 rubric JSON과 topic pack source를 작성할 때의 공통 원칙을 관리한다.

이 문서에는 다음 내용을 둔다.

- Model Answer source 작성 기준
- Fact Anchor source 작성 기준
- Topic Importance source 작성 기준
- Logic Check source 작성 기준
- 표, 다이어그램, 수식, ASCII 그림에서 claim을 추출하는 기준
- Fact Anchor와 Logic Check의 경계

---

### 6.4 Topic Pack Workflow 문서

`topic_pack_workflow.md`는 새 topic을 추가하거나 기존 topic을 보강할 때의 절차를 관리한다.

이 문서에는 다음 내용을 둔다.

- `README.md` 작성 기준
- `README.md`에서 Topic Sheet 후보 생성
- 사람이 Topic Sheet 검토
- Topic Sheet에서 schema-locked JSON candidate 생성
- generated bank promote
- smoke / Telegram 재채점 확인
- commit 전 확인 절차

---

### 6.5 Logic Check 문서

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

---

## 7. Topic Sheet와 Topic Pack 문서 관계

| 문서/파일 | 역할 |
|---|---|
| `rubrics/topic_packs/<topic_id>/README.md` | 사람이 topic 의도와 검토 메모를 남기는 설명서 |
| `docs/topic_sheets/<topic_id>.md` | JSON 생성을 위한 구조화된 Markdown input |
| `rubrics/topic_packs/<topic_id>/*.json` | 사람이 검토한 source JSON |
| `rubrics/generated/*.generated.json` | runtime용 build output |

README에서 JSON으로 바로 가지 않는다.

```text
README.md
  → Topic Sheet 후보
  → 사람 검토
  → schema-locked JSON candidate
  → generated promote
```

이 흐름을 문서화하는 기준 파일은 `topic_pack_workflow.md`이다.

---

## 8. 표와 다이어그램 관련 문서 기준

표, 다이어그램, ASCII 그림, s-plane 그림, block diagram, 수식 전개는 문서상 다음 기준으로 다룬다.

| 대상 | 주 문서 | 보조 문서 |
|---|---|---|
| Fact Anchor에서 evidence로 인정하는 기준 | `rubric_authoring_guide.md` | `topic_pack_workflow.md` |
| Logic Check에서 fatal/warn으로 보는 기준 | `rubric_authoring_guide.md` | `logic_check_profiles_readme.md` |
| LLM verifier profile에 넣을 truth/safe condition | `logic_check_profiles_readme.md` | `logic_check_profile_generator_prompt.md` |
| regex 기반 rule 후보 | `logic_check_json_generator_prompt.md` | `rubric_authoring_guide.md` |

원칙:

- 표/다이어그램 자체가 정답 또는 오답은 아니다.
- 표/다이어그램에서 읽히는 claim이 평가 대상이다.
- Fact Anchor는 올바른 claim coverage를 인정한다.
- Logic Check는 정답과 충돌하는 claim을 fatal/warn으로 판단한다.
- 그림 위치만으로 fatal 처리하지 않는다.
- 라벨, 본문 설명, 수식, 표의 mapping이 함께 충돌할 때 fatal 후보가 된다.

---

## 9. 문서 변경 후 검증

문서만 수정했을 때:

```bash
cd ~/hermes/workspace/prof_eng_answer

git diff --check
git diff --stat
git status --short
```

Rubric 또는 Topic Pack 문서를 수정했을 때:

```bash
python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_manager.py validate-topic-pack-quality
python3 scripts/rubric_manager.py validate-topic-pack-release
git diff --check
```

Logic Check 관련 문서를 수정했을 때:

```bash
python3 scripts/validate_logic_check_de_policy.py
python3 scripts/check_logic_check_de_claim_trust_regression.py
python3 scripts/validate_logic_check_bank.py
git diff --check
```

Topic Pack generated 결과까지 확인할 때:

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated
python3 scripts/rubric_manager.py smoke-topic-pack --topic-id <topic_id>
```

---

## 10. 중복 방지 규칙

1. 루트 README에는 빠른 실행과 전체 구조 요약만 둔다.
2. docs README에는 문서 목록과 문서별 책임 범위만 둔다.
3. 세부 표와 긴 정책 설명은 전용 문서에 둔다.
4. 같은 표를 README와 docs README에 동시에 길게 유지하지 않는다.
5. 검증 명령은 목적별 최소 명령만 둔다.
6. 오래된 D/E 직접 평가 구조나 deprecated prompt 표현은 다시 넣지 않는다.
7. README와 docs README는 append 방식으로 누적하지 않고 필요 시 완전 재작성한다.
