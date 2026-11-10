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
    assert result["total_score"] == 14.5
    assert result["deterministic_score"]["score_floor_policy"] == "earned_only"
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


def test_legacy_replay_exposes_removed_15_point_floor(monkeypatch):
    answer = (
        "차압식 유량계는 차압의 제곱근에 비례한다. "
        "층류식 유량계는 차압에 비례한다."
    )
    earned = grade_deterministically(question_text=QUESTION, answer_text=answer)
    monkeypatch.setenv("ESSAY_LEGACY_15_FLOOR", "1")
    legacy = grade_deterministically(question_text=QUESTION, answer_text=answer)
    assert legacy["total_score"] == 15.0
    assert earned["total_score"] == 14.5
    assert earned["deterministic_score"]["score_floor_policy"] == "earned_only"
    assert earned["deterministic_score"]["technically_adequate_floor_applied"] is False


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


def test_symbolic_dp_formula_variants_are_recognized_as_partial_without_inferred_conditions():
    question = "차압식 유량계의 원리와 유량 환산 시 적용조건을 설명하시오."
    formulas = (
        "Q=K√(ΔP/ρ)",
        r"Q = K \sqrt{\Delta P / \rho}",
        "Q ∝ √ΔP",
    )
    results = [
        grade_deterministically(question_text=question, answer_text=formula)
        for formula in formulas
    ]
    for result in results:
        rows = {row["requirement_id"]: row for row in result["requirements"]}
        assert rows["flow_dp_primary_element_conditions"]["status"] == "PARTIAL"
        assert result["provider_calls"] == 0
        assert result["total_score"] < 15.0
        if result["symbolic_formula_evidence"]:
            candidate = result["symbolic_formula_evidence"][0]
            assert candidate["candidate_status"] == "PARTIAL"
            assert candidate["unstated_conditions_inferred"] is False
            assert candidate["dimension_check"] == "not_inferred"


def test_symbolic_linear_dp_formula_is_wrong_but_counts_as_addressed_for_b():
    result = grade_deterministically(
        question_text="차압식 유량계의 원리와 유량 환산 시 적용조건을 설명하시오.",
        answer_text="Q=K·ΔP",
    )
    row = next(
        row for row in result["requirements"]
        if row["requirement_id"] == "flow_dp_primary_element_conditions"
    )
    assert row["status"] == "WRONG"
    assert result["deterministic_score"]["score_breakdown"]["B_requirement_completeness"] == 3.0
    assert result["deterministic_score"]["score_breakdown"]["C_fact_correctness"] == 0.0
    assert result["provider_calls"] == 0


def test_composite_dp_question_is_provisional_when_approved_scope_covers_only_some_demands():
    question = (
        "차압식 유량계의 원리와 유량 환산 시 적용조건, 측정 정확도에 영향을 주는 "
        "요인과 개선 대책, 현장 적용 시 고려사항을 설명하시오."
    )
    answer = (
        "체적유량은 Q=K√(ΔP/ρ)로 나타낸다. Vena Contracta 위치에 따라 K가 달라진다. "
        "압력 측정 위치가 정확도에 영향을 준다고 설명하고, Impulse Line의 막힘·누설을 "
        "점검하며 진단과 유지보수를 고려한다. 설치비, 이중화와 정지 위험도 비교한다."
    )
    result = grade_deterministically(question_text=question, answer_text=answer)
    diagnostic = result["question_scope_evaluation"]["diagnostics"][0]
    assert result["topic_id"] == TOPIC
    assert diagnostic["status"] == "INCOMPLETE_COMPOSITE_SCOPE"
    assert {"improvement_methods", "field_application"} <= set(diagnostic["unrepresented_facets"])
    assert result["resolution_review"]["score_status"] == "provisional"
    assert result["resolution_review"]["reason"] == "question_scope_incomplete"
    assert result["requirement_summary"]["UNRESOLVED"] == 1
    assert result["verdict"] == "REVIEW_REQUIRED"
    assert not result["official_pass_met"]
    assert result["provider_calls"] == 0
