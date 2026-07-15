# LQR 최적 상태피드백·Riccati 방정식·가중치 설계

## 1. Topic 기본정보

- Topic ID: `lqr_optimal_state_feedback_riccati_weighting_design`
- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: `LLM_ONLY`
- 결정론적 검사: 비활성화
- 작성 기준일: 2026-07-11

## 2. 출제 범위

연속시간 선형시불변 시스템에서 무한시간 LQR 최적 상태피드백
제어기를 설계하는 원리와 절차를 다룬다.

비용함수, 상태 및 제어입력 가중치, 연속시간 대수 Riccati 방정식,
최적 상태피드백 이득, 안정화 해의 존재조건과 폐루프 특성을
설명한다.

가중치 선정, 상태와 입력의 단위 정규화, Bryson's rule, 극점 배치와
LQR의 차이, 기준입력 추종을 위한 프리필터와 LQI, 액추에이터 포화,
이산시간 LQR, 관측기와 실제 구현 검증까지 포함한다.

## 3. 기본 가정과 기호

기본 연속시간 상태공간 모델은 다음과 같다.

    x_dot = A x + B u

기본 무한시간 비용함수는 교차항이 없는 다음 형태를 사용한다.

    J = integral_0^infinity (x^T Q x + u^T R u) dt

최적 상태피드백은 다음과 같이 정의한다.

    u = -K x

- `x`: 상태벡터
- `u`: 제어입력
- `Q`: 상태편차 가중행렬
- `R`: 제어입력 가중행렬
- `P`: Riccati 방정식의 안정화 해
- `K`: 최적 상태피드백 이득
- `A-BK`: LQR 폐루프 행렬
- `J`: 무한시간 이차 비용함수

특별한 언급이 없으면 `(A,B)`는 안정화 가능하고,
`(Q^(1/2),A)`는 검출 가능하며, `Q`는 대칭 양의 준정부호,
`R`은 대칭 양의 정부호라고 가정한다.

## 4. Fact Anchor 요구사항

### A01 — `state_lqr_design_objective_cost`

LQR은 상태편차와 제어입력 사용량의 상충관계를 이차 비용함수로
정의하고, 이를 최소화하는 상태피드백 이득을 구하는 최적제어
방법이다.

기본 비용함수는 다음과 같다.

    J = integral_0^infinity (x^T Q x + u^T R u) dt

필수 내용:

- 상태편차 감소와 제어에너지 또는 제어부담을 함께 평가한다.
- LQR의 optimal은 선택한 모델과 비용함수에 대한 최적임을 뜻한다.
- 실제 성능은 `Q`, `R`, 모델 정확도와 구현 제약에 의존한다.
- 물리적으로 모든 성능지표를 자동 최적화하는 것은 아니다.

### A02 — `state_lqr_weight_matrix_conditions`

기본 연속시간 LQR에서 가중행렬은 일반적으로 다음 조건을 만족한다.

    Q = Q^T >= 0
    R = R^T > 0

필수 내용:

- `Q`는 상태편차의 비용을 정의한다.
- `R`은 제어입력 비용을 정의한다.
- `R>0`은 비용함수의 입력항과 `R^(-1)`을 정상적으로 정의한다.
- 비대칭 행렬은 대칭 부분이 이차형식에 기여하므로 통상 대칭행렬을
  사용한다.
- 교차항 `2x^TNu`를 포함하는 일반형은 별도 조건과 일반화된 Riccati
  식이 필요하다.

### A03 — `state_lqr_care_stabilizing_solution`

교차항이 없는 연속시간 무한시간 LQR의 대수 Riccati 방정식은 다음과
같다.

    A^T P + P A - P B R^(-1) B^T P + Q = 0

필수 내용:

- 단순한 대수해가 아니라 폐루프를 안정하게 만드는 stabilizing
  solution을 선택한다.
- 조건이 만족되면 관련 안정화 해 `P`는 대칭 양의 준정부호가 된다.
- Riccati 방정식의 여러 수학적 해와 제어에 필요한 안정화 해를
  구분한다.
- 수치해의 residual과 폐루프 안정성을 함께 확인한다.

### A04 — `state_lqr_optimal_gain_closed_loop`

안정화 Riccati 해 `P`를 이용하면 최적 상태피드백 이득은 다음과
같다.

    K = R^(-1) B^T P
    u = -K x

폐루프 행렬은 다음과 같다.

    A_cl = A - B K

필수 내용:

- 최적 입력의 부호 규약을 일관되게 사용한다.
- `K`는 `Q`, `R`, `A`, `B`에 의해 결정된다.
- 폐루프 극점은 `A-BK`의 고유값이다.
- 비용함수 최소화 결과와 폐루프 안정성 검증을 연결한다.

### A05 — `state_lqr_existence_stabilizability_detectability`

무한시간 연속 LQR의 유한하고 안정화한 해를 보장하기 위해서는
통상 다음 조건을 확인한다.

- `(A,B)`의 stabilizability
- `(Q^(1/2),A)`의 detectability
- `Q>=0`
- `R>0`

필수 내용:

- 완전한 가제어성은 충분조건이지만 항상 필요한 최소조건은 아니다.
- 가제어하지 않은 모드가 이미 안정하면 stabilizability가 성립할 수
  있다.
- 비용함수에서 관찰되지 않는 불안정 모드는 detectability 조건을
  위반한다.
- 조건을 확인하지 않고 Riccati 해의 존재와 안정성을 단정하지 않는다.

### A06 — `state_lqr_q_weight_state_tradeoff`

`Q`의 특정 상태 가중치를 상대적으로 증가시키면 해당 상태편차를
더 강하게 억제하려는 설계가 된다.

필수 내용:

- 상태응답이 빨라지거나 상태편차가 감소할 수 있다.
- 일반적으로 제어입력 증가, 포화, 노이즈 민감도와 강인성 저하가
  발생할 수 있다.
- 하나의 `Q` 원소 증가가 모든 상태와 모든 성능을 단조롭게 개선한다고
  단정하지 않는다.
- 상태 결합과 비대각 `Q`의 의미를 고려한다.

### A07 — `state_lqr_r_weight_control_tradeoff`

`R`을 상대적으로 증가시키면 제어입력 사용을 더 강하게 제한하고,
`R`을 상대적으로 감소시키면 더 큰 제어입력을 허용하는 방향으로
설계된다.

필수 내용:

- 큰 `R`은 일반적으로 응답을 완만하게 하고 제어입력을 줄인다.
- 작은 `R`은 빠른 응답을 유도할 수 있지만 큰 입력, 포화와 미모델
  고주파 동특성 문제를 유발할 수 있다.
- `R`을 0 또는 특이행렬로 임의 설정하지 않는다.
- 실제 액추에이터 용량과 입력 단위를 반영한다.

### A08 — `state_lqr_common_scaling_invariance`

기본 무한시간 LQR에서 `Q`와 `R`을 동일한 양의 상수 `gamma`로
동시에 배율 조정하면 비용함수 전체만 배율되고 최적 이득 `K`는
변하지 않는다.

    Q_new = gamma Q
    R_new = gamma R
    gamma > 0

필수 내용:

- 제어이득은 `Q`와 `R`의 절대크기보다 상대적 비율에 영향을 받는다.
- 비용값 `J`와 Riccati 해 `P`의 스케일은 달라질 수 있다.
- `Q`만 또는 `R`만 변경하는 경우와 동일 배율 변경을 구분한다.
- 유한시간, 제약조건 또는 다른 비용항이 추가된 경우에는 별도 검토가
  필요하다.

### A09 — `state_lqr_state_input_normalization_bryson`

상태와 입력은 단위와 허용범위가 다르므로 가중치 선정 전에
정규화하거나 허용 최대편차를 기준으로 초기 가중치를 설정해야 한다.

Bryson's rule의 대표 초기값은 다음과 같다.

    Q_ii = 1 / x_i,max^2
    R_jj = 1 / u_j,max^2

필수 내용:

- Bryson's rule은 초기 튜닝용 경험칙이다.
- 허용 가능한 최대 상태편차와 입력크기를 물리적으로 정의한다.
- 동일한 수치의 대각 가중치가 동일한 물리적 중요도를 뜻하지 않는다.
- 최종 가중치는 시뮬레이션과 강인성 검증을 통해 조정한다.

### A10 — `state_lqr_pole_placement_distinction`

극점 배치는 원하는 폐루프 극점을 직접 지정하고 상태피드백 이득을
계산한다. LQR은 선택한 비용함수를 최소화한 결과로 폐루프 극점이
결정된다.

필수 내용:

- LQR은 폐루프 극점을 직접 지정하는 방법이 아니다.
- `Q`, `R` 조정으로 극점 위치가 간접적으로 변한다.
- 극점 배치는 명시적 동특성 요구에 유리하다.
- LQR은 상태성능과 제어부담의 체계적 절충에 유리하다.
- 두 방법 모두 가제어성 또는 안정화 가능성과 실제 제약 검증이
  필요하다.

### A11 — `state_lqr_tracking_prefilter_lqi`

기본 LQR은 원점으로 상태를 조절하는 regulator이며, 상수 기준입력의
정상상태 오차 0을 자동으로 보장하지 않는다.

필수 내용:

- 상태피드백 프리필터를 결합하여 기준입력 정상상태 이득을 조정할 수
  있다.
- 출력오차 적분상태를 추가한 LQI로 상수 기준입력과 상수 외란에 대한
  정상상태 오차를 개선할 수 있다.
- LQI에서는 확대시스템의 stabilizability와 원점 출력조절 가능성을
  확인한다.
- 프리필터와 적분상태의 역할을 구분한다.

### A12 — `state_lqr_saturation_constraints_limit`

표준 LQR의 이차 비용함수는 제어입력 크기를 비용으로 penalize하지만,
액추에이터의 hard saturation을 직접 제약조건으로 강제하지 않는다.

필수 내용:

- 큰 입력에는 비용이 부과되지만 입력 상·하한을 절대적으로 보장하지
  않는다.
- 실제 포화가 발생하면 선형 최적성 및 안정성 가정이 깨질 수 있다.
- LQI에서는 windup과 anti-windup을 검토한다.
- 엄격한 상태·입력 제약은 constrained optimal control 또는 MPC와
  같은 방법을 고려한다.

### A13 — `state_lqr_continuous_discrete_riccati_distinction`

연속시간 LQR은 CARE를 사용하고, 이산시간 LQR은 이산시간 대수
Riccati 방정식인 DARE를 사용한다.

기본 이산시간 모델은 다음과 같다.

    x[k+1] = A_d x[k] + B_d u[k]

DARE와 이산 최적이득은 다음과 같다.

    P = A_d^T P A_d
        - A_d^T P B_d
          (R + B_d^T P B_d)^(-1)
          B_d^T P A_d
        + Q

    K_d = (R + B_d^T P B_d)^(-1) B_d^T P A_d

필수 내용:

- 연속 CARE 해와 이산 DARE 해를 동일하게 사용하지 않는다.
- 연속 plant를 이산화할 때 샘플링주기와 비용함수 이산화를 고려한다.
- 이산 폐루프 안정성은 `A_d-B_dK_d`의 고유값이 단위원 내부에 있는지
  확인한다.
- 계산지연과 zero-order hold 영향을 검토한다.

### A14 — `state_lqr_robustness_observer_implementation_validation`

최종 LQR 제어기는 명목 비용함수 최소화뿐 아니라 실제 폐루프 성능과
구현 가능성을 종합 검증해야 한다.

필수 내용:

- `A-BK`의 폐루프 극점과 감쇠 특성
- 상태응답과 제어입력 크기
- 액추에이터 포화와 rate limit
- 모델 불확실성, 시간지연과 미모델 동특성
- 상태를 측정할 수 없는 경우 관측기 또는 Kalman filter
- 관측기와 제어기의 결합 및 separation principle의 적용조건
- 측정노이즈와 제어입력 노이즈 민감도
- 연속·이산 모델의 일치성과 샘플링주기
- Riccati residual과 수치조건
- 기준입력 추종과 외란응답
- 민감도, 강인성과 Monte Carlo 또는 파라미터 변화 검증

## 5. Fatal Wrong Claim 요구사항

### F01 — `state_lqr_fatal_arbitrary_q_r`

잘못된 주장:

LQR의 `Q`와 `R`은 행렬 조건과 물리적 의미에 관계없이 아무 값이나
사용해도 된다.

정확한 기준:

기본 LQR에서는 `Q`를 대칭 양의 준정부호, `R`을 대칭 양의 정부호로
설정하고 상태·입력의 단위, 허용범위와 설계목표를 반영해야 한다.

### F02 — `state_lqr_fatal_larger_q_always_better`

잘못된 주장:

`Q`를 크게 할수록 상태오차, 제어입력, 강인성과 모든 과도응답
성능이 항상 함께 향상된다.

정확한 기준:

상태 가중치 증가는 특정 상태편차 억제를 강화할 수 있지만 더 큰
제어입력, 포화, 노이즈 민감도와 강인성 저하를 유발할 수 있다.

### F03 — `state_lqr_fatal_smaller_r_no_control_cost`

잘못된 주장:

`R`을 0에 가깝게 줄일수록 제어입력 제한과 포화에 관계없이 최적
성능이 계속 향상된다.

정확한 기준:

작은 `R`은 큰 제어입력을 허용해 포화와 미모델 동특성을 자극할 수
있으며, 기본 이론에서 `R`은 양의 정부호여야 한다.

### F04 — `state_lqr_fatal_direct_pole_assignment`

잘못된 주장:

LQR은 사용자가 지정한 폐루프 극점을 정확히 배치하는 직접 극점
배치 방법이다.

정확한 기준:

LQR 폐루프 극점은 선택한 `Q`, `R`에 대한 비용함수 최소화 결과로
간접 결정되며, 원하는 극점을 직접 지정하는 방법은 극점 배치다.

### F05 — `state_lqr_fatal_unstabilizable_always_solution`

잘못된 주장:

`Q>=0`, `R>0`이면 `(A,B)`가 안정화 가능하지 않아도 항상 안정한
Riccati 해와 LQR 폐루프를 얻을 수 있다.

정확한 기준:

불안정한 비가제어 모드가 존재하면 상태피드백으로 안정화할 수 없다.
무한시간 안정화 LQR에는 stabilizability와 detectability 조건이
필요하다.

### F06 — `state_lqr_fatal_basic_lqr_zero_tracking_error`

잘못된 주장:

기본 LQR 상태피드백을 적용하면 별도 기준입력 경로 없이 모든 상수
기준입력의 정상상태 오차가 자동으로 0이 된다.

정확한 기준:

기본 LQR은 원점 조절기다. 기준입력 추종에는 정상상태 프리필터,
적분상태를 추가한 LQI 또는 다른 servo 구조가 필요할 수 있다.

### F07 — `state_lqr_fatal_cost_handles_hard_saturation`

잘못된 주장:

비용함수에 `u^TRu`가 있으므로 표준 LQR은 액추에이터의 hard
saturation과 입력 제한을 정확히 보장한다.

정확한 기준:

`R`은 입력 사용에 비용을 부과할 뿐 hard constraint를 직접 강제하지
않는다. 포화 시 별도 비선형 검증과 제약 최적제어가 필요하다.

### F08 — `state_lqr_fatal_care_equals_dare`

잘못된 주장:

연속시간 CARE에서 구한 `P`, `K`를 샘플링한 이산시스템에 그대로
사용하면 이산시간 LQR 최적해가 된다.

정확한 기준:

이산시간 시스템은 이산 모델과 DARE를 사용해 `K_d`를 계산해야 하며,
샘플링주기와 이산 비용함수를 고려해야 한다.

## 6. 권장 답안 구조

### O01 — LQR 설계 목적과 비용함수

상태편차와 제어입력의 상충관계를 비용함수로 정의하고 LQR의
최적성이 선택한 모델과 가중치에 대한 최적임을 설명한다.

참조 Anchor:

- `state_lqr_design_objective_cost`
- `state_lqr_weight_matrix_conditions`

### O02 — CARE와 최적 상태피드백 이득

연속시간 대수 Riccati 방정식, 안정화 해 `P`, 최적 이득 `K`와
폐루프 행렬 `A-BK`를 설명한다.

참조 Anchor:

- `state_lqr_care_stabilizing_solution`
- `state_lqr_optimal_gain_closed_loop`

### O03 — 해의 존재조건과 안정성

stabilizability, detectability, `Q>=0`, `R>0` 조건과 폐루프 안정성을
설명한다.

참조 Anchor:

- `state_lqr_existence_stabilizability_detectability`

### O04 — Q와 R의 가중치 설계

`Q`, `R` 변화가 상태응답, 제어입력, 포화와 강인성에 미치는 영향을
비교한다.

참조 Anchor:

- `state_lqr_q_weight_state_tradeoff`
- `state_lqr_r_weight_control_tradeoff`
- `state_lqr_common_scaling_invariance`

### O05 — 정규화와 Bryson's rule

상태·입력의 단위와 허용범위를 반영하여 초기 가중치를 선정하고
최종적으로 반복 튜닝하는 방법을 설명한다.

참조 Anchor:

- `state_lqr_state_input_normalization_bryson`

### O06 — 극점 배치와 기준입력 추종

극점 배치와 LQR의 차이를 설명하고 기본 regulator를 프리필터 또는
LQI로 확장하는 방법을 설명한다.

참조 Anchor:

- `state_lqr_pole_placement_distinction`
- `state_lqr_tracking_prefilter_lqi`

### O07 — 제약조건과 연속·이산 설계

표준 LQR의 포화 및 hard constraint 한계를 설명하고 CARE와 DARE를
구분한다.

참조 Anchor:

- `state_lqr_saturation_constraints_limit`
- `state_lqr_continuous_discrete_riccati_distinction`

### O08 — 관측기·강인성·최종 검증

관측기 기반 구현, 입력제한, 모델 불확실성, 노이즈, 샘플링과 수치
검증을 종합한다.

참조 Anchor:

- `state_lqr_robustness_observer_implementation_validation`

## 7. 고득점 해제조건

### H01 — 비용함수와 최적성의 범위

LQR의 최적성이 선택한 선형모델과 이차 비용함수에 대한 최적임을
설명한다.

### H02 — CARE와 안정화 해

CARE, 안정화 Riccati 해 `P`, 최적이득 `K`와 `A-BK`의 관계를
정확히 제시한다.

### H03 — 존재조건의 정확한 구분

가제어성보다 완화된 stabilizability와 detectability 조건을 설명한다.

### H04 — 가중치 상충관계

`Q`와 `R` 변화에 따른 상태편차, 제어입력, 포화, 노이즈와 강인성의
상충관계를 설명한다.

### H05 — 스케일과 정규화

`Q`, `R`의 동일 배율 불변성과 상태·입력 단위를 반영한 정규화 및
Bryson's rule을 설명한다.

### H06 — 극점 배치·LQR·LQI의 역할 구분

극점 직접 배치와 비용 최적화의 차이, 기본 LQR regulator와 LQI
servo의 차이를 설명한다.

### H07 — 포화와 이산시간 설계

표준 LQR이 hard saturation을 보장하지 않는 이유와 CARE·DARE의
차이를 설명한다.

### H08 — 실제 폐루프 종합 검증

폐루프 극점, 제어입력, 포화, 관측기, 불확실성, 노이즈, 샘플링과
Riccati 수치오차를 종합 검증한다.

## 8. Source Topic Pack 작성 계약

후속 Source Topic Pack은 다음 파일로 구성한다.

- `README.md`
- `fact_anchor.json`
- `logic_check.json`
- `model_answer.json`
- `topic_importance.json`

필수 수량:

- Fact Anchor: 14개
- Fatal Wrong Claim: 8개
- 권장 답안 구조: 8개
- 고득점 해제조건: 8개

추가 원칙:

- 모든 ID는 이 문서에 정의된 전역 고유 ID를 그대로 사용한다.
- 결정론적 검사는 비활성화한다.
- candidate extraction rule은 비워 둔다.
- 공식 누락이나 단순 계산 실수만으로 즉시 Fatal 처리하지 않는다.
- 조건 없는 반대 주장과 핵심 최적제어 원리 위반을 Fatal 후보로
  판정한다.
- `Q`, `R` 튜닝에 하나의 절대 정답이 있다고 가정하지 않는다.
- CARE와 DARE, regulator와 servo, 비용 penalty와 hard constraint를
  명확히 구분한다.

## LQR 설계 적용조건

- 교차항이 없는 표준 연속시간 무한시간 LQR에서 Q=Q^T⪰0, R=R^T≻0, (A,B)가 stabilizable이고 (Q^(1/2),A)가 detectable이면 폐루프 A-BK를 Hurwitz로 만드는 고유한 양의 준정부호 안정화 해 P=P^T⪰0가 존재한다. 완전 가제어성과 완전 관측성은 더 강한 충분조건이다.
- (Q^(1/2),A)의 detectability는 비용함수에서 보이지 않는 불안정 모드를 배제하기 위한 CARE 조건이다. 실제 상태를 모두 측정하지 못해 관측기를 사용할 때에는 측정쌍 (C,A)의 detectability와 추정오차 동역학 A-LC의 안정성을 별도로 확인한다.
- 기본 LQR은 원점 조절기이다. 비영점 평형점을 추종하려면 실현 가능한 정상상태 (x_r,u_r)를 구하고 x-x_r, u-u_r의 오차좌표로 설계한다. 정적 프리필터는 명목 정상상태 추종을 보완하지만 모델 오차와 상수 외란에 대한 robust zero error를 보장하지 않는다. LQI는 적분상태를 포함한 확대시스템의 stabilizability를 확인하고 포화 시 windup을 검증해야 한다.
- 특정 상태의 Q 가중치를 상대적으로 높이면 그 상태편차 억제를 더 중시하는 최적해가 계산된다. 다만 Riccati 해와 폐루프 이득은 결합적으로 변하므로 모든 상태응답의 단조 개선을 보장하지 않는다. 제어입력, 포화, 측정·추정 잡음과 모델 불확실성에 대한 민감도는 별도로 검증한다.
- 이산시간 LQR은 이산화된 (A_d,B_d), 이산시간 비용 정의와 DARE를 사용한다. 표본시간과 연속 비용의 이산 등가화 방법에 따라 Q_d와 R_d가 달라질 수 있으므로 CARE 식을 그대로 적용하지 않는다.
- 답안이 J=∫(x^TQx+2x^TNu+u^TRu)dt의 교차항 N을 포함한 일반화 LQR을 명시하고 비용 블록행렬 조건, 일반화 Riccati 방정식과 이득식을 일관되게 사용하면 기본식과 다르다는 이유만으로 오류 처리하지 않는다.
- Fatal의 직접 점수 영향은 B/C에 한정한다. D/E 점수는 직접 변경하지 않고 관련 현장 적용·제언의 claim trust만 limited로 표시한다.

## Fact verification references

- MathWorks `lqr`: continuous-time LQR cost, gain and Riccati solution
- MathWorks `icare`: stabilizing continuous-time Riccati solution
- MathWorks `dlqr` and `idare`: discrete-time LQR and DARE
- MathWorks `lqi`: integral-state augmentation and tracking
- MathWorks `place`: state-feedback and observer pole placement
- MIT Underactuated Robotics: LQR, equilibrium and trajectory linearization
