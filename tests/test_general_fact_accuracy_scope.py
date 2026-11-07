"""Universal-Fact question scope and Korean-expression score boundaries."""

import json
from pathlib import Path

from grading.scoring.deterministic_primary_grader import grade_deterministically


ROOT = Path(__file__).resolve().parents[1]


def test_operational_change_answer_levels_are_separated_without_llm():
    payload = json.loads(
        (ROOT / "calibration/qtype_golden/cases/implementation_evaluation.json")
        .read_text(encoding="utf-8")
    )
    scores = {}
    for case in payload["cases"]:
        if case["case_id"] not in {"QG-IE-LOW-01", "QG-IE-PASS-01", "QG-IE-HIGH-01"}:
            continue
        grade = grade_deterministically(
            question_text=case["question"],
            answer_text=case["answer"],
            qualitative_de_mode="off",
        )
        scores[case["case_id"]] = grade["total_score"]
        assert grade["provider_calls"] == 0
    assert set(scores) == {"QG-IE-LOW-01", "QG-IE-PASS-01", "QG-IE-HIGH-01"}
    assert scores["QG-IE-LOW-01"] < 15
    assert 15 <= scores["QG-IE-PASS-01"] < 20
    assert scores["QG-IE-HIGH-01"] >= 20
