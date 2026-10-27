"""Chapter 22 DP-versus-laminar question contract regression."""

from grading.scoring.deterministic_primary_grader import grade_deterministically


TOPIC = "flow_measurement_meter_principles_velocity_selection"
QUESTION = "차압식 유량계와 층류식 유량계에서 차압과 유량의 관계를 비교하고 적용 조건을 설명하시오."
CORRECT = (
    "차압식 오리피스는 베르누이 관계로 비압축성 정상 유동에서 유량이 차압의 제곱근에 비례한다. "
    "방출계수와 베타비, 밀도, 레이놀즈 수 보정이 필요하다. "
    "층류식 유량계는 Hagen-Poiseuille 관계에서 유량이 차압에 비례하고 "
    "점도와 관 길이 및 반지름에 영향을 받는다."
)
SWAPPED = (
    "차압식 유량계는 유량이 차압에 비례한다. "
    "층류식 유량계는 유량이 차압의 제곱근에 비례한다."
)


def test_chapter22_correct_dp_and_laminar_relations_are_scored():
    result = grade_deterministically(question_text=QUESTION, answer_text=CORRECT)
    assert result["topic_id"] == TOPIC
    assert result["provider_calls"] == 0
    assert result["question_scope_evaluation"]["selections"][0]["mode"] == "explicit_question_contract"
    states = {row["requirement_id"]: row["status"] for row in result["requirements"]}
    assert states == {
        "flow_dp_primary_element_conditions": "SATISFIED",
        "flow_laminar_pressure_relation": "SATISFIED",
        "flow_dp_conversion_conditions": "SATISFIED",
        "flow_laminar_regime_conditions": "SATISFIED",
    }


def test_chapter22_swapped_relations_are_wrong_not_missing():
    result = grade_deterministically(question_text=QUESTION, answer_text=SWAPPED)
    assert result["topic_id"] == TOPIC
    assert result["provider_calls"] == 0
    assert result["requirement_summary"]["WRONG"] == 2
    assert result["total_score"] < grade_deterministically(
        question_text=QUESTION, answer_text=CORRECT,
    )["total_score"]


def test_chapter22_bare_relations_do_not_earn_condition_requirements():
    result = grade_deterministically(
        question_text=QUESTION,
        answer_text=(
            "차압식 유량계는 차압의 제곱근에 비례한다. "
            "층류식 유량계는 차압에 비례한다."
        ),
    )
    assert result["requirement_summary"]["MISSING"] == 2
    assert result["total_score"] < grade_deterministically(
        question_text=QUESTION, answer_text=CORRECT,
    )["total_score"]


def test_symbolic_equivalent_relations_are_recognized():
    result = grade_deterministically(
        question_text=QUESTION,
        answer_text=(
            "차압식 유량계의 Q는 √ΔP에 비례한다. "
            "층류식 유량계의 Q는 ΔP에 선형 비례한다."
        ),
    )
    states = {row["requirement_id"]: row["status"] for row in result["requirements"]}
    assert states["flow_dp_primary_element_conditions"] == "SATISFIED"
    assert states["flow_laminar_pressure_relation"] == "SATISFIED"


def test_chapter22_dp_only_question_does_not_require_laminar_fact():
    result = grade_deterministically(
        question_text="차압식 유량계의 원리와 유량 환산 시 적용조건을 설명하시오.",
        answer_text="차압식 유량계는 차압의 제곱근에 비례하는 유량을 측정한다.",
    )
    assert result["topic_id"] == TOPIC
    assert {row["requirement_id"] for row in result["requirements"]} == {
        "flow_dp_primary_element_conditions"
    }


def test_unrelated_new_subject_does_not_inherit_dp_qualification():
    result = grade_deterministically(
        question_text=QUESTION,
        answer_text=(
            "차압식 유량계는 차압의 제곱근에 비례한다. "
            "제어밸브는 방출계수와 베타비 보정이 필요하다. "
            "층류식 유량계는 차압에 비례한다."
        ),
    )
    states = {row["requirement_id"]: row["status"] for row in result["requirements"]}
    assert states["flow_dp_conversion_conditions"] != "SATISFIED"


def test_dp_qualification_is_not_inherited_across_paragraph_break():
    result = grade_deterministically(
        question_text=QUESTION,
        answer_text=(
            "차압식 유량계는 차압의 제곱근에 비례한다.\n\n"
            "방출계수와 베타비 보정이 필요하다. "
            "층류식 유량계는 차압에 비례한다."
        ),
    )
    states = {row["requirement_id"]: row["status"] for row in result["requirements"]}
    assert states["flow_dp_conversion_conditions"] != "SATISFIED"
