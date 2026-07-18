from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from expert_calibration_dataset import (
    CalibrationContractError,
    DIRECT_SCORE_APPLICATION,
    PRODUCTION_CALIBRATION_ENABLED,
    SCORE_EFFECT,
    load_jsonl,
    validate_dataset,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate an offline expert "
            "calibration JSONL dataset."
        )
    )
    parser.add_argument(
        "dataset",
        type=Path,
    )
    parser.add_argument(
        "--require-finalized",
        action="store_true",
    )
    args = parser.parse_args()

    try:
        records = load_jsonl(args.dataset)
        report = validate_dataset(
            records,
            require_finalized=args.require_finalized,
        )
    except (
        CalibrationContractError,
        OSError,
    ) as error:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(error),
                    "production_calibration_enabled": (
                        PRODUCTION_CALIBRATION_ENABLED
                    ),
                    "score_effect": SCORE_EFFECT,
                    "direct_score_application": (
                        DIRECT_SCORE_APPLICATION
                    ),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    output = {
        key: value
        for key, value in report.items()
        if key != "records"
    }
    output["ok"] = True

    print(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
