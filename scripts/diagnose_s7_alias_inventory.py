#!/usr/bin/env python3
"""Replay the identical S7 Golden pathway and trace missing ontology aliases.

Produces PRIVATE-safe ID-only reports outside the repository:
    python3 -B scripts/diagnose_s7_alias_inventory.py \
      --output /tmp/s7_alias_inventory.json \
      --baseline-output /tmp/s7_baseline_same_run.json

No scores, ontology or registry are modified. Mismatched 47/179 baseline
terminates with exit code 2 and MUST block candidate edits/approvals.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.evidence.s7_alias_root_cause_audit import S7AliasRootCauseTrace
from grading.quality.expert_accuracy_benchmark import (
    load_jsonl, validate_gold_case,
)
from scripts.evaluate_claim_alignment_s7 import evaluate_cases

BASELINE_SHA = "5e4fc40e8925ce147d6d08c838f993b12a563f18"


def _safe_output(path: Path) -> None:
    if (
        not path.is_absolute()
        or path.resolve().is_relative_to(ROOT.resolve())
        or path.exists() or path.is_symlink()
    ):
        raise ValueError("output must be a new absolute path outside the repo")


def _write_private(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--golden", type=Path,
        default=ROOT / "calibration" / "expert_accuracy_golden.jsonl",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline-output", type=Path)
    args = parser.parse_args(argv)
    try:
        _safe_output(args.output)
        if args.baseline_output is not None:
            _safe_output(args.baseline_output)
            if args.output.resolve() == args.baseline_output.resolve():
                raise ValueError("baseline and diagnostic outputs must differ")
    except ValueError as error:
        parser.error(str(error))
    golden = load_jsonl(args.golden, validate_gold_case)
    if not golden:
        parser.error("golden calibration cases unavailable")

    trace = S7AliasRootCauseTrace(root=ROOT)
    baseline = evaluate_cases(golden, alias_observer=trace.observe)
    result = trace.result(baseline)
    revision = subprocess.run(
        ["git", "-c", "safe.directory=" + str(ROOT), "rev-parse", "HEAD"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    result["execution_commit_sha"] = (
        revision.stdout.strip() if revision.returncode == 0 else None
    )
    result["baseline_reference_sha"] = BASELINE_SHA
    result["baseline_source_path"] = str(args.golden.relative_to(ROOT)) if (
        args.golden.is_relative_to(ROOT)
    ) else "external_golden_input"
    result["replayed_via"] = (
        "scripts.evaluate_claim_alignment_s7.evaluate_cases "
        "with read-only alias_observer callback"
    )
    # The original S7 output is optional but, when requested, comes from the
    # SAME 47-case grading/alignment pass rather than a second invocation.
    if args.baseline_output is not None:
        _write_private(args.baseline_output, baseline)
    _write_private(args.output, result)
    summary = {
        "status": result["status"],
        "execution_commit_sha": result["execution_commit_sha"],
        "graded_case_count": baseline["graded_case_count"],
        "policy_abstention_count": baseline["expected_policy_abstention_count"],
        "alias_missing_projection_count": result[
            "projection_count_with_duplicates"
        ],
        "unique_topic_fact_count": result["unique_topic_fact_count"],
        "unique_missing_id_counts_by_role": result[
            "unique_missing_id_counts_by_role"
        ],
        "primary_cause_projection_counts": result[
            "primary_cause_projection_counts"
        ],
        "mismatches": result["baseline_reproduction"]["mismatches"],
        "score_admission": "DISABLED",
    }
    print(json.dumps(summary, ensure_ascii=False))
    # Never allow a false successful replay to justify alias admission.
    return 0 if result["status"] == "REPRODUCED_BASELINE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
