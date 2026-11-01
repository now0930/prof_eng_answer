"""Fail-closed scoring reference guards for independently sourced revision holds."""
import csv
import json
from pathlib import Path

from grading.evidence.fact_anchor_scoring_exclusions import (
    excluded_from_scoring,
    independent_revision_holds,
    scoring_exclusions,
)

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "reports/fact_anchor_independent_verification_audit_20261101.csv"
HOLDS = ROOT / "grading/evidence/fact_anchor_independent_revision_holds_20261101.json"


def test_revision_holds_are_exactly_independently_reviewed_revisions():
    with AUDIT.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected = {
        (row["fact_id"], row["topic_id"], row["anchor_id"])
        for row in rows if row["final_technical_verdict"] == "REVISE_REQUIRED"
    }
    with HOLDS.open(encoding="utf-8") as handle:
        data = json.load(handle)
    found = {(r["fact_id"], r["topic_id"], r["anchor_id"]) for r in data["holds"]}
    assert found == expected
    assert len(found) == len(data["holds"]) == 42
    assert all(row["reason"] == "primary_source_revision_pending" for row in data["holds"])
    assert all(
        excluded_from_scoring(fact_id=fid, topic_id=topic, anchor_id=anchor)
        for fid, topic, anchor in found
    )


def test_original_276_exclusions_remain_unchanged_and_do_not_overlap():
    old_ids, old_anchors = scoring_exclusions()
    new_ids, new_anchors = independent_revision_holds()
    assert len(old_ids) == len(old_anchors) == 276
    assert len(new_ids) == len(new_anchors) == 40
    assert not (old_ids & new_ids)
    assert not (old_anchors & new_anchors)


def test_kept_and_unreviewed_anchors_are_not_blanket_excluded():
    with AUDIT.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    verified = next(
        row for row in rows if row["final_technical_verdict"] == "KEEP_BOUNDED"
        and not row["scoring_exclusion_reason"]
    )
    assert not excluded_from_scoring(
        fact_id=verified["fact_id"],
        topic_id=verified["topic_id"],
        anchor_id=verified["anchor_id"],
    )
