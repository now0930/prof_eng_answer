"""EMC negative-only invariant ownership never steals unrelated positive Fact credit."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from grading.evidence.topic_machine_contract import (
    TopicMachineContractError, validate_topic_machine_contract,
)
from grading.scoring import deterministic_requirement_evaluator as evaluator

TOPIC = "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC
TARGETS = {
    "EMC_SINGLE_POINT_UNIVERSAL": "ipgse_single_multi_point_conditional",
    "EMC_SHIELD_REPLACES_PE": "ipgse_shield_not_pe",
    "EMC_REDUNDANCY_IGNORES_CCF": "ipgse_redundant_supply_boundary",
    "EMC_GROUND_LOOP_RESISTANCE_ONLY": "ipgse_ground_loop_safe_mitigation",
    "EMC_SINGLE_COUNTERMEASURE_UNIVERSAL": "ipgse_source_path_victim_mitigation",
    "EMC_REWIRE_BEFORE_EVIDENCE": "ipgse_evidence_before_rewire",
}
FOUR = {
    "ipgse_scope_chain", "ipgse_emi_coupling_paths",
    "ipgse_power_quality_scope", "ipgse_final_verification",
}
SAMPLE_EMI = {
    "subject": "emc_coupling_modes", "predicate": "diagnoses",
    "object": "emc_source_path_victim", "polarity": "positive",
    "assertion_context": "asserted", "claim_id": "positive_emi_claim",
}


def _contract():
    data = json.loads((PACK / "logic_check.json").read_text(encoding="utf-8"))
    return validate_topic_machine_contract(data["machine_contract"], topic_id=TOPIC)


def _evaluate(codes=(), claims=None):
    # This test is a one-process shadow: never edit exclusion manifests.
    # The standalone source bundle lacks server-only HOLD manifests.
    # Turn off ONLY the evaluator lookup inside this test; production is unchanged.
    with patch.object(evaluator, "excluded_from_scoring", return_value=False):
        return evaluator.evaluate_deterministic_requirements(
            claims=list(claims or []), invariant_codes=list(codes),
            topic_ids=[TOPIC], extraction_complete=True,
            requirement_scope_by_topic={TOPIC: ["ipgse_emi_coupling_paths"]},
        )


def test_six_binding_targets_match_semantic_anchors_and_are_negative_only():
    contract = _contract()
    bindings = {x["invariant_code"]: x for x in contract["invariant_bindings"]}
    rules = {x["requirement_id"]: x for x in contract["requirement_rules"]}
    for code, anchor in TARGETS.items():
        assert bindings[code]["requirement_refs"] == [anchor]
        assert rules[anchor] == {
            "requirement_id": anchor, "required_fact_ids": [],
            "minimum_match_count": 0, "violation_only": True,
        }
    for anchor in FOUR:
        assert not rules[anchor].get("violation_only", False)


def test_negative_only_requirements_do_not_count_when_no_error():
    result = _evaluate(claims=[SAMPLE_EMI])
    statuses = {row["requirement_id"]: row["status"] for row in result["requirements"]}
    assert statuses["ipgse_emi_coupling_paths"] == "SATISFIED"
    assert all(anchor not in statuses for anchor in TARGETS.values())
    assert not result["findings"]


@pytest.mark.parametrize("code,target", list(TARGETS.items()))
def test_each_invariant_downgrades_only_its_own_anchor(code, target):
    result = _evaluate([code], [SAMPLE_EMI])
    statuses = {row["requirement_id"]: row["status"] for row in result["requirements"]}
    assert statuses[target] == "WRONG"
    assert statuses["ipgse_emi_coupling_paths"] == "SATISFIED"
    assert all((anchor not in statuses or statuses[anchor] != "WRONG")
               for anchor in FOUR)
    matched = [f for f in result["findings"] if f["invariant_code"] == code]
    assert len(matched) == 1
    assert matched[0]["requirement_refs"] == [target]
    rule_row = next(r for r in result["requirements"] if r["requirement_id"] == target)
    assert rule_row["evidence_mode"] == "deterministic_invariant_only"
    assert rule_row["matched_fact_ids"] == []
    assert result["fatal_or_core_error"] == (matched[0]["classification"] == "fatal")


@pytest.mark.parametrize("mutation", [
    {"required_fact_ids": ["emc_pe_distinct_reference"]},
    {"minimum_match_count": 1},
    {"allow_subject_mention_partial": True},
    {"violation_only": "true"},
])
def test_negative_only_contract_must_not_claim_positive_fact_or_credit(mutation):
    contract = _contract()
    candidate = next(r for r in contract["requirement_rules"] if r["requirement_id"] ==
                     "ipgse_single_multi_point_conditional")
    candidate.update(mutation)
    with pytest.raises(TopicMachineContractError):
        validate_topic_machine_contract(contract, topic_id=TOPIC)


def test_independent_wrong_finding_survives_hold_without_positive_credit():
    """A scoring HOLD never authorizes Fact credit or hides a proven violation.

    This is a policy simulation; it never changes exclusion manifests.
    """
    with patch.object(evaluator, "excluded_from_scoring", return_value=True):
        baseline = evaluator.evaluate_deterministic_requirements(
            claims=[SAMPLE_EMI], invariant_codes=[], topic_ids=[TOPIC],
            extraction_complete=True,
        )
        assert not baseline["requirements"]
        for code, target in TARGETS.items():
            result = evaluator.evaluate_deterministic_requirements(
                claims=[SAMPLE_EMI], invariant_codes=[code], topic_ids=[TOPIC],
                extraction_complete=True,
            )
            rows = result["requirements"]
            assert len(rows) == 1
            assert rows[0]["requirement_id"] == target
            assert rows[0]["status"] == "WRONG"
            assert rows[0]["evidence_mode"] == "deterministic_invariant_only"
            assert not rows[0]["matched_fact_ids"]
            assert result["summary"]["SATISFIED"] == 0
            assert result["summary"]["PARTIAL"] == 0
