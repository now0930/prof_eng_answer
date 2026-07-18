from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from expert_calibration_dataset import (
    CalibrationContractError,
    load_jsonl,
    validate_record,
)
from export_expert_calibration_record import (
    ExpertCalibrationExportError,
    build_draft_from_session,
    canonical_sha256,
    export_draft_record,
)


QUESTION = "제어밸브 불평형력을 설명하시오."
ANSWER = "압력차와 유효면적을 검토한다."

TOPIC_ID = (
    "control_valve_fluid_forces_"
    "unbalance_friction_actuator_"
    "sizing_fail_safe"
)

BREAKDOWN = [
    {"layer_id": "A", "score": 1.5},
    {"layer_id": "B", "score": 2.5},
    {"layer_id": "C", "score": 2.0},
    {"layer_id": "D", "score": 2.0},
    {"layer_id": "E", "score": 0.5},
]

ANCHORS = [
    {
        "id": (
            "control_valve_"
            "pressure_force_surface_integration"
        )
    },
    {
        "id": (
            "control_valve_"
            "packing_friction"
        )
    },
]


def create_fixture(root: Path) -> tuple[Path, Path]:
    session = root / "session-001"
    session.mkdir()

    (session / "input.txt").write_text(
        QUESTION + "\n" + ANSWER,
        encoding="utf-8",
    )
    (session / "grade.json").write_text(
        json.dumps(
            {
                "total_score": 8.5,
                "breakdown": BREAKDOWN,
                "question_type": (
                    "PRINCIPLE_INTERPRETATION"
                ),
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (session / "fact_anchor_evaluation.json").write_text(
        json.dumps(
            {
                "question_text": QUESTION,
                "anchors": ANCHORS,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    rubric = {
        "version": "test-rubric-v1",
        "items": [
            {"id": "A"},
            {"id": "B"},
        ],
    }
    (session / "rubric_snapshot.json").write_text(
        json.dumps(
            rubric,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    bank = root / "fact_anchors.json"
    bank.write_text(
        json.dumps(
            {
                "topics": [
                    {
                        "topic_id": TOPIC_ID,
                        "fact_anchors": ANCHORS,
                    },
                    {
                        "topic_id": "other_topic",
                        "fact_anchors": [
                            {"id": "other_anchor"}
                        ],
                    },
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return session, bank


class OfflineExporterTests(unittest.TestCase):
    def test_builds_deterministic_draft(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            session, bank = create_fixture(
                Path(tmp)
            )

            first, first_diag = (
                build_draft_from_session(
                    session,
                    fact_anchor_bank_path=bank,
                )
            )
            second, second_diag = (
                build_draft_from_session(
                    session,
                    fact_anchor_bank_path=bank,
                )
            )

            self.assertEqual(first, second)
            self.assertEqual(
                first_diag,
                second_diag,
            )
            self.assertEqual(
                first["topic_id"],
                TOPIC_ID,
            )
            self.assertEqual(
                first["answer_text"],
                ANSWER,
            )
            self.assertEqual(
                first[
                    "adjudication_status"
                ],
                "draft",
            )
            self.assertEqual(
                first["score_effect"],
                "none",
            )
            self.assertFalse(
                first[
                    "direct_score_application"
                ]
            )
            validate_record(first)

    def test_extracts_layer_breakdown(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            session, bank = create_fixture(
                Path(tmp)
            )
            record, diagnostics = (
                build_draft_from_session(
                    session,
                    fact_anchor_bank_path=bank,
                )
            )

            self.assertEqual(
                record["model_breakdown"],
                {
                    "A": 1.5,
                    "B": 2.5,
                    "C": 2.0,
                    "D": 2.0,
                    "E": 0.5,
                },
            )
            self.assertEqual(
                record["model_total_score"],
                8.5,
            )
            self.assertEqual(
                diagnostics[
                    "model_breakdown_source"
                ],
                "grade.breakdown",
            )

    def test_rubric_hash_is_canonical(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            session, bank = create_fixture(
                Path(tmp)
            )
            record, _ = (
                build_draft_from_session(
                    session,
                    fact_anchor_bank_path=bank,
                )
            )
            rubric = json.loads(
                (
                    session
                    / "rubric_snapshot.json"
                ).read_text(
                    encoding="utf-8"
                )
            )

            self.assertEqual(
                record[
                    "rubric_snapshot_hash"
                ],
                canonical_sha256(rubric),
            )

    def test_exports_and_loads_jsonl(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session, bank = create_fixture(
                root
            )
            output = root / "dataset.jsonl"

            report = export_draft_record(
                session,
                output,
                fact_anchor_bank_path=bank,
            )
            records = load_jsonl(output)

            self.assertTrue(report["ok"])
            self.assertEqual(len(records), 1)
            self.assertEqual(
                records[0]["topic_id"],
                TOPIC_ID,
            )
            self.assertTrue(
                report["diagnostics"][
                    "source_session_unchanged"
                ]
            )

    def test_duplicate_export_is_rejected(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session, bank = create_fixture(
                root
            )
            output = root / "dataset.jsonl"

            export_draft_record(
                session,
                output,
                fact_anchor_bank_path=bank,
            )

            with self.assertRaises(
                CalibrationContractError
            ):
                export_draft_record(
                    session,
                    output,
                    fact_anchor_bank_path=bank,
                )

    def test_replace_existing_is_stable(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session, bank = create_fixture(
                root
            )
            output = root / "dataset.jsonl"

            first = export_draft_record(
                session,
                output,
                fact_anchor_bank_path=bank,
            )
            second = export_draft_record(
                session,
                output,
                fact_anchor_bank_path=bank,
                replace_existing=True,
            )

            self.assertEqual(
                first["record"],
                second["record"],
            )
            self.assertEqual(
                len(load_jsonl(output)),
                1,
            )

    def test_rejects_non_prefix_input(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session, bank = create_fixture(
                root
            )
            (session / "input.txt").write_text(
                "다른 문제\n" + ANSWER,
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ExpertCalibrationExportError,
                "does not start",
            ):
                build_draft_from_session(
                    session,
                    fact_anchor_bank_path=bank,
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
