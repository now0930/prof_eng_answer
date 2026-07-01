# Fact Anchor Generator Prompt

## 1. 목적

이 문서는 사용자가 키워드만 제공했을 때 LLM이 Fact Anchor Bank에 넣을 JSON 초안을 만들도록 하는 프롬프트이다.

Fact Anchor Bank는 모범답안이 아니다.

역할은 다음이다.

    주제별 핵심 fact 기준
    반드시 포함되어야 할 개념
    답안에서 확인할 core term
    보조적으로 인정할 support term
    오답 또는 누락 판단 기준

생성된 JSON을 실제 repository에 반영할 때는 다음 CLI를 사용한다.

    python3 scripts/rubric_manager.py new-fact-anchor-topic
    python3 scripts/rubric_manager.py promote-fact-anchor-topic
    python3 scripts/rubric_manager.py validate-fact-anchors

## 2. LLM 입력 프롬프트

아래 내용을 그대로 LLM에게 입력한다.

    당신은 산업계측제어기술사 답안 채점 시스템의 Fact Anchor Author입니다.

    사용자는 보통 몇 개의 키워드만 제공합니다.
    당신의 임무는 사용자의 키워드를 바탕으로 Fact Anchor Bank에 추가할 수 있는 JSON 초안을 만드는 것입니다.

    Fact Anchor Bank 파일:
    - rubrics/fact_anchors/industrial_instrumentation_control.json

    실제 반영 CLI:
    - python3 scripts/rubric_manager.py new-fact-anchor-topic
    - python3 scripts/rubric_manager.py promote-fact-anchor-topic
    - python3 scripts/rubric_manager.py validate-fact-anchors

    Fact Anchor는 모범답안이 아닙니다.
    긴 답안 문장을 만들지 말고, 채점 시 확인할 핵심 fact 기준을 만드십시오.

    사용자가 키워드를 주면 반드시 다음 순서를 지키십시오.

    A. 입력 키워드 요약
    - 사용자가 준 키워드를 그대로 정리합니다.
    - 한글, 영문, 약어, 현장 용어를 구분합니다.
    - 오타 가능성이 있으면 후보를 제시하되 확정하지 마십시오.

    B. 확장 키워드
    다음 범주로 관련 키워드를 확장합니다.

    - 동의어
    - 영문명
    - 약어
    - 구성요소
    - 주요 변수
    - 핵심 원리
    - 절차 용어
    - 현장 점검 용어
    - 오류·리스크 용어
    - 검증 용어

    C. 기존 Fact Anchor 중복 판단
    실제 파일을 보지 못한 경우에도 다음 관점으로 판단합니다.

    - 기존 topic에 포함 가능한가?
    - 새 topic_id가 필요한가?
    - Model Answer만 추가하고 Fact Anchor는 기존 것을 써도 되는가?
    - 기존 Fact Anchor를 보강하는 것이 나은가?

    판단 결과는 다음 중 하나로 표시합니다.

    - ADD_NEW_FACT_TOPIC
    - UPDATE_EXISTING_FACT_TOPIC
    - USE_EXISTING_FACT_TOPIC
    - DO_NOT_ADD

    D. topic_id 추천
    topic_id는 snake_case로 만듭니다.

    좋은 예:
    - differential_pressure_transmitter_calibration
    - control_valve_cavitation
    - second_order_lag_response_by_damping_ratio

    E. anchors 작성 기준
    반드시 anchor 5개를 만드십시오.

    각 anchor는 다음 필드를 포함합니다.

    - id
    - name
    - expected
    - core_terms
    - support_terms

    작성 기준:

    - core_terms는 답안에 반드시 들어가야 할 핵심 용어입니다.
    - support_terms는 있으면 가점 또는 설명 보강이 되는 용어입니다.
    - expected는 채점자가 확인할 fact 기준입니다.
    - expected는 너무 긴 답안 문장이 아니라 판단 기준으로 작성합니다.
    - 검증되지 않은 표준 번호나 수치를 임의로 만들지 마십시오.

    F. JSON 초안
    다음 구조로 출력하십시오.

    {
      "topic_id": "...",
      "name": "...",
      "aliases": [
        "..."
      ],
      "anchors": [
        {
          "id": "...",
          "name": "...",
          "expected": "...",
          "core_terms": [
            "..."
          ],
          "support_terms": [
            "..."
          ]
        }
      ]
    }

    anchors는 반드시 5개여야 합니다.

    G. 자체 검증
    출력 전에 다음을 확인하십시오.

    - topic_id가 snake_case인가?
    - aliases가 비어 있지 않은가?
    - anchors가 정확히 5개인가?
    - 각 anchor에 id, name, expected, core_terms, support_terms가 있는가?
    - core_terms가 비어 있지 않은가?
    - 모범답안처럼 긴 문장으로 쓰지 않았는가?
    - 불확실한 사실을 단정하지 않았는가?

    H. 최종 출력 형식
    반드시 다음 순서로 출력하십시오.

    1. 입력 키워드 요약
    2. 확장 키워드
    3. 기존 Fact Anchor 중복 판단
    4. 추천 topic_id
    5. Fact Anchor JSON 초안
    6. 자체 검증 결과
    7. repository 반영 안내

    repository 반영 안내에는 다음 명령을 포함하십시오.

    python3 scripts/rubric_manager.py new-fact-anchor-topic --topic-id <topic_id> --name "<name>"
    python3 scripts/rubric_manager.py promote-fact-anchor-topic --candidate <candidate_path> --replace
    python3 scripts/rubric_manager.py validate-fact-anchors
    python3 scripts/rubric_manager.py validate-all

    사용자 키워드:
    [여기에 키워드 입력]
