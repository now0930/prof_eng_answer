#!/usr/bin/env python3
"""Evaluate final five S7 pending expert-review Facts (ID-only; score disabled)."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from grading.evidence.s7_remaining_five_expert_queue import evaluate_remaining_five_queue


def _external(path: Path) -> bool:
    return path.is_absolute() and not path.resolve().is_relative_to(ROOT.resolve())


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-review", type=Path, required=True)
    p.add_argument("--nonformula-triage", type=Path, required=True)
    p.add_argument("--condition-scope", type=Path, required=True)
    p.add_argument(
        "--challenge", type=Path,
        default=ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json",
    )
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        if any(not _external(x) for x in (
            args.source_review, args.nonformula_triage,
            args.condition_scope, args.output
        )) or args.output.exists() or args.output.is_symlink():
            raise ValueError("input and output evidence must use private external paths")
        src = json.loads(args.source_review.read_text(encoding="utf-8"))
        triage = json.loads(args.nonformula_triage.read_text(encoding="utf-8"))
        scope = json.loads(args.condition_scope.read_text(encoding="utf-8"))
        challenge = json.loads(args.challenge.read_text(encoding="utf-8"))
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                text=True, capture_output=True, check=False)
        if (commit.returncode
                or commit.stdout.strip() != src.get("inventory_execution_sha")
                or any(commit.stdout.strip() != x.get("execution_commit_sha")
                       for x in (triage, scope))):
            raise ValueError("cross-commit evidence is not admissible for review")
        report = evaluate_remaining_five_queue(src, triage, scope, challenge)
        report["execution_commit_sha"] = commit.stdout.strip()
        args.output.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd = os.open(args.output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            json.dump(report, out, indent=2, ensure_ascii=False, sort_keys=True)
            out.write("\n")
        print(json.dumps({
            "status": report["status"],
            "pending_fact_count": report["queued_fact_count"],
            "authored_draft_count": report["authored_draft_answer_count"],
            "unproven_source_condition_ids": report["source_condition_ids_total"],
            "independently_labeled_answer_count": 0,
            "score_admission": "DISABLED",
        }, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        print(json.dumps({"status": "REMAINING_FIVE_REVIEW_QUEUE_HOLD",
                          "score_admission": "DISABLED"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
