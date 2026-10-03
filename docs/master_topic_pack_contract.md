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

The initial compatibility adapter may project existing packs without requiring
Master files for all existing topics. Representative Master records are added
incrementally; legacy packs are not mass-migrated in this stage.

## Projection ownership

- `grading-projection-v1`: read-only pointers to existing grading source files.
- `training-projection-v1`: learner-facing topic content references and daily
  target, with the later queue contract targeting two questions per day.
- `diagnosis-projection-v1`: diagnostic dimensions over existing source
  references; it does not calculate or alter the grader's score.

Relative paths must stay inside the repository. Master updates do not directly
edit generated banks or user history.
