#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from coverage_feedback_retention import (
    DEFAULT_MAX_AGE_DAYS,
    apply_coverage_retention_plan,
    build_coverage_retention_plan,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Plan or explicitly apply retention only to "
            "coverage_feedback_event.json artifacts."
        )
    )
    parser.add_argument(
        "--sessions-root",
        default="data/sessions",
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=DEFAULT_MAX_AGE_DAYS,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Actually delete eligible coverage artifacts. "
            "Without this flag the command is dry-run only."
        ),
    )
    args = parser.parse_args()

    plan = build_coverage_retention_plan(
        Path(args.sessions_root),
        max_age_days=args.max_age_days,
    )
    result = apply_coverage_retention_plan(
        plan,
        apply=args.apply,
    )

    print(
        json.dumps(
            {
                "plan": plan,
                "result": result,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
