"""Cross-layer alignment: traceable, strictly score-neutral, no live LLM."""
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from grading.evidence.canonical_grading_evidence import build_canonical_grading_evidence
from grading.evidence.claim_alignment_contract import (
    ClaimAlignmentError, build_alignment_result, validate_alignment_result,
)
from grading.evidence.claim_alignment_engine import analyze_claim_alignment
from grading.evidence.fact_claim_adapter import project_fact_claims
from grading.evidence.logic_rule_adapter import project_logic_rules
from grading.evidence.semantic_admission import (
    SemanticAdmissionError, evaluate_semantic_admission,
)


TOPIC = "pid_controller_tuning_sequence_gain_effects"
ANSWER = "I 제어는 정상상태 오차를 줄일 수 있다."
FACT = {
    "owner_topic_id": TOPIC, "fact_id": "i_action_effect",
    "parent_anchor_id": "i_action_effect", "importance": "must",
    "relation": {
        "subject": "integral_action", "predicate": "reduces",
        "object": "steady_state_error", "polarity": "positive",
        "conditions": [],
    },
    "projection_status": "VERIFIED_REGISTRY_RELATION", "source_fact_id": "registry_i",
}
SOURCE = {"mode": "deterministic_parser", "resolver_id": "test_parser",
          "resolver_version": "1"}


def claim(*, polarity="positive", conditions=None, assertion_context="asserted"):
    return {
        **FACT["relation"], "claim_id": "cl_1", "polarity": polarity,
        "conditions": list(conditions or []),
        "assertion_context": assertion_context,
        "source_text": ANSWER,
        "source_span": {"start": 0, "end": len(ANSWER)},
    }


def parsed(*, polarity="positive", conditions=None, context="asserted"):
    doc = build_canonical_grading_evidence(
        question_text="I 동작을 설명하시오.",
        answer_text=ANSWER, source=SOURCE,
        claims=[claim(polarity=polarity, conditions=conditions,
                      assertion_context=context)],
    )
    return {"canonical_evidence": doc, "unresolved_spans": []}


def align(parser_output=None, fact=None):
    with patch("grading.evidence.claim_alignment_engine.project_fact_claims",
               return_value=[copy.deepcopy(fact or FACT)]), patch(
        "grading.evidence.claim_alignment_engine.project_logic_rules",
        return_value=[],
    ):
        return analyze_claim_alignment(
            question_text="I 동작을 설명하시오.", answer_text=ANSWER,
            topic_ids=[TOPIC], parser_output=parser_output or parsed(),
            required_by_topic={TOPIC: {"i_action_effect"}},
        )


def test_exact_claim_maps_to_fact_without_score():
    result = align()
    assert result["score_effect"] == "none"
    assert result["authority"] == "audit_only"
    assert result["summary"]["relation_counts"]["EXACT_RELATION"] == 1
    assert result["alignments"][0]["fact_id"] == "i_action_effect"
    assert ANSWER not in json.dumps(result, ensure_ascii=False)
    validate_alignment_result(result, answer_text=ANSWER)


def test_missing_fact_condition_never_becomes_full_match():
    fact = copy.deepcopy(FACT)
    fact["relation"]["conditions"] = ["closed_loop_stable"]
    result = align(fact=fact)
    assert result["alignments"][0]["relation"] == "CONDITION_GAP"


def test_opposite_polarity_is_candidate_not_fatal():
    result = align(parsed(polarity="negative"))
    assert result["alignments"][0]["relation"] == "CONTRADICTION_CANDIDATE"
    assert "severity" not in result["alignments"][0]
    assert "WRONG" not in json.dumps(result)


@pytest.mark.parametrize("context", ["quoted", "rejected", "corrected"])
def test_nonasserted_claim_never_triggers_alignment(context):
    result = align(parsed(context=context))
    assert result["summary"]["alignment_count"] == 0


def test_unstructured_fact_cannot_infer_relation():
    fact = copy.deepcopy(FACT)
    fact["relation"] = None
    result = align(fact=fact)
    assert result["summary"]["alignment_count"] == 0


def test_stale_question_cannot_reuse_a_valid_answer_alignment():
    # Valid answer text and valid evidence hash are not enough: the question
    # and its selected scope must be the ones the parser actually saw.
    with patch("grading.evidence.claim_alignment_engine.project_fact_claims",
               return_value=[copy.deepcopy(FACT)]), patch(
        "grading.evidence.claim_alignment_engine.project_logic_rules",
        return_value=[],
    ):
        with pytest.raises(ValueError, match="question fingerprint"):
            analyze_claim_alignment(
                question_text="전혀 다른 질문", answer_text=ANSWER,
                topic_ids=[TOPIC], parser_output=parsed(),
            )


def test_modified_canonical_claim_with_stale_evidence_digest_is_rejected():
    stale = parsed()
    stale["canonical_evidence"]["claims"][0]["predicate"] = "unrelated_to"
    with pytest.raises(ValueError, match="evidence fingerprint"):
        align(parser_output=stale)


def test_semantic_resolver_cannot_impersonate_the_deterministic_parser():
    foreign = build_canonical_grading_evidence(
        question_text="I 동작을 설명하시오.", answer_text=ANSWER,
        source={"mode": "semantic_resolver",
                "resolver_id": "reviewer", "resolver_version": "1"},
        claims=[claim()],
    )
    with pytest.raises(ValueError, match="requires deterministic parser"):
        align(parser_output={"canonical_evidence": foreign, "unresolved_spans": []})


def test_claim_with_explicit_foreign_topic_ownership_cannot_align():
    other_owner = claim()
    other_owner["qualifiers"] = {
        "owner_topic_id": "thermocouple_temperature_sensor_seebeck_reference_junction_compensation",
    }
    foreign = build_canonical_grading_evidence(
        question_text="I 동작을 설명하시오.", answer_text=ANSWER,
        source=SOURCE, claims=[other_owner],
    )
    result = align(parser_output={
        "canonical_evidence": foreign, "unresolved_spans": [],
    })
    assert result["summary"]["alignment_count"] == 0


def test_foreign_answer_hash_fails_closed():
    other = parsed()
    with pytest.raises(ValueError, match="fingerprint"):
        with patch("grading.evidence.claim_alignment_engine.project_fact_claims"):
            analyze_claim_alignment(
                question_text="other", answer_text=ANSWER + "!",
                topic_ids=[TOPIC], parser_output=other,
            )


def test_corrupt_fingerprint_and_score_injection_rejected():
    result = align()
    changed = copy.deepcopy(result)
    changed["alignments"][0]["relation"] = "UNRESOLVED"
    with pytest.raises(ClaimAlignmentError, match="fingerprint"):
        validate_alignment_result(changed, answer_text=ANSWER)
    changed = copy.deepcopy(result)
    changed["score_effect"] = "replace_abc"
    with pytest.raises(ClaimAlignmentError, match="cannot change scores"):
        validate_alignment_result(changed, answer_text=ANSWER)


def test_semantic_agreement_is_not_independent_proof():
    result = align()
    proposal = {"fact_id": "i_action_effect", "interpretation": "supported",
                "quote": ANSWER}
    accepted = evaluate_semantic_admission(
        suggestion=proposal, review={"state": "semantic_agreement"},
        alignment=result, valid_fact_ids={"i_action_effect"},
        source_span={"start": 0, "end": len(ANSWER)}, answer_text=ANSWER,
    )
    assert accepted["state"] == "ALIGNED_WITH_DETERMINISTIC_EVIDENCE"
    assert accepted["final_grade_allowed"] is False
    assert accepted["score_effect"] == "none"
    fact = copy.deepcopy(FACT)
    fact["relation"]["conditions"] = ["closed_loop_stable"]
    pending = evaluate_semantic_admission(
        suggestion=proposal, review={"state": "semantic_agreement"},
        alignment=align(fact=fact), valid_fact_ids={"i_action_effect"},
        source_span={"start": 0, "end": len(ANSWER)}, answer_text=ANSWER,
    )
    assert pending["state"] == "PENDING"
    foreign = evaluate_semantic_admission(
        suggestion={**proposal, "quote": "허위 답변"},
        review={"state": "semantic_agreement"},
        alignment=result, valid_fact_ids={"i_action_effect"},
        source_span={"start": 0, "end": len(ANSWER)}, answer_text=ANSWER,
    )
    assert foreign["state"] == "PENDING"
    assert foreign["reason_codes"] == ["unbound_or_foreign_quote"]
    unbound = evaluate_semantic_admission(
        suggestion=proposal, review={"state": "semantic_agreement"},
        alignment=result, valid_fact_ids={"i_action_effect"},
    )
    assert unbound["state"] == "PENDING"
    assert "unbound_answer_span" in unbound["reason_codes"]
    with pytest.raises(SemanticAdmissionError):
        evaluate_semantic_admission(
            suggestion={"fact_id": "unapproved", "interpretation": "supported"},
            review={"state": "semantic_agreement"}, alignment=result,
            valid_fact_ids={"i_action_effect"},
        )


def test_fact_projection_respects_score_exclusion_and_scope():
    with tempfile.TemporaryDirectory() as td:
        topic_dir = Path(td) / "rubrics/topic_packs" / TOPIC
        topic_dir.mkdir(parents=True)
        (topic_dir / "fact_anchor.json").write_text(json.dumps({
            "anchors": [
                {"anchor_id": "i_action_effect", "importance": "must"},
                {"anchor_id": "blocked", "importance": "optional"},
            ],
        }), encoding="utf-8")
        contract = {
            "owner_topic_id": TOPIC,
            "facts": [{"fact_id": "i_action_effect", **FACT["relation"]}],
        }
        with patch("grading.evidence.fact_claim_adapter.ROOT", Path(td)), patch(
            "grading.evidence.fact_claim_adapter.load_machine_contracts",
            return_value=[contract],
        ), patch(
            "grading.evidence.fact_claim_adapter.excluded_from_scoring",
            side_effect=lambda **kw: kw["anchor_id"] == "blocked",
        ):
            rows = project_fact_claims(
                [TOPIC], required_by_topic={TOPIC: {"i_action_effect", "blocked"}},
            )
    assert len(rows) == 1
    assert rows[0]["projection_status"] == "STRUCTURED_MACHINE_RELATION"
    assert rows[0]["relation"]["subject"] == "integral_action"


def test_disabled_logic_rules_never_activate_in_projection():
    with tempfile.TemporaryDirectory() as td:
        directory = Path(td) / "rubrics/topic_packs" / TOPIC
        directory.mkdir(parents=True)
        path = directory / "logic_check.json"
        path.write_text(json.dumps({
            "deterministic_checks": {
                "enabled": False,
                "fatal_checks": [{"id": "bad", "severity": "fatal"}],
            },
        }), encoding="utf-8")
        with patch("grading.evidence.logic_rule_adapter.ROOT", Path(td)):
            assert project_logic_rules([TOPIC]) == []
        path.write_text(json.dumps({
            "deterministic_checks": {
                "enabled": True,
                "fatal_checks": [{"id": "bad", "severity": "fatal"}],
            },
        }), encoding="utf-8")
        with patch("grading.evidence.logic_rule_adapter.ROOT", Path(td)):
            rules = project_logic_rules([TOPIC])
            assert rules[0]["rule_id"] == "bad"
            assert rules[0]["authority"] == "existing_logic_evaluator_only"


def test_missing_or_empty_deterministic_logic_profile_has_no_fallback_rules():
    with tempfile.TemporaryDirectory() as td:
        directory = Path(td) / "rubrics/topic_packs" / TOPIC
        directory.mkdir(parents=True)
        path = directory / "logic_check.json"
        # Top-level rules can be profile examples rather than enabled
        # deterministic checks. Do not silently activate them in the audit.
        root_fatal = [{"id": "top_level_only", "severity": "fatal"}]
        for data in (
            {"fatal_checks": root_fatal},
            {"fatal_checks": root_fatal, "deterministic_checks": {}},
            {"fatal_checks": root_fatal, "deterministic_checks": {"fatal_checks": []}},
            {"fatal_checks": root_fatal, "deterministic_checks": {
                "enabled": False, "fatal_checks": root_fatal,
            }},
        ):
            path.write_text(json.dumps(data), encoding="utf-8")
            with patch("grading.evidence.logic_rule_adapter.ROOT", Path(td)):
                assert project_logic_rules([TOPIC]) == []

        path.write_text(json.dumps({
            "deterministic_checks": {
                "fatal_checks": [{"id": "nested_default_on", "severity": "fatal"}],
            },
        }), encoding="utf-8")
        with patch("grading.evidence.logic_rule_adapter.ROOT", Path(td)):
            projected = project_logic_rules([TOPIC])
        assert len(projected) == 1
        assert projected[0]["rule_id"] == "nested_default_on"


def test_registry_verified_relation_preferred_to_machine_contract():
    with tempfile.TemporaryDirectory() as td:
        folder = Path(td) / "rubrics/topic_packs" / TOPIC
        folder.mkdir(parents=True)
        (folder / "fact_anchor.json").write_text(json.dumps({
            "anchors": [{"anchor_id": "i_action_effect", "importance": "must"}],
        }), encoding="utf-8")
        canonical_registry = dict(FACT["relation"])
        canonical_registry["predicate"] = "eliminates"
        with patch("grading.evidence.fact_claim_adapter.ROOT", Path(td)), patch(
            "grading.evidence.fact_claim_adapter.load_machine_contracts",
            return_value=[{"owner_topic_id": TOPIC,
                           "facts": [{"fact_id": "i_action_effect", **FACT["relation"]}]}],
        ), patch(
            "grading.evidence.fact_claim_adapter._verified_source_index",
            return_value={(TOPIC, "i_action_effect"): {
                "source_fact_id": "registry_i", "revision": 1,
                "relation": canonical_registry}},
        ), patch(
            "grading.evidence.fact_claim_adapter.excluded_from_scoring",
            return_value=False,
        ):
            rows = project_fact_claims([TOPIC], required_by_topic={TOPIC: {"i_action_effect"}})
            unscoped = project_fact_claims([TOPIC], required_by_topic={})
    assert not unscoped
    assert rows[0]["projection_status"] == "VERIFIED_REGISTRY_RELATION"
    assert rows[0]["relation"]["predicate"] == "eliminates"
    assert rows[0]["machine_relation_differs"] is True
    assert rows[0]["source_fact_id"] == "registry_i"

def test_duplicate_verified_fact_legacy_ids_do_not_select_one_arbitrarily():
    from grading.evidence.fact_claim_adapter import _registry_index
    f = {"topic_id": TOPIC, "legacy_anchor_id": "common_anchor",
         "review_status": "approved", "verification_status": "verified",
         "revision": 1, "relation": dict(FACT["relation"])}
    with patch("grading.evidence.fact_claim_adapter.load_approved_fact_registry",
               return_value={"facts": [
                   {**f, "fact_id": "distinct_fact_one"},
                   {**f, "fact_id": "distinct_fact_two"},
               ]}):
        # Unique synthetic cache key; no actual registry or network access.
        result = _registry_index("synthetic_root_for_duplicate_test", 12, 34)
    assert (TOPIC, "common_anchor") not in result

def test_unverified_machine_relation_is_never_claimed_as_verified():
    machine_only = copy.deepcopy(FACT)
    machine_only["projection_status"] = "STRUCTURED_MACHINE_RELATION"
    machine_only["source_fact_id"] = None
    result = align(fact=machine_only)
    assert result["alignments"][0]["relation"] == "UNRESOLVED"
    assert result["alignments"][0]["reason"] == "source_relation_not_independently_verified"


def test_absolute_quantifier_keeps_relation_unresolved_without_logic_check():
    answer = "I 제어는 항상 정상상태 오차를 줄인다."
    c = {
        **FACT["relation"], "claim_id": "claim_universal",
        "source_text": answer, "source_span": {"start": 0, "end": len(answer)},
        "assertion_context": "asserted",
    }
    doc = build_canonical_grading_evidence(
        question_text="I 동작을 설명하시오.", answer_text=answer,
        source=SOURCE, claims=[c],
    )
    with patch("grading.evidence.claim_alignment_engine.project_fact_claims",
               return_value=[copy.deepcopy(FACT)]), patch(
        "grading.evidence.claim_alignment_engine.project_logic_rules",
        return_value=[],
    ):
        result = analyze_claim_alignment(
            question_text="I 동작을 설명하시오.", answer_text=answer,
            topic_ids=[TOPIC], parser_output={
                "canonical_evidence": doc, "unresolved_spans": [],
            },
        )
    assert result["alignments"][0]["relation"] == "UNRESOLVED"
    assert result["alignments"][0]["reason"] == "absolute_quantifier_requires_logic_verification"


def test_alignment_cannot_reference_a_fact_outside_projection():
    with pytest.raises(ClaimAlignmentError, match="non-projected"):
        build_alignment_result(
            answer_text=ANSWER, topic_ids=[TOPIC],
            fact_projection=[copy.deepcopy(FACT)], logic_projection=[],
            alignments=[{
                "answer_claim_id": "claim1",
                "fact_id": "invented_answer_fact",
                "owner_topic_id": TOPIC, "relation": "EXACT_RELATION",
                "reason": "forged", "source_span": {"start": 0, "end": len(ANSWER)},
            }],
            unresolved=[],
        )
