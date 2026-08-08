# Topic Router v2 설계 원칙

## 1. 목적

Topic Router v2의 목표는 문제와 가장 비슷한 Topic 하나를 무조건 고르는 것이 아니다.

목표는 문제의 요구사항을 분석하여 실제 채점에 필요한 Topic evidence를 안전하게 결정하는 것이다.

```text
Question
    ↓
Question Demand
    ↓
Rule-based Candidate Router
    ↓
LLM Semantic Adjudication
    ↓
Deterministic Routing Policy
    ↓
SINGLE_TOPIC / MULTI_TOPIC / GENERAL / AMBIGUOUS
    ↓
Topic Evidence + General Evidence
    ↓
Grading
```

기본 원칙은 다음과 같다.

> Rule은 후보 검색과 안전장치를 담당하고, LLM은 의미 판단을 담당하며, 최종 적용은 deterministic policy가 검증한다.

## 2. 현재 Router에서 유지할 기반

현재 deterministic Router의 후보 생성·방어 기능은 버리지 않는다.

유지할 주요 신호와 기능은 다음과 같다.

- Question Type
- Fact-derived `topic_id`
- 질문 내 topic/alias 신호
- `question_examples`
- `topic_aliases`
- `field_connection_points`
- 답안의 alias/field 신호는 약한 보조 evidence로만 사용
- candidate score
- top score / second score / margin
- Top-K candidate
- `matched`
- `ambiguous`
- `unmatched`

현재 Router의 핵심 장점은 **재현성, 회귀 테스트 가능성, weak/ambiguous candidate 거부**다. v2는 이를 대체하지 않고 확장한다.

## 3. Rule 기반 계층의 책임

Rule 계층은 다음을 담당한다.

### 3.1 Candidate generation

전체 Topic inventory에서 Top-K 후보를 만든다.

사용 가능한 evidence:

- question text
- question type
- fact-derived topic signal
- exact/normalized topic 표현
- aliases
- representative question examples
- field connection points

### 3.2 Guard

Rule은 다음 안전장치를 가진다.

- 존재하지 않는 `topic_id` 거부
- minimum score
- candidate 수 제한
- score/margin 계산
- alias collision 방어
- answer contamination 방어
- LLM 출력 schema 검사
- LLM이 Rule 후보 밖 Topic을 임의 생성하는 행위 차단
- 최종 fallback 실행

### 3.3 Final enforcement

LLM 결과는 제안이다. production routing contract를 만족하는지 Rule이 다시 확인한 뒤 적용한다.

## 4. LLM의 역할

LLM은 deterministic candidate search를 대체하지 않는다. LLM은 **semantic adjudication layer**다.

### 4.1 Question Demand Decomposition

LLM의 첫 번째 역할은 문제를 요구사항 단위로 분해하는 것이다.

예:

```text
문제:
열전대와 RTD의 측정원리, 주요 오차 및 적용상의 차이를 설명하시오.

Demands:
D1. 열전대 측정원리
D2. RTD 측정원리
D3. 열전대 주요 오차
D4. RTD 주요 오차
D5. 적용 특성 비교
```

Demand는 문제에서 추출한다. 학생 답안을 기준으로 새로운 demand를 만들지 않는다.

### 4.2 Topic Sheet 기반 의미 판정

LLM에는 전체 Topic Pack을 무제한으로 제공하지 않는다.

Rule이 고른 Top-K 후보에 대해 다음 semantic catalog를 제공한다.

- `topic_id`
- title
- positive ownership
- negative boundary
- core facts
- representative questions
- adjacent Topic boundary

Topic Sheet가 이 semantic catalog의 기준 문서가 된다.

### 4.3 SINGLE과 MULTI 구분

낮은 score margin은 두 의미를 가질 수 있다.

- **AMBIGUOUS**: A인지 B인지 판단하기 어렵다.
- **MULTI_TOPIC**: 문제에서 A와 B를 실제로 둘 다 요구한다.

LLM은 question demand와 Topic Sheet의 ownership을 비교하여 이를 구분한다.

### 4.4 Demand-to-Topic mapping

복합 문제에서는 Topic 목록만 선택하지 않고 각 demand가 어떤 Topic evidence로 검증되는지 연결한다.

```text
D1 → Topic A / PRIMARY
D2 → Topic B / PRIMARY
D3 → Topic A + Topic C / SUPPORTING
D4 → uncovered
```

이 결과는 향후 multi-topic Fact Anchor와 Logic Check selection의 입력이 된다.

### 4.5 GENERAL 판단

LLM은 가장 가까운 Topic을 강제로 고르지 않는다.

기존 후보가 문제 요구사항을 충분히 설명하지 못하면 `GENERAL`을 제안할 수 있어야 한다.

## 5. LLM이 하지 않는 일

LLM Router는 다음 권한을 갖지 않는다.

1. 존재하지 않는 Topic 생성
2. Topic Sheet/Topic Pack의 의미 범위 변경
3. 새로운 Fact Anchor 생성
4. 학생 답안을 기준으로 문제 Topic 변경
5. 후보 evidence가 부족한데 강제 Topic 선택
6. 채점 점수 직접 결정
7. PRIMARY/SECONDARY classification 문서를 runtime에서 임의 변경
8. coverage 상태를 자동 확정

Router의 책임은 **무엇을 근거로 채점할 것인지 결정하는 것**까지다.

## 6. Routing Mode

v2는 최소 네 가지 routing mode를 구분한다.

### SINGLE_TOPIC

문제의 핵심 demand를 하나의 Topic이 충분히 소유한다.

### MULTI_TOPIC

문제가 둘 이상의 Topic을 명시적·실질적으로 함께 요구한다.

### GENERAL

문제의 의미는 명확하지만 현재 Topic evidence가 충분하지 않다.

### AMBIGUOUS

문제 자체의 정보가 부족하거나 후보 간 의미 경계를 안정적으로 결정할 수 없다.

`GENERAL`과 `AMBIGUOUS`를 혼동하지 않는다.

## 7. PRIMARY / SUPPORTING / NONE

Multi-topic candidate는 동일한 권한을 갖지 않는다.

- **PRIMARY**: 문제에서 직접 요구하는 핵심 Topic
- **SUPPORTING**: 핵심 demand를 설명하는 데 필요한 보조 Topic
- **NONE**: 관련 용어는 있지만 이 문제의 positive grading evidence로 사용하면 안 되는 Topic

이는 `docs/topic_pack_classification.md`의 공식 criterion PRIMARY/SECONDARY와 별개의 runtime 역할이다.

즉 다음 두 개념을 구분한다.

```text
Classification PRIMARY/SECONDARY
= 공식 criterion ↔ Topic ownership

Runtime PRIMARY/SUPPORTING
= 이번 실제 문제 ↔ Topic evidence 역할
```

## 8. Topic Evidence Coverage

향후 v2는 문제 demand 중 Topic-specific evidence로 설명 가능한 범위를 측정한다.

예:

```text
D1 → Topic evidence
D2 → Topic evidence
D3 → Topic evidence
D4 → General
D5 → General
```

이때 `topic_evidence_coverage`를 기록할 수 있다.

초기에는 threshold를 고정하지 않는다. 기출·회귀 데이터를 통해 calibration한다.

향후 정책 예시는 다음과 같다.

```text
높은 Topic evidence coverage
→ Topic-aware grading

중간 coverage
→ Hybrid grading

낮은 coverage
→ General grading
```

숫자 threshold는 empirical validation 후 결정한다.

## 9. LLM 출력 계약 방향

LLM 결과는 free-form prose가 아니라 구조화된 결과로 제한한다.

개념 예:

```json
{
  "routing_mode": "MULTI_TOPIC",
  "demands": [
    {
      "id": "D1",
      "text": "캐비테이션 발생 메커니즘",
      "topic_id": "control_valve_cavitation_flashing_choked_flow_damage_prevention",
      "role": "PRIMARY",
      "confidence": 0.96
    },
    {
      "id": "D2",
      "text": "동특성 영향",
      "topic_id": "control_valve_deadband_stiction_response_time_positioner_dynamic_performance",
      "role": "SUPPORTING",
      "confidence": 0.74
    }
  ],
  "uncovered_demands": []
}
```

실제 schema는 구현 단계에서 별도 version으로 고정한다.

## 10. Rule-LLM-Rule sandwich

최종 architecture는 다음 원칙을 따른다.

```text
Rule
- candidate generation
- deterministic evidence
        ↓
LLM
- demand decomposition
- semantic comparison
- single/multi/general proposal
        ↓
Rule
- schema validation
- allowed topic validation
- confidence/coverage policy
- final routing enforcement
```

LLM은 semantic reasoning을 제공하지만 최종 production contract의 집행자는 deterministic code다.

## 11. General fallback

Topic Pack이 없거나 Topic evidence가 부족해도 채점 자체를 중단하지 않는다.

```text
Topic-specific evidence 충분
→ Topic-aware grading

복합 문제
→ Multi-topic evidence

일부 demand만 Topic으로 설명
→ Hybrid

Topic evidence 부족
→ General
```

General path에서는 특정 Topic의 Fact Anchor를 억지로 적용하지 않는다.

General 결과는 향후 taxonomy/coverage 개선을 위한 feedback으로 기록할 수 있다.

## 12. 단계적 도입

### Phase 1 — Shadow Mode

기존 Router가 production routing을 계속 담당한다.

LLM Router는 동일 문제에 대해 결과만 생성·저장한다.

비교 항목:

- legacy primary Topic
- LLM routing mode
- LLM PRIMARY/SUPPORTING
- uncovered demand
- false routing
- ambiguous vs multi 구분

### Phase 2 — Ambiguous / Unmatched 보완

기존 Router가 `ambiguous` 또는 `unmatched`일 때 LLM semantic adjudication을 사용한다.

### Phase 3 — Multi-Topic

검증된 LLM demand mapping을 이용해 둘 이상의 Topic evidence를 실제 채점에 사용한다.

### Phase 4 — Hybrid General

Topic evidence로 설명되지 않는 demand만 General evaluator에 넘긴다.

### Phase 5 — Coverage Feedback

반복되는 GENERAL/uncovered demand를 분석하여 다음 중 하나로 분류한다.

- Router/alias 개선
- 기존 Topic Sheet 범위 확장
- source anomaly repair
- 공식 criterion PARTIAL/GAP
- 신규 Topic 후보

## 13. 검증 원칙

Router v2 변경은 최소 다음 회귀군을 유지한다.

- 명확한 single-topic 문제
- alias만 다른 동일 의미 문제
- 인접 Topic contamination
- answer contamination
- tied candidate
- weak candidate
- 명확한 compare/multi-topic 문제
- 기존 Topic으로 덮이지 않는 General 문제
- problem wording이 모호한 Ambiguous 문제

동일 입력에 대한 routing 재현성과 structured output schema를 검증한다.

LLM을 사용하는 단계에서는 deterministic sampling 설정과 실패 fallback을 명시한다.

## 14. 최종 운영 원칙

1. Rule Router를 제거하지 않는다.
2. LLM은 semantic adjudication에 집중한다.
3. 문제 요구사항은 답안이 아니라 question에서 추출한다.
4. LLM은 Rule Top-K와 Topic Sheet semantic boundary를 기준으로 판단한다.
5. 명확한 복합 문제를 ambiguous로 처리하지 않는다.
6. evidence가 부족하면 강제 매칭하지 않는다.
7. LLM 출력은 deterministic policy가 검증한 후에만 사용한다.
8. Topic-specific evidence와 General evidence의 출처를 구분한다.
9. GENERAL/uncovered demand를 향후 coverage 개선 feedback으로 활용한다.
10. 처음에는 shadow mode로 도입하고 검증 후 production 권한을 점진적으로 확대한다.
