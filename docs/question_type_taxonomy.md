# Question Type Taxonomy v2

이 문서는 산업계측제어기술사 2~4교시 답안 채점에서 사용하는 `question_type` 체계를 설명한다.

`question_type`은 별도 점수체계가 아니다.  
기존 A/B/C/D/E 25점 채점 구조를 유지하면서, C항목 Fact 기반 설명과 D항목 현장 적용·판단·제언을 보강하기 위한 lens이다.

---

## 1. 기본 원칙

기술사 답안은 단답식 키워드 나열이 아니라 다음 구조로 평가한다.

| 항목 | 의미 |
|---|---|
| A | 배경과 문제 진입 |
| B | 문제 요구 파악 |
| C | Fact 기반 설명 |
| D | 현장 적용·판단·제언 |
| E | 연결성·면접 방어 가능성 |

`question_type`은 주로 C와 D를 보강한다.

```text

question_type = 큰 답안 전개 방향
sub_criteria = 해당 유형에서 언급되어야 할 세부 범주
coverage = 답안이 세부 범주를 얼마나 충족했는지 평가한 결과
```

---

## 2. 최종 question_type

| question_type | 의미 | 흡수한 기존 유형 |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·동작·계산·설계·수식 해석형 | `PRINCIPLE`, `CALC_DESIGN` |
| `DIAGNOSIS_ACTION` | 문제·원인·영향·대책·개선 실행형 | `PROBLEM_SOLVE`, `CAUSE_ACTION` |
| `COMPARE_SELECTION` | 비교·분류·선정 판단형 | `COMPARE`, 일부 `STRUCTURE` |
| `IMPLEMENTATION_EVALUATION` | 적용·절차·방법·평가형 | `PROCEDURE`, `APPLICATION`, `EVALUATION`, 일부 `STRUCTURE` |

삭제 또는 흡수된 유형:

| 기존 type | 처리 |
|---|---|
| `DEFINE` | 삭제. 1교시 단답형 중심이므로 2~4교시 채점에서는 사용하지 않음 |
| `CALC_DESIGN` | `PRINCIPLE_INTERPRETATION`에 흡수 |
| `PROBLEM_SOLVE` | `DIAGNOSIS_ACTION`에 흡수 |
| `CAUSE_ACTION` | `DIAGNOSIS_ACTION`에 흡수 |
| `PROCEDURE` | `IMPLEMENTATION_EVALUATION`에 흡수 |
| `APPLICATION` | `IMPLEMENTATION_EVALUATION`에 흡수 |
| `EVALUATION` | `IMPLEMENTATION_EVALUATION`에 흡수 |
| `STRUCTURE` | 독립 type이 아니라 각 유형의 Fact 설명 요소로 흡수 |

---

## 3. PRINCIPLE_INTERPRETATION

원리·동작·계산·설계·수식 해석형이다.

계산 문제가 있어도 계산 자체가 목적이 아니다.  
식이 왜 성립하는지, 어떤 원리인지, 계산 결과가 현장에서 어떤 의미인지 설명해야 한다.

| 세부 범주 | 채점 시 확인할 내용 |
|---|---|
| `background_need` | 왜 이 원리나 계산이 필요한가 |
| `structure_components` | 대상 시스템, 회로, 계기, 제어 loop 구성요소를 설명했는가 |
| `principle_mechanism` | 동작 원리와 물리적 의미를 설명했는가 |
| `formula_model_variables` | 수식, 모델, 변수, 단위의 의미를 설명했는가 |
| `calculation_or_interpretation` | 계산 또는 해석 과정이 논리적인가 |
| `result_meaning` | 결과값이나 응답특성의 의미를 설명했는가 |
| `field_judgement` | 선정, tuning, 안정성, 제어성, 한계 등을 언급했는가 |

예시:

| 문제 | 분류 |
|---|---|
| 2차 시스템의 응답특성을 설명하시오 | `PRINCIPLE_INTERPRETATION` |
| Cv를 계산하고 밸브를 선정하시오 | `PRINCIPLE_INTERPRETATION` |
| 전달함수를 구하고 의미를 설명하시오 | `PRINCIPLE_INTERPRETATION` |
| 센서 분해능을 계산하시오 | `PRINCIPLE_INTERPRETATION` |

---

## 4. DIAGNOSIS_ACTION

문제·원인·영향·대책·개선 실행형이다.

문제점만 쓰거나 대책만 쓰면 부족하다.  
무엇이 문제인지, 왜 발생하는지, 어떤 영향을 주는지, 어떻게 해결할지, 실제로 가능한지를 함께 설명해야 한다.

| 세부 범주 | 채점 시 확인할 내용 |
|---|---|
| `background_need` | 왜 이 문제가 중요한가 |
| `problem_definition` | 무엇이 문제인지 명확히 정의했는가 |
| `cause_mechanism` | 기술적 원인과 발생 메커니즘을 설명했는가 |
| `impact_risk` | 품질, 안전, 신뢰성, 제어성, 유지보수 영향을 설명했는가 |
| `action_countermeasure` | 설계, 운전, 유지보수, 계측, 제어 측면 대책이 있는가 |
| `feasibility_tradeoff` | 비용, 기존 설비, 적용 난이도, trade-off를 언급했는가 |
| `priority_and_verification` | 대책 우선순위와 검증 방법을 제시했는가 |

예시:

| 문제 | 분류 |
|---|---|
| 캐비테이션의 원인과 대책을 설명하시오 | `DIAGNOSIS_ACTION` |
| 노이즈 발생원인과 저감대책을 설명하시오 | `DIAGNOSIS_ACTION` |
| 계측 시스템 도입 시 문제점과 개선방안을 설명하시오 | `DIAGNOSIS_ACTION` |
| 제어밸브 선정 시 고려사항을 설명하시오 | `DIAGNOSIS_ACTION` |

---

## 5. COMPARE_SELECTION

비교·분류·선정 판단형이다.

종류나 특징을 나열하는 것이 아니라, 비교축을 만들고 적용 조건에 따라 선정 판단까지 가야 한다.

| 세부 범주 | 채점 시 확인할 내용 |
|---|---|
| `background_need` | 왜 비교나 선정이 필요한가 |
| `classification_axis` | 어떤 기준으로 분류했는가 |
| `structure_features` | 각 방식의 구조, 기능, 특징을 설명했는가 |
| `comparison_axis` | 정확도, 응답속도, 비용, 유지보수성 등 비교축이 있는가 |
| `pros_cons_limits` | 각 방식의 장점과 한계를 설명했는가 |
| `application_conditions` | 어떤 현장 조건에서 적합한지 설명했는가 |
| `selection_judgement` | 최종적으로 어떤 경우에 무엇을 선택할지 제시했는가 |

예시:

| 문제 | 분류 |
|---|---|
| 수위 측정 방식의 종류와 특징을 설명하시오 | `COMPARE_SELECTION` |
| 제어밸브 종류 및 장단점을 설명하시오 | `COMPARE_SELECTION` |
| 정확도와 정밀도를 비교 설명하시오 | `COMPARE_SELECTION` |
| 방폭지역 Zone/Class/Division을 비교 설명하시오 | `COMPARE_SELECTION` |

---

## 6. IMPLEMENTATION_EVALUATION

적용·절차·방법·평가형이다.

적용, 절차, 교정, 시험, 평가, 효과 분석은 하나의 흐름으로 본다.

```text

적용 필요성
-> 적용 대상 선정
-> 시스템 구성 또는 절차
-> 실행 조건
-> 평가 기준
-> 효과와 한계
-> 현장 적용 판단
```

| 세부 범주 | 채점 시 확인할 내용 |
|---|---|
| `background_need` | 왜 적용 또는 평가가 필요한가 |
| `target_scope` | 어디에 적용하는지, 대상 설비·공정이 명확한가 |
| `system_configuration` | 필요한 장비, 계기, 신호, 제어 구조를 설명했는가 |
| `procedure_method` | 적용, 설치, 교정, 시험, 검증 절차가 있는가 |
| `selection_criteria` | 장비, 방식, 조건을 선택하는 기준이 있는가 |
| `evaluation_metrics` | 성능, 안정성, 품질, 비용, 효과 지표를 제시했는가 |
| `operation_improvement_judgement` | 적용 후 운영 판단, 검증, 개선, 확장성을 언급했는가 |

C항목과 D항목은 다음처럼 분리한다.

| 항목 | 역할 |
|---|---|
| C항목 | 적용 대상, 시스템 구성, 절차·방법, 선정 기준, 평가 지표, 효과·한계 |
| D항목 | 기존 설비 연계, 적용 조건, 비용·효과, 운영 리스크, 유지보수성, 검증 방법, 개선·확장 방향 |

예시:

| 문제 | 분류 |
|---|---|
| 차압전송기의 교정회로와 교정절차를 설명하시오 | `IMPLEMENTATION_EVALUATION` |
| 감시제어시스템의 구성과 적용 방법을 설명하시오 | `IMPLEMENTATION_EVALUATION` |
| 원격검침시스템의 기능, 구성 및 설계를 설명하시오 | `IMPLEMENTATION_EVALUATION` |
| 소프트웨어 품질 평가 항목을 설명하시오 | `IMPLEMENTATION_EVALUATION` |

---

## 7. Semantic Grader Coverage

Gemini/CLOVA semantic grader는 다음 필드를 출력하도록 요청받는다.

```json

{
  "question_type_coverage": {
    "question_type": "IMPLEMENTATION_EVALUATION",
    "name_ko": "적용·평가형",
    "sub_criteria_coverage": [
      {
        "criterion": "target_scope",
        "status": "present | partial | missing",
        "evidence": "답안 근거 또는 누락 설명",
        "impact": "C 또는 D 점수에 주는 영향"
      }
    ],
    "c_fact_focus_coverage": {
      "covered": ["충족된 C항목 focus"],
      "missing": ["부족한 C항목 focus"]
    },
    "d_field_judgement_focus_coverage": {
      "covered": ["충족된 D항목 focus"],
      "missing": ["부족한 D항목 focus"]
    },
    "missing_sub_criteria": ["누락된 sub_criteria"],
    "overall_coverage": "strong | adequate | weak | poor",
    "scoring_hint": "A/B/C/D/E 중 어느 항목을 보수적으로 볼지 설명"
  }
}
```

---

## 8. 점수 보정 모드

coverage 결과는 기본적으로 점수를 직접 바꾸지 않는다.

```env

QUESTION_TYPE_COVERAGE_SCORE_MODE=warn
```

`warn` 모드에서는 보정 후보만 표시한다.

```text

coverage 보정 후보: -0.45점, mode=warn
```

실제 약한 감점을 적용하려면 다음을 사용한다.

```env

QUESTION_TYPE_COVERAGE_SCORE_MODE=strict
```

strict 모드도 보수적으로 동작한다.

| 항목 | 값 |
|---|---:|
| 최대 총 보정 | 0.75점 |
| C항목 관련 최대 보정 | 0.45점 |
| D항목 관련 최대 보정 | 0.30점 |

---

## 9. Telegram 출력

Telegram 답변 끝에는 다음 요약이 붙을 수 있다.

```text

[Question Type Coverage]
- 문제 유형 lens: 적용·평가형(IMPLEMENTATION_EVALUATION)
- 세부 요구 충족도: weak
- 부족한 세부 범주: selection_criteria, evaluation_metrics
- C항목 보완 필요: 시스템 구성, 선정 기준, 평가 지표
- D항목 보완 필요: 기존 설비와의 연계, 운영 리스크, 적용 후 검증 방법
- coverage 보정 후보: -0.45점, mode=warn
```

---

## 10. 관련 파일

| 파일 | 역할 |
|---|---|
| `rubrics/question_types/v2_professional_engineer.json` | v2 question_type 정의 |
| `question_type_taxonomy.py` | v2 taxonomy load, legacy mapping, detection |
| `question_type_output_adapter.py` | grade에 question_type_v2 정보 추가 |
| `semantic_question_type_prompt.py` | Gemini/CLOVA prompt용 세부 기준 생성 |
| `semantic_question_type_postprocess.py` | semantic result에 coverage fallback 보정 |
| `question_type_coverage_adapter.py` | coverage를 피드백에 반영 |
| `question_type_coverage_score_adjuster.py` | warn/strict 점수 보정 후보 계산 |
| `bot.py` | Telegram 출력에 coverage 요약 표시 |
