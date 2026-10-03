# Additive Learning Layer

The learning layer builds on the existing Topic Pack registry. It does not
change the grader's A/B/C/D/E contract, deterministic checks, routing, fatal
handling, canonical Question Types, Golden cases, or release gates.

```text
existing Topic Pack
        │
        ▼
Master Topic Pack (versioned references and projection contracts)
        ├── grading projection ──► existing grader source files
        ├── training projection ─► prompts, outline, facts, practice targets
        └── diagnosis projection ► facts, deterministic checks, topic guidance
                                      │
answer ─► existing grade ─► diagnosis ─► SQLite training history
                                                  │
                                                  ▼
                                       daily two-item review queue
```

## Contracts and code

- Master records: `master_topic_packs/<topic_id>.json`
- Master schema: `schemas/master_topic_pack.schema.json`
- Projection adapters: `master_topic_pack.py`
- Training history: `training_history.py` and `schemas/training_history.schema.json`
- Queue selection contract: `review_queue.py` and `schemas/review_queue.schema.json`
- Graded result bridge: `learning_workflow.py`
- WordPress references and approval proposals: `source_update.py`

The history database path is supplied by the caller. Each attempt stores its
question and topic identity, attempt time, final score, structured diagnosis,
review status, last review time, and next review time. The queue contract
defaults to a weakness item and a retention item, each from a distinct Topic.
Selection candidates are supplied by the caller so ranking policy can evolve
independently from persistence.

WordPress synchronization is not implemented here. The Master preserves
WordPress URLs and source metadata. A source change produces a
`pending_approval` proposal; applying it requires an approver identity and a
matching Master revision.

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
