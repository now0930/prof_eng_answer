# Logic Check JSON Bank Generator Prompt

이 문서는 `rubrics/logic_checks/industrial_instrumentation_control.json`에 추가할 수 있는 Logic Check Bank JSON 초안을 생성하기 위한 LLM 프롬프트입니다.

Logic Check Bank는 topic별 정규식 기반 fatal, major, minor, question type, field application, coherence feedback 규칙을 담습니다. 반면 `rubrics/logic_check_profiles/industrial_instrumentation_control.json`은 LLM verifier가 candidate evidence와 truth schema를 비교할 때 사용하는 profile입니다.

| 파일 | 주 역할 |
|---|---|
| `rubrics/logic_checks/industrial_instrumentation_control.json` | Python rule 기반 topic check, regex check, fallback check, D/E feedback check |
| `rubrics/logic_check_profiles/industrial_instrumentation_control.json` | LLM verifier용 truth schema, fatal/safe condition, candidate extraction profile |

---

## 사용 프롬프트

당신은 기술사 답안 채점 시스템의 Logic Check JSON Bank 설계자입니다.

목표는 특정 기술사 문항에 대해 `rubrics/logic_checks/industrial_instrumentation_control.json`의 `topic_logic_checks` 배열에 추가할 수 있는 JSON 객체를 설계하는 것입니다.

다음 원칙을 반드시 지키십시오.

1. Logic Check JSON Bank는 일반 채점 rubric이 아니라, 정답과 직접 충돌하는 핵심 오류와 주요 누락을 감지하기 위한 rule bank입니다.
2. Fatal은 정답과 직접 충돌하는 경우에만 적용하십시오.
3. 단순 누락, 설명 부족, 표현 미흡은 fatal이 아니라 major 또는 minor로 분류하십시오.
4. Fatal regex는 가능한 좁게 작성하십시오.
5. 좋은 답안에도 나오는 표현은 fatal regex에 넣지 마십시오.
6. 근사값, 현장 최적점, 관용 표현은 safe context 또는 profile safe_conditions에서 보호해야 합니다.
7. C 영역은 핵심 이론·정의·수식 정확성 중심입니다.
8. D 영역은 현장 적용성·설계 판단·비용·호환성·리스크 중심입니다.
9. E 영역은 논리 연결성과 면접 방어 가능성 중심입니다.
10. C 영역 fatal이 있더라도 D/E의 부분 장점은 ceiling 적용 전 의미 평가에 보존하십시오.
11. THEORY_CORE 문항에서 C 영역 fatal이 발생하면 최종 score cap 정책은 유지하십시오.
12. 가능한 Python 코드 변경 없이 JSON에 규칙을 담으십시오.
13. 표 답안은 단순 문자열이 아니라 `구분명 => 값` claim 구조로 해석될 수 있도록 rule을 설계하십시오.

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

### 현재 사용 중인 Logic Check Bank schema 참고

```json
{CURRENT_LOGIC_CHECK_JSON_SCHEMA_OR_EXISTING_TOPIC}
```

아래 단계에 따라 `topic_logic_checks`에 들어갈 topic 객체를 설계하십시오.

---

## 1. Topic 기본 정보

다음 필드를 작성하십시오.

- topic_id
- topic_name
- enabled
- question_type
- difficulty_profile
- topic_aliases

topic_aliases에는 한국어, 영어, 약어, 기호, 수험생이 자주 쓰는 표현을 포함하십시오.

## 2. Fatal Checks 작성

fatal_checks는 정답과 직접 충돌하는 오류만 포함하십시오.

각 fatal check는 다음 필드를 포함하십시오.

- id
- severity: `"fatal"`
- wrong_patterns
- message
- correct_rule
- affected_layers
- recommended_ceiling

작성 원칙:

- wrong_patterns는 정규식 문자열 배열입니다.
- 너무 넓은 regex를 쓰지 마십시오.
- 반드시 오답 표현과 정답 충돌이 동시에 드러나도록 작성하십시오.
- 단순히 특정 키워드가 등장했다는 이유만으로 fatal 처리하지 마십시오.
- C 영역 핵심 오류는 affected_layers를 `["C"]` 또는 `["C", "E"]`로 설정하십시오.
- THEORY_CORE fatal은 recommended_ceiling 10.0을 사용하십시오.

## 3. Major Checks 작성

major_checks는 핵심 구성요소 누락 또는 불충분을 잡습니다.

각 major check는 다음 필드를 포함하십시오.

- id
- severity: `"major"`
- required_patterns
- min_required
- message
- correct_rule
- affected_layers

작성 원칙:

- major는 score cap을 걸지 않습니다.
- 정답 핵심 요소가 부족하지만 반대로 쓰지는 않은 경우에 사용하십시오.
- required_patterns는 핵심 정답 요소를 넓게 커버하되, 너무 느슨하게 만들지 마십시오.

## 4. Question Type Checks 작성

question_type_checks는 문제 유형별 요구 충족을 평가합니다.

각 check는 다음 필드를 포함하십시오.

- id
- severity: `"minor"` 또는 `"major"`
- question_type
- required_axes 또는 required_patterns
- min_required
- message
- affected_layers

작성 원칙:

- 비교·선정형은 비교축, 장단점, 적용 조건, 선정 기준을 요구하십시오.
- 원리·해석형은 작동 원리, 변수 관계, 인과관계, 수식 의미를 요구하십시오.
- 진단·대책형은 원인, 영향, 대책, 재발방지, 검증 기준을 요구하십시오.
- 적용·평가형은 절차, 구성, 적용 조건, 효과 평가, 한계를 요구하십시오.

## 5. Advanced Trade-off Checks 작성

advanced_tradeoff_checks는 고급 키워드만 언급하고 실무 trade-off가 없는 경우를 잡습니다.

각 check는 다음 필드를 포함하십시오.

- id
- severity: `"minor"`
- trigger_patterns
- required_context_patterns
- message
- affected_layers

작성 원칙:

- TSN, EtherCAT, Smith Predictor, IMC, AI, digital twin 등 고급 키워드는 단독 언급만으로 가점이 아닙니다.
- 비용, 호환성, 기존 설비 영향, 정지시간, 운전 리스크, 모델 불일치, 유지보수성, 검증 기준이 함께 있어야 합니다.

## 6. Field Application Checks 작성

field_application_checks는 D 영역을 평가합니다.

positive check와 minor check를 분리하십시오.

positive check는 다음을 인정합니다.

- 현장 문제를 정확히 연결함
- 비용, 호환성, 기존 설비 영향, 운전 리스크를 언급함
- 공정별 적용 조건을 제시함
- 검증 기준을 제시함

minor check는 다음을 지적합니다.

- 고급 키워드만 있고 trade-off가 없음
- 현장 적용이 일반론에 그침
- 공정별 선정 기준이 없음
- 검증 기준이 없음

## 7. Coherence Defense Checks 작성

coherence_defense_checks는 E 영역을 평가합니다.

다음 유형을 포함하십시오.

- theory_to_field_chain_present: 이론 → 현상 → 현장 문제 → 대책 → 검증/결론 연결 인정
- conclusion_without_selection_or_verification: 결론이 일반론으로 끝나는 경우 minor
- fatal_theory_but_field_credit_preserved: C fatal이 있어도 D/E 피드백은 보존한다는 policy

policy check에는 다음 scoring_policy를 포함하십시오.

```json
{
  "preserve_pre_ceiling_feedback": true,
  "do_not_override_c_fatal_cap": true,
  "executive_summary_rule": "현장 적용 시도는 인정되나 핵심 이론 오류로 최종 cap 적용이라고 설명한다."
}
```

## 8. Feedback Templates 작성

d_e_feedback_templates를 작성하십시오.

필드는 다음과 같습니다.

- d_positive
- d_minor
- e_positive
- e_minor
- ceiling_note

각 문장은 채점 결과에 그대로 넣을 수 있는 한국어 문장으로 작성하십시오.

## 9. Next Practice Points 작성

next_practice_points에는 수험생이 다음 답안을 쓸 때 바로 적용할 수 있는 훈련 포인트를 3~5개 작성하십시오.

---

## 출력 형식

출력은 오직 valid JSON 객체 하나로 작성하십시오. Markdown code block, 설명문, 주석은 출력하지 마십시오.

```json
{
  "topic_id": "...",
  "topic_name": "...",
  "enabled": true,
  "question_type": "...",
  "difficulty_profile": "THEORY_CORE / STANDARD / APPLICATION",
  "topic_aliases": [],
  "fatal_checks": [
    {
      "id": "...",
      "severity": "fatal",
      "wrong_patterns": [],
      "message": "...",
      "correct_rule": "...",
      "affected_layers": ["C"],
      "recommended_ceiling": 10.0
    }
  ],
  "major_checks": [
    {
      "id": "...",
      "severity": "major",
      "required_patterns": [],
      "min_required": 2,
      "message": "...",
      "correct_rule": "...",
      "affected_layers": ["C"]
    }
  ],
  "question_type_checks": [
    {
      "id": "...",
      "severity": "minor",
      "question_type": "...",
      "required_axes": [],
      "min_required": 3,
      "message": "...",
      "affected_layers": ["B", "C", "D"]
    }
  ],
  "advanced_tradeoff_checks": [
    {
      "id": "...",
      "severity": "minor",
      "trigger_patterns": [],
      "required_context_patterns": [],
      "message": "...",
      "affected_layers": ["D", "E"]
    }
  ],
  "field_application_checks": [
    {
      "id": "...",
      "severity": "positive",
      "question_type": "...",
      "evidence_patterns": [],
      "min_required": 3,
      "message": "...",
      "affected_layers": ["D", "E"],
      "scoring_hint": {
        "d_credit": "partial_positive",
        "e_credit": "partial_positive",
        "note": "C 영역 fatal이 있더라도 D/E의 현장 적용 시도는 ceiling 적용 전 의미 평가에 반영한다."
      }
    }
  ],
  "coherence_defense_checks": [
    {
      "id": "theory_to_field_chain_present",
      "severity": "positive",
      "chain_patterns": [],
      "min_required": 4,
      "message": "...",
      "affected_layers": ["E"]
    },
    {
      "id": "conclusion_without_selection_or_verification",
      "severity": "minor",
      "trigger_patterns": [],
      "required_context_patterns": [],
      "min_required": 2,
      "message": "...",
      "affected_layers": ["E"]
    },
    {
      "id": "fatal_theory_but_field_credit_preserved",
      "severity": "policy",
      "message": "C 영역 fatal이 있더라도 D/E의 현장 적용 시도는 별도 피드백으로 보존한다. 단 최종 점수는 THEORY_CORE fatal ceiling을 우선 적용한다.",
      "affected_layers": ["D", "E"],
      "scoring_policy": {
        "preserve_pre_ceiling_feedback": true,
        "do_not_override_c_fatal_cap": true,
        "executive_summary_rule": "현장 적용 시도는 인정되나 핵심 이론 오류로 최종 cap 적용이라고 설명한다."
      }
    }
  ],
  "d_e_feedback_templates": {
    "d_positive": "...",
    "d_minor": "...",
    "e_positive": "...",
    "e_minor": "...",
    "ceiling_note": "..."
  },
  "next_practice_points": []
}
```

## 검토 기준

- fatal regex가 너무 넓으면 안 됩니다.
- fatal은 반드시 정답과 직접 충돌해야 합니다.
- safe condition이 필요한 내용은 Logic Check Profile 쪽에도 반영해야 합니다.
- D/E는 감점·가점 피드백 중심이어야 하며 C fatal cap을 덮어쓰면 안 됩니다.
- JSON은 `topic_logic_checks` 배열에 바로 넣을 수 있는 topic 객체여야 합니다.
