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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-stable", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    kwargs = {
        "root": ROOT,
        "golden_path": ROOT / "calibration" / "expert_accuracy_golden.jsonl",
    }
    first = run_deterministic_replay_audit(**kwargs)
    second = run_deterministic_replay_audit(**kwargs)
    stable = first == second
    report = {
        "version": "deterministic_stability_gate_v1",
        "marker": "DETERMINISTIC_STABILITY_GATE_V1",
        "provider_calls": 0,
        "run_count": 2,
        "exact_match": stable,
        "decision": "STABLE" if stable else "UNSTABLE",
        "authority_decision": first["decision"],
        "deterministic_score_coverage": first["deterministic_score_coverage"],
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 2 if args.require_stable and not stable else 0


if __name__ == "__main__":
    raise SystemExit(main())
