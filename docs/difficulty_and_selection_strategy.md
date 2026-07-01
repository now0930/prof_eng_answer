# Difficulty and Selection Strategy

Difficulty Profile은 A/B/C/D/E 점수를 대체하지 않는다. 이 문서는 문항 난이도, 고득점 가능성, ceiling 후보, 문항 선택 전략을 설명한다.

## 1. 위치

```text
A/B/C/D/E 25점 구조 = 기본 점수 체계
Question Type v2 = C/D 항목 보완 lens
Difficulty Profile = 고득점 가능성·선택 전략·ceiling lens
Fact Anchor = 핵심 fact 기준
Model Answer Bank = 대표 답안 구조와 패턴
```

Difficulty Profile은 다음을 하지 않는다.

- A/B/C/D/E 점수를 직접 대체하지 않음
- Question Type을 대체하지 않음
- 어려운 문제 선택 자체에 가산점을 주지 않음
- 쉬운 문제라는 이유만으로 자동 감점하지 않음

## 2. Profile 종류

| Profile | 의미 | 기본 ceiling |
|---|---|---:|
| `BASIC_CONCEPT` | 정의, 개념, 구성 중심 | 15.0 |
| `FIELD_APPLICATION` | 현장 적용, 선정, 개선방안 중심 | 15.75 |
| `DESIGN_EVALUATION` | 설계, 평가, 효과 분석 중심 | 16.5 |
| `THEORY_CORE` | 제어이론, 2차 시스템, 안정도 등 핵심 이론 | 17.5 |

기본 ceiling은 고득점 가능성 해석 기준이다. 실제 점수 제한 여부는 `DIFFICULTY_CEILING_MODE`에 따른다.

## 3. Ceiling mode

| 모드 | 의미 |
|---|---|
| `warn` | ceiling 후보만 계산하고 점수는 변경하지 않음 |
| `strict` | recommended cap이 현재 점수보다 낮으면 실제 제한 |
| `off` | difficulty ceiling 계산/출력 비활성 |

운영 환경이 `strict`이면 Telegram 출력에서 다음을 구분해야 한다.

- ceiling 적용 전 단순 평균
- ceiling 적용 전 가중 점수
- difficulty ceiling 적용 후 최종 점수
- cap 사유

## 4. BASIC_CONCEPT

정의, 개념, 구성, 기본 기능 설명 중심 문제다.

대표 신호:

- 정의하시오
- 개념을 설명하시오
- 구성요소를 설명하시오
- 특징을 설명하시오

채점 특징:

- 기본 개념을 정확히 쓰면 안정 점수 확보 가능
- 정의 수준에 머물면 고득점 어려움
- 현장 적용, 한계, 실무 의미를 연결해야 합격권 접근

## 5. FIELD_APPLICATION

현장 적용, 선정, 개선방안, 유지보수, 운전 리스크가 중요한 문제다.

대표 신호:

- 적용 방안을 설명하시오
- 개선방안을 설명하시오
- 선정 기준을 설명하시오
- 현장 적용 시 고려사항
- 교정 절차를 설명하시오

채점 특징:

- 정의나 원리만으로 부족
- 기존 설비 영향, 적용 조건, 비용, 유지보수성, 검증 기준 필요
- D항목 현장 판단 비중이 커짐

## 6. DESIGN_EVALUATION

설계안, 시스템 구성, 성능 평가, 효과 분석이 중요한 문제다.

대표 신호:

- 설계하시오
- 평가하시오
- 효과를 분석하시오
- 시스템 구성을 설명하시오
- 적용 결과를 평가하시오

채점 특징:

- 설계 근거와 평가 지표 필요
- 대안 비교, 적용 조건, 성능 지표, 비용·효과 분석 필요
- 결론에서 어떤 설계안이 적합한지 판단해야 함

## 7. THEORY_CORE

제어이론, 동특성, 안정도, 전달함수, 상태방정식, 2차 시스템 등 이론 핵심 문제다.

대표 신호:

- 전달함수를 구하시오
- 안정도를 판별하시오
- 감쇠비를 설명하시오
- 2차 시스템 응답특성을 설명하시오
- 상태방정식을 설명하시오
- 주파수 응답을 설명하시오

채점 특징:

- 정확히 쓰면 고득점 가능
- 수식, 변수, 조건, 해석을 틀리면 큰 감점 위험
- 선택 자체 가산점 없음
- 정확한 표준 모델·변수·응답특성·현장 해석이 연결되어야 high band unlock

## 8. THEORY_CORE high band unlock

`THEORY_CORE`는 고위험·고보상형이다. 고득점 band를 열려면 다음이 필요하다.

- 표준 모델 또는 특성방정식
- 핵심 변수 정의
- 수식 관계
- 조건별 해석
- 응답특성
- 안정성 또는 물리적 의미
- 현장 tuning 또는 제어 loop 영향

fatal error 예:

- 감쇠비 구간별 응답특성 반대 설명
- 안정과 불안정 반대 판단
- 극점 위치와 응답특성의 잘못된 연결
- 전달함수 또는 특성방정식 핵심 관계 오류
- 오버슈트, 감쇠, 진동성 관계 반대 설명

`strict` 모드에서는 fatal error가 감지되면 10점 cap 후보가 실제 적용될 수 있다.

## 9. 2차 시스템 예시

2차 시스템 감쇠비 문제에서 다음 오류는 fatal candidate다.

- `ζ = sin^-1(ωd/ωn)`처럼 잘못된 관계식 사용
- `0 < ζ < 1` 부족감쇠를 단순 발산으로 설명
- 무감쇠, 부족감쇠, 임계감쇠, 과감쇠, 불안정 조건을 구분하지 않음

보완 방향:

- `s² + 2ζωn s + ωn² = 0` 기준으로 설명
- `ωd = ωn√(1-ζ²)` 관계 명시
- 감쇠비별 상승시간, 피크시간, 오버슈트율, 정착시간 비교
- PID tuning, hunting, servo, 압력/유량/온도 control loop와 연결

## 10. 문항 선택 전략

| 선택 상황 | 전략 |
|---|---|
| 쉬운 개념 문제만 선택 | 안정적이나 고득점 ceiling 낮음 |
| 현장 적용 문제 선택 | 실무 경험으로 합격권 접근 가능 |
| 설계·평가 문제 선택 | 구조화하면 중상위 점수 가능 |
| 제어이론 문제 선택 | 정확하면 고득점, 오류 시 위험 |

제어이론 문제는 다음 조건을 만족할 때 선택하는 것이 좋다.

- 수식과 변수 의미를 빠르게 쓸 수 있음
- 조건별 해석을 정확히 설명 가능
- 결과를 현장 tuning 또는 제어성으로 연결 가능
- 부분점수 방어 구조를 알고 있음

## 11. 답안 길이와 volume cap

짧은 답안은 Difficulty와 별개로 volume cap이 적용될 수 있다.

대표 조건:

- 답안 이미지 없이 텍스트가 매우 짧음
- A/B/C/D/E 구조가 거의 없음
- fact는 일부 있으나 현장 판단 없음
- 25점 문항 평균 전개량에 미달

이 경우 점수가 낮은 이유는 Difficulty가 높아서가 아니라, 기술사 답안으로 필요한 전개량이 부족하기 때문이다.

## 12. 관련 파일

| 파일 | 역할 |
|---|---|
| `rubrics/difficulty_profiles/default.json` | Profile 정의와 기본 ceiling |
| `difficulty_strategy.py` | 문제 난이도 분류 |
| `difficulty_output_adapter.py` | grade에 difficulty 설명 attach |
| `difficulty_score_ceiling.py` | recommended cap 계산 및 strict 적용 |
| `grading_agents.py` | phase2 pipeline에서 difficulty 결합 |
| `bot.py` | Telegram 출력에서 ceiling 전/후 점수 표시 |
