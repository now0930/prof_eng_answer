# 상태피드백 기준입력 추종·프리필터·적분보상 설계

## Topic ID

`state_feedback_reference_tracking_prefilter_integral_action`

## 분류

- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: `LLM_ONLY`
- 결정론적 검사: 비활성화

## 대표 문제

상태피드백 제어에서 기준입력 추종과 정상상태 오차 보상을 위한
프리필터와 적분상태 확대설계를 설명하고 실제 구현 시 고려사항을
논하시오.

## 기본 상태피드백

    x_dot = A x + B u
    y     = C x
    u     = -K x + N_r r

폐루프 상태방정식은 다음과 같다.

    x_dot = (A-BK)x + B N_r r

## 정상상태 프리필터

SISO, `D=0`, 안정한 `A-BK`와 가역한 DC 이득에서 다음 식을 사용한다.

    N_r = -[C(A-BK)^(-1)B]^(-1)

프리필터는 기준입력 feedforward 보상이며 모델오차와 외란 제거를
일반적으로 보장하지 않는다.

## 적분상태 확대설계

    ξ_dot = r - y
    u     = -K_x x + K_i ξ

`D=0`일 때 기본 확대행렬은 다음과 같다.

    A_a = [ A   0 ]
          [-C   0 ]

    B_a = [ B ]
          [ 0 ]

확대시스템의 가제어성 또는 안정화 가능성과 원점 불변영점을
반드시 확인한다.

## Source 구성

- `fact_anchor.json`: 14개 핵심 사실과 8개 Fatal 오개념
- `logic_check.json`: LLM truth schema와 fatal condition
- `model_answer.json`: 8개 권장 답안 구조
- `topic_importance.json`: 8개 고득점 해제조건
- `README.md`: Topic Pack 안내

## 핵심 채점 원칙

- 극점 배치와 정상상태 추종을 구분한다.
- 프리필터 공식은 적용조건과 부호 규약을 함께 평가한다.
- 적분 확대시스템의 가제어성·안정화 가능성을 확인한다.
- 단순 공식 누락은 즉시 Fatal로 처리하지 않는다.
- 포화, windup, 관측기 노이즈와 이산 구현을 포함해 검증한다.
