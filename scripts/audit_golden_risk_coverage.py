#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from golden_risk_coverage import audit_golden_risk_coverage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--golden", type=Path,
        default=ROOT / "calibration/expert_accuracy_golden.jsonl",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()
    report = audit_golden_risk_coverage(root=ROOT, golden_path=args.golden.resolve())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    summary = {key: value for key, value in report.items() if key != "topics"}
    summary["top_priorities"] = report["topics"][:max(args.top, 0)]
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
