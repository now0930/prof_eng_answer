# Topic Pack Workflow 문서

> 기준 시점: `topic_router.py`를 분리하기 전까지의 topic pack 자동화 구조 정리  
> 목적: 산업계측제어기술사 채점 Bot에서 topic pack을 어디에 저장하고, 어떻게 검토하며, legacy/generated 평가 모드를 어떻게 운영하는지 명확히 정리한다.

---

## 1. 핵심 결론

현재 topic pack 관련 구조는 다음 원칙으로 운영한다.

```text
원천 데이터:
  rubrics/topic_packs/<topic_id>/

빌드 산출물:
  rubrics/generated/*.generated.json

기존 legacy bank:
  rubrics/*/industrial_instrumentation_control.json

평가 기본 모드:
  generated topic bank로 전환 예정 또는 전환 후 사용

legacy fallback:
  RUBRIC_BANK_MODE=legacy 로 강제 실행

topic 선택:
  현재는 model_answer_router.py가 사실상 topic router 역할 수행

향후 개선:
  topic_router.py를 별도 분리
```

즉, **완성된 topic의 기준 파일은 `rubrics/topic_packs/<topic_id>/`에 있고**, `rubrics/generated/`는 실행용 aggregate 산출물이다.

---

## 2. 디렉터리 역할

### 2.1 Topic Pack 원천 저장 위치

완성된 topic pack은 다음 위치에 저장한다.

```text
rubrics/topic_packs/<topic_id>/
```

예시:

```text
rubrics/topic_packs/second_order_lag_response_by_damping_ratio/
rubrics/topic_packs/second_order_system_resonance_frequency_response/
```

각 topic pack은 보통 다음 파일을 가진다.

```text
README.md
fact_anchor.json
model_answer.json
topic_importance.json
logic_check.json
topic_status.json       # changed-only/frozen workflow 도입 후
```

역할은 다음과 같다.

| 파일 | 역할 |
|---|---|
| `README.md` | topic pack 설명, 적용 범위, 검토 메모 |
| `fact_anchor.json` | 해당 topic의 fact 기준점, 핵심 키워드, 오개념 방지 기준 |
| `model_answer.json` | 채점 참조용 모범답안, routing alias, question example |
| `topic_importance.json` | 난이도, 시험 전략, 중요도 layer |
| `logic_check.json` | deterministic logic check 및 LLM logic profile |
| `topic_status.json` | topic의 draft/reviewed/approved/frozen 상태와 content hash |

---

### 2.2 Generated Bank 위치

generated bank는 topic pack 전체를 합쳐 만든 실행용 산출물이다.

```text
rubrics/generated/
```

대표 파일은 다음과 같다.

```text
fact_anchors.generated.json
model_answers.generated.json
topic_importance.generated.json
logic_checks.generated.json
logic_check_profiles.generated.json
topic_pack_manifest.generated.json
```

중요한 점은 다음과 같다.

```text
rubrics/topic_packs/:
  사람이 관리하는 source of truth

rubrics/generated/:
  runtime에서 읽기 쉽게 합친 build output
```

따라서 `rubrics/generated/*.json`이 변경되었다고 해서 개별 topic pack 원본이 수정된 것은 아니다.

---

### 2.3 Legacy Bank 위치

기존 legacy 방식은 다음 파일들을 사용한다.

```text
rubrics/fact_anchors/industrial_instrumentation_control.json
rubrics/model_answers/industrial_instrumentation_control.json
rubrics/topic_importance/industrial_instrumentation_control.json
rubrics/logic_checks/industrial_instrumentation_control.json
rubrics/logic_check_profiles/industrial_instrumentation_control.json
```

topic pack 전환 전에는 이 legacy bank가 기본 평가 기준이었다.

---

## 3. Legacy / Generated 평가 모드

### 3.1 모드 선택 원칙

평가 bank 경로는 `rubric_bank_paths.py`에서 결정한다.

```text
RUBRIC_BANK_MODE=generated
  → rubrics/generated/*.generated.json 사용

RUBRIC_BANK_MODE=legacy
  → 기존 industrial_instrumentation_control.json 사용
```

운영 정책은 다음처럼 가져간다.

```text
기본 평가:
  generated topic bank

기존 전체 범위 fallback:
  RUBRIC_BANK_MODE=legacy

topic pack 개발/검증:
  generated와 legacy를 smoke에서 비교
```

### 3.2 기본 generated 모드

generated를 기본값으로 바꾸면 일반 실행은 다음처럼 동작한다.

```bash
python3 bot.py
```

내부적으로 generated bank를 읽는다.

legacy로 강제하려면 다음처럼 실행한다.

```bash
RUBRIC_BANK_MODE=legacy python3 bot.py
```

### 3.3 Logic Check Profile 경로

`logic_llm_verifier.py`도 `resolve_rubric_bank_path("logic_check_profiles")`를 사용하도록 맞춘다.

기대 동작은 다음과 같다.

```text
RUBRIC_BANK_MODE=generated
  → rubrics/generated/logic_check_profiles.generated.json

RUBRIC_BANK_MODE=legacy
  → rubrics/logic_check_profiles/industrial_instrumentation_control.json

LOGIC_CHECK_PROFILE_PATH 지정
  → 지정 경로를 최우선 사용
```

---

## 4. 현재 Topic 선택 방식

### 4.1 현재 구조

현재는 독립된 `topic_router.py`가 없다.  
대신 `model_answer_router.py`의 `find_model_answer_reference()`가 사실상 topic routing 역할을 한다.

현재 흐름은 다음과 같다.

```text
문제 문장 / 답안
→ question_type_router로 문제 유형 추정
→ fact_eval에서 topic_id 후보 추출
→ model_answer_router가 model_answers bank 전체 scoring
→ 최고점 model_answer 선택
→ 선택된 model_answer의 topic_id를 최종 topic으로 사용
→ logic_check / difficulty_strategy가 해당 topic_id를 이어받음
```

즉, **현재 최종 topic은 model answer reference 선택 결과에 의해 결정된다.**

### 4.2 Scoring 기준

topic 후보 scoring에는 다음 요소가 반영된다.

```text
question_type 일치:
  높은 가중치

fact_eval에서 topic_id 일치:
  높은 가중치

question_examples 매칭:
  강한 routing signal

topic_aliases / aliases 매칭:
  topic 관련 키워드 signal

field_connection_points 매칭:
  현장 연결 키워드 signal

문제/답안 text 안에 topic_id 직접 포함:
  보조 signal
```

따라서 topic pack의 `model_answer.json`에서 다음 항목이 중요하다.

```text
question_examples
topic_aliases
field_connection_points
question_type
topic_id
```

### 4.3 현재 방식의 장점

```text
- 별도 router 없이 기존 model_answer 선택 흐름과 자연스럽게 결합됨
- question_type과 topic_id를 함께 고려함
- legacy/generated bank 모두 같은 방식으로 처리 가능
```

### 4.4 현재 방식의 한계

```text
- topic 선택 책임이 model_answer_router.py 안에 섞여 있음
- topic 후보 점수와 model_answer 선택 점수가 분리되어 있지 않음
- topic 수가 늘어나면 routing debug가 어려워질 수 있음
- topic만 먼저 고르고, 그 topic 안에서 model answer를 고르는 구조가 아님
```

따라서 다음 개선은 `topic_router.py` 분리다.

---

## 5. 향후 Topic Router 분리 방향

향후 구조는 다음처럼 나눈다.

```text
1. topic_router.py
   문제 문장 기준으로 topic_id 선택

2. question_type_router.py
   문제 유형 선택

3. model_answer_router.py
   topic_id + question_type 기준으로 model_answer 선택

4. logic_check_evaluator.py
   topic_id 기준으로 logic_check 선택

5. difficulty_strategy.py
   topic_id 기준으로 난이도/문항 선택 전략 적용
```

목표는 다음과 같다.

```text
문제 → topic 선택
문제 → question_type 선택
topic + question_type → model_answer 선택
topic → logic_check / difficulty / importance 적용
```

이렇게 분리하면 routing 검증과 debugging이 쉬워진다.

---

## 6. Topic Pack 작성 Workflow

### 6.1 신규 topic 생성

신규 topic은 scaffold 명령으로 생성한다.

```bash
python3 scripts/rubric_manager.py create-topic-pack \
  --topic-id <topic_id>
```

생성 후 다음 파일을 작성한다.

```text
README.md
fact_anchor.json
model_answer.json
topic_importance.json
logic_check.json
```

### 6.2 작성 중 검증

작성 중에는 전체 release validation을 반복하지 말고, 해당 topic만 검증한다.

```bash
python3 scripts/rubric_manager.py validate-topic-pack-quality \
  --topic-id <topic_id>
```

routing smoke도 해당 topic만 수행한다.

```bash
python3 scripts/rubric_manager.py smoke-topic-pack \
  --topic-id <topic_id>
```

Gemini 보조 검토도 해당 topic만 수행한다.

```bash
python3 scripts/rubric_manager.py review-topic-pack \
  --topic-id <topic_id>
```

### 6.3 전체 release 검증

release 직전에는 전체 검증을 수행한다.

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release
```

이 명령은 다음 항목을 검증한다.

```text
py_compile
generated pipeline
topic pack quality
topic pack smoke
synthetic session cleanup
smoke report cleanup
```

---

## 7. Frozen / Changed-only Workflow

### 7.1 문제의식

topic pack 수가 늘어나면 매번 전체 topic을 Gemini review하거나 generated 파일을 남기는 방식은 불편하다.

특히 다음 문제가 생긴다.

```text
- 완성된 topic까지 매번 검토 대상처럼 보임
- rubrics/generated/*.json이 매번 git diff에 남음
- 신규 topic만 검토하고 싶은데 전체 topic을 반복 확인하게 됨
```

이를 해결하기 위해 topic별 상태 파일을 둔다.

```text
rubrics/topic_packs/<topic_id>/topic_status.json
```

### 7.2 topic_status.json 예시

```json
{
  "topic_id": "second_order_system_resonance_frequency_response",
  "status": "frozen",
  "review_state": "reviewed",
  "content_hash": "sha256:...",
  "last_validated_at": "2026-07-04T12:00:00",
  "last_reviewed_at": "2026-07-04T12:10:00",
  "last_review_model": "gemini-2.5-flash",
  "last_review_report": "reports/topic_pack_gemini_review_second_order_system_resonance_frequency_response_20260704_121000.json",
  "approved_at": "2026-07-04T12:15:00",
  "frozen_at": "2026-07-04T12:15:00",
  "notes": []
}
```

### 7.3 status 의미

| status | 의미 |
|---|---|
| `draft` | 작성 중 |
| `reviewed` | Gemini 또는 사람 검토 완료 |
| `approved` | 사람 승인 완료 |
| `frozen` | 완성본으로 고정, 기본 changed-only 검토에서 제외 |

### 7.4 hash 의미

`content_hash`는 다음 파일들을 기준으로 계산한다.

```text
README.md
fact_anchor.json
model_answer.json
topic_importance.json
logic_check.json
```

이 파일 중 하나라도 바뀌면 해당 topic은 changed로 판단한다.

---

## 8. Topic Status 명령

### 8.1 전체 status 확인

```bash
python3 scripts/rubric_manager.py topic-pack-status --all --include-frozen
```

출력 예:

```text
topic_id	status	review_state	changed	last_validated_at	last_reviewed_at
second_order_lag_response_by_damping_ratio	frozen	not_reviewed	no	2026-07-04T12:00:00	
second_order_system_resonance_frequency_response	frozen	reviewed	no	2026-07-04T12:00:00	2026-07-04T12:10:00
```

### 8.2 topic을 frozen 처리

```bash
python3 scripts/rubric_manager.py topic-pack-status \
  --topic-id <topic_id> \
  --set-status frozen \
  --sync-hash \
  --mark-validated \
  --note "initial frozen topic pack"
```

### 8.3 review 완료 처리

```bash
python3 scripts/rubric_manager.py topic-pack-status \
  --topic-id <topic_id> \
  --set-status reviewed \
  --sync-hash \
  --mark-reviewed \
  --review-model gemini-2.5-flash \
  --review-report reports/<review_report>.json
```

---

## 9. Changed-only Review

### 9.1 변경된 topic만 Gemini review

```bash
python3 scripts/rubric_manager.py review-topic-pack-all --changed-only
```

동작 원칙:

```text
hash 동일 topic:
  skip

frozen + hash 동일 topic:
  skip

hash 변경 topic:
  review-topic-pack 실행
  성공 시 topic_status.json에 reviewed/hash 저장
```

### 9.2 frozen topic도 강제로 포함

```bash
python3 scripts/rubric_manager.py review-topic-pack-all \
  --changed-only \
  --include-frozen
```

### 9.3 실패해도 계속 진행

```bash
python3 scripts/rubric_manager.py review-topic-pack-all \
  --changed-only \
  --keep-going
```

---

## 10. Generated 파일 관리 정책

### 10.1 기본 정책

`rubrics/generated/*.json`은 build output이므로, 일반 검증 후 git diff에 남지 않는 것이 좋다.

권장 정책:

```text
validate-topic-pack-release 기본 실행:
  generated snapshot 저장
  generated pipeline 실행
  검증 완료 후 generated snapshot 복원

generated 실제 갱신:
  --promote-generated 옵션을 명시한 경우에만 worktree에 남김
```

### 10.2 일반 release validation

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release
```

기대 동작:

```text
generated output: restoring pre-validation snapshot
```

### 10.3 generated를 실제 반영

generated bank를 커밋하고 싶은 경우에만 다음처럼 실행한다.

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release \
  --promote-generated
```

이 경우 `rubrics/generated/*.json` 변경이 worktree에 남는다.

---

## 11. 검토 Report 위치

Gemini review 결과는 다음 위치에 저장한다.

```text
reports/topic_pack_gemini_review_<topic_id>_<timestamp>.json
reports/topic_pack_gemini_review_<topic_id>_<timestamp>.md
```

이 report는 보조 검토 자료다.

중요한 원칙:

```text
deterministic validator:
  release gate

Gemini review:
  사람 검토 보조
```

즉 Gemini review 결과가 `minor`, `major`, `blocker`를 말하더라도 최종 판단은 사람이 한다.  
다만 `blocker` 또는 명백한 fact 오류 지적은 반드시 확인한다.

---

## 12. 현재 완성된 Topic

현재 topic pack 기반으로 작성된 핵심 topic은 다음과 같다.

```text
second_order_lag_response_by_damping_ratio
second_order_system_resonance_frequency_response
```

각 topic은 다음 경로에 있다.

```text
rubrics/topic_packs/second_order_lag_response_by_damping_ratio/
rubrics/topic_packs/second_order_system_resonance_frequency_response/
```

이 topic들은 frozen workflow 도입 후 다음처럼 고정할 수 있다.

```bash
python3 scripts/rubric_manager.py topic-pack-status \
  --topic-id second_order_lag_response_by_damping_ratio \
  --set-status frozen \
  --sync-hash \
  --mark-validated \
  --note "initial frozen topic pack"

python3 scripts/rubric_manager.py topic-pack-status \
  --topic-id second_order_system_resonance_frequency_response \
  --set-status frozen \
  --sync-hash \
  --mark-validated \
  --mark-reviewed \
  --review-model gemini-2.5-flash \
  --note "initial frozen topic pack"
```

---

## 13. 권장 운영 루프

### 13.1 신규 topic 추가 루프

```text
1. create-topic-pack
2. fact_anchor/model_answer/topic_importance/logic_check 작성
3. validate-topic-pack-quality --topic-id
4. smoke-topic-pack --topic-id
5. review-topic-pack --topic-id
6. topic-pack-status --set-status reviewed 또는 frozen
7. validate-topic-pack-release
8. commit
```

### 13.2 여러 topic이 쌓인 후 운영 루프

```text
1. topic-pack-status --all --include-frozen
2. 변경 topic만 review-topic-pack-all --changed-only
3. validate-topic-pack-release
4. 필요할 때만 --promote-generated
5. commit
```

---

## 14. Commit 기준

### 14.1 topic pack 원본 변경 시

커밋 대상:

```text
rubrics/topic_packs/<topic_id>/*
```

필요 시:

```text
rubrics/generated/*.generated.json
```

단, generated는 정책적으로 promote할 때만 포함한다.

### 14.2 자동화 코드 변경 시

커밋 대상 예:

```text
scripts/rubric_manager.py
scripts/create_topic_pack.py
scripts/smoke_topic_pack.py
scripts/validate_topic_pack_quality.py
scripts/validate_topic_pack_release.py
scripts/topic_pack_status.py
scripts/review_topic_pack.py
scripts/review_topic_pack_all.py
scripts/topic_review_llm.py
rubric_bank_paths.py
logic_llm_verifier.py
```

### 14.3 review report

`reports/topic_pack_gemini_review_*.json`과 `.md`는 기본적으로 commit하지 않는다.

이유:

```text
- timestamp 산출물
- LLM 호출 결과
- review 보조 자료
- source of truth가 아님
```

필요하면 approved report만 별도 보존 정책을 둔다.

---

## 15. 현재 남은 개선 작업

### 15.1 topic_router.py 분리

가장 중요한 다음 개선이다.

목표:

```text
문제 문장에서 topic_id를 먼저 선택
model_answer_router는 선택된 topic 안에서만 answer reference 선택
logic_check/difficulty는 동일 topic_id를 사용
```

예상 파일:

```text
topic_router.py
scripts/smoke_topic_router.py
reports/topic_router_smoke.json
```

### 15.2 topic coverage 확장

다음 topic 후보:

```text
PID 제어기 P/I/D 동작과 튜닝
Routh-Hurwitz 안정판별
Bode 선도와 gain/phase margin
Nyquist 안정도
Control valve Cv
Positioner / I/P converter
SIS / SIL
계측기 정확도·정밀도·오차
```

### 15.3 generated promote 정책 정리

현재 목표:

```text
일반 validate:
  generated 복원

release/tag:
  --promote-generated로 generated 반영
```

이 정책을 README 또는 별도 운영 문서에 명시한다.

---

## 16. 요약

현재 topic pack 작업은 다음 상태다.

```text
완료:
  topic pack source 구조
  generated bank pipeline
  legacy/generated mode 분기
  logic_check_profiles generated 연동
  topic pack quality validation
  topic pack routing smoke
  Gemini review
  release validation
  frozen/changed-only workflow 설계 및 도입 예정

아직 개선 필요:
  topic_router.py 분리
  topic coverage 확장
  generated promote 정책 안정화
```

핵심 운영 원칙은 다음 한 줄이다.

```text
완성 topic은 rubrics/topic_packs/<topic_id>/에 보존하고,
generated는 실행용 산출물로만 다루며,
검토는 changed-only 기준으로 신규/수정 topic에 집중한다.
```
