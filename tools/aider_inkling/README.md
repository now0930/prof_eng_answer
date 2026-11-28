# Aider–Inkling V6.0 RC1

Install the files from this directory into `~/aider_inkling` on Linux. The integrated controller expects a separate grading checkout at `~/aider_inkling/repo`. Use a disposable grading checkout when running automation that edits files. The validator uses the existing Python environment at `~/hermes/validation/.venv-xdist/bin/python` with the grading dependencies, pytest, and pytest-xdist.

For an end-to-end run, provide an authorized local baseline answer at `~/aider_inkling/test_answers/feedback_control.txt`. Plans with scope checks also require a local `test_answers/compiler_case.json` and its referenced inputs. Install Docker Compose and make the local Ollama model `inkling-2-mini-aider` available on port 11434. Start the proxy in a separate terminal with `python3 inkling_proxy.py`. The controller directs batch Aider requests to port 11435.

From `~/aider_inkling`, compile an existing V6 JSON plan or run it using the following commands.

```sh
./develop.sh --plan /path/to/approved-plan.json --compile-only
./develop.sh --plan /path/to/approved-plan.json
```

The `--plan` mode reuses local JSON and makes no Copilot calls. Use it for this release to avoid further Copilot costs. A full run writes local evidence under `runs/` and `test_answers/runs/` and can modify the grading checkout. Keep answers, plans, logs, and run artifacts local.

See [design](DESIGN.md) and [validation](VALIDATION.md).
