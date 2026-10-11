import json
from pathlib import Path

from scripts.verify_representative_fact_sources import SIGNALS, audit_catalog


ROOT = Path(__file__).resolve().parents[1]


def test_source_signal_audit_matches_approved_registry():
    facts = json.loads((ROOT / "grading" / "evidence" / "approved_fact_registry.json").read_text(encoding="utf-8"))["facts"]
    catalog = {}
    for fact in facts:
        if not fact["source_refs"]:
            continue
        source = next(row for row in json.loads((ROOT / "master_topic_packs" / f"{fact['topic_id']}.json").read_text(encoding="utf-8"))["sources"] if row["source_id"] == fact["source_refs"][0]["source_id"])
        catalog[source["source_id"]] = {"source_url": source["source_url"], "version": source["version"],
                                        "content_sha256": fact["source_refs"][0]["source_sha256"],
                                        "fetch_status": "available", "extracted_text": " ".join(SIGNALS[fact["fact_id"]])}
    result = audit_catalog(ROOT, catalog)
    assert result["all_source_signals_match"] is True
    assert result["runtime_scoring_enabled"] is False
    source_free = next(row for row in result["outcomes"] if row["fact_id"] == "nyquist_negative_feedback_characteristic_equation")
    assert source_free["source_audit"] == "not_applicable_independently_verified"
    assert source_free["source_approved"] is None
    assert source_free["fact_approved"] is True
    assert all(row["source_approved"] and row["fact_approved"] for row in result["outcomes"] if row["source_audit"] == "checked")
    first_source_backed = next(fact for fact in facts if fact["source_refs"])
    catalog[first_source_backed["source_refs"][0]["source_id"]]["extracted_text"] = ""
    assert audit_catalog(ROOT, catalog)["all_source_signals_match"] is False
