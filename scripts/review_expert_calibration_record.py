from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from expert_calibration_dataset import (
    CalibrationContractError,
    finalize_record,
    load_jsonl,
    validate_dataset,
    validate_record,
    write_jsonl_atomic,
)


FINAL_REVIEW_METHODS = (
    "single_expert",
    "dual_expert",
    "panel_adjudication",
    "official_exam_score",
)

FINAL_ADJUDICATION_STATUSES = (
    "reviewed",
    "adjudicated",
)


class ExpertCalibrationReviewError(ValueError):
    pass


def _validate_selector(
    *,
    record_id: str | None,
    submission_hash: str | None,
) -> tuple[str, str]:
    selectors = [
        (
            "record_id",
            record_id.strip()
            if isinstance(record_id, str)
            else "",
        ),
        (
            "submission_hash",
            submission_hash.strip()
            if isinstance(submission_hash, str)
            else "",
        ),
    ]
    selected = [
        item
        for item in selectors
        if item[1]
    ]

    if len(selected) != 1:
        raise ExpertCalibrationReviewError(
            "exactly one selector is required: "
            "record_id or submission_hash"
        )

    return selected[0]


def _normalize_breakdown(
    *,
    a_score: float,
    b_score: float,
    c_score: float,
    d_score: float,
    e_score: float,
) -> dict[str, float]:
    values = {
        "A": a_score,
        "B": b_score,
        "C": c_score,
        "D": d_score,
        "E": e_score,
    }
    output = {}

    for layer, value in values.items():
        if isinstance(value, bool) or not isinstance(
            value,
            (int, float),
        ):
            raise ExpertCalibrationReviewError(
                f"{layer} score must be numeric"
            )

        output[layer] = float(value)

    return output


def review_record_in_dataset(
    dataset_path: str | Path,
    *,
    record_id: str | None = None,
    submission_hash: str | None = None,
    a_score: float,
    b_score: float,
    c_score: float,
    d_score: float,
    e_score: float,
    reviewer_id: str,
    reviewed_at: str,
    review_method: str,
    adjudication_status: str = "reviewed",
) -> dict[str, Any]:
    selector_name, selector_value = (
        _validate_selector(
            record_id=record_id,
            submission_hash=submission_hash,
        )
    )

    if review_method not in FINAL_REVIEW_METHODS:
        raise ExpertCalibrationReviewError(
            "review_method must be one of: "
            + ", ".join(FINAL_REVIEW_METHODS)
        )

    if (
        adjudication_status
        not in FINAL_ADJUDICATION_STATUSES
    ):
        raise ExpertCalibrationReviewError(
            "adjudication_status must be "
            "reviewed or adjudicated"
        )

    path = Path(dataset_path).expanduser()
    records = load_jsonl(path)

    matches = [
        index
        for index, record in enumerate(records)
        if record.get(selector_name) == selector_value
    ]

    if not matches:
        raise ExpertCalibrationReviewError(
            f"record not found for "
            f"{selector_name}={selector_value}"
        )

    if len(matches) != 1:
        raise ExpertCalibrationReviewError(
            f"selector is ambiguous for "
            f"{selector_name}={selector_value}"
        )

    selected_index = matches[0]
    original_record = records[selected_index]
    original_notes = original_record.get("notes", "")
    original_record_hash = original_record.get(
        "record_hash"
    )

    breakdown = _normalize_breakdown(
        a_score=a_score,
        b_score=b_score,
        c_score=c_score,
        d_score=d_score,
        e_score=e_score,
    )
    expert_total = round(
        sum(breakdown.values()),
        10,
    )

    reviewed_record = finalize_record(
        original_record,
        expert_total_score=expert_total,
        expert_breakdown=breakdown,
        reviewer_id=reviewer_id,
        reviewed_at=reviewed_at,
        review_method=review_method,
        adjudication_status=(
            adjudication_status
        ),
    )

    validate_record(
        reviewed_record,
        require_finalized=True,
    )

    if reviewed_record.get("notes", "") != original_notes:
        raise ExpertCalibrationReviewError(
            "existing notes were not preserved"
        )

    updated_records = list(records)
    updated_records[selected_index] = (
        reviewed_record
    )

    prewrite_report = validate_dataset(
        updated_records,
        require_finalized=False,
    )
    write_report = write_jsonl_atomic(
        path,
        updated_records,
        require_finalized=False,
    )

    reloaded_records = load_jsonl(path)
    postwrite_report = validate_dataset(
        reloaded_records,
        require_finalized=False,
    )

    persisted = reloaded_records[selected_index]

    if (
        persisted.get("record_hash")
        != reviewed_record.get("record_hash")
    ):
        raise ExpertCalibrationReviewError(
            "persisted record hash mismatch"
        )

    if len(reloaded_records) != len(records):
        raise ExpertCalibrationReviewError(
            "dataset record count changed"
        )

    return {
        "ok": True,
        "dataset_path": str(path.resolve()),
        "selector": {
            "name": selector_name,
            "value": selector_value,
        },
        "selected_index": selected_index,
        "record_count": len(reloaded_records),
        "record": persisted,
        "record_hash_changed": (
            original_record_hash
            != persisted.get("record_hash")
        ),
        "notes_preserved": (
            persisted.get("notes", "")
            == original_notes
        ),
        "prewrite_report": prewrite_report,
        "write_report": write_report,
        "postwrite_report": postwrite_report,
        "calibration_ready": False,
        "production_calibration_enabled": False,
        "score_effect": "none",
        "direct_score_application": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Finalize exactly one expert "
            "calibration draft record in an "
            "external JSONL dataset."
        )
    )
    parser.add_argument(
        "dataset_jsonl",
        type=Path,
    )

    selector = parser.add_mutually_exclusive_group(
        required=True
    )
    selector.add_argument(
        "--record-id",
        default=None,
    )
    selector.add_argument(
        "--submission-hash",
        default=None,
    )

    parser.add_argument(
        "--a",
        dest="a_score",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--b",
        dest="b_score",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--c",
        dest="c_score",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--d",
        dest="d_score",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--e",
        dest="e_score",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--reviewer-id",
        required=True,
    )
    parser.add_argument(
        "--reviewed-at",
        required=True,
        help=(
            "Timezone-aware ISO-8601 timestamp, "
            "for example "
            "2026-07-18T12:00:00+09:00"
        ),
    )
    parser.add_argument(
        "--review-method",
        choices=FINAL_REVIEW_METHODS,
        required=True,
    )
    parser.add_argument(
        "--adjudication-status",
        choices=FINAL_ADJUDICATION_STATUSES,
        default="reviewed",
    )

    args = parser.parse_args()

    try:
        result = review_record_in_dataset(
            args.dataset_jsonl,
            record_id=args.record_id,
            submission_hash=(
                args.submission_hash
            ),
            a_score=args.a_score,
            b_score=args.b_score,
            c_score=args.c_score,
            d_score=args.d_score,
            e_score=args.e_score,
            reviewer_id=args.reviewer_id,
            reviewed_at=args.reviewed_at,
            review_method=args.review_method,
            adjudication_status=(
                args.adjudication_status
            ),
        )
    except (
        CalibrationContractError,
        ExpertCalibrationReviewError,
        OSError,
    ) as error:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(error),
                    "calibration_ready": False,
                    "production_calibration_enabled": (
                        False
                    ),
                    "score_effect": "none",
                    "direct_score_application": (
                        False
                    ),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
