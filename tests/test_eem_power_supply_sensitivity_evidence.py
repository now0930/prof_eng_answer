import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
ANCHOR = "eem_power_supply_sensitivity"


def test_power_supply_sensitivity_anchor_matches_source_scoped_fact():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    pack = json.loads((ROOT / "rubrics/topic_packs" / TOPIC / "fact_anchor.json").read_text())
    anchor = next(row for row in pack["anchors"] if row["anchor_id"] == ANCHOR)
    fact = next(row for row in registry["facts"] if row["topic_id"] == TOPIC and row["legacy_anchor_id"] == ANCHOR)
    assert fact["fact_id"] == "eem_power_supply_and_reference_disturbance_can_propagate_to_measurement_output"
    assert fact["statement"] == anchor["statement"]
    assert fact["verification_status"] == "verified"
    assert fact["review_status"] == "approved"
    assert fact["score_effect"] == "none"
    assert fact["source_refs"] == []
    assert {ref["authority_id"] for ref in fact["verification_refs"]} == {
        "ADI_SIGNAL_CHAIN_POWER_SUPPLY_NOISE_SENSITIVITY",
        "ADI_SENSOR_EXCITATION_RATIOMETRIC_MEASUREMENT",
        "ADI_ADC_REFERENCE_NOISE_AND_ERROR",
        "NI_GROUND_POTENTIAL_DIFFERENCE_MEASUREMENT_ERROR",
    }
    assert all(ref["locator"] and ref["supports_claim"] for ref in fact["verification_refs"])
    assert "this_claim_does_not_assert_that_all_supply_noise_is_transferred_without_attenuation" in fact["relation"]["conditions"]
