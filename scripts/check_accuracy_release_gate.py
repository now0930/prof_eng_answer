#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from accuracy_release_gate import evaluate_accuracy_release_gate
from expert_accuracy_benchmark import load_jsonl, validate_gold_case


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument(
        "--golden",
        type=Path,
        default=ROOT / "calibration" / "expert_accuracy_golden.jsonl",
    )
    parser.add_argument(
        "--policy",
        type=Path,
        default=ROOT / "calibration" / "expert_accuracy_release_policy.json",
    )
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    report = json.loads(args.report.resolve().read_text(encoding="utf-8"))
    gold = load_jsonl(args.golden.resolve(), validate_gold_case)
    policy = json.loads(args.policy.resolve().read_text(encoding="utf-8"))
    result = evaluate_accuracy_release_gate(report, gold, policy)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.require_ready and not result["ready"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
