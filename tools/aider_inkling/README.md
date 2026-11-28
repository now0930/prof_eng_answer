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

## Switch AI providers

Set either backend independently. Leave the variables unset to use Copilot
for planning and Aider + Inkling for editing. The compiler, grading checks,
and final regression test are shared by both paths.

```sh
export V6_PLANNER_COMMAND='["/path/to/planner-wrapper"]'
export V6_EDITOR_COMMAND='["/path/to/editor-wrapper"]'
./develop.sh "Describe the desired grading change" --compile-only
```

- A planner wrapper receives the planning prompt as UTF-8 on stdin. Its
  working directory is a temporary copy of the supported project files. It
  writes a single `inkling_plan_v6` JSON object to stdout and diagnostics
  to stderr. Use `--plan` to bypass planning and reuse approved JSON.
- An editor wrapper runs from the grading checkout. The controller appends
  the absolute path of the compiled task prompt and the single allowed
  repository-relative target path to its argument array. The wrapper applies
  the exact edit in place and reports failure with a nonzero exit code.
  The controller still verifies the staged index, commit, changed paths, and
  exact output. A custom editor uses its own model connection.
- A configured command is a JSON argument array. Keep credentials in the
  wrapper's environment or credential store, since command arguments can
  appear in logs. These commands run locally with your account's permissions.
  Wrappers that call external models must keep private answers, credentials,
  and private logs out of their requests and respect your cost limits.

After inspecting the compiled plan, run `./develop.sh --plan /path/to/approved-plan.json`
to start the confirmation and editing flow with the selected editor.

## Local Ollama profiles

On the 245k host, the built-in adapter uses installed local GGUF models through
Ollama on `127.0.0.1:11434`. Select planning and editing models independently.
The planning context contains explicit tracked project paths within the
controller's temporary workspace. The model will only receive these files.

```sh
export V6_OLLAMA_PLAN_MODEL=llama3.2:3b
export V6_OLLAMA_PLAN_CONTEXT='["grading/coverage_feedback/retention.py"]'
./develop.sh "Describe one exact change in the selected file" --compile-only

export V6_OLLAMA_EDIT_MODEL=llama3.2:3b
./develop.sh --plan /path/to/approved-plan.json
```

Set only one backend per role. Unset the relevant `V6_OLLAMA_*_MODEL` variable
to use the corresponding command adapter or default. A saved plan bypasses
the planning model. Keep model inputs small and specify exact target symbols
and test files in the objective. The local adapter limits each request to
16,000 input bytes and rejects cloud model tags. The built-in editor compares
the model output with the compiler's approved hash before writing the file.

Run the platform unit tests with
`python3 -m unittest discover -s tools/aider_inkling -p test_ai_backends.py`
from the Git checkout.
