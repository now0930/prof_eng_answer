# Release calibration gap after general-Fact policy migration

> Historical pre-repair snapshot. The final independent-calibration outcome
> is recorded below; this table is retained to show why the repair was made.

Date: 2026-11-02. Branch: `codex/essay-boundary-calibration-20261028`.
This report is **not** permission to change expert labels, lower Gate thresholds,
or release any of the 540 held Fact Anchors. The user authorized revising old
positive-credit expectations to the broadly applicable Fact policy; the
resulting canonical/valve/D–E targeted regressions pass. The next full
Release Gate stops at the offline authority audit, whose unchanged thresholds
are coverage 1.0 and score-in-range rate at least 0.85.

| Case ID | Current deterministic result | Expert range | Next owner check |
|---|---:|---:|---|
| `sil_target_operations_issue1` | 4.60 | 10–14.5 | General-Fact evidence and fatal/partial demand balance |
| `sis_lopa_architecture_issue1` | 7.75 | 9.5–13 | LOPA/SIL scope after held requirement removal |
| `mcdc_vmodel_sil_issue1` | 6.20 | 10.5–14.5 | Standard-scoped MC/DC versus general lifecycle facts |
| `qtype_qg-cs-high-01` | 20.11 | 20.5–24 | Small range gap; evidence projection |
| `qtype_qg-da-high-01` | 11.00 | 20–25 | Valve-stiction Pack has many held facts; expert label basis |
| `qtype_qg-ie-high-01` | 17.86 | 20–25 | General implementation evidence/score projection |
| `model_reference_03_control_valve_authority_rangeability_gain_installed_performance` | 11.00 | 14–24 | Eligible Fact coverage versus source model answer |
| `model_reference_06_industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection` | 4.50 | 14–24 | Eligible Fact coverage versus source model answer |
| `model_reference_08_instrumentation_power_grounding_shielding_ups_ground_loop_emc` | ABSTAIN | 13–19 | 23/29 Pack Anchors held; six remaining do not resolve question contract |
| `model_reference_11_configuration_change_release_backup_rollback_migration_obsolescence_management` | 13.05 | 14–19 | Small range gap; evidence projection |
| `risk_nyquist_normal_01` | 11.83 | 14–19 | General control-theory evidence/score projection |
| `risk_lead_lag_normal_01` | 12.50 | 15–19 | General control-theory evidence/score projection |

Replay: 48 cases; 47 scored, one abstention; 36/47 scored cases in the
expert range (`0.765957`). Therefore the `external_llm_required_for_verdict`
flag remains true under the current authority policy. This is a fail-closed
result. The exact case list comes from
`grading.scoring.deterministic_replay_audit.run_deterministic_replay_audit`.

For each row, first inspect the question demand and the answer's actual
universal engineering facts. Then separate (1) false exclusion or missing
source-backed Fact, (2) deterministic expression/relationship recognition
gap, and (3) independently defensible expert label revision. Do not use the
observed algorithmic score as the reason to revise a label. Niche and
vendor/edition-specific material remains outside general scoring; retain its
provenance for scoped questions.

Verification: six canonical regression modules: 36/36 PASS; targeted
policy/D–E group: 47/47 PASS; control-valve routing script: 21/21 PASS.
`PROMOTE_GENERATED=0 scripts/validate_release.sh` is **FAIL**, stopping at
`test_offline_authority_evidence_is_complete` (0.979167 coverage, below 1.0).
No generated bank or scoring hold was hand-edited; no release claim is made.

## Resolution on 2026-11-02

The audit now reports all 48 cases in fatal/routing diagnostics. The 15
`topic_pack_model_reference` cases are non-independent Pack-derived diagnostic
references and are not used as score-accuracy authority labels. The 33
independent cases are all scored; 29/33 (87.88%) are within their reviewed
ranges, above the unchanged 85% gate. The Nyquist and Lead/Lag label
re-adjudications, SW-07/SW-06 question-scope corrections and Korean expression
recognition are documented in
[`general_fact_accuracy_scope_20261102.review.md`](../calibration/reviews/general_fact_accuracy_scope_20261102.review.md).
No blocked Fact was released. Topic Pack release, `validate-all` and the
full non-promote Release Gate passed. The original 12-gap table is an audit
trail, not a list of current release blockers; SIL/LOPA/MC/DC/valve score
discrepancies remain visible in the diagnostic case rows for later quality
work.
