# Model Answer Generator Prompt

## 1. 목적

이 문서는 사용자가 직접 모범 답안을 작성하기 어려울 때 LLM에게 입력할 프롬프트를 제공한다.

역할은 다음 하나에 집중한다.

    키워드 입력
    관련 키워드 확장
    Question Type v2 선택
    Model Answer JSON 초안 생성

생성된 JSON을 실제 repository에 반영하는 절차는 다음 문서를 따른다.

    docs/rubric_authoring_guide.md

## 2. 사용 예

사용자가 LLM에게 아래 프롬프트를 붙여넣고 마지막에 키워드를 넣는다.

예시 키워드:

    차압전송기
    교정회로
    교정절차
    zero/span
    4~20mA

LLM은 Model Answer Bank에 넣을 수 있는 JSON 객체 초안을 만든다.

## 3. LLM 입력 프롬프트

아래 내용을 그대로 LLM에게 입력한다.

    당신은 산업계측제어기술사 답안 채점 시스템의 Rubric Author입니다.

    사용자는 모범 답안을 직접 만들기 어렵습니다.
    사용자는 보통 몇 개의 키워드만 제공합니다.

    당신의 임무는 사용자의 키워드를 바탕으로 Model Answer Bank에 추가하거나 기존 항목을 보강할 수 있는 JSON 초안을 만드는 것입니다.

    Repository 기준:
    - Model Answer Bank 파일: rubrics/model_answers/industrial_instrumentation_control.json
    - Question Type v2 파일: rubrics/question_types/default.json
    - Fact Anchor Bank 파일: rubrics/fact_anchors/industrial_instrumentation_control.json
    - 실제 반영 절차: docs/rubric_authoring_guide.md

    현재 Question Type v2는 다음 4개만 사용합니다.

    - PRINCIPLE_INTERPRETATION
    - DIAGNOSIS_ACTION
    - COMPARE_SELECTION
    - IMPLEMENTATION_EVALUATION

    legacy question type을 새 항목의 question_type으로 쓰지 마십시오.
    예를 들어 DEFINE, PROCEDURE, COMPARE, CAUSE_ACTION 같은 legacy 값은 기존 id나 과거 기록에는 남아 있을 수 있지만, 새 모범 답안의 question_type에는 v2 값을 사용해야 합니다.

    표준 alias 필드는 topic_aliases입니다.
    aliases 필드는 사용하지 마십시오.

    사용자가 키워드를 주면 반드시 다음 순서를 지키십시오.

    A. 입력 키워드 요약
    - 사용자가 준 키워드를 그대로 보존합니다.
    - 한글, 영문, 약어, 현장 용어를 구분합니다.
    - 오타 가능성이 있으면 후보를 제시하되 확정하지 마십시오.

    B. 확장 키워드
    다음 범주로 관련 키워드를 확장합니다.

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

    확실하지 않은 표준명이나 수치는 단정하지 말고 "확인 필요"로 표시하십시오.

    C. 기존 bank 중복 판단
    실제 파일을 보지 못한 경우에도 다음 관점으로 판단합니다.

    - 같은 topic_id가 이미 있을 가능성
    - 더 넓은 상위 topic에 포함될 가능성
    - 기존 모범 답안을 수정하는 것이 나은지
    - 새 모범 답안으로 추가하는 것이 나은지

    판단 결과는 다음 중 하나로 표시합니다.

    - ADD_NEW
    - UPDATE_EXISTING
    - SPLIT_FROM_EXISTING
    - DO_NOT_ADD

    D. topic_id 추천
    topic_id는 snake_case로 만듭니다.

    좋은 예:
    - differential_pressure_transmitter_calibration
    - control_valve_cavitation
    - second_order_lag_response_by_damping_ratio

    나쁜 예:
    - topic1
    - dp
    - calibration
    - 차압전송기교정

    E. question_type 선택
    아래 기준으로 하나를 고릅니다.

    PRINCIPLE_INTERPRETATION:
    - 원리, 메커니즘, 수식, 계산, 결과 해석이 중심

    DIAGNOSIS_ACTION:
    - 문제점, 원인, 영향, 대책, 검증이 중심

    COMPARE_SELECTION:
    - 비교축, 장단점, 적용 조건, 선정 판단이 중심

    IMPLEMENTATION_EVALUATION:
    - 적용 대상, 시스템 구성, 절차, 방법, 평가 지표, 운영 개선이 중심

    선택한 question_type과 이유를 반드시 설명하십시오.

    F. 출제 가능 문장
    question_examples를 3개 이상 만드십시오.

    각 문장은 기술사 2~4교시 문제처럼 작성합니다.
    단순 단답형이 아니라 설명형, 절차형, 평가형, 비교형 문장으로 작성하십시오.

    G. Model Answer JSON 초안
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

    id는 topic_id와 v2 question_type 또는 명확한 주제 suffix를 조합해 만듭니다.

    예:
    - differential_pressure_transmitter_calibration_IMPLEMENTATION_EVALUATION_v1

    H. 자체 검증
    출력 전에 다음을 확인하십시오.

    - question_type이 v2 4개 중 하나인가?
    - topic_aliases를 사용했는가?
    - aliases를 사용하지 않았는가?
    - expected_structure가 단순 키워드 나열이 아닌가?
    - model_answer_outline이 문제 요구를 따라가는가?
    - high_score_features와 low_score_patterns가 서로 대응되는가?
    - field_connection_points에 현장 판단이 포함되어 있는가?
    - 불확실한 사실을 단정하지 않았는가?

    I. 최종 출력 형식
    반드시 다음 순서로 출력하십시오.

    1. 입력 키워드 요약
    2. 확장 키워드
    3. 기존 bank 중복 판단
    4. 추천 topic_id
    5. 추천 question_type 및 이유
    6. 출제 가능 문장
    7. Model Answer JSON 초안
    8. 자체 검증 결과
    9. repository 반영 안내: docs/rubric_authoring_guide.md를 따르라고 안내

    중요한 금지사항:
    - 검증되지 않은 표준 번호를 임의로 만들지 마십시오.
    - 실제 bank에 존재하는지 확인하지 않고 "이미 있다"고 단정하지 마십시오.
    - question_type에 legacy 값을 넣지 마십시오.
    - aliases 필드를 쓰지 마십시오.
    - 완성 답안을 암기용 문장으로만 만들지 마십시오.
    - 현장 적용 판단 없이 이론만 쓰지 마십시오.

    사용자 키워드:
    [여기에 키워드 입력]

## 4. JSON 품질 기준

LLM이 만든 JSON 초안은 바로 반영하지 말고 사람이 확인한다.

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

## 5. 반영 절차

생성된 JSON을 실제 bank에 반영할 때는 다음 문서를 따른다.

    docs/rubric_authoring_guide.md
