# V6 design

[Issue #51](https://github.com/now0930/prof_eng_answer/issues/51) records the four design principles.

1. Save Copilot's development plan as JSON.
2. Keep the Command Compiler independent of the AI model.
3. Separate code modification from quality validation.
4. Preserve each stage's inputs, outputs, and execution records locally. Keep private answers, credentials, and detailed logs out of GitHub and external model inputs.

The integrated `develop.py` validates the plan, compiles exact edits, runs Aider with local Inkling for each ordered task, and checks its output against the approved edits. Verification includes change-scope checks, deterministic regrading before and after edits, optional scope diagnostics, and a final six-worker regression run. The grading and validation paths are preserved in RC1. Module extraction and further model integrations are deferred pending practical validation.
