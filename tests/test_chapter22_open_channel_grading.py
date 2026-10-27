"""Synthetic open-channel candidate checks; no personal answers are used."""

from grading.scoring.deterministic_primary_grader import grade_deterministically


TOPIC = "open_channel_weir_flume_head_discharge_submergence_selection"
QUESTION = "직사각형 위어와 V-notch 위어의 수두-유량 관계를 비교하고, 플룸의 수몰 영향을 설명하시오."
CORRECT = (
    "직사각형 위어는 자유 월류에서 유량이 수두의 3/2 제곱에 비례한다. "
    "V-notch 위어는 자유 월류에서 유량이 수두의 5/2 제곱에 비례한다. "
    "플룸은 하류 수위가 높아져 수몰되면 수몰 보정이 필요하다."
)
WRONG = (
    "직사각형 위어는 수두의 5/2 제곱에 비례한다. "
    "V-notch 위어는 수두의 3/2 제곱에 비례한다. "
    "플룸은 수몰 보정이 필요 없다."
)


def test_open_channel_question_routes_to_own_topic_and_credits_relations():
    result = grade_deterministically(question_text=QUESTION, answer_text=CORRECT)
    assert result["topic_id"] == TOPIC
    assert result["provider_calls"] == 0
    assert result["requirement_summary"]["SATISFIED"] == 3
    assert all(row["owner_topic_id"] == TOPIC for row in result["requirements"])


def test_swapped_weir_exponents_and_omitted_submergence_correction_are_wrong():
    result = grade_deterministically(question_text=QUESTION, answer_text=WRONG)
    assert result["topic_id"] == TOPIC
    assert result["requirement_summary"]["WRONG"] == 3
    assert result["total_score"] < grade_deterministically(
        question_text=QUESTION, answer_text=CORRECT,
    )["total_score"]
