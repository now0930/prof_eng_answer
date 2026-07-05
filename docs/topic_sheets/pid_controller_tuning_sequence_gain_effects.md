# PID 제어기 튜닝 순서와 P/I/D 게인 영향 Topic Sheet

## 1. Topic metadata

- topic_id: pid_controller_tuning_sequence_gain_effects
- title_ko: PID 제어기 튜닝 순서와 P/I/D 게인 영향

## 2. Core correct facts

- PID 제어기는 비례(P), 적분(I), 미분(D) 동작의 조합으로 제어 출력을 생성함.
- P 동작은 현재 오차에 비례하여 응답 속도를 개선하나 과도하면 overshoot와 진동을 유발함.
- I 동작은 누적 오차를 보상하여 정상상태 오차를 제거하나 과도하면 windup과 hunting을 유발함.
- D 동작은 오차 변화율을 이용해 예측 및 감쇠 효과를 제공하나 노이즈에 민감함.
- 일반적인 현장 튜닝 순서는 P(기본 응답/안정성) → I(정상상태 오차 제거) → D(필요 시 감쇠/overshoot 저감) 순임.
- 현장 제어 루프에서는 actuator saturation, sensor noise, valve stiction, dead time 등을 고려해야 함.

## 3. Acceptable answer expressions

- P는 응답 속도를 높이나 과도하면 overshoot와 진동을 키운다.
- I는 정상상태 오차를 제거하지만 과도하면 windup과 hunting을 만든다.
- D는 damping을 증가시키지만 noise amplification 문제가 있다.
- 튜닝은 P로 안정한 기본 응답을 만들고 I로 offset을 제거한 뒤 D는 필요한 경우에만 추가한다.
- PI 제어는 공정 제어에서 널리 사용된다.
- PD 제어기는 존재하며, 주로 damping과 빠른 응답이 필요한 계에서 사용할 수 있다.
- D 동작은 미분 kick과 노이즈 문제 때문에 필터와 함께 사용하거나 사용하지 않을 수 있다.
- I 동작에는 anti-windup이 필요할 수 있다.

## 4. Fatal wrong claims

#### id

pid_tuning_d_first_general_rule

#### claim

일반적인 PID 튜닝에서 D를 항상 먼저 조정해야 한다.

#### reason

D는 노이즈와 조작량 급변에 민감하여 첫 튜닝 대상이 아님.

#### id

integral_increases_damping

#### claim

I 동작이 damping을 증가시키거나 overshoot를 줄인다.

#### reason

I 동작은 정상상태 오차 제거가 목적이며 과도하면 진동을 증가시킴.

#### id

derivative_removes_steady_state_error

#### claim

D 동작이 정상상태 오차를 제거한다.

#### reason

정상상태 오차 제거는 I 동작의 역할임.

#### id

pd_controller_does_not_exist

#### claim

PD 제어기는 존재하지 않는다.

#### reason

PD 제어기는 존재하며 특정 응용 분야에서 사용됨.

#### id

p_gain_always_stabilizes

#### claim

P 게인을 키우면 항상 안정해진다.

#### reason

P 게인을 과도하게 키우면 불안정해질 수 있음.

#### id

integral_action_no_windup_risk

#### claim

I 동작에는 windup이나 포화 문제가 없다.

#### reason

Actuator saturation 상황에서 적분 windup은 필수 고려사항임.

## 5. Warn-level weak claims

- P/I/D의 역할만 나열하고 튜닝 순서를 언급하지 않음.
- 현장 제약 조건(noise, saturation, valve wear 등)에 대한 고려가 없음.
- D 동작의 노이즈 민감성이나 I 동작의 windup 위험을 누락함.
- Ziegler-Nichols 방법론만 제시하고 현장 재조정 판단을 누락함.

## 6. False positive cautions

- PI 제어만 사용하는 경우를 언급하는 것은 정상임.
- D 동작이 damping 효과를 가진다고 서술하는 것은 정상임.
- I 동작이 offset 제거에 효과적이라고 서술하는 것은 정상임.
- anti-windup의 필요성을 언급하는 것은 정상임.

## 7. Regex candidate patterns

- D.*먼저.*튜닝
- I.*damping.*증가
- D.*정상상태.*오차.*제거
- PD.*존재하지.*않는다
- P.*게인.*키우면.*항상.*안정

## 8. fact_anchor.json generation guidance

PID 수식, P/I/D 각 항의 역할, 일반적인 튜닝 순서(P-I-D)를 핵심 앵커로 설정.

## 9. logic_check.json generation guidance

D가 먼저 튜닝되는지, I가 damping을 증가시킨다고 하는지, D가 offset을 제거한다고 하는지 여부를 체크.

## 10. model_answer.json generation guidance

PID 수식 정의, 각 게인별 응답 영향, P-I-D 튜닝 순서, 현장 제약사항(windup, noise, saturation)을 포함한 모범 답안 구성.

## 11. topic_importance.json generation guidance

산업계측제어기술사로서 현장 튜닝의 실무적 이해도를 평가하므로 중요도 상(High)으로 설정.

## 12. Human review checklist

- P, I, D 역할이 뒤바뀌지 않았는가?
- I가 damping 증가 수단으로 잘못 설명되지 않았는가?
- D가 정상상태 오차 제거 수단으로 잘못 설명되지 않았는가?
- 일반적 튜닝 순서가 P 또는 PI 기반 안정화 후 I/D 보정으로 설명되었는가?
- 현장 문제(windup, noise, saturation)가 포함되었는가?
