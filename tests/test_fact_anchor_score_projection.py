"""Legacy Anchor scoring accepts only reviewed source evidence in shadow mode."""
from copy import deepcopy
import hashlib
from pathlib import Path

import pytest

from grading.evidence.approved_fact_registry import load_approved_fact_registry
from grading.evidence.fact_anchor_score_projection import (
    calculate_shadow_score, project_verified_fact_evidence,
)
from grading.evidence.fact_grounded_contracts import FactGroundedContractError, fingerprint


def sample():
    facts = load_approved_fact_registry(Path(__file__).resolve().parents[1])["facts"]
    fact = next(row for row in facts if row.get("legacy_anchor_id")
                and row["relation"]["conditions"])
    question = "Explain this engineering relation."
    answer = "This answer gives a reviewed technical explanation."
    contract = {
        "schema_version": fact["schema_version"],
        "question_sha256": hashlib.sha256(question.encode()).hexdigest(),
        "knowledge_snapshot_sha256": fingerprint([fact]),
        "requirements": [{"requirement_id": "r1",
                          "source_span": {"start": 0, "end": len(question)},
                          "source_text": question, "task": "explain",
                          "fact_refs": [fact["fact_id"]], "resolution": "resolved"}],
        "score_effect": "none",
    }
    evaluation = {
        "requirements": [{"owner_topic_id": fact["topic_id"],
                          "requirement_id": fact["legacy_anchor_id"],
                          "status": "MISSING", "importance": "core",
                          "evidence_text": ""}],
        "findings": [], "fatal_or_core_error": False,
    }
    evidence = [{"fact_id": fact["fact_id"],
                 "source_span": {"start": 0, "end": len(answer)},
                 "source_text": answer, "reviewer_id": "reviewed_by_domain_expert",
                 "verification_mode": "human_review",
                 "knowledge_snapshot_sha256": contract["knowledge_snapshot_sha256"]}]
    return fact, question, answer, contract, evaluation, evidence


def project(fact, question, answer, contract, evaluation, evidence):
    return project_verified_fact_evidence(
        question_text=question, answer_text=answer, facts=[fact],
        question_contract=contract, requirement_evaluation=evaluation,
        reviewed_evidence=evidence,
    )


def test_reviewed_fact_projects_by_anchor_and_uses_existing_score_engine():
    values = sample()
    original = deepcopy(values[4])
    result = project(*values)
    assert len(result["promoted"]) == 1
    assert result["requirement_evaluation"]["requirements"][0]["status"] == "SATISFIED"
    assert values[4] == original
    score = calculate_shadow_score(answer_text=values[2], projection=result)
    assert score["score"]["decision"] == "SCORED"
    assert score["final_grade_allowed"] is False


def test_llm_agreement_cannot_self_certify_a_fact():
    values = list(sample())
    values[5][0]["verification_mode"] = "llm_consensus"
    with pytest.raises(FactGroundedContractError, match="not verified evidence"):
        project(*values)


def test_fatal_and_wrong_are_not_overridden():
    values = list(sample())
    values[4]["fatal_or_core_error"] = True
    assert not project(*values)["promoted"]
    values[4]["fatal_or_core_error"] = False
    values[4]["requirements"][0]["status"] = "WRONG"
    assert not project(*values)["promoted"]


def test_forged_quote_and_stale_snapshot_are_rejected():
    values = list(sample())
    values[5][0]["source_text"] = "invented"
    with pytest.raises(FactGroundedContractError, match="quote mismatch"):
        project(*values)
    values = list(sample())
    values[5][0]["knowledge_snapshot_sha256"] = "0" * 64
    with pytest.raises(FactGroundedContractError, match="stale knowledge"):
        project(*values)


def test_shared_anchor_requires_every_scoped_fact():
    rows = load_approved_fact_registry(Path(__file__).resolve().parents[1])["facts"]
    grouped = {}
    for row in rows:
        grouped.setdefault((row["topic_id"], row.get("legacy_anchor_id")), []).append(row)
    pair = next(value for key, value in grouped.items() if key[1] and len(value) == 2)
    _, question, answer, contract, evaluation, _ = sample()
    contract["knowledge_snapshot_sha256"] = fingerprint(sorted(pair, key=lambda row: row["fact_id"]))
    contract["requirements"][0]["fact_refs"] = [row["fact_id"] for row in pair]
    evaluation["requirements"][0].update(owner_topic_id=pair[0]["topic_id"],
                                          requirement_id=pair[0]["legacy_anchor_id"])
    evidence = [{"fact_id": pair[0]["fact_id"],
                 "source_span": {"start": 0, "end": len(answer)}, "source_text": answer,
                 "reviewer_id": "domain_expert", "verification_mode": "human_review",
                 "knowledge_snapshot_sha256": contract["knowledge_snapshot_sha256"]}]
    projected = project_verified_fact_evidence(
        question_text=question, answer_text=answer, facts=pair,
        question_contract=contract, requirement_evaluation=evaluation,
        reviewed_evidence=evidence,
    )
    assert projected["requirement_evaluation"]["requirements"][0]["status"] == "MISSING"
    assert projected["skipped"][0]["reason"] == "anchor_fact_group_incomplete"


def test_shared_anchor_cannot_be_satisfied_by_narrow_question_scope():
    rows = load_approved_fact_registry(Path(__file__).resolve().parents[1])["facts"]
    grouped = {}
    for row in rows:
        grouped.setdefault((row["topic_id"], row.get("legacy_anchor_id")), []).append(row)
    pair = next(value for key, value in grouped.items() if key[1] and len(value) == 2)
    _, question, answer, contract, evaluation, _ = sample()
    contract["knowledge_snapshot_sha256"] = fingerprint(sorted(pair, key=lambda row: row["fact_id"]))
    contract["requirements"][0]["fact_refs"] = [pair[0]["fact_id"]]
    evaluation["requirements"][0].update(owner_topic_id=pair[0]["topic_id"],
                                          requirement_id=pair[0]["legacy_anchor_id"])
    evidence = [{"fact_id": pair[0]["fact_id"],
                 "source_span": {"start": 0, "end": len(answer)}, "source_text": answer,
                 "reviewer_id": "domain_expert", "verification_mode": "human_review",
                 "knowledge_snapshot_sha256": contract["knowledge_snapshot_sha256"]}]
    projected = project_verified_fact_evidence(
        question_text=question, answer_text=answer, facts=pair,
        question_contract=contract, requirement_evaluation=evaluation,
        reviewed_evidence=evidence,
    )
    assert not projected["promoted"]
    assert projected["skipped"][0]["reason"] == "anchor_fact_group_incomplete"
