import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from canonical_claim_extractor import extract_canonical_claim_evidence
from deterministic_primary_grader import grade_deterministically


TOPIC = "sil_target_determination_risk_reduction_and_lifecycle"
FIXTURE = REPO / "calibration/sil_target_operations_overgrading_regression.json"
PROMOTED_IDS = {
    "sis_sif_sil_scope",
    "required_rrf_relation",
    "target_pfd_relation",
    "demand_mode_metric_selection",
    "achieved_sil_verification",
    "operations_moc_revalidation",
    "cyber_ai_safety_boundary",
}


def topic_rows(grade):
    return {
        row["requirement_id"]: row
        for row in grade["requirements"]
        if row["owner_topic_id"] == TOPIC
    }


class SilTargetCanonicalPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_original_retains_four_fatal_states_and_canonical_missing_details(self):
        grade = grade_deterministically(
            question_text=self.fixture["question"],
            answer_text=self.fixture["original_answer"],
        )
        rows = topic_rows(grade)
        self.assertEqual(grade["total_score"], 13.0)
        self.assertFalse(grade["official_pass_met"])
        self.assertEqual(
            {key: rows[key]["status"] for key in (
                "target_pfd_relation",
                "demand_mode_metric_selection",
                "proof_test_diagnostics_reliability",
                "operations_moc_security_ai_lifecycle",
            )},
            {
                "target_pfd_relation": "WRONG",
                "demand_mode_metric_selection": "WRONG",
                "proof_test_diagnostics_reliability": "WRONG",
                "operations_moc_security_ai_lifecycle": "WRONG",
            },
        )
        self.assertEqual(rows["sis_sif_sil_scope"]["status"], "SATISFIED")
        for requirement_id in (
            "required_rrf_relation",
            "achieved_sil_verification",
            "operations_moc_revalidation",
            "cyber_ai_safety_boundary",
        ):
            self.assertEqual(rows[requirement_id]["status"], "MISSING")
        self.assertEqual(grade["canonical_promotion"]["comparison_count"], 7)

    def test_corrected_answer_recognizes_all_promoted_relations(self):
        original = grade_deterministically(
            question_text=self.fixture["question"],
            answer_text=self.fixture["original_answer"],
        )
        corrected = grade_deterministically(
            question_text=self.fixture["question"],
            answer_text=self.fixture["corrected_answer"],
        )
        rows = topic_rows(corrected)
        self.assertGreaterEqual(corrected["total_score"] - original["total_score"], 2.0)
        self.assertTrue(corrected["official_pass_met"])
        self.assertEqual(
            {rows[key]["status"] for key in PROMOTED_IDS}, {"SATISFIED"}
        )
        self.assertEqual(rows["proof_test_diagnostics_reliability"]["status"], "SATISFIED")
        self.assertEqual(rows["operations_moc_security_ai_lifecycle"]["status"], "SATISFIED")

    def test_frequency_ratio_formula_is_extracted_without_answer_hardcoding(self):
        evidence = extract_canonical_claim_evidence(
            "저수요에서 목표 PFDavg는 F_target/(F_D*product(P_i))로 정한다.",
            topic_ids=[TOPIC],
        )
        self.assertTrue(any(
            row["subject"] == "target_probability"
            and row["predicate"] == "derived_by_ratio"
            and row["object"] == "event_frequencies"
            for row in evidence["canonical_evidence"]["claims"]
        ))

    def test_negative_surface_supplement_relation_is_positive_canonical_fact(self):
        evidence = extract_canonical_claim_evidence(
            "PST는 full-stroke proof test를 대체하지 않는다.",
            topic_ids=[TOPIC],
        )
        matches = [
            row for row in evidence["canonical_evidence"]["claims"]
            if row["subject"] == "partial_stroke_test"
            and row["predicate"] == "supplements"
            and row["object"] == "full_proof_test"
        ]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["polarity"], "positive")

    def test_explicit_negation_of_ai_lifecycle_control_is_wrong(self):
        grade = grade_deterministically(
            question_text=self.fixture["question"],
            answer_text=(
                "AI 생성 코드는 IEC 61508/61511 수명주기 통제를 적용하지 않는다. "
                "OT 보안은 기능안전과의 상호영향을 함께 검증한다."
            ),
        )
        self.assertEqual(
            topic_rows(grade)["cyber_ai_safety_boundary"]["status"], "WRONG"
        )


if __name__ == "__main__":
    unittest.main()
