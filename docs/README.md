# Docs Index

이 문서: `README.md`

이 디렉터리는 `prof_eng_answer`의 운영, 채점 구조, question type, difficulty, rubric, JSON Bank 관리 문서를 정리한다.

현재 운영 기준은 다음과 같다.

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

## 1. 핵심 문서

| 문서 | 목적 |
|---|---|
| `operation_runbook.md` | 운영 점검, 재시작, 장애 대응 |
| `docker_compose_usage.md` | Docker Compose 운영 방식 |
| `grading_architecture.md` | A/B/C/D/E 25점 채점 구조와 pipeline |
| `question_type_taxonomy.md` | Question Type v2 taxonomy, sub criteria, coverage |
| `difficulty_and_selection_strategy.md` | Difficulty Profile, ceiling, 문항 선택 전략 |
| `llm_provider.md` | Gemini, CLOVA provider 설정 |
| `rubric_authoring_guide.md` | Rubric, Fact Anchor, Model Answer Bank 실제 수정·검증·커밋 절차 |

## 2. LLM 생성 프롬프트 문서

| 문서 | 목적 |
|---|---|
| `model_answer_generator_prompt.md` | 키워드만으로 Model Answer JSON 초안을 생성하는 LLM 프롬프트 |
| `fact_anchor_generator_prompt.md` | 키워드만으로 Fact Anchor JSON 초안을 생성하는 LLM 프롬프트 |
| `topic_importance_generator_prompt.md` | 키워드만으로 Topic Importance JSON 초안을 생성하는 LLM 프롬프트 |

## 3. 보조 문서

| 문서 | 성격 |
|---|---|
| `migration_plan.md` | 구조 변경 및 migration 기록 |
| `structure_review.md` | 과거 구조 검토 문서. 현재 기준과 다를 수 있음 |

## 4. 가장 먼저 볼 문서

운영 중 문제가 생기면 다음 순서로 확인한다.

    operation_runbook.md
    docker_compose_usage.md
    grading_architecture.md

Rubric 또는 JSON Bank를 수정할 때는 다음 순서로 확인한다.

    rubric_authoring_guide.md
    model_answer_generator_prompt.md
    fact_anchor_generator_prompt.md
    topic_importance_generator_prompt.md

## 5. 현재 채점 구조 요약

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

사용자가 주로 수정하는 파일은 다음 3개이다.

    Model Answer Bank
    Fact Anchor Bank
    Topic Importance

단, Topic Importance는 시험 선택 전략에 영향을 주므로 Model Answer보다 신중하게 수정한다.

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

## 9. Model Answer Bank 관리 함수

Model Answer Bank는 다음 CLI로 관리한다.

| 명령 | 역할 |
|---|---|
| `list-model-answers` | 현재 Model Answer 목록 확인 |
| `new-model-answer` | editable candidate JSON 생성 |
| `promote-model-answer` | candidate를 bank에 추가 또는 수정 |
| `delete-model-answer` | Model Answer 삭제 |
| `validate-model-answers` | Model Answer Bank 검증 |

예시:

    python3 scripts/rubric_manager.py list-model-answers

    python3 scripts/rubric_manager.py new-model-answer \
      --topic-id differential_pressure_transmitter_calibration \
      --question-type IMPLEMENTATION_EVALUATION \
      --title "차압전송기 교정회로와 교정절차 모범 답안" \
      --alias "차압전송기" \
      --alias "DP transmitter"

    python3 scripts/rubric_manager.py promote-model-answer \
      --candidate rubrics/content_candidates/model_answers/<candidate>.json \
      --replace

    python3 scripts/rubric_manager.py delete-model-answer \
      --id differential_pressure_transmitter_calibration_PROCEDURE_v1

    python3 scripts/rubric_manager.py validate-model-answers

Model Answer Bank의 고유키는 `id`이다.
`topic_id + question_type`은 검색·분류 기준이지 고유키가 아니다.

## 10. Fact Anchor Bank 관리 함수

Fact Anchor Bank는 다음 CLI로 관리한다.

| 명령 | 역할 |
|---|---|
| `list-fact-anchors` | Fact Anchor topic 목록 확인 |
| `new-fact-anchor-topic` | editable candidate JSON 생성 |
| `promote-fact-anchor-topic` | candidate를 bank에 추가 또는 수정 |
| `delete-fact-anchor-topic` | Fact Anchor topic 삭제 |
| `validate-fact-anchors` | Fact Anchor Bank 검증 |

예시:

    python3 scripts/rubric_manager.py list-fact-anchors

    python3 scripts/rubric_manager.py new-fact-anchor-topic \
      --topic-id differential_pressure_transmitter_calibration \
      --name "차압전송기 교정" \
      --alias "차압전송기" \
      --alias "DP transmitter"

    python3 scripts/rubric_manager.py promote-fact-anchor-topic \
      --candidate rubrics/content_candidates/fact_anchors/<candidate>.json \
      --replace

    python3 scripts/rubric_manager.py delete-fact-anchor-topic \
      --topic-id differential_pressure_transmitter_calibration

    python3 scripts/rubric_manager.py validate-fact-anchors

Fact Anchor topic은 `anchors` 5개를 가져야 한다.
각 anchor는 `id`, `name`, `expected`, `core_terms`, `support_terms`를 포함해야 한다.

## 11. Topic Importance 관리 함수

Topic Importance는 다음 CLI로 관리한다.

| 명령 | 역할 |
|---|---|
| `list-topic-importance` | Topic Importance 목록 확인 |
| `new-topic-importance` | editable candidate JSON 생성 |
| `promote-topic-importance` | candidate를 bank에 추가 또는 수정 |
| `delete-topic-importance` | Topic Importance 삭제 |
| `validate-topic-importance` | Topic Importance Bank 검증 |

예시:

    python3 scripts/rubric_manager.py list-topic-importance

    python3 scripts/rubric_manager.py new-topic-importance \
      --topic-id differential_pressure_transmitter_calibration \
      --label "차압전송기 교정" \
      --difficulty FIELD_APPLICATION \
      --selection-importance NORMAL \
      --alias "차압전송기" \
      --alias "DP transmitter"

    python3 scripts/rubric_manager.py promote-topic-importance \
      --candidate rubrics/content_candidates/topic_importance/<candidate>.json \
      --replace

    python3 scripts/rubric_manager.py delete-topic-importance \
      --topic-id differential_pressure_transmitter_calibration

    python3 scripts/rubric_manager.py validate-topic-importance

Topic Importance는 개별 답안 품질보다 시험 선택 전략과 난이도 판단에 가깝다.
따라서 새 Model Answer를 추가할 때마다 자동으로 추가하지 말고, 필요할 때만 별도 topic으로 관리한다.

## 12. CRUD 검증 함수

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

주의:

실제 운영 JSON이 변경되면 안 된다.

    rubrics/model_answers/industrial_instrumentation_control.json
    rubrics/fact_anchors/industrial_instrumentation_control.json
    rubrics/topic_importance/industrial_instrumentation_control.json

## 13. LLM 프롬프트 사용법

사용자가 키워드만 줄 경우, 다음 순서로 진행한다.

    1. Model Answer JSON 초안 생성
    2. Fact Anchor JSON 초안 필요 여부 검토
    3. Topic Importance JSON 초안 필요 여부 검토
    4. candidate JSON 생성
    5. 사람이 JSON 확인
    6. promote 명령으로 반영
    7. validate-all 실행
    8. commit

### 13.1 Model Answer 생성

사용 문서:

    model_answer_generator_prompt.md

사용 상황:

- 새 주제의 답안 구조가 필요함
- 고득점 요소와 저득점 패턴을 만들고 싶음
- 현장 적용 포인트를 답안 기준에 넣고 싶음

반영 CLI:

    python3 scripts/rubric_manager.py new-model-answer ...
    python3 scripts/rubric_manager.py promote-model-answer --candidate <candidate> --replace
    python3 scripts/rubric_manager.py validate-model-answers

### 13.2 Fact Anchor 생성

사용 문서:

    fact_anchor_generator_prompt.md

사용 상황:

- 새 topic의 핵심 fact 기준이 필요함
- 기존 Fact Anchor에 해당 주제의 core term이 부족함
- 답안에서 반드시 확인할 fact 기준을 만들고 싶음

반영 CLI:

    python3 scripts/rubric_manager.py new-fact-anchor-topic ...
    python3 scripts/rubric_manager.py promote-fact-anchor-topic --candidate <candidate> --replace
    python3 scripts/rubric_manager.py validate-fact-anchors

### 13.3 Topic Importance 생성

사용 문서:

    topic_importance_generator_prompt.md

사용 상황:

- 새 topic이 문항 선택 전략에 영향을 줌
- difficulty, target score, ceiling 판단이 필요함
- 회피 위험이나 치명 오답 위험을 관리해야 함

반영 CLI:

    python3 scripts/rubric_manager.py new-topic-importance ...
    python3 scripts/rubric_manager.py promote-topic-importance --candidate <candidate> --replace
    python3 scripts/rubric_manager.py validate-topic-importance

## 14. Question Type v2 요약

현재 question type은 4개 lens로 정리한다.

| question_type | 의미 |
|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 |
| `DIAGNOSIS_ACTION` | 진단·대책형 |
| `COMPARE_SELECTION` | 비교·선정형 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 |

`DEFINE`은 독립 유형으로 사용하지 않고, legacy mapping을 통해 v2 유형으로 흡수한다.

## 15. Difficulty Profile 요약

| Profile | 의미 |
|---|---|
| `BASIC_CONCEPT` | 정의, 개념, 구성 중심 |
| `FIELD_APPLICATION` | 현장 적용, 선정, 개선방안 중심 |
| `DESIGN_EVALUATION` | 설계, 평가, 효과 분석 중심 |
| `THEORY_CORE` | 제어이론, 2차 시스템, 안정도 등 핵심 이론 |

Difficulty Profile은 A/B/C/D/E 점수를 대체하지 않는다.
고득점 가능성, ceiling 후보, 문항 선택 전략을 설명하는 보조 lens이다.

## 16. 운영상 중요한 주의

`bot.py`는 운영 시 다음 방식으로 실행된다.

    python -u bot.py

파일 내부에서는 다음 흐름으로 진입한다.

    if __name__ == "__main__":
        main()

`main()` 내부에는 polling loop가 있으므로, 이 코드 아래쪽에 append한 wrapper는 실행되지 않는다.

따라서 최종 Telegram 출력 정리는 `send_message()` boundary에서 처리해야 한다.

## 17. 대표 smoke test

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

## 18. 전체 검증

    cd ~/hermes/workspace/prof_eng_answer

    python3 -m py_compile \
      rubric_registry.py \
      scripts/rubric_manager.py \
      scripts/test_rubric_content_crud.py

    python3 scripts/test_rubric_content_crud.py
    python3 scripts/rubric_manager.py validate-all
    git diff --check
    git status --short

정상 기준:

    CRUD TESTS PASSED
    ALL VALID

## 19. 문서 정합성 확인

README가 참조하는 docs 파일이 실제 존재하는지 확인한다.

    cd ~/hermes/workspace/prof_eng_answer

    echo "[README referenced docs]"
    grep -oE 'docs/[A-Za-z0-9_./-]+\.md' README.md | sort -u

    echo
    echo "[missing referenced docs]"
    for f in $(grep -oE 'docs/[A-Za-z0-9_./-]+\.md' README.md | sort -u); do
      [ -f "$f" ] || echo "MISSING: $f"
    done

docs README가 docs 디렉터리의 모든 문서를 설명하는지도 확인한다.

    echo
    echo "[docs files not mentioned in docs/README.md]"
    for f in $(find docs -maxdepth 1 -type f -name '*.md' -printf '%f\n' | sort); do
      grep -q "\`$f\`" docs/README.md || echo "MISSING_IN_DOCS_README: $f"
    done

정상 기준:

    MISSING 출력 없음
    MISSING_IN_DOCS_README 출력 없음

## Logic Check 운영 문서

- [Logic Check JSON Profile 운영 가이드](./logic_check_profiles_readme.md)
  - 표·도면·수식·비교 구조를 Model Answer / Fact Anchor / Logic Check에 나누어 반영하는 기준
  - 2차 감쇠비 문항의 잘못된 표와 S-평면 각도 오류 처리 기준
