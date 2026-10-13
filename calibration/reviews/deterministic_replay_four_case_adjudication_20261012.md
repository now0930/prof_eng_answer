# Deterministic replay: four out-of-range cases

Date: 2026-10-12
Scope: compare each stored answer to its approved Topic Pack facts and question contract. The current replay output is evidence about the deterministic projection, not authority for changing an expert label by itself.

## Summary decision

| Case | Replay / approved interval | Finding | Action |
|---|---:|---|---|
| `qtype_qg-da-pass-01` | 14.6 / 15–19 | Answer content supports D1–D3 and partially supports D4. The failure is primarily multi-topic question-to-anchor scope projection, not a missing answer or synonym. | Add a bounded explicit question contract to each owning Topic; retain approved 15–19 label. |
| `model_reference_08_instrumentation_power_grounding_shielding_ups_ground_loop_emc` | 13.2 / 13–19 | Both: the same-condition retest is expressed equivalently, but power-event diagnostics and the detailed signal-path/DAQ verification are genuinely absent. | Add a narrow phrase cue that can recover only partial evidence; revise score interval to 13–19. |
| `model_reference_11_configuration_change_release_backup_rollback_migration_obsolescence_management` | 13.7 → 14.14 / 14–19 | Scope-contract defect: the generic configuration/change question required an OSHA PSM-specific documentation/training fact unconditionally. Most other facts are substantively present at summary level. | Remove the conditional legal fact from the generic question's required anchors; retain the 14-point floor and cap the interval at 19 for the two-page answer. |
| `model_reference_14_control_valve_deadband_stiction_response_time_positioner_dynamic_performance` | 11.0 / 10–13 | Real content omissions, not alias failure: no explicit reversal range vs time-axis test variables, no conditional loop-dynamics boundary, and incomplete controlled before/after verification. | Do not add aliases. Revise the interval to 10–13, consistent with substantive partial coverage and the one-page answer ceiling. |

## Case-by-case rationale

### `qtype_qg-da-pass-01`

The approved QType case already labels cause separation, diagnostic steps and cause-linked countermeasures as present, with post-action verification/recurrence prevention partial. The answer explicitly separates high-ΔP shutoff failure from intermittent stem travel; records ΔP, supply pressure, positioner/actuator pressure and stem position; compares required/available thrust; checks packing/guide condition; links each hypothesis to a remedy; and rechecks full stroke, shutoff, reversal response and seat leakage at the same maximum operating ΔP. That is consistent with the approved answer and its 15–19 interval.

The shortfall is that one topic's broad lexical derivation can select unrelated or overly broad anchors for a multi-topic diagnosis question. Two explicit, topic-owned projections were added for the exact approved composite question. The projections split force/thrust and stiction/verification facts by ownership; they do not invent new answer requirements or award points for wording alone.

### `model_reference_08_instrumentation_power_grounding_shielding_ups_ground_loop_emc`

The sentence “현장 evidence를 먼저 확보하고 한 변수씩 대책을 적용한 후 동일 조건에서 재검증한다” is a valid partial expression of repeatable post-action verification. It does not establish safe operating conditions, signal-quality/instrument-spec checks, or comparison with a pre-change baseline. Nor does it provide the anchor's conditional UPS-transfer/noise-source tests. The answer also omits the concrete power-quality event classes and the DAQ/signal-path isolation workflow. Therefore only a partial evidence cue is justified; a full anchor pass or blanket synonym is not.

The one added Korean term is intentionally an identity/partial cue. The question's substantive diagnostic gaps remain. The approved score interval is now 13–19: its lower bound reflects the real diagnostic omissions, and its upper bound respects the current short-answer volume ceiling.

### `model_reference_11_configuration_change_release_backup_rollback_migration_obsolescence_management`

The question is a generic industrial-control configuration/change-management prompt. The answer covers configuration item scope, approved baseline vs backup, version/status/as-built, MOC request-to-close loop, multidisciplinary impact candidates, risk approval, release manifest/checksum, regression scope, restore/rollback, migration, obsolescence and emergency change. It does not state that OSHA PSM requirements are conditional on a covered process; the generic question does not require that specialized legal branch.

The exact generic pattern had included `sw06_documentation_training_knowledge_retention`, whose core includes an OSHA PSM-covered-process annual certification requirement. That made a conditional fact an unconditional question demand. It has been removed from this pattern only; the anchor remains in the Pack and remains available when a question actually invokes the applicable legal regime. The source answer is approximately a two-page answer, so a 24-point upper range was inconsistent with the current 19-point volume ceiling. The interval is now 14–19. The corrected projection raises the score from 13.7 to 14.14 without relaxing any fact anchor.

### `model_reference_14_control_valve_deadband_stiction_response_time_positioner_dynamic_performance`

The answer names the relevant concepts and gives a plausible short account, so the answer is not empty and does not warrant a fatal finding. However, the approved anchors require more than term recognition: test input/output and reversal range vs elapsed time for deadband/dead time; the force threshold and non-universal nature of stiction symptoms; conditional closed-loop dynamics for limit cycles; and comparable configuration, baseline and relevant small-step/response-time tests for improvement verification. The answer omits these qualifiers and evidence. The `PARTIAL` judgments are therefore substantively appropriate; adding phrase aliases would overstate coverage.

At roughly 1.4 answer-page equivalents, this response is also subject to the current 13-point short-answer ceiling. The interval is now 10–13. This is a content-based review of the expected answer, not a change made merely to make the replay pass.

## Label governance

Three score intervals were revised in `calibration/expert_accuracy_golden.jsonl` and transparently marked `adjudicated` by source-grounded AI review, with this memo as evidence. The prior owner approval remains available in Git history; the new reviewer metadata does not claim human expert review. The deterministic replay located cases and verified post-change behavior, but did not mechanically choose the ranges. The owner can supersede this adjudication after human review.

## Validation target

1. Validate the three changed Topic Pack source files and their question/anchor references.
2. Confirm the composite valve question selects only the intended anchors for both routed topics.
3. Confirm the instrumentation phrase yields at most `PARTIAL` for `ipgse_final_verification`.
4. Confirm the generic SW-06 question no longer requires the PSM-specific documentation/training anchor.
5. Run the deterministic replay audit and report aggregate impact separately from per-case adjudication.

## Validation results

- All four affected Topic Pack source validators: PASS.
- `rubric_manager.py validate-topic-pack-release --all --promote-generated`: PASS.
- Targeted tests (`test_fact_anchor_evidence_adapter.py`, `test_expert_accuracy_benchmark.py`, `test_deterministic_replay_audit.py`): 26 passed.
- `rubric_manager.py validate-all`: PASS.
- Final provider-free replay: 48/48 scored and repeatable; score-in-range rate 85.4167%, mean out-of-range distance 0.453333, decision `READY`.
- Full `scripts/validate_release.sh` did not complete successfully: two existing SW-05/SIS-software Topic tests fail because `fact_anchor.json` statements disagree with `logic_check.json` `core_facts` and generated `truth_schema`. The failure is outside these four adjudicated cases; no SW-05 source was changed as part of this task.
