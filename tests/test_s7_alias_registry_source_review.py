"""Fail-closed S7 Registry-source join tests; no Golden text or score changes."""
from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.review_s7_alias_registry_sources import build_source_review


def _fact():
    return {
        "fact_id": "approved_scoped_source",
        "topic_id": "sample_topic",
        "legacy_anchor_id": "sample_anchor",
        "statement": "A testable source statement with a qualification.",
        "revision": 1,
        "review_status": "approved",
        "verification_status": "verified",
        "verification_refs": [{
            "authority_id": "source_01", "locator": "section 1", "citation": "official"
        }],
        "source_refs": [],
        "score_effect": "none",
        "relation": {
            "subject": "source_entity",
            "predicate": "requires",
            "object": "an_object",
            "conditions": ["under_specified_conditions"],
        },
    }


def _row(case_id="case_a"):
    return {
        "case_id": case_id,
        "owner_topic_id": "sample_topic",
        "fact_id": "sample_anchor",
        "source_fact_id": "approved_scoped_source",
        "primary_cause": "ID_NOT_FOUND",
        "missing_components": ["subject", "predicate", "object"],
        "component_evidence": {
            field: {
                "id": value, "role": field, "missing_in_runtime": True,
                "runtime_alias_count": 0, "raw_definition": None,
                "cause": "ID_NOT_FOUND",
            } for field, value in (
                ("subject", "source_entity"),
                ("predicate", "requires"),
                ("object", "an_object"),
            )
        },
        "relation": {
            "subject": "source_entity", "predicate": "requires",
            "object": "an_object", "polarity": "positive",
            "conditions": ["under_specified_conditions"],
        },
    }


def _inventory(rows=None):
    return {
        "schema_version": "s7_alias_root_cause_audit.v1",
        "status": "REPRODUCED_BASELINE",
        "score_admission": "DISABLED",
        "baseline_reproduction": {"mismatches": {}},
        "rows": [_row()] if rows is None else rows,
    }


def test_verified_source_join_is_individual_and_no_alias_is_auto_approved():
    report = build_source_review(
        _inventory(), {"facts": [_fact()]}, require_full_baseline=False,
    )
    assert report["projection_count_with_duplicates"] == 1
    assert report["unique_topic_fact_count"] == 1
    assert report["conditioned_fact_count"] == 1
    assert report["decision_counts"] == {
        "HOLD": 1, "ACCEPT": 0, "REVISE": 0, "REJECT": 0,
    }
    item = report["rows"][0]
    assert item["source_fact_id"] == "approved_scoped_source"
    assert item["source_statement"] == _fact()["statement"]
    assert item["registry_verification_refs"] == _fact()["verification_refs"]
    assert item["risk_flags"] == [
        "ID_NOT_DEFINED_IN_PARSER_ONTOLOGY",
        "CONDITIONS_MUST_BE_ASSERTED_NOT_GUESSED",
        "BROAD_PREDICATE_FALSE_POSITIVE_RISK",
    ]
    assert item["candidate_alias"] is None
    assert item["candidate_wording"] is None
    assert item["review_decision"] == "HOLD"
    assert item["score_effect"] == "none"


def test_duplicate_golden_projections_not_mistaken_for_unique_facts():
    report = build_source_review(
        _inventory([_row("a"), _row("b")]), {"facts": [_fact()]},
        require_full_baseline=False,
    )
    assert report["projection_count_with_duplicates"] == 2
    assert report["unique_topic_fact_count"] == 1
    assert report["duplicate_projections"] == 1
    assert report["rows"][0]["case_ids"] == ["a", "b"]
    assert report["rows"][0]["occurrences_in_47_golden"] == 2


def test_missing_source_owner_or_relation_is_an_error():
    original = _fact()
    for mutated in (
        {**original, "topic_id": "different_topic"},
        {**original, "verification_status": "unverified"},
        {**original, "review_status": "candidate"},
        {**original, "relation": {
            **original["relation"], "predicate": "different_predicate",
        }},
        {**original, "legacy_anchor_id": "some_other_anchor"},
        {**original, "verification_refs": []},
    ):
        with pytest.raises(ValueError):
            build_source_review(
                _inventory(), {"facts": [mutated]},
                require_full_baseline=False,
            )


def test_conflicting_source_relation_across_cases_fails_closed():
    bad = _row("b")
    bad["relation"] = {**bad["relation"], "object": "different_object"}
    with pytest.raises(ValueError, match="conflicting"):
        build_source_review(
            _inventory([_row("a"), bad]), {"facts": [_fact()]},
            require_full_baseline=False,
        )


def test_alias_inventory_mismatch_is_not_accepted_or_silently_fixed():
    for key, value in (
        ("status", "BASELINE_MISMATCH"),
        ("score_admission", "ENABLED"),
        ("baseline_reproduction", {"mismatches": {"x": 1}}),
    ):
        bad = _inventory()
        bad[key] = value
        with pytest.raises(ValueError):
            build_source_review(
                bad, {"facts": [_fact()]}, require_full_baseline=False,
            )
    with pytest.raises(ValueError, match="179/119"):
        build_source_review(_inventory(), {"facts": [_fact()]})


def test_no_unapproved_fact_can_be_pulled_into_review():
    bad = _inventory()
    bad["rows"][0]["source_fact_id"] = "not_approved_source"
    with pytest.raises(ValueError, match="absent"):
        build_source_review(
            bad, {"facts": [_fact()]}, require_full_baseline=False,
        )
