import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from canonical_claim_extractor import extract_canonical_claim_evidence
from deterministic_primary_grader import grade_deterministically
from deterministic_requirement_evaluator import evaluate_deterministic_requirements
from fact_anchor_evidence_adapter import (
    augment_requirement_evaluation,
    evaluate_fact_anchor_requirements,
    requirement_scope_by_topic,
)


TOPIC = "hazop_lopa_ipl_risk_reduction_sil_target_allocation"
FIXTURE = REPO / "calibration/sis_lopa_architecture_overgrading_regression.json"
CANONICAL_IDS = {
    "hazop_lopa_lopa_scenario_boundary",
    "hazop_lopa_initiating_event_frequency",
    "hazop_lopa_ipl_definition",
    "hazop_lopa_residual_frequency_after_existing_ipls",
    "hazop_lopa_required_rrf",
    "hazop_lopa_pfdavg_rrf_relation",
    "hazop_lopa_sil_band_mapping",
    "hazop_lopa_sif_allocation_boundary",
    "hazop_lopa_srs_handoff",
}


def canonical_rows(question: str, answer: str):
    anchors = evaluate_fact_anchor_requirements(
        question_text=question, answer_text=answer, topic_ids=[TOPIC],
    )
    extraction = extract_canonical_claim_evidence(
        answer, question_text=question, topic_ids=[TOPIC],
    )
    evaluation = evaluate_deterministic_requirements(
        claims=extraction["canonical_evidence"]["claims"],
        invariant_codes=[], topic_ids=[TOPIC], extraction_complete=True,
        requirement_scope_by_topic=requirement_scope_by_topic(anchors),
    )
    merged = augment_requirement_evaluation(evaluation, anchors)
    return {
        row["requirement_id"]: row
        for row in merged["requirements"]
        if row["requirement_id"] in CANONICAL_IDS
    }, merged, extraction


class HazopLopaCanonicalPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_historical_architecture_case_stays_below_pass_with_specific_gaps(self):
        case = self.fixture
        grade = grade_deterministically(
            question_text=case["question"], answer_text=case["answer"],
        )
        rows = {
            row["requirement_id"]: row for row in grade["requirements"]
            if row["requirement_id"] in CANONICAL_IDS
        }
        expected_range = case["expected"]["total_range"]
        self.assertLessEqual(grade["total_score"], expected_range["max"])
        self.assertEqual(
            grade["total_score"],
            grade["deterministic_score"]["score_before_floors"],
        )
        self.assertFalse(
            grade["deterministic_score"]["substantive_fatal_floor_applied"]
        )
        self.assertFalse(grade["official_pass_met"])
        self.assertEqual(grade["provider_calls"], 0)
        self.assertEqual(grade["canonical_promotion"]["comparison_count"], 9)
        self.assertEqual(rows["hazop_lopa_pfdavg_rrf_relation"]["status"], "PARTIAL")
        self.assertEqual(rows["hazop_lopa_sif_allocation_boundary"]["status"], "PARTIAL")
        for requirement_id in CANONICAL_IDS - {
            "hazop_lopa_pfdavg_rrf_relation",
            "hazop_lopa_sif_allocation_boundary",
        }:
            self.assertEqual(rows[requirement_id]["status"], "MISSING")

    def test_complete_lopa_answer_satisfies_all_nine_relations(self):
        answer = (
            "LOPA scenario는 initiating event와 consequence endpoint로 경계를 정의한다. "
            "Initiating event frequency는 원인 사건이 발생하는 빈도를 의미하며 "
            "설비 이력과 신뢰성 자료를 근거로 산정한다. "
            "IPL은 독립성과 검증가능성을 충족할 때 인정한다. "
            "Residual frequency는 initiating event frequency와 조건부 수정인자 및 "
            "인정 가능한 기존 IPL의 PFD를 근거로 산정한다. "
            "RRF_required는 F_residual/F_tolerable 비로 계산한다. "
            "PFDavg_target은 1/RRF_required이며 F_tolerable/F_residual의 빈도 비로 정한다. "
            "목표 SIL은 PFDavg·PFH SIL 구간에 매핑한다. "
            "전체 SIF 고장은 센서·로직솔버·최종요소로 구성한다. "
            "SIF 할당은 trip setpoint·safe state·response time·process safety time을 정의한다. "
            "LOPA 결과는 원인·감지변수·trip 조건·safe state·목표 SIL·응답시간·"
            "proof test·bypass·reset·운전모드를 SRS 입력으로 인계한다."
        )
        rows, _, _ = canonical_rows(self.fixture["question"], answer)
        self.assertEqual(set(rows), CANONICAL_IDS)
        self.assertEqual({row["status"] for row in rows.values()}, {"SATISFIED"})

    def test_component_list_without_safe_function_boundary_is_partial(self):
        rows, _, _ = canonical_rows(
            self.fixture["question"],
            "전체 SIF 고장은 센서·로직솔버·최종요소로 구성한다.",
        )
        self.assertEqual(rows["hazop_lopa_sif_allocation_boundary"]["status"], "PARTIAL")

    def test_rejected_ipl_independence_is_wrong(self):
        rows, _, _ = canonical_rows(
            "독립보호계층 IPL의 인정조건과 이중계산 방지방안을 설명하시오.",
            "IPL은 독립성과 검증가능성을 충족하지 않는다.",
        )
        self.assertEqual(rows["hazop_lopa_ipl_definition"]["status"], "WRONG")

    def test_narrow_rrf_question_activates_only_its_three_machine_contracts(self):
        rows, merged, _ = canonical_rows(
            "RRF, PFDavg와 SIL의 관계를 설명하고 목표 SIL과 달성 SIL을 비교하시오.",
            "RRF_required는 F_residual/F_tolerable 비로 계산한다. "
            "PFDavg_target은 1/RRF_required이며 F_tolerable/F_residual의 빈도 비로 정한다. "
            "목표 SIL은 PFDavg·PFH SIL 구간에 매핑한다.",
        )
        self.assertEqual(
            set(rows),
            {
                "hazop_lopa_required_rrf",
                "hazop_lopa_pfdavg_rrf_relation",
                "hazop_lopa_sil_band_mapping",
            },
        )
        self.assertFalse(any(
            row["requirement_id"] == "hazop_lopa_sif_allocation_boundary"
            for row in merged["requirements"]
        ))


if __name__ == "__main__":
    unittest.main()
