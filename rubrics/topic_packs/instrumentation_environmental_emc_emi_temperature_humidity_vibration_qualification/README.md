# 계측기 환경·EMC/EMI·온도·습도·진동 Qualification 및 검증

## Topic ID

`instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`

## Criterion

`IC-2027-W-3-10`

## Question type

Primary: `IMPLEMENTATION_EVALUATION`

Supported secondary: `DIAGNOSIS_ACTION`

Supported tertiary: `PRINCIPLE_INTERPRETATION`

## Difficulty

`FIELD_APPLICATION`

## 핵심 범위

- Qualification requirement traceability
- EMC와 EMI 개념 구분
- Emission과 immunity 구분
- Conducted / radiated / ESD / EFT / surge / RF 등 applicable EMC test category
- Representative DUT setup와 operating mode
- Pre-test functional baseline
- In-test output / reset / communication / recovery monitoring
- Predefined acceptance criteria
- Operating / storage temperature qualification
- Humidity failure mechanism과 condensation condition
- Sine / random vibration, axis, fixture / mounting
- Test instrument calibration / uncertainty
- Failure evidence / root cause / corrective action
- Re-test / requalification
- Qualification report / change traceability

## 핵심 답안 흐름

`Requirement → Test Plan/Setup → Stress Exposure → Functional Monitoring → Acceptance → Failure Analysis/Corrective Action → Re-test/Report`

## 중요한 경계

- EMC와 EMI는 같은 개념이 아니다.
- Emission과 immunity는 같은 시험이 아니다.
- 모든 계측기에 동일 severity·duration을 적용하지 않는다.
- 시험 종료 후 power-on만으로 qualification pass를 판단하지 않는다.
- Field EMI troubleshooting과 qualification을 동일 활동으로 보지 않는다.
- Specific standard edition/test level/dwell time은 적용 요구 근거 없이 고정하지 않는다.

## Ownership boundary

- `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
  - Plant EMI noise, ground loop, grounding/shielding/EMC mitigation 진단·대책
  - 본 Topic은 **defined qualification test와 evidence**를 소유
- `instrumentation_installation_wiring_impulse_tubing_inspection_codes`
  - Cable/gland/wiring/tubing field installation
  - 본 Topic은 **representative test setup condition**을 평가
- `control_hardware_lifecycle_panel_architecture_component_selection_production_verification`
  - HW architecture/component/lifecycle/production verification 전체
  - 본 Topic은 **환경·EMC qualification evidence**를 독립 소유
- `electronics_error_noise_drift_tolerance_aging_power_mitigation`
  - Component-level noise/drift/tolerance/aging/power error chain
  - 본 Topic은 **environmental stress qualification result**를 소유

## Logic Check 정책

- Fact Anchor: 32
- Fatal misconception: 10
- Primary Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- Deterministic direct checks: disabled
- Direct score application: disabled
- Direct D/E effect: none

## Standard policy

Specific standard edition, severity, dwell, sweep range, test level과 acceptance class는 적용 제품규격·프로젝트 specification·관할 요구에서 결정한다. 이 Topic Pack은 출처 없는 고정 수치를 사용하지 않는다.

## Historical frequency

Historical frequency는 근거가 없으므로 사용하지 않는다.

## Source

- `docs/topic_sheets/instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification.md`
- Repository exam-scope criterion `IC-2027-W-3-10`
- Instrumentation environmental and EMC qualification engineering fundamentals

Source JSON authored by ChatGPT. Focused regression, generated rebuild, classification/release registration and commit은 별도 단계이다.
