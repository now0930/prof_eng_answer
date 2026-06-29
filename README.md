# prof_eng_answer

`prof_eng_answer`는 산업계측제어기술사 답안을 Telegram으로 입력받아, 기술사 시험 관점에서 채점하고 보완 방향을 제시하는 채점 Bot이다.

이 프로젝트의 핵심 목적은 단순 키워드 매칭이 아니라, 다음을 함께 평가하는 것이다.

- 문제 의도 파악
- 기술 Fact 설명 수준
- 현장 적용성
- 설계·운영 판단
- 답안 구조와 면접 방어 가능성
- 모범답안 Bank와 Fact Anchor 기준 충족 여부
- 문제 유형별 요구사항 충족 여부
- 문항 난이도와 선택 전략

## 1. 전체 기능 요약

Bot은 다음 흐름으로 동작한다.

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

운영 기준은 다음과 같다.

| 항목 | 기준 |
|---|---|
| Repository 위치 | `~/hermes/workspace/prof_eng_answer` |
| Compose 위치 | `~/hermes/docker-compose.yml` |
| Bot 컨테이너 | `prof_eng_answer_bot` |
| Bot 실행 방식 | `python -u bot.py` |
| 수동 nohup 실행 | 사용하지 않음 |
| Provider 기본 모드 | `auto` |
| Primary provider | `gemini` |
| Fallback provider | `clova` |
| 최종 출력 정리 위치 | `send_message()` boundary |

## 2. 채점 파이프라인

채점 파이프라인은 LLM 의미 평가와 Python rule 후처리를 결합한다.

### 2.1 입력

사용자는 Telegram에서 다음 형식으로 입력한다.

    /grade
    문제: 차압전송기의 교정회로와 교정절차를 설명하시오.

    답안:
    차압전송기는 기준 압력을 인가하고 4~20mA 출력을 확인하여 zero와 span을 조정한다.

Bot은 문제와 답안을 분리한 뒤, 문제 유형과 답안 길이, 핵심 키워드, 답안 구조를 분석한다.

### 2.2 LLM semantic grading

LLM은 답안의 의미를 평가한다.

주요 평가 내용은 다음과 같다.

- 문제 요구를 이해했는가
- 핵심 Fact가 포함되었는가
- 설명이 기술사 답안 수준인가
- 현장 적용성과 설계 판단이 있는가
- 답안 구조가 논리적으로 연결되는가
- Question Type v2 lens에 맞는 요구사항을 충족했는가

현재 provider 구조는 다음과 같다.

| Provider | 역할 |
|---|---|
| `gemini` | 기본 semantic grader |
| `clova` | fallback semantic grader |
| `auto` | Gemini 우선, 실패 시 CLOVA 사용 |

### 2.3 Python rule 후처리

LLM 결과는 그대로 최종 점수가 되지 않는다.

Python rule은 다음을 보정한다.

- A/B/C/D/E 점수 범위 정규화
- 너무 짧은 답안에 대한 volume cap
- Question Type coverage 보정 후보
- Difficulty ceiling 후보
- fallback coverage 처리
- Telegram 출력 문구 정리
- legacy GENERAL 문구 제거

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

점수 기준은 다음과 같다.

| 기준 | 점수 |
|---|---:|
| 공식 합격선 | 15점 |
| 실전 목표선 | 17.5점 |
| 고득점 기준 | 20점 |

## 4. 3인 채점자 layer

Bot은 하나의 답안을 3명 관점으로 나누어 평가한다.

| 채점자 | 주요 관점 |
|---|---|
| 교수 채점자 | 원리, 개념 정확성, 체계성, 이론적 설명 |
| 기술사 채점자 | 현장 절차, 적용 조건, 리스크, 검증 기준 |
| 기업 임원 채점자 | 비용, 유지보수성, 기존 설비 영향, 실현 가능성 |

A/B/C/D/E 항목마다 3인 layer의 영향이 다르다.

| 항목 | 교수 | 기술사 | 기업 임원 |
|---|---:|---:|---:|
| A. 배경과 문제 진입 | 0.3 | 0.4 | 0.3 |
| B. 문제 요구 파악 | 0.4 | 0.5 | 0.1 |
| C. Fact 기반 내용 설명 | 0.45 | 0.45 | 0.1 |
| D. 현장 적용·설계 판단 | 0.15 | 0.45 | 0.4 |
| E. 연결성·면접 방어 | 0.25 | 0.5 | 0.25 |

즉, C항목은 교수와 기술사 관점이 강하고, D항목은 기술사와 기업 임원 관점이 강하다.

## 5. 모범답안 Bank

모범답안은 정답 문장 매칭용이 아니다.

모범답안 Bank의 목적은 다음이다.

- 답안 전개 구조 제공
- 핵심 Fact 기준 제공
- 고득점 요소 정의
- 저득점 패턴 정의
- 현장 적용·설계 판단 기준 제공
- Semantic grader와 Python rule 판단 보강

모범답안 본체 파일은 다음이다.

    rubrics/model_answers/industrial_instrumentation_control.json

목록 확인:

    cd ~/hermes/workspace/prof_eng_answer
    python3 scripts/rubric_manager.py list-model-answers

전체 검증:

    python3 scripts/rubric_manager.py validate-all

현재 모범답안은 다음과 같은 구조를 가진다.

| 필드 | 의미 |
|---|---|
| `id` | 모범답안 고유 ID |
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

## 6. 모범답안 추가·수정·삭제

자세한 절차는 다음 문서에 있다.

    docs/rubric_authoring_guide.md

키워드만으로 LLM이 모범답안 초안을 만들게 하려면 다음 문서를 사용한다.

    docs/model_answer_generator_prompt.md

### 6.1 추가

새 모범답안은 Python upsert 방식으로 추가한다.

기본 절차:

    cd ~/hermes/workspace/prof_eng_answer

    mkdir -p backups
    cp rubrics/model_answers/industrial_instrumentation_control.json \
       backups/industrial_instrumentation_control.before_update.$(date +%Y%m%d_%H%M%S).json

    vim /tmp/new_model_answer.json

`/tmp/new_model_answer.json`에는 LLM이 생성한 JSON 객체 하나를 넣는다.

반영:

    python3 - <<'PY'
    import json
    from pathlib import Path

    bank_path = Path("rubrics/model_answers/industrial_instrumentation_control.json")
    new_path = Path("/tmp/new_model_answer.json")

    bank = json.loads(bank_path.read_text(encoding="utf-8"))
    new_answer = json.loads(new_path.read_text(encoding="utf-8"))

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

    valid_types = {
        "PRINCIPLE_INTERPRETATION",
        "DIAGNOSIS_ACTION",
        "COMPARE_SELECTION",
        "IMPLEMENTATION_EVALUATION",
    }

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

### 6.2 수정

수정은 같은 `id`로 upsert한다.

- 기존 항목을 조회한다.
- 필요한 필드를 수정한다.
- 같은 `id`로 저장한다.
- validate-all을 실행한다.

수정 전 조회:

    python3 scripts/rubric_manager.py list-model-answers

특정 항목 조회:

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

### 6.3 삭제

삭제는 LLM 판단만으로 수행하지 않는다.

삭제 가능한 경우는 다음이다.

- 중복 항목이 명확함
- 잘못된 question_type으로 작성됨
- topic이 현재 rubric 범위와 맞지 않음
- 더 좋은 항목으로 대체됨

삭제 전에는 반드시 백업을 만든다.

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

삭제 후 검증한다.

    python3 scripts/rubric_manager.py validate-all
    git diff --check
    git status --short

## 7. Fact Anchor Bank

Fact Anchor는 특정 주제에서 반드시 확인해야 할 핵심 개념과 기술 요소를 제공한다.

본체 파일은 다음이다.

    rubrics/fact_anchors/industrial_instrumentation_control.json

Fact Anchor는 모범답안과 다르다.

| 구분 | 역할 |
|---|---|
| Fact Anchor | 핵심 개념, 용어, 원리, 현장 키워드 기준 |
| Model Answer Bank | 답안 구조, 고득점 요소, 저득점 패턴 기준 |

## 8. Question Type v2

현재 새 모범답안의 `question_type`은 다음 4개 중 하나만 사용한다.

| question_type | 의미 |
|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 |
| `DIAGNOSIS_ACTION` | 진단·대책형 |
| `COMPARE_SELECTION` | 비교·선정형 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 |

legacy 유형은 새 항목의 `question_type`으로 직접 사용하지 않는다.

| legacy | v2 |
|---|---|
| `DEFINE` | `PRINCIPLE_INTERPRETATION` |
| `PRINCIPLE` | `PRINCIPLE_INTERPRETATION` |
| `CALC_DESIGN` | `PRINCIPLE_INTERPRETATION` |
| `CAUSE_ACTION` | `DIAGNOSIS_ACTION` |
| `PROBLEM_SOLVE` | `DIAGNOSIS_ACTION` |
| `COMPARE` | `COMPARE_SELECTION` |
| `PROCEDURE` | `IMPLEMENTATION_EVALUATION` |
| `APPLICATION` | `IMPLEMENTATION_EVALUATION` |
| `EVALUATION` | `IMPLEMENTATION_EVALUATION` |

## 9. Difficulty Profile과 ceiling

Difficulty Profile은 문제 자체의 고득점 가능성과 선택 전략을 설명하는 보조 lens이다.

| Profile | 의미 | 기본 ceiling |
|---|---|---:|
| `BASIC_CONCEPT` | 정의, 개념, 구성 중심 | 15.00 |
| `FIELD_APPLICATION` | 현장 적용, 선정, 개선방안 중심 | 15.75 |
| `DESIGN_EVALUATION` | 설계, 평가, 효과 분석 중심 | 16.50 |
| `THEORY_CORE` | 제어이론, 2차 시스템, 안정도 등 핵심 이론 | 17.50 |

기본 모드는 다음이다.

    DIFFICULTY_CEILING_MODE=warn

| 모드 | 의미 |
|---|---|
| `warn` | ceiling 후보만 표시하고 점수는 변경하지 않음 |
| `strict` | ceiling 초과 점수를 실제 제한 |
| `off` | ceiling 계산과 출력 비활성 |

## 10. 4문제 선택 전략

기술사 시험에서는 여러 문제 중 일부를 선택해 답안을 작성한다.
따라서 채점 점수와 문항 선택 전략을 분리해서 봐야 한다.

기본 전략은 다음과 같다.

| 문항 성격 | 선택 전략 |
|---|---|
| BASIC_CONCEPT | 안정 점수형. 고득점 ceiling은 낮음 |
| FIELD_APPLICATION | 실무 경험을 구조화하면 안정적으로 15점 접근 가능 |
| DESIGN_EVALUATION | 설계 기준과 평가 지표를 쓰면 중상위 점수 가능 |
| THEORY_CORE | 정확하면 고득점 가능하지만 오답 위험이 큼 |

4문제를 선택해야 한다면 다음 조합이 안정적이다.

| 조합 | 의미 |
|---|---|
| 안정형 2문제 | BASIC_CONCEPT 또는 FIELD_APPLICATION |
| 실무형 1문제 | FIELD_APPLICATION 또는 DESIGN_EVALUATION |
| 고득점 도전 1문제 | THEORY_CORE 또는 DESIGN_EVALUATION |

주의:

- 제어이론 문제를 선택했다는 사실만으로 가산점이 붙지는 않는다.
- 제어이론 문제를 정확히 풀면 고득점 band가 열린다.
- 제어이론 문제를 틀리면 감점 폭이 클 수 있다.
- 쉬운 문제도 현장 판단이 부족하면 합격선 근처에 머문다.

## 11. 대표 smoke test

Telegram에서 다음을 보낸다.

    /grade
    문제: 차압전송기의 교정회로와 교정절차를 설명하시오.

    답안:
    차압전송기는 기준 압력을 인가하고 4~20mA 출력을 확인하여 zero와 span을 조정한다.

정상 확인 기준:

- 채점 완료 메시지가 온다.
- `[Question Type Coverage]`가 출력된다.
- 문제 유형 lens가 `적용·평가형(IMPLEMENTATION_EVALUATION)`로 표시된다.
- `C항목 보완: 일반 설명형 유형에서는 ...` 문구가 없어야 한다.
- `C항목 보완: 문제 유형 lens에 맞는 핵심 fact...` 문구가 나와야 한다.

## 12. 문서

| 문서 | 목적 |
|---|---|
| `docs/README.md` | 문서 인덱스 |
| `docs/operation_runbook.md` | 운영 점검, 재시작, 장애 대응 |
| `docs/docker_compose_usage.md` | Docker Compose 운영 방식 |
| `docs/grading_architecture.md` | A/B/C/D/E 채점 구조와 pipeline |
| `docs/question_type_taxonomy.md` | Question Type v2 taxonomy와 coverage |
| `docs/difficulty_and_selection_strategy.md` | Difficulty Profile, ceiling, 문항 선택 전략 |
| `docs/llm_provider.md` | Gemini/CLOVA provider 설정 |
| `docs/rubric_authoring_guide.md` | Rubric, Fact Anchor, Model Answer 추가·수정·삭제 절차 |
| `docs/model_answer_generator_prompt.md` | 키워드 기반 Model Answer Bank 초안 생성 LLM 프롬프트 |
| `docs/migration_plan.md` | migration 기록 |
| `docs/structure_review.md` | 구조 검토 기록 |

## 13. 검증

코드와 rubric 검증:

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/rubric_manager.py validate-all

    python3 -m py_compile \
      bot.py \
      grading_agents.py \
      gemini_grader.py \
      clova_grader.py \
      difficulty_strategy.py \
      difficulty_output_adapter.py \
      difficulty_score_ceiling.py \
      question_type_taxonomy.py \
      question_type_coverage_adapter.py \
      question_type_coverage_score_adjuster.py \
      semantic_question_type_prompt.py \
      semantic_question_type_postprocess.py \
      scripts/validate_model_answer_bank.py

Markdown과 Git 상태 확인:

    git diff --check
    git status --short

## 14. 운영

Bot 상태 확인:

    cd ~/hermes
    docker compose ps prof-eng-answer-bot
    docker logs --tail=120 prof_eng_answer_bot

Bot 재시작:

    cd ~/hermes
    docker compose restart prof-eng-answer-bot

Model Answer Bank나 rubric 파일을 Bot이 시작 시점에 캐시한다면 재시작 후 테스트한다.
