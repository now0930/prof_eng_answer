# LQR 최적 상태피드백·Riccati 방정식·가중치 설계

## Topic ID

`lqr_optimal_state_feedback_riccati_weighting_design`

## 분류

- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: `LLM_ONLY`
- 결정론적 검사: 비활성화

## 대표 문제

LQR 최적 상태피드백 제어기의 비용함수, Riccati 방정식, 가중치
선정방법과 실제 구현 시 고려사항을 설명하시오.

## 연속시간 비용함수

    J = integral_0^infinity (x^T Q x + u^T R u) dt

기본 가중행렬 조건은 다음과 같다.

    Q = Q^T >= 0
    R = R^T > 0

## CARE와 최적 상태피드백

    A^T P + P A - P B R^(-1) B^T P + Q = 0

    K = R^(-1) B^T P
    u = -K x
    A_cl = A - B K

제어에는 폐루프를 안정하게 만드는 stabilizing solution `P`를
사용한다.

## 해의 존재조건

- `(A,B)`의 stabilizability
- `(Q^(1/2),A)`의 detectability
- `Q>=0`
- `R>0`

완전 가제어성은 충분조건이지만 항상 필요한 최소조건은 아니다.

## 가중치 설계

- 큰 상태 가중치는 해당 상태편차 억제를 강화할 수 있다.
- 큰 입력 가중치는 제어입력을 줄이고 응답을 완만하게 할 수 있다.
- `Q`와 `R`을 동일한 양의 배율로 변경하면 기본 무한시간 LQR의
  `K`는 변하지 않는다.
- Bryson's rule은 허용범위를 이용한 초기 가중치 선정 경험칙이다.

## 추종과 제약조건

기본 LQR은 원점 조절기다. 기준입력 추종에는 프리필터 또는 LQI를
사용할 수 있다.

`u^TRu`는 입력 사용에 비용을 부과하지만 hard saturation을 직접
보장하지 않는다.

## 연속·이산 구분

- 연속시간 LQR: CARE
- 이산시간 LQR: DARE
- 이산 폐루프 안정성: `A_d-B_dK_d`의 고유값이 단위원 내부

## Source 구성

- `fact_anchor.json`: 14개 핵심 사실과 8개 Fatal 오개념
- `logic_check.json`: LLM truth schema와 fatal condition
- `model_answer.json`: 8개 권장 답안 구조
- `topic_importance.json`: 8개 고득점 해제조건
- `README.md`: Topic Pack 안내

## 핵심 채점 원칙

- 비용함수와 최적성의 범위를 구분한다.
- CARE의 안정화 해와 존재조건을 평가한다.
- Q와 R 튜닝을 단조로운 성능 향상으로 설명하지 않는다.
- LQR과 극점 배치 및 LQI를 구분한다.
- 입력 penalty와 hard constraint를 구분한다.
- CARE와 DARE를 구분한다.
- 포화, 관측기, 불확실성과 수치조건을 포함해 검증한다.
