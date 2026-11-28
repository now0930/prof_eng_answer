# V6.0 RC1 validation

The prior 245k integration run recorded **1,729 passed, 2 skipped** in 149.94 seconds. The same answer scored **12.4 → 12.4 out of 25**, with zero external grading provider calls. The three planned file edits passed the change-scope checks. The answer's missing evidence remained unresolved.

The initial Copilot-generated plan failed nested JSON Anchor symbol validation. The compiler's symbol handling was manually corrected, and the same saved plan was reused for the recorded successful run. RC1 is a release candidate pending repeated practical validation.

The registration check compiles both Python files and checks both shell scripts for syntax. The historical end-to-end run is recorded in [Issue #51](https://github.com/now0930/prof_eng_answer/issues/51). Registration uses no further Copilot calls.
