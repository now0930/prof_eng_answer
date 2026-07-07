from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDITOR_PATH = (
    ROOT
    / "scripts"
    / "rubric_audit"
    / "deep_model_fact_relationship_audit.py"
)
MODEL_PATH = (
    ROOT
    / "rubrics"
    / "model_answers"
    / "industrial_instrumentation_control.json"
)
FACT_PATH = (
    ROOT
    / "rubrics"
    / "fact_anchors"
    / "industrial_instrumentation_control.json"
)


def load_auditor() -> ModuleType:
    if not AUDITOR_PATH.exists():
        raise AssertionError(
            f"deep auditor is missing: {AUDITOR_PATH}"
        )

    if AUDITOR_PATH.stat().st_size < 1000:
        raise AssertionError(
            "deep auditor is empty or unexpectedly small: "
            f"{AUDITOR_PATH.stat().st_size} bytes"
        )

    spec = importlib.util.spec_from_file_location(
        "deep_model_fact_relationship_audit_under_test",
        AUDITOR_PATH,
    )

    if spec is None or spec.loader is None:
        raise AssertionError(
            "unable to create deep-auditor import specification"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DeepModelFactRelationshipAuditorTest(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.auditor = load_auditor()
        cls.model_data = json.loads(
            MODEL_PATH.read_text(encoding="utf-8")
        )
        cls.fact_data = json.loads(
            FACT_PATH.read_text(encoding="utf-8")
        )

        cls.models = cls.auditor.model_variants_by_topic(
            cls.model_data.get("answers", [])
        )
        cls.facts = cls.auditor.fact_by_topic(
            cls.fact_data.get("topics", [])
        )

    def test_source_is_nonempty_and_has_required_api(
        self,
    ) -> None:
        self.assertGreater(
            AUDITOR_PATH.stat().st_size,
            1000,
        )

        self.assertEqual(
            ROOT,
            self.auditor.ROOT,
        )

        required = (
            "audit_topic",
            "write_reports",
            "model_variants_by_topic",
            "fact_by_topic",
            "main",
        )

        for name in required:
            with self.subTest(name=name):
                self.assertTrue(
                    callable(
                        getattr(
                            self.auditor,
                            name,
                            None,
                        )
                    ),
                    msg=f"missing callable: {name}",
                )

    def test_current_bank_has_no_blocker_or_major(
        self,
    ) -> None:
        topic_ids = sorted(
            set(self.models) | set(self.facts)
        )

        rows = [
            self.auditor.audit_topic(
                topic_id,
                self.models.get(topic_id, []),
                self.facts.get(topic_id),
            )
            for topic_id in topic_ids
        ]

        self.assertEqual(55, len(rows))

        severe = [
            (
                row.get("severity"),
                row.get("topic_id"),
                row.get("issues"),
            )
            for row in rows
            if row.get("severity")
            in {"BLOCKER", "MAJOR"}
        ]

        self.assertEqual([], severe)


    def test_write_reports_uses_repository_root_and_lf(
        self,
    ) -> None:
        self.assertEqual(
            ROOT,
            self.auditor.ROOT,
        )

        rows = [
            {
                "severity": "OK",
                "topic_id": "fixture_topic",
                "model_variants": 1,
                "fact_exists": True,
                "anchor_count": 5,
                "coverage_score": 1.0,
                "anchor_coverage": "5/5",
                "issues": ["OK"],
            }
        ]

        original_md = self.auditor.OUT_MD
        original_csv = self.auditor.OUT_CSV

        try:
            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                output_md = tmp_path / "audit.md"
                output_csv = tmp_path / "audit.csv"

                self.auditor.OUT_MD = output_md
                self.auditor.OUT_CSV = output_csv
                self.auditor.write_reports(rows)

                self.assertTrue(output_md.exists())
                self.assertTrue(output_csv.exists())

                raw = output_csv.read_bytes()

                self.assertNotIn(
                    bytes([13]),
                    raw,
                )
                self.assertEqual(
                    2,
                    raw.count(bytes([10])),
                )

                with output_csv.open(
                    encoding="utf-8",
                    newline="",
                ) as handle:
                    csv_lines = handle.readlines()

                self.assertEqual(
                    2,
                    len(csv_lines),
                )
                self.assertTrue(
                    csv_lines[0].startswith(
                        "severity,topic_id,"
                    )
                )
        finally:
            self.auditor.OUT_MD = original_md
            self.auditor.OUT_CSV = original_csv

    def test_broad_trigger_warning_uses_exact_match(
        self,
    ) -> None:
        cases: list[tuple[str, str, str]] = [
            (
                "pressure_dp_transmitter",
                "압력",
                "압력계",
            ),
            (
                "industrial_communication_protocol",
                "통신",
                "통신망",
            ),
        ]

        for (
            topic_id,
            exact_broad_trigger,
            specific_trigger,
        ) in cases:
            with self.subTest(topic_id=topic_id):
                models = self.models[topic_id]
                base_fact: dict[str, Any] = copy.deepcopy(
                    self.facts[topic_id]
                )

                base_fact["triggers"] = [
                    trigger
                    for trigger in (
                        base_fact.get("triggers") or []
                    )
                    if str(trigger).strip().casefold()
                    != exact_broad_trigger.casefold()
                ]

                specific_fact = copy.deepcopy(base_fact)
                specific_fact["triggers"].append(
                    specific_trigger
                )

                specific_row = self.auditor.audit_topic(
                    topic_id,
                    models,
                    specific_fact,
                )

                specific_issues = " | ".join(
                    specific_row.get("issues", [])
                )

                self.assertNotIn(
                    "오라우팅 위험 trigger",
                    specific_issues,
                )

                broad_fact = copy.deepcopy(base_fact)
                broad_fact["triggers"].append(
                    exact_broad_trigger
                )

                broad_row = self.auditor.audit_topic(
                    topic_id,
                    models,
                    broad_fact,
                )

                broad_issues = " | ".join(
                    broad_row.get("issues", [])
                )

                self.assertEqual(
                    "MAJOR",
                    broad_row.get("severity"),
                )
                self.assertIn(
                    "오라우팅 위험 trigger",
                    broad_issues,
                )
                self.assertIn(
                    exact_broad_trigger,
                    broad_issues,
                )


if __name__ == "__main__":
    unittest.main()
