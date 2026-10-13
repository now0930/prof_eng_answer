"""An independent reread can identify disagreement without granting a grade."""
from copy import deepcopy

import pytest

from grading.evidence.fact_semantic_review import review_assist_response
from grading.evidence.unresolved_semantic_assist import build_assist_request
from test_fact_candidate_resolver import fact


def inputs(excerpt="LOPA reduces risk."):
    row = fact()
    request = build_assist_request(
        question="Explain LOPA.", answer=excerpt, facts=[row],
        work_item={"requirement_id": "r1", "fact_ids": [row["fact_id"]],
                   "source_span": {"start": 0, "end": len(excerpt)},
                   "reason": "parser_unresolved"},
        versions={k: "v1" for k in ("model", "prompt", "parser", "verifier", "policy")},
    )
    first = {"rows": [{"fact_id": row["fact_id"], "interpretation": "supported",
                       "quote": excerpt, "reason": "first reading", "missing_conditions": []}]}
    return request, first


def support(request):
    return {"interpretation": "supported", "quote": request["excerpt"],
            "reason": "second reading", "missing_conditions": []}


def test_agreement_is_still_unverified_and_reviewer_is_blind():
    request, first = inputs()
    seen = []
    def reviewer(payload):
        seen.append(payload)
        return support(payload)
    result = review_assist_response(request=request, response=first, provider=reviewer,
                                    reviewer_version="v1")
    assert result["rows"][0]["state"] == "semantic_agreement"
    assert result["rows"][0]["independently_verified"] is False
    assert result["final_grade_allowed"] is False
    assert result["score_effect"] == "none"
    assert "first reading" not in str(seen)
    assert "rows" not in seen[0]


def test_disagreement_and_missing_condition_stay_out_of_scoring():
    request, first = inputs()
    def reviewer(payload):
        return {"interpretation": "unknown", "quote": payload["excerpt"],
                "reason": "not enough evidence", "missing_conditions": []}
    assert review_assist_response(request=request, response=first, provider=reviewer,
                                  reviewer_version="v1")["rows"][0]["state"] == "disagreement"
    with_condition = deepcopy(request)
    with_condition["facts"][0]["relation"]["conditions"] = ["requires_mode"]
    partial = deepcopy(first)
    partial["rows"][0]["interpretation"] = "partial"
    partial["rows"][0]["missing_conditions"] = ["requires_mode"]
    assert review_assist_response(request=with_condition, response=partial, provider=reviewer,
                                  reviewer_version="v1")["rows"][0]["state"] == "disagreement"


def test_wrong_sil_formula_is_blocked_before_review():
    request, first = inputs("PFD_avg <= F_H,max × F_D")
    def forbidden(payload):
        pytest.fail("reviewer must not see known invalid formula")
    result = review_assist_response(request=request, response=first, provider=forbidden,
                                    reviewer_version="v1")
    assert result["rows"][0]["state"] == "blocked"
    assert result["reviewer_calls"] == 0


@pytest.mark.parametrize("corrupt", [
    lambda value: value.update(score=25),
    lambda value: value.update(quote="invented"),
    lambda value: value.update(missing_conditions=["invented"]),
])
def test_invalid_review_cannot_create_agreement(corrupt):
    request, first = inputs()
    def reviewer(payload):
        value = support(payload)
        corrupt(value)
        return value
    result = review_assist_response(request=request, response=first, provider=reviewer,
                                    reviewer_version="v1")
    assert result["rows"][0]["state"] == "unresolved"
    assert result["rows"][0]["independently_verified"] is False


def test_cache_is_revalidated_and_versioned():
    request, first = inputs()
    cache = {}
    original = review_assist_response(request=request, response=first, provider=support,
                                      reviewer_version="v1", cache=cache)
    key = original["rows"][0]["review_hash"]
    assert review_assist_response(request=request, response=first, provider=support,
                                  reviewer_version="v1", cache=cache)["reviewer_calls"] == 0
    assert review_assist_response(request=request, response=first, provider=support,
                                  reviewer_version="v2", cache=cache)["reviewer_calls"] == 1
    cache[key]["quote"] = "not in answer"
    assert review_assist_response(request=request, response=first, provider=support,
                                  reviewer_version="v1", cache=cache)["rows"][0]["state"] == "unresolved"


def test_provider_failure_does_not_disclose_exception_text():
    request, first = inputs()
    def reviewer(payload):
        raise RuntimeError("SECRET ANSWER KEY")
    result = review_assist_response(request=request, response=first, provider=reviewer,
                                    reviewer_version="v1")
    assert result["rows"][0]["state"] == "unresolved"
    assert "SECRET ANSWER KEY" not in str(result)
