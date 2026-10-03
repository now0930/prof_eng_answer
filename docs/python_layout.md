# Python module layout

The Telegram entry point is `bot.py`. Existing grading modules at the repository
root retain their import names because release scripts, replay tools, and tests
use them directly. The grading authority remains in those modules.

## Study package

`study/` owns the additive Master Topic Pack and learning features:

| Module | Responsibility |
| --- | --- |
| `master_topic_pack.py` | Master schema checks and read-only projections |
| `source_update.py` | WordPress source references and approval proposals |
| `training_history.py` | SQLite attempt and review persistence |
| `review_queue.py` | Two-item queue contract and selector |
| `learning_workflow.py` | Contract-level grade-to-history bridge |
| `learning_runtime.py` | Bot-facing persistence and daily selection |

New code imports these as `study.<module>`. The six matching root files are
compatibility imports for existing callers. Keep those imports until their
callers have migrated and the full release gate passes without them.

The package may read a finalized grade and the existing Topic Pack sources.
It does not own scoring, routing, Question Type taxonomy, fatal checks, or
the deterministic primary authority.

## Existing operational layout

- `grading/coverage_feedback/`: post-grade coverage event, persistence,
  aggregation, report, and retention modules. These five modules moved from
  the repository root; runtime and script imports now use this package.
- `grading/providers/`: optional provider selection, per-chat settings, and
  deterministic request sampling contracts, plus the Gemini and CLOVA legacy
  provider implementations. These five modules moved from the repository root.
- `scripts/`: release gates, commands, audit tools, and historical regression
  scripts. Existing script paths are part of the release contract.
- `tests/`: focused contracts and integration checks.
- `schemas/`: JSON contracts for the study layer and other data.
- `master_topic_packs/`: representative Master records.
- `rubrics/`: existing Topic Pack and grading data.

Further root-module moves should be made by domain. Compatibility imports are
needed only when callers still depend on an old import name. A move must
preserve `python3 bot.py`, script paths, test discovery, and the persisted
grading output.
