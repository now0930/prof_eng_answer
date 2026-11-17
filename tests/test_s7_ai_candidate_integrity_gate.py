"""S7 AI candidate pool must remain an unscored, non-independent dataset."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from grading.evidence.s7_ai_candidate_integrity_gate import (
    EXPECTED_TYPES, ROLE, SCOPE, quarantine_ai_candidate_pool,
)

ROOT = Path(__file__).resolve().parents[1]


def _sample():
    challenge = json.loads(
        (ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json")
        .read_text(encoding="utf-8")
    )
    source = {
        "schema_version": "s7_alias_registry_source_review.v1",
        "status": "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD",
        "inventory_execution_sha": "test-source-head",
        "score_admission": "DISABLED", "score_effect": "none",
        "projection_count_with_duplicates": 179,
        "unique_topic_fact_count": 119,
        "decision_counts": {"HOLD": 119, "ACCEPT": 0},
        "rows": [],
    }
    for fid, s in SCOPE.items():
        source["rows"].append({
            "owner_topic_id": s["owner"],
            "fact_id": fid,
            "source_fact_id": s["source_fact_id"],
            "relation": {
                "subject": s["subject"], "predicate": s["predicate"],
                "object": s["object"], "conditions": list(s["conditions"]),
                "polarity": "positive",
            },
            "review_decision": "HOLD",
            "candidate_alias": None,
            "registry_review_status": "approved",
            "registry_verification_status": "verified",
            "registry_verification_refs": [{"authority_id": "synthetic-fixture"}],
            "technical_equivalence_of_candidate": "NOT_ASSESSED",
            "score_effect": "none",
        })
    for n in range(114):
        source["rows"].append({
            "owner_topic_id": "unrelated-topic-%04d" % n,
            "fact_id": "unrelated-fact-%04d" % n,
        })
    ai = {
        "schema_version": "s7_ai_authored_holdout_candidates.v1",
        "source_head_sha": "test-source-head",
        "provenance": "AI_GENERATED_UNREVIEWED_NOT_INDEPENDENT_EXPERT_NOT_GOLDEN",
        "candidate_count": 20,
        "score_admission": "DISABLED",
        "cases": [],
    }
    for fid in SCOPE:
        for no, proposed_type in EXPECTED_TYPES.items():
            ai["cases"].append({
                "fact_id": fid,
                "case_no": no,
                "proposed_type": proposed_type,
                "review_status": "NEEDS_INDEPENDENT_EXPERT_LABEL",
                "text": "UNREVIEWED MOCK AI DRAFT %s %d" % (fid, no),
            })
    return source, ai, challenge


def test_quarantine_all_twenty_and_flag_one_structurally_impossible_condition_case():
    source, ai, challenge = _sample()
    r = quarantine_ai_candidate_pool(source, ai, challenge)
    assert r["status"] == "AI_CANDIDATES_QUARANTINED_NOT_EXPERT_BENCHMARK"
    assert r["candidate_count"] == 20
    assert r["candidate_role"] == ROLE
    assert r["candidate_type_counts"] == {
        "ambiguous_or_quoted": 5,
        "contrary_relation": 5,
        "omitted_conditions": 5,
        "technically_consistent": 5,
    }
    assert r["source_condition_ids_total_across_five_facts"] == 8
    assert r["structurally_flagged_count"] == 1
    assert r["flag_counts"] == {
        "NO_SOURCE_CONDITIONS_TO_OMIT_RETAG_OR_REWRITE": 1
    }
    flagged = [x for x in r["rows"] if x["research_quality_flags"]]
    assert len(flagged) == 1
    assert flagged[0]["candidate_id"] == "sw04_v_model_definition_ai_03"
    assert flagged[0]["review_status"] == "STRUCTURAL_RETAG_OR_REWRITE_REQUIRED"
    assert flagged[0]["source_required_condition_count"] == 0
    assert r["independently_validated_count"] == 0
    assert r["independent_test_set_admission"] == "PROHIBITED"
    assert r["expert_benchmark_ready"] is False
    assert r["parser_accuracy"] is None
    assert r["candidate_decision"] == "HOLD"
    assert r["automatic_alias_admission"] is False
    assert r["score_admission"] == "DISABLED"
    assert all(x["score_effect"] == "none" for x in r["rows"])
    assert all(x["independently_validated_label"] is None for x in r["rows"])
    raw = json.dumps(r, ensure_ascii=False)
    assert "UNREVIEWED MOCK AI DRAFT" not in raw
    assert "authored_draft_text" not in raw
    assert "source_statement" not in raw


@pytest.mark.parametrize("mutation", [
    "source_sha", "source_admission", "source_not_hold", "source_accepted",
    "source_deleted", "source_relation", "source_conditions", "source_unverified",
    "source_refs_missing", "source_alias_accepted", "source_score",
    "ai_wrong_head", "ai_false_provenance", "ai_scoring", "ai_count",
    "ai_duplicate_identity", "ai_wrong_case_no", "ai_unknown_fact",
    "ai_wrong_type", "ai_preapproved", "ai_no_text",
    "author_label_changed", "author_score_enabled", "author_wrong_schema",
])
def test_source_or_candidate_authority_and_identity_drift_fails_closed(mutation):
    source, ai, challenge = _sample()
    if mutation == "source_sha":
        source["inventory_execution_sha"] = "other"
    elif mutation == "source_admission":
        source["score_admission"] = "ENABLED"
    elif mutation == "source_not_hold":
        source["decision_counts"]["HOLD"] = 118
    elif mutation == "source_accepted":
        source["rows"][0]["review_decision"] = "ACCEPT"
    elif mutation == "source_deleted":
        source["rows"].pop()
    elif mutation == "source_relation":
        source["rows"][0]["relation"]["subject"] = "foreign-subject"
    elif mutation == "source_conditions":
        source["rows"][0]["relation"]["conditions"] = []
    elif mutation == "source_unverified":
        source["rows"][0]["registry_verification_status"] = "unverified"
    elif mutation == "source_refs_missing":
        source["rows"][0]["registry_verification_refs"] = []
    elif mutation == "source_alias_accepted":
        source["rows"][0]["candidate_alias"] = "AUTO"
    elif mutation == "source_score":
        source["rows"][0]["score_effect"] = "credit"
    elif mutation == "ai_wrong_head":
        ai["source_head_sha"] = "other"
    elif mutation == "ai_false_provenance":
        ai["provenance"] = "INDEPENDENT_EXPERT_ADJUDICATED"
    elif mutation == "ai_scoring":
        ai["score_admission"] = "ENABLED"
    elif mutation == "ai_count":
        ai["cases"].pop()
    elif mutation == "ai_duplicate_identity":
        ai["cases"].append(deepcopy(ai["cases"][0]))
    elif mutation == "ai_wrong_case_no":
        ai["cases"][0]["case_no"] = 7
    elif mutation == "ai_unknown_fact":
        ai["cases"][0]["fact_id"] = "wrong-fact"
    elif mutation == "ai_wrong_type":
        ai["cases"][0]["proposed_type"] = "independently_correct"
    elif mutation == "ai_preapproved":
        ai["cases"][0]["review_status"] = "APPROVED"
    elif mutation == "ai_no_text":
        ai["cases"][0]["text"] = ""
    elif mutation == "author_label_changed":
        next(c for c in challenge["cases"] if c["fact_id"] in SCOPE)[
            "positive_label"
        ] = "EXPERT_VERIFIED"
    elif mutation == "author_score_enabled":
        challenge["score_admission"] = "ENABLED"
    else:
        challenge["schema_version"] = "unknown"
    with pytest.raises((KeyError, ValueError)):
        quarantine_ai_candidate_pool(source, ai, challenge)


def test_original_author_draft_exact_copy_stays_quarantined_and_flagged():
    source, ai, challenge = _sample()
    target = next(c for c in challenge["cases"]
                  if c["fact_id"] == ai["cases"][0]["fact_id"])
    ai["cases"][0]["text"] = target["positive_answer"]
    r = quarantine_ai_candidate_pool(source, ai, challenge)
    assert r["flag_counts"]["EXACT_COPY_OF_ORIGINAL_AUTHOR_DRAFT_REVIEW"] == 1
    assert r["independent_test_set_admission"] == "PROHIBITED"


def test_repeated_ai_draft_text_flagged_not_auto_deduplicated_into_truth():
    source, ai, challenge = _sample()
    ai["cases"][1]["text"] = ai["cases"][0]["text"]
    r = quarantine_ai_candidate_pool(source, ai, challenge)
    assert r["flag_counts"]["DUPLICATE_AI_TEXT_REVIEW"] == 1
    assert r["candidate_count"] == 20
    assert r["parser_accuracy"] is None


def test_private_candidate_cli_is_not_in_the_actions_workflow():
    workflow = (ROOT / ".github/workflows/validation.yml").read_text(
        encoding="utf-8"
    )
    assert "audit_s7_private_ai_candidates.py" not in workflow
    assert "ai_generated_holdout_candidates.json" not in workflow
