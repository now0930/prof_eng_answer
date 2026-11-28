# Aider–Inkling V6.0 RC1

Install the files from this directory into `~/aider_inkling` on Linux. The integrated controller expects a separate grading checkout at `~/aider_inkling/repo`. Use a disposable grading checkout when running automation that edits files. The validator uses the existing Python environment at `~/hermes/validation/.venv-xdist/bin/python` with the grading dependencies, pytest, and pytest-xdist.

For an end-to-end run, provide an authorized local baseline answer at `~/aider_inkling/test_answers/feedback_control.txt`. Plans with scope checks also require a local `test_answers/compiler_case.json` and its referenced inputs. Install Docker Compose and make the local Ollama model `inkling-2-mini-aider` available on port 11434. Start the proxy in a separate terminal with `python3 inkling_proxy.py`. The controller directs batch Aider requests to port 11435.

From `~/aider_inkling`, compile an existing V6 JSON plan or run it using the following commands.

```sh
./develop.sh --plan /path/to/approved-plan.json --compile-only
./develop.sh --plan /path/to/approved-plan.json
```

The `--plan` mode reuses local JSON and makes no Copilot calls. Use it for this release to avoid further Copilot costs. A full run writes local evidence under `runs/` and `test_answers/runs/` and can modify the grading checkout. Aider chat and input history are stored under `aider_home/`. Keep answers, plans, logs, and run artifacts local.

See [design](DESIGN.md) and [validation](VALIDATION.md).

## Workflow modules

- `develop.py` owns the command-line entry point, run lock, user approval, and stage order.
- `planner.py` builds the V6 JSON plan through Copilot or an external-provider command. It also loads saved plans.
- `compiler.py` validates the plan, tracked paths, and symbols, and compiles exact edits.
- `executor.py` runs Aider with local Inkling for each approved task.
- `validator.py` checks edit scope and exact output, runs the same-answer grading and scope checks, and launches pytest.

The Copilot planner requires the existing `COPILOT_FREE_CONFIRMED=1` setting.
To use an independently configured external-service wrapper, set
`V6_PLANNER_COMMAND` to its JSON argument array and `V6_EXTERNAL_PLAN_CONTEXT`
to the JSON array of approved tracked files. The wrapper reads the planning
prompt from standard input and writes only an `inkling_plan_v6` JSON object to
standard output. Keep it configured for an external service. The controller
restricts the files copied into its input workspace, while the wrapper controls
its network destination. OpenAI is outside the scope of this release.

For example, with an external planner wrapper already configured:

```sh
export V6_PLANNER_COMMAND='["/path/to/external-planner-wrapper"]'
export V6_EXTERNAL_PLAN_CONTEXT='["grading/coverage_feedback/retention.py"]'
./develop.sh "Describe the desired change" --compile-only
```

Clear any previous `V6_OLLAMA_PLAN_MODEL`, `V6_OLLAMA_PLAN_CONTEXT`,
`V6_EDITOR_COMMAND`, and `V6_OLLAMA_EDIT_MODEL` settings before running the
current entry point. A saved plan bypasses provider selection. The compiled
edits still require interactive approval before Aider + Inkling starts.

## Gemini planner

The Gemini Developer API can produce the V6 plan directly. The default model
is `gemini-3.8-flash`; override it with `V6_GEMINI_MODEL` if needed. Provide
`GEMINI_API_KEY` in the calling shell and choose only the tracked files you
intend to share with Google.

```sh
unset V6_PLANNER_COMMAND
export V6_PLAN_PROVIDER=gemini
export V6_GEMINI_MODEL=gemini-3.1-flash-lite
export V6_EXTERNAL_PLAN_CONTEXT='["grading/coverage_feedback/retention.py"]'
./develop.sh "Describe the desired change" --compile-only
```

The example selects the Flash-Lite model used in the live smoke test. Use a free-tier project for a free smoke test and synthetic inputs for the first API request.

The request uses the shared plan schema and the explicitly selected files.
The compiler still checks the response locally. Inspect the saved
`runs/<timestamp>/plan.json`, then use `--plan` to run Aider + Inkling after
confirming the edits. Replaying a plan makes no Gemini request.
