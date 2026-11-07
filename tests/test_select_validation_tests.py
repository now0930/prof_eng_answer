"""PR classification must not silently skip unknown or safety-sensitive changes."""

from scripts.select_validation_tests import classify_paths, is_documentation


def test_document_only_avoids_full_release():
    result = classify_paths(["docs/reviews/pr19_notes.md", "README.md"])
    assert result["mode"] == "docs"
    assert result["tests"] == []


def test_topic_sheet_is_not_ordinary_documentation():
    assert not is_documentation("docs/topic_sheets/instrumentation.md")
    result = classify_paths(["docs/topic_sheets/instrumentation.md"])
    assert result["mode"] == "focused"
    assert result["topic_validation"] is True
    assert "tests/test_fact_anchor_scoring_exclusions.py" in result["tests"]


def test_expert_accuracy_adapter_runs_authoritative_grading_regressions():
    result = classify_paths([
        "grading/quality/expert_accuracy_benchmark.py",
        "tests/test_expert_accuracy_benchmark.py",
    ])
    assert result["mode"] == "focused"
    assert "tests/test_deterministic_primary_grader.py" in result["tests"]
    assert "tests/test_expert_accuracy_benchmark.py" in result["tests"]


def test_workflow_change_checks_ci_contracts_without_full_release():
    result = classify_paths([".github/workflows/validation.yml"])
    assert result["mode"] == "focused"
    assert "tests/test_release_candidate.py" in result["tests"]
    assert "tests/test_select_validation_tests.py" in result["tests"]


def test_mixed_topic_and_grading_changes_keep_both_guards():
    result = classify_paths(["rubrics/topic_packs/example/fact_anchor.json",
                             "grading/scoring/deterministic_score_engine.py"])
    assert result["mode"] == "focused"
    assert result["topic_validation"] is True
    assert "tests/test_deterministic_score_engine.py" in result["tests"]


def test_test_only_updates_run_that_test():
    result = classify_paths(["tests/test_expert_accuracy_benchmark.py"])
    assert result["mode"] == "focused"
    assert "tests/test_expert_accuracy_benchmark.py" in result["tests"]


def test_unknown_dependency_change_runs_full_release():
    assert classify_paths(["pyproject.toml"])["mode"] == "full"
    assert classify_paths(["requirements.txt"])["mode"] == "full"
    assert classify_paths(["scripts/unknown_business_logic.py"])["mode"] == "full"


def test_standalone_test_scripts_fail_closed_to_full():
    assert classify_paths(["scripts/test_some_regression.py"])["mode"] == "full"


def test_empty_diff_runs_full_release():
    assert classify_paths([])["mode"] == "full"


def test_docs_and_code_are_not_docs_only():
    assert classify_paths(["docs/reviews/readme.md",
                           "grading/evidence/logic_check_evaluator.py"])["mode"] == "focused"
