#!/usr/bin/env python3
from __future__ import annotations

import unittest

from grade_output_summarizer import _build_payload, _render


def render_without_llm(grade: dict) -> str:
    payload = _build_payload(grade)
    summary = {
        "headline": "테스트 판정",
        "overall": payload.get("summary") or "테스트 총평",
        "key_reasons": ["핵심 근거"],
        "section_basis": ["A/B/C/D/E 기준 확인"],
        "improvements": ["개선점"],
    }
    return _render(summary, payload)


class GradeOutputFormatterRegressionTest(unittest.TestCase):
    def test_basic_score_header_is_rendered(self) -> None:
        text = render_without_llm(
            {
                "total_score": 16.0,
                "max_score": 25,
                "score_range": "15~17",
                "confidence": "high",
                "official_pass_score": 15,
                "practical_target_score": 17.5,
                "summary": "기본 개념은 충족했으나 현장 판단이 부족합니다.",
            }
        )

        self.assertIn("채점 완료: 16.0/25", text)
        self.assertIn("예상 점수대: 15~17", text)
        self.assertIn("신뢰도: high", text)
        self.assertIn("공식 합격선: 15점 (달성)", text)
        self.assertIn("실전 목표선: 17.5점 (미달)", text)
        self.assertIn("총평: 기본 개념은 충족했으나 현장 판단이 부족합니다.", text)

    def test_fatal_logic_check_forces_cap_score_range(self) -> None:
        text = render_without_llm(
            {
                "total_score": 10.0,
                "max_score": 25,
                "confidence": "high",
                "summary": "치명 오류로 고득점이 제한됩니다.",
                "logic_check_evaluation": {
                    "fatal_error_detected": True,
                    "mode": "topic_specific",
                    "findings": [
                        {
                            "severity": "fatal",
                            "message": "극점 부호 오류",
                            "evidence": "s = +ζωn ± jωd",
                            "correct_rule": "안정 2차계 극점의 실수부는 -ζωn이다.",
                        }
                    ],
                },
            }
        )

        self.assertIn("채점 완료: 10.0/25", text)
        self.assertIn("예상 점수대: 10.0점 cap 적용", text)
        self.assertIn("총평: 치명 오류로 고득점이 제한됩니다.", text)


if __name__ == "__main__":
    unittest.main()
