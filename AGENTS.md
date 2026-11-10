# Repository Instructions

## User-approved operational validation policy (2026-11-09)

The repository owner explicitly chose **pytest as the required code-validation boundary**. Accuracy Gate and `qualification.status=READY` are **not required for deployment**. Keep accuracy/stability experiments as opt-in diagnostics only; do not reintroduce paid 48×2 provider runs or new mandatory quality gates without the owner's explicit request. Run the complete offline pytest suite and report actual passed/failed/skipped counts. `calibration/pytest_quarantine.json` must contain only currently approved exact exclusions; do not automatically add failures. Preserve existing grading weights, Goldens, scoring authority and Fact Anchor rules. Protect private runtime data and its restore path before operational changes. Do not update or restart the live production bot as part of development validation.


## Topic Pack changes

The user delegated content approval to an AI reviewer on 2026-10-28 and on 2026-10-29 requested a lower-token-cost method instead of routine Astra approval. Use deterministic validation first, then a lower-cost reviewer (for example `gpt-6-luna`) for source-grounded technical review. Record the actual model with `approve-topic --reviewer <model_id> --review-method ai --review-report <report>`; never label AI review as human review or claim source verification from schema checks alone. Uncertain/unsupported claims stay pending. Keep source-hash, validation and promotion gates. The human-only instructions below describe the original default; this explicit delegation supersedes them for evidence-backed AI reviews.

Before creating or modifying a Topic Pack, read `docs/topic_pack_workflow.md` completely.

- Start every new Topic with `rubric_manager.py add-topic`; do not assemble an unmanaged scaffold manually.
- Keep the Topic in `draft / human_review_required` until a person reviews the README and source JSON.
- Record approval with `rubric_manager.py approve-topic --reviewer <reviewer_id>`.
- Do not bypass the approval/hash gate by editing generated banks directly.
- Run the full `validate-topic-pack-release --all` integration gate before commit or push.
- Treat `docs/topic_pack_workflow.md` as the human procedure and `scripts/topic_pack_workflow_controller.py` plus validators as the executable contract.

## Mandatory study loop (2026-11-07)

The user's standard exam-preparation workflow is:
1. ChatGPT asks **one** 25-point professional-engineer essay question based on a suitable, eligible existing Topic Pack. Do not reveal model answers, scoring keywords, or solution hints before the learner answers.
2. The learner writes the original answer independently; treat uploads, OCR, and raw session text as private user data.
3. The existing Telegram bot grades via `/grade` using the unchanged deterministic A/B/C and qualitative D/E policy. Preserve its original score/verdict, attempt, and question context.
4. **After grading**, ChatGPT authors a complete engineering model answer to that same question, grounded in validated Topic facts and clearly distinguished from unverified sources or model inference.
5. ChatGPT identifies missing technical requirements, factual misconceptions, causal/logic gaps, and engineering-judgment gaps; offer focused review material, self-check questions and `/review` navigation.

This is a **study workflow**, not an instruction to regrade or alter the scoring architecture. Keep question-specific demands distinct from all facts in a Topic Pack. Learning artifacts must carry a review state and `score_effect: none`. Never auto-promote assistant/Argon-written model answers to canonical scoring facts or silently rewrite raw learner answers and grades. A human review-status claim requires actual human review. Preserve private per-attempt data outside the public repository. See `docs/answer_review_loop_policy.md` for the owner-by-step contract and completion criteria.

## Strict guardrails

- Never edit runtime bank files in `rubrics/generated/` by hand. Generate or promote them only through `scripts/rubric_manager.py` (for example, `validate-topic-pack-release --all --promote-generated`), then check that committed output matches a fresh rebuild.
- After adding a rubric or changing grading code, run both `PROMOTE_GENERATED=0 scripts/validate_release.sh` and `python3 scripts/rubric_manager.py validate-all`. Run the applicable pytest suite as well and report its actual passed/failed/skipped counts. The previously reported **747 passed** is a historical snapshot, not a permanent test-count target; do not weaken or omit tests to match it.
- Do not put personal answers, session or review history, credentials (including `.env`), or real production databases into a public commit. Keep private WordPress source/OCR data outside the public repository too.
- Preserve A/B/C/D/E scoring, deterministic primary authority, canonical Question Type and topic routing, fatal handling, Golden tests, and release gates unless the task explicitly authorizes changing those contracts and the corresponding regressions are updated.

## Universal Fact Anchor scoring admission and exclusion (2026-11-01)

**Mandatory for every new and revised Topic Pack and Fact Anchor.** Read and
apply `docs/fact_anchor_eligibility_policy.md` before authoring or approving
engineering facts. Only verified, broadly industrially applicable engineering
principles, physical laws and properly bounded official standards can serve
as core scoring references. Exclude niche/vendor-specific detail, narrowly
jurisdictional or edition-scoped rules, duplicate scoring demands and
unresolved overgeneralizations from general scoring references. Preserve
source history; exclusions do not certify technical falsehood. Unverified
items remain pending and must not be auto-approved because a prior registry
label says `verified`. Enforce the current excluded ID overlay in every
question/answer scoring path, not merely in a written report. Do not promote
source or generated views, or claim test success, without the existing
validation and release gates.
