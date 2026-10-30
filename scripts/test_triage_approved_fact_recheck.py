"""Regression checks for deterministic Fact recheck triage."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys
import csv
import json
import re
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from triage_approved_fact_recheck import triage  # noqa: E402
from validate_selected_fact_recheck_coverage import validate as validate_selected_review  # noqa: E402


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

    def test_committed_snapshot_is_a_consistent_historical_review(self) -> None:
        # The 2026-10-29 snapshot is the immutable review input. Remediation
        # legitimately changes the current registry, so comparing their SHA
        # or row count would make the historical review unreleasable.
        saved = json.loads((ROOT / "reports/approved_fact_recheck_summary_20261029.json").read_text(encoding="utf-8"))
        with (ROOT / "reports/approved_fact_recheck_triage_20261029.csv").open(encoding="utf-8", newline="") as handle:
            saved_rows = list(csv.DictReader(handle))
        self.assertEqual(len(saved_rows), saved["total_fact_rows"])
        self.assertEqual(len({row["fact_id"] for row in saved_rows}), len(saved_rows))
        self.assertEqual(dict(Counter(row["priority"] for row in saved_rows)), saved["priority_counts"])
        self.assertEqual(sum(saved["priority_counts"][key] for key in ("P0", "P1", "SAMPLE")), saved["review_queue_rows"])

    def test_final_hold_rows_match_the_historical_csv_fact_ids(self) -> None:
        result = validate_selected_review()
        self.assertEqual(result["selected_reviewed"], result["selected"])
        self.assertEqual(result["selected_verdicts"]["HOLD"], 18)

    def test_general_principle_resolution_covers_each_historical_hold_without_vendor_example(self) -> None:
        p1 = (ROOT / "reports/fact_recheck_p1_rest_20261029.md").read_text(encoding="utf-8")
        final_hold = p1.split("### Final follow-up: remaining unresolved and omitted selected facts", 1)[1]
        final_hold = final_hold.split("| CSV 행 | Fact ID | 판정 |", 1)[0]
        old_ids = set(re.findall(r"^\|\s*\d+\s*\|\s*([a-z][a-z0-9_]*)\s*\|", final_hold, re.M))
        old_ids.add("valve_repair_report_example_separates_as_found_and_as_left_test_data")
        self.assertEqual(len(old_ids), 18)
        report = (ROOT / "reports/fact_recheck_general_principle_resolution_20261030.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| `([a-z][a-z0-9_]*)` \| (GENERAL_VERIFIED|REPLACED_SPECIFIC_EXAMPLE) \|", report, re.M)
        self.assertEqual({fact_id for fact_id, _ in rows}, old_ids)
        self.assertEqual(sum(status == "GENERAL_VERIFIED" for _, status in rows), 17)
        self.assertEqual(sum(status == "REPLACED_SPECIFIC_EXAMPLE" for _, status in rows), 1)
        facts = {row["fact_id"]: row for row in json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text(encoding="utf-8"))["facts"]}
        for fact_id, status in rows:
            if status == "GENERAL_VERIFIED":
                self.assertIn(fact_id, facts)
                self.assertEqual(facts[fact_id]["verification_status"], "verified")
                self.assertTrue(facts[fact_id]["verification_refs"])
        self.assertNotIn("valve_repair_report_example_separates_as_found_and_as_left_test_data", facts)
        replacement = facts["valve_as_found_as_left_results_require_comparable_test_basis"]
        self.assertNotIn("Emerson", replacement["statement"])
        self.assertIn("시험기준의 비교 가능성", replacement["statement"])


if __name__ == "__main__":
    unittest.main()
