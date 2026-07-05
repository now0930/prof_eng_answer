# PID 제어기 튜닝 순서와 P/I/D 게인 영향

## 1. Topic scope

이 topic은 PID 제어기에서 P, I, D 동작의 의미와 게인 변화가 폐루프 응답에 미치는 영향, 그리고 현장에서 튜닝 순서를 어떻게 잡는지를 평가한다.

대표 질문:

- PID 제어기의 P, I, D 동작과 튜닝 순서를 설명하시오.
- PID 튜닝 시 P, I, D 게인의 영향을 설명하시오.
- PID 제어기에서 I 게인과 D 게인 중 무엇을 먼저 조정해야 하는지 설명하시오.
- 현장 제어 루프에서 PID 튜닝 시 고려사항을 설명하시오.

## 2. Core correct facts

- PID 제어기는 비례(P), 적분(I), 미분(D) 동작을 조합하여 오차에 대한 제어 출력을 만든다.
- 이상적인 연속형 PID는 `u(t)=Kp e(t)+Ki∫e(t)dt+Kd de(t)/dt`로 표현할 수 있다.
- 또는 `Gc(s)=Kp + Ki/s + Kd s` 형태로 표현할 수 있다.
- P 동작은 현재 오차에 비례하여 제어 출력을 만들며 응답 속도를 빠르게 하지만 너무 크면 overshoot와 진동이 증가한다.
- I 동작은 누적 오차를 보상하여 정상상태 오차를 제거하지만 너무 크면 overshoot, 진동, 적분 포화, 응답 지연을 유발한다.
- D 동작은 오차 변화율을 이용해 예측·감쇠 효과를 주며 overshoot와 진동을 줄일 수 있지만 노이즈에 민감하다.
- 일반적인 현장 튜닝은 먼저 P로 기본 응답성과 안정성을 확보하고, 그 다음 I로 정상상태 오차를 제거하며, 마지막으로 D를 필요한 경우에만 감쇠·overshoot 저감 목적으로 추가한다.
- 따라서 일반적인 순서는 `P → I → D` 또는 PI 기반 안정화 후 D 보정이다.
- D를 먼저 크게 적용하면 계측 노이즈 증폭, 조작량 급변, 밸브 마모, actuator 부담이 커질 수 있다.
- I를 너무 일찍 또는 과도하게 적용하면 적분 windup과 hunting이 발생할 수 있다.
- 실제 공정에서는 D 동작을 쓰지 않는 PI 제어도 흔하다.
- PD 제어기는 존재하며 위치 제어, 서보, 기계계처럼 정상상태 오차보다 damping과 빠른 응답이 중요한 경우 사용될 수 있다.
- 다만 일반적인 process control에서는 load disturbance와 정상상태 오차 제거가 중요하므로 PI 또는 PID가 더 흔하다.
- 튜닝은 공정 특성, dead time, time constant, sensor noise, actuator saturation, valve stiction, 안전성, 운전 모드에 따라 달라진다.
- 현장에서는 manual/auto 전환, output limit, anti-windup, derivative filter, setpoint weighting, bumpless transfer를 함께 고려해야 한다.

## 3. Acceptable answer expressions

- P는 응답 속도를 높이나 과도하면 overshoot와 진동을 키운다.
- I는 정상상태 오차를 제거하지만 과도하면 windup과 hunting을 만든다.
- D는 damping을 증가시키지만 noise amplification 문제가 있다.
- 튜닝은 P로 안정한 기본 응답을 만들고 I로 offset을 제거한 뒤 D는 필요한 경우에만 추가한다.
- PI 제어는 공정 제어에서 널리 사용된다.
- PD 제어기는 존재하며, 주로 damping과 빠른 응답이 필요한 계에서 사용할 수 있다.
- D 동작은 미분 kick과 노이즈 문제 때문에 필터와 함께 사용하거나 사용하지 않을 수 있다.
- I 동작에는 anti-windup이 필요할 수 있다.
- 현장 튜닝은 overshoot, settling time, steady-state error, actuator saturation, noise, maintenance cost를 함께 고려한다.

## 4. Fatal wrong claims

### id: pid_tuning_d_first_general_rule

- wrong claim: 일반적인 PID 튜닝에서 D를 항상 먼저 조정해야 한다고 설명한다.
- why fatal: D는 노이즈와 조작량 급변에 민감하므로 일반적 첫 튜닝 대상이 아니며, 보통 P 또는 PI 기반 안정화 후 필요 시 보정한다.
- examples:
  - PID 튜닝은 D 게인을 먼저 잡아야 한다.
  - D를 먼저 크게 주면 안정해지므로 그 다음 P와 I를 조정한다.
- expected cap: 10.0

### id: integral_increases_damping

- wrong claim: I 동작이 damping을 증가시키거나 overshoot를 줄이는 주된 수단이라고 설명한다.
- why fatal: I 동작은 정상상태 오차 제거가 주목적이며, 과도하면 overshoot와 진동을 증가시킬 수 있다.
- examples:
  - I 게인을 키우면 damping ratio가 증가한다.
  - I 동작은 진동을 억제하고 overshoot를 줄인다.
- expected cap: 10.0

### id: derivative_removes_steady_state_error

- wrong claim: D 동작이 정상상태 오차를 제거한다고 설명한다.
- why fatal: 정상상태 오차 제거는 주로 I 동작의 역할이며, D는 변화율 기반 감쇠·예측 동작이다.
- examples:
  - D 제어는 offset을 제거한다.
  - 정상상태 오차를 없애려면 D 게인을 키운다.
- expected cap: 10.0

### id: pd_controller_does_not_exist

- wrong claim: PD 제어기는 존재하지 않는다고 설명한다.
- why fatal: PD 제어기는 존재하며, 정상상태 오차 제거보다 damping과 빠른 응답이 중요한 계에서 사용할 수 있다.
- examples:
  - PD 제어기는 없다.
  - PID에서 I가 없으면 제어기가 성립하지 않는다.
- expected cap: 10.0

### id: p_gain_always_stabilizes

- wrong claim: P 게인을 키우면 항상 안정해진다고 설명한다.
- why fatal: P 게인을 과도하게 키우면 overshoot, hunting, 불안정이 증가할 수 있다.
- examples:
  - Kp를 계속 키우면 안정도가 계속 좋아진다.
  - P 게인은 클수록 무조건 좋다.
- expected cap: 10.0

### id: integral_action_no_windup_risk

- wrong claim: I 동작에는 windup이나 포화 문제가 없다고 설명한다.
- why fatal: actuator saturation 상황에서 적분 windup은 PID 튜닝의 대표적인 현장 문제이다.
- examples:
  - I 제어는 누적되지만 포화 문제는 없다.
  - anti-windup은 PID 튜닝에서 필요 없다.
- expected cap: 10.0

## 5. Warn-level weak claims

- P/I/D의 역할은 설명했지만 튜닝 순서를 설명하지 않는다.
- 튜닝 순서는 설명했지만 현장 제약인 noise, saturation, valve wear, dead time을 언급하지 않는다.
- D 동작의 장점만 쓰고 노이즈 민감성을 설명하지 않는다.
- I 동작의 정상상태 오차 제거만 쓰고 windup을 설명하지 않는다.
- P 게인의 응답 속도 증가만 쓰고 overshoot/hunting 위험을 설명하지 않는다.
- Ziegler-Nichols 등 방법론을 언급했지만 적용 한계와 보수적 재조정을 설명하지 않는다.
- 기술사 답안인데 비용, 유지보수, 기존 설비 영향, 운전 안정성 판단이 없다.

## 6. False positive cautions

- “일반적으로 P → I → D 순서로 잡는다”는 정상이다.
- “현장에서는 PI만 사용하는 경우도 많다”는 정상이다.
- “PD 제어는 존재하지만 process control에서는 PI/PID가 더 흔하다”는 정상이다.
- “I를 먼저 고려할 수 있는 특수 상황이 있다”고 조건부로 설명하는 것은 fatal이 아니다.
- “D는 damping 효과가 있다”는 정상이다.
- “D는 노이즈에 민감해 필터와 함께 사용한다”는 정상이다.
- “P 게인이 너무 작으면 응답이 느리다”는 정상이다.
- “P 게인이 너무 크면 불안정해질 수 있다”는 정상이다.
- “I는 offset 제거에 효과적이다”는 정상이다.
- “anti-windup이 필요하다”는 정상이다.

## 7. Topic Sheet generation guidance

Topic Sheet는 다음을 포함해야 한다.

- PID 수식과 각 항의 의미
- P/I/D 게인 증가가 rise time, overshoot, settling time, steady-state error, stability에 미치는 영향
- 일반적인 튜닝 순서 `P → I → D`
- PI 제어와 PID 제어의 현장 차이
- PD 제어기의 존재와 적용 영역
- I windup, D noise amplification, derivative kick, actuator saturation
- field judgement: 안전성, 유지보수, 밸브 마모, 센서 노이즈, 공정 dead time, 기존 설비 적용성
- fatal rule은 단순 누락이 아니라 핵심 역할을 반대로 설명한 경우에만 적용
- LLM semantic verifier가 문맥으로 fatal claim을 판정할 수 있도록 wrong claim과 safe condition을 명확히 분리

## 8. Human review checklist

- P, I, D 역할이 서로 뒤바뀌지 않았는가?
- I가 damping 증가 수단으로 잘못 설명되지 않았는가?
- D가 정상상태 오차 제거 수단으로 잘못 설명되지 않았는가?
- 일반적 튜닝 순서가 P 또는 PI 기반 안정화 후 I/D 보정으로 설명되었는가?
- D를 무조건 먼저 조정해야 한다고 하지 않았는가?
- PD 제어기가 존재하지 않는다고 잘못 쓰지 않았는가?
- windup, noise, saturation, valve wear 등 현장 문제가 들어갔는가?
- 단순히 Ziegler-Nichols 공식을 암기한 수준이 아니라 현장 재조정 판단을 포함하는가?
