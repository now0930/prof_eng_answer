"""Exact-ID audit, Registry, Topic Pack and generated-bank consistency gate."""

import csv
import json
from pathlib import Path

from scripts.reconcile_fact_anchor_review_1290 import build, csv_rows
from scripts.export_fact_anchor_revision_review import build_rows, render, OUTPUT
from scripts.validate_fact_anchor_content_review import validate
from scripts import merge_fact_anchor_content_reviews as review_merge
import pytest


ROOT = Path(__file__).resolve().parents[1]


def test_1290_review_and_executable_holds_are_identical():
    _, current = csv_rows(ROOT / "reports/fact_anchor_independent_verification_audit_20261101.csv")
    _, expected, source, revision, exclusion = build()
    assert current == expected
    for name, value in (
        ("fact_anchor_unresolved_source_holds_20261101.json", source),
        ("fact_anchor_independent_revision_holds_20261101.json", revision),
        ("fact_anchor_scoring_exclusions_20261101.json", exclusion),
    ):
        assert json.loads((ROOT / "grading/evidence" / name).read_text()) == value
    assert (len(source["holds"]), len(revision["holds"]), len(exclusion["exclusions"])) == (80, 80, 276)


def test_1290_fact_id_owners_exist_in_registry_source_and_generated():
    with (ROOT / "reports/fact_anchor_independent_verification_audit_20261101.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    registry = {
        row["fact_id"]: row
        for row in json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())["facts"]
    }
    generated = {
        topic["topic_id"]: {row["anchor_id"] for row in topic["anchors"]}
        for topic in json.loads((ROOT / "rubrics/generated/fact_anchors.generated.json").read_text())["topics"]
    }
    source = {}
    for row in rows:
        topic_id, anchor_id, fact_id = row["topic_id"], row["anchor_id"], row["fact_id"]
        if topic_id not in source:
            path = ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json"
            source[topic_id] = {item["anchor_id"] for item in json.loads(path.read_text())["anchors"]}
        assert registry[fact_id]["topic_id"] == topic_id
        assert registry[fact_id]["legacy_anchor_id"] == anchor_id
        assert anchor_id in source[topic_id]
        assert anchor_id in generated[topic_id]


def test_chatgpt_content_review_packet_is_complete_but_undecided():
    rows = build_rows()
    assert len(rows) == 80
    assert all(row["chatgpt_review_status"] == "UNREVIEWED" for row in rows)
    assert all(not row["proposed_statement"] and not row["source_locator"] for row in rows)
    assert OUTPUT.read_text(encoding="utf-8") == render(rows)
    assert validate(OUTPUT)["UNREVIEWED"] == 80


def test_content_review_format_rejects_unattributed_correction(tmp_path):
    rows = build_rows()
    rows[0]["chatgpt_review_status"] = "KEEP_WITH_CORRECTION"
    rows[0]["proposed_statement"] = "Unattributed revision"
    path = tmp_path / "review.csv"
    path.write_text(render(rows), encoding="utf-8")
    with pytest.raises(ValueError, match="Reviewer identity/date missing"):
        validate(path)


def test_content_review_format_rejects_changed_canonical_text(tmp_path):
    rows = build_rows()
    rows[0]["current_topic_pack_statement"] = "silently changed"
    path = tmp_path / "review.csv"
    path.write_text(render(rows), encoding="utf-8")
    with pytest.raises(ValueError, match="Original source fields were changed"):
        validate(path)


def test_content_review_batches_merge_exactly_without_promotion(tmp_path, monkeypatch):
    rows = build_rows()
    batches = []
    for label, priorities in (("p0", {"P0"}), ("p1", {"P1"}), ("rest", {"DEFER", "SAMPLE"})):
        path = tmp_path / f"{label}.csv"
        path.write_text(render([row for row in rows if row["queue_priority"] in priorities]), encoding="utf-8")
        batches.append((label, priorities, path))
    monkeypatch.setattr(review_merge, "BATCHES", tuple(batches))
    assert review_merge.merge() == rows


def test_completed_chatgpt_review_is_exact_and_does_not_promote_scoring():
    path = ROOT / "reports/fact_anchor_chatgpt_review_completed_80_20261102.csv"
    assert validate(path) == {
        "UNREVIEWED": 0,
        "KEEP_WITH_CORRECTION": 28,
        "HOLD_INSUFFICIENT_EVIDENCE": 46,
        "EXCLUDE_FROM_GENERAL_SCORING": 6,
    }
    assert path.read_text(encoding="utf-8") == render(review_merge.merge())
    _, _, source, revision, exclusion = build()
    assert sum(map(len, (source["holds"], revision["holds"], exclusion["exclusions"]))) == 436
