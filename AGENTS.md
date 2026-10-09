# Repository Instructions

## Topic Pack changes

Before creating or modifying a Topic Pack, read `docs/topic_pack_workflow.md` completely.

- Start every new Topic with `rubric_manager.py add-topic`; do not assemble an unmanaged scaffold manually.
- Keep the Topic in `draft / human_review_required` until a person reviews the README and source JSON.
- Record approval with `rubric_manager.py approve-topic --reviewer <reviewer_id>`.
- Do not bypass the approval/hash gate by editing generated banks directly.
- Run the full `validate-topic-pack-release --all` integration gate before commit or push.
- Treat `docs/topic_pack_workflow.md` as the human procedure and `scripts/topic_pack_workflow_controller.py` plus validators as the executable contract.

## Strict guardrails

- Never edit runtime bank files in `rubrics/generated/` by hand. Generate or promote them only through `scripts/rubric_manager.py` (for example, `validate-topic-pack-release --all --promote-generated`), then check that committed output matches a fresh rebuild.
- After adding a rubric or changing grading code, run both `PROMOTE_GENERATED=0 scripts/validate_release.sh` and `python3 scripts/rubric_manager.py validate-all`. Run the applicable pytest suite as well and report its actual passed/failed/skipped counts. The previously reported **747 passed** is a historical snapshot, not a permanent test-count target; do not weaken or omit tests to match it.
- Do not put personal answers, session or review history, credentials (including `.env`), or real production databases into a public commit. Keep private WordPress source/OCR data outside the public repository too.
- Preserve A/B/C/D/E scoring, deterministic primary authority, canonical Question Type and topic routing, fatal handling, Golden tests, and release gates unless the task explicitly authorizes changing those contracts and the corresponding regressions are updated.
