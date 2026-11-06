# Chapters 22/31/32: Fact admission and private-source synchronization

This addendum supersedes the *pending* runtime status in `wordpress_chapters_22_31_32_release_20261106.md`; it does not alter the immutable managed-Pack review report. The private WordPress database and extracted text bundles remain Git-ignored and must not be committed.

## Four Fact admissions

| Fact | Independent evidence | Scope condition |
| --- | --- | --- |
| `flow_inventory_change_net_balance` | Kuphaldt, Change-of-quantity Flow Measurement, multiple paths/net-flow discussion | Accounted inventory mass balance; multiple paths do not identify individual streams. |
| `relation_control_offset_setpoint` | Kuphaldt, Relation Control | Addition/subtraction of a compatible-unit offset, not ratio multiplication. |
| `feedforward_dynamic_compensation_timing` | Kuphaldt, Feedforward with Dynamic Compensation | Path delay/lag and causal realizability; no universal exact cancellation. |
| `limit_control_bound_signal` | Kuphaldt, Limit, Selector, and Override Controls | Identify the bounded signal; a selector can implement the same bound, but other selection purposes are not automatically equivalent. |

Each has an explicit textbook locator and `score_effect: none` in the approved Fact Registry. The original source anchors remain question-scoped; this Registry admission does not change the A–E scoring contract or give the Registry independent point-setting authority. The historical inventory addendum retains its original candidate rows, while the partition test subtracts the four now-promoted pairs from the live pending set.

## Private WordPress source

The local staging catalog was synchronized from the WordPress category on 2026-11-06: 317 posts. Post IDs 9774, 9782, 9789, 9814 and 9839 were matched to Master source references using their exact content SHA-256 versions. Six reviewed post-to-Topic links cover five Topics (post 9839 links to two). Five private bundles were built from the approved links; linked HTML text for all five posts was loaded in the Training projection. The private database and these five bundles were separately backed up off-repository; SQLite integrity check passed. PDF/image OCR was **not** performed in this synchronization, and empty extracted attachment text was not promoted as Fact evidence.

The previously stored WordPress database and bundles in the separate operating checkout were not overwritten. Deployment requires a reviewed private-data synchronization and an operating checkout update; a successful repository test alone does not establish that the running Telegram container uses the new data.

## Repository validation

- Full pytest: 1,463 passed, 1 skipped; one pre-existing `PytestReturnNotNoneWarning` in the private-view test.
- Focused Registry/WordPress tests after the final test addition: 394 passed.
- `python3 scripts/rubric_manager.py validate-all`: PASS.
- `python3 scripts/rubric_manager.py validate-topic-pack-release --all`: PASS.
- `PROMOTE_GENERATED=0 scripts/validate_release.sh`: PASS; opt-in ten-run reproducibility gate skipped by policy.
- Generated freshness and `git diff --check`: PASS.
