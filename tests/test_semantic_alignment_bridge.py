"""Private LLM review can be audited against verified Facts, never score A-E."""
from __future__ import annotations

import copy
import hashlib

import pytest

from grading.evidence.claim_alignment_contract import build_alignment_result
from grading.evidence.fact_grounded_contracts import fingerprint
from grading.evidence.semantic_alignment_bridge import (
    SemanticAlignmentBridgeError, link_private_semantic_report,
)

QUESTION = "열전대 측정 원리를 설명하시오."
ANSWER = "열전대의 전압은 두 접점 온도에 따라 달라진다."
TOPIC = "thermocouple_temperature_sensor_seebeck_reference_junction_compensation"
ANCHOR = "thermocouple_measures_temperature_difference"
FACT_ID = "verified_thermocouple_temperature_difference"
FACT = {
    "fact_id": FACT_ID, "topic_id": TOPIC, "legacy_anchor_id": ANCHOR,
    "review_status": "approved", "verification_status": "verified",
}
SPAN = {"start": 0, "end": len(ANSWER)}


def alignment(verified=True, exact=True):
    fact_projection = [{
        "owner_topic_id": TOPIC, "fact_id": ANCHOR,
        "parent_anchor_id": ANCHOR,
        "projection_status": (
            "VERIFIED_REGISTRY_RELATION" if verified
            else "STRUCTURED_MACHINE_RELATION"
        ),
        "source_fact_id": FACT_ID if verified else None,
        "relation": None, "importance": "must",
    }]
    return build_alignment_result(
        answer_text=ANSWER, topic_ids=[TOPIC],
        fact_projection=fact_projection,
        logic_projection=[],
        alignments=[{
            "answer_claim_id": "claim1", "fact_id": ANCHOR,
            "owner_topic_id": TOPIC,
            "relation": "EXACT_RELATION" if exact else "CONDITION_GAP",
            "reason": "fixture", "source_span": SPAN,
        }],
        unresolved=[],
    )


def report(*, state="semantic_agreement", quote=ANSWER):
    return {
        "schema_version": "semantic-assist-private-run-v1",
        "question_sha256": hashlib.sha256(QUESTION.encode()).hexdigest(),
        "answer_sha256": hashlib.sha256(ANSWER.encode()).hexdigest(),
        "facts_sha256": fingerprint([FACT]),
        "score_effect": "none", "final_grade_allowed": False,
        "result": {
            "score_effect": "none", "final_grade_allowed": False,
            "assistance": {
                "items": [{
                    "requirement_id": "req_1",
                    "source_span": SPAN,
                    "proposals": [{
                        "fact_id": FACT_ID,
                        "interpretation": "supported",
                        "quote": quote,
                        "missing_conditions": [],
                    }],
                    "semantic_review": {"rows": [
                        {"fact_id": FACT_ID, "state": state},
                    ]},
                }],
            },
        },
    }


def run(*, source=None, align=None, facts=None):
    return link_private_semantic_report(
        question=QUESTION, answer=ANSWER, report=source or report(),
        alignment=align or alignment(), approved_facts=facts or [FACT],
    )


def test_verified_fact_exact_span_and_review_are_only_diagnostic():
    r = run()
    assert r["disposition_counts"] == {
        "ALIGNED_WITH_DETERMINISTIC_EVIDENCE": 1,
    }
    assert r["score_effect"] == "none"
    assert r["final_grade_allowed"] is False
    assert "total_score" not in r
    assert ANSWER not in str(r)


def test_independent_disagreement_remains_pending():
    r = run(source=report(state="disagreement"))
    assert r["disposition_counts"] == {"PENDING": 1}
    assert r["rows"][0]["reason_codes"] == ["independent_review_not_agreed"]


def test_source_without_verified_projection_never_admits():
    r = run(align=alignment(verified=False))
    assert r["rows"][0]["state"] == "PENDING"
    assert "fact_outside_verified_question_scope" in r["rows"][0]["reason_codes"]


def test_conditions_and_foreign_quote_remain_pending():
    r = run(align=alignment(exact=False))
    assert r["rows"][0]["state"] == "PENDING"
    r = run(source=report(quote="원문에 없는 허위 근거"))
    assert r["rows"][0]["reason_codes"] == ["unbound_or_foreign_quote"]


def test_tampered_hash_and_scoring_authority_are_blocked():
    stale = report()
    stale["answer_sha256"] = "0" * 64
    with pytest.raises(SemanticAlignmentBridgeError):
        run(source=stale)
    scored = report()
    scored["final_grade_allowed"] = True
    with pytest.raises(SemanticAlignmentBridgeError):
        run(source=scored)
    mismatched = report()
    mismatched["result"]["score_effect"] = "replace_bc"
    with pytest.raises(SemanticAlignmentBridgeError):
        run(source=mismatched)


def test_absent_parser_span_is_a_hard_error():
    broken = report()
    del broken["result"]["assistance"]["items"][0]["source_span"]
    with pytest.raises(SemanticAlignmentBridgeError, match="parser_span"):
        run(source=broken)


def test_unapproved_fact_cannot_reappear_through_llm():
    bad_fact = copy.deepcopy(FACT)
    bad_fact["verification_status"] = "unverified"
    with pytest.raises(SemanticAlignmentBridgeError, match="unapproved_fact"):
        run(facts=[bad_fact])
