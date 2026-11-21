"""S7 six revised private draft candidates: metadata only, no scoring promotion."""
from __future__ import annotations

import json
from pathlib import Path

from grading.evidence.s7_remaining_five_expert_queue import SCOPE


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "calibration/s7_six_ai_candidate_revision_manifest_v1.json"
PREVIOUS = ROOT / "calibration/s7_ai_20_case_provisional_review_v1.json"
EXPECTED = {
    "effective_unbalanced_area_ai_03": (
        "CONDITION_SCOPE_UNSPECIFIED", "ACTUAL_PRESSURE_GEOMETRY_NOT_SPECIFIED"
    ),
    "effective_unbalanced_area_ai_04": (
        "HYPOTHETICAL_QUOTE_UNVERIFIED", "NO_CLAIM_OF_REAL_UNSOURCED_DOCUMENT"
    ),
    "sw06_baseline_approved_reference_ai_03": (
        "CONDITION_SCOPE_UNSPECIFIED", "APPROVAL_AND_IDENTIFICATION_UNASSERTED"
    ),
    "deadband_definition_direction_reversal_ai_03": (
        "PARTIAL_TRUE_TEST_SCOPE_UNSPECIFIED", "PARTIAL_DEFINITION_IS_NOT_CONTRADICTION"
    ),
    "sw04_v_model_definition_ai_03": (
        "RELATION_MAPPING_UNSPECIFIED", "NO_SOURCE_CONDITION_IDS_TO_OMIT"
    ),
    "nyquist_contour_and_mapping_ai_03": (
        "PARTIAL_TRUE_FULL_CONTOUR_UNSPECIFIED", "FREQUENCY_PLOT_PARTIAL_TRUTH"
    ),
}


def _load():
    return (
        json.loads(MANIFEST.read_text(encoding="utf-8")),
        json.loads(PREVIOUS.read_text(encoding="utf-8")),
    )


def test_six_rewrites_match_all_six_previous_rewrite_required_cases():
    rev, previous = _load()
    assert rev["schema_version"] == "s7_six_ai_candidate_revision_manifest.v1"
    assert rev["parent_provisional_review_schema"] == previous["schema_version"]
    assert rev["source_inventory_execution_sha"] == previous["source_inventory_execution_sha"]
    assert rev["candidate_revised_count"] == len(rev["cases"]) == 6
    assert rev["other_candidates_unchanged_count"] == 14
    earlier = {
        r["candidate_id"]: r for r in previous["cases"]
        if r["provisional_decision"] == "REWRITE_REQUIRED"
    }
    actual = {r["candidate_id"]: r for r in rev["cases"]}
    assert len(earlier) == len(actual) == 6
    assert set(actual) == set(earlier) == set(EXPECTED)
    for case_id, row in actual.items():
        assert row["fact_id"] == earlier[case_id]["fact_id"]
        assert row["previous_decision"] == "REWRITE_REQUIRED"
        assert (
            row["proposed_research_role"], row["change_reason_code"]
        ) == EXPECTED[case_id]
        assert row["source_required_condition_count"] == len(
            SCOPE[row["fact_id"]]["conditions"]
        )


def test_v_model_zero_conditions_cannot_be_recast_as_omitted_condition():
    rev, _ = _load()
    by_id = {r["candidate_id"]: r for r in rev["cases"]}
    assert SCOPE["sw04_v_model_definition"]["conditions"] == []
    row = by_id["sw04_v_model_definition_ai_03"]
    assert row["source_required_condition_count"] == 0
    assert row["proposed_research_role"] == "RELATION_MAPPING_UNSPECIFIED"
    assert row["change_reason_code"] == "NO_SOURCE_CONDITION_IDS_TO_OMIT"


def test_partial_true_nyquist_and_deadband_not_auto_false():
    rev, _ = _load()
    by_id = {r["candidate_id"]: r for r in rev["cases"]}
    assert by_id["nyquist_contour_and_mapping_ai_03"]["proposed_research_role"] == (
        "PARTIAL_TRUE_FULL_CONTOUR_UNSPECIFIED"
    )
    assert by_id["deadband_definition_direction_reversal_ai_03"][
        "proposed_research_role"
    ] == "PARTIAL_TRUE_TEST_SCOPE_UNSPECIFIED"
    assert all(x["independent_truth_label"] is None for x in by_id.values())
    assert all(not x["parser_output_extraction_checked"] for x in by_id.values())


def test_research_manifest_is_never_admitted_as_ground_truth_or_grade():
    rev, _ = _load()
    assert rev["status"] == "SIX_REVISED_PRIVATE_DRAFTS_NOT_EXPERT_VALIDATED"
    assert rev["authoring_provenance"] == "SINGLE_AI_MODEL_REVISED_AI_GENERATED_TEST_CANDIDATES"
    assert rev["independent_expert_review_count"] == 0
    assert rev["independent_holdout_admission"] == "PROHIBITED"
    assert rev["score_admission"] == "DISABLED"
    assert rev["candidate_decision"] == "HOLD"
    assert rev["automatic_alias_admission"] is False
    assert rev["original_fact_anchor_modified"] is False
    assert rev["original_texts_in_repo"] is False
    assert rev["revised_texts_in_repo"] is False
    for row in rev["cases"]:
        assert row["revision_state"] == "PRIVATE_AI_DRAFT_REVISED_NOT_EXPERT_VALIDATED"
        assert row["score_effect"] == "none"
        assert row["source_conditions_proven_from_answer"] == 0
    serialized = MANIFEST.read_text(encoding="utf-8")
    for forbidden in (
        '"revised_text"', '"original_text"', '"expert_label": "',
        '"candidate_alias"', '"answer_text"', '"source_statement"',
    ):
        assert forbidden not in serialized


def test_private_six_case_texts_not_uploaded_to_actions_or_raw_repo_fixtures():
    workflow = (ROOT / ".github/workflows/validation.yml").read_text(
        encoding="utf-8"
    )
    for forbidden in (
        "s7_private_six_revised_candidates",
        "s7_six_rewrite_before_after_private_review",
        "audit_s7_private_expert_reviews.py",
    ):
        assert forbidden not in workflow
