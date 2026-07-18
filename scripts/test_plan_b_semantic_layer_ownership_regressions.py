from __future__ import annotations

# PLAN_B_TEST_REPO_BOOTSTRAP_V1
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import unittest

import gemini_grader
import grading_agents
import originality_grader


def _layers(c_score=1.0, d_score=1.0):
    return [
        {"layer_id": "A", "score": 1.0, "max": 3.0, "reason": "A base"},
        {"layer_id": "B", "score": 3.0, "max": 6.0, "reason": "B base"},
        {"layer_id": "C", "score": c_score, "max": 8.0, "reason": "C base"},
        {"layer_id": "D", "score": d_score, "max": 6.0, "reason": "D base"},
        {"layer_id": "E", "score": 0.5, "max": 2.0, "reason": "E base"},
    ]


def _parsed(technical_error_risk=False, gate=None):
    value = {
        "overall_comment": "C Fact가 부족하나 현장 판단은 존재함.",
        "anchors": [
            {"id": "O1", "name": "문제 재해석 능력", "level": 0.5, "reason": "현장 문제로 확장함.", "evidence": ["운전 조건을 구분함"]},
            {"id": "O2", "name": "현장 조건 반영", "level": 0.7, "reason": "조건을 반영함.", "evidence": ["최소·최대 운전 조건"]},
            {"id": "O3", "name": "대안 비교와 trade-off", "level": 0.7, "reason": "비용과 안전을 비교함.", "evidence": ["비용보다 안전 우선"]},
            {"id": "O4", "name": "적용 우선순위 제시", "level": 0.5, "reason": "단계 적용을 제시함.", "evidence": ["진단 후 부분 변경"]},
            {"id": "O5", "name": "검증 가능성", "level": 0.6, "reason": "검증 지표를 제시함.", "evidence": ["추세와 동작시간 확인"]},
        ],
        "average_level": 0.6,
        "raw_originality_score": 1.2,
        "technical_error_risk": technical_error_risk,
    }
    if gate is not None:
        value["technical_error_gate"] = gate
    return value


class PlanBGeneralLayerOwnershipTest(unittest.TestCase):
    def test_semantic_prompt_contract_is_general(self):
        original = gemini_grader._PLAN_B_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_V1
        try:
            gemini_grader._PLAN_B_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_V1 = lambda *args, **kwargs: "BASE"
            prompt = gemini_grader.build_gemini_grading_prompt(question_text="PID 튜닝 절차를 설명하시오.", answer_text="답안")
        finally:
            gemini_grader._PLAN_B_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_V1 = original
        self.assertIn("[PLAN_B_GENERAL_LAYER_OWNERSHIP_V1]", prompt)
        self.assertIn("B는 문제문이 명시적으로 요구한 항목", prompt)
        self.assertIn("C는 기술 Fact, 공식, 부호와 방향", prompt)
        self.assertIn("D는 실제 선정·설계·운전 판단", prompt)
        self.assertIn("E는 배경→요구→Fact→판단→결론", prompt)
        self.assertNotIn("control_valve", prompt.lower())

    def test_originality_prompt_is_not_second_c_or_d(self):
        original = originality_grader._PLAN_B_ORIGINAL_BUILD_ORIGINALITY_PROMPT_V1
        try:
            originality_grader._PLAN_B_ORIGINAL_BUILD_ORIGINALITY_PROMPT_V1 = lambda *args, **kwargs: "BASE"
            prompt = originality_grader.build_originality_prompt(question_text="두 센서를 비교하고 현장 선정 기준을 제시하시오.", answer_text="답안")
        finally:
            originality_grader._PLAN_B_ORIGINAL_BUILD_ORIGINALITY_PROMPT_V1 = original
        self.assertIn("[PLAN_B_ORIGINALITY_OWNERSHIP_V1]", prompt)
        self.assertIn("C가 낮다는 사실만으로", prompt)
        self.assertIn('"technical_error_gate"', prompt)
        self.assertNotIn("control_valve", prompt.lower())

    def test_rater_b_comments_only_describe_requirement_response(self):
        for rater_id in ("professor", "professional_engineer", "executive"):
            comment = grading_agents._phase4_rater_layer_comment(rater_id, "B")
            self.assertIn("요구", comment)
            self.assertNotIn("정확성", comment)
            self.assertNotIn("문제점", comment)

    def test_low_c_and_low_d_do_not_blanket_cap_originality(self):
        layers = _layers(c_score=1.0, d_score=1.0)
        evaluation = {"parsed": _parsed()}
        result = grading_agents._phase8_apply_originality_to_layer_scores(layers, evaluation, {"level": "two_page_text"})
        parsed = evaluation["parsed"]
        self.assertEqual(parsed["final_originality_score"], 1.2)
        self.assertFalse(any(cap.get("type") in {"fact_gate", "countermeasure_gate"} for cap in parsed["applied_caps"]))
        d_row = next(row for row in result if row["layer_id"] == "D")
        e_row = next(row for row in result if row["layer_id"] == "E")
        self.assertGreater(d_row["score"], 1.0)
        self.assertGreater(e_row["score"], 0.5)
        self.assertNotIn("C Fact가 부족", d_row["reason"])
        self.assertNotIn("C Fact가 부족", e_row["reason"])
        self.assertIn("현장 조건 반영", d_row["reason"])

    def test_untrusted_technical_risk_is_diagnostic_only(self):
        evaluation = {"parsed": _parsed(technical_error_risk=True)}
        grading_agents._phase8_apply_originality_to_layer_scores(_layers(), evaluation, {"level": "two_page_text"})
        self.assertEqual(evaluation["parsed"]["final_originality_score"], 1.2)
        self.assertFalse(evaluation["parsed"]["technical_error_gate_evaluation"]["applied"])

    def test_trusted_fatal_error_can_block_originality(self):
        evaluation = {"parsed": _parsed(True, {"severity": "fatal", "trust_source": "logic_check", "blocks_originality": True, "reason": "핵심 결론을 반대로 만드는 오류"})}
        grading_agents._phase8_apply_originality_to_layer_scores(_layers(), evaluation, {"level": "two_page_text"})
        self.assertEqual(evaluation["parsed"]["final_originality_score"], 0.0)
        self.assertTrue(evaluation["parsed"]["technical_error_gate_evaluation"]["applied"])
        self.assertEqual(evaluation["parsed"]["applied_caps"][0]["type"], "trusted_technical_error_gate")

    def test_short_answer_gate_is_preserved(self):
        evaluation = {"parsed": _parsed()}
        grading_agents._phase8_apply_originality_to_layer_scores(_layers(), evaluation, {"level": "text_only_short_answer"})
        self.assertEqual(evaluation["parsed"]["final_originality_score"], 0.7)
        self.assertEqual(evaluation["parsed"]["applied_caps"][0]["type"], "short_answer_gate")



# PLAN_B_NEGATIVE_EVIDENCE_BONUS_REASON_REGRESSION_V1
class PlanBNegativeEvidenceBonusReasonRegressionTest(
    unittest.TestCase
):
    def test_negative_anchor_evidence_is_not_used_as_bonus_reason(self):
        parsed = {
            "anchors": [
                {
                    "id": "O1",
                    "name": "문제 재해석 능력",
                    "level": 0.5,
                    "reason": "일부 재해석만 확인됨.",
                    "evidence": [
                        "일반론적으로 나열함",
                    ],
                },
                {
                    "id": "O4",
                    "name": "적용 우선순위 제시",
                    "level": 0.5,
                    "reason": "우선순위가 구체적이지 않음.",
                    "evidence": [
                        "단계적 실행 전략 부재",
                    ],
                },
                {
                    "id": "O5",
                    "name": "검증 가능성",
                    "level": 0.5,
                    "reason": "검증 기준이 부족함.",
                    "evidence": [
                        "기준값이 제시되지 않음",
                    ],
                },
            ],
        }

        summary = (
            grading_agents
            ._phase8_plan_b_positive_anchor_summary(
                parsed
            )
        )

        self.assertEqual(
            summary,
            (
                "구조화된 O1~O5 인정 근거: "
                "문제 재해석 능력 0.50 / "
                "적용 우선순위 제시 0.50 / "
                "검증 가능성 0.50"
            ),
        )
        self.assertNotIn(
            "일반론적으로 나열함",
            summary,
        )
        self.assertNotIn(
            "단계적 실행 전략 부재",
            summary,
        )
        self.assertNotIn(
            "기준값이 제시되지 않음",
            summary,
        )

if __name__ == "__main__":
    unittest.main()
