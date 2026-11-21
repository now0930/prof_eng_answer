"""Synthetic, score-neutral checks for read-only S7 missing-alias tracing."""
from __future__ import annotations

import json

import pytest

from grading.evidence.s7_alias_root_cause_audit import (
    S7AliasRootCauseTrace, _component_info,
)

TOPIC = "test_topic"
FACT = "test_fact"
SOURCE_FACT = "approved_fact"


def _ontology(tmp_path, *, entities=None, quantities=None, predicates=None):
    folder = tmp_path / "grading_ontology"
    folder.mkdir(parents=True)
    for name, key, rows in (
        ("engineering_concepts", "concepts", entities or []),
        ("quantities", "quantities", quantities or []),
        ("canonical_predicates", "predicates", predicates or []),
    ):
        (folder / (name + ".json")).write_text(
            json.dumps({key: rows}, ensure_ascii=False), encoding="utf-8",
        )


def _aligned(subject, predicate, obj):
    return {"fact_projection": [{
        "owner_topic_id": TOPIC,
        "fact_id": FACT,
        "source_fact_id": SOURCE_FACT,
        "projection_status": "VERIFIED_REGISTRY_RELATION",
        "relation_source": "verified_registry",
        "relation": {
            "subject": subject, "predicate": predicate, "object": obj,
            "polarity": "positive", "conditions": [],
        },
    }]}


def _surface(missing):
    combination = "+".join(missing)
    return {
        "verified_fact_projection_count": 1,
        "alias_missing_component_counts": {role: 1 for role in missing},
        "alias_missing_combination_counts": {combination: 1},
        "disposition_counts": {"ALIAS_INVENTORY_INCOMPLETE": 1},
    }


def _s7_report():
    return {
        "graded_case_count": 47,
        "expected_policy_abstention_count": 1,
        "unexpected_baseline_failure_count": 0,
        "alignment_failure_count": 0,
        "score_admission": "DISABLED",
        "registry_surface_recall": {"candidate_count": 0},
        "golden_coverage": {
            "alignment_relation_counts": {"EXACT_RELATION": 0},
        },
    }


def test_missing_projection_has_single_primary_cause_and_no_answer(tmp_path):
    _ontology(tmp_path)
    trace = S7AliasRootCauseTrace(
        root=tmp_path, runtime_aliases={}, runtime_predicates={},
    )
    trace.observe(
        "case_1", _aligned("not_sub", "not_pred", "not_obj"),
        _surface(("subject", "predicate", "object")),
    )
    report = trace.result(_s7_report())
    assert report["status"] == "BASELINE_MISMATCH"  # synthetic 1 != 179
    assert report["projection_count_with_duplicates"] == 1
    assert report["unique_topic_fact_count"] == 1
    assert report["unique_missing_id_counts_by_role"] == {
        "subject": 1, "predicate": 1, "object": 1,
    }
    assert report["primary_cause_projection_counts"]["ID_NOT_FOUND"] == 1
    assert sum(report["primary_cause_projection_counts"].values()) == 1
    assert report["component_cause_counts_non_partition"]["ID_NOT_FOUND"] == 3
    assert report["baseline_reproduction"]["mismatches"]
    assert report["rows"][0]["relation"]["subject"] == "not_sub"
    assert report["rows"][0]["score_effect"] == "none"
    assert "raw answer private" not in json.dumps(report)


def test_identical_fact_across_cases_is_counted_twice_but_unique_once(tmp_path):
    _ontology(tmp_path)
    trace = S7AliasRootCauseTrace(
        root=tmp_path, runtime_aliases={}, runtime_predicates={},
    )
    for case_id in ("case_1", "case_2"):
        trace.observe(
            case_id, _aligned("a", "b", "c"),
            _surface(("subject", "predicate", "object")),
        )
    report = trace.result(_s7_report())
    assert report["projection_count_with_duplicates"] == 2
    assert report["unique_topic_fact_count"] == 1
    assert report["unique_source_fact_count"] == 1
    assert report["duplicate_projection_count_vs_unique_topic_fact"] == 1
    with pytest.raises(ValueError, match="duplicate"):
        trace.observe(
            "case_1", _aligned("a", "b", "c"),
            _surface(("subject", "predicate", "object")),
        )


def test_role_mismatch_is_not_classified_as_unknown_id(tmp_path):
    _ontology(tmp_path, entities=[{"id": "entity_role", "aliases": ["기술 개념"]}])
    trace = S7AliasRootCauseTrace(
        root=tmp_path, runtime_aliases={}, runtime_predicates={},
    )
    trace.observe(
        "case_1", _aligned("subject_missing", "entity_role", "object_missing"),
        _surface(("subject", "predicate", "object")),
    )
    report = trace.result(_s7_report())
    assert report["rows"][0]["component_evidence"]["predicate"]["cause"] == (
        "UNSUPPORTED_RELATION"
    )
    assert report["rows"][0]["primary_cause"] == "UNSUPPORTED_RELATION"
    assert report["primary_cause_projection_counts"]["UNSUPPORTED_RELATION"] == 1
    assert report["component_cause_counts_non_partition"]["ID_NOT_FOUND"] == 2


def test_predicate_empty_and_malformed_alias_classes_use_runtime_behavior(tmp_path):
    _ontology(tmp_path, predicates=[
        {"id": "empty", "aliases": []},
        {"id": "malformed", "aliases": "not-a-list"},
    ])
    predicates = {
        "empty": [],  # _load_predicates yields [] for empty explicit aliases.
    }
    for predicate, expected in (
        ("empty", "EMPTY_ALIAS"),
        ("malformed", "INVALID_ALIAS_FORMAT"),
    ):
        detail = _component_info(
            "predicate", predicate, entities={}, predicates={
                "empty": {
                    "source_file": "canonical_predicates.json", "aliases": [],
                    "duplicate_definition": False,
                },
                "malformed": {
                    "source_file": "canonical_predicates.json",
                    "aliases": "not-a-list", "duplicate_definition": False,
                },
            },
            runtime_entities={}, runtime_predicates=predicates,
        )
        assert detail["missing_in_runtime"] is True
        assert detail["cause"] == expected


def test_actual_loader_fallback_for_existing_concept_is_not_false_missing(tmp_path):
    _ontology(tmp_path, entities=[{"id": "exists", "aliases": []}])
    # _load_aliases always gives a default alias derived from concept ID.
    detail = _component_info(
        "subject", "exists",
        entities={"exists": {
            "source_file": "engineering_concepts.json", "aliases": [],
            "duplicate_definition": False,
        }},
        predicates={}, runtime_entities={"exists": ["exists"]},
        runtime_predicates={},
    )
    assert detail["missing_in_runtime"] is False
    assert detail["cause"] is None


def test_trace_rejects_count_mismatch_instead_of_fabricating_179(tmp_path):
    _ontology(tmp_path)
    trace = S7AliasRootCauseTrace(
        root=tmp_path, runtime_aliases={}, runtime_predicates={},
    )
    bad = _surface(("subject", "predicate", "object"))
    bad["alias_missing_component_counts"]["subject"] = 999
    with pytest.raises(ValueError, match="component counts"):
        trace.observe(
            "case_1", _aligned("a", "b", "c"), bad,
        )
