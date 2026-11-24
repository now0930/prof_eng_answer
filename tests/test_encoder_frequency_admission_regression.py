"""One-Anchor encoder frequency admission regression; offline and provider-free."""
import unittest

from grading.evidence.fact_anchor_evidence_adapter import (
    evaluate_fact_anchor_requirements,
)
from grading.routing.deterministic_topic_router import route_question_topics
from grading.scoring.deterministic_primary_grader import grade_deterministically
from grading.scoring.deterministic_score_engine import calculate_deterministic_score

TOPIC = "speed_rotation_measurement_encoder_proximity_tachometer_selection_error"
ANCHOR = "encoder_frequency_limit_selection"
QUESTION = (
    "Encoder의 PPR/CPR, quadrature decoding 및 maximum frequency 선정관계를 설명하시오."
)
CASES = {
    "canonical": (
        "Encoder와 receiving counter/PLC에는 최대 output/input frequency가 "
        "있으므로 최고 회전속도와 N_eff의 곱이 허용 주파수를 넘지 않도록 선정한다. "
        "해상도를 높이면 동일 속도에서 pulse frequency도 증가한다."
    ),
    "opposite": (
        "Encoder와 receiving counter/PLC에는 최대 output/input frequency 제한이 "
        "없으므로 최고 회전속도와 N_eff의 곱이 허용 주파수를 넘어도 상관없다. "
        "해상도를 높이면 동일 속도에서 pulse frequency는 증가하지 않는다."
    ),
    "mention": "maximum frequency, N_eff, PLC counter 세 가지 용어를 열거한다.",
    "correct": (
        "Encoder와 PLC의 최대 입력 주파수를 확인하고, 최고 회전속도 및 encoder "
        "해상도에 따른 출력 pulse frequency를 점검하여 counter 처리 한계 이내로 선정한다."
    ),
}


def anchor_row(answer):
    result = evaluate_fact_anchor_requirements(
        answer_text=answer, topic_ids=[TOPIC], question_text=QUESTION,
    )
    rows = [row for row in result["requirements"] if row["requirement_id"] == ANCHOR]
    if len(rows) != 1:
        raise AssertionError(f"target anchor count={len(rows)}")
    return rows[0]


class EncoderFrequencyAdmissionRegression(unittest.TestCase):
    def test_question_owner_and_target_are_active(self):
        route = route_question_topics(QUESTION)
        self.assertEqual(route["status"], "ROUTED")
        self.assertEqual(route["primary_topic_id"], TOPIC)
        for answer in CASES.values():
            row = anchor_row(answer)
            self.assertEqual(row["importance"], "core")
            self.assertEqual(row["evidence_mode"], "bounded_encoder_frequency_relation")

    def test_four_original_cases_prevent_keyword_credit(self):
        expected = {
            "canonical": "SATISFIED",
            "opposite": "MISSING",
            "mention": "MISSING",
            "correct": "PARTIAL",
        }
        for name, answer in CASES.items():
            with self.subTest(case=name):
                row = anchor_row(answer)
                self.assertEqual(row["status"], expected[name])
                if name in {"opposite", "mention"}:
                    self.assertIsNone(row["source_span"])
                    self.assertEqual(row["evidence_text"], "")

    def test_full_scoring_path_and_target_status(self):
        for name, answer in CASES.items():
            with self.subTest(case=name):
                grade = grade_deterministically(
                    question_text=QUESTION, answer_text=answer,
                    qualitative_de_mode="off",
                )
                rows = [
                    row for row in grade["requirements"]
                    if row["owner_topic_id"] == TOPIC and row["requirement_id"] == ANCHOR
                ]
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["status"], anchor_row(answer)["status"])
                self.assertEqual(grade["llm_verdict_authority"], 0)
                self.assertIsInstance(grade["total_score"], (int, float))
                self.assertFalse(grade["resolution_review"]["required"])

    def test_isolated_requirement_credit_is_monotone(self):
        results = {}
        for name, answer in CASES.items():
            row = anchor_row(answer)
            results[name] = calculate_deterministic_score(
                {"requirements": [row], "findings": [], "fatal_or_core_error": False},
            )
            self.assertEqual(results[name]["decision"], "SCORED")
        self.assertGreater(
            results["canonical"]["total_score"],
            results["correct"]["total_score"],
        )
        self.assertGreater(
            results["correct"]["total_score"],
            results["mention"]["total_score"],
        )
        self.assertEqual(
            results["mention"]["total_score"],
            results["opposite"]["total_score"],
        )

    def test_explicit_positive_paraphrase_is_admitted(self):
        row = anchor_row(
            "엔코더와 PLC 입력의 최대 주파수를 확인해 허용 범위 이내로 선정한다. "
            "동일 회전수에서 PPR을 높이면 출력 펄스 주파수가 증가한다."
        )
        self.assertEqual(row["status"], "SATISFIED")

    def test_opposition_and_listing_do_not_get_full_credit(self):
        unsafe = [
            "PLC counter의 최대 frequency 제한이 없으므로 고려할 필요가 없다.",
            "해상도를 높이면 pulse frequency는 증가하지 않는다.",
            "PPR은 무조건 좋고 maximum frequency는 고려할 필요가 없다.",
            "Encoder, N_eff, maximum frequency, PLC counter를 목록으로 열거한다.",
            '일부는 "Encoder와 PLC 최대 주파수를 확인해 이내로 선정한다. '
            'PPR을 높이면 pulse frequency가 증가한다"라고 주장한다.',
            "만약 센서의 최대 주파수 제한이 없다면 PPR을 높여도 상관없다.",
        ]
        for answer in unsafe:
            with self.subTest(answer=answer):
                self.assertNotEqual(anchor_row(answer)["status"], "SATISFIED")

    def test_qualified_scope_only(self):
        # The targeted relation must not appear when the question contract
        # does not require it, or under an unrelated Topic.
        other_question = (
            "Incremental encoder에서 A/B quadrature와 Z channel을 설명하시오."
        )
        result = evaluate_fact_anchor_requirements(
            answer_text=CASES["canonical"], topic_ids=[TOPIC],
            question_text=other_question,
        )
        matches = [row for row in result["requirements"]
                   if row["requirement_id"] == ANCHOR]
        if matches:
            self.assertEqual(
                matches[0]["evidence_mode"], "bounded_encoder_frequency_relation",
            )
        unrelated = evaluate_fact_anchor_requirements(
            answer_text=CASES["canonical"],
            topic_ids=["industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience"],
            question_text=QUESTION,
        )
        self.assertFalse(any(row["requirement_id"] == ANCHOR
                             for row in unrelated["requirements"]))


if __name__ == "__main__":
    unittest.main()
