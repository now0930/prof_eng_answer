from __future__ import annotations

import ast
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = (
    ROOT / "gemini_grader.py",
    ROOT / "question_type_coverage_adapter.py",
    ROOT / "verified_defect_reconciliation.py",
    ROOT / "grading_agents.py",
    ROOT / "grade_output_summarizer.py",
    ROOT / "verdict_consistency.py",
)


def _top_level_function_names(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]


def test_grading_pipeline_modules_have_no_function_redefinition_chain() -> None:
    for path in MODULES:
        counts = Counter(_top_level_function_names(path))
        duplicates = sorted(name for name, count in counts.items() if count > 1)
        assert not duplicates, f"{path.name}: duplicate top-level functions: {duplicates}"


def test_public_finalization_entrypoints_remain_explicit() -> None:
    required = {
        "gemini_grader.py": {
            "build_gemini_grading_prompt",
            "gemini_semantic_grade",
        },
        "question_type_coverage_adapter.py": {
            "attach_question_type_coverage_feedback",
            "ensure_grade_question_type_coverage",
        },
        "verified_defect_reconciliation.py": {
            "reconcile_verified_defects_with_coverage",
        },
        "grading_agents.py": {"run_agent_pipeline"},
        "grade_output_summarizer.py": {
            "summarize_grade_for_telegram",
            "_build_payload",
            "_normalise_summary",
            "_render",
        },
        "verdict_consistency.py": {
            "reconcile_verdict_summary",
            "enforce_final_decision_consistency",
            "enforce_final_score_status_narrative_consistency",
        },
    }
    for path in MODULES:
        assert required[path.name].issubset(
            _top_level_function_names(path)
        ), path.name


def test_previous_implementation_alias_pattern_is_not_reintroduced() -> None:
    forbidden = (
        "PREVIOUS_BUILD_PAYLOAD",
        "PREVIOUS_RENDER",
        "PREVIOUS_ENFORCE_FINAL_DECISION",
        "existing_enforce_final_decision_consistency",
        "_ORIGINAL_ATTACH_QTYPE_COVERAGE",
        "_VERIFIED_DEFECT_PREVIOUS_RECONCILE",
        "_STAGE25G5B_PREVIOUS_RECONCILE",
        "_STAGE25G5E2_PREVIOUS_RECONCILE",
        "_STAGE17E5_PREVIOUS_RUN_AGENT_PIPELINE",
    )
    for path in MODULES:
        source = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in source, f"{path.name}: forbidden wrapper alias {token}"


def main() -> None:
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"FINALIZATION_MODULE_STRUCTURE_TESTS={len(tests)}_PASS")


if __name__ == "__main__":
    main()
