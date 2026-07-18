from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from expert_calibration_dataset import (
    CalibrationContractError,
    DIRECT_SCORE_APPLICATION,
    PRODUCTION_CALIBRATION_ENABLED,
    SCORE_EFFECT,
    build_draft_record,
    deterministic_dataset_split,
    finalize_record,
    load_jsonl,
    validate_dataset,
    validate_record,
    with_record_hash,
    write_jsonl_atomic,
)


RUBRIC_HASH = "a" * 64

MODEL_BREAKDOWN = {
    "A": 2.0,
    "B": 4.0,
    "C": 5.0,
    "D": 3.0,
    "E": 1.0,
}

EXPERT_BREAKDOWN = {
    "A": 2.2,
    "B": 4.1,
    "C": 5.4,
    "D": 3.1,
    "E": 1.2,
}


def draft(
    answer: str = "전문 답안",
):
    return build_draft_record(
        record_id=None,
        question_text=(
            "제어밸브 불평형력을 "
            "설명하시오."
        ),
        answer_text=answer,
        topic_id=(
            "control_valve_fluid_forces_"
            "unbalance_friction_actuator_"
            "sizing_fail_safe"
        ),
        question_type=(
            "PRINCIPLE_INTERPRETATION"
        ),
        rubric_snapshot_hash=(
            RUBRIC_HASH
        ),
        model_total_score=14.0,
        model_breakdown=(
            MODEL_BREAKDOWN
        ),
    )


class ExpertDatasetContractTests(
    unittest.TestCase
):
    def test_draft_is_stable_and_non_scoring(
        self,
    ):
        first = draft()
        second = draft()

        self.assertEqual(first, second)
        self.assertEqual(
            first["score_effect"],
            "none",
        )
        self.assertFalse(
            first[
                "direct_score_application"
            ]
        )
        self.assertFalse(
            PRODUCTION_CALIBRATION_ENABLED
        )
        self.assertEqual(
            SCORE_EFFECT,
            "none",
        )
        self.assertFalse(
            DIRECT_SCORE_APPLICATION
        )

    def test_finalize_requires_review_metadata(
        self,
    ):
        reviewed = finalize_record(
            draft(),
            expert_total_score=16.0,
            expert_breakdown=(
                EXPERT_BREAKDOWN
            ),
            reviewer_id="expert:01",
            reviewed_at=(
                "2026-07-18T10:00:00+09:00"
            ),
            review_method="single_expert",
        )

        self.assertEqual(
            reviewed[
                "adjudication_status"
            ],
            "reviewed",
        )
        self.assertEqual(
            reviewed[
                "expert_total_score"
            ],
            16.0,
        )

    def test_identity_mismatch_is_rejected(
        self,
    ):
        record = draft()
        record["answer_text"] = "변조"

        with self.assertRaisesRegex(
            CalibrationContractError,
            "submission_hash",
        ):
            validate_record(record)

    def test_layer_bounds_rejected_before_hashing(
        self,
    ):
        record = draft()
        record["model_breakdown"]["A"] = 4.0
        record.pop("record_hash")

        with self.assertRaisesRegex(
            CalibrationContractError,
            "outside",
        ):
            with_record_hash(record)

    def test_expert_total_must_match_layers(
        self,
    ):
        with self.assertRaisesRegex(
            CalibrationContractError,
            "expert_total_score",
        ):
            finalize_record(
                draft(),
                expert_total_score=15.0,
                expert_breakdown=(
                    EXPERT_BREAKDOWN
                ),
                reviewer_id="expert:01",
                reviewed_at=(
                    "2026-07-18T10:00:00+09:00"
                ),
                review_method=(
                    "single_expert"
                ),
            )

    def test_duplicate_submission_is_rejected(
        self,
    ):
        first = draft()
        second = copy.deepcopy(first)
        second["record_id"] = "other"
        second.pop("record_hash")
        second = with_record_hash(second)

        with self.assertRaisesRegex(
            CalibrationContractError,
            "duplicate submission_hash",
        ):
            validate_dataset(
                [first, second]
            )

    def test_session_path_is_rejected(
        self,
    ):
        path = (
            Path.cwd()
            / "data"
            / "sessions"
            / "forbidden.jsonl"
        )

        with self.assertRaisesRegex(
            CalibrationContractError,
            "must not be stored",
        ):
            write_jsonl_atomic(
                path,
                [draft()],
            )

    def test_split_is_stable(
        self,
    ):
        record = draft()

        first = deterministic_dataset_split(
            record["submission_hash"]
        )
        second = deterministic_dataset_split(
            record["submission_hash"]
        )

        self.assertEqual(first, second)
        self.assertIn(
            first,
            {"train", "holdout"},
        )

    def test_atomic_jsonl_roundtrip(
        self,
    ):
        reviewed = finalize_record(
            draft(),
            expert_total_score=16.0,
            expert_breakdown=(
                EXPERT_BREAKDOWN
            ),
            reviewer_id="expert:01",
            reviewed_at=(
                "2026-07-18T10:00:00+09:00"
            ),
            review_method="single_expert",
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.jsonl"

            report = write_jsonl_atomic(
                path,
                [reviewed],
                require_finalized=True,
            )
            loaded = load_jsonl(path)
            validated = validate_dataset(
                loaded,
                require_finalized=True,
            )

            self.assertEqual(
                loaded,
                [reviewed],
            )
            self.assertEqual(
                report[
                    "finalized_record_count"
                ],
                1,
            )
            self.assertEqual(
                validated["record_count"],
                1,
            )
            self.assertFalse(
                report[
                    "production_calibration_enabled"
                ]
            )
            self.assertFalse(
                report["calibration_ready"]
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
