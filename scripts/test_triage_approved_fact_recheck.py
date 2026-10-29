"""Regression checks for deterministic Fact recheck triage."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from triage_approved_fact_recheck import triage  # noqa: E402


class ApprovedFactRecheckTriageTests(unittest.TestCase):
    def test_every_registry_row_has_one_disposition(self) -> None:
        rows, summary = triage(ROOT)
        self.assertEqual(len(rows), summary["total_fact_rows"])
        self.assertEqual(len({row["fact_id"] for row in rows}), len(rows))
        self.assertEqual(sum(summary["priority_counts"].values()), len(rows))
        self.assertEqual(summary["review_queue_rows"] + summary["deferred_rows"], len(rows))

    def test_known_lineage_and_condition_signals_are_not_hidden(self) -> None:
        rows, _ = triage(ROOT)
        by_id = {row["fact_id"]: row for row in rows}
        self.assertEqual(by_id["liquid_in_glass_thermometer_calibration_is_immersion_condition_specific"]["priority"], "P0")
        self.assertIn("anchor_missing", by_id["liquid_in_glass_thermometer_calibration_is_immersion_condition_specific"]["reasons"])
        self.assertEqual(by_id["second_order_normalized_frequency_response_magnitude"]["priority"], "P0")

    def test_repeated_run_is_identical_and_sample_is_optional(self) -> None:
        first = triage(ROOT)
        self.assertEqual(first, triage(ROOT))
        no_sample_rows, no_sample_summary = triage(ROOT, sample_per_topic=0)
        self.assertEqual(no_sample_summary["priority_counts"]["SAMPLE"], 0)
        self.assertEqual(len(no_sample_rows), len(first[0]))

    def test_committed_snapshot_matches_current_registry(self) -> None:
        rows, summary = triage(ROOT)
        saved = json.loads((ROOT / "reports/approved_fact_recheck_summary_20261029.json").read_text(encoding="utf-8"))
        with (ROOT / "reports/approved_fact_recheck_triage_20261029.csv").open(encoding="utf-8", newline="") as handle:
            saved_rows = list(csv.DictReader(handle))
        self.assertEqual(saved, summary)
        self.assertEqual(saved_rows, rows)


if __name__ == "__main__":
    unittest.main()
