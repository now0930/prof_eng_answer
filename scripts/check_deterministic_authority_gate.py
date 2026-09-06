#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deterministic_replay_audit import run_deterministic_replay_audit
from grading_authority_policy import evaluate_authority_removal_gate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    replay = run_deterministic_replay_audit(
        root=ROOT,
        golden_path=ROOT / "calibration" / "expert_accuracy_golden.jsonl",
    )
    report = evaluate_authority_removal_gate(
        replay,
        known_overgrading_regression_pass=replay["known_overgrading_regression_pass"],
        normal_answer_regression_pass=replay["normal_answer_regression_pass"],
        score_verdict_consistency_pass=replay["score_verdict_consistency_pass"],
    )
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 2 if args.require_ready and not report["ready"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
