from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import statistics
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Iterable

from expert_calibration_dataset import (
    CalibrationContractError,
    DIRECT_SCORE_APPLICATION,
    PRODUCTION_CALIBRATION_ENABLED,
    SCORE_EFFECT,
    deterministic_dataset_split,
    load_jsonl,
    validate_dataset,
)


REPORT_VERSION = "expert_calibration_report_v1"
INCLUDED_STATUSES = frozenset(
    {
        "reviewed",
        "adjudicated",
    }
)
EXCLUDED_METRIC_STATUSES = frozenset(
    {
        "draft",
        "excluded",
    }
)
LAYERS = ("A", "B", "C", "D", "E")


class ExpertCalibrationReportError(ValueError):
    pass


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _source_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise ExpertCalibrationReportError(
            f"unable to read source dataset: {error}"
        ) from error


def _external_output_path(
    path: str | Path,
    *,
    source_path: Path,
) -> Path:
    output = Path(path).expanduser().resolve()
    source = source_path.expanduser().resolve()

    if output == source:
        raise ExpertCalibrationReportError(
            "report output must not replace source dataset"
        )

    repository_root = Path(__file__).resolve().parents[1]
    sessions_root = (
        repository_root
        / "data"
        / "sessions"
    ).resolve()

    try:
        output.relative_to(sessions_root)
    except ValueError:
        pass
    else:
        raise ExpertCalibrationReportError(
            "report output must not be under data/sessions"
        )

    return output


def _atomic_write_text(
    path: Path,
    text: str,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(
            temporary_path,
            path,
        )
    except OSError as error:
        if (
            temporary_path is not None
            and temporary_path.exists()
        ):
            temporary_path.unlink(
                missing_ok=True
            )

        raise ExpertCalibrationReportError(
            f"unable to write report: {error}"
        ) from error


def _empty_metrics() -> dict[str, Any]:
    return {
        "count": 0,
        "model_mean": None,
        "expert_mean": None,
        "bias_model_minus_expert": None,
        "mae": None,
        "rmse": None,
        "max_absolute_error": None,
    }


def compute_pair_metrics(
    pairs: Iterable[tuple[float, float]],
) -> dict[str, Any]:
    normalized = [
        (
            float(model_value),
            float(expert_value),
        )
        for model_value, expert_value in pairs
    ]

    if not normalized:
        return _empty_metrics()

    errors = [
        model_value - expert_value
        for model_value, expert_value
        in normalized
    ]
    absolute_errors = [
        abs(error)
        for error in errors
    ]

    return {
        "count": len(normalized),
        "model_mean": statistics.fmean(
            model_value
            for model_value, _
            in normalized
        ),
        "expert_mean": statistics.fmean(
            expert_value
            for _, expert_value
            in normalized
        ),
        "bias_model_minus_expert": (
            statistics.fmean(errors)
        ),
        "mae": statistics.fmean(
            absolute_errors
        ),
        "rmse": math.sqrt(
            statistics.fmean(
                error * error
                for error in errors
            )
        ),
        "max_absolute_error": max(
            absolute_errors
        ),
    }


def _record_metrics(
    records: Iterable[dict[str, Any]],
    *,
    model_getter: Callable[
        [dict[str, Any]],
        float,
    ],
    expert_getter: Callable[
        [dict[str, Any]],
        float,
    ],
) -> dict[str, Any]:
    return compute_pair_metrics(
        (
            model_getter(record),
            expert_getter(record),
        )
        for record in records
    )


def _group_total_metrics(
    records: Iterable[dict[str, Any]],
    *,
    field: str,
) -> dict[str, dict[str, Any]]:
    groups: dict[
        str,
        list[dict[str, Any]],
    ] = defaultdict(list)

    for record in records:
        groups[str(record[field])].append(record)

    return {
        key: _record_metrics(
            groups[key],
            model_getter=lambda record: (
                record["model_total_score"]
            ),
            expert_getter=lambda record: (
                record["expert_total_score"]
            ),
        )
        for key in sorted(groups)
    }


def _layer_metrics(
    records: Iterable[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    materialized = list(records)

    return {
        layer: _record_metrics(
            materialized,
            model_getter=(
                lambda record, key=layer: (
                    record[
                        "model_breakdown"
                    ][key]
                )
            ),
            expert_getter=(
                lambda record, key=layer: (
                    record[
                        "expert_breakdown"
                    ][key]
                )
            ),
        )
        for layer in LAYERS
    }


def build_calibration_report(
    records: Iterable[dict[str, Any]],
    *,
    dataset_path: str | Path,
    source_sha256: str,
    holdout_percent: int = 20,
) -> dict[str, Any]:
    materialized = list(records)
    dataset_report = validate_dataset(
        materialized,
        require_finalized=False,
    )

    status_counts = Counter(
        str(record["adjudication_status"])
        for record in materialized
    )
    analyzed_records = [
        record
        for record in materialized
        if record["adjudication_status"]
        in INCLUDED_STATUSES
    ]

    split_records = {
        "train": [],
        "holdout": [],
    }

    for record in analyzed_records:
        split_name = deterministic_dataset_split(
            record["submission_hash"],
            holdout_percent=holdout_percent,
        )
        split_records[split_name].append(record)

    total_metrics = _record_metrics(
        analyzed_records,
        model_getter=lambda record: (
            record["model_total_score"]
        ),
        expert_getter=lambda record: (
            record["expert_total_score"]
        ),
    )

    dataset_summary = {
        key: value
        for key, value
        in dataset_report.items()
        if key != "records"
    }
    dataset_summary.update(
        {
            "status_counts": {
                key: status_counts[key]
                for key in sorted(status_counts)
            },
            "analyzed_record_count": len(
                analyzed_records
            ),
            "metric_excluded_record_count": (
                len(materialized)
                - len(analyzed_records)
            ),
            "holdout_percent": holdout_percent,
            "train_record_count": len(
                split_records["train"]
            ),
            "holdout_record_count": len(
                split_records["holdout"]
            ),
        }
    )

    return {
        "version": REPORT_VERSION,
        "dataset": {
            "path": str(
                Path(dataset_path)
                .expanduser()
                .resolve()
            ),
            "sha256": source_sha256,
            "summary": dataset_summary,
        },
        "metric_policy": {
            "error_direction": (
                "model_minus_expert"
            ),
            "included_statuses": sorted(
                INCLUDED_STATUSES
            ),
            "excluded_statuses": sorted(
                EXCLUDED_METRIC_STATUSES
            ),
            "json_precision": (
                "native floating-point"
            ),
            "markdown_precision": 4,
        },
        "metrics": {
            "overall_total_score": (
                total_metrics
            ),
            "layers": _layer_metrics(
                analyzed_records
            ),
            "splits": {
                name: _record_metrics(
                    split_records[name],
                    model_getter=(
                        lambda record: (
                            record[
                                "model_total_score"
                            ]
                        )
                    ),
                    expert_getter=(
                        lambda record: (
                            record[
                                "expert_total_score"
                            ]
                        )
                    ),
                )
                for name in (
                    "train",
                    "holdout",
                )
            },
            "by_topic_id": (
                _group_total_metrics(
                    analyzed_records,
                    field="topic_id",
                )
            ),
            "by_question_type": (
                _group_total_metrics(
                    analyzed_records,
                    field="question_type",
                )
            ),
        },
        "readiness": {
            "report_generation_ready": True,
            "diagnostic_metrics_available": (
                bool(analyzed_records)
            ),
            "analysis_ready": False,
            "analysis_reason": (
                "No approved minimum expert-label "
                "or holdout threshold is defined."
            ),
            "calibration_ready": False,
        },
        "production_policy": {
            "production_calibration_enabled": (
                PRODUCTION_CALIBRATION_ENABLED
            ),
            "score_effect": SCORE_EFFECT,
            "direct_score_application": (
                DIRECT_SCORE_APPLICATION
            ),
        },
        "source_dataset_unchanged": True,
    }


def _format_metric(
    value: Any,
) -> str:
    if value is None:
        return "N/A"

    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        return f"{value:.4f}"

    return str(value)


def _escape_markdown(value: Any) -> str:
    return (
        str(value)
        .replace("|", r"\|")
        .replace("\n", " ")
    )


def _metric_table(
    rows: Iterable[
        tuple[str, dict[str, Any]]
    ],
) -> list[str]:
    output = [
        (
            "| Scope | Count | Model mean | "
            "Expert mean | Bias | MAE | "
            "RMSE | Max abs error |"
        ),
        (
            "|---|---:|---:|---:|---:|---:|"
            "---:|---:|"
        ),
    ]

    for label, metrics in rows:
        output.append(
            "| "
            + _escape_markdown(label)
            + " | "
            + " | ".join(
                _format_metric(
                    metrics[field]
                )
                for field in (
                    "count",
                    "model_mean",
                    "expert_mean",
                    "bias_model_minus_expert",
                    "mae",
                    "rmse",
                    "max_absolute_error",
                )
            )
            + " |"
        )

    return output


def render_markdown(
    report: dict[str, Any],
) -> str:
    summary = report["dataset"]["summary"]
    metrics = report["metrics"]
    readiness = report["readiness"]
    policy = report["production_policy"]

    lines = [
        "# Expert Calibration Diagnostic Report",
        "",
        f"- Report version: `{report['version']}`",
        (
            "- Source dataset: `"
            + report["dataset"]["path"]
            + "`"
        ),
        (
            "- Source SHA-256: `"
            + report["dataset"]["sha256"]
            + "`"
        ),
        (
            "- Source dataset unchanged: `"
            + str(
                report[
                    "source_dataset_unchanged"
                ]
            ).lower()
            + "`"
        ),
        "",
        "## Dataset Summary",
        "",
        (
            f"- Records: "
            f"{summary['record_count']}"
        ),
        (
            f"- Analyzed records: "
            f"{summary['analyzed_record_count']}"
        ),
        (
            f"- Excluded from metrics: "
            f"{summary['metric_excluded_record_count']}"
        ),
        (
            f"- Train records: "
            f"{summary['train_record_count']}"
        ),
        (
            f"- Holdout records: "
            f"{summary['holdout_record_count']}"
        ),
        (
            f"- Holdout percent: "
            f"{summary['holdout_percent']}%"
        ),
        "",
        "### Status Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]

    for status, count in (
        summary["status_counts"].items()
    ):
        lines.append(
            f"| {_escape_markdown(status)} | "
            f"{count} |"
        )

    lines.extend(
        [
            "",
            "## Total Score Metrics",
            "",
        ]
    )
    lines.extend(
        _metric_table(
            [
                (
                    "overall",
                    metrics[
                        "overall_total_score"
                    ],
                ),
                (
                    "train",
                    metrics["splits"]["train"],
                ),
                (
                    "holdout",
                    metrics[
                        "splits"
                    ]["holdout"],
                ),
            ]
        )
    )

    lines.extend(
        [
            "",
            "## Layer Metrics",
            "",
        ]
    )
    lines.extend(
        _metric_table(
            (
                layer,
                metrics["layers"][layer],
            )
            for layer in LAYERS
        )
    )

    lines.extend(
        [
            "",
            "## Topic Metrics",
            "",
        ]
    )
    lines.extend(
        _metric_table(
            metrics[
                "by_topic_id"
            ].items()
        )
    )

    lines.extend(
        [
            "",
            "## Question Type Metrics",
            "",
        ]
    )
    lines.extend(
        _metric_table(
            metrics[
                "by_question_type"
            ].items()
        )
    )

    lines.extend(
        [
            "",
            "## Readiness",
            "",
            (
                "- Diagnostic metrics available: `"
                + str(
                    readiness[
                        "diagnostic_metrics_available"
                    ]
                ).lower()
                + "`"
            ),
            (
                "- Analysis ready: `"
                + str(
                    readiness["analysis_ready"]
                ).lower()
                + "`"
            ),
            (
                "- Calibration ready: `"
                + str(
                    readiness[
                        "calibration_ready"
                    ]
                ).lower()
                + "`"
            ),
            (
                "- Reason: "
                + readiness["analysis_reason"]
            ),
            "",
            "## Production Policy",
            "",
            (
                "- Production calibration enabled: `"
                + str(
                    policy[
                        "production_calibration_enabled"
                    ]
                ).lower()
                + "`"
            ),
            (
                "- Score effect: `"
                + policy["score_effect"]
                + "`"
            ),
            (
                "- Direct score application: `"
                + str(
                    policy[
                        "direct_score_application"
                    ]
                ).lower()
                + "`"
            ),
            "",
        ]
    )

    return "\n".join(lines)


def generate_report_files(
    dataset_path: str | Path,
    json_output_path: str | Path,
    markdown_output_path: str | Path,
    *,
    holdout_percent: int = 20,
) -> dict[str, Any]:
    source_path = (
        Path(dataset_path)
        .expanduser()
        .resolve()
    )
    json_path = _external_output_path(
        json_output_path,
        source_path=source_path,
    )
    markdown_path = _external_output_path(
        markdown_output_path,
        source_path=source_path,
    )

    if json_path == markdown_path:
        raise ExpertCalibrationReportError(
            "JSON and Markdown output paths "
            "must be different"
        )

    before_bytes = _source_bytes(source_path)
    records = load_jsonl(source_path)
    after_load_bytes = _source_bytes(
        source_path
    )

    if after_load_bytes != before_bytes:
        raise ExpertCalibrationReportError(
            "source dataset changed while loading"
        )

    report = build_calibration_report(
        records,
        dataset_path=source_path,
        source_sha256=_sha256_bytes(
            before_bytes
        ),
        holdout_percent=holdout_percent,
    )

    json_text = json.dumps(
        report,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    markdown_text = (
        render_markdown(report)
    )

    try:
        _atomic_write_text(
            json_path,
            json_text,
        )
        _atomic_write_text(
            markdown_path,
            markdown_text,
        )

        after_output_bytes = _source_bytes(
            source_path
        )

        if after_output_bytes != before_bytes:
            raise ExpertCalibrationReportError(
                "source dataset changed while "
                "writing reports"
            )
    except Exception:
        json_path.unlink(
            missing_ok=True
        )
        markdown_path.unlink(
            missing_ok=True
        )
        raise

    return {
        "ok": True,
        "dataset_path": str(source_path),
        "json_output_path": str(json_path),
        "markdown_output_path": (
            str(markdown_path)
        ),
        "report": report,
        "source_dataset_unchanged": True,
        "calibration_ready": False,
        "production_calibration_enabled": (
            PRODUCTION_CALIBRATION_ENABLED
        ),
        "score_effect": SCORE_EFFECT,
        "direct_score_application": (
            DIRECT_SCORE_APPLICATION
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate diagnostic JSON and "
            "Markdown reports from an external "
            "expert calibration JSONL dataset."
        )
    )
    parser.add_argument(
        "dataset_jsonl",
        type=Path,
    )
    parser.add_argument(
        "json_output",
        type=Path,
    )
    parser.add_argument(
        "markdown_output",
        type=Path,
    )
    parser.add_argument(
        "--holdout-percent",
        type=int,
        default=20,
    )

    args = parser.parse_args()

    try:
        result = generate_report_files(
            args.dataset_jsonl,
            args.json_output,
            args.markdown_output,
            holdout_percent=(
                args.holdout_percent
            ),
        )
    except (
        CalibrationContractError,
        ExpertCalibrationReportError,
        OSError,
        ValueError,
    ) as error:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(error),
                    "calibration_ready": False,
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
