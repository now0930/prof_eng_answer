# Docs Index

이 문서: `README.md`

이 디렉터리는 `prof_eng_answer`의 운영, 채점 구조, Question Type, Difficulty, Rubric JSON Bank 관리 문서를 정리한다.

문서는 두 종류로 구분한다.

| 구분 | 의미 |
|---|---|
| 코드 연계 문서 | 현재 Python 코드, JSON 설정, CLI 명령과 직접 연결되는 문서 |
| 구조 참고 문서 | 현재 동작을 직접 설명하지는 않지만, migration 이력이나 전체 구조 이해에 도움이 되는 문서 |

## 1. 현재 운영 기준

| 항목 | 기준 |
|---|---|
| Telegram Bot 실행 주체 | `prof_eng_answer_bot` |
| Compose 위치 | `~/hermes/docker-compose.yml` |
| Repository 위치 | `~/hermes/workspace/prof_eng_answer` |
| Bot 실행 방식 | `python -u bot.py` |
| 수동 nohup 실행 | 사용하지 않음 |
| LLM 기본 모드 | `auto` |
| Question Type coverage | `warn` 기본 |
| Difficulty ceiling | `warn` 기본 |

## 2. 코드 연계 핵심 문서

| 문서 | 코드·JSON 근거 | 목적 |
|---|---|---|
| `operation_runbook.md` | `bot.py`, Docker Compose, 로그 확인 명령 | 운영 점검, 재시작, 장애 대응 |
| `docker_compose_usage.md` | `docker-compose.yaml`, `docker-compose.example.yml`, `scripts/run_prof_eng_bot.sh` | Docker Compose 운영 방식 |
| `grading_architecture.md` | `grading_agents.py`, `grading_config.py`, `rubrics/scoring_model/default.json`, `rubrics/raters/layered_default.json` | A/B/C/D/E 25점 채점 구조와 pipeline |
| `question_type_taxonomy.md` | `question_type_taxonomy.py`, `question_type_output_adapter.py`, `question_type_coverage_adapter.py`, `rubrics/question_types/default.json` | Question Type v2 taxonomy, sub criteria, coverage |
| `difficulty_and_selection_strategy.md` | `difficulty_strategy.py`, `difficulty_output_adapter.py`, `difficulty_score_ceiling.py`, `rubrics/difficulty_profiles/default.json`, `rubrics/topic_importance/industrial_instrumentation_control.json`, `rubrics/exam_selection/default.json` | Difficulty Profile, ceiling, 문항 선택 전략 |
| `llm_provider.md` | `llm_provider_router.py`, `llm_provider_settings.py`, `gemini_grader.py`, `clova_grader.py` | Gemini, CLOVA provider 설정 |
| `rubric_authoring_guide.md` | `rubric_registry.py`, `scripts/rubric_manager.py`, `rubrics/model_answers/industrial_instrumentation_control.json`, `rubrics/fact_anchors/industrial_instrumentation_control.json`, `rubrics/topic_importance/industrial_instrumentation_control.json` | Rubric JSON Bank 실제 수정·검증·커밋 절차 |

## 3. LLM 생성 프롬프트 문서

이 문서들은 코드가 직접 실행하는 문서가 아니다.  
사용자가 키워드를 입력했을 때 LLM으로 JSON 초안을 만들기 위한 작업 보조 문서이다.

| 문서 | 연결되는 JSON | 연결되는 CLI |
|---|---|---|
| `model_answer_generator_prompt.md` | `rubrics/model_answers/industrial_instrumentation_control.json` | `new-model-answer`, `promote-model-answer`, `validate-model-answers` |
| `fact_anchor_generator_prompt.md` | `rubrics/fact_anchors/industrial_instrumentation_control.json` | `new-fact-anchor-topic`, `promote-fact-anchor-topic`, `validate-fact-anchors` |
| `topic_importance_generator_prompt.md` | `rubrics/topic_importance/industrial_instrumentation_control.json` | `new-topic-importance`, `promote-topic-importance`, `validate-topic-importance` |

## 4. 구조 참고 문서

아래 문서는 현재 실행 코드와 1:1로 연결되는 active 문서가 아니다.  
다만 사용자가 전체 구조와 migration 흐름을 이해하는 데 도움이 되므로 reference 문서로 유지한다.

| 문서 | 유지 이유 |
|---|---|
| `migration_plan.md` | 구조 변경과 migration 기록 확인용 |
| `structure_review.md` | 과거 구조 검토와 설계 판단 흐름 확인용 |

이 두 문서는 현재 코드 기준과 다를 수 있으므로, 운영 판단은 핵심 문서를 우선한다.

## 5. 현재 채점 pipeline 요약

채점 구조는 다음 흐름을 따른다.

    Telegram /grade 입력
    문제와 답안 파싱
    Gemini 또는 CLOVA semantic grader 실행
    Python rule 기반 A/B/C/D/E 점수 후처리
    Question Type v2 coverage attach
    Difficulty Profile attach
    Telegram formatter 구성
    send_message boundary cleanup

## 6. 전체 Rubric JSON 관계도

채점 기준 JSON은 `rubrics/active_profile.json`을 중심으로 연결된다.

    rubrics/active_profile.json
    │
    ├─ scoring_model
    │  └─ rubrics/scoring_model/default.json
    │     ├─ A/B/C/D/E 25점 구조
    │     ├─ rater_weights_by_layer
    │     ├─ cap_rules
    │     └─ answer_sheet_volume_policy
    │
    ├─ subject_rubric
    │  └─ rubrics/subjects/industrial_instrumentation_control.json
    │     ├─ 시험 범위
    │     ├─ 답안 작성 구조
    │     ├─ keyword_groups
    │     ├─ demand_alignment_rules
    │     ├─ fact_anchor_bank 경로
    │     ├─ question_type_profile 경로
    │     └─ model_answer_bank 경로
    │
    ├─ rater_profile
    │  └─ rubrics/raters/layered_default.json
    │     ├─ professor
    │     ├─ professional_engineer
    │     └─ executive
    │
    └─ legacy_rubric
       └─ rubrics/default.json
          └─ 기존 코드 호환용

채점 중 직접 참조되는 주요 JSON은 다음과 같다.

    rubrics/question_types/default.json
    rubrics/fact_anchors/industrial_instrumentation_control.json
    rubrics/model_answers/industrial_instrumentation_control.json
    rubrics/topic_importance/industrial_instrumentation_control.json
    rubrics/difficulty_profiles/default.json
    rubrics/exam_selection/default.json
    rubrics/originality/default.json

## 7. JSON 문서 역할

| JSON | 역할 | 일반 사용자 수정 |
|---|---|---|
| `rubrics/model_answers/industrial_instrumentation_control.json` | Model Answer Bank. 답안 구조, 고득점 요소, 저득점 패턴, 현장 적용 포인트 | 수정 대상 |
| `rubrics/fact_anchors/industrial_instrumentation_control.json` | Fact Anchor Bank. topic별 핵심 fact, core term, support term | 수정 대상 |
| `rubrics/topic_importance/industrial_instrumentation_control.json` | Topic Importance. 난이도, 선택 중요도, score ceiling, 4문제 선택 전략 | 제한적 수정 대상 |
| `rubrics/question_types/default.json` | Question Type v2 4개 lens와 coverage 기준 | 보통 수정하지 않음 |
| `rubrics/difficulty_profiles/default.json` | Difficulty Profile 기본 정의 | 보통 수정하지 않음 |
| `rubrics/exam_selection/default.json` | 6문제 중 4문제 선택 전략 | 보통 수정하지 않음 |
| `rubrics/scoring_model/default.json` | A/B/C/D/E 배점, cap rule, rater weight | 정책 변경 시만 수정 |
| `rubrics/raters/layered_default.json` | 교수·기술사·기업 임원 관점 | 정책 변경 시만 수정 |
| `rubrics/active_profile.json` | active config root | 수정하지 않음 |
| `schemas/grade_schema.json` | grade output schema | 수정하지 않음 |
| `schemas/answer_structure_schema.json` | answer structure schema | 수정하지 않음 |

## 8. 사용자가 수정하는 3개 JSON의 관계

세 JSON은 같은 topic을 서로 다른 관점에서 설명한다.

    사용자 키워드
    │
    ├─ Model Answer Bank
    │  ├─ 답안 전개 구조
    │  ├─ model_answer_outline
    │  ├─ high_score_features
    │  ├─ low_score_patterns
    │  └─ field_connection_points
    │
    ├─ Fact Anchor Bank
    │  ├─ 핵심 fact 5개
    │  ├─ expected
    │  ├─ core_terms
    │  └─ support_terms
    │
    └─ Topic Importance
       ├─ difficulty
       ├─ selection_importance
       ├─ target_score
       ├─ excellent_score_band
       ├─ omission_risk
       └─ fatal_error_risk

운영 원칙은 다음이다.

| 상황 | 처리 |
|---|---|
| 새 주제의 답안 구조가 필요함 | Model Answer Bank 추가 |
| 새 주제의 핵심 fact 기준이 기존 anchor에 없음 | Fact Anchor Bank 추가 또는 수정 |
| 새 주제가 문항 선택 전략과 난이도 판단에 영향을 줌 | Topic Importance 추가 또는 수정 |
| 단순 세부 절차만 추가됨 | Model Answer만 수정하고 Fact Anchor/Topic Importance는 유지 가능 |
| 기존 topic 안에 흡수 가능함 | 새 topic을 만들지 않고 기존 JSON 수정 |

## 9. Rubric JSON Bank 관리 CLI

Model Answer Bank 관리:

    python3 scripts/rubric_manager.py list-model-answers
    python3 scripts/rubric_manager.py new-model-answer
    python3 scripts/rubric_manager.py promote-model-answer
    python3 scripts/rubric_manager.py delete-model-answer
    python3 scripts/rubric_manager.py validate-model-answers

Fact Anchor Bank 관리:

    python3 scripts/rubric_manager.py list-fact-anchors
    python3 scripts/rubric_manager.py new-fact-anchor-topic
    python3 scripts/rubric_manager.py promote-fact-anchor-topic
    python3 scripts/rubric_manager.py delete-fact-anchor-topic
    python3 scripts/rubric_manager.py validate-fact-anchors

Topic Importance 관리:

    python3 scripts/rubric_manager.py list-topic-importance
    python3 scripts/rubric_manager.py new-topic-importance
    python3 scripts/rubric_manager.py promote-topic-importance
    python3 scripts/rubric_manager.py delete-topic-importance
    python3 scripts/rubric_manager.py validate-topic-importance

전체 검증:

    python3 scripts/rubric_manager.py validate-all

## 10. CRUD 검증

추가·수정·삭제 스크립트는 실제 bank를 직접 건드리지 않고 임시 복사본에서 검증한다.

검증 스크립트:

    python3 scripts/test_rubric_content_crud.py

검증 내용:

| 대상 | 검증 |
|---|---|
| Model Answer Bank | add → update → delete → validate |
| Fact Anchor Bank | add → update → delete → validate |
| Topic Importance | add → update → delete → validate |

정상 기준:

    CRUD TESTS PASSED

## 11. LLM 프롬프트 사용법

사용자가 키워드만 줄 경우 다음 순서로 진행한다.

    1. Model Answer JSON 초안 생성
    2. Fact Anchor JSON 초안 필요 여부 검토
    3. Topic Importance JSON 초안 필요 여부 검토
    4. candidate JSON 생성
    5. 사람이 JSON 확인
    6. promote 명령으로 반영
    7. validate-all 실행
    8. commit

Model Answer 생성:

    model_answer_generator_prompt.md
    python3 scripts/rubric_manager.py new-model-answer ...
    python3 scripts/rubric_manager.py promote-model-answer --candidate <candidate> --replace
    python3 scripts/rubric_manager.py validate-model-answers

Fact Anchor 생성:

    fact_anchor_generator_prompt.md
    python3 scripts/rubric_manager.py new-fact-anchor-topic ...
    python3 scripts/rubric_manager.py promote-fact-anchor-topic --candidate <candidate> --replace
    python3 scripts/rubric_manager.py validate-fact-anchors

Topic Importance 생성:

    topic_importance_generator_prompt.md
    python3 scripts/rubric_manager.py new-topic-importance ...
    python3 scripts/rubric_manager.py promote-topic-importance --candidate <candidate> --replace
    python3 scripts/rubric_manager.py validate-topic-importance

## 12. Question Type v2 요약

현재 question type은 4개 lens로 정리한다.

| question_type | 의미 |
|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 |
| `DIAGNOSIS_ACTION` | 진단·대책형 |
| `COMPARE_SELECTION` | 비교·선정형 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 |

`DEFINE`은 독립 유형으로 사용하지 않고, legacy mapping을 통해 v2 유형으로 흡수한다.

## 13. Difficulty Profile 요약

| Profile | 의미 |
|---|---|
| `BASIC_CONCEPT` | 정의, 개념, 구성 중심 |
| `FIELD_APPLICATION` | 현장 적용, 선정, 개선방안 중심 |
| `DESIGN_EVALUATION` | 설계, 평가, 효과 분석 중심 |
| `THEORY_CORE` | 제어이론, 2차 시스템, 안정도 등 핵심 이론 |

Difficulty Profile은 A/B/C/D/E 점수를 대체하지 않는다.  
고득점 가능성, ceiling 후보, 문항 선택 전략을 설명하는 보조 lens이다.

## 14. 운영상 중요한 주의

`bot.py`는 운영 시 다음 방식으로 실행된다.

    python -u bot.py

파일 내부에서는 다음 흐름으로 진입한다.

    if __name__ == "__main__":
        main()

`main()` 내부에는 polling loop가 있으므로, 이 코드 아래쪽에 append한 wrapper는 실행되지 않는다.

따라서 최종 Telegram 출력 정리는 `send_message()` boundary에서 처리해야 한다.

## 15. 대표 smoke test

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

## 16. 문서/코드 정합성 검증

문서와 코드 설명이 맞는지 확인한다.

    cd ~/hermes/workspace/prof_eng_answer

    python3 scripts/audit_docs_against_code.py

전체 기능 검증:

    python3 -m py_compile \
      rubric_registry.py \
      scripts/rubric_manager.py \
      scripts/test_rubric_content_crud.py

    python3 scripts/test_rubric_content_crud.py
    python3 scripts/rubric_manager.py validate-all
    git diff --check
    git status --short

정상 기준:

    DOC AUDIT PASSED
    CRUD TESTS PASSED
    ALL VALID
