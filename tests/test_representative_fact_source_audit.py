import json
from pathlib import Path

from scripts.verify_representative_fact_sources import SIGNALS, audit_catalog


ROOT = Path(__file__).resolve().parents[1]


def test_source_signal_audit_is_read_only_and_not_approval():
    facts = json.loads((ROOT / "reports" / "fact_grounded_representative_candidates_20261010.json").read_text(encoding="utf-8"))["facts"]
    catalog = {}
    for fact in facts:
        source = next(row for row in json.loads((ROOT / "master_topic_packs" / f"{fact['topic_id']}.json").read_text(encoding="utf-8"))["sources"] if row["source_id"] == fact["source_refs"][0]["source_id"])
        catalog[source["source_id"]] = {"source_url": source["source_url"], "version": source["version"],
                                        "content_sha256": fact["source_refs"][0]["source_sha256"],
                                        "fetch_status": "available", "extracted_text": " ".join(SIGNALS[fact["fact_id"]])}
    result = audit_catalog(ROOT, catalog)
    assert result["all_source_signals_match"] is True
    assert result["runtime_promotion_allowed"] is False
    assert all(not row["source_approved"] and not row["fact_approved"] for row in result["outcomes"])
    catalog[facts[0]["source_refs"][0]["source_id"]]["extracted_text"] = ""
    assert audit_catalog(ROOT, catalog)["all_source_signals_match"] is False
