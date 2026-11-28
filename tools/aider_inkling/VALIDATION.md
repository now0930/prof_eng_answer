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
