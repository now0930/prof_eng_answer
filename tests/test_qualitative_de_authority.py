"""Bounded D/E score replacement; deterministic A/B/C and ceilings remain owners."""

import json
from copy import deepcopy
from unittest.mock import patch

import pytest

from grading.scoring.deterministic_primary_grader import grade_deterministically
from grading.scoring.deterministic_score_engine import calculate_deterministic_score
from grading.quality.operational_checksheet import build_quality_checksheet


QUESTION = "열전대와 RTD의 원리, 특성 비교, 정확도 요인과 개선 방안을 설명하시오."
ANSWER = (
    "열전대는 제벡 효과로 온도차를 잰다. RTD는 저항 변화로 온도를 잰다. "
    "4선식은 리드선 오차를 줄인다."
)


def _valid_de(prompt):
    data = json.loads(prompt)
    row = next(row for row in data["requirements"] if row["status"] in {"SATISFIED", "PARTIAL"})
    start, end = row["source_span"]["start"], row["source_span"]["end"]
    criteria = []
    for key in ("D1", "D2", "D3", "E1", "E2"):
        positive = key == "D1"
        criteria.append({
            "criterion_id": key, "score": 1 if positive else 0,
            "reason": "답안 근거를 제시함" if positive else "독립적인 근거가 부족함",
            "topic_id": row["owner_topic_id"],
            "quote": data["answer"][start:end] if positive else None,
            "start": start if positive else None,
            "end": end if positive else None,
        })
    return json.dumps({"criteria": criteria, "interview_questions": [],
                       "abc_observations": []}, ensure_ascii=False)


def test_valid_argon_de_replaces_only_d_e_and_recomputes_total():
    original = grade_deterministically(
        question_text=QUESTION, answer_text=ANSWER, qualitative_de_mode="off")
    grade = grade_deterministically(
        question_text=QUESTION, answer_text=ANSWER,
        qualitative_de_mode="argon", qualitative_de_llm_fn=_valid_de)
    old = original["deterministic_score"]["score_breakdown"]
    new = grade["deterministic_score"]["score_breakdown"]
    for key in ("A_structure", "B_requirement_completeness", "C_fact_correctness"):
        assert new[key] == old[key]
    assert new["D_engineering_judgment"] == 1
    assert new["E_linkage"] == 0
    assert grade["total_score"] == original["total_score"] + 1
    assert grade["qualitative_de_evaluation"]["status"] == "APPLIED"
    assert grade["qualitative_de_evaluation"]["score_effect"] == "replace_de"
    assert grade["provider_calls"] == 1
    assert grade["llm_score_authority"] == "D_E_ONLY"
    assert grade["llm_verdict_authority"] == 0
    checks = {row["check_id"]: row for row in build_quality_checksheet(grade)["checks"]}
    assert checks["score_authority"]["result"] == "pass"
    tampered = deepcopy(grade)
    tampered["llm_score_authority"] = "A_B_C_D_E"
    checks = {row["check_id"]: row for row in build_quality_checksheet(tampered)["checks"]}
    assert checks["score_authority"]["result"] == "fail"


def test_invalid_or_unavailable_argon_falls_back_without_zeroing_d_e():
    original = grade_deterministically(
        question_text=QUESTION, answer_text=ANSWER, qualitative_de_mode="off")
    invalid = grade_deterministically(
        question_text=QUESTION, answer_text=ANSWER,
        qualitative_de_mode="argon", qualitative_de_llm_fn=lambda prompt: '{"total_score":25}')
    assert invalid["qualitative_de_evaluation"]["status"] == "FALLBACK"
    assert invalid["total_score"] == original["total_score"]
    assert invalid["deterministic_score"]["score_breakdown"] == original["deterministic_score"]["score_breakdown"]
    assert invalid["provider_calls"] == 1
    checks = {row["check_id"]: row for row in build_quality_checksheet(invalid)["checks"]}
    assert checks["score_authority"]["result"] == "pass"
    with patch.dict("os.environ", {"GEMINI_API_KEY": ""}):
        absent = grade_deterministically(
            question_text=QUESTION, answer_text=ANSWER, qualitative_de_mode="argon")
    assert absent["qualitative_de_evaluation"]["status"] == "FALLBACK"
    assert absent["qualitative_de_evaluation"]["reason_code"] == "provider_not_configured"
    assert absent["provider_calls"] == 0
    assert absent["total_score"] == original["total_score"]


def test_argon_override_cannot_remove_fatal_or_pass_ceiling():
    evaluation = {
        "requirements": [{"status": "SATISFIED"}] * 3 + [{"status": "WRONG"}],
        "findings": [{"classification": "fatal", "recommended_ceiling": 13.0}],
        "fatal_or_core_error": True,
    }
    result = calculate_deterministic_score(
        evaluation, answer_text="공정 조건에서 선정하고 검증 결과를 기록한다.",
        de_override={"D_engineering_judgment": 6, "E_linkage": 2},
    )
    assert result["qualitative_de_score_effect"] == "replace_de"
    assert result["total_score"] <= 13.0
    assert result["verdict"] == "NEEDS_CORRECTION"
    assert result["official_pass_met"] is False
    with pytest.raises(ValueError, match="invalid_qualitative_de_override"):
        calculate_deterministic_score(
            evaluation, answer_text="답안",
            de_override={"D_engineering_judgment": 7, "E_linkage": 2},
        )
