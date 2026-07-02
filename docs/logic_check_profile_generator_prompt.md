# Logic Check Profile Generator Prompt

이 문서는 `rubrics/logic_check_profiles/industrial_instrumentation_control.json`에 추가할 수 있는 Logic Check Profile JSON을 생성하기 위한 LLM 프롬프트입니다.

Logic Check Profile은 `logic_llm_verifier.py`가 사용하는 topic별 검증 지식입니다. 핵심 목적은 일반 채점이 아니라, 수험생 답안의 정의 오류, 수식 오류, 경계값 오류, 물리적 인과 오류, safe condition을 LLM verifier가 안정적으로 판정하도록 하는 것입니다.

---

## 사용 프롬프트

당신은 기술사 답안 채점 시스템의 Logic Check Profile 설계자입니다.

목표는 특정 기술사 문항에 대해 `rubrics/logic_check_profiles/industrial_instrumentation_control.json`에 추가할 수 있는 Logic Check Profile JSON을 설계하는 것입니다.

다음 원칙을 반드시 지키십시오.

1. Logic Check Profile은 일반 채점 rubric이 아니라, 핵심 이론 오류·정의 오류·수식 오류·논리 비약을 검출하기 위한 검증 profile입니다.
2. Fatal은 정답과 직접 충돌하는 경우에만 적용하십시오.
3. 단순 누락, 설명 부족, 표현 미흡은 fatal이 아니라 major 또는 minor로 분류하십시오.
4. 실무적 표현, 관용적 근사값, 현장 최적점은 safe condition으로 보호하십시오.
5. C 영역은 핵심 이론·정의·수식 정확성 중심입니다.
6. D 영역은 현장 적용성·설계 판단·비용·호환성·리스크 중심입니다.
7. E 영역은 이론 → 현장 문제 → 대책 → 검증 기준으로 이어지는 논리 연결성과 면접 방어 가능성 중심입니다.
8. C 영역 fatal이 발생해도 D/E의 부분 장점은 ceiling 적용 전 의미 평가에 보존하십시오.
9. 단, THEORY_CORE 문항에서 C 영역 fatal이 발생하면 최종 score cap 정책은 유지하십시오.
10. profile은 Python 코드에 하드코딩하지 않고 JSON에 지식과 판정 기준을 담는 구조여야 합니다.

입력 정보는 다음과 같습니다.

### 문항 정보

- topic_id: `{TOPIC_ID}`
- topic_name: `{TOPIC_NAME}`
- question_type: `{QUESTION_TYPE}`
- difficulty_profile: `{DIFFICULTY_PROFILE}`
- question_text: `{QUESTION_TEXT}`

### 정답 기준 / Fact Anchor

```text
{FACT_ANCHORS_OR_MODEL_ANSWER}
```

### 수험생 오답 사례

```text
{WRONG_STUDENT_ANSWER_EXAMPLES}
```

### 정상 답안 또는 safe 예시

```text
{SAFE_OR_GOOD_ANSWER_EXAMPLES}
```

### 현재 사용 중인 profile schema 참고

```json
{CURRENT_PROFILE_SCHEMA_OR_EXISTING_TOPIC_PROFILE}
```

아래 단계에 따라 profile을 설계하십시오.

---

## 1. Topic 식별

- topic_id, display_name, difficulty, question_type을 정의하십시오.
- topic_aliases를 작성하십시오.
- 한국어 표현, 영어 표현, 약어, 기호 표현을 모두 포함하십시오.

## 2. Candidate Extraction 설계

- 답안에서 검증에 필요한 핵심 문장, 표, 수식, 도식 설명을 추출할 수 있도록 key_terms를 정의하십시오.
- 표 형태 답안도 처리할 수 있도록 structured_mapping rule을 포함하십시오.
- 수식, 경계값, 비교표, 인과관계 표현을 추출할 nearby_regex 또는 line_regex rule을 설계하십시오.
- 후보 추출은 과도하게 넓지 않게 하되, 수험생이 흔히 쓰는 오타·혼용 표현은 어느 정도 허용하십시오.

## 3. Truth Schema 작성

- 해당 topic의 표준 정의, 공식, 경계 조건, 물리적 의미, 현장 적용 원칙을 간결한 문장으로 작성하십시오.
- 수식은 가능한 한 명확하게 작성하십시오.
- 이 schema는 fatal/major/minor 판단의 기준이 됩니다.

## 4. Fatal Conditions 작성

- 정답과 직접 충돌하는 오류만 fatal로 작성하십시오.
- 특히 다음 유형을 fatal 후보로 보십시오.
  - 정의를 반대로 씀
  - 수식의 변수 관계를 반대로 씀
  - 경계값을 잘못 정의함
  - 안정/불안정, 수렴/발산을 혼동함
  - 표준 물리 거동과 반대되는 응답 특성을 씀
- fatal condition마다 왜 치명적인지 reasoning이 가능하도록 문장을 구체화하십시오.
- fatal에는 affected_layers를 명시하십시오. 보통 핵심 이론 오류는 `["C"]` 또는 `["C", "E"]`입니다.
- THEORY_CORE fatal에는 recommended_ceiling 10.0을 적용할 수 있도록 설계하십시오.

## 5. Safe Conditions 작성

- 오탐을 막기 위한 예외 조건을 작성하십시오.
- 근사값, 실무 최적점, 관용 표현, 부분적으로 맞는 설명은 안전하게 보호하십시오.
- “이 표현 자체는 fatal이 아니다. 단, 정의로 오용하면 fatal이다.” 형식의 safe condition을 반드시 포함하십시오.

## 6. Major Checks 작성

- 반드시 있어야 하는 핵심 구성요소가 누락된 경우를 major로 정의하십시오.
- 단, major는 score cap을 걸지 않습니다.
- required_patterns와 min_required를 포함하십시오.

## 7. Question Type Checks 작성

- question_type에 맞는 요구사항을 점검하십시오.
- 비교·선정형이면 비교축, 선정 기준, 장단점, 적용 조건을 요구하십시오.
- 원리 설명형이면 작동 원리, 변수 관계, 인과관계를 요구하십시오.
- 절차형이면 단계, 기준, 검증 절차를 요구하십시오.

## 8. D 영역 Field Application Checks 작성

- 현장 적용성, 설계 판단, 비용, 기존 설비 영향, 운전 리스크, 유지보수성, 검증 기준을 평가하십시오.
- 좋은 현장 연결은 positive check로 인정하십시오.
- 고급 키워드만 있고 trade-off가 없으면 minor로 평가하십시오.
- D 영역은 fatal 남발 금지입니다.

## 9. E 영역 Coherence Defense Checks 작성

- 답안이 이론식 → 현상 → 문제점 → 현장 대책 → 비용/리스크 → 검증/결론으로 연결되는지 평가하십시오.
- 결론이 일반론으로 끝나고 선정 기준 또는 검증 기준이 없으면 minor로 평가하십시오.
- C fatal이 있더라도 D/E 피드백은 보존한다는 policy check를 포함하십시오.

## 10. Feedback Templates 작성

- positive, minor, ceiling_note를 분리하십시오.
- 채점 결과에 그대로 삽입 가능한 한국어 문장으로 작성하십시오.

## 11. Output Contract 작성

- verifier가 반환해야 할 JSON field를 정의하십시오.
- verdict 값은 pass, warn, fatal로 제한하십시오.
- confidence threshold를 포함하십시오.
- LLM verifier 실패 또는 confidence 부족 시 fatal cap을 적용하지 않는 fail-safe 원칙을 포함하십시오.

---

## 출력 형식

출력은 오직 valid JSON 객체 하나로 작성하십시오. Markdown code block, 설명문, 주석은 출력하지 마십시오.

```json
{
  "topic_id": "...",
  "display_name": "...",
  "difficulty": "THEORY_CORE / STANDARD / APPLICATION",
  "question_type": "...",
  "cap_policy": {
    "fatal_recommended_ceiling": 10.0,
    "fatal_confidence_threshold": 0.75,
    "fail_safe_on_verifier_error": true
  },
  "topic_aliases": [],
  "candidate_extraction": {
    "max_candidates": 12,
    "nearby_window": 1,
    "key_terms": [],
    "rules": []
  },
  "truth_schema": [],
  "fatal_conditions": [],
  "safe_conditions": [],
  "major_checks": [],
  "question_type_checks": [],
  "field_application_checks": [],
  "coherence_defense_checks": [],
  "feedback_templates": {
    "c_fatal": "",
    "d_positive": "",
    "d_minor": "",
    "e_positive": "",
    "e_minor": "",
    "ceiling_note": ""
  },
  "next_practice_points": [],
  "output_contract": {
    "json_only": true,
    "required_fields": [
      "verdict",
      "confidence",
      "reason",
      "findings"
    ],
    "verdict_values": [
      "pass",
      "warn",
      "fatal"
    ]
  }
}
```

## 검토 기준

- fatal condition이 너무 넓으면 안 됩니다.
- safe condition이 반드시 있어야 합니다.
- D/E는 감점·가점 피드백 중심이어야 하며, C fatal cap을 덮어쓰면 안 됩니다.
- 표, 수식, 도식, 문장형 답안을 모두 처리할 수 있어야 합니다.
- JSON은 바로 저장 가능한 형식이어야 합니다.
