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

## LQR 설계 적용조건

- 교차항이 없는 표준 연속시간 무한시간 LQR에서 Q=Q^T⪰0, R=R^T≻0, (A,B)가 stabilizable이고 (Q^(1/2),A)가 detectable이면 폐루프 A-BK를 Hurwitz로 만드는 고유한 양의 준정부호 안정화 해 P=P^T⪰0가 존재한다. 완전 가제어성과 완전 관측성은 더 강한 충분조건이다.
- (Q^(1/2),A)의 detectability는 비용함수에서 보이지 않는 불안정 모드를 배제하기 위한 CARE 조건이다. 실제 상태를 모두 측정하지 못해 관측기를 사용할 때에는 측정쌍 (C,A)의 detectability와 추정오차 동역학 A-LC의 안정성을 별도로 확인한다.
- 기본 LQR은 원점 조절기이다. 비영점 평형점을 추종하려면 실현 가능한 정상상태 (x_r,u_r)를 구하고 x-x_r, u-u_r의 오차좌표로 설계한다. 정적 프리필터는 명목 정상상태 추종을 보완하지만 모델 오차와 상수 외란에 대한 robust zero error를 보장하지 않는다. LQI는 적분상태를 포함한 확대시스템의 stabilizability를 확인하고 포화 시 windup을 검증해야 한다.
- 특정 상태의 Q 가중치를 상대적으로 높이면 그 상태편차 억제를 더 중시하는 최적해가 계산된다. 다만 Riccati 해와 폐루프 이득은 결합적으로 변하므로 모든 상태응답의 단조 개선을 보장하지 않는다. 제어입력, 포화, 측정·추정 잡음과 모델 불확실성에 대한 민감도는 별도로 검증한다.
- 이산시간 LQR은 이산화된 (A_d,B_d), 이산시간 비용 정의와 DARE를 사용한다. 표본시간과 연속 비용의 이산 등가화 방법에 따라 Q_d와 R_d가 달라질 수 있으므로 CARE 식을 그대로 적용하지 않는다.
- 답안이 J=∫(x^TQx+2x^TNu+u^TRu)dt의 교차항 N을 포함한 일반화 LQR을 명시하고 비용 블록행렬 조건, 일반화 Riccati 방정식과 이득식을 일관되게 사용하면 기본식과 다르다는 이유만으로 오류 처리하지 않는다.
- Fatal의 직접 점수 영향은 B/C에 한정한다. D/E 점수는 직접 변경하지 않고 관련 현장 적용·제언의 claim trust만 limited로 표시한다.

## Fact verification references

- MathWorks `lqr`
- MathWorks `icare`
- MathWorks `dlqr` and `idare`
- MathWorks `lqi`
- MathWorks `place`
- MIT Underactuated Robotics LQR notes
