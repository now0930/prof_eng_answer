"""A universal checklist must not earn credit for change-specific OT analysis."""

from grading.scoring.deterministic_primary_grader import grade_deterministically


QUESTION = (
    "산업용 제어시스템에 Management of Change(MOC)를 적용할 때 "
    "변경요청, 영향분석, 승인, 실행 및 종료절차를 설명하시오."
)
TARGET = "sw06_impact_analysis_multidisciplinary"
EXCLUDED = "sw06_moc_trigger_and_scope"


def test_general_moc_preserves_scope_and_rejects_asserted_universal_checklist():
    normal = "영향분석: 변경마다 실제로 영향을 받는 통신, HMI, 안전기능을 식별하고 복구계획을 검토한다."
    cases = [
        (normal, "SATISFIED"),
        (normal + " OSHA PSM 적용 공정의 해당 변경에만 별도 법적 요건을 확인한다.", "SATISFIED"),
        (normal + ' “모든 변경에 동일한 고정 체크리스트를 강제한다”는 틀린 주장이다.', "SATISFIED"),
        (normal + " 모든 변경에 동일한 고정 체크리스트를 강제한다는 주장은 틀렸다.", "SATISFIED"),
        (
            "영향분석: 모든 변경에 동일한 고정 체크리스트를 강제한다. "
            "통신, HMI, 안전기능, 복구계획을 전부 검토한다.",
            "MISSING",
        ),
    ]
    for answer, expected in cases:
        grade = grade_deterministically(
            question_text=QUESTION, answer_text=answer, qualitative_de_mode="off",
        )
        rows = {row["requirement_id"]: row for row in grade["requirements"]}
        assert EXCLUDED not in rows
        assert rows[TARGET]["status"] == expected
        if expected == "MISSING":
            assert rows[TARGET]["source_span"] is None
