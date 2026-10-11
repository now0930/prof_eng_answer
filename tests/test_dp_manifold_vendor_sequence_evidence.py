import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC = "dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation"


def test_rosemount_three_valve_sequences_are_vendor_scoped_and_source_backed():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    facts = {row["legacy_anchor_id"]: row for row in registry["facts"] if row["topic_id"] == TOPIC}
    pack = json.loads((ROOT / "rubrics/topic_packs" / TOPIC / "fact_anchor.json").read_text())
    anchors = {row["anchor_id"]: row for row in pack["anchors"]}

    expected = {
        "manifold_isolation_sequence": "rosemount_2051_three_valve_zero_check_isolation_side_sequence",
        "manifold_return_sequence": "rosemount_2051_three_valve_zero_check_return_sequence",
    }
    for anchor_id, fact_id in expected.items():
        fact = facts[anchor_id]
        anchor = anchors[anchor_id]
        assert fact["fact_id"] == fact_id
        assert fact["verification_status"] == "verified"
        assert fact["score_effect"] == "none"
        assert fact["statement"] == anchor["statement"]
        assert len(fact["verification_refs"]) == 1
        assert fact["verification_refs"][0]["authority_id"] == "EMERSON_ROSEMOUNT_2051_3_VALVE_OPERATION"
        assert "claim_is_scoped_to_rosemount_2051_three_valve_configuration" in fact["relation"]["conditions"]

    assert "bleed valve" in anchors["manifold_isolation_sequence"]["statement"]
    assert "H/L isolation open, equalizing closed" in anchors["manifold_return_sequence"]["statement"]
