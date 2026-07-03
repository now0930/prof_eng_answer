# Logic Check Profile Generator Prompt

이 문서는 `rubrics/logic_check_profiles/industrial_instrumentation_control.json`에 추가할 수 있는 LLM verifier profile 초안을 생성하기 위한 프롬프트다.

Logic Check Profile은 일반 채점 rubric이 아니다.
Logic Check Profile은 답안에서 candidate evidence를 추출하고, truth schema와 비교하여 topic별 핵심 이론·정의·수식·논리 오류를 검증하기 위한 LLM verifier용 지식 구조다.

## 1. 파일 역할

| 파일 | 역할 |
|---|---|
| `rubrics/logic_checks/industrial_instrumentation_control.json` | Python rule 기반 topic truth check, regex check, fallback check, D/E claim trust metadata |
| `rubrics/logic_check_profiles/industrial_instrumentation_control.json` | LLM verifier용 truth schema, fatal condition, safe condition, evidence extraction profile |

## 2. 핵심 원칙

1. Logic Check Profile은 D/E를 직접 평가하지 않는다.
2. D/E 점수는 A/B/C/D/E scoring model에서만 산정한다.
3. Logic Check Profile은 topic truth gate를 위한 verifier 지식만 제공한다.
4. 정답과 직접 충돌하는 핵심 이론 오류만 fatal로 본다.
5. 단순 누락, 설명 부족, 표현 미흡은 fatal로 분류하지 않는다.
6. 좋은 답안에도 등장할 수 있는 표현은 safe condition으로 보호한다.
7. 근사값, 현장 최적점, 관용 표현은 fatal과 분리한다.
8. 표 답안은 단순 문자열이 아니라 `구분명 => 값` claim 구조로 해석한다.
9. diagram, table, formula answer는 candidate evidence 단위로 추출한다.
10. D/E와의 연결은 profile에서 채점하지 않고, Logic Check Bank의 `de_claim_trust` metadata로만 표현한다.
11. Logic Check finding의 `affected_layers`에는 원칙적으로 `A`, `B`, `C`만 사용한다.
12. `D`, `E`는 `affected_layers`가 아니라 `de_claim_trust.target_layers`로만 연결한다.
13. LLM verifier가 confidence가 낮으면 fatal을 강제하지 않는다.
14. Python regex check와 LLM verifier는 서로 보완하되, D/E 직접 평가를 생성하지 않는다.

## 3. 입력 정보

### 문항 정보

- topic_id: {TOPIC_ID}
- topic_name: {TOPIC_NAME}
- question_type: {QUESTION_TYPE}
- difficulty_profile: {DIFFICULTY_PROFILE}
- question_text: {QUESTION_TEXT}

### 정답 기준 / Fact Anchor / Model Answer

아래 내용을 기준으로 truth schema를 구성한다.

    {FACT_ANCHORS_OR_MODEL_ANSWER}

### 수험생 오답 사례

아래 사례에서 정답과 직접 충돌하는 claim을 추출한다.

    {WRONG_STUDENT_ANSWER_EXAMPLES}

### 정상 답안 또는 safe 예시

아래 표현은 좋은 답안 또는 허용 가능한 표현이다.
fatal condition이 아래 표현을 오탐하지 않도록 safe condition을 만든다.

    {SAFE_OR_GOOD_ANSWER_EXAMPLES}

### 현재 사용 중인 Logic Check Profile schema 참고

아래 기존 profile 구조를 참고하되, D/E 직접 평가 항목은 생성하지 않는다.

    {CURRENT_LOGIC_CHECK_PROFILE_SCHEMA_OR_EXISTING_TOPIC}

## 4. 작성 대상

생성할 profile topic은 다음 목적을 가져야 한다.

- 답안에서 핵심 claim을 추출한다.
- claim이 truth schema와 직접 충돌하는지 확인한다.
- fatal condition과 safe condition을 분리한다.
- 표, 수식, 도식, 문장형 답안을 모두 candidate evidence로 해석한다.
- LLM verifier가 C 중심의 topic truth를 판단하게 한다.
- D/E는 채점하지 않고, topic truth 결과가 D/E claim trust에 활용될 수 있음을 metadata 수준에서만 남긴다.

## 5. Profile 기본 필드

다음 필드를 작성한다.

- topic_id
- topic_name
- enabled
- difficulty_profile
- question_type
- topic_aliases
- verifier_scope
- candidate_evidence_schema
- truth_schema
- fatal_conditions
- safe_conditions
- ambiguity_policy
- output_policy

## 6. candidate_evidence_schema 작성 기준

candidate evidence는 답안에서 LLM verifier가 비교할 수 있는 최소 claim 단위다.

포함할 수 있는 claim type:

- definition_claim
- formula_claim
- region_classification_claim
- causal_claim
- comparison_claim
- table_row_claim
- diagram_label_claim
- selection_claim
- conclusion_claim

주의 사항:

1. table 답안은 row 단위로 claim을 추출한다.
2. 수식 답안은 기호와 의미를 함께 추출한다.
3. diagram 답안은 label, arrow, axis, region, boundary를 claim으로 추출한다.
4. conclusion claim은 C 영역 truth와 직접 연결될 때만 검증한다.
5. 현장 적용 claim은 D 점수로 평가하지 않고, 그 전제가 되는 C 영역 truth만 검증한다.

## 7. truth_schema 작성 기준

truth schema는 topic별로 반드시 맞아야 하는 핵심 사실이다.

각 truth item은 다음 정보를 포함한다.

- id
- statement
- canonical_terms
- acceptable_variants
- unacceptable_conflicts
- claim_type
- severity_if_contradicted

작성 원칙:

1. 핵심 이론·정의·수식·구간·분류를 우선한다.
2. 좋은 답안에서 다르게 표현될 수 있는 표현은 acceptable_variants에 넣는다.
3. 정답과 직접 반대되는 표현은 unacceptable_conflicts에 넣는다.
4. 단순 누락은 fatal로 보지 않는다.
5. 이론 전제를 무너뜨리는 오류만 fatal 후보로 둔다.

## 8. fatal_conditions 작성 기준

fatal condition은 정답과 직접 충돌하는 경우만 작성한다.

각 fatal condition은 다음 정보를 포함한다.

- id
- description
- trigger_claim_pattern
- why_fatal
- related_truth_ids
- recommended_severity
- recommended_ceiling

작성 원칙:

1. `recommended_severity`는 보통 `fatal`이다.
2. THEORY_CORE topic의 핵심 오류는 `recommended_ceiling: 10.0`을 사용한다.
3. safe condition에 걸리는 표현은 fatal로 판단하지 않는다.
4. confidence가 낮으면 fatal을 강제하지 않는다.
5. D/E 부족, 현장성 부족, 면접 방어 부족은 fatal condition에 넣지 않는다.

## 9. safe_conditions 작성 기준

safe condition은 오탐 방지를 위한 보호 규칙이다.

각 safe condition은 다음 정보를 포함한다.

- id
- description
- safe_claim_pattern
- why_safe
- related_truth_ids

작성 원칙:

1. 현장 최적점과 표준 정의를 구분한다.
2. 근사값과 정확한 정의를 구분한다.
3. 관용 표현과 정답 충돌 표현을 구분한다.
4. 좋은 답안에도 등장하는 표현은 safe로 보호한다.
5. 단순히 특정 숫자나 키워드가 등장했다는 이유로 fatal 처리하지 않는다.

## 10. ambiguity_policy 작성 기준

ambiguity_policy는 LLM verifier가 애매한 답안을 처리하는 방법이다.

권장 정책:

- 명시적 충돌이 없으면 fatal로 판단하지 않는다.
- 단순 누락은 major 또는 minor 후보로만 본다.
- candidate evidence가 부족하면 insufficient_evidence로 둔다.
- confidence가 낮으면 safe 쪽으로 판단한다.
- 수식 표기가 다르더라도 의미가 같으면 safe로 판단한다.
- ASCII 수식과 Unicode 수식을 모두 허용한다.

## 11. output_policy 작성 기준

output_policy는 verifier가 반환해야 하는 결과를 정의한다.

필수 출력 요소:

- applicable
- confidence
- mode
- fatal_error_detected
- candidate_claims
- matched_truth_ids
- violated_truth_ids
- findings
- safe_reasoning
- verifier_notes

주의 사항:

1. D/E 점수는 출력하지 않는다.
2. D/E 감점·가점 문구를 출력하지 않는다.
3. D/E와의 연결은 `de_claim_trust_reference` 같은 metadata 설명으로만 표현한다.
4. finding의 affected layer는 C 중심으로 둔다.
5. B/C 보조 진단은 가능하지만, D/E 직접 평가는 금지한다.

## 12. D/E claim trust reference

Profile에는 필요한 경우 다음 수준의 설명만 포함한다.

    "de_claim_trust_reference": {
      "enabled": true,
      "score_effect": "none",
      "meaning": "이 profile의 topic truth 검증 결과는 Logic Check Bank의 de_claim_trust metadata에서 D/E 주장 신뢰도 판단의 근거로만 사용된다. D/E 점수는 A/B/C/D/E scoring model에서만 산정한다."
    }

이 필드는 D/E 평가 항목이 아니다.
이 필드는 profile이 D/E scoring을 하지 않는다는 경계 표시다.

## 13. 생성 금지 항목

다음 성격의 항목은 생성하지 않는다.

- D/E 직접 평가 항목
- 현장 적용 부족 감점 항목
- 면접 방어 부족 감점 항목
- 고급 키워드 trade-off 부족 감점 항목
- D/E feedback template
- field application feedback block
- coherence defense feedback block
- advanced trade-off feedback block

## 14. 출력 JSON 구조 예시

출력은 오직 valid JSON 객체 하나로 작성한다.
Markdown code block, 설명문, 주석은 출력하지 않는다.

    {
      "topic_id": "...",
      "topic_name": "...",
      "enabled": true,
      "difficulty_profile": "THEORY_CORE",
      "question_type": "PRINCIPLE_INTERPRETATION",
      "topic_aliases": [],
      "verifier_scope": {
        "purpose": "topic truth verification",
        "does_not_score_d_or_e": true,
        "score_effect": "none"
      },
      "candidate_evidence_schema": {
        "claim_types": [
          "definition_claim",
          "formula_claim",
          "region_classification_claim",
          "causal_claim",
          "comparison_claim",
          "table_row_claim",
          "diagram_label_claim",
          "selection_claim",
          "conclusion_claim"
        ],
        "extraction_rules": []
      },
      "truth_schema": [
        {
          "id": "T1",
          "statement": "...",
          "canonical_terms": [],
          "acceptable_variants": [],
          "unacceptable_conflicts": [],
          "claim_type": "definition_claim",
          "severity_if_contradicted": "fatal"
        }
      ],
      "fatal_conditions": [
        {
          "id": "F1",
          "description": "...",
          "trigger_claim_pattern": "...",
          "why_fatal": "...",
          "related_truth_ids": ["T1"],
          "recommended_severity": "fatal",
          "recommended_ceiling": 10.0
        }
      ],
      "safe_conditions": [
        {
          "id": "S1",
          "description": "...",
          "safe_claim_pattern": "...",
          "why_safe": "...",
          "related_truth_ids": ["T1"]
        }
      ],
      "ambiguity_policy": {
        "default_when_uncertain": "do_not_force_fatal",
        "missing_information": "insufficient_evidence",
        "low_confidence": "safe_or_warn"
      },
      "output_policy": {
        "does_not_score_d_or_e": true,
        "finding_layers": ["A", "B", "C"],
        "score_effect": "none",
        "de_claim_trust_reference_only": true
      },
      "de_claim_trust_reference": {
        "enabled": true,
        "score_effect": "none",
        "meaning": "이 profile의 topic truth 검증 결과는 D/E claim trust metadata의 근거로만 사용된다."
      }
    }

## 15. 최종 검토 기준

- D/E를 직접 평가하지 않는가
- D/E 점수를 감점·가점하지 않는가
- field application, coherence defense, advanced trade-off를 별도 평가 블록으로 만들지 않았는가
- affected layer에 D/E를 넣지 않았는가
- fatal condition은 정답과 직접 충돌하는가
- safe condition이 좋은 답안을 보호하는가
- 표, 수식, 도식 답안을 claim으로 해석할 수 있는가
- confidence가 낮을 때 fatal을 강제하지 않는가
- JSON은 profile bank에 바로 넣을 수 있는 구조인가
