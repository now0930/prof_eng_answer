import json
from pathlib import Path

from grading.evidence.fact_grounded_contracts import legacy_anchor_index, validate_fact


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "fact_grounded_representative_candidates_20261010.json"


def test_representative_candidates_are_source_bound_but_not_approved():
    payload = json.loads(REPORT.read_text(encoding="utf-8"))
    assert len(payload["facts"]) == 3
    for fact in payload["facts"]:
        validate_fact(fact)
        assert fact["review_status"] == "candidate"
        assert fact["score_effect"] == "none"
        assert fact["legacy_anchor_id"] in legacy_anchor_index(ROOT, fact["topic_id"])["anchor_ids"]
        master = json.loads((ROOT / "master_topic_packs" / f"{fact['topic_id']}.json").read_text(encoding="utf-8"))
        source = next(row for row in master["sources"] if row["source_id"] == fact["source_refs"][0]["source_id"])
        assert source["version"] == fact["source_refs"][0]["source_version"]
        assert source["verification_status"] == "unverified"
