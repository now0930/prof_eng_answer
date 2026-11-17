"""S7 last-five review queue: independent labels remain pending, never scoring."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from grading.evidence.s7_remaining_five_expert_queue import (
    PENDING, SCOPE, evaluate_remaining_five_queue,
)

ROOT = Path(__file__).resolve().parents[1]


def _sample():
    fixture = json.loads(
        (ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json")
        .read_text(encoding="utf-8")
    )
    source = {
        "schema_version": "s7_alias_registry_source_review.v1",
        "status": "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD",
        "score_admission": "DISABLED", "score_effect": "none",
        "inventory_execution_sha": "test-only-sha",
        "projection_count_with_duplicates": 179,
        "unique_topic_fact_count": 119,
        "decision_counts": {"HOLD": 119, "ACCEPT": 0},
        "rows": [],
    }
    triage = {
        "schema_version": "s7_nonformula_surface_triage.v1",
        "status": "NONFORMULA_DRAFT_SURFACE_REVIEW_ONLY",
        "score_admission": "DISABLED", "score_effect": "none",
        "candidate_decision": "HOLD", "automatic_alias_admission": False,
        "source_inventory_execution_sha": "test-only-sha",
        "execution_commit_sha": "test-only-sha",
        "nonformula_fact_count": 14,
        "unprobed_nonformula_fact_count": 10,
        "rows": [],
    }
    scope = {
        "schema_version": "s7_condition_scope_shadow.v1",
        "status": "CONDITION_SCOPE_DRAFT_CUES_REVIEW_ONLY",
        "score_admission": "DISABLED", "score_effect": "none",
        "candidate_decision": "HOLD", "automatic_alias_admission": False,
        "source_inventory_execution_sha": "test-only-sha",
        "execution_commit_sha": "test-only-sha",
        "draft_pair_count": 5,
        "source_conditions_proven": 0,
        "rows": [
            {"owner_topic_id": "source_different_owner", "fact_id": "other_fact_1"},
            {"owner_topic_id": "source_different_owner", "fact_id": "other_fact_2"},
            {"owner_topic_id": "source_different_owner", "fact_id": "other_fact_3"},
            {"owner_topic_id": "source_different_owner", "fact_id": "other_fact_4"},
            {"owner_topic_id": "source_different_owner", "fact_id": "other_fact_5"},
        ],
    }
    for case in fixture["cases"]:
        fid = case["fact_id"]
        if fid not in SCOPE:
            continue
        spec = SCOPE[fid]
        source["rows"].append({
            "owner_topic_id": spec["owner"],
            "fact_id": fid,
            "source_fact_id": spec["source_fact_id"],
            "registry_review_status": "approved",
            "registry_verification_status": "verified",
            "registry_verification_refs": [{"authority_id": "test-only"}],
            "candidate_alias": None,
            "technical_equivalence_of_candidate": "NOT_ASSESSED",
            "review_decision": "HOLD", "score_effect": "none",
            "relation": {
                "subject": spec["subject"], "predicate": spec["predicate"],
                "object": spec["object"], "conditions": list(spec["conditions"]),
                "polarity": "positive",
            },
            "risk_flags": ["ID_NOT_DEFINED_IN_PARSER_ONTOLOGY"],
        })
        triage["rows"].append({
            "owner_topic_id": spec["owner"], "fact_id": fid,
            "source_fact_id": spec["source_fact_id"],
            "source_predicate_id": spec["predicate"],
            "pilot_selected": False,
            "positive_surface_cue": "NOT_PROBED",
            "adversarial_surface_cue": "NOT_PROBED",
            "score_effect": "none",
        })
    return source, triage, scope, fixture


def test_five_missing_facts_all_queued_without_any_source_answer_text():
    src, triage, condition, challenge = _sample()
    report = evaluate_remaining_five_queue(src, triage, condition, challenge,
                                           strict=False)
    assert report["status"] == "FIVE_UNPROBED_FACTS_QUEUED_FOR_INDEPENDENT_REVIEW"
    assert report["queued_fact_count"] == 5
    assert report["authored_draft_answer_count"] == 10
    assert report["source_condition_ids_total"] == 8
    assert report["review_pending_count"] == 5
    assert report["independently_labeled_answer_count"] == 0
    assert report["score_admission"] == "DISABLED"
    assert report["automatic_alias_admission"] is False
    assert report["candidate_decision"] == "HOLD"
    assert report["answer_parsed_exact_relation_count"] is None
    assert report["measured_precision"] is None
    assert report["measured_recall"] is None
    assert report["measured_accuracy"] is None
    assert {x["fact_id"] for x in report["rows"]} == set(SCOPE)
    assert all(x["review_status"] == PENDING for x in report["rows"])
    assert all(x["score_effect"] == "none" for x in report["rows"])
    assert all(x["independent_claim_label"] == "NOT_EVALUATED"
               for x in report["rows"])
    assert report["rows"][0]["source_fact_id"]
    as_json = json.dumps(report, ensure_ascii=False)
    for row in challenge["cases"]:
        assert row["positive_answer"] not in as_json
        assert row["adversarial_answer"] not in as_json
    assert "source_statement" not in as_json
    assert "registry_verification_refs" not in as_json


@pytest.mark.parametrize("mutation", [
    "baseline_sha", "source_row_missing", "duplicated_source",
    "relation_object", "missing_conditions", "source_accepted",
    "unverified_source", "missing_authority", "accepted_alias",
    "triage_probed", "triage_source_id", "triage_score",
    "scope_overlap", "scope_sha", "scope_proven", "scope_admission",
    "source_score", "challenge_score", "challenge_owner", "challenge_label",
])
def test_fail_closed_on_source_scope_or_admission_drift(mutation):
    src, triage, scope, challenge = _sample()
    case = next(x for x in challenge["cases"] if x["fact_id"] in SCOPE)
    if mutation == "baseline_sha":
        triage["execution_commit_sha"] = "foreign-sha"
    elif mutation == "source_row_missing":
        src["rows"].pop()
    elif mutation == "duplicated_source":
        src["rows"].append(dict(src["rows"][0]))
    elif mutation == "relation_object":
        src["rows"][0]["relation"]["object"] = "incorrect"
    elif mutation == "missing_conditions":
        src["rows"][0]["relation"]["conditions"] = []
    elif mutation == "source_accepted":
        src["rows"][0]["review_decision"] = "ACCEPT"
    elif mutation == "unverified_source":
        src["rows"][0]["registry_verification_status"] = "unverified"
    elif mutation == "missing_authority":
        src["rows"][0]["registry_verification_refs"] = []
    elif mutation == "accepted_alias":
        src["rows"][0]["candidate_alias"] = "new-alias"
    elif mutation == "triage_probed":
        triage["rows"][0]["pilot_selected"] = True
    elif mutation == "triage_source_id":
        triage["rows"][0]["source_fact_id"] = "different"
    elif mutation == "triage_score":
        triage["rows"][0]["score_effect"] = "credit"
    elif mutation == "scope_overlap":
        scope["rows"][0] = {
            "owner_topic_id": case["owner_topic_id"], "fact_id": case["fact_id"]
        }
    elif mutation == "scope_sha":
        scope["source_inventory_execution_sha"] = "foreign"
    elif mutation == "scope_proven":
        scope["source_conditions_proven"] = 1
        # strict=False allows shortened test fixtures, but no condition proofs
        # may be silently inherited from a prior literal-cue pilot.
        scope["status"] = "PROVEN"
    elif mutation == "scope_admission":
        scope["score_admission"] = "ENABLED"
    elif mutation == "source_score":
        src["rows"][0]["score_effect"] = "credit"
    elif mutation == "challenge_score":
        case["score_effect"] = "credit"
    elif mutation == "challenge_owner":
        case["owner_topic_id"] = "wrong"
    elif mutation == "challenge_label":
        case["positive_label"] = "EXPERT_APPROVED"
    with pytest.raises((ValueError, KeyError)):
        evaluate_remaining_five_queue(src, triage, scope, challenge, strict=False)


def test_full_run_baseline_strict_requires_all_119_sources():
    src, triage, scope, fixture = _sample()
    with pytest.raises(ValueError, match="baseline"):
        evaluate_remaining_five_queue(src, triage, scope, fixture, strict=True)


def test_verified_registry_preserves_all_five_relation_id_conditions():
    from grading.evidence.fact_claim_adapter import project_fact_claims

    required: dict[str, set[str]] = {}
    for fid, s in SCOPE.items():
        required.setdefault(s["owner"], set()).add(fid)
    rows = project_fact_claims(sorted(required), required_by_topic=required)
    by_id = {(x["owner_topic_id"], x["fact_id"]): x for x in rows}
    assert len(by_id) == 5
    for fid, spec in SCOPE.items():
        row = by_id[(spec["owner"], fid)]
        assert row["projection_status"] == "VERIFIED_REGISTRY_RELATION"
        assert row["source_fact_id"] == spec["source_fact_id"]
        for key in ("subject", "predicate", "object", "conditions"):
            assert row["relation"][key] == spec[key]


def test_nyquist_and_vmodel_draft_scope_remains_under_human_review():
    src, triage, scope, fixture = _sample()
    report = evaluate_remaining_five_queue(src, triage, scope, fixture,
                                           strict=False)
    by_id = {x["fact_id"]: x for x in report["rows"]}
    assert by_id["nyquist_contour_and_mapping"]["source_condition_ids_not_asserted"] == [
        "rhp_stability_analysis"
    ]
    assert by_id["sw04_v_model_definition"]["source_condition_ids_not_asserted"] == []
    assert by_id["sw04_v_model_definition"]["review_status"] == PENDING
