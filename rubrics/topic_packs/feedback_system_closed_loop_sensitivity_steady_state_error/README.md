# 피드백 시스템의 폐루프 구조·민감도·정상상태 오차

## Topic ID

`feedback_system_closed_loop_sensitivity_steady_state_error`

## Question Type

`PRINCIPLE_INTERPRETATION`

## Difficulty and importance

- Difficulty: `THEORY_CORE`
- Selection importance: `CORE_MUST_PREPARE`
- Rubric source status: reviewed
- Generated bank status: not promoted

## 범위

이 Topic Pack은 다음 내용을 하나의 피드백 제어 기본 주제로 평가한다.

1. 표준 음의 피드백 구조
2. 폐루프 전달함수와 특성방정식
3. 민감도 함수 `S`와 상보 민감도 함수 `T`
4. 추종, 출력 외란과 측정 잡음의 전달경로
5. 최종값 정리와 정상상태 오차
6. 시스템 형과 정적 오차상수
7. 루프 이득·대역폭·안정여유의 상충관계
8. 현장 적용 제약과 검증 방법

## 기본 가정과 핵심식

표준 음의 피드백은 다음 부호를 기준으로 한다.

    E(s) = R(s) - H(s)Y(s)
    L(s) = G(s)H(s)
    Y(s)/R(s) = G(s) / [1 + G(s)H(s)]
    1 + L(s) = 0

민감도 함수는 다음과 같다.

    S(s) = 1 / [1 + L(s)]
    T(s) = L(s) / [1 + L(s)]
    S(s) + T(s) = 1

단위 피드백에서는 기준입력에 대한 출력 전달함수를 `T`로 표현할 수 있다.

정상상태 오차는 폐루프가 최종값 정리의 적용 조건을 만족할 때 다음과 같이 계산한다.

    e_ss = lim[s→0] sE(s)

## 시스템 형과 정상상태 오차

시스템 형은 단위 피드백 개루프 `L(s)`에 포함된 원점 극, 즉 순수 적분기의 수이다.

    Kp_e = lim[s→0] L(s)
    Kv   = lim[s→0] sL(s)
    Ka   = lim[s→0] s²L(s)

안정한 단위 피드백과 단위 입력 기준의 대표 관계는 다음과 같다.

| System Type | Step | Ramp | Parabolic |
|---|---:|---:|---:|
| Type 0 | `1/(1+Kp_e)` | `∞` | `∞` |
| Type 1 | `0` | `1/Kv` | `∞` |
| Type 2 | `0` | `0` | `1/Ka` |

## 민감도 해석

- 낮은 주파수에서 `|L|`가 크면 `|S|`가 작아져 추종 오차, 출력 외란과 모델 변화의 영향이 감소할 수 있다.
- 단위 피드백의 표준 위치에서 측정 잡음의 출력 전달은 `-T`이므로 높은 이득만으로 모든 잡음을 제거할 수 없다.
- `S+T=1`이므로 모든 주파수에서 `S`와 `T`를 동시에 임의로 작게 만들 수 없다.
- 시간지연, 비최소위상 영점과 미모델 고주파 동특성은 가능한 대역폭을 제한한다.

## 기술사 답안 권장 전개

1. 피드백의 목적과 표준 블록 구조
2. 폐루프 전달함수와 특성방정식 유도
3. `S`, `T`, `S+T=1`과 물리적 의미
4. 외란·잡음 전달경로
5. 최종값 정리와 시스템 형
6. 입력별 정상상태 오차
7. 성능과 안정성의 상충관계
8. 현장 제약과 검증 방법
9. 결론

## Fatal 오개념

다음 주장은 핵심 이론 오류 후보이다.

- 표준 음의 피드백의 분모가 `1-GH`라는 주장
- `S`와 `T`가 동일하다는 주장
- 루프 이득이 클수록 항상 안정하다는 주장
- 시스템 형을 폐루프 차수나 전체 극 수로 정의하는 주장
- Type 0의 단위 계단 정상상태 오차가 항상 0이라는 주장
- 높은 루프 이득이 측정 잡음을 모든 주파수에서 완전히 제거한다는 주장
- 불안정한 폐루프에도 최종값 정리를 무조건 적용할 수 있다는 주장
- 피드백이 모든 외란을 위치와 주파수에 관계없이 완전히 제거한다는 주장

합산점 부호 관례를 명확히 선언하고 일관되게 유도한 경우에는 기호 차이만으로 fatal 처리하지 않는다.

## 현장 적용 고려사항

- 공정 및 통신 시간지연
- 센서 정확도, 잡음과 필터
- 샘플링 주기와 계산 지연
- 액추에이터 포화와 속도 제한
- 적분 windup과 anti-windup
- set-point prefilter와 feedforward
- Bode/Nyquist 안정여유
- step, disturbance, noise와 saturation test
- 기존 설비 변경 비용과 유지보수성

## Routing phrases

- 피드백 시스템
- 음의 피드백
- 폐루프 전달함수
- 민감도 함수
- 상보 민감도
- 정상상태 오차
- 시스템 형
- 정적 오차상수
- disturbance rejection
- measurement noise
- feedback sensitivity
- steady-state error

## 완료 상태

- [x] Fact Anchor 작성
- [x] Model Answer 구조 작성
- [x] Routing alias와 field point 작성
- [x] Topic Importance 확정
- [x] Logic fatal·major·safe condition 작성
- [x] 표준 부호 관례와 false-positive caution 작성
- [ ] generated bank build 및 promote
- [ ] routing·difficulty·logic smoke
- [ ] 실제 Telegram 재채점

## Source validation

    python3 scripts/rubric_manager.py validate-topic-packs
