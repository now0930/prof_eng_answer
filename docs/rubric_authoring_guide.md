# Rubric Authoring Guide

이 문서는 `prof_eng_answer`의 Rubric, Fact Anchor, Model Answer Bank를 repository에 안전하게 추가·수정·삭제하는 절차를 정리한다. LLM으로 초안을 만드는 방법은 generator prompt 문서를 사용하고, 이 문서는 **반영·검증·커밋 절차**를 담당한다.

## 1. 수정 대상 JSON

| 파일 | 역할 | 일반 수정 여부 |
|---|---|---|
| `rubrics/model_answers/industrial_instrumentation_control.json` | 주제별 Model Answer Bank | 수정 대상 |
| `rubrics/fact_anchors/industrial_instrumentation_control.json` | topic별 핵심 Fact Anchor | 수정 대상 |
| `rubrics/topic_importance/industrial_instrumentation_control.json` | 주제 중요도와 선택 전략 | 제한적 수정 |
| `rubrics/question_types/default.json` | Question Type v2 lens | 보통 수정하지 않음 |
| `rubrics/difficulty_profiles/default.json` | Difficulty Profile | 보통 수정하지 않음 |
| `rubrics/scoring_model/default.json` | A/B/C/D/E 배점과 cap rule | 정책 변경 시 수정 |
| `rubrics/raters/layered_default.json` | 3인 채점자 관점 | 정책 변경 시 수정 |

## 2. Question Type 기준

신규 Model Answer의 `question_type`은 다음 4개 중 하나만 사용한다.

| question_type | 의미 |
|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 |
| `DIAGNOSIS_ACTION` | 진단·대책형 |
| `COMPARE_SELECTION` | 비교·선정형 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 |

`DEFINE`, `PROCEDURE`, `COMPARE`, `CAUSE_ACTION` 같은 legacy 값은 신규 `question_type`으로 쓰지 않는다. 기존 migration 기록에는 `legacy_question_type`으로 남을 수 있다.

## 3. Model Answer Bank 원칙

Model Answer Bank는 정답 문장 매칭용이 아니다.

역할:

- 답안 전개 구조 제공
- 고득점 요소 정의
- 저득점 패턴 정의
- 현장 적용 포인트 제공
- semantic grader와 Python rule 판단 보강

본체 파일:

```text
rubrics/model_answers/industrial_instrumentation_control.json
```

표준 필드:

| 필드 | 의미 |
|---|---|
| `id` | 고유 ID |
| `topic_id` | 주제 식별자 |
| `question_type` | Question Type v2 |
| `title` | 사람이 읽는 제목 |
| `topic_aliases` | 검색·라우팅용 alias |
| `question_examples` | 출제 가능 문장 |
| `expected_structure` | 답안 전개 순서 |
| `model_answer_outline` | 모범 답안 흐름 |
| `high_score_features` | 고득점 요소 |
| `low_score_patterns` | 저득점 패턴 |
| `field_connection_points` | 현장 적용 포인트 |
| `revision_notes` | 작성 의도와 수정 이력 |
| `legacy_question_type` | migration 기록용 선택 필드 |

표준 alias 필드는 `topic_aliases`이다. 신규 항목에서 `aliases`를 쓰지 않는다.

## 4. Fact Anchor Bank 원칙

Fact Anchor는 topic별 핵심 fact 기준이다.

본체 파일:

```text
rubrics/fact_anchors/industrial_instrumentation_control.json
```

Topic 필드:

| 필드 | 의미 |
|---|---|
| `topic_id` | Model Answer와 연결되는 topic |
| `name` | 사람이 읽는 이름 |
| `triggers` | topic matching 핵심 표현 |
| `aliases` | 동의어, 약어, 현장 표현 |
| `anchors` | 핵심 fact anchor 목록 |

Anchor 필드:

| 필드 | 의미 |
|---|---|
| `id` | anchor ID |
| `name` | anchor 이름 |
| `expected` | 반드시 설명해야 하는 fact |
| `core_terms` | 핵심 용어 |
| `support_terms` | 보조 용어 |

현재 검증 기준상 topic별 anchor는 5개를 기준으로 한다.

## 5. Model Answer와 Fact Anchor 관계

```text
Fact Anchor = topic별 fact 기준
Model Answer = topic_id + question_type별 답안 구조
```

원칙:

- Model Answer의 모든 `topic_id`는 Fact Anchor Bank에 있어야 함
- Fact Anchor `topic_id`는 중복되면 안 됨
- Model Answer `id`는 중복되면 안 됨
- 같은 topic에 여러 question type Model Answer를 둘 수 있음
- 같은 topic의 Model Answer들은 같은 Fact Anchor를 공유할 수 있음

## 6. 신규 Model Answer 추가 절차

1. topic이 기존 Fact Anchor에 있는지 확인한다.
2. 없으면 Fact Anchor를 먼저 추가한다.
3. Model Answer JSON 초안을 만든다.
4. `question_type`이 v2 4개 중 하나인지 확인한다.
5. 필수 필드를 확인한다.
6. validate-all을 실행한다.
7. audit을 실행한다.

예시 검증:

```bash
cd ~/hermes/workspace/prof_eng_answer
python3 scripts/validate_model_answer_bank.py
python3 scripts/validate_fact_anchor_bank.py
python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_audit/run_rubric_audit.py
git diff --check
git status --short
```

## 7. 기존 Model Answer 수정

```bash
cd ~/hermes/workspace/prof_eng_answer
python3 scripts/rubric_manager.py list-model-answers
```

수정 원칙:

- `expected_structure`는 문제 요구 흐름과 맞춘다.
- `model_answer_outline`은 채점자가 기대하는 답안 흐름을 담는다.
- `high_score_features`는 과도하게 길게 늘리지 않는다.
- `low_score_patterns`에는 실제 저득점 위험을 적는다.
- factual 내용은 같은 topic의 Fact Anchor와 모순되면 안 된다.

수정 후:

```bash
python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_audit/run_rubric_audit.py
git diff --check
git status --short
```

## 8. 삭제 원칙

Model Answer 또는 Fact Anchor 삭제는 신중하게 한다.

삭제 가능한 경우:

- 중복 항목이 명확함
- 잘못된 question_type으로 작성됨
- topic이 현재 rubric 범위와 맞지 않음
- 더 좋은 항목으로 대체됨

Fact Anchor 삭제 전 확인:

- 같은 `topic_id`를 사용하는 Model Answer가 남아 있으면 삭제하지 않는다.
- Model Answer가 모두 삭제된 topic만 Fact Anchor 삭제를 검토한다.

## 9. Rubric audit

Rubric 변경 후에는 다음을 실행한다.

```bash
python3 scripts/rubric_audit/run_rubric_audit.py
```

통과 기준:

```text
Fact Anchor MAJOR = 0
Model Answer relationship MAJOR = 0
validate-all = OK
priority MINOR = 0
```

일반 `MINOR`는 advisory로 유지할 수 있다. `MINOR`를 0으로 만들기 위해 Model Answer를 과도하게 늘리거나 validator 점수에 과적합하지 않는다.

## 10. 커밋 절차

```bash
cd ~/hermes/workspace/prof_eng_answer
python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_audit/run_rubric_audit.py
git diff --check
git status --short

git add rubrics docs README.md scripts
git commit -m "Update rubric bank and documentation"
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

## 11. Bot 반영

Rubric Bank를 Bot이 시작 시점에 읽고 캐시한다면 재시작이 필요할 수 있다.

```bash
cd ~/hermes
docker compose restart prof-eng-answer-bot
docker logs --tail=80 prof_eng_answer_bot
```
