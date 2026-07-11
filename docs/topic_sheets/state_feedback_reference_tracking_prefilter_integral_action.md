# 상태피드백 기준입력 추종·프리필터·적분보상 설계

## 1. Topic 기본정보

- Topic ID: `state_feedback_reference_tracking_prefilter_integral_action`
- 문제 유형: `CALC_DESIGN`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: `LLM_ONLY`
- 결정론적 검사: 비활성화
- 작성 기준일: 2026-07-11

## 2. 출제 범위

상태공간 모델에서 상태피드백으로 폐루프 극점을 배치한 뒤 기준입력을
추종하는 방법을 다룬다. 정상상태 프리필터와 적분상태 확대설계의
원리, 적용 조건과 차이를 설명한다.

관측기, 액추에이터 포화, anti-windup, 모델 불확실성, 측정노이즈와
이산 구현까지 포함하여 실제 제어기 설계 관점에서 검증한다.

## 3. 기본 가정과 기호

기본 연속시간 상태공간 모델은 다음과 같다.

    x_dot = A x + B u
    y     = C x + D u

단순 프리필터 공식과 기본 확대시스템은 특별한 언급이 없으면
SISO, `D=0`, 상수 기준입력과 안정한 폐루프를 가정한다.

- `x`: 상태벡터
- `u`: 제어입력
- `y`: 제어출력
- `r`: 기준입력
- `K`: 상태피드백 이득
- `N_r`: 정상상태 프리필터 이득
- `ξ`: 출력오차 적분상태
- `K_i`: 적분상태 이득
- `A_cl=A-BK`: 상태피드백 폐루프 행렬

## 4. Fact Anchor 요구사항

### A01 — `state_tracking_design_objective`

상태피드백 추종제어는 폐루프 안정화와 극점 배치뿐 아니라 기준입력
추종, 정상상태 오차, 외란 제거, 제어입력, 포화와 강인성을 함께
만족하도록 설계해야 한다.

필수 내용:

- 안정화와 기준입력 추종은 서로 다른 설계 요구조건이다.
- 과도응답과 정상상태 성능을 분리하여 평가한다.
- 모델 정확도, 포화와 측정노이즈를 포함한다.

### A02 — `state_tracking_feedback_law_closed_loop`

상태를 직접 측정할 수 있을 때 기본 상태피드백 제어법칙은 다음과
같이 표현할 수 있다.

    u = -K x + N_r r

이때 상태방정식은 다음과 같다.

    x_dot = (A-BK)x + B N_r r

필수 내용:

- 폐루프 동특성은 `A-BK`가 결정한다.
- `K`는 안정성과 과도응답을 조정한다.
- `N_r`은 기준입력의 정상상태 크기를 조정한다.
- `K`와 `N_r`의 역할을 혼동하지 않는다.

### A03 — `state_tracking_pole_placement_tracking_distinction`

가제어한 시스템에서 `K`를 이용해 `A-BK`의 극점을 배치할 수 있지만,
폐루프 극점 배치만으로 `y_ss=r` 또는 정상상태 오차 0이 자동으로
보장되지는 않는다.

필수 내용:

- 극점 배치는 내부 동특성과 안정성을 결정한다.
- 출력의 정상상태 크기는 `B`, `C`, `D`, `K`와 기준입력 경로에
  의존한다.
- 단위 피드백 전달함수와 상태피드백 구조를 동일하게 취급하지 않는다.

### A04 — `state_tracking_prefilter_steady_state_derivation`

SISO, `D=0`, 안정한 `A-BK`와 0이 아닌 폐루프 DC 이득을 가정하면
상수 기준입력의 정상상태에서 다음 관계가 성립한다.

    0 = (A-BK)x_ss + B N_r r
    x_ss = -(A-BK)^(-1) B N_r r
    y_ss = -C(A-BK)^(-1)B N_r r

따라서 `y_ss=r`을 만족하는 프리필터는 다음과 같다.

    N_r = -[C(A-BK)^(-1)B]^(-1)

필수 내용:

- 정상상태 방정식에서 공식을 유도한다.
- 역행렬과 스칼라 역수가 존재해야 한다.
- 부호는 제어법칙의 정의에 따라 달라질 수 있다.
- `D≠0` 또는 MIMO에서는 일반화된 정상상태 이득식을 사용한다.

### A05 — `state_tracking_prefilter_existence_model_dependence`

프리필터는 기준입력에 대한 feedforward 보상이다. 정확한 모델과
상수 기준입력에서는 정상상태 스케일 오차를 제거할 수 있지만,
모델 오차와 외란을 적분 피드백처럼 자동 제거하지는 않는다.

필수 내용:

- 폐루프 DC 이득이 0이면 유한한 `N_r`을 구할 수 없다.
- MIMO에서는 정상상태 이득행렬의 가역성 또는 적절한 의사역행렬과
  추종 가능성 검토가 필요하다.
- plant 파라미터가 변하면 계산한 `N_r`의 정확도가 저하된다.
- 프리필터는 폐루프 극점을 변경하지 않는다.

### A06 — `state_tracking_integral_internal_model_principle`

상수 기준입력과 상수 외란에 대해 강인한 정상상태 오차 제거가
필요하면 출력오차의 적분상태를 추가할 수 있다.

    ξ_dot = r - y
    u     = -K_x x + K_i ξ

필수 내용:

- 적분기는 상수 신호의 내부모델을 제어기에 포함한다.
- 폐루프가 안정하고 포화가 지속되지 않는 조건이 필요하다.
- 적분동작은 프리필터와 달리 피드백 오차를 누적한다.
- 임의 주파수 외란이나 모든 모델오차를 제거하는 것은 아니다.

### A07 — `state_tracking_augmented_system_formulation`

`D=0`에서 적분상태를 포함한 확대시스템은 다음과 같이 구성할 수
있다.

    [x_dot] = [ A   0 ][x] + [B]u + [0]r
    [ξ_dot]   [-C   0 ][ξ]   [0]    [I]

확대상태를 `x_a=[x^T ξ^T]^T`로 정의하고 확대시스템의 상태피드백
이득을 설계한다.

필수 내용:

- 확대 행렬의 차원을 정확히 정의한다.
- `u=-K_xx+K_iξ`의 부호 규약과 폐루프 행렬을 일관되게 사용한다.
- 적분극을 포함한 전체 폐루프 극점을 배치하거나 최적화한다.
- `D≠0`이면 적분상태 식과 확대행렬을 다시 구성한다.

### A08 — `state_tracking_augmented_controllability_stabilizability`

원래 시스템이 가제어하더라도 적분상태를 추가한 확대시스템이
자동으로 가제어하는 것은 아니다. 임의 극점 배치에는 확대시스템의
가제어성이 필요하며, 안정화 목적에는 최소한 안정화 가능성을
확인해야 한다.

상수 출력조절 가능성은 다음과 같은 원점 rank 조건과 관련된다.

    rank([ A  B ]) = n + p
         ([ C  0 ])

필수 내용:

- 원점에 불변영점이 있으면 적분 출력조절이 불가능할 수 있다.
- 추종할 출력 수와 입력 수의 관계를 확인한다.
- 확대시스템의 controllability rank 또는 stabilizability를 검증한다.
- 원래 시스템의 가제어성과 확대시스템의 가제어성을 구분한다.

### A09 — `state_tracking_prefilter_integral_role_separation`

프리필터와 적분기는 모두 정상상태 추종을 개선하지만 역할과 특성이
다르다.

필수 내용:

- 프리필터는 모델 기반 feedforward 스케일 보상이다.
- 적분기는 출력오차 기반 feedback 보상이다.
- 프리필터는 빠른 명령응답과 적분기의 초기 부담 감소에 유리하다.
- 적분기는 모델 오차와 상수 외란에 더 강인하지만 위상지연과
  windup을 유발할 수 있다.
- 필요하면 두 방법을 함께 사용하고 전체 폐루프를 재검증한다.

### A10 — `state_tracking_disturbance_reference_performance`

기준입력 추종과 외란 제거는 입력 위치와 외란 모델에 따라 다르게
분석해야 한다.

필수 내용:

- 프리필터만으로 출력 또는 plant 입력에 가해지는 외란을 제거할 수
  없다.
- 적분기는 안정한 폐루프에서 상수 또는 내부모델에 포함된 외란을
  제거할 수 있다.
- 입력채널에 들어오는 matched disturbance와 다른 경로의 외란을
  구분한다.
- 기준입력 응답, 부하외란 응답과 측정노이즈 응답을 각각 평가한다.

### A11 — `state_tracking_observer_separation_principle`

모든 상태를 측정할 수 없으면 관측기 상태 `x_hat`을 사용한다.

    u = -K x_hat + N_r r

또는 적분상태와 결합하여 observer-based servo controller를 구성한다.

필수 내용:

- 가관측성 또는 검출 가능성을 확인한다.
- 이상적인 선형 시불변 모델에서는 separation principle이 성립한다.
- 제어기 극점과 관측기 극점을 독립적으로 설계할 수 있다.
- 지나치게 빠른 관측기는 측정노이즈와 미모델 동특성을 증폭할 수 있다.
- 관측기 극점이 제어기 극점과 같아야 하는 것은 아니다.

### A12 — `state_tracking_saturation_anti_windup`

액추에이터 포화 상태에서 적분오차가 계속 누적되면 windup이 발생해
큰 오버슈트와 느린 회복을 유발할 수 있다.

필수 내용:

- 실제 입력 제한을 명시한다.
- conditional integration, clamping 또는 back-calculation과 같은
  anti-windup 방법을 설명한다.
- 포화 중 적분상태의 동작을 검증한다.
- 선형 폐루프 극점만으로 포화 응답을 보장할 수 없음을 설명한다.

### A13 — `state_tracking_robustness_noise_gain_tradeoff`

큰 적분이득이나 지나치게 빠른 극점은 정상상태 오차와 응답속도를
개선할 수 있지만 제어입력 증가, 포화, 진동, 노이즈 증폭과 강인성
저하를 유발할 수 있다.

필수 내용:

- 성능과 제어입력의 상충관계를 평가한다.
- 모델 불확실성과 시간지연을 고려한다.
- sensitivity와 complementary sensitivity의 관점에서 검증한다.
- 적분기와 관측기 설계가 서로 결합된 실제 응답을 확인한다.

### A14 — `state_tracking_implementation_validation`

최종 제어기는 다음 항목을 종합 검증해야 한다.

필수 내용:

- 폐루프 및 확대시스템 극점
- 가제어성, 안정화 가능성, 가관측성 또는 검출 가능성
- 기준입력 추종오차와 과도응답
- 상수 외란 및 모델오차 응답
- 제어입력 크기와 액추에이터 포화
- anti-windup 성능
- 측정노이즈와 관측오차
- sensitivity와 complementary sensitivity
- 샘플링주기, 이산화와 계산지연
- 파라미터 불확실성에 대한 강인성

## 5. Fatal Wrong Claim 요구사항

### F01 — `state_tracking_fatal_pole_placement_guarantees_zero_error`

잘못된 주장:

상태피드백으로 원하는 폐루프 극점을 배치하면 기준입력의 정상상태
오차가 항상 0이 된다.

정확한 기준:

극점 배치는 폐루프 동특성을 결정하지만 출력의 정상상태 이득은
별도이다. 프리필터, 적분보상 또는 다른 서보 구조가 필요할 수 있다.

### F02 — `state_tracking_fatal_prefilter_rejects_disturbance`

잘못된 주장:

정상상태 프리필터를 적용하면 모델오차와 모든 외란도 자동으로
제거된다.

정확한 기준:

프리필터는 기준입력 feedforward 보상이다. 피드백 오차를 적분하지
않으므로 모델오차와 외란 제거를 일반적으로 보장하지 않는다.

### F03 — `state_tracking_fatal_nbar_always_one`

잘못된 주장:

단위 기준입력을 추종하므로 프리필터 이득 `N_r`은 항상 1이다.

정확한 기준:

`N_r`은 상태피드백이 적용된 폐루프의 DC 이득에 따라 결정된다.
특수한 경우를 제외하면 1로 고정되지 않는다.

### F04 — `state_tracking_fatal_integral_needs_no_augmented_check`

잘못된 주장:

원래 시스템이 가제어하면 적분상태를 추가한 시스템도 자동으로
가제어하므로 별도 검증이 필요 없다.

정확한 기준:

확대시스템의 가제어성 또는 안정화 가능성을 별도로 확인해야 한다.
원점 불변영점으로 인해 적분 출력조절이 불가능할 수도 있다.

### F05 — `state_tracking_fatal_integral_gain_unbounded_improvement`

잘못된 주장:

적분이득을 계속 높일수록 정상상태와 과도응답 성능이 모두 향상된다.

정확한 기준:

큰 적분이득은 진동, 낮은 안정여유, 큰 제어입력, 포화와 windup을
유발할 수 있으므로 전체 폐루프 성능을 검증해야 한다.

### F06 — `state_tracking_fatal_saturation_irrelevant`

잘못된 주장:

상태공간 폐루프 극점이 안정하면 액추에이터 포화는 추종성능과
무관하다.

정확한 기준:

포화는 선형 설계 가정을 깨뜨리고 적분 windup과 느린 복구를
유발한다. 입력 제한과 anti-windup을 포함해 검증해야 한다.

### F07 — `state_tracking_fatal_observer_poles_equal_controller`

잘못된 주장:

분리원리에 따라 관측기 극점은 상태피드백 제어기 극점과 반드시
동일하게 배치해야 한다.

정확한 기준:

이상적인 선형 모델에서 제어기와 관측기 극점은 독립적으로 설계할
수 있다. 관측기는 일반적으로 더 빠르게 설계하지만 노이즈와
미모델 동특성을 고려해야 한다.

### F08 — `state_tracking_fatal_uncontrollable_arbitrary_poles`

잘못된 주장:

가제어하지 않은 시스템도 상태피드백 이득을 선택하면 모든 폐루프
극점을 임의로 배치할 수 있다.

정확한 기준:

임의 극점 배치에는 가제어성이 필요하다. 안정화 목적이라면
불안정 모드가 가제어한 안정화 가능성을 최소 조건으로 확인한다.

## 6. 권장 답안 구조

### O01 — 설계 문제와 추종 요구조건

안정화, 과도응답, 정상상태 오차, 외란 제거와 실제 입력 제한을
구분하여 설계 목표를 정의한다.

참조 Anchor:

- `state_tracking_design_objective`
- `state_tracking_pole_placement_tracking_distinction`

### O02 — 상태피드백과 폐루프 극점

`u=-Kx+N_rr`과 `A-BK`를 제시하고 `K`가 폐루프 동특성을 결정하는
원리를 설명한다.

참조 Anchor:

- `state_tracking_feedback_law_closed_loop`

### O03 — 정상상태 프리필터 설계

정상상태 방정식에서 `N_r`을 유도하고 존재조건, 모델 의존성과
MIMO·`D≠0`에서의 한계를 설명한다.

참조 Anchor:

- `state_tracking_prefilter_steady_state_derivation`
- `state_tracking_prefilter_existence_model_dependence`

### O04 — 적분상태와 내부모델 원리

출력오차 적분상태를 추가하고 상수 기준입력과 상수 외란의
정상상태 오차를 제거하는 원리를 설명한다.

참조 Anchor:

- `state_tracking_integral_internal_model_principle`
- `state_tracking_augmented_system_formulation`

### O05 — 확대시스템 설계 가능성

확대시스템의 가제어성·안정화 가능성과 원점 불변영점 조건을
검증한다.

참조 Anchor:

- `state_tracking_augmented_controllability_stabilizability`

### O06 — 프리필터와 적분보상의 비교

feedforward와 feedback의 역할을 구분하고 기준입력 추종, 외란 제거와
결합사용 방법을 설명한다.

참조 Anchor:

- `state_tracking_prefilter_integral_role_separation`
- `state_tracking_disturbance_reference_performance`

### O07 — 관측기·포화·강인성

관측기 기반 구현, separation principle, anti-windup과 이득 증가에
따른 성능 상충관계를 설명한다.

참조 Anchor:

- `state_tracking_observer_separation_principle`
- `state_tracking_saturation_anti_windup`
- `state_tracking_robustness_noise_gain_tradeoff`

### O08 — 구현 및 최종 검증

연속·이산 폐루프에서 추종오차, 외란응답, 제어입력, 노이즈,
불확실성과 계산지연을 종합 검증한다.

참조 Anchor:

- `state_tracking_implementation_validation`

## 7. 고득점 해제조건

### H01 — 안정화와 추종의 구분

폐루프 극점 배치만으로 정상상태 오차 0이 보장되지 않는 이유를
설명한다.

### H02 — 프리필터 공식의 조건부 유도

SISO, `D=0`, 안정한 `A-BK`와 가역한 DC 이득 조건에서 `N_r`을
정상상태 방정식으로 유도한다.

### H03 — 프리필터의 역할과 한계

프리필터가 기준입력 feedforward 보상이며 모델오차와 외란 제거를
일반적으로 보장하지 않는다고 설명한다.

### H04 — 적분상태와 내부모델 원리

적분상태가 상수 기준입력과 상수 외란의 내부모델로 동작하는
조건을 설명한다.

### H05 — 확대시스템 검증

확대시스템의 가제어성 또는 안정화 가능성과 원점 불변영점 조건을
확인한다.

### H06 — 프리필터와 적분기의 역할 분리

빠른 명령응답, 모델 의존성, 외란 강인성, 위상지연과 windup을
기준으로 두 방법을 비교한다.

### H07 — 관측기와 비선형 제약

separation principle, 관측기 노이즈, 액추에이터 포화와 anti-windup을
설명한다.

### H08 — 종합 폐루프 검증

추종오차, 외란응답, 제어입력, sensitivity, 노이즈, 불확실성과
이산 구현을 종합 검증한다.

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
- 단순 공식 누락은 Fatal로 처리하지 않는다.
- 조건을 생략한 과도한 단정과 핵심 원리의 반대 주장을 구분한다.
- 공식의 부호는 정의한 제어법칙 및 적분상태 부호 규약과 함께 평가한다.
