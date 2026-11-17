#!/usr/bin/env python3
"""Research-only, source-verified five-Fact condition/scope shadow CLI."""
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
from grading.evidence.s7_condition_scope_shadow import evaluate_condition_scope_shadow


def _external(path: Path) -> bool:
    return path.is_absolute() and not path.resolve().is_relative_to(ROOT.resolve())


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-review", type=Path, required=True)
    p.add_argument("--nonformula-triage", type=Path, required=True)
    p.add_argument(
        "--challenge", type=Path,
        default=ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json",
    )
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        if (not _external(args.source_review)
                or not _external(args.nonformula_triage)
                or not _external(args.output)
                or args.output.exists() or args.output.is_symlink()):
            raise ValueError("research artifacts must use safe external paths")
        src = json.loads(args.source_review.read_text(encoding="utf-8"))
        triage = json.loads(args.nonformula_triage.read_text(encoding="utf-8"))
        challenge = json.loads(args.challenge.read_text(encoding="utf-8"))
        rev = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT,
            capture_output=True, text=True, check=False,
        )
        if (rev.returncode
                or rev.stdout.strip() != src.get("inventory_execution_sha")
                or rev.stdout.strip() != triage.get("execution_commit_sha")):
            raise ValueError("cross-HEAD evidence must not be treated as verified")
        report = evaluate_condition_scope_shadow(src, triage, challenge)
        report["execution_commit_sha"] = rev.stdout.strip()
        args.output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            json.dump(report, out, ensure_ascii=False, indent=2, sort_keys=True)
            out.write("\n")
        print(json.dumps({
            "status": report["status"],
            "draft_pairs": report["draft_pair_count"],
            "condition_dependency_facts": report["condition_dependency_fact_count"],
            "nyquist_scope_facts": report["nyquist_scope_fact_count"],
            "positive_surface_cues": report["positive_surface_cues"],
            "adversarial_contrary_cues": report["adversarial_contrary_cues"],
            "source_conditions_proven": report["source_conditions_proven"],
            "accuracy_claim": "NOT_ESTABLISHED",
            "score_admission": "DISABLED",
        }, ensure_ascii=False))
        return 0 if report["status"] == "CONDITION_SCOPE_DRAFT_CUES_REVIEW_ONLY" else 2
    except (KeyError, ValueError, TypeError, OSError, json.JSONDecodeError):
        print(json.dumps({"status": "CONDITION_SCOPE_SHADOW_HOLD",
                          "score_admission": "DISABLED"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
