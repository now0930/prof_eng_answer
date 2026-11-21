"""Fail-closed nonformula triage tests; author drafts are not expert labels."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from grading.evidence.s7_nonformula_surface_triage import (
    PILOT, TRIAGE, _surface_cue, evaluate_nonformula_triage,
)

_EXPECTED = "EXPECTED_SURFACE_CUE_NOT_SEMANTICALLY_VALIDATED"
_CONTRARY = "CONTRARY_SURFACE_CUE_REVIEW"


def _sample() -> tuple[dict, dict, dict]:
    root = Path(__file__).resolve().parents[1]
    challenge = json.loads(
        (root / "calibration/s7_alias_negative_claim_challenge_v1.json")
        .read_text(encoding="utf-8")
    )
    source = {
        "schema_version": "s7_alias_registry_source_review.v1",
        "status": "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD",
        "score_admission": "DISABLED",
        "score_effect": "none",
        "unique_topic_fact_count": 119,
        "projection_count_with_duplicates": 179,
        "decision_counts": {"HOLD": 119, "ACCEPT": 0},
        "inventory_execution_sha": "synthetic-unit-test-head",
        "rows": [],
    }
    bridge = {
        "schema_version": "s7_registry_relation_bridge.v1",
        "status": "BORROWED_SOURCE_IDS_ONLY_RESEARCH_INCONCLUSIVE",
        "score_admission": "DISABLED",
        "score_effect": "none",
        "candidate_decision": "HOLD",
        "automatic_alias_admission": False,
        "source_inventory_execution_sha": "synthetic-unit-test-head",
        "execution_commit_sha": "synthetic-unit-test-head",
        "formula_source_id_candidate_count": 6,
        "uncovered_nonformula_fact_count": 14,
        "rows": [],
    }
    for case in challenge["cases"]:
        fid = case["fact_id"]
        if fid not in TRIAGE:
            continue
        source_id = "source_" + fid
        source["rows"].append({
            "owner_topic_id": case["owner_topic_id"],
            "fact_id": fid,
            "source_fact_id": source_id,
            "registry_review_status": "approved",
            "registry_verification_status": "verified",
            "registry_verification_refs": [{"authority_id": "synthetic-only"}],
            "review_decision": "HOLD",
            "candidate_alias": None,
            "technical_equivalence_of_candidate": "NOT_ASSESSED",
            "score_effect": "none",
            "relation": {
                "subject": case["relation_subject_id"],
                "predicate": TRIAGE[fid][1],
                "object": "fixture_object_only",
                "polarity": "positive",
                "conditions": ["fixture_condition_not_proven"],
            },
        })
        bridge["rows"].append({
            "owner_topic_id": case["owner_topic_id"],
            "fact_id": fid,
            "source_fact_id": source_id,
            "score_effect": "none",
            "source_relation_candidate_not_answer_parsed": None,
            "positive_probe_status": "NO_FORMULA_SHADOW_COVERAGE",
        })
    return source, challenge, bridge


def test_classifies_all_fourteen_but_parses_only_four_draft_pairs():
    source, challenge, bridge = _sample()
    r = evaluate_nonformula_triage(source, challenge, bridge, strict=False)
    assert r["status"] == "NONFORMULA_DRAFT_SURFACE_REVIEW_ONLY"
    assert r["nonformula_fact_count"] == 14
    assert r["pilot_fact_count"] == 4
    assert r["unprobed_nonformula_fact_count"] == 10
    assert r["triage_group_counts"] == {
        "CONDITIONAL_DEPENDENCY": 3,
        "DEFINITION_OR_CONSTRUCTION": 5,
        "MAPPING_OR_TRACEABILITY": 2,
        "POLE_ZERO_SCOPE_COUNT": 2,
        "TREND_OR_TIME_BASIS": 2,
    }
    assert r["pilot_positive_surface_cues"] == {_EXPECTED: 4}
    assert r["pilot_adversarial_surface_cues"] == {_CONTRARY: 4}
    assert r["answer_parsed_exact_relations"] is None
    assert r["measured_precision"] is None
    assert r["measured_recall"] is None
    assert r["measured_accuracy"] is None
    assert r["score_admission"] == "DISABLED"
    assert r["automatic_alias_admission"] is False
    assert r["candidate_decision"] == "HOLD"
    assert len(r["rows"]) == 14
    assert all(x["score_effect"] == "none" for x in r["rows"])
    assert all(x["source_condition_id_count_not_verified_by_answer"] == 1 for x in r["rows"])
    for x in r["rows"]:
        if x["fact_id"] not in PILOT:
            assert x["positive_surface_cue"] == "NOT_PROBED"
            assert x["adversarial_surface_cue"] == "NOT_PROBED"
    rendered = json.dumps(r, ensure_ascii=False)
    assert "Single-port globe valve body는" not in rendered
    assert "수증기 분압이 일정하고" not in rendered


@pytest.mark.parametrize(("fid", "positive", "negative"), [
    ("single_port_globe_throttling_structure",
     "Single-port globe valve body는 한 개의 시트링으로 선형 이동식 폐쇄 구조이다.",
     "Single-port globe valve body는 두 개의 시트링을 사용한다."),
    ("rtd_four_wire_kelvin_measurement",
     "4선식 Kelvin RTD는 전류 인가 두 선과 고입력 임피던스 전압 검출 두 선을 분리하여 오차를 줄인다.",
     "2선식 RTD도 4선식과 같은 보상이 성립한다."),
    ("rh_temperature_dependence",
     "수증기 분압이 일정하면 온도가 증가할 때 상대습도는 감소한다.",
     "수증기 분압이 일정하면 온도가 증가할 때 상대습도는 반드시 증가한다."),
    ("radar_pulse_time_of_flight",
     "FMR56/FMR57 펄스 레이더는 왕복 시간을 이용하여 D=ct/2를 구한다.",
     "FMR56/FMR57 펄스 레이더는 왕복 시간을 이용하여 D=ct로 구한다."),
])
def test_four_surface_pilots_have_directional_negative_controls(fid, positive, negative):
    assert _surface_cue(fid, positive) == _EXPECTED
    assert _surface_cue(fid, negative) == _CONTRARY


@pytest.mark.parametrize(("fid", "text"), [
    ("single_port_globe_throttling_structure", "밸브에는 시트링이 있다."),
    ("rtd_four_wire_kelvin_measurement", "4선식 RTD가 좋다."),
    ("rh_temperature_dependence", "온도가 증가하면 상대습도가 감소한다."),
    ("radar_pulse_time_of_flight", "FMCW에서는 D=ct/2다."),
])
def test_missing_owner_or_conditions_are_unresolved(fid, text):
    assert _surface_cue(fid, text) == "NO_UNAMBIGUOUS_SURFACE_CUE"


@pytest.mark.parametrize(("fid", "text"), [
    ("single_port_globe_throttling_structure",
     "Single-port globe body는 한 개의 시트링을 사용하고 선형 이동하나 두 개의 시트링도 쓴다."),
    ("rtd_four_wire_kelvin_measurement",
     "4선식 Kelvin RTD는 전류 인가 두 선과 고입력 임피던스 전압 검출 두 선을 분리해 오차를 줄인다. 2선식 RTD도 4선식과 같은 보상이 된다."),
    ("rh_temperature_dependence",
     "수증기 분압 일정, 온도가 증가하면 상대습도는 감소하고 상대습도는 증가한다."),
    ("radar_pulse_time_of_flight",
     "FMR56/FMR57 펄스 레이더의 왕복 시간 D=ct/2이지만 D=ct라고도 쓴다."),
])
def test_competing_answers_are_ambiguous_and_never_positive(fid, text):
    assert _surface_cue(fid, text) == "AMBIGUOUS_SURFACE_CUE_HOLD"


def test_explicit_rejection_context_cannot_receive_positive_candidate():
    text = "수증기 분압이 일정하면 온도가 증가할 때 상대습도는 감소한다는 주장은 틀리다"
    assert _surface_cue("rh_temperature_dependence", text) == (
        "ASSERTION_CONTEXT_UNVERIFIED"
    )


@pytest.mark.parametrize("change", [
    "bridge_sha", "source_approved", "source_subject", "source_predicate",
    "source_score_effect", "source_conditions", "bridge_borrowed",
    "alias_accepted", "missing_verified_refs", "challenge_owner",
    "challenge_score", "source_score_admission",
])
def test_identity_and_authority_drift_always_block(change):
    source, challenge, bridge = _sample()
    if change == "bridge_sha":
        bridge["execution_commit_sha"] = "foreign-head"
    elif change == "source_approved":
        source["rows"][0]["review_decision"] = "ACCEPT"
    elif change == "source_subject":
        source["rows"][0]["relation"]["subject"] = "wrong"
    elif change == "source_predicate":
        source["rows"][0]["relation"]["predicate"] = "unverified"
    elif change == "source_score_effect":
        source["rows"][0]["score_effect"] = "credit"
    elif change == "source_conditions":
        source["rows"][0]["relation"]["polarity"] = "negative"
    elif change == "bridge_borrowed":
        bridge["rows"][0]["source_relation_candidate_not_answer_parsed"] = {"x": "y"}
    elif change == "alias_accepted":
        source["rows"][0]["candidate_alias"] = "unapproved alias"
    elif change == "missing_verified_refs":
        source["rows"][0]["registry_verification_refs"] = []
    elif change == "challenge_owner":
        target = next(c for c in challenge["cases"] if c["fact_id"] in TRIAGE)
        target["owner_topic_id"] = "wrong_owner"
    elif change == "challenge_score":
        target = next(c for c in challenge["cases"] if c["fact_id"] in TRIAGE)
        target["score_effect"] = "credit"
    elif change == "source_score_admission":
        source["score_admission"] = "ENABLED"
    with pytest.raises((ValueError, KeyError)):
        evaluate_nonformula_triage(source, challenge, bridge, strict=False)


def test_strict_mode_requires_full_actual_119_source_rows_and_twenty_bridge_rows():
    source, challenge, bridge = _sample()
    with pytest.raises(ValueError, match="baseline drift"):
        evaluate_nonformula_triage(source, challenge, bridge)


def test_fourteen_live_registry_predicates_have_no_generic_alias_promotion():
    from grading.evidence.fact_claim_adapter import project_fact_claims

    source, challenge, bridge = _sample()
    selected: dict[str, set[str]] = {}
    for case in challenge["cases"]:
        if case["fact_id"] in TRIAGE:
            selected.setdefault(case["owner_topic_id"], set()).add(case["fact_id"])
    projection = project_fact_claims(selected, required_by_topic=selected)
    asserted = {(p["owner_topic_id"], p["fact_id"]): p for p in projection}
    assert len(asserted) == 14
    for case in challenge["cases"]:
        if case["fact_id"] not in TRIAGE:
            continue
        projected = asserted[(case["owner_topic_id"], case["fact_id"])]
        assert projected["projection_status"] == "VERIFIED_REGISTRY_RELATION"
        assert projected["relation"]["subject"] == case["relation_subject_id"]
        assert projected["relation"]["predicate"] == TRIAGE[case["fact_id"]][1]
