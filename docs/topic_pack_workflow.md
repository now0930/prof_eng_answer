# Topic Pack Workflow

이 문서는 `prof_eng_answer`에서 새 topic을 추가하거나 기존 topic을 보강할 때의 표준 workflow를 정의한다.

핵심 목적은 다음과 같다.

1. topic별 채점 기준을 사람이 검토 가능한 단위로 관리한다.
2. README, Topic Sheet, JSON source, generated bank의 역할을 분리한다.
3. LLM을 사용하더라도 기존 JSON schema를 깨지 않도록 schema lock을 유지한다.
4. Fact Anchor와 Logic Check의 경계를 명확히 한다.
5. 표, 다이어그램, ASCII 그림, 수식 전개를 claim 중심으로 평가한다.

---

## 1. 전체 흐름

새 topic은 아래 순서로 추가한다.

```text
1. Topic Pack source 생성
2. Topic Pack README 작성
3. README → Topic Sheet 후보 생성
4. 사람이 Topic Sheet 검토
5. Topic Sheet → schema-locked JSON candidate 생성
6. 사람이 JSON diff 검토
7. Topic Pack quality 검증
8. generated bank promote
9. smoke / Telegram 재채점 확인
10. commit
```

중요 원칙:

```text
README → JSON 직행 금지
Topic Sheet 검토 단계 유지
generated bank 직접 수정 금지
source JSON과 generated JSON의 역할 분리
```

---

## 2. 파일 구조

Topic Pack source:

```text
rubrics/topic_packs/<topic_id>/
  README.md
  fact_anchor.json
  logic_check.json
  model_answer.json
  topic_importance.json
  topic_status.json
```

Topic Sheet:

```text
docs/topic_sheets/<topic_id>.md
```

Generated bank:

```text
rubrics/generated/fact_anchors.generated.json
rubrics/generated/model_answers.generated.json
rubrics/generated/topic_importance.generated.json
rubrics/generated/logic_checks.generated.json
rubrics/generated/logic_check_profiles.generated.json
rubrics/generated/topic_pack_manifest.generated.json
```

역할:

| 파일 | 역할 |
|---|---|
| `README.md` | 사람이 topic 의도, 정답 기준, 검토 메모를 남기는 설명서 |
| `docs/topic_sheets/<topic_id>.md` | JSON 생성을 위한 구조화된 Markdown input |
| `fact_anchor.json` | 핵심 fact coverage source |
| `logic_check.json` | fatal/warn 이론 오류 source |
| `model_answer.json` | 고득점 답안 구조 source |
| `topic_importance.json` | 난이도, 중요도, high-band unlock 조건 source |
| `topic_status.json` | topic hash와 상태 관리 |
| `rubrics/generated/*.json` | runtime용 build output |

---

## 3. Topic ID 원칙

`topic_id`는 다음 기준으로 정한다.

- 영어 소문자와 underscore 사용
- 문제의 핵심 개념과 출제 축을 함께 표현
- 너무 넓은 이름 금지
- 기존 topic과 겹치지 않게 작성
- resonance, damping, PID 등 인접 topic과 routing alias 충돌 주의

예:

```text
좋음:
second_order_lag_response_by_damping_ratio
second_order_system_resonance_frequency_response

나쁨:
second_order_system
control_theory
damping
```

넓은 topic id는 model answer routing, fact anchor matching, logic check 적용 범위를 흐리게 만든다.

---

## 4. Topic Pack 생성

새 topic pack skeleton을 생성한다.

```bash
cd ~/hermes/workspace/prof_eng_answer

python3 scripts/rubric_manager.py create-topic-pack \
  --topic-id <topic_id>
```

생성 후 확인:

```bash
find rubrics/topic_packs/<topic_id> -maxdepth 1 -type f | sort
```

---

## 5. Topic Pack README 작성

`rubrics/topic_packs/<topic_id>/README.md`는 사람이 읽기 위한 검토 문서다.

이 README는 runtime source가 아니다. 하지만 나중에 Topic Sheet를 만들 때 좋은 입력이 된다.

권장 구조:

```markdown
# <topic title> Topic Pack

## 목적

## 대표 문제

## 핵심 정답 기준

## 정답으로 인정할 표현

## 핵심 fatal 오류

## warn 수준의 부족한 표현

## false positive 주의사항

## 표와 다이어그램 처리 메모

## 현장 적용 판단 기준

## 검토 메모
```

README에는 자연어 설명을 쓴다. JSON schema를 설명하려고 하지 않는다.

---

## 6. README에서 Topic Sheet 후보 생성

README를 바탕으로 Topic Sheet 후보를 생성한다.

```bash
python3 scripts/generate_topic_sheet_from_readme.py \
  --topic-id <topic_id> \
  --model gemini-2.5-flash \
  --overwrite
```

출력:

```text
docs/topic_sheets/<topic_id>.md
```

프롬프트만 확인하려면:

```bash
python3 scripts/generate_topic_sheet_from_readme.py \
  --topic-id <topic_id> \
  --print-prompt
```

주의:

- 이 단계는 JSON을 만들지 않는다.
- 생성된 Topic Sheet는 후보일 뿐이다.
- 사람이 반드시 검토한다.

---

## 7. Topic Sheet 검토

Topic Sheet는 JSON 생성을 위한 구조화된 입력이다.

필수 섹션:

```text
1. Topic metadata
2. Core correct facts
3. Acceptable answer expressions
4. Fatal wrong claims
5. Warn-level weak claims
6. False positive cautions
7. Regex candidate patterns
8. fact_anchor.json generation guidance
9. logic_check.json generation guidance
10. model_answer.json generation guidance
11. topic_importance.json generation guidance
12. Human review checklist
```

검토 기준:

- 대표 문제가 정확한가?
- topic_id가 문서에 포함되어 있는가?
- 정답 fact가 atomic statement로 나뉘어 있는가?
- fatal 오류와 단순 누락이 구분되어 있는가?
- false positive caution이 충분한가?
- regex 후보가 너무 넓지 않은가?
- 표/다이어그램을 claim 중심으로 해석하도록 되어 있는가?
- Fact Anchor와 Logic Check의 경계가 분명한가?

---

## 8. Topic Sheet에서 JSON candidate 생성

사람이 검토한 Topic Sheet에서 topic pack source JSON candidate를 생성한다.

```bash
python3 scripts/generate_topic_pack_from_sheet.py \
  --topic-id <topic_id> \
  --sheet docs/topic_sheets/<topic_id>.md \
  --model gemini-2.5-flash
```

기본 출력은 `.candidate.json`이다.

```text
rubrics/topic_packs/<topic_id>/fact_anchor.candidate.json
rubrics/topic_packs/<topic_id>/logic_check.candidate.json
rubrics/topic_packs/<topic_id>/model_answer.candidate.json
rubrics/topic_packs/<topic_id>/topic_importance.candidate.json
```

source JSON을 직접 갱신하려면 `--overwrite`를 사용한다.

```bash
python3 scripts/generate_topic_pack_from_sheet.py \
  --topic-id <topic_id> \
  --sheet docs/topic_sheets/<topic_id>.md \
  --model gemini-2.5-flash \
  --overwrite
```

권장 운영은 다음과 같다.

```text
초안 생성:
  candidate 생성

사람 검토:
  diff 확인

반영:
  필요 시 --overwrite 또는 수동 반영
```

---

## 9. Schema Lock 원칙

`generate_topic_pack_from_sheet.py`는 기존 source JSON을 schema template으로 사용한다.

원칙:

- 새 schema를 만들지 않는다.
- 기존 top-level key를 유지한다.
- 기존 nested key를 유지한다.
- 기존 list item shape를 유지한다.
- 기존 schema에 없는 pseudo field를 만들지 않는다.
- logic_check에 `"condition"` 같은 pseudo-code 필드를 만들지 않는다.
- LLM이 필드를 누락하면 기존 값을 복구한다.
- LLM이 schema를 줄이면 post-process merge로 되돌린다.

특히 Logic Check에서 금지되는 형태:

```json
{
  "condition": "ζ == 1 && pole_type == '중근'"
}
```

이 형태가 위험한 이유:

- runtime schema와 맞지 않는다.
- `ζ=1 → 중근`은 정답인데 fatal로 잡을 수 있다.
- wrong pattern, safe condition, verifier profile 경계가 무너진다.

---

## 10. Fact Anchor 작성 기준

Fact Anchor는 “정답 요소를 언급했는가”를 본다.

Fact Anchor에 넣을 것:

- 정의
- 핵심 수식
- 조건
- 분류 기준
- 원리
- 비교축
- 현장 적용과 연결되는 핵심 fact
- 표/다이어그램에서 올바르게 읽히는 claim

Fact Anchor에 넣지 말 것:

- 오답 regex
- fatal cap 정책
- 감점 문구
- LLM verifier 판단 조건
- safe condition
- 오답 예시 중심의 rule

예:

```text
Fact Anchor:
  ζ=1은 임계감쇠이며 중근을 갖는다.
  ζ>1은 과감쇠이며 서로 다른 두 실근을 갖는다.
  안정한 부족감쇠 극점은 s=-ζωn±jωd이다.

Logic Check:
  ζ=1을 overdamped로 분류하면 fatal.
  overdamped를 중근으로 설명하면 fatal.
  s=+ζωn±jωd를 안정 극점식으로 쓰면 fatal.
```

---

## 11. Logic Check 작성 기준

Logic Check는 “정답과 충돌하는가”를 본다.

Logic Check에 넣을 것:

- fatal wrong claim
- major/warn weak claim
- wrong_patterns
- safe condition
- false positive caution
- affected layer
- recommended ceiling
- D/E claim trust metadata
- LLM verifier focus

Logic Check에 넣지 말 것:

- 단순 누락을 fatal 처리하는 rule
- 좋은 답안에도 나올 수 있는 contrastive statement를 잡는 broad regex
- 표 위치만 보고 판단하는 rule
- schema에 없는 pseudo field

fatal로 볼 수 있는 경우:

- topic의 핵심 이론을 반대로 설명
- 수식의 안정성 부호가 반대
- 분류 mapping이 정답과 충돌
- 안전/위험 조건을 반대로 설명
- 현장 판단의 전제가 되는 이론이 깨짐

warn/major로 둘 경우:

- 핵심 항목 누락
- 비교축 부족
- 현장 적용 부족
- 용어가 모호하지만 정답과 직접 충돌하지 않음
- ASCII 그림은 있으나 설명이 부족함

---

## 12. 표와 다이어그램 처리 기준

표, 다이어그램, ASCII 그림, s-plane 그림, block diagram, 수식 전개는 그 자체가 정답 또는 오답이 아니다. 평가 대상은 거기서 읽히는 claim이다.

### 12.1 Fact Anchor에서의 처리

Fact Anchor는 표와 다이어그램에서 올바른 claim을 evidence로 인정한다.

예:

| 답안 표현 | Fact Anchor 처리 |
|---|---|
| 표에서 `0<ζ<1 → underdamped → overshoot 있음` | 부족감쇠 응답 특성 evidence |
| s-plane 그림에서 좌반평면 복소켤레근과 감쇠진동을 설명 | 극점-응답 관계 evidence |
| block diagram에서 feedback과 dead time을 보조로 설명 | 보조 현장 적용 evidence |
| 수식으로 `ωd=ωn√(1-ζ²)` 제시 | 부족감쇠 감쇠진동수 evidence |

단, 표가 있어도 의미 claim이 틀리면 Fact Anchor coverage만으로 고득점 처리하면 안 된다.

### 12.2 Logic Check에서의 처리

Logic Check는 표와 다이어그램의 claim이 정답과 충돌할 때 적용한다.

예:

| 답안 표현 | Logic Check 처리 |
|---|---|
| 표에서 `ζ=1 → over damped` | fatal 후보 |
| 표에서 `overdamped → 중근` | fatal 후보 |
| 수식에서 `s=+ζωn±jωd`를 안정 극점식으로 제시 | fatal 후보 |
| s-plane 설명에서 `RHP stable`이라고 설명 | fatal 후보 |
| 그림만 있고 설명이 불명확함 | fatal 아님, warn 또는 coverage 부족 |

### 12.3 ASCII 그림 주의

ASCII 그림은 파싱이 불안정할 수 있으므로 다음 원칙을 따른다.

- 그림 위치만으로 fatal 처리하지 않는다.
- 그림 주변의 라벨, 표 셀, 본문 설명을 함께 본다.
- claim이 명시되지 않으면 fatal로 단정하지 않는다.
- 사람이 읽으면 명확한 오답이라도 regex가 놓칠 수 있으므로 LLM verifier profile에 candidate evidence 추출 지침을 둔다.

### 12.4 표 cell mapping 주의

표는 셀 간 정렬이 깨질 수 있다. 따라서 다음을 함께 확인한다.

- 같은 행의 header와 값
- 바로 위/아래 행의 라벨
- 본문 bullet의 재진술
- 표 뒤의 결론 문장

예를 들어 아래와 같은 답안은 fatal로 볼 수 있다.

```text
ζ=1 인 경우는 → over damped
overdamped => 중근
```

반면 아래 문장은 fatal이 아니다.

```text
ζ=1은 over damped가 아니라 critical damping이다.
```

---

## 13. False Positive 방지 기준

Logic Check에는 false positive 방지 기준이 반드시 필요하다.

예:

| 표현 | 처리 |
|---|---|
| `ζ=1은 over damped가 아니라 critical damping이다` | 정답 설명 |
| `σ=ζωn`을 감쇠율 크기로 정의하고 최종 극점식을 `s=-σ±jωd`로 제시 | 허용 가능 |
| `ζ≈0.707`을 실무 절충값으로 설명 | 허용 가능 |
| `ζ≈0.707`을 임계감쇠 정의로 설명 | 오류 |
| `ζ=sinθ`를 허수축 기준 각도로 정의 | 허용 가능 |
| `ζ=sinθ`를 음의 실수축 기준 각도로 정의 | 오류 후보 |

---

## 14. generated bank promote

source JSON을 수정한 뒤에는 generated bank를 갱신한다.

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated
```

이 명령은 다음을 수행한다.

1. Python compile
2. topic pack validation
3. generated bank build
4. generated bank validation
5. topic pack quality validation
6. smoke-topic-pack
7. generated output promote

변경되는 파일:

```text
rubrics/generated/fact_anchors.generated.json
rubrics/generated/model_answers.generated.json
rubrics/generated/topic_importance.generated.json
rubrics/generated/logic_checks.generated.json
rubrics/generated/logic_check_profiles.generated.json
rubrics/generated/topic_pack_manifest.generated.json
```

---

## 15. smoke와 Telegram 검증

Topic Pack smoke:

```bash
python3 scripts/rubric_manager.py smoke-topic-pack --topic-id <topic_id>
```

legacy/generated 비교:

```bash
python3 scripts/smoke_compare_rubric_bank_modes.py <session_path>
```

Telegram 재채점에서 확인할 것:

- topic이 맞게 routing되는가?
- Logic Check가 적용되는가?
- fatal 오류가 있으면 `mode=fatal, fatal=True`가 나오는가?
- recommended cap이 의도한 값으로 적용되는가?
- 최종 Bot 출력이 사용자에게 이해 가능하게 나오나?

예:

```text
phase3b logic check applied: topic=<topic_id>, mode=fatal, fatal=True
phase21 final difficulty ceiling evaluated: recommended_cap=10.0, capped_score=10.0
```

---

## 16. commit 전 확인

```bash
git status --short
git diff --stat
git diff --check
```

Python 검증:

```bash
python3 -m py_compile \
  scripts/generate_topic_sheet_from_readme.py \
  scripts/generate_topic_pack_from_sheet.py \
  scripts/rubric_manager.py \
  scripts/topic_review_llm.py
```

Topic Pack 검증:

```bash
python3 scripts/rubric_manager.py validate-topic-pack-quality
python3 scripts/rubric_manager.py validate-topic-pack-release
```

커밋 대상에 포함할 수 있는 것:

```text
rubrics/topic_packs/<topic_id>/*.json
rubrics/topic_packs/<topic_id>/README.md
docs/topic_sheets/<topic_id>.md
rubrics/generated/*.generated.json
scripts/generate_topic_sheet_from_readme.py
scripts/generate_topic_pack_from_sheet.py
scripts/rubric_manager.py
docs/*.md
README.md
scripts/README.md
```

커밋 제외:

```text
reports/topic_pack_generation_*.json
reports/topic_sheet_generation_*.json
__pycache__/
patch_*.py
*.candidate.json
임시 실험 파일
```

---

## 17. 권장 commit 분리

Rubric 동작 수정과 authoring 도구 추가는 분리한다.

예:

```bash
git commit -m "fix(rubrics): cap fatal damping-ratio logic errors"
git commit -m "feat(rubrics): add README-to-topic-sheet authoring flow"
git commit -m "docs: update topic pack authoring workflow"
```

문서만 수정한 경우:

```bash
git commit -m "docs: update topic pack authoring workflow"
```
