# V6 design

[Issue #51](https://github.com/now0930/prof_eng_answer/issues/51) records the four design principles.

1. Save Copilot's development plan as JSON.
2. Keep the Command Compiler independent of the AI model.
3. Separate code modification from quality validation.
4. Preserve each stage's inputs, outputs, and execution records locally. Keep private answers, credentials, and detailed logs out of GitHub and external model inputs.

The integrated `develop.py` validates the plan, compiles exact edits, runs Aider with local Inkling for each ordered task, and checks its output against the approved edits. Verification includes change-scope checks, deterministic regrading before and after edits, optional scope diagnostics, and a final six-worker regression run. The grading and validation paths are preserved in RC1. Compiler and validation remain integrated in the controller.

## Provider adapters

The planner and editor now have separate command adapters in `ai_backends.py`. The
planner produces the same V6 JSON contract whether plans come from Copilot,
another configured command, or an approved file. Editors receive the compiler's
exact task prompt and one allowed target. The integrated controller owns plan
validation, scope and exact-output checks, regrading, and pytest.

The built-in Ollama editor sends only the approved change blocks to the
selected local model. It applies returned blocks through the shared exact-edit
contract in `edit_contract.py` and checks the hash before replacing the file.
Compiler and validator orchestration stay in the controller.
