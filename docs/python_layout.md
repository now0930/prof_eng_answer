# Python module layout

The only repository-root Python files are the Telegram entry point `bot.py`
and the public grading pipeline entry point `grading_agents.py`.
Implementation modules live in domain packages under `grading/`, and their
import paths are updated across runtime and tests. The deterministic grading
authority is unchanged. `scripts/test_python_layout_contract.py` guards this
boundary in the release gate.

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

Code imports these as `study.<module>`. The old root compatibility imports
were removed after their remaining callers migrated and the release gate passed.

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
- `grading/routing/`: Question Type, Question Demand, Topic selection, and
  semantic routing contracts. Repository data paths are resolved from the
  package location.
- `grading/evidence/`: extracted claims, facts, formulas, engineering
  invariants, logic checks, and verified defect evidence.
- `grading/scoring/`: deterministic requirement evaluation, score evidence,
  score engine, primary grade, score policy, output, calibration, and
  replay/shadow checks.
- `grading/rubrics/`: Topic Pack bank paths and registry access; both retain
  repository-root-relative path resolution.
- `grading/quality/`: expert accuracy benchmark, calibration dataset,
  Golden-risk audit, and accuracy release policy.
- `scripts/`: release gates, commands, audit tools, and historical regression
  scripts. One-off README and encoding utilities live in
  `scripts/maintenance/`. Existing script paths are part of the release
  contract.
- `tests/`: focused contracts, integration checks, and historical stage
  regressions previously kept at the repository root.
- `schemas/`: JSON contracts for the study layer and other data.
- `master_topic_packs/`: representative Master records.
- `rubrics/`: existing Topic Pack and grading data.

Further implementation moves should be made by domain. Compatibility imports
are needed only when callers still depend on an old import name. A move must
preserve `python3 bot.py`, script paths, test discovery, and the persisted
grading output.
