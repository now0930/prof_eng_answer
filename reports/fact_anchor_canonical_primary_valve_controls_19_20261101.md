# Independent Fact Anchor source-to-claim audit — 2026-11-01 (19 claims)

Scope: Each exact original claim was read from `rubrics/topic_packs/<topic_id>/fact_anchor.json` on `codex/essay-boundary-calibration-20261028` and compared to the identified original publisher source/section. `KEEP_BOUNDED` is not blanket approval of unrelated or product-specific requirements. The four original exclusion overlay categories still govern grading.

Official source media include publisher HTML and original indexed Emerson PDFs. For **Emerson Control Valve Handbook 6th edition**, attempted web PDF page screenshot returned a content-length error, so review only covers retrieved publisher-indexed text, not a page-image confirmation. PDF-based rows must not be described as visually checked.

This evidence report updates review metadata only: it does not change canonical source facts, generated banks, review holds, or a live grading authority. No repo release tests ran.

## 1. control_valve_cv_kv_conversion_is_approximate_unit_conversion

- Canonical: `control_valve_sizing_cv_kv_reynolds_liquid_selection` / `cv_kv_conversion_relation`
- Exact original statement: Cv와 Kv는 서로 변환 가능하며 통상 Kv≈0.865Cv, Cv≈1.156Kv를 사용한다.
- Source: Spirax Sarco, *Control Valve Capacity*
- Locator: Table 6.2.1, definitions and conversion
- Link: https://www.spiraxsarco.com/learn-about-steam/control-hardware-electric-pneumatic-actuation/control-valve-capacity
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Cv(US)=1.156099 Kv; inversion Kv≈0.86498 Cv. Use Cv(US), not British imperial gallons and specify bar-based Kv.

## 2. kv_reference_definition_is_water_flow_at_one_bar_with_source_specific_temperature

- Canonical: `control_valve_sizing_cv_kv_reynolds_liquid_selection` / `kv_reference_definition_metric_units`
- Exact original statement: Kv는 지정된 기준상태의 물이 밸브 전후 1 bar 차압에서 흐르는 m³/h 유량을 기준으로 하며 정확한 기준온도 wording은 적용 표준과 제조사 문서를 확인한다.
- Source: Spirax Sarco, *Control Valve Capacity*
- Locator: Table 6.2.1, definitions and conversion
- Link: https://www.spiraxsarco.com/learn-about-steam/control-hardware-electric-pneumatic-actuation/control-valve-capacity
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Kv uses m³/h of water across 1 bar, at specified temperature (Spirax typical 5–40°C); manufacturer/standard variant must be identified.

## 3. control_valve_cv_us_unit_reference_definition

- Canonical: `control_valve_sizing_cv_kv_reynolds_liquid_selection` / `cv_reference_definition_us_units`
- Exact original statement: 일반적인 Cv 정의는 60°F 물이 밸브 전후 1 psi 차압에서 흐르는 US gpm 유량을 기준으로 한다.
- Source: Spirax Sarco, *Control Valve Capacity*
- Locator: Table 6.2.1, definitions and conversion
- Link: https://www.spiraxsarco.com/learn-about-steam/control-hardware-electric-pneumatic-actuation/control-valve-capacity
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: US Cv is US gpm of water across 1 psi, 60°F is common selected reference but official Spirax standard definition allows a stated temperature in 40–100°F; DO NOT treat 60°F universal without the specific source.

## 4. control_valve_basic_liquid_equation_applicability_boundary

- Canonical: `control_valve_sizing_cv_kv_reynolds_liquid_selection` / `basic_equation_applicability_boundary`
- Exact original statement: 기본 액체식은 단상·비압축성·비초크·난류 조건을 전제로 하며 cavitation, flashing, choked, two-phase와 non-Newtonian service에는 추가 검토가 필요하다.
- Source: Emerson, *Control Valve Handbook, 6th edition*
- Locator: Ch.2 §§2.1.1 and 2.1.3; Ch.5 §§5.5-5.6, Liquid and Gas Sizing, N1 and properties
- Link: https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf
- Checked form: publisher indexed PDF text; screenshot failed (large file)
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Simple turbulent single-phase nonchoked liquid sizing excludes flashing, choking and unusual non-Newtonian/viscous/two-phase cases; apply correction factors and phase-change checks.

## 5. control_valve_sizing_pressure_drop_operating_point_boundary

- Canonical: `control_valve_sizing_cv_kv_reynolds_liquid_selection` / `sizing_pressure_drop_definition`
- Exact original statement: Sizing pressure drop은 정의한 운전점의 valve inlet pressure와 outlet pressure 차이며 available system differential과 valve에 실제 배분되는 pressure drop을 구분한다.
- Source: Spirax Sarco, *Control Valve Sizing for Water Systems*
- Locator: Sections Water Sizing, Section on Pumps
- Link: https://www.spiraxsarco.com/learn-about-steam/control-hardware-electric-pneumatic-actuation/control-valve-sizing-for-water-systems
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: For each operating case ΔPvalve=P1−P2, and pump/system losses mean full available pressure is not necessarily across valve. Both flow and valve ΔP needed.

## 6. control_valve_undersized_capacity_may_fail_maximum_flow_case

- Canonical: `control_valve_sizing_cv_kv_reynolds_liquid_selection` / `undersized_valve_selection_consequence`
- Exact original statement: Selected capacity가 부족하면 maximum flow를 확보하지 못하거나 과도한 pressure drop와 high travel operation이 발생할 수 있다.
- Source: Spirax Sarco, *Control Valve Sizing for Water Systems*
- Locator: Sections Water Sizing, Section on Pumps
- Link: https://www.spiraxsarco.com/learn-about-steam/control-hardware-electric-pneumatic-actuation/control-valve-sizing-for-water-systems
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: If rated Cv/Kv cannot pass Qmax at available ΔP under applicable sizing limits, required max flow cannot be attained; the system may instead operate at shifted pressure or near full travel.

## 7. control_valve_oversizing_can_reduce_low_flow_control_performance

- Canonical: `control_valve_sizing_cv_kv_reynolds_liquid_selection` / `oversized_valve_selection_consequence`
- Exact original statement: Selected rated capacity가 지나치게 크면 normal travel이 낮아지고 실제 resolution, installed gain과 control performance가 악화될 수 있다.
- Source: Emerson, *Properly Size Control Valves*
- Locator: Reasons for Concern, valve oversizing impacts
- Link: https://www.emerson.com/is/content/emerson/it/final-control/flow-controls/products/valves/properly-size-control-valves.pdf
- Checked form: publisher indexed PDF text; screenshot not verified
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Large rated Cv can place normal control at low travel and amplify changes in flow per travel, causing poor control or cycling in some loops; not inevitable and no fixed 20-80% universal rule.

## 8. liquid_sizing_screens_cavitation_flashing_and_choked_flow_with_pressure_data

- Canonical: `control_valve_sizing_cv_kv_reynolds_liquid_selection` / `cavitation_flashing_choked_screening`
- Exact original statement: Basic liquid sizing 후 vapor pressure, pressure recovery와 downstream pressure를 이용해 cavitation, flashing과 liquid choked 가능성을 screening해야 하며 상세 criterion과 damage prevention은 Topic 8이 소유한다.
- Source: Emerson, *Control Valve Flashing*
- Locator: Understanding Flashing / Damage Potential
- Link: https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/valve-flashing
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: After single-phase liquid sizing, compare inlet/outlet/vena pressures with vapor pressure and valve recovery; P2<Pv indicates flashing; cannot equate damage severity with choked prediction.

## 9. static_system_head_is_independent_of_flow_rate

- Canonical: `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` / `control_valve_static_head_installed_characteristic_effect`
- Exact original statement: Static head는 flow와 직접 비례하지 않는 pressure requirement로 작용하여 friction-dominated system과 다른 valve differential pressure 분배를 만들 수 있다.
- Source: KSB, *System Characteristic Curve*
- Locator: System head equation, static geodetic/pressure components and friction losses
- Link: https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/system-characteristic-curve-1116274
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Static system head is geodetic/terminal pressure contribution for fixed boundaries; unlike fluid-friction loss it does not vary with Q. Can vary if supply/destination level or terminal pressure changes.

## 10. control_process_gain_is_local_to_operating_conditions

- Canonical: `control_valve_authority_rangeability_gain_installed_performance` / `process_gain_operating_point_dependency`
- Exact original statement: Process gain은 유량, 부하, 열·물질수지와 운전점에 따라 달라질 수 있다.
- Source: MathWorks, *Linearize Nonlinear Models*
- Locator: What Is Linearization?, Operating Point Impact
- Link: https://www.mathworks.com/help/slcontrol/ug/linearizing-nonlinear-models.html
- Checked form: official HTML, R2026b
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Local derivative/linearized process gain depends on model state/input around stated operating point, especially for nonlinear plants.

## 11. sensitivity_complementary_sensitivity_tradeoff

- Canonical: `bode_frequency_response_stability_margin_bandwidth` / `sensitivity_robustness_noise_tradeoff`
- Exact original statement: S(s)=1/(1+L(s))와 T(s)=L(s)/(1+L(s))를 이용해 저주파 추종·외란 억제와 고주파 잡음·미모델 동특성 사이의 trade-off를 평가한다.
- Source: MathWorks, *Loop Shaping for Performance and Robustness*
- Locator: Loop Shapes, Performance and Robustness; S=(I+L)^-1, T=L(I+L)^-1
- Link: https://kr.mathworks.com/help/robust/gs/loop-shaping-for-performance-and-robustness.html
- Checked form: official HTML, R2026b
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: For standard negative feedback S=(1+L)^-1, T=L/(1+L), S+T=1 in SISO. Low-frequency high L improves rejection/tracking and high-frequency T constrains uncertainty/noise; MIMO convention must be specified.

## 12. control_valve_cavitation_bubble_collapse_generates_noise

- Canonical: `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` / `cavitation_bubble_collapse_noise`
- Exact original statement: Cavitation bubble collapse는 impulsive pressure와 broadband noise를 만들 수 있다.
- Source: Emerson, *Cavitation in Control Valves*
- Locator: Understanding / Definition / Noise and Vibration
- Link: https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/cavitation
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Pressure recovery after vapor bubble formation can cause collapse, impulsive pressure, objectionable noise/vibration; not every bubbly flow is collapsing cavitation.

## 13. sound_pressure_level_uses_rms_pressure_ratio_at_measurement_location

- Canonical: `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim` / `sound_pressure_level_definition`
- Exact original statement: Sound pressure level은 rms acoustic pressure ratio에 20·log10을 적용한 observation-point level이다.
- Source: OSHA, *OSHA Technical Manual Section III Chapter 5*
- Locator: Appendix B.1 Sound Pressure Level
- Link: https://www.osha.gov/otm/section-3-health-hazards/chapter-5
- Checked form: official HTML, equation
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Lp=20log10(prms/pref) dB at measurement location with reference 20μPa for airborne sound; distinguish instantaneous vs rms averaging and Lp from sound power level.

## 14. ip_transducer_converts_electrical_current_to_pneumatic_pressure_not_valve_travel

- Canonical: `control_valve_positioner_ip_converter_booster_accessories_calibration` / `ip_converter_current_pressure_transduction`
- Exact original statement: I/P converter는 current-to-pressure transducer이며 valve travel feedback controller가 아니다.
- Source: Emerson, *I/P Transducers*
- Locator: What Are Transducers? / Principles of Operation
- Link: https://www.emerson.com/en/final-control/catalog/products-and-software/valve-actuator-regulator-instrumentation/i-p-transducers
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: I/P converts current command into proportional pneumatic pressure; a positioner may be downstream. An I/P alone need not compare actual valve travel.

## 15. three_way_valve_converges_or_splits_flow

- Canonical: `control_valve_types_globe_rotary_body_actuator_selection` / `three_way_mixing_diverting_function`
- Exact original statement: Three-way valve는 두 유로를 혼합하거나 한 유로를 두 방향으로 분기하여 배관과 밸브 수를 줄일 수 있으며 mixing과 diverting 방향은 본체 설계와 압력 조건에 맞춰 적용해야 한다.
- Source: Emerson, *3 Way Control Valves*
- Locator: What is a Three-Way Valve?
- Link: https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/3-way-control-valves
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Three-port mixing/diverting arrangements combine/split streams with actual flow direction dependent on construction and operating pressures; piping simplification possible, not guaranteed.

## 16. displacer_buoyancy_equals_displaced_liquid_weight

- Canonical: `displacer_level_buoyancy_torque_tube_density_interface_calibration` / `displacer_buoyancy`
- Exact original statement: 균일한 액체에서 침수체적 V_sub의 부력은 F_b = rho g V_sub이다. 액위 변화가 침수체적과 겉보기 무게를 바꾼다.
- Source: Emerson, *Fisher 249BP Cageless Sensor*
- Locator: Product Description, Archimedes' Principle
- Link: https://www.emerson.com/en/final-control/products/fisher-249bp
- Checked form: official HTML
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: For homogeneous fluid under hydrostatic conditions Archimedes gives buoyancy ρgVsub; buoyancy changes displacer apparent load with immersed volume/density.

## 17. control_valve_deadband_signal_range_is_distinct_from_dead_time_interval

- Canonical: `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` / `deadband_not_dead_time`
- Exact original statement: 밸브 travel을 관측 출력으로 하는 시험에서 deadband는 입력 방향을 반전한 뒤에도 관측 출력 변화가 시작되지 않는 입력 신호 범위이며, dead time은 step 입력을 시작한 때부터 첫 관측 가능한 응답이 나올 때까지의 시간이다. 따라서 deadband는 신호 크기 범위, dead time은 시간 간격이며 시험의 입력·출력 변수를 명시해 서로 구분한다.
- Source: Emerson, *Control Valve Handbook, 6th edition*
- Locator: Ch.2 §§2.1.1 and 2.1.3; Ch.5 §§5.5-5.6, Liquid and Gas Sizing, N1 and properties
- Link: https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf
- Checked form: publisher indexed PDF text; screenshot failed (large file)
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Deadband is input signal reversal band with no output/travel change; dead time is elapsed time from step input until detectable movement, different dimensions and protocol dependent.

## 18. control_valve_response_time_separates_dead_time_and_dynamic_time

- Canonical: `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` / `response_time_dead_dynamic_separation`
- Exact original statement: Valve response time은 command 변화 후 움직임 시작 전 dead time과 움직임 시작 후 목표 변화에 접근하는 dynamic time으로 구분할 수 있다.
- Source: Emerson, *Control Valve Handbook, 6th edition*
- Locator: Ch.2 §§2.1.1 and 2.1.3; Ch.5 §§5.5-5.6, Liquid and Gas Sizing, N1 and properties
- Link: https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf
- Checked form: publisher indexed PDF text; screenshot failed (large file)
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Chapter 2 §2.1.3 T63 is delay before motion plus elapsed dynamic part to 63% of response; alternate test definitions must be declared.

## 19. control_valve_gas_sizing_selects_property_input_by_equation_form

- Canonical: `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` / `gas_property_input_selection`
- Exact original statement: Gas sizing은 선택한 equation form에 따라 molecular weight, gas specific gravity 또는 inlet density를 사용한다.
- Source: Emerson, *Control Valve Handbook, 6th edition*
- Locator: Ch.2 §§2.1.1 and 2.1.3; Ch.5 §§5.5-5.6, Liquid and Gas Sizing, N1 and properties
- Link: https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf
- Checked form: publisher indexed PDF text; screenshot failed (large file)
- Verdict: **KEEP_BOUNDED**
- Validity conditions and caveat: Gas sizing forms can use molecular weight, SG or inlet density depending on selected formulation and flow unit basis; always use absolute pressure/temperature and appropriate compressibility.


## Review limitations

Records do not include source hash/reviewer approval runs, full standard license review, or release-test results. Non-core detail is not made an independent scoring demand by appearance in this report.