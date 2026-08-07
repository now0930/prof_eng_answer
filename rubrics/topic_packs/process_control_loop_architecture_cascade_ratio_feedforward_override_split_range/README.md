# 공정제어 Loop Architecture: Cascade·Ratio·Feedforward·Override·Split-Range

## Topic ID

`process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`

## 분류

- Question Type: `COMPARE_SELECTION`
- Difficulty: `THEORY_CORE`
- Selection importance: `CORE_MUST_PREPARE`
- Official criteria: `IC-2027-W-3-1`, `IC-2027-W-3-4`
- Roadmap: TIER 1 / Priority 1

## 평가 목적

이 Topic은 단일 feedback loop를 기준으로 공정에서 사용하는 classical multi-loop architecture를
구조·적용조건·선정·현장 구현까지 연결하여 평가한다.

핵심 구조는 다음과 같다.

1. Single loop
2. Cascade
3. Ratio
4. Feedforward
5. Feedforward + Feedback
6. Override / Selective
7. Split-range

## 핵심 원칙

- Cascade: `Primary CO → Secondary SP`, secondary가 final element를 조작한다.
- Cascade는 secondary loop가 충분히 빠르고 주요 disturbance를 먼저 감지할 때 효과가 크다.
- Ratio는 wild stream과 controlled stream의 비를 유지하며 ratio convention을 명시한다.
- Feedforward는 measured disturbance를 PV 변화 전에 보상하며 model과 realizability 조건이 필요하다.
- Feedforward와 feedback은 선행보상과 잔여오차 보정으로 상호보완한다.
- Override는 selector로 constraint를 보호하며 non-selected controller tracking이 중요하다.
- Split-range는 one-controller/multiple-final-element 구조이며 transition을 설계·검증한다.
- 복합구조는 성능뿐 아니라 sensor, maintenance, fail action, legacy DCS/PLC와 비용을 함께 평가한다.

## 기존 Topic과의 경계

- PID gain tuning: `pid_controller_tuning_sequence_gain_effects`
- Feedback 전달함수·S/T·정상상태 오차: `feedback_system_closed_loop_sensitivity_steady_state_error`
- State-space/LQR: 관련 state-space Topic
- Valve authority/rangeability/installed gain: `control_valve_authority_rangeability_gain_installed_performance`
- Valve inherent/installed characteristic: `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`

이 Topic은 이론을 다시 전개하기보다 **공정제어 구조를 어떻게 선택하고 구현하는가**를 직접 소유한다.

## 기술사 답안 권장 전개

1. 배경과 기본 process loop
2. Cascade
3. Ratio
4. Feedforward + Feedback
5. Override / Selective
6. Split-range
7. 구조 비교와 선정
8. 현장 문제점과 개선
9. FAT/SAT/commissioning 검증
10. 비용·legacy 적용성 결론

## 현장 적용 고려사항

- signal scaling
- controller action
- remote/local 및 manual/auto mode
- output tracking
- anti-windup
- actuator saturation
- sensor failure
- fail action
- startup/shutdown
- selector direction
- split transition
- DCS/PLC function block
- 추가 계기와 engineering cost
- simulation, FAT, SAT, commissioning

## Source validation

`python3 scripts/rubric_manager.py validate-topic-packs`

## 상태

- [x] Requirements/Topic Sheet 작성
- [x] README 작성
- [x] Model Answer source 작성
- [x] Fact Anchor source 작성
- [x] Logic Check source 작성
- [x] Topic Importance source 작성
- [ ] focused validation
- [ ] generated bank rebuild
- [ ] release validation
- [ ] commit
- [ ] push
