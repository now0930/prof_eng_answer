# 제어 Hardware Lifecycle·Panel Architecture·부품선정·생산검증

## Topic ID

`control_hardware_lifecycle_panel_architecture_component_selection_production_verification`

## Criterion

`IC-2027-W-3-9`

## Question type

Primary: `IMPLEMENTATION_EVALUATION`

Supported secondary: `COMPARE_SELECTION`

Supported tertiary: `DIAGNOSIS_ACTION`

## Difficulty

`DESIGN_EVALUATION`

## 핵심 범위

- Hardware requirement decomposition / traceability
- Panel/product hardware architecture와 interface
- Power budget / protection
- I/O / communication / isolation architecture
- Component selection / derating / lifecycle availability
- Thermal / physical layout / maintainability
- Design review / verification plan
- Prototype / design verification
- Verification vs validation
- DFM / DFA
- BOM / configuration baseline
- Incoming / manufacturing process control
- Production test coverage / EOL
- Test fixture / test software control
- Nonconformance / rework / retest
- Change impact / re-verification / release gate

## 핵심 답안 흐름

`Requirement → Architecture/Interface → Component Selection → Design Verification → Manufacturability/Production Control → Production Verification → Configuration/Release`

## 중요한 경계

- Prototype pass ≠ production readiness
- FAT pass ≠ complete hardware design verification
- FAT pass ≠ production verification
- Verification ≠ Validation
- Component selection ≠ nominal rating only
- Production test ≠ complete design verification repetition
- Component substitution은 uncontrolled change가 아니다.

## Ownership boundary

- `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
  - Grounding/shield/ground-loop/EMC 설계 메커니즘
  - 본 Topic은 해당 requirement를 **hardware architecture와 DV에 반영**
- `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
  - Field cable/gland/wiring/tubing installation
  - 본 Topic은 **panel/product internal hardware implementation 및 manufacturing**
- `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`
  - 온도·습도·진동·EMC qualification 상세 시험/evidence
  - 본 Topic은 qualification 결과를 **hardware release gate**에 연결
- `electronics_error_noise_drift_tolerance_aging_power_mitigation`
  - Component-level noise/drift/tolerance/aging/power error chain
  - 본 Topic은 requirement 수준의 tolerance/accuracy margin과 component selection을 소유
- `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`
  - Software lifecycle/V-model
  - 본 Topic은 processor/I/O/interface/panel **hardware lifecycle**
- `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`
  - Project FAT/SAT/commissioning acceptance
  - 본 Topic은 **hardware design verification와 production verification**

## Logic Check 정책

- Fact Anchor: 35
- Fatal misconception: 10
- Primary Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Deterministic direct checks: disabled
- Direct score application: disabled
- Direct D/E effect: none

## Fixed-number policy

Derating percentage, design margin, production-test limit와 standard edition은 component type, manufacturer data와 applicable project/product requirement에 따라 달라진다. Source Pack은 근거 없는 고정 수치를 사용하지 않는다.

## Historical frequency

Historical frequency는 근거가 없으므로 사용하지 않는다.

## Source

- `docs/topic_sheets/control_hardware_lifecycle_panel_architecture_component_selection_production_verification.md`
- Repository exam-scope criterion `IC-2027-W-3-9`
- Industrial control hardware lifecycle, architecture, component selection and production verification fundamentals

Source JSON authored by ChatGPT. Focused regression, generated rebuild, classification/release registration and commit은 별도 단계이다.
