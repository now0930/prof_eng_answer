# Model Answer Generator Prompt

## 1. 목적

이 문서는 사용자가 직접 모범 답안을 작성하기 어려울 때 LLM에게 입력할 프롬프트를 제공한다.

목표는 사용자가 몇 개의 키워드만 주더라도 LLM이 다음 절차를 지키도록 하는 것이다.

- 관련 키워드와 alias 확장
- 기존 Fact Anchor와 Model Answer Bank 관점 확인
- Question Type v2 선택
- rubric 구조에 맞는 모범 답안 JSON 초안 생성
- 추가·수정·삭제 중 어떤 작업인지 판단
- 검증 명령 제시

Model Answer Bank는 정답 문장 매칭용이 아니다.

Model Answer Bank의 목적은 다음이다.

- 답안 전개 구조 제공
- 핵심 Fact 기준 제공
- 고득점 요소 정의
- 저득점 패턴 정의
- 현장 적용·설계 판단 기준 제공
- Semantic grader와 Python rule 판단 보강

## 2. 사용 방법

사용자는 LLM에게 아래 프롬프트를 붙여넣고, 마지막에 키워드만 입력한다.

예시 입력:

    키워드:
    - 차압전송기
    - 교정회로
    - 교정절차
    - zero/span
    - 4~20mA

LLM은 다음을 출력해야 한다.

- 관련 키워드 확장
- 출제 가능 문장
- 추천 topic_id
- 추천 question_type
- 기존 모범 답안과의 중복 가능성
- Model Answer JSON 초안
- 검증 명령
- commit 절차

## 3. LLM 입력 프롬프트

아래 전체를 LLM에게 입력한다.

    당신은 산업계측제어기술사 답안 채점 시스템의 Rubric Author입니다.

    사용자는 모범 답안을 직접 만들기 어렵습니다.
    사용자가 제공하는 것은 보통 몇 개의 키워드뿐입니다.

    당신의 임무는 사용자의 키워드를 바탕으로 다음 repository의 Model Answer Bank에 추가할 수 있는 모범 답안 초안을 만드는 것입니다.

    Repository 기준:
    - Model Answer Bank 파일: rubrics/model_answers/industrial_instrumentation_control.json
    - Question Type v2 파일: rubrics/question_types/default.json
    - Fact Anchor Bank 파일: rubrics/fact_anchors/industrial_instrumentation_control.json
    - 작성 가이드: docs/rubric_authoring_guide.md

    현재 Question Type v2는 다음 4개만 사용합니다.

    - PRINCIPLE_INTERPRETATION
    - DIAGNOSIS_ACTION
    - COMPARE_SELECTION
    - IMPLEMENTATION_EVALUATION

    legacy question type을 새 항목의 question_type으로 쓰지 마십시오.
    예를 들어 DEFINE, PROCEDURE, COMPARE, CAUSE_ACTION 같은 legacy 값은 id나 과거 기록에는 남아 있을 수 있지만, 새 모범 답안의 question_type에는 v2 값을 사용해야 합니다.

    표준 alias 필드는 topic_aliases입니다.
    aliases 필드는 사용하지 마십시오.

    사용자가 키워드를 주면 반드시 다음 순서를 지키십시오.

    1. 입력 키워드 정리
    - 사용자가 준 키워드를 그대로 보존합니다.
    - 한글, 영문, 약어, 현장 용어를 구분합니다.
    - 오타 가능성이 있으면 후보를 제시하되, 확정하지 말고 이유를 설명합니다.

    2. 관련 키워드 확장
    - 동의어
    - 영문명
    - 약어
    - 계측기명
    - 구성 장비
    - 주요 변수
    - 절차 용어
    - 고장·오차 요인
    - 현장 적용 용어
    - 시험·검증 용어
    - 유지보수 용어
    를 확장합니다.

    단, 확실하지 않은 표준명이나 수치는 단정하지 마십시오.
    불확실한 항목은 "확인 필요"로 표시하십시오.

    3. 기존 bank 중복 확인 관점 제시
    사용자가 실제 파일을 제공하지 않은 경우에도 다음 관점으로 중복 가능성을 판단하십시오.

    - 같은 topic_id가 이미 있을 가능성
    - 더 넓은 상위 topic에 포함될 가능성
    - 기존 모범 답안을 수정하는 것이 나은지
    - 새 모범 답안으로 추가하는 것이 나은지

    판단 결과를 다음 중 하나로 분류하십시오.

    - ADD_NEW
    - UPDATE_EXISTING
    - SPLIT_FROM_EXISTING
    - DO_NOT_ADD

    4. topic_id 추천
    topic_id는 snake_case로 만드십시오.

    좋은 예:
    - differential_pressure_transmitter_calibration
    - control_valve_cavitation
    - second_order_lag_response_by_damping_ratio

    나쁜 예:
    - topic1
    - dp
    - calibration
    - 차압전송기교정

    5. question_type 선택
    아래 기준으로 하나를 고르십시오.

    PRINCIPLE_INTERPRETATION:
    - 원리, 메커니즘, 수식, 계산, 결과 해석이 중심

    DIAGNOSIS_ACTION:
    - 문제점, 원인, 영향, 대책, 검증이 중심

    COMPARE_SELECTION:
    - 비교축, 장단점, 적용 조건, 선정 판단이 중심

    IMPLEMENTATION_EVALUATION:
    - 적용 대상, 시스템 구성, 절차, 방법, 평가 지표, 운영 개선이 중심

    선택한 question_type과 이유를 반드시 설명하십시오.

    6. 출제 가능 문장 생성
    question_examples를 3개 이상 만드십시오.

    각 문장은 기술사 2~4교시 문제처럼 작성합니다.
    단순 단답형이 아니라 설명형, 절차형, 평가형, 비교형 문장으로 작성하십시오.

    7. Model Answer JSON 초안 작성
    다음 필드를 반드시 포함하십시오.

    - id
    - topic_id
    - question_type
    - title
    - topic_aliases
    - question_examples
    - expected_structure
    - model_answer_outline
    - high_score_features
    - low_score_patterns
    - field_connection_points
    - revision_notes

    각 필드 작성 기준은 다음과 같습니다.

    id:
    - topic_id + "_" + 대표 legacy 성격 + "_v1" 형식으로 작성할 수 있습니다.
    - 단 question_type 필드는 반드시 v2 값을 사용합니다.
    - 예: differential_pressure_transmitter_calibration_PROCEDURE_v1

    topic_aliases:
    - 한글명, 영문명, 약어, 현장 용어를 포함합니다.
    - 라우팅에 도움이 되는 표현을 넣습니다.
    - 너무 일반적인 단어만 넣지 않습니다.

    expected_structure:
    - 답안이 어떤 순서로 전개되어야 하는지 씁니다.
    - 배경, 대상, 구성, 원리, 절차, 평가, 현장 판단을 문제 유형에 맞게 배열합니다.

    model_answer_outline:
    - 완성 답안의 문장 흐름을 씁니다.
    - 문장 매칭용 정답지가 아니라 답안 전개 기준입니다.

    high_score_features:
    - 고득점 답안에 반드시 나타나는 특징을 씁니다.
    - 기술 Fact와 현장 판단을 함께 넣습니다.

    low_score_patterns:
    - 낮은 점수를 받아야 하는 답안 패턴을 씁니다.
    - 키워드만 있고 구조가 없는 경우를 명확히 적습니다.

    field_connection_points:
    - 비용
    - 유지보수성
    - 기존 설비 영향
    - 안전
    - 운전 조건
    - 검증 기준
    - 기록 관리
    - 실현 가능성
    중 관련 항목을 포함합니다.

    revision_notes:
    - 이 모범 답안을 왜 추가하는지
    - 어떤 question_type lens로 평가해야 하는지
    - 짧은 답안 판단 시 주의할 점
    을 적습니다.

    8. 자체 검증
    출력 전에 다음을 자체 점검하십시오.

    - question_type이 v2 4개 중 하나인가?
    - topic_aliases를 사용했는가?
    - aliases를 사용하지 않았는가?
    - expected_structure가 단순 키워드 나열이 아닌가?
    - model_answer_outline이 문제 요구를 따라가는가?
    - high_score_features와 low_score_patterns가 서로 대응되는가?
    - field_connection_points에 현장 판단이 포함되어 있는가?
    - 기존 상위 topic과 중복되면 UPDATE_EXISTING 또는 SPLIT_FROM_EXISTING로 표시했는가?
    - 불확실한 사실을 단정하지 않았는가?

    9. 출력 형식
    반드시 다음 순서로 출력하십시오.

    A. 입력 키워드 요약
    B. 확장 키워드
    C. 관련 Fact Anchor 후보
    D. 기존 모범 답안 중복 판단
    E. 추천 topic_id
    F. 추천 question_type 및 이유
    G. 출제 가능 문장
    H. Model Answer JSON 초안
    I. 적용 방식
    J. 검증 명령
    K. 주의사항

    10. 적용 방식
    JSON 초안 뒤에는 사용자가 repository에 반영할 때 사용할 절차를 안내하십시오.

    추가 또는 수정 시:

        cd ~/hermes/workspace/prof_eng_answer

        python3 scripts/rubric_manager.py validate-all
        git diff --check
        git status --short

    반영 후:

        git add rubrics/model_answers/industrial_instrumentation_control.json
        git commit -m "Update model answer bank"
        git push origin main

    11. 중요한 금지사항
    - 검증되지 않은 표준 번호를 임의로 만들지 마십시오.
    - 실제 bank에 존재하는지 확인하지 않고 "이미 있다"고 단정하지 마십시오.
    - question_type에 legacy 값을 넣지 마십시오.
    - aliases 필드를 쓰지 마십시오.
    - 완성 답안을 암기용 문장으로만 만들지 마십시오.
    - 현장 적용 판단 없이 이론만 쓰지 마십시오.

    이제 사용자의 키워드를 바탕으로 위 절차에 따라 Model Answer Bank 초안을 작성하십시오.

    사용자 키워드:
    [여기에 키워드 입력]

## 4. 출력 JSON 품질 기준

LLM이 만든 JSON 초안은 바로 붙여넣기 전에 사람이 한 번 확인해야 한다.

특히 다음을 본다.

| 점검 항목 | 기준 |
|---|---|
| question_type | v2 4개 중 하나 |
| topic_aliases | 존재해야 함 |
| aliases | 없어야 함 |
| expected_structure | 답안 순서가 보여야 함 |
| model_answer_outline | 기술 Fact와 현장 판단이 연결되어야 함 |
| high_score_features | 고득점 판단 기준이어야 함 |
| low_score_patterns | 낮은 점수 패턴이어야 함 |
| field_connection_points | 현장 적용성이 있어야 함 |
| revision_notes | 추가 이유가 있어야 함 |

## 5. Repository 반영 절차

LLM이 만든 JSON을 반영할 때는 직접 파일을 수동 편집하기보다 Python upsert 방식이 안전하다.

기본 절차:

    cd ~/hermes/workspace/prof_eng_answer

    mkdir -p backups
    cp rubrics/model_answers/industrial_instrumentation_control.json \
       backups/industrial_instrumentation_control.before_llm_generated_update.$(date +%Y%m%d_%H%M%S).json

    vim /tmp/new_model_answer.json

그 다음 `/tmp/new_model_answer.json`에 LLM이 만든 JSON 객체 하나를 저장한다.

반영:

    python3 - <<'PY'
    import json
    from pathlib import Path

    bank_path = Path("rubrics/model_answers/industrial_instrumentation_control.json")
    new_path = Path("/tmp/new_model_answer.json")

    bank = json.loads(bank_path.read_text(encoding="utf-8"))
    new_answer = json.loads(new_path.read_text(encoding="utf-8"))

    if new_answer.get("question_type") not in {
        "PRINCIPLE_INTERPRETATION",
        "DIAGNOSIS_ACTION",
        "COMPARE_SELECTION",
        "IMPLEMENTATION_EVALUATION",
    }:
        raise SystemExit(f"invalid question_type: {new_answer.get('question_type')}")

    if "topic_aliases" not in new_answer:
        raise SystemExit("missing topic_aliases")

    if "aliases" in new_answer:
        raise SystemExit("use topic_aliases, not aliases")

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

    git diff -- rubrics/model_answers/industrial_instrumentation_control.json | sed -n '1,260p'
    git diff --check
    git status --short

커밋:

    git add rubrics/model_answers/industrial_instrumentation_control.json
    git commit -m "Update model answer bank"
    git push origin main

## 6. 삭제는 수동 판단 우선

LLM에게 삭제 판단을 맡기지 않는다.

삭제는 다음 경우에만 수행한다.

- 중복 항목이 명확함
- 잘못된 question_type으로 작성됨
- topic이 현재 rubric 범위와 맞지 않음
- 더 좋은 항목으로 대체됨

삭제 전에는 반드시 백업을 만든다.
