# Documentation Index

이 디렉터리는 `prof_eng_answer`의 운영, 채점 설계, Rubric authoring, Topic Pack과 Logic Check 문서를 관리합니다.

프로젝트 소개, 빠른 실행, 핵심 정책과 기본 검증은 루트 [`README.md`](../README.md)에서 확인합니다. 이 문서는 **문서 탐색과 책임 범위**만 담당하며 루트 README의 내용을 반복하지 않습니다.

---

## 1. 문서 경계

| 위치 | 담당 범위 |
|---|---|
| [`../README.md`](../README.md) | 프로젝트 소개, 빠른 실행, 핵심 정책, 기본 검증 |
| `docs/README.md` | 문서 인덱스, 문서별 책임, source of truth, 유지 규칙 |
| `docs/*.md` | 주제별 상세 설계와 운영 기준 |
| `docs/topic_sheets/` | 사람이 검토하는 Topic Pack 구조화 입력 |
| `docs/archive/` | 과거 설계와 migration 참고 이력 |

한 정책의 상세 설명은 한 문서만 소유합니다. 다른 문서에서는 링크와 경계 설명만 제공합니다.

---

## 2. 작업별 문서 찾기

| 작업 | 우선 문서 | 관련 문서 |
|---|---|---|
| Bot 상태 확인, 재시작, 장애 대응 | [`operation_runbook.md`](operation_runbook.md) | [`docker_compose_usage.md`](docker_compose_usage.md) |
| Compose service, mount, 실행 구조 확인 | [`docker_compose_usage.md`](docker_compose_usage.md) | [`operation_runbook.md`](operation_runbook.md) |
| A/B/C/D/E와 최종 score flow 이해 | [`grading_architecture.md`](grading_architecture.md) | [`question_type_taxonomy.md`](question_type_taxonomy.md), [`difficulty_and_selection_strategy.md`](difficulty_and_selection_strategy.md) |
| 문제 유형과 coverage 기준 확인 | [`question_type_taxonomy.md`](question_type_taxonomy.md) | [`grading_architecture.md`](grading_architecture.md) |
| THEORY_CORE, 난이도와 ceiling 확인 | [`difficulty_and_selection_strategy.md`](difficulty_and_selection_strategy.md) | [`grading_architecture.md`](grading_architecture.md) |
| Gemini·CLOVA·Ollama 설정 확인 | [`llm_provider.md`](llm_provider.md) | [`operation_runbook.md`](operation_runbook.md) |
| Rubric source 작성·수정 | [`rubric_authoring_guide.md`](rubric_authoring_guide.md) | [`topic_pack_workflow.md`](topic_pack_workflow.md) |
| 새 topic 추가 또는 기존 topic 보강 | [`topic_pack_workflow.md`](topic_pack_workflow.md) | [`rubric_authoring_guide.md`](rubric_authoring_guide.md) |
| Logic Check 운영 기준 확인 | [`logic_check_profiles_readme.md`](logic_check_profiles_readme.md) | [`rubric_authoring_guide.md`](rubric_authoring_guide.md) |
| Logic Check Profile 초안 생성 | [`logic_check_profile_generator_prompt.md`](logic_check_profile_generator_prompt.md) | [`logic_check_profiles_readme.md`](logic_check_profiles_readme.md) |
| rule-based Logic Check JSON 초안 생성 | [`logic_check_json_generator_prompt.md`](logic_check_json_generator_prompt.md) | [`logic_check_profiles_readme.md`](logic_check_profiles_readme.md) |
| Topic Sheet 검토 | [`topic_pack_workflow.md`](topic_pack_workflow.md) | `topic_sheets/<topic_id>.md` |
| 과거 판단 근거 확인 | `archive/` | 현재 기준 문서와 반드시 대조 |

---

## 3. 현재 기준 문서

### 운영

| 문서 | 책임 |
|---|---|
| [`operation_runbook.md`](operation_runbook.md) | 운영 상태 점검, 재시작, 장애 대응, 중복 polling과 운영 smoke |
| [`docker_compose_usage.md`](docker_compose_usage.md) | Compose 위치, service, container, mount, network와 실행 명령 |

### 채점 설계

| 문서 | 책임 |
|---|---|
| [`grading_architecture.md`](grading_architecture.md) | grading pipeline, A/B/C/D/E, score adjustment, cap 적용 순서와 final reconciliation |
| [`question_type_taxonomy.md`](question_type_taxonomy.md) | active type, legacy mapping, detector, sub-criteria, coverage 상태와 최종 type/name |
| [`difficulty_and_selection_strategy.md`](difficulty_and_selection_strategy.md) | Difficulty Profile, 문항 선택 전략, THEORY_CORE, recommended ceiling과 applied cap |
| [`llm_provider.md`](llm_provider.md) | provider routing, fallback, JSON parsing과 Python 후처리 경계 |

### Rubric와 Topic Pack

| 문서 | 책임 |
|---|---|
| [`rubric_authoring_guide.md`](rubric_authoring_guide.md) | Fact Anchor, Model Answer, Topic Importance와 Logic Check source 작성 기준 |
| [`topic_pack_workflow.md`](topic_pack_workflow.md) | Topic Pack README → Topic Sheet → source JSON → generated bank → smoke 절차 |

### Logic Check

| 문서 | 책임 |
|---|---|
| [`logic_check_profiles_readme.md`](logic_check_profiles_readme.md) | Logic Check Profile 운영, truth schema, fatal·safe condition과 false-positive 방지 |
| [`logic_check_profile_generator_prompt.md`](logic_check_profile_generator_prompt.md) | LLM verifier profile JSON 초안 생성 계약 |
| [`logic_check_json_generator_prompt.md`](logic_check_json_generator_prompt.md) | rule-based Logic Check JSON 초안 생성 계약 |

---

## 4. 정책별 소유 문서

| 정책 | 상세 소유 문서 | 주요 runtime |
|---|---|---|
| A/B/C/D/E 배점과 score flow | `grading_architecture.md` | `grading_agents.py`, `grade_score_reconciler.py` |
| `present`, `partial`, `incorrect`, `missing` | `question_type_taxonomy.md` | `question_type_coverage_adapter.py` |
| 명시적 핵심 요구 누락 hard cap | `grading_architecture.md` | `explicit_requirement_cap.py` |
| coverage `warn`, `strict`, `off` | `grading_architecture.md` | `question_type_coverage_score_adjuster.py` |
| 최종 Question Type과 한국어 이름 | `question_type_taxonomy.md` | `question_type_output_adapter.py` |
| Logic fatal과 D/E claim trust | `logic_check_profiles_readme.md` | `logic_check_evaluator.py`, `logic_llm_verifier.py` |
| Difficulty Profile과 recommended ceiling | `difficulty_and_selection_strategy.md` | `difficulty_strategy.py`, `difficulty_score_ceiling.py` |
| 실제 numeric cap과 `cap 적용` 출력 | `grading_architecture.md` | `grade_score_reconciler.py`, `grade_output_summarizer.py` |
| Rubric source와 generated bank | `rubric_authoring_guide.md` | `rubric_bank_paths.py`, `rubric_registry.py` |
| Topic Pack 생성·검증·promote | `topic_pack_workflow.md` | `scripts/rubric_manager.py` |

이 인덱스에는 정책의 세부 수치와 알고리즘을 복제하지 않습니다.

---

## 5. Source of Truth

| 주제 | 우선 기준 |
|---|---|
| Telegram 입력과 fallback 출력 | `bot.py`, `grade_output_summarizer.py` |
| grading orchestration | `grading_agents.py`, `difficulty_output_adapter.py` |
| 최종 점수, cap과 score range | `grade_score_reconciler.py` |
| A/B/C/D/E | `rubrics/scoring_model/default.json`과 runtime scoring code |
| Question Type | `rubrics/question_types/default.json`과 Question Type module |
| 명시적 요구 hard cap | `explicit_requirement_cap.py` |
| coverage score adjustment | `question_type_coverage_score_adjuster.py` |
| Difficulty ceiling | `difficulty_score_ceiling.py` |
| Logic Check | Logic Check source JSON, profile JSON, evaluator와 verifier |
| Topic Pack | `rubrics/topic_packs/<topic_id>/` |
| generated bank | `rubrics/generated/*.generated.json` |
| 실제 운영 | 현재 Compose 설정과 실행 중인 container |

문서와 runtime이 충돌하면 문서 내용을 추측으로 유지하지 말고 위 source와 검증 결과를 확인해 문서를 갱신합니다.

---

## 6. 작업 디렉터리

### `topic_sheets/`

Topic Pack source JSON을 만들기 전에 사람이 검토하는 구조화 Markdown input을 보관합니다. Topic Sheet는 runtime Rubric이 아닙니다.

### `archive/`

과거 설계, migration 기록과 폐기된 접근 방식을 보관합니다. 현재 동작의 기준으로 단독 인용하지 않습니다.

---

## 7. 문서 작성 규칙

1. 한 정책의 상세 설명은 한 문서만 소유합니다.
2. 루트 README의 실행·검증 내용을 세부 문서에 그대로 복제하지 않습니다.
3. 세부 문서 사이에도 긴 표, 명령과 정책 문구를 복사하지 않습니다.
4. 현재 존재하지 않는 파일을 인덱스에 등록하지 않습니다.
5. migration 중간 상태와 일회성 검증 로그는 `archive/`로 이동합니다.
6. `incorrect`와 `missing`을 같은 누락으로 설명하지 않습니다.
7. coverage `warn`을 실제 점수 변경으로 설명하지 않습니다.
8. Logic fatal, recommended cap과 actually applied cap을 구분합니다.
9. Topic Pack source와 generated output을 같은 역할로 설명하지 않습니다.
10. generator prompt와 사람이 읽는 운영 guide를 분리합니다.

---

## 8. 문서 변경 후 확인

문서만 수정한 경우:

```bash
git diff --check
git diff --stat
git status --short --branch
```

문서가 runtime 정책을 설명한다면 해당 focused regression도 실행합니다. 전체 release validation과 Rubric Audit은 루트 [`README.md`](../README.md)의 검증 절차를 따릅니다.

---

## 9. 새 문서 추가 기준

새 문서를 만들기 전에 다음을 확인합니다.

1. 기존 문서에 둘 수 없는 독립 책임이 있는가?
2. 일회성 작업 로그가 아니라 장기 기준인가?
3. 기존 문서와 내용이 중복되지 않는가?
4. 담당 source code 또는 JSON이 명확한가?
5. 이 인덱스에 읽는 목적과 책임 범위를 추가할 수 있는가?

조건을 만족하지 않으면 새 파일보다 기존 담당 문서를 수정합니다.
