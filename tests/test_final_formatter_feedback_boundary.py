from __future__ import annotations

from copy import deepcopy
import ast
import inspect
import unittest

import grading_agents as ga
from grade_output_summarizer import (
    _build_payload,
    _normalise_summary,
    _render,
)


PUBLIC_KEYS = (
    "summary",
    "rater_summary",
    "strengths",
    "weaknesses",
    "rewrite_advice",
    "improvement_points",
    "next_practice_focus",
)

FORBIDDEN_AUTO_POLICY = (
    "비용, 시간, 적용 가능성, 기존 설비 영향",
    "비용·유지보수·기존 설비",
    "현장 적용·설계 판단·제언 순서로",
    "현장 적용성, 제언, 기술사적 판단 제시",
    "Cost-Benefit",
)


def public_text(obj: dict) -> str:
    rows = []

    for key in PUBLIC_KEYS:
        value = obj.get(key)

        if isinstance(value, list):
            rows.extend(str(item) for item in value)
        elif value is not None:
            rows.append(str(value))

    return "\n".join(rows)


class FinalFormatterFeedbackBoundaryTest(unittest.TestCase):
    def test_phase14_does_not_semantically_rewrite_generic_policy(self) -> None:
        source = {
            "rewrite_advice": [
                (
                    "대책은 비용, 시간, 적용 가능성, 기존 설비 영향, "
                    "운전 리스크까지 연결하세요."
                )
            ],
            "summary": "기존 요약",
        }

        actual = ga._phase14_compact_feedback_output(
            deepcopy(source)
        )

        self.assertEqual(
            actual["rewrite_advice"],
            source["rewrite_advice"],
        )

    def test_phase16_phase17_do_not_invent_field_cost_policy(self) -> None:
        grade = {
            "summary": "핵심 원리와 변수 관계를 설명했습니다.",
            "rater_summary": (
                "내부 채점 관점은 사용자 요구와 분리합니다."
            ),
            "strengths": ["핵심 식을 제시했습니다."],
            "weaknesses": ["변수 의미 설명이 부족합니다."],
            "rewrite_advice": [
                "원리와 결과 해석의 연결을 보완하세요."
            ],
            "improvement_points": [
                "명시 요구의 누락 항목을 보완하세요."
            ],
            "next_practice_focus": [
                "문제 요구 해석·완전성"
            ],
        }

        before = public_text(grade)
        self.assertFalse(
            any(token in before for token in FORBIDDEN_AUTO_POLICY)
        )

        after16 = ga._phase16_polish_final_output(
            deepcopy(grade)
        )
        after17 = ga._phase17_final_phrase_cleanup(
            deepcopy(after16)
        )
        text = public_text(after17)

        for token in FORBIDDEN_AUTO_POLICY:
            self.assertNotIn(token, text)

    def test_final_question_demand_projection_runs_after_polish_and_difficulty(self) -> None:
        source = inspect.getsource(
            ga._phase2_postprocess_grade
        )
        tree = ast.parse(source)
        fn = tree.body[0]

        calls = []

        for node in ast.walk(fn):
            if not isinstance(node, ast.Call):
                continue

            func = node.func

            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            else:
                continue

            calls.append((node.lineno, name))

        phase9 = [
            line
            for line, name in calls
            if name == "_phase9_apply_type_aware_de_feedback_policy"
        ]
        phase16 = max(
            line
            for line, name in calls
            if name == "_phase16_polish_final_output"
        )
        phase17 = max(
            line
            for line, name in calls
            if name == "_phase17_final_phrase_cleanup"
        )
        difficulty = max(
            line
            for line, name in calls
            if name == "attach_difficulty_strategy_to_grade"
        )
        ceiling = max(
            line
            for line, name in calls
            if name == "apply_difficulty_score_ceiling"
        )

        self.assertGreaterEqual(len(phase9), 3)
        self.assertGreater(
            phase9[-1],
            max(phase16, phase17, difficulty, ceiling),
        )

    def test_compact_summarizer_does_not_invent_unasked_policy(self) -> None:
        grade = {
            "total_score": 17.0,
            "max_score": 25.0,
            "score_range": "17~17",
            "confidence": "high",
            "official_pass_score": 15.0,
            "practical_target_score": 17.5,
            "high_score_target": 20.0,
            "summary": "원리와 변수 관계를 중심으로 평가했습니다.",
            "strengths": ["핵심 식을 제시했습니다."],
            "weaknesses": ["변수 의미 설명이 부족합니다."],
            "rewrite_advice": [
                "원리→수식→결과 해석을 연결하세요."
            ],
            "next_practice_focus": [
                "원리·수식·변수 의미·결과 해석의 연결"
            ],
            "question_type_evaluation": {
                "primary_type": {
                    "id": "PRINCIPLE_INTERPRETATION",
                }
            },
        }

        payload = _build_payload(deepcopy(grade))
        summary = _normalise_summary(None, payload)
        rendered = _render(summary, payload)

        for token in FORBIDDEN_AUTO_POLICY:
            self.assertNotIn(token, rendered)

    def test_formatter_sources_are_not_feedback_policy_owners(self) -> None:
        import bot
        import grade_output_summarizer as gos

        functions = (
            ga._phase16_polish_final_output,
            ga._phase17_final_phrase_cleanup,
            gos._render,
            bot.format_result,
        )

        forbidden_literal_fragments = (
            "모든 문제 유형에서",
            "비용, 시간, 적용 가능성, 기존 설비 영향",
            "FIELD_APPLICATION 보완:",
            "FIELD_APPLICATION 고득점 조건:",
        )

        for function in functions:
            source = inspect.getsource(function)

            for token in forbidden_literal_fragments:
                with self.subTest(
                    function=function.__name__,
                    token=token,
                ):
                    self.assertNotIn(token, source)


# STAGE18B3_STRUCTURED_DEFECT_OUTPUT_PRIORITY_V1
class StructuredDefectFinalFormatterPriorityTest(
    unittest.TestCase
):
    @staticmethod
    def _grade() -> dict:
        return {
            "total_score": 18.0,
            "max_score": 25.0,
            "official_pass_score": 15.0,
            "practical_target_score": 17.5,
            "high_score_target": 20.0,
            "summary": (
                "기술적 개념의 정확성이 우수합니다."
            ),
            "rewrite_advice": [
                (
                    "대책은 비용, 시간, 적용 가능성, "
                    "기존 설비 영향을 검토하세요."
                )
            ],
            "general_evidence_contract": {
                "defects": [
                    {
                        "defect_id": "DEFECT-1",
                        "defect_type": (
                            "correctness_error"
                        ),
                        "severity": "major",
                        "owner_layer": "C",
                        "explanation": (
                            "압력과 유량 관계의 부호가 "
                            "반대로 기술되었습니다."
                        ),
                    }
                ],
            },
            "verified_defect_reconciliation": {
                "marker": (
                    "VERIFIED_DEFECT_RECONCILIATION_V1"
                ),
                "score_effect": "none",
                "primary_score_owner": "C",
                "b_completeness_double_deduction": (
                    False
                ),
                "applied_defect_ids": [
                    "DEFECT-1"
                ],
                "unresolved_defect_ids": [],
            },
        }

    def test_payload_threads_existing_reconciliation(
        self,
    ) -> None:
        grade = self._grade()
        payload = _build_payload(
            deepcopy(grade)
        )

        self.assertEqual(
            payload[
                "verified_defect_reconciliation"
            ][
                "applied_defect_ids"
            ],
            ["DEFECT-1"],
        )
        priority = payload[
            "structured_defect_output_priority"
        ]
        self.assertEqual(
            priority["source"],
            (
                "existing_verified_defect_"
                "reconciliation"
            ),
        )
        self.assertFalse(
            priority[
                "generic_feedback_can_override"
            ]
        )
        self.assertEqual(
            payload["score"]["total"],
            18.0,
        )

    def test_verified_defect_precedes_generic_feedback(
        self,
    ) -> None:
        grade = self._grade()
        payload = _build_payload(
            deepcopy(grade)
        )
        llm_summary = {
            "headline": "우수",
            "overall": (
                "기술적 개념의 정확성이 우수합니다."
            ),
            "key_reasons": [
                "비용과 적용 가능성을 검토했습니다."
            ],
            "improvements": [
                (
                    "비용, 시간, 적용 가능성, "
                    "기존 설비 영향을 검토하세요."
                )
            ],
        }
        summary = _normalise_summary(
            llm_summary,
            payload,
        )

        self.assertEqual(
            summary["headline"],
            "검증된 핵심 기술 오류 보완 필요",
        )
        self.assertEqual(
            summary["key_reasons"][0],
            (
                "압력과 유량 관계의 부호가 "
                "반대로 기술되었습니다."
            ),
        )
        self.assertTrue(
            summary["improvements"][0].startswith(
                "검증된 기술 오류:"
            )
        )
        self.assertNotIn(
            "비용, 시간, 적용 가능성",
            "\n".join(
                summary["improvements"]
            ),
        )
        self.assertEqual(
            summary[
                "structured_defect_output_priority"
            ][
                "verified_correctness_count"
            ],
            1,
        )

    def test_direct_render_rechecks_structured_priority(
        self,
    ) -> None:
        payload = _build_payload(
            deepcopy(self._grade())
        )
        rendered = _render(
            {
                "headline": "우수",
                "overall": (
                    "기술적 개념의 정확성이 우수합니다."
                ),
                "key_reasons": [
                    "비용 검토가 충분합니다."
                ],
                "improvements": [
                    "비용·유지보수 검토"
                ],
            },
            payload,
        )

        self.assertIn(
            "판정: 검증된 핵심 기술 오류 보완 필요",
            rendered,
        )
        self.assertIn(
            (
                "압력과 유량 관계의 부호가 "
                "반대로 기술되었습니다."
            ),
            rendered,
        )
        self.assertNotIn(
            "비용·유지보수 검토",
            rendered,
        )


if __name__ == "__main__":
    unittest.main(verbosity=0)
