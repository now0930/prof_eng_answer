# Topic Pack Workflow

이 문서는 새 Topic을 추가하거나 기존 Topic을 보강할 때의 현재 표준 workflow를 정의한다.

Topic Pack 구조와 현재 inventory는 `topic_pack_architecture.md`, JSON 내용 기준은 `rubric_authoring_guide.md`를 함께 본다.

> **채점 일관성 정본:** 문제 요구 축, 답안 축, Fact 증거 게이트, 점수 항목 간 전파 제한과 판정 정합성은 [`grading_architecture.md`](grading_architecture.md)의 ‘채점 일관성’ 절을 따른다. 이 문서는 해당 계약을 중복 정의하지 않고 실행 절차만 설명한다.

> **실행 계약:** 프로그램은 이 Markdown을 파싱하지 않는다. 신규 Topic의 순서·승인·해시·rollback은 `scripts/topic_pack_workflow_controller.py`, `validate_topic_pack_release.py`와 `rubric_manager.py add-topic/approve-topic`이 강제한다. 코딩 에이전트는 루트 `AGENTS.md`에 따라 작업 전 이 문서를 읽는다.


## 1. 핵심 원칙

```text
요구사항과 Topic 경계를 먼저 확정한다.
Topic Sheet는 사람이 검토한다.
source JSON은 직접 작성하거나 검토 가능한 보조 생성 경로로 만든다.
generated bank는 직접 수정하지 않는다.
Topic source와 integration rebuild를 분리한다.
한 Topic의 변경은 한 Topic 단위로 검증·commit한다.
```

LLM 결과는 Topic Sheet 밖의 기술 사실을 추가하는 근거가 아니다. 보조 생성 결과가 신규 scaffold의 canonical 경로에 놓이더라도 사람의 의미 검토와 validator 통과 전에는 승인된 source가 아니다.

## 2. 전체 흐름

```text
1. Candidate와 기존 Topic 중복 확인
2. Topic Sheet에서 ownership·Fact·negative boundary 확정
3. add-topic으로 동일 topic_id의 관리되는 scaffold 생성
4. source JSON 직접 작성 또는 Topic Sheet 기반 보조 생성
5. README와 source JSON을 사람이 의미 검토
6. approve-topic으로 사람 검토·source hash·focused validation·promote 기록
7. 변경 위험에 따라 routing/live smoke와 Golden case 보강
8. 통합 시점에 전체 inventory validation
9. commit·push 후 local/tracking/remote SHA와 CI 확인
10. runtime 영향이 있으면 별도 deployment Gate 수행
```

## 3. 파일 구조

```text
rubrics/topic_packs/<topic_id>/
├── README.md
├── fact_anchor.json
├── logic_check.json
├── model_answer.json
├── topic_importance.json
├── question_demand_axes.json  # 선택: canonical explicit-demand contract
└── topic_status.json          # 선택: 상태 metadata
```

Topic Sheet:

```text
docs/topic_sheets/<topic_id>.md
```

`add-topic`으로 만든 Pack의 `topic_status.json`은 `draft / human_review_required`에서 시작한다. `approve-topic`은 reviewer, 승인 시점과 canonical source hash를 기록한다. 이후 README 또는 source JSON이 바뀌면 승인이 자동 무효화되어 promote와 전체 integration이 실패한다. 기존 77개 legacy Pack에는 이 계약을 소급 강제하지 않는다.

Generated bank:

```text
rubrics/generated/
├── fact_anchors.generated.json
├── logic_check_profiles.generated.json
├── logic_checks.generated.json
├── model_answers.generated.json
├── topic_importance.generated.json
└── topic_pack_manifest.generated.json
```

## 4. Topic 범위 확정

작성 전에 다음을 정한다.

- 대표 기출/예상 문제
- 문제에서 직접 요구하는 축
- 핵심 정답 Fact
- 수식과 조건
- 현장 적용 판단
- fatal wrong claim
- warn-level 부족
- false positive
- 인접 Topic과 ownership
- expected question pattern

Topic이 너무 넓으면 routing alias와 Logic Check 적용 범위가 흐려진다.

## 5. Topic ID

원칙:

- 영어 소문자와 underscore
- 핵심 개념과 출제 축을 함께 표현
- 기존 Topic과 겹치지 않음
- 한 문제군의 ownership을 설명할 수 있을 정도로 구체적
- broad umbrella 이름 금지

좋은 예:

```text
second_order_lag_response_by_damping_ratio
control_valve_sizing_cv_kv_reynolds_liquid_selection
industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience
```

## 6. Topic README와 Topic Sheet

Topic Pack README는 사람이 읽는 설명서다.

권장 내용:

- 목적
- 대표 문제
- Topic boundary
- 핵심 정답
- 인정 가능한 표현
- fatal 오류
- warn 수준
- false positive
- 현장 적용
- 인접 Topic handoff
- 검토 메모

Topic Sheet는 JSON authoring 전 구조화 input이다.

권장 섹션:

1. Topic metadata
2. Scope and ownership
3. Core correct facts
4. Acceptable expressions
5. Fatal wrong claims
6. Warn-level weak claims
7. False positive cautions
8. Expected question patterns
9. Fact Anchor guidance
10. Model Answer guidance
11. Logic Check guidance
12. Topic Importance guidance
13. Cross-topic handoff
14. Human review checklist

## 7. Source JSON authoring

Topic Sheet를 확정한 뒤 직접 작성 또는 보조 생성 중 하나를 선택한다. 두 경로 모두 같은 schema, 사람의 diff 검토와 focused validation을 적용한다.

기존 Topic Pack 중 schema가 가장 가까운 파일을 template로 사용한다.

작성 전 확인:

```bash
find rubrics/topic_packs/<reference_topic> \
  -maxdepth 1 -type f -print | sort
```

JSON은 다음 원칙을 지킨다.

- 기존 top-level schema 유지
- nested object/list shape 유지
- validator가 모르는 pseudo field 금지
- required field 누락 금지
- topic_id 일치
- cross-reference anchor ID 실존 확인
- broad alias 최소화
- expected question과 Topic ownership 일치

Generator는 authoring 시간을 줄이는 도구이며 승인 주체가 아니다. 기존 검토본을 보호하고, 생성 결과의 기술 사실·경계·교차 참조를 사람이 검토한다.

### 7.1 Topic Sheet 기반 보조 생성

신규 Topic의 표준 시작 명령은 다음과 같다. `--generate`를 생략하면 관리되는 scaffold만 만들고 JSON은 직접 작성한다.

```bash
python3 scripts/rubric_manager.py add-topic \
  --topic-id <topic_id> \
  --title "<한글 제목>" \
  --sheet docs/topic_sheets/<topic_id>.md \
  --question-type <QUESTION_TYPE> \
  --difficulty <DIFFICULTY> \
  --generate
```

생성기는 Topic Sheet만 기술 내용의 근거로 사용한다. 4개 JSON 호출은 두 묶음으로 병렬화하고 일관성 검토를 마지막에 수행한다. 신규 scaffold만 기본 canonical source로 승격하며, 기존 검토본은 `--overwrite` 없이는 교체하지 않는다. 기존 source를 보존한 초안이 필요하면 `--candidate-only`를 사용한다. 생성 또는 검증 실패 시 canonical source는 작업 전 상태로 복구된다.

사람이 README와 4개 JSON의 기술 사실·ownership·fatal/false-positive 경계를 검토한 뒤 다음 명령으로 승인한다.

```bash
python3 scripts/rubric_manager.py approve-topic \
  --topic-id <topic_id> \
  --reviewer <reviewer_id>
```

승인 명령은 draft 검증, 사람 승인 metadata와 source hash 기록, 재검증과 generated promote를 한 transaction으로 수행한다. promote가 실패하면 승인 상태와 generated output을 복구한다. 실제 provider routing 확인이 필요한 경우에만 `--smoke`를 추가한다.

## 8. Fact Anchor

Fact Anchor는 “정답 요소가 있는가”를 본다.

포함:

- 정의
- 핵심 식
- 변수와 단위
- 조건
- 분류
- 원리
- 인과관계
- 비교축
- 현장 판단의 기반 Fact

포함하지 않음:

- 오답 regex
- 감점 문구
- fatal cap 정책
- verifier-only condition
- safe exception 중심의 rule

Atomic Fact로 분리한다.

## 9. Model Answer

Model Answer는 정답 문장 matching 파일이 아니다.

포함:

- representative question
- expected question pattern
- topic aliases
- 답안 구조
- high-score features
- common missing points
- low-score patterns
- field connection
- adjacent Topic handoff

Alias는 routing을 흔들 정도로 넓게 쓰지 않는다.

## 10. Topic Importance

Topic Importance는 difficulty와 시험 전략 metadata를 제공한다.

포함:

- difficulty
- selection importance
- primary question type
- high-band unlock conditions
- omission/fatal risk
- field judgement
- revision note

Difficulty는 점수를 직접 주지 않는다.

## 11. Logic Check

Logic Check는 “정답과 직접 충돌하는가”를 본다.

포함:

- fatal wrong claim
- major/warn claim
- wrong pattern
- safe condition
- false positive caution
- affected layer
- recommended ceiling metadata
- verifier focus
- D/E claim trust metadata

단순 누락을 fatal로 만들지 않는다.

좋은 답안에 등장할 수 있는 부정·비교 표현을 broad regex로 잡지 않는다.

## 12. Schema validation 주의

최근 Topic Pack 확장에서 특히 확인할 항목:

- expected question object의 required anchor reference key
- recommended outline item의 `section`
- object type field를 string placeholder로 두지 않음
- topic_importance의 difficulty classification
- cross-lane / cross-topic owner
- generated manifest topic count
- source와 generated topic_id 일치

Validator가 기대하는 실제 key 이름을 확인하고 임의의 유사 key를 만들지 않는다.

## 13. Topic focused validation

기본 순서:

```text
python3 -m py_compile <변경 관련 Python이 있을 때>
→ topic focused tests
→ schema / quality validator
→ git diff --check
→ 필요한 범위의 validate-all
```

Topic source만 변경했고 runtime Python이 바뀌지 않았다면 container 전체 회귀를 반복하지 않는다.

단일 Topic의 빠른 release 검증과 generated promote는 다음 명령을 사용한다.

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release \
  --topic-id <topic_id> \
  --promote-generated
```

`--topic-id`를 생략하면 Git에서 변경된 Topic을 자동 선택한다. 변경 Topic이 없으면 모호한 전체 검증을 실행하지 않고 실패한다. 모든 Topic을 검사할 때만 `--all`을 사용한다. live LLM smoke는 외부 모델과 container 환경이 필요하므로 기본 검증에서 제외하며 필요할 때 `--smoke`를 명시한다.

## 14. 의미 감사

자동 validator 통과만으로 완료하지 않는다.

확인:

- Fact가 실제로 맞는가
- expected question과 content가 일치하는가
- high-band 조건이 Topic 내용과 일치하는가
- Logic Check가 정답을 fatal로 잡지 않는가
- safe case가 충분한가
- 인접 Topic ownership을 침범하지 않는가
- broad alias가 다른 Topic routing을 끌어오지 않는가

여러 Topic을 병렬 작성했다면 integration 전 cross-topic semantic audit를 수행한다.

## 15. Commit 경계

권장:

```text
Topic A 작성
→ focused validation
→ Topic A local commit

Topic B 작성
→ focused validation
→ Topic B local commit
```

서로 다른 Topic을 하나의 대형 source commit으로 묶지 않는다.

공통 validator나 release gate 수정은 Topic source commit과 분리한다.

## 16. 병렬 lane

대규모 확장은 전용 worktree/branch를 사용할 수 있다.

원칙:

- lane별 소유 Topic 명확화
- 다른 lane source 수정 금지
- production common code 최소화
- Topic별 local commit
- lane-wide validation 후 push
- integration에서 patch-equivalence와 cross-topic ownership 확인

generated bank는 각 lane이 반복 생성하지 않고 최종 integration에서 한 번 rebuild하는 방식을 권장한다.

## 17. Generated rebuild

Source가 모두 확정된 integration 단계에서 generated bank를 갱신한다.

예:

```bash
PROMOTE_GENERATED=1 \
RUN_SMOKE_TOPIC_PACKS=0 \
RUN_GRADING_REPRODUCIBILITY=0 \
scripts/validate_release.sh
```

또는 통합 시점에 다음 전체 release/promote 명령을 사용한다.

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release \
  --all \
  --promote-generated
```

생성 대상은 6개다.

Generated JSON은 직접 편집하지 않는다.

## 18. Non-promote release validation

최종 generated commit 이후에는 GitHub Actions와 같은 non-promote 경로를 검증한다.

```bash
PROMOTE_GENERATED=0 \
RUN_SMOKE_TOPIC_PACKS=0 \
RUN_GRADING_REPRODUCIBILITY=0 \
scripts/validate_release.sh
```

이 경로는 generated output을 검증하되 promote하지 않아야 한다.

## 19. Hermetic regression

Committed test는 clean checkout에서 재현되어야 한다.

금지:

```text
data/sessions/<local-only-session-id>/input.txt
data/sessions/<local-only-session-id>/grade.json
```

재현 fixture:

```text
scripts/fixtures/<semantic_fixture_name>/
```

필요한 historical input을 fixture로 옮길 때는 개인 session ID를 영구 테스트 API로 사용하지 않는다.

## 20. Container smoke

Container smoke는 다음 변경에만 우선 수행한다.

- LLM integration
- container-only dependency
- container hostname
- mount / path
- runtime env
- deployment
- live Telegram persistence/output

Static Topic JSON, docs, pure validator test만 바뀐 경우 host focused validation과 release validation을 우선한다.

## 21. 최종 확인

```bash
git status --short
git diff --stat
git diff --check

python3 scripts/rubric_manager.py validate-all

PROMOTE_GENERATED=0 \
RUN_SMOKE_TOPIC_PACKS=0 \
RUN_GRADING_REPRODUCIBILITY=0 \
scripts/validate_release.sh
```

필요하면 detached clean worktree에서 release validation을 한 번 더 실행한다.

## 22. Push

모든 Topic과 integration 검증이 끝난 뒤 push한다.

대규모 parallel 작업에서는 중간 Topic마다 원격 push를 반복하지 않고 lane/batch 완료 후 push하는 방식을 권장한다.

Push 후 GitHub Actions validation이 해당 commit에서 `success`인지 확인한다.

## 23. Topic Pack 확장 Gate (`ab94b69` 이후)

### 23.1 Source와 분류 정본

- 기술 내용은 사람이 검토한 Topic Sheet와 Topic Pack source가 소유한다.
- 기본 source는 README와 4개 JSON이며 `question_demand_axes.json`, `topic_status.json`은 필요할 때만 추가한다.
- generated 6개 파일은 builder output이므로 직접 수정하지 않는다.
- 난이도 분류는 각 `topic_importance.json`에서 계산한다. Topic ID 목록이나 총계를 Python literal로 중복 등록하지 않는다.

### 23.2 빠른 기본 경로

```bash
# 신규 Topic 시작: 관리되는 draft 생성과 선택적 보조 authoring
python3 scripts/rubric_manager.py add-topic \
  --topic-id <topic_id> --title "<제목>" \
  --sheet docs/topic_sheets/<topic_id>.md --generate

# 사람 검토 후 승인·검증·promote
python3 scripts/rubric_manager.py approve-topic \
  --topic-id <topic_id> --reviewer <reviewer_id>

# 통합 시점에만 전체 inventory 검증
python3 scripts/rubric_manager.py validate-topic-pack-release --all
```

새 workflow로 관리되는 Topic은 승인 상태와 현재 source hash가 일치하지 않으면 generated promote와 `--all` 통합 검증을 통과할 수 없다. 외부 provider가 필요한 smoke는 기본 검증에서 제외하며 실제 routing/provider 동작을 확인해야 할 때만 승인 명령에 `--smoke`를 명시한다.

### 23.3 보조 생성 안전장치

- 4개 JSON 생성은 두 병렬 묶음과 마지막 일관성 검토로 수행한다.
- 신규 scaffold만 기본 canonical 경로에 승격한다.
- 기존 검토본은 `--overwrite` 없이는 바꾸지 않는다.
- canonical을 보존한 후보만 필요하면 `--candidate-only`를 사용한다.
- 생성 또는 검증 실패 시 canonical과 generated 상태를 작업 전으로 복구한다.
- 사람 승인 이후 canonical source가 바뀌면 content hash mismatch로 승인을 무효화한다.

### 23.4 위험 기반 회귀

모든 신규 Topic에 고정 개수의 Golden case를 강제하지 않는다. 다음 변경에는 정답·오답·경계 사례를 추가한다.

- scoring, fatal/major 또는 coverage 의미를 바꾸는 경우
- 안전 핵심 수식·단위·조건을 새로 소유하는 경우
- 기존 Topic과 routing 경계가 겹치는 경우
- 실제 과대·과소 채점 회귀를 수정하는 경우

별칭, 설명 문서처럼 채점 의미를 바꾸지 않는 변경은 focused validator로 충분하다.

### 23.5 완료 조건

- 변경 Topic focused validation 통과
- generated rebuild와 idempotence 통과
- 의도하지 않은 기존 Topic 변경 없음
- `git diff --check` 및 통합 전 `--all` 통과
- runtime 영향이 있으면 정확도·배포 Gate를 별도 통과
- local HEAD, tracking ref와 remote SHA 일치

과거 대규모 확장의 상세 postmortem은 [`archive/20260819_stage17e3_topic_pack_pipeline_postmortem.md`](archive/20260819_stage17e3_topic_pack_pipeline_postmortem.md)에만 보존한다.
