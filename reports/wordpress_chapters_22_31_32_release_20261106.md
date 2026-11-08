# WordPress Chapters 22/31/32 Topic Pack integration — validation record

Date: 2026-11-06. Branch: `codex/essay-boundary-calibration-20261028`.

Five WordPress posts (IDs 9774, 9782, 9789, 9814, 9839) were reconciled with five current Master Topic Packs and the pre-existing Chapter 22 open-channel Pack. Four question-scoped Fact Anchors were added to two Topic Packs; the Chapter 32.1/32.2–32.6 posts supplied source references and bounded explanations without duplicate or edition-specific scoring Facts. The four new Anchors were recorded in the inventory addendum as **Registry admission pending**; their source-grounded Topic Pack review is recorded in `wordpress_chapters_22_31_32_topic_pack_review_20261106.md`. Source references remain unverified until the private source database is synchronized, and no source hash from the earlier Chapter 22-1 snapshot was silently replaced.

The managed Flow Pack was reapproved by delegated AI review (`gpt-6-luna` configured reviewer; agent-visible label `GPT-6 / Codex`) after source and quality checks. Its source hash and immutable review-report hash are captured in `topic_status.json`. A preapproval workflow defect was fixed: source checks now run before the refreshed approval hash, while full generated/release validation still runs after approval. The corresponding controller regression was updated and a reapproval test added.

## Final checks

| Check | Result |
| --- | --- |
| `python3 -m pytest -q` | PASS: 1,463 passed, 1 skipped, 1 pre-existing `PytestReturnNotNoneWarning` in the private Master-view test. |
| `PROMOTE_GENERATED=0 scripts/validate_release.sh` | PASS (exit 0). Dedicated 10-run reproducibility gate remains opt-in and was skipped by the release script. |
| `python3 scripts/rubric_manager.py validate-topic-pack-release --all` | PASS: 89 Topic Packs, 2,096 source Anchors. |
| `python3 scripts/rubric_manager.py validate-all` | PASS. |
| `python3 scripts/test_generated_rubrics_freshness.py` | PASS, 2 tests. |
| `git diff --check` | PASS. |

The two initial full-suite failures were the previous eight-pattern test and the 2,092-Anchor audit inventory. These were reconciled to 11 explicit patterns and 2,096 source Anchors without relaxing fact-boundary checks; the final full suite passed. The initial managed-Pack approval attempt also failed because it ran generated validation against a stale approval hash; the source-first preapproval fix and new regression cover this case.

This is a repository/source integration record, not a claim that the user's private WordPress/OCR database was rebuilt or that a running Telegram container was redeployed.
