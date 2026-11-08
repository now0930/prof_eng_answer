# Balanced/Unbalanced Trim: 17 remaining claim-by-claim original-source checks (2026-11-01)

Baseline: commit `b339f694` on `codex/essay-boundary-calibration-20261028`, Topic Pack `rubrics/topic_packs/balanced_trim_unbalanced_trim_structure_sealing_applications/fact_anchor.json`. Reviewer: GPT-6; direct lookup of each *original canonical Anchor statement* against first-party sources. Neither a historic `verified` label nor the fact ID name was accepted as evidence.

**Outcome:** 12 KEEP_BOUNDED; 2 HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE; 3 SOURCE_CHECKED_VENDOR_APPLICATION_HOLD. **No generic scoring promotion** for the five source-scoped/insufficient cases. All 17 were previously PENDING in the exact 1,290 ID CSV. A manufacturer-specific maintenance recommendation is not transformed into a universal law.

## Evidence sources and inspections

- **H** — Fisher/Emerson, Control Valve Handbook 5th edition (2017), §3.1.1.2–3 (pp.52–53), §5.2 (pp.95–96), §5.11.1 (pp.111–112): https://www.controlsouthern.com/getattachment/14bc18f1-f84e-4e5f-89eb-9cb31151946b/emerson-fisher-control-valve-handbook-fifth-edition.pdf
- **M** — Emerson Fisher, HP and HPA Valves Instruction Manual D101634X012, Aug 2024, §3.6 p.30, Fig.12 p.33: https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101634x012-hp-and-hpa-control-valves-fisher.pdf
- **P** — Parker Hannifin, O-Ring Handbook ORD 5700, §2.3 and damage analysis §10.5 (elastomer chemistry/extrusion/RGD): https://www.parker.com/content/dam/Parker-com/Literature/O-Ring-Division-Literature/ORD-5700.pdf
- **E-C** — Emerson Fisher easy-e EZ-C Cryogenic Control Valve, product original: https://www.emerson.com/en/final-control/products/fisher-ez-c
- **E-ED** — Emerson Fisher easy-e ED Control Valve, product original: https://www.emerson.com/en/final-control/products/fisher-ed
- **E-HPA** — Emerson Fisher HPAS Control Valve, product original: https://www.emerson.com/en/final-control/products/fisher-hpas
- **E-W** — Emerson Fisher WhisperFlo low-noise trim, product original: https://www.emerson.com/en/final-control/products/fisher-whisperflo

Web PDF screenshot pages were visually checked: H PDF page indexes 51, 52, 110, 111 (printed pp. 52, 53, 111, 112); M page indexes 30 and 33 (printed pp.30 and 33). Parker technical source's searchable publisher text was read for material scope; do not claim Parker PDF images visually checked.

## Individual verdicts

| Exact Fact ID | Verdict | Primary original locator | Reason, conditions and non-general-scoring boundary |
|---|---|---|---|
| `balance_seal_resistance_is_actuator_load` | `KEEP_BOUNDED` | H§5.11.1.4 | Seal friction adds to actuator force, but depends on seal construction; do not require an invented coefficient. |
| `balanced_globe_trim_seat_and_balance_seal_boundaries` | `KEEP_BOUNDED` | H§3.1.1.3; M Fig.12 | Separate body pressure containment, plug/cage regions, seat interface and plug-to-cage seal; this is a structural distinction, not a rule that each component is an identical external pressure vessel boundary. |
| `balanced_trim_defined_case_force_review_is_configuration_specific` | `HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE` | H§5.11.1 | Handbook verifies unbalance, seating, packing, special force components but NOT the claimed full Minimum/Normal/Maximum/startup/shutdown matrix as a general obligation. Do not admit this checklist as core grading. |
| `balanced_trim_elastomer_seal_compatibility_and_failure_modes_are_condition_specific` | `SOURCE_CHECKED_VENDOR_APPLICATION_HOLD` | P§2.3,§10.5; M Fig.12 | Swelling/shrinkage, extrusion and decompression damage are documented for elastomer compounds and selected constructions. Original multi-mode inspection checklist is too specialized to be mandatory generic balanced-trim scoring. |
| `balanced_trim_extreme_temperature_seal_checks_are_model_specific` | `KEEP_BOUNDED` | E-C; E-ED; P§2.3 | Cryogenic and hot service require matching material and seal design to specified operating conditions; no universal numeric limit or universal seal type. |
| `balanced_trim_particulate_blockage_risk_is_passage_and_model_specific` | `SOURCE_CHECKED_VENDOR_APPLICATION_HOLD` | M§3.6 p.30 | Original HP/HPA manual explicitly requires inspection and cleaning of balance holes, but this particular maintenance instruction and detailed slurry strainer guidance are not generic requirements for all balanced trims. |
| `control_valve_pressure_force_direction_is_construction_specific` | `KEEP_BOUNDED` | H§3.1.1.2–3; H§5.11.1.1 | Net force sign depends on flow-up/flow-down, plug/stem/seat geometry and pressure; cannot infer from a universal arrow. |
| `balanced_and_noise_attenuation_trim_are_distinct_coexisting_functions` | `KEEP_BOUNDED` | H§3.1.1.3; E-W | Pressure-balancing reduces static forces while low-noise staging manages flow energy. Fisher balanced cage constructions can also use noise-attenuation trims. No mandatory vendor design. |
| `balanced_trim_selection_should_be_reconciled_with_vendor_force_and_seal_data` | `SOURCE_CHECKED_VENDOR_APPLICATION_HOLD` | H§5.11.1.1,§5.11.1.4; M§3.6 | Manufacturer force and seal configuration matter; prescribing specific cutaway/force-table/maintenance document set as a scoring requirement is a procedural vendor-scoped checklist. |
| `balanced_trim_unbalance_force_equation` | `KEEP_BOUNDED` | H§5.11.1.1 p.111 | The signed net pressure force or magnitude follows ΔP times appropriate effective unbalance area in the stated static configuration. State units and pressure boundaries. |
| `balanced_trim_force_advantage_is_case_specific_in_high_dp_or_large_valves` | `KEEP_BOUNDED` | H§3.1.1.3,§5.11.1.1; E-HPA | Balanced plug can lower required thrust at high differential pressures when relevant compared with unbalanced construction; not an automatic selection for all sizes or fluids. |
| `balance_passage_equalizes_plug_pressure` | `KEEP_BOUNDED` | H§3.1.1.3; M§3.6 p.30 | Pressure balancing passage enables pressure communication, thereby reducing static plug load in the documented construction; does not imply zero net force. |
| `balanced_trim_force_reduction_area_ratio` | `KEEP_BOUNDED` | H§5.11.1.1 p.111 + F=ΔPA | For same ΔP and definitions, /Fr///Fu/=/Ar///Au/ under quasi-static comparison and nonzero denominator; not valid with differing force components or transient pressure gradients. |
| `balanced_trim_pressure_equalization_has_finite_transient` | `HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE` | H§3.1.1.3; M§3.6 | Pressure communication path established, but these inspected original pages do NOT characterize chamber transient/response time. Physical plausibility alone does not establish stated dynamic scope or a scoring threshold. |
| `balanced_trim_residual_unbalance_area` | `KEEP_BOUNDED` | H§5.11.1.1 p.111 | Handbook expressly documents small residual unbalance area even in balanced valves, with manufacturer-specified geometry. |
| `control_valve_effective_unbalance_area_definition` | `KEEP_BOUNDED` | H§5.11.1.1 p.111 | Effective/net unbalance area is the geometry-dependent area used to calculate resultant pressure force. Not necessarily equal to nominal port or seat area. |
| `plug_to_cage_and_seat_leakage_paths_are_distinct` | `KEEP_BOUNDED` | H§3.1.1.3; H§5.2; M Fig.12 | Leakage past plug-to-cage balance seal is distinct from leakage across closed plug/seat shutoff interface; seat-leakage class is a separately specified test basis. |

## Audit effects and release boundary

This review changes source-audit disposition and matching unresolved-source hold overlay only. Original Topic Pack statements, Registry legacy status, generated banks, deterministic A/B/C grading contract, 46 independent revision holds and 276 separate scoring exclusions remain untouched. Such source-audit KEEP_BOUNDED is not automatically a managed canonical source approval. Test snapshot expected after these 17 changes: 355 PENDING, 568 KEEP_BOUNDED, 31 insufficient-primary-source holds, 7 standard-scoped holds, 7 vendor-application holds, 46 REVISE_REQUIRED, 275 screening exclusions and one legacy scoped-only; total original 1,290. Executable unresolved-source holds 400 (355+31+7+7); old overlay 276 and independent revision overlay 46 unchanged. New pending items still require original material comparisons. Full release validation/managed approval not executed through this GitHub-only session; do not claim release PASS or merge draft PR until canonical regressions have been fixed and re-run.
