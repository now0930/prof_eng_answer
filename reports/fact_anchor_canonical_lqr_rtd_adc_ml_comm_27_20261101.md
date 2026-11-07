# Canonical fact-anchor independent source review: 27 claims (2026-11-01)

Branch: `codex/essay-boundary-calibration-20261028`. Reviewer: GPT-6 (AI technical original-source review, not human/approval workflow). Access date: 2026-11-01. All rows compare the **actual canonical `fact_anchor.json` statement**, not just a fact ID, to the cited publisher's HTML documentation, or for IEC 60751:2022 the identified publicly hosted preview. No native Topic Pack/score runtime files modified; no gate/test executed.

Verdict KEEP_BOUNDED means the explicit scope below is supported. **No** publisher opinion, vendor model special-case, legally local code or a cited example automatically becomes a universally required grading anchor. Do not claim full standard text was reviewed from the preview.

## 1. continuous_and_discrete_lqr_use_different_riccati_equations

- Canonical topic/anchor: `lqr_optimal_state_feedback_riccati_weighting_design` / `state_lqr_continuous_discrete_riccati_distinction`
- Original source statement: 연속시간 LQR은 CARE를 사용하고 이산시간 LQR은 DARE와 K_d=(R+B_d^TPB_d)^(-1)B_d^TPA_d를 사용하며, 두 해를 동일하게 취급해서는 안 된다.
- Evidence: MathWorks, *lqr MATLAB R2026b*, Algorithms; comparison with DLQR Algorithms
- Link: https://www.mathworks.com/help/control/ref/lti.lqr.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: CARE uses A'P+PA-PBR^-1B'P+Q=0; discrete DARE includes B'PB+R and A'PB. Original formula uses N=0 and discrete A_d,B_d. Source covers both.

## 2. continuous_time_lqr_care_and_stabilizing_solution

- Canonical topic/anchor: `lqr_optimal_state_feedback_riccati_weighting_design` / `state_lqr_care_stabilizing_solution`
- Original source statement: 교차항이 없는 연속시간 무한시간 LQR의 CARE는 A^TP+PA-PBR^(-1)B^TP+Q=0이며, 제어에는 A-BR^(-1)B^TP를 안정하게 만드는 stabilizing solution P를 사용한다.
- Evidence: MathWorks, *lqr MATLAB R2026b*, Algorithms; standard N=0 CARE and closed loop
- Link: https://www.mathworks.com/help/control/ref/lti.lqr.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: P is symmetric stabilizing solution under LQR existence assumptions; open-loop/closed-loop A,B sizes and R>0 required.

## 3. continuous_time_lqr_gain_and_closed_loop_poles

- Canonical topic/anchor: `lqr_optimal_state_feedback_riccati_weighting_design` / `state_lqr_optimal_gain_closed_loop`
- Original source statement: 안정화 Riccati 해 P에서 K=R^(-1)B^TP를 계산하고 u=-Kx를 적용하면 폐루프 행렬은 A-BK가 되며 그 고유값이 LQR 폐루프 극점이다.
- Evidence: MathWorks, *lqr MATLAB R2026b*, Algorithms: K=R^-1B'S and poles eig(A-BK)
- Link: https://www.mathworks.com/help/control/ref/lti.lqr.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Formula shown for continuous-time state feedback with N=0; do not apply discrete gain formula.

## 4. continuous_time_lqr_quadratic_cost_state_and_effort

- Canonical topic/anchor: `lqr_optimal_state_feedback_riccati_weighting_design` / `state_lqr_design_objective_cost`
- Original source statement: LQR은 상태편차와 제어입력 사용량의 상충관계를 J=∫(x^TQx+u^TRu)dt의 이차 비용함수로 정의하고 이를 최소화하는 상태피드백 이득을 구하는 최적제어 방법이다.
- Evidence: MathWorks, *lqr MATLAB R2026b*, Algorithms: continuous infinite-horizon J integral
- Link: https://www.mathworks.com/help/control/ref/lti.lqr.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Quadratic cost assumes declared Q,R, linear state dynamics, feasible stabilizing controller; not a hard input constraint.

## 5. lqr_cost_optimization_indirectly_determines_closed_loop_poles

- Canonical topic/anchor: `lqr_optimal_state_feedback_riccati_weighting_design` / `state_lqr_pole_placement_distinction`
- Original source statement: 극점 배치는 원하는 폐루프 극점을 직접 지정하지만 LQR은 Q와 R로 정의한 비용함수 최소화 결과로 폐루프 극점이 간접 결정된다.
- Evidence: MathWorks, *lqr MATLAB R2026b*, Description and Algorithms: Q/R optimum and closed-loop P
- Link: https://www.mathworks.com/help/control/ref/lti.lqr.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: K from cost weights; returned eig(A-BK) poles not independently chosen. Differences between LQR and arbitrary pole placement are valid under model assumptions.

## 6. lqr_stabilizing_care_existence_conditions

- Canonical topic/anchor: `lqr_optimal_state_feedback_riccati_weighting_design` / `state_lqr_existence_stabilizability_detectability`
- Original source statement: 교차항이 없는 표준 연속시간 무한시간 LQR에서 Q=Q^T⪰0, R=R^T≻0, (A,B)가 stabilizable이고 (Q^(1/2),A)가 detectable이면 폐루프 A-BK를 Hurwitz로 만드는 고유한 양의 준정부호 안정화 해 P=P^T⪰0가 존재한다. 완전 가제어성과 완전 관측성은 더 강한 충분조건이다.
- Evidence: MathWorks, *lqr MATLAB R2026b*, Limitations: (A,B) stabilizable, R>0, Q positive semidefinite, no unobservable imaginary-axis mode
- Link: https://www.mathworks.com/help/control/ref/lti.lqr.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Canonical (Q^(1/2),A) detectable suffices for absence of unobservable imaginary-axis modes, plus stabilizability and positive definite R. This is a sufficient condition, not necessary for every generalized Riccati variant.

## 7. rtd_callendar_van_dusen_characteristic

- Canonical topic/anchor: `rtd_temperature_sensor_principle_pt100_wiring_compensation` / `rtd_callendar_van_dusen_characteristic`
- Original source statement: Pt100의 저항-온도 관계는 전 온도범위에서 완전한 직선이 아니며, 0℃ 이상에서는 R_t=R_0(1+At+Bt²), 0℃ 미만에서는 C(t−100)t³ 항을 추가하는 Callendar–Van Dusen 관계를 사용한다.
- Evidence: IEC 60751:2022 (publicly hosted standard preview), *Industrial Platinum Resistance Thermometers*, IEC 60751:2022 clause 4.2: R0(1+At+Bt²) and C term below zero
- Link: https://standards.iteh.ai/catalog/standards/sist/9f8d6d0e-7670-47db-a6de-211d516528a4/sist-en-iec-60751-2022
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Standard nominal platinum relation; A/B/C specified; do not treat individual measured RTD as exactly nominal over all tolerance classes.

## 8. rtd_four_wire_kelvin_measurement

- Canonical topic/anchor: `rtd_temperature_sensor_principle_pt100_wiring_compensation` / `rtd_four_wire_kelvin_measurement`
- Original source statement: 4선식 RTD는 force lead로 측정전류를 공급하고 sense lead로 RTD 양단 전압을 측정하는 Kelvin 방식으로 리드선 전압강하 영향을 크게 줄인다.
- Evidence: Analog Devices, *Precision Temperature Measurement Solution using RTD*, 3-wire and 4-wire configurations, Figure 3; force/sense Kelvin
- Link: https://www.analog.com/en/resources/analog-dialogue/articles/a-precision-temperature-measurement-solution-with-high-emc-performance-using-an-rtd.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: High-impedance sense terminals remove lead voltage drops approximately; input bias, thermoelectric EMF and excitation errors remain.

## 9. rtd_metal_resistance_temperature_principle

- Canonical topic/anchor: `rtd_temperature_sensor_principle_pt100_wiring_compensation` / `rtd_metal_resistance_temperature_principle`
- Original source statement: RTD는 R=ρl/A에서 금속 비저항 ρ가 온도에 따라 변하는 성질을 주된 변환원리로 이용하며, 백금은 안정성·재현성·내식성이 우수하여 널리 사용된다.
- Evidence: NI, *Taking Temperature Measurements with RTDs*, Basic RTD Principle and Platinum resistance curves
- Link: https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000x1rnCAA&l=en-US
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Resistance of metal varies reproducibly with T. R=ρl/A is a fixed-geometry approximation and geometry also has thermal expansion; no universal linear alpha over whole range.

## 10. rtd_pt100_reference_resistance_alpha_standard

- Canonical topic/anchor: `rtd_temperature_sensor_principle_pt100_wiring_compensation` / `rtd_pt100_reference_resistance_alpha_standard`
- Original source statement: Pt100은 0℃에서 공칭저항이 100 Ω인 백금 RTD이며, 대표 산업용 표준 특성의 평균 온도계수 α는 약 0.00385/℃이다.
- Evidence: IEC 60751:2022 (publicly hosted standard preview), *Industrial Platinum Resistance Thermometers*, IEC 60751:2022 clause 4.2, Pt100 in table A.1; supplementary NI RTD how-to
- Link: https://standards.iteh.ai/catalog/standards/sist/9f8d6d0e-7670-47db-a6de-211d516528a4/sist-en-iec-60751-2022
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Pt100 R0=100Ω at 0°C and nominal mean alpha≈0.00385/°C for this industrial platinum standard; there are other platinum curves.

## 11. rtd_self_heating_thermal_error

- Canonical topic/anchor: `rtd_temperature_sensor_principle_pt100_wiring_compensation` / `rtd_self_heating_thermal_error`
- Original source statement: RTD의 여기전류는 P=I_exc²R_RTD의 열을 발생시키며, 열이 충분히 방출되지 않으면 감온부 온도가 실제 공정온도보다 높아지는 자기발열 오차가 발생한다.
- Evidence: IEC 60751:2022 (publicly hosted standard preview), *Industrial Platinum Resistance Thermometers*, IEC 60751:2022 clause 5.3 measuring current and self-heating limits
- Link: https://standards.iteh.ai/catalog/standards/sist/9f8d6d0e-7670-47db-a6de-211d516528a4/sist-en-iec-60751-2022
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: I²R Joule heat creates error if heat dissipation is limited, measured thermal rise depends on medium and immersion; self-heating current limit is standard-class-specific.

## 12. rtd_three_wire_bridge_compensation_assumptions

- Canonical topic/anchor: `rtd_temperature_sensor_principle_pt100_wiring_compensation` / `rtd_three_wire_bridge_compensation_assumptions`
- Original source statement: 3선식 RTD는 bridge 또는 차동측정에서 R_L1≈R_L2라는 동일 리드저항 가정을 이용하여 리드선 영향의 1차 성분을 상쇄한다.
- Evidence: Analog Devices, *CN0383 Circuit Note*, CN0383 section Lead Resistance Consideration: matched leads and excitation current
- Link: https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/cn0383.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: 3-wire cancellation assumes approximate equal lead resistances (and matched currents for the chosen circuitry); not all 3-wire readouts use identical bridge implementation.

## 13. rtd_wiring_method_selection_tradeoff

- Canonical topic/anchor: `rtd_temperature_sensor_principle_pt100_wiring_compensation` / `rtd_wiring_method_selection_tradeoff`
- Original source statement: RTD의 2선식·3선식·4선식은 요구 불확도, 배선거리, 비용, 단자 수, transmitter 위치와 유지보수성을 함께 고려하여 선정한다.
- Evidence: Analog Devices, *Precision Temperature Measurement Solution using RTD*, 2/3/4-wire solutions and economic/accuracy tradeoff
- Link: https://www.analog.com/en/resources/analog-dialogue/articles/a-precision-temperature-measurement-solution-with-high-emc-performance-using-an-rtd.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: 2-wire economical but lead errors; 3-wire conditional compensation; 4-wire highest lead rejection at added wiring cost; actual required uncertainty and distance remain application-specific.

## 14. eem_adc_aliasing_distinct_from_quantization

- Canonical topic/anchor: `electronics_error_noise_drift_tolerance_aging_power_mitigation` / `eem_adc_aliasing_boundary`
- Original source statement: Sampling system에서는 Nyquist 조건과 anti-alias filtering이 필요하며 aliasing은 대역 밖 신호가 잘못된 저주파 성분으로 접혀 들어오는 오류로 단순 quantization noise와 구분한다.
- Evidence: Analog Devices, *AC and DC Data Acquisition Signal Chains Made Easy*, Combating Challenges: sampling aliasing versus quantization noise
- Link: https://www.analog.com/en/resources/analog-dialogue/articles/ac-and-dc-data-acquisition-signal-chains-made-easy.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Aliasing folds spectral frequencies above Nyquist into lower baseband, whereas quantization stems from finite ADC levels; filters/oversampling assumptions must be stated.

## 15. eem_adc_offset_error_transfer_intercept_and_circuit_sources

- Canonical topic/anchor: `electronics_error_noise_drift_tolerance_aging_power_mitigation` / `eem_offset_error`
- Original source statement: Offset error는 입력이 기준값 또는 zero일 때 출력에 일정하게 더해지는 bias 성분으로, 증폭기 input offset, bias current에 의한 voltage drop, reference mismatch와 같은 회로원인으로 발생할 수 있다.
- Evidence: Analog Devices, *Chapter 20 Analog to Digital Conversion*, ADC error table: Offset; supplementary Analog Devices ABCs offset section
- Link: https://wiki.analog.com/university/courses/electronics/text/chapter-20
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Offset shifts converter transfer intercept. Listed opamp bias and reference mismatch are possible signal-chain sources, not mandatory in every ADC topology.

## 16. eem_adc_transfer_linearity_residual_after_offset_gain

- Canonical topic/anchor: `electronics_error_noise_drift_tolerance_aging_power_mitigation` / `eem_linearity_error`
- Original source statement: Linearity error는 offset과 gain을 제거한 뒤에도 실제 transfer가 이상적인 직선 또는 정의된 특성에서 벗어나는 성분으로, 단순 zero/span calibration만으로 완전히 제거되지 않을 수 있다.
- Evidence: Analog Devices, *Chapter 20 Analog to Digital Conversion*, INL after offset and gain adjustment / transfer curve
- Link: https://wiki.analog.com/university/courses/electronics/text/chapter-20
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: INL remains even after two-point calibration for nonlinear transfer, depends on definition (endpoint vs best fit).

## 17. eem_filter_noise_reduction_phase_and_settling_limits

- Canonical topic/anchor: `electronics_error_noise_drift_tolerance_aging_power_mitigation` / `eem_filter_noise_mitigation`
- Original source statement: Analog/digital filtering은 관심 대역 밖 noise를 줄일 수 있지만 cutoff와 order를 과도하게 제한하면 response delay, phase distortion 또는 유효 transient 손실이 생길 수 있어 signal bandwidth 기준으로 설계해야 한다.
- Evidence: Analog Devices, *Practical Filter Design Challenges for Precision ADCs*, Section 3 Phase Delay and Matching; section 4 Settling Time and digital filter latency
- Link: https://www.analog.com/en/resources/analog-dialogue/articles/practical-filter-design-precision-adcs.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Anti-noise filtering trades attenuation against phase/group delay, settling and signal preservation; exact response depends on type/order and sampling.

## 18. eem_signal_chain_gain_error_sources

- Canonical topic/anchor: `electronics_error_noise_drift_tolerance_aging_power_mitigation` / `eem_gain_error`
- Original source statement: Gain error는 이상적인 transfer slope와 실제 slope의 차이로 입력 크기에 비례해 오차가 커지며 resistor ratio, amplifier gain accuracy, reference scale과 ADC full-scale path가 원인이 될 수 있다.
- Evidence: Analog Devices, *The ABCs of ADCs*, Offset and Gain Errors
- Link: https://www.analog.com/en/resources/technical-articles/the-abcs-of-analog-to-digital-converters-how-adc-errors-affect-system-performance.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Transfer slope error scales with applied signal; resistor/reference/amplifier implementation may contribute, not all will exist in every architecture.

## 19. eem_snr_dynamic_range_noise_floor_vs_nominal_bits

- Canonical topic/anchor: `electronics_error_noise_drift_tolerance_aging_power_mitigation` / `eem_snr_dynamic_range`
- Original source statement: Signal-to-noise ratio와 dynamic range는 작은 유효신호가 전자 noise floor에 묻히지 않는지 평가하는 지표이며 단순 ADC bit 수만 높인다고 front-end noise floor가 자동으로 낮아지는 것은 아니다.
- Evidence: Analog Devices, *The ABCs of ADCs*, Abstract and quantization/INL/noise error budget
- Link: https://www.analog.com/en/resources/technical-articles/the-abcs-of-analog-to-digital-converters-how-adc-errors-affect-system-performance.html
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Nominal ADC resolution does not guarantee signal-chain effective bits or noise floor; SNR and full-scale dynamic range depend on front-end electronics and noise bandwidth.

## 20. ml_precision_is_true_positives_over_predicted_positives

- Canonical topic/anchor: `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` / `precision_metric`
- Original source statement: Precision은 모델이 Positive로 판정한 사례 중 실제 Positive의 비율이며 오경보가 많은 경우 낮아진다.
- Evidence: Google Developers, *Machine Learning Crash Course: Precision and Recall*, Precision formula TP/(TP+FP)
- Link: https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Defined for binary/classwise positives; undefined when TP+FP=0 without an application-defined zero-division policy. False positives lower precision given TP.

## 21. ml_recall_is_true_positives_over_actual_positives

- Canonical topic/anchor: `industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle` / `recall_metric`
- Original source statement: Recall은 실제 Positive 중 모델이 검출한 비율이며 위험 고장의 미검출이 중요한 경우 핵심 지표가 된다.
- Evidence: Google Developers, *Machine Learning Crash Course: Precision and Recall*, Recall formula TP/(TP+FN)
- Link: https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Defined for binary/classwise positives; undefined when no actual positives. False negatives reduce recall given TP.

## 22. opc_ua_address_space_services_information_models_and_subscriptions

- Canonical topic/anchor: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` / `sw07_opcua`
- Original source statement: OPC UA는 platform-independent service, address space, information model과 method·event·subscription을 제공하여 시스템 간 의미 있는 데이터 교환을 지원하는 상호운용 아키텍처이다.
- Evidence: OPC Foundation, *Unified Architecture Technology Overview*, UA Technology Overview: Address Space, Read/Write, Events, Methods, Subscriptions
- Link: https://opcfoundation.org/about/opc-technologies/opc-ua/
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Interoperability only where profiles, models, access permissions and supported server services align; UA architecture not guaranteed deterministic motion-control network.

## 23. hart_superimposes_digital_data_and_configuration_on_4_20ma

- Canonical topic/anchor: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` / `sw07_hart_overlay`
- Original source statement: HART는 기존 4–20 mA 아날로그 신호 위에 디지털 통신을 중첩하여 주 변수와 함께 설정·상태·추가 변수·진단정보를 교환할 수 있게 한다.
- Evidence: FieldComm Group, *HART Technology Explained*, HART Technology Explained, FSK on analog 4–20mA
- Link: https://www.fieldcommgroup.org/technologies/hart/hart-technology-explained
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Traditional point-to-point HART overlay carries configuration, status, diagnostic and extra values; alternate HART modes may have fixed analog current, not always an analog PV signal.

## 24. relative_humidity_is_vapor_pressure_ratio_at_same_temperature

- Canonical topic/anchor: `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` / `relative_humidity_definition`
- Original source statement: Relative humidity는 같은 온도에서 실제 수증기 분압 P_w를 포화수증기압 P_ws(T)로 나눈 비이며 RH[%] = 100·P_w/P_ws(T)로 정의한다. 포화수증기압은 온도함수이므로 RH는 온도에 강하게 의존한다.
- Evidence: Vaisala, *HM40 User Guide: Parameters*, HM40 parameters: RH definition
- Link: https://docs.vaisala.com/r/M211088EN-D/en-US/GUID-F1EB60A0-9D47-4257-B24D-142DAE551AFA
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: RH=Pw/Pws(T)×100%, same T, specified saturation reference and water-vapor equilibrium; temperature-dependent denominator.

## 25. probe_temperature_difference_can_bias_rh_or_cause_condensation

- Canonical topic/anchor: `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` / `condensation_sensor_temperature_error`
- Original source statement: Sensor surface가 주변공기보다 차가워 local RH가 높아지거나 dew point 이하로 내려가면 condensation이 발생할 수 있다. 반대로 self-heating이나 warm surface는 local RH를 낮춰 실제 process RH와 차이를 만들 수 있다.
- Evidence: Vaisala, *HM70 User Guide: Errors from Temperature Differences*, HM70 Errors Caused by Temperature Differences; dew-point condensation discussion
- Link: https://docs.vaisala.com/r/M210297EN-G/en-US/GUID-9D273B5F-99DE-4C66-B8C9-644EED6833B6
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Probe/process T mismatch biases apparent RH; surface below local dew point condenses, warmer probe lowers local RH. Applies near-equilibrated gas/humidity conditions.

## 26. piezoelectric_direct_effect_charge_generation

- Canonical topic/anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_direct_effect_charge_generation`
- Original source statement: 기계적 힘 또는 응력이 압전재료의 분극을 변화시켜 전극에 전하를 발생시키며 센서에는 직접 압전효과를 사용한다.
- Evidence: PCB Piezotronics, *Introduction to Piezoelectric Force Sensors*, How Piezoelectric Force Sensors Work, static and dynamic force
- Link: https://www.pcb.com/resources/technical-information/introduction-to-force-sensors
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Mechanical stress creates charge in piezoelectric material for direct effect; precise axes, coupling and linear operating region vary by design.

## 27. piezoelectric_static_limit_electrical_time_constant

- Canonical topic/anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_static_limit_electrical_time_constant`
- Original source statement: 발생전하는 누설경로로 감소하고 τ=RC의 전기적 시정수 때문에 진정한 DC 또는 무기한 정하중 측정에는 제한이 있다.
- Evidence: PCB Piezotronics, *Introduction to Piezoelectric Force Sensors*, Why Only Dynamic Force Can Be Measured; Discharge Time Constant
- Link: https://www.pcb.com/resources/technical-information/introduction-to-force-sensors
- Decision: **KEEP_BOUNDED**
- Claim/evidence mapping and limits: Leakage path causes step-charge decay toward zero with electrical discharge time constant; quasi-static response depends on time constant; not an absolute impossibility of short quasi-static measurement.


## Scope of this commit

This report is a fact-by-fact evidence record. The original exclusion and independent-revision-hold overlays remain authoritative for scoring. No original claim text, generated bank, exclusion overlay, or approval metadata changed. CI/release validation not performed. Conditional statements must remain bounded in future scoring reviews.