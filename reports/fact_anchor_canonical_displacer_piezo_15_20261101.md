# Sensor physics canonical fact-anchor evidence — 2026-11-01

Reviewer: GPT-6 (AI, 2026-11-01). Fifteen canonical `fact_anchor.json` original statements individually compared to primary manufacturer HTML plus explicitly stated physical derivation where indicated. **13 fully scoped confirmations, 2 HOLD**. No Topic Pack JSON altered, tests not executed. General scoring exclusions and requirements remain separate.

## 1. displacer_density_change_can_bias_level_indication

- Source topic / Anchor: `displacer_level_buoyancy_torque_tube_density_interface_calibration` / `displacer_density_error`
- Canonical statement: 설계 액체 밀도와 실제 밀도가 달라지면 같은 잠김 체적의 부력이 달라져 레벨 지시가 편향될 수 있다.
- Publisher: Emerson/Fisher, *Fisher 249BP Cageless Sensor*
- Source: https://www.emerson.com/en/final-control/products/fisher-249bp
- Section/equation: Product Description / Specific Gravity
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Density/specific-gravity changes affect buoyant force at same submergence; requires known calibration density and temperature.

## 2. displacer_force_sensing_differs_from_free_float_position_sensing

- Source topic / Anchor: `displacer_level_buoyancy_torque_tube_density_interface_calibration` / `displacer_float_boundary`
- Canonical statement: 고정·현수된 displacer는 부력에 따른 힘 변화를 검출하고 자유 Float는 액면을 따라 움직이는 위치를 검출한다.
- Publisher: Emerson/Fisher, *Level Controllers Sensing Types*
- Source: https://www.emerson.com/en/final-control/catalog/products-and-software/valve-actuator-regulator-instrumentation/level-controllers
- Section/equation: Float-style Level Sensing vs Displacer-style Level Sensing
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Free float changes position with surface; suspended displacer changes load in suspension as buoyancy changes. Does not assert every displacer has perfectly fixed position.

## 3. fully_submerged_interface_displacer_force_depends_on_density_difference

- Source topic / Anchor: `displacer_level_buoyancy_torque_tube_density_interface_calibration` / `displacer_interface_density_difference`
- Canonical statement: 두 비혼합 액체의 계면 측정은 각 액체의 밀도와 침수체적 배분에 의존한다. 전체 침수·균일 밀도 조건이면 F_b = g(rho_L V_L + rho_U V_U)이고 V_L+V_U는 일정해 계면 감도가 밀도차에 비례한다.
- Publisher: Emerson/Fisher, *Fisher 249BP Cageless Sensor*
- Source: https://www.emerson.com/en/final-control/products/fisher-249bp
- Section/equation: Displacer sensor Archimedes, level/interface/density uses; buoyancy additive force derivation
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: For two unmixed immiscible liquids and fully submerged displacer, Fb = g(ρlowerVlower+ρupperVupper); sensitivity ∝ density difference if total immersed V fixed. Manufacturer confirms method, formula independently derives from Archimedes; assumes hydrostatic density uniform in each layer.

## 4. charge_amplifier_feedback_resistor_low_frequency_cutoff

- Source topic / Anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `charge_amplifier_feedback_resistor_low_frequency_cutoff`
- Canonical statement: 피드백 저항 Rf는 방전경로를 제공하고 저주파 차단은 fc≈1/(2πRfCf)로 근사하며 RfCf가 클수록 더 낮은 주파수를 측정할 수 있다.
- Publisher: PCB Piezotronics, *Introduction to Piezoelectric Force Sensors*
- Source: https://www.pcb.com/resources/technical-information/introduction-to-force-sensors
- Section/equation: DTC Charge Mode System, external feedback R,C
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Feedback RfCf sets RC high-pass time constant, fc≈1/(2πRfCf) for 1st order, and actual electronics/cable may impose another highpass.

## 5. piezoelectric_accelerometer_inertial_force_chain

- Source topic / Anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_accelerometer_inertial_force_chain`
- Canonical statement: 압전 가속도계는 내부 관성질량에 작용하는 F=ma의 힘을 압전소자가 검출하여 가속도로 환산한다.
- Publisher: PCB Piezotronics, *Introduction to Piezoelectric Accelerometers*
- Source: https://www.pcb.com/resources/technical-information/introduction-to-accelerometers
- Section/equation: Construction of ICP Accelerometers: seismic mass stressing crystals
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Newton F=ma in sensor mechanical axis and fixed proof mass; actual output calibration includes sensitivity and mounting/dynamics.

## 6. piezoelectric_charge_constant_q_df

- Source topic / Anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_charge_constant_q_df`
- Canonical statement: 단일 축 선형영역에서 Q=dF로 나타내며 d는 시간미분이 아니라 재료·결정축·분극 및 하중방향에 따른 압전 전하상수이다.
- Publisher: PCB Piezotronics, *Introduction to Piezoelectric Force Sensors*
- Source: https://www.pcb.com/resources/technical-information/introduction-to-force-sensors
- Section/equation: Direct force/charge proportionality; charge sensitivity pC/lb etc
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Q=dF in small-signal linear static stress-to-charge step response, with sensitivity d in C/N along specified piezo axis. d is coefficient, not derivative.

## 7. piezoelectric_equivalent_circuit_charge_capacitance_leakage

- Source topic / Anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_equivalent_circuit_charge_capacitance_leakage`
- Canonical statement: 압전센서는 전하원과 센서 정전용량 Cp, 절연 및 누설을 나타내는 병렬저항 Rp로 모델링하며 케이블과 입력단도 등가회로에 포함한다.
- Publisher: PCB Piezotronics, *Signal Conditioning Basics*
- Source: https://www.pcb.com/resources/technical-information/signal-conditioning-basics
- Section/equation: Voltage Mode and Charge Mode Systems; Figures 2/4 circuit schematics
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Ideal charge generator in parallel Cp and leakage Rp, cable/input capacitance add to voltage-mode readout. Model applies to charge mode; internally integrated electronics change equivalent interface.

## 8. piezoelectric_force_sensor_measurement_chain

- Source topic / Anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_force_sensor_measurement_chain`
- Canonical statement: 압전식 힘센서는 힘을 압전소자의 응력과 전하로 바꾸고 conditioner 출력과 교정감도를 이용해 다시 힘으로 환산한다.
- Publisher: PCB Piezotronics, *Introduction to Piezoelectric Force Sensors*
- Source: https://www.pcb.com/resources/technical-information/introduction-to-force-sensors
- Section/equation: Piezoelectric force sensor working principle, charge and conditioner
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Dynamic force produces stress→charge; charge/current conditioner converts to voltage and calibration sensitivity recovers force; not reliable indefinitely under constant load.

## 9. piezoelectric_frequency_band_flat_response_resonance

- Source topic / Anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_frequency_band_flat_response_resonance`
- Canonical statement: 유효 측정대역은 전기적 저주파 차단과 기계적 고주파 공진 사이이며 정밀측정은 일반적으로 공진을 피한 평탄대역에서 수행한다.
- Publisher: PCB Piezotronics, *Introduction to Piezoelectric Accelerometers*
- Source: https://www.pcb.com/resources/technical-information/introduction-to-accelerometers
- Section/equation: Low Frequency Response and High Frequency Response (resonance)
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Usable band bounded by AC coupling RC at low f and mechanical resonance high f, with frequency flatness requirement/calibration; different sensor models vary.

## 10. piezoelectric_mounting_stiffness_torque_contact_resonance

- Source topic / Anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_mounting_stiffness_torque_contact_resonance`
- Canonical statement: 설치강성, 체결토크와 설치면 상태는 접촉공진과 고주파 응답을 변화시키므로 규정된 설치조건으로 관리한다.
- Publisher: PCB Piezotronics, *Guidelines for Mounting Test Accelerometers*
- Source: https://www.pcb.com/resources/technical-information/mounting
- Section/equation: Frequency Response and Stud Mounting, surface/torque guidance
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: High-frequency response and mounted resonance depend on mounting stiffness, torque and surface; no universal tightening torque.

## 11. piezoelectric_voltage_charge_capacitance_relation

- Source topic / Anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_voltage_charge_capacitance_relation`
- Canonical statement: 개방회로 전압은 V=Q/C로 근사하며 단순 전압입력에서는 센서와 케이블의 등가정전용량이 감도와 주파수특성에 영향을 준다.
- Publisher: PCB Piezotronics, *Signal Conditioning Basics*
- Source: https://www.pcb.com/resources/technical-information/signal-conditioning-basics
- Section/equation: Equations 1 and 2: V1=q/C1 and V2=q/(C1+C2+C3)
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Open circuit V=q/Csensor; load/cable/input capacitance lowers measured voltage sensitivity in voltage-mode high-impedance connection.

## 12. piezoresistive_pressure_sensor_bridge_readout

- Source topic / Anchor: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` / `piezoresistive_principle_bridge`
- Canonical statement: Piezoresistive pressure sensor는 diaphragm의 변형으로 반도체 또는 strain element의 저항이 변하는 효과를 이용하며, 여러 저항을 Wheatstone bridge로 구성해 작은 저항변화를 차동 전압으로 읽는 방식이 대표적이다.
- Publisher: Analog Devices, *Demystifying Piezoresistive Pressure Sensors*
- Source: https://www.analog.com/en/resources/technical-articles/demystifying-piezoresistive-pressure-sensors.html
- Section/equation: Resistive Sensors bridge output Vdiff and diaphragm deformation
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Strained diaphragm changes resistor values and bridge yields differential voltage under excitation; designs differ, not all piezoresistive sensors use 4-active-resistor bridge.

## 13. piezoresistive_vs_piezoelectric_static_pressure_response

- Source topic / Anchor: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` / `piezoresistive_static_capability`
- Canonical statement: Piezoresistive 방식은 외부 excitation과 signal conditioning이 필요하지만 정적 압력과 저주파 압력도 측정할 수 있다. 전하 누설 때문에 정적 측정이 어려운 piezoelectric sensor와 구분해야 한다.
- Publisher: Analog Devices, *Demystifying Piezoresistive Pressure Sensors*
- Source: https://www.analog.com/en/resources/technical-articles/demystifying-piezoresistive-pressure-sensors.html
- Section/equation: Pressure-sensitive resistive bridge description and PCB piezo high-pass limitation
- Verdict: **KEEP_BOUNDED**
- Verified scope/counterexample or missing source: Piezoresistive with excitation can measure steady pressure, piezoelectric charge signal decays via leakage and is preferred dynamic changes; temperature and bias/drift need correction.

## 14. piezoelectric_signal_conditioning_filter_adc_antialias

- Source topic / Anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_signal_conditioning_filter_adc_antialias`
- Canonical statement: 측정시스템은 conditioner, 입력범위, high-pass와 low-pass filter, anti-aliasing filter, sampling rate와 ADC 동적범위를 함께 설계한다.
- Publisher: PCB Piezotronics, *Signal Conditioning Basics*
- Source: https://www.pcb.com/resources/technical-information/signal-conditioning-basics
- Section/equation: Signal Conditioning Basics, bandwidth and cable/low-pass limits
- Verdict: **HOLD_INCOMPLETE_ADC_EVIDENCE**
- Verified scope/counterexample or missing source: Original article supports conditioning, input range and bandwidth, but does not directly establish all ADC anti-aliasing/sampling design requirements; need original ADC front-end source.

## 15. piezoelectric_temperature_pyroelectric_thermal_shock

- Source topic / Anchor: `piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration` / `piezoelectric_temperature_pyroelectric_thermal_shock`
- Canonical statement: 온도는 감도와 절연저항을 변화시키며 빠른 온도변화는 열팽창응력과 pyroelectric output에 의한 과도출력을 만들 수 있다.
- Publisher: PCB Piezotronics, *Introduction to Piezoelectric Accelerometers*
- Source: https://www.pcb.com/resources/technical-information/introduction-to-accelerometers
- Section/equation: Temperature / operating limitations
- Verdict: **HOLD_PARTIAL_TEMPERATURE_SOURCE**
- Verified scope/counterexample or missing source: PCB accelerometer introduction does not explicitly prove pyroelectric vs thermal shock and coefficient model in original statement; need primary sensing physics/manual.


The Fisher displacer interface equation follows Archimedes with total fixed displaced volume; official product page supports principle but does not itself state the expanded equation. This distinction is critical: a reproducible physics derivation is evidence for that identity under stated assumptions, not a false quote from a vendor. HOLD rows remain NOT_PERFORMED. No complete primary-source verification is claimed for those holds.
