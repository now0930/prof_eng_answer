# Independent primary-source review batch 03 - control valves (2026-11-01)

Parent: ffaf3c6da810949dfe9e59183fa0314589f19eab. Queue 1,290; previous primary checks 46; new checks 23; cumulative 69; remaining 1,221. Outcome: 18 KEEP_BOUNDED, 5 REVISE_REQUIRED, 0 demonstrated falsehood/rejections.

Primary source: Valmet, Flow Control Manual chapter 2, section 2.2-2.4.6, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/ (issuing organization's public HTML, accessed 2026-11-01). Scope: manufacturer DPm and gain recommendations are engineering examples, not universal statutory rules. The original statements and explicit conditions below are taken from canonical Registry; old verification metadata alone was not counted.

### 1. control_valve_inherent_characteristic_is_constant_dp_curve - KEEP_BOUNDED
Original: An inherent valve flow characteristic is the relationship between valve travel and flow coefficient measured or defined at constant pressure drop across the valve; under the corresponding non-choked liquid conditions, flow is proportional to Cv.
Source locator: Valmet manual 2.4.1, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Inherent characteristic is valve flow/Cv as a function of travel at constant valve differential pressure.
Original conditions: valve_pressure_drop_is_held_constant; fluid_and_test_conditions_are_defined; flow_is_not_choked

### 2. control_valve_installed_characteristic_depends_on_pipeline - KEEP_BOUNDED
Original: An installed flow characteristic is the actual flow-versus-travel relationship with the valve operating in its process pipeline; it depends on both the valve's inherent characteristic and the pipeline pressure-loss behavior.
Source locator: Valmet manual 2.4.2, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Installed curve depends on piping and inherent valve response.
Original conditions: valve_is_installed_in_process_pipeline; operating_conditions_are_considered

### 3. control_valve_installed_dp_changes_with_pipeline_flow_losses - KEEP_BOUNDED
Original: In an installed process pipeline, flow-dependent pressure losses can change the pressure differential available across the valve; consequently the installed flow curve can differ from the inherent curve even when source and receiver pressures are fixed.
Source locator: Valmet manual 2.4.2, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Pipe losses change with flow, changing available valve differential pressure.
Original conditions: valve_is_installed_in_process_pipeline; pipeline_losses_vary_with_flow

### 4. linear_inherent_curve_does_not_guarantee_linear_installed_flow - KEEP_BOUNDED
Original: A linear inherent trim does not guarantee a linear installed flow-versus-travel curve: if valve differential pressure varies with flow, the liquid-flow relation combines Cv(travel) with the changing pressure drop.
Source locator: Valmet manual 2.4.1B, 2.4.2, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Linear inherent curve does not guarantee constant installed flow slope due to variable differential pressure.
Original conditions: installed_valve_pressure_drop_varies_over_operating_range; liquid_flow_is_non_choked_or_appropriate_sizing_model_is_used

### 5. equal_percentage_can_help_linearize_installed_curve_conditionally - KEEP_BOUNDED
Original: An equal-percentage inherent characteristic is often selected to help produce a more nearly linear installed response when valve pressure drop decreases as flow rises, but it does not guarantee a linear installed curve; process-specific sizing/modeling is required.
Source locator: Valmet manual 2.4.1C, 2.4.6, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Equal-percentage can compensate falling valve pressure drop as flow increases but is not guaranteed for all pipelines.
Original conditions: valve_dp_decreases_as_flow_increases; system_is_within_assumptions_of_selection_guidance; installed_performance_is_checked

### 6. valve_characteristic_selection_is_process_condition_dependent - KEEP_BOUNDED
Original: Control-valve characteristic and size selection must use the actual process operating conditions and the target installed behavior; a trim label alone is insufficient to establish suitability across an operating range.
Source locator: Valmet manual 2.2-2.3, 2.4.3, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Operating points, valve type/size and installed gain must inform selection.
Original conditions: actual_process_conditions_are_defined; required_operating_range_is_considered; installed_behavior_is_evaluated

### 7. valve_characteristic_application_mappings_are_not_universal - KEEP_BOUNDED
Original: Typical application mappings for linear, equal-percentage, and quick-opening trims are guidance rather than universal rules: actual suitability depends on the process pressure distribution, operating range, valve sizing, and control objective.
Source locator: Valmet manual 2.4.1, 2.4.6, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Characteristic examples are application guidance rather than universal requirements.
Original conditions: selection_is_not_based_only_on_trim_name; installed_conditions_and_control_objective_are_checked

### 8. authority_comparison_requires_complete_hydraulic_boundary - REVISE_REQUIRED
Original: An authority calculation is meaningful only after defining the hydraulic boundary and pressure-drop convention; pumps, static head, bypasses, and parallel branches can change which pressure drops belong in the denominator and may invalidate a simple series-circuit formula.
Source locator: Valmet manual 2.4.4 Process model / DPm, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Valmet defines DPm specifically and discusses pump/pipe boundary; not evidence that every valve-authority denominator uses the same formula.
Original conditions: all_included_paths_and_sources_are_identified; static_and_dynamic_terms_are_separated; authority_formula_matches_boundary
Proposed corrected fact (not promoted): State numerator, denominator, flow point and pipeline boundary; Valmet DPm is valve drop at maximum process flow divided by valve drop at closure for the specified model. Do not equate DPm to all authority conventions.

### 9. valve_and_pipe_pressure_drops_redistribute_with_flow - KEEP_BOUNDED
Original: As flow changes in an installed circuit, flow-dependent piping and equipment losses change and redistribute the pressure drop available across the valve; the direction and amount depend on the pressure source, system topology, and operating point.
Source locator: Valmet manual 2.4.2, 2.4.4, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Changing pipe/equipment losses affects available valve drop with system boundary and pump curve.
Original conditions: circuit_topology_and_pressure_source_are_defined; flow_dependent_losses_are_present

### 10. low_authority_can_distort_installed_curve_conditionally - REVISE_REQUIRED
Original: When the valve takes a small share of the relevant system pressure drop, changes in other system losses can strongly affect its available Δp and installed flow curve; low authority can therefore increase distortion from the inherent curve, but magnitude and shape depend on trim and system conditions.
Source locator: Valmet manual 2.4.2-2.4.4, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Valmet discusses DPm ratio and installed distortion, not all definitions of low valve authority.
Original conditions: authority_is_computed_for_relevant_operating_range; inherent_curve_and_system_model_are_known
Proposed corrected fact (not promoted): For a declared series hydraulic boundary and ratio, small available valve pressure drop can contribute to installed curve distortion; compute the actual installed characteristic instead of assuming a universal authority threshold.

### 11. valve_authority_has_no_universal_acceptance_threshold - REVISE_REQUIRED
Original: There is no single authority value that is a universal pass/fail criterion for all control-valve systems; acceptable allocation depends on the declared authority convention, operating range, controllability target, energy cost, pump/system limits, and process requirements.
Source locator: Valmet manual 2.4.4 liquid/gas examples, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Valmet gives liquid and gas DPm rules of thumb but does not establish universal limits for every valve authority definition.
Original conditions: system_requirements_and_authority_convention_are_declared
Proposed corrected fact (not promoted): Do not use a single vendor rule-of-thumb pressure-drop ratio as a universal pass/fail value; state the ratio definition and evaluate the process requirements.

### 12. oversized_valve_can_operate_at_low_travel - KEEP_BOUNDED
Original: A valve selected with excess capacity may meet required flow at a relatively low travel; whether it is oversized must be judged against the actual minimum, normal, and maximum process cases, not nominal line size alone.
Source locator: Valmet manual 2.4.3 Figs.19-20, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Valmet illustrates oversized valve high gain at low flow; actual travel is application-dependent.
Original conditions: selected_capacity_exceeds_process_requirement_at_case; actual_process_cases_are_used

### 13. oversized_valve_can_have_high_low_flow_installed_gain - KEEP_BOUNDED
Original: An oversized valve can exhibit high installed gain at small process flows, making small position changes produce relatively large flow changes and potentially worsening accuracy or promoting hunting; this is a possible outcome, not an inevitable result for every valve and loop.
Source locator: Valmet manual 2.4.3 Figs.19-20, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Oversizing can increase low-flow installed gain, reduce accuracy and promote hunting in model examples.
Original conditions: actual_valve_and_process_installed_curve_are_evaluated; loop_dynamics_and_mechanical_accuracy_are_considered

### 14. inherent_valve_gain_is_local_slope_under_constant_dp - KEEP_BOUNDED
Original: Inherent valve gain is the local slope of the inherent flow or relative-Cv characteristic with respect to valve travel under its constant-pressure-drop reference condition; normalization determines its numerical value.
Source locator: Valmet manual 2.4.1, 2.4.3, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Inherent curve under constant drop; local slope defines inherent gain, with normalization noted.
Original conditions: constant_dp_reference_condition_applies; flow_and_travel_normalization_are_defined

### 15. installed_valve_gain_is_actual_flow_travel_slope - KEEP_BOUNDED
Original: Installed valve gain is the local change in actual relative flow divided by the corresponding change in relative travel along the installed characteristic; its value depends on the chosen flow and travel normalization.
Source locator: Valmet manual 2.4.3 Eq.11, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Installed gain is actual relative flow change per relative travel change.
Original conditions: installed_characteristic_is_defined; flow_and_travel_normalization_are_defined

### 16. installed_valve_gain_varies_over_process_operating_range - KEEP_BOUNDED
Original: Installed valve gain is generally a function of operating point and can vary with flow and travel because both the inherent curve and pressure-drop distribution contribute to the installed curve; it should not be assumed constant without evaluation.
Source locator: Valmet manual 2.4.3, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Gain can vary by operating point and is not automatically constant.
Original conditions: inherent_curve_or_system_pressure_distribution_is_nonlinear; operating_range_is_examined

### 17. installed_gain_need_not_equal_inherent_gain - KEEP_BOUNDED
Original: Installed gain need not equal inherent gain: the installed curve includes process-pipeline pressure behavior in addition to the valve's constant-Δp inherent characteristic.
Source locator: Valmet manual 2.4.1-2.4.3, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Installed gain includes process pressure behavior absent from constant-differential inherent curves.
Original conditions: valve_pressure_drop_varies_with_flow_or_travel; both_gain_definitions_use_comparable_normalization

### 18. equal_percentage_is_only_conditional_process_compensation - KEEP_BOUNDED
Original: An equal-percentage inherent characteristic can help compensate for a changing process/valve pressure relationship in some applications, but it does not guarantee constant process or loop gain; the installed process model and control objective determine suitability.
Source locator: Valmet manual 2.4.1C, 2.4.6, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Equal-percentage is one possible compensation technique, not a universal constant-gain guarantee.
Original conditions: process_nonlinearity_and_pressure_model_are_known; installed_gain_is_evaluated; no_universal_loop_gain_claim_is_made

### 19. installed_gain_variation_can_change_loop_sensitivity - KEEP_BOUNDED
Original: If installed valve gain changes substantially across the required operating range, the same controller output change can cause different relative flow changes at different operating points; this can make a fixed controller tuning feel more or less aggressive, subject to the other loop dynamics.
Source locator: Valmet manual 2.4.3 Eqs.11-12, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: A given valve travel increment changes relative flow by operating-point-dependent gain.
Original conditions: controller_output_change_is_comparable; plant_and_measurement_dynamics_are_also_considered

### 20. installed_valve_cases_should_cover_min_normal_max_flow - KEEP_BOUNDED
Original: Installed performance should be evaluated over the required process flow range, including minimum, normal, and maximum cases where applicable, because travel, valve Δp, and installed gain vary with operating condition.
Source locator: Valmet manual 2.2, 2.4.4, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Evaluate service flow range including min/normal/max if these are specified; no universal fixed cases.
Original conditions: process_cases_are_representative; pressure_and_gain_are_calculated_per_case

### 21. valve_selection_final_check_uses_installed_curve_and_gain - KEEP_BOUNDED
Original: A final control-valve selection check should examine predicted installed flow and gain over the required process range together with the actual process conditions; inherent/catalog characteristic alone does not establish installed controllability.
Source locator: Valmet manual 2.3, 2.4.3, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Installed gain and curve matter to sizing and controllability beyond the catalog characteristic.
Original conditions: process_model_is_based_on_representative_cases; valve_and_system_boundary_are_defined; dynamic_loop_claims_are_not_inferred_from_static_curve_alone

### 22. gas_sizing_checks_defined_minimum_normal_maximum_cases - REVISE_REQUIRED
Original: Control-valve gas sizing은 지정된 minimum, normal, maximum service cases를 각각 검토하며 각 case의 실제 flow와 pressure conditions를 사용한다.
Source locator: Valmet manual 2.2, 2.4.4, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Valmet supports actual operating cases for installed behavior, not a mandatory three-case gas sizing formula for every application.
Original conditions: minimum_normal_and_maximum_are_project_defined_operating_cases_not_a_universal_mandatory_case_count; each_case_uses_its_own_flow_and_relevant_upstream_downstream_pressure_temperature_and_fluid_property_inputs; actual_process_conditions_are_preferred_and_assumptions_reduce_sizing_confidence; the_claim_does_not_assert_that_every_case_is_governing_for_capacity_or_noise
Proposed corrected fact (not promoted): Gas sizing uses the defined service cases and an appropriate compressible-flow sizing method; include min/normal/max only where applicable.

### 23. control_valve_minimum_flow_is_installed_controllability_not_catalog_c_minimum - REVISE_REQUIRED
Original: Low-flow service는 catalog minimum Cv가 아니라 installed system에서 안정적으로 반복 제어할 수 있는 minimum controllable flow를 확인한다.
Source locator: Valmet manual 2.3, 2.4.3, https://www.valmet.com/flowcontrol/valves/flow-control-manual/control-valve-installed-performance/
Independent comparison: Installed gain informs controllability but this source does not prove all minimum-flow criteria or catalog constraints.
Original conditions: inherent_rangeability_uses_valve_capacity_coefficients_and_installed_rangeability_uses_actual_flow_range; installed_flow_characteristic_depends_on_both_inherent_valve_characteristic_and_process_pipeline_pressure_behavior; controllability_tolerance_and_smallest_repeatable_signal_response_are_application_and_valve_dependent; catalog_minimum_capacity_alone_does_not_establish_installed_minimum_controllable_process_flow
Proposed corrected fact (not promoted): Minimum controllable flow is evaluated from operating range, installed gain, control accuracy and equipment limits; catalog Cv alone cannot establish it.

Remaining 1,221 facts are NOT independently source-certified. REVISE_REQUIRED is not a rejection: the proposed replacements still need source Topic Pack review, protected Registry/score-reference updates, focused tests and full release validation. Excluded 276 claims remain untouched. No testing, generated regeneration, production release or main merge performed.
