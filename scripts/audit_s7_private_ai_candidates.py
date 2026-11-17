#!/usr/bin/env python3
"""Manual offline S7 AI candidate integrity gate; private metadata-only output.

Do not treat the AI candidate pool as independent evaluation data. Its
technical/semantic correctness can be determined only by separate review.
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
from grading.evidence.s7_ai_candidate_integrity_gate import quarantine_ai_candidate_pool


def _external(path: Path) -> bool:
    return path.is_absolute() and not path.resolve().is_relative_to(ROOT.resolve())


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-review", type=Path, required=True)
    p.add_argument("--ai-candidates", type=Path, required=True)
    p.add_argument("--author-challenge", type=Path,
                   default=ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json")
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        if (
            not all(_external(p) for p in
                    (args.source_review, args.ai_candidates, args.report))
            or len({p.resolve() for p in
                    (args.source_review, args.ai_candidates, args.report)}) != 3
            or args.report.exists() or args.report.is_symlink()
        ):
            raise ValueError("fresh private output and external research inputs required")
        src = json.loads(args.source_review.read_text(encoding="utf-8"))
        candidates = json.loads(args.ai_candidates.read_text(encoding="utf-8"))
        challenge = json.loads(args.author_challenge.read_text(encoding="utf-8"))
        report = quarantine_ai_candidate_pool(src, candidates, challenge)
        args.report.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
        fd = os.open(args.report, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            json.dump(report, out, ensure_ascii=False, indent=2, sort_keys=True)
            out.write("\n")
        print(json.dumps({
            "status": report["status"],
            "candidates": report["candidate_count"],
            "structurally_flagged": report["structurally_flagged_count"],
            "flags": report["flag_counts"],
            "independent_benchmark_admission": "PROHIBITED",
            "score_admission": "DISABLED",
        }, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        print(json.dumps({"status": "AI_CANDIDATE_INTEGRITY_HOLD",
                          "score_admission": "DISABLED"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
