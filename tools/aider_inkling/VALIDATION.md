# V6.0 RC1 validation

The prior 245k integration run recorded **1,729 passed, 2 skipped** in 149.94 seconds. The same answer scored **12.4 → 12.4 out of 25**, with zero external grading provider calls. The three planned file edits passed the change-scope checks. The answer's missing evidence remained unresolved.

The initial Copilot-generated plan failed nested JSON Anchor symbol validation. The compiler's symbol handling was manually corrected, and the same saved plan was reused for the recorded successful run. RC1 is a release candidate pending repeated practical validation.

The registration check compiles both Python files and checks both shell scripts for syntax. The historical end-to-end run is recorded in [Issue #51](https://github.com/now0930/prof_eng_answer/issues/51). Registration uses no further Copilot calls.

## Multi-provider verification on 245k

The deployed command-adapter flow passed an offline integration trial in a
temporary repository with mock planner, editor, grader, and final test runner.
The local Ollama integration was then exercised against a separate checkout of
grading commit `a4dccee`.

| Model | Planner JSON compiled | Exact edits accepted |
| --- | --- | --- |
| `llama3.2:3b` | 1/1 | 3/3 |
| `hf.co/sky7350/Mica-v0.1-4B:Q5_K_M` | 1/1 | 3/3 |

The edit cases added behavior-preserving comments to three existing Python
modules. Both editors received the same approved edits. Earlier full-source
and free-form block prompts generated mismatches. The final editor sends only
approved blocks, checks the proposed bytes against the compiler's output hash,
and then replaces the file. These results cover integration and edit fidelity
on small changes. Broader feature work and grading-quality improvements
remain separate validation targets.

The clean grading baseline at `a4dccee` reported **1,718 passed, 2 skipped**.
No Copilot calls or billable external model calls were made in these trials.

A separate functional trial used three changes to existing project code:
skip a symlinked session directory, preserve numeric zero in event text
normalization, and preserve false in aggregate text normalization. Both models
passed all three exact-output comparisons and functional assertions. These
trial changes were confined to temporary grading checkouts.

The integrated Mica run applied all three comment-only edits and deterministically
regraded the same local answer, **5.0 → 5.0 out of 25**, with zero external
grading provider calls. This run used a fresh checkout of `a4dccee`.

The post-edit regression run also passed **1,718 tests with 2 skipped** in
139.22 seconds. The provider adapter unit suite passed **7 tests**.

## Modular workflow refactor

The entry point now delegates to separate planner, compiler, executor, and
validator modules. The offline workflow test exercises external planner
command selection, approved context, V6 compilation, saved-plan replay,
the standard Aider command with a test double, and validation of the
result. It also checks that local planner settings, alternate editor settings,
and writes beyond the approved file are rejected.

On 245k, three existing project plans compiled successfully in a clean
grading checkout with no model calls or grading changes. The earlier live
regression and model comparison results above belong to the earlier runtime.
A fresh live model execution and regression run were not part of this refactor
check.

Run the workflow test from the platform directory with
`bash test_workflow.sh`.

## Gemini check

The offline workflow test verifies the Gemini request URL, header, JSON
schema, selected-source context and compilation of the simulated API
response.

On 245k, one live Gemini Developer API request using
`gemini-3.1-flash-lite` generated a V6 plan from synthetic project files. The
response passed exact-edit preflight and left the synthetic checkout
unchanged. The API key was supplied for that request without saving it.
Billing for the Google project was not independently checked.

A separate saved-plan test used Aider with local Inkling on a clean checkout
of `a4dccee`. Aider initially wrote its history in the grading checkout,
which correctly triggered the file-scope guard. The batch editor now writes
chat and input history to the platform's `aider_home/` directory.

After the fix, only the approved comment in the target Python file changed.
The same answer scored **5.0 → 5.0**, with zero external grading provider
calls. The full pytest run reported **1,718 passed, 2 skipped** in 147.67
seconds. The small synthetic Gemini compilation test and the full
saved-plan Inkling test were separate runs.
