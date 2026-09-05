# prof_eng_answer

`prof_eng_answer`는 산업계측제어기술사 **2~4교시 논술형 답안**을 Telegram으로 입력받아 25점 문항 기준으로 채점하고, 기술 오류와 보완 방향을 제시하는 답안 평가 시스템입니다.

단순 키워드 포함 여부가 아니라 문제 요구 해석, Fact 정확성, 현장 적용 판단, 논리 연결성, 문제 유형별 요구 충족도와 검증된 핵심 오류를 함께 평가합니다.

> 이 문서는 프로젝트 소개, 빠른 실행, 현재 채점 계약과 검증 방법을 설명합니다. 상세 설계와 운영 기준은 [`docs/README.md`](docs/README.md)에서 찾을 수 있습니다.

> 장기 채점 품질 로드맵과 현재 진행 상태는 [GitHub Issue #1](https://github.com/now0930/prof_eng_answer/issues/1)에서 추적합니다. 이슈는 구현 상태와 검증 증거를 관리하고, 고정 정책과 반복 운영 절차는 `docs/` 문서가 소유합니다.

> 최신 개발 상태(2026-09-03): 답안 분량 기반 점수 상승과 장문 semantic 신호에 의한 atomic requirement `correct` 승격을 제거했습니다. `base_score=A+B+C+D+E`, `final_score=min(base_score, verified hard caps)`를 적용하며, 결정론적 logic fatal은 총점 14.5점, 검증된 핵심 major correctness defect는 17.4점으로 제한합니다. 20점 이상은 개별 core evidence와 D의 현장조건→판단→검증 근거가 있을 때만 허용합니다. 기존 prediction 30건을 새 상태 의미로 재측정한 [정확도 report](reports/expert_accuracy_seed_current.json)는 요구 상태 정확도 55.86%로 [release gate](docs/accuracy_release_gate.md) `HOLD`입니다. 실제 provider 재채점 후에만 배포를 재승인합니다.

---

## 1. 주요 기능

- Telegram `/grade` 명령 기반 답안 채점
- Gemini semantic grader와 CLOVA fallback
- Ollama 기반 보조 분석과 점수 조정 지원
- A/B/C/D/E 25점 계층형 채점
- A·D·E semantic 평가와 B·C native evidence projection을 결합한 하이브리드 채점
- 교수·기술사·기업 임원 관점의 3인 평가와 진단 정보
- 문제문만 사용하는 deterministic Question Type lens
- Topic Pack이 소유하는 canonical primary lens와 답안 비의존형 routing
- Topic Pack의 구조화된 Question Demand를 exact ID·순서·cardinality로 provider 출력에 투영
- provider projection 불일치 시 1회 strict retry 후 fail-closed
- Fact Anchor와 Model Answer Bank 기반 평가
- Logic Check와 topic-specific deterministic checker
- 명시적 요구사항의 `present`, `partial`, `incorrect`, `missing` 분리
- 실제 핵심 요구 누락에만 적용되는 B layer hard cap
- 검증된 correctness defect와 coverage 표시의 동기화
- 동일 오류의 layer 간 중복 감점 방지
- Difficulty Strategy와 score ceiling 평가
- Topic Pack source와 generated Rubric Bank 관리
- 채점 완료 세션 격리와 동일 초 session ID 충돌 방지
- 전송 메타데이터와 중첩 `/grade`를 제거하는 보수적 제출문 정규화
- 원문·정규화문과 정규화 증적의 session 보존
- Fatal·Major 오류와 합격·고득점·Full Credit 판정의 충돌 방지
- 최종 `grade.json`과 Telegram 출력의 동일 객체 보장
- release validation과 focused regression
- Topic Pack 어휘와 분리된 topic-neutral generic grading contract
- 최종 채점 결과에 process-stable runtime provenance 6개 필드 첨부
- runtime provenance와 Docker image·container·host parity 기반 deployment proof의 경계 명시

### 현재 검증 기준

| 항목 | 현재 값 |
|---|---:|
| 총점 | 25점 |
| 채점 Layer | 5개 |
| Active Question Type | 4개 |
| Topic Sheet | 77개 |
| Topic Pack source | 77개 topic |
| Generated Rubric Bank | 6개 |
| 기본 Rubric Bank mode | `generated` |
| Generic grading contract | `stage23.generic_grading_contract.v1` |
| Generic scoring policy | `stage23.generic_scoring_policy.v1` |
| Runtime provenance | `runtime_grading_provenance_v1` |
| Runtime provenance scoring policy | `stage23_generic_grading_contract_v1` |
| 전문가 정확도 Gate | `HOLD` (30 reviewed cases / 25 topics) |
| 요구 추출 F1 / 상태 정확도 | 1.0000 / 55.86% |
| Major·Fatal 정밀도 / 재현율 | 100% / 100% |
| 평균 허용구간 외 거리 | 0.8723 |

`runtime_grading_provenance_v1`은 실행 process 수준의 commit, 시작 시각, router/evaluator/verifier SHA와 scoring policy를 기록합니다. Docker image digest, container ID·시작 시각, PID 교체와 host/container module parity는 별도의 deployment proof이며 [Issue #1](https://github.com/now0930/prof_eng_answer/issues/1)의 P0 항목으로 관리합니다.

Topic Pack 개수는 `rubrics/generated/topic_pack_manifest.generated.json`을 기준으로 확인합니다. Legacy 통합 bank는 호환 목적으로 유지되며, legacy 파일의 Model Answer·Fact Topic 개수를 현재 Topic Pack coverage 개수로 사용하지 않습니다. Runtime bank 선택의 기준은 `rubric_bank_paths.py`와 `RUBRIC_BANK_MODE`입니다.

---

## 2. 채점 구조

총점은 25점입니다.

| Layer | 이름 | 배점 | 평가 초점 |
|---|---|---:|---|
| A | 문제 진입·답안 구조 | 3 | 도입, 목차, 답안 구조와 문제 진입 |
| B | 문제 요구 해석·완전성 | 6 | 문제에서 요구한 항목에 실제로 답했는지 |
| C | 유형별 Fact 기반 내용 설명 | 8 | 핵심 사실, 원리, 식, 인과관계의 정확성 |
| D | 현장 적용·설계 판단·제언 | 6 | 적용 조건, 선정 기준, trade-off와 실행 가능성 |
| E | 연결성·면접 방어 가능성 | 2 | 문단 연결, 결론, 추가 질문 대응 가능성 |

| 기준 | 점수 |
|---|---:|
| 공식 합격선 | 15 / 25 |
| 실전 목표선 | 17 / 25 |
| 고득점 기준 | 20 / 25 |

Question Type, Fact Anchor, Model Answer, Logic Check, deterministic checker와 Difficulty Strategy는 A/B/C/D/E 체계를 대체하지 않습니다. 이들은 평가 근거를 제공하고 최종 결과의 정합성을 보완합니다.

### 2.1 하이브리드 점수 소유권

A/B/C/D/E 체계는 유지하지만 최종 점수의 주된 근거는 Layer별로 다릅니다.

| Layer | 최종 점수의 주된 근거 |
|---|---|
| A | Gemini semantic 평가: 문제 진입, 구조, 범위 통제 |
| B | Question Demand별 충족 상태를 0~3으로 평가한 native projection |
| C | Question Demand에 연결된 Fact Anchor의 정확성·연결 상태를 0~3으로 평가한 native projection |
| D | Gemini semantic 평가: 적용성, 제약·trade-off, 검증·실행 |
| E | Gemini semantic 평가: 영역 간 연결성과 면접 방어 가능성 |

상세 Question Demand 행이 있으면 B는 다음과 같이 계산합니다.

```text
B = 6 × (Question Demand 상태 평균 ÷ 3)
Coverage = 상태가 2 이상인 Demand 수 ÷ 전체 적용 Demand 수 × 100
```

Question Demand의 내부 상태는 `0=없음`, `1=언급`, `2=설명·검증`, `3=요구 조건까지 충족`입니다. 상세 행을 사용할 수 없을 때만 summary 기반 공식 `2 × (covered_ratio + verified_ratio + mean_demand_level)`을 호환 경로로 사용합니다.

C는 연결된 Fact Anchor 상태를 사용합니다.

```text
C = 8 × (Fact Anchor 상태 평균 ÷ 3)
```

Fact Anchor의 내부 상태는 `0=없음`, `1=언급`, `2=정확`, `3=정확한 Fact를 Question Demand와 연결`입니다. Native projection을 만들 수 없을 때는 `fact_eval.c_score`를 우선하고, 그 값도 없으면 `accuracy + core_concept + problem_link + compactness`를 호환 경로로 사용합니다.

Question Type과 Model Answer는 평가 범위와 기대 구조를 제공합니다. Logic Check와 deterministic checker는 검증된 오류와 cap 근거를 제공합니다. 이들은 25점 Layer 체계를 유지하면서 B·C native projection과 A·D·E semantic 평가의 정합성을 보완합니다.

---

## 3. Active Question Type

현재 active type은 4개입니다.

| ID | 이름 | 대표 요구 |
|---|---|---|
| `COMPARE_SELECTION` | 비교·선정형 | 비교 기준, 장단점, 적용 조건, 최종 선정 |
| `DIAGNOSIS_ACTION` | 진단·대책형 | 현상, 원인, 진단, 개선 대책 |
| `IMPLEMENTATION_EVALUATION` | 적용·평가형 | 구현 절차, 운영 조건, 검증과 평가 |
| `PRINCIPLE_INTERPRETATION` | 원리·해석형 | 원리, 구성, 수식, 동작과 의미 해석 |

Question Type lens는 **문제문만** 사용해 결정합니다. 답안 내용, 답안 길이, 이모지와 표현 차이는 lens를 변경하지 않습니다. Rule-based 결과를 우선하고 신뢰도 조건을 만족할 때 최종 type을 고정합니다.

Legacy 유형명은 입력 호환을 위해 canonical type으로 매핑될 수 있지만, 최종 root, 한국어 이름과 Telegram 출력은 active type 기준으로 동기화합니다.

문제문이 Topic Pack의 `question_demand_axes.json` activation 조건과 일치하면 해당 파일의 `canonical_primary_lens`가 canonical owner가 됩니다. 이 계약은 답안 본문을 사용하지 않으며, provider가 반환한 explicit requirement가 Topic Pack의 요구축 ID·순서·개수와 정확히 일치하는지 검증합니다.

---

## 4. 현재 채점 정책

### 4.1 `incorrect`와 `missing` 분리

명시적 요구와 Question Type 세부 기준은 네 상태로 관리합니다.

| 상태 | 의미 | 처리 |
|---|---|---|
| `present` | 정확하고 충분하게 답함 | 정상 인정 |
| `partial` | 직접 답했지만 설명이 부족함 | 부분 인정 |
| `incorrect` | 직접 답했지만 핵심 사실이 틀림 | correctness 평가와 표시에서 제한 |
| `missing` | 요구에 실질적으로 답하지 않음 | 조건 충족 시 누락 hard cap 대상 |

`incorrect`는 오답이고 `missing`은 미응답입니다. 직접 답했지만 틀린 내용은 누락으로 바꾸지 않습니다.

공개 판정 상태와 B·C 계산용 내부 상태는 목적이 다릅니다. 공개 상태는 오답과 누락을 구분해 표시하고 hard cap 여부를 판단합니다. 내부 0~3 상태는 충족 수준을 점수로 환산합니다. 특히 `incorrect`는 내부적으로 `missing`으로 바꾸지 않으며, 기술적 정확성 오류는 기본적으로 C layer가 소유합니다.

Telegram 출력도 두 상태를 분리합니다.

```text
- 전체 판정: weak
- 상태: 충족 1 · 부분 0 · 오답 2 · 누락 0
- 명시적 핵심 요구 오답 응답: 마찰력 개념 설명, Fail Safe 스프링 설계 기준
```

### 4.2 명시적 요구사항 hard cap

Hard cap은 다음 조건을 모두 만족하는 **실제 핵심 요구 누락**에만 적용합니다.

- `question_type_coverage.coverage_source=semantic_grader`
- `explicit_requirement_coverage.source=question_text`
- 추출 신뢰도가 `high`
- `is_core=true`
- 상태가 `missing`

`partial`과 `incorrect`는 누락 hard cap 대상이 아닙니다.

| 실제 누락 상태 | B항목 상한 | 총점 상한 |
|---|---:|---:|
| 핵심 요구 1개 누락 | 3.5 / 6 | 17.0 / 25 |
| 핵심 요구 2개 이상 누락 | 2.0 / 6 | 14.0 / 25 |
| 핵심 요구 전체 누락 | 1.5 / 6 | 12.5 / 25 |

### 4.3 Verified defect와 단일 점수 소유권

결정론적 checker 또는 신뢰 가능한 evaluator가 검증한 correctness defect는 관련 명시적 요구사항에 연결합니다.

- 연결된 요구사항의 상태는 `incorrect`가 됩니다.
- Fact 정확성 오류의 기본 owner는 C layer입니다.
- B layer는 요구 응답 여부와 완전성을 담당합니다.
- 같은 오류를 B completeness, C correctness, D/E에 중복 감점하지 않습니다.
- D/E에는 별도의 현장 판단 또는 연결성 근거가 있을 때만 독립 제한을 적용합니다.
- Coverage 표시 동기화 자체는 점수를 변경하지 않습니다.

Topic-specific checker는 문맥과 부정을 구분해야 합니다. 예를 들어 “속도에 비례하는 힘이 아니다”와 같은 부정문은 오류로 검출하지 않으며, 명시적인 잘못된 식이나 부호 모순은 correctness defect로 승격할 수 있습니다.

### 4.4 Question Type coverage 보정

`QUESTION_TYPE_COVERAGE_SCORE_MODE`는 다음과 같이 동작합니다.

| 모드 | 동작 |
|---|---|
| `warn` | 보정 후보와 표시만 기록하며 점수는 변경하지 않음 |
| `strict` | 유효한 보정 후보가 현재 점수보다 낮을 때 제한적으로 반영 |
| `off` | coverage 점수 보정 비활성 |

기본값은 `warn`입니다. Coverage 보정은 약한 보조 정책이며, 명시적 요구사항 hard cap이나 C correctness defect와 같은 근거를 중복 감점하지 않습니다.

### 4.5 Phase 8 constraint-only 정책

Phase 8 originality 평가는 semantic 점수에 가산점을 주지 않습니다. A·C·D·E는 Phase 6 semantic 점수와 Phase 8 후보 중 낮은 값만 유지합니다.

```text
A·C·D·E = min(Phase 6 semantic score, Phase 8 candidate)
```

B는 Phase 8의 최종 소유 대상이 아닙니다. Phase 8 처리 후 Question Demand native projection이 B를 다시 결정합니다. Connection 평가는 진단 정보로 유지하며 E점수를 직접 덮어쓰지 않습니다.

### 4.6 검증된 correctness 오류와 numeric cap

Logic Check는 핵심 이론 오류를 검증합니다.

- 결정론적 Logic fatal은 총점 14.5점 hard cap을 적용합니다.
- 구조화 evidence로 core requirement에 연결된 major correctness defect는 총점 17.4점 hard cap을 적용합니다.
- LLM 단독 주장, 스타일 지적, non-core major는 numeric cap 근거가 아닙니다.
- 해당 cap은 A/B/C/D/E의 오류 소유권과 별개인 최종 안전장치이며, 동일 오류를 layer별로 중복 감점하지 않습니다.
- Recommended ceiling과 실제 적용된 numeric cap을 구분합니다.
- Telegram의 `cap 적용` 문구는 실제 numeric cap이 적용된 경우에만 출력합니다.

### 4.7 최종 객체와 저장 정합성

최종 결과는 다음 순서를 보장합니다.

핵심 채점 경로는 함수 재정의나 `previous implementation` wrapper를 사용하지 않습니다. Gemini prompt·semantic 평가, question-type coverage, verified-defect reconciliation, agent 실행, 출력 요약과 verdict 정합성은 각각 이름 있는 내부 단계를 하나의 공개 진입점에서 합성합니다. `tests/test_finalization_module_structure.py`가 이 6개 핵심 모듈의 top-level 함수 중복 정의와 과거 wrapper alias 재유입을 차단합니다.

```text
보수적 제출문 정규화
  → semantic grading
  → deterministic checker와 evidence bridge
  → Phase 8 constraint-only 처리
  → Question Demand 기반 B와 Fact Anchor 기반 C reconciliation
  → verified defect, hard cap과 difficulty ceiling 적용
  → generic grading contract 기반 demand·claim·evidence 정규화
  → display alias와 coverage 정규화
  → 최종 native B·C serialization sync
  → final decision consistency
  → runtime grading provenance 첨부
  → grade.json 저장
  → 동일 객체를 Telegram formatter에 전달
```

`grading_agents.py`와 `bot.py` 양쪽의 최종 persistence guard는 score-bearing field가 변경되지 않았는지 확인합니다. 따라서 `weak`, `오답 2`와 같은 표시 결과와 저장된 `grade.json`이 동일해야 합니다.


제출문 정규화는 기술 내용을 재작성하지 않습니다. Telegram timestamp, speaker prefix, Bot 응답, 중첩 `/grade`, `/cancel`, `끝`과 zero-width 문자를 보수적으로 제거하고 원문과 정규화문을 모두 보존합니다.

`grade_submission_normalizer.py`가 제출문 정규화를 소유하고, `verdict_consistency.py`가 최종 판정 일관성을 소유합니다.

최종 판정 일관성은 점수를 올리거나 재계산하지 않습니다. 다만 verified correctness cap은 별도 최종 경계에서 숫자를 단방향으로만 낮춥니다.

- Fatal 오류는 praise, Full Credit, strong와 합격 판정을 차단합니다.
- Major 비치명 오류는 Full Credit과 strong를 차단하지만 합격을 일률적으로 차단하지 않습니다.
- Minor 오류는 기존 판정을 유지합니다.
- `grade_output_summarizer.py`는 동일 허용 플래그를 사용하여 Telegram 표시를 동기화합니다.

### 4.8 세션 격리

채점 결과는 `data/sessions/<session_id>/`에 저장합니다.

- Active session의 상태가 `graded`이면 다음 채점 전에 새 세션을 생성합니다.
- 같은 chat에서 연속 채점해도 이전 `grade.json`을 덮어쓰지 않습니다.
- 동일 초에 session을 여러 개 생성하면 충돌 방지 suffix를 붙입니다.
- 저장 경로는 Telegram 결과에 함께 표시합니다.

### 4.9 Generic grading contract와 runtime provenance

Generic grading contract는 Topic Pack의 주제 어휘, Fact Anchor와 Model Answer에서 분리된 topic-neutral 계약입니다. 문제 분야와 관계없이 demand 상태, claim 관계, evidence 신뢰도와 D/E 요구사항의 감점 가능 여부를 같은 형식으로 정규화합니다.

현재 schema와 scoring policy는 다음과 같습니다.

| 구분 | 현재 값 |
|---|---|
| Generic contract schema | `stage23.generic_grading_contract.v1` |
| Generic scoring policy | `stage23.generic_scoring_policy.v1` |
| Runtime provenance schema | `runtime_grading_provenance_v1` |
| Runtime provenance의 scoring policy | `stage23_generic_grading_contract_v1` |

Demand 평가는 네 상태를 사용합니다.

| 상태 | 의미 | correctness credit |
|---|---|---:|
| `CORRECT` | 요구에 정확하게 답함 | 1.0 |
| `PARTIAL` | 요구에 답했으나 불완전함 | 0.5 |
| `WRONG` | 요구를 언급했지만 핵심 내용이 틀림 | 0.0 |
| `MISSING` | 요구에 실질적으로 답하지 않음 | 0.0 |

`WRONG`과 `MISSING`은 correctness credit이 같아도 의미가 다릅니다. Mention coverage와 correctness coverage를 분리하며, 오답을 누락으로 바꾸지 않습니다.

Claim 관계는 `DEFINITION`, `CLASSIFICATION`, `PURPOSE`, `MAPPING`, `CAUSE_EFFECT`, `CONDITION`, `SEQUENCE`, `METRIC_SCOPE`, `COMPONENT`, `EQUIVALENCE`로 구분합니다. Alignment는 `ALIGNED`, `PARTIAL`, `CONTRADICTED`, `UNSUPPORTED`, `NOT_APPLICABLE`로 관리합니다.

Evidence trust tier는 다음과 같습니다.

| Tier | 의미 | 기본 credit 원칙 |
|---|---|---|
| `DETERMINISTIC` | 결정론적 checker와 재현 가능한 규칙 | 정렬 상태가 유효하면 full trust |
| `VERIFIED_STRUCTURED` | 검증된 구조화 evidence | 정렬 상태가 유효하면 full trust |
| `SEMANTIC_INFERRED` | LLM 또는 semantic 판단으로 추론 | 최대 partial trust |
| `UNSUPPORTED` | 검증 가능한 근거 없음 | credit 없음 |

D/E 요구사항은 `MANDATORY`, `OPTIONAL_BONUS`, `NO_PENALTY`로 구분합니다. 명시적으로 요구되고 `MANDATORY`로 분류된 항목만 미충족 감점을 허용합니다. 요구되지 않은 적용·제언을 일반적인 필수 감점 근거로 사용하지 않습니다.

최종 grade 객체에는 `runtime_grading_provenance`를 첨부합니다.

| 필드 | 의미 |
|---|---|
| `engine_commit` | 실행 코드의 Git commit |
| `engine_process_started_at` | 해당 Python 프로세스에서 provenance 모듈을 초기화한 UTC 시각 |
| `router_version` | Question Type Router 파일의 SHA256 식별자 |
| `evaluator_sha` | Logic Check evaluator 파일 SHA256 |
| `verifier_sha` | Logic LLM verifier 파일 SHA256 |
| `scoring_policy_version` | runtime scoring policy 식별자 |

Provenance 값은 한 Python 프로세스 안에서 안정적으로 유지됩니다. 서로 다른 프로세스의 `engine_process_started_at`은 동일하다고 가정하지 않습니다. 배포 프로세스와 read-only probe를 비교할 때는 `engine_commit`, `router_version`, `evaluator_sha`, `verifier_sha`, `scoring_policy_version`을 exact match하고, 각 process timestamp는 별도로 검증합니다.

Bind mount 환경에서 `engine_commit`을 읽을 때는 repository 경로를 명시하고 command-scoped `safe.directory`를 사용합니다. Global 또는 system Git config는 변경하지 않습니다.

### 4.10 Topic Pack exact Question Demand projection

`hazop_lopa_ipl_risk_reduction_sil_target_allocation` Topic Pack은 반응기 과압력 SIS 문제에 대해 다음 8개 요구축을 소유합니다.

1. 시나리오·원인 정의
2. 기존 IPL 적격성
3. 요구 RRF·목표 SIL
4. 요구 모드·SIL 지표
5. 완전한 SIF 아키텍처
6. 정량 검증·차원 일관성
7. 독립성·CCF·HFT 절충
8. Proof test·수명주기

계약의 canonical lens는 `IMPLEMENTATION_EVALUATION`입니다. Provider projection은 8개 requirement ID의 exact cardinality, ID set과 순서를 모두 만족해야 합니다. 첫 응답이 계약과 다르면 strict contract로 한 번만 재시도하고, 재시도도 불일치하면 불완전한 coverage를 채점 결과로 통과시키지 않고 fail-closed 처리합니다.

Stage35E2 기준 focused regression 6/6과 full release validation은 통과했습니다. Fresh live session `20260830_081215_5960502198`과 `20260830_081351_5960502198`에서도 동일 lens와 fatal 판정 보존을 확인했습니다.

현재 알려진 제한은 canonical lens reconciliation 뒤 최종 Telegram `question_type_coverage_summary`가 `unknown`으로 축약되어 8축 상태 집계가 표시되지 않는 점입니다. 내부 exact projection을 임의의 type-specific sub-criteria로 대체하지 않으며, explicit 8축 summary만 보존하는 Stage35E3 작업은 [Issue #1](https://github.com/now0930/prof_eng_answer/issues/1)에서 보류 상태로 추적합니다.

---

## 5. 빠른 실행

### 5.1 운영 중인 Hermes Compose

```bash
cd ~/hermes

docker compose up -d prof-eng-answer-bot
docker logs --tail=100 -f prof_eng_answer_bot
```

코드 반영 후 재시작:

```bash
cd ~/hermes

docker compose restart prof-eng-answer-bot
docker logs --tail=100 -f prof_eng_answer_bot
```

상태 확인:

```bash
docker compose ps
docker inspect -f '{{.State.Running}}' prof_eng_answer_bot
```

### 5.2 저장소의 standalone 예제

```bash
cd /home/now0930/hermes/workspace/prof_eng_answer

cp .env.example .env
cp docker-compose.example.yml docker-compose.yml

vim .env
docker compose up -d prof-eng-answer-bot
docker logs --tail=100 -f prof_eng_answer_bot
```

예제 Compose는 외부 Docker network `ai_net`을 사용합니다. Network가 없다면 한 번만 생성합니다.

```bash
docker network create ai_net
```

상세 운영 절차는 [`docs/operation_runbook.md`](docs/operation_runbook.md), Compose 구조는 [`docs/docker_compose_usage.md`](docs/docker_compose_usage.md)를 참조합니다.

---

## 6. 환경변수

핵심 예시는 다음과 같습니다.

```dotenv
# Telegram
TELEGRAM_BOT_TOKEN=

# Gemini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.1-flash-lite

# Ollama
OLLAMA_URL=http://ollama:11434
OLLAMA_MODEL=

# Provider routing
LLM_PROVIDER=auto
LLM_PRIMARY=gemini
LLM_FALLBACK=clova

# CLOVA
CLOVA_API_KEY=
CLOVA_BASE_URL=
CLOVA_MODEL=

# Rubric bank
RUBRIC_BANK_MODE=generated

# Question Type coverage: warn | strict | off
QUESTION_TYPE_COVERAGE_SCORE_MODE=warn

# Difficulty ceiling: warn | strict
DIFFICULTY_CEILING_MODE=warn
```

| 값 | 의미 |
|---|---|
| `LLM_PROVIDER=auto` | Gemini primary, CLOVA fallback |
| `LLM_PROVIDER=gemini` | Gemini만 사용 |
| `LLM_PROVIDER=clova` | CLOVA만 사용 |

실제 운영값은 `.env`와 현재 Compose 설정을 기준으로 확인합니다.

---

## 7. Telegram 사용

Bot에서 `/grade`를 입력한 뒤 문제와 답안을 전송합니다.

```text
/grade

문제:
공압식 밸브 선정 시 불평형력과 마찰력을 설명하고,
Fail Safe 구현을 위한 Spring 설계 기준을 제시하시오.

답안:
...
```

결과에는 다음 정보가 포함됩니다.

- 총점과 예상 점수대
- 공식 합격선과 실전 목표선
- A/B/C/D/E 점수
- 핵심 판정과 항목별 근거
- Logic Check와 deterministic checker 결과
- Question Type 요구사항 충족도
- 명시적 요구의 오답·누락 구분
- 보완 방향
- 저장된 session 경로
- `runtime_grading_provenance` 6개 필드와 실행 코드 추적 정보

세션 디렉터리에는 다음 파일이 저장될 수 있습니다.

```text
data/sessions/<session_id>/
├── input.raw.txt
├── input.txt
├── input.normalized.txt
├── submission_normalization.json
├── grade.json
├── meta.json
├── images/
└── 단계별 snapshot
```

---

## 8. 처리 흐름

```text
Telegram /grade
  → bot.py 원문 보존과 보수적 제출문 정규화
  → grading identity와 question-only lens
  → grading_agents.py 공통 정규화 경계
  → LLM provider routing
  → semantic grading과 3인 rater 합성
  → Fact Anchor / Model Answer
  → Topic Pack question_demand_axes bridge
  → provider exact requirement projection 검증·1회 strict retry
  → explicit requirement coverage
  → Logic Check와 deterministic checker
  → generic demand/claim/evidence contract 정규화
  → single-owner evidence guard
  → Difficulty Strategy와 score ceiling
  → final score reconciliation
  → verified defect/coverage final persistence
  → Bot second-writer final persistence
  → final decision consistency
  → runtime grading provenance 첨부
  → grade.json 저장
  → Telegram output formatter
```

핵심 원칙은 다음과 같습니다.

1. 점수는 A/B/C/D/E가 소유합니다.
2. Coverage와 checker는 근거와 제한을 제공합니다.
3. 한 오류는 하나의 canonical owner를 가집니다.
4. 저장 객체와 출력 객체는 동일해야 합니다.
5. 완료된 session은 다음 채점에 재사용하지 않습니다.
6. 제출문 정규화는 topic-neutral하고 idempotent해야 합니다.
7. 최종 판정 일관성은 점수를 올리지 않으며, 검증된 correctness cap만 단방향 하향 적용합니다.

---

## 9. Topic Sheet, Topic Pack과 Generated Rubric Bank

현재 runtime 기본값은 Topic Pack 기반 `generated` bank입니다. Legacy bank는 비교·호환 목적으로 유지합니다.

현재 저장소의 출제범위·Topic·runtime 관계는 다음 순서로 관리합니다.

```text
한국산업인력공단 공식 출제기준
    ↓
Exam Scope / Criterion
    ↓
Classification / Coverage
PRIMARY / SECONDARY · COVERED / PARTIAL / GAP
    ↓
Topic Sheet
    ↓
Topic Pack Source
    ↓
Generated Rubric Bank
    ↓
Topic Router
    ↓
Runtime Grading
```

공식 출제기준과 Topic은 반드시 1:1이 아닙니다. 하나의 criterion이 여러 Topic을 요구하거나 하나의 Topic이 여러 criterion을 지원할 수 있으므로 `docs/topic_pack_classification.md`에서 PRIMARY/SECONDARY ownership을 관리합니다. 반면 **Topic Sheet와 Topic Pack은 동일 `<topic_id>`의 1:1 관계**입니다.

출제범위와 Topic Pack의 상세 연결 원칙은 [`docs/exam_scope/industrial_instrumentation_control_exam_scope_to_topic_pack_model.md`](docs/exam_scope/industrial_instrumentation_control_exam_scope_to_topic_pack_model.md)에서 관리합니다.

### 9.1 Topic Sheet와 Topic Pack의 관계

**Topic Sheet**는 사람이 읽고 검토하는 **주제 설계서(authoring/design specification)**입니다.

경로:

```text
docs/topic_sheets/<topic_id>.md
```

Topic Sheet에서는 해당 Topic이 무엇을 설명해야 하는지 먼저 정합니다. Topic에 따라 문서 형식에는 차이가 있지만, 주로 다음 내용을 다룹니다.

- Topic identity / metadata
- 출제 의도와 대표 문제
- 포함 범위와 제외 범위
- 핵심 Fact와 고득점 답안 기준
- 대표 오답과 Fatal Wrong Claims
- 인접 Topic과의 ownership 경계
- Routing alias / field point
- Fact 검증 근거와 semantic review 요구사항

즉, Topic Sheet는 JSON을 만들기 전에 **“이 Topic이 무엇을 소유하고 무엇을 소유하지 않는가”를 먼저 고정하는 문서**입니다.

**Topic Pack**은 Topic Sheet에서 확정한 의미 경계를 채점기가 사용할 수 있도록 구조화한 **machine-readable grading source of truth**입니다.

경로:

```text
rubrics/topic_packs/<topic_id>/
├── README.md
├── fact_anchor.json
├── logic_check.json
├── model_answer.json
└── topic_importance.json
```

현재 저장소에는 **Topic Sheet 77개와 Topic Pack 77개가 있으며, 동일한 `<topic_id>`로 77개 모두 1:1 대응**합니다. Topic Sheet만 있고 Topic Pack이 없는 항목도 없고, Topic Pack만 있고 Topic Sheet가 없는 항목도 없습니다.

이 관계를 기준으로 신규 Topic은 다음 원칙을 따릅니다.

1. 먼저 `docs/topic_sheets/<topic_id>.md`에서 의미 범위와 ownership을 확정합니다.
2. 같은 `<topic_id>`의 `rubrics/topic_packs/<topic_id>/`를 작성합니다.
3. `fact_anchor.json`, `logic_check.json`, `model_answer.json`, `topic_importance.json`은 Topic Sheet에서 확정한 **동일한 의미 경계**를 공유해야 합니다.
4. Topic 전용 focused regression으로 핵심 Fact, fatal claim, 인접 Topic contamination을 검증합니다.
5. 검증된 Topic Pack source를 builder로 합쳐 Generated Rubric Bank를 만듭니다.

따라서 관계는 다음과 같습니다.

```text
Topic Sheet = 사람 기준의 주제 설계서
Topic Pack  = Topic Sheet를 구조화한 채점 source
Generated Rubric Bank = 검증된 Topic Pack을 runtime용으로 합친 build output
```

Topic Sheet와 Topic Pack의 개수는 특정 분야별 별도 집계보다 **전체 Topic inventory를 기준으로 관리**합니다. 현재 authoritative Topic inventory는 77개입니다.

### 9.2 저장 위치와 역할

| 구분 | 위치 | 역할 |
|---|---|---|
| Topic Sheet | `docs/topic_sheets/<topic_id>.md` | Topic 의미 범위, 핵심 Fact, 오개념, ownership, authoring 요구사항을 정의하는 사람 기준 설계서 |
| Topic Pack Source | `rubrics/topic_packs/<topic_id>/` | Topic Sheet를 구조화한 검증 가능한 grading source of truth |
| Focused Regression | `scripts/test_<topic>_*.py` | Topic별 핵심 사실·fatal·인접 Topic contamination 회귀 검증 |
| Generated Rubric Bank | `rubrics/generated/*.generated.json` | 검증된 Topic Pack source를 runtime bank로 합친 build output |
| Classification / Coverage / Roadmap | `docs/topic_pack_classification.md`, `docs/exam_scope/` | 공식 criterion ownership, coverage와 추가 우선순위 관리 |
| Legacy Rubric Bank | `rubrics/*/industrial_instrumentation_control.json` | 기존 통합 bank와 호환·비교 경로 |

현재 저장소에는 **77개 Topic Pack**이 있으며 generated runtime bank는 다음 **6개**입니다.

```text
fact_anchors.generated.json
model_answers.generated.json
topic_importance.generated.json
logic_checks.generated.json
logic_check_profiles.generated.json
topic_pack_manifest.generated.json
```

`rubrics/generated/*.generated.json`은 직접 편집하지 않습니다. 사람이 의미를 설계하는 시작점은 Topic Sheet이고, 채점 source of truth는 Topic Pack입니다. Source authoring과 검증이 끝난 뒤 builder로 generated bank를 재생성합니다.

### 9.3 앞으로의 신규 Topic Pack 추가 절차

```text
1. Candidate 선정
   ↓
2. Read-only 중복·ownership·인접 Topic 경계 감사
   ↓
3. Topic Sheet 작성·확정
   ↓
4. 동일 topic_id의 Topic Pack source 4종 작성
   ↓
5. Topic 전용 focused semantic regression 작성·통과
   ↓
6. LLM 의미감사와 source 경계 검토
   ↓
7. Classification / Coverage / Roadmap 영향 판정
   ↓
8. Generated 6-bank 재생성
   ↓
9. Generated 의미감사 + semantic idempotence 감사
   ↓
10. focused / source / generated / Router / release 검증
   ↓
11. 검증된 파일만 Topic 단위 독립 commit
   ↓
12. 별도 push 후 local / tracking / remote SHA 검증
```

단일 신규 Topic은 `validate-topic-pack-release --topic-id <topic_id> --promote-generated`로 검증합니다. 인자 없는 실행은 Git에서 변경된 Topic만 선택하며, 전체 inventory 검증은 통합 시점에 `--all`로 명시합니다. 외부 모델을 호출하는 smoke는 기본 경로에서 제외하고 필요할 때 `--smoke`로 실행합니다.

운영 원칙:

- 신규 Topic은 공식 criterion의 `GAP`/`PARTIAL`, 기출 반복성, 현장 중요도와 Roadmap을 근거로 선정합니다.
- 단순히 키워드가 다르다는 이유로 Topic을 분리하지 않습니다.
- 기존 Topic과 원리·오류·적용 범위가 실질적으로 겹치면 신규 Topic을 만들지 않습니다.
- 기존 Topic의 내용 오류·혼입은 **coverage backlog와 source anomaly를 구분**하고, 신규 Topic 생성보다 기존 Topic repair를 우선합니다.
- Topic Sheet에서 먼저 positive ownership과 negative boundary를 확정한 뒤 Topic Pack source에 반영합니다.
- `fact_anchor.json`, `logic_check.json`, `model_answer.json`, `topic_importance.json`은 동일한 Topic 의미 경계를 공유해야 합니다.
- 인접 Topic 내용은 `fatal_wrong_claims`, `rejected_explanations`, `low_score_patterns` 같은 negative boundary로 둘 수 있지만 현재 Topic의 positive ownership으로 사용하지 않습니다.
- `docs/topic_pack_classification.md`의 PRIMARY/SECONDARY ownership은 실제 의미 범위가 변할 때만 수정합니다.
- Coverage Matrix는 공식 criterion 상태가 실제로 변할 때만 갱신합니다.
- 최신동향·법령·표준처럼 정적 Topic Pack으로 고정하기 어려운 범위는 `DYNAMIC_REVIEW_LANE`으로 관리할 수 있습니다.
- LLM 의미감사는 저장소 스크립트가 LLM을 호출하도록 만들지 않고 별도 review 단계에서 수행합니다.
- builder의 timestamp 등 의도적으로 변하는 field는 byte equality가 아니라 해당 field를 정규화한 **semantic idempotence**로 확인합니다.
- production Python, container 전용 hostname, mount, dependency 또는 runtime 경계가 바뀌지 않는 Topic 작업은 host focused validation을 기본으로 하며 불필요한 container 전체 회귀를 반복하지 않습니다.
- 병렬 Topic 확장은 Topic별 local commit을 유지하고 Lane 전체 검증 후 Lane branch를 한 번만 push합니다.
- shared classification / coverage / generated 변경은 Lane 결과를 통합한 뒤 별도 integration 단계에서 수행합니다.
- commit과 push는 분리하고 force push는 사용하지 않습니다.
- push 후 local HEAD, tracking ref, remote SHA가 동일한지 확인합니다.

기본 validation 흐름:

```text
py_compile
  → Topic focused regression
  → source / generated validator
  → Router regression
  → git diff --check
  → rubric_manager.py validate-all
  → 필요한 경우에만 container smoke
```

### 9.4 Topic Router v2 방향

Topic Pack은 문제은행이 아니므로 실제 시험문제가 항상 Topic 하나와 1:1로 일치한다고 가정하지 않습니다. Router는 장기적으로 다음 네 상태를 구분합니다.

- `SINGLE_TOPIC`: 하나의 Topic evidence로 충분
- `MULTI_TOPIC`: 둘 이상의 Topic을 실제 문제 요구사항이 함께 요구
- `GENERAL`: 문제는 명확하지만 현재 Topic evidence가 충분하지 않음
- `AMBIGUOUS`: 문제 자체가 모호하여 Topic을 안정적으로 결정하기 어려움

구현 원칙은 **Rule → LLM → Rule** 구조입니다.

```text
Rule: candidate generation / guard
    ↓
LLM: question demand decomposition / semantic adjudication
    ↓
Rule: schema / topic / confidence / fallback policy validation
```

Rule은 재현 가능한 후보 검색과 안전장치를 담당하고, LLM은 Topic Sheet의 positive ownership·negative boundary를 이용한 의미 판단을 담당합니다. LLM은 존재하지 않는 Topic을 만들거나 점수를 직접 결정하지 않습니다.

초기에는 기존 deterministic Router를 production에 유지하고 LLM 결과만 기록하는 **shadow mode**로 시작하며, 이후 `ambiguous/unmatched` 보완 → multi-topic → hybrid general 순으로 점진적으로 확대합니다.

상세 설계는 [`docs/topic_router_v2_design.md`](docs/topic_router_v2_design.md)를 기준으로 합니다.

### 9.5 로컬 운영 스크립트와 Git tracking

`gemini_script/`는 authoring, audit, commit, push를 보조하는 **로컬 일회성 운영 스크립트 공간**입니다.

- production source가 아닙니다.
- Git tracking 대상이 아니며 `.gitignore`로 제외합니다.
- Topic Sheet, Topic Pack source 또는 generated bank의 source of truth로 사용하지 않습니다.
- 운영 스크립트가 없어도 committed source와 테스트만으로 저장소 상태를 재검증할 수 있어야 합니다.
- 재사용 가능한 production 도구가 필요하면 `gemini_script/`가 아니라 `scripts/` 아래에 일반화된 CLI/validator로 작성하고 테스트와 함께 추적합니다.

현재 Topic inventory의 authoritative runtime 목록은 [`rubrics/generated/topic_pack_manifest.generated.json`](rubrics/generated/topic_pack_manifest.generated.json), 공식 criterion ownership은 [`docs/topic_pack_classification.md`](docs/topic_pack_classification.md), 상세 authoring 절차는 [`docs/rubric_authoring_guide.md`](docs/rubric_authoring_guide.md)와 [`docs/topic_pack_workflow.md`](docs/topic_pack_workflow.md)를 기준으로 합니다.

---

## 10. 검증

### 10.1 기본 순서

변경 종류에 따라 다음 순서를 사용합니다.

```text
py_compile
  → focused tests
  → git diff --check
  → validate-all
  → 필요한 경우 container smoke
```

Container smoke는 다음 변경에 수행합니다.

- LLM 연동
- Container 전용 hostname 또는 dependency
- mount와 runtime path
- 환경변수와 배포 흐름
- Bot의 실제 저장·출력 경로

문서만 수정했다면 Markdown 구조, 상대 링크, authoritative value와 `git diff --check`를 우선 검증합니다.

### 10.2 전체 Rubric validation

```bash
python3 scripts/rubric_manager.py validate-all
```

또는 release script:

```bash
PROMOTE_GENERATED=0 \
RUN_SMOKE_TOPIC_PACKS=0 \
bash scripts/validate_release.sh
```

Generated bank를 실제 반영할 때만 `PROMOTE_GENERATED=1`을 사용합니다.

### 10.3 핵심 회귀 테스트

```bash
python3 -m unittest -v \
  scripts.test_final_verified_coverage_and_session_isolation \
  scripts.test_post_release_control_valve_live_regressions \
  scripts.test_verified_defect_reconciliation \
  scripts.test_verified_defect_single_owner_guard \
  scripts.test_requirement_coverage \
  scripts.test_general_grading_runtime_e2e \
  test_stage23_generic_grading_contract

python3 tests/test_stage35e2_provider_eight_axis_canonical_lens.py
```

주요 검증 대상:

- question-only deterministic lens
- `incorrect`와 `missing` 분리
- 실제 누락에만 hard cap 적용
- verified defect와 coverage row 연결
- single-owner score policy
- 최종 `grade.json`과 Telegram 출력 동기화
- session 격리와 동일 초 ID 충돌 방지
- score-bearing field 불변
- Topic Pack 8축 contract와 provider exact projection
- 동일 문제의 답안 비의존형 canonical lens
- projection 불일치 1회 retry와 fail-closed

### 10.4 문서만 수정했을 때

```bash
git diff --check -- README.md docs
```

상대 링크와 현재 Rubric 수치도 함께 확인합니다.

---

## 11. 문서

| 목적 | 문서 |
|---|---|
| 문서 인덱스와 source of truth | [`docs/README.md`](docs/README.md) |
| 운영, 재시작, 장애 대응 | [`docs/operation_runbook.md`](docs/operation_runbook.md) |
| Docker Compose | [`docs/docker_compose_usage.md`](docs/docker_compose_usage.md) |
| 채점 구조와 score flow | [`docs/grading_architecture.md`](docs/grading_architecture.md) |
| Question Type | [`docs/question_type_taxonomy.md`](docs/question_type_taxonomy.md) |
| 난이도와 ceiling | [`docs/difficulty_and_selection_strategy.md`](docs/difficulty_and_selection_strategy.md) |
| LLM provider | [`docs/llm_provider.md`](docs/llm_provider.md) |
| Rubric 작성 | [`docs/rubric_authoring_guide.md`](docs/rubric_authoring_guide.md) |
| Topic Pack workflow | [`docs/topic_pack_workflow.md`](docs/topic_pack_workflow.md) |
| Logic Check 운영 | [`docs/logic_check_profiles_readme.md`](docs/logic_check_profiles_readme.md) |

---

## 12. 주요 파일

| 파일 | 역할 |
|---|---|
| `bot.py` | Telegram 입력, session 격리, 최종 저장과 출력 객체 관리 |
| `grading_agents.py` | semantic grading orchestration과 최종 persistence |
| `grading_identity.py` | 문제·제출 정규화와 재현성 identity |
| `question_type_router.py` | 문제문 및 Topic Pack canonical contract 기반 deterministic lens |
| `question_type_coverage_adapter.py` | coverage 정규화·상태 집계와 canonical lens reconciliation |
| `question_demand_contract.py` | 문제문 추출, Topic Pack 8축 bridge와 canonical lens contract |
| `explicit_requirement_cap.py` | 명시적 핵심 요구의 실제 누락 hard cap |
| `question_type_coverage_score_adjuster.py` | coverage 보정 후보와 strict 적용 |
| `control_valve_formula_checker.py` | 제어밸브 topic-specific deterministic checker |
| `control_valve_correctness_bridge.py` | checker finding을 evidence contract로 연결 |
| `verified_defect_reconciliation.py` | verified defect와 explicit coverage 동기화 |
| `evaluation_ledger.py` | 원자 요구별 coverage·검증 오류의 단일 정규 상태 원장 |
| `evidence_calibration.py` | 원장 근거 기반 confidence·strong 최종 상한 |
| `verified_correctness_score_cap.py` | topic-neutral verified fatal·core major 총점 hard cap |
| `accuracy_release_gate.py` | 전문가 교차 주제 정확도 기반 운영 배포 READY/HOLD 판정 |
| `layer_evidence_guard.py` | layer별 evidence와 single-owner 제한 |
| `logic_check_evaluator.py` | 핵심 이론 오류 평가 병합 |
| `difficulty_score_ceiling.py` | difficulty ceiling 평가와 strict 적용 |
| `grade_score_reconciler.py` | 최종 점수·cap·score range 정합성 |
| `generic_grading_contract.py` | Topic-neutral demand·claim·evidence·D/E requirement 계약 |
| `runtime_grading_provenance.py` | 최종 grade에 process-stable 실행 provenance 첨부 |
| `verdict_consistency.py` | 구조화 판정과 최종 서술·합격·고득점 판정 정합성 |
| `grade_output_summarizer.py` | Telegram 요약과 deterministic fallback |
| `scripts/rubric_manager.py` | Rubric과 Topic Pack 관리 |
| `scripts/validate_release.sh` | release 전 통합 검증 |

---

## 13. 유지 원칙

1. 루트 README에는 프로젝트 개요와 현재 운영 계약만 유지합니다.
2. 상세 설계와 운영 절차는 `docs/`에서 관리합니다.
3. 과거 migration log와 긴 실행 로그를 README에 누적하지 않습니다.
4. 문서의 수치와 개수는 source JSON과 validation 결과를 기준으로 갱신합니다.
5. `incorrect`와 `missing`을 같은 누락 상태로 설명하지 않습니다.
6. B completeness와 C correctness를 중복 감점하지 않습니다.
7. `warn`을 실제 점수 변경으로 설명하지 않습니다.
8. Logic fatal, recommended ceiling과 실제 applied cap을 구분합니다.
9. Question Type을 답안 내용으로 바꾸지 않습니다.
10. 저장 객체와 Telegram 출력 객체가 다르다고 설명하지 않습니다.
11. 문서와 runtime이 충돌하면 현재 코드, Rubric source와 회귀 결과를 우선 확인합니다.
12. Topic Pack 어휘와 generic grading contract를 결합하지 않습니다.
13. 서로 다른 Python 프로세스의 `engine_process_started_at`을 exact match하지 않습니다.
14. 배포와 probe의 provenance 비교에서는 안정 필드 5개를 exact match하고 process timestamp를 별도로 검증합니다.

## 설계·운영 문서

- [Topic Router v2 설계·운영 문서](docs/topic_router_v2.md) — Question Demand, Semantic Router, SINGLE/MULTI/GENERAL/AMBIGUOUS 모드, Hybrid General, demand-scoped grading 및 운영 feature gate를 정리합니다.
