# Fact Anchor 1,656 proposal reconciliation — 2026-11-04

Work branch: `codex/essay-boundary-calibration-20261028`; starting commit:
`1dc6878cc338abf35257e7adebdf5a40d3d87c8f`.
Private input ZIP SHA-256:
`218e38a415f8ee0ebdbb0a3b0f22b9c69d8b4f401b0c3ff8709cda90f1b05de4`.
The ZIP, its raw audit CSV and the 1,656-row private staging JSON are not
committed. Package `SHA256SUMS.txt` and its own validator passed. All 1,656
original `(topic_id, anchor_id, statement_sha256)` keys and statements match
the current branch's Topic Packs, with zero duplicates or mismatches.

## Decision, not an approval shortcut

| Proposal group | Rows | Action on this branch |
|---|---:|---|
| Prior strict verdict retained | 415 | Original statements and runtime behavior unchanged |
| New `SUPPORTED` / `SUPPORTED_WITH_SCOPE` proposals | 1,135 | Private staging only; **zero new operational approvals** |
| Proposed holds | 25 | 22 newly blocked; 3 existing canonical contracts held in staging pending conflict review |
| Proposed non-scoring / routing exclusions | 81 | Newly blocked from general Fact scoring |
| **Total** | **1,656** | |

The package-wide candidate labels are 216 `SUPPORTED`, 1,334
`SUPPORTED_WITH_SCOPE`, 25 `UNVERIFIED`, and 81 `EXCLUDE_NONSCORING`.
These are proposals, not 1,550 newly verified or approved runtime facts.
The new operational exclusion overlay is source-hash pinned and contains 103
keys: 17 source-review pending, 5 formula/safety-review pending, 76
non-scoring metadata, and 5 non-Fact routing metadata. It is disjoint from
the pre-existing 436 blocked keys. Current Topic Pack total: 2,092;
currently blocked: **539**; not blocked: **1,553**. “Not blocked” does not
mean independently reverified or actually required by every question.

## Three unresolved legacy-contract conflicts

The package proposes `UNVERIFIED` for three existing canonical requirements:

- `sil_target_determination_risk_reduction_and_lifecycle / required_rrf_relation`
- `sil_target_determination_risk_reduction_and_lifecycle / target_pfd_relation`
- `nyquist_stability_criterion_gain_phase_margin / argument_principle_pnz_relation`

Immediate runtime blocking broke protected SIL canonical-promotion and
Nyquist Golden regressions (two errors and one failure on the first full
Release Gate attempt). The proposed **revised sentences remain unapproved**
in private staging. Existing canonical statements and scoring behavior remain
unchanged until exact formula conventions, primary evidence and question
contracts are reconciled. This is not a claim that the three proposals passed
fact review, and the 25 proposed holds are **not** fully operationally resolved.

One existing test expected `system_sif_sil_context_boundary`—a repository
Topic-ownership sentence—to score in an explicit final-element question. The
new non-scoring policy excludes it, while the actual final-element technical
requirements remain. The test now explicitly guards against scoring that
internal routing sentence and retains the remaining technical requirements.

## Validation and remaining work

- Package checks: ZIP member hashes and packaged 1,656/199-key validator PASS;
  current-repository statement/hash join: 1,656/1,656 PASS.
- Focused regression: 25 passed.
- `python3 scripts/rubric_manager.py validate-all`: PASS.
- `PROMOTE_GENERATED=0 scripts/validate_release.sh`: first attempts exposed
  the conflicts above; final run PASS with `TOPIC_CONTENT_AUDIT=PASS`
  (89 Topics, 89 Masters, 763 questions, 2,092 Anchors). Optional dedicated
  10-run P0 reproducibility gate was not enabled.
- `python3 -m pytest -q`: **1,461 passed, 1 skipped, 1 warning**. The warning
  concerns a pre-existing test returning `False` instead of asserting.

Remaining: individually verify the 1,135 new proposed technical claims and
their question scope/duplicate score ownership before any promotion; resolve
the three canonical formula conflicts against primary evidence and protected
regressions; review whether routing-only Anchors should be removed from
`required_anchor_ids` in source Model Answers without changing valid grading
requirements. Do not claim 1,656/1,656 source verification from this staging
and gate run. No A–E authority, Fatal rule, Topic routing owner or generated
bank was changed.
