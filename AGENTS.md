# Repository Instructions

For code-grounded documentation changes, consult [the AI/developer implementation map](docs/ai_implementation_reference.md) and keep [the human README](README.md) concise. This is navigation, not a replacement for the policies below.

## Documentation policy (human and AI, 2026-11-13)

Keep the [human README](README.md) and [document index](docs/README.md)
concise; place accurate implementation details in the
[AI code map](docs/ai_implementation_reference.md) and linked technical contracts.
Follow [document governance](docs/document_governance.md). Actively maintained
detailed guides start with a short human-oriented summary, then preserve exact
contract details for AI/developers. Do not present historical Gate results
as current requirements. Never reformat canonical Topic Pack READMEs, Topic
Sheets, source hashes, historical reports or private data just to simplify docs.
Code, actual configuration, source JSON and focused tests determine behavior;
document-only commits do not imply deployment.

## WordPress URL intake direction and anti-drift (2026-11-13)

For any task involving a supplied WordPress post URL or repeated WordPress
catalog ingestion, first read [human intake policy](docs/wordpress_url_continuous_workflow.md)
and [AI/Codex execution contract](docs/wordpress_url_continuous_ai_runbook.md),
then inspect current code and private state through authorized tools.
Do not treat a supplied single post URL as a supported `--category-url` argument.
Preserve the sequence: identify/version → first-party OCR → compare existing Topic
ownership → evidence-backed link review → separate Master source approval →
private learning source → independently verified Fact/content proposal.
Do not silently turn a link recommendation into approval or grading authority.
Prioritize existing Topics, exact locators, idempotency, privacy, review provenance
and rollback; scope unrelated enhancements as separate proposals.
Never claim URL-driven automatic intake, DB writes, release/deployment or
validation happened when only documentation or research was performed.
Do not add new scoring gates or bypass the explicit approval process.

## User-approved operational validation policy (2026-11-09)

The repository owner explicitly chose **pytest as the required code-validation boundary**. Accuracy Gate and `qualification.status=READY` are **not required for deployment**. Keep accuracy/stability experiments as opt-in diagnostics only; do not reintroduce paid 48×2 provider runs or new mandatory quality gates without the owner's explicit request. Run the complete offline pytest suite and report actual passed/failed/skipped counts. `calibration/pytest_quarantine.json` must contain only currently approved exact exclusions; do not automatically add failures. Preserve existing grading weights, Goldens, scoring authority and Fact Anchor rules. Protect private runtime data and its restore path before operational changes. Do not update or restart the live production bot as part of development validation.


## Topic Pack changes

The user delegated content approval to an AI reviewer on 2026-10-28 and on 2026-10-29 requested a lower-token-cost method instead of routine Astra approval. Use deterministic validation first, then a lower-cost reviewer (for example `gpt-6-luna`) for source-grounded technical review. Record the actual model with `approve-topic --reviewer <model_id> --review-method ai --review-report <report>`; never label AI review as human review or claim source verification from schema checks alone. Uncertain/unsupported claims stay pending. Keep source-hash, validation and promotion gates. The human-only instructions below describe the original default; this explicit delegation supersedes them for evidence-backed AI reviews.

Before creating or modifying a Topic Pack, read `docs/topic_pack_workflow.md` completely.

- Start every new Topic with `rubric_manager.py add-topic`; do not assemble an unmanaged scaffold manually.
- Keep a new Topic in `draft / human_review_required` until an authorized human or delegated source-grounded AI reviewer approves the README and source JSON. The legacy status label alone does not require a human reviewer.
- Record actual reviewer and review method with `rubric_manager.py approve-topic --reviewer <reviewer_id>`; for delegated AI use `--review-method ai --review-report <report>` and never label AI review as human.
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

## Canonical Topic Pack vs private learning/reasoning records (2026-11-11; owner clarification)

**Keep these two layers separate.** A Topic Pack is a clear, concise, nonredundant reference of validated engineering facts; the private learning DB explains *how the learner reaches those facts*. Do not expand canonical Fact Anchors to contain a learner's misconceptions, personal answer history, lengthy derivations, tentative ideas, or tutoring dialogue. Do not remove indispensable applicability conditions, assumptions, units, limitations or provenance merely to shorten a Fact.

- **Canonical layer (Topic Pack / Fact Anchor):** retain one technically accurate, source-grounded, broadly applicable claim per appropriate canonical owner, with only the assumptions and limits needed to state it correctly. Reuse existing Anchors before proposing a new one. Keep the existing eligibility, AI/human reviewer delegation, source-hash, approval, scoring-exclusion and release procedures unchanged.
- **Private layer (learner reasoning and corrections):** store evidence-linked misconceptions, omissions, ambiguous interpretations and the *reasoning/derivation path* from starting assumptions, equations and source passages to the correct engineering proposition. Link each record to learner, Topic, question, attempt or conversation, original evidence/span, correction and why it holds, operating conditions, source locator, self-check question, review state and subsequent verification. Preserve the original answer and finalized grade. Mark all learning records `score_effect: none`. Distinguish an observed error from a mere omission or an AI hypothesis; do not assert that the learner misunderstood something without evidence.
- **Fact-candidate boundary:** learning materials, private WordPress reviews and AI explanations can suggest a generic engineering claim. Before any canonical change, strip personal data, check for overlap/ownership, independently substantiate the exact bounded claim and use the **existing** review/promotion/validation workflow. Never automatically elevate a private correction, an attractive derivation, an LLM answer or a staging label to a scored Fact.
- **Behavioral compatibility:** the standard independent question → learner answer → `/grade` → model answer → review loop remains the default. An explicit user request for `/review` may continue to display an existing study answer even when no prior attempt exists; preserve that current behavior. Do not add a new mandatory Fact approval gate or change the present AI reviewer workflow solely because of this clarification.
- **Implementation status:** these are authoring and data-separation requirements, not a claim that the private misconception/derivation schema or its automation has already been implemented. Keep personal data and full source excerpts outside public Git and outside canonical scoring outputs.

See [the study loop policy](docs/answer_review_loop_policy.md) and
[Fact Anchor eligibility](docs/fact_anchor_eligibility_policy.md).

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

## Dedicated 10-run grading reproducibility check removal (2026-11-12)

The repository owner permanently removed the dedicated check that grades the
same input ten times. Do not restore its runner, environment switch, release or
CI path, PASS/SKIP reporting, required/optional validation instruction, or
recommendation for future work. New release reports must not require, request,
or reserve a result field for this removed check.

This policy does not remove single-run deterministic grading checks, grading
accuracy regressions, Golden tests, or the offline pytest suite. Preserve historical audit reports as records of what
was run at the time; do not require this check in new release reports.
