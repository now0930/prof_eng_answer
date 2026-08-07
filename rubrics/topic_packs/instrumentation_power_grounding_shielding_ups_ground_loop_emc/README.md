# 계장 전원·접지·차폐·UPS·Ground Loop·EMC 진단 및 대책

## Topic ID

`instrumentation_power_grounding_shielding_ups_ground_loop_emc`

## Criterion

`IC-2027-W-2-6`

## Question type

Primary: `DIAGNOSIS_ACTION`

Supported secondary: `IMPLEMENTATION_EVALUATION`

Supported tertiary: `PRINCIPLE_INTERPRETATION`

## Difficulty

`FIELD_APPLICATION`

## 핵심 범위

- Instrumentation power integrity와 power-quality symptom
- Protective earth와 signal/reference ground의 기능 구분
- Equipotential bonding과 frequency-dependent impedance
- Single-point / multi-point grounding 적용 조건
- Ground-loop mechanism과 safe mitigation
- Common-mode / differential-mode noise
- Cable shield 역할과 one-end / both-end / 360-degree termination 조건
- Conducted / radiated / capacitive / inductive / common-impedance coupling
- Source → path → victim EMC diagnosis
- EMI filter·bonding·SPD coordination
- DC power distribution과 redundant supply common point
- UPS ride-through, sizing, battery aging, bypass와 neutral/ground reference
- Before/after evidence와 one-change-at-a-time field diagnosis
- 대책 후 normal / transient / UPS transfer / noise-source 조건 재검증

## 핵심 답안 흐름

`전원·기준전위 → 접지·본딩 → 차폐·coupling path → ground-loop/EMI evidence → UPS·EMC 대책 → 현장 재검증`

## 중요한 안전 경계

- Noise 저감을 이유로 보호접지(PE)를 임의 해제하지 않는다.
- Cable shield를 PE 또는 정상 부하전류 귀로로 사용하지 않는다.
- Single-point grounding을 모든 주파수의 절대 규칙으로 사용하지 않는다.
- 모든 shield를 무조건 한쪽 끝 접지한다고 일반화하지 않는다.
- UPS를 모든 EMC·surge·ground-loop 문제의 만능 해법으로 취급하지 않는다.

## Lane A ownership 경계

- Topic 2 `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
  - cable tray, gland, terminal, impulse tubing, 설치 검사, code/technical-standard 상세 적용
- Topic 3 `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`
  - EMC emission/immunity qualification test, severity, temperature/humidity/vibration qualification
- Topic 4 `control_hardware_lifecycle_panel_architecture_component_selection_production_verification`
  - panel architecture, component selection, HW lifecycle, prototype/production verification
- Topic 5 `electronics_error_noise_drift_tolerance_aging_power_mitigation`
  - electronic component-level noise/drift/tolerance/aging/power error chain

Topic 1은 위 범위를 침범하지 않고 **전원·접지·본딩·차폐·ground loop·UPS·설치 레벨 EMC 진단/대책**을 소유한다.

## Logic Check 정책

- Fact Anchor: 29
- Fatal misconception: 9
- Primary Question Type: `DIAGNOSIS_ACTION`
- Difficulty: `FIELD_APPLICATION`
- Deterministic direct checks: disabled
- Direct score application: disabled
- Direct D/E effect: none

## Historical frequency

Historical frequency는 근거가 없으므로 사용하지 않는다.

## Source

- `docs/topic_sheets/instrumentation_power_grounding_shielding_ups_ground_loop_emc.md`
- Repository exam-scope criterion `IC-2027-W-2-6`
- Instrumentation power, grounding, bonding, shielding, ground-loop, UPS and EMC engineering fundamentals

Source JSON authored by ChatGPT. Generated-bank build, classification registration, release registration and focused regression are separate stages.
