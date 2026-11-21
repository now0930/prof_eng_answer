# S7 B7: Five condition/dependency and Nyquist P/Z scope draft probes (2026-11-17)

## Baseline and boundaries

Last verified Actions run #43990318481 at be70a1424c22e589e242638fec84dc4ef2ed7514 completed with 1885 passed, 2 skipped, VALIDATION=PASS. Source review shows 119 HOLD unique Facts from 179 missing projections. Original canonical Claim Alignment: 0/20 authored positive and 0/20 authored adversarial cases with EXACT_RELATION. Formula shadow: 6 expected and 6 inverse. Registry source-borrowed ID bridge: 6 candidates and 14 unsupported nonformula facts. The 14-Fact triage piloted four authored pairs and left ten NOT_PROBED.

**New HEAD is NOT yet CI-validated. Prior PASS applies only to the older SHA.**

## Source-verified Registry relation identities

The following identities/conditions were directly read from the source-review Artifact for run #43984387892; this is not independent expert adjudication of answer text:

- safe_state_process_hazard_basis: final_element_safe_action_process_dependent, protective_system_safe_action depends_on process_hazard_and_safety_requirement; conditions safe_action_is_defined_for_the_specific_process and valve_mechanical_fail_action_is_not_assumed_to_equal_process_safe_state
- residual_frequency_before_sif: sil_residual_frequency_before_sif, pre_sif_residual_frequency equals initiating_rate_times_modifiers_and_existing_ipl_pfds; conditions consistent_consequence_endpoint and independent_ipl_credits
- thermocouple_measures_temperature_difference: thermocouple_measures_temperature_difference, thermocouple_emf depends_on measuring_and_reference_junction_temperatures; condition thermocouple_material_pair_known
- closed_loop_rhp_poles_count: closed_loop_rhp_poles_count, z_parameter counts closed_loop_rhp_poles; conditions no_unmodeled_cancellation and standard_negative_feedback
- open_loop_rhp_poles_count: open_loop_rhp_poles_count, p_parameter counts open_loop_rhp_poles; condition multiplicity_included

## Experimental scope and limits

The research-only module grading/evidence/s7_condition_scope_shadow.py checks five exact owner/source/relation identities, joins immutable source-review and prior nonformula-triage artifacts from the same execution SHA, and compares literal indicators in five author-drafted source-consistent texts and five author-drafted contrary texts.

The five paired contrasts are:
1. Process hazard/SRS-specific safe action versus universal fail-close regardless of hazard.
2. Independent IPL credits/consistent scenario for pre-SIF residual frequency versus double-counting dependent IPLs.
3. Known thermocouple material pair and reference junction versus EMF-only absolute temperature inference.
4. Nyquist Z: no unmodeled cancellation + negative feedback, zeros of 1+L(s) and closed-loop RHP poles versus zeros of L(s).
5. Nyquist P: open-loop RHP pole counts with multiplicity versus closed-loop poles without multiplicity.

An observed phrase is only a drafting cue; the answer's technical correctness, condition ID satisfaction, and generalizable natural-language semantics remain **NOT ESTABLISHED**. Explicit conflict, missing condition cue, negative/rejected context, ambiguous owner, alias drift, or data from another HEAD => HOLD. Never infer EXACT_RELATION, TRUE/FALSE grade, Fatal, WRONG, ceiling, A-E score, or candidate Aliases from the bridge.

Modules:
- grading/evidence/s7_condition_scope_shadow.py
- scripts/evaluate_s7_condition_scope_shadow.py
- tests/test_s7_condition_scope_shadow.py
- workflow non-gating seventh Artifact: s7-condition-scope-shadow

## Verification requirement

Manually run the validation workflow for the new HEAD, using the branch feat/claim-alignment-verification-20261114 with run_s7_experiment=OFF and run_s7_alias_diagnostics=ON. Audit all seven generated artifacts separately and check pytest and VALIDATION. Expected authored-pair cue accounting is 5 positive + 5 contrary, source_conditions_proven=0, answer_parsed_exact_relation_count=null; however do not claim these outputs as achieved before the new run completes.

Throughout: PR #38 Draft; 119 Facts HOLD; score_admission=DISABLED; B7/D2/D3 OPEN; no registry/ontology/topic pack/machine contract/scorer change, no main merge or deployment.
