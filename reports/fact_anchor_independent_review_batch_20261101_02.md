# Fact Anchor independent primary-text review — batch 02 (2026-11-01)

Parent commit: `e1071a4ea8552b513fa63b3e310680da50f9a989` (existing work branch only). Original Queue 1,290; previously source-reviewed 9; newly source-reviewed **37**; cumulative source-reviewed **46**; remaining **1244**. New outcomes: **31 KEEP_BOUNDED**, **6 REVISE_REQUIRED**, **0 DELETE/REJECT confirmed**. A revision requirement is NOT evidence of falsity; do not automatically replace source Topic Packs or promote revised claims before standard source authoring and regression validation.

Review method: Original Registry `statement` and `relation.conditions` were inspected against the actual publicly accessible issuing organization's HTML on 2026-11-01. A previous `verified` flag or a reference URL alone did not qualify. HSE guidance establishes engineering control principles, not universally binding national legislation. Each claim below has an explicit mapped primary source, rationale and applicable limitations. The entire 1,290-row audit is NOT fully verified. No tests, release validation, or generated-source promotion were performed in this connector-only review.

## Primary sources consulted

- **HSE**: UK HSE, Control systems, sections Safety-related systems / Protection systems / Proof testing / Maintenance / Modification. https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm (viewed 2026-11-01)
- **HSEFS**: UK HSE, Functional safety, SIS and safety lifecycle. https://www.hse.gov.uk/eci/functional.htm (viewed 2026-11-01)
- **NISTCAL**: NIST, Recommended Calibration Interval, Q&A. https://www.nist.gov/calibrations/recommended-calibration-interval (viewed 2026-11-01)
- **NISTTR**: NIST, Metrological Traceability: Frequently Asked Questions and Policy, §§3.2, 5.1.1, 5.2.1. https://www.nist.gov/metrology/metrological-traceability (viewed 2026-11-01)
- **NISTMTBF**: NIST/SEMATECH e-Handbook, §8.4.5.1, Estimating the MTBF. https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm (viewed 2026-11-01)
- **SIEMENS**: Siemens, SIMATIC S7-1200 Programmable controller V20 (11/2024), Configuring digital input filter times. https://docs.tia.siemens.cloud/r/simatic_s7_1200_manual_collection_enus_20/device-configuration/configuring-the-operation-of-the-cpu/configuring-digital-input-filter-times (viewed 2026-11-01)
- **MATH**: MathWorks R2026b, Design Requirements, Root Locus and Pole-Zero Plot Requirements. https://www.mathworks.com/help/control/ug/design-requirements.html (viewed 2026-11-01)
- **EXIDA**: exida, Back to Basics 17 - PFH, 2019-11-19. https://www.exida.com/blog/back-to-basics-17-pfh (viewed 2026-11-01)
- **EXIDAPFD**: exida, PFDavg definition. https://www.exida.com/Resources/Term/pfdavg (viewed 2026-11-01)

## Per-Fact decisions

### 1. `calibration_interval_depends_on_requirements_stability_history_and_use` — KEEP_BOUNDED

- Source: `NISTCAL` (see issuing-authority URLs above).
- Original Registry statement: Calibration intervals are not universal fixed values: they should be selected and reviewed against the required measurement accuracy or criticality, applicable contract/regulatory limits, instrument stability and environment, use, manufacturer guidance, and as-found/history evidence. Interval changes require evidence that continued fitness is maintained; the applicable program governs the decision.
- Independent comparison: NIST explicitly rejects one universal recalibration interval and identifies accuracy, contractual requirements, stability, environment and as-submitted/post-calibration history; manufacturer advice remains a contextual factor, not a NIST mandate.
- Applicable Registry conditions: `instrument_and_measurement_purpose_are_defined`; `applicable_regulatory_or_contractual_interval_requirements_take_precedence`; `interval_adjustment_is_supported_by_measurement_assurance_and_calibration_history`

### 2. `metrological_traceability_chain_uncertainty_and_interval_are_purpose_dependent` — KEEP_BOUNDED

- Source: `NISTTR`, `NISTCAL` (see issuing-authority URLs above).
- Original Registry statement: Metrological traceability is a property of a measurement result relating it to a reference through a documented unbroken chain of calibrations, each contributing to measurement uncertainty; traceability alone does not establish fitness for purpose. NIST sets no universal recalibration interval; accuracy needs, contract/regulation, instrument stability, environment and measurement history can affect interval selection.
- Independent comparison: NIST defines result-specific traceability via a documented unbroken chain with uncertainty, rejects mere instrument certificates as sufficient, and rejects a universal recalibration interval.
- Applicable Registry conditions: `traceability_is_a_property_of_measurement_results_not_a_blanket_property_of_an_instrument`; `each_calibration_link_contributes_to_measurement_uncertainty`; `traceability_does_not_guarantee_fitness_for_purpose`; `no_universal_nist_recalibration_interval_is_claimed`

### 3. `mtbf_operating_time_per_confirmed_failure` — KEEP_BOUNDED

- Source: `NISTMTBF` (see issuing-authority URLs above).
- Original Registry statement: For a repairable asset under a defined observation and failure-counting basis, empirical MTBF is estimated as accumulated operating time divided by the number of qualifying failures. The failure definition and included operating-time boundary must be consistent; repair, waiting, and requalification time are not operating time in the NIST glossary definition.
- Independent comparison: The cited HPP/exponential estimator is total accumulated operating time divided by qualifying failures; zero-failure observations need one-sided bound, not division by zero.
- Applicable Registry conditions: `repairable_asset_and_qualifying_failure_definition_are_specified`; `observation_period_and_operating_time_boundary_are_consistent`; `zero_failure_cases_require_censored_or_confidence_bound_treatment_not_division_by_zero`

### 4. `calibration_reference_standard_uncertainty_traceability_control` — REVISE_REQUIRED

- Source: `NISTTR` (see issuing-authority URLs above).
- Original Registry statement: A reference standard used to calibrate measurement equipment must be fit for the measurement's required accuracy/uncertainty and tolerance, with its identity, current calibration status, environmental conditions, handling/storage and use history controlled as required by the measurement program. Metrological traceability requires a documented calibration chain to stated references, with uncertainty contributions recorded at each link; no universal accuracy-ratio is implied.
- Independent comparison: NIST supports documented traceability and uncertainty but does not establish that the entire listed reference-standard inventory/handling/control checklist is universally mandatory in all programs.
- Applicable Registry conditions: `required_measurement_accuracy_and_tolerance_are_defined`; `applicable_metrology_quality_program_sets_record_and_control_requirements`; `traceability_claim_has_documented_calibration_chain_and_uncertainty`
- Proposed replacement (NOT automatically promoted): A measurement's traceability is established through a documented calibration chain to a defined reference, with uncertainty attributed to each link; reference-standard selection and administrative controls follow the applicable measurement program and needed uncertainty.

### 5. `positioner_calibration_as_found_as_left_recording_scope` — REVISE_REQUIRED

- Source: `NISTCAL` (see issuing-authority URLs above).
- Original Registry statement: For positioner calibration or diagnostic work, distinguish and retain the as-found condition before adjustment from the as-left condition after adjustment/verification. Emerson describes capturing DVC6200 as-found data with a valve-signature diagnostic before calibration; NIST recommends pre- and post-calibration accuracy/precision data in calibration reports. The detailed fields and acceptance limits depend on the device and governing procedure; no universal fixed record set is asserted.
- Independent comparison: NIST supports pre- and post-calibration records generally, but the DVC6200 valve-signature example was not independently checked in this batch and must not be promoted as a universal core scoring fact.
- Applicable Registry conditions: `claim_is_scoped_to_calibration_or_diagnostic_work`; `as_found_condition_is_distinguished_from_post_adjustment_as_left_condition`; `emerson_dvc6200_signature_capture_is_model_specific`; `record_fields_and_acceptance_limits_follow_device_and_governing_procedure`; `no_universal_fixed_record_set_is_asserted`
- Proposed replacement (NOT automatically promoted): For calibration where adjustment may change instrument performance, retain applicable as-found and as-left measurement results sufficient to evaluate drift and demonstrate return-to-service acceptance under the governing procedure. Device-specific diagnostics are optional examples.

### 6. `root_locus_dominant_pole_design_approximation` — KEEP_BOUNDED

- Source: `MATH` (see issuing-authority URLs above).
- Original Registry statement: 고차 시스템에서 목표 감쇠비와 정착시간으로 우세 폐루프 극의 설계점을 정할 때는 2차 우세계 근사를 전제로 하며, 비우세 극·모드의 영향과 전체 폐루프 응답이 근사 가정에 부합하는지 확인해야 한다.
- Independent comparison: MathWorks explicitly treats settling-time and overshoot root-locus boundaries as exact for a second-order model without zeros and approximations for higher-order systems; verify actual closed-loop response.
- Applicable Registry conditions: `higher_order_linear_model`; `dominant_second_order_behavior_is_validated`; `remaining_pole_modes_do_not_materially_invalidate_design`

### 7. `second_order_margin_damping_overshoot_bandwidth_trend` — REVISE_REQUIRED

- Source: `MATH` (see issuing-authority URLs above).
- Original Registry statement: For a dominant-second-order-like closed loop, phase margin is an approximate proxy for damping (for the standard model, ζ is roughly PM/100 when PM is below about 70°); greater damping reduces second-order overshoot, while increasing the natural-frequency scale at fixed damping raises bandwidth and shortens the response time scale. These are model-dependent design trends, not universal laws for arbitrary systems.
- Independent comparison: MathWorks supports damping-overshoot exact second-order relation and higher-order approximation but does NOT establish the blanket ζ≈PM/100 heuristic and its 70° threshold in this inspected source.
- Applicable Registry conditions: `dominant_second_order_like_closed_loop`; `phase_margin_below_approximately_seventy_degrees_for_rule_of_thumb`; `natural_frequency_scaled_at_fixed_damping`
- Proposed replacement (NOT automatically promoted): For a canonical second-order system without zeros, damping ratio controls overshoot, and root-locus transient requirements can be interpreted in terms of dominant poles. For higher-order systems, pole-boundary estimates are approximate and actual closed-loop response must be checked. Do not treat ζ≈PM/100 as independently certified by this source.

### 8. `sw02_debounce_hysteresis_reduce_chatter_with_response_time_tradeoff` — REVISE_REQUIRED

- Source: `SIEMENS` (see issuing-authority URLs above).
- Original Registry statement: For sampled digital inputs, a debounce/filter or time qualification can reject short contact-bounce transitions, and hysteresis can prevent repeated switching when a noisy slowly varying signal crosses a threshold. These methods change detection behavior: short legitimate pulses may be missed and configured filters add response delay. Therefore thresholds and delays must be selected against both nuisance-transition behavior and the required protective response time; no universal setting is implied.
- Independent comparison: Siemens explicitly documents input-filter bounce rejection, suppressed short pulses and response-time risk. This page does not independently establish the separate analog-threshold hysteresis claim.
- Applicable Registry conditions: `filtering_and_hysteresis_are_selected_for_the_signal_and_application_not_applied_as_a_universal_bundle`; `pulse_rejection_and_filter_delay_are_included_in_input_detection_and_protective_response_assessment`; `the_selected_method_must_not_hide_a_legitimate_required_transition`
- Proposed replacement (NOT automatically promoted): A configured digital-input debounce/filter can suppress contact-bounce and short noise transitions but can also delay or suppress legitimate short events. Select filter time against both noise behavior and required detection time; assess hysteresis separately using a threshold-specific authoritative source.

### 9. `sw02_manual_control_does_not_remove_hazard_preventing_protection` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: HSE describes process control and automatic batch/sequence control as distinct from protection functions: sequences may also be performed procedurally under manual control, but protective interlocks prevent hazardous control actions by either an operator or the process-control system. Operator commands that could demand a protective-system action should be prevented or verified. Thus manual mode may change normal sequence ownership, but does not by itself authorize disabling required protection; the permitted manual actions and any separately managed override must be defined for the application.
- Independent comparison: HSE contrasts manual procedural sequences with protective interlocks which prevent hazardous operator or controller actions; overrides require separate management.
- Applicable Registry conditions: `normal_sequence_may_be_implemented_automatically_or_procedurally_under_manual_control`; `protective_interlocks_must_prevent_operator_or_process_control_actions_that_could_initiate_a_hazard`; `any_protection_override_is_separately_authorized_and_managed_under_application_safety_requirements`

### 10. `sw02_fail_safe_action_is_application_defined_safe_state` — KEEP_BOUNDED

- Source: `HSE`, `HSEFS` (see issuing-authority URLs above).
- Original Registry statement: Functional-safety guidance defines the objective as achieving or maintaining a defined safe state, and control-system guidance describes actuators taking a specified tripped state on loss of signal or utilities. The appropriate state is process- and hazard-dependent: it is not universally fail-closed or de-energized, and in some circumstances power must be maintained to preserve safety.
- Independent comparison: HSE explicitly permits passive or active measures including emergency cooling; a process-specific safe state cannot always be reduced to power-off or valve-close.
- Applicable Registry conditions: `safe_state_and_failure_response_are_defined_by_process_hazard_and_safety_requirements`; `actuator_and_final_element_behavior_are_verified_for_the_relevant_failure_modes`; `neither_fail_closed_nor_deenergize_is_universally_safe`

### 11. `sis_software_systematic_failure_needs_lifecycle_controls` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Software의 체계적 고장은 단순한 일정 고장률 계산만으로 충분히 통제할 수 없다.
- Independent comparison: HSE requires systematic/common-mode failure controls via safety lifecycle and software engineering rather than inference from a constant random failure rate.
- Applicable Registry conditions: `systematic_failure_is_addressed_by_lifecycle_and_software_methods`; `random_hardware_reliability_analysis_remains_separately_relevant`

### 12. `sis_proof_test_detects_unrevealed_dangerous_failures` — REVISE_REQUIRED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Proof Test는 진단으로 발견되지 않은 위험 고장을 검출하고 기능을 복원하기 위한 주기 시험이며 Software Validation을 대체하지 않는다.
- Independent comparison: HSE confirms finding unrevealed dangerous faults and post-maintenance reinstatement, but proof test by itself does not necessarily restore a failed function and is not identical to software validation.
- Applicable Registry conditions: `proof_test_interval_and_coverage_are_defined_for_the_safety_function`; `software_validation_is_a_distinct_safety_lifecycle_activity`; `detected_failures_require_controlled_reinstatement_and_retest`
- Proposed replacement (NOT automatically promoted): Proof testing seeks to reveal dangerous failures not disclosed during normal operation or online diagnostics; detected deficiencies require separate corrective action and safe reinstatement. Proof testing does not replace software validation.

### 13. `sis_shared_resources_create_common_cause_dependency` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: BPCS와 SIS를 분리해도 Sensor, 전원, Network, Engineering Tool 또는 유지보수 절차를 공유하면 공통원인이 남을 수 있다.
- Independent comparison: HSE identifies shared utilities, management systems, interfaces, and remote diagnostic access as potential dependencies; actual shared engineering tools/networks require case-specific review.
- Applicable Registry conditions: `shared_components_utilities_interfaces_or_management_processes_are_assessed`; `independence_is_demonstrated_for_the_claimed_risk_reduction`

### 14. `sis_common_cause_dependency_independence_assessment` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: 공통원인과 종속성은 독립 채널 가정을 훼손하므로 정량·정성 평가에서 별도 고려한다.
- Independent comparison: HSE requires separation and assessment of common-mode, utilities and management-system dependencies; independent channels cannot be assumed simply from duplication.
- Applicable Registry conditions: `shared_interfaces_components_utilities_and_management_are_reviewed`; `independence_measures_are_defined_for_the_required_integrity`

### 15. `sis_pfdavg_pfh_demand_mode_measure_boundary` — KEEP_BOUNDED

- Source: `HSE`, `EXIDA`, `EXIDAPFD` (see issuing-authority URLs above).
- Original Registry statement: PFDavg는 저요구 모드, PFH는 고요구·연속 모드의 목표 고장척도이며 서로 임의 교환하지 않는다.
- Independent comparison: HSE distinguishes low-demand failure probability from high/continuous-demand failures per hour; exida distinguishes time-averaged PFDavg from PFH; these quantities cannot be compared as dimensionally identical.
- Applicable Registry conditions: `demand_mode_is_classified_for_the_safety_function`; `units_and_demand_mode_are_preserved_when_comparing_integrity_targets`

### 16. `sis_override_and_maintenance_bypass_controls` — REVISE_REQUIRED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Overrides are managed by authorization, security, recording, monitoring, review and reset requirements. If a maintenance bypass is unavoidable, procedures provide an equivalent level of safety (for example temporary barriers or permit-to-work), with reinstatement and proof testing after maintenance.
- Independent comparison: HSE documents override authorization/security/logging/reset and post-maintenance reinstatement, but no inspected text promises an equivalent level of safety for every bypass or mandates the examples as universal conditions.
- Applicable Registry conditions: `bypass_is_limited_to_unavoidable_maintenance_context_in_the_cited_guidance`; `equivalent_safety_measures_are_defined_in_site_procedures`; `post_maintenance_reinstatement_and_proof_testing_are_performed`
- Proposed replacement (NOT automatically promoted): Override and maintenance-bypass arrangements for protective systems must follow the defined authorization, monitoring, recording and reinstatement process; any compensating measures and feasibility of an equivalent safety level are risk- and site-specific.

### 17. `sis_modification_control_and_safety_verification` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: SIS 변경은 무단 변경과 성급한 변경을 방지하는 관리 절차로 통제하며, 변경 후 안전기능과 무결성이 유지됨을 Verification으로 확인하고 유능한 인원이 설계·구현한다.
- Independent comparison: HSE Modification section explicitly requires prevention of unauthorized/poorly conceived changes, competent staff and verification of preserved safety function and integrity.
- Applicable Registry conditions: `modifications_are_authorized_and_managed`; `safety_verification_confirms_required_function_and_integrity_are_maintained`; `design_and_implementation_are_performed_by_competent_persons`

### 18. `final_element_valve_actuator_utility_scope` — KEEP_BOUNDED

- Source: `HSE`, `HSEFS` (see issuing-authority URLs above).
- Original Registry statement: SIS final elements include devices such as valves that are manipulated to achieve a safe state; the associated actuator safety function may include its valve, actuator, positioner, power supply and required utilities.
- Independent comparison: HSE identifies sensor/logic/final elements, valves, and utilities required for safety function; optional positioner/power components count only when actually necessary to the specific SIF.
- Applicable Registry conditions: `specific_package_boundary_depends_on_safety_function`; `only_utilities_required_for_actuator_safety_function_are_included`

### 19. `final_element_safe_action_process_dependent` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: The protective action required to reach or maintain a safe state depends on the process; fail-close or fail-open is not a universal safe state independent of the hazard and SRS.
- Independent comparison: HSE states action depends upon process, and safe protection can be active or passive; fail-open/fail-close cannot be universalized.
- Applicable Registry conditions: `safe_action_is_defined_for_the_specific_process`; `valve_mechanical_fail_action_is_not_assumed_to_equal_process_safe_state`

### 20. `deenergize_trip_requires_application_safe_action_check` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: De-energize-to-trip can cause a trip action on loss of signal or power, but the actuator action must be checked for consistency with the process-specific safe-state requirement.
- Independent comparison: HSE discusses de-energize-to-trip but also possible active protection requiring continued utilities, so required safe action is application-specific.
- Applicable Registry conditions: `loss_of_signal_or_power_is_in_the_defined_trip_case`; `actual_actuator_and_process_response_are_verified_for_the_application`

### 21. `protective_system_required_utility_scope_and_integrity` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Utilities required for the protective system safety function are within its scope and should have integrity consistent with their contribution; shared utilities are considered in independence and common-cause assessment.
- Independent comparison: HSE Safety related systems and Independence sections include utilities used by safety functions and require shared-utility dependencies to be considered.
- Applicable Registry conditions: `utility_is_required_to_perform_the_safety_function`; `independence_claim_accounts_for_shared_utility`

### 22. `proof_test_frequency_detection_and_repair_time_effect` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Protective-system PFD or failure rate depends on proof-test frequency and the test's ability to reveal previously hidden failures; for high-diagnostic-coverage systems, failure-rate performance also depends on repair time.
- Independent comparison: HSE Proof testing and Maintenance sections tie dangerous failure exposure to test frequency/coverage and diagnostic-dependent reliability to mean time to repair.
- Applicable Registry conditions: `proof_test_reveals_previously_hidden_dangerous_failures`; `repair_time_claim_is_limited_to_systems_with_high_diagnostic_coverage`

### 23. `proof_test_procedure_acceptance_and_safe_execution` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Proof-test procedures specify success/failure criteria and safe test conduct, including applicable management arrangements, operating restrictions and personnel competence; post-maintenance reinstatement and proof testing are addressed by maintenance procedures.
- Independent comparison: HSE specifies proof-test success/failure criteria and safe arrangements; maintenance covers post-work reinstatement and proof testing.
- Applicable Registry conditions: `procedure_is_available_for_the_relevant_safety_function`; `management_operating_and_competence_controls_are_defined_as_applicable`

### 24. `sis_override_and_post_maintenance_restoration_controls` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Protective-system operating procedures manage override authorization, security, recording, monitoring, review and reset; maintenance procedures include post-maintenance reinstatement and proof testing. The detailed independent verification method is site-specific.
- Independent comparison: HSE Operation and Maintenance sections describe override approval, logging, reset and post-maintenance restoration; plant-specific checks are not a fixed universal procedure.
- Applicable Registry conditions: `override_controls_are_defined_in_protective_system_operating_procedures`; `post_maintenance_reinstatement_and_proof_testing_are_defined`; `independence_of_verification_is_not_claimed_as_a_universal_hse_requirement`

### 25. `sis_proof_test_expected_trip_and_end_to_end_scope` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Proof-test procedures should reveal dangerous failures hidden during normal operation, include tests under expected trip conditions where practicable, and include end-to-end testing at appropriate intervals. Scope and criteria are set for the SIF.
- Independent comparison: HSE Proof testing calls for revealing normally undetected dangerous faults, testing at expected trip conditions where possible and appropriate end-to-end tests.
- Applicable Registry conditions: `test_conditions_represent_expected_trip_conditions_or_alternative_reveal_measures_are_defined`; `end_to_end_test_is_scheduled_at_appropriate_intervals`; `test_scope_is_defined_for_the_protective_function`

### 26. `shared_dependencies_and_environment_affect_independence` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Shared utilities, environmental interactions and common maintenance procedures or personnel can affect claimed protective-system independence and should be considered in common-cause assessment.
- Independent comparison: HSE explicitly identifies shared utilities, environmental influence and maintenance/management systems in common-cause and independence analysis.
- Applicable Registry conditions: `dependencies_are_assessed_for_the_specific_installation`; `no_universal_common_cause_probability_is_inferred`

### 27. `sis_modification_and_spares_controls` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: SIS modifications are controlled to prevent unauthorized or ill-conceived changes and verified to preserve required safety function and integrity; maintenance procedures control spares by segregating faulty/nonconforming parts and preventing interchange of similar parts.
- Independent comparison: HSE Modification/Maintenance sections cover controlled change, safety verification and prevention of incorrect spare interchange.
- Applicable Registry conditions: `modification_verification_is_limited_to_maintaining_required_function_and_integrity`; `spare_controls_follow_the_maintenance_procedure`

### 28. `repair_performance_monitored_against_design_criteria` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Where high diagnostic coverage is claimed, observed repair performance should be monitored and reviewed against the design criteria.
- Independent comparison: HSE Maintenance section states that repair performance should be monitored against design criteria where high diagnostic coverage is claimed.
- Applicable Registry conditions: `the_claimed_diagnostic_coverage_is_high`; `observed_repair_performance_is_compared_with_design_criteria`

### 29. `safety_function_failure_metric_depends_on_demand_mode` — KEEP_BOUNDED

- Source: `HSE`, `EXIDA` (see issuing-authority URLs above).
- Original Registry statement: PFDavg와 PFH의 선택은 SIF의 demand mode 정의에 근거해야 한다.
- Independent comparison: HSE distinguishes failure probability at demand versus frequency per hour; exida identifies PFH as high/continuous-demand metric.
- Applicable Registry conditions: `low_demand_uses_probability_of_failure_on_demand_metric`; `high_or_continuous_demand_uses_failure_rate_per_hour_metric`

### 30. `low_demand_sif_integrity_uses_average_probability_of_failure_on_demand` — KEEP_BOUNDED

- Source: `HSE`, `EXIDAPFD` (see issuing-authority URLs above).
- Original Registry statement: 저수요 SIF의 정량 목표는 일반적으로 평균 요구시 실패확률인 PFDavg로 표현한다.
- Independent comparison: HSE gives probability of failure on demand at low demand and exida names PFDavg as the time-averaged low-demand SIL performance measure.
- Applicable Registry conditions: `safety_function_operates_in_low_demand_mode`

### 31. `high_or_continuous_demand_sif_integrity_uses_dangerous_failure_rate` — KEEP_BOUNDED

- Source: `HSE`, `EXIDA` (see issuing-authority URLs above).
- Original Registry statement: 고수요 또는 연속수요 SIF의 정량 목표는 일반적으로 시간당 위험고장 빈도 지표인 PFH로 표현한다.
- Independent comparison: HSE identifies per-hour failure metric for high and continuous demand; exida explains PFH and diagnostic relevance.
- Applicable Registry conditions: `safety_function_operates_in_high_demand_or_continuous_mode`

### 32. `longer_proof_test_interval_increases_latent_failure_exposure_under_constant_rate_model` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Proof Test Interval이 길어지면 잠복 위험고장의 평균 노출시간이 증가할 수 있다.
- Independent comparison: HSE confirms protective-system failure probability depends on test interval and revealed fraction. Increased latent exposure follows under the fact's constant-rate and unchanged-coverage assumptions.
- Applicable Registry conditions: `failure_remains_undetected_until_proof_test`; `constant_failure_rate_and_periodic_test_assumption`; `no_compensating_online_diagnostic_or_interim_test`

### 33. `common_cause_failures_reduce_redundancy_benefit_under_independence_assumption` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: CCF는 중복 채널을 동시에 무력화하여 독립고장 가정의 이점을 감소시킨다.
- Independent comparison: HSE states redundancy is one fault-tolerance layer and independence/common-mode threats must be assessed; shared failures defeat the assumed independent-channel benefit.
- Applicable Registry conditions: `common_cause_or_shared_coupling_can_affect_multiple_channels`; `quantitative_contribution_depends_on_the_selected_ccf_model_and_evidence`

### 34. `physical_separation_independent_utilities_and_diversity_are_ccf_mitigation_measures` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: 물리적 분리, 독립 전원·배관·환경, 다양성, 독립 교정·정비 절차는 CCF 저감 근거가 될 수 있다.
- Independent comparison: HSE lists separate utilities, physical separation, diverse technology, and independent maintenance and test processes as common-mode mitigation examples.
- Applicable Registry conditions: `measures_are_selected_for_identified_shared_causes_and_couplings`; `measures_reduce_but_do_not_guarantee_elimination_of_common_cause_failure`

### 35. `hft_and_voting_architecture_alone_do_not_demonstrate_achieved_sil` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: Voting 구조와 HFT는 SIL 달성의 한 요소이며 단독으로 SIL을 보장하지 않는다.
- Independent comparison: HSE explicitly distinguishes hardware fault tolerance and diagnostic coverage from system-wide reliability demonstration and safety lifecycle evidence.
- Applicable Registry conditions: `hardware_architectural_constraints_are_only_part_of_integrity_evidence`; `reliability_model_and_lifecycle_evidence_are_needed_for_the_complete_function`

### 36. `certified_subsystem_sil_does_not_automatically_establish_complete_sif_integrity` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: 개별 구성요소 인증은 전체 SIF의 Achieved SIL을 자동 결정하지 않는다.
- Independent comparison: HSE requires system architecture reliability and full design/installation/maintenance integrity evidence; component claims alone cannot establish entire SIF integrity.
- Applicable Registry conditions: `complete_sif_architecture_and_all_element_contributions_are_evaluated`; `certificate_scope_and_assumptions_match_the_application`

### 37. `random_hardware_failure_calculation_does_not_replace_systematic_and_lifecycle_evidence` — KEEP_BOUNDED

- Source: `HSE` (see issuing-authority URLs above).
- Original Registry statement: 정량 하드웨어 무결성 계산은 체계적 무결성, 소프트웨어 V&V, 형상관리와 독립성 증거를 대체하지 않는다.
- Independent comparison: HSE treats random hardware failures and systematic/common-mode lifecycle controls as distinct indispensable evidence.
- Applicable Registry conditions: `hardware_random_failure_and_systematic_failure_are_distinct_evidence_domains`; `complete_safety_lifecycle_requirements_remain_applicable`

## Admission and release safeguards

- The 276 separately excluded noncore/scoped/duplicate/generalization Fact IDs remain excluded and unmodified.
- `KEEP_BOUNDED` means primary HTML was read and supports the stated physical/engineering core **with the recorded conditions**; it does not imply universal regulation or independent validation of any extra examples beyond the assessed claim.
- `REVISE_REQUIRED` has **not** been promoted to an eligible replacement. The original scoring reference must be removed or guarded pending source Topic Pack amendment, verification-reference update, generated-bank rebuild, focused tests and release validation.
- All previously unreviewed IDs keep `NOT_PERFORMED` / `PENDING_INDEPENDENT_CLAIM_BY_CLAIM_REVIEW`. Do not interpret previous Registry `verified` as current reapproval.
- **No branch integration into `main`**, CI claim, or release gate PASS is asserted by this audit.
