#!/usr/bin/env python3
"""Compare a candidate with current main; reuse existing offline Topic checks.

This is an ordinary-development guard, not an owner-authentication mechanism.
A separately authorized contract transition needs an explicit reviewed policy
change, not a candidate-authored exception or a regenerated expected score.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTECTED = frozenset({
    "GRADING_DIRECTION_CONTRACT.md",
    "pytest.ini",
    "calibration/pytest_quarantine.json",
    "calibration/deterministic_authority_policy.json",
    "calibration/grading_integrity_drift_baseline.json",
    "calibration/general_grading_cross_topic_cases.json",
    "calibration/expert_accuracy_golden.jsonl",
    "grading/evidence/fact_anchor_independent_revision_holds_20261101.json",
    "grading/evidence/fact_anchor_unresolved_source_holds_20261101.json",
    "grading/evidence/fact_anchor_1656_candidate_holds_20261104.json",
    "scripts/check_grading_integrity_drift.py",
    "tests/test_grading_authority_policy.py",
    "tests/test_deterministic_score_engine.py",
    "tests/test_qualitative_de_authority.py",
    "tests/test_fatal_taxonomy.py",
    "tests/test_verified_correctness_score_cap.py",
    "tests/test_deterministic_topic_router.py",
    "tests/test_grading_integrity_drift.py",
    "tests/test_fact_anchor_scoring_exclusions.py",
    "tests/test_fact_anchor_independent_revision_holds.py",
    "tests/test_fact_anchor_unresolved_source_holds.py",
    "tests/test_fact_anchor_1656_candidate_holds.py",
    "tests/test_cross_topic_accuracy_contract.py",
})
TOPIC_PREFIXES = ("rubrics/topic_packs/", "rubrics/generated/",
                  "master_topic_packs/", "grading/ontology/")
TOPIC_FILES = frozenset({
    "grading/evidence/approved_fact_registry.json",
    "grading/evidence/fact_anchor_scoring_exclusions_20261101.json",
    "grading/evidence/fact_anchor_scoring_exclusions.py",
    "scripts/build_generated_rubrics.py",
    "scripts/validate_topic_pack_release.py",
    "scripts/validate_topic_packs.py",
    "scripts/validate_topic_pack_quality.py",
    "scripts/check_generated_rubrics_freshness.py",
    "scripts/rubric_manager.py",
    "scripts/topic_pack_workflow_controller.py",
})


def regression_path(path: str) -> bool:
    return (path.startswith(("tests/", "scripts/test_"))
            and path.endswith(".py"))


def protected_path(path: str) -> bool:
    return (path in PROTECTED
            or (path.startswith(("calibration/qtype_golden/", "calibration/risk_golden/"))
                and path.endswith(".json"))
            or (path.startswith("calibration/")
                and path.endswith("_overgrading_regression.json")))


def classify_changes(rows: list[tuple[str, str]]) -> tuple[list[str], list[str], bool]:
    """Do not allow existing protected contracts/fixtures to be rewritten.

    Additive tests/fixtures are allowed. Other existing tests edited in place
    need a visible review, not an automatic claim of unchanged assertions.
    """
    blocked, review = [], []
    topic_changed = False
    for status, path in rows:
        if status != "A" and (protected_path(path)
                              or (status == "D" and regression_path(path))):
            blocked.append(path)
        elif status != "A" and regression_path(path):
            review.append(path)
        if path.startswith(TOPIC_PREFIXES) or path in TOPIC_FILES:
            topic_changed = True
    return sorted(set(blocked)), sorted(set(review)), topic_changed


def changed_paths(base: str) -> list[tuple[str, str]]:
    # A moving or unrelated main must not silently change the comparison scope.
    sha = subprocess.check_output(
        ["git", "rev-parse", "--verify", base + "^{commit}"], cwd=ROOT, text=True
    ).strip()
    subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"],
                   cwd=ROOT, check=True)
    raw = subprocess.check_output(
        ["git", "diff", "--no-renames", "--name-status", "-z", sha, "HEAD", "--"],
        cwd=ROOT,
    ).split(b"\0")
    if raw[-1] != b"" or (len(raw) - 1) % 2:
        raise ValueError("unexpected Git diff format")
    return [(raw[i].decode("ascii"), raw[i+1].decode("utf-8", "surrogateescape"))
            for i in range(0, len(raw)-1, 2)]


def run_topic_checks() -> None:
    env = os.environ.copy()
    for key in list(env):
        if key in {"GEMINI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_GENERATIVE_AI_API_KEY",
                   "CLOVA_API_KEY", "CLOVA_APIGW_API_KEY"} or key.startswith("VALIDATION_"):
            env.pop(key, None)
    env.update(VALIDATION_LIVE_API="0", QUALITATIVE_DE_MODE="off", PROMOTE_GENERATED="0")
    for args in (
        ("scripts/rubric_manager.py", "validate-all"),
        ("scripts/check_generated_rubrics_freshness.py",),
        ("scripts/rubric_manager.py", "validate-topic-pack-release", "--all"),
    ):
        subprocess.run([sys.executable, "-B", *args], cwd=ROOT, env=env, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--topic-checks", action="store_true",
                        help="run existing Topic validators when relevant paths changed")
    args = parser.parse_args()
    try:
        blocked, review, topic_changed = classify_changes(changed_paths(args.base))
        for path in blocked:
            print("PROTECTED_CHANGE:", path)
        for path in review:
            print("REVIEW_EXISTING_REGRESSION:", path)
        if blocked:
            print("GRADING_GUARD=HOLD: separately authorized contract review required")
            return 1
        print("GRADING_GUARD=PASS (path-level protection only; not semantic proof)")
        if args.topic_checks:
            if topic_changed:
                run_topic_checks()
            else:
                print("TOPIC_COMPATIBILITY=NOT_APPLICABLE (no relevant changed paths)")
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError):
        print("GRADING_GUARD=HOLD: comparison or existing validator failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
