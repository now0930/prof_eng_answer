"""Regression for the thermocouple/RTD comparison question scope."""

import unittest
import json
import tempfile
from unittest.mock import patch

from grading.routing.deterministic_topic_router import route_question_topics
from grading.evidence.fact_anchor_evidence_adapter import evaluate_fact_anchor_requirements
from grading.evidence.cross_topic_question_contract import load_contracts, select_contract
from grading.scoring.deterministic_primary_grader import grade_deterministically
from grading_agents import run_agent_pipeline


QUESTION = (
    "열전대, 측온 저항체(원문: 축은 저항체) 측정원리, 특성 비교\n"
    "측정 정확도에 영향을 미치는 요인, 개선 방안"
)
EXPECTED_TOPICS = {
    "rtd_temperature_sensor_principle_pt100_wiring_compensation",
    "thermocouple_temperature_sensor_seebeck_reference_junction_compensation",
}


class TemperatureComparisonScopeTest(unittest.TestCase):
    def test_question_routes_only_to_both_temperature_sensors(self):
        route = route_question_topics(QUESTION)
        self.assertEqual(set(route["topic_ids"]), EXPECTED_TOPICS)
        self.assertNotIn("second_order_lag_response_by_damping_ratio", route["topic_ids"])

    def test_unrelated_topic_cannot_create_missing_scope(self):
        route = route_question_topics(QUESTION)
        result = evaluate_fact_anchor_requirements(
            question_text=QUESTION,
            answer_text="",
            topic_ids=route["topic_ids"],
        )
        self.assertEqual(
            {row["owner_topic_id"] for row in result["question_contract_selections"]},
            EXPECTED_TOPICS,
        )
        required = {row["requirement_id"] for row in result["requirements"]}
        self.assertNotIn("__question_scope__", required)

    def test_cross_topic_contract_has_four_axes_and_valid_fact_sources(self):
        contracts = load_contracts()
        contract = select_contract(QUESTION, route_question_topics(QUESTION)["topic_ids"])
        self.assertIn(contract, contracts)
        self.assertEqual(
            {row["demand_axis"] for row in contract["requirements"]},
            {"measurement_principle", "characteristics_comparison", "accuracy_factors", "improvement_methods"},
        )
        self.assertIsNone(select_contract("열전대의 원리만 설명하시오", route_question_topics(QUESTION)["topic_ids"]))

    def test_deterministic_relations_beat_keyword_only_partial(self):
        answer = (
            "열전대는 제벡 효과로 측정접점과 기준점의 온도 차이에 따라 전압이 발생한다.\n"
            "RTD는 온도에 따라 저항이 변한다.\n"
            "열전대는 견고하고 넓은 범위에 쓰이며 RTD는 열전대 대비 정확하다.\n"
            "RTD는 wire의 저항이 온도 측정에 오차를 만든다.\n"
            "RTD 자기 발열은 측정전류를 낮춰 줄인다.\n"
        )
        grade = grade_deterministically(question_text=QUESTION, answer_text=answer)
        requirements = {row["requirement_id"]: row for row in grade["requirements"]}
        self.assertEqual(grade["topic_ids"], list(route_question_topics(QUESTION)["topic_ids"]))
        self.assertTrue(grade["question_scope_evaluation"]["exact"])
        self.assertEqual(requirements["tc_seebeck_temperature_difference"]["status"], "SATISFIED")
        self.assertEqual(requirements["rtd_resistance_temperature_relation"]["status"], "SATISFIED")
        self.assertEqual(grade["provider_calls"], 0)

    def test_keyword_list_cannot_pass_as_engineering_relations(self):
        grade = grade_deterministically(
            question_text=QUESTION,
            answer_text="열전대 RTD 제벡 저항 냉접점 3선 4선 정확도 개선",
        )
        self.assertEqual(grade["requirement_summary"]["SATISFIED"], 0)
        self.assertLess(grade["total_score"], 15.0)

    def test_explicit_wrong_wire_claim_cannot_be_overridden_by_llm(self):
        answer = "열전대는 저항 성질이 비슷한 금속을 wire로 사용한다."
        calls = []

        def fake_llm(prompt):
            calls.append(prompt)
            return json.dumps({"judgments": [{
                "requirement_id": "tc_extension_wire_thermoelectric_match",
                "status": "SATISFIED", "quote": answer,
            }]})

        grade = grade_deterministically(
            question_text=QUESTION, answer_text=answer, llm_evidence_fn=fake_llm,
        )
        row = next(row for row in grade["requirements"] if row["requirement_id"] == "tc_extension_wire_thermoelectric_match")
        self.assertEqual(row["status"], "WRONG")
        self.assertEqual(grade["llm_verdict_authority"], 0)

    def test_rejected_wrong_wire_claim_is_not_counted_as_adopted(self):
        grade = grade_deterministically(
            question_text=QUESTION,
            answer_text="열전대는 저항 성질이 비슷한 금속을 wire로 사용한다는 설명은 잘못이다.",
        )
        row = next(row for row in grade["requirements"] if row["requirement_id"] == "tc_extension_wire_thermoelectric_match")
        self.assertNotEqual(row["status"], "WRONG")

    def test_llm_quote_can_be_suggested_but_never_changes_abc(self):
        answer = "열전대는 제벡 효과로 온도차를 잰다."

        def fake_llm(prompt):
            request = json.loads(prompt)
            self.assertNotIn("score", request["output_schema"])
            self.assertNotIn("answer", request)
            self.assertTrue(all("answer_excerpts" in row for row in request["requirements"]))
            return json.dumps({"judgments": [
                {"requirement_id": "tc_seebeck_temperature_difference", "status": "SATISFIED", "quote": answer},
                {"requirement_id": "rtd_resistance_temperature_relation", "status": "SATISFIED", "quote": answer},
                {"requirement_id": "tc_range_ruggedness_characteristic", "status": "SATISFIED", "quote": "답안에 없는 문장"},
            ]})

        grade = grade_deterministically(
            question_text=QUESTION, answer_text=answer, llm_evidence_fn=fake_llm,
        )
        rows = {row["requirement_id"]: row for row in grade["requirements"]}
        self.assertEqual(rows["tc_seebeck_temperature_difference"]["status"], "PARTIAL")
        self.assertEqual(rows["rtd_resistance_temperature_relation"]["status"], "MISSING")
        self.assertEqual(rows["tc_range_ruggedness_characteristic"]["status"], "MISSING")
        self.assertEqual(grade["provider_calls"], 1)
        self.assertEqual(grade["cross_topic_evidence"]["llm_evidence_audit"]["accepted_count"], 1)
        self.assertEqual(grade["cross_topic_evidence"]["llm_evidence_suggestions"][0]["score_effect"], "none")
        baseline = grade_deterministically(question_text=QUESTION, answer_text=answer)
        self.assertEqual(grade["total_score"], baseline["total_score"])
        self.assertEqual(grade["deterministic_score"]["score_breakdown"],
                         baseline["deterministic_score"]["score_breakdown"])

    def test_llm_failure_preserves_deterministic_grade(self):
        answer = "열전대는 제벡 효과로 온도차를 잰다."
        baseline = grade_deterministically(question_text=QUESTION, answer_text=answer)

        def unavailable(_prompt):
            raise ConnectionError("provider unavailable")

        assisted = grade_deterministically(
            question_text=QUESTION, answer_text=answer, llm_evidence_fn=unavailable,
        )
        self.assertEqual(assisted["total_score"], baseline["total_score"])
        self.assertEqual(assisted["requirement_summary"], baseline["requirement_summary"])
        self.assertEqual(assisted["cross_topic_evidence"]["llm_evidence_audit"]["error_type"], "ConnectionError")

    def test_malformed_llm_output_preserves_deterministic_grade(self):
        answer = "열전대는 제벡 효과로 온도차를 잰다."
        baseline = grade_deterministically(question_text=QUESTION, answer_text=answer)
        assisted = grade_deterministically(
            question_text=QUESTION, answer_text=answer,
            llm_evidence_fn=lambda _prompt: "not-json",
        )
        self.assertEqual(assisted["total_score"], baseline["total_score"])
        self.assertEqual(assisted["cross_topic_evidence"]["llm_evidence_audit"]["error_type"], "JSONDecodeError")

    def test_production_entrypoint_wires_optional_evidence_resolver(self):
        answer = "열전대는 제벡 효과로 온도차를 잰다."
        calls = []

        def fake_llm(prompt):
            calls.append(prompt)
            return json.dumps({"judgments": [{
                "requirement_id": "tc_seebeck_temperature_difference",
                "status": "SATISFIED", "quote": answer,
            }]})

        with tempfile.TemporaryDirectory() as directory, patch(
            "grading.scoring.grading_authority_policy.enforce_requested_authority_mode",
            return_value={"DETERMINISTIC_GRADING_PRIMARY": True},
        ):
            _, grade = run_agent_pipeline(
                call_ollama_fn=fake_llm,
                raw_text=f"[문제] {QUESTION}\n[답안]\n{answer}",
                rubric={}, sid="synthetic-temperature-comparison",
                image_count=0, session_dir=directory,
            )
        self.assertEqual(len(calls), 1)
        self.assertEqual(grade["provider_calls"], 1)
        self.assertEqual(grade["llm_verdict_authority"], 0)
        self.assertEqual(grade["cross_topic_evidence"]["llm_evidence_audit"]["accepted_count"], 1)
        self.assertEqual(grade["requirement_summary"]["SATISFIED"], 0)

    def test_provider_free_regrade_handles_partial_contract_without_llm(self):
        answer = "열전대는 제벡 효과로 온도차를 잰다."
        with tempfile.TemporaryDirectory() as directory, patch(
            "grading.scoring.grading_authority_policy.enforce_requested_authority_mode",
            return_value={"DETERMINISTIC_GRADING_PRIMARY": True},
        ):
            _, grade = run_agent_pipeline(
                call_ollama_fn=None,
                raw_text=f"[문제] {QUESTION}\n[답안]\n{answer}",
                rubric={}, sid="provider-free-temperature-regrade",
                image_count=0, session_dir=directory,
            )
        self.assertEqual(grade["provider_calls"], 0)
        self.assertEqual(grade["cross_topic_evidence"]["llm_evidence_audit"]["attempted"], False)
        self.assertGreater(grade["requirement_summary"]["PARTIAL"], 0)


if __name__ == "__main__":
    unittest.main()
