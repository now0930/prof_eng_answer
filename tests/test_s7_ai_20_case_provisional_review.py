"""S7 20 AI-authored research proposals: provisional verdicts are NOT truth."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

from grading.evidence.s7_ai_candidate_integrity_gate import (
    EXPECTED_TYPES,
    SCOPE,
)

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "calibration" / "s7_ai_20_case_provisional_review_v1.json"
REWRITES = {
    "effective_unbalanced_area_ai_03",
    "effective_unbalanced_area_ai_04",
    "sw06_baseline_approved_reference_ai_03",
    "deadband_definition_direction_reversal_ai_03",
    "sw04_v_model_definition_ai_03",
    "nyquist_contour_and_mapping_ai_03",
}


def _read():
    return json.loads(FILE.read_text(encoding="utf-8"))


def test_provisional_review_has_all_five_by_four_without_any_admitted_labels():
    d = _read()
    assert d["schema_version"] == "s7_ai_20_case_provisional_review.v1"
    assert d["status"] == "SOURCE_ASSISTED_SINGLE_MODEL_PRELIMINARY_REVIEW_ONLY"
    assert d["provenance"] == "SAME_AI_MODEL_AS_GENERATOR_NOT_INDEPENDENT_ADJUDICATION"
    assert d["source_inventory_execution_sha"] == (
        "7409e045c6837b818cafc110b507679b896d06ab"
    )
    assert d["candidate_count"] == len(d["cases"]) == 20
    assert set(SCOPE) == {r["fact_id"] for r in d["cases"]}
    assert d["retained_research_only"] == 14
    assert d["rewrite_required"] == 6
    assert d["expert_adjudicated_count"] == 0
    assert d["expert_benchmark_ready"] is False
    assert d["independent_holdout_admission"] == "PROHIBITED"
    assert d["candidate_decision"] == "HOLD"
    assert d["score_admission"] == "DISABLED"
    assert d["automatic_alias_admission"] is False
    by_id = {row["candidate_id"]: row for row in d["cases"]}
    assert len(by_id) == 20
    assert set(by_id) == {
        f"{fact_id}_ai_{i:02}"
        for fact_id in SCOPE for i in EXPECTED_TYPES
    }
    expected_decisions = {
        "RETAIN_RESEARCH_ONLY": 14,
        "REWRITE_REQUIRED": 6,
    }
    assert Counter(row["provisional_decision"] for row in d["cases"]) == (
        expected_decisions
    )
    assert {
        r["candidate_id"] for r in d["cases"]
        if r["provisional_decision"] == "REWRITE_REQUIRED"
    } == REWRITES
    for row in d["cases"]:
        fact_id = row["fact_id"]
        case_no = int(row["candidate_id"].rsplit("_", 1)[1])
        assert row["candidate_id"] == f"{fact_id}_ai_{case_no:02}"
        assert row["original_proposed_type"] == EXPECTED_TYPES[case_no]
        assert row["score_admission"] == "DISABLED"
        assert row["expert_label"] is None
        assert isinstance(row["review_issue_code"], str)
        assert row["review_issue_code"]


def test_v_model_cannot_masquerade_as_missing_required_condition():
    d = _read()
    assert SCOPE["sw04_v_model_definition"]["conditions"] == []
    case = next(r for r in d["cases"]
                if r["candidate_id"] == "sw04_v_model_definition_ai_03")
    assert case["original_proposed_type"] == "omitted_conditions"
    assert case["provisional_decision"] == "REWRITE_REQUIRED"
    assert case["review_issue_code"] == "INVALID_OMISSION_TYPE"
    assert case["expert_label"] is None


def test_partial_truth_cannot_be_treated_as_false_relation():
    rows = {r["candidate_id"]: r for r in _read()["cases"]}
    assert rows["nyquist_contour_and_mapping_ai_03"][
        "review_issue_code"
    ] == "PARTIAL_FREQUENCY_RESPONSE_TRUE"
    assert rows["effective_unbalanced_area_ai_03"][
        "review_issue_code"
    ] == "UNDERSPECIFIED_POSSIBLY_TRUE"
    assert rows["deadband_definition_direction_reversal_ai_03"][
        "review_issue_code"
    ] == "UNDERSPECIFIED_POSSIBLY_TRUE"
    assert all(row["expert_label"] is None for row in rows.values())


def test_review_metadata_has_no_private_draft_text_or_scoring_authority():
    d = _read()
    allowed = {
        "candidate_id", "fact_id", "original_proposed_type",
        "provisional_decision", "review_issue_code", "expert_label",
        "score_admission",
    }
    assert all(set(row) == allowed for row in d["cases"])
    public_text = FILE.read_text(encoding="utf-8")
    assert "ai_authored_text" not in public_text
    assert "positive_answer" not in public_text
    assert "adversarial_answer" not in public_text
    assert "source_statement" not in public_text
    assert "suggested_revision_ko" not in public_text
    assert "accuracy" not in d
    assert "score_effect" not in d


def test_research_review_cannot_implicitly_extend_actions_or_goldens():
    workflow = (ROOT / ".github/workflows/validation.yml").read_text(
        encoding="utf-8"
    )
    assert "s7_ai_20_case_provisional_review_v1" not in workflow
    assert "audit_s7_private_ai_candidates.py" not in workflow
