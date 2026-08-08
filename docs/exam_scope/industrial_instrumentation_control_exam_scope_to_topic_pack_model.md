# 산업계측제어기술사 출제범위와 Topic Pack 연결 모델

## 1. 목적

이 문서는 한국산업인력공단이 제시하는 산업계측제어기술사 출제범위를 저장소의 Topic Sheet와 Topic Pack으로 어떻게 연결하는지 정의한다.

Topic Pack은 예상 문제 문장을 저장하는 문제은행이 아니다. Topic Pack은 공식 출제범위를 실제 채점에 사용할 수 있는 **재사용 가능한 지식 단위**로 구조화한 것이다.

따라서 다음 두 문장을 구분한다.

- **공식 출제범위를 Topic Pack inventory가 coverage한다.**
- **미래에 출제될 모든 문제 문장이 특정 Topic Pack 하나와 1:1로 일치한다.**

첫 번째는 이 저장소가 관리하는 coverage 목표이고, 두 번째는 보장하지 않는다.

## 2. 문서 계층과 책임

출제범위와 Topic Pack은 다음 계층으로 연결한다.

```text
한국산업인력공단 공식 출제기준
        ↓
Exam Scope / Criterion
        ↓
Classification / Coverage
PRIMARY / SECONDARY
COVERED / PARTIAL / GAP
        ↓
Topic Sheet
positive ownership / negative boundary
        ↓ 동일 topic_id, 1:1
Topic Pack
fact / logic / model answer / importance
        ↓
Generated Rubric Bank
        ↓
Runtime Grading
```

각 계층의 책임은 다음과 같다.

| 계층 | 저장 위치 | 책임 |
|---|---|---|
| 공식 출제기준 정규화·분석 | `docs/exam_scope/` | 산업인력공단 출제범위를 저장소가 추적할 수 있는 criterion과 coverage 단위로 정리 |
| Topic classification | `docs/topic_pack_classification.md` | criterion과 Topic의 PRIMARY/SECONDARY ownership 관계를 관리 |
| Topic Sheet | `docs/topic_sheets/<topic_id>.md` | 하나의 Topic이 실제로 소유하는 의미 범위와 인접 Topic 경계를 정의 |
| Topic Pack | `rubrics/topic_packs/<topic_id>/` | Topic Sheet의 의미 범위를 machine-readable grading source로 구현 |
| Generated bank | `rubrics/generated/*.generated.json` | 검증된 Topic Pack을 runtime용 bank로 통합 |

## 3. Criterion과 Topic은 1:1 관계가 아니다

산업인력공단의 한 출제 criterion은 여러 Topic의 지식을 함께 요구할 수 있다. 반대로 하나의 Topic이 여러 criterion을 지원할 수도 있다.

따라서 다음 관계를 허용한다.

```text
Official Criterion ↔ Topic
= 1:N 또는 N:M 가능
```

예를 들어 하나의 비교·선정 문제는 센서별 원리 Topic과 측정오차 Topic을 동시에 요구할 수 있다. 이 경우 Topic을 억지로 하나로 합치지 않고 ownership을 구분한다.

- **PRIMARY**: 해당 criterion의 핵심 내용을 직접 책임지는 Topic
- **SECONDARY**: 핵심 설명을 보조하지만 criterion 전체를 소유하지 않는 Topic

PRIMARY/SECONDARY는 Topic Pack의 점수 가중치를 자동으로 의미하지 않는다. 이는 **공식 범위와 Topic 간의 ownership 관계**를 표현한다.

## 4. Coverage의 의미

공식 criterion마다 현재 Topic inventory의 coverage 상태를 관리한다.

- **COVERED**: 필요한 핵심 지식이 기존 Topic으로 충분히 설명 가능
- **PARTIAL**: 관련 Topic은 있으나 공식 범위의 일부가 충분히 소유되지 않음
- **GAP**: 해당 criterion을 책임질 Topic coverage가 없음

Coverage는 Topic Pack 숫자를 늘리기 위한 지표가 아니다. 신규 Topic은 실제 의미 경계가 독립적일 때만 추가한다.

다음 순서를 따른다.

```text
공식 criterion
    ↓
기존 Topic ownership 확인
    ↓
COVERED / PARTIAL / GAP
    ↓
기존 Topic 확장 또는 신규 Topic 필요성 판단
    ↓
Topic Sheet 작성
    ↓
Topic Pack 구현
```

단순히 키워드가 다르거나 문제 표현이 새롭다는 이유만으로 신규 Topic을 만들지 않는다.

## 5. Topic Sheet와 Topic Pack은 1:1 관계

Criterion과 Topic은 N:M 관계가 가능하지만 Topic Sheet와 Topic Pack은 다르다.

```text
docs/topic_sheets/<topic_id>.md
              ↕
rubrics/topic_packs/<topic_id>/
```

동일한 `<topic_id>`를 사용하며 1:1로 대응한다.

Topic Sheet에서 다음을 먼저 확정한다.

- positive ownership: 이 Topic이 반드시 설명해야 하는 범위
- negative boundary: 인접 Topic에 속하며 현재 Topic이 소유하지 않는 범위
- core facts
- fatal wrong claims
- 대표 문제와 routing 표현
- 인접 Topic ownership 경계

Topic Pack은 이 범위를 다시 정의하지 않는다. Topic Sheet의 동일한 의미 경계를 다음 네 grading 역할로 구현한다.

| 파일 | 역할 |
|---|---|
| `fact_anchor.json` | 정확한 사실·원리·수식·조건 |
| `logic_check.json` | 논리 오류, fatal wrong claim, 인접 Topic contamination |
| `model_answer.json` | 고득점 답안의 내용과 구조 |
| `topic_importance.json` | 중요도와 시험 전략 정보 |

## 6. Topic Pack coverage와 실제 시험문제 routing은 다른 문제

공식 출제범위를 Topic Pack이 coverage하더라도 실제 시험문제가 항상 Topic Pack 하나와 일치하는 것은 아니다.

실제 문제는 다음 세 형태를 가질 수 있다.

1. 기존 Topic 하나의 범위를 직접 묻는 문제
2. 여러 Topic을 조합한 복합 문제
3. 공식 범위 안에 있지만 현재 Topic evidence로 충분히 설명되지 않는 새로운 문제

따라서 runtime은 Topic Pack을 문제은행처럼 사용하지 않는다.

```text
실제 시험문제
    ↓
Topic Router
    ├─ SINGLE_TOPIC
    ├─ MULTI_TOPIC
    ├─ GENERAL
    └─ AMBIGUOUS
```

- `SINGLE_TOPIC`: 하나의 Topic evidence로 충분히 설명 가능
- `MULTI_TOPIC`: 둘 이상의 Topic을 실제 문제 요구사항이 함께 요구
- `GENERAL`: 문제는 명확하지만 현재 Topic evidence가 충분하지 않음
- `AMBIGUOUS`: 문제 자체가 모호하여 Topic ownership을 안정적으로 결정하기 어려움

`GENERAL`은 채점 실패를 의미하지 않는다. Topic-specific evidence가 부족한 부분을 일반 채점 기준으로 평가하기 위한 fallback이다.

## 7. 실제 기출이 기존 Topic으로 충분히 설명되지 않을 때

실제 기출이 `GENERAL` 또는 낮은 Topic evidence coverage로 판정되면 곧바로 신규 Topic을 생성하지 않는다.

다음 순서로 재검토한다.

```text
실제 기출
    ↓
기존 Topic alias / Router 문제인가?
    ├─ Yes → Router 또는 Topic Sheet routing 표현 개선
    └─ No
        ↓
기존 Topic의 의미 범위가 실제로 부족한가?
    ├─ 기존 Topic 확장 가능 → source repair/extension
    └─ 독립 지식 경계 필요
        ↓
공식 criterion coverage 재평가
        ↓
PARTIAL / GAP이면 신규 Topic 후보
```

즉 실제 기출은 Topic taxonomy를 개선하는 feedback이지만, 신규 Topic 생성의 자동 트리거는 아니다.

## 8. 운영 원칙

1. 공식 출제범위가 Topic inventory보다 상위 개념이다.
2. Topic Pack은 문제은행이 아니라 채점 가능한 지식 단위다.
3. Criterion↔Topic은 N:M이 가능하며 PRIMARY/SECONDARY로 ownership을 관리한다.
4. Topic Sheet↔Topic Pack은 동일 `topic_id`의 1:1 관계다.
5. Topic Sheet에서 positive ownership과 negative boundary를 먼저 확정한다.
6. 실제 문제의 표현이 새롭다는 이유만으로 신규 Topic을 만들지 않는다.
7. 여러 Topic을 실제로 요구하면 `MULTI_TOPIC`으로 처리한다.
8. Topic evidence가 부족하면 억지 매칭하지 않고 `GENERAL` 경로를 사용한다.
9. 반복되는 GENERAL/uncovered demand는 coverage 개선 후보로 기록한다.
10. “공식 범위 coverage”와 “미래 문제 문장 100% 예측”을 동일시하지 않는다.
