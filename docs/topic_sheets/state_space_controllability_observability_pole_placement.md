# 상태공간 모델의 제어가능성·관측가능성과 극점배치 설계

## 1. Topic Pack 기본 정보

- Topic ID: `state_space_controllability_observability_pole_placement`
- 제목: 상태공간 모델의 제어가능성·관측가능성과 극점배치 설계
- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: `LLM_ONLY`
- deterministic logic check: 비활성
- candidate extraction rules: 빈 배열
- 주요 범위: 연속시간 선형 시불변 시스템
- 보조 범위: 이산시간 구현 시 주의사항
- 제외 범위: 비선형 관측기, 확장 Kalman filter의 상세 유도, 강인제어의 상세 설계

## 2. Topic Pack의 목적

이 Topic Pack은 상태공간 모델을 단순히 행렬 형태로 정의하는 수준을 넘어 다음 사항을 평가한다.

1. 상태방정식과 출력방정식의 물리적 의미를 설명한다.
2. 전달함수와 상태공간 realization의 관계를 조건과 함께 설명한다.
3. 제어가능성과 관측가능성을 rank 조건 및 PBH test로 판정한다.
4. stabilizability와 detectability를 완전 제어가능성·관측가능성과 구분한다.
5. 상태피드백에 의한 폐루프 극점배치 조건을 설명한다.
6. 상태관측기의 오차 동역학과 관측기 극점 설계를 설명한다.
7. separation principle의 적용 조건과 한계를 설명한다.
8. 기준입력 추종, 정상상태 오차, 적분기 추가 및 prefilter의 역할을 설명한다.
9. 포화, 모델 오차, 잡음, sampling, 수치조건과 같은 현장 구현 문제를 설명한다.
10. 계산 결과를 실제 제어기·관측기 설계 판단과 연결한다.

## 3. 잠금된 핵심 정의와 수식

### 3.1 연속시간 상태공간 모델

기본 모델은 다음과 같다.

- 상태방정식: `x_dot(t) = A x(t) + B u(t)`
- 출력방정식: `y(t) = C x(t) + D u(t)`

차원은 다음과 같다.

- `x ∈ R^n`
- `u ∈ R^m`
- `y ∈ R^p`
- `A ∈ R^(n×n)`
- `B ∈ R^(n×m)`
- `C ∈ R^(p×n)`
- `D ∈ R^(p×m)`

상태변수는 미래 출력을 결정하는 데 필요한 최소 내부변수로 설명할 수 있지만, 임의로 선택한 realization이 항상 최소차수인 것은 아니다.

### 3.2 전달함수와 상태공간의 관계

영 초기조건에서 전달함수 행렬은 다음과 같다.

`G(s) = C(sI-A)^(-1)B + D`

이 관계를 설명할 때 다음 조건을 명시한다.

- 전달함수는 외부 입력·출력 관계를 나타낸다.
- 상태공간 모델은 내부 상태와 초기조건을 표현할 수 있다.
- 동일한 전달함수에 여러 상태공간 realization이 존재할 수 있다.
- similarity transformation으로 표현이 달라져도 입력·출력 동특성은 유지된다.
- 비최소 realization에는 입력·출력에서 보이지 않는 내부 모드가 포함될 수 있다.

### 3.3 A 행렬 고유값과 전달함수 극점

`det(sI-A)=0`의 근은 A 행렬의 고유값이다.

최소 realization에서는 전달함수의 극점과 A의 고유값이 일치한다.

비최소 realization에서는 다음 현상이 가능하다.

- 제어 불가능한 모드
- 관측 불가능한 모드
- pole-zero cancellation
- 전달함수에서 보이지 않는 내부 고유값

따라서 “A의 모든 고유값은 항상 전달함수의 극점이다”라고 일반화하면 안 된다.

### 3.4 제어가능성 행렬

연속시간 LTI 시스템의 제어가능성 행렬은 다음과 같다.

`C_c = [B, AB, A^2B, ..., A^(n-1)B]`

완전 제어가능 조건은 다음과 같다.

`rank(C_c) = n`

의미는 유한시간 동안 적절한 입력을 사용하여 임의의 초기상태에서 임의의 최종상태로 상태를 이동시킬 수 있다는 것이다.

MIMO 시스템에서는 B가 여러 열을 가지므로 제어가능성 행렬 전체의 rank로 판정한다.

### 3.5 PBH 제어가능성 test

PBH 제어가능성 조건은 A의 모든 고유값 `λ`에 대해 다음과 같다.

`rank[λI-A, B] = n`

동등한 좌고유벡터 표현은 다음과 같다.

`q^T A = λ q^T`인 0이 아닌 `q`에 대해 `q^T B ≠ 0`

PBH test는 어떤 고유모드가 입력에 의해 제어되는지를 모드별로 해석하는 데 유용하다.

### 3.6 Stabilizability

완전 제어가능하지 않더라도 모든 불안정 모드가 제어가능하면 stabilizable하다.

연속시간 시스템에서 stabilizability 조건은 실수부가 0 이상인 모든 고유값 `λ`에 대해 다음 rank 조건이 성립하는 것이다.

`rank[λI-A, B] = n`

안정한 제어 불가능 모드는 남아 있어도 상태피드백으로 전체 폐루프를 안정화할 수 있다.

따라서 다음은 서로 다른 개념이다.

- controllability
- stabilizability
- stability

### 3.7 관측가능성 행렬

관측가능성 행렬은 다음과 같다.

`O = [C; CA; CA^2; ...; CA^(n-1)]`

완전 관측가능 조건은 다음과 같다.

`rank(O) = n`

의미는 유한시간의 입력과 출력 정보로 초기상태를 유일하게 복원할 수 있다는 것이다.

### 3.8 PBH 관측가능성 test

PBH 관측가능성 조건은 A의 모든 고유값 `λ`에 대해 다음과 같다.

`rank[[λI-A]; C] = n`

동등한 우고유벡터 표현은 다음과 같다.

`A v = λ v`인 0이 아닌 `v`에 대해 `C v ≠ 0`

출력에 나타나지 않는 고유모드는 관측 불가능하다.

### 3.9 Detectability

완전 관측가능하지 않더라도 모든 불안정 모드가 관측가능하면 detectable하다.

연속시간 시스템에서 detectability 조건은 실수부가 0 이상인 모든 고유값에 대해 PBH 관측가능성 rank 조건이 성립하는 것이다.

안정한 관측 불가능 모드는 남아 있어도 관측오차가 수렴하는 observer를 설계할 수 있다.

### 3.10 상태피드백

상태피드백 제어입력은 다음과 같이 정의한다.

`u = -Kx + Nr`

D가 없다고 가정하면 폐루프 상태방정식은 다음과 같다.

`x_dot = (A-BK)x + BN r`

폐루프 극점은 `A-BK`의 고유값이다.

완전 제어가능한 시스템에서는 상태피드백으로 폐루프 극점을 임의의 원하는 위치에 배치할 수 있다.

제어 불가능한 모드의 고유값은 K로 이동시킬 수 없다.

### 3.11 극점배치 설계

극점배치 절차는 다음 순서를 기본으로 한다.

1. A와 B의 차원 및 모델 의미를 확인한다.
2. 제어가능성 또는 stabilizability를 판정한다.
3. 시간응답 사양을 목표 극점으로 변환한다.
4. `A-BK`가 목표 특성다항식을 갖도록 K를 계산한다.
5. 계산된 폐루프 고유값을 재검증한다.
6. 제어입력 크기와 포화를 확인한다.
7. 모델 불확실성과 운전점 변화에 대한 민감도를 확인한다.

목표 극점을 지나치게 좌측에 배치하면 응답은 빨라질 수 있지만 다음 문제가 커질 수 있다.

- 큰 제어입력
- actuator saturation
- 미모델링 고주파 동특성 자극
- sampling 한계
- 잡음 민감도 증가
- 모델 오차 민감도 증가

### 3.12 Ackermann 공식

SISO 완전 제어가능 시스템에서 Ackermann 공식으로 K를 계산할 수 있다.

개념적 표현은 다음과 같다.

`K = e_n^T C_c^(-1) φ_d(A)`

여기서 다음을 확인한다.

- `C_c`는 제어가능성 행렬이다.
- `φ_d(A)`는 목표 특성다항식을 A에 대입한 행렬다항식이다.
- `e_n^T = [0, ..., 0, 1]`
- 부호 규약은 `u=-Kx`를 기준으로 한다.

Ackermann 공식은 이론적으로 명확하지만 고차 시스템이나 condition number가 큰 시스템에서는 수치적으로 취약할 수 있다.

실제 계산에서는 다음을 함께 고려한다.

- controllable canonical form
- Schur 기반 pole placement
- numerical conditioning
- state scaling
- robust pole assignment

### 3.13 전상태 관측기

Luenberger observer는 다음과 같이 표현한다.

`x_hat_dot = A x_hat + B u + L(y-C x_hat)`

관측오차를 다음과 같이 정의한다.

`e = x - x_hat`

D가 적절히 처리된 경우 오차 동역학은 다음과 같다.

`e_dot = (A-LC)e`

관측기 극점은 `A-LC`의 고유값이다.

완전 관측가능한 시스템에서는 L을 사용하여 관측기 극점을 임의로 배치할 수 있다.

Detectable한 시스템에서는 적어도 관측오차가 수렴하도록 안정한 observer를 설계할 수 있다.

### 3.14 관측기 극점 선정

관측기 극점은 일반적으로 제어기 폐루프 극점보다 빠르게 선정하지만 “반드시 특정 배수”라는 절대 규칙은 없다.

너무 빠른 관측기 극점은 다음 문제를 유발할 수 있다.

- 센서 잡음 증폭
- peaking
- 초기 추정오차에 의한 큰 과도응답
- 미모델링 동특성 민감도 증가
- discrete sampling과 계산주기 한계

따라서 관측기 속도는 다음 요소를 함께 고려해 정한다.

- 센서 대역폭
- 잡음 수준
- sampling period
- 모델 정확도
- actuator 및 계산 자원
- 초기상태 불확실성

### 3.15 Observer 기반 상태피드백

실제 상태를 직접 측정하지 못하는 경우 다음 제어입력을 사용할 수 있다.

`u = -K x_hat + Nr`

확대 시스템의 동특성은 적절한 좌표변환 아래에서 다음 두 행렬의 고유값으로 분리된다.

- `A-BK`
- `A-LC`

이것이 separation principle의 핵심이다.

### 3.16 Separation principle의 조건

선형 시불변 시스템에서 다음 조건 아래 controller와 observer를 독립적으로 설계할 수 있다.

- 모델이 LTI 형태이다.
- 상태피드백 controller가 안정화 가능하다.
- observer가 수렴하도록 설계 가능하다.
- 선형 모델의 적용 범위가 유효하다.

다음 조건에서는 단순한 separation principle 해석을 그대로 일반화하면 안 된다.

- 강한 비선형성
- actuator saturation
- switching 또는 hybrid dynamics
- 큰 모델 불확실성
- 시간변화 시스템
- 제약조건이 지배적인 시스템
- 심각한 sampling 및 delay 영향

### 3.17 기준입력 추종과 정상상태 오차

상태피드백 `u=-Kx`는 폐루프 극점을 바꾸지만 기준입력의 정상상태 추종을 자동으로 보장하지 않는다.

정상상태 오차 개선 방법은 다음과 같다.

- reference prefilter N
- integral state augmentation
- disturbance model augmentation
- servo design
- feedforward compensation

Prefilter는 정확한 모델과 일정한 기준입력 조건에서 추종 이득을 조정할 수 있지만, 지속 외란이나 모델 오차에 대한 적분 보상과 동일하지 않다.

Integral augmentation은 정상상태 오차 제거에 유리하지만 다음을 다시 확인해야 한다.

- 확대 시스템 제어가능성
- windup
- actuator saturation
- 적분기 초기조건
- 폐루프 극점과 강인성

### 3.18 최소 realization과 Kalman decomposition

Minimal realization은 제어가능하고 관측가능한 상태만 포함하는 최소차수 realization이다.

Kalman decomposition은 상태공간을 다음 부분으로 분해할 수 있다.

- controllable and observable
- controllable and unobservable
- uncontrollable and observable
- uncontrollable and unobservable

입력·출력 전달함수의 최소 realization에는 controllable and observable 부분만 남는다.

내부 안정성을 판단할 때는 전달함수에서 상쇄되어 보이지 않는 내부 불안정 모드가 없는지 확인해야 한다.

### 3.19 이산시간 구현

연속시간 설계를 디지털 제어기로 구현할 때 다음을 확인한다.

- discretization 방법
- sampling period
- zero-order hold
- 연속시간 극점과 이산시간 극점의 관계 `z=e^(sT)`
- 계산지연
- quantization
- estimator update timing
- actuator command update timing

이산시간 안정영역은 단위원 내부이며, 연속시간 좌반평면과 직접 동일하지 않다.

### 3.20 현장 설계 검증

최종 설계에서는 다음 항목을 확인한다.

1. 모델의 운전점과 선형화 범위
2. 상태변수의 물리적 의미와 측정 가능성
3. 단위와 state scaling
4. controllability 및 observability rank
5. rank 판정 tolerance와 condition number
6. 목표 controller pole
7. 목표 observer pole
8. actuator saturation 및 rate limit
9. sensor noise와 filtering
10. sampling 및 계산주기
11. 모델 오차와 parameter 변화
12. 초기상태 및 observer peaking
13. 기준입력 추종과 외란 억제
14. simulation, HIL 및 단계적 현장 적용

## 4. Fact Anchor 계약

### A01. 상태공간 모델과 차원

- Anchor ID: `state_space_model_and_dimensions`
- 중요도: `must`
- 핵심 내용:
  - `x_dot=Ax+Bu`
  - `y=Cx+Du`
  - 상태·입력·출력 및 행렬 차원
  - 내부상태와 초기조건 표현
- 오류 방지:
  - 상태변수를 단순 출력변수와 동일시하지 않는다.
  - 임의 realization이 항상 최소차수라고 하지 않는다.

### A02. 전달함수와 realization 관계

- Anchor ID: `transfer_function_realization_relation`
- 중요도: `must`
- 핵심 내용:
  - `G(s)=C(sI-A)^(-1)B+D`
  - 영 초기조건
  - 동일 전달함수의 여러 realization
  - similarity transformation
- 오류 방지:
  - 전달함수와 상태공간을 조건 없이 완전히 동일한 표현이라고 하지 않는다.

### A03. 고유값·극점과 최소 realization

- Anchor ID: `eigenvalue_pole_minimal_realization`
- 중요도: `must`
- 핵심 내용:
  - A의 고유값
  - 전달함수 극점
  - 최소 realization
  - pole-zero cancellation
  - 숨은 내부 모드
- 오류 방지:
  - 모든 A 고유값이 항상 전달함수 극점이라고 하지 않는다.

### A04. 제어가능성 행렬과 rank

- Anchor ID: `controllability_matrix_rank`
- 중요도: `must`
- 핵심 내용:
  - `C_c=[B,AB,...,A^(n-1)B]`
  - `rank(C_c)=n`
  - 상태 도달 가능성
- 오류 방지:
  - B의 rank만으로 전체 제어가능성을 판단하지 않는다.

### A05. PBH 제어가능성과 stabilizability

- Anchor ID: `pbh_controllability_stabilizability`
- 중요도: `must`
- 핵심 내용:
  - `rank[λI-A,B]=n`
  - 모드별 제어가능성
  - 불안정 모드 제어가능성
  - stabilizability
- 오류 방지:
  - stabilizable을 완전 제어가능과 동일시하지 않는다.

### A06. 관측가능성 행렬과 rank

- Anchor ID: `observability_matrix_rank`
- 중요도: `must`
- 핵심 내용:
  - `O=[C;CA;...;CA^(n-1)]`
  - `rank(O)=n`
  - 초기상태 복원
- 오류 방지:
  - C의 rank만으로 전체 관측가능성을 판단하지 않는다.

### A07. PBH 관측가능성과 detectability

- Anchor ID: `pbh_observability_detectability`
- 중요도: `must`
- 핵심 내용:
  - `rank[[λI-A];C]=n`
  - 모드별 관측가능성
  - 불안정 모드 관측가능성
  - detectability
- 오류 방지:
  - detectable을 완전 관측가능과 동일시하지 않는다.

### A08. 상태피드백 폐루프 모델

- Anchor ID: `state_feedback_closed_loop`
- 중요도: `must`
- 핵심 내용:
  - `u=-Kx+Nr`
  - `A-BK`
  - 폐루프 고유값
  - 부호 규약
- 오류 방지:
  - 상태피드백이 A 자체의 물리적 plant dynamics를 제거한다고 표현하지 않는다.

### A09. 극점배치 가능 조건

- Anchor ID: `pole_placement_conditions`
- 중요도: `must`
- 핵심 내용:
  - 완전 제어가능 시 임의 극점배치
  - 제어 불가능 모드의 고유값은 이동 불가
  - stabilizable이면 안정화 가능
- 오류 방지:
  - 제어 불가능한 시스템에서도 모든 극점을 임의 배치할 수 있다고 하지 않는다.

### A10. Ackermann 공식과 수치 한계

- Anchor ID: `ackermann_and_numerical_limits`
- 중요도: `must`
- 핵심 내용:
  - SISO Ackermann 공식
  - 목표 특성다항식
  - controllability matrix inverse
  - numerical conditioning
  - state scaling
- 오류 방지:
  - 고차·ill-conditioned 시스템에서도 항상 수치적으로 안전하다고 하지 않는다.

### A11. Observer 오차 동역학

- Anchor ID: `observer_error_dynamics`
- 중요도: `must`
- 핵심 내용:
  - Luenberger observer
  - `e_dot=(A-LC)e`
  - 관측기 극점
  - observability와 detectability
- 오류 방지:
  - 관측 불가능한 불안정 모드를 observer로 임의 안정화할 수 있다고 하지 않는다.

### A12. Separation principle 조건

- Anchor ID: `separation_principle_conditions`
- 중요도: `must`
- 핵심 내용:
  - `A-BK`
  - `A-LC`
  - controller와 observer 독립 설계
  - LTI 조건
  - 비선형·포화·불확실성 한계
- 오류 방지:
  - 모든 비선형 및 포화 시스템에 무조건 적용된다고 하지 않는다.

### A13. 기준입력 추종과 적분 보상

- Anchor ID: `reference_tracking_integral_action`
- 중요도: `must`
- 핵심 내용:
  - state feedback만으로 정상상태 오차 0이 보장되지 않음
  - prefilter
  - integral augmentation
  - disturbance rejection
  - 확대 시스템 제어가능성
- 오류 방지:
  - prefilter와 적분 보상을 동일한 기능이라고 하지 않는다.

### A14. 구현 trade-off와 검증

- Anchor ID: `implementation_tradeoffs_validation`
- 중요도: `must`
- 핵심 내용:
  - pole speed와 control effort
  - observer speed와 noise
  - saturation
  - sampling
  - model uncertainty
  - scaling 및 numerical conditioning
  - simulation과 현장 단계 적용
- 오류 방지:
  - 극점을 무조건 빠르게 배치할수록 좋은 설계라고 하지 않는다.

## 5. Fatal Misconception 계약

### F01. 제어가능성과 안정성 동일시

- Fatal ID: `controllability_equals_stability`
- 잘못된 주장:
  - 제어가능하면 open-loop 시스템은 반드시 안정하다.
  - 불안정하면 제어 불가능하다.
- 올바른 기준:
  - controllability와 stability는 서로 다른 속성이다.

### F02. 모든 realization은 자동으로 제어·관측 가능

- Fatal ID: `all_realizations_controllable_observable`
- 잘못된 주장:
  - 상태공간으로 표현되면 항상 제어가능하고 관측가능하다.
- 올바른 기준:
  - rank 또는 PBH test로 각각 확인해야 한다.

### F03. 제어 불가능한 극점도 임의 배치 가능

- Fatal ID: `uncontrollable_poles_arbitrary_placement`
- 잘못된 주장:
  - K를 선택하면 시스템의 모든 고유값을 항상 원하는 위치로 이동할 수 있다.
- 올바른 기준:
  - 완전 제어가능해야 임의 극점배치가 가능하며 제어 불가능 모드는 이동하지 않는다.

### F04. 관측 불가능 상태의 완전 복원

- Fatal ID: `unobservable_states_exactly_reconstructable`
- 잘못된 주장:
  - L을 크게 하면 관측 불가능 상태도 출력으로 정확히 복원할 수 있다.
- 올바른 기준:
  - 관측 불가능한 불안정 모드는 observer로 복원·수렴시킬 수 없다.

### F05. A 고유값과 전달함수 극점의 무조건 일치

- Fatal ID: `a_eigenvalues_always_transfer_poles`
- 잘못된 주장:
  - 모든 realization에서 A의 모든 고유값은 항상 전달함수 극점과 정확히 일치한다.
- 올바른 기준:
  - 최소 realization에서 일치하며 비최소 realization에는 숨은 모드와 상쇄가 있을 수 있다.

### F06. 상태피드백만으로 정상상태 오차 항상 0

- Fatal ID: `state_feedback_always_zero_steady_state_error`
- 잘못된 주장:
  - `u=-Kx`만 적용하면 모든 기준입력과 외란에 대해 정상상태 오차가 자동으로 0이 된다.
- 올바른 기준:
  - prefilter, 적분 확대 또는 disturbance model이 추가로 필요할 수 있다.

### F07. 관측기 극점은 제어기 극점과 동일해야 함

- Fatal ID: `observer_poles_must_equal_controller_poles`
- 잘못된 주장:
  - separation principle 때문에 observer pole과 controller pole은 반드시 같아야 한다.
- 올바른 기준:
  - 두 극점 집합은 독립 설계할 수 있으며 잡음·peaking·sampling을 고려해 선정한다.

### F08. Separation principle의 무조건적 적용

- Fatal ID: `separation_principle_unconditional`
- 잘못된 주장:
  - observer 기반 상태피드백의 독립 설계는 비선형, 포화, 시간변화, 제약 시스템에서도 조건 없이 성립한다.
- 올바른 기준:
  - 기본 separation principle은 LTI 모델과 해당 안정화·검출 가능 조건에서 적용한다.

## 6. LLM Truth Schema 계약

Truth schema는 다음 14개 ID를 Fact Anchor와 동일하게 사용한다.

1. `state_space_model_and_dimensions`
2. `transfer_function_realization_relation`
3. `eigenvalue_pole_minimal_realization`
4. `controllability_matrix_rank`
5. `pbh_controllability_stabilizability`
6. `observability_matrix_rank`
7. `pbh_observability_detectability`
8. `state_feedback_closed_loop`
9. `pole_placement_conditions`
10. `ackermann_and_numerical_limits`
11. `observer_error_dynamics`
12. `separation_principle_conditions`
13. `reference_tracking_integral_action`
14. `implementation_tradeoffs_validation`

Fatal condition은 다음 8개 ID를 Fatal Misconception과 동일하게 사용한다.

1. `controllability_equals_stability`
2. `all_realizations_controllable_observable`
3. `uncontrollable_poles_arbitrary_placement`
4. `unobservable_states_exactly_reconstructable`
5. `a_eigenvalues_always_transfer_poles`
6. `state_feedback_always_zero_steady_state_error`
7. `observer_poles_must_equal_controller_poles`
8. `separation_principle_unconditional`

## 7. Safe Expression 계약

다음 표현은 조건을 충족하면 정답으로 인정한다.

1. 상태방정식을 `dx/dt=Ax+Bu`로 표기한다.
2. controllability matrix를 `M_c`, `Q_c`, `P` 등 다른 기호로 표기한다.
3. observability matrix를 `M_o`, `Q_o` 등 다른 기호로 표기한다.
4. rank 조건을 full row rank 또는 rank n으로 표현한다.
5. PBH matrix의 열 배치나 부호를 동등한 형태로 표현한다.
6. `u=-Kx` 대신 `u=Kx`를 사용하되 폐루프 행렬의 부호 규약을 일관되게 설명한다.
7. observer injection을 `L(y-Cx_hat)` 또는 동등한 형태로 표현한다.
8. stabilizability를 모든 불안정 모드가 제어가능한 조건으로 설명한다.
9. detectability를 모든 불안정 모드가 관측가능한 조건으로 설명한다.
10. 목표 극점을 자연주파수·감쇠비·정착시간 사양으로부터 정한다.
11. Ackermann 대신 `place`, canonical form 또는 Schur 기반 방법을 사용한다.
12. prefilter 대신 reference gain 또는 feedforward gain이라는 표현을 사용한다.
13. integral augmentation을 servo augmentation 또는 error integrator 추가로 표현한다.
14. observer를 state estimator 또는 Luenberger estimator라고 표현한다.
15. 최소 realization을 controllable and observable realization으로 설명한다.
16. 수치 rank 판정에서 tolerance와 singular value를 사용한다.

## 8. Question Pattern 계약

### Q01. 상태공간 기본 해석

- 상태공간 모델의 구성과 전달함수와의 관계를 설명하시오.

### Q02. 제어가능성 계산

- 주어진 A, B 행렬의 제어가능성을 판정하고 그 의미를 설명하시오.

### Q03. 관측가능성 계산

- 주어진 A, C 행렬의 관측가능성을 판정하고 그 의미를 설명하시오.

### Q04. PBH test

- PBH test를 이용하여 제어가능성·관측가능성을 판정하시오.

### Q05. 상태피드백 극점배치

- 상태피드백으로 목표 폐루프 극점을 만족하는 K를 설계하시오.

### Q06. Observer 설계

- 전상태 관측기의 원리와 observer gain L의 설계 절차를 설명하시오.

### Q07. Observer 기반 상태피드백

- separation principle을 이용한 observer 기반 상태피드백 설계를 설명하시오.

### Q08. 추종 및 현장 적용

- 상태피드백 시스템의 정상상태 오차 개선과 현장 구현 시 고려사항을 설명하시오.

## 9. 권장 답안 구조

### O01. 배경과 상태공간 설계 목적

- Outline ID: `state_space_design_purpose`
- 상태공간 모델이 내부상태, 초기조건, MIMO 시스템 및 현대제어 설계에 필요한 이유를 설명한다.

### O02. 모델과 전달함수 관계

- Outline ID: `model_and_realization_relation`
- `x_dot=Ax+Bu`, `y=Cx+Du`, `G(s)=C(sI-A)^(-1)B+D`와 최소 realization 조건을 설명한다.

### O03. 제어가능성과 stabilizability

- Outline ID: `controllability_and_stabilizability`
- controllability matrix, rank 조건, PBH test 및 stabilizability를 설명한다.

### O04. 관측가능성과 detectability

- Outline ID: `observability_and_detectability`
- observability matrix, rank 조건, PBH test 및 detectability를 설명한다.

### O05. 상태피드백과 극점배치

- Outline ID: `state_feedback_pole_placement`
- `A-BK`, 목표 극점 선정, Ackermann 또는 수치 pole placement 절차를 설명한다.

### O06. Observer와 separation principle

- Outline ID: `observer_and_separation_principle`
- `A-LC`, observer pole 선정, observer 기반 상태피드백과 적용 조건을 설명한다.

### O07. 기준입력 추종과 적분 확대

- Outline ID: `reference_tracking_and_integral_augmentation`
- prefilter, integral augmentation, 정상상태 오차 및 외란 억제를 설명한다.

### O08. 현장 구현과 검증

- Outline ID: `implementation_and_validation`
- 포화, 잡음, sampling, scaling, 수치조건, 모델 오차 및 단계적 적용을 설명한다.

## 10. 고득점 판단 조건

### H01. 모델 정의의 정확성

- `x_dot=Ax+Bu`, `y=Cx+Du`와 행렬 차원을 정확히 설명한다.

### H02. 내부·외부 동특성 구분

- 전달함수와 realization, 최소 realization, 숨은 내부 모드의 관계를 설명한다.

### H03. 제어가능성의 계산과 해석

- controllability matrix와 PBH test를 계산하고 stabilizability와 구분한다.

### H04. 관측가능성의 계산과 해석

- observability matrix와 PBH test를 계산하고 detectability와 구분한다.

### H05. 극점배치 설계

- 목표 사양을 폐루프 극점으로 변환하고 `A-BK`를 검증한다.

### H06. Observer 설계

- `e_dot=(A-LC)e`를 유도하고 observer 속도와 잡음 trade-off를 설명한다.

### H07. 추종 성능 설계

- 상태피드백만으로 정상상태 오차가 보장되지 않음을 설명하고 prefilter 또는 적분 확대를 적용한다.

### H08. 현장 설계 판단

- 포화, control effort, sampling, scaling, 모델 오차, sensor noise와 검증 절차를 연결한다.

## 11. Common Missing Point 계약

1. 상태·입력·출력 및 행렬 차원을 누락함.
2. 전달함수 관계에서 영 초기조건을 누락함.
3. 최소 realization 조건을 누락함.
4. controllability matrix의 rank만 쓰고 물리적 의미를 설명하지 않음.
5. observability matrix의 rank만 쓰고 상태 복원 의미를 설명하지 않음.
6. stabilizability와 controllability를 구분하지 않음.
7. detectability와 observability를 구분하지 않음.
8. `A-BK` 부호 규약을 누락함.
9. 제어 불가능 모드의 극점은 이동하지 않는다는 점을 누락함.
10. observer error dynamics를 누락함.
11. observer pole을 무조건 매우 빠르게 배치함.
12. separation principle의 적용 조건을 누락함.
13. 정상상태 오차 보상 방법을 누락함.
14. actuator saturation과 control effort를 누락함.
15. sensor noise와 observer peaking을 누락함.
16. sampling과 계산지연을 누락함.
17. state scaling과 numerical conditioning을 누락함.
18. simulation 및 현장 단계 적용을 누락함.

## 12. Routing Alias 계약

다음 alias를 routing에 사용한다.

- 상태공간
- 상태 공간
- state space
- state-space
- 상태방정식
- state equation
- A B C D matrix
- 제어가능성
- controllability
- 가제어성
- 관측가능성
- observability
- 가관측성
- stabilizability
- 안정화가능성
- detectability
- 검출가능성
- PBH test
- Hautus test
- 제어가능성 행렬
- controllability matrix
- 관측가능성 행렬
- observability matrix
- 상태피드백
- state feedback
- 극점배치
- pole placement
- pole assignment
- Ackermann
- 아커만
- Luenberger observer
- 상태관측기
- state observer
- state estimator
- observer gain
- separation principle
- 분리원리
- minimal realization
- 최소 realization
- Kalman decomposition
- 적분 확대
- integral augmentation
- reference prefilter

## 13. Routing Field Point 계약

1. `x_dot=Ax+Bu`
2. `y=Cx+Du`
3. `G(s)=C(sI-A)^(-1)B+D`
4. controllability matrix의 rank를 계산한다.
5. observability matrix의 rank를 계산한다.
6. PBH test로 고유모드별 제어·관측 가능성을 확인한다.
7. stabilizability와 detectability를 구분한다.
8. `A-BK`의 목표 고유값을 확인한다.
9. Ackermann 또는 수치 pole placement를 적용한다.
10. `A-LC`의 observer pole을 확인한다.
11. controller pole과 observer pole을 독립적으로 설계한다.
12. prefilter 또는 integral augmentation으로 추종 오차를 개선한다.
13. actuator saturation과 control effort를 확인한다.
14. observer noise와 peaking을 확인한다.
15. sampling period와 계산지연을 확인한다.
16. state scaling과 condition number를 확인한다.
17. 모델 오차와 운전점 변화를 검증한다.
18. simulation, HIL 및 단계적 현장 적용을 수행한다.

## 14. Candidate Key Term 계약

Candidate key term은 최소 다음 항목을 포함한다.

1. state space
2. 상태공간
3. state equation
4. 상태방정식
5. controllability
6. 제어가능성
7. controllability matrix
8. observability
9. 관측가능성
10. observability matrix
11. PBH
12. Hautus
13. stabilizability
14. detectability
15. state feedback
16. 상태피드백
17. pole placement
18. 극점배치
19. Ackermann
20. Luenberger observer
21. state observer
22. observer gain
23. separation principle
24. minimal realization
25. Kalman decomposition
26. reference prefilter
27. integral augmentation
28. actuator saturation
29. observer peaking
30. numerical conditioning
31. state scaling
32. sampling period
33. model uncertainty
34. control effort

Candidate extraction은 LLM-only로 수행하며 deterministic candidate rule은 사용하지 않는다.

## 15. Source Policy 계약

- source mode: `LLM_ONLY`
- deterministic check: disabled
- deterministic fatal rule: empty
- deterministic major rule: empty
- candidate extraction rules: empty
- LLM truth schema: 14개
- LLM fatal condition: 8개
- 각 판단은 단순 keyword 존재 여부가 아니라 문장의 의미와 부호·조건·한계를 평가한다.
- 표현이 다르더라도 수학적으로 동등하면 인정한다.
- 모호하거나 상충되는 답안은 낮은 confidence 또는 warning으로 처리한다.
- LLM 호출 실패는 확정 fatal로 처리하지 않고 안전한 diagnostic warning으로 처리한다.

## 16. 다른 Topic Pack과의 경계

### 전달함수·상태공간 비교 Topic과의 경계

기존 `transfer_function_state_space`는 두 표현의 비교와 선정이 중심이다.

이번 Topic Pack은 다음 설계 내용을 중심으로 한다.

- controllability
- observability
- stabilizability
- detectability
- state feedback
- pole placement
- observer
- separation principle
- reference tracking

### 근궤적 Topic과의 경계

근궤적은 scalar gain 변화에 따른 폐루프 극점 궤적을 해석한다.

이번 Topic Pack은 full-state feedback gain K로 폐루프 고유값을 직접 배치하는 현대제어 설계가 중심이다.

### Bode·Nyquist Topic과의 경계

Bode·Nyquist는 주파수응답과 안정여유가 중심이다.

이번 Topic Pack은 상태변수, 내부 모드, rank, eigenstructure 및 observer 설계가 중심이다.

### 정상상태 오차·prefilter Topic과의 경계

기존 기준입력 추종 Topic과 내용이 연결되지만 이번 Topic Pack에서는 다음 관점으로 제한한다.

- state feedback에서 reference gain의 필요성
- integral state augmentation
- 확대 시스템 controllability
- observer 기반 servo 구현

## 17. 최종 완료 조건

Source Topic Pack은 다음 조건을 모두 만족해야 한다.

1. 요구사항 Markdown이 존재한다.
2. source JSON 4개와 README가 존재한다.
3. Fact Anchor가 정확히 14개이다.
4. Fatal Misconception이 정확히 8개이다.
5. LLM truth schema가 정확히 14개이다.
6. LLM fatal condition이 정확히 8개이다.
7. recommended outline이 정확히 8개이다.
8. high-band unlock condition이 정확히 8개이다.
9. question pattern이 최소 8개이다.
10. candidate key term이 최소 25개이다.
11. deterministic checks가 비활성이다.
12. deterministic rule 배열이 비어 있다.
13. candidate extraction rule 배열이 비어 있다.
14. `CALC_DESIGN`으로 지정한다.
15. `THEORY_CORE`로 지정한다.
16. `CORE_MUST_PREPARE`로 지정한다.
17. source validator가 통과한다.
18. quality validator의 error와 warning이 모두 0이다.
19. generated Rubric Bank 6개에 정확히 반영된다.
20. routing smoke에서 primary topic으로 선택된다.
21. LLM semantic review가 통과한다.
22. release validation이 통과한다.
23. Rubric Audit의 MAJOR와 priority MINOR가 0이다.
24. 최종 commit에는 예상한 source·sheet·generated 파일만 포함한다.
