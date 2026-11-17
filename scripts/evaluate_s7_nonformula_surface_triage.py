#!/usr/bin/env python3
"""S7 14-Fact research triage from immutable source and bridge artifacts."""
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

from grading.evidence.s7_nonformula_surface_triage import evaluate_nonformula_triage


def _external(path: Path) -> bool:
    return path.is_absolute() and not path.resolve().is_relative_to(ROOT.resolve())


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-review", type=Path, required=True)
    p.add_argument("--relation-bridge", type=Path, required=True)
    p.add_argument(
        "--challenge", type=Path,
        default=ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json",
    )
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        if not (_external(args.source_review)
                and _external(args.relation_bridge)
                and _external(args.output)
                and not args.output.exists()
                and not args.output.is_symlink()):
            raise ValueError("research-only I/O must use external immutable inputs")
        src = json.loads(args.source_review.read_text(encoding="utf-8"))
        bridge = json.loads(args.relation_bridge.read_text(encoding="utf-8"))
        challenge = json.loads(args.challenge.read_text(encoding="utf-8"))
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT,
            capture_output=True, text=True, check=False,
        )
        if (head.returncode
                or head.stdout.strip() != src.get("inventory_execution_sha")
                or head.stdout.strip() != bridge.get("execution_commit_sha")):
            raise ValueError("source and bridge are not evidence from the same HEAD")
        result = evaluate_nonformula_triage(src, challenge, bridge)
        result["execution_commit_sha"] = head.stdout.strip()
        args.output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            json.dump(result, out, indent=2, ensure_ascii=False, sort_keys=True)
            out.write("\n")
        print(json.dumps({
            "status": result["status"],
            "nonformula_facts": result["nonformula_fact_count"],
            "triage_groups": result["triage_group_counts"],
            "author_draft_pilot_facts": result["pilot_fact_count"],
            "positive_surface_cues": result["pilot_positive_surface_cues"],
            "adversarial_surface_cues": result["pilot_adversarial_surface_cues"],
            "unprobed_facts": result["unprobed_nonformula_fact_count"],
            "accuracy_claim": "NOT_ESTABLISHED",
            "score_admission": result["score_admission"],
        }, ensure_ascii=False))
        return 0 if result["status"] == "NONFORMULA_DRAFT_SURFACE_REVIEW_ONLY" else 2
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        print(json.dumps({
            "status": "NONFORMULA_TRIAGE_HOLD",
            "score_admission": "DISABLED",
        }))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
