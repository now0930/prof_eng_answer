# 전자기기 오차·Noise·Drift·Tolerance·Aging·Power 영향 및 대책

## 1. Topic identity

- Topic ID: `electronics_error_noise_drift_tolerance_aging_power_mitigation`
- Criterion: `IC-2027-W-1-4`
- Lane: `SOFTWARE_LLM_LANE_A`
- Primary Question Type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Historical frequency: 사용하지 않음

## 2. 출제 의도

이 Topic은 센서 하나의 오차를 설명하는 문제가 아니다.

다양한 계측전자에 공통인 전자오차를 다음 chain으로 설명해야 한다.

`Input signal → Interface/Amplifier/Filter → Reference/Power → ADC → Output`

각 단계에서 발생하는 error contributor를 분리한다.

`Offset/Gain/Linearity + Noise + Drift + Tolerance + Aging + Power/Reference + ADC`

그리고 원인에 맞는 mitigation을 적용한 뒤 residual error를 다시 검증한다.

## 3. Error Classification

전자오차는 최소 다음을 구분한다.

### Systematic error

반복 가능한 방향성을 갖는 오차.

예:

- Offset
- Gain error
- Linearity error
- Reference scale error

### Random error

순간값이 불규칙하게 변하는 확률적 성분.

대표적으로 noise가 있다.

### Drift

Temperature, time, supply, self-heating, operating condition 등의 변화에 따라 parameter가 변한다.

오차 종류를 모두 “noise”라고 표현하면 대책도 잘못 선택하게 된다.

## 4. Offset Error

Offset error는 zero 또는 기준 입력에서 일정한 출력 bias가 나타나는 성분이다.

주요 회로 원인:

- Amplifier input offset
- Bias current × source resistance
- Reference mismatch
- Leakage
- Unbalanced interface

Calibration 또는 auto-zero 구조로 보정할 수 있지만 원인과 장기 drift를 같이 봐야 한다.

## 5. Gain Error

Gain error는 이상적 transfer slope와 실제 slope의 차이다.

원인:

- Resistor ratio
- Amplifier gain accuracy
- Reference scale
- ADC full-scale path

Offset을 제거해도 gain error는 남을 수 있다.

## 6. Linearity Error

Linearity error는 offset과 gain을 제거한 뒤에도 transfer characteristic이 이상적인 관계에서 벗어나는 성분이다.

따라서 zero/span 두 점 calibration만으로 완전히 제거되지 않을 수 있다.

## 7. Random Noise

Random noise는 측정값의 순간 분산을 증가시킨다.

전자회로 noise source 예:

- Thermal noise
- Shot noise
- Amplifier input noise
- Reference noise
- Conversion noise
- External coupling

Noise는 amplitude만 볼 것이 아니라 measurement bandwidth와 함께 봐야 한다.

## 8. Noise Bandwidth

Noise spectral density가 존재하면 측정 bandwidth가 넓을수록 integrated noise가 커질 수 있다.

Bandwidth를 줄이면 noise는 감소할 수 있다.

그러나:

- Response time 증가
- Transient attenuation
- Phase delay

가 발생할 수 있다.

따라서 signal bandwidth를 먼저 정의한다.

## 9. SNR / Dynamic Range

SNR은 유효신호와 noise의 상대 크기를 본다.

Dynamic range는 큰 신호와 작은 신호를 모두 유효하게 다룰 수 있는 범위를 본다.

ADC bit 수만 높인다고 front-end noise floor가 자동으로 낮아지지 않는다.

## 10. Drift

Drift는 일정 component가 operating condition에 따라 변하는 현상이다.

원인 예:

- Temperature
- Self-heating
- Supply variation
- Humidity/contamination 영향
- Time
- Mechanical/thermal stress history

Offset drift와 gain drift를 구분할 수 있다.

## 11. Temperature Coefficient

Temperature coefficient는 온도 변화에 대한 parameter 민감도이다.

전체 회로에서는 다음이 누적될 수 있다.

- Resistor ratio tempco
- Reference tempco
- Amplifier offset drift
- Gain drift
- Sensor-interface network drift

따라서 component 하나의 tempco가 아니라 sensitivity와 error budget으로 본다.

## 12. Tolerance

Tolerance는 component nominal value의 제조 편차다.

예:

- Resistor value tolerance
- Reference initial accuracy
- Amplifier gain tolerance

Tolerance는 drift와 다르다.

`Tolerance = initial manufacturing spread`

`Drift = condition/time dependent change`

## 13. Tolerance Propagation

Component tolerance는 circuit sensitivity를 통해 output error로 변환된다.

방법:

- Worst-case analysis
- Statistical analysis
- Sensitivity analysis

목표는 모든 숫자를 나열하는 것이 아니라 dominant contributor를 찾는 것이다.

## 14. Aging

Aging은 장기 사용 또는 보관 중 parameter가 변하는 현상이다.

초기 tolerance와 다르다.

또한 단기 temperature drift와도 구분한다.

Aging은:

- Reference long-term stability
- Resistor long-term drift
- Capacitor change
- Contact/interface degradation

등을 통해 calibration stability를 악화시킬 수 있다.

## 15. Power Supply Variation

Local electronics의 supply 상태도 error source다.

- Supply variation
- Ripple
- Regulator noise
- Reference movement
- Excitation variation

이 disturbance가 amplifier/reference/ADC/sensor excitation을 통해 output으로 전달되는 sensitivity를 평가한다.

## 16. PSRR

PSRR은 supply disturbance가 circuit output 또는 input-referred error로 전달되는 정도를 나타낸다.

PSRR은 frequency와 operating condition에 따라 달라질 수 있다.

따라서 nominal 단일 수치가 모든 주파수의 supply disturbance 제거를 보장한다고 설명하면 안 된다.

## 17. Reference Error

Reference는 scale을 결정하는 핵심 component가 될 수 있다.

주요 error:

- Initial accuracy
- Temperature coefficient
- Noise
- Load sensitivity
- Aging

ADC reference 또는 bridge excitation과 연결되면 gain/scale error로 직접 전파될 수 있다.

## 18. ADC Quantization

ADC는 연속값을 유한 code로 변환한다.

Quantization은 discretization error다.

그러나 ADC total accuracy에는 다음도 포함된다.

- Offset
- Gain
- INL
- DNL
- Reference error
- Noise

따라서 quantization 또는 bit 수만으로 accuracy를 판단하지 않는다.

## 19. Resolution vs Accuracy

Resolution:

`얼마나 작은 code step을 구분할 수 있는가`

Accuracy:

`실제 변환값이 true value에 얼마나 가까운가`

고해상도 ADC가 반드시 고정확도 ADC는 아니다.

## 20. Sampling / Aliasing

Sampling system에서는 signal bandwidth에 적합한 sampling과 anti-alias filtering이 필요하다.

Aliasing은 대역 밖 신호가 잘못된 저주파 성분으로 보이는 현상이다.

이는 quantization noise와 다른 mechanism이다.

## 21. Filtering

Filter는 noise mitigation에 유효하다.

하지만 cutoff/order 선정에 따라:

- Noise reduction
- Response delay
- Phase distortion
- Transient loss

trade-off가 생긴다.

Filter는 deterministic offset/gain error를 자동 보정하지 않는다.

## 22. Calibration

Calibration은 traceable reference와 비교하여 반복 가능한 systematic error를 추정하고 보정한다.

주로:

- Offset
- Gain
- Scale

보정에 유효하다.

그러나 calibration 한 번으로:

- Random noise
- Future drift
- Aging

이 영구 제거되지는 않는다.

## 23. Calibration Interval

Calibration interval은 다음을 기준으로 정한다.

- Stability history
- Drift trend
- Required uncertainty/accuracy
- Environment
- Usage criticality
- Maintenance cost

모든 device에 동일한 fixed interval을 적용하는 방식은 부적절하다.

## 24. Circuit-Level Mitigation

원인에 따라 다음을 사용할 수 있다.

- Low-noise amplifier
- Low-drift reference
- Matched resistor network
- Ratiometric architecture
- Differential measurement
- Auto-zero / chopper
- Decoupling
- Local filtering
- PCB return-current control
- Sensitive-node protection

모든 방법에는 cost, bandwidth, complexity trade-off가 있다.

## 25. PCB / Local Layout

Local electronics layout은 coupling error에 영향을 준다.

- Return current path
- Analog/digital partition
- Decoupling
- Reference routing
- High-impedance node protection
- Short sensitive loop

하지만 plant grounding topology와 field shield termination은 별도 Topic이다.

## 26. Error Budget

각 contributor를 공통 기준으로 환산한다.

예:

`Input-referred error`

또는

`Output-referred error`

그 뒤:

- Offset
- Gain
- Noise
- Tolerance
- Temperature drift
- Reference
- ADC
- Supply sensitivity

를 결합한다.

목적은 total error만 구하는 것이 아니라 dominant contributor를 찾는 것이다.

## 27. Worst-case vs RSS

모든 error를 한 방식으로 더하지 않는다.

Deterministic limit 또는 완전히 correlated contribution은 worst-case가 보수적일 수 있다.

독립적인 random contributor는 RSS 같은 statistical combination을 사용할 수 있다.

전제는 correlation과 distribution을 확인하는 것이다.

## 28. Diagnosis

전자오차가 발생하면 먼저 “noise”라고 단정하지 않는다.

확인 순서 예:

- Zero
- Span
- Signal level
- Temperature trend
- Supply/reference
- Bandwidth
- Time trend
- Channel correlation

이 데이터를 사용해 offset/gain/noise/drift/power path를 분리한다.

## 29. Mitigation Hierarchy

대책은 원인에 맞게 조합한다.

`Source reduction → Sensitivity/coupling reduction → Conditioning/filtering → Calibration/compensation → Monitoring/recalibration`

하나의 대책이 모든 error mechanism을 제거한다고 가정하지 않는다.

## 30. Residual Verification

대책 후 다시 확인한다.

- Zero/span
- Noise level
- Temperature sensitivity
- Supply sensitivity
- Repeatability
- Long-term trend

Residual error가 requirement와 error budget을 만족해야 한다.

## 31. Ownership Boundary

### Topic 1 — Power/Grounding/EMC

`instrumentation_power_grounding_shielding_ups_ground_loop_emc`

소유:

- Plant power quality
- Grounding topology
- Shield termination
- Ground loop
- Field EMC diagnosis

Topic 5 소유:

- Local regulator/reference
- PSRR
- PCB-level coupling contributor
- Electronics error chain

### Topic 3 — Environmental Qualification

`instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification`

소유:

- Qualification setup
- Stress
- Monitoring
- Pass/fail evidence

Topic 5 소유:

- Temperature drift mechanism
- Aging/error mechanism

### Topic 4 — Hardware Lifecycle

`control_hardware_lifecycle_panel_architecture_component_selection_production_verification`

소유:

- Architecture
- Component selection governance
- Design verification
- Manufacturing
- Production verification

Topic 5 소유:

- Component/circuit error mechanism
- Error budget
- Mitigation rationale

### Sensor-specific Topics

각 센서의 sensing principle과 sensor-specific compensation은 해당 Topic이 소유한다.

Topic 5는 여러 센서 interface에 공통인 electronics error를 소유한다.

### Metrology / Calibration Topics

Accuracy, precision, repeatability, uncertainty와 traceability의 일반 정의는 metrology Topic이 소유한다.

Topic 5는 그 결과에 기여하는 circuit-level error source를 소유한다.

## 32. 고득점 답안 조건

고득점 답안은 다음을 포함한다.

- Systematic/random/drift 구분
- Offset/gain/linearity 구분
- Noise-bandwidth 관계
- Tolerance/drift/aging 구분
- Supply/reference/PSRR
- ADC resolution ≠ accuracy
- Error budget
- Worst-case vs RSS
- Filtering/calibration 역할과 한계
- Residual verification
- Adjacent Topic ownership boundary

## 33. Fixed-number policy

다음은 universal fixed number를 사용하지 않는다.

- PSRR
- Drift
- Tolerance
- Filter cutoff
- Calibration interval

Device, frequency, environment, requirement와 source data에 따라 달라진다.

Historical frequency는 근거가 없으므로 사용하지 않는다.
