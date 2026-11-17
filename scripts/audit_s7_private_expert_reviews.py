#!/usr/bin/env python3
"""Offline private S7 two-reviewer agreement audit; never a scoring gate.

Requires original label-hidden packet and two independently returned copies.
Writes only metadata and disagreement IDs to a new file outside repository.
It cannot authenticate reviewer independence, establish expert truth, or
change any scorer/Fact Registry/ontology data.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from grading.evidence.s7_independent_review_validation import audit_two_reviewer_submissions


def _external(p: Path) -> bool:
    return p.is_absolute() and not p.resolve().is_relative_to(ROOT.resolve())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original-packet", type=Path, required=True)
    parser.add_argument("--reviewer-a", type=Path, required=True)
    parser.add_argument("--reviewer-b", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        paths = (args.original_packet, args.reviewer_a,
                 args.reviewer_b, args.report)
        if (not all(_external(p) for p in paths)
                or len({str(p.resolve()) for p in paths}) != 4
                or args.report.exists()
                or args.report.is_symlink()):
            raise ValueError("all four paths must be distinct and outside repository")
        packet, a, b = (
            json.loads(path.read_text(encoding="utf-8"))
            for path in paths[:3]
        )
        report = audit_two_reviewer_submissions(packet, a, b)
        args.report.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd = os.open(args.report, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            json.dump(report, out, ensure_ascii=False, indent=2, sort_keys=True)
            out.write("\n")
        print(json.dumps({
            "status": report["status"],
            "reviewed_drafts": report["reviewed_draft_count"],
            "label_agreements": report["matching_relation_labels"],
            "condition_agreements": report["matching_condition_coverage"],
            "manual_disagreements": report["disagreement_count"],
            "expert_benchmark_ready": False,
            "score_admission": "DISABLED",
        }, ensure_ascii=False))
        return 0  # Disagreements require humans, not a failing/automatic CI gate.
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        print(json.dumps({"status": "PRIVATE_TWO_REVIEWER_AUDIT_HOLD",
                          "score_admission": "DISABLED"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
