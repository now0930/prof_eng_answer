"""Private S7 reviewer consensus audit: untrusted labels never become grades."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from grading.evidence.s7_independent_review_validation import (
    audit_two_reviewer_submissions,
)


def _docs():
    facts = ["valve_area", "baseline", "deadband", "v_model", "nyquist"]
    source_cards = [
        {"fact_id": f, "source_fact_id": f + "_verified",
         "source_statement": "private-source-sentence-" + f,
         "source_relation": {"subject": f, "predicate": "is",
                             "object": f + "_obj", "polarity": "positive",
                             "conditions": ["c_" + f] if f != "v_model" else []},
         "verification_refs": [{"authority_id": "test_only"}]}
        for f in facts
    ]
    items = [
        {"review_item_id": "secret-review-item-%03d" % n,
         "fact_id": facts[n // 2],
         "authored_draft_text": "PRIVATE ANSWER TEXT ITEM " + str(n),
         "expert_label": "",
         "condition_ids_explicitly_asserted": [],
         "condition_ids_missing_or_ambiguous": [],
         "disputed_claim_or_scope_notes": "",
         "expert_rationale": "", "reviewer_confidence": ""}
        for n in range(10)
    ]
    prompts = [
        {"fact_id": f, "new_correct_paraphrase": "",
         "new_wrong_relation_or_direction": "",
         "new_missing_condition_case": "",
         "new_ambiguous_or_quoted_statement": "",
         "sources_or_assumptions": ""}
        for f in facts
    ]
    packet = {
        "schema_version": "s7_independent_expert_packet.v1",
        "reviewer_id": "", "review_date": "",
        "reviewer_affiliation_or_domain": "",
        "evaluation_status": "AWAITING_INDEPENDENT_REVIEW",
        "source_inventory_execution_sha": "unit-test-head",
        "score_admission": "DISABLED", "score_effect": "none",
        "allowed_expert_labels": [
            "RELATION_WITH_REQUIRED_CONDITIONS",
            "RELATION_BUT_CONDITIONS_MISSING",
            "CONTRADICTORY_RELATION",
            "UNDETERMINED_OR_OUT_OF_SCOPE",
        ],
        "source_cards": source_cards,
        "items_to_adjudicate": items,
        "independently_authored_challenge_requests": prompts,
    }
    a, b = deepcopy(packet), deepcopy(packet)
    for reviewer, doc in (("reviewer-A-pseudonym", a),
                          ("reviewer-B-pseudonym", b)):
        doc["reviewer_id"] = reviewer
        doc["review_date"] = "2026-11-17"
        doc["reviewer_affiliation_or_domain"] = "Test-only independent field"
        doc["evaluation_status"] = "COMPLETE_BY_INDEPENDENT_REVIEWER"
        for item in doc["items_to_adjudicate"]:
            fid = item["fact_id"]
            item["expert_label"] = "RELATION_WITH_REQUIRED_CONDITIONS"
            item["condition_ids_explicitly_asserted"] = (
                ["c_" + fid] if fid != "v_model" else []
            )
            item["disputed_claim_or_scope_notes"] = "No dispute documented in fixture"
            item["expert_rationale"] = "Test fixture rationale, not real expert evidence"
            item["reviewer_confidence"] = "MEDIUM"
    return packet, a, b


def test_two_complete_mock_reviews_are_only_agreement_not_ground_truth():
    source, a, b = _docs()
    report = audit_two_reviewer_submissions(source, a, b)
    assert report["reviewed_draft_count"] == 10
    assert report["matching_relation_labels"] == 10
    assert report["matching_condition_coverage"] == 10
    assert report["disagreement_count"] == 0
    assert report["status"] == (
        "TWO_REVIEWER_AGREEMENT_INDEPENDENCE_NOT_AUTHENTICATED"
    )
    assert report["human_identity_independence_verified"] is False
    assert report["expert_benchmark_ready"] is False
    assert report["scorer_accuracy"] is None
    assert report["scorer_precision"] is None
    assert report["scorer_recall"] is None
    assert report["score_admission"] == "DISABLED"
    assert report["candidate_decision"] == "HOLD"
    assert report["automatic_alias_admission"] is False
    public = json.dumps(report)
    assert "PRIVATE ANSWER" not in public
    assert "private-source-sentence" not in public
    assert "expert_rationale" not in public
    assert "reviewer-A-pseudonym" not in public


def test_label_or_condition_disagreement_remains_manual_hold():
    source, a, b = _docs()
    b["items_to_adjudicate"][0].update({
        "expert_label": "RELATION_BUT_CONDITIONS_MISSING",
        "condition_ids_explicitly_asserted": [],
        "condition_ids_missing_or_ambiguous": ["c_valve_area"],
    })
    report = audit_two_reviewer_submissions(source, a, b)
    assert report["status"] == "TWO_REVIEWER_DISAGREEMENT_MANUAL_RECONCILIATION"
    assert report["matching_relation_labels"] == 9
    assert report["matching_condition_coverage"] == 9
    assert report["disagreement_count"] == 1
    assert report["disagreements"][0]["requires_manual_reconciliation"]
    assert report["expert_benchmark_ready"] is False


@pytest.mark.parametrize("mutation", [
    "same_reviewer", "missing_label", "unknown_label", "wrong_condition_id",
    "missing_required_conditions", "contradictory_coverage",
    "altered_answer", "altered_fact", "deleted_case", "duplicate_case",
    "foreign_sha", "source_changed", "score_enabled", "author_key_injection",
    "invalid_date", "missing_rationale", "missing_dispute_notes",
    "bad_confidence", "unapproved_completion", "other_label_source",
])
def test_forged_or_incomplete_reviews_are_fail_closed(mutation):
    source, a, b = _docs()
    case = b["items_to_adjudicate"][0]
    if mutation == "same_reviewer":
        b["reviewer_id"] = a["reviewer_id"]
    elif mutation == "missing_label":
        case["expert_label"] = ""
    elif mutation == "unknown_label":
        case["expert_label"] = "AUTOMATICALLY_APPROVED"
    elif mutation == "wrong_condition_id":
        case["condition_ids_explicitly_asserted"] = ["fabricated"]
    elif mutation == "missing_required_conditions":
        case["condition_ids_explicitly_asserted"] = []
    elif mutation == "contradictory_coverage":
        case["condition_ids_missing_or_ambiguous"] = ["c_valve_area"]
    elif mutation == "altered_answer":
        case["authored_draft_text"] = "Modified answer text"
    elif mutation == "altered_fact":
        case["fact_id"] = "baseline"
    elif mutation == "deleted_case":
        b["items_to_adjudicate"].pop(0)
    elif mutation == "duplicate_case":
        b["items_to_adjudicate"].append(deepcopy(case))
    elif mutation == "foreign_sha":
        b["source_inventory_execution_sha"] = "old-head"
    elif mutation == "source_changed":
        b["source_cards"][0]["source_statement"] = "surreptitiously changed"
    elif mutation == "score_enabled":
        b["score_admission"] = "ENABLED"
    elif mutation == "author_key_injection":
        case["author_side"] = "authored_positive"
    elif mutation == "invalid_date":
        b["review_date"] = "2026-02-31"
    elif mutation == "missing_rationale":
        case["expert_rationale"] = ""
    elif mutation == "missing_dispute_notes":
        case["disputed_claim_or_scope_notes"] = ""
    elif mutation == "bad_confidence":
        case["reviewer_confidence"] = "100%"
    elif mutation == "unapproved_completion":
        b["evaluation_status"] = "AUTO_APPROVED"
    else:
        b["allowed_expert_labels"] = ["EVERYTHING_IS_RIGHT"]
    with pytest.raises((ValueError, KeyError, TypeError)):
        audit_two_reviewer_submissions(source, a, b)


def test_unresolved_and_false_relations_can_be_explicitly_recorded():
    source, a, b = _docs()
    for doc in (a, b):
        doc["items_to_adjudicate"][1].update({
            "expert_label": "CONTRADICTORY_RELATION",
            "condition_ids_explicitly_asserted": [],
        })
        doc["items_to_adjudicate"][2].update({
            "expert_label": "UNDETERMINED_OR_OUT_OF_SCOPE",
            "condition_ids_explicitly_asserted": [],
        })
    report = audit_two_reviewer_submissions(source, a, b)
    assert report["matching_relation_labels"] == 10
    assert report["expert_benchmark_ready"] is False


def test_private_review_tool_is_not_run_from_actions():
    workflow = (Path(__file__).resolve().parents[1] /
                ".github/workflows/validation.yml").read_text(encoding="utf-8")
    assert "audit_s7_private_expert_reviews.py" not in workflow
    assert "prepare_s7_private_expert_review_packet.py" not in workflow
