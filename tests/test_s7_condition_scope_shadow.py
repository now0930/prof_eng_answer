"""S7 five held condition/scope cases: literal cues, not semantic grading."""
from __future__ import annotations

import json
from pathlib import Path
from copy import deepcopy

import pytest

from grading.evidence.s7_condition_scope_shadow import (
    SPECS, _cue, evaluate_condition_scope_shadow,
)

ROOT = Path(__file__).resolve().parents[1]
_EXPECTED = "AUTHOR_DRAFT_EXPECTED_CUE_ONLY"
_CONTRARY = "AUTHOR_DRAFT_CONTRARY_CUE_REVIEW"


def _sample():
    all_cases = json.loads(
        (ROOT / "calibration/s7_alias_negative_claim_challenge_v1.json")
        .read_text(encoding="utf-8")
    )
    src = {
        "schema_version": "s7_alias_registry_source_review.v1",
        "status": "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD",
        "score_effect": "none",
        "score_admission": "DISABLED",
        "inventory_execution_sha": "unit-test-head",
        "projection_count_with_duplicates": 179,
        "unique_topic_fact_count": 119,
        "decision_counts": {"HOLD": 119, "ACCEPT": 0},
        "rows": [],
    }
    triage = {
        "schema_version": "s7_nonformula_surface_triage.v1",
        "status": "NONFORMULA_DRAFT_SURFACE_REVIEW_ONLY",
        "score_effect": "none",
        "score_admission": "DISABLED",
        "candidate_decision": "HOLD",
        "automatic_alias_admission": False,
        "source_inventory_execution_sha": "unit-test-head",
        "execution_commit_sha": "unit-test-head",
        "nonformula_fact_count": 14,
        "unprobed_nonformula_fact_count": 10,
        "rows": [],
    }
    for case in all_cases["cases"]:
        fid = case["fact_id"]
        if fid not in SPECS:
            continue
        spec = SPECS[fid]
        src["rows"].append({
            "owner_topic_id": spec["owner"], "fact_id": fid,
            "source_fact_id": spec["source"],
            "relation": {
                "subject": spec["subject"], "predicate": spec["predicate"],
                "object": spec["object"], "conditions": list(spec["conditions"]),
                "polarity": "positive",
            },
            "registry_review_status": "approved",
            "registry_verification_status": "verified",
            "registry_verification_refs": [{"authority_id": "fixture-only"}],
            "review_decision": "HOLD",
            "technical_equivalence_of_candidate": "NOT_ASSESSED",
            "candidate_alias": None, "score_effect": "none",
        })
        triage["rows"].append({
            "owner_topic_id": spec["owner"], "fact_id": fid,
            "source_fact_id": spec["source"],
            "source_predicate_id": spec["predicate"],
            "pilot_selected": False,
            "positive_surface_cue": "NOT_PROBED",
            "adversarial_surface_cue": "NOT_PROBED",
            "score_effect": "none",
        })
    return src, triage, all_cases


def test_five_source_owned_draft_pairs_cues_and_holds():
    src, triage, challenge = _sample()
    result = evaluate_condition_scope_shadow(src, triage, challenge, strict=False)
    assert result["status"] == "CONDITION_SCOPE_DRAFT_CUES_REVIEW_ONLY"
    assert result["draft_pair_count"] == 5
    assert result["condition_dependency_fact_count"] == 3
    assert result["nyquist_scope_fact_count"] == 2
    assert result["positive_surface_cues"] == 5
    assert result["adversarial_contrary_cues"] == 5
    assert result["source_conditions_proven"] == 0
    assert result["candidate_decision"] == "HOLD"
    assert result["score_admission"] == "DISABLED"
    assert result["measured_accuracy"] is None
    assert result["answer_parsed_exact_relation_count"] is None
    assert all(x["conditions_validated"] is False for x in result["rows"])
    assert all(x["score_effect"] == "none" for x in result["rows"])
    assert all(x["source_condition_ids_unproven"] for x in result["rows"])
    as_text = json.dumps(result, ensure_ascii=False)
    assert "표준 음의 피드백이고 미모델링 상쇄" not in as_text
    assert "열전대 기전력만 알면" not in as_text


def test_each_original_author_draft_has_narrow_pos_and_contrary_cue():
    _, _, fixture = _sample()
    for case in fixture["cases"]:
        fid = case["fact_id"]
        if fid in SPECS:
            assert _cue(fid, case["positive_answer"]) == _EXPECTED, fid
            assert _cue(fid, case["adversarial_answer"]) == _CONTRARY, fid


def test_conditional_missing_qualifier_never_becomes_expected_claim():
    _, _, fixture = _sample()
    omissions = {
        "safe_state_process_hazard_basis": "안전 요구사항",
        "residual_frequency_before_sif": "독립 IPL",
        "thermocouple_measures_temperature_difference": "기준접점 온도를 알아야",
        "closed_loop_rhp_poles_count": "표준 음의 피드백",
        "open_loop_rhp_poles_count": "중복도를 포함",
    }
    for case in fixture["cases"]:
        if case["fact_id"] not in omissions:
            continue
        missing = omissions[case["fact_id"]]
        assert missing in case["positive_answer"]
        truncated = case["positive_answer"].replace(missing, "", 1)
        assert _cue(case["fact_id"], truncated) != _EXPECTED


@pytest.mark.parametrize("fact_id", sorted(SPECS))
def test_conflicting_positive_and_contrary_drafts_fail_closed(fact_id):
    _, _, fixture = _sample()
    case = next(c for c in fixture["cases"] if c["fact_id"] == fact_id)
    mixed = case["positive_answer"] + " " + case["adversarial_answer"]
    # When the same answer contains both claims, the tool may flag rejection
    # context but must never treat it as a positive-only assertion.
    assert _cue(fact_id, mixed) != _EXPECTED


def test_explicit_rejection_of_source_consistent_draft_not_accepted():
    _, _, fixture = _sample()
    for c in fixture["cases"]:
        if c["fact_id"] in SPECS:
            assert _cue(c["fact_id"], c["positive_answer"] + " 라는 주장은 틀리다") == (
                "REJECTION_CONTEXT_HOLD"
            )


@pytest.mark.parametrize("mutation", [
    "source_review_decision", "source_relation", "source_conditions",
    "source_verification_ref", "source_alias", "source_score",
    "triage_sha", "triage_preprobed", "triage_alias_state",
    "triage_score", "challenge_owner", "challenge_score",
    "challenge_author_labels", "source_admission",
])
def test_source_identity_condition_scope_and_scoring_guards(mutation):
    source, triage, fixture = _sample()
    scoped = next(c for c in fixture["cases"] if c["fact_id"] in SPECS)
    if mutation == "source_review_decision":
        source["rows"][0]["review_decision"] = "ACCEPT"
    elif mutation == "source_relation":
        source["rows"][0]["relation"]["object"] = "invented"
    elif mutation == "source_conditions":
        source["rows"][0]["relation"]["conditions"] = []
    elif mutation == "source_verification_ref":
        source["rows"][0]["registry_verification_refs"] = []
    elif mutation == "source_alias":
        source["rows"][0]["candidate_alias"] = "unverified"
    elif mutation == "source_score":
        source["rows"][0]["score_effect"] = "credit"
    elif mutation == "triage_sha":
        triage["execution_commit_sha"] = "foreign-head"
    elif mutation == "triage_preprobed":
        triage["rows"][0]["pilot_selected"] = True
    elif mutation == "triage_alias_state":
        triage["candidate_decision"] = "ACCEPT"
    elif mutation == "triage_score":
        triage["rows"][0]["score_effect"] = "credit"
    elif mutation == "challenge_owner":
        scoped["owner_topic_id"] = "foreign-owner"
    elif mutation == "challenge_score":
        scoped["score_effect"] = "credit"
    elif mutation == "challenge_author_labels":
        scoped["positive_label"] = "EXPERT_CONFIRMED"
    else:
        source["score_admission"] = "ENABLED"
    with pytest.raises((ValueError, KeyError)):
        evaluate_condition_scope_shadow(source, triage, fixture, strict=False)


def test_strict_mode_requires_real_119_fact_source_and_14_triage_rows():
    source, triage, fixture = _sample()
    with pytest.raises(ValueError, match="baseline"):
        evaluate_condition_scope_shadow(source, triage, fixture)


def test_registry_source_owns_five_real_fact_relations():
    from grading.evidence.fact_claim_adapter import project_fact_claims

    required: dict[str, set[str]] = {}
    for fid, spec in SPECS.items():
        required.setdefault(spec["owner"], set()).add(fid)
    actual = project_fact_claims(sorted(required), required_by_topic=required)
    index = {(r["owner_topic_id"], r["fact_id"]): r for r in actual}
    assert len(index) == len(SPECS)
    for fid, spec in SPECS.items():
        row = index[(spec["owner"], fid)]
        assert row["projection_status"] == "VERIFIED_REGISTRY_RELATION"
        assert row["source_fact_id"] == spec["source"]
        for field in ("subject", "predicate", "object", "conditions"):
            assert row["relation"][field] == spec[field]
