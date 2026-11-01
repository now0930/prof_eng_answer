# Independent primary-source review batch 04: LVDT / CCPS LOPA / delays (2026-11-01)

Parent 7acf5ac2ac36a485c7af28a55f30fabb125141b5. Queue 1,290; previous independent 69; added 31; cumulative 100; still unreviewed 1190. Batch verdicts: KEEP_BOUNDED 13, REVISE_REQUIRED 18, scientifically rejected 0. A request to REVISE does not mean claim is false; it means original specific assertion was not independently substantiated by the cited primary source.

Primary sources visited: TE Connectivity Understanding LVDTs https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html (sections How Does an LVDT Work, Axial Positions, Core Types, Differential Output Voltage), AIChE/CCPS LOPA Data https://ccps.aiche.org/resources/tools/lopa (What is LOPA, Basic LOPA Steps, Core Attributes, LOPA Components), MathWorks R2026b Analyze Control Systems with Delays https://www.mathworks.com/help/control/ug/analyzing-control-systems-with-delays.html (Control of Processes with Delays; Pade Approximation). All HTML accessed 2026-11-01. Vendor/model-specific supporting examples are not automatically general-purpose scoring requirements. CCPS index describes only the published scope, not the entirety of the paid LOPA guideline.

### 1. lvdt_primary_secondary_movable_core_structure - KEEP_BOUNDED
Original fact: A typical LVDT has a primary winding centered between two symmetrically arranged secondary windings and a movable magnetically permeable core that moves axially without contacting the coil bore.
Source: https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html - How Does an LVDT Work?
Primary-text comparison: TE states central primary, opposed secondaries and contact-free movable core in a typical construction.
Original conditions: claim_is_about_a_typical_laminated_or_tubular_lvdt_configuration

### 2. lvdt_primary_ac_excitation_induces_secondary_voltages - KEEP_BOUNDED
Original fact: An LVDT primary winding is energized with AC, and the magnetic flux coupled through its movable core induces voltages in the two secondary windings.
Source: https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html - How Does an LVDT Work?; AC-Operated LVDT Sensors
Primary-text comparison: AC excitation and induction into the secondary coils are explicitly described.
Original conditions: excitation_amplitude_and_frequency_are_within_the_sensor_specification

### 3. lvdt_secondary_voltage_difference_is_differential_output - KEEP_BOUNDED
Original fact: For the series-opposed secondary connection, the LVDT output is the difference between the secondary voltages, conventionally written Eout = E1 − E2 with sign determined by winding polarity.
Source: https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html - Axial Positions
Primary-text comparison: Opposed winding and E1−E2 differential output are explicitly described.
Original conditions: secondary_voltage_polarities_are_defined_consistently

### 4. lvdt_ideal_null_equal_secondary_voltages_cancel - KEEP_BOUNDED
Original fact: At the ideal LVDT null position, equal secondary voltages cancel in the series-opposed connection, making the differential output essentially zero while the individual secondary voltages are not thereby required to be zero.
Source: https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html - Axial Positions
Primary-text comparison: At centered null, the two individually induced voltages are equal, giving nearly zero difference, not zero individual EMFs.
Original conditions: ideal_electrical_balance; series_opposed_secondary_connection

### 5. lvdt_output_magnitude_tracks_displacement_in_specified_linear_range - KEEP_BOUNDED
Original fact: Within its specified linear range, an LVDT's differential output magnitude varies approximately linearly with core displacement from null; behavior beyond that range can have reduced linearity.
Source: https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html - Output Voltage; Figure 3
Primary-text comparison: TE confirms linear response only over the specified core range, with reduced linearity beyond.
Original conditions: core_remains_within_manufacturer_specified_linear_range

### 6. lvdt_phase_reversal_indicates_direction_across_null - KEEP_BOUNDED
Original fact: The LVDT differential AC output phase changes by approximately 180 degrees relative to primary excitation as the core crosses null, and suitable signal-conditioning circuitry can use that phase reversal to determine direction.
Source: https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html - Differential Output Voltage; Figure 3
Primary-text comparison: TE documents approximately 180 degree AC phase reversal as the core crosses null.
Original conditions: phase_is_referenced_to_primary_excitation; signal_conditioner_accounts_for_its_phase_path

### 7. lvdt_linearity_is_specified_range_limited - KEEP_BOUNDED
Original fact: LVDT linearity is specified for a defined core-motion range; operation beyond full range may remain possible but with degraded linearity, so full mechanical travel must not be assumed to be the specified linear measurement range.
Source: https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html - Differential Output Voltage; Figure 3
Primary-text comparison: TE distinguishes usable motion range from specified linear measurement range.
Original conditions: range_is_taken_from_the_specific_sensor_datasheet

### 8. lvdt_core_motion_changes_opposed_secondary_coupling - KEEP_BOUNDED
Original fact: In a conventional LVDT, moving the ferromagnetic core toward one secondary increases the magnetic coupling and induced voltage of that secondary while decreasing coupling and induced voltage in the other; moving through the centered null reverses which secondary has the greater induced voltage. In the linear magnetic operating regime this is equivalently described as a position-dependent change in the effective primary-to-secondary mutual inductances.
Source: https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html - Axial Positions; AC-Operated LVDT Sensors
Primary-text comparison: TE explicitly describes differential induction and opposing secondary coupling; mutual-inductance interpretation is valid only under original fact linear-core conditions.
Original conditions: claim_assumes_conventional_symmetric_three_winding_lvdt; coupling_and_voltage_change_are_opposed_between_secondaries; mutual_inductance_interpretation_assumes_linear_magnetic_operation

### 9. lvdt_and_strain_gauge_use_different_transduction_chains - REVISE_REQUIRED
Original fact: An LVDT senses linear motion through AC-excited transformer windings and the position-dependent magnetic coupling of a movable ferromagnetic core, producing a differential secondary voltage. A strain-gauge displacement instrument instead infers motion from strain in a mechanical member or elastic element via a small resistance change in bonded gauges, commonly converted to voltage with a Wheatstone bridge. The latter requires a mechanical strain-to-displacement relationship and is not the same transduction mechanism as the LVDT.
Source: https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html - How Does an LVDT Work?
Primary-text comparison: TE confirms only the LVDT excitation/coupling chain. Strain-gauge Wheatstone bridge/displacement mechanics require separate original authoritative evidence.
Original conditions: strain_gauge_displacement_inference_requires_a_mechanical_elastic_element; wheatstone_bridge_is_a_common_signal_conversion_not_an_absolute_requirement_for_every_system; comparison_is_at_the_transduction_principle_level
Proposed source-bounded replacement (NOT promoted): An LVDT converts axial core motion into a differential secondary voltage through AC transformer coupling. Compare to a strain-gauge displacement transducer only after confirming that transducer's own mechanical strain-to-displacement mapping and source.

### 10. lvdt_alignment_and_radial_sensitivity_depend_on_core_construction - REVISE_REQUIRED
Original fact: TE Connectivity describes free-core LVDTs with radial clearance and no coil contact, and explains that the LVDT responds primarily to axial core position; its tutorial also distinguishes free-core from guided-core and spring-loaded constructions. TE says a precision guided probe uses a linear bearing to minimize radial play and side-loading effects. NewTek similarly treats alignment and side-load limits as installation considerations, while noting some misalignment need not degrade measurement. Therefore radial misalignment is construction- and magnitude-dependent; the evidence does not support claiming that every radial offset causes zero shift, hysteresis, or repeatability error.
Source: https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html - Core Types; Free-Core LVDTs; Spring Loaded LVDTs
Primary-text comparison: TE confirms free core radial clearance and guided probe bearings limiting side-load effects, but the cited NewTek misalignment details are not independently verified here.
Original conditions: free_core_radial_clearance_and_guided_probe_bearing_examples_are_construction_specific; no_universal_zero_shift_hysteresis_or_repeatability_error_is_attributed_to_all_radial_offset; follow_selected_manufacturer_mounting_and_side_load_limits
Proposed source-bounded replacement (NOT promoted): Free-core and guided/spring-loaded LVDTs differ in core alignment and bearing design; radial-play and side-loading performance must be taken from the chosen configuration and manufacturer's mounting limits. Avoid any universal offset-induced zero/hysteresis assumption.

### 11. hazop_lopa_ipl_definition - KEEP_BOUNDED
Original fact: IPL은 특정 scenario를 예방하거나 결과를 완화하는 독립된 보호수단으로서 기능이 명확하고 성능을 검증할 수 있어야 한다.
Source: https://ccps.aiche.org/resources/tools/lopa - What is LOPA; Core Attributes; Independent Layer of Protection
Primary-text comparison: CCPS defines IPL as specific independent device/system/action preventing the given consequence and lists functionality, independence, reliability and auditability.
Original conditions: independent; functional; verifiable

### 12. hazop_lopa_ipl_independence - REVISE_REQUIRED
Original fact: IPL credit은 initiating event와 다른 IPL로부터 충분히 독립되어야 하며, 공유 자원과 공통원인에 따른 동시 상실 가능성을 평가·관리한 근거가 필요하다.
Source: https://ccps.aiche.org/resources/tools/lopa - Independent Layer of Protection; Core Attributes
Primary-text comparison: CCPS requires independence from initiating event and other credited IPLs. It does not detail every shared-resource mitigation proof or a universal CCF calculation.
Original conditions: shared_dependencies_assessed
Proposed source-bounded replacement (NOT promoted): Credited IPL must operate independently of its initiating event and other credited protection layers for the defined scenario; examine any dependencies that could defeat this assumption.

### 13. hazop_lopa_initiating_event_frequency - REVISE_REQUIRED
Original fact: Initiating event frequency는 원인 사건이 분석조건에서 발생하는 빈도이며 설비 이력, 신뢰성 자료와 적용 경계를 근거로 정한다.
Source: https://ccps.aiche.org/resources/tools/lopa - Basic LOPA Steps; Initiating Events
Primary-text comparison: CCPS confirms estimating initiating-event frequency, but the exact source-of-history and reliability-data quality requirements in the original statement are not specified on this page.
Original conditions: defined_analysis_boundary; data_basis_documented
Proposed source-bounded replacement (NOT promoted): For each defined scenario, identify the initiating event and assign a documented, analysis-bounded initiating-event frequency with a suitable evidence basis.

### 14. hazop_lopa_enabling_and_conditional_modifiers - REVISE_REQUIRED
Original fact: Enabling condition과 conditional modifier는 실제 노출시간, 점화확률, 재실확률 등 scenario에 필요한 조건부 확률만 근거 있게 적용한다.
Source: https://ccps.aiche.org/resources/tools/lopa - Conditional Modifier; Enabling Conditions
Primary-text comparison: CCPS distinguishes enabling conditions and conditional modifiers but does not in this source page enumerate ignition, occupancy, exposure formulas or prescribe all double-counting rules.
Original conditions: relevant_to_scenario; no_double_counting
Proposed source-bounded replacement (NOT promoted): Include enabling conditions and conditional modifiers only when relevant to the defined scenario; they are distinct and not mandatory in every LOPA.

### 15. hazop_lopa_ipl_dependability_auditability - REVISE_REQUIRED
Original fact: IPL은 요구 시 동작할 충분한 dependability와 시험·정비·기록을 통한 auditability를 갖추어야 하며 주장한 PFD를 수명주기 동안 유지해야 한다.
Source: https://ccps.aiche.org/resources/tools/lopa - Core Attributes; LOPA Components
Primary-text comparison: CCPS lists reliability, integrity and auditability, but this page does not establish original claim's specific throughout-lifecycle numerical PFD guarantee or exact testing cycle.
Original conditions: lifecycle_maintenance
Proposed source-bounded replacement (NOT promoted): A credited IPL should possess adequate reliability, integrity and auditability for its scenario. Numerical lifetime performance and test/maintenance provisions require additional primary evidence.

### 16. hazop_lopa_consequence_without_credited_protection - REVISE_REQUIRED
Original fact: LOPA consequence는 해당 scenario에서 credit하려는 보호계층의 효과를 먼저 포함하지 않은 상태로 정의해야 순환논리와 이중계산을 피할 수 있다.
Source: https://ccps.aiche.org/resources/tools/lopa - Basic LOPA Steps
Primary-text comparison: CCPS instructs defining consequence and then applying IPL PFD. It does not state the exact universal consequence-endpoint treatment or all baseline protection conventions.
Original conditions: scenario_endpoint_consistent; no_double_counting
Proposed source-bounded replacement (NOT promoted): Define scenario cause-consequence endpoint consistently before crediting independent protection layers; record which safeguards are and are not credited.

### 17. hazop_lopa_tolerable_event_frequency - REVISE_REQUIRED
Original fact: Tolerable event frequency는 회사 또는 사업장의 승인된 위험수용기준에서 consequence category별로 정하며 분석자가 임의로 선택하지 않는다.
Source: https://ccps.aiche.org/resources/tools/lopa - Basic LOPA Steps
Primary-text comparison: CCPS directs risk evaluation after mitigation but this page does not state whose risk acceptance criteria must be used or how categories are authorized.
Original conditions: consequence_category_defined
Proposed source-bounded replacement (NOT promoted): Compare scenario mitigated consequence frequency with the applicable organization's defined risk acceptance criteria; do not invent universal thresholds.

### 18. hazop_lopa_ipl_specificity - KEEP_BOUNDED
Original fact: IPL은 분석한 원인–결과 scenario에 실제로 작동하는 구체적 보호기능이어야 하며 일반적인 좋은 설계나 교육만으로 자동 credit할 수 없다.
Source: https://ccps.aiche.org/resources/tools/lopa - Independent Layer of Protection; Core Attributes
Primary-text comparison: CCPS defines scenario-specific protection device, system or action and its functionality, independence and reliability attributes.
Original conditions: functionality_demonstrated

### 19. hazop_lopa_no_double_counting - KEEP_BOUNDED
Original fact: 동일 Sensor, Logic Solver, Final Element, Utility 또는 동일 작업자 대응에 의존하는 보호기능은 독립성이 입증되지 않으면 서로 다른 IPL로 중복 credit하지 않는다.
Source: https://ccps.aiche.org/resources/tools/lopa - Independent Layer of Protection; Basic LOPA Steps
Primary-text comparison: An IPL must be independent of the initiating event and other IPLs, so the same dependent safeguard cannot be treated as two independent PFD factors; specific sensor-sharing examples need case-specific review.
Original conditions: common_cause_reviewed

### 20. hazop_lopa_common_cause_dependency - REVISE_REQUIRED
Original fact: 공통 전원·배관·계측탭·환경·정비절차·소프트웨어와 같은 dependency는 IPL 곱셈 전에 식별하고 독립성 또는 공통원인 보정을 검토해야 한다.
Source: https://ccps.aiche.org/resources/tools/lopa - Core Attributes; Independent Layer of Protection
Primary-text comparison: The necessity of IPL independence is explicit, but the full enumerated common-cause checklist and model calculation are not covered by this webpage.
Original conditions: before_multiplying_ipl_pfds
Proposed source-bounded replacement (NOT promoted): Before multiplying credited IPL failure probabilities, check whether protection layers depend on common conditions or resources that would violate their independence.

### 21. hazop_lopa_bpcs_ipl_credit - REVISE_REQUIRED
Original fact: BPCS 기능을 IPL로 credit하려면 initiating cause와의 독립성, 감지–판단–조작 경로, 고장모드와 성능 근거를 확인해야 하며 BPCS가 원인인 경우 같은 기능을 자동 credit할 수 없다.
Source: https://ccps.aiche.org/resources/tools/lopa - Independent Layer of Protection; Core Attributes
Primary-text comparison: Core CCPS IPL independence rule is supported; BPCS-specific detection/action chain and initiating-cause exceptions require a BPCS-specific source.
Original conditions: initiating_cause_not_same_function
Proposed source-bounded replacement (NOT promoted): A BPCS control layer may only be credited as an IPL when its specific scenario protection and independence are demonstrated; BPCS-specific evidence must be verified separately.

### 22. hazop_lopa_residual_frequency_after_existing_ipls - KEEP_BOUNDED
Original fact: 기존 non-SIS IPL을 반영한 residual frequency가 허용빈도보다 크면 그 차이를 줄일 추가 위험감소가 필요하다.
Source: https://ccps.aiche.org/resources/tools/lopa - Basic LOPA Steps
Primary-text comparison: CCPS explicitly combines initiating frequency and IPL PFD to find mitigated consequence frequency and assesses whether additional IPL is needed.
Original conditions: same_scenario_endpoint; same_time_basis

### 23. hazop_lopa_no_additional_sif_when_ratio_below_one - REVISE_REQUIRED
Original fact: 정의된 LOPA scenario에서 required RRF가 1 이하이면 해당 빈도 기준만으로는 추가 SIF 요구가 발생하지 않으나, 다른 scenario와 ALARP 검토는 별개다.
Source: https://ccps.aiche.org/resources/tools/lopa - Basic LOPA Steps
Primary-text comparison: CCPS indicates whether additional IPL is required from scenario risk but does not define required RRF <=1 as a no-SIF rule or address other ALARP requirements.
Original conditions: single_defined_scenario; other_risk_obligations_remain
Proposed source-bounded replacement (NOT promoted): If the evaluated scenario already meets its accepted frequency criterion, the LOPA calculation alone does not establish a need for another IPL; assess other scenarios and requirements separately.

### 24. sil_hazard_scenario_boundary - REVISE_REQUIRED
Original fact: 목표 SIL은 initiating event, 운전조건, consequence endpoint와 필요한 safe state가 명확한 위험 시나리오별로 결정한다. 서로 다른 원인이나 결과를 한 빈도로 뭉치지 않는다.
Source: https://ccps.aiche.org/resources/tools/lopa - What is LOPA; Basic LOPA Steps
Primary-text comparison: CCPS explicitly restricts the analysis to a single cause-consequence pair; it does not directly establish target SIL determination or all required safe states.
Original conditions: cause_and_consequence_defined
Proposed source-bounded replacement (NOT promoted): For LOPA, define each single cause–consequence scenario clearly before calculating needed risk reduction. Specific SIF/SIL allocation requires further IEC functional-safety evidence.

### 25. sil_initiating_frequency_modifiers - REVISE_REQUIRED
Original fact: 보호계층 적용 전 시나리오 빈도는 initiating event frequency에 실제 노출시간, 점화확률, 재실확률 등 해당 시나리오에 필요한 enabling condition과 conditional modifier를 곱해 산정한다.
Source: https://ccps.aiche.org/resources/tools/lopa - Basic LOPA Steps; Enabling Conditions; Conditional Modifier
Primary-text comparison: Source lists event frequencies and separate modifiers but not the original unconditional multiplicative factorization or examples for all cases.
Original conditions: scenario_specific; no_double_counting
Proposed source-bounded replacement (NOT promoted): Determine initiating-event frequency for the defined scenario and apply relevant enabling conditions and conditional modifiers using defensible assumptions; check the exact formula against a detailed LOPA reference.

### 26. sil_existing_ipl_independence - REVISE_REQUIRED
Original fact: 기존 보호수단은 specificity, independence, dependability와 auditability를 만족할 때만 IPL credit을 부여하며 BPCS·alarm·operator action·SIS가 센서, 전원, 로직 또는 인력을 공유하면 종속성과 공통원인을 반영한다.
Source: https://ccps.aiche.org/resources/tools/lopa - Independent Layer of Protection; Core Attributes
Primary-text comparison: Source supports generic IPL attributes, but detailed SIF/BPCS/operator shared-resource assessment and SIL credit need corroborating authority.
Original conditions: shared_resources_assessed
Proposed source-bounded replacement (NOT promoted): Credit only defined, sufficiently independent and reliable protection layers for a specific cause-consequence scenario; assess common resource dependencies rather than assuming all protective actions are independent.

### 27. delay_and_nonminimum_phase_design_limits - REVISE_REQUIRED
Original fact: A pure delay e^(−sτ) has unit magnitude and phase −ωτ radians; this phase lag grows with frequency, while right-half-plane zeros add nonminimum-phase lag and constrain achievable closed-loop bandwidth and stability margins.
Source: https://www.mathworks.com/help/control/ug/analyzing-control-systems-with-delays.html - Control of Processes with Delays; Pade Approximation
Primary-text comparison: MathWorks confirms delay's linear phase shift and bandwidth/stability constraint, but this page does not independently establish RHP-zero phase constraints as a combined claim.
Original conditions: continuous_time_pure_delay; omega_in_radians_per_time_unit; tau_in_matching_time_unit
Proposed source-bounded replacement (NOT promoted): An ideal transport delay e^(−sT) has unit frequency-response magnitude and phase −ωT, adding phase lag that can constrain stability margins and bandwidth. Assess right-half-plane zeros separately using a source covering nonminimum-phase zeros.

### 28. feedback_stability_bandwidth_tradeoff - REVISE_REQUIRED
Original fact: 루프 대역폭 증가는 조건에 따라 추종과 외란응답을 빠르게 할 수 있지만 성능과 안정여유의 절충이 필요하다. 시간지연은 위상을 추가로 낮춰 대역폭과 폐루프 안정성을 제한한다. 폐루프 설계에서는 제어 대역 밖의 측정잡음 민감도와 미모델 동특성도 함께 제한해야 하며, 높은 대역폭을 무조건 목표로 삼지 않는다.
Source: https://www.mathworks.com/help/control/ug/analyzing-control-systems-with-delays.html - Control of Processes with Delays; Sensitivity Analysis
Primary-text comparison: MathWorks supports delay-related phase lag, stability and bandwidth tradeoff; it does not directly establish the complete original sensor noise, unmodelled dynamics and actuator-constraint checklist.
Original conditions: plant_dynamics_and_uncertainty_considered; delay_present_for_delay_claim
Proposed source-bounded replacement (NOT promoted): Delays add frequency-dependent phase lag and can limit achievable closed-loop bandwidth and stability; evaluate model fidelity and design constraints for the specific process.

### 29. routh_time_delay_requires_approximation_or_frequency_method - KEEP_BOUNDED
Original fact: Routh–Hurwitz 판별은 유한차수 다항식의 근을 대상으로 하므로 e^(−Ls)가 포함된 초월 특성방정식에는 직접 적용할 수 없고, Padé 근사 등 유한차수 근사나 Nyquist 같은 주파수영역 방법을 사용한다.
Source: https://www.mathworks.com/help/control/ug/analyzing-control-systems-with-delays.html - Control of Processes with Delays; Pade Approximation
Primary-text comparison: Characteristic equation containing e^(−sT) is not a finite polynomial, so a polynomial Routh array cannot operate on the exact delay. MathWorks describes explicit delay models and finite-dimensional Pade approximations, warning to verify their range.
Original conditions: exact_delay_retained

### 30. compensator_design_trades_crossover_margins_low_frequency_gain_and_noise_under_model_uncertainty - REVISE_REQUIRED
Original fact: Loop-shaping a lead/lag or PID compensator involves application-specific choices of crossover/bandwidth, stability margins, low-frequency gain for tracking/disturbance rejection, and high-frequency roll-off for noise and model uncertainty. Before deployment, check whether the linear design remains acceptable over relevant operating points and nonidealities such as process delay, actuator saturation/rate limits, valve deadband and model error; linear Bode margins alone do not represent all nonlinear implementation behavior. The target values and validation tests depend on the loop's operating envelope and risk/performance requirements.
Source: https://www.mathworks.com/help/control/ug/analyzing-control-systems-with-delays.html - Control of Processes with Delays; Sensitivity Analysis
Primary-text comparison: Source covers process-delay analysis and approximation sensitivity, not every listed controller design constraint, gain-noise tradeoff or field validation workflow.
Original conditions: crossover_and_margins_are_selected_for_the_plant_and_performance_requirements; high_frequency_rolloff_considers_noise_and_model_uncertainty; delay_and_plant_variations_are_included_in_robustness_checks; actuator_limits_and_valve_deadband_are_tested_when_present; linear_margins_do_not_replace_nonlinear_or_field_validation
Proposed source-bounded replacement (NOT promoted): In compensator design for processes with delay, check closed-loop stability and performance under the actual delay and verify any Pade approximation; the complete noise, uncertainty, actuator and field checklist needs separate source evidence.

### 31. lead_lag_rhp_zero_and_delay_bandwidth_constraints - REVISE_REQUIRED
Original fact: A right-half-plane (non-minimum-phase) zero typically constrains closed-loop bandwidth to below the zero frequency to preserve phase/performance margin, while a pure delay contributes phase lag proportional to frequency and therefore constrains crossover and stability-margin selection. These are plant-dependent limitations; a lead compensator cannot provide arbitrary bandwidth or response speed irrespective of them.
Source: https://www.mathworks.com/help/control/ug/analyzing-control-systems-with-delays.html - Control of Processes with Delays
Primary-text comparison: The delay bandwidth effect is directly supported; the particular RHP-zero bandwidth target and lead-compensator limitations are not established by this page.
Original conditions: rhp_zero_bandwidth_limit_is_a_design_rule_not_universal_exact_bound; pure_delay_phase_lag_is_minus_omega_times_delay; actual_limit_depends_on_plant_model_and_performance_requirements
Proposed source-bounded replacement (NOT promoted): Transport delay adds −ωT phase lag and can limit compensator crossover/bandwidth; additional nonminimum-phase zero limitations require separate evidence and plant-dependent design.


## Safeguards

The previously excluded 276 records remain excluded and are not promoted. Neither original Registry nor source Topic Packs, generated rubric banks nor actual grading code has been changed by this report. Before admitting revised claims into core scoring, update authoritative source Fact/Anchor with full evidence, regenerate outputs and perform regressions/release gates.  No release validation has been run. All other Queue entries remain source-unverified even if legacy Registry says verified.
