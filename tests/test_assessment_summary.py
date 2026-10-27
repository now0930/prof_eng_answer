from study.assessment_summary import summarize_assessment


def test_60_target_uses_whole_assessment_not_each_question():
    grades = [
        {"question_id": str(index), "total_score": score, "max_score": 25}
        for index, score in enumerate((8, 17, 18, 17), 1)
    ]
    result = summarize_assessment(grades)
    assert result["decision"] == "TARGET_MET"
    assert result["points"] == 60
    assert result["target_met"] is True


def test_incomplete_assessment_cannot_pass():
    result = summarize_assessment([
        {"question_id": "1", "total_score": 24, "max_score": 25},
    ])
    assert result["decision"] == "INCOMPLETE"
    assert result["target_met"] is False


def test_complete_below_target():
    result = summarize_assessment([
        {"question_id": str(index), "total_score": 14, "max_score": 25}
        for index in range(4)
    ])
    assert result["decision"] == "BELOW_TARGET"


def test_duplicate_question_rejected():
    import pytest

    with pytest.raises(ValueError, match="duplicate"):
        summarize_assessment([
            {"question_id": "same", "total_score": 15},
            {"question_id": "same", "total_score": 15},
        ])


def test_provisional_grade_cannot_be_final_exam_input():
    import pytest

    with pytest.raises(ValueError, match="provisional"):
        summarize_assessment([{
            "question_id": "1", "total_score": 15,
            "resolution_review": {"required": True},
        }])
