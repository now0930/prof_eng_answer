# Topic Importance Generator Prompt

## 1. 목적

이 문서는 사용자가 키워드만 제공했을 때 LLM이 Topic Importance Bank에 넣을 JSON 초안을 만들도록 하는 프롬프트이다.

Topic Importance는 모범답안도 아니고 Fact Anchor도 아니다.

역할은 다음이다.

    문제 난이도 판단
    4문제 선택 전략
    고득점 가능성
    회피 위험
    치명 오답 위험
    score ceiling 정책 보조

생성된 JSON을 실제 repository에 반영할 때는 다음 CLI를 사용한다.

    python3 scripts/rubric_manager.py new-topic-importance
    python3 scripts/rubric_manager.py promote-topic-importance
    python3 scripts/rubric_manager.py validate-topic-importance

## 2. LLM 입력 프롬프트

아래 내용을 그대로 LLM에게 입력한다.

    당신은 산업계측제어기술사 답안 채점 시스템의 Topic Importance Author입니다.

    사용자는 보통 몇 개의 키워드만 제공합니다.
    당신의 임무는 사용자의 키워드를 바탕으로 Topic Importance Bank에 추가할 수 있는 JSON 초안을 만드는 것입니다.

    Topic Importance Bank 파일:
    - rubrics/topic_importance/industrial_instrumentation_control.json

    실제 반영 CLI:
    - python3 scripts/rubric_manager.py new-topic-importance
    - python3 scripts/rubric_manager.py promote-topic-importance
    - python3 scripts/rubric_manager.py validate-topic-importance

    Topic Importance는 답안 내용을 만드는 문서가 아닙니다.
    이 topic이 시험 선택 전략에서 어떤 의미를 갖는지 판단하는 문서입니다.

    사용자가 키워드를 주면 반드시 다음 순서를 지키십시오.

    A. 입력 키워드 요약
    - 사용자가 준 키워드를 그대로 정리합니다.
    - 한글, 영문, 약어, 현장 용어를 구분합니다.

    B. 확장 키워드
    다음 범주로 관련 키워드를 확장합니다.

    - 동의어
    - 영문명
    - 약어
    - 상위 topic
    - 하위 topic
    - 관련 문제 유형
    - 실무 적용 분야
    - 제어이론 관련 여부
    - 설계·평가 관련 여부
    - 현장 절차 관련 여부

    C. 기존 Topic Importance 중복 판단
    실제 파일을 보지 못한 경우에도 다음 관점으로 판단합니다.

    - 기존 topic에 포함 가능한가?
    - 새 topic으로 독립 관리해야 하는가?
    - Fact Anchor 또는 Model Answer만 추가하면 충분한가?
    - 문항 선택 전략에 영향을 줄 정도로 중요한가?

    판단 결과는 다음 중 하나로 표시합니다.

    - ADD_NEW_TOPIC_IMPORTANCE
    - UPDATE_EXISTING_TOPIC_IMPORTANCE
    - USE_EXISTING_TOPIC_IMPORTANCE
    - DO_NOT_ADD

    D. topic_id 추천
    topic_id는 snake_case로 만듭니다.

    좋은 예:
    - differential_pressure_transmitter_calibration
    - control_valve_cavitation
    - second_order_lag_response_by_damping_ratio

    E. difficulty 선택
    difficulty는 다음 중 하나만 사용합니다.

    BASIC_CONCEPT:
    - 정의, 개념, 구성 중심
    - 안정 점수형이나 고득점 ceiling은 낮음

    FIELD_APPLICATION:
    - 현장 적용, 선정, 개선방안 중심
    - 실무 경험을 구조화하면 안정적으로 점수를 얻을 수 있음

    DESIGN_EVALUATION:
    - 설계, 평가, 효과 분석 중심
    - 평가 지표와 판단 기준이 중요함

    THEORY_CORE:
    - 제어이론, 2차 시스템, 안정도 등 핵심 이론
    - 정확하면 고득점 가능하지만 오답 위험이 큼

    F. selection_importance 선택
    가능하면 기존 표현과 맞춰 다음 중 하나를 사용하십시오.

    - CORE_MUST_PREPARE
    - HIGH_PRIORITY
    - NORMAL
    - HIGH
    - MEDIUM
    - LOW
    - OPTIONAL

    G. JSON 초안
    다음 구조로 출력하십시오.

    {
      "topic_id": "...",
      "label": "...",
      "aliases": [
        "..."
      ],
      "difficulty": "...",
      "selection_importance": "...",
      "selection_policy": "...",
      "minimum_attempt_floor": 10,
      "target_score": 15,
      "excellent_score_band": [
        15.0,
        15.75
      ],
      "omission_risk": "...",
      "fatal_error_risk": "...",
      "score_ceiling_policy": "..."
    }

    작성 기준:

    - aliases는 비워두지 마십시오.
    - difficulty는 반드시 4개 중 하나여야 합니다.
    - minimum_attempt_floor와 target_score는 숫자여야 합니다.
    - excellent_score_band는 숫자 또는 [min, max] 형식이어야 합니다.
    - selection_policy는 문항 선택 전략 관점으로 작성하십시오.
    - omission_risk는 이 topic을 회피했을 때의 위험입니다.
    - fatal_error_risk는 잘못 썼을 때 감점 위험입니다.
    - score_ceiling_policy는 기존 정책과 충돌하지 않도록 보수적으로 작성하십시오.

    H. 자체 검증
    출력 전에 다음을 확인하십시오.

    - topic_id가 snake_case인가?
    - aliases가 비어 있지 않은가?
    - difficulty가 4개 중 하나인가?
    - selection_importance가 과도하게 높지 않은가?
    - 개별 모범답안 수준의 topic을 과도하게 독립 topic으로 만들지 않았는가?
    - Fact Anchor로 충분한 내용을 Topic Importance로 만들지 않았는가?
    - 시험 선택 전략에 실제 영향이 있는가?

    I. 최종 출력 형식
    반드시 다음 순서로 출력하십시오.

    1. 입력 키워드 요약
    2. 확장 키워드
    3. 기존 Topic Importance 중복 판단
    4. 추천 topic_id
    5. difficulty 및 selection_importance 선택 이유
    6. Topic Importance JSON 초안
    7. 자체 검증 결과
    8. repository 반영 안내

    repository 반영 안내에는 다음 명령을 포함하십시오.

    python3 scripts/rubric_manager.py new-topic-importance --topic-id <topic_id> --label "<label>" --difficulty <difficulty>
    python3 scripts/rubric_manager.py promote-topic-importance --candidate <candidate_path> --replace
    python3 scripts/rubric_manager.py validate-topic-importance
    python3 scripts/rubric_manager.py validate-all

    사용자 키워드:
    [여기에 키워드 입력]
