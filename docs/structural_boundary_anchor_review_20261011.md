# Structural cross-Topic boundary-anchor review — 2026-10-11

## Scope and classification

The 2,073-anchor inventory currently contains 2,065 technical Fact anchors and eight
cross-Topic ownership boundaries. These boundaries are not technical Facts and are not
added to `approved_fact_registry.json`. Their review asks only whether each
referenced target Topic Pack exists and contains the subject matter the source
boundary assigns to it. This is an internal structure check, not independent
engineering fact verification.

| Boundary anchor | Target Topic Pack | Internal evidence checked | Result |
|---|---|---|---|
| `ipgse_topic2_boundary` | `instrumentation_installation_wiring_impulse_tubing_inspection_codes` | Target anchors cover cable routing/mechanical protection, glands, terminals, and impulse lines. | Structural scope confirmed; not a technical Fact. |
| `ipgse_topic3_boundary` | `instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification` | Target anchors cover EMC emission/immunity, test categories, temperature, and vibration qualification. | Structural scope confirmed; not a technical Fact. |
| `ipgse_topic4_boundary` | `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | Target anchors cover hardware lifecycle, component selection, and production-test coverage. | Structural scope confirmed; not a technical Fact. |
| `ipgse_topic5_boundary` | `electronics_error_noise_drift_tolerance_aging_power_mitigation` | Target anchors cover noise, drift, tolerance, aging, and power-supply sensitivity. | Structural scope confirmed; not a technical Fact. |

All four target directories and `fact_anchor.json` files were present at review
time. The result is recorded in `reports/full_topic_fact_source_audit_20261010.json`
under `totals.structural_boundary_reviews`. These four must not be included in the
technical-Fact verified count; they remain separately classified in the 2,073
inventory total.

## Follow-up: additional pure ownership hand-offs (2026-10-11)

Four anchors in `balanced_trim_unbalanced_trim_structure_sealing_applications`
contain only a Topic ownership assignment and no independent engineering proposition:

| Anchor | Assigned owner | Pack evidence |
|---|---|---|
| `actuator_sizing_topic1_handoff` | `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe` | `control_valve_actuator_sizing_worst_case_conditions`, `control_valve_fail_close_force_balance`, `control_valve_fail_open_force_balance` |
| `body_cage_guide_topic4_handoff` | `control_valve_types_globe_rotary_body_actuator_selection` | `cage_guided_alignment_and_flow_path`, `post_guided_plug_alignment`, `port_guided_plug_alignment`, `body_actuator_selection_multi_criteria` |
| `leakage_packing_topic13_boundary` | `control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions` | `shutoff_class_purpose_scope`, `packing_material_ring_arrangement`, `fugitive_emission_source_monitoring` |
| `severe_service_material_topic14_boundary` | `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles` | `hardfacing_coating_ceramic`, `cage_multihole_particle_sensitivity` |

The target Pack contents confirm repository subject ownership; this is not
independent engineering verification. These four are classified as structural
boundaries and kept out of the technical Fact registry. The dynamic-friction and
low-noise anchors were technically verified and narrowed: the former does not
attribute every hysteresis/dynamic symptom to packing friction, and the latter
states that balanced and noise-attenuation trim functions are distinct but may
coexist. Both are score-neutral verified Facts. Machine-readable boundary evidence is recorded in
`reports/structural_boundary_anchor_review_20261012.json`.

## Additional software-project and hazardous-environment ownership boundaries (2026-10-11)

Two further anchors were classified as repository ownership contracts:

| Source boundary | Destination scope checked |
|---|---|
| `sw04_sw10_boundary` | General software lifecycle Topic SW-04 → FAT/SAT/project execution Topic SW-10 |
| `hec_ownership_boundary` | Hazardous-environment controls → Ex/IS selection, environmental qualification, grounding/UPS and SIL/SIS Topics |

Target Pack anchor IDs are enumerated in the machine-readable review. For
`hec_ownership_boundary`, only the ownership allocation is structural; its technical
safe-state/fail-safe claims remain subject to separate Fact verification.

## Additional software and instrumentation ownership boundaries (2026-10-11)

The follow-up report separately checks source/target pack anchors for these
repository-internal handoffs. They contain no independent physical proposition and
are not technical Facts:

| Source boundary | Destination scope checked |
|---|---|
| `sw02_sw03_boundary` | SW-02 logic/state transitions ↔ SW-03 HMI/alarm/operator information |
| `sw02_sw05_boundary` | SW-02 operational logic ↔ SW-05 safety lifecycle/SIL/Safety V&V |
| `sw10_sw04_boundary` | SW-10 project/FAT/SAT execution ↔ SW-04 development lifecycle/RTM/tests |
| `sw10_sw02_boundary` | SW-10 interlock records/tests ↔ SW-02 interlock/trip logic |
| `sw10_sw03_boundary` | SW-10 alarm-list/testing records ↔ SW-03 alarm/operator-information scope |
| `sw04_sw05_boundary` | SW-04 general software lifecycle ↔ SW-05 safety lifecycle |
| `sw04_mcdc_detailed_coverage_boundary` | SW-04 lifecycle ↔ dedicated MC/DC structural-coverage Topic |
| `sw03_sw02_boundary` | SW-03 operator-information scope ↔ SW-02 interlock/trip logic |
| `sw03_sw04_sw10_boundary` | SW-03 operations information ↔ SW-04 lifecycle and SW-10 project acceptance |
| `sw08_sw07_boundary` | SW-08 timing/recovery ↔ SW-07 protocol/interoperability |
| `sw07_sw08_boundary` | SW-07 communications ↔ SW-08 timing/recovery |
| `sw07_sw09_boundary` | SW-07 communications ↔ SW-09 cybersecurity |
| `sis_mcdc_structural_coverage_boundary` | SW-05 safety context ↔ dedicated MC/DC Topic |
| `topic1_topic3_topic11_boundary` | Smart-positioner diagnosis ↔ valve-force, dynamic-performance and positioner Topics |
| `topic13_topic15_topic16_boundary` | Smart-positioner diagnosis ↔ leakage, SIS/PST and valve-package lifecycle Topics |

These assignments are validated only against the repository's declared source and
target Pack inventories. They do not assert that standards universally prescribe
these SW numbers, ownership boundaries, or exclusions. The machine-readable report
contains per-target anchor IDs; the structural regression checks that every source
and target anchor exists and that these boundaries do not enter the technical Fact
registry.

## Additional valve and installation-topic ownership boundaries (2026-10-11)

Eight more source anchors were confirmed as repository routing/handoff contracts
only. Their destination Pack anchors are listed in the machine-readable report:

| Source boundary | Destination scope checked |
|---|---|
| `smart_diagnostics_topic12_handoff` | Conventional positioner Topic → smart diagnostics/signature Topic 12 |
| `sis_esd_pst_topic15_handoff` | Conventional positioner Topic → SIS/ESD/PST final-element Topic 15 |
| `package_workflow_topic16_handoff` | Positioner accessories Topic → valve-package lifecycle Topic 16 |
| `topic1_topic3_topic10_boundary` | Seat leakage Topic → actuator sizing, dynamic performance, and balanced-trim Topics |
| `topic11_topic12_topic14_boundary` | Seat leakage Topic → positioner, diagnostics, and severe-service Topics |
| `iiwic_pid_document_boundary` | Field installation Topic → P&ID design Topic |
| `iiwic_hazardous_area_boundary` | Field installation Topic → hazardous-area/Ex/IS selection Topic |
| `iiwic_topic1_boundary` | Field installation Topic → grounding/power/EMC Topic |

The review confirms that the declared destination topics and anchor IDs exist. It
does not certify the technical correctness of facts inside those Topics. Mixed
boundary statements that also make physical, safety, or operating claims remain in
the technical review queue rather than being automatically reclassified.

## Additional qualification, IIoT and design-basis hand-offs (2026-10-11)

Six further boundaries were confirmed against their destination Pack inventories:

| Source boundary | Assigned destination |
|---|---|
| `ieeq_topic2_boundary` | Field installation/wiring/inspection Topic |
| `ieeq_topic4_boundary` | Control hardware lifecycle Topic |
| `ieeq_topic5_boundary` | Electronics error/noise/drift Topic |
| `iiot_protocol_connectivity_handoff` | Industrial wired/wireless communication Topic |
| `iiot_historian_mes_data_handoff` | Historian/MES/IT-OT data integration Topic |
| `iiwic_design_basis_boundary` | Instrumentation design-basis/codes/deviation Topic |

The corresponding target anchor IDs are enforced in the machine-readable boundary
review regression. Classification is internal content ownership only; any physical,
qualification, or process recommendation in adjacent anchors remains independently
subject to technical fact review.

## Additional pure ownership hand-off (2026-10-11)

`control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim/topic8_hydrodynamic_noise_handoff`
assigns cavitation, flashing, liquid choked-flow, and FL-factor material to Topic 8.
The target Pack contains anchors for liquid choked-flow capacity, cavitation/flashing
distinction, flashing, and FL meaning/relation to cavitation susceptibility. This
confirms the repository's ownership crosswalk only; it does not independently verify
the physical claims in Topic 8. The hand-off is recorded as structural and remains
outside `approved_fact_registry.json`.

## SW-06 lifecycle ownership hand-offs (2026-10-11)

Two SW-06 anchors are project-internal ownership declarations rather than
independent engineering facts:

| Boundary anchor | Assigned owner | Pack evidence |
|---|---|---|
| `sw06_sw04_boundary` | `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` (SW-04) | Requirements, architecture, development change impact, verification, validation and regression-test anchors. |
| `sw06_sw09_boundary` | `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` (SW-09) | Incident-response, trusted-recovery and security-backup anchors. |

These confirm repository taxonomy and subject handoff only. They do not assert
that external standards universally divide these activities under SW-04/SW-06/SW-09,
nor that either Topic owns all backup, recovery, change or verification activities
in every organization. Machine-readable references are recorded in
`reports/structural_boundary_anchor_review_20261012.json`.

The SW-06 Pack also contains `sw06_sw04_boundary` and `sw06_sw09_boundary`. These
are classified the same way: their target Pack inventories confirm the repository's
internal subject routing, but do not prove a universal standards-based responsibility
split. They remain outside the engineering Fact registry. `sw06_parallel_operation_controls`
is different: it makes technical risk/benefit claims about parallel operation and
remains unresolved until independently supported or narrowed.
