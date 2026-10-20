"""Synthetic, non-private D/E shadow contract tests.

These tests verify gates, not LLM accuracy or expert agreement.
"""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from grading.qualitative.de_shadow import evaluate_qualitative_de
from grading.qualitative.repeatability import measure_repeated_shadow
from grading.qualitative.shadow_input import project_deterministic_shadow_input
from grading.qualitative.shadow_storage import project_learning_diagnosis, save_private_shadow


TOPIC = "rtd_temperature_sensor_principle_pt100_wiring_compensation"
QUESTION = "RTD와 열전대의 선택 조건을 설명하시오."
ANSWER = (
    "고온 범위에서는 열전대를 선택한다.\n"
    "열전대는 고온에 견디므로 이 조건에 적합하다.\n"
    "정밀도가 중요하면 RTD가 대안이지만 측정 범위는 좁다.\n"
    "RTD의 리드선 저항은 측정 오차를 만든다.\n"
    "4선식은 별도 전압 측정선으로 리드선 오차를 줄인다."
)


def spans(answer=ANSWER):
    lines = answer.splitlines()
    return [(answer.index(line), answer.index(line) + len(line), line) for line in lines]


def baseline(answer=ANSWER, *, wrong_index=None):
    rows = []
    for index, (start, end, line) in enumerate(spans(answer)):
        rows.append({"requirement_id": f"r{index}", "owner_topic_id": TOPIC,
                     "status": "WRONG" if index == wrong_index else "SATISFIED",
                     "source_span": {"start": start, "end": end}, "evidence_text": line})
    return {"score_breakdown": {"A_structure": 3.0, "B_requirement_completeness": 5.0,
                                "C_fact_correctness": 6.0}, "requirements": rows}


def proposal(answer=ANSWER, *, scores=None):
    points = scores or {"D1": 2, "D2": 2, "D3": 2, "E1": 1, "E2": 1}
    criteria = []
    for index, key in enumerate(("D1", "D2", "D3", "E1", "E2")):
        start, end, line = spans(answer)[index]
        score = points[key]
        criteria.append({"criterion_id": key, "score": score, "reason": f"{key} 근거",
                         "topic_id": TOPIC, "quote": line if score else None,
                         "start": start if score else None, "end": end if score else None})
    start, end, line = spans(answer)[4]
    return {"criteria": criteria, "interview_questions": [{
        "question_id": "interview_rtd_lead_error_1",
        "question": "4선식은 3선식과 어떻게 다른가?", "topic_id": TOPIC,
        "reason": "리드선 오차에 대한 설명 확장", "expected_elements": ["전류선", "전압선"],
        "quote": line, "start": start, "end": end,
    }], "abc_observations": []}


def run(response, *, answer=ANSWER, abc=None):
    return evaluate_qualitative_de(
        QUESTION, answer, abc or baseline(answer), {"topic_ids": [TOPIC]},
        llm_call=lambda _: json.dumps(response, ensure_ascii=False),
    )


class QualitativeDEShadowTests(unittest.TestCase):
    def test_valid_proposal_is_score_neutral_and_has_learning_questions(self):
        result = run(proposal())
        self.assertEqual(result["status"], "SHADOW_VALIDATED")
        self.assertEqual((result["proposed_d"], result["proposed_e"]), (6, 2))
        self.assertEqual(result["score_effect"], "none")
        self.assertNotIn("total_score", result)
        self.assertFalse(result["semantic_truth_verified"])
        projected = project_learning_diagnosis(result)
        self.assertEqual(projected["training_candidates"][0]["review_status"], "candidate")
        self.assertEqual(len(projected["diagnosis_candidates"]), 5)

    def test_abc_input_is_immutable_and_llm_cannot_set_total(self):
        abc = baseline()
        original = copy.deepcopy(abc)
        malicious = proposal()
        malicious["total_score"] = 25
        result = run(malicious, abc=abc)
        self.assertEqual(result["status"], "UNEVALUATED")
        self.assertEqual(result["reason_code"], "invalid_or_unauthorized_response_fields")
        self.assertEqual(abc, original)

    def test_wrong_technical_claim_cannot_earn_d_or_interview_credit(self):
        result = run(proposal(), abc=baseline(wrong_index=0))
        self.assertEqual(result["reason_code"], "wrong_claim_used_for_positive_credit")
        bad_question = proposal()
        bad_question["interview_questions"][0].update(dict(zip(
            ("start", "end", "quote"), spans()[4],
        )))
        self.assertEqual(run(bad_question, abc=baseline(wrong_index=4))["reason_code"],
                         "wrong_claim_used_for_positive_credit")

    def test_generic_conclusion_without_fact_span_cannot_earn_credit(self):
        generic = ANSWER + "\n상황에 맞게 최선을 선택한다."
        candidate = proposal()
        start, end, line = spans(generic)[5]
        candidate["criteria"][0].update({"start": start, "end": end, "quote": line})
        # A line with no approved technical evidence is not a D/E credit source.
        fact_rows = baseline(generic)
        fact_rows["requirements"].pop()
        self.assertEqual(run(candidate, answer=generic, abc=fact_rows)["reason_code"],
                         "positive_evidence_not_bound_to_verified_fact")

    def test_conclusion_removal_and_technical_paraphrase_keep_literal_gate_stable(self):
        # The synthetic baseline has no conclusion; adding/removing a generic
        # conclusion does not create new supported technical spans.
        original = run(proposal())
        paraphrased = ANSWER.replace(
            "4선식은 별도 전압 측정선으로 리드선 오차를 줄인다.",
            "4도체 Kelvin 접속은 전압선과 전류선을 분리해 리드선 오차를 낮춘다.",
        )
        revised = run(proposal(paraphrased), answer=paraphrased)
        self.assertEqual(original["status"], "SHADOW_VALIDATED")
        self.assertEqual(revised["status"], "SHADOW_VALIDATED")
        self.assertEqual((original["proposed_d"], original["proposed_e"]),
                         (revised["proposed_d"], revised["proposed_e"]))

    def test_duplicate_positive_quote_and_fabricated_quote_are_rejected(self):
        duplicate = proposal()
        duplicate["criteria"][1].update({key: duplicate["criteria"][0][key]
                                           for key in ("start", "end", "quote")})
        self.assertEqual(run(duplicate)["reason_code"], "duplicate_positive_evidence")
        fabricated = proposal()
        fabricated["criteria"][0]["quote"] = "답안에 없는 전문적인 주장이다"
        self.assertEqual(run(fabricated)["reason_code"], "quote_span_mismatch")

    def test_unique_literal_quote_repairs_bad_model_index_only(self):
        candidate = proposal()
        candidate["criteria"][0]["start"] = 1
        candidate["criteria"][0]["end"] += 1
        result = run(candidate)
        self.assertEqual(result["status"], "SHADOW_VALIDATED")
        self.assertEqual(result["span_corrections"], 1)
        self.assertEqual(result["criteria"][0]["start"], spans()[0][0])
        self.assertEqual(result["criteria"][0]["end"], spans()[0][1])

    def test_provider_failure_and_missing_provider_are_unevaluated_not_zero(self):
        missing = evaluate_qualitative_de(QUESTION, ANSWER, baseline(), {"topic_ids": [TOPIC]})
        self.assertEqual(missing["status"], "UNEVALUATED")
        self.assertNotIn("proposed_d", missing)
        self.assertEqual(project_learning_diagnosis(missing)["training_candidates"], [])
        failure = evaluate_qualitative_de(QUESTION, ANSWER, baseline(), {"topic_ids": [TOPIC]},
                                          llm_call=lambda _: (_ for _ in ()).throw(ConnectionError("private text")))
        self.assertEqual(failure["reason_code"], "ConnectionError")
        self.assertNotIn("private text", json.dumps(failure))

    def test_response_scope_range_and_schema_are_bounded(self):
        over = proposal()
        over["criteria"][0]["score"] = 3
        self.assertEqual(run(over)["reason_code"], "criterion_score_out_of_range")
        wrong_topic = proposal()
        wrong_topic["criteria"][0]["topic_id"] = "unrelated_second_order_topic"
        self.assertEqual(run(wrong_topic)["reason_code"], "invalid_criterion_scope_or_reason")
        extra = proposal()
        extra["interview_questions"] = extra["interview_questions"] * 4
        self.assertEqual(run(extra)["reason_code"], "invalid_response_schema")

    def test_unverified_fact_context_is_never_sent_to_model(self):
        calls = []
        result = evaluate_qualitative_de(
            QUESTION, ANSWER, baseline(),
            {"topic_ids": [TOPIC], "verified_facts": [{
                "topic_id": TOPIC, "text": "unreviewed claim", "verification_status": "candidate",
            }]}, llm_call=lambda prompt: calls.append(prompt) or json.dumps(proposal()),
        )
        self.assertEqual(result["status"], "UNEVALUATED")
        self.assertEqual(result["reason_code"], "unverified_topic_fact_context")
        self.assertEqual(calls, [])

    def test_interview_question_requires_e1_evidence(self):
        candidate = proposal()
        candidate["criteria"][3].update({"score": 0, "quote": None, "start": None, "end": None})
        self.assertEqual(run(candidate)["reason_code"], "interview_score_question_inconsistent")

    def test_e1_positive_without_question_is_unevaluated(self):
        candidate = proposal()
        candidate["interview_questions"] = []
        self.assertEqual(run(candidate)["reason_code"], "interview_score_question_inconsistent")

    def test_repeatability_is_redacted_and_not_expert_truth(self):
        calls = []
        def provider(prompt):
            calls.append(prompt)
            candidate = proposal()
            candidate["criteria"][0]["score"] = 2 if len(calls) % 2 else 1
            return json.dumps(candidate, ensure_ascii=False)

        report = measure_repeated_shadow(
            QUESTION, ANSWER, baseline(), {"topic_ids": [TOPIC]}, provider,
            {"provider": "test", "model_id": "fixed", "temperature": 0,
             "prompt_version": "v1"}, runs=3,
        )
        self.assertEqual(report["validated_runs"], 3)
        self.assertEqual(report["request_hash_distinct"], 1)
        self.assertEqual(report["criterion_dispersion"]["D1"]["min"], 1)
        self.assertEqual(report["criterion_dispersion"]["D1"]["max"], 2)
        self.assertEqual(report["acceptance_status"], "REVIEW_REQUIRED")
        self.assertNotIn(ANSWER, json.dumps(report, ensure_ascii=False))
        self.assertNotIn("total_score", report)

    def test_repeatability_missing_provider_is_incomplete_not_zero(self):
        report = measure_repeated_shadow(
            QUESTION, ANSWER, baseline(), {"topic_ids": [TOPIC]}, None, {}, runs=2,
        )
        self.assertEqual(report["measurement_status"], "INCOMPLETE")
        self.assertEqual(report["validated_runs"], 0)
        self.assertIsNone(report["criterion_dispersion"]["D1"])
        self.assertEqual(report["provider_calls"], 0)

    def test_shadow_input_uses_requirement_owners_not_router_candidates(self):
        from grading.scoring.deterministic_primary_grader import grade_deterministically
        question = "열전대와 RTD의 원리, 특성 비교, 정확도 요인과 개선 방안을 설명하시오."
        answer = "열전대는 제벡 효과로 온도차를 잰다. RTD는 저항 변화로 온도를 잰다."
        grade = grade_deterministically(question_text=question, answer_text=answer)
        abc, context = project_deterministic_shadow_input(grade)
        self.assertEqual(set(context["topic_ids"]), {
            row["owner_topic_id"] for row in grade["requirements"]
        })
        self.assertNotIn("second_order_lag_response_by_damping_ratio", context["topic_ids"])
        self.assertEqual(abc["score_breakdown"]["A_structure"],
                         grade["deterministic_score"]["score_breakdown"]["A_structure"])
        self.assertNotIn("total_score", abc)

    def test_private_storage_is_exclusive_and_permissioned(self):
        result = run(proposal())
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "shadow.json"
            save_private_shadow(target, result)
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError):
                save_private_shadow(target, result)


if __name__ == "__main__":
    unittest.main()
