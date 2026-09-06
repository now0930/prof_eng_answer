#!/usr/bin/env python3
"""Compare repeated expert-benchmark predictions and report state variance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from demand_state_stability import analyze_stability, load_stability_inputs


def _markdown(report: dict) -> str:
    lines = [
        "# Demand-state stability report",
        "",
        f"- Runs: {report['run_count']}",
        f"- Reviewed universe: {report['reviewed_case_count']} cases / "
        f"{report['reviewed_demand_count']} demands",
        f"- All-run agreement: {report['all_run_state_agreement']}",
        f"- Unstable demands: {report['unstable_demand_count']}",
        f"- Materially unstable demands: {report['materially_unstable_demand_count']}",
        f"- Maximum case score spread: {report['maximum_case_score_spread']}",
        "",
        "## Pairwise runs",
        "",
        "| Left | Right | Agreement | Changed | Material |",
        "|---|---|---:|---:|---:|",
    ]
    for row in report["pairwise"]:
        lines.append(
            f"| {row['left']} | {row['right']} | {row['agreement']} | "
            f"{row['changed_demand_count']} | {row['material_transition_count']} |"
        )
    lines.extend(["", "## Unstable demands", ""])
    for row in report["unstable_demands"]:
        states = ", ".join(f"{name}={state}" for name, state in row["states"].items())
        lines.append(
            f"- `{row['case_id']}:{row['demand_id']}` gold={row['gold']}; {states}"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--golden", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, action="append", required=True)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()
    if len(args.predictions) < 2:
        parser.error("--predictions must be supplied at least twice")
    gold, runs = load_stability_inputs(args.golden, args.predictions)
    report = analyze_stability(gold, runs)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(_markdown(report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
