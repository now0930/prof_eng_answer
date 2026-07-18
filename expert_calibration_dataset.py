from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from grading_identity import build_grading_identity


RECORD_VERSION = "expert_calibration_record_v1"
DATASET_VERSION = "expert_calibration_dataset_v1"

PRODUCTION_CALIBRATION_ENABLED = False
SCORE_EFFECT = "none"
DIRECT_SCORE_APPLICATION = False

TOTAL_MAX = 25.0
TOLERANCE = 0.05

LAYER_MAX = {
    "A": 3.0,
    "B": 6.0,
    "C": 8.0,
    "D": 6.0,
    "E": 2.0,
}

FINAL_STATUSES = {
    "reviewed",
    "adjudicated",
}

ALLOWED_STATUSES = {
    "draft",
    "reviewed",
    "adjudicated",
    "excluded",
}

ALLOWED_METHODS = {
    "pending",
    "single_expert",
    "dual_expert",
    "panel_adjudication",
    "official_exam_score",
}

REQUIRED_FIELDS = {
    "version",
    "record_id",
    "question_text",
    "answer_text",
    "question_hash",
    "submission_hash",
    "topic_id",
    "question_type",
    "rubric_snapshot_hash",
    "model_total_score",
    "model_breakdown",
    "expert_total_score",
    "expert_breakdown",
    "reviewer_id",
    "reviewed_at",
    "review_method",
    "adjudication_status",
    "notes",
    "score_effect",
    "direct_score_application",
    "record_hash",
}


class CalibrationContractError(ValueError):
    pass


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _sha256(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()


def _required_text(
    value: Any,
    field: str,
) -> str:
    result = str(value or "").strip()

    if not result:
        raise CalibrationContractError(
            f"{field} must not be empty"
        )

    return result


def _finite_number(
    value: Any,
    field: str,
) -> float:
    if isinstance(value, bool):
        raise CalibrationContractError(
            f"{field} must be numeric"
        )

    try:
        result = float(value)
    except (TypeError, ValueError) as error:
        raise CalibrationContractError(
            f"{field} must be numeric"
        ) from error

    if not math.isfinite(result):
        raise CalibrationContractError(
            f"{field} must be finite"
        )

    return result


def _sha256_hash(
    value: Any,
    field: str,
) -> str:
    result = str(value or "").strip().lower()

    if (
        len(result) != 64
        or any(
            char not in "0123456789abcdef"
            for char in result
        )
    ):
        raise CalibrationContractError(
            f"{field} must be a lowercase "
            "SHA-256 digest"
        )

    return result


def _reviewed_at(
    value: Any,
    *,
    required: bool,
) -> str | None:
    if value in {None, ""}:
        if required:
            raise CalibrationContractError(
                "reviewed_at is required"
            )

        return None

    result = str(value).strip()
    candidate = (
        result[:-1] + "+00:00"
        if result.endswith("Z")
        else result
    )

    try:
        parsed = datetime.fromisoformat(
            candidate
        )
    except ValueError as error:
        raise CalibrationContractError(
            "reviewed_at must be ISO-8601"
        ) from error

    if parsed.tzinfo is None:
        raise CalibrationContractError(
            "reviewed_at must include timezone"
        )

    return result


def normalize_breakdown(
    value: Any,
    field: str,
) -> dict[str, float]:
    if not isinstance(value, dict):
        raise CalibrationContractError(
            f"{field} must be an object"
        )

    if set(value) != set(LAYER_MAX):
        raise CalibrationContractError(
            f"{field} must contain exactly "
            "A/B/C/D/E"
        )

    output = {}

    for layer, maximum in LAYER_MAX.items():
        raw_score = value[layer]

        if isinstance(raw_score, dict):
            if "score" not in raw_score:
                raise CalibrationContractError(
                    f"{field}.{layer} has no score"
                )

            raw_score = raw_score["score"]

        score = _finite_number(
            raw_score,
            f"{field}.{layer}",
        )

        if (
            score < -TOLERANCE
            or score > maximum + TOLERANCE
        ):
            raise CalibrationContractError(
                f"{field}.{layer} outside "
                f"0..{maximum}"
            )

        output[layer] = round(
            min(
                max(score, 0.0),
                maximum,
            ),
            4,
        )

    return output


def breakdown_total(
    value: dict[str, float],
) -> float:
    return round(
        sum(
            value[layer]
            for layer in LAYER_MAX
        ),
        4,
    )


def _normalized_payload(
    record: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise CalibrationContractError(
            "record must be an object"
        )

    missing = sorted(
        (
            REQUIRED_FIELDS
            - {"record_hash"}
        )
        - set(record)
    )

    if missing:
        raise CalibrationContractError(
            "missing fields: "
            + ", ".join(missing)
        )

    output = copy.deepcopy(record)
    output.pop("record_hash", None)

    if output["version"] != RECORD_VERSION:
        raise CalibrationContractError(
            "unsupported record version"
        )

    for field in (
        "record_id",
        "question_text",
        "answer_text",
        "topic_id",
        "question_type",
    ):
        output[field] = _required_text(
            output[field],
            field,
        )

    output["question_hash"] = (
        _sha256_hash(
            output["question_hash"],
            "question_hash",
        )
    )
    output["submission_hash"] = (
        _sha256_hash(
            output["submission_hash"],
            "submission_hash",
        )
    )
    output["rubric_snapshot_hash"] = (
        _sha256_hash(
            output["rubric_snapshot_hash"],
            "rubric_snapshot_hash",
        )
    )

    identity = build_grading_identity(
        question_text=(
            output["question_text"]
        ),
        answer_text=(
            output["answer_text"]
        ),
    ).to_dict()

    if (
        output["question_hash"]
        != identity["question_hash"]
    ):
        raise CalibrationContractError(
            "question_hash mismatch"
        )

    if (
        output["submission_hash"]
        != identity["submission_hash"]
    ):
        raise CalibrationContractError(
            "submission_hash mismatch"
        )

    model_total = _finite_number(
        output["model_total_score"],
        "model_total_score",
    )

    if not (
        -TOLERANCE
        <= model_total
        <= TOTAL_MAX + TOLERANCE
    ):
        raise CalibrationContractError(
            "model_total_score outside 0..25"
        )

    model_breakdown = normalize_breakdown(
        output["model_breakdown"],
        "model_breakdown",
    )

    model_total = round(
        min(
            max(model_total, 0.0),
            TOTAL_MAX,
        ),
        4,
    )

    if (
        model_total
        > breakdown_total(
            model_breakdown
        )
        + TOLERANCE
    ):
        raise CalibrationContractError(
            "model_total_score exceeds "
            "model_breakdown sum"
        )

    output["model_total_score"] = model_total
    output["model_breakdown"] = (
        model_breakdown
    )

    status = _required_text(
        output["adjudication_status"],
        "adjudication_status",
    )

    if status not in ALLOWED_STATUSES:
        raise CalibrationContractError(
            "unsupported adjudication_status"
        )

    method = _required_text(
        output["review_method"],
        "review_method",
    )

    if method not in ALLOWED_METHODS:
        raise CalibrationContractError(
            "unsupported review_method"
        )

    output["adjudication_status"] = status
    output["review_method"] = method

    if status in FINAL_STATUSES:
        expert_total = _finite_number(
            output["expert_total_score"],
            "expert_total_score",
        )

        if not (
            -TOLERANCE
            <= expert_total
            <= TOTAL_MAX + TOLERANCE
        ):
            raise CalibrationContractError(
                "expert_total_score outside 0..25"
            )

        expert_breakdown = (
            normalize_breakdown(
                output["expert_breakdown"],
                "expert_breakdown",
            )
        )
        expert_total = round(
            min(
                max(expert_total, 0.0),
                TOTAL_MAX,
            ),
            4,
        )

        if abs(
            expert_total
            - breakdown_total(
                expert_breakdown
            )
        ) > TOLERANCE:
            raise CalibrationContractError(
                "expert_total_score must equal "
                "expert_breakdown sum"
            )

        if method == "pending":
            raise CalibrationContractError(
                "finalized record cannot use "
                "review_method=pending"
            )

        output["expert_total_score"] = (
            expert_total
        )
        output["expert_breakdown"] = (
            expert_breakdown
        )
        output["reviewer_id"] = (
            _required_text(
                output["reviewer_id"],
                "reviewer_id",
            )
        )
        output["reviewed_at"] = (
            _reviewed_at(
                output["reviewed_at"],
                required=True,
            )
        )

    else:
        if (
            output["expert_total_score"]
            is not None
        ):
            raise CalibrationContractError(
                "non-final record cannot contain "
                "expert_total_score"
            )

        if (
            output["expert_breakdown"]
            is not None
        ):
            raise CalibrationContractError(
                "non-final record cannot contain "
                "expert_breakdown"
            )

        if (
            status == "draft"
            and method != "pending"
        ):
            raise CalibrationContractError(
                "draft record must use "
                "review_method=pending"
            )

        output["expert_total_score"] = None
        output["expert_breakdown"] = None
        output["reviewer_id"] = str(
            output["reviewer_id"] or ""
        ).strip()
        output["reviewed_at"] = _reviewed_at(
            output["reviewed_at"],
            required=False,
        )

    output["notes"] = str(
        output["notes"] or ""
    )

    if output["score_effect"] != SCORE_EFFECT:
        raise CalibrationContractError(
            "score_effect must be none"
        )

    if (
        output[
            "direct_score_application"
        ]
        is not False
    ):
        raise CalibrationContractError(
            "direct_score_application "
            "must be false"
        )

    return output


def with_record_hash(
    record: dict[str, Any],
) -> dict[str, Any]:
    output = _normalized_payload(record)
    output["record_hash"] = _sha256(output)

    return output


def validate_record(
    record: dict[str, Any],
    *,
    require_finalized: bool = False,
) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise CalibrationContractError(
            "record must be an object"
        )

    missing = sorted(
        REQUIRED_FIELDS - set(record)
    )

    if missing:
        raise CalibrationContractError(
            "missing fields: "
            + ", ".join(missing)
        )

    supplied_hash = _sha256_hash(
        record["record_hash"],
        "record_hash",
    )
    output = _normalized_payload(record)
    expected_hash = _sha256(output)

    if supplied_hash != expected_hash:
        raise CalibrationContractError(
            "record_hash mismatch"
        )

    output["record_hash"] = supplied_hash

    if (
        require_finalized
        and output[
            "adjudication_status"
        ]
        not in FINAL_STATUSES
    ):
        raise CalibrationContractError(
            "finalized record required"
        )

    return output


def build_draft_record(
    *,
    record_id: str | None,
    question_text: str,
    answer_text: str,
    topic_id: str,
    question_type: str,
    rubric_snapshot_hash: str,
    model_total_score: float,
    model_breakdown: dict[str, Any],
    notes: str = "",
) -> dict[str, Any]:
    identity = build_grading_identity(
        question_text=question_text,
        answer_text=answer_text,
    ).to_dict()

    record = {
        "version": RECORD_VERSION,
        "record_id": (
            record_id
            or (
                "expert-"
                + identity[
                    "submission_hash"
                ][:16]
            )
        ),
        "question_text": question_text,
        "answer_text": answer_text,
        "question_hash": (
            identity["question_hash"]
        ),
        "submission_hash": (
            identity["submission_hash"]
        ),
        "topic_id": topic_id,
        "question_type": question_type,
        "rubric_snapshot_hash": (
            rubric_snapshot_hash
        ),
        "model_total_score": (
            model_total_score
        ),
        "model_breakdown": (
            copy.deepcopy(
                model_breakdown
            )
        ),
        "expert_total_score": None,
        "expert_breakdown": None,
        "reviewer_id": "",
        "reviewed_at": None,
        "review_method": "pending",
        "adjudication_status": "draft",
        "notes": notes,
        "score_effect": SCORE_EFFECT,
        "direct_score_application": (
            DIRECT_SCORE_APPLICATION
        ),
    }

    return with_record_hash(record)


def finalize_record(
    record: dict[str, Any],
    *,
    expert_total_score: float,
    expert_breakdown: dict[str, Any],
    reviewer_id: str,
    reviewed_at: str,
    review_method: str,
    adjudication_status: str = (
        "reviewed"
    ),
) -> dict[str, Any]:
    output = validate_record(record)
    output.pop("record_hash", None)
    output["expert_total_score"] = (
        expert_total_score
    )
    output["expert_breakdown"] = (
        copy.deepcopy(
            expert_breakdown
        )
    )
    output["reviewer_id"] = reviewer_id
    output["reviewed_at"] = reviewed_at
    output["review_method"] = review_method
    output["adjudication_status"] = (
        adjudication_status
    )

    return validate_record(
        with_record_hash(output),
        require_finalized=True,
    )


def deterministic_dataset_split(
    submission_hash: str,
    *,
    holdout_percent: int = 20,
) -> str:
    digest = _sha256_hash(
        submission_hash,
        "submission_hash",
    )

    if not 1 <= holdout_percent <= 99:
        raise CalibrationContractError(
            "holdout_percent outside 1..99"
        )

    bucket = int(digest[:8], 16) % 100

    return (
        "holdout"
        if bucket < holdout_percent
        else "train"
    )


def validate_dataset(
    records: Iterable[
        dict[str, Any]
    ],
    *,
    require_finalized: bool = False,
) -> dict[str, Any]:
    normalized = []
    record_ids = set()
    submission_hashes = set()
    question_hashes = set()

    for index, record in enumerate(
        records,
        start=1,
    ):
        try:
            validated = validate_record(
                record,
                require_finalized=(
                    require_finalized
                ),
            )
        except CalibrationContractError as error:
            raise CalibrationContractError(
                f"record {index}: {error}"
            ) from error

        if (
            validated["record_id"]
            in record_ids
        ):
            raise CalibrationContractError(
                "duplicate record_id"
            )

        if (
            validated["submission_hash"]
            in submission_hashes
        ):
            raise CalibrationContractError(
                "duplicate submission_hash"
            )

        record_ids.add(
            validated["record_id"]
        )
        submission_hashes.add(
            validated["submission_hash"]
        )
        question_hashes.add(
            validated["question_hash"]
        )
        normalized.append(validated)

    finalized_count = sum(
        record["adjudication_status"]
        in FINAL_STATUSES
        for record in normalized
    )

    return {
        "version": DATASET_VERSION,
        "record_count": len(normalized),
        "finalized_record_count": (
            finalized_count
        ),
        "unique_question_count": len(
            question_hashes
        ),
        "unique_submission_count": len(
            submission_hashes
        ),
        "calibration_ready": False,
        "production_calibration_enabled": (
            PRODUCTION_CALIBRATION_ENABLED
        ),
        "score_effect": SCORE_EFFECT,
        "direct_score_application": (
            DIRECT_SCORE_APPLICATION
        ),
        "records": normalized,
    }


def _external_path(
    path: str | Path,
) -> Path:
    target = Path(path).expanduser().resolve()
    sessions = (
        Path.cwd()
        / "data"
        / "sessions"
    ).resolve()

    try:
        target.relative_to(sessions)
    except ValueError:
        return target

    raise CalibrationContractError(
        "expert dataset must not be stored "
        "under data/sessions"
    )


def write_jsonl_atomic(
    path: str | Path,
    records: Iterable[
        dict[str, Any]
    ],
    *,
    require_finalized: bool = False,
) -> dict[str, Any]:
    target = _external_path(path)
    report = validate_dataset(
        records,
        require_finalized=(
            require_finalized
        ),
    )
    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    descriptor, temporary_name = (
        tempfile.mkstemp(
            prefix=target.name + ".",
            suffix=".tmp",
            dir=str(target.parent),
        )
    )
    temporary = Path(temporary_name)

    try:
        with os.fdopen(
            descriptor,
            "w",
            encoding="utf-8",
        ) as handle:
            for record in report["records"]:
                handle.write(
                    _canonical_json(record)
                    + "\n"
                )

            handle.flush()
            os.fsync(handle.fileno())

        temporary.replace(target)

    except Exception:
        temporary.unlink(
            missing_ok=True
        )
        raise

    return {
        key: value
        for key, value in report.items()
        if key != "records"
    }


def load_jsonl(
    path: str | Path,
) -> list[dict[str, Any]]:
    source = _external_path(path)
    records = []

    with source.open(
        "r",
        encoding="utf-8",
    ) as handle:
        for line_number, line in enumerate(
            handle,
            start=1,
        ):
            if not line.strip():
                continue

            try:
                value = json.loads(line)
            except json.JSONDecodeError as error:
                raise CalibrationContractError(
                    f"line {line_number}: "
                    "invalid JSON"
                ) from error

            if not isinstance(value, dict):
                raise CalibrationContractError(
                    f"line {line_number}: "
                    "record must be object"
                )

            records.append(value)

    return records
