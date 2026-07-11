# 상태공간 모델의 제어가능성·관측가능성과 극점배치 설계

## Topic Pack 정보

- Topic ID: `state_space_controllability_observability_pole_placement`
- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: `LLM_ONLY`
- deterministic checks: disabled
- candidate extraction rules: empty

## 평가 목적

이 Topic Pack은 상태공간 모델의 정의만 확인하지 않는다.

다음 내용을 하나의 설계 흐름으로 평가한다.

1. 상태방정식과 출력방정식
2. 전달함수와 realization 관계
3. 최소 realization과 숨은 내부 모드
4. 제어가능성과 stabilizability
5. 관측가능성과 detectability
6. 상태피드백과 폐루프 극점배치
7. Luenberger observer
8. separation principle
9. 기준입력 추종과 적분 확대
10. 포화·잡음·sampling·수치조건 검증

## 핵심 수식

- `x_dot=Ax+Bu`
- `y=Cx+Du`
- `G(s)=C(sI-A)^(-1)B+D`
- `C_c=[B,AB,...,A^(n-1)B]`
- `rank(C_c)=n`
- `O=[C;CA;...;CA^(n-1)]`
- `rank(O)=n`
- `rank[λI-A,B]=n`
- `rank[[λI-A];C]=n`
- `u=-Kx+Nr`
- `x_dot=(A-BK)x+BNr`
- `e_dot=(A-LC)e`
- `K=e_n^T C_c^(-1)φ_d(A)`
- `z=e^(sT)`

## 설계 판단 원칙

- controllability와 stability는 서로 다른 속성이다.
- stabilizability는 완전 제어가능성과 구분한다.
- detectability는 완전 관측가능성과 구분한다.
- 제어 불가능한 모드는 상태피드백으로 이동시킬 수 없다.
- 관측 불가능한 불안정 모드는 observer로 수렴시킬 수 없다.
- controller pole과 observer pole은 독립적으로 설계할 수 있다.
- 상태피드백만으로 정상상태 추종오차 0이 자동 보장되지 않는다.
- 빠른 극점은 control effort, 포화, 잡음과 sampling 문제를 키울 수 있다.

## Fact Anchor

총 14개의 Anchor를 사용한다.

- `state_space_model_and_dimensions`
- `transfer_function_realization_relation`
- `eigenvalue_pole_minimal_realization`
- `controllability_matrix_rank`
- `pbh_controllability_stabilizability`
- `observability_matrix_rank`
- `pbh_observability_detectability`
- `state_feedback_closed_loop`
- `pole_placement_conditions`
- `ackermann_and_numerical_limits`
- `observer_error_dynamics`
- `separation_principle_conditions`
- `reference_tracking_integral_action`
- `implementation_tradeoffs_validation`

## Fatal Misconception

총 8개의 Fatal 조건을 사용한다.

- `controllability_equals_stability`
- `all_realizations_controllable_observable`
- `uncontrollable_poles_arbitrary_placement`
- `unobservable_states_exactly_reconstructable`
- `a_eigenvalues_always_transfer_poles`
- `state_feedback_always_zero_steady_state_error`
- `observer_poles_must_equal_controller_poles`
- `separation_principle_unconditional`

## 권장 답안 흐름

1. 배경과 상태공간 설계 목적
2. 모델과 전달함수 관계
3. 제어가능성과 stabilizability
4. 관측가능성과 detectability
5. 상태피드백과 극점배치
6. Observer와 separation principle
7. 기준입력 추종과 적분 확대
8. 현장 구현과 검증

## 현장 적용 기준

- actuator saturation
- actuator rate limit
- control effort
- sensor noise
- observer peaking
- sampling period
- 계산지연
- state scaling
- numerical conditioning
- model uncertainty
- 운전점 변화
- simulation
- HIL
- 단계적 현장 적용

## 기존 Topic과의 경계

기존 `transfer_function_state_space`는 전달함수와 상태공간 표현의 비교가 중심이다.

이 Topic Pack은 controllability, observability, pole placement, observer와 servo 설계가 중심이다.

근궤적은 scalar gain 변화에 따른 폐루프 극점 이동을 해석하지만, 이 Topic Pack은 full-state feedback gain K를 설계한다.

## 유지보수 원칙

요구사항 기준 문서는 다음 파일이다.

`docs/topic_sheets/state_space_controllability_observability_pole_placement.md`

Source 변경 후 generated Rubric Bank 6개를 다시 생성해야 한다.

Source validator와 quality validator의 error와 warning이 모두 0이어야 한다.

LLM semantic review에서는 rank 조건, 부호 convention, 적용 조건과 현장 한계를 함께 검토한다.
