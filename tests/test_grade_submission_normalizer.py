from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from grade_submission_normalizer import (
    normalize_grade_submission,
    normalize_pipeline_call,
)


class GradeSubmissionNormalizerTest(
    unittest.TestCase
):
    def test_normal_answer_is_preserved(
        self,
    ) -> None:
        source = (
            "문제: PID 제어기의 특성을 "
            "설명하시오.\n"
            "1. 개요\n"
            "비례·적분·미분 동작을 설명한다."
        )
        result = normalize_grade_submission(
            source
        )
        self.assertEqual(
            result["normalized_text"],
            source,
        )
        self.assertFalse(result["changed"])

    def test_nested_grade_uses_last_submission(
        self,
    ) -> None:
        source = (
            "[2026-08-19 오후 2:00] "
            "이 대원: /grade\n"
            "문제: 이전 문제\n"
            "이전 답안\n"
            "[2026-08-19 오후 2:01] "
            "Bot name: 채점기: 안내\n"
            "이 메시지는 제거되어야 한다.\n"
            "[2026-08-19 오후 2:02] "
            "이 대원: /grade\n"
            "문제: 최종 문제\n"
            "최종 답안\n"
            "끝.\n"
            "[2026-08-19 오후 2:03] "
            "Bot name: 채점기: 채점 시작\n"
            "채점 엔진 안내\n"
        )
        result = normalize_grade_submission(
            source
        )
        self.assertEqual(
            result["normalized_text"],
            "문제: 최종 문제\n최종 답안",
        )
        self.assertIn(
            "nested_grade_segments_removed",
            result["events"],
        )
        self.assertNotIn(
            "이전 문제",
            result["normalized_text"],
        )
        self.assertNotIn(
            "채점 엔진",
            result["normalized_text"],
        )

    def test_idempotent(self) -> None:
        source = (
            "[2026-08-19 오후 3:05] "
            "이 대원: /grade\n"
            "문제: V-model을 설명하시오.\n"
            "답안 내용\n"
            "끝.\n"
        )
        first = normalize_grade_submission(
            source
        )
        second = normalize_grade_submission(
            first["normalized_text"]
        )
        self.assertEqual(
            first["normalized_text"],
            second["normalized_text"],
        )

    def test_kwargs_pipeline_call_normalized(
        self,
    ) -> None:
        def target(*args, **kwargs):
            return args, kwargs

        args, kwargs, evidence = (
            normalize_pipeline_call(
                target,
                (),
                {
                    "raw_text": (
                        "/grade\n"
                        "문제: 최종 문제\n"
                        "최종 답안\n"
                        "끝."
                    )
                },
            )
        )
        self.assertEqual(args, ())
        self.assertEqual(
            kwargs["raw_text"],
            "문제: 최종 문제\n최종 답안",
        )
        self.assertTrue(evidence["changed"])


if __name__ == "__main__":
    unittest.main()
