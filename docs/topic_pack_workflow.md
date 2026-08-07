# Topic Pack Workflow

이 문서는 새 Topic을 추가하거나 기존 Topic을 보강할 때의 현재 표준 workflow를 정의한다.

Topic Pack 구조와 현재 inventory는 `topic_pack_architecture.md`, JSON 내용 기준은 `rubric_authoring_guide.md`를 함께 본다.

## 1. 핵심 원칙

```text
요구사항과 Topic 경계를 먼저 확정한다.
Topic Sheet는 사람이 검토한다.
source JSON은 기존 schema를 기준으로 직접 작성한다.
generated bank는 직접 수정하지 않는다.
Topic source와 integration rebuild를 분리한다.
한 Topic의 변경은 한 Topic 단위로 검증·commit한다.
```

LLM을 사용할 수 있지만, opaque JSON generation 결과를 그대로 source of truth로 채택하지 않는다. 기존 schema와 validator를 기준으로 명시적으로 작성한 JSON diff를 사람이 검토한다.

## 2. 전체 흐름

```text
1. 문제 범위와 요구사항 Markdown 확정
2. 기존 Topic 검색과 ownership 경계 확인
3. topic_id 확정
4. Topic Pack skeleton / README 준비
5. Topic Sheet 작성·검토
6. 인접 Topic schema 확인
7. fact_anchor.json 직접 작성
8. model_answer.json 직접 작성
9. topic_importance.json 직접 작성
10. logic_check.json 직접 작성
11. topic focused validation
12. 의미 감사와 boundary 검토
13. Topic 단위 local commit
14. batch/lane 완료 후 integration
15. generated bank 6개 rebuild
16. release validation
17. clean checkout / GitHub Actions 확인
18. push
```

## 3. 파일 구조

```text
rubrics/topic_packs/<topic_id>/
├── README.md
├── fact_anchor.json
├── logic_check.json
├── model_answer.json
└── topic_importance.json
```

Topic Sheet:

```text
docs/topic_sheets/<topic_id>.md
```

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

## 7. JSON 직접 authoring

현재 표준 경로는 Topic Sheet를 확정한 뒤 source JSON을 직접 작성하는 방식이다.

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

Generator script가 존재하더라도 표준 source authoring을 대체하지 않는다. 사용한다면 초안 또는 schema 참고용으로만 사용하고 최종 JSON diff를 직접 검토한다.

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

또는 현재 `rubric_manager.py`의 release/promote 명령을 사용한다.

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
