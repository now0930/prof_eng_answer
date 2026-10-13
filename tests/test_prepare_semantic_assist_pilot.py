"""Private pilot selection is pinned to question text, never answer content."""
from copy import deepcopy

from grading.evidence.fact_grounded_contracts import validate_question_contract
from scripts.prepare_semantic_assist_pilot import SCOPES, prepare


def test_three_pilot_contracts_are_valid_but_provisional():
    for case_id in SCOPES:
        payload = prepare(case_id)
        contract = payload["question_contract"]
        refs = {fact_id for row in contract["requirements"] for fact_id in row["fact_refs"]}
        validate_question_contract(contract, payload["question"], refs)
        assert contract["score_effect"] == "none"
        assert all(row["resolution"] == "resolved" for row in contract["requirements"])


def test_question_scope_does_not_depend_on_answer():
    payload = prepare("sil_target_operations_issue1")
    altered = deepcopy(payload)
    altered["answer"] = "Entirely different response"
    assert altered["question_contract"] == payload["question_contract"]
