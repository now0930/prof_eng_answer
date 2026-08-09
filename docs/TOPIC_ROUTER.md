# Topic Router 개발 현황 및 전체 로드맵

> 이 문서는 `README.md`와 분리된 Topic Router / Question Type / 채점 Architecture 운영 기준 문서이다.
> `README.md`는 기존 상태를 유지하며, 이후 Topic Router·Golden Set·Topic Pack 확장에 관한 진행 상태는 본 문서를 갱신한다.

## 1. 문서 목적

산업계측제어기술사 답안 채점 Bot의 현재 안정 상태를 기준선으로 확정하고, 향후 다음 작업을 일관된 절차로 수행하기 위한 운영 문서이다.

핵심 개발 방향은 다음과 같다.

1. 현재 4-QType 기반 채점 Architecture를 안정 기준선으로 유지한다.
2. 다음 최우선 작업으로 **4-QType Production Golden Set**을 구축한다.
3. Golden Set 구축 완료 후 Topic Pack을 추가한다.
4. Topic 추가 시 기존 Golden Regression을 반드시 수행한다.
5. 새로운 대표 위험·Router 충돌·출제 유형이 추가될 때 Golden Set도 함께 확장한다.
6. Production blocker가 아닌 기존 결함은 별도 Backlog로 분리한다.

---

## 2. 현재 안정 기준선

기준일: **2026-08-09**

```text
Repository:
https://github.com/now0930/prof_eng_answer

Branch:
main

Stable baseline:
49ac8e220404d9e9d277b601c21d21930b38d42a

Local HEAD:
49ac8e220404d9e9d277b601c21d21930b38d42a

origin/main:
49ac8e220404d9e9d277b601c21d21930b38d42a

Ahead:
0

Behind:
0

Worktree:
CLEAN
```

본 SHA를 **4-QType D/E Architecture의 최초 Production 안정 기준선**으로 사용한다.

---

## 3. 현재 채점 Architecture

전체 흐름은 다음과 같다.

```text
Question
  ↓
Question Demand 분석
  ↓
Question Type 판정
  ↓
Topic Router
  ↓
Routing Mode 결정
  ↓
Topic / General Evidence 구성
  ↓
A/B/C/D/E 평가
  ↓
Coverage / Fact Dependency / Logic 제한
  ↓
Originality 평가
  ↓
Rater 진단
  ↓
Question Type + Explicit Question Demand 기반 Feedback
  ↓
최종 25점 단일 점수
```

핵심 불변조건:

- **One Question = One Score**
- Question Router는 학생 답안이나 점수를 이용해 Topic을 선택하지 않는다.
- Topic evidence는 Model Answer와 Fact Anchor를 중심으로 구성한다.
- Hybrid는 별도 Runtime Mode가 아니라 **Evidence Composition 방식**이다.
- D/E의 최종 점수 owner와 public feedback owner를 분리한다.
- Difficulty는 Question Type이나 Question Demand를 확장하지 않는다.

---

## 4. Canonical Question Type

현재 Production 기준 Canonical Question Type은 4개이다.

| Type | 한글 | 핵심 평가 관점 |
|---|---|---|
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | 원리, 메커니즘, 수식, 해석, 조건·한계 |
| `COMPARE_SELECTION` | 비교·선정형 | 비교 기준, 장단점, 적용 조건, Trade-off, 선정 |
| `DIAGNOSIS_ACTION` | 진단·대책형 | 현상, 원인, 진단, 대책, 검증, 재발 방지 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | 적용, 설계 판단, 구현, 검증, 운영·평가 |

기존 DEFINE, PRINCIPLE, PROCEDURE, CALC_DESIGN, CAUSE_ACTION 등의 세분 유형은 신규 채점 정책의 Canonical Type으로 사용하지 않는다. 필요한 경우 기존 데이터 호환 목적으로만 취급한다.

---

## 5. A/B/C/D/E 기본 배점

기본 배점은 변경하지 않는다.

| Layer | 기본 의미 | 배점 |
|---|---|---:|
| A | 문제 진입·답안 구조 | 3 |
| B | 문제 요구 해석·완전성 | 6 |
| C | 유형별 Fact 기반 내용 설명 | 8 |
| D | 공학적 판단 영역 | 6 |
| E | 연결성·면접 방어 가능성 | 2 |
| **합계** |  | **25** |

D/E의 실제 평가 의미는 Question Type과 Explicit Question Demand에 의해 결정한다.

---

## 6. 4-QType D/E Policy Matrix

### 6.1 PRINCIPLE_INTERPRETATION

D의 핵심:

- 원리 이해
- 메커니즘 해석
- 수식과 변수 의미
- 원인 → 결과 관계
- 조건 및 한계
- 문제 요구 범위 내 공학적 판단

문제에서 요구하지 않았다면 현장 적용 사례, 비용, 경제성, 기존 설비 영향, 구체적 실행계획을 일반적인 고득점 필수조건으로 강요하지 않는다.

### 6.2 COMPARE_SELECTION

D의 핵심:

- 비교 기준
- 장단점
- 적용 조건
- Trade-off
- 선정 논리
- 최종 선택 근거

단순 차이점 나열보다 **왜 해당 조건에서 특정 대안을 선택하는가**를 중요하게 평가한다.

### 6.3 DIAGNOSIS_ACTION

D의 핵심:

- 현상
- 원인
- 진단
- 대책
- 검증
- 재발 방지

원인과 대책 사이의 논리적 연결을 중요하게 평가한다.

### 6.4 IMPLEMENTATION_EVALUATION

D의 핵심:

- 적용 방법
- 설계 판단
- 구현 조건
- 실행 가능성
- 검증 방법
- 운영 및 유지관리
- 문제에서 요구되는 경우 비용·기존 설비 영향

---

## 7. Explicit Question Demand 우선 원칙

Question Type은 전체적인 평가 관점을 결정하지만 실제 채점 범위는 문제에서 요구한 내용을 우선한다.

```text
Question Type
      +
Explicit Question Demand
      ↓
Actual Score / Feedback Scope
```

예를 들어 `PRINCIPLE_INTERPRETATION`이라도 문제에서 선정 기준, 보존기간, 폐기 원칙, 검증 방법 등을 명시적으로 요구하면 해당 항목은 정상 평가 대상이다.

---

## 8. D/E Score Ownership

현재 정책:

```text
A/B/C
→ Rater weighted scoring 적용 가능

D/E
→ Question Type 및 upstream semantic score가 numeric owner
→ Rater 결과는 diagnostic-only
```

3-Rater 결과가 authoritative D/E score를 다시 덮어쓰지 않는다.

---

## 9. Public Feedback Ownership

최종 public feedback owner:

```text
Question Type
+
Explicit Question Demand
```

Rater persona의 일반론은 내부 진단으로 유지할 수 있으나 최종 public feedback을 소유하지 않는다.

---

## 10. Difficulty 정책

```text
Difficulty ≠ Question Type
Difficulty ≠ Question Demand
Difficulty ≠ Public Feedback Scope Owner
```

Difficulty는 문제 난이도, 기대 답안 수준, Score ceiling, 평가 전략을 위한 독립 축이다.

---

## 11. Originality 정책

단순 요구사항 충족은 Originality가 아니다.

Originality는 조건에 따른 판단, Trade-off, 한계 인식, 독립적인 해석, 대안 선택 근거, 검증 가능한 추가 판단을 중심으로 평가한다.

Hybrid 문제에서는 General 영역의 내용이 Topic 영역 Originality Bonus를 부당하게 발생시키지 않도록 scope projection을 적용한다.

---

## 12. Topic Router / Runtime Mode

현재 주요 Runtime Mode:

```text
SINGLE_TOPIC
MULTI_TOPIC
GENERAL
AMBIGUOUS
```

Hybrid는 Runtime Mode가 아니다.

```text
Question Demand 분해
       ↓
Topic에서 평가 가능한 Demand
       +
General Evidence가 필요한 Demand
       ↓
Evidence Composition
       ↓
하나의 A/B/C/D/E Score
```

---

## 13. Fact Dependency

D/E 고득점은 C 영역의 Fact 정확성을 전제로 한다.

현재 `PRINCIPLE_INTERPRETATION` 중심 terminality 검증은 완료하였다. 향후 4개 유형 전체로 확대한다.

---

## 14. 현재까지 완료한 핵심 작업

### Question Type

- [x] Canonical Question Type 4종 정의
- [x] 4-QType D/E Policy Matrix
- [x] Explicit Demand override
- [x] Legacy Type 호환 경계 정리

### Score Ownership

- [x] D/E authoritative score owner 정리
- [x] 3-Rater D/E overwrite 차단
- [x] Rater candidate score 보존
- [x] D/E rater diagnostic-only 처리

### Feedback

- [x] Question Type-aware feedback
- [x] Explicit Question Demand feedback scope
- [x] Rater persona public feedback ownership 차단
- [x] Difficulty feedback scope 침범 차단
- [x] Generic field/cost advice projection

### Originality

- [x] Hybrid Originality scope
- [x] Question Type-aware Originality scope
- [x] Explicit Demand baseline double-credit 차단
- [x] Out-of-scope positive bonus 차단

### Regression / Release

- [x] Lane A/B/C 독립 개발
- [x] main 통합
- [x] Host focused regression
- [x] Full host release validation
- [x] Container runtime validation
- [x] Production 실제 재채점
- [x] 동일 답안 13.72점 재현
- [x] 신규 QType 정책 테스트 release coverage 등록
- [x] main 단일 push 및 local/remote SHA 동기화

---

## 15. Production Acceptance 기준 사례

```text
Score:
13.72 / 25.0

Question Type:
PRINCIPLE_INTERPRETATION

Requirement Coverage:
92.9%

Partial Demand:
result_meaning

Confidence:
high
```

동일 Production 환경 반복 결과:

```text
13.72
→
13.72
```

---

## 16. 알려진 Backlog

다음 Phase10 회귀 4건은 현재 QType 작업 이전 BASE에서도 존재하였다.

```text
test_phase10_logging_failure_preserves_valid_reference
test_phase10_persistence_failure_is_reported_and_preserves_result
test_phase10_router_failure_persists_fallback
test_phase10_success_persists_reference
```

현재 Production blocker로 취급하지 않으며 다음 별도 Backlog로 보류한다.

```text
Phase10 Model Answer Reference Contract Audit & Repair
```

---

# 17. 다음 최우선 작업: 4-QType Production Golden Set

상태:

```text
NEXT
```

목적:

> 향후 Router, Topic Pack, Score Policy, Feedback Policy를 변경할 때 기존 정상 채점 동작이 깨졌는지 즉시 판단할 수 있는 Production 기준선을 만든다.

---

## 18. Golden Set 초기 구성

```text
4 Question Types
×
3 Answer Levels
=
12 Golden Cases
```

답안 수준:

```text
LOW
PASS
HIGH
```

가능하면 각 Type에서 서로 다른 Topic을 사용해 특정 Topic 의존성을 낮춘다.

---

## 19. Golden Case 필수 필드

```text
case_id
question
answer_level
expected_question_type
expected_question_demands
expected_topic
expected_routing_mode
expected_evidence_scope
expected_A_range
expected_B_range
expected_C_range
expected_D_range
expected_E_range
expected_total_range
expected_coverage
expected_fact_cap_behavior
expected_originality_scope
required_feedback_characteristics
forbidden_feedback
```

LLM 기반 점수는 exact number보다 허용 범위를 중심으로 관리한다.

Question Type, Topic, Routing Mode, Question Demand, Critical Fact 판단, Fatal Logic 여부, Feedback Scope는 가능한 한 deterministic하게 유지한다.

---

## 20. Golden Set Acceptance

### Routing

```text
Question Type: 100% 목표
대표 Golden Topic: 100% 목표
Routing Mode: 100% 목표
```

### Score

```text
동일 답안 총점 반복 편차:
가능하면 ±0.5점 이내
```

### Feedback

- 요구하지 않은 평가기준을 강요하지 않는가
- 실제 부족한 Demand를 지적하는가
- Fact 오류를 정확히 지적하는가
- Question Type과 맞는 보완 방향인가
- 고득점 조건이 문제 요구범위를 벗어나지 않는가

---

# 21. Golden Set 구축 후 Topic 추가 정책

```text
Topic 후보 선정
    ↓
Fact Anchor 작성
    ↓
Model Answer 작성
    ↓
Logic Check 필요 여부 판단
    ↓
Topic Router 등록
    ↓
Question Type 매핑 확인
    ↓
Focused Validation
    ↓
4-QType Golden Regression
    ↓
새 Golden Case 필요 여부 판단
    ↓
Release Validation / 필요 시 Production E2E
    ↓
Commit / Release
```

---

## 22. Topic 추가 시 Golden Set 업데이트 기준

다음 중 하나에 해당하면 Golden Case 추가를 우선한다.

- 새로운 Question Type 행동을 검증해야 하는 Topic
- 기존 Topic과 Router 충돌 가능성이 높은 Topic
- Multi-topic 문제에 자주 결합되는 Topic
- Fact Dependency가 중요한 Topic
- Logic Fatal이 필요한 Topic
- 기출 빈도가 높은 Topic
- 채점 결과가 자주 흔들리는 Topic
- 산업계측제어기술사 핵심 출제영역

Golden Set은 Topic Pack 전체의 복사본이 아니라 **채점 Architecture의 대표 위험과 주요 출제 패턴을 커버하는 회귀 기준집**으로 운영한다.

---

# 23. 전체 개발 로드맵

## Phase 0. 4-QType Architecture 안정화

상태: **COMPLETE**

Baseline:

```text
49ac8e220404d9e9d277b601c21d21930b38d42a
```

## Phase 1. 4-QType Production Golden Set

상태: **NEXT**

- [ ] 4개 Question Type 대표 문제 선정
- [ ] LOW / PASS / HIGH 답안 구성
- [ ] Question Demand 기준 정의
- [ ] Expected Topic / Routing Mode 정의
- [ ] A/B/C/D/E 허용 범위 정의
- [ ] Forbidden Feedback 정의
- [ ] Production 반복 채점
- [ ] 재현성 측정
- [ ] Golden Dataset 확정
- [ ] Golden Regression Runner 구축
- [ ] Release validation 연결

## Phase 2. Topic Pack 확장 + Golden Set 동기화

상태: **PLANNED**

```text
Topic 추가
    ↓
Focused Validation
    ↓
Router Validation
    ↓
4-QType Golden Regression
    ↓
필요한 Golden Case 추가
    ↓
Release
```

## Phase 3. Question Type별 Score Calibration

상태: **PLANNED**

저득점 / 중간 / 합격권 / 고득점 답안을 축적하여 전문가 판단과 Bot 점수의 관계를 검증한다.

## Phase 4. Question Type-aware Output Label

상태: **PLANNED**

```text
PRINCIPLE_INTERPRETATION
D. 원리 해석·공학 판단
E. 논리 연결·설명 방어성

COMPARE_SELECTION
D. 비교·선정 판단
E. 선정 논리·방어성

DIAGNOSIS_ACTION
D. 진단·대책 타당성
E. 원인-대책 연결성

IMPLEMENTATION_EVALUATION
D. 적용·설계 판단
E. 실행 논리·검증 가능성
```

## Phase 5. Router Accuracy 고도화

상태: **PLANNED**

Question Type Router, Topic Router, Runtime Mode 및 Hybrid evidence composition을 Golden Set 기준으로 개선한다.

## Phase 6. Multi-topic / Hybrid 확대

상태: **PLANNED**

원리+비교, 원리+선정, 원인+대책, 설계+검증, 기술 설명+관리기준과 같은 복합 문제를 확대한다.

## Phase 7. 반복 채점 재현성 정량화

상태: **PLANNED**

Question Type, Topic, Routing Mode, 총점, Layer, Coverage, Originality 변동을 기록한다.

## Phase 8. Fact Dependency Cap 전 유형 확대

상태: **PLANNED**

4개 Type 전체에서 Fact 오류가 D/E 고득점으로 우회되지 않는지 검증한다.

## Phase 9. Feedback 품질 고도화

상태: **PLANNED**

최종 출력이 다음에 직접 답하도록 개선한다.

1. 왜 이 점수인가?
2. 무엇이 부족한가?
3. 어떻게 해야 17~20점 수준으로 올라가는가?

## Phase 10. Repository / Documentation 지속 정비

상태: **ONGOING**

- 완료 Worktree 정리
- 완료 Branch 정리
- Topic Router 문서 최신화
- Golden Set 문서 최신화
- Topic 현황 최신화
- Release Validation 절차 최신화
- Legacy 설명 제거 또는 Compatibility 표시

`README.md`는 별도 요청이 없는 한 본 Topic Router 운영 문서 갱신 과정에서 수정하지 않는다.

## Phase 11. Phase10 기존 회귀 Backlog

상태: **DEFERRED**

```text
Phase10 Model Answer Reference Contract Audit & Repair
```

---

# 24. 향후 기본 개발 Cycle

```text
Topic 선정
   ↓
Fact / Model / Logic 작성
   ↓
Focused Validation
   ↓
Router / Question Type 검증
   ↓
4-QType Golden Regression
   ↓
Golden Case 추가 필요 판단
   ↓
Release Validation / E2E
   ↓
Release
   ↓
TOPIC_ROUTER.md 진행 상태 갱신
```

---

# 25. 우선순위

```text
P0
4-QType Architecture 안정 Baseline
→ COMPLETE

P1
4-QType Production Golden Set
→ NEXT

P2
Topic Pack 추가 + Golden Set 지속 업데이트

P3
Question Type별 Score Calibration

P4
Question Type-aware Output Label

P5
Router Accuracy 개선

P6
Multi-topic / Hybrid 확대

P7
반복 채점 재현성 정량화

P8
Fact Dependency Cap 전 유형 검증

P9
Feedback 품질 개선

P10
Repository / Documentation 지속 정리

BACKLOG
Phase10 기존 회귀 4건 독립 감사 및 수리
```

---

# 26. 문서 갱신 규칙

본 문서는 다음 경우 반드시 갱신한다.

1. Stable baseline SHA 변경
2. Golden Set Case 추가·삭제·변경
3. 신규 Topic Pack Production 반영
4. Router 정책 변경
5. Question Type 정책 변경
6. Score / Feedback ownership 변경
7. Production Acceptance 기준 변경
8. 주요 Backlog 해결 또는 신규 등록

Topic 추가 시 최소 갱신 항목:

```text
Current baseline
Topic status
Golden regression status
New Golden case 여부
Known conflicts / router ambiguity
Release validation status
```

---

# 27. 현재 다음 작업

```text
CURRENT BASELINE
49ac8e220404d9e9d277b601c21d21930b38d42a

NEXT
4-QType Production Golden Set 구축

AFTER GOLDEN SET
Topic Pack 추가
→ Golden Regression
→ 필요한 Golden Case 추가
→ Release
→ TOPIC_ROUTER.md 갱신

DEFERRED
Phase10 기존 회귀 4건
```

현재부터 본 문서를 Topic Router 및 채점 Architecture 확장의 기준 문서로 사용한다.
