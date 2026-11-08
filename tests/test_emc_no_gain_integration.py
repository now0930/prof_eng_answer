"""EMC model-plus-wrong counterfactual must not increase score.

This test uses memory-only shadow authorization to exercise the held four
anchors. It never edits exclusion lists or calibration files.
"""

import json
from pathlib import Path
from unittest.mock import patch

from grading.evidence import fact_anchor_evidence_adapter as adapter
from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring
from grading.scoring.deterministic_primary_grader import grade_deterministically

ROOT = Path(__file__).resolve().parents[1]
TOPIC = "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
CANDIDATES = {
    "ipgse_scope_chain", "ipgse_emi_coupling_paths",
    "ipgse_power_quality_scope", "ipgse_final_verification",
}
WRONG = {
    "EMC_UNSAFE_PE_DISCONNECTION": "계장 노이즈를 제거하기 위해 보호접지 PE를 제거한다.",
    "EMC_SHIELD_ONE_END_UNIVERSAL": "모든 차폐 케이블은 반드시 한쪽만 접지한다.",
    "EMC_UPS_UNIVERSAL_FIX": "UPS를 사용하면 모든 EMC 문제가 해결된다.",
    "EMC_SHIELD_REPLACES_PE": "보호접지 PE를 cable shield로 대체하면 된다.",
    "EMC_SINGLE_POINT_UNIVERSAL": "단일점 접지는 모든 주파수에서 항상 최선이다.",
    "EMC_REDUNDANCY_IGNORES_CCF": "전원 공급장치 두 대를 병렬로 이중화하면 공통고장은 발생하지 않는다.",
    "EMC_GROUND_LOOP_RESISTANCE_ONLY": "Ground loop 문제는 저항만 낮추면 항상 해결된다.",
    "EMC_SINGLE_COUNTERMEASURE_UNIVERSAL": "EMC 문제는 필터 하나로 모든 노이즈가 해결된다.",
    "EMC_REWIRE_BEFORE_EVIDENCE": "노이즈가 보이면 측정 없이 shield 배선을 먼저 재결선해야 한다.",
}


def test_model_append_wrong_cannot_raise_score():
    path = ROOT / "calibration/expert_accuracy_model_answer_cases.json"
    bank = json.loads(path.read_text(encoding="utf-8"))
    case = next(row for row in bank["cases"] if row["case_id"].startswith(
        "model_reference_08_instrumentation_power"
    ))
    assert all(excluded_from_scoring(topic_id=TOPIC, anchor_id=anchor)
               for anchor in (*CANDIDATES, "ipgse_diagnostic_workflow"))

    existing = adapter.excluded_from_scoring

    def scoped_shadow(*, topic_id, anchor_id="", fact_id=""):
        if topic_id == TOPIC and anchor_id in CANDIDATES:
            return False
        return existing(topic_id=topic_id, anchor_id=anchor_id, fact_id=fact_id)

    def run(answer):
        return grade_deterministically(
            question_text=case["question"], answer_text=answer,
            qualitative_de_mode="off",
        )

    with patch.object(adapter, "excluded_from_scoring", side_effect=scoped_shadow):
        model = run(case["answer"])
        baseline = model["total_score"]
        assert isinstance(baseline, (int, float)) and 0 <= baseline <= 25.0
        for code, sentence in WRONG.items():
            trial = run(case["answer"].rstrip() + "\n\n" + sentence)
            assert trial["total_score"] <= baseline, (code, trial["total_score"], baseline)
            assert any(f["invariant_code"] == code for f in
                       trial["logic_check_evaluation"]["findings"])
            assert trial["official_pass_met"] is False
            assert trial["emc_no_gain_guard"]["status"] in {"CAP_APPLIED", "CHECKED_NO_CAP"}
            assert trial["emc_no_gain_guard"]["effective_total"] <= baseline

    assert all(excluded_from_scoring(topic_id=TOPIC, anchor_id=anchor)
               for anchor in (*CANDIDATES, "ipgse_diagnostic_workflow"))
