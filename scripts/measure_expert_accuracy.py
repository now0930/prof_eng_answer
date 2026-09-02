#!/usr/bin/env python3
"""Measure grading output against reviewed expert golden labels."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from expert_accuracy_benchmark import (
    load_jsonl,
    measure_accuracy,
    prediction_from_grade,
    validate_gold_case,
    validate_prediction,
)


DEFAULT_GOLDEN = REPO / "calibration" / "expert_accuracy_golden.jsonl"


def _grade_argument(value: str) -> tuple[str, Path]:
    case_id, separator, raw_path = value.partition("=")
    if not separator or not case_id.strip() or not raw_path.strip():
        raise argparse.ArgumentTypeError("--grade requires CASE_ID=GRADE_JSON")
    return case_id.strip(), Path(raw_path).expanduser().resolve()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden", type=Path, default=DEFAULT_GOLDEN)
    parser.add_argument("--predictions", type=Path)
    parser.add_argument("--grade", action="append", type=_grade_argument, default=[])
    parser.add_argument("--include-draft", action="store_true")
    parser.add_argument("--require-cases", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    gold = load_jsonl(args.golden.resolve(), validate_gold_case)
    predictions = []
    if args.predictions:
        predictions.extend(load_jsonl(args.predictions.resolve(), validate_prediction))
    for case_id, path in args.grade:
        predictions.append(prediction_from_grade(
            case_id,
            json.loads(path.read_text(encoding="utf-8")),
        ))

    report = measure_accuracy(gold, predictions, include_draft=args.include_draft)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if args.require_cases and report["evaluated_case_count"] == 0:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
