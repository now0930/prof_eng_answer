# 난이도와 문항 선택 전략

이 문서는 문제 난이도, 점수 ceiling, 문항 선택 전략을 설명한다.

기존 A/B/C/D/E 25점 채점 구조는 유지한다.  
난이도는 점수 체계를 대체하지 않고, 채점 엄격도와 고득점 가능성 판단에 사용한다.

---

## 1. 기본 원칙

| 구분 | 의미 |
|---|---|
| Answer Difficulty | 선택한 문제 자체의 난이도와 채점 엄격도 |
| Selection Importance | 시험에서 반드시 준비해야 할 핵심 주제인지 여부 |
| Score Ceiling | 쉬운 문제의 고득점 상한 |
| Band Unlock | 어려운 문제에서 고득점 band가 열리는 조건 |

핵심 원칙:

```text
쉬운 문제 = 안정 점수형, ceiling 낮음
제어이론 문제 = 고위험·고보상형
제어이론 선택 자체 = 가산점 없음
제어이론 정확 풀이 = 고득점 band unlock
제어이론 회피 = 개별 감점이 아니라 선택 전략 risk
```

---

## 2. 난이도 Profile

| Profile | 의미 | 기본 ceiling |
|---|---|---:|
| `BASIC_CONCEPT` | 정의, 개념, 구성 중심 | 19 |
| `FIELD_APPLICATION` | 현장 적용, 선정, 개선방안 중심 | 21 |
| `DESIGN_EVALUATION` | 설계, 평가, 효과 분석 중심 | 22 |
| `THEORY_CORE` | 제어이론, 2차 시스템, 안정도 등 핵심 이론 | 25 |

---

## 3. Ceiling Mode

기본값은 `warn`이다.

```env
DIFFICULTY_CEILING_MODE=warn
```

`warn` 모드는 cap 후보만 계산하고 실제 점수는 바꾸지 않는다.

실제 점수를 제한하려면 `strict`를 사용한다.

```env
DIFFICULTY_CEILING_MODE=strict
```

`strict` 모드에서는 다음을 적용한다.

| Profile | 적용 |
|---|---|
| `BASIC_CONCEPT` | 19점 초과 시 19점 cap |
| `FIELD_APPLICATION` | 21점 초과 시 21점 cap |
| `DESIGN_EVALUATION` | 22점 초과 시 22점 cap |
| `THEORY_CORE` | unlock 부족 시 20점 cap 후보 |
| `THEORY_CORE` fatal error | 더 강한 cap 후보 |

---

## 4. THEORY_CORE

`THEORY_CORE`는 제어이론, feedback system, 2차 시스템, 안정도, 과도응답 같은 핵심 이론 문제이다.

이 문제는 선택 자체로 가산점을 주지 않는다.  
정확히 풀었을 때만 21~25점 고득점 band가 열린다.

고득점 unlock 조건:

- 표준 모델 또는 특성방정식
- 핵심 변수 정의
- 수식 관계
- 조건별 해석
- 응답특성
- 안정성 또는 물리 의미
- 현장 tuning 또는 제어 loop 영향

예: 2차 시스템

- 감쇠비 ζ
- 고유진동수 ωn
- 극점 위치
- ζ < 1, ζ = 1, ζ > 1 구분
- overshoot, settling time, rise time
- 현장 loop 안정성 판단

---

## 5. Selection Importance

| Importance | 의미 |
|---|---|
| `CORE_MUST_PREPARE` | 반복 출제되는 핵심 변별 주제. 반드시 준비해야 함 |
| `HIGH_PRIORITY` | 선택 우선순위가 높은 주제 |
| `NORMAL` | 일반 선택 가능 주제 |
| `OPTIONAL` | 안전하지만 고득점 ceiling이 낮을 수 있는 주제 |

제어이론, feedback system, 2차 시스템, 안정도, 과도응답 계열은 `CORE_MUST_PREPARE`로 관리한다.

---

## 6. 문항 선택 전략

기술사 시험은 여러 문제 중 일부를 선택해 답안을 작성한다.  
따라서 개별 답안 점수와 문항 선택 전략은 분리한다.

| 상황 | 판단 |
|---|---|
| 쉬운 문제 4개로 평균 통과 | 가능하지만 고득점 ceiling 낮음 |
| 제어이론 선택 후 낮은 점수 | 선택 방향은 타당할 수 있으나 실행력 부족 |
| 제어이론 회피 | 직접 감점이 아니라 selection risk |
| 제어이론 정확 풀이 | 고득점 band unlock |

---

## 7. 관련 파일

| 파일 | 역할 |
|---|---|
| `difficulty_strategy.py` | 난이도와 선택 중요도 분류 |
| `difficulty_output_adapter.py` | phase20 난이도 설명 출력 |
| `difficulty_score_ceiling.py` | phase21 ceiling 계산 및 strict 적용 |
| `rubrics/difficulty_profiles/default.json` | 난이도 Profile |
| `rubrics/topic_importance/industrial_instrumentation_control.json` | topic별 난이도와 선택 중요도 |
| `rubrics/exam_selection/default.json` | 시험 문항 선택 전략 기준 |
