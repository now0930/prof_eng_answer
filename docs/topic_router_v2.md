# Topic Router v2 설계·운영 문서

## 1. 목적

Topic Router v2는 산업계측제어기술사 채점 Bot에서 하나의 문제에 포함된 여러 요구사항을 분해하고, 각 요구사항을 적절한 Topic Pack 또는 General evidence에 연결하기 위한 라우팅 계층이다.

기존의 단일 Topic 중심 라우팅은 복합 문제에서 다음 한계가 있었다.

- 하나의 문제 안에 서로 다른 Topic 요구가 존재할 수 있다.
- 일부 요구는 Topic Pack에 포함되지만 일부 요구는 아직 Topic Pack이 없을 수 있다.
- Topic Pack 전체 내용을 문제의 필수 답안 체크리스트처럼 사용하면, 실제 문제에서 요구하지 않은 세부 항목까지 감점 기준으로 확장될 수 있다.
- 여러 Topic이 선택되더라도 기술사 한 문제는 하나의 답안이며 하나의 점수로 평가되어야 한다.

Topic Router v2는 이 문제를 해결하기 위해 **Question Demand 단위 분해 → Rule/Semantic Routing → deterministic routing policy → Topic/General evidence 구성 → 단일 A/B/C/D/E 채점** 흐름을 사용한다.

---

## 2. 핵심 설계 원칙

### 2.1 Question-first routing

라우팅은 학생 답안이나 채점 결과가 아니라 **문제 자체의 요구사항**으로 결정한다.

학생 답안에 특정 키워드가 있다는 이유로 Topic을 선택하거나, 점수가 낮다는 이유로 다른 Topic을 추가하지 않는다.

### 2.2 One question = one score

복수 Topic이 선택되어도 Topic별 점수를 합산하거나 평균하지 않는다.

최종 산출은 기존 채점 구조를 그대로 유지한다.

- A: 구조
- B: 요구 해석
- C: Fact 설명
- D: 현장 판단
- E: 연결성

즉, 하나의 문제에 대해 **하나의 A/B/C/D/E 평가와 하나의 총점**만 생성한다.

### 2.3 Topic evidence는 지식 근거이지 문제 범위가 아니다

Topic Pack의 `model_answer`와 `fact_anchor`는 채점에 사용할 수 있는 지식 근거다.

그러나 Topic Pack에 존재한다는 이유만으로 다음 항목을 자동으로 문제의 필수 요구사항으로 간주해서는 안 된다.

- expected structure
- high-score feature
- common missing point
- field connection
- 개별 fact anchor

문제 범위는 Question Demand가 결정하고, Topic evidence는 그 범위 안의 설명을 검증하는 데 사용한다.

### 2.4 GENERAL은 정상 모드다

Topic Pack이 없는 요구사항이 존재한다고 해서 Router 실패로 보지 않는다.

Topic coverage가 없으면 General evidence를 사용할 수 있으며, 이는 정상적인 grading path다.

### 2.5 AMBIGUOUS와 coverage gap은 다르다

- `AMBIGUOUS`: Router가 요구사항의 소유 Topic을 충분히 확정하지 못한 상태
- uncovered demand: 요구사항은 명확하지만 대응 Topic Pack이 없는 상태

두 상태를 혼동하지 않는다.

---

## 3. 전체 처리 흐름

```text
Question
  ↓
Question Demand decomposition
  ↓
Rule Candidate Router
  ↓
Semantic Router / LLM semantic adjudication
  ↓
Deterministic Routing Policy
  ↓
Runtime Mode
  ├─ SINGLE_TOPIC
  ├─ MULTI_TOPIC
  ├─ GENERAL
  └─ AMBIGUOUS
  ↓
Topic Evidence / General Evidence
  ↓
Gemini Semantic Grader
  ↓
A/B/C/D/E
  ↓
One Question / One Score
```

라우팅 단계와 채점 단계는 분리한다.

Router는 **어떤 evidence를 사용할지** 결정하고, Gemini Semantic Grader는 그 evidence와 문제 요구를 바탕으로 **한 번의 채점 결과**를 생성한다.

---

## 4. Runtime Mode

### 4.1 `SINGLE_TOPIC`

하나의 Topic Pack이 문제 요구를 담당하는 경우다.

또한 하나의 Topic이 일부 요구를 담당하고 나머지가 uncovered인 경우에도 Topic ownership 관점에서는 `SINGLE_TOPIC`이 유지될 수 있으며, uncovered 부분은 Hybrid General evidence로 보완한다.

### 4.2 `MULTI_TOPIC`

서로 다른 요구사항이 2개 이상의 Topic Pack에 명확히 매핑되는 경우다.

예:

```text
D1 → Topic A
D2 → Topic A
D3 → Topic B
```

Topic A와 Topic B의 evidence를 함께 제공하지만, **Topic A 점수 + Topic B 점수 방식으로 채점하지 않는다.**

### 4.3 `GENERAL`

적절한 Topic Pack을 선택하지 않는 것이 정상인 문제다.

GENERAL은 fallback failure가 아니라 정상적인 runtime mode다.

### 4.4 `AMBIGUOUS`

후보 Topic 간 우열이 충분히 확정되지 않아 deterministic routing policy가 명확한 소유 Topic을 결정하지 못한 경우다.

AMBIGUOUS를 Topic coverage 부족과 동일하게 취급하지 않는다.

---

## 5. 환경변수

Repository의 `.env.example`은 Router v2 기능 gate의 권장 기본값과 의미를 문서화한다.

실제 운영 `.env`는 deployment 환경에서 관리하며 repository에 저장하지 않는다.

```dotenv
QUESTION_DEMAND_SHADOW_ENABLED=true
SEMANTIC_ROUTER_SHADOW_ENABLED=true
ASSISTED_ROUTING_ENABLED=true
MULTI_TOPIC_GRADING_ENABLED=true
HYBRID_GENERAL_GRADING_ENABLED=true
```

### 5.1 `QUESTION_DEMAND_SHADOW_ENABLED`

문제를 D1, D2, D3 등의 독립 요구사항으로 분해한다.

이 demand가 이후 Router 판단의 기본 단위가 된다.

### 5.2 `SEMANTIC_ROUTER_SHADOW_ENABLED`

각 demand를 Topic Pack과 의미 기반으로 매핑한다.

Topic 후보와 confidence를 생성하며 Rule Router만으로 해결하기 어려운 표현 차이를 보완한다.

### 5.3 `ASSISTED_ROUTING_ENABLED`

Rule Router와 Semantic Router 결과를 실제 grading routing decision에 반영한다.

### 5.4 `MULTI_TOPIC_GRADING_ENABLED`

하나의 문제에 2개 이상의 Topic owner가 존재할 때 Multi-Topic evidence를 구성한다.

이 기능은 **복수 evidence 사용 기능**이며 복수 점수 기능이 아니다.

### 5.5 `HYBRID_GENERAL_GRADING_ENABLED`

일부 demand가 Topic에 매핑되고 일부 demand는 uncovered일 때, Topic evidence와 uncovered demand용 General evidence를 함께 제공한다.

---

## 6. Multi-Topic evidence 계약

`multi_topic_evidence_consumer.py`는 Multi-Topic model reference를 Gemini용 subject rubric에 연결한다.

실제 attach key는 다음과 같다.

```text
multi_topic_grading_evidence
```

대표적인 evidence metadata는 다음 구조를 가진다.

```json
{
  "version": "multi_topic_subject_evidence_v1",
  "routing_mode": "MULTI_TOPIC",
  "primary_topic_ids": [
    "topic_a",
    "topic_b"
  ],
  "uncovered_demand_ids": []
}
```

`MULTI_TOPIC` 활성 여부는 `applicable` 같은 별도 boolean 필드가 아니라 다음 값으로 판단한다.

```text
multi_topic_grading_evidence.routing_mode == "MULTI_TOPIC"
```

이 schema는 2026-08-08 production replay audit에서 실제 Gemini 입력 객체를 재구성하여 확인했다.

---

## 7. Demand-scoped grading 계약

Multi-Topic grading에서는 Topic evidence 전체를 그대로 Gemini에 제공할 수 있지만, **누락·완전성·개선사항 판단은 demand 범위로 제한**해야 한다.

핵심 규칙은 다음과 같다.

1. `model_answer`와 `fact_anchor`는 knowledge reference이며 checklist가 아니다.
2. semantic `demand_mappings`를 기준으로 각 Topic의 적용 범위를 결정한다.
3. omission, completeness, layer scoring, improvement advice는 해당 demand를 설명하는 데 필요한 세부사항만 요구한다.
4. Topic evidence에 존재한다는 이유만으로 out-of-scope anchor를 감점 또는 개선 요구로 사용하지 않는다.
5. 서로 다른 Topic 또는 서로 다른 demand 사이에 요구사항을 전이하지 않는다.
6. 같은 Topic에 여러 demand가 매핑된 경우 적용 범위는 해당 demand들의 union이다.
7. evidence는 in-scope demand를 검증할 수 있지만 문제 범위를 확장할 수 없다.
8. 학생이 실제로 작성한 명백한 factual error는 demand-scope와 별개로 감점할 수 있다.
9. Multi-Topic에서도 one-question-one-score 원칙을 유지한다.
10. missing-point 비판은 명시적인 demand 또는 그 demand를 설명하는 데 필수적인 내용으로 추적 가능해야 한다.

Gemini prompt에는 이 규칙을 `[MULTI_TOPIC_DEMAND_SCOPE_CONTRACT_V1]` 계약으로 주입한다.

---

## 8. 실제 결함 사례와 수리

### 8.1 시험 문제

실제 Telegram E2E에서 다음 복합 문제를 사용했다.

```text
스트레인 게이지와 로드셀의 측정 원리,
Wheatstone Bridge 및 온도 보상 방법을 설명하고,
계측설비 변경 시 변경관리 절차를 제시하시오.
```

Question Demand는 다음과 같이 분해되었다.

| Demand | 내용 | Topic |
|---|---|---|
| D1 | 스트레인 게이지 측정 원리 | strain/load-cell Topic |
| D2 | 로드셀 측정 원리 | strain/load-cell Topic |
| D3 | Wheatstone Bridge | strain/load-cell Topic |
| D4 | 온도 보상 | strain/load-cell Topic |
| D5 | 계측설비 변경관리 절차 | configuration/change-management Topic |

Semantic mapping confidence는 D1~D4가 `1.0`, D5가 `0.95`였다.

Routing 결과는 다음과 같았다.

```text
routing_mode=MULTI_TOPIC
primary_topic_ids=[
  strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error,
  configuration_change_release_backup_rollback_migration_obsolescence_management
]
uncovered_demand_ids=[]
```

### 8.2 발견된 오류

초기 Gemini feedback은 D5 변경관리 요구에 대해 다음과 같은 보완을 요구했다.

```text
편심하중
과부하
```

그러나 이 항목은 load-cell 설치 및 적용상의 리스크이며, 일반적인 계측설비 변경관리 절차의 필수 요구사항이 아니다.

즉 다음과 같은 cross-Topic contamination이 발생했다.

```text
Load-cell Topic 전체 evidence
        ↓
편심하중 / 과부하
        ↓
D5 변경관리의 누락 항목으로 잘못 전이
```

### 8.3 원인

원인은 두 단계로 확인되었다.

첫째, Gemini가 full Topic evidence를 문제의 답안 checklist처럼 사용할 수 있는 prompt 상태였다.

둘째, 이를 막기 위해 추가한 demand-scope prompt wrapper의 활성 조건이 실제 evidence schema와 맞지 않았다.

초기 helper는 다음과 같은 필드를 기대했다.

```text
multi_topic_grading_evidence.applicable
```

그러나 실제 attach evidence에는 `applicable`이 존재하지 않았다.

실제 authoritative signal은 다음이었다.

```text
multi_topic_grading_evidence.routing_mode = MULTI_TOPIC
```

따라서 prompt contract 자체는 존재했지만 production Gemini prompt에는 추가되지 않았다.

### 8.4 수리

활성 조건을 실제 evidence schema에 맞춰 다음 의미로 변경했다.

```text
multi_topic_grading_evidence.routing_mode == "MULTI_TOPIC"
```

Demand-scope contract의 내용은 유지했다.

수리 commit:

```text
609317bc76d66b4055c2b5efd079aba27130012d
fix: scope multi topic grading evidence by demand
```

---

## 9. Production E2E 수리 검증

수리 전 Gemini semantic prompt hash:

```text
75f0d740234730fc8e7b7a628a4292bc33462e8876f3830065b707a2ccc6c387
```

수리 후 Gemini semantic prompt hash:

```text
483e54aef558181e650e07624dca43c3cad51460815dc0db9f59940132e6a63f
```

따라서 수정된 demand-scope contract가 실제 Gemini 호출까지 전달된 것을 확인했다.

수리 후 raw Gemini response에서 다음 표현은 모두 제거되었다.

```text
편심하중
안전과부하
과부하 방지
```

반면 D5 변경관리 평가는 실제 문제 범위에 맞는 다음 항목으로 변경되었다.

```text
루프 체크
교정 성적서
인터록 테스트
Rollback
정지 시간
비용
운전 리스크
```

수리 전후 Routing은 변경되지 않았다.

```text
D1 → strain/load-cell Topic
D2 → strain/load-cell Topic
D3 → strain/load-cell Topic
D4 → strain/load-cell Topic
D5 → configuration/change-management Topic
```

즉 이번 수정은 Router mapping을 바꾸는 방식이 아니라 **올바르게 선택된 Topic evidence의 채점 적용 범위를 demand 단위로 제한한 수정**이다.

점수는 수리 전후 모두 `12.93/25.0`이었다.

이는 수리 실패가 아니다. 이번 결함의 acceptance criterion은 특정 점수 상승이 아니라 **out-of-scope cross-Topic 감점 및 improvement advice 제거**였다.

---

## 10. Gemini grading evidence 흐름

현재 grading orchestration의 핵심 순서는 다음과 같다.

```text
Question Type lens
  ↓
Model Answer Reference
  ↓
Multi-Topic context enrichment
  ↓
Hybrid General context enrichment
  ↓
subject_rubric_for_gemini 구성
  ↓
attach_multi_topic_evidence_to_subject_rubric(...)
  ↓
attach_hybrid_general_evidence_to_subject_rubric(...)
  ↓
_phase6_run_gemini_semantic_grader(...)
```

Multi-Topic context가 포함된 runtime `model_answer_reference`는 최종 `grade.json`에 포함된다.

주의할 점은 standalone `model_answer_reference.json`이 context enrichment 이전 시점에 persist될 수 있어, 최종 `grade.json.model_answer_reference`와 내용 차이가 있을 수 있다는 것이다.

재현 또는 감사 시에는 **최종 grading에 사용된 embedded model reference를 우선 확인**한다.

---

## 11. Evidence 사용 범위

Topic grading evidence는 다음 두 종류를 사용한다.

```text
model_answer
fact_anchor
```

다음 정보는 Topic selection이나 최종 scoring evidence를 임의로 확장하는 용도로 사용하지 않는다.

```text
logic_check
topic_importance
학생 답안의 키워드
학생 점수
```

Logic/importance 계층은 각각 정의된 별도 역할을 유지한다.

---

## 12. Coverage feedback

Topic coverage feedback은 grading score와 분리된 downstream feedback 계층이다.

핵심 원칙은 다음과 같다.

- uncovered demand가 있을 때만 coverage event의 근거가 된다.
- 기존 `question_type_coverage_score_adjustment`와 별도 기능이다.
- coverage feedback 자체가 Topic을 자동 생성하지 않는다.
- recurrence 판단은 동일 세션 반복이 아니라 distinct session 기준으로 관리한다.
- coverage gap이 존재하더라도 현재 문제의 점수는 기존 A/B/C/D/E grading contract에 따라 산출한다.

---

## 13. 운영 설정

### 13.1 `.env.example`

Repository의 `.env.example`은 Router v2 gate를 모두 `true` 권장값으로 문서화한다.

문서화 commit:

```text
b23ecffc88c8bdd25b7e321e68bd38758d33a850
docs: document Topic Router v2 environment gates
```

### 13.2 실제 `.env`

실제 API key, Telegram token, Router gate 등의 운영값은 deployment 환경의 `.env`에서 관리한다.

운영 `.env`는 repository에 commit하지 않는다.

### 13.3 Docker Compose 재적용

`.env` 값을 변경한 뒤 다음 명령만 실행하면 기존 컨테이너의 환경변수는 바뀌지 않을 수 있다.

```bash
docker compose restart prof-eng-answer-bot
```

환경변수 변경을 확실히 적용하려면 container recreate가 필요하다.

```bash
docker compose up -d --force-recreate prof-eng-answer-bot
```

재기동 후에는 container environment뿐 아니라 production Python gate 함수도 함께 확인한다.

---

## 14. 주요 구현 파일

현재 Router v2 흐름을 감사하거나 수정할 때 우선 확인할 파일은 다음과 같다.

```text
question_demand_shadow.py
semantic_router_shadow.py
assisted_routing.py
multi_topic_grading_context.py
multi_topic_evidence_consumer.py
hybrid_general_grading_context.py
hybrid_general_prompt.py
gemini_grader.py
grading_agents.py
```

Demand-scope prompt regression:

```text
scripts/test_multi_topic_demand_scope_prompt.py
```

---

## 15. 검증 원칙

Router v2 변경 시 최소한 다음 순서를 따른다.

### 15.1 Static validation

```text
py_compile
git diff --check
```

### 15.2 Focused regression

변경 계층에 해당하는 Router / evidence consumer / prompt regression을 우선 수행한다.

### 15.3 Repository validation

관련 validator와 release validation을 수행한다.

### 15.4 Container smoke

다음에 해당하는 경우 container smoke를 수행한다.

- 환경변수 gate 변경
- LLM 호출 경로 변경
- mount/runtime 차이 영향
- container-only dependency 영향

### 15.5 Real Telegram E2E

Prompt 또는 semantic grading contract를 변경한 경우 실제 Telegram grading E2E를 수행한다.

단순 점수 비교만 하지 않고 다음 artifact를 확인한다.

```text
routing_mode
primary_topic_ids
demand_mappings
uncovered_demand_ids
Gemini prompt_hash
Gemini raw response
최종 A/B/C/D/E 및 total score
```

특히 prompt 변경은 `prompt_hash`가 실제로 변경되는지 확인해야 한다.

---

## 16. 현재 완료 상태

2026-08-09 기준 다음 항목은 production 반영까지 완료되었다.

- Question Demand 기반 routing
- Semantic Router
- Assisted Routing
- `SINGLE_TOPIC`
- `MULTI_TOPIC`
- `GENERAL`
- `AMBIGUOUS`
- Multi-Topic grading evidence
- Hybrid General grading infrastructure
- Coverage feedback persistence/aggregation
- distinct-session recurrence
- Multi-Topic demand-scope grading contract
- Router v2 5개 feature gate 운영 활성화
- `.env.example` 환경변수 문서화
- 실제 Telegram Multi-Topic E2E
- cross-Topic contamination repair

현재 repository 상태 기준점:

```text
main = origin/main
HEAD = b23ecffc88c8bdd25b7e321e68bd38758d33a850
```

---

## 17. 남은 우선 검증

다음 우선순위는 **실제 Hybrid uncovered-demand production E2E**다.

검증해야 할 시나리오는 다음과 같다.

```text
Question
  ├─ D1 → Topic A
  ├─ D2 → Topic A
  └─ D3 → uncovered
```

기대 결과:

```text
routing_mode = SINGLE_TOPIC
Topic evidence = Topic A
Hybrid General evidence = D3 only
uncovered_demand_ids = [D3]
one question = one score
Stage 8 coverage event = uncovered D3 기준 생성
```

이 검증에서도 Topic evidence가 uncovered demand의 문제 범위를 침범하거나, General evidence가 Topic-covered demand를 중복 평가해서는 안 된다.

---

## 18. 변경 시 지켜야 할 불변조건

Router v2를 이후 확장할 때 다음 조건은 유지한다.

1. 학생 답안은 routing input이 아니다.
2. 점수는 routing input이 아니다.
3. 한 문제는 한 점수만 가진다.
4. Multi-Topic은 evidence aggregation이지 score aggregation이 아니다.
5. Topic Pack 전체가 문제의 자동 checklist가 아니다.
6. Question Demand가 grading scope의 기준이다.
7. uncovered demand는 General evidence로 처리할 수 있다.
8. GENERAL은 정상 모드다.
9. AMBIGUOUS와 coverage gap을 구분한다.
10. coverage feedback은 scoring과 분리한다.
11. prompt 수정은 실제 production `prompt_hash`까지 확인한다.
12. runtime gate 변경은 container recreate 후 production 함수까지 검증한다.
