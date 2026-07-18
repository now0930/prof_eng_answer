from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from expert_calibration_dataset import (
    CalibrationContractError,
    build_draft_record,
    load_jsonl,
    validate_dataset,
    write_jsonl_atomic,
)
from review_expert_calibration_record import (
    ExpertCalibrationReviewError,
    review_record_in_dataset,
)


def draft(
    *,
    record_id: str,
    question: str,
    answer: str,
    notes: str,
) -> dict:
    return build_draft_record(
        record_id=record_id,
        question_text=question,
        answer_text=answer,
        topic_id="review_workflow_topic",
        question_type=(
            "PRINCIPLE_INTERPRETATION"
        ),
        rubric_snapshot_hash="a" * 64,
        model_total_score=5.0,
        model_breakdown={
            "A": 1.0,
            "B": 1.0,
            "C": 1.0,
            "D": 1.0,
            "E": 1.0,
        },
        notes=notes,
    )


def review_kwargs() -> dict:
    return {
        "a_score": 2.0,
        "b_score": 2.5,
        "c_score": 3.0,
        "d_score": 2.0,
        "e_score": 1.0,
        "reviewer_id": "expert-001",
        "reviewed_at": (
            "2026-07-18T12:00:00+09:00"
        ),
        "review_method": "single_expert",
        "adjudication_status": "reviewed",
    }


class ExpertReviewWorkflowTests(
    unittest.TestCase
):
    def create_dataset(
        self,
        root: Path,
        records: list[dict],
    ) -> Path:
        path = root / "expert_dataset.jsonl"
        write_jsonl_atomic(path, records)
        return path

    def test_review_by_record_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-001",
                question="문제 1",
                answer="답안 1",
                notes="keep me",
            )
            path = self.create_dataset(
                root,
                [first],
            )

            result = review_record_in_dataset(
                path,
                record_id="record-001",
                **review_kwargs(),
            )
            record = load_jsonl(path)[0]

            self.assertTrue(result["ok"])
            self.assertEqual(
                record["adjudication_status"],
                "reviewed",
            )
            self.assertEqual(
                record["expert_total_score"],
                10.5,
            )

    def test_review_by_submission_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-002",
                question="문제 2",
                answer="답안 2",
                notes="hash selector",
            )
            path = self.create_dataset(
                root,
                [first],
            )

            result = review_record_in_dataset(
                path,
                submission_hash=(
                    first["submission_hash"]
                ),
                **review_kwargs(),
            )

            self.assertEqual(
                result["selector"]["name"],
                "submission_hash",
            )

    def test_exactly_one_selector_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-003",
                question="문제 3",
                answer="답안 3",
                notes="selector",
            )
            path = self.create_dataset(
                root,
                [first],
            )

            with self.assertRaises(
                ExpertCalibrationReviewError
            ):
                review_record_in_dataset(
                    path,
                    **review_kwargs(),
                )

            with self.assertRaises(
                ExpertCalibrationReviewError
            ):
                review_record_in_dataset(
                    path,
                    record_id="record-003",
                    submission_hash=(
                        first["submission_hash"]
                    ),
                    **review_kwargs(),
                )

    def test_record_not_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-004",
                question="문제 4",
                answer="답안 4",
                notes="not found",
            )
            path = self.create_dataset(
                root,
                [first],
            )

            with self.assertRaisesRegex(
                ExpertCalibrationReviewError,
                "not found",
            ):
                review_record_in_dataset(
                    path,
                    record_id="missing",
                    **review_kwargs(),
                )

    def test_ambiguous_record_id_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="duplicate-id",
                question="문제 5-1",
                answer="답안 5-1",
                notes="first",
            )
            second = draft(
                record_id="duplicate-id",
                question="문제 5-2",
                answer="답안 5-2",
                notes="second",
            )
            path = root / "expert_dataset.jsonl"

            with patch(
                "review_expert_calibration_record.load_jsonl",
                return_value=[first, second],
            ):
                with self.assertRaisesRegex(
                    ExpertCalibrationReviewError,
                    "ambiguous",
                ):
                    review_record_in_dataset(
                        path,
                        record_id="duplicate-id",
                        **review_kwargs(),
                    )

    def test_notes_and_other_records_preserved(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-006-a",
                question="문제 6-1",
                answer="답안 6-1",
                notes="selected notes",
            )
            second = draft(
                record_id="record-006-b",
                question="문제 6-2",
                answer="답안 6-2",
                notes="untouched notes",
            )
            path = self.create_dataset(
                root,
                [first, second],
            )

            review_record_in_dataset(
                path,
                record_id="record-006-a",
                **review_kwargs(),
            )
            records = load_jsonl(path)

            self.assertEqual(
                records[0]["notes"],
                "selected notes",
            )
            self.assertEqual(
                records[1],
                second,
            )

    def test_naive_datetime_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-007",
                question="문제 7",
                answer="답안 7",
                notes="datetime",
            )
            path = self.create_dataset(
                root,
                [first],
            )
            kwargs = review_kwargs()
            kwargs["reviewed_at"] = (
                "2026-07-18T12:00:00"
            )

            with self.assertRaises(
                CalibrationContractError
            ):
                review_record_in_dataset(
                    path,
                    record_id="record-007",
                    **kwargs,
                )

    def test_pending_method_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-008",
                question="문제 8",
                answer="답안 8",
                notes="pending",
            )
            path = self.create_dataset(
                root,
                [first],
            )
            kwargs = review_kwargs()
            kwargs["review_method"] = "pending"

            with self.assertRaises(
                ExpertCalibrationReviewError
            ):
                review_record_in_dataset(
                    path,
                    record_id="record-008",
                    **kwargs,
                )

    def test_layer_maximum_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-009",
                question="문제 9",
                answer="답안 9",
                notes="max",
            )
            path = self.create_dataset(
                root,
                [first],
            )
            kwargs = review_kwargs()
            kwargs["a_score"] = 4.0

            with self.assertRaises(
                CalibrationContractError
            ):
                review_record_in_dataset(
                    path,
                    record_id="record-009",
                    **kwargs,
                )

    def test_adjudicated_status_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-010",
                question="문제 10",
                answer="답안 10",
                notes="panel",
            )
            path = self.create_dataset(
                root,
                [first],
            )
            kwargs = review_kwargs()
            kwargs["review_method"] = (
                "panel_adjudication"
            )
            kwargs["adjudication_status"] = (
                "adjudicated"
            )

            review_record_in_dataset(
                path,
                record_id="record-010",
                **kwargs,
            )
            record = load_jsonl(path)[0]

            self.assertEqual(
                record["adjudication_status"],
                "adjudicated",
            )

    def test_atomic_result_remains_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-011",
                question="문제 11",
                answer="답안 11",
                notes="atomic",
            )
            path = self.create_dataset(
                root,
                [first],
            )

            result = review_record_in_dataset(
                path,
                record_id="record-011",
                **review_kwargs(),
            )
            records = load_jsonl(path)
            report = validate_dataset(records)

            self.assertTrue(
                result["record_hash_changed"]
            )
            self.assertTrue(
                result["notes_preserved"]
            )
            self.assertEqual(
                report["record_count"],
                1,
            )

    def test_production_policy_remains_disabled(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = draft(
                record_id="record-012",
                question="문제 12",
                answer="답안 12",
                notes="policy",
            )
            path = self.create_dataset(
                root,
                [first],
            )

            result = review_record_in_dataset(
                path,
                record_id="record-012",
                **review_kwargs(),
            )

            self.assertFalse(
                result[
                    "production_calibration_enabled"
                ]
            )
            self.assertFalse(
                result["calibration_ready"]
            )
            self.assertEqual(
                result["score_effect"],
                "none",
            )
            self.assertFalse(
                result[
                    "direct_score_application"
                ]
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
