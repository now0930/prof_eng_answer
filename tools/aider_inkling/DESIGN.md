# V6 design

[Issue #51](https://github.com/now0930/prof_eng_answer/issues/51) records the four design principles.

1. Save Copilot's development plan as JSON.
2. Keep the Command Compiler independent of the AI model.
3. Separate code modification from quality validation.
4. Preserve each stage's inputs, outputs, and execution records locally. Keep private answers, credentials, and detailed logs out of GitHub and external model inputs.

The V6 workflow validates the plan, compiles exact edits, runs Aider with local Inkling for each ordered task, and checks its output against the approved edits. Verification includes change-scope checks, deterministic regrading before and after edits, optional scope diagnostics, and a final six-worker regression run. The grading and validation paths are preserved in RC1.

## Module boundaries

`develop.py` orchestrates `planner.py`, `compiler.py`, `executor.py` and
`validator.py` in that order, with interactive approval before execution.
`run_context.py` holds per-run paths, Git snapshots, backups, and subprocess
logging. The compiler uses the same exact-edit contract in `edit_contract.py`.
The validator owns repository scope, exact-output, scoring and regression checks.

The supported workflow uses an external planner and local Inkling editing.
The earlier local-model comparison code remains available as separate tooling.
Copilot and saved plans work through the existing contracts. Dedicated OpenAI
and Gemini adapters can be added to the planner without changing the compiler,
executor, or validator.
