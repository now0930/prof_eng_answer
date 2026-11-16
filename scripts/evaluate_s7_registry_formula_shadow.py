#!/usr/bin/env python3
"""Score-neutral S7 Registry mathematical formula shadow challenge."""
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

from grading.evidence.s7_registry_formula_shadow import evaluate_formula_shadow


def _write_private_new(path: Path, report: dict) -> None:
    if (not path.is_absolute() or path.resolve().is_relative_to(ROOT.resolve())
            or path.exists() or path.is_symlink()):
        raise ValueError("output must be a new absolute path outside repository")
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, indent=2, sort_keys=True)
        out.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-review", required=True, type=Path)
    parser.add_argument(
        "--challenge", type=Path,
        default=ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json",
    )
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if (not args.source_review.is_absolute()
                or args.source_review.resolve().is_relative_to(ROOT.resolve())):
            raise ValueError("source review must be outside repository")
        source = json.loads(args.source_review.read_text(encoding="utf-8"))
        challenge = json.loads(args.challenge.read_text(encoding="utf-8"))
        git = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
            text=True, check=False,
        )
        if git.returncode or git.stdout.strip() != source.get("inventory_execution_sha"):
            raise ValueError("source review artifact belongs to different HEAD")
        report = evaluate_formula_shadow(source, challenge)
        report["execution_commit_sha"] = git.stdout.strip()
        _write_private_new(args.output, report)
        print(json.dumps({
            "status": report["status"],
            "formula_pairs": report["formula_fact_pairs"],
            "positive_syntax_candidates": report["positive_expected_formula_pattern_count"],
            "negative_false_candidates": report["adversarial_expected_formula_pattern_count"],
            "negative_inverted_patterns": report["adversarial_inverted_formula_pattern_count"],
            "accuracy_claim": "NOT_ESTABLISHED",
            "score_admission": report["score_admission"],
        }, ensure_ascii=False))
        return 2 if report["status"] == "COUNTEREXAMPLE_PATTERN_COLLISION_REVIEW" else 0
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError):
        print(json.dumps({
            "status": "FORMULA_SHADOW_HOLD", "score_admission": "DISABLED",
        }))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
