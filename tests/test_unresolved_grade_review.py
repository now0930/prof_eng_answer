from grading.scoring.deterministic_primary_grader import grade_deterministically
from bot import format_result


QUESTION = "차압식 유량계와 층류식 유량계에서 차압과 유량의 관계를 비교하고 적용 조건을 설명하시오."


def test_related_unresolved_sentence_requires_review_without_inventing_credit():
    result = grade_deterministically(
        question_text=QUESTION,
        answer_text=(
            "차압식 유량계는 압력과 유량에 관계가 있다. "
            "층류식 유량계는 차압에 비례한다."
        ),
        qualitative_de_mode="off",
    )
    assert result["resolution_review"]["required"] is True
    assert "flow_dp_primary_element_conditions" in result["resolution_review"]["requirement_ids"]
    assert result["resolution_review"]["score_status"] == "provisional"
    assert result["passing_score_allowed"] is False
    assert result["official_pass_met"] is False
    assert result["verdict"] == "REVIEW_REQUIRED"
    assert result["provider_calls"] == 0
    display = format_result(result)
    assert "문항 참고선(전체 60/100 환산): 15점 (보류)" in display
    assert "판정: 의미 해석 검토 필요(잠정 점수)" in display


def test_complete_relation_remains_final():
    result = grade_deterministically(
        question_text=QUESTION,
        answer_text=(
            "차압식 유량계는 차압의 제곱근에 비례한다. "
            "층류식 유량계는 차압에 비례한다."
        ),
        qualitative_de_mode="off",
    )
    assert result["resolution_review"]["required"] is False
    assert result["resolution_review"]["score_status"] == "final"
