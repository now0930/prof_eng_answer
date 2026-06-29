# Rubric Authoring Guide

## 1. 목적

이 문서는 `prof_eng_answer`의 Rubric, Fact Anchor, Model Answer Bank를 실제 repository에 추가·수정·삭제하는 운영 절차를 정리한다.

키워드만으로 Model Answer JSON 초안을 만들고 싶다면 다음 문서를 사용한다.

    docs/model_answer_generator_prompt.md

이 문서는 LLM 프롬프트 문서가 아니라, 생성된 초안을 repository에 안전하게 반영하는 운영 문서이다.

## 2. 현재 기준 파일

| 파일 | 역할 |
|---|---|
| `rubrics/question_types/default.json` | Question Type v2 4개 lens와 C/D항목 coverage 기준 |
| `rubrics/fact_anchors/industrial_instrumentation_control.json` | 주제별 핵심 Fact Anchor |
| `rubrics/model_answers/industrial_instrumentation_control.json` | 주제별 Model Answer Bank |
| `rubrics/originality/default.json` | 독창성·기술사적 판단성 평가 기준 |
| `rubrics/scoring_model/default.json` | A/B/C/D/E 배점 구조 |

## 3. Question Type v2 기준

새 rubric 또는 model answer의 `question_type`은 다음 4개 중 하나만 사용한다.

| question_type | 의미 |
|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 |
| `DIAGNOSIS_ACTION` | 진단·대책형 |
| `COMPARE_SELECTION` | 비교·선정형 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 |

`DEFINE`, `PROCEDURE`, `COMPARE`, `CAUSE_ACTION` 같은 legacy 값은 새 항목의 `question_type`으로 쓰지 않는다. 기존 id나 migration 기록에는 남을 수 있지만, 신규 작성 기준은 v2 4개이다.

## 4. Model Answer Bank 원칙

Model Answer Bank는 정답 문장 매칭용이 아니다.

역할은 다음과 같다.

- 답안 전개 구조 제공
- 핵심 Fact 기준 제공
- 고득점 요소 정의
- 저득점 패턴 정의
- 현장 적용·설계 판단 기준 제공
- Semantic grader와 Python rule 판단 보강

본체 파일:

    rubrics/model_answers/industrial_instrumentation_control.json

목록 확인:

    cd ~/hermes/workspace/prof_eng_answer
    python3 scripts/rubric_manager.py list-model-answers

전체 검증:

    python3 scripts/rubric_manager.py validate-all

## 5. Model Answer 필드

새 Model Answer는 다음 필드를 갖는다.

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

표준 alias 필드는 `topic_aliases`이다. `aliases`는 쓰지 않는다.

## 6. 새 Model Answer 추가

LLM으로 JSON 초안을 만들 경우 먼저 다음 문서를 사용한다.

    docs/model_answer_generator_prompt.md

생성된 JSON 객체 하나를 `/tmp/new_model_answer.json`에 저장한 뒤 upsert한다.

    cd ~/hermes/workspace/prof_eng_answer

    mkdir -p backups
    cp rubrics/model_answers/industrial_instrumentation_control.json \
       backups/industrial_instrumentation_control.before_update.$(date +%Y%m%d_%H%M%S).json

    vim /tmp/new_model_answer.json

반영:

    python3 - <<'PY'
    import json
    from pathlib import Path

    bank_path = Path("rubrics/model_answers/industrial_instrumentation_control.json")
    new_path = Path("/tmp/new_model_answer.json")

    bank = json.loads(bank_path.read_text(encoding="utf-8"))
    new_answer = json.loads(new_path.read_text(encoding="utf-8"))

    valid_types = {
        "PRINCIPLE_INTERPRETATION",
        "DIAGNOSIS_ACTION",
        "COMPARE_SELECTION",
        "IMPLEMENTATION_EVALUATION",
    }

    required = [
        "id",
        "topic_id",
        "question_type",
        "title",
        "topic_aliases",
        "question_examples",
        "expected_structure",
        "model_answer_outline",
        "high_score_features",
        "low_score_patterns",
        "field_connection_points",
        "revision_notes",
    ]

    if new_answer.get("question_type") not in valid_types:
        raise SystemExit(f"invalid question_type: {new_answer.get('question_type')}")

    if "aliases" in new_answer:
        raise SystemExit("use topic_aliases, not aliases")

    missing = [key for key in required if key not in new_answer]
    if missing:
        raise SystemExit(f"missing keys: {missing}")

    answers = bank.setdefault("answers", [])
    before = len(answers)

    answers[:] = [a for a in answers if a.get("id") != new_answer["id"]]
    answers.append(new_answer)

    bank_path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("upserted:", new_answer["id"])
    print("before:", before)
    print("after:", len(answers))
    PY

검증:

    python3 scripts/rubric_manager.py validate-all
    python3 scripts/rubric_manager.py list-model-answers
    git diff --check
    git status --short

## 7. 기존 Model Answer 수정

수정은 같은 `id`로 upsert한다.

먼저 기존 항목을 확인한다.

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/rubric_manager.py list-model-answers

특정 항목 확인:

    python3 - <<'PY'
    import json
    from pathlib import Path

    target_id = "differential_pressure_transmitter_calibration_PROCEDURE_v1"

    bank = json.loads(Path("rubrics/model_answers/industrial_instrumentation_control.json").read_text(encoding="utf-8"))

    for item in bank.get("answers", []):
        if item.get("id") == target_id:
            print(json.dumps(item, ensure_ascii=False, indent=2))
            break
    else:
        raise SystemExit(f"not found: {target_id}")
    PY

수정 후에는 반드시 검증한다.

    python3 scripts/rubric_manager.py validate-all
    git diff --check
    git status --short

## 8. 기존 Model Answer 삭제

삭제는 신중하게 한다. LLM 판단만으로 삭제하지 않는다.

삭제 가능한 경우:

- 중복 항목이 명확함
- 잘못된 question_type으로 작성됨
- topic이 현재 rubric 범위와 맞지 않음
- 더 좋은 항목으로 대체됨

삭제 전 백업:

    cd ~/hermes/workspace/prof_eng_answer

    mkdir -p backups
    cp rubrics/model_answers/industrial_instrumentation_control.json \
       backups/industrial_instrumentation_control.before_delete.$(date +%Y%m%d_%H%M%S).json

삭제 예시:

    python3 - <<'PY'
    import json
    from pathlib import Path

    target_id = "example_topic_IMPLEMENTATION_EVALUATION_v1"

    p = Path("rubrics/model_answers/industrial_instrumentation_control.json")
    bank = json.loads(p.read_text(encoding="utf-8"))

    before = len(bank.get("answers", []))
    bank["answers"] = [a for a in bank.get("answers", []) if a.get("id") != target_id]
    after = len(bank["answers"])

    if before == after:
        raise SystemExit(f"not found: {target_id}")

    p.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("deleted:", target_id)
    print("before:", before)
    print("after:", after)
    PY

삭제 후 검증:

    python3 scripts/rubric_manager.py validate-all
    git diff --check
    git status --short

## 9. 커밋 절차

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/rubric_manager.py validate-all
    git diff --check
    git status --short

    git add rubrics/model_answers/industrial_instrumentation_control.json
    git commit -m "Update model answer bank"
    git push origin main

    git fetch origin main
    git rev-parse --short HEAD
    git rev-parse --short origin/main
    git status --short

정상 기준:

    HEAD == origin/main
    git status --short 출력 없음

## 10. Bot 반영

Model Answer Bank를 Bot이 시작 시점에 읽고 캐시한다면 재시작이 필요할 수 있다.

    cd ~/hermes

    docker compose restart prof-eng-answer-bot
    docker logs --tail=80 prof_eng_answer_bot
