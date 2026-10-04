# Additive Learning Layer

The learning layer builds on the existing Topic Pack registry. It does not
change the grader's A/B/C/D/E contract, deterministic checks, routing, fatal
handling, canonical Question Types, Golden cases, or release gates.

```text
WordPress post / PDF / image / HTML
        │ sync, version, OCR/text extraction
        ▼
SQLite source catalog ── candidate post↔topic links ── human review
                                                        │
                                             source-reference proposal
                                                        │
                                                  user approval
                                                        ▼
Master Topic Pack (Topic identity, legacy references, approved sources)
        ├── Grading View ──► existing Topic Pack ──► deterministic/semantic grader
        ├── Training View ─► practice prompt, outline, facts, study targets
        └── Feedback View ─► final grade + diagnosis guidance ─► learner feedback
                                                                  │
                                                  SQLite training history
                                                                  ▲
Learner ── `/review <topic_id or title>` ──► selected Topic study material
```

The three Views are separate read-only projections over the current Topic Pack
content. The Master owns Topic identity, projection contracts, and approved
source references; it is not a second grading-rule database. The feedback
View is the learner-facing use of the `diagnosis` projection and must not
change the finalized score or verdict.

## Contracts and code

- Master records: `master_topic_packs/<topic_id>.json`
- Master schema: `schemas/master_topic_pack.schema.json`
- Projection adapters: `study/master_topic_pack.py`
- Training history: `study/training_history.py` and `schemas/training_history.schema.json`
- Optional queue selection contract: `study/review_queue.py` and `schemas/review_queue.schema.json`
- Graded result bridge: `study/learning_workflow.py`
- Production grade-history persistence: `study/learning_runtime.py`, called
  after `grade.json` is finalized by `bot.py`
- WordPress references and approval proposals: `study/source_update.py`
- Curated Topic-content change proposal contract:
  `study/content_update.py` and `schemas/content_update_proposal.schema.json`
- Curated content proposal persistence/review: the separate
  `content_update_proposals` table in the WordPress catalog database
- WordPress category ingestion, source catalog, media-version tracking, local
  PDF text extraction/OCR, and review commands: `scripts/wordpress_catalog.py`
- Local generated catalog: `data/wordpress_sources.sqlite3` (ignored runtime
  data; regenerate from the configured category URL)

## View consumers and ownership

| View | Contract and intended consumer | Current wiring |
| --- | --- | --- |
| Grading | `project_grading()` / `grading_compatibility_payload()` exposes the existing grading source files without editing or translating them. The existing Topic Pack and routing remain authoritative. | Projection is currently exercised by contract/integration tests, not called from the production grading path. This is intentional until compatibility is proven at the real adapter boundary. |
| Training | `project_training()` provides question patterns, examples, outline, fact anchors, high-score points, study targets, hash-pinned WordPress HTML, and optional curated worked examples. Curated aids carry source evidence and an explicit review status; none of these inputs are canonical grading facts. | `/review <topic_id or title>` resolves a user-selected Topic without consulting the date, then displays its question, outline, facts, and source-based aids. |
| Feedback | `project_diagnosis()` provides anchors, fatal misconceptions, deterministic checks, guidance with `score_effect: none`, and pointers to matching curated study aids. | Finalized attempts retain the existing grade-derived diagnosis and an additive `topic_guidance` payload. User-selected review presents saved prior weaknesses and Topic guidance separately; none feed back into scoring. |

The production sequence is: finalize grade exactly as today; build the Training
and Feedback Views as read-only payloads; persist the final score and structured
feedback; let the learner select a Topic for review. The optional queue contract
is not the Telegram review selector. The Grading View must not become a second
scoring implementation. Any future grader adapter switch requires a separate
parity and regression stage.

### Next adapter stage: bounded implementation and regression gates

The first production adapter stage should be limited to the learning runtime;
it must not touch `bot.py`'s grading or score-finalization path.

1. Change `_master_question()` to obtain the question pattern/examples through
   the Training View. Preserve today's question-selection precedence and output
   exactly; if the view lacks a usable prompt, retain the current legacy-source
   fallback. This avoids changing the review queue while making the consumer
   boundary explicit. If the Training View needs an additive `question_examples`
   field to preserve precedence, version or test that projection contract first.
2. Add a feedback adapter that accepts the finalized grade and the
   topic's Diagnosis View and returns a separate learner-feedback payload.
   Keep `diagnosis_from_grade()` as the persisted-grade compatibility baseline;
   attach projection guidance separately rather than allowing it to overwrite
   grade-derived findings. The adapter may explain findings and suggest study
   actions, but cannot calculate scores, change verdicts, or promote a
   projection signal into a fatal finding on its own.
3. In `record_completed_grade()`, call these adapters only after the grade is
   final. Persist the same score/verdict and existing diagnosis fields; any new
   feedback fields are additive. If a Master/View is unavailable or malformed,
   preserve the existing history behavior and do not block delivery of the
   finalized grade.

Required regression gates for that implementation stage:

- Training adapter parity: for representative Master Topics, selected
  question ID/text remain identical to the pre-adapter legacy behavior; test
  empty examples/patterns and fallback behavior.
- Feedback isolation: snapshot the grade before/after adapter use and assert
  `final_total_score`, `total_score`, `verdict`, `score_status`, and all existing
  grade fields are unchanged; assert `score_effect == "none"` on guidance.
- Persistence compatibility: existing history fields and SQLite schema remain
  readable; feedback additions are optional and old rows still load.
- Integration failure isolation: missing/invalid View data cannot prevent the
  finalized grade response or corrupt an already-saved grade.
- Run Master schema/projection/training-diagnosis/history/queue/integration
  tests, the bot learning-history integration test, and the existing Grader
  deterministic, fatal, canonical-routing, Golden, and release-gate suites.
  No existing gate may be edited or weakened to accommodate the adapters.

This is a scope and gate definition, not a grader integration approval: the
grading projection remains test-only, and no adapter may replace the existing
Topic Pack or deterministic primary authority in this stage.

## WordPress change-proposal lifecycle

1. Sync WordPress posts and first-party media into the source catalog. Record
   parent post URL, exact asset URL, source ID, version/hash, timestamps, and
   extracted text. PDF binaries remain outside the catalog; OCR text is stored
   locally.
2. Generate candidate post-to-Topic links from title, excerpt, and tags. Scores
   are ranking hints only. A person approves or rejects each mapping.
3. For each approved Topic/source pair, queue a source-reference proposal. If
   the Topic has no Master yet, keep it as `waiting_for_master`; otherwise use
   `pending_approval` with the current Master revision as its base.
4. `--preview-proposal ID` checks one pending proposal against the current
   Master; `--preview-pending-proposals` checks the queue. Both display old/new
   references without writes. On explicit
   approval, append or replace the source reference and increment
   the Master revision. The catalog approval and atomic Master replacement are
   protected with rollback and ambiguous-commit reconciliation. Other pending
   proposals are rebased, but still need individual approval. An applied
   reference remains `unverified` until its contents and location are checked.
5. When the source changes, record old/new version or hash in
   `source_change_events` and create proposals for Topics with approved links.
   An event with no approved Topic association remains `pending_topic_review`.

Only after the source-reference proposal is approved and its new `updated_at`
is present in Master can the Topic qualify for `recently_changed_topic` review.
An unapproved catalog event/proposal does not change a learner's queue or
Training/Feedback View.
The catalog-to-Master approval boundary and the resulting review-candidate
signal are covered by `scripts/test_wordpress_review_integration.py`.

For human mapping review, `--export-topic-link-review PATH` creates a
repository-local, non-overwriting CSV snapshot of approved links, pending
candidate links, and unmatched posts. Rows include post title/URL/excerpt/tags,
candidate Topic and lexical evidence, plus linked asset metadata. The export
does not update the catalog; each mapping is still applied individually with
`--review-topic-link POST_ID TOPIC_ID approve|reject` after review.
The LLM-assisted, recommendation-only review procedure is documented in
`docs/wordpress_topic_link_llm_review_guide.md`; it explicitly prohibits
automatic approval or Master/Topic edits.

This lifecycle currently updates **source references**, not canonical facts or
grading rules. The Training View can expose the exact extracted text for an
already-linked private WordPress source bundle, with a content hash and
`unverified` status, as review material. It does not summarize, normalize, or
promote that text into a grading/diagnosis fact. A material WordPress content
change must not silently alter curated Topic content: a later content-curation
proposal should identify the affected Fact/section, show the source diff and
evidence, and require approval before canonical Topic content changes. This
separates source-based study access from knowledge-content changes. Curated
worked examples belong in `study/learning_materials/`, linked from Master, with
evidence hash and locator, score-neutral fields, and an explicit review state;
they are not written into `rubrics/topic_packs/` or generated banks.

The proposal-only content contract is separate from source-reference updates.
It pins the Master revision, target source key/record/field, before and proposed
text, source ID/URL/version/hash, locator and supporting excerpt, and derives
the impacted Views. Explicit approval/rejection is recorded with identity and
time. An approved change can be transformed into an in-memory candidate only
when its base revision, linked evidence, target uniqueness, and before-value
still match. `--prepare-content-candidate ID` writes the result to an isolated
repository-local candidate bundle with a hash manifest. It does not overwrite
Master or canonical Topic files. Canonical application uses
`--apply-content-candidate ID --applied-by NAME`; it requires a `candidate_ready`
catalog record and rechecks the candidate bundle, current revision, and target
before-value, then records the apply identity/time. `--validate-content-candidate ID`
runs this preflight without changing canonical files or proposal status, and
prints the target, before/after values, rationale, affected Views, source
evidence, and files a later apply would replace. Apply attempts rollback if a file
replacement fails. Neither command runs regression/release gates:
run those before and after applying a real proposal, and do not apply a content
proposal without its specific user approval.

Pending proposals can be persisted and reviewed independently from source
reference proposals. `--list-content-proposals` lists them;
`--approve-content-proposal ID --reviewed-by NAME` records approval only, and
`--reject-content-proposal ID --reviewed-by NAME` records rejection. Approval
checks the current Master revision and linked source identity/URL. It does not
write canonical Topic files or alter a live View. Candidate bundles can be
created only for approved proposals and are marked `candidate_ready` in the
catalog after generation.

The history database path is supplied by the caller. Each attempt stores its
question and topic identity, attempt time, final score, structured diagnosis,
review status, last review time, and next review time. The queue contract
defaults to a weakness item and a retention item, each from a distinct Topic.
Selection candidates are supplied by the caller so ranking policy can evolve
independently from persistence.

Telegram review is user-selected and not date-driven. Use
`/review <topic_id or title>` to request any Master Topic; exact Topic IDs and
titles are preferred, a unique partial match is accepted, and ambiguous
matches are listed for the learner to disambiguate. `/review done <topic_id>`
records completion for any valid Master Topic, whether or not the Topic was in
an optional queue. Repeating `/review` for a Topic does not consume or rotate a
daily queue.

The `review_queue` schema and selector remain available as an optional
contract for later use, but the Telegram `/review` command does not create or
read daily queue snapshots. Grading persists only the attempt and its
score-neutral diagnosis; it does not create a date-bound queue as a side effect.

A new Topic can be marked reviewed before the learner has submitted a graded
answer. Its review timestamps are stored separately from scored attempts, so
reviewing it does not invent a score or diagnosis. `next_review_at` remains
historical scheduling metadata and does not control manual Topic selection.

The Telegram adapter uses `chat_id` as the learner scope. Every successful
grade with a routed Topic is recorded after `grade.json` has been written. A
history write failure is logged and does not change or block the grade.
`/review <topic_id or title>` displays exactly the selected Topic's Training
View and prior score-neutral guidance; `/review done <topic_id>` records a
manual review and its timestamps. No date-based candidate ranking is used by
the Telegram command.

Catalog synchronization and source-change detection are implemented, while
automatic writes into Master records are disabled. A change tied to an
approved Topic mapping creates a `pending_approval` source-reference proposal;
applying it requires an approver identity and a matching Master revision.

The first catalog pass covers the Industrial Instrumentation/Control Engineer
category configured in `scripts/wordpress_catalog.py`. It indexes every
category post and its PDF, image, HTML, and Overleaf links. Candidate topic
links are generated from title, excerpt, and tags and remain `pending_review`;
their lexical scores are ranking aids, not calibrated probabilities. They are
not copied into any Master automatically. Approving a candidate link
queues a separate source update proposal. Applying that proposal requires an
explicit approver identity. Posts with no existing Master record remain queued
as `waiting_for_master`.

The catalog stores source URLs, WordPress media identifiers and modification
times, post text, content hashes, and extracted PDF text; it does not store
media binaries. Here, first-party means `now0930.pe.kr` or one of its
subdomains. Only those PDFs are download/OCR candidates. For first-party PDFs,
digitally embedded text is extracted
page by page. Pages without usable embedded text are rendered locally and
recognized with Tesseract using Korean and English language data. External
PDF links are retained as metadata and are not downloaded or OCRed. Run
`python3 scripts/wordpress_catalog.py --ocr` to synchronize and process pending
first-party PDFs. On Debian/Ubuntu, install `tesseract-ocr`,
`tesseract-ocr-kor`, `tesseract-ocr-eng`, and `poppler-utils` first. Use
`--list-pending`, `--review-topic-link POST_ID TOPIC_ID approve|reject`, and
`--approve-proposal ID --approved-by NAME` to manage the review and approval
flow. A manually selected Topic ID can be approved for an unmatched post with
the same `--review-topic-link` command.

In a Master source reference, `wordpress_url` identifies the parent blog post
and `source_url` identifies the exact PDF/image/HTML/Overleaf asset. The
catalog database keeps both ends of this relationship, along with `source_id`
and the WordPress media version.

## Validation

Validate the representative Master records and their legacy source references:

```bash
python3 scripts/validate_master_topic_packs.py
```

Run the additive structure and integration checks with the corresponding
`tests/test_master_topic_pack_*.py`,
`tests/test_training_diagnosis_projections.py`,
`tests/test_training_history_and_review_queue.py`, and
`tests/test_wordpress_source_contract.py` scripts. Existing release validation
continues to run through `scripts/validate_release.sh` without changing its
grading policies.
