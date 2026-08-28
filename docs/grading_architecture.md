# Grading Architecture

이 문서는 현재 `prof_eng_answer`의 채점 pipeline과 점수 소유권을 설명한다.

세부 provider 설정은 `llm_provider.md`, Difficulty와 ceiling은 `difficulty_and_selection_strategy.md`, Question Type은 `question_type_taxonomy.md`, Topic Pack 구조는 `topic_pack_architecture.md`를 우선한다.

## 1. 기본 원칙

기술사 답안은 단순 키워드 포함 여부가 아니라 다음을 함께 평가한다.

- 문제 요구를 직접 충족하는가
- 핵심 Fact가 정확한가
- 원리·수식·조건과 결과를 논리적으로 연결하는가
- 현장 적용 조건, 리스크, 비용, 유지보수성을 판단하는가
- 결론과 제언이 Fact에서 도출되는가
- 같은 오류를 여러 layer에서 중복 감점하지 않는가
- 최종 저장 객체와 Telegram 출력 객체가 일치하는가

점수의 canonical owner는 A/B/C/D/E layer다. Question Type, Fact Anchor, Model Answer, Logic Check, deterministic checker와 Difficulty는 근거·보정·제한을 제공한다.

## 2. A/B/C/D/E 25점 구조

| Layer | 이름 | 배점 | 평가 초점 |
|---|---|---:|---|
| A | 문제 진입·답안 구조 | 3 | 배경, 핵심 쟁점, 목차와 답안 구조 |
| B | 문제 요구 해석·완전성 | 6 | 요구동사, 세부 요구, 직접 응답과 완전성 |
| C | 유형별 Fact 기반 내용 설명 | 8 | 핵심 Fact, 원리, 식, 조건, 인과관계의 정확성 |
| D | 현장 적용·설계 판단·제언 | 6 | 적용조건, trade-off, 비용, 리스크, 검증 가능성 |
| E | 연결성·면접 방어 가능성 | 2 | 문단 연결, 결론, 근거의 방어 가능성 |
| 합계 |  | 25 |  |

| 기준 | 점수 |
|---|---:|
| 공식 합격선 | 15 |
| 실전 목표선 | 17 |
| 고득점 기준 | 20 |

Source of truth는 `rubrics/scoring_model/default.json`이다.

## 3. Runtime 흐름

```text
Telegram /grade
  → bot.py 원문 보존과 grade_submission_normalizer.py
  → grading_identity.py
  → question-only deterministic Question Type lens
  → grading_agents.py 공통 정규화 경계
  → LLM provider routing
  → semantic grading과 3인 rater 합성
  → Fact Anchor / Model Answer evidence
  → explicit requirement coverage
  → Logic Check / deterministic checker
  → verified defect reconciliation
  → single-owner layer evidence guard
  → Difficulty Strategy / recommended ceiling
  → final score reconciliation
  → final coverage persistence
  → verdict_consistency.py
  → grade.json 저장
  → 동일 객체를 Telegram formatter에 전달
```

`grading_agents.py`가 최초 최종화한 뒤 `bot.py`에서도 final persistence guard를 수행한다. score-bearing field는 저장 직전에 다시 일관성을 확인한다.


### 3.1 제출문 정규화 계약

`grade_submission_normalizer.py`는 채점 입력 앞단의 topic-neutral transport normalization을 소유한다.

정규화 대상:

- Telegram timestamp와 speaker prefix
- Bot 응답 블록
- 중첩 `/grade`와 `/cancel`
- 종료 표식 `끝`
- zero-width 문자
- 과도한 앞뒤 공백과 연속 빈 줄

정규화는 기술 문장, 수식, 단위와 주장 내용을 재작성하지 않는다.

`bot.py`는 다음 증적을 session에 보존한다.

```text
input.raw.txt
input.txt
input.normalized.txt
submission_normalization.json
```

공통 `grading_agents.py` 경계도 동일 normalizer를 적용한다. 정규화 결과는 idempotent해야 하며 같은 입력을 반복 정규화해도 결과가 변하지 않아야 한다.

## 4. 3인 layer 평가

| 채점자 | 중점 |
|---|---|
| 교수 채점자 | 원리, 개념 정확성, 체계성 |
| 기술사 채점자 | 현장 절차, 적용 조건, 리스크, 검증 |
| 기업 임원 채점자 | 비용, 유지보수성, 기존 설비 영향, 실현 가능성 |

Layer별 가중치는 `rubrics/scoring_model/default.json`이 기준이다. 단순 평균, layer 가중 점수와 실제 적용된 cap 이후 최종 점수는 구분한다.

## 5. Question Type

Active Question Type은 4종이다.

- `PRINCIPLE_INTERPRETATION`
- `DIAGNOSIS_ACTION`
- `COMPARE_SELECTION`
- `IMPLEMENTATION_EVALUATION`

최종 Question Type lens는 **문제문만** 사용한다. 답안 내용, 길이, 표현 차이로 type을 바꾸지 않는다.

Semantic grader는 coverage evidence를 제공할 수 있지만 type 소유권은 deterministic router와 canonical taxonomy에 있다.

### 5.1 Question Type provenance 계약

- `question_contract.json`의 `question_type.id`가 session의 canonical Question Type이다.
- 후단 adapter는 Question Contract가 전달되면 문제문을 다시 분류하지 않는다.
- Question Contract가 없는 호환 경로만 `question_type_router.detect_question_type`을 사용한다.
- `question_type`, `question_type_v2`, root `question_type_coverage`, coverage score adjustment는 같은 canonical type을 사용한다.
- `legacy_grade_reference`, `model_answer_reference` 등 reference-only branch의 type과 coverage는 최종 판정·점수·출력의 source가 될 수 없다.
- semantic coverage type이 canonical type과 다르면 유형별 coverage를 무효화하되, 문제문에서 직접 추출한 explicit requirement evidence는 보존한다.

## 6. Coverage 상태

명시적 요구와 Question Type coverage는 다음 네 상태를 사용한다.

| 상태 | 의미 |
|---|---|
| `present` | 정확하고 충분하게 응답 |
| `partial` | 직접 응답했지만 불충분 |
| `incorrect` | 직접 응답했지만 핵심 Fact가 틀림 |
| `missing` | 실질적으로 응답하지 않음 |

`incorrect`와 `missing`은 다르다.

- `incorrect`: correctness 문제
- `missing`: completeness 문제

직접 답했지만 틀린 내용을 `missing`으로 바꾸지 않는다.

## 7. 명시적 요구 hard cap

`explicit_requirement_cap.py`가 authoritative runtime이다.

Hard cap은 다음 조건을 모두 만족할 때만 적용한다.

- `question_type_coverage.coverage_source=semantic_grader`
- explicit requirement block의 `source=question_text`
- `extraction_confidence=high`
- `is_core=true`
- 상태가 `missing`

`partial`과 `incorrect`는 hard cap 대상이 아니다.

| 실제 핵심 누락 | B 상한 | 총점 상한 |
|---|---:|---:|
| 1개 | 3.5 / 6 | 17.0 / 25 |
| 2개 이상 | 2.0 / 6 | 14.0 / 25 |
| 전체 | 1.5 / 6 | 12.5 / 25 |

이 정책은 일반 Question Type sub-criteria 부족을 hard cap으로 바꾸기 위한 기능이 아니다.

## 8. Fact Anchor와 Model Answer

Fact Anchor는 topic별 factual coverage를 제공한다.

- 정의
- 핵심 수식
- 조건
- 분류 기준
- 인과관계
- 비교축
- 현장 판단을 지탱하는 Fact

Model Answer는 정답 문장 매칭용이 아니다.

- 고득점 답안 구조
- 설명 깊이
- common missing points
- field connection
- question demand와의 관계

현재 기본 runtime bank는 Topic Pack source에서 생성한 `rubrics/generated/` bank다.

## 9. Logic Check와 deterministic checker

Logic Check는 정답과 직접 충돌하는 핵심 이론 오류를 검증한다.

Topic-specific checker는 수식, 부호, 방향, 조건 같은 deterministic defect를 보완한다.

검증된 defect는 evidence bridge를 통해 explicit requirement와 연결될 수 있으며 해당 응답 상태는 `incorrect`로 동기화할 수 있다.

Coverage 표시 동기화 자체는 점수를 직접 변경하지 않는다.

## 10. Single-owner score policy

같은 오류를 여러 layer에서 중복 감점하지 않는다.

기본 원칙:

- B는 요구 응답 여부와 완전성
- C는 factual correctness의 기본 owner
- D는 독립적인 현장 판단·설계 판단
- E는 독립적인 연결성·방어 가능성

예를 들어 C에서 검증된 Fact 오류가 이미 score owner를 갖는다면, 동일 사실을 B completeness와 D/E에서 다시 직접 감점하지 않는다.

D/E 제한은 별도의 field judgement 또는 connection evidence가 있을 때만 독립적으로 적용한다.

## 11. Logic fatal과 Difficulty ceiling

Logic fatal과 numeric cap은 같은 개념이 아니다.

- Logic fatal은 correctness / claim trust evidence다.
- Difficulty는 고득점 가능성과 recommended ceiling을 계산한다.
- 실제 numeric cap 적용 여부는 runtime mode와 final reconciler가 결정한다.

환경변수:

```text
DIFFICULTY_CEILING_MODE=warn | strict | off
```

`warn`은 cap 후보를 기록하지만 점수를 직접 변경하지 않는다. `strict`에서는 유효한 recommended cap이 실제 점수에 적용될 수 있다.

Telegram의 `cap 적용` 표현은 실제 numeric cap이 적용된 경우에만 사용한다.

## 12. 최종 score reconciliation과 persistence

최종 단계에서는 다음을 일치시킨다.

- A/B/C/D/E breakdown
- total score
- applied cap
- score range
- official pass / practical target 표시
- explicit requirement coverage
- verified defect 표시
- Telegram summary

최종 저장:

```text
final grade object
  → final decision consistency
  → grade.json
  → same object
  → Telegram formatter
```

### 12.1 최종 판정 일관성 계약

`verdict_consistency.py`는 오류 심각도와 최종 칭찬·Full Credit·strong·합격 표시의 충돌을 제거한다.

| 오류 상태 | Full Credit | strong | 합격 | 숫자 점수 |
|---|---|---|---|---|
| Fatal | 차단 | 차단 | 차단 | 유지 |
| Major 비치명 | 차단 | 차단 | 일률 차단하지 않음 | 유지 |
| Minor | 기존 판정 유지 | 기존 판정 유지 | 기존 판정 유지 | 유지 |

이 단계는 score reconciliation을 다시 수행하지 않는다. `total_score`와 layer score를 직접 변경하지 않는다.

`grade_output_summarizer.py`는 `passing_score_allowed`와 `strong_verdict_allowed`를 사용해 공식 합격선, 실전 목표선과 고득점 표시를 동기화한다. 따라서 저장 객체와 Telegram 출력은 같은 최종 판정 계약을 사용한다.

완료된 session은 다음 채점에서 재사용하지 않는다. 동일 초 session ID 충돌도 방지한다.

#### 공통 판정 경계와 실행 계약

이 절은 기술사 채점기의 공통 판정 경계를 정의하는 정본이다. 개별 Topic Pack과
문제 유형은 이 경계를 완화하거나 우회할 수 없다. 세부 작성·검증 절차는 연결된
실행 문서를 따르며, 동일한 계약 본문을 여러 문서에 복제하지 않는다.

##### 문제 요구 축과 답안 축

- 문제의 명시 요구와 요구 간 관계를 먼저 구조화한다.
- 답안이 모범답안과 다른 축을 선택해도 문제와 관련되고 내부적으로 일관되면
  구조·요구 해석·연결성의 제한된 점수를 인정한다.
- 축 일관성은 Fact 정확성이나 요구사항 100% 충족을 자동으로 의미하지 않는다.

##### Fact 증거 게이트

기술 Fact는 원자적 주장 단위로 판정한다.

- `SUPPORTED`: 검증 근거가 있으므로 Fact 가산 가능
- `UNSUPPORTED`: Fact 가산 금지, 자동 감점 금지
- `CONTRADICTED`: Fact 가산 금지, 오류 정책에 따라 감점 또는 상한 적용
- `NOT_APPLICABLE`: Fact 점수 대상 아님

Fact Anchor보다 강한 결론은 지원된 것으로 보지 않는다. “도움이 된다”를
“달성한다”로, “감소시킨다”를 “제거한다”로, “일부 검출한다”를 “전체
검증한다”로 확대하지 않는다.

##### 점수 항목 간 전파 제한

- 구조가 좋다는 이유로 Fact 정확성을 가산하지 않는다.
- 관련 용어를 언급했다는 이유로 verified coverage를 부여하지 않는다.
- 축이 일관된다는 이유로 요구사항을 100% 충족했다고 판정하지 않는다.
- 미검증 기술 주장을 기술사 판단이나 현장성 점수로 우회 가산하지 않는다.
- 연결성은 평가할 수 있으나 잘못된 핵심 전제를 중심으로 한 연결에는 높은
  점수를 주지 않는다.

##### 기술사 판단과 판정 정합성

- 기술사 판단은 검증된 전제, 조건, 대안, trade-off, 검증 방법과 수용 기준을
  근거로 평가한다.
- `strong` 판정은 핵심 요구별 검증된 Fact, 충분한 verified coverage, 핵심
  충돌 부재, 관련되고 일관된 답안 축을 모두 요구한다.
- 최종 점수, 등급, coverage, 총평과 보완 방향은 동일한 근거를 사용한다.
- 보완 방향은 문제 요구에서 가장 큰 미충족, 오류, 검증 공백 순으로 제시한다.

##### 일반화 우선 회귀 정책

- 개별 답안의 모든 틀린 문장을 규칙으로 추가하지 않는다.
- 공통 scoring gate, coverage gate, verdict gate의 실패를 먼저 확인한다.
- Topic 전용 규칙은 도메인 불변식 또는 반복 가능한 오개념일 때만 추가한다.
- 한 사례의 수정은 다른 Topic과 문제 유형에서도 같은 경계를 유지하는지
  회귀 검증한다.

##### Topic Pack과 generated 경계

- Source Topic Pack이 정본이다.
- 기존 Topic과 인접 Topic의 소유권·경계를 먼저 확인한다.
- generated 파일은 build 결과이며 직접 수정하지 않는다.
- Fact, fatal, model, importance와 README의 projection 관계를 유지한다.

##### 변경·검증·문서화 게이트

채점 계약 변경은 read-only inventory, owner 확정, 최소 수정, focused test,
`git diff --check`, clean-snapshot release validation, commit·push 분리,
post-push remote audit 순서를 따른다.

채점 철학, 점수 경계, 공통 gate, question type, Topic Pack schema,
generated projection 또는 release 절차가 바뀌면 코드·테스트와 함께 이 정본과
관련 실행 문서를 갱신한다.

##### 기계 판독 계약

- `QUESTION_AXIS_FIRST`
- `ANSWER_AXIS_ALLOWED`
- `AXIS_CONSISTENCY_EARNS_LIMITED_CREDIT`
- `AXIS_CREDIT_DOES_NOT_IMPLY_FACT_CREDIT`
- `MENTION_IS_NOT_VERIFIED_COVERAGE`
- `NO_SUPPORT_NO_POSITIVE_FACT_CREDIT`
- `UNSUPPORTED_IS_NOT_AUTOMATICALLY_WRONG`
- `CONTRADICTION_ONLY_TRIGGERS_ERROR_PENALTY`
- `ENGINEERING_CREDIT_REQUIRES_TRUSTED_PREMISES`
- `STRONG_REQUIRES_FACT_SUPPORT_AND_AXIS_COHERENCE`
- `GENERALIZED_FIX_BEFORE_CASE_SPECIFIC_RULE`
- `SOURCE_FIRST_GENERATED_BY_BUILD_ONLY`
- `DOCUMENTATION_CHANGES_WITH_CONTRACT`

## 13. Topic Pack과 runtime bank

Topic Pack source:

```text
rubrics/topic_packs/<topic_id>/
```

Generated runtime bank:

```text
rubrics/generated/
```

기본 `RUBRIC_BANK_MODE`는 `generated`다. Legacy bank는 호환과 비교 용도로 유지한다.

Topic Pack 개수와 inventory는 `rubrics/generated/topic_pack_manifest.generated.json`을 기준으로 확인한다.

## 14. 검증 경계

기본 순서:

```text
py_compile
  → focused regression
  → git diff --check
  → validate-all / release validation
  → 필요한 경우에만 container smoke
```

Committed regression은 개발자 로컬 `data/sessions/...` 파일에 의존하지 않는다. 필요한 입력은 `scripts/fixtures/`에 tracked fixture로 둔다.

Container smoke는 LLM integration, container-only dependency, hostname, mount, environment 또는 deployment/runtime 차이가 실제로 있는 변경에 한정한다.

## 15. 주요 runtime owner

| 파일 | 역할 |
|---|---|
| `bot.py` | Telegram 입력, 원문·정규화문 증적, session, 최종 persistence와 formatter boundary |
| `grade_submission_normalizer.py` | topic-neutral 제출문 정규화와 정규화 증적 |
| `grading_agents.py` | semantic grading orchestration과 공통 정규화 경계 |
| `grading_identity.py` | 문제·제출 정규화와 재현성 identity |
| `question_type_router.py` | question-only deterministic lens |
| `question_type_coverage_adapter.py` | coverage 정규화 |
| `explicit_requirement_cap.py` | 실제 핵심 `missing` hard cap |
| `verified_defect_reconciliation.py` | verified defect와 coverage 동기화 |
| `layer_evidence_guard.py` | single-owner evidence 제한 |
| `logic_check_evaluator.py` | Logic Check 병합 |
| `difficulty_score_ceiling.py` | recommended ceiling과 strict 적용 |
| `grade_score_reconciler.py` | 최종 점수·cap·score range 정합성 |
| `verdict_consistency.py` | Fatal·Major·Minor 최종 판정 일관성과 숫자 점수 보존 |
| `grade_output_summarizer.py` | Telegram 요약, pass·strong 표시 동기화와 deterministic fallback |
| `rubric_bank_paths.py` | legacy/generated runtime bank 선택 |
