import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC = "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"


def test_verified_mcdc_definition_anchors_match_pack_and_faa_evidence():
    registry = json.loads((ROOT / "grading/evidence/approved_fact_registry.json").read_text())
    facts = {
        row["legacy_anchor_id"]: row
        for row in registry["facts"]
        if row["topic_id"] == TOPIC
    }
    pack = json.loads((ROOT / "rubrics/topic_packs" / TOPIC / "fact_anchor.json").read_text())
    anchors = {row["anchor_id"]: row for row in pack["anchors"]}

    expected = {
        "mcdc_dynamic_analysis_relation": "mcdc_dynamic_test_evidence_requires_oracle_and_traceability",
        "mcdc_structural_vs_requirements_coverage": "mcdc_structural_and_requirement_coverage_are_complementary",
        "mcdc_deactivated_code": "mcdc_deactivated_code_is_configuration_scoped_inactive_code",
        "mcdc_multiple_condition_coverage": "mcdc_mcc_exercises_all_condition_combinations",
        "mcdc_independent_effect_pair": "mcdc_independence_pair_changes_decision_via_target_effect",
        "mcdc_masked_inactive_condition": "mcdc_inactive_boolean_branch_masks_other_condition_effect",
        "mcdc_requirements_based_testing_first": "mcdc_structural_coverage_complements_requirements_based_tests",
        "mcdc_unique_cause": "mcdc_unique_cause_pair_holds_other_conditions_fixed",
        "mcdc_masking": "mcdc_masking_allows_non_target_changes_when_effect_masked",
        "mcdc_n_plus_one_limit": "mcdc_n_plus_one_test_count_is_not_universal",
        "mcdc_coupled_conditions": "mcdc_condition_coupling_can_invalidate_unique_cause_pairs",
        "mcdc_coverage_analysis_workflow": "mcdc_coverage_analysis_traces_artifacts_and_disposes_uncovered_structure",
        "mcdc_uncovered_code_disposition": "uncovered_structural_code_is_analyzed_and_its_disposition_recorded",
        "mcdc_static_analysis_relation": "static_analysis_complements_but_does_not_supply_execution_coverage_evidence",
        "mcdc_dead_code": "unneeded_dead_code_is_removed_or_its_residual_risk_justified",
        "mcdc_source_object_coverage": "source_object_coverage_equivalence_is_analyzed_when_generated_code_changes_structure",
        "mcdc_coverage_tool_qualification": "coverage_tool_assurance_depends_on_tool_use_and_unverified_output_risk",
        "mcdc_compiler_optimization": "compiler_generated_object_structure_can_differ_from_source_decision_structure",
        "mcdc_instrumentation_effect": "coverage_instrumentation_can_add_runtime_overhead_and_change_observed_execution",
        "mcdc_short_circuit": "short_circuit_evaluation_can_mask_unexecuted_boolean_conditions",
        "mcdc_target_environment": "coverage_test_environment_represents_target_hardware_and_timing_conditions",
        "mcdc_lifecycle_vv_boundary": "structural_mcdc_coverage_is_one_vv_evidence_not_a_lifecycle_substitute",
        "mcdc_defensive_code": "safety_error_handling_behavior_is_requirement_traced_and_tested",
        "mcdc_control_data_flow_complement": "mcdc_decision_coverage_does_not_replace_other_data_timing_and_boundary_analyses",
        "mcdc_regression_change": "software_changes_trigger_regression_and_coverage_impact_review",
    }
    for anchor_id, fact_id in expected.items():
        fact = facts[anchor_id]
        assert fact["fact_id"] == fact_id
        assert fact["verification_status"] == "verified"
        assert fact["review_status"] == "approved"
        assert fact["score_effect"] == "none"
        assert fact["statement"] == anchors[anchor_id]["statement"]
        refs = fact["verification_refs"]
        assert refs
        assert all(
            "faa.gov" in ref["url"]
            or "ntrs.nasa.gov" in ref["url"]
            or "swehb.nasa.gov" in ref["url"]
            or "nodis3.gsfc.nasa.gov" in ref["url"]
            for ref in refs
        )
        assert all(ref["authority_type"] in {"official_documentation", "primary_research"} for ref in refs)
