# 평가 기준과 유형별 모범 답안 작성 가이드

## 1. 기본 원칙

이 프로젝트의 채점 구조는 다음을 유지한다.

- A: 배경과 문제 진입
- B: 문제 요구 파악
- C: 유형별 Fact 기반 내용 설명
- D: 현장 적용·설계 판단·제언
- E: 연결성·면접 방어 가능성

문제 유형은 별도 점수 체계가 아니라 C항목을 평가하는 렌즈이다.

## 2. JSON 역할

| 파일 | 역할 |
|---|---|
| `rubrics/question_types/default.json` | DEFINE, COMPARE, CALC_DESIGN 등 문제 유형별 C항목 평가 렌즈 |
| `rubrics/fact_anchors/industrial_instrumentation_control.json` | 주제별 핵심 Fact Anchor |
| `rubrics/model_answers/industrial_instrumentation_control.json` | 주제 + 문제유형별 기준 답안 |
| `rubrics/originality/default.json` | 독창성·기술사적 판단성 평가 기준 |
| `rubrics/scoring_model/default.json` | A/B/C/D/E 배점 구조 |

## 3. 모범 답안 작성 원칙

모범 답안은 정답 문장 매칭용이 아니다.

좋은 모범 답안은 다음을 포함해야 한다.

1. 문제 유형에 맞는 C항목 전개 방식
2. 반드시 들어갈 핵심 Fact
3. 현장 적용 의미
4. 설계 판단 또는 제언
5. 저득점 패턴
6. 현장 연결 포인트

## 4. 새 모범 답안 추가 절차

예시: Cv 비교형 모범 답안 초안 생성

```bash
python3 scripts/rubric_manager.py new-model-answer \
  --topic-id cv_valve_flow_coefficient \
  --question-type COMPARE \
  --title "Cv 비교·선정형 모범 답안" \
  --question "Cv와 Kv를 비교하고 적용 기준을 설명하시오." \
  --alias "Cv" \
  --alias "Kv" \
  --field "밸브 사이징" \
  --field "제조사 data"
```

주의: 실제 터미널에서 실행할 때도 마지막 줄에는 `\`를 붙이지 않는다.

생성된 candidate를 편집한다.

```bash
vim rubrics/model_answers/candidates/cv_valve_flow_coefficient_COMPARE_v1.json
```

검증 후 승격한다.

```bash
python3 scripts/rubric_manager.py promote-model-answer \
  --candidate rubrics/model_answers/candidates/cv_valve_flow_coefficient_COMPARE_v1.json

python3 scripts/rubric_manager.py validate-all
```

## 5. question_type 선택 기준

| 유형 | C항목에서 보는 것 |
|---|---|
| DEFINE | 정의, 핵심 개념, 적용 범위, 한계, 실무 의미 |
| PRINCIPLE | 발생 조건, 원리, 메커니즘, 인과관계, 결과 현상 |
| STRUCTURE | 구성요소, 분류 기준, 계층 구조, 역할 관계 |
| COMPARE | 비교 대상, 비교축, 장단점, 적용 조건, 선정 기준 |
| PROBLEM_SOLVE | 문제 현상, 요구 파악, 원인, 개선 방향, 한계 |
| CAUSE_ACTION | 직접 원인, 근본 원인, 발생 메커니즘, 원인별 대책 |
| PROCEDURE | 절차 순서, 입력 자료, 수행 방법, 판단 기준, 산출물 |
| CALC_DESIGN | 공식, 변수, 단위, 계산 과정, 결과 해석, 설계 기준 |
| APPLICATION | 적용 대상, 적용 조건, 제약, 적용 방식, 기대 효과 |
| EVALUATION | 평가 대상, 지표, 방법, before/after, 효과, 한계 |

## 6. 점검 명령

```bash
python3 scripts/rubric_manager.py list-types
python3 scripts/rubric_manager.py list-model-answers
python3 scripts/rubric_manager.py validate-all
```

<!-- MODEL_ANSWER_OPS_START -->
## Model Answer Bank 추가·수정·삭제 절차

Model Answer Bank는 기술사 답안을 문장 단위로 강제 매칭하기 위한 정답지가 아니다.

용도는 다음과 같다.

- 문제 유형별 답안 전개 구조 제공
- 고득점 답안의 Fact 기준 제공
- 저득점 패턴 식별
- 현장 적용성, 유지보수성, 검증 기준 평가
- Semantic grader와 Python rule의 판단 근거 보강

현재 기본 bank 파일은 다음이다.

    rubrics/model_answers/industrial_instrumentation_control.json

현재 목록 확인:

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/rubric_manager.py list-model-answers

특정 topic만 확인:

    python3 scripts/rubric_manager.py list-model-answers \
      | grep -i 'differential\|차압\|calibration' || true

전체 검증:

    python3 scripts/rubric_manager.py validate-all

### 1. 추가 원칙

새 모범 답안은 다음 기준으로 추가한다.

| 항목 | 기준 |
|---|---|
| `id` | 고유해야 함 |
| `topic_id` | Fact Anchor 또는 문제 주제와 연결되는 식별자 |
| `question_type` | Question Type v2 값 사용 |
| `title` | 사람이 읽을 수 있는 제목 |
| `topic_aliases` | 검색·라우팅에 사용할 alias |
| `question_examples` | 대표 출제 문장 |
| `expected_structure` | 답안에 포함되어야 할 구조 |
| `model_answer_outline` | 모범 답안 전개 흐름 |
| `high_score_features` | 고득점 요소 |
| `low_score_patterns` | 저득점 패턴 |
| `field_connection_points` | 현장 적용·설계 판단 포인트 |
| `revision_notes` | 작성 의도와 평가 주의사항 |

Question Type v2 값은 다음 중 하나를 사용한다.

    PRINCIPLE_INTERPRETATION
    DIAGNOSIS_ACTION
    COMPARE_SELECTION
    IMPLEMENTATION_EVALUATION

예를 들어 차압전송기 교정회로와 교정절차 문제는 보통 다음처럼 둔다.

    question_type: IMPLEMENTATION_EVALUATION

### 2. 새 모범 답안 추가

가장 안전한 방식은 Python으로 JSON을 읽고, 같은 `id`가 있으면 교체하고 없으면 추가하는 upsert 방식이다.

예시:

    cd ~/hermes/workspace/prof_eng_answer

    mkdir -p backups
    cp rubrics/model_answers/industrial_instrumentation_control.json \
       backups/industrial_instrumentation_control.before_update.$(date +%Y%m%d_%H%M%S).json

    python3 - <<'PY'
    import json
    from pathlib import Path

    p = Path("rubrics/model_answers/industrial_instrumentation_control.json")
    bank = json.loads(p.read_text(encoding="utf-8"))

    new_answer = {
        "id": "example_topic_IMPLEMENTATION_EVALUATION_v1",
        "topic_id": "example_topic",
        "question_type": "IMPLEMENTATION_EVALUATION",
        "title": "예시 모범 답안",
        "topic_aliases": [
            "예시",
            "example"
        ],
        "question_examples": [
            "예시 문제를 설명하시오."
        ],
        "expected_structure": [
            "배경을 제시한다.",
            "대상과 범위를 정의한다.",
            "시스템 구성 또는 절차를 설명한다.",
            "평가 기준과 현장 적용 조건을 제시한다."
        ],
        "model_answer_outline": [
            "문제 배경을 설명한다.",
            "핵심 구성과 절차를 설명한다.",
            "현장 적용 시 유의사항을 설명한다.",
            "판정 기준과 유지보수 관점을 제시한다."
        ],
        "high_score_features": [
            "문제 요구와 답안 구조가 일치한다.",
            "핵심 Fact와 현장 판단이 함께 제시된다."
        ],
        "low_score_patterns": [
            "정의만 쓰고 절차나 평가 기준이 없다.",
            "현장 적용 조건이 없다."
        ],
        "field_connection_points": [
            "기존 설비와의 연계성을 검토한다.",
            "비용, 유지보수성, 검증 방법을 고려한다."
        ],
        "revision_notes": [
            "새 모범 답안 작성 예시이다."
        ]
    }

    answers = bank.setdefault("answers", [])
    answers[:] = [a for a in answers if a.get("id") != new_answer["id"]]
    answers.append(new_answer)

    p.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("upserted:", new_answer["id"])
    PY

추가 후 반드시 검증한다.

    python3 scripts/rubric_manager.py validate-all

    python3 scripts/rubric_manager.py list-model-answers \
      | grep -i 'example_topic\|예시' || true

    git diff -- rubrics/model_answers/industrial_instrumentation_control.json | sed -n '1,260p'
    git diff --check
    git status --short

### 3. 기존 모범 답안 수정

수정할 항목을 먼저 찾는다.

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/rubric_manager.py list-model-answers

    python3 - <<'PY'
    import json
    from pathlib import Path

    p = Path("rubrics/model_answers/industrial_instrumentation_control.json")
    bank = json.loads(p.read_text(encoding="utf-8"))

    target_id = "differential_pressure_transmitter_calibration_PROCEDURE_v1"

    for item in bank.get("answers", []):
        if item.get("id") == target_id:
            print(json.dumps(item, ensure_ascii=False, indent=2))
            break
    else:
        raise SystemExit(f"not found: {target_id}")
    PY

필드를 수정할 때도 Python upsert 방식으로 처리한다.

    python3 - <<'PY'
    import json
    from pathlib import Path

    p = Path("rubrics/model_answers/industrial_instrumentation_control.json")
    bank = json.loads(p.read_text(encoding="utf-8"))

    target_id = "differential_pressure_transmitter_calibration_PROCEDURE_v1"

    for item in bank.get("answers", []):
        if item.get("id") == target_id:
            item.setdefault("revision_notes", []).append(
                "수정 이력: 현장 적용 판단 기준을 보강함."
            )
            item.setdefault("high_score_features", []).append(
                "교정 전후 제어 loop 영향과 alarm/interlock bypass 여부를 검토한다."
            )
            break
    else:
        raise SystemExit(f"not found: {target_id}")

    p.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated:", target_id)
    PY

수정 후 검증한다.

    python3 scripts/rubric_manager.py validate-all
    git diff --check
    git status --short

### 4. 기존 모범 답안 삭제

삭제는 신중하게 한다.

삭제 전에 반드시 백업과 diff 확인을 수행한다.

    cd ~/hermes/workspace/prof_eng_answer

    mkdir -p backups
    cp rubrics/model_answers/industrial_instrumentation_control.json \
       backups/industrial_instrumentation_control.before_delete.$(date +%Y%m%d_%H%M%S).json

삭제할 id를 확인한다.

    python3 scripts/rubric_manager.py list-model-answers

삭제한다.

    python3 - <<'PY'
    import json
    from pathlib import Path

    p = Path("rubrics/model_answers/industrial_instrumentation_control.json")
    bank = json.loads(p.read_text(encoding="utf-8"))

    target_id = "example_topic_IMPLEMENTATION_EVALUATION_v1"

    answers = bank.get("answers", [])
    before = len(answers)
    answers = [a for a in answers if a.get("id") != target_id]
    after = len(answers)

    if before == after:
        raise SystemExit(f"not found: {target_id}")

    bank["answers"] = answers
    p.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("deleted:", target_id)
    print("before:", before)
    print("after:", after)
    PY

삭제 후 검증한다.

    python3 scripts/rubric_manager.py validate-all

    python3 scripts/rubric_manager.py list-model-answers \
      | grep -i 'example_topic' || true

    git diff --check
    git status --short

### 5. alias 관리

모범 답안 alias는 `topic_aliases`를 표준 필드로 사용한다.

권장:

    "topic_aliases": [
      "차압전송기",
      "DP transmitter",
      "differential pressure transmitter",
      "교정회로",
      "교정절차"
    ]

비권장:

    "aliases": [
      "차압전송기"
    ]

호환성 때문에 일부 코드가 `aliases`를 fallback으로 읽을 수는 있지만, bank에는 `topic_aliases`로 저장한다.

### 6. 커밋 절차

검증이 끝나면 커밋한다.

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

### 7. Bot 반영

Model Answer Bank를 프로세스 시작 시 읽고 캐시하는 구조라면 Bot 재시작이 필요할 수 있다.

    cd ~/hermes

    docker compose restart prof-eng-answer-bot
    docker logs --tail=80 prof_eng_answer_bot

문서만 수정한 경우 재시작은 필요 없다.

<!-- MODEL_ANSWER_OPS_END -->
