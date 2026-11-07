# Independent primary-document review batch 05 — valve liquid/gas flow and analog wiring (2026-11-01)

Previous independently checked 100/1,290; newly reviewed 19; cumulative 119; still pending 1171. New KEEP_BOUNDED 8; new REVISE_REQUIRED 11; new empirically rejected 0.

Original issuing-authority sources (read publicly available HTML on 2026-11-01): Valmet Flow Control Manual Ch.3 https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/; Valmet Flow Control Manual Ch.4 https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/; National Instruments, Field Wiring and Noise Considerations for Analog Signals, updated Aug 15, 2024 https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html. Claim-to-section locator, original Fact and reason/possible correction below. Avoid interpreting vendor recommended numerical velocities as mandatory for every manufacturer or service.

### 1. control_valve_high_flow_velocity_depends_on_local_flow_area_and_volumetric_condition — KEEP_BOUNDED
- Original: High-flow service에서는 local flow area와 volumetric condition에 따른 velocity를 확인하고 trim throat, body outlet와 downstream pipe의 area 변화를 함께 검토한다.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/; section 3.1, 3.7
- Comparison: Valmet explicitly derives local velocity rise at vena contracta from flow area contraction and distinguishes actual valve/piping geometry.
- Original conditions: steady_one_dimensional_continuity_uses_volumetric_flow_equals_area_times_average_velocity; constant_density_liquid_flow_has_constant_volumetric_flow_along_the_flow_path; compressible_or_two_phase_flow_requires_local_density_or_phase_specific_flow_calculation; vena_contracta_location_and_actual_flow_area_depend_on_valve_style_size_and_pressure_conditions; attached_reducers_and_pipe_geometry_affect_local_velocity_and_pressure_loss

### 2. control_valve_low_reynolds_flow_requires_nonturbulent_sizing_correction — KEEP_BOUNDED
- Original: Low flow, high viscosity와 small passage에서는 Reynolds effect와 laminar correction을 확인하고 일반 turbulent-flow sizing을 그대로 적용하지 않는다.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/; section 3.2, Reynolds number factor FR
- Comparison: Valmet explicitly specifies FR correction for low-velocity/high-viscosity/small-size non-turbulent liquid flow; excluded non-Newtonian/suspension examples derive from separate IEC scope and are not being independently recertified.
- Original conditions: low_reynolds_or_nonturbulent_conditions_can_occur_with_high_viscosity_low_velocity_or_small_valve_size; the_reynolds_number_factor_corrects_control_valve_sizing_for_nonturbulent_flow_conditions; iec_60534_2_1_incompressible_equations_are_for_newtonian_incompressible_fluids_and_not_non_newtonian_fluids_slurries_or_liquid_solid_conveyance; correction_is_applied_only_when_the_standard_or_manufacturer_sizing_method_and_actual_flow_conditions_require_it

### 3. cryogenic_fluid_phase_state_can_change_with_heat_leak_and_pressure_reduction — REVISE_REQUIRED
- Original: Cryogenic fluid는 heat leak와 pressure reduction으로 vaporization, flashing와 two-phase flow가 발생할 수 있으므로 phase state와 sizing assumption을 확인한다.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/; section 3.3.3 Flashing
- Comparison: Valmet supports saturation/flashing from pressure reduction. This chapter does not explicitly assess cryogenic heat leak and two-phase thermodynamic phase equilibrium together.
- Original conditions: heat_input_can_boil_a_cryogenic_liquid_when_its_thermodynamic_state_reaches_saturation; pressure_reduction_below_the_liquid_vapor_pressure_can_vaporize_part_of_the_flow_and_create_flashing; whether_and_how_much_vapor_forms_depends_on_fluid_properties_pressure_temperature_and_heat_transfer; sizing_method_must_match_the_actual_single_phase_or_two_phase_state_and_applicable_standard
- Proposed corrected wording (NOT promoted): At local pressure below saturation pressure, an initially liquid stream may vaporize and flash downstream; cryogenic heat leak and fluid-property-specific two-phase behavior require separate thermodynamic source verification.

### 4. high_velocity_can_promote_valve_erosion_and_condition_dependent_flow_vibration_fatigue — REVISE_REQUIRED
- Original: High flow와 high velocity는 trim·body·downstream erosion, flow-induced vibration와 mechanical fatigue를 유발할 수 있다.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/; section 3.3.1, 3.3.3, 3.7
- Comparison: Valmet confirms cavitation/flashing-related erosion and vibration with velocity and materials; this chapter does not establish every original fatigue stress-cycle mechanism.
- Original conditions: erosion_location_and_rate_depend_on_phase_particle_content_material_and_local_valve_or_piping_geometry; high_velocity_is_a_contributing_erosion_factor_but_does_not_by_itself_determine_damage_rate_or_location; flow_induced_vibration_requires_dynamic_excitation_and_structural_response_and_is_affected_by_resonance_support_and_piping_layout; fatigue_damage_depends_on_stress_range_cycles_and_exposure_and_is_not_implied_by_high_flow_alone
- Proposed corrected wording (NOT promoted): High local flow velocity can aggravate erosion and, for flashing flow, vibration under affected flow, material and geometry conditions. Do not infer fatigue failure without dynamic stress/cycle analysis.

### 5. control_valve_outlet_geometry_and_downstream_piping_shift_local_flow_effects — REVISE_REQUIRED
- Original: Valve outlet jet, reducer, elbow와 downstream-pipe diameter는 velocity recovery, vibration, erosion와 noise의 위치를 바꿀 수 있다.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/; section 3.1; 3.3.1; 3.3.3
- Comparison: Valmet supports shifting cavitation collapse/noise downstream and geometry effects, but does not establish every reducer/elbow erosion/vibration maximum location.
- Original conditions: fittings_and_area_changes_disturb_the_flow_profile_and_must_be_included_in_installed_valve_sizing_and_assessment; flashing_or_cavitation_bubble_collapse_and_associated_noise_or_damage_can_extend_into_downstream_piping; erosion_and_vibration_location_depend_on_flow_regime_phase_particle_content_and_actual_geometry; the_claim_is_a_possible_location_shift_not_a_universal_prediction_of_peak_location_or_severity
- Proposed corrected wording (NOT promoted): Valves and downstream piping can experience shifting cavitation collapse, noise and flow/erosion effects as pressure recovery and phase regime change; severity and position require case-specific analysis.

### 6. control_valve_severe_service_risk_includes_cavitation_flashing_and_noise — REVISE_REQUIRED
- Original: Cavitation, flashing와 aerodynamic·hydrodynamic noise는 severe-service risk를 구성할 수 있으나 physics, prediction와 mitigation 상세는 Topic 8과 Topic 9가 소유한다.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/; section 3.3, 3.4
- Comparison: Valmet discusses cavitation, flashing, vibration and hydrodynamic noise, but the original statement also asserts aerodynamic sources and an internal Topic Pack ownership policy not verifiable from this source.
- Original conditions: cavitation_damage_and_noise_depend_on_vapor_bubble_formation_collapse_flow_velocity_material_and_valve_or_downstream_geometry; flashing_is_a_persistent_two_phase_flow_condition_that_can_cause_erosion_or_vibration_in_some_services; aerodynamic_and_hydrodynamic_noise_sources_and_mitigation_are_distinct_and_require_regime_specific_assessment; the_statement_is_a_severe_service_risk_handoff_not_a_claim_that_all_cavitation_flashing_or_noise_cases_cause_failure; repository_scope_assigns_cavitation_flashing_detail_to_control_valve_cavitation_flashing_choked_flow_damage_prevention_and_noise_detail_to_control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim
- Proposed corrected wording (NOT promoted): Cavitation, flashing and related hydrodynamic noise can represent distinct liquid-service risks; aerodynamic noise and repository ownership require separate evidence/administrative classification.

### 7. control_valve_aerodynamic_noise_from_turbulent_gas_flow — KEEP_BOUNDED
- Original: Control-valve aerodynamic noise arises from turbulent gas or steam flow and, in high-pressure-ratio or choked regimes, can include noise-producing interactions of shock waves and turbulence in the jet and downstream flow.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/; section 4.3.1
- Comparison: Valmet documents turbulent gas/steam throttling noise and, at critical/choked flow, shock-turbulence interactions.
- Original conditions: claim_is_limited_to_gas_vapor_or_steam_control_valve_service; claim_is_limited_to_compressible_gas_or_steam_throttling_in_a_control_valve; turbulence_is_a_noise_mechanism_and_shock_wave_interaction_is_high_pressure_ratio_or_choked_regime_specific; shock_waves_are_not_asserted_for_all_gas_service_or_all_pressure_ratios; no_universal_noise_level_or_attenuation_value_is_claimed

### 8. control_valve_high_pressure_ratio_jet_shock_interaction_noise — KEEP_BOUNDED
- Original: In high-pressure-ratio or choked gas/steam control-valve flow, interactions between shock waves and turbulence in the jet or downstream flow can be important aerodynamic-noise sources; this mechanism is not asserted for every gas condition.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/; section 4.3.1
- Comparison: Valmet specifically describes shocks and turbulent interactions under choked/high-pressure-ratio gas/steam service rather than every gas valve.
- Original conditions: mechanism_is_limited_to_high_pressure_ratio_or_choked_compressible_flow; shock_interaction_is_not_claimed_for_all_gas_or_steam_service; noise_prediction_depends_on_flow_regime_and_geometry; no_universal_noise_level_or_critical_pressure_ratio_is_claimed

### 9. control_valve_gas_choking_is_sonic_flow_capacity_limit — KEEP_BOUNDED
- Original: Gas/steam choking occurs when sonic velocity is reached at the vena contracta and, after the fully choked limit at fixed inlet pressure and valve opening, a further pressure-drop increase does not increase flow; it is a finite-flow regime used to select the applicable aerodynamic-noise model, not zero flow.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/; section 4.1 General; 4.2
- Comparison: Valmet distinguishes sonic inception from fully choked capacity limit, with no further flow rise at constant inlet pressure and valve opening.
- Original conditions: choking_definition_is_for_compressible_gas_or_steam_valve_flow; the_no_additional_flow_statement_applies_after_full_choking_at_fixed_inlet_pressure_and_opening; choked_flow_is_not_zero_flow; noise_prediction_regime_selection_depends_on_pressure_ratio_and_service_conditions

### 10. control_valve_aerodynamic_noise_depends_on_velocity_and_geometry — KEEP_BOUNDED
- Original: Aerodynamic-noise generation and prediction depend on flow velocity/sonic regime and the valve, trim, and downstream piping geometry; the prediction method uses service conditions and accounts for piping transmission when estimating external sound pressure.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/; section 4.3.1-4.4
- Comparison: Valmet noise models depend on flow velocity, Mach/shock flow regime and pipe/valve geometry and transmitted external SPL; no universal number is supported.
- Original conditions: claim_is_limited_to_compressible_gas_or_steam_control_valve_noise; velocity_and_mach_regime_are_not_interchangeable_without_speed_of_sound_and_state_conditions; downstream_pipe_transmission_is_distinguished_from_noise_generation_at_the_source; no_universal_velocity_or_mach_limit_is_claimed

### 11. control_valve_external_spl_depends_on_observation_and_environment — KEEP_BOUNDED
- Original: External sound-pressure level is a point/observer quantity that depends on source-to-observer distance and direction, and measurement or prediction conditions must account for the acoustic environment, reflecting surfaces, and noise-path treatments such as enclosures.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/; section 4.4 noise observation; environmental attenuation
- Comparison: Valmet explains observation distance, direction, wind/barriers and enclosure/sound-path attenuation; source power and observer SPL are distinct.
- Original conditions: external_spl_is_not_the_source_sound_power_level; distance_and_directional_effects_depend_on_source_geometry_and_radiation_pattern; reflection_and_environment_corrections_are_method_and_site_specific; enclosure_effect_is_treatment_specific_and_no_fixed_attenuation_is_claimed

### 12. control_valve_diffuser_pressure_drop_capacity_erosion_and_noise_must_be_evaluated — REVISE_REQUIRED
- Original: Diffuser·orifice는 system pressure drop을 분담하지만 capacity, erosion과 자체 noise를 함께 검토한다.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/; section 4.5 Diffusers; Attenuator plates
- Comparison: Valmet directly supports fixed diffuser sizing, pressure-drop split and separate noise sources but this page does not establish every erosion/wet-steam/fatigue checklist item.
- Original conditions: series_diffuser_use_is_scoped_to_a_suitable_pressure_drop_and_flow_case_not_all_control_valve_services; fixed_diffuser_or_attenuator_capacity_and_intermediate_pressure_are_sized_for_the_governing_flow_case; valve_and_diffuser_noise_are_evaluated_as_separate_sources_and_combined_by_the_selected_method; diffuser_flow_velocity_and_erosion_controls_depend_on_impurities_wet_steam_and_other_service_conditions; manufacturer_examples_and_recommendations_are_not_universal_device_performance_guarantees
- Proposed corrected wording (NOT promoted): A fixed downstream diffuser redistributes a specified pressure drop and must be sized for actual flow capacity while its own generated noise is included in a package estimate; evaluate erosion separately for the actual medium.

### 13. control_valve_noise_assessment_integrates_mechanism_path_mitigation_and_verification — REVISE_REQUIRED
- Original: Control valve noise 평가는 acoustic quantity, source mechanism, transmission path, mitigation과 field verification을 통합한다.
- Primary source: https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/; section 4.3-4.5
- Comparison: Valmet supports source mechanism, path transmission and source/path attenuation, not an unconditional mandatory field-measurement/validation step.
- Original conditions: this_is_an_engineering_assessment_framework_not_a_claim_that_one_standard_mandates_a_fixed_universal_workflow; aerodynamic_and_hydrodynamic_noise_methods_apply_to_different_flow_mechanisms_and_have_distinct_scope; transmission_path_and_external_sound_depend_on_pipe_and_observation_conditions; mitigation_is_selected_for_the_identified_source_and_path_and_remains_application_specific; field_measurement_is_used_for_validation_when_required_or_appropriate_and_is_not_assumed_to_be_part_of_every_prediction
- Proposed corrected wording (NOT promoted): For gas/steam valve noise, assess throttling-source mechanism, pipe/environment transmission path and suitable source/path mitigation; field verification is application dependent.

### 14. ipgse_vfd_motor_and_signal_cable_separation_reduces_coupling — REVISE_REQUIRED
- Original: Drive installation guidance recommends routing VFD motor/power cables away from control and signal cables, avoiding long parallel runs, and crossing near 90 degrees when crossing cannot be avoided. Increased separation and reduced overlap reduce capacitive and inductive coupling; exact spacing and routing rules remain device- and installation-specific.
- Primary source: https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html; section Minimizing Noise Coupling in Interconnects
- Comparison: NI establishes noise-coupling physics and cabling mitigation, but does not independently prescribe VFD-specific 90-degree crossing or drive-specific separation distances.
- Original conditions: the_statement_is_a_coupling_reduction_principle_not_a_guarantee_of_zero_interference; ninety_degree_crossing_is_a_drive_manufacturer_recommendation_when_crossing_is_unavoidable; minimum_separation_distance_is_not_universal_and_follows_the_applicable_drive_and_site_requirements
- Proposed corrected wording (NOT promoted): Reducing capacitive/inductive signal-cable coupling by geometry, separation and shielding is generally useful; VFD installation-specific routing rules must be taken from the drive manufacturer.

### 15. ipgse_emi_source_path_victim_and_coupling_types — REVISE_REQUIRED
- Original: EMC analysis identifies a disturbance source, a victim, and one or more coupling paths. Schneider Electric's Electrical Installation Guide lists common-mode impedance (galvanic), capacitive, inductive, and radiated coupling; conducted/common-impedance and field-coupling mechanisms require path-specific diagnosis and mitigation.
- Primary source: https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html; section Minimizing Noise Coupling; Balanced Systems
- Comparison: NI explains capacitive/inductive coupling and common-mode paths but the full named EMC taxonomy attributed to Schneider was not independently checked here.
- Original conditions: the_coupling_categories_are_diagnostic_models_and_multiple_paths_may_coexist; conducted_is_used_for_galvanic_or_common_impedance_transfer_not_as_a_synonym_for_all_coupling; specific_path_is_identified_for_the_actual_installation_before_selecting_mitigation
- Proposed corrected wording (NOT promoted): EMC troubleshooting identifies interference source, coupling mechanisms and vulnerable measurement input; validate common-impedance/capacitive/inductive/radiated mechanisms with authoritative EMC documentation.

### 16. ipgse_dc_distribution_capacity_drop_selectivity_and_return_path_review — REVISE_REQUIRED
- Original: DC instrumentation power distribution should be checked against the selected supply's capacity and load-step behavior, conductor voltage drop, branch protection/selectivity, and shared-return impedance effects on signal reference; the required checks and corrective measures depend on the connected loads, wiring, and protection design.
- Primary source: https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html; section Types of Signal Sources; Minimizing Noise Coupling
- Comparison: NI validates shared-ground/return and measurement-noise interactions but not supply capacity/load-step or branch selective protection design requirements.
- Original conditions: supply_capacity_and_load_step_performance_are_checked_against_the_actual_load_and_selected_supply_specification; conductor_voltage_drop_depends_on_load_current_wire_resistance_and_run_length; branch_selectivity_depends_on_supply_short_circuit_current_limit_and_selected_protection_devices; shared_return_impedance_can_couple_load_current_into_low_level_signal_measurements; design_values_and_protection_choices_are_installation_and_component_specific
- Proposed corrected wording (NOT promoted): Shared return/ground impedance and wiring reference selection can couple noise into instrumentation measurements; analyze DC supply capacity, voltage drop and selective protection separately using electrical installation standards.

### 17. ipgse_emc_source_path_victim_model_guides_layered_mitigation — KEEP_BOUNDED
- Original: EMC troubleshooting can be structured around an interference source, a coupling path, and a susceptible victim; mitigation may reduce emissions at the source, weaken or interrupt coupling, and/or improve victim immunity. This is a diagnostic framework, not a claim that one filter or grounding change will solve every installation.
- Primary source: https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html; section Minimizing Noise Coupling; Noise Reduction
- Comparison: NI shows distinguishing coupling mechanisms and matching noise-reduction methods rather than asserting one grounding change solves all interference.
- Original conditions: the_model_is_used_to_structure_emc_diagnosis_and_mitigation_not_as_a_complete_product_compliance_test; coupling_may_be_conducted_capacitive_inductive_or_radiated_as_relevant_to_the_installation; mitigation_is_selected_from_measured_or_reasonably_identified_source_path_and_victim_mechanisms; a_single_filter_or_grounding_change_is_not_assumed_sufficient_without_retesting_the_affected_system

### 18. ipgse_signal_cable_shield_is_not_assumed_pe_or_load_return — REVISE_REQUIRED
- Original: For instrumentation signal wiring, cable shields and drain wires are normally EMC coupling-control paths, not protective-earth conductors or normal load-return conductors. A cable shield or armor may serve as PE only where the specific power-cable construction and its conductivity meet applicable protective-conductor and fault-disconnection requirements.
- Primary source: https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html; section Minimizing Noise Coupling, shielding
- Comparison: NI supports shielding to reduce noise, but whether any cable shield/armor can act as PE and fault-disconnection rules requires separate electrical code evidence.
- Original conditions: signal_cable_shield_and_drain_wire_are_not_used_as_normal_load_return_paths_in_the_described_instrumentation_wiring; a_shield_or_armor_used_as_pe_is_a_specific_exception_for_a_cable_designed_and_verified_for_that_role; pe_suitability_requires_conductivity_and_fault_current_capacity_sufficient_for_protective_device_disconnection_under_applicable_rules; the_specific_cable_type_installation_and_local_electrical_code_control
- Proposed corrected wording (NOT promoted): Signal-cable shield/grounding treatment should be selected for EMC performance, without assuming shield is load return; PE adequacy is governed separately by applicable electrical safety standards.

### 19. ipgse_measurement_reference_ground_common_mode_and_ratings_checked_before_connection — REVISE_REQUIRED
- Original: Before measuring grounded or floating signals, identify the source and instrument reference relationship and keep every input within the instrument's specified common-mode/input limits. A ground-referenced input can create a ground-loop current or short a grounded source if connected with an incompatible reference; select differential, nonreferenced, or isolated measurement only as appropriate to the source and device. For hazardous electrical environments, verify the meter and leads/probes have ratings appropriate to the measurement category and voltage.
- Primary source: https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html; section Grounded Sources; Floating Sources; Common Mode
- Comparison: NI strongly supports DIFF/NRSE/RSE reference and CMRR limits, but hazardous-environment CAT meter/probe rating requirement is not part of this inspected source.
- Original conditions: common_mode_range_and_cmr_requirements_are_device_specific_and_must_be_checked_in_the_instrument_manual; ground_referenced_connection_to_grounded_source_with_different_reference_potential_can_create_ground_loop_current_or_short_the_source; differential_or_nonreferenced_configuration_is_recommended_for_the_described_ni_grounded_source_case_but_is_not_a_universal_prescription; measurement_category_and_voltage_ratings_must_suit_the_electrical_environment_for_both_meter_and_leads_or_probes; protective_earth_must_not_be_disconnected_as_a_noise_remedy
- Proposed corrected wording (NOT promoted): Identify the grounded/floating source, measurement reference and input common-mode limits before selecting measurement configuration; verify hazardous-environment measurement-category ratings separately.

## Status and safeguards
The 276 pre-excluded items remain excluded; new REVISE_REQUIRED items are NOT approved replacement scoring anchors. The Registry, Topic Packs, generated rubrics and runtime code are unchanged. No tests, CI, release gate or main merge were executed. Remaining claims retain independent review status NOT_PERFORMED irrespective of legacy verified status.
