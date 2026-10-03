# Master Topic Pack Integration: Stage 1 Inventory

Status: `PASS`

Repository baseline: `1f541e7`

Scope: additive learning and diagnosis structures; existing grading authority remains unchanged.

## Existing source of truth

- Topic source files live in `rubrics/topic_packs/<topic_id>/`.
- Each legacy pack commonly contains `fact_anchor.json`, `logic_check.json`,
  `model_answer.json`, and `topic_importance.json`; some also contain
  `question_demand_axes.json` and status metadata.
- Generated grading inputs live under `rubrics/generated/` and are rebuilt and
  validated by the Topic Pack workflow. They must not be edited directly.
- `schemas/topic_pack_spec.schema.json` describes a compiled technical-content
  specification. It is not a versioned master record for source references,
  learning/diagnosis projections, or learner history.
- `schemas/topic_pack_profile.schema.json` describes compiler profiles and is
  not the learner-facing master contract.
- Grading runtime and deterministic checks resolve the existing Topic Pack and
  generated-bank artifacts through the current routing and registry paths.
- No shared Training History or Review Queue persistence contract is present
  at this baseline.

## Compatibility boundary

The new Master Topic Pack will be an additive, versioned envelope. An adapter
will read existing Topic Pack files without changing their schema or routing
authority, then expose read-only Grading, Training, and Diagnosis projections.
The existing deterministic grading paths remain authoritative. User attempt
history and queue state will be stored separately from Topic Pack source data.

## Implementation stages

1. Inventory and compatibility boundary — passed.
2. Master schema and contract.
3. Read-only projection interfaces.
4. Training and diagnosis interfaces.
5. Training history and review queue contracts.
6. WordPress source-reference contract.
7. Representative Topic integration.
8. Full regression and release validation.

Each stage is committed only after its focused checks pass. The final push is
reserved for completion of Stage 8.
