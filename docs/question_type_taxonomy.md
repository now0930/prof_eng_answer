# Question Type v2 Taxonomy

## 1. 목적

Question Type v2는 기술사 2~4교시 답안에 맞춰 C항목 Fact 전개와 D항목 현장 판단을 보강하기 위한 lens이다.

Question Type은 별도 점수 체계가 아니다.

즉, 다음을 직접 대체하지 않는다.

- A/B/C/D/E 25점 채점 구조
- Difficulty Profile
- Fact Anchor
- Model Answer Bank

Question Type v2는 문제 유형별로 C항목과 D항목에서 무엇을 더 봐야 하는지 정리하는 보조 평가축이다.

## 2. v2 설계 원칙

기술사 2~4교시 답안에서는 단답식 정의 문제가 거의 없다.

따라서 기존 `DEFINE`을 독립 유형으로 두지 않고, 다음 4개 대분류로 통합한다.

| question_type | 한국어명 | 핵심 평가 방향 |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | 원리, 메커니즘, 수식, 계산, 결과 해석 |
| `DIAGNOSIS_ACTION` | 진단·대책형 | 문제, 원인, 영향, 대책, 검증 |
| `COMPARE_SELECTION` | 비교·선정형 | 비교축, 장단점, 적용 조건, 선정 판단 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | 대상, 구성, 절차, 평가 지표, 운영 개선 |

## 3. Legacy mapping

기존 legacy question type은 내부 호환을 위해 v2로 mapping한다.

| legacy question_type | v2 question_type |
|---|---|
| `DEFINE` | `PRINCIPLE_INTERPRETATION` |
| `PRINCIPLE` | `PRINCIPLE_INTERPRETATION` |
| `CALC_DESIGN` | `PRINCIPLE_INTERPRETATION` |
| `PROBLEM_SOLVE` | `DIAGNOSIS_ACTION` |
| `CAUSE_ACTION` | `DIAGNOSIS_ACTION` |
| `COMPARE` | `COMPARE_SELECTION` |
| `PROCEDURE` | `IMPLEMENTATION_EVALUATION` |
| `APPLICATION` | `IMPLEMENTATION_EVALUATION` |
| `EVALUATION` | `IMPLEMENTATION_EVALUATION` |

`STRUCTURE`는 독립 유형으로 사용하지 않고, 문제 맥락에 따라 다음 중 하나로 흡수한다.

| STRUCTURE 성격 | mapping |
|---|---|
| 구성 요소·분류 중심 | `COMPARE_SELECTION` |
| 시스템 구성·절차·적용 중심 | `IMPLEMENTATION_EVALUATION` |
| 원리 설명을 위한 구조 | `PRINCIPLE_INTERPRETATION` |

## 4. PRINCIPLE_INTERPRETATION

원리·해석형은 대상의 동작 원리, 전달함수, 수식, 변수 의미, 계산 결과의 해석을 설명하는 문제에 사용한다.

대표 문제 신호:

- 원리를 설명하시오
- 전달함수를 구하시오
- 응답특성을 설명하시오
- 안정도와 감쇠비를 설명하시오
- 계산하시오
- 수식의 각 항을 설명하시오

Sub criteria:

    background_need
    structure_components
    principle_mechanism
    formula_model_variables
    calculation_or_interpretation
    result_meaning
    field_judgement

C항목 Fact focus:

- 원리와 메커니즘
- 구성 요소
- 수식, 변수, 단위
- 계산 또는 해석 과정
- 결과 의미

D항목 Field judgement focus:

- 현장 적용 시 해석상 주의점
- 설계 여유
- 운전 조건 변화 영향
- 측정·제어 안정성 판단

## 5. DIAGNOSIS_ACTION

진단·대책형은 문제점, 발생 원인, 영향, 대책, 우선순위, 검증 방법을 설명하는 문제에 사용한다.

대표 문제 신호:

- 원인과 대책
- 문제점과 개선방안
- 고장 원인
- 오차 발생 원인
- 방지 대책
- 개선 방법

Sub criteria:

    background_need
    problem_definition
    cause_mechanism
    impact_risk
    action_countermeasure
    feasibility_tradeoff
    priority_and_verification

C항목 Fact focus:

- 문제 정의
- 원인 메커니즘
- 영향과 리스크
- 대책의 기술적 근거

D항목 Field judgement focus:

- 우선순위
- 비용·효과
- 적용 가능성
- 검증 방법
- 재발 방지

## 6. COMPARE_SELECTION

비교·선정형은 두 개 이상의 기술, 방식, 장치, 제어 전략을 비교하고 적용 조건에 따라 선정하는 문제에 사용한다.

대표 문제 신호:

- 비교하시오
- 차이점을 설명하시오
- 장단점을 설명하시오
- 선정 기준을 제시하시오
- 적용 조건을 비교하시오

Sub criteria:

    background_need
    classification_axis
    structure_features
    comparison_axis
    pros_cons_limits
    application_conditions
    selection_judgement

C항목 Fact focus:

- 분류 기준
- 구조적 특징
- 비교축
- 장단점과 한계
- 적용 조건

D항목 Field judgement focus:

- 선정 판단
- 현장 조건별 적용성
- 비용·유지보수성
- 기존 설비와의 연계
- trade-off

## 7. IMPLEMENTATION_EVALUATION

적용·평가형은 시스템 구성, 절차, 방법, 적용 범위, 평가 지표, 운영 개선 효과를 설명하는 문제에 사용한다.

차압전송기 교정회로와 교정절차 문제는 보통 이 유형에 해당한다.

대표 문제 신호:

- 절차를 설명하시오
- 방법을 설명하시오
- 구성도를 설명하시오
- 적용 사례를 설명하시오
- 평가 방법을 설명하시오
- 교정 절차를 설명하시오

Sub criteria:

    background_need
    target_scope
    system_configuration
    procedure_method
    selection_criteria
    evaluation_metrics
    operation_improvement_judgement

C항목 Fact focus:

- 적용 대상
- 시스템 구성
- 절차와 방법
- 선정 기준
- 평가 지표

D항목 Field judgement focus:

- 기존 설비와의 연계
- 적용 조건
- 비용·효과
- 운영 리스크
- 유지보수성
- 적용 후 검증 방법
- 개선 효과와 한계

## 8. Detector 우선순위

Question Type detector는 복합 신호가 있을 때 다음 우선순위를 사용한다.

    DIAGNOSIS_ACTION
    COMPARE_SELECTION
    IMPLEMENTATION_EVALUATION
    PRINCIPLE_INTERPRETATION

명확한 문제·대책, 비교, 적용 신호가 없으면 기본 fallback은 `PRINCIPLE_INTERPRETATION`이다.

단, 시스템 구성도, 절차, 교정, 시험, 평가, 적용 사례 중심이면 `IMPLEMENTATION_EVALUATION`을 우선한다.

## 9. Compound signal 예시

| 문제 표현 | 우선 type |
|---|---|
| 원인과 대책 | `DIAGNOSIS_ACTION` |
| 문제점과 개선방안 | `DIAGNOSIS_ACTION` |
| 비교하시오 | `COMPARE_SELECTION` |
| 장단점과 선정 기준 | `COMPARE_SELECTION` |
| 교정절차를 설명하시오 | `IMPLEMENTATION_EVALUATION` |
| 구성도와 절차 | `IMPLEMENTATION_EVALUATION` |
| 전달함수를 구하시오 | `PRINCIPLE_INTERPRETATION` |
| 감쇠비와 응답특성 | `PRINCIPLE_INTERPRETATION` |

## 10. question_type_coverage 구조

Semantic grader는 가능하면 `question_type_coverage`를 반환해야 한다.

핵심 필드:

    question_type
    name_ko
    coverage_source
    sub_criteria_coverage
    c_fact_focus_coverage
    d_field_judgement_focus_coverage
    missing_sub_criteria
    overall_coverage
    scoring_hint

예시 구조:

    question_type_coverage:
      question_type: IMPLEMENTATION_EVALUATION
      name_ko: 적용·평가형
      coverage_source: semantic_grader
      overall_coverage: poor
      missing_sub_criteria:
        - system_configuration
        - evaluation_metrics
      c_fact_focus_coverage:
        covered: []
        missing:
          - 시스템 구성
          - 절차·방법
          - 평가 지표
      d_field_judgement_focus_coverage:
        covered: []
        missing:
          - 운영 리스크
          - 유지보수성
          - 적용 후 검증 방법

## 11. Coverage 상태값

| 상태 | 의미 |
|---|---|
| `present` | 답안에 충분히 포함됨 |
| `partial` | 일부 언급은 있으나 기술사 답안 수준에는 부족 |
| `missing` | 요구 요소가 사실상 누락됨 |

전체 coverage는 다음 중 하나를 사용한다.

| overall_coverage | 의미 |
|---|---|
| `strong` | 유형별 요구를 충분히 충족 |
| `adequate` | 핵심 요구 대부분 충족 |
| `weak` | 주요 요소가 일부 누락 |
| `poor` | 유형별 핵심 요구가 대부분 누락 |
| `unknown` | semantic coverage를 판단할 수 없음 |

## 12. fallback 원칙

Semantic grader가 `question_type_coverage`를 반환하지 못하면 fallback coverage를 만든다.

fallback coverage의 특징:

- `coverage_source`는 `fallback_missing_semantic_field` 또는 `fallback_missing_grade_field`
- `overall_coverage`는 `unknown`
- 점수 보정 후보 계산에 사용하지 않음
- Telegram 출력에서 diagnostic 정보로만 사용

fallback 또는 unknown coverage는 실제 점수 감점에 사용하면 안 된다.

## 13. Score adjustment mode

Question Type coverage 보정 모드는 다음 환경변수로 제어한다.

    QUESTION_TYPE_COVERAGE_SCORE_MODE=warn

| 모드 | 의미 |
|---|---|
| `warn` | 보정 후보만 표시. 점수 변경 없음 |
| `strict` | 약한 보정을 실제 적용 |
| `off` | coverage 보정 비활성 |

현재 운영 기본값은 `warn`이다.

## 14. Telegram 출력 예시

    [Question Type Coverage]
    - 문제 유형 lens: 적용·평가형(IMPLEMENTATION_EVALUATION)
    - 세부 요구 충족도: poor
    - 부족한 세부 범주: background_need, target_scope, system_configuration, selection_criteria, evaluation_metrics 외 1개
    - C항목 보완 필요: 시스템 구성, 절차·방법, 평가 지표
    - D항목 보완 필요: 운영 리스크, 유지보수성, 적용 후 검증 방법
    - coverage 보정 후보: -0.75점, mode=warn

## 15. 관련 파일

| 파일 | 역할 |
|---|---|
| `rubrics/question_types/v2_professional_engineer.json` | v2 taxonomy 원본 |
| `rubrics/question_types/default.json` | 기본 taxonomy 설정 |
| `question_type_taxonomy.py` | taxonomy loader, normalizer, detector |
| `semantic_question_type_prompt.py` | semantic grader prompt contract |
| `semantic_question_type_postprocess.py` | coverage fallback/postprocess |
| `question_type_coverage_adapter.py` | grade root promotion 및 출력 보강 |
| `question_type_coverage_score_adjuster.py` | coverage 점수 보정 후보 계산 |
| `difficulty_output_adapter.py` | difficulty 출력과 question type coverage attach |
