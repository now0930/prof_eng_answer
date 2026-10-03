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
                                                                  │
                                                                  ▼
                                                       daily 2-item queue
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
- Queue selection contract: `study/review_queue.py` and `schemas/review_queue.schema.json`
- Graded result bridge: `study/learning_workflow.py`
- Production persistence and queue integration: `study/learning_runtime.py`, called
  after `grade.json` is finalized by `bot.py`
- WordPress references and approval proposals: `study/source_update.py`
- WordPress category ingestion, source catalog, media-version tracking, local
  PDF text extraction/OCR, and review commands: `scripts/wordpress_catalog.py`
- Local generated catalog: `data/wordpress_sources.sqlite3` (ignored runtime
  data; regenerate from the configured category URL)

## View consumers and ownership

| View | Contract and intended consumer | Current wiring |
| --- | --- | --- |
| Grading | `project_grading()` / `grading_compatibility_payload()` exposes the existing grading source files without editing or translating them. The existing Topic Pack and routing remain authoritative. | Projection is currently exercised by contract/integration tests, not called from the production grading path. This is intentional until compatibility is proven at the real adapter boundary. |
| Training | `project_training()` provides question patterns, outline, fact anchors, high-score points, and study targets. A trainer or `/review` presentation layer may consume it; it must not write grade fields. | `/review` builds its queue from Master metadata, but its question text is currently read directly from legacy `model_answer` in `learning_runtime._master_question()`. It does not yet consume `project_training()`. |
| Feedback | `project_diagnosis()` provides anchors, fatal misconceptions, deterministic checks, and guidance with `score_effect: none`. Combine it with the already-finalized grade to explain misses and next actions. | Production history currently stores a compact diagnosis extracted from the final grade via `diagnosis_from_grade()`. It does not yet combine the diagnosis projection with that result. |

The intended production sequence is: finalize grade exactly as today; build the
Training and Feedback Views as read-only payloads; persist the final score and
structured feedback; select the next queue from history. The Grading View must
not become a second scoring implementation. Any future grader adapter switch
requires a separate parity and regression stage.

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
4. On explicit approval, append or replace the source reference and increment
   the Master revision. Other pending proposals are rebased, but still need
   individual approval. An applied reference remains `unverified` until its
   contents and location are checked.
5. When the source changes, record old/new version or hash in
   `source_change_events` and create proposals for Topics with approved links.
   An event with no approved Topic association remains `pending_topic_review`.

This lifecycle currently updates **source references**, not the actual facts,
grading rules, or learning content. A material WordPress content change must
not silently enter any View: a later content-curation proposal should identify
the affected Fact/section, show the source diff and evidence, and require
approval before curated Topic content changes. This separates provenance
maintenance from knowledge-content changes.

The history database path is supplied by the caller. Each attempt stores its
question and topic identity, attempt time, final score, structured diagnosis,
review status, last review time, and next review time. The queue contract
defaults to a weakness item and a retention item, each from a distinct Topic.
Selection candidates are supplied by the caller so ranking policy can evolve
independently from persistence.

The first `/review` request for a learner on a local calendar day persists a
daily queue snapshot in SQLite. Subsequent requests that day return the same
maximum-two items rather than replenishing the queue. `/review done` only
accepts a pending item in that day's queue and marks it completed; the next
day gets a newly selected queue. This keeps the daily target bounded even if
the learner reopens the command repeatedly.

A new Topic can be marked reviewed before the learner has submitted a graded
answer. Its next due date is stored separately from scored attempts, so
reviewing it does not invent a score or diagnosis. Once due, it returns as a
long-unreviewed Topic. A source change is treated as new only when it happened
after the latest attempt or completed review.

The Telegram adapter uses `chat_id` as the learner scope. Every successful
grade with a routed Topic is recorded after `grade.json` has been written. A
history write failure is logged and does not change or block the grade. `/review`
shows up to two Topics; `/review done <topic_id>` records completion and sets
the next review to 30 days later as a starter interval. A weak score is below
15/25, a source update newer than the latest attempt is a recently changed
candidate, and unseen Master Topics are new-topic candidates. These starter
selection rules are isolated in `study/learning_runtime.py` for future replacement.

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
media binaries. For first-party PDFs, digitally embedded text is extracted
page by page. Pages without usable embedded text are rendered locally and
recognized with Tesseract using Korean and English language data. External
PDF links are retained as metadata and are not downloaded. Run
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
