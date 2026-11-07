# Sixteen canonical engineering Fact Anchor primary comparisons — 2026-11-01

Reviewer GPT-6 (AI, 2026-11-01); branch codex/essay-boundary-calibration-20261028. The **actual original canonical Fact Anchor statement** was fetched and independently compared against named manufacturer/professional technical source. Verdict KEEP_BOUNDED reflects only this proposition under the specified physical/service assumptions, NOT an automatic general mandatory grading reference. Users require broadly applicable general facts; niche implementation is contextual.

PDF pages: Yokogawa p5-1 screenshot (zero-index24), Emerson Fp p637 screenshot (zero-index11) visually checked. Siemens ratio manual from original PDF text, screenshot attempted and failed 403 — not visually certified. HTML references have directly accessible original publisher text.

## 1. humidity_field_check_and_calibration_require_reference_equilibration

- Canonical topic/anchor: `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` / `calibration_traceability_field_check`
- Original statement: 습도센서는 salt solution, humidity generator, reference hygrometer 또는 chilled mirror 등 적합한 reference와 비교하여 calibration할 수 있으며 field check와 full calibration의 목적을 구분하고 traceability와 equilibration time을 관리한다.
- Source: Vaisala HMK15 User Guide M210185EN-E
- Publisher URL: https://docs.vaisala.com/r/M210185EN-E/en-US/GUID-9699E3D8-9ACC-4A9C-BECE-200EB22B378C/GUID-C07F31DF-A6EF-43F4-94EC-C6AF46F7DE0A
- Locator: On-site calibrations; temperature stabilization (30–120 min)
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Manufacturer documents traceable salt humidity references, stabilization and comparison; field check must be distinguished from laboratory full-calibration certificates. Reference hygrometer, generator, and chilled mirror may be alternatives but exact selection requires procedure.

## 2. capacitive_rh_measurement_requires_sensor_temperature_context

- Canonical topic/anchor: `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` / `capacitive_sensor_temperature_compensation`
- Original statement: Capacitive RH sensor는 polymer response, electronics와 RH 정의 자체가 temperature의 영향을 받으므로 colocated temperature sensing과 calibration coefficient를 이용한 temperature compensation이 중요하다.
- Source: Vaisala HUMICAP User Guide M212022EN-M
- Publisher URL: https://docs.vaisala.com/r/M212022EN-M/en-US/GUID-CECDAD3B-5A62-4C0E-8C2D-BB496612A906
- Locator: HUMICAP technology: capacitance, composite temperature sensor
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Humidity polymer changes capacitance with absorbed vapor, temperature sensor supplies RH T context; model-specific calibration coefficients and electronic temperature correction, not one universal algorithm.

## 3. pressure_changes_compressed_gas_dew_point_parameter

- Canonical topic/anchor: `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` / `pressure_dew_point_effect`
- Original statement: Dew point는 pressure condition의 영향을 받으므로 compressed gas에서는 pressure dew point와 atmospheric-equivalent dew point를 혼동하지 않는다. 압력변화 시 같은 moisture content라도 condensation condition이 달라질 수 있다.
- Source: Vaisala Dew Point in Compressed Air
- Publisher URL: https://www.vaisala.com/en/blog/2019-09/what-dew-point-and-how-measure-it
- Locator: Effect of pressure on dew point
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Pressure changes vapor partial pressure and dew point even if gas moisture ratio conserved; compare pressure dewpoint and ambient equivalent at same declared gas pressure basis.

## 4. gas_impulse_lines_should_drain_condensate_away_from_low_points

- Canonical topic/anchor: `instrumentation_installation_wiring_impulse_tubing_inspection_codes` / `iiwic_gas_service_principle`
- Original statement: Gas service에서는 condensate가 impulse path에 고여 hydrostatic error를 만들지 않도록 condensate 배출 방향과 transmitter 위치를 process 조건에 맞게 구성한다.
- Source: Yokogawa EJA Pressure Transmitters User Manual IM01C21D01-01E 12e
- Publisher URL: https://web-material3.yokogawa.com/IM01C21D01-01EN.pdf
- Locator: §5.1.2(1)-(2), actual page 5-1, PDF zero-based page 24 screenshot visually inspected
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Gas impulse line should avoid liquid condensate hydrostatic bias; tap/transmitter elevation enables drain back to process per service geometry. Specific 45° manufacturer install geometry not general rule.

## 5. liquid_impulse_lines_must_manage_trapped_gas_and_liquid_head

- Canonical topic/anchor: `instrumentation_installation_wiring_impulse_tubing_inspection_codes` / `iiwic_liquid_service_principle`
- Original statement: Liquid pressure/DP service에서는 impulse path가 액으로 유지되고 trapped gas가 측정오차를 만들지 않도록 routing·venting·transmitter 위치를 service 조건에 맞게 구성한다.
- Source: Yokogawa EJA Pressure Transmitters User Manual IM01C21D01-01E 12e
- Publisher URL: https://web-material3.yokogawa.com/IM01C21D01-01EN.pdf
- Locator: §5.1.2(1)-(2), actual page 5-1, PDF zero-based page 24 screenshot visually inspected
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Liquid impulse line must avoid trapped gas, be vented and route to reduce gas pockets; actual liquid-head and transmitter elevation compensation in measurement are service-specific.

## 6. feedforward_ideal_cancellation_and_realizability_boundary

- Canonical topic/anchor: `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` / `feedforward_principle`
- Original statement: Feedforward 제어는 측정 가능한 외란 d를 이용해 controlled variable이 변하기 전에 조작량을 보정하는 구조이다. 선형 모델 y=G_u u+G_d d에서 이상적 보상은 조건이 허용되면 G_ff=-G_d/G_u로 표현할 수 있으나 실제 구현은 안정성·인과성·properness·model uncertainty를 고려한 실현 가능한 근사여야 한다.
- Source: MathWorks What is Feedforward Control? official transcript 2018
- Publisher URL: https://www.mathworks.com/videos/control-systems-in-practice-part-3-what-is-feedforward-control-1535712796292.html
- Locator: Transcript lines 103–124, dynamic inversion, Gd/Gp cancellation, causal approximation
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: For Y=Gu U+Gd D, ideal U=-(Gd/Gu)D by algebra when Gu invertible; noncausal/time-delay inverse and imperfect models require realizable approximation, assumptions stated.

## 7. process_cascade_requires_useful_relative_secondary_dynamics

- Canonical topic/anchor: `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` / `cascade_secondary_faster`
- Original statement: Cascade가 효과적이려면 secondary loop가 primary loop보다 충분히 빠르게 응답해야 하며, secondary loop의 동특성이 느리면 두 루프의 상호작용으로 오히려 응답이 악화될 수 있다. 특정 속도비를 모든 공정의 절대 기준으로 고정해서는 안 된다.
- Source: MathWorks Designing Cascade Control System with PI Controllers R2026b
- Publisher URL: https://www.mathworks.com/help/control/ug/designing-cascade-control-system-with-pi-controllers.html
- Locator: Introduction to Cascade Control: faster inner loop than outer
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Inner faster than outer needed for useful local disturbance rejection. No universal numeric speed ratio; excessive interaction can defeat performance.

## 8. ratio_control_wild_flow_scales_secondary_setpoint

- Canonical topic/anchor: `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` / `ratio_control_structure`
- Original statement: Ratio 제어는 기준이 되는 wild/master stream과 조작되는 controlled stream 사이의 비를 유지하는 구조이며, 비의 정의를 명시하면 일반적으로 controlled-flow setpoint를 SP_c=R·F_w와 같이 생성해 secondary flow controller가 조작한다.
- Source: Siemens SIMATIC S7-300/S7-400 Implementing Ratio or Mixture Controllers
- Publisher URL: https://docs.tia.siemens.cloud/r/en-us/v21/pid-control/pid-control-s7-300-s7-400/using-fm-455-s7-300-s7-400/parameter-assignment-fm-455-s7-300-s7-400/deviation-s7-300-s7-400/implementing-ratio-or-mixture-controllers-s7-300-s7-400?contentId=hjXcRseR~k4J_M63isZXbQ
- Locator: Determining multipliers, flow setpoint multiplying ratio factor and safety setpoint limits
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Slave flow setpoint is master/wild flow times configured ratio (possibly with offset/scaling); streams must be in compatible quantities/units.

## 9. ratio_scaling_and_low_flow_division_sensitivity

- Canonical topic/anchor: `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` / `ratio_scaling_and_low_flow`
- Original statement: Ratio 제어에서는 두 측정값의 단위·범위·밀도 또는 보정 기준을 일치시켜야 하며, wild stream이 매우 작거나 0에 가까운 영역에서는 나눗셈형 ratio 계산과 noise가 불안정해질 수 있어 low-flow logic, limit 또는 startup mode가 필요하다.
- Source: Siemens SIPART DR22 Controller Manual C73000-B7476-C222-10
- Publisher URL: https://support.industry.siemens.com/cs/attachments/29200540/6DR2200_Manual_C222_10_en.pdf
- Locator: Ratio controller section: x1/x2 unstable near zero, limited to 0.5%; indexed PDF text confirmed, screenshot attempted 403
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: SIEMENS x1/x2 ratio becomes unstable at small denominator; use guarded low-flow logic and scaling. Vendor 0.5% guard is model example only; other units, startup/bypass rules application-specific.

## 10. state_tracking_prefilter_is_nominal_feedforward_not_disturbance_feedback

- Canonical topic/anchor: `state_feedback_reference_tracking_prefilter_integral_action` / `state_tracking_prefilter_existence_model_dependence`
- Original statement: 프리필터는 모델 기반 기준입력 feedforward 보상으로서 폐루프 DC 이득이 가역해야 하며, 모델 오차와 외란을 적분 피드백처럼 자동 제거하지는 않는다.
- Source: MathWorks Single Loop Feedback/Prefilter Compensator Design R2026b
- Publisher URL: https://www.mathworks.com/help/control/ug/single-loop-feedbackprefilter-compensator-design.html
- Locator: Design Overview: prefilter tunes reference tracking, feedback PID rejects external disturbance
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Nominal reference prefilter uses invertible nonzero closed-loop DC gain for exact step scaling; unknown disturbances/model errors require feedback/integral or disturbance control, not static prefilter.

## 11. hazop_lopa_lopa_frequency_equation

- Canonical topic/anchor: `hazop_lopa_ipl_risk_reduction_sil_target_allocation` / `hazop_lopa_lopa_frequency_equation`
- Original statement: LOPA의 residual scenario frequency는 initiating event frequency에 적용 가능한 조건부 수정인자와 독립보호계층의 PFD를 곱하여 산정한다.
- Source: ISA InTech, HAZOP and LOPA to Calculate a SIS (2016)
- Publisher URL: https://www.isa.org/intech-home/2016/january-february/features/safety-instrumented-system-sil-calculation
- Locator: LOPA worksheet and SIL calculation equations, initiating freq × mitigation factors, target freq
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Intermediate scenario frequency is initiating rate times conditionally applicable IPL probabilities/modifiers, with independence credited only where justified; multiple scenarios/shared layers need careful aggregation.

## 12. radar_interference_and_multiple_reflection_echoes

- Canonical topic/anchor: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` / `radar_false_echo_multiple_reflection`
- Original statement: 노즐, 탱크 벽, 교반기, 보강재 및 가열코일은 허위에코를 만들 수 있고 탱크 구조와 표면 사이의 다중반사는 잘못된 거리피크를 만들 수 있다.
- Source: Emerson Smart Echo Supervision FAQ
- Publisher URL: https://www.emerson.com/en/measurement-instrumentation/catalog/level-measurement/smart-echo-supervision
- Locator: Frequently Asked Questions: agitators, coils, nozzles create false radar returns
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Internal tank structures, coils, agitators and nozzles generate false competing returns; multiple interactions may produce spurious peaks. Exact suppression algorithm vendor-specific.

## 13. radar_beam_footprint_and_obstruction_echo

- Canonical topic/anchor: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error` / `radar_antenna_beam_footprint`
- Original statement: 안테나 빔각과 측정거리가 조사면적을 결정하며 빔 경로에 벽, 노즐 또는 내부구조물이 들어오면 허위에코 가능성이 증가한다.
- Source: Emerson Smart Echo Supervision FAQ
- Publisher URL: https://www.emerson.com/en/measurement-instrumentation/catalog/level-measurement/smart-echo-supervision
- Locator: Frequently Asked Questions: agitators, coils, nozzles create false radar returns
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: If antenna cone angle fixed, footprint radius ∝ range via elementary geometry; obstructions in illuminated path can create false echoes. No fixed universal beam width/angle.

## 14. control_valve_fp_depends_on_valve_and_attached_geometry

- Canonical topic/anchor: `control_valve_sizing_cv_kv_reynolds_liquid_selection` / `piping_factor_geometry_dependency`
- Original statement: Fp는 valve size, pipe size, fitting type, reducer·expander geometry와 selected valve coefficient에 따라 달라질 수 있다.
- Source: Emerson Fisher Technical Valve Sizing Calculations d351798x012
- Publisher URL: https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d351798x012_11.pdf
- Locator: Page 637, Determining Piping Geometry Factor (Fp), screenshot PDF zero-index 11 visually checked
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Fp formula depends on Cv, nominal valve size d, piping size D, fittings resistance coefficients ΣK; use actual reducers/expanders; Fp=1 only under no attached fittings defined test setup.

## 15. pid_derivative_damping_noise_and_kick

- Canonical topic/anchor: `pid_controller_tuning_sequence_gain_effects` / `d_action_effect`
- Original statement: D 동작은 오차 변화율을 이용한 예측·감쇠 동작으로 overshoot와 진동 저감에 기여할 수 있으나, 센서 노이즈와 미분 kick에 민감하여 필터와 함께 제한적으로 사용한다.
- Source: MathWorks Two-Degree-of-Freedom PID Controllers R2026b
- Publisher URL: https://www.mathworks.com/help/control/ug/two-degree-of-freedom-2-dof-pid-controllers.html
- Locator: Parallel u=Kp(br-y)+Ki/s(r-y)+Kds/(Tfs+1)(cr-y), setpoint derivative and filter
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Derivative term acts on fast error variations and may increase damping, but differentiates sensor noise and reference-step derivative can kick if derivative on error (c=1). Filtering and c=0 derivative-on-measurement are application mitigations.

## 16. pid_proportional_error_response_tradeoff

- Canonical topic/anchor: `pid_controller_tuning_sequence_gain_effects` / `p_action_effect`
- Original statement: P 동작은 현재 오차에 비례하여 제어 출력을 만들며 응답 속도와 오차 보상에 기여하지만, 과도하면 overshoot, hunting, 진동, 불안정을 증가시킬 수 있다.
- Source: MathWorks PID Tuning Algorithm / Assessing Gain and Phase Margins R2026b
- Publisher URL: https://www.mathworks.com/help/control/ug/assessing-gain-and-phase-margins.html
- Locator: Increased loop gain lowers margin/produces larger oscillations, sometimes instability
- Technical verdict: **KEEP_BOUNDED**
- Evidence mapping and bounded conditions/counterexamples: Increasing proportional loop gain can speed reaction but reduce stability margin and increase oscillation/overshoot depending plant. Controller sign/dynamics and saturation prevent universal monotonic response.


Reviewed evidence records do not edit original Topic Pack, generated bank, or scoring admission overlay; runtime tests/CI not run. A bounded source match remains subject to eligibility policy and duplicate/noncore exclusions.