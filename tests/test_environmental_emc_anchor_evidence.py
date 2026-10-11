import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC = "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification"


def test_verified_emc_qualification_anchors_match_source_scoped_facts():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    topic = json.loads((ROOT / "rubrics/topic_packs" / TOPIC / "fact_anchor.json").read_text())
    facts = {
        row["legacy_anchor_id"]: row
        for row in registry["facts"]
        if row["topic_id"] == TOPIC
    }
    anchors = {row["anchor_id"]: row for row in topic["anchors"]}
    expected = {
        "ieeq_emission_immunity_distinction": "ieeq_emission_and_immunity_are_distinct_emc_evidence",
        "ieeq_emc_test_categories": "ieeq_emc_test_families_are_selected_by_applicable_requirement",
        "ieeq_test_setup_representative": "ieeq_emc_test_configuration_is_documented_and_method_specific",
        "ieeq_acceptance_criteria_predefined": "ieeq_qualification_acceptance_criteria_precede_test",
        "ieeq_temperature_transition_boundary": "ieeq_environmental_temperature_profile_is_tailored_not_universal",
        "ieeq_uncertainty_margin": "ieeq_emc_measurement_uncertainty_is_considered_in_test_results",
        "ieeq_measurement_instrument_control": "ieeq_emc_method_calibration_and_setup_are_standard_specific",
        "ieeq_standard_edition_policy": "ieeq_standard_applicability_and_levels_follow_product_requirements",
        "ieeq_qualification_vs_field_troubleshooting": "ieeq_emc_standardized_tests_are_not_in_situ_diagnostics",
        "ieeq_vibration_sine_random": "ieeq_vibration_test_method_is_selected_from_environment",
        "ieeq_condensation_condition": "ieeq_humidity_test_condensation_condition_is_method_specific",
        "ieeq_emc_emi_distinction": "ieeq_emc_and_emi_distinguish_compatibility_from_disturbance",
    }
    assert len(expected) == 12
    for anchor_id, fact_id in expected.items():
        fact = facts[anchor_id]
        assert fact["fact_id"] == fact_id
        assert fact["statement"] == anchors[anchor_id]["statement"]
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert fact["source_refs"] == []
        assert fact["verification_refs"]
        assert all(ref["authority_type"] == "official_documentation" for ref in fact["verification_refs"])
        assert all(ref["supports_claim"] and ref["locator"] for ref in fact["verification_refs"])
    category_refs = {ref["authority_id"] for ref in facts["ieeq_emc_test_categories"]["verification_refs"]}
    assert {
        "IEC_61000_4_2_ESD_TEST",
        "IEC_61000_4_3_RADIATED_RF_IMMUNITY",
        "IEC_61000_4_4_EFT_BURST_IMMUNITY",
        "IEC_61000_4_5_SURGE_IMMUNITY",
        "IEC_61000_4_6_CONDUCTED_RF_IMMUNITY",
        "IEC_61000_4_8_POWER_FREQUENCY_MAGNETIC_IMMUNITY",
        "IEC_61000_4_11_VOLTAGE_DIP_IMMUNITY",
        "IEC_61000_6_8_CONDUCTED_RADIATED_EMISSIONS",
    } <= category_refs


def test_unreviewed_operating_mode_anchor_remains_unverified():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    fact = next(
        row for row in registry["facts"]
        if row["topic_id"] == TOPIC and row["legacy_anchor_id"] == "ieeq_operating_mode_worst_case"
    ) if any(
        row["topic_id"] == TOPIC and row["legacy_anchor_id"] == "ieeq_operating_mode_worst_case"
        for row in registry["facts"]
    ) else None
    assert fact is None
