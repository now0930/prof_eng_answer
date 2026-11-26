# Repository Instructions

## Operations-first guardrails (2026-11-26)

The primary purpose is professional-engineer exam preparation, not perpetual grader development. Use the verified existing operating path; reproduce observed defects and fix only their confirmed causes. Keep one owner per change and at most three concurrent work items. No unsolicited full-inventory review, broad refactor, new schema/ontology/evaluator, or research expansion. #40 / Draft PR #49 is frozen at `733d55416442f1469c3d21f38d994e8cd9c059a7`; its research path is not admitted to scoring. Preserve D4 and the 119 HOLD exclusions. Do not reopen them without explicit owner approval.

### Preserve the current grading architecture

- Preserve deterministic A/B/C authority, bounded D/E proposals and program-owned final decisions, A3/B6/C8/D6/E2 (25 points), pass criteria, Fatal/WRONG/ceiling, approved Fact eligibility, exclusions, Question Type/routing and question-specific demand scope. Reuse the existing Topic Pack, Question Contract, Engineering Ontology and evaluator. Do not infer missing knowledge or relax conditions to improve scores.
- Preserve original answers, grades and review history; an authorized regrade is a separate record. The current 89 Topics / 2,096 Anchors are a reference inventory, not a permanent count constraint. Evidence-grounded corrections and approved additions are allowed through the existing workflow.
- Change shared scoring architecture, approval rules or research admission only with separate explicit owner approval. A new Topic alone is not a reason to introduce another scoring path.

### New or revised Topic / Fact Anchor

Before authoring, read [Topic Pack Workflow](docs/topic_pack_workflow.md) and [Fact Anchor eligibility](docs/fact_anchor_eligibility_policy.md). Compare the candidate with the current full Topic inventory; document nearby owners, scope, duplicates, contradictions, question demands and routing aliases. Prefer existing Topic reuse or a bounded extension; create a managed Topic only for an independent subject. Shared principles may be referenced across Topics without duplicate score credit; use existing ownership/score-group contracts. Preserve essential assumptions, conditions, units and exceptions. Uncertain conflicts remain HOLD, not automatically approved.

Use existing add-topic, reviewer delegation, source-hash approval, validators and official generation. Before integration, demonstrate new-topic routing and scoped requirements, relevant old-topic routing and normal/wrong/partial/conditional answers, ambiguous/compound questions, no duplicate scoring, and unchanged unrelated protected behavior. Compare actual baseline/candidate results; legitimate intended changes must be explained, not hidden. Do not treat schema or keyword checks as proof of technical non-conflict. Do not re-review every existing fact to add one Topic; inspect the full inventory for candidates and focus detailed review on overlapping owners.

### Private data and deployment

Public GitHub may contain code, approved shared knowledge, synthetic tests and sanitized summaries only. Never publish private answers, OCR/images, sessions, grades, learning records, WordPress source/DB, provider requests/responses, keys or production configuration in commits, Issues, PRs or logs. Store private evidence and replay manifests outside public Git, keep existing live data paths until inventoried, and use isolated snapshots for development. Follow [Operation Runbook](docs/operation_runbook.md). Do not develop in the live checkout. Do not perform destructive Git/Docker operations, data deletion/migration, main merge, deployment or service restart without explicit owner approval and verified backup/restore where relevant.

Use the path guard and documented Git hooks as defense-in-depth; they do not establish absence of sensitive content. Review staged diffs and outgoing history before publishing. Keep manual Actions only; full offline pytest and existing Topic/release gates remain the required code validation, with no new paid qualification or ten-run gate. Record actual results and SHA, NOT_RUN where applicable. Commit/push within the specifically authorized isolated scope; never bypass the owner approval boundary for main or deployment.


### Existing validation protection

The manual `validate` job compares the candidate to current `origin/main` using `scripts/check_existing_grading_contract.py`. Ordinary changes must not rewrite protected grading-policy files, selected existing critical regressions or existing Golden expectations, delete existing regression scripts, or expand pytest quarantine. Additive tests and bounded grader fixes remain allowed. Other existing regression edits are explicitly reported for review; reviewers must inspect assertions and not weaken coverage. A protected change is HOLD: a separately owner-authorized, reviewed contract transition is required, not a candidate-provided bypass. Do not modify the checker, workflow or test collection to evade this rule. This path guard is not proof of unchanged semantics or owner identity; owner diff review and existing behavioral pytest remain essential. When Topic, Registry, ontology or generated/build paths change, the same job additionally invokes existing `validate-all`, generated freshness, and `validate-topic-pack-release --all` without promotion or live smoke. No new accuracy threshold, external model call, or automatic Actions trigger is introduced.

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
