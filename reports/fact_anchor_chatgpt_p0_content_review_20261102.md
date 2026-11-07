# P0 Fact Anchor content review (ChatGPT)

Reviewed 2026-11-02 by **gpt-6-luna** against the first-party/primary URLs in the 80-row review queue. This review covers its 17 `P0` records only. “KEEP_WITH_CORRECTION” means the bounded proposition is supportable as wording; it does not approve a Topic Pack/Registry edit or lift any scoring hold. “HOLD” means the opened evidence does not establish the claim closely enough. “EXCLUDE” means the described item is not a suitable general-scoring anchor, even if a narrow example may be true. No scoring hold was removed.

## Decisions

### 1. `four_to_twenty_milliamp_repair_requires_end_to_end_reverification` — HOLD

**Current claim:** After restoring a 4–20 mA loop, verify low/mid/high points at the installed loop and receiver, scaling, alarm/fault-current behavior, and returned-to-service state.

**Sources and locator:** Rockwell Automation, [P_AIChan Reference Manual](https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/syslib-rm042_-en-p.pdf), pp. 11 and 27 (PDF pp. 11, 27), lines 310–313 and 849–871: configurable raw input and engineering-unit ranges; explicit example mapping 4–20 mA to −50…250 °C. Emerson, [Rosemount 8750W manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/flow-magnetic/documents/manual-rosemount-8750w-magnetic-flowmeter-platform-for-utility-water-and-wastewater-applications.pdf), could not be fetched by the browser (oversized PDF).

**Conditions/counterexample:** Rockwell supports scaling configuration for this specific library object, not the post-repair 3-point end-to-end test, alarm/fault behavior, acceptance, or documentation practice. The Emerson source was not inspectable. Different receiving equipment and loop functions may have different diagnostics and proof-test requirements. **Decision: HOLD** for the full maintenance proposition; no repair procedure should be elevated from these sources alone.

**Proposed wording:** None pending a directly accessible maintenance or commissioning procedure explicitly supporting the proposed verification steps.

### 2. `second_order_margin_damping_overshoot_bandwidth_trend` — KEEP_WITH_CORRECTION

**Current claim:** In dominant-second-order-like systems, phase margin approximates damping (ζ roughly PM/100 below about 70°); more damping reduces second-order overshoot, and higher natural frequency at fixed damping increases bandwidth and speeds response.

**Sources and locator:** MIT OpenCourseWare, [16.30 Topic 4: Control Design using Bode Plots](https://ocw.mit.edu/courses/16-30-feedback-control-systems-fall-2010/06f5c464cfe3b1ed6f93fafcef241d8f_MIT16_30F10_lec04.pdf), PDF pp. 4–5, lines 39–41 and 74–91: second-order time response and plotted relationships among damping ratio, bandwidth, crossover, and resonant frequency. MathWorks, [Design Requirements](https://www.mathworks.com/help/control/ug/design-requirements.html), “Percent Overshoot,” lines 94–100, states the overshoot requirement can be expressed in terms of damping ratio. The source does not support the linear PM/100 approximation at every value below 70°.

**Conditions/counterexample:** Exact overshoot/damping relation assumes the standard underdamped second-order response. Phase margin is only a heuristic damping proxy under suitable loop shape and dominant-pole assumptions; higher-order, nonminimum-phase, delayed, or resonant systems can violate the intuition. Avoid presenting PM/100 as a quantitative law.

**Proposed wording:** “For an underdamped standard second-order response, increasing damping ratio reduces percent overshoot; at fixed damping ratio, increasing natural frequency raises the response frequency scale and generally shortens response time. Phase margin may serve as a qualitative damping proxy for suitably dominant second-order-like loops, but the relationship is model-dependent.”

### 3. `sw02_debounce_hysteresis_reduce_chatter_with_response_time_tradeoff` — KEEP_WITH_CORRECTION

**Current claim:** Debounce/time qualification rejects short contact bounce; hysteresis reduces repeated switching around a noisy threshold; both affect detection and may miss short valid pulses/add delay, so settings depend on nuisance events and required protective response.

**Sources and locator:** Siemens, [Configuring digital input filter times, S7-1200 V20](https://docs.tia.siemens.cloud/r/simatic_s7_1200_manual_collection_enus_20/device-configuration/configuring-the-operation-of-the-cpu/configuring-digital-input-filter-times), section “The digital input filter works as follows,” lines 1089–1106: transitions are accumulated to the filter time; short transitions can be undetected and unexpected operation may result. Analog Devices, [Curing Comparator Instability with Hysteresis](https://www.analog.com/en/resources/analog-dialogue/articles/curing-comparator-instability-with-hysteresis.html), section “Variables affecting hysteresis” (lines 56 onward), covers comparator hysteresis; direct line extraction of the stated anti-chatter mechanism was limited.

**Conditions/counterexample:** Siemens is a particular PLC product and its configurable times are not general safety settings. Digital input filtering and analog comparator hysteresis are distinct techniques. A short legitimate pulse can be suppressed; neither should be used where it violates required response or pulse-capture behavior.

**Proposed wording:** “Input filtering/time qualification can reject transitions shorter than the configured qualification interval, and comparator hysteresis can reduce repeated switching near a noisy threshold. Both alter detection behavior; select implementation and settings against the required response and valid pulse duration.”

### 4. `calibration_reference_standard_uncertainty_traceability_control` — KEEP_WITH_CORRECTION

**Current claim:** A calibration reference must suit required accuracy/uncertainty and tolerance; identity/status/environment/handling history are controlled as required; traceability is an unbroken documented calibration chain with uncertainty at each link; no universal accuracy ratio.

**Sources and locator:** NIST, [Metrological Traceability: FAQ and Policy](https://www.nist.gov/metrology/metrological-traceability), §5.2.1 lines 373–375: traceability is an unbroken chain of calibrations, each contributing to uncertainty. Lines 415–419 describe determining uncertainties at each step and the specified references. NIST does not establish a universal accuracy-ratio criterion in this material.

**Conditions/counterexample:** Traceability alone does not establish fitness for purpose, nor does it guarantee that a standard’s uncertainty is small enough for a particular tolerance. Control of status, handling, and environment depends on the measurement program and applicable quality system.

**Proposed wording:** “For a calibration result requiring metrological traceability, document an unbroken calibration chain to stated references and account for uncertainty contributions at each link. Select and maintain the reference standard to meet the measurement’s stated uncertainty/tolerance needs; no fixed accuracy ratio follows universally.”

### 5. `valve_authority_has_no_universal_acceptance_threshold` — KEEP_WITH_CORRECTION

**Current claim:** No universal authority pass/fail value applies across all control-valve systems; acceptable allocation depends on definition, operating range, controllability, energy cost, system limits, and process requirements.

**Sources and locator:** Valmet, [What is a control valve authority?](https://www.valmet.com/insights/articles/flow-control/control-valve-authority---ask-the-flow-control-expert/), lines 138 onward: high authority means valve takes most total system pressure drop; low authority means piping loss is significant relative to valve loss; the term is “not standardized internationally.” Valmet, [Control Valve Installed Performance](https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/), §2.1 lines 88–91, describes calculation of installed performance and use of installed accuracy.

**Conditions/counterexample:** The sources support differing definitions and an application-dependent installed-performance calculation. They do not prove that no industry or project standard ever sets a threshold. A specified project criterion remains binding within its own scope.

**Proposed wording:** “Valve authority conventions and definitions are not internationally standardized; therefore, compare values only after declaring the convention/system boundary. Acceptance is project- and operating-condition-specific, not a universal threshold.”

### 6. `valve_authority_is_defined_for_declared_operating_condition` — KEEP_WITH_CORRECTION

**Current claim:** Authority is a dimensionless measure of valve share of defined system pressure-drop budget at stated condition; conventions vary and comparison requires declared formula/system boundary.

**Sources and locator:** Valmet, [What is a control valve authority?](https://www.valmet.com/insights/articles/flow-control/control-valve-authority---ask-the-flow-control-expert/), lines 138 onward defines high/low authority by valve pressure-drop share relative to total/pipeline loss and expressly notes no international standardization.

**Conditions/counterexample:** The source supports the pressure-drop-share concept and lack of standardized definition, but does not enumerate the alternate closed-valve-normalized formula described in the current wording. Definitions are convention-dependent.

**Proposed wording:** “Valve authority describes the control valve’s share of a stated system pressure-drop basis at an operating condition. Since conventions are not internationally standardized, state the equation and system boundary before comparing authority values.”

### 7. `installed_characteristic_selection_checks_system_operating_cases` — KEEP_WITH_CORRECTION

**Current claim:** Selection should assess installed rather than only inherent characteristic; installed relation depends on system pressure; use minimum/normal/maximum cases within operating envelope.

**Sources and locator:** Emerson, [Control Valve Sourcebook—Refining](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/control-valve-sourcebook-refining-en.pdf), glossary “Inherent Valve Gain” and “Installed Characteristic,” PDF p. 113, lines 9596–9602, distinguishes constant-pressure-drop inherent gain from installed characteristic. Valmet, [Control Valve Installed Performance](https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/), §2.1 lines 88–91, describes predicting installed performance with a pipeline model and sizing/selection software.

**Conditions/counterexample:** The Emerson source is refinery-oriented and does not establish a universal mandate to calculate exactly min/normal/max cases. Case selection should follow the specified operating envelope. Installed characteristic depends on the complete system, not only pump head or valve trim.

**Proposed wording:** “For a specified control-valve operating envelope, assess the installed flow characteristic using the relevant valve and system pressure conditions; the inherent curve alone does not describe installed performance. Evaluate the operating cases needed by the project’s envelope and control objective.”

### 8. `positioner_calibration_as_found_as_left_recording_scope` — KEEP_WITH_CORRECTION

**Current claim:** Preserve as-found before adjustment and as-left after calibration/verification; DVC6200 signature captures as-found; NIST recommends pre/post data; exact fields depend on instrument/procedure.

**Sources and locator:** Emerson, [Fisher FIELDVUE DVC6200 HW1 manual](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/im-fieldvue-dvc6200-hw1-digital-valve-controller-retired-product-d103409x012.pdf), PDF p. 85 (printed p. 80), “Sensor Calibration,” lines 3763–3766: before calibration for suspected drift, perform Valve Signature diagnostic using ValveLink; this captures as-found data for root-cause analysis. NIST [Recommended Calibration Interval](https://www.nist.gov/calibrations/recommended-calibration-interval) is cited in the source list, but its direct page does not establish a universal as-left record requirement.

**Conditions/counterexample:** DVC6200 signature is product-specific, diagnostic data is not identical to a complete calibration report, and the manual does not call for as-left data in this passage. The record requirement should be tied to the governing work procedure.

**Proposed wording:** “When calibration work requires a before/after comparison, retain the pre-adjustment condition and post-adjustment verification results under the governing procedure. A DVC6200 valve-signature test is one manufacturer-specific means of capturing as-found data.”

### 9. `feedback_stability_bandwidth_tradeoff` — KEEP_WITH_CORRECTION

**Current claim:** Bandwidth may improve tracking/disturbance response but trades against margins; delay lowers phase and limits bandwidth/stability; assess out-of-band noise and unmodeled dynamics; high bandwidth is not an unconditional goal.

**Sources and locator:** MathWorks, [Analyze Control Systems with Delays](https://www.mathworks.com/help/control/ug/analyzing-control-systems-with-delays.html), §“Control of Processes with Delays,” lines 21–24: delay causes linear phase shifts that limit control bandwidth and affect closed-loop stability. MathWorks, [Modeling Uncertainty](https://www.mathworks.com/help/robust/gs/modeling-uncertainty.html), lines 17–20: balancing low-frequency disturbance/bias rejection against sensor noise and model uncertainty, with high-frequency roll-off. MathWorks, [PID tuning for setpoint tracking vs. disturbance rejection](https://www.mathworks.com/help/control/ug/pid-tuning-for-setpoint-tracking-vs-disturbance-rejection.html) is listed in the queue but not needed for the bounded claim.

**Conditions/counterexample:** These are control-design tradeoffs, not a monotonic guarantee that raising bandwidth improves all tracking or disturbance performance. Noise/model uncertainty and delay can dominate. Numerical target margins remain application-specific.

**Proposed wording:** “Control bandwidth is selected as a design tradeoff: process delay adds phase lag and limits achievable bandwidth, while feedback gain/bandwidth must be balanced against stability margin, sensor-noise amplification, and model uncertainty. The suitable bandwidth depends on the loop and its requirements.”

### 10. `hazop_lopa_no_additional_sif_when_ratio_below_one` — HOLD

**Current claim:** In a defined LOPA scenario, required RRF ≤ 1 means the frequency criterion alone creates no further SIF requirement, while other scenarios and ALARP remain separate.

**Source and locator:** AIChE/CCPS, [LOPA Data](https://ccps.aiche.org/resources/tools/lopa), opened page; it is a resource landing page. No statement or locator establishing the RRF ≤ 1 rule was present in the page text. A primary LOPA methodology source/clause was not supplied or verified.

**Conditions/counterexample:** LOPA terminology and allocation rules depend on the method, initiating-event frequency, enabling conditions, consequence target, and credited IPLs. The apparent arithmetic interpretation of a risk-reduction factor does not independently establish whether a SIF is required or how ALARP is treated.

**Proposed wording:** None until a directly inspectable CCPS/standard methodology clause establishes this exact decision rule and its assumptions.

### 11. `batch_genealogy_links_material_lots_with_execution_context_when_records_are_captured` — KEEP_WITH_CORRECTION

**Current claim:** Genealogy may link material lots/sublots to equipment, batch/recipe/execution records, process conditions and quality results for traceability; ISA-95 and ISA-88 model relevant structures; completeness depends on site capture/correlation.

**Sources and locator:** OPC Foundation, [OPC UA Common Object Model: ISA-95, full text](https://reference.opcfoundation.org/specs/OPC-10030/full), §8.4.3.4, lines 2087–2118: identified MaterialLot and optional TestedByMaterialTest, AssembledFromLot/Sublot, Status, StorageLocation, Quantity references. ISA, [ANSI/ISA-88.00.04-2006 preview](https://www.isa.org/getmedia/4b46d97c-6954-4936-97f5-db672f3fd154/S_880004_preview.pdf), PDF p. 1, lines 12–16: Part 4 defines batch production record contents and is a reference model for storing/exchanging records, allowing retrieval, analysis, and reporting of selected data.

**Conditions/counterexample:** These are information models/reference models, not proof that every implementation automatically captures equipment, all conditions, quality, genealogy, or recall completeness. Several referenced attributes/relations are optional. Site configuration and data capture are necessary.

**Proposed wording:** “A manufacturing information model can represent identified material lots and sublots, their assembly relationships, and batch production records for retrieval and analysis. The actual genealogy and context available depend on the records and links an implementation captures.”

### 12. `production_ai_monitoring_tracks_behavior_against_contextual_baselines` — KEEP_WITH_CORRECTION

**Current claim:** In operation, monitor differences between predeployment and operational performance/input-output distributions, data/sensor quality, system function/anomalies; reassess performance when ground truth appears; metrics and thresholds depend on risk/context.

**Sources and locator:** NIST AI RMF Core, [Measure function](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/), lines 192–194: measurement analyzes/assesses/benchmarks/monitors AI risk and impacts; systems should be tested before deployment and regularly in operation; document functionality and trustworthiness. NIST AI RMF Playbook, [Measure](https://airc.nist.gov/airmf-resources/playbook/measure/), line 921 and surrounding metric guidance, asks whether metrics accurately/usefully measure performance.

**Conditions/counterexample:** NIST supports regular operational testing and context-relevant risk measurement, not a prescribed universal metric list, baseline-drift trigger, or ground-truth availability schedule. “Sensor quality” is deployment-specific.

**Proposed wording:** “Test AI systems before deployment and regularly during operation; select risk-relevant measures for functionality and trustworthiness in the deployment context, and document their limits. The RMF does not prescribe one fixed metric list or threshold for all systems.”

### 13. `training_data_representativeness_is_intended_use_specific` — KEEP_WITH_CORRECTION

**Current claim:** Training/evaluation material should suit and represent intended equipment/operation/deployment context; listed factors are examples; document sampling context, quality, ground-truth/label limits and bias.

**Sources and locator:** NIST AI RMF Playbook, [Measure](https://airc.nist.gov/airmf-resources/playbook/measure/), lines 221–226: evaluations involving human subjects should be representative of the relevant population; non-representative data may produce inaccurate assessments or harmful outcomes; full operational representativeness can be difficult or impossible. NIST AI RMF Core [Measure](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/), lines 192–194 supports context-informed risk measurement and regular testing.

**Conditions/counterexample:** The explicit representativeness source excerpt concerns human-subject evaluations; applying it to all industrial sensor/training datasets is a principled extension, but not directly stated in that passage. Normal/fault/mode/season/maintenance dimensions are examples, not universal required strata.

**Proposed wording:** “Assess whether training and evaluation data adequately reflect the intended use and deployment context, and document material gaps, quality limits, and known bias. Choose relevant coverage dimensions for the application; no single checklist applies to every project.”

### 14. `ipgse_dc_distribution_capacity_drop_selectivity_and_return_path_review` — HOLD

**Current claim:** DC instrumentation distribution should be assessed for supply capacity/load-step response, conductor voltage drop, branch protection/selectivity, and shared-return impedance effects on signal reference.

**Sources and locator:** NI, [Field Wiring and Noise Considerations for Analog Signals](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html), opened source; relevant topic is field wiring and noise, but the current browser extraction did not expose a specific locator supporting shared-return impedance or the complete checklist. NI, [Cabling and Current-Resistance Loss Considerations](https://www.ni.com/en/shop/electronic-test-instrumentation/power-supplies-and-loads/what-are-programmable-power-supplies/cabling-and-current-resistance-loss-considerations-for-programma.html), opened source; discusses cable resistance/current-related loss in the context of programmable DC sources. Siemens SITOP technical document could not be fetched (oversized PDF).

**Conditions/counterexample:** The claim bundles supply sizing, dynamic response, voltage drop, protection coordination, and common-impedance coupling. The available opened pages do not establish the whole list as a general mandatory review. NI programmable-source cabling advice is equipment-context specific.

**Proposed wording:** None pending exact accessible clauses covering the full distribution design claim. Individually supported electrical principles may be retained as separate, condition-bounded facts.

### 15. `nyquist_field_validation_separates_linear_margins_from_nonlinear_constraints` — KEEP_WITH_CORRECTION

**Current claim:** For a negative-feedback loop, Nyquist margin is assessed around −1; practical robustness review considers operating-point linearizations and gain/phase/delay margins, uncertainty/noise; linear margins do not certify saturated behavior, which needs separate nonlinear assessment/anti-windup consideration.

**Sources and locator:** MathWorks, [allmargin](https://www.mathworks.com/help/control/ref/dynamicsystem.allmargin.html), lines 29–34: computes gain, phase, delay margins and crossover frequencies for a specified SISO/MIMO negative-feedback loop. MathWorks, [Modeling Uncertainty](https://www.mathworks.com/help/robust/gs/modeling-uncertainty.html), lines 17–20: feedback design balances disturbances against sensor noise and model uncertainty. MathWorks, [Anti-Windup Control Using PID Controller Block](https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html), lines 13–19: saturation can cause integration windup; example demonstrates anti-windup approaches.

**Conditions/counterexample:** The cited `allmargin` page computes classical margins; it does not define a Nyquist “stability margin around −1” as a single scalar nor claim that field validation must use all named checks. Saturation is nonlinear, so classical linear margins alone do not establish saturated closed-loop performance. Anti-windup is one remedy, not universally required.

**Proposed wording:** “Classical gain, phase, and delay margins characterize a specified linearized negative-feedback model. They do not by themselves establish performance under actuator saturation; assess relevant nonlinear actuator limits separately when they occur in the operating envelope. Margin targets and operating cases are application-specific.”

### 16. `hamamatsu_direct_tof_uses_wavelength_centered_filter_for_background` — EXCLUDE

**Current claim:** Hamamatsu’s pulsed direct-ToF receiver uses a band-pass filter centered on transmitted wavelength λ₀ to reduce background light, explicitly as an example rather than universal requirement.

**Source and locator:** Hamamatsu, [Measuring distance with light](https://hub.hamamatsu.com/us/en/application-notes/automotive/measuring-distance-with-light.html), opened actual application note. Its extracted discussion covers direct/indirect ToF and interferometry (e.g. lines 126–128, 270–286, 330–331); searching the opened page for “band-pass” and “filter” returned no matching text. Therefore the cited URL does not substantiate this receiver-filter claim.

**Conditions/counterexample:** Even if a Hamamatsu product note elsewhere verifies this implementation, it remains a manufacturer-specific optical design example, explicitly non-universal, and is ineligible as a general engineering scoring anchor under the policy’s vendor-detail exclusion. It could appear as unscored context in a Hamamatsu-specific question with a direct source.

**Proposed wording:** None for general scoring. Keep only as vendor-specific context if another exact Hamamatsu source supports it.

### 17. `rtd_calibration_uncertainty_depends_on_reference_bath_readout_and_sensor_application_effects` — KEEP_WITH_CORRECTION

**Current claim:** When calibration/range characterization is required, compare assembled chain to traceable reference in stable, characterized source across range; account for reference/source/readout and RTD effects including self-heating, immersion/contact, lead resistance, repeatability/stability; no fixed point count.

**Sources and locator:** BIPM/CCT, [Guide to Secondary Thermometry: Industrial Platinum Resistance Thermometers](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=932587), §4.1 PDF pp. 24–25, lines 927–937: self-heating depends on measuring current and medium; evaluate in situ where use conditions differ. §4.2 PDF pp. 25–26, lines 1003–1014: immersion error and sufficient immersion depend on sensor/conditions. §5.3 PDF pp. 55–56, lines 2146–2150: example calibration uncertainty budget, explicitly may be incomplete and numerical values illustrative. NIST, [Industrial Thermometer Calibrations](https://www.nist.gov/pml/sensor-science/thermodynamic-metrology/industrial-thermometer-calibrations), opened page for service scope.

**Conditions/counterexample:** The guide supports application effects and uncertainty-budget construction, not a universal instruction to calibrate every assembled chain at multiple points or include every named term in every budget. Lead resistance is wiring-dependent; immersion/contact effects depend on installation. Point selection and method must follow the calibration objective/range.

**Proposed wording:** “For RTD calibration, characterize the sensor and readout over the required range using a suitable temperature source and reference. Include relevant uncertainty and use-condition effects—such as self-heating and immersion—according to sensor, wiring, medium, and method; select points to meet the calibration objective.”

## Scope and preservation

This is an evidence/content review, not an approval or promotion record. The current independent verification and scoring hold overlays remain authoritative and unchanged. In particular, supported wording here does not establish that an existing Fact Anchor was already independently verified, and no generated view, registry row, Topic Pack, or scoring behavior was changed.
