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


TOPIC = "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"
FIXTURE = REPO / "calibration/vmodel_sw_verification_overgrading_regression.json"
CANONICAL_IDS = {
    "sw04_v_model_definition",
    "sw04_unit_test",
    "sw04_integration_test",
    "sw04_system_test",
    "sw04_verification_definition",
    "sw04_validation_definition",
    "sw04_rtm_bidirectional",
    "sw04_configuration_baseline",
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


class VModelCanonicalPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_historical_overgrading_case_is_below_pass_with_canonical_reasons(self):
        case = self.fixture
        grade = grade_deterministically(
            question_text=case["question"], answer_text=case["answer"],
        )
        expected = case["expected"]
        self.assertGreaterEqual(grade["total_score"], expected["score_min"])
        self.assertLessEqual(grade["total_score"], expected["score_max"])
        self.assertFalse(grade["official_pass_met"])
        self.assertEqual(grade["provider_calls"], 0)
        rows = {
            row["requirement_id"]: row for row in grade["requirements"]
            if row["requirement_id"] in CANONICAL_IDS
        }
        self.assertEqual(
            {key: rows[key]["status"] for key in expected["canonical_requirement_status"]},
            expected["canonical_requirement_status"],
        )
        promotion = grade["canonical_promotion"]
        self.assertGreaterEqual(
            promotion["comparison_count"],
            expected["minimum_canonical_comparison_count"],
        )
        self.assertGreaterEqual(
            promotion["status_change_count"],
            expected["minimum_status_change_count"],
        )

    def test_complete_engineering_answer_satisfies_canonical_relations(self):
        answer = (
            "V-Model은 개발단계와 시험단계의 대응관계를 연결하고 시험기준을 개발 초기에 준비한다. "
            "단위시험은 소프트웨어 모듈을 검증하고 정상·경계·오류 경로를 검증한다. "
            "통합시험은 모듈 간 인터페이스를 검증하고 순서·타이밍·오류전파를 검증한다. "
            "시스템시험은 시스템 요구사항을 만족시키고 성능·장애복구·외부 인터페이스를 평가한다. "
            "Verification은 명세와 설계기준 적합성을 확인하고 Validation은 의도된 사용목적을 확인한다. "
            "RTM은 요구사항-설계-코드를 추적하고 순방향과 역방향을 추적한다. "
            "Baseline은 컴파일러 버전과 라이브러리 버전을 관리하고 변경 영향과 재검증을 관리한다."
        )
        rows, _, _ = canonical_rows(self.fixture["question"], answer)
        self.assertEqual(set(rows), CANONICAL_IDS)
        self.assertEqual({row["status"] for row in rows.values()}, {"SATISFIED"})

    def test_wrong_interface_claim_is_wrong_not_keyword_partial(self):
        answer = "통합시험은 모듈 간 인터페이스를 검증하지 않는다."
        rows, _, _ = canonical_rows(
            "단위시험, 통합시험과 시스템시험을 비교하고 적용절차를 설명하시오.",
            answer,
        )
        self.assertEqual(rows["sw04_integration_test"]["status"], "WRONG")

    def test_nested_module_word_does_not_create_unrelated_unit_claim(self):
        extraction = extract_canonical_claim_evidence(
            "통합시험은 모듈 간 인터페이스를 검증한다.", topic_ids=[TOPIC],
        )
        claims = extraction["canonical_evidence"]["claims"]
        self.assertFalse(any(
            row["subject"] == "integration_test"
            and row["object"] == "software_unit"
            for row in claims
        ))

    def test_question_scope_excludes_unrequested_anchor_contracts(self):
        rows, merged, _ = canonical_rows(
            "Verification과 Validation의 차이와 적용방법을 설명하시오.",
            "Verification은 명세와 설계기준 적합성을 확인한다. "
            "Validation은 의도된 사용목적을 확인한다.",
        )
        self.assertEqual(
            set(rows),
            {"sw04_verification_definition", "sw04_validation_definition"},
        )
        self.assertFalse(any(
            row["requirement_id"] == "sw04_unit_test"
            for row in merged["requirements"]
        ))


if __name__ == "__main__":
    unittest.main()
