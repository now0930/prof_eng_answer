import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
ANCHOR = "eem_filter_not_offset_fix"


def test_filter_noise_anchor_matches_independently_verified_fact():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    pack = json.loads((ROOT / "rubrics/topic_packs" / TOPIC / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == ANCHOR)
    fact = next(row for row in registry["facts"] if row["topic_id"] == TOPIC and row["legacy_anchor_id"] == ANCHOR)
    assert fact["fact_id"] == "eem_filter_noise_suppression_does_not_calibrate_systematic_error"
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ADI_CHOPPER_AMPLIFIER_DC_AC_FILTER_SEPARATION",
        "ADI_DATA_CONVERTER_GAIN_REFERENCE_CALIBRATION",
    }
    assert all(ref["locator"] and ref["supports_claim"] for ref in fact["verification_refs"])
    assert "a_high_pass_that_rejects_dc_also_rejects_any_wanted_dc_signal_component" in fact["relation"]["conditions"]
