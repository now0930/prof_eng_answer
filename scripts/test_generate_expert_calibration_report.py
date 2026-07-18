from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from expert_calibration_dataset import (
    build_draft_record,
    deterministic_dataset_split,
    finalize_record,
    load_jsonl,
    validate_record,
    with_record_hash,
    write_jsonl_atomic,
)
from generate_expert_calibration_report import (
    ExpertCalibrationReportError,
    build_calibration_report,
    compute_pair_metrics,
    generate_report_files,
)


def make_record(
    *,
    index: int,
    status: str = "reviewed",
    topic_id: str = "topic_a",
    question_type: str = (
        "PRINCIPLE_INTERPRETATION"
    ),
    model_breakdown: (
        dict[str, float] | None
    ) = None,
    expert_breakdown: (
        dict[str, float] | None
    ) = None,
) -> dict:
    model_values = model_breakdown or {
        "A": 1.0,
        "B": 2.0,
        "C": 2.0,
        "D": 2.0,
        "E": 1.0,
    }
    expert_values = expert_breakdown or {
        "A": 1.5,
        "B": 2.5,
        "C": 2.5,
        "D": 2.0,
        "E": 1.0,
    }

    draft = build_draft_record(
        record_id=f"report-record-{index}",
        question_text=f"보고서 문제 {index}",
        answer_text=f"보고서 답안 {index}",
        topic_id=topic_id,
        question_type=question_type,
        rubric_snapshot_hash=(
            f"{index + 1:064x}"[-64:]
        ),
        model_total_score=round(
            sum(model_values.values()),
            10,
        ),
        model_breakdown=model_values,
        notes=f"notes-{index}",
    )

    if status == "draft":
        return draft

    if status == "excluded":
        excluded = dict(draft)
        excluded["adjudication_status"] = (
            "excluded"
        )
        excluded = with_record_hash(excluded)
        validate_record(excluded)
        return excluded

    return finalize_record(
        draft,
        expert_total_score=round(
            sum(expert_values.values()),
            10,
        ),
        expert_breakdown=expert_values,
        reviewer_id="expert",
        reviewed_at=(
            "2026-07-18T12:00:00+09:00"
        ),
        review_method=(
            "panel_adjudication"
            if status == "adjudicated"
            else "single_expert"
        ),
        adjudication_status=status,
    )


class OfflineCalibrationReportTests(
    unittest.TestCase
):
    def write_dataset(
        self,
        root: Path,
        records: list[dict],
    ) -> Path:
        path = root / "expert_dataset.jsonl"
        write_jsonl_atomic(path, records)
        return path

    def test_empty_dataset_report(self):
        report = build_calibration_report(
            [],
            dataset_path="/tmp/empty.jsonl",
            source_sha256="0" * 64,
        )

        self.assertEqual(
            report["dataset"]["summary"][
                "record_count"
            ],
            0,
        )
        self.assertEqual(
            report["metrics"][
                "overall_total_score"
            ]["count"],
            0,
        )
        self.assertIsNone(
            report["metrics"][
                "overall_total_score"
            ]["mae"]
        )

    def test_draft_only_dataset_report(self):
        record = make_record(
            index=1,
            status="draft",
        )
        report = build_calibration_report(
            [record],
            dataset_path="/tmp/draft.jsonl",
            source_sha256="1" * 64,
        )

        self.assertEqual(
            report["dataset"]["summary"][
                "analyzed_record_count"
            ],
            0,
        )
        self.assertFalse(
            report["readiness"][
                "diagnostic_metrics_available"
            ]
        )

    def test_finalized_overall_metrics(self):
        pairs = [
            (8.0, 9.0),
            (10.0, 11.5),
            (12.0, 11.0),
            (14.0, 15.0),
        ]
        metrics = compute_pair_metrics(pairs)

        self.assertEqual(
            metrics["count"],
            4,
        )
        self.assertAlmostEqual(
            metrics[
                "bias_model_minus_expert"
            ],
            -0.625,
        )
        self.assertAlmostEqual(
            metrics["mae"],
            1.125,
        )
        self.assertAlmostEqual(
            metrics["rmse"],
            1.14564392373896,
        )

    def test_layer_metrics(self):
        record = make_record(
            index=2,
            model_breakdown={
                "A": 1.0,
                "B": 2.0,
                "C": 3.0,
                "D": 2.0,
                "E": 1.0,
            },
            expert_breakdown={
                "A": 1.5,
                "B": 2.5,
                "C": 4.0,
                "D": 2.0,
                "E": 1.0,
            },
        )
        report = build_calibration_report(
            [record],
            dataset_path="/tmp/layer.jsonl",
            source_sha256="2" * 64,
        )

        self.assertEqual(
            report["metrics"]["layers"][
                "C"
            ]["mae"],
            1.0,
        )
        self.assertEqual(
            report["metrics"]["layers"][
                "D"
            ][
                "bias_model_minus_expert"
            ],
            0.0,
        )

    def test_deterministic_split_metrics(self):
        records = [
            make_record(index=index + 10)
            for index in range(40)
        ]
        report = build_calibration_report(
            records,
            dataset_path="/tmp/split.jsonl",
            source_sha256="3" * 64,
        )
        summary = report[
            "dataset"
        ]["summary"]

        expected = {
            "train": 0,
            "holdout": 0,
        }

        for record in records:
            expected[
                deterministic_dataset_split(
                    record["submission_hash"]
                )
            ] += 1

        self.assertEqual(
            summary["train_record_count"],
            expected["train"],
        )
        self.assertEqual(
            summary["holdout_record_count"],
            expected["holdout"],
        )
        self.assertGreater(
            expected["train"],
            0,
        )
        self.assertGreater(
            expected["holdout"],
            0,
        )

    def test_topic_grouping(self):
        records = [
            make_record(
                index=50,
                topic_id="topic_a",
            ),
            make_record(
                index=51,
                topic_id="topic_b",
            ),
            make_record(
                index=52,
                topic_id="topic_a",
            ),
        ]
        report = build_calibration_report(
            records,
            dataset_path="/tmp/topic.jsonl",
            source_sha256="4" * 64,
        )

        self.assertEqual(
            report["metrics"][
                "by_topic_id"
            ]["topic_a"]["count"],
            2,
        )
        self.assertEqual(
            report["metrics"][
                "by_topic_id"
            ]["topic_b"]["count"],
            1,
        )

    def test_question_type_grouping(self):
        records = [
            make_record(
                index=60,
                question_type=(
                    "COMPARE_SELECTION"
                ),
            ),
            make_record(
                index=61,
                question_type=(
                    "PRINCIPLE_INTERPRETATION"
                ),
            ),
        ]
        report = build_calibration_report(
            records,
            dataset_path="/tmp/type.jsonl",
            source_sha256="5" * 64,
        )

        self.assertEqual(
            set(
                report["metrics"][
                    "by_question_type"
                ]
            ),
            {
                "COMPARE_SELECTION",
                "PRINCIPLE_INTERPRETATION",
            },
        )

    def test_excluded_record_omitted(self):
        reviewed = make_record(
            index=70,
            status="reviewed",
        )
        excluded = make_record(
            index=71,
            status="excluded",
        )
        report = build_calibration_report(
            [reviewed, excluded],
            dataset_path="/tmp/excluded.jsonl",
            source_sha256="6" * 64,
        )

        self.assertEqual(
            report["dataset"]["summary"][
                "record_count"
            ],
            2,
        )
        self.assertEqual(
            report["dataset"]["summary"][
                "analyzed_record_count"
            ],
            1,
        )
        self.assertEqual(
            report["metrics"][
                "overall_total_score"
            ]["count"],
            1,
        )

    def test_atomic_outputs_and_source_unchanged(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = [
                make_record(index=80),
                make_record(
                    index=81,
                    status="adjudicated",
                ),
            ]
            dataset = self.write_dataset(
                root,
                records,
            )
            before = dataset.read_bytes()
            json_output = root / "report.json"
            markdown_output = root / "report.md"

            result = generate_report_files(
                dataset,
                json_output,
                markdown_output,
            )

            self.assertEqual(
                dataset.read_bytes(),
                before,
            )
            self.assertTrue(
                result[
                    "source_dataset_unchanged"
                ]
            )
            self.assertTrue(
                json_output.is_file()
            )
            self.assertTrue(
                markdown_output.is_file()
            )
            self.assertIn(
                "Expert Calibration "
                "Diagnostic Report",
                markdown_output.read_text(
                    encoding="utf-8"
                ),
            )
            loaded = json.loads(
                json_output.read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                loaded["version"],
                "expert_calibration_report_v1",
            )
            self.assertFalse(
                list(
                    root.glob(
                        ".*.tmp"
                    )
                )
            )

    def test_sessions_output_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset = self.write_dataset(
                root,
                [make_record(index=90)],
            )
            repository_root = (
                Path(__file__)
                .resolve()
                .parents[1]
            )
            forbidden = (
                repository_root
                / "data"
                / "sessions"
                / "forbidden-report.json"
            )

            with self.assertRaises(
                ExpertCalibrationReportError
            ):
                generate_report_files(
                    dataset,
                    forbidden,
                    root / "report.md",
                )

    def test_production_policy_disabled(self):
        report = build_calibration_report(
            [make_record(index=100)],
            dataset_path="/tmp/policy.jsonl",
            source_sha256="7" * 64,
        )

        self.assertFalse(
            report["readiness"][
                "analysis_ready"
            ]
        )
        self.assertFalse(
            report["readiness"][
                "calibration_ready"
            ]
        )
        self.assertFalse(
            report["production_policy"][
                "production_calibration_enabled"
            ]
        )
        self.assertEqual(
            report["production_policy"][
                "score_effect"
            ],
            "none",
        )
        self.assertFalse(
            report["production_policy"][
                "direct_score_application"
            ]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
