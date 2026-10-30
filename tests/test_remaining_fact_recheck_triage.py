"""Operationally inert selection of the remaining Fact review queue."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from triage_remaining_fact_recheck import _historically_reviewed, select_batch, triage  # noqa: E402


def test_current_registry_accounting_and_unique_assignment() -> None:
    rows, summary = triage(ROOT)
    ids = [row["fact_id"] for row in rows]
    assert len(ids) == len(set(ids)) == summary["unreviewed_rows"]
    current_ids = {fact["fact_id"] for fact in json.loads(
        (ROOT / "grading/evidence/approved_fact_registry.json").read_text(encoding="utf-8"))["facts"]}
    assert summary["current_registry_rows"] == len(current_ids)
    assert summary["historically_reviewed_current_rows"] == len(current_ids & _historically_reviewed(ROOT))
    assert summary["unreviewed_rows"] == len(current_ids - _historically_reviewed(ROOT))
    assert sum(summary["priority_counts"].values()) == len(rows)
    assert all(row["review_status"] == "UNREVIEWED" for row in rows)


def test_repeated_selection_is_stable_and_read_only() -> None:
    path = ROOT / "grading/evidence/approved_fact_registry.json"
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    assert triage(ROOT) == triage(ROOT)
    rows, summary = triage(ROOT, sample_per_topic=0)
    assert summary["priority_counts"]["SAMPLE"] == 0
    assert len(rows) == summary["unreviewed_rows"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before


def test_historical_review_and_replacement_are_not_mislabeled() -> None:
    rows, _ = triage(ROOT)
    ids = {row["fact_id"] for row in rows}
    assert "second_order_overdamped_response" not in ids
    assert "valve_repair_report_example_separates_as_found_and_as_left_test_data" not in ids
    assert "valve_as_found_as_left_results_require_comparable_test_basis" in ids
    registry_ids = {fact["fact_id"] for fact in json.loads(
        (ROOT / "grading/evidence/approved_fact_registry.json").read_text(encoding="utf-8"))
        ["facts"]}
    assert ids <= registry_ids


def test_first_batch_is_bounded_and_topic_diverse() -> None:
    rows, _ = triage(ROOT)
    batch = select_batch(rows, size=20)
    assert len(batch) == 20
    assert len({row["topic_id"] for row in batch}) == 20
    assert all(row["priority"] == "P0" for row in batch)
    assert select_batch(rows, size=0) == []


def test_first_batch_review_report_covers_only_selected_facts() -> None:
    rows, _ = triage(ROOT)
    expected = {row["fact_id"] for row in select_batch(rows, size=20)}
    report = (ROOT / "reports/remaining_fact_recheck_batch01_20261030.md").read_text(encoding="utf-8")
    found = re.findall(r"^\| \d+ \| `([a-z][a-z0-9_]*)` \| (GENERAL_PRINCIPLE_CONSISTENT|SOURCE_SCOPE_CHECK|NARROW_OR_CORRECT) \|", report, re.M)
    assert len(found) == len(expected) == 20
    assert {fact_id for fact_id, _ in found} == expected
    assert sum(status == "GENERAL_PRINCIPLE_CONSISTENT" for _, status in found) == 12
    assert sum(status == "SOURCE_SCOPE_CHECK" for _, status in found) == 7
    assert sum(status == "NARROW_OR_CORRECT" for _, status in found) == 1
