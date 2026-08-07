# 전자기기 오차·Noise·Drift·Tolerance·Aging·Power 영향 및 대책

## Topic ID

`electronics_error_noise_drift_tolerance_aging_power_mitigation`

## Criterion

`IC-2027-W-1-4`

## Question type

Primary: `PRINCIPLE_INTERPRETATION`

Supported secondary: `DIAGNOSIS_ACTION`

Supported tertiary: `IMPLEMENTATION_EVALUATION`

## Difficulty

`FIELD_APPLICATION`

## 핵심 범위

- Offset / bias error
- Gain error
- Linearity error
- Random noise / noise bandwidth / SNR
- Drift / temperature coefficient
- Component tolerance / propagation
- Aging / long-term stability
- Local supply/reference sensitivity / PSRR
- ADC quantization / resolution / accuracy
- Error budget / worst-case / RSS
- Filtering / calibration / compensation
- PCB/local electronics mitigation
- Diagnosis / residual verification

## 핵심 답안 흐름

`Source → Electronic path/sensitivity → Output error → Error budget → Cause-specific mitigation → Residual verification`

## 반드시 구분할 개념

- Random noise ≠ systematic offset/gain error
- Tolerance ≠ drift ≠ aging
- ADC resolution/quantization ≠ total accuracy
- Filtering ≠ deterministic offset/gain calibration
- Calibration ≠ permanent removal of random noise/future drift/aging
- PSRR nominal value ≠ all-frequency immunity

## Ownership boundary

- `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
  - Plant/panel power quality, grounding, shielding, ground loop, field EMC diagnosis
  - 본 Topic은 **local electronics supply/reference/PSRR와 PCB-level error contributor**
- `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`
  - 환경/EMC qualification 상세 test setup·stress·monitoring·evidence
  - 본 Topic은 **temperature drift/aging mechanism**
- `control_hardware_lifecycle_panel_architecture_component_selection_production_verification`
  - HW architecture/component selection governance/DV/manufacturing
  - 본 Topic은 **component/circuit error mechanism과 error budget**
- Sensor-specific Topics
  - 각 sensing principle과 sensor-specific compensation
  - 본 Topic은 **여러 sensor interface에 공통인 electronics error**
- Metrology/Calibration Topics
  - Accuracy, precision, uncertainty, traceability의 일반 정의
  - 본 Topic은 **circuit-level error contributor**

## Logic Check 정책

- Fact Anchor: 36
- Fatal misconception: 10
- Primary Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Deterministic direct checks: disabled
- Direct score application: disabled
- Direct D/E effect: none

## Fixed-number policy

PSRR, drift, tolerance, filter cutoff, calibration interval 등은 component/device, frequency, environment, requirement에 따라 달라진다. Source Pack은 근거 없는 universal fixed number를 사용하지 않는다.

## Historical frequency

Historical frequency는 근거가 없으므로 사용하지 않는다.

## Source

- `docs/topic_sheets/electronics_error_noise_drift_tolerance_aging_power_mitigation.md`
- Repository exam-scope criterion `IC-2027-W-1-4`
- Cross-cutting instrumentation electronics error fundamentals

Source JSON authored by ChatGPT. Focused regression, generated rebuild, classification/release registration and commit은 별도 단계이다.
