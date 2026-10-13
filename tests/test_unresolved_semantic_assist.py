from copy import deepcopy

import pytest

from grading.evidence.unresolved_semantic_assist import assist_unresolved
from test_fact_candidate_resolver import fact


def run(provider, **changes):
    options = dict(question="Explain risk reduction.", answer="LOPA reduces risk.",
                   facts=[fact()], work_items=[{
                       "requirement_id": "r1", "fact_ids": ["risk_reduction"],
                       "source_span": {"start": 0, "end": 18}, "reason": "unmatched_expression"}],
                   versions={k: "v1" for k in ("model", "prompt", "parser", "verifier", "policy")},
                   provider=provider, enabled=True)
    options.update(changes)
    return assist_unresolved(**options)


def response(request):
    return {"rows": [{"fact_id": "risk_reduction", "interpretation": "supported",
                      "quote": request["excerpt"], "reason": "fixture interpretation",
                      "missing_conditions": []}]}


def test_disabled_and_no_work_make_no_calls():
    def forbidden(request):
        pytest.fail("provider should not be called")
    assert run(forbidden, enabled=False)["provider_calls"] == 0
    assert run(forbidden, work_items=[])["items"] == []


def test_proposal_never_grants_score_or_verification():
    result = run(response)
    assert result["items"][0]["state"] == "pending_verification"
    assert result["items"][0]["verified"] is False
    assert result["score_effect"] == "none"
    assert result["final_grade_allowed"] is False


@pytest.mark.parametrize("mutation", [
    lambda r: r["rows"][0].update(score=25),
    lambda r: r["rows"][0].update(quote="invented quote"),
    lambda r: r["rows"][0].update(fact_id="out_of_scope"),
    lambda r: r["rows"].clear(),
    lambda r: r["rows"][0].update(missing_conditions=["invented_condition"]),
])
def test_invalid_model_responses_stay_unresolved(mutation):
    def provider(request):
        value = response(request)
        mutation(value)
        return value
    assert run(provider)["items"][0]["state"] == "unresolved"


def test_timeout_preserves_unresolved_without_error_body():
    def provider(request):
        raise TimeoutError("private credentials")
    result = run(provider)
    assert result["items"][0]["error_type"] == "TimeoutError"
    assert "private credentials" not in str(result)


def test_cache_reuse_invalidation_and_revalidation():
    cache = {}
    first = run(response, cache=cache)
    assert run(response, cache=cache)["provider_calls"] == 0
    assert run(response, cache=cache, answer="LOPA reduces risk. Extra.")["provider_calls"] == 1
    versions = {k: "v2" for k in ("model", "prompt", "parser", "verifier", "policy")}
    assert run(response, cache=cache, versions=versions)["provider_calls"] == 1
    key = first["items"][0]["request_hash"]
    cache[key]["rows"][0]["quote"] = "corrupt"
    assert run(response, cache=cache)["items"][0]["state"] == "unresolved"


def test_input_objects_remain_unchanged():
    facts = [fact()]
    original = deepcopy(facts)
    def provider(request):
        value = response(request)
        request["facts"].clear()
        return value
    run(provider, facts=facts)
    assert facts == original
