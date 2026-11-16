"""The S7 Registry relation bridge is an audit, NOT a scoring adapter."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from grading.evidence.s7_registry_formula_shadow import SPECS
from grading.evidence.s7_registry_relation_bridge import build_relation_bridge


def _fixture() -> tuple[dict, dict, dict]:
    root = Path(__file__).resolve().parents[1]
    raw = json.loads(
        (root / "calibration/s7_alias_negative_claim_challenge_v1.json")
        .read_text(encoding="utf-8")
    )
    sample_src = {
        "schema_version": "s7_alias_registry_source_review.v1",
        "status": "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD",
        "score_admission": "DISABLED",
        "score_effect": "none",
        "inventory_execution_sha": "mock-head-sha",
        "unique_topic_fact_count": 119,
        "projection_count_with_duplicates": 179,
        "decision_counts": {"HOLD": 119, "ACCEPT": 0},
        "rows": [],
    }
    shadow = {
        "schema_version": "s7_registry_formula_shadow.v1",
        "status": "SHADOW_FORMULA_PATTERNS_REVIEW_ONLY",
        "score_admission": "DISABLED",
        "score_effect": "none",
        "automatic_alias_admission": False,
        "all_candidate_decisions": "HOLD",
        "source_inventory_execution_sha": "mock-head-sha",
        "execution_commit_sha": "mock-head-sha",
        "rows": [],
    }
    for case in raw["cases"]:
        fid = case["fact_id"]
        spec = SPECS.get(fid)
        relation = {
            "subject": case["relation_subject_id"],
            "predicate": "fixture_only_nonformula_predicate",
            "object": "fixture_only_nonformula_object",
            "polarity": "positive",
            "conditions": [],
        }
        if spec:
            relation = {
                "subject": spec["subject"], "predicate": spec["predicate"],
                "object": spec["object"], "polarity": "positive",
                "conditions": list(spec["conditions"]),
            }
        sample_src["rows"].append({
            "owner_topic_id": case["owner_topic_id"],
            "fact_id": fid,
            "source_fact_id": spec["source"] if spec else fid,
            "source_statement": "Synthetic source content for unit tests only.",
            "registry_review_status": "approved",
            "registry_verification_status": "verified",
            "registry_verification_refs": [{"authority_id": "fixture-only"}],
            "review_decision": "HOLD",
            "candidate_alias": None,
            "technical_equivalence_of_candidate": "NOT_ASSESSED",
            "score_effect": "none",
            "relation": relation,
        })
        if spec:
            shadow["rows"].append({
                "case_id": case["case_id"],
                "owner_topic_id": case["owner_topic_id"],
                "fact_id": fid,
                "source_fact_id": spec["source"],
                "formula_family": spec["family"],
                "score_effect": "none",
                "positive": {
                    "formula_syntax": "EXPECTED_FORMULA_SYNTAX",
                    "qualifier_cue_present_not_validated": True,
                },
                "adversarial": {
                    "formula_syntax": "INVERTED_FORMULA_SYNTAX",
                    "qualifier_cue_present_not_validated": True,
                },
            })
    return sample_src, raw, shadow


def test_bridge_reconciles_only_six_source_owned_formula_ids():
    src, challenge, shadow = _fixture()
    result = build_relation_bridge(src, challenge, shadow, strict=False)
    assert result["status"] == "BORROWED_SOURCE_IDS_ONLY_RESEARCH_INCONCLUSIVE"
    assert result["draft_fact_pair_count"] == 20
    assert result["formula_source_id_candidate_count"] == 6
    assert result["formula_direction_conflict_review_count"] == 6
    assert result["uncovered_nonformula_fact_count"] == 14
    assert result["answer_extracted_exact_relation_count"] is None
    assert result["measured_accuracy"] is None
    assert result["measured_precision"] is None
    assert result["measured_recall"] is None
    assert result["score_admission"] == "DISABLED"
    assert result["automatic_alias_admission"] is False
    assert result["candidate_decision"] == "HOLD"
    rows = result["rows"]
    assert all(row["score_effect"] == "none" for row in rows)
    for row in rows:
        if row["fact_id"] in SPECS:
            spec = SPECS[row["fact_id"]]
            borrowed = row["source_relation_candidate_not_answer_parsed"]
            assert borrowed is not None
            assert borrowed["subject"] == spec["subject"]
            assert borrowed["predicate"] == spec["predicate"]
            assert borrowed["object"] == spec["object"]
            assert borrowed["condition_ids_not_validated"] == spec["conditions"]
            assert borrowed["conditions_proven_by_answer"] is False
            assert borrowed["answer_relation_extraction"] == "NOT_ESTABLISHED"
            assert row["positive_probe_status"] == "FORMULA_TO_SOURCE_IDS_CANDIDATE_ONLY"
            assert row["adversarial_probe_status"] == "FORMULA_DIRECTION_CONFLICT_REVIEW"
        else:
            assert row["source_relation_candidate_not_answer_parsed"] is None
            assert row["positive_probe_status"] == "NO_FORMULA_SHADOW_COVERAGE"
    exported = json.dumps(result, ensure_ascii=False)
    assert "저요구 모드와 동일한 사고 기준에서" not in exported
    assert "Synthetic source content for unit tests only" not in exported


def test_all_forged_adversarial_positive_patterns_fail_closed():
    src, challenge, shadow = _fixture()
    shadow["rows"][0]["adversarial"]["formula_syntax"] = "EXPECTED_FORMULA_SYNTAX"
    with pytest.raises(ValueError, match="adversarial"):
        build_relation_bridge(src, challenge, shadow, strict=False)


@pytest.mark.parametrize("mode", [
    "source_approval", "source_relation", "missing_verified_ref", "alias_acceptance",
    "scoring_enabled", "formula_sha", "formula_scope", "wrong_challenge_owner",
    "source_missing", "formula_score_effect", "relabel_challenge",
])
def test_bridge_guard_fails_closed_on_any_identity_or_approval_drift(mode):
    src, challenge, shadow = _fixture()
    if mode == "source_approval":
        src["rows"][0]["review_decision"] = "ACCEPT"
    elif mode == "source_relation":
        target = next(r for r in src["rows"] if r["fact_id"] in SPECS)
        target["relation"]["object"] = "invented_parser_object"
    elif mode == "missing_verified_ref":
        src["rows"][0]["registry_verification_refs"] = []
    elif mode == "alias_acceptance":
        src["rows"][0]["candidate_alias"] = "a new alias"
    elif mode == "scoring_enabled":
        src["score_admission"] = "ENABLED"
    elif mode == "formula_sha":
        shadow["execution_commit_sha"] = "foreign-head"
    elif mode == "formula_scope":
        shadow["rows"].pop()
    elif mode == "wrong_challenge_owner":
        challenge["cases"][0]["owner_topic_id"] = "wrong_topic"
    elif mode == "source_missing":
        src["rows"].pop()
    elif mode == "formula_score_effect":
        shadow["score_effect"] = "credit"
    elif mode == "relabel_challenge":
        challenge["cases"][0]["positive_label"] = "VERIFIED"
    with pytest.raises((ValueError, KeyError)):
        build_relation_bridge(src, challenge, shadow, strict=False)


def test_strict_requires_live_119_rows_not_synthetic_partial_source():
    src, challenge, shadow = _fixture()
    with pytest.raises(ValueError, match="baseline"):
        build_relation_bridge(src, challenge, shadow, strict=True)


def test_ambiguous_formula_mapping_is_held_not_credited():
    src, challenge, shadow = _fixture()
    shadow["rows"][0]["positive"]["formula_syntax"] = "NO_LITERAL_PATTERN"
    result = build_relation_bridge(src, challenge, shadow, strict=False)
    assert result["formula_source_id_candidate_count"] == 5
    row = next(r for r in result["rows"]
               if r["fact_id"] == shadow["rows"][0]["fact_id"])
    assert row["source_relation_candidate_not_answer_parsed"] is None
    assert row["positive_probe_status"] == "FORMULA_SYNTAX_AMBIGUOUS_HOLD"


def test_canonical_scoring_engine_not_imported_by_shadow_module():
    import sys
    import grading.evidence.s7_registry_relation_bridge as bridge

    assert not hasattr(bridge, "evaluate_deterministic_requirements")
    assert not hasattr(bridge, "analyze_claim_alignment")
    assert "score" not in bridge.VERSION
