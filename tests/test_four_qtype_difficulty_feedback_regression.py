from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

import difficulty_output_adapter as difficulty_adapter
import grading_agents as ga


QTYPES = {
    "DEFINE": "스마트 센서의 정의와 구성요소를 설명하시오.",
    "PRINCIPLE_INTERPRETATION": (
        "2차 시스템의 감쇠비와 과도응답 특성을 설명하시오."
    ),
    "COMPARE_SELECTION": (
        "A 방식과 B 방식을 비교하고 선정 기준을 설명하시오."
    ),
    "PROBLEM_SOLVE": (
        "제어계의 문제점을 분석하고 개선방안을 설명하시오."
    ),
}

DIFFICULTIES = (
    "BASIC_CONCEPT",
    "THEORY_CORE",
    "FIELD_APPLICATION",
    "DESIGN_EVALUATION",
)

PUBLIC_KEYS = (
    "summary",
    "rewrite_advice",
    "improvement_points",
    "next_practice_focus",
    "weaknesses",
)

FORBIDDEN_UNASKED = (
    "비용, 시간, 적용 가능성, 기존 설비 영향",
    "비용·유지보수·기존 설비",
    "비용·유지보수 영향",
    "현장 적용·설계 판단·제언 순서로",
    "현장 적용성, 제언, 기술사적 판단 제시",
    "FIELD_APPLICATION 보완:",
    "FIELD_APPLICATION 고득점 조건:",
    "Cost-Benefit",
)

IDENTITY_PATCHES = (
    "attach_question_type_v2_to_grade",
    "ensure_grade_question_type_coverage",
    "attach_question_type_coverage_feedback",
    "apply_explicit_requirement_hard_cap",
    "apply_question_type_coverage_score_adjustment",
)


def identity(grade, *args, **kwargs):
    return grade


def base_grade() -> dict:
    return {
        "summary": "UPSTREAM SUMMARY",
        "question_type_evaluation": {},
        "rewrite_advice": [
            (
                "배경 → 문제 요구 → 유형별 Fact 기반 내용 설명 → "
                "현장 적용·설계 판단·제언 순서로 답안을 확장하세요."
            ),
            (
                "대책은 비용, 시간, 적용 가능성, 기존 설비 영향, "
                "운전 리스크까지 연결하세요."
            ),
            "핵심 요구와 Fact 관계를 명확히 설명하세요.",
            "대안 비교와 trade-off를 명확히 쓰세요.",
        ],
        "improvement_points": [
            (
                "FIELD_APPLICATION 보완: 선정 기준, 현장 조건, 문제점, "
                "개선방안, 비용·유지보수 영향을 함께 쓰세요."
            ),
            "명시 요구의 누락 항목을 보완하세요.",
        ],
        "next_practice_focus": [
            "현장 적용성, 제언, 기술사적 판단 제시",
            "문제 요구 해석·완전성",
        ],
        "weaknesses": [
            "비용 대비 성능(Cost-Benefit) 검토가 부족합니다.",
            "핵심 변수 설명이 부족합니다.",
        ],
        "rater_results": [],
    }


def public_snapshot(grade: dict) -> dict:
    return {
        key: deepcopy(grade.get(key))
        for key in PUBLIC_KEYS
    }


def public_text(grade: dict) -> str:
    rows = []

    for key in PUBLIC_KEYS:
        value = grade.get(key)

        if isinstance(value, list):
            rows.extend(str(item) for item in value)
        elif value is not None:
            rows.append(str(value))

    return "\n".join(rows)


def attach_difficulty(grade: dict, difficulty: str) -> dict:
    patches = [
        patch.object(
            difficulty_adapter,
            name,
            side_effect=identity,
        )
        for name in IDENTITY_PATCHES
    ]

    for ctx in patches:
        ctx.start()

    try:
        with (
            patch.object(
                difficulty_adapter,
                "summarize_question_strategy",
                return_value={
                    "matched": True,
                    "difficulty": difficulty,
                    "difficulty_label": difficulty,
                    "selection_importance": "NORMAL",
                    "selection_policy": "NORMAL",
                    "default_score_ceiling": 20,
                    "topic_id": "matrix_topic",
                },
            ),
            patch.object(
                difficulty_adapter,
                "_difficulty_topic_id_from_grade",
                return_value=None,
            ),
            patch.object(
                difficulty_adapter,
                "_topic_importance_strategy_from_topic_id",
                return_value={},
            ),
        ):
            return (
                difficulty_adapter
                .attach_difficulty_strategy_to_grade(
                    deepcopy(grade),
                    question_text="matrix question",
                )
            )
    finally:
        for ctx in reversed(patches):
            ctx.stop()


def final_project(
    grade: dict,
    qid: str,
    question: str,
) -> dict:
    return ga._phase9_apply_type_aware_de_feedback_policy(
        grade=deepcopy(grade),
        question_type_eval={
            "question_type": qid,
        },
        input_text=question,
    )


class FourQtypeDifficultyRegressionTest(unittest.TestCase):
    pass


def make_matrix_test(qid: str, difficulty: str):
    def test(self):
        source = base_grade()
        before_difficulty = public_snapshot(source)

        after_difficulty = attach_difficulty(
            source,
            difficulty,
        )

        # Difficulty may attach strategy metadata/warnings, but must not own
        # user-facing summary/advice/weakness/focus/improvement fields.
        self.assertEqual(
            public_snapshot(after_difficulty),
            before_difficulty,
        )

        final = final_project(
            after_difficulty,
            qid,
            QTYPES[qid],
        )

        self.assertEqual(
            final["difficulty_strategy"]["difficulty"],
            difficulty,
        )

        text = public_text(final)

        for token in FORBIDDEN_UNASKED:
            with self.subTest(token=token):
                self.assertNotIn(token, text)

        self.assertIn(
            "핵심 요구와 Fact 관계를 명확히 설명하세요.",
            text,
        )
        self.assertIn(
            "문제 요구 해석·완전성",
            text,
        )

        if qid == "COMPARE_SELECTION":
            self.assertIn(
                "대안 비교와 trade-off를 명확히 쓰세요.",
                text,
            )
        else:
            self.assertNotIn(
                "대안 비교와 trade-off를 명확히 쓰세요.",
                text,
            )

        if qid == "PRINCIPLE_INTERPRETATION":
            self.assertIn(
                "원리·해석형 D/E",
                text,
            )
            self.assertIn(
                "원리·수식·변수 의미·결과 해석의 연결",
                final["next_practice_focus"],
            )

        projection = final[
            "public_feedback_question_demand_projection"
        ]
        self.assertFalse(
            projection["score_axis_changed"]
        )
        self.assertFalse(
            projection["difficulty_axis_changed"]
        )

    return test


for _qid in QTYPES:
    for _difficulty in DIFFICULTIES:
        setattr(
            FourQtypeDifficultyRegressionTest,
            "test_matrix__"
            + _qid.lower()
            + "__"
            + _difficulty.lower(),
            make_matrix_test(
                _qid,
                _difficulty,
            ),
        )


class MatrixInvariantTest(unittest.TestCase):
    def test_same_qtype_public_feedback_is_identical_across_difficulty(self):
        for qid, question in QTYPES.items():
            snapshots = []

            for difficulty in DIFFICULTIES:
                final = final_project(
                    attach_difficulty(
                        base_grade(),
                        difficulty,
                    ),
                    qid,
                    question,
                )
                snapshots.append(
                    public_snapshot(final)
                )

            for snapshot in snapshots[1:]:
                self.assertEqual(
                    snapshot,
                    snapshots[0],
                    msg=qid,
                )

    def test_matrix_dimensions_are_locked(self):
        self.assertEqual(len(QTYPES), 4)
        self.assertEqual(len(DIFFICULTIES), 4)
        self.assertEqual(
            len(QTYPES) * len(DIFFICULTIES),
            16,
        )


if __name__ == "__main__":
    unittest.main(verbosity=0)
