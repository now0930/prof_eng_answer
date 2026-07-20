# Documentation Index

이 디렉터리는 `prof_eng_answer`의 운영, 채점 설계, Rubric authoring, Topic Pack과 Logic Check 문서를 관리합니다.

프로젝트 소개, 빠른 실행과 현재 runtime 계약은 루트 [`README.md`](../README.md)에서 확인합니다. 이 문서는 **문서 탐색, 정책 소유권과 source of truth**를 담당합니다.

---

## 1. 문서 경계

| 위치 | 책임 |
|---|---|
| 루트 `README.md` | 프로젝트 개요, 현재 채점 계약, 실행과 기본 검증 |
| `docs/README.md` | 문서 인덱스, 정책별 책임, source of truth와 유지 규칙 |
| `docs/*.md` | 주제별 상세 설계와 운영 기준 |
| `docs/topic_sheets/` | Topic Pack source JSON 작성 전 사람이 검토하는 Markdown |
| `docs/archive/` | 과거 설계, migration과 참고 이력 |

세부 알고리즘과 수치는 한 문서에 중복 복제하지 않습니다. 현재 동작과 충돌할 때는 runtime code, Rubric JSON과 focused regression을 우선합니다.

---

## 2. 작업별 문서 찾기

| 작업 | 우선 문서 | 관련 문서 |
|---|---|---|
| Bot 상태 확인, 재시작, 장애 대응 | [`operation_runbook.md`](operation_runbook.md) | [`docker_compose_usage.md`](docker_compose_usage.md) |
| Compose service, mount와 network 확인 | [`docker_compose_usage.md`](docker_compose_usage.md) | [`operation_runbook.md`](operation_runbook.md) |
| A/B/C/D/E와 최종 score flow 이해 | [`grading_architecture.md`](grading_architecture.md) | [`question_type_taxonomy.md`](question_type_taxonomy.md), [`difficulty_and_selection_strategy.md`](difficulty_and_selection_strategy.md) |
| Active Question Type과 deterministic lens 확인 | [`question_type_taxonomy.md`](question_type_taxonomy.md) | [`grading_architecture.md`](grading_architecture.md) |
| `incorrect`, `missing`과 hard cap 확인 | [`grading_architecture.md`](grading_architecture.md) | [`question_type_taxonomy.md`](question_type_taxonomy.md) |
| Verified defect와 single-owner 정책 확인 | [`grading_architecture.md`](grading_architecture.md) | [`logic_check_profiles_readme.md`](logic_check_profiles_readme.md) |
| Difficulty Profile과 ceiling 확인 | [`difficulty_and_selection_strategy.md`](difficulty_and_selection_strategy.md) | [`grading_architecture.md`](grading_architecture.md) |
| Gemini·CLOVA·Ollama 설정 확인 | [`llm_provider.md`](llm_provider.md) | [`operation_runbook.md`](operation_runbook.md) |
| Rubric source 작성·수정 | [`rubric_authoring_guide.md`](rubric_authoring_guide.md) | [`topic_pack_workflow.md`](topic_pack_workflow.md) |
| 새 topic 추가 또는 기존 topic 보강 | [`topic_pack_workflow.md`](topic_pack_workflow.md) | [`rubric_authoring_guide.md`](rubric_authoring_guide.md) |
| Logic Check 운영 기준 확인 | [`logic_check_profiles_readme.md`](logic_check_profiles_readme.md) | [`rubric_authoring_guide.md`](rubric_authoring_guide.md) |
| Logic Check Profile 초안 확인 | [`logic_check_profile_generator_prompt.md`](logic_check_profile_generator_prompt.md) | [`logic_check_profiles_readme.md`](logic_check_profiles_readme.md) |
| Rule-based Logic Check JSON 초안 확인 | [`logic_check_json_generator_prompt.md`](logic_check_json_generator_prompt.md) | [`logic_check_profiles_readme.md`](logic_check_profiles_readme.md) |
| Topic Sheet 검토 | [`topic_pack_workflow.md`](topic_pack_workflow.md) | `topic_sheets/<topic_id>.md` |
| 과거 판단 근거 확인 | `archive/` | 현재 기준 문서와 반드시 대조 |

---

## 3. 현재 기준 문서

### 운영

| 문서 | 책임 |
|---|---|
| [`operation_runbook.md`](operation_runbook.md) | 운영 상태 점검, 재시작, 장애 대응, polling과 운영 smoke |
| [`docker_compose_usage.md`](docker_compose_usage.md) | Compose 위치, service, container, mount, network와 실행 명령 |

### 채점 설계

| 문서 | 책임 |
|---|---|
| [`grading_architecture.md`](grading_architecture.md) | grading pipeline, A/B/C/D/E, score adjustment, cap, verified defect, final persistence |
| [`question_type_taxonomy.md`](question_type_taxonomy.md) | active type 4종, legacy mapping, question-only lens, coverage 상태와 최종 type/name |
| [`difficulty_and_selection_strategy.md`](difficulty_and_selection_strategy.md) | Difficulty Profile, THEORY_CORE, recommended ceiling과 applied cap |
| [`llm_provider.md`](llm_provider.md) | provider routing, fallback, JSON parsing과 Python 후처리 경계 |

### Rubric와 Topic Pack

| 문서 | 책임 |
|---|---|
| [`rubric_authoring_guide.md`](rubric_authoring_guide.md) | Fact Anchor, Model Answer, Topic Importance와 Logic Check source 작성 기준 |
| [`topic_pack_workflow.md`](topic_pack_workflow.md) | 요구사항 Markdown → Topic Sheet → source JSON → generated bank → focused validation |

### Logic Check

| 문서 | 책임 |
|---|---|
| [`logic_check_profiles_readme.md`](logic_check_profiles_readme.md) | Logic Check source, profile, evaluator, verifier와 D/E claim trust |
| [`logic_check_profile_generator_prompt.md`](logic_check_profile_generator_prompt.md) | Profile 초안 작성용 prompt |
| [`logic_check_json_generator_prompt.md`](logic_check_json_generator_prompt.md) | Rule-based Logic Check JSON 초안 작성용 prompt |

Generator prompt는 source of truth가 아닙니다. 사람이 검토한 Topic Pack JSON과 현재 runtime code가 기준입니다.

---

## 4. 현재 runtime 계약 요약

이 절은 문서 탐색을 위한 요약입니다. 세부 수치의 source of truth는 아래 표의 파일입니다.

| 항목 | 현재 계약 | Source of truth |
|---|---|---|
| 배점 | A/B/C/D/E = 3/6/8/6/2 | `rubrics/scoring_model/default.json` |
| Active Question Type | 4종 | `rubrics/question_types/default.json`, Question Type modules |
| Model Answer | 57개 | `rubrics/model_answers/industrial_instrumentation_control.json` |
| Fact Topic | 55개 | `rubrics/fact_anchors/industrial_instrumentation_control.json` |
| Topic Importance | 8개 | `rubrics/topic_importance/industrial_instrumentation_control.json` |
| Lens 입력 | 문제문만 사용 | `question_type_router.py`, `grading_identity.py` |
| Coverage 상태 | `present`, `partial`, `incorrect`, `missing` | `question_type_coverage_adapter.py` |
| Hard cap | high-confidence 핵심 `missing`에만 적용 | `explicit_requirement_cap.py` |
| Correctness owner | verified Fact 오류는 기본 C owner | `verified_defect_reconciliation.py`, `layer_evidence_guard.py` |
| 최종 저장 | score reconciliation 후 coverage finalizer를 적용한 객체 저장 | `grading_agents.py`, `bot.py` |
| Session | 완료 세션 격리, 동일 초 ID 충돌 방지 | `bot.py` |

Question Type을 semantic grader의 자유 선택 결과로 설명하지 않습니다. 현재 lens는 문제문 기반 deterministic routing과 confidence gate가 기준입니다.

Verified defect가 explicit requirement에 연결되면 표시 상태는 `incorrect`가 됩니다. 이 동기화는 기본적으로 score-neutral이며, 동일 오류를 B와 C 또는 D/E에 중복 귀속하지 않습니다.

---

## 5. 정책별 소유 문서와 runtime

| 정책 | 상세 소유 문서 | 주요 runtime |
|---|---|---|
| A/B/C/D/E 배점과 score flow | `grading_architecture.md` | `grading_agents.py`, `grade_score_reconciler.py` |
| Deterministic grading identity | `grading_architecture.md` | `grading_identity.py` |
| Question-only type lens | `question_type_taxonomy.md` | `question_type_router.py`, `question_type_taxonomy.py` |
| `present`, `partial`, `incorrect`, `missing` | `question_type_taxonomy.md` | `question_type_coverage_adapter.py` |
| 명시적 핵심 요구 누락 hard cap | `grading_architecture.md` | `explicit_requirement_cap.py` |
| Coverage `warn`, `strict`, `off` | `grading_architecture.md` | `question_type_coverage_score_adjuster.py` |
| Verified defect와 explicit requirement 연결 | `grading_architecture.md` | `verified_defect_reconciliation.py` |
| Topic-specific correctness finding | `grading_architecture.md` | `control_valve_formula_checker.py`, `control_valve_correctness_bridge.py` |
| Single-owner layer 제한 | `grading_architecture.md` | `layer_evidence_guard.py` |
| Logic fatal과 D/E claim trust | `logic_check_profiles_readme.md` | `logic_check_evaluator.py`, `logic_llm_verifier.py` |
| Difficulty Profile과 recommended ceiling | `difficulty_and_selection_strategy.md` | `difficulty_strategy.py`, `difficulty_score_ceiling.py` |
| 실제 numeric cap과 `cap 적용` 출력 | `grading_architecture.md` | `grade_score_reconciler.py`, `grade_output_summarizer.py` |
| 최종 coverage persistence | `grading_architecture.md` | `grading_agents.py`, `bot.py` |
| 완료 세션 격리와 ID 충돌 방지 | `operation_runbook.md` | `bot.py` |
| Rubric source와 generated bank | `rubric_authoring_guide.md` | `rubric_bank_paths.py`, `rubric_registry.py` |
| Topic Pack 생성·검증·promote | `topic_pack_workflow.md` | `scripts/rubric_manager.py` |

이 인덱스에는 세부 알고리즘을 복제하지 않습니다. 새 정책을 추가할 때는 상세 문서와 runtime owner를 함께 등록합니다.

---

## 6. Source of Truth

| 주제 | 우선 기준 |
|---|---|
| Telegram 입력, session과 최종 저장 | `bot.py` |
| Grading orchestration과 최초 persistence | `grading_agents.py` |
| 최종 점수, cap과 score range | `grade_score_reconciler.py` |
| A/B/C/D/E | `rubrics/scoring_model/default.json`과 runtime scoring code |
| Question Type | `rubrics/question_types/default.json`, `question_type_router.py` |
| Explicit coverage | `question_type_coverage_adapter.py` |
| 명시적 요구 hard cap | `explicit_requirement_cap.py` |
| Verified defect mapping | `verified_defect_reconciliation.py` |
| Layer별 evidence owner | `layer_evidence_guard.py` |
| Coverage score adjustment | `question_type_coverage_score_adjuster.py` |
| Difficulty ceiling | `difficulty_score_ceiling.py` |
| Logic Check | Logic Check source JSON, profile JSON, evaluator와 verifier |
| Topic Pack | `rubrics/topic_packs/<topic_id>/` |
| Generated bank | `rubrics/generated/*.generated.json` |
| 실제 운영 | 현재 Compose 설정과 실행 중인 container |
| 회귀 계약 | `scripts/test_*.py`와 release validation 결과 |

문서와 runtime이 충돌하면 현재 commit의 code, JSON, focused regression과 실제 container를 확인합니다. 과거 commit 메시지나 archive 문서를 현재 정책으로 사용하지 않습니다.

---

## 7. 작업 디렉터리

### `topic_sheets/`

Topic Pack source JSON을 만들기 전에 사람이 검토하는 구조화 Markdown을 보관합니다. Topic Sheet는 runtime Rubric이 아닙니다.

### `archive/`

과거 설계, migration 판단과 긴 검증 기록을 보관합니다. Archive 내용은 현재 기준 문서와 대조하지 않고 직접 적용하지 않습니다.

---

## 8. 문서 작성 규칙

1. 루트 README와 상세 문서의 책임을 분리합니다.
2. 같은 정책의 세부 수치와 알고리즘을 여러 문서에 복제하지 않습니다.
3. 현재 존재하는 파일만 인덱스에 등록합니다.
4. 수치와 개수는 source JSON과 validation 결과로 확인합니다.
5. Migration 중간 상태와 일회성 실행 로그는 `archive/`에 둡니다.
6. `incorrect`와 `missing`을 같은 누락으로 설명하지 않습니다.
7. B completeness와 C correctness를 같은 감점으로 설명하지 않습니다.
8. Coverage `warn`을 실제 점수 변경으로 설명하지 않습니다.
9. Logic fatal, recommended ceiling과 actually applied cap을 구분합니다.
10. Question Type을 답안 내용에 따라 바뀌는 값으로 설명하지 않습니다.
11. Topic Pack source와 generated output을 같은 역할로 설명하지 않습니다.
12. Generator prompt와 사람이 검토하는 운영 guide를 구분합니다.
13. 최종 저장 객체와 Telegram 출력 객체가 다르다고 설명하지 않습니다.
14. 완료된 채점이 같은 session 디렉터리를 재사용한다고 설명하지 않습니다.

---

## 9. 문서 변경 후 확인

문서만 수정했을 때 최소 검증:

```bash
git diff --check -- README.md docs/README.md
```

추가로 확인할 항목:

- Markdown heading 구조
- 상대 링크 대상 존재 여부
- A/B/C/D/E 배점
- Active Question Type 4종
- Model Answer, Fact Topic과 Topic Importance 개수
- 현재 runtime owner 파일
- 오래된 semantic lens와 session 재사용 설명 제거

문서가 runtime 정책을 설명한다면 관련 focused regression 결과와 비교합니다. 코드나 JSON을 함께 변경하지 않았다면 불필요한 container smoke를 반복하지 않습니다.

전체 release validation은 루트 [`README.md`](../README.md)의 절차를 따릅니다.

---

## 10. 새 문서 추가 기준

새 문서는 다음 조건을 만족할 때만 추가합니다.

- 기존 문서에 넣으면 책임 범위가 지나치게 넓어짐
- 독립적인 운영 또는 설계 수명주기를 가짐
- 명확한 runtime owner 또는 source JSON이 있음
- 현재 기준 문서와 archive 문서를 구분할 수 있음

새 문서를 추가하면 다음을 함께 갱신합니다.

1. 이 인덱스의 작업별 문서 표
2. 현재 기준 문서 표
3. 정책별 소유 문서와 runtime 표
4. Source of Truth 표
5. 상대 링크 검증
