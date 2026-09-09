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
    evaluate_fact_anchor_requirements,
    requirement_scope_by_topic,
)


MCDC_TOPIC = "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
SW_TOPIC = "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"
FIXTURE = REPO / "calibration/mcdc_vmodel_sil_overgrading_regression.json"


def canonical_rows(topic: str, question: str, answer: str):
    anchors = evaluate_fact_anchor_requirements(
        question_text=question, answer_text=answer, topic_ids=[topic],
    )
    extraction = extract_canonical_claim_evidence(
        answer, question_text=question, topic_ids=[topic],
    )
    evaluation = evaluate_deterministic_requirements(
        claims=extraction["canonical_evidence"]["claims"],
        invariant_codes=[], topic_ids=[topic], extraction_complete=True,
        requirement_scope_by_topic=requirement_scope_by_topic(anchors),
    )
    return {row["requirement_id"]: row for row in evaluation["requirements"]}


class McdcCrossTopicCanonicalPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_reviewed_operating_case_preserves_range_and_four_fatals(self):
        case = self.fixture
        grade = grade_deterministically(
            question_text=case["question"], answer_text=case["answer"],
        )
        expected = case["expected"]
        self.assertGreaterEqual(grade["total_score"], expected["total_range"]["min"])
        self.assertLessEqual(grade["total_score"], expected["total_range"]["max"])
        self.assertFalse(grade["official_pass_met"])
        self.assertEqual(grade["provider_calls"], 0)
        self.assertEqual(set(grade["topic_ids"]), set(case["expected_topic_ids"]))
        finding_ids = {
            row["finding_id"] for row in grade["logic_check_evaluation"]["findings"]
        }
        self.assertEqual(finding_ids, set(expected["required_fatal_ids"]))
        rows = {row["requirement_id"]: row for row in grade["requirements"]}
        self.assertEqual(rows["sw04_v_model_definition"]["status"], "PARTIAL")
        self.assertEqual(rows["sw04_unit_test"]["status"], "WRONG")
        self.assertEqual(rows["sw04_system_test"]["status"], "PARTIAL")
        self.assertEqual(rows["sw04_static_analysis"]["status"], "PARTIAL")
        self.assertEqual(rows["sw04_dynamic_analysis"]["status"], "PARTIAL")
        self.assertEqual(rows["mcdc_one_hundred_percent_limit"]["status"], "WRONG")
        self.assertEqual(grade["canonical_promotion"]["comparison_count"], 8)
        self.assertEqual(grade["deterministic_score"]["raw_requirement_count"], 13)
        self.assertEqual(grade["deterministic_score"]["scoring_group_count"], 8)

    def test_exact_cross_topic_scope_does_not_activate_all_topic_anchors(self):
        case = self.fixture
        grade = grade_deterministically(
            question_text=case["question"], answer_text=case["answer"],
        )
        ids = {row["requirement_id"] for row in grade["requirements"]}
        self.assertNotIn("mcdc_dead_code", ids)
        self.assertNotIn("sw04_configuration_baseline", ids)
        self.assertNotIn("proof_test_relation", ids)

    def test_concept_mention_is_partial_never_satisfied(self):
        rows = canonical_rows(
            SW_TOPIC,
            "정적분석, 동적분석과 회귀시험의 목적과 차이를 설명하시오.",
            "정적분석과 동적분석을 수행한다.",
        )
        self.assertEqual(rows["sw04_static_analysis"]["status"], "PARTIAL")
        self.assertEqual(rows["sw04_dynamic_analysis"]["status"], "PARTIAL")

    def test_complete_mcdc_relations_are_satisfied(self):
        question = "MC/DC의 개념, 목적과 충족조건을 설명하시오."
        answer = (
            "MC/DC는 구조적 커버리지이다. "
            "MC/DC는 각 원자 조건의 독립 영향을 검증한다. "
            "MC/DC 적용 수준은 적용 표준에 따라 결정한다. "
            "MC/DC는 전체 SIL 달성을 단독으로 보장하지 않는다."
        )
        rows = canonical_rows(MCDC_TOPIC, question, answer)
        expected = {
            "mcdc_normative_applicability",
            "mcdc_purpose",
            "mcdc_definition",
            "mcdc_one_hundred_percent_limit",
        }
        self.assertEqual(set(rows), expected)
        self.assertEqual({rows[key]["status"] for key in expected}, {"SATISFIED"})

    def test_denied_independent_effect_is_wrong(self):
        rows = canonical_rows(
            MCDC_TOPIC,
            "MC/DC의 개념, 목적과 충족조건을 설명하시오.",
            "MC/DC는 각 원자 조건의 독립 영향을 검증하지 않는다.",
        )
        self.assertEqual(rows["mcdc_definition"]["status"], "WRONG")

    def test_static_and_dynamic_analysis_use_relations_not_keywords(self):
        rows = canonical_rows(
            SW_TOPIC,
            "정적분석, 동적분석과 회귀시험의 목적과 차이를 설명하시오.",
            "정적분석은 실행하지 않고 규칙위반·데이터흐름·제어흐름과 잠재 결함을 분석한다. "
            "동적분석은 실행 중 경로·시간·자원·인터페이스와 실제 반응을 분석한다.",
        )
        self.assertEqual(rows["sw04_static_analysis"]["status"], "SATISFIED")
        self.assertEqual(rows["sw04_dynamic_analysis"]["status"], "SATISFIED")

    def test_lifecycle_question_does_not_activate_unrequested_mcdc_relations(self):
        rows = canonical_rows(
            MCDC_TOPIC,
            "MC/DC가 소프트웨어 수명주기 검증·확인에서 사용하는 구조적 커버리지 증거이며 다른 수명주기 활동을 대체하지 않는 이유를 설명",
            "MC/DC는 요구사항 추적성·독립성·검증·확인 활동을 대체하지 않고 보완한다.",
        )
        self.assertIn("mcdc_lifecycle_vv_boundary", rows)
        self.assertEqual(rows["mcdc_lifecycle_vv_boundary"]["status"], "SATISFIED")
        self.assertNotIn("mcdc_definition", rows)
        self.assertNotIn("mcdc_one_hundred_percent_limit", rows)


if __name__ == "__main__":
    unittest.main()
