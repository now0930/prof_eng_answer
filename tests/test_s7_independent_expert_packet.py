"""Private S7 reviewer packet: label leakage, crosswalk and authority guards."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from grading.evidence.s7_independent_expert_packet import (
    _sha256_manifest, prepare_private_expert_review_packet,
)
from grading.evidence.s7_remaining_five_expert_queue import SCOPE

ROOT = Path(__file__).resolve().parents[1]


def _sample():
    fixture = json.loads(
        (ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json")
        .read_text(encoding="utf-8")
    )
    src = {
        "schema_version": "s7_alias_registry_source_review.v1",
        "status": "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD",
        "score_admission": "DISABLED", "score_effect": "none",
        "inventory_execution_sha": "test-only-sha",
        "rows": [],
    }
    queue = {
        "schema_version": "s7_remaining_five_expert_queue.v1",
        "status": "FIVE_UNPROBED_FACTS_QUEUED_FOR_INDEPENDENT_REVIEW",
        "score_admission": "DISABLED", "score_effect": "none",
        "candidate_decision": "HOLD",
        "automatic_alias_admission": False,
        "source_inventory_execution_sha": "test-only-sha",
        "execution_commit_sha": "test-only-sha",
        "queued_fact_count": 5, "authored_draft_answer_count": 10,
        "independently_labeled_answer_count": 0,
        "rows": [],
    }
    for case in fixture["cases"]:
        fid = case["fact_id"]
        if fid not in SCOPE:
            continue
        spec = SCOPE[fid]
        src["rows"].append({
            "owner_topic_id": spec["owner"], "fact_id": fid,
            "source_fact_id": spec["source_fact_id"],
            "source_statement": "Fixture-only verified relation " + fid,
            "relation": {
                "subject": spec["subject"], "predicate": spec["predicate"],
                "object": spec["object"],
                "polarity": "positive", "conditions": spec["conditions"],
            },
            "registry_review_status": "approved",
            "registry_verification_status": "verified",
            "registry_verification_refs": [{
                "authority_id": "TEST_ONLY_AUTHORITY",
                "citation": "synthetic fixture",
                "locator": "fixture reference",
                "url": None,
            }],
            "review_decision": "HOLD",
            "candidate_alias": None,
        })
        queue["rows"].append({
            "owner_topic_id": spec["owner"], "fact_id": fid,
            "source_fact_id": spec["source_fact_id"],
            "review_status": "PENDING_INDEPENDENT_ADJUDICATION",
            "score_effect": "none",
        })
    return src, queue, fixture


def _packet(src, queue, fixture):
    numbers = iter(f"secret-review-item-{i:04d}" for i in range(10))
    return prepare_private_expert_review_packet(
        src, queue, fixture,
        token_factory=lambda: next(numbers),
        shuffle=lambda items: items.reverse(),
    )


def test_blinded_packet_separates_author_side_and_contains_empty_review_fields():
    src, queue, fixture = _sample()
    packet, secret = _packet(src, queue, fixture)
    assert packet["evaluation_status"] == "AWAITING_INDEPENDENT_REVIEW"
    assert packet["score_admission"] == "DISABLED"
    assert packet["score_effect"] == "none"
    assert len(packet["source_cards"]) == 5
    assert len(packet["items_to_adjudicate"]) == 10
    assert len(packet["independently_authored_challenge_requests"]) == 5
    assert secret["secrecy"] == "EXTERNAL_PRIVATE_FILE_NOT_FOR_REVIEWER_OR_CI"
    assert len(secret["items"]) == 10
    assert len({x["review_item_id"] for x in secret["items"]}) == 10
    assert {x["author_side"] for x in secret["items"]} == {
        "authored_positive", "authored_adversarial",
    }
    assert {i["fact_id"] for i in packet["items_to_adjudicate"]} == set(SCOPE)
    manifest = [
        {"review_item_id": i["review_item_id"],
         "fact_id": i["fact_id"],
         "authored_draft_text": i["authored_draft_text"]}
        for i in packet["items_to_adjudicate"]
    ]
    assert secret["manifest_sha256"] == _sha256_manifest(manifest)
    assert all(item["expert_label"] == "" for item in packet["items_to_adjudicate"])
    assert all(not item["condition_ids_explicitly_asserted"]
               for item in packet["items_to_adjudicate"])
    assert all(x["new_correct_paraphrase"] == "" for x in
               packet["independently_authored_challenge_requests"])
    visible = json.dumps(packet, ensure_ascii=False)
    assert '"author_side"' not in visible
    assert '"positive_label"' not in visible
    assert '"adversarial_label"' not in visible
    assert '"case_id"' not in visible
    assert '"adversarial_type"' not in visible
    assert '"source_statement"' in visible
    assert '"authored_draft_text"' in visible
    assert '"reviewer_id": ""' in visible


@pytest.mark.parametrize("mutation", [
    "source_not_verified", "source_decision", "missing_ref", "relation",
    "queue_admitted", "queue_sha", "queue_processed", "queue_score",
    "queue_no_alias_gate", "review_completed", "challenge_label", "challenge_score",
])
def test_private_packet_rejects_prohibited_authority_or_label_drift(mutation):
    src, queue, fixture = _sample()
    selected = next(c for c in fixture["cases"] if c["fact_id"] in SCOPE)
    if mutation == "source_not_verified":
        src["rows"][0]["registry_verification_status"] = "unverified"
    elif mutation == "source_decision":
        src["rows"][0]["review_decision"] = "ACCEPT"
    elif mutation == "missing_ref":
        src["rows"][0]["registry_verification_refs"] = []
    elif mutation == "relation":
        src["rows"][0]["relation"]["object"] = "invented"
    elif mutation == "queue_admitted":
        queue["candidate_decision"] = "ACCEPT"
    elif mutation == "queue_sha":
        queue["execution_commit_sha"] = "wrong-head"
    elif mutation == "queue_processed":
        queue["rows"][0]["review_status"] = "EXPERT_APPROVED"
    elif mutation == "queue_score":
        queue["rows"][0]["score_effect"] = "credit"
    elif mutation == "queue_no_alias_gate":
        queue["automatic_alias_admission"] = True
    elif mutation == "review_completed":
        queue["independently_labeled_answer_count"] = 1
    elif mutation == "challenge_label":
        selected["positive_label"] = "INDEPENDENT_REVIEWED"
    elif mutation == "challenge_score":
        selected["score_effect"] = "credit"
    with pytest.raises((ValueError, KeyError)):
        _packet(src, queue, fixture)


def test_duplicate_or_predictable_token_is_fail_closed():
    src, queue, fixture = _sample()
    with pytest.raises(ValueError, match="short private"):
        prepare_private_expert_review_packet(
            src, queue, fixture,
            token_factory=lambda: "short",
            shuffle=lambda x: None,
        )
    with pytest.raises(ValueError, match="duplicate"):
        prepare_private_expert_review_packet(
            src, queue, fixture,
            token_factory=lambda: "long_token_value_used_everywhere",
            shuffle=lambda x: None,
        )


def test_reviewer_packet_contains_no_claim_of_expert_accuracy_or_automatic_score():
    src, queue, fixture = _sample()
    p, k = _packet(src, queue, fixture)
    assert "grade" not in p["schema_version"]
    assert "REVIEW" in p["evaluation_status"]
    assert k["schema_version"] == "s7_independent_expert_sealed_map.v1"
    assert all(x["fact_id"] in SCOPE for x in p["source_cards"])
    assert all(x["score_effect"] == "none" for x in [p])
