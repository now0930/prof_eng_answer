# TIER 1 Topic 1 요구사항 — 공정제어 Loop Architecture: Cascade·Ratio·Feedforward·Override·Split-Range

## 1. Topic 계약

- Topic ID: `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range`
- Primary Question Type: `COMPARE_SELECTION`
- Difficulty: `THEORY_CORE`
- Selection importance: `CORE_MUST_PREPARE`
- Official criteria:
  - `IC-2027-W-3-1` 유체제어의 기본요소와 설계요소
  - `IC-2027-W-3-4` 단일루프 및 다중루프 제어설계
- Coverage before: `PARTIAL + PARTIAL`
- Roadmap: `TIER 1 / Priority 1`
- Historical frequency: 정량 점수 사용 금지

## 2. 작성 목적

현재 Topic Pack은 PID, feedback theory, state-space, control-valve 성능은 강하지만
공정 현장에서 사용하는 classical loop architecture를 하나의 설계 흐름으로 평가하지 못한다.

이 Topic은 단일루프를 기준으로 다음 다중루프·복합구조를 설명하고 선정할 수 있는지를 평가한다.

1. Cascade
2. Ratio
3. Feedforward
4. Feedforward + Feedback
5. Override / Selective
6. Split-range

핵심은 구조 이름 나열이 아니라 **왜 그 구조를 쓰는지, 신호가 어떻게 연결되는지,
어떤 조건에서 효과가 있고, 어떤 현장 문제를 일으키는지**를 논리적으로 설명하는 것이다.

## 3. Ownership 경계

### 이 Topic의 직접 ownership

- process variable(PV), setpoint(SP), controller output(CO), manipulated variable(MV)의 loop chain
- single-loop process-control architecture
- primary/secondary cascade structure
- ratio station과 wild/controlled stream
- measured-disturbance feedforward
- feedforward + feedback trim
- override/selective selector structure
- split-range mapping과 transition
- architecture selection
- multi-loop interaction의 classical field-level 판단
- DCS/PLC 구현, fail action, mode transfer, commissioning 검증

### 기존 Topic ownership 유지

- PID P/I/D gain 영향과 tuning 순서:
  `pid_controller_tuning_sequence_gain_effects`
- generic closed-loop transfer, sensitivity S/T, steady-state error:
  `feedback_system_closed_loop_sensitivity_steady_state_error`
- state-space controllability/observability/pole placement:
  `state_space_controllability_observability_pole_placement`
- LQR와 Riccati:
  `lqr_optimal_state_feedback_riccati_weighting_design`
- state-feedback reference tracking/integral augmentation:
  `state_feedback_reference_tracking_prefilter_integral_action`
- valve authority/rangeability/installed gain:
  `control_valve_authority_rangeability_gain_installed_performance`
- inherent/installed valve characteristic:
  `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`

## 4. 핵심 Fact

### 4.1 기본 단일루프

기본 공정제어 루프는 다음 signal chain으로 설명한다.

`Process → Sensor/Transmitter → PV → Controller → CO → Final Control Element → MV → Process`

제어기는 `SP - PV` 관계에 따라 CO를 만들고 final control element가 MV를 변화시킨다.
단일루프는 단순하고 유지보수가 쉽지만 disturbance가 PV에 나타난 뒤 보정하는 feedback 구조가 기본이다.

### 4.2 Cascade

일반 cascade의 핵심 연결은 다음이다.

`Primary Controller CO → Secondary Controller SP`

Secondary controller가 final control element를 직접 조작한다.

효과적인 cascade의 핵심조건:

- secondary loop가 primary loop보다 충분히 빠를 것
- secondary PV가 조작경로의 주요 disturbance를 primary PV보다 먼저 감지할 수 있을 것
- secondary measurement가 신뢰 가능할 것
- inner-loop saturation과 mode transfer가 적절히 처리될 것

특정 3배, 5배와 같은 속도비를 모든 공정의 절대법칙으로 고정하지 않는다.

### 4.3 Ratio

Ratio control은 wild/master stream과 controlled stream의 관계를 유지한다.

Ratio 정의를 `R = F_c/F_w`로 두면 대표적으로:

`SP_c = R · F_w`

가 된다.

반대 convention도 가능하므로 답안은 ratio 정의를 먼저 명시해야 한다.

현장에서는 다음을 검토한다.

- engineering unit와 scaling
- mass/volume basis
- density compensation 필요 여부
- wild flow가 0에 가까운 영역
- startup/shutdown 시 ratio hold 또는 mode change
- flow transmitter range와 noise

### 4.4 Feedforward

Feedforward는 **측정 가능한 disturbance를 PV가 변하기 전에 보상**한다.

선형 모델이

`y = G_u(s)u + G_d(s)d`

라면 이상적인 cancellation은 조건이 허용될 때

`G_ff(s) = -G_d(s)/G_u(s)`

로 표현할 수 있다.

그러나 실제 구현에서는 다음을 확인한다.

- disturbance가 측정 가능한가
- process model이 충분히 정확한가
- inverse가 causal/proper/stable하게 구현 가능한가
- sensor noise와 delay가 과도하지 않은가

따라서 실제 공정에서는 feedforward와 feedback을 결합해
feedforward가 선행보상하고 feedback이 model mismatch와 미측정 disturbance의 잔여오차를 보정하는 구조가 유리하다.

### 4.5 Override / Selective

Override는 정상 제어목표와 constraint 보호목표를 가진 복수 controller signal에서
high/low selector 등을 이용해 **현재 더 제한적인 제어명령을 선택**한다.

High/low selector는 절대적으로 정해지는 것이 아니다.
controller action, signal direction, final-element fail action과 보호하려는 constraint에 따라 결정한다.

비선택 controller에는 다음이 필요할 수 있다.

- external reset feedback
- output tracking
- anti-windup
- bumpless transfer

그렇지 않으면 selector 전환 시 bump와 integral windup이 발생할 수 있다.

### 4.6 Split-range

Split-range는 **하나의 controller output을 둘 이상의 final control element에 분할**한다.

예:

- heating valve + cooling valve
- makeup valve + vent valve
- small valve + large valve

`0~50% / 50~100%`는 단순 예이다.
실제 split point와 overlap/deadband는 process requirement와 installed response로 결정한다.

주요 문제:

- transition deadband
- excessive overlap
- combined installed gain 불연속
- hunting
- fail-action conflict
- valve characteristic mismatch

따라서 transition 구간을 trend와 step test로 검증한다.

## 5. 구조 비교·선정 기준

| 공정 요구 | 우선 검토 구조 | 핵심 조건 |
|---|---|---|
| 단순한 하나의 PV 제어 | Single loop | 구조 단순성, maintenance |
| 빠른 내부 disturbance 선행 억제 | Cascade | secondary loop가 충분히 빠름 |
| 두 물질/유량의 비 유지 | Ratio | 기준 stream 신뢰성, scaling |
| 측정 가능한 disturbance 선제 보상 | Feedforward | disturbance measurement와 model |
| 정상목표보다 constraint 보호가 우선 | Override | selector direction, tracking |
| 한 controller로 복수 final element 사용 | Split-range | transition과 combined response |

복합구조를 선택할수록 sensor, logic, tuning, testing과 maintenance 비용이 증가한다.
따라서 구조의 복잡성 자체가 성능의 우수성을 의미하지 않는다.

## 6. 현장 문제점과 개선방향

### 문제점

- cascade inner loop가 충분히 빠르지 않음
- ratio scaling 또는 low-flow division 문제
- feedforward model mismatch와 sensor delay
- selector 전환 시 windup/bump
- split-range transition hunting
- shared actuator saturation
- controller action/fail action 방향 오류
- sensor failure와 bad PV propagation
- startup/shutdown에서 정상 운전 logic을 그대로 사용
- 기존 DCS/PLC에서 필요한 function block 또는 tracking 기능 부족

### 개선

- simulation 또는 process model로 구조 필요성부터 검증
- additional sensor의 신뢰도와 유지보수성 검토
- mode tracking, anti-windup, bumpless transfer 적용
- low-flow, sensor bad, saturation, startup/shutdown exception logic 정의
- selector와 split-range transition을 FAT/SAT에서 별도 test
- minimum/normal/maximum operating point에서 trend 검증
- 기존 DCS/PLC 기능을 우선 활용하고 custom logic은 최소화
- 추가 transmitter/valve/engineering cost와 expected performance benefit 비교
- 변경 전 rollback과 기존 운전 mode 영향 검토

## 7. 기술사 답안 권장 흐름

1. 배경: 단일 feedback의 한계와 다중루프 필요성
2. 기본 loop: PV-SP-CO-MV
3. Cascade
4. Ratio
5. Feedforward + Feedback
6. Override
7. Split-range
8. 구조별 비교·선정기준
9. 현장 문제점
10. 구현·검증·비용·legacy 개선방안

## 8. Fatal 오개념

다음은 직접 반대 주장일 때 Fatal 후보이다.

- cascade secondary loop가 primary보다 느릴수록 좋다
- secondary CO가 primary SP가 되는 것이 일반 cascade라고 한다
- secondary 측정값만 추가하면 cascade는 항상 개선된다
- ratio가 두 독립 setpoint를 유지하는 구조라고 한다
- feedforward는 disturbance measurement/model 없이 모든 disturbance를 제거한다고 한다
- feedforward가 있으면 feedback은 항상 불필요하다고 한다
- override가 controller 출력을 평균한다고 한다
- override는 항상 high selector여야 한다고 한다
- split-range와 override가 동일하다고 한다
- split-range transition은 자동으로 항상 부드럽다고 한다
- 다중루프는 복잡할수록 항상 좋다고 한다

## 9. Source boundary

첨부된 Step 0 bundle은 기존 7개 Topic의 ownership 및 repository schema를 제공한다.
Cascade·Ratio·Override·Split-range의 세부 technical fact는 표준 공정제어 공학 지식으로 보완했다.
이번 단계에서는 historical frequency를 근거로 사용하지 않는다.

## 10. 완료조건

- Topic Sheet 작성
- README 작성
- `model_answer.json` 작성
- `fact_anchor.json` 작성
- `logic_check.json` 작성
- `topic_importance.json` 작성
- 모든 recommended outline `anchor_refs`가 실제 anchor에 존재
- JSON parse error 0
- source validator PASS
- generated rebuild는 후속 단계에서 수행
- commit/push는 후속 단계에서 수행
