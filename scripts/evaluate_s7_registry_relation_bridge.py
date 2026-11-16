#!/usr/bin/env python3
"""Offline S7 source-owned relation-ID shadow; NEVER canonical grading."""
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

from grading.evidence.s7_registry_relation_bridge import build_relation_bridge


def _outside_repo(path: Path) -> bool:
    return path.is_absolute() and not path.resolve().is_relative_to(ROOT.resolve())


def _write_private_new(path: Path, result: dict) -> None:
    if not _outside_repo(path) or path.exists() or path.is_symlink():
        raise ValueError("must write fresh private path outside repository")
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2, sort_keys=True)
        out.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-review", required=True, type=Path)
    parser.add_argument("--formula-shadow", required=True, type=Path)
    parser.add_argument(
        "--challenge", type=Path,
        default=ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json",
    )
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if not all(_outside_repo(p) for p in
                   (args.source_review, args.formula_shadow)):
            raise ValueError("S7 evidence inputs must be external artifacts")
        src = json.loads(args.source_review.read_text(encoding="utf-8"))
        formula = json.loads(args.formula_shadow.read_text(encoding="utf-8"))
        fixture = json.loads(args.challenge.read_text(encoding="utf-8"))
        rev = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                             text=True, capture_output=True, check=False)
        if (rev.returncode or rev.stdout.strip() != src.get("inventory_execution_sha")
                or rev.stdout.strip() != formula.get("execution_commit_sha")):
            raise ValueError("S7 source and formula inputs do not belong to this HEAD")
        result = build_relation_bridge(src, fixture, formula)
        result["execution_commit_sha"] = rev.stdout.strip()
        _write_private_new(args.output, result)
        print(json.dumps({
            "status": result["status"],
            "draft_pairs": result["draft_fact_pair_count"],
            "source_id_only_candidates": result["formula_source_id_candidate_count"],
            "adversarial_direction_review": result["formula_direction_conflict_review_count"],
            "unsupported_nonformula": result["uncovered_nonformula_fact_count"],
            "claim_exact_relation": "NOT_ESTABLISHED",
            "score_admission": result["score_admission"],
        }, ensure_ascii=False))
        return 0
    except (ValueError, TypeError, KeyError, OSError, json.JSONDecodeError):
        print(json.dumps({
            "status": "SOURCE_RELATION_BRIDGE_HOLD",
            "score_admission": "DISABLED",
        }))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
