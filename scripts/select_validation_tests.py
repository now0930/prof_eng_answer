#!/usr/bin/env python3
"""Choose PR-only focused validation; unknown changes fail closed to full CI.

PR synchronize diffs the whole push when the event provides a trusted
before SHA. If the previous SHA cannot be verified, compare the entire PR
against the merge base. Neither path may silently discard changed files.
"""
from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess

SHA = re.compile(r"[0-9a-f]{40}\Z")
PYTEST_FILE = re.compile(r"tests/test_[A-Za-z0-9_]+\.py\Z")
SCRIPT_TEST_FILE = re.compile(r"scripts/test_[A-Za-z0-9_]+\.py\Z")

GRADING_TESTS = (
    "tests/test_deterministic_primary_grader.py",
    "tests/test_deterministic_requirement_evaluator.py",
    "tests/test_deterministic_score_engine.py",
    "tests/test_expert_accuracy_benchmark.py",
    "tests/test_expert_accuracy_production_gate.py",
    "tests/test_fact_anchor_evidence_adapter.py",
    "tests/test_qualitative_de_authority.py",
    "tests/test_qualitative_de_provider_transport.py",
    "tests/test_regrade_semantic_success.py",
)
TOPIC_TESTS = (
    "tests/test_fact_anchor_evidence_adapter.py",
    "tests/test_fact_anchor_scoring_exclusions.py",
    "tests/test_fact_anchor_independent_revision_holds.py",
    "tests/test_fact_anchor_unresolved_source_holds.py",
    "tests/test_deterministic_requirement_evaluator.py",
    "tests/test_deterministic_primary_grader.py",
    "tests/test_machine_contract_contradiction_policy.py",
    "tests/test_expert_accuracy_benchmark.py",
)
RUNTIME_TESTS = (
    "tests/test_regrade_to_telegram.py",
    "tests/test_telegram_export_grading_regression.py",
    "tests/test_release_candidate.py",
    "tests/test_deterministic_primary_grader.py",
)
CI_TESTS = (
    "tests/test_release_candidate.py",
    "tests/test_regrade_semantic_success.py",
    "tests/test_expert_accuracy_production_gate.py",
    "tests/test_expert_accuracy_benchmark.py",
)
GRADING_SCRIPTS = {
    "scripts/regrade_expert_accuracy_seed.py",
    "scripts/measure_expert_accuracy.py",
    "scripts/check_accuracy_release_gate.py",
    "scripts/check_demand_state_stability_gate.py",
    "scripts/analyze_demand_state_stability.py",
    "scripts/audit_expert_qualification_failures.py",
}
CI_SCRIPTS = {
    "scripts/select_validation_tests.py",
    "scripts/validate_release.sh",
    "scripts/release_candidate.py",
}


def is_documentation(path: str) -> bool:
    return path == "README.md" or (
        path.startswith("docs/")
        and not path.startswith("docs/topic_sheets/")
        and path.endswith(".md")
    )


def classify_paths(paths: list[str]) -> dict[str, object]:
    if not paths:
        return {"mode": "full", "tests": [], "topic_validation": False,
                "reason": "empty_diff"}
    scopes: set[str] = set()
    tests: set[str] = set()
    unknown: list[str] = []
    for path in paths:
        if is_documentation(path):
            continue
        if PYTEST_FILE.fullmatch(path):
            tests.add(path)
        elif SCRIPT_TEST_FILE.fullmatch(path):
            # Standalone script tests are not necessarily discoverable by
            # pytest. Require the complete release suite for these changes.
            unknown.append(path)
        elif path.startswith("grading/") or path in {
            "grading_agents.py",
            "grading_ontology/engineering_concepts.json",
            "grading_ontology/quantities.json",
        }:
            scopes.add("grading")
        elif path.startswith(("rubrics/", "calibration/", "grading_ontology/",
                              "docs/topic_sheets/")):
            scopes.add("topic")
        elif path.startswith("study/") or path in {"bot.py"}:
            scopes.add("runtime")
        elif path.startswith(".github/") or path in CI_SCRIPTS:
            scopes.add("ci")
        elif path in GRADING_SCRIPTS:
            scopes.add("grading")
        else:
            unknown.append(path)
    if unknown:
        return {"mode": "full", "tests": [], "topic_validation": False,
                "reason": "unclassified_or_high_risk"}
    if not scopes and not tests:
        return {"mode": "docs", "tests": [], "topic_validation": False,
                "reason": "documentation_only"}
    tests.add("tests/test_select_validation_tests.py")
    for scope, group in (
        ("grading", GRADING_TESTS),
        ("topic", TOPIC_TESTS),
        ("runtime", RUNTIME_TESTS),
        ("ci", CI_TESTS),
    ):
        if scope in scopes:
            tests.update(group)
    return {"mode": "focused", "tests": sorted(tests),
            "topic_validation": "topic" in scopes,
            "reason": "+".join(sorted(scopes)) or "changed_tests"}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], check=check, capture_output=True)


def diff_paths(base: str, head: str) -> list[str]:
    result = git("diff", "--name-only", "-z", base, head, "--").stdout
    return sorted({part.decode("utf-8") for part in result.split(b"\0") if part})


def select_diff() -> tuple[list[str], str]:
    base = os.environ["BASE_SHA"].lower()
    head = os.environ["HEAD_SHA"].lower()
    before = os.environ.get("BEFORE_SHA", "").lower()
    action = os.environ.get("PR_ACTION", "")
    if not SHA.fullmatch(base) or not SHA.fullmatch(head):
        raise ValueError("invalid PR SHA")
    if (
        action == "synchronize"
        and SHA.fullmatch(before)
        and before != head
        and git("cat-file", "-e", f"{before}^{{commit}}", check=False).returncode == 0
        and git("merge-base", "--is-ancestor", before, head, check=False).returncode == 0
    ):
        return diff_paths(before, head), "synchronize_push"
    merge_base = git("merge-base", base, head).stdout.decode().strip()
    if not SHA.fullmatch(merge_base):
        raise ValueError("could not establish PR merge base")
    return diff_paths(merge_base, head), "full_pr_fallback"


def main() -> None:
    paths, range_type = select_diff()
    result = classify_paths(paths)
    # Deleted/renamed tests must never be silently ignored.
    if result["mode"] == "focused" and any(
        not Path(path).is_file() for path in result["tests"]
    ):
        result = {"mode": "full", "tests": [],
                  "topic_validation": False, "reason": "missing_selected_test"}
    output = Path(os.environ["GITHUB_OUTPUT"])
    with output.open("a", encoding="utf-8") as stream:
        stream.write(f"mode={result['mode']}\n")
        stream.write(f"tests={' '.join(result['tests'])}\n")
        stream.write(f"topic_validation={str(result['topic_validation']).lower()}\n")
    print(f"VALIDATION_MODE={result['mode']} DIFF_RANGE={range_type} "
          f"CHANGED_FILES={len(paths)} REASON={result['reason']}")
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with Path(summary_file).open("a", encoding="utf-8") as stream:
            stream.write(f"Validation: **{result['mode']}** "
                         f"({range_type}; {len(paths)} files; "
                         f"{result['reason']}).\n")
    # The focused check never claims a full Release Gate or production READY.


if __name__ == "__main__":
    main()
