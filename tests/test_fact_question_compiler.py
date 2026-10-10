"""Question-only compilation must fail closed on knowledge gaps and ambiguity."""

from __future__ import annotations

import copy
import inspect

import pytest

from grading.evidence.fact_grounded_contracts import VERSION, FactGroundedContractError
from grading.routing.fact_question_compiler import compile_question_contract


QUESTION = "LOPA의 위험감소 결정 방법을 설명하라."
ALIASES = {"risk_reduction": ["위험감소"]}


def fact(fact_id: str = "risk_reduction", status: str = "approved") -> dict:
    return {
        "schema_version": VERSION, "fact_id": fact_id,
        "topic_id": "sil_target_determination_risk_reduction_and_lifecycle",
        "statement": "합성 사실", "relation": {
            "subject": "lopa", "predicate": "determines", "object": "risk_reduction",
            "conditions": [],
        },
        "source_refs": [{
            "source_id": "fixture:post:1", "source_version": "1",
            "source_sha256": "a" * 64, "locator": "section:body",
        }],
        "review_status": status, "revision": 1, "score_effect": "none",
    }


def requirement(task: str = "explain", targets: list[str] | None = None) -> dict:
    return {
        "schema_version": VERSION, "candidate_id": "requirement_1",
        "kind": "question_requirement", "source_span": {"start": 0, "end": len(QUESTION)},
        "source_text": QUESTION,
        "proposal": {"task": task, "target_concepts": targets or ["risk_reduction"], "conditions": []},
        "producer": {"mode": "deterministic_parser", "resolver_id": "fixture", "resolver_version": "1"},
        "score_effect": "none",
    }


def test_unique_approved_fact_resolves_without_answer_input() -> None:
    assert "answer_text" not in inspect.signature(compile_question_contract).parameters
    result = compile_question_contract(QUESTION, [fact()], [requirement()], concept_aliases=ALIASES)
    assert result["requirements"][0]["resolution"] == "resolved"
    assert result["requirements"][0]["fact_refs"] == ["risk_reduction"]
    assert result["score_effect"] == "none"


def test_unapproved_fact_is_knowledge_gap() -> None:
    result = compile_question_contract(QUESTION, [fact(status="candidate")], [requirement()])
    assert result["requirements"][0]["resolution"] == "knowledge_gap"
    assert result["requirements"][0]["fact_refs"] == []


def test_multiple_facts_and_complex_task_remain_ambiguous() -> None:
    two = [fact(), fact("risk_reduction_alternative")]
    assert compile_question_contract(QUESTION, two, [requirement()], concept_aliases=ALIASES)["requirements"][0]["resolution"] == "ambiguous"
    assert compile_question_contract(QUESTION, [fact()], [requirement("compare")], concept_aliases=ALIASES)["requirements"][0]["resolution"] == "ambiguous"


def test_unverified_alias_or_semantic_candidate_cannot_resolve() -> None:
    assert compile_question_contract(QUESTION, [fact()], [requirement()])["requirements"][0]["resolution"] == "ambiguous"
    candidate = requirement()
    candidate["producer"]["mode"] = "semantic_resolver"
    assert compile_question_contract(QUESTION, [fact()], [candidate], concept_aliases=ALIASES)["requirements"][0]["resolution"] == "ambiguous"


def test_conditions_and_target_must_match_explicitly() -> None:
    conditioned = fact()
    conditioned["relation"]["conditions"] = ["scenario_boundary"]
    assert compile_question_contract(QUESTION, [conditioned], [requirement()])["requirements"][0]["resolution"] == "knowledge_gap"
    assert compile_question_contract(QUESTION, [fact()], [requirement(targets=["sil_target"])])["requirements"][0]["resolution"] == "knowledge_gap"


def test_unanchored_or_authoritative_candidate_is_rejected() -> None:
    invalid = requirement()
    invalid["source_text"] = "답안에서 끌어온 요구"
    with pytest.raises(FactGroundedContractError):
        compile_question_contract(QUESTION, [fact()], [invalid])
    invalid = copy.deepcopy(requirement())
    invalid["proposal"]["score"] = 25
    with pytest.raises(FactGroundedContractError):
        compile_question_contract(QUESTION, [fact()], [invalid])


def test_same_question_and_facts_compile_to_same_contract() -> None:
    first = compile_question_contract(QUESTION, [fact()], [requirement()], concept_aliases=ALIASES)
    second = compile_question_contract(QUESTION, [copy.deepcopy(fact())], [copy.deepcopy(requirement())], concept_aliases=ALIASES)
    assert first == second
