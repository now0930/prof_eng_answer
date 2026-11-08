# General-Fact Release validation — 2026-11-02

Branch: `codex/essay-boundary-calibration-20261028`. This report records the
tested workspace before branch publication; it does not claim `main` or a
running container was deployed.

| Check | Result |
|---|---|
| 1,290-row audit / operational hold reconciliation | PASS; 80 revision + 184 source/promotion + 276 general-scoring exclusions = 540 blocked |
| Independent deterministic score audit | PASS; 33/33 scored, 29/33 in reviewed range; 15 Pack-derived model references remain in diagnostic/fatal/routing replay |
| SW-06 LOW/PASS/HIGH boundary | PASS; 4.5 / 18.5 / 20.75 out of 25 |
| Topic Pack release integration | PASS; generated pipeline and quality |
| `rubric_manager.py validate-all` | PASS |
| Full `pytest -q` | 1,453 passed, 1 skipped, 1 existing return-value warning |
| Final `PROMOTE_GENERATED=0 scripts/validate_release.sh` | PASS, exit 0; opt-in 10-run reproducibility Gate skipped by design |
| Diff / privacy scan | `git diff --check` clean; no private session, database or `.env` file staged |

The historical full-pytest failures were fixed without admitting held Facts:
Displacer preflight now compares the question contract with its scoring-eligible
subset; source-only wet/dry calibration remains held. The anchor inventory now
records three later-added source Anchors and distinguishes two already-promoted
gyro Anchors from the older pending snapshot. Legacy tests expecting blocked
SIL/LOPA/MC/DC/valve positive credit were changed to assert the absence of
those scored requirements while retaining fatal and routing checks.

Content promotion of the 80 revision candidates and 184 source/promotion
candidates remains **pending**. The 276 general-scoring exclusions remain in
force. Passing this release validates the current fail-closed operating state,
not factual approval of those held claims.

Publication status: local branch commit `2d730ea` contains the validated
changes. `git push origin codex/essay-boundary-calibration-20261028` failed
because the local HTTPS credential helper could not supply a GitHub username;
`gh auth status` also reports an invalid token. A second push attempt with
network escalation returned the same authentication error. No force push,
remote branch update, PR merge, container rollout or CI verification occurred.
