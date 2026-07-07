#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT
    / "scripts"
    / "rubric_audit"
    / "report_priority_minor_relationships.py"
)


def load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "priority_minor_reporter_under_test",
        MODULE_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"cannot import reporter: {MODULE_PATH}"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_csv(
    path: Path,
    rows: list[dict[str, str]],
) -> None:
    fieldnames = [
        "priority",
        "action",
        "topic_id",
        "answer_id",
        "question_type",
        "check",
        "score",
        "message",
        "action_reason",
    ]

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)


class PriorityMinorReporterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.input_path = self.root / "analysis.csv"
        self.output_path = self.root / "priority.md"

        self.module.IN_CSV = self.input_path
        self.module.OUT_MD = self.output_path

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_zero_priority_rows_passes(self) -> None:
        write_csv(
            self.input_path,
            [
                {
                    "priority": "P3",
                    "action": "advisory_review",
                    "topic_id": "topic_p3",
                    "answer_id": "answer_p3",
                    "score": "",
                    "message": "advisory",
                    "action_reason": "keep",
                }
            ],
        )

        result = self.module.main()

        self.assertEqual(result, 0)
        report = self.output_path.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "- priority MINOR: 0",
            report,
        )
        self.assertIn("- 없음", report)
        self.assertNotIn("answer_p3", report)

    def test_p1_and_p2_are_counted_but_p3_is_excluded(
        self,
    ) -> None:
        write_csv(
            self.input_path,
            [
                {
                    "priority": "P2",
                    "action": "outline_fix",
                    "topic_id": "topic_b",
                    "answer_id": "answer_b",
                    "score": "0.67",
                    "message": "P2 issue",
                    "action_reason": "repair",
                },
                {
                    "priority": "P3",
                    "action": "advisory_review",
                    "topic_id": "topic_c",
                    "answer_id": "answer_c",
                    "score": "0.75",
                    "message": "P3 issue",
                    "action_reason": "review",
                },
                {
                    "priority": "P1",
                    "action": "manual_review",
                    "topic_id": "topic_a",
                    "answer_id": "answer_a",
                    "score": "0.50",
                    "message": "P1 issue",
                    "action_reason": "fix now",
                },
            ],
        )

        result = self.module.main()

        self.assertEqual(result, 1)
        report = self.output_path.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "- priority MINOR: 2",
            report,
        )
        self.assertIn("- P1: 1", report)
        self.assertIn("- P2: 1", report)
        self.assertIn("answer_a", report)
        self.assertIn("answer_b", report)
        self.assertNotIn("answer_c", report)
        self.assertLess(
            report.index("answer_a"),
            report.index("answer_b"),
        )

    def test_missing_input_fails(self) -> None:
        with self.assertRaises(SystemExit):
            self.module.main()


if __name__ == "__main__":
    unittest.main()
