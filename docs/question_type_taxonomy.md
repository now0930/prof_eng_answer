# Question Type v2 Taxonomy

Question Type v2는 기술사 2~4교시 답안에 맞춰 C항목 Fact 전개와 D항목 현장 판단을 보강하기 위한 lens이다. 별도 점수 체계가 아니며 A/B/C/D/E를 대체하지 않는다.

## 1. v2 대분류

| question_type | 한국어명 | 핵심 평가 방향 |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | 원리, 메커니즘, 수식, 계산, 결과 해석 |
| `DIAGNOSIS_ACTION` | 진단·대책형 | 문제, 원인, 영향, 대책, 검증 |
| `COMPARE_SELECTION` | 비교·선정형 | 비교축, 장단점, 적용 조건, 선정 판단 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | 대상, 구성, 절차, 평가 지표, 운영 개선 |

## 2. Legacy mapping

| legacy question_type | v2 question_type |
|---|---|
| `DEFINE` | 신규 작성에서는 사용하지 않음. 필요 시 원리·해석형에 흡수 |
| `PRINCIPLE` | `PRINCIPLE_INTERPRETATION` |
| `CALC_DESIGN` | `PRINCIPLE_INTERPRETATION` |
| `PROBLEM_SOLVE` | `DIAGNOSIS_ACTION` |
| `CAUSE_ACTION` | `DIAGNOSIS_ACTION` |
| `COMPARE` | `COMPARE_SELECTION` |
| `STRUCTURE` | 보통 `COMPARE_SELECTION`, 맥락에 따라 `IMPLEMENTATION_EVALUATION` 또는 `PRINCIPLE_INTERPRETATION` |
| `PROCEDURE` | `IMPLEMENTATION_EVALUATION` |
| `APPLICATION` | `IMPLEMENTATION_EVALUATION` |
| `EVALUATION` | `IMPLEMENTATION_EVALUATION` |

신규 Model Answer의 `question_type`은 반드시 v2 4개 중 하나여야 한다.

## 3. PRINCIPLE_INTERPRETATION

원리·해석형은 대상의 동작 원리, 전달함수, 수식, 변수 의미, 계산 결과 해석을 설명하는 문제에 사용한다.

대표 신호:

- 원리를 설명하시오
- 전달함수를 구하시오
- 응답특성을 설명하시오
- 안정도와 감쇠비를 설명하시오
- 계산하시오
- 수식의 각 항을 설명하시오

C항목 focus:

- 구성요소
- 동작 원리와 물리적 의미
- 수식·모델·변수·단위
- 계산 또는 해석 과정
- 결과값 또는 응답특성 의미

D항목 focus:

- 설계 판단
- tuning, 안정성, 제어성, 오차 영향
- 현장 적용 한계
- 유지보수와 운전 조건
- 비용·성능 trade-off

## 4. DIAGNOSIS_ACTION

진단·대책형은 문제점, 발생 원인, 영향, 대책, 우선순위, 검증 방법을 설명하는 문제에 사용한다.

대표 신호:

- 원인과 대책
- 문제점과 개선방안
- 고장 원인
- 오차 발생 원인
- 방지 대책
- 개선 방법

C항목 focus:

- 문제 정의
- 원인 메커니즘
- 영향과 리스크
- 대책의 기술적 근거

D항목 focus:

- 우선순위
- 비용·효과
- 적용 가능성
- 검증 방법
- 재발 방지

## 5. COMPARE_SELECTION

비교·선정형은 두 개 이상의 기술, 방식, 장치, 제어 전략을 비교하고 적용 조건에 따라 선정하는 문제에 사용한다.

대표 신호:

- 비교하시오
- 차이점을 설명하시오
- 장단점을 설명하시오
- 선정 기준을 제시하시오
- 적용 조건을 비교하시오

C항목 focus:

- 분류 기준
- 구조적 특징
- 비교축
- 장점과 한계
- 적용 조건

D항목 focus:

- 선정 판단
- 현장 조건별 적용성
- 비용·유지보수성
- 기존 설비와의 연계
- trade-off

## 6. IMPLEMENTATION_EVALUATION

적용·평가형은 시스템 구성, 절차, 방법, 적용 범위, 평가 지표, 운영 개선 효과를 설명하는 문제에 사용한다.

대표 신호:

- 절차를 설명하시오
- 방법을 설명하시오
- 구성도를 설명하시오
- 적용 사례를 설명하시오
- 평가 방법을 설명하시오
- 교정 절차를 설명하시오

C항목 focus:

- 적용 대상
- 시스템 구성
- 절차와 방법
- 선정 기준
- 평가 지표

D항목 focus:

- 기존 설비와의 연계
- 적용 조건
- 비용·효과
- 운영 리스크
- 유지보수성
- 적용 후 검증 방법
- 개선 효과와 한계

## 7. Detector 우선순위

복합 신호가 있을 때 일반 우선순위는 다음과 같다.

```text
DIAGNOSIS_ACTION
COMPARE_SELECTION
IMPLEMENTATION_EVALUATION
PRINCIPLE_INTERPRETATION
```

명확한 진단, 비교, 적용 신호가 없으면 fallback은 `PRINCIPLE_INTERPRETATION`이다.

## 8. Coverage 구조

Semantic grader는 가능하면 `question_type_coverage`를 반환한다.

핵심 필드:

- `question_type`
- `name_ko`
- `coverage_source`
- `sub_criteria_coverage`
- `c_fact_focus_coverage`
- `d_field_judgement_focus_coverage`
- `missing_sub_criteria`
- `overall_coverage`
- `scoring_hint`

Coverage 상태값:

| 상태 | 의미 |
|---|---|
| `present` | 충분히 포함 |
| `partial` | 일부 언급은 있으나 부족 |
| `missing` | 사실상 누락 |

전체 coverage:

| overall_coverage | 의미 |
|---|---|
| `strong` | 유형별 요구 충분히 충족 |
| `adequate` | 핵심 요구 대부분 충족 |
| `weak` | 주요 요소 일부 누락 |
| `poor` | 핵심 요구 대부분 누락 |
| `unknown` | 판단 불가 |

## 9. Coverage score adjustment

환경변수:

```text
QUESTION_TYPE_COVERAGE_SCORE_MODE=warn
```

| 모드 | 의미 |
|---|---|
| `warn` | 보정 후보만 표시. 점수 변경 없음 |
| `strict` | 약한 보정을 실제 적용 |
| `off` | coverage 보정 비활성 |

Fallback 또는 `unknown` coverage는 실제 감점에 사용하지 않는다.

## 10. Telegram 출력 예시

```text
[Question Type Coverage]
- 문제 유형 lens: 비교·선정형(COMPARE_SELECTION)
- 세부 요구 충족도: adequate
- 부족한 세부 범주: comparison_axis, selection_judgement
- C항목 보완 필요: 상세 비교축, 정량적 지표
- D항목 보완 필요: 비용/운전 리스크 trade-off, 최종 선정 기준
- coverage 보정 후보: -0.39점, mode=warn
```

## 11. 관련 파일

| 파일 | 역할 |
|---|---|
| `rubrics/question_types/default.json` | 기본 taxonomy 설정 |
| `question_type_taxonomy.py` | taxonomy loader, normalizer, detector |
| `semantic_question_type_prompt.py` | semantic grader prompt contract |
| `semantic_question_type_postprocess.py` | coverage fallback/postprocess |
| `question_type_coverage_adapter.py` | grade root promotion 및 출력 보강 |
| `question_type_coverage_score_adjuster.py` | coverage 점수 보정 후보 계산 |
| `question_type_output_adapter.py` | 출력 보조 |
