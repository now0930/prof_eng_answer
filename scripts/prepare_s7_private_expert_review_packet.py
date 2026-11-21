#!/usr/bin/env python3
"""Prepare two private files: label-hidden reviewer packet and sealed author key.

NEVER upload either file as a CI artifact or commit to the repository.
Only expert evaluations entered later can produce independent labels.
"""
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
from grading.evidence.s7_independent_expert_packet import prepare_private_expert_review_packet


def _external(path: Path) -> bool:
    return path.is_absolute() and not path.resolve().is_relative_to(ROOT.resolve())


def _private_new(path: Path, obj: dict) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump(obj, out, indent=2, sort_keys=True, ensure_ascii=False)
        out.write("\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-review", type=Path, required=True)
    p.add_argument("--review-queue", type=Path, required=True)
    p.add_argument("--challenge", type=Path, default=(
        ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json"
    ))
    p.add_argument("--reviewer-packet", type=Path, required=True)
    p.add_argument("--sealed-map", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        paths = (args.source_review, args.review_queue,
                 args.reviewer_packet, args.sealed_map)
        if (not all(_external(path) for path in paths)
                or args.reviewer_packet.resolve() == args.sealed_map.resolve()
                or args.reviewer_packet.exists() or args.sealed_map.exists()
                or args.reviewer_packet.is_symlink()
                or args.sealed_map.is_symlink()):
            raise ValueError("two fresh, separate outputs outside repository required")
        src = json.loads(args.source_review.read_text(encoding="utf-8"))
        queue = json.loads(args.review_queue.read_text(encoding="utf-8"))
        challenge = json.loads(args.challenge.read_text(encoding="utf-8"))
        rev = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, check=False)
        if (rev.returncode
                or rev.stdout.strip() != src.get("inventory_execution_sha")
                or rev.stdout.strip() != queue.get("execution_commit_sha")):
            raise ValueError("review packet must be generated from identical current HEAD")
        packet, key = prepare_private_expert_review_packet(src, queue, challenge)
        _private_new(args.sealed_map, key)
        _private_new(args.reviewer_packet, packet)
        print(json.dumps({
            "status": "PRIVATE_PACKET_CREATED_UNREVIEWED",
            "source_fact_count": len(packet["source_cards"]),
            "unlabeled_answer_count": len(packet["items_to_adjudicate"]),
            "independent_reviews_received": 0,
            "score_admission": "DISABLED",
            "warning": "DO_NOT_COMMIT_OR_UPLOAD_PACKET_OR_SEALED_MAP",
        }, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError):
        print(json.dumps({
            "status": "PRIVATE_EXPERT_REVIEW_PACKET_HOLD",
            "score_admission": "DISABLED",
        }))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
