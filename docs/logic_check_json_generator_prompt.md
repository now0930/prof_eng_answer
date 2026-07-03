# Logic Check JSON Bank Generator Prompt

이 문서는 `rubrics/logic_checks/industrial_instrumentation_control.json`에 추가할 수 있는 Logic Check Bank JSON 초안을 생성하기 위한 LLM 프롬프트다.

Logic Check Bank는 일반 A/B/C/D/E 채점 rubric이 아니다.
Logic Check Bank의 역할은 topic별 핵심 이론·정의·수식·논리 오류를 검증하는 topic truth gate다.

`rubrics/logic_check_profiles/industrial_instrumentation_control.json`은 LLM verifier가 candidate evidence와 truth schema를 비교할 때 사용하는 profile이다.

## 파일 역할

| 파일 | 주 역할 |
|---|---|
| `rubrics/logic_checks/industrial_instrumentation_control.json` | Python rule 기반 topic truth check, regex check, fallback check, D/E claim trust metadata |
| `rubrics/logic_check_profiles/industrial_instrumentation_control.json` | LLM verifier용 truth schema, fatal/safe condition, candidate extraction profile |

## 핵심 원칙

1. Logic Check JSON Bank는 D/E를 직접 평가하지 않는다.
2. D/E 점수는 A/B/C/D/E scoring model에서만 산정한다.
3. Logic Check는 정답과 직접 충돌하는 핵심 오류를 검출한다.
4. Fatal은 정답과 직접 충돌하는 경우에만 적용한다.
5. 단순 누락, 설명 부족, 표현 미흡은 fatal로 분류하지 않는다.
6. Fatal regex는 가능한 좁게 작성한다.
7. 좋은 답안에도 나오는 표현은 fatal regex에 넣지 않는다.
8. 근사값, 현장 최적점, 관용 표현은 safe context 또는 profile safe_conditions에서 보호한다.
9. C 영역은 핵심 이론·정의·수식 정확성 중심이다.
10. Logic Check finding의 `affected_layers`에는 원칙적으로 `A`, `B`, `C`만 사용한다.
11. `D`, `E`는 `affected_layers`가 아니라 `de_claim_trust.target_layers`로만 연결한다.
12. THEORY_CORE 문항에서 C 영역 fatal이 발생하면 최종 score cap 정책은 유지한다.
13. C 영역 fatal이 있더라도 D/E 현장 적용 시도 자체는 A/B/C/D/E scoring model에서 별도 평가한다.
14. Logic Check는 해당 D/E 주장의 이론적 신뢰 가능 여부만 표시한다.
15. 표 답안은 단순 문자열이 아니라 `구분명 => 값` claim 구조로 해석될 수 있도록 rule을 설계한다.

## 입력 정보

### 문항 정보

- topic_id: {TOPIC_ID}
- topic_name: {TOPIC_NAME}
- question_type: {QUESTION_TYPE}
- difficulty_profile: {DIFFICULTY_PROFILE}
- question_text: {QUESTION_TEXT}

### 정답 기준 / Fact Anchor

아래 내용을 기준으로 topic truth check를 설계한다.

    {FACT_ANCHORS_OR_MODEL_ANSWER}

### 수험생 오답 사례

아래 오답 사례에서 정답과 직접 충돌하는 주장을 추출한다.

    {WRONG_STUDENT_ANSWER_EXAMPLES}

### 정상 답안 또는 safe 예시

아래 표현은 좋은 답안 또는 허용 가능한 표현이다.
fatal regex가 아래 표현을 잘못 잡지 않도록 safe context를 고려한다.

    {SAFE_OR_GOOD_ANSWER_EXAMPLES}

### 현재 사용 중인 Logic Check Bank schema 참고

아래 schema 또는 기존 topic 구조를 참고하되, 금지 필드는 생성하지 않는다.

    {CURRENT_LOGIC_CHECK_JSON_SCHEMA_OR_EXISTING_TOPIC}

## 작성 단계

### 1. Topic 기본 정보

다음 필드를 작성한다.

- topic_id
- topic_name
- enabled
- question_type
- difficulty_profile
- topic_aliases

`topic_aliases`에는 한국어, 영어, 약어, 기호, 수험생이 자주 쓰는 표현을 포함한다.

### 2. Fatal Checks 작성

`fatal_checks`는 정답과 직접 충돌하는 오류만 포함한다.

각 fatal check는 다음 필드를 포함한다.

- id
- severity: "fatal"
- wrong_patterns
- message
- correct_rule
- affected_layers
- recommended_ceiling

작성 원칙:

- `wrong_patterns`는 정규식 문자열 배열이다.
- 너무 넓은 regex를 쓰지 않는다.
- 반드시 오답 표현과 정답 충돌이 동시에 드러나도록 작성한다.
- 단순히 특정 키워드가 등장했다는 이유만으로 fatal 처리하지 않는다.
- C 영역 핵심 오류는 `affected_layers`를 `["C"]`로 설정한다.
- THEORY_CORE fatal은 `recommended_ceiling: 10.0`을 사용한다.

### 3. Major Checks 작성

`major_checks`는 핵심 구성요소 누락 또는 불충분을 잡는다.

각 major check는 다음 필드를 포함한다.

- id
- severity: "major"
- required_patterns
- min_required
- message
- correct_rule
- affected_layers

작성 원칙:

- major는 score cap을 걸지 않는다.
- 정답 핵심 요소가 부족하지만 반대로 쓰지는 않은 경우에 사용한다.
- `required_patterns`는 핵심 정답 요소를 넓게 커버하되, 너무 느슨하게 만들지 않는다.
- `affected_layers`는 `["C"]`를 기본값으로 사용한다.

### 4. Question Type Checks 작성

`question_type_checks`는 문제 유형별 C 중심 요구 충족을 보조 확인한다.

각 check는 다음 필드를 포함한다.

- id
- severity: "minor" 또는 "major"
- question_type
- required_axes 또는 required_patterns
- min_required
- message
- affected_layers

작성 원칙:

- 비교·선정형은 비교축, 장단점, 적용 조건, 선정 기준을 요구할 수 있다.
- 원리·해석형은 작동 원리, 변수 관계, 인과관계, 수식 의미를 요구할 수 있다.
- 진단·대책형은 원인, 영향, 대책, 재발방지, 검증 기준을 요구할 수 있다.
- 적용·평가형은 절차, 구성, 적용 조건, 효과 평가, 한계를 요구할 수 있다.
- 단, 이 항목은 D/E 점수를 직접 평가하지 않는다.
- `affected_layers`에는 `D`, `E`를 넣지 않는다.

### 5. D/E Claim Trust Metadata 작성

Logic Check topic에는 `de_claim_trust`를 작성한다.

이 metadata는 D/E 점수를 변경하지 않는다.
Logic Check를 통과한 topic에 기반한 D/E 현장 적용 주장과 결론 주장을 이론적으로 신뢰할 수 있음을 표시한다.

필수 필드:

- enabled
- target_layers
- score_effect
- trust_effect
- pass_meaning
- fatal_meaning
- rule

예시 JSON 구조:

    {
      "de_claim_trust": {
        "enabled": true,
        "target_layers": ["D", "E"],
        "score_effect": "none",
        "trust_effect": "logic_pass_supports_d_e_claim_reliability",
        "pass_meaning": "이 topic의 핵심 이론·정의·수식 주장이 정답과 직접 충돌하지 않으므로, 이를 기반으로 한 D/E 현장 적용 주장과 결론 주장은 이론적으로 신뢰할 수 있다.",
        "fatal_meaning": "이 topic의 핵심 이론 주장이 정답과 충돌하므로, 이를 기반으로 한 D/E 현장 적용 주장과 결론 주장은 강하게 신뢰하지 않는다.",
        "rule": "Logic Check는 D/E를 직접 평가하지 않는다. D/E 점수는 A/B/C/D/E scoring model에서만 산정한다."
      }
    }

### 6. Next Practice Points 작성

`next_practice_points`에는 수험생이 다음 답안을 쓸 때 바로 적용할 수 있는 훈련 포인트를 3~5개 작성한다.

## 금지 필드

다음 필드는 생성하지 않는다.

- advanced_tradeoff_checks
- field_application_checks
- coherence_defense_checks
- d_e_feedback_templates

## 출력 형식

출력은 오직 valid JSON 객체 하나로 작성한다.
Markdown code block, 설명문, 주석은 출력하지 않는다.

출력 JSON 구조:

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
          "affected_layers": ["B", "C"]
        }
      ],
      "de_claim_trust": {
        "enabled": true,
        "target_layers": ["D", "E"],
        "score_effect": "none",
        "trust_effect": "logic_pass_supports_d_e_claim_reliability",
        "pass_meaning": "...",
        "fatal_meaning": "...",
        "rule": "Logic Check는 D/E를 직접 평가하지 않는다. D/E 점수는 A/B/C/D/E scoring model에서만 산정한다."
      },
      "next_practice_points": []
    }

## 검토 기준

- fatal regex가 너무 넓으면 안 된다.
- fatal은 반드시 정답과 직접 충돌해야 한다.
- safe condition이 필요한 내용은 Logic Check Profile 쪽에도 반영해야 한다.
- D/E는 `affected_layers`에 넣지 않는다.
- D/E 점수는 Logic Check에서 감점·가점하지 않는다.
- D/E와의 연결은 `de_claim_trust` metadata로만 표현한다.
- JSON은 `topic_logic_checks` 배열에 바로 넣을 수 있는 topic 객체여야 한다.
