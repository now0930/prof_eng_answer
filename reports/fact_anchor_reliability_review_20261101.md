# Five independent fact comparisons (2026-11-01)

- `inherent_availability_mtbf_mttr_two_state_model`: KEEP_BOUNDED. NASA: https://www.nasa.gov/wp-content/uploads/2023/11/170508-formulas-inherent-availability-and-reliability-with-constant-failure-and-repair-rates.pdf . Steady-state two-state inherent availability is MTBF/(MTBF+MTTR), not operational availability with logistics downtime.
- `eem_uncertainty_combination_respects_correlation`: KEEP_BOUNDED. NIST TN 1297 section 5: https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty . Include covariance of correlated input quantities; simple RSS is not general.
- `markov_reliability_model_uses_system_states_and_transition_rates_to_track_state_probabilities`: KEEP_BOUNDED. ESA reliability handbook section 9.4.3: https://nrpmhandbook.reliability.space/en/stable/system/handbook/reliability_prediction/methods.html . Constant transition rates and defined mutually exclusive states are assumptions of the illustrated CTMC method.
- `pfdavg_approximation_requires_explicit_model_assumptions_and_scope`: KEEP_BOUNDED. Yokogawa IEC 61511 discussion: https://www.yokogawa.com/eu/library/resources/white-papers/effects-on-pfdavg/ . Specify low-demand operation, failure rate and test assumptions, and function boundary.
- `hazop_lopa_pfdavg_rrf_relation`: KEEP_BOUNDED. Same Yokogawa IEC 61511 interpretation: RRF=1/PFDavg for a low-demand SIF. Do not generalize to continuous/high-demand modes.

Review limitation: each named principle was source-compared; complete Topic Pack sentences and licensed IEC text were not inspected. These limits must carry into scoring.
