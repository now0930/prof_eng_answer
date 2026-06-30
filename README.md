# prof_eng_answer

`prof_eng_answer`는 산업계측제어기술사 답안을 Telegram으로 입력받아, 기술사 시험 관점에서 채점하고 보완 방향을 제시하는 답안 평가 Bot이다.

이 프로젝트의 핵심 목적은 단순 키워드 매칭이 아니라 다음을 함께 평가하는 것이다.

- 문제 의도 파악
- 기술 Fact 설명 수준
- 현장 적용성
- 설계·운영 판단
- 답안 구조와 면접 방어 가능성
- Model Answer Bank와 Fact Anchor Bank 기준 충족 여부
- Question Type v2 lens 충족 여부
- 문항 난이도와 선택 전략

---

## 1. 현재 운영 기준

| 항목 | 기준 |
|---|---|
| Repository 위치 | `~/hermes/workspace/prof_eng_answer` |
| Compose 위치 | `~/hermes/docker-compose.yml` |
| Bot 컨테이너 | `prof_eng_answer_bot` |
| Bot 실행 방식 | `python -u bot.py` |
| 수동 `nohup` 실행 | 사용하지 않음 |
| LLM provider 기본 모드 | `auto` |
| Primary provider | `gemini` |
| Fallback provider | `clova` |
| 최종 Telegram 출력 정리 위치 | `send_message()` boundary |

운영 절차는 `docs/operation_runbook.md`를 우선한다.

---

## 2. 전체 채점 흐름

```text
Telegram /grade 입력
문제와 답안 파싱
LLM provider 선택
Gemini 또는 CLOVA semantic grader 실행
Python rule 기반 A/B/C/D/E 점수 후처리
3인 채점자 layer 평가 반영
Fact Anchor Bank 참조
Model Answer Bank 참조
Question Type v2 coverage 평가
Difficulty Profile과 ceiling 후보 계산
Telegram formatter 구성
send_message boundary cleanup
최종 채점 결과 출력
```

LLM 의미 평가는 최종 점수를 단독 결정하지 않는다. Python rule 후처리가 점수 범위, 답안 길이, Question Type coverage, Difficulty ceiling, fallback 처리, Telegram 출력 문구를 보정한다.

---

## 3. A/B/C/D/E 25점 채점 구조

총점은 25점이다.

| 항목 | 배점 | 평가 내용 |
|---|---:|---|
| A | 4 | 배경과 문제 진입 |
| B | 5 | 문제 요구 파악 |
| C | 8 | 유형별 Fact 기반 내용 설명 |
| D | 6 | 현장 적용·설계 판단·제언 |
| E | 2 | 연결성·면접 방어 가능성 |
| 합계 | 25 | 전체 답안 점수 |

| 기준 | 점수 |
|---|---:|
| 공식 합격선 | 15 |
| 실전 목표선 | 17.5 |
| 고득점 기준 | 20 |

---

## 4. 3인 채점자 layer

Bot은 하나의 답안을 3명 관점으로 나누어 본다.

| 채점자 | 주요 관점 |
|---|---|
| 교수 채점자 | 원리, 개념 정확성, 체계성, 이론적 설명 |
| 기술사 채점자 | 현장 절차, 적용 조건, 리스크, 검증 기준 |
| 기업 임원 채점자 | 비용, 유지보수성, 기존 설비 영향, 실현 가능성 |

A/B/C/D/E 항목마다 3인 layer의 영향은 다르다. C항목은 교수와 기술사 관점이 강하고, D항목은 기술사와 기업 임원 관점이 강하다.

---

## 5. Question Type v2

Question Type은 별도 점수체계가 아니다. A/B/C/D/E 점수체계를 대체하지 않고, C항목의 fact 전개 방향과 D항목의 현장 판단 방향을 정하는 lens이다.

현재 신규 항목에 사용하는 question type은 4개이다.

| question_type | 의미 | 흡수한 legacy type |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | `PRINCIPLE`, `CALC_DESIGN` |
| `DIAGNOSIS_ACTION` | 진단·대책형 | `PROBLEM_SOLVE`, `CAUSE_ACTION` |
| `COMPARE_SELECTION` | 비교·선정형 | `COMPARE`, `STRUCTURE` |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | `PROCEDURE`, `APPLICATION`, `EVALUATION`, `STRUCTURE` |

주의 사항:

- `DEFINE`은 신규 체계에서 사용하지 않는다.
- `STRUCTURE`는 독립 question type이 아니라 비교·선정형 또는 적용·평가형의 fact 설명 요소로 흡수한다.
- 기존 항목의 `legacy_question_type`은 migration 기록으로 남을 수 있다.
- 신규 `question_type` 값은 반드시 위 4개 중 하나여야 한다.

검증:

```bash
python3 scripts/validate_question_type_profile.py
```

---

## 6. 핵심 파일

| 구분 | 경로 | 역할 |
|---|---|---|
| Bot entrypoint | `bot.py` | Telegram Bot 실행 진입점 |
| LLM provider router | `llm_provider_router.py` | Gemini/CLOVA provider 선택 |
| Gemini grader | `gemini_grader.py` | Gemini semantic grading |
| CLOVA grader | `clova_grader.py` | CLOVA fallback grading |
| Question type router | `question_type_router.py` | 문제 유형 추론 |
| Model answer router | `model_answer_router.py` | Model Answer Bank 참조 |
| Rubric registry | `rubric_registry.py` | Rubric 파일 로딩 |
| Rubric manager | `scripts/rubric_manager.py` | Rubric 관리 CLI 진입점 |
| Model Answer Bank | `rubrics/model_answers/industrial_instrumentation_control.json` | topic/question_type별 모범답안 구조 |
| Fact Anchor Bank | `rubrics/fact_anchors/industrial_instrumentation_control.json` | topic별 핵심 fact 기준 |
| Question Type Profile | `rubrics/question_types/default.json` | v2 question type lens |

현재 GitHub 기준 Bank 규모:

| 항목 | 수량 |
|---|---:|
| model answers | 57 |
| model topics | 55 |
| fact topics | 55 |
| shared topics | 55 |

---

## 7. Model Answer Bank

본체 파일:

```bash
rubrics/model_answers/industrial_instrumentation_control.json
```

Model Answer Bank는 정답 문장 매칭용이 아니다. 역할은 다음이다.

- 답안 전개 구조 제공
- 핵심 Fact 기준 제공
- 고득점 요소 정의
- 저득점 패턴 정의
- 현장 적용·설계 판단 기준 제공
- Semantic grader와 Python rule 판단 보강

각 answer는 최소한 다음 필드를 갖는다.

| 필드 | 의미 |
|---|---|
| `id` | 모범답안 고유 ID |
| `topic_id` | 주제 식별자 |
| `question_type` | Question Type v2 |
| `title` | 사람이 읽는 제목 |
| `question_examples` | 출제 가능 문장 |
| `topic_aliases` | 검색·라우팅용 alias |
| `expected_structure` | 답안 전개 순서 |
| `model_answer_outline` | 모범 답안 흐름 |
| `high_score_features` | 고득점 요소 |
| `low_score_patterns` | 저득점 패턴 |
| `field_connection_points` | 현장 적용 포인트 |
| `revision_notes` | 작성 의도와 수정 이력 |
| `legacy_question_type` | 선택 필드. legacy migration 기록 |

목록 확인:

```bash
python3 scripts/rubric_manager.py list-model-answers
```

검증:

```bash
python3 scripts/validate_model_answer_bank.py
```

---

## 8. Fact Anchor Bank

본체 파일:

```bash
rubrics/fact_anchors/industrial_instrumentation_control.json
```

Fact Anchor Bank는 topic별로 반드시 확인해야 할 핵심 fact 기준이다. Model Answer보다 더 기초적인 factual 기준이며, 하나의 topic에 대해 여러 question type 모범답안이 이 기준을 공유할 수 있다.

각 topic은 최소한 다음 필드를 갖는다.

| 필드 | 의미 |
|---|---|
| `topic_id` | Model Answer와 연결되는 topic 식별자 |
| `name` | 사람이 읽는 topic 이름 |
| `triggers` | topic matching에 쓰는 핵심 표현 |
| `aliases` | 동의어, 약어, 현장 표현 |
| `anchors` | 핵심 fact anchor 목록 |

각 anchor는 최소한 다음 필드를 갖는다.

| 필드 | 의미 |
|---|---|
| `id` | anchor ID |
| `name` | anchor 이름 |
| `expected` | 반드시 설명해야 하는 fact |
| `core_terms` | 핵심 용어 |
| `support_terms` | 보조 용어 |

현재 `validate_fact_anchor_bank.py` 기준으로 topic별 `anchors`는 5개여야 한다.

검증:

```bash
python3 scripts/validate_fact_anchor_bank.py
```

---

## 9. Model Answer와 Fact Anchor의 topic 관계

두 Bank의 관계는 다음 원칙을 따른다.

```text
Fact Anchor = topic별 fact 기준
Model Answer = topic_id + question_type별 답안 구조
```

필수 관계:

- Model Answer의 모든 `topic_id`는 Fact Anchor Bank에 존재해야 한다.
- Fact Anchor의 `topic_id`는 중복되면 안 된다.
- Model Answer의 `id`는 중복되면 안 된다.
- 같은 `topic_id`를 여러 Model Answer가 공유할 수 있다.
- 같은 `topic_id`라도 `question_type` 또는 `legacy_question_type`이 다르면 별도 답안으로 둘 수 있다.

허용되는 관계:

```text
Fact Anchor topic 1개 : Model Answer 1개
Fact Anchor topic 1개 : Model Answer 여러 개
```

허용하지 않는 관계:

```text
Model Answer topic_id가 Fact Anchor Bank에 없음
Fact Anchor topic_id 중복
Model Answer id 중복
같은 topic_id + question_type + legacy_question_type 중복
빈 anchors
빈 model_answer_outline
빈 high_score_features
빈 low_score_patterns
```

정합성 검증:

```bash
python3 scripts/validate_model_fact_consistency.py
```

`validate_model_fact_consistency.py`가 없는 환경에서는 먼저 스크립트를 추가한 뒤 실행한다. 기본 검증만 할 때는 다음을 실행한다.

```bash
python3 scripts/rubric_manager.py validate-all
```

---

## 10. Model Answer 추가·수정·삭제 방법

### 10.1 기존 Model Answer 수정

1. `topic_id` 또는 `id`로 기존 answer를 찾는다.
2. `question_examples`, `expected_structure`, `model_answer_outline`, `high_score_features`, `low_score_patterns`, `field_connection_points`를 수정한다.
3. factual 내용은 반드시 같은 `topic_id`의 Fact Anchor와 모순되지 않게 한다.
4. 수정 후 검증한다.

```bash
python3 scripts/validate_model_answer_bank.py
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
git diff --check
```

### 10.2 신규 Model Answer 추가

1. 새 `topic_id`를 정한다.
2. 같은 `topic_id`가 Fact Anchor Bank에 있는지 먼저 확인한다.
3. 없으면 Fact Anchor를 먼저 추가한다.
4. Model Answer Bank에 answer를 추가한다.
5. `question_type`은 v2 4개 중 하나만 사용한다.
6. 같은 topic에 여러 출제 유형이 필요하면 같은 `topic_id`로 여러 Model Answer를 둘 수 있다.

ID 권장 형식:

```text
<topic_id>_<QUESTION_TYPE>_v1
```

legacy migration 항목이면 `legacy_question_type`을 별도로 남긴다.

### 10.3 Model Answer 삭제

1. 삭제 대상 `id`를 확인한다.
2. 같은 `topic_id`를 쓰는 다른 Model Answer가 남는지 확인한다.
3. 다른 Model Answer가 남으면 Fact Anchor는 유지한다.
4. 해당 topic의 Model Answer가 모두 없어지면 Fact Anchor 삭제 여부를 검토한다.
5. 삭제 후 검증한다.

---

## 11. Fact Anchor 추가·수정·삭제 방법

### 11.1 기존 Fact Anchor 수정

1. `topic_id`로 topic을 찾는다.
2. `anchors[].expected`에 반드시 설명해야 할 fact를 명확히 쓴다.
3. `core_terms`에는 채점에서 핵심으로 볼 용어를 둔다.
4. `support_terms`에는 보조 용어와 현장 표현을 둔다.
5. 같은 `topic_id`의 Model Answer와 충돌하지 않게 맞춘다.

검증:

```bash
python3 scripts/validate_fact_anchor_bank.py
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
```

### 11.2 신규 Fact Anchor 추가

1. Model Answer에 추가할 `topic_id`와 동일한 `topic_id`를 사용한다.
2. `name`, `triggers`, `aliases`를 작성한다.
3. `anchors`는 현재 검증 기준에 맞춰 5개 작성한다.
4. 각 anchor에는 `id`, `name`, `expected`, `core_terms`, `support_terms`를 채운다.
5. 그 다음 Model Answer를 추가한다.

### 11.3 Fact Anchor 삭제

1. 먼저 같은 `topic_id`를 사용하는 Model Answer가 남아 있는지 확인한다.
2. Model Answer가 남아 있으면 삭제하면 안 된다.
3. Model Answer가 모두 삭제된 topic만 Fact Anchor 삭제를 검토한다.
4. 삭제 후 정합성 검증을 실행한다.

---

## 12. Review Design Importer

batch별 검토 markdown은 보통 아래에 둔다.

```bash
wordpress_docs/review_designs/
```

실행 예:

```bash
python3 scripts/import_review_design.py wordpress_docs/review_designs/batch_014_design_1topic.md
```

주의 사항:

- `scripts/import_review_design.py` 내부에 topic별 `META`를 누적하지 않는다.
- 한글 metadata는 review design markdown 또는 JSON Bank에 둔다.
- importer는 변환 도구이며 기술적 사실 검증 도구가 아니다.
- import 후 반드시 Model Answer Bank, Fact Anchor Bank, topic 정합성을 검증한다.

검증:

```bash
python3 scripts/validate_model_answer_bank.py
python3 scripts/validate_fact_anchor_bank.py
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
```

---

## 13. 문서 구조

활성 문서:

| 문서 | 역할 |
|---|---|
| `docs/README.md` | docs 인덱스 |
| `docs/operation_runbook.md` | Bot 운영, 재시작, 장애 대응 |
| `docs/docker_compose_usage.md` | Docker Compose 기반 실행 방식 |
| `docs/grading_architecture.md` | A/B/C/D/E 채점 구조 |
| `docs/question_type_taxonomy.md` | Question Type v2 기준 |
| `docs/difficulty_and_selection_strategy.md` | 난이도와 문항 선택 전략 |
| `docs/llm_provider.md` | Gemini/CLOVA provider 설정 |
| `docs/rubric_authoring_guide.md` | Rubric Bank 작성과 수정 방법 |
| `docs/model_answer_generator_prompt.md` | Model Answer 초안 생성 프롬프트 |
| `docs/fact_anchor_generator_prompt.md` | Fact Anchor 초안 생성 프롬프트 |
| `docs/topic_importance_generator_prompt.md` | Topic importance 초안 생성 프롬프트 |

오래된 문서 정책:

- 현재 코드와 충돌하는 문서는 삭제하지 않고 `docs/archive/` 아래로 이동한다.
- `current_grading_architecture.md`, `docs/structure_review.md`, `docs/migration_plan.md`는 현재 기준 문서가 아니라 archive 후보로 본다.
- 충돌이 있을 때 우선순위는 현재 Python 코드, 현재 JSON Rubric Bank, `README.md`, `docs/README.md`, 세부 docs 순서이다.

---

## 14. 기본 검증 명령

전체 검증:

```bash
python3 scripts/rubric_manager.py validate-all
```

권장 검증:

```bash
python3 scripts/validate_question_type_profile.py
python3 scripts/validate_model_answer_bank.py
python3 scripts/validate_fact_anchor_bank.py
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
git diff --check
```

인코딩 깨짐 확인:

```bash
python3 scripts/scan_visible_mojibake.py README.md docs/*.md scripts/*.py rubrics/model_answers/industrial_instrumentation_control.json rubrics/fact_anchors/industrial_instrumentation_control.json || echo "OK: visible mojibake 없음"
```

---

## 15. Bot 반영

Rubric Bank를 Bot이 시작 시점에 읽고 캐시한다면 재시작이 필요할 수 있다.

```bash
cd ~/hermes
docker compose restart prof-eng-answer-bot
docker logs --tail=80 prof_eng_answer_bot
```

운영 점검은 `docs/operation_runbook.md`를 따른다.

---

## 16. Commit 절차

```bash
cd ~/hermes/workspace/prof_eng_answer

python3 scripts/validate_question_type_profile.py
python3 scripts/validate_model_answer_bank.py
python3 scripts/validate_fact_anchor_bank.py
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
git diff --check
git status --short

git add README.md docs scripts rubrics
git commit -m "Update README and rubric documentation"
git status --short
```

원격 반영 후 확인:

```bash
git push origin main
git fetch origin main
git rev-parse --short HEAD
git rev-parse --short origin/main
git status --short
```

정상 기준:

```text
HEAD == origin/main
git status --short 출력 없음
```
