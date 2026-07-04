# Rubric Authoring Guide

이 문서는 `prof_eng_answer`에서 Model Answer, Fact Anchor, Topic Importance, Logic Check를 작성할 때의 공통 기준을 정의한다.

현재 운영 기준은 Topic Pack source를 중심으로 한다.

```text
rubrics/topic_packs/<topic_id>/
  README.md
  fact_anchor.json
  logic_check.json
  model_answer.json
  topic_importance.json
  topic_status.json
```

`rubrics/generated/*.generated.json`은 runtime에서 읽기 쉽게 합친 build output이다. 직접 수정하지 않는다.

---

## 1. 작성 원칙

Rubric은 가능한 JSON source로 관리하고, Python 코드는 routing, parsing, validation, score postprocess에 집중한다.

역할 구분:

| 구분 | 역할 |
|---|---|
| Model Answer | 고득점 답안의 구조와 서술 방향 |
| Fact Anchor | 정답 요소 coverage |
| Topic Importance | topic 난이도, 출제 중요도, high-band unlock 조건 |
| Logic Check | 정답과 충돌하는 핵심 이론 오류 |
| Logic Check Profile | LLM verifier가 evidence를 추출하고 truth schema와 비교하는 기준 |
| Difficulty Ceiling | 난이도와 fatal 오류에 따른 최종 score cap |

---

## 2. Topic Pack 작성 순서

새 topic은 다음 순서로 작성한다.

```text
README.md
  → Topic Sheet
  → fact_anchor.json
  → model_answer.json
  → topic_importance.json
  → logic_check.json
  → generated promote
```

명령:

```bash
python3 scripts/rubric_manager.py create-topic-pack --topic-id <topic_id>

python3 scripts/generate_topic_sheet_from_readme.py \
  --topic-id <topic_id> \
  --model gemini-2.5-flash \
  --overwrite

python3 scripts/generate_topic_pack_from_sheet.py \
  --topic-id <topic_id> \
  --sheet docs/topic_sheets/<topic_id>.md \
  --model gemini-2.5-flash

python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated
```

README와 Topic Sheet는 authoring input이고, JSON source가 runtime 기준이다. generated bank는 build output이다.

---

## 3. Model Answer 작성 기준

Model Answer는 모범 답안 문장을 외우게 하는 파일이 아니다. 답안 구조, 전개 깊이, 고득점 특징, 현장 적용 방향을 정의한다.

포함할 것:

- representative question
- topic aliases
- expected structure
- model answer outline
- high score features
- common missing points
- low score patterns
- field connection points
- question type과의 관계

넓게 쓰되 topic routing이 흔들릴 정도로 alias를 과도하게 넣지 않는다.

예:

```text
좋음:
- 2차 지연시스템 감쇠비별 응답특성
- damping ratio response
- ζ별 과도응답
- 부족감쇠 / 임계감쇠 / 과감쇠 비교

주의:
- 2차 시스템 전체
- resonance 전체
- PID 전체
```

Model Answer는 정답 문장 매칭용이 아니라 채점자가 무엇을 고득점 답안으로 볼지 정리하는 기준이다.

---

## 4. Fact Anchor 작성 기준

Fact Anchor는 “무엇을 썼는가”를 본다.

### 4.1 넣을 것

- 핵심 정의
- 핵심 수식
- 조건
- 분류 기준
- 원리
- 인과관계
- 비교축
- 현장 적용을 지탱하는 fact
- 표와 다이어그램에서 올바르게 읽히는 claim

예:

```text
ζ=1은 임계감쇠이며 중근을 갖는다.
ζ>1은 과감쇠이며 서로 다른 두 실근을 갖는다.
0<ζ<1은 부족감쇠이며 좌반평면 복소켤레근, 감쇠진동, 오버슈트 가능 특성을 갖는다.
안정한 부족감쇠 극점은 s=-ζωn±jωd이다.
```

### 4.2 넣지 말 것

- 오답 regex
- fatal cap 정책
- 감점 문구
- LLM verifier 전용 condition
- safe condition
- false positive exception 중심의 rule
- 좋은 답안과 나쁜 답안을 구분하는 logic 자체

Fact Anchor는 coverage 기준이다. 정답과 충돌하는지 여부는 Logic Check가 담당한다.

---

## 5. Logic Check 작성 기준

Logic Check는 “맞게 썼는가”를 본다. 단순 누락이나 표현 부족을 잡는 기능이 아니다.

### 5.1 넣을 것

- 정답 기준과 직접 충돌하는 fatal wrong claim
- 중요한 이론 오류 또는 분류 오류
- 안정성, 부호, 조건, 방향, 원인-결과 반전
- wrong_patterns
- safe condition
- false positive caution
- recommended ceiling
- affected layers
- D/E claim trust metadata
- LLM verifier focus

### 5.2 넣지 말 것

- 단순 누락을 fatal 처리하는 rule
- 표현이 애매한데 정답과 직접 충돌하지 않는 rule
- 좋은 답안에도 등장하는 contrastive expression을 잡는 broad regex
- 표의 위치만 보고 판단하는 rule
- schema에 없는 pseudo field

금지 예:

```json
{
  "condition": "ζ == 1 && pole_type == '중근'"
}
```

이유:

- runtime schema와 맞지 않는다.
- `ζ=1 → 중근`은 정답이다.
- pseudo-code field는 validator와 runtime이 해석하지 못한다.

---

## 6. Fact Anchor와 Logic Check의 경계

| 상황 | Fact Anchor | Logic Check |
|---|---|---|
| 핵심 개념을 올바르게 언급 | coverage 인정 | pass |
| 핵심 개념을 누락 | coverage 부족 | 보통 fatal 아님 |
| 핵심 개념을 반대로 설명 | coverage로만 인정하면 안 됨 | fatal 또는 major |
| 수식은 썼지만 부호가 반대 | 수식 언급 자체는 evidence일 수 있음 | fatal 후보 |
| 표를 작성했지만 mapping이 틀림 | 표 형식 자체는 가점 아님 | wrong claim으로 평가 |
| 다이어그램이 있으나 설명이 불명확 | 제한적 evidence | warn 또는 확인 필요 |
| 좋은 답안의 반박 표현 | coverage 가능 | safe condition으로 보호 |

핵심 문장:

```text
Fact Anchor는 정답 요소의 존재를 본다.
Logic Check는 그 정답 요소가 정답과 충돌하는지 본다.
```

---

## 7. 표 처리 기준

표는 답안 구조를 명확하게 만들 수 있으므로 고득점 요소가 될 수 있다. 그러나 표 자체가 정답은 아니다.

### 7.1 Fact Anchor에서 표 처리

Fact Anchor는 표에서 올바른 claim을 추출한다.

예:

| 표 내용 | Fact Anchor 인정 |
|---|---|
| `0<ζ<1 → 부족감쇠 → 복소켤레근 → overshoot` | 부족감쇠 특성 |
| `ζ=1 → 임계감쇠 → 중근` | 임계감쇠 특성 |
| `ζ>1 → 과감쇠 → 서로 다른 두 실근` | 과감쇠 특성 |
| `오버슈트, 상승시간, 정착시간 비교` | 비교축 제시 |

### 7.2 Logic Check에서 표 처리

표 안의 mapping이 정답과 충돌하면 Logic Check 대상이다.

예:

| 표 내용 | 처리 |
|---|---|
| `ζ=1 → over damped` | fatal |
| `overdamped → 중근` | fatal |
| `0<ζ<1 → unstable` | fatal 후보 |
| `ζ=0 → 점근 안정` | fatal 후보 |
| 비교축이 하나만 있음 | warn 또는 coverage 부족 |

### 7.3 표 parsing 주의

Markdown 표, ASCII 표, box drawing 표는 파싱 중 셀 경계가 깨질 수 있다.

따라서 다음을 함께 본다.

- header
- 같은 열의 값
- 같은 행의 라벨
- 표 아래 bullet 설명
- 본문에서 반복되는 claim
- 주변 수식

표의 셀 위치만으로 fatal 처리하지 않는다.

---

## 8. 다이어그램 처리 기준

다이어그램은 다음 형태를 포함한다.

- ASCII s-plane
- pole-zero plot
- block diagram
- signal flow diagram
- response curve sketch
- table-like diagram
- 수식 전개와 그림이 결합된 설명

### 8.1 Fact Anchor에서 다이어그램 처리

다이어그램이 올바른 claim을 전달하면 evidence로 인정한다.

예:

| 다이어그램 claim | Fact Anchor 인정 |
|---|---|
| 좌반평면 복소켤레근 | 안정한 부족감쇠 극점 |
| 허수축 순허수근 | 무감쇠 지속진동 |
| 우반평면 극점 | 불안정 |
| response curve에서 overshoot와 settling 표시 | 응답특성 비교 |
| block diagram에서 dead time을 보조 요소로 설명 | 현장 적용 보조 설명 |

### 8.2 Logic Check에서 다이어그램 처리

다이어그램의 claim이 정답과 충돌하면 Logic Check 대상이다.

예:

| 다이어그램 claim | 처리 |
|---|---|
| RHP pole을 stable이라고 설명 | fatal |
| LHP pole을 unstable이라고 설명 | fatal |
| 안정 극점 실수부를 `+ζωn`으로 표시 | fatal |
| `ζ=1` 위치를 overdamped로 표시 | fatal |
| 그림만 있고 라벨이 모호함 | fatal 아님 |

### 8.3 그림만으로 fatal 처리하지 않는 이유

ASCII 그림은 다음 문제가 있다.

- 정렬이 깨질 수 있다.
- OCR/텍스트 변환에서 라벨이 섞일 수 있다.
- 그림의 축 기준이 본문 설명과 다를 수 있다.
- θ 기준축에 따라 `sinθ`와 `cosθ` 해석이 달라질 수 있다.

따라서 Logic Check는 그림의 위치가 아니라 **그림에서 명시된 claim**을 평가한다.

---

## 9. 수식 처리 기준

수식은 Fact Anchor와 Logic Check 모두에서 중요하다.

### 9.1 Fact Anchor에서 수식 처리

올바른 수식은 fact evidence다.

예:

```text
s² + 2ζωn s + ωn² = 0
s = -ζωn ± jωd
ωd = ωn√(1-ζ²)
```

### 9.2 Logic Check에서 수식 처리

수식이 정답과 충돌하면 fatal 후보다.

예:

```text
s = +ζωn ± jωd
s = ζωn ± jωd
```

단, 다음 경우는 허용 가능하다.

```text
σ = ζωn을 양의 감쇠율 크기로 정의하고,
최종 극점식을 s = -σ ± jωd로 쓴 경우
```

따라서 Logic Check는 중간 변수 정의와 최종 극점식을 함께 봐야 한다.

---

## 10. False Positive 방지 기준

Logic Check는 오탐을 피해야 한다.

대표 safe case:

| 표현 | 처리 |
|---|---|
| `ζ=1은 overdamped가 아니라 critical damping이다` | 정답 |
| `임계감쇠는 중근이다` | 정답 |
| `과감쇠는 서로 다른 두 실근이다` | 정답 |
| `σ=ζωn`을 감쇠율 크기로 정의하고 `s=-σ±jωd`로 마무리 | 허용 가능 |
| `ζ≈0.707`을 실무 절충값으로 설명 | 허용 가능 |
| `ζ≈0.707`을 임계감쇠 정의로 설명 | 오류 |
| θ를 허수축 기준으로 두고 `ζ=sinθ` | 허용 가능 |
| θ를 음의 실수축 기준으로 두고 `ζ=sinθ` | 오류 후보 |

Regex를 만들 때는 “not overdamped”, “아니라”, “not”, “except”, “구분해야 한다” 같은 contrastive statement를 오탐하지 않도록 주의한다.

---

## 11. Topic Importance 작성 기준

Topic Importance는 점수를 직접 주는 파일이 아니다. 난이도, 선택 전략, high-band unlock 조건, fatal cap 정책에 필요한 metadata를 제공한다.

포함할 것:

- difficulty
- selection importance
- target score 또는 high band 기준
- high-band unlock conditions
- omission risk
- fatal error risk
- score ceiling policy
- 실전 선택 전략

THEORY_CORE topic은 다음 기준을 포함한다.

- 핵심 모델 또는 방정식 제시
- 핵심 조건과 분류 기준 제시
- 극점/근/안정성 해석
- 응답특성 비교
- 현장 적용 trade-off
- fatal logic error 없음

---

## 12. Topic Pack README 작성 기준

Topic Pack README는 사람이 topic을 검토하기 위한 문서다.

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

README는 간결해도 된다. 그러나 다음은 반드시 구분한다.

```text
정답 기준
오답 기준
false positive 주의사항
표/다이어그램 처리 기준
```

---

## 13. Topic Sheet 작성 기준

Topic Sheet는 JSON 생성을 위한 구조화된 Markdown input이다.

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

README보다 더 구조화되어야 하며, 특히 fatal/warn/false positive/regex 후보가 분리되어야 한다.

---

## 14. Generated Bank 작성 금지

`rubrics/generated/*.generated.json`은 직접 수정하지 않는다.

수정 흐름:

```text
topic pack source JSON 수정
  → validate-topic-pack-release --promote-generated
  → generated bank 갱신
```

명령:

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated
```

---

## 15. 검토 체크리스트

JSON을 promote하기 전에 확인한다.

- topic_id가 정확한가?
- Model Answer alias가 너무 넓지 않은가?
- Fact Anchor가 정답 coverage 중심인가?
- Logic Check가 단순 누락을 fatal로 잡지 않는가?
- Logic Check가 정답과 충돌하는 오류만 fatal로 잡는가?
- false positive caution이 충분한가?
- 표/다이어그램에서 claim을 추출하는 기준이 명확한가?
- generated bank를 직접 수정하지 않았는가?
- smoke test에서 primary topic이 기대 topic으로 잡히는가?
- Telegram 재채점에서 fatal cap이 의도대로 적용되는가?

---

## 16. 검증 명령

```bash
python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_manager.py validate-topic-pack-quality
python3 scripts/rubric_manager.py validate-topic-pack-release
python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated
python3 scripts/rubric_manager.py smoke-topic-pack --topic-id <topic_id>
git diff --check
```
