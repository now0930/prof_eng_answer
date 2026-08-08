#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from coverage_feedback_aggregator import (
    aggregate_coverage_feedback,
)
from coverage_feedback_report import (
    build_coverage_review_report,
    render_coverage_review_markdown,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only cross-session coverage-gap "
            "human-review report."
        )
    )
    parser.add_argument(
        "--sessions-root",
        default="data/sessions",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
    )
    args = parser.parse_args()

    aggregate = aggregate_coverage_feedback(
        Path(args.sessions_root),
        human_review_threshold=args.threshold,
    )
    report = build_coverage_review_report(
        aggregate
    )

    if args.format == "json":
        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(
            render_coverage_review_markdown(
                report
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
