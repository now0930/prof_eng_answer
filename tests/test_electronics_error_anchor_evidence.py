import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC = "electronics_error_noise_drift_tolerance_aging_power_mitigation"


def test_verified_adc_error_anchors_match_pack_and_have_direct_authority_evidence():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    facts = {
        row["legacy_anchor_id"]: row
        for row in registry["facts"]
        if row["topic_id"] == TOPIC
    }
    pack = json.loads((ROOT / "rubrics/topic_packs" / TOPIC / "fact_anchor.json").read_text())
    anchors = {row["anchor_id"]: row for row in pack["anchors"]}

    expected = {
        "eem_adc_resolution_accuracy": "eem_adc_resolution_accuracy_distinction",
        "eem_adc_quantization": "eem_adc_quantization_vs_accuracy",
        "eem_adc_aliasing_boundary": "eem_adc_aliasing_distinct_from_quantization",
        "eem_noise_bandwidth": "eem_measurement_noise_bandwidth_response_tradeoff",
        "eem_filter_noise_mitigation": "eem_filter_noise_reduction_phase_and_settling_limits",
        "eem_psrr": "eem_psrr_frequency_and_condition_dependence",
        "eem_linearity_error": "eem_adc_transfer_linearity_residual_after_offset_gain",
        "eem_random_noise": "eem_signal_chain_noise_sources_and_bandwidth",
        "eem_rss_worstcase": "eem_uncertainty_combination_respects_correlation",
        "eem_reference_error": "eem_reference_accuracy_drift_noise_load_contributors",
        "eem_offset_error": "eem_adc_offset_error_transfer_intercept_and_circuit_sources",
        "eem_gain_error": "eem_signal_chain_gain_error_sources",
        "eem_error_classification": "eem_measurement_error_classification_systematic_random_drift",
        "eem_calibration_interval": "eem_recalibration_interval_risk_history_and_cost_basis",
        "eem_tolerance_definition": "eem_component_tolerance_distinct_from_operating_drift",
        "eem_temperature_coefficient": "eem_temperature_coefficient_circuit_error_budget_contributors",
        "eem_tolerance_propagation": "eem_tolerance_sensitivity_propagation_and_budgeting",
        "eem_error_budget": "eem_error_budget_common_reference_and_dominant_terms",
        "eem_aging_definition": "eem_aging_parameter_stability_over_time_and_stress",
        "eem_calibration_systematic": "eem_calibration_corrects_measured_bias_not_future_performance",
        "eem_snr_dynamic_range": "eem_snr_dynamic_range_noise_floor_vs_nominal_bits",
    }
    for anchor_id, fact_id in expected.items():
        fact = facts[anchor_id]
        assert fact["fact_id"] == fact_id
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert fact["statement"] == anchors[anchor_id]["statement"]
        assert fact["verification_refs"]
        assert all(ref["authority_type"] in {"official_documentation", "standard", "textbook", "peer_reviewed", "primary_research", "other_authoritative", "calculation"} for ref in fact["verification_refs"])
