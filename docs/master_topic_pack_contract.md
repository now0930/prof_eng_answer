# Master Topic Pack Contract

Status: additive interface, schema version `master-topic-pack-v1`.

`schemas/master_topic_pack.schema.json` defines the Master envelope. Each record
points to the existing Topic Pack source files and declares three versioned
projection interfaces. It does not copy or reinterpret deterministic grading
rules. Grading projection authority remains the existing Topic Pack and runtime
routing. Training history is learner data and must be persisted separately.

The `sources` array preserves WordPress references and other source metadata.
An empty array is valid while references are being collected. A source
reference records both `wordpress_url` (the parent blog post) and `source_url`
(the exact PDF, image, HTML, or Overleaf asset); legacy records may omit
`source_url`, in which case it is treated as `wordpress_url`. A WordPress
change creates a proposal and requires explicit user approval before the
Master record changes.

An approved source-reference update records provenance; it does not import
extracted WordPress/PDF text into grading, training, or diagnosis content. A
content change that would alter a fact, fatal misconception, question pattern,
or other View input requires a separate reviewed content proposal. Source
references remain `unverified` until the referenced material and page/section
are checked.

Source-reference proposal approval uses a SQLite write transaction and an
atomic Master-file replacement. If a database operation fails before commit,
the catalog transaction is rolled back and the previous Master bytes are
restored. If commit acknowledgement is ambiguous, the code checks the durable
proposal status and retains the matching Master state; if it cannot determine
the outcome, it stops with an explicit manual-reconciliation error rather than
silently retrying.
`--preview-proposal ID` validates a pending source-reference proposal against
the current Master and shows the prior and proposed references plus candidate
revision without changing catalog state or canonical files.
`--preview-pending-proposals` runs the same check across the pending queue and
reports each item as valid or invalid without applying any proposal.

`schemas/content_update_proposal.schema.json` and
`study/content_update.py` define that proposal-only contract. A proposal pins
the base Master revision, identifies one source-file record and field path,
records before/proposed text, and carries a linked source ID/URL/version/hash,
locator, and excerpt. `affected_views` is derived from the Master projection
configuration so reviewers can see the blast radius. Creation and validation
do not edit Topic files or Master records. Approval/rejection transitions
require an identity and timestamp. The pure candidate transformation checks
the Master revision, linked evidence, unique target record, and exact
`before_value`, then returns proposed source payloads and an incremented Master
revision in memory. Canonical application is a separate, explicit operation
requiring an apply identity. It revalidates catalog state, candidate manifest
and hashes, regenerated diff, current Master revision, and target before-value.
It replaces only the targeted legacy Topic source and Master record, records
`applied_by` / `applied_at`, and attempts to restore the original files if a
write fails. Applying a real proposal still requires the user's specific
approval; the normal regression suite must pass before and afterward because
the apply command does not itself run release gates.
The catalog packages that result as a review bundle under
`data/content_update_candidates/<proposal_id>/`, including candidate Master,
Topic source payloads, proposal, and a hash manifest. This copies files only to
the isolated bundle; original Topic files and Master remain unchanged until an
explicit `--apply-content-candidate ID --applied-by NAME` operation.
`--validate-content-candidate ID` runs the same integrity and revision
preflight without changing canonical files or proposal status, and reports the
files that a later explicit apply would replace, together with the before/after
value, reason, affected Views, and source evidence needed for human review.

The initial compatibility adapter may project existing packs without requiring
Master files for all existing topics. Representative Master records are added
incrementally; legacy packs are not mass-migrated in this stage.

## Projection ownership

- `grading-projection-v1`: read-only pointers to existing grading source files.
- `training-projection-v1`: learner-facing topic content references and daily
  target, with the later queue contract targeting two questions per day.
- `diagnosis-projection-v1`: diagnostic dimensions over existing source
  references; it does not calculate or alter the grader's score.

## Consumer boundary

All projections are read-only. The grading projection is a compatibility view
over the existing Topic Pack; it is not a new grader or scoring authority. The
training projection may provide practice prompts and study content. The
diagnosis projection is consumed as feedback guidance alongside the finalized
grade and must have no score/verdict effect. Training history and review
selection are separate learner state and must not be written into a Topic Pack.

Relative paths must stay inside the repository. Master updates do not directly
edit generated banks or user history.

Training and Diagnosis Views expose deep-copied `source_references` from the
Master, including exact asset URL and verification status. The feedback adapter
preserves these references alongside guidance; the review-material consumer can
read the current references from Training View. References are navigation and
provenance, not additional fact anchors. Grading Projection remains unchanged.
Older feedback snapshots may omit this additive field.

The Training View may also expose `source_materials` from the private
`data/wordpress_topic_packs/<topic_id>.json` bundle, but only for WordPress
post/page IDs already linked in that Topic's Master `sources`. The adapter
preserves the extracted WXR-HTML text, extraction method, content SHA-256,
source URL, and verification status. It fails closed on mismatched topic/source
identity, URL, or content hash. This is unverified study/reference material,
not canonical fact content and not a Grading Projection input. Raw source text
is not embedded in grading results or saved diagnosis snapshots; diagnosis
continues to give navigation references and score-neutral guidance, while a
learner can open the corresponding Training View material for review.

For concise, reviewed study aids, a Master record may optionally reference
tracked files under `study/learning_materials/`. These packs are a separate
training/feedback layer: each item pins an already-linked WordPress source ID,
version, extracted-text hash, locator, and excerpt; it declares
`score_effect: none` and a review status. Training View exposes the full aid;
Diagnosis/Feedback View exposes only its title and source pointer as a review
recommendation. A source/hash mismatch prevents the aid from loading. Adding
one does not edit legacy Topic JSON, generated grading banks, or any scoring
projection. The first example is a Nyquist delay-margin worked problem marked
`llm_reviewed_human_pending` rather than as a human-verified fact.
