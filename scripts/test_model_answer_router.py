#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any

# 이 파일을 `python3 scripts/test_model_answer_router.py`로 실행해도
# 저장소 루트의 모듈을 import할 수 있도록 한다.
ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from model_answer_router import find_model_answer_reference


PT100_TOPIC = "rtd_pt100_wire_connection_compensation"

PRINCIPLE_TYPE = {
    "primary_type": {
        "id": "PRINCIPLE_INTERPRETATION",
    }
}

GENERAL_TYPE = {
    "primary_type": {
        "id": "GENERAL",
    }
}


def make_answer(
    answer_id: str,
    topic_id: str,
    *,
    question_type: str = "PRINCIPLE_INTERPRETATION",
    question_examples: list[str] | None = None,
    topic_aliases: list[str] | None = None,
    aliases: list[str] | None = None,
    routing_aliases: list[str] | None = None,
    field_connection_points: list[str] | None = None,
    routing_field_points: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": answer_id,
        "topic_id": topic_id,
        "question_type": question_type,
        "title": topic_id,
        "question_examples": question_examples or [],
        "topic_aliases": topic_aliases or [],
        "aliases": aliases or [],
        "routing_aliases": routing_aliases or [],
        "expected_structure": [],
        "model_answer_outline": [],
        "high_score_features": [],
        "low_score_patterns": [],
        "field_connection_points": field_connection_points or [],
        "routing_field_points": routing_field_points or [],
        "revision_notes": [],
    }


def selected_topic(result: dict[str, Any]) -> str | None:
    reference = result.get("primary_reference") or {}
    return reference.get("topic_id")


class ModelAnswerRouterTest(unittest.TestCase):
    def test_question_topic_survives_answer_contamination(self) -> None:
        bank = {
            "policy": {},
            "answers": [
                make_answer(
                    "pt100",
                    "rtd_pt100",
                    topic_aliases=[
                        "PT100",
                        "RTD",
                        "3선식 브리지",
                    ],
                ),
                make_answer(
                    "ntc",
                    "thermistor_ntc",
                    topic_aliases=[
                        "NTC",
                        "thermistor",
                        "열폭주",
                    ],
                ),
            ],
        }

        result = find_model_answer_reference(
            question_text=(
                "PT100의 3선식 브리지와 "
                "리드선 저항 보상을 설명하시오."
            ),
            answer_text=(
                "NTC thermistor 열폭주를 반복하여 "
                "잘못 설명하였다."
            ),
            question_type_eval=PRINCIPLE_TYPE,
            bank=bank,
        )

        self.assertTrue(result["matched"])
        self.assertEqual(selected_topic(result), "rtd_pt100")
        self.assertGreater(
            result["question_score"],
            result["answer_score"],
        )

    def test_answer_only_signal_is_rejected(self) -> None:
        bank = {
            "policy": {},
            "answers": [
                make_answer(
                    "ntc",
                    "thermistor_ntc",
                    topic_aliases=[
                        "NTC",
                        "thermistor",
                    ],
                    field_connection_points=[
                        "온도 상승 저항 감소",
                    ],
                ),
            ],
        }

        result = find_model_answer_reference(
            question_text="다음 센서의 원리를 설명하시오.",
            answer_text=(
                "NTC thermistor는 온도 상승 시 "
                "저항이 감소한다."
            ),
            question_type_eval=PRINCIPLE_TYPE,
            bank=bank,
        )

        self.assertFalse(result["matched"])
        self.assertFalse(result["ambiguous"])
        self.assertEqual(
            result["routing_status"],
            "unmatched",
        )
        self.assertIsNone(result["primary_reference"])

    def test_tied_candidates_are_ambiguous(self) -> None:
        bank = {
            "policy": {},
            "answers": [
                make_answer(
                    "alpha",
                    "topic_alpha",
                    topic_aliases=["alpha"],
                ),
                make_answer(
                    "beta",
                    "topic_beta",
                    topic_aliases=["beta"],
                ),
            ],
        }

        result = find_model_answer_reference(
            question_text="alpha와 beta를 설명하시오.",
            question_type_eval=PRINCIPLE_TYPE,
            bank=bank,
        )

        self.assertFalse(result["matched"])
        self.assertTrue(result["ambiguous"])
        self.assertEqual(
            result["routing_status"],
            "ambiguous",
        )
        self.assertEqual(result["score_margin"], 0)
        self.assertIsNone(result["primary_reference"])

    def test_weak_candidate_is_rejected(self) -> None:
        bank = {
            "policy": {},
            "answers": [
                make_answer(
                    "weak",
                    "weak_topic",
                    topic_aliases=["weak"],
                ),
            ],
        }

        result = find_model_answer_reference(
            question_text="weak",
            question_type_eval=GENERAL_TYPE,
            bank=bank,
        )

        self.assertFalse(result["matched"])
        self.assertEqual(
            result["routing_status"],
            "insufficient_score",
        )
        self.assertLess(result["top_score"], 50)

    def test_alias_fields_are_merged_and_deduplicated(self) -> None:
        bank = {
            "policy": {},
            "answers": [
                make_answer(
                    "alias_union",
                    "alias_union_topic",
                    topic_aliases=[
                        "PT100",
                        "RTD",
                    ],
                    aliases=[
                        "측온저항체",
                        "PT-100",
                    ],
                    routing_aliases=[
                        "3선식 브리지",
                        "RTD",
                    ],
                ),
            ],
        }

        result = find_model_answer_reference(
            question_text=(
                "PT100 측온저항체의 "
                "3선식 브리지를 설명하시오."
            ),
            question_type_eval=PRINCIPLE_TYPE,
            bank=bank,
        )

        self.assertTrue(result["matched"])

        terms = result["primary_reference"]["topic_aliases"]

        self.assertIn("PT100", terms)
        self.assertIn("RTD", terms)
        self.assertIn("측온저항체", terms)
        self.assertIn("3선식 브리지", terms)

        # normalize_text 기준으로 PT100과 PT-100은 중복이다.
        self.assertNotIn("PT-100", terms)
        self.assertEqual(terms.count("RTD"), 1)

    def test_field_fields_are_merged(self) -> None:
        bank = {
            "policy": {},
            "answers": [
                make_answer(
                    "field_union",
                    "field_union_topic",
                    field_connection_points=[
                        "리드선 저항",
                    ],
                    routing_field_points=[
                        "3선식 브리지 평형",
                        "리드선 저항",
                    ],
                ),
            ],
        }

        result = find_model_answer_reference(
            question_text=(
                "리드선 저항과 "
                "3선식 브리지 평형을 설명하시오."
            ),
            question_type_eval=PRINCIPLE_TYPE,
            bank=bank,
        )

        self.assertTrue(result["matched"])

        fields = result["primary_reference"][
            "field_connection_points"
        ]

        self.assertIn("리드선 저항", fields)
        self.assertIn("3선식 브리지 평형", fields)
        self.assertEqual(fields.count("리드선 저항"), 1)

    def test_question_field_bonus_is_capped(self) -> None:
        field_terms = [
            f"field{i:02d}"
            for i in range(1, 11)
        ]

        bank = {
            "policy": {},
            "answers": [
                make_answer(
                    "field_cap",
                    "field_cap_topic",
                    field_connection_points=field_terms,
                ),
            ],
        }

        result = find_model_answer_reference(
            question_text=" ".join(field_terms),
            question_type_eval=GENERAL_TYPE,
            bank=bank,
        )

        self.assertFalse(result["matched"])
        self.assertEqual(
            result["routing_status"],
            "insufficient_score",
        )

        candidate = result["candidates"][0]

        self.assertEqual(candidate["question_score"], 15)
        self.assertEqual(
            candidate["score_breakdown"]["question"],
            15,
        )

    def test_answer_field_bonus_is_capped(self) -> None:
        field_terms = [
            f"answerfield{i:02d}"
            for i in range(1, 11)
        ]

        bank = {
            "policy": {},
            "answers": [
                make_answer(
                    "answer_field_cap",
                    "answer_field_cap_topic",
                    question_examples=["고유 기준 문제"],
                    field_connection_points=field_terms,
                ),
            ],
        }

        result = find_model_answer_reference(
            question_text="고유 기준 문제",
            answer_text=" ".join(field_terms),
            question_type_eval=GENERAL_TYPE,
            bank=bank,
        )

        self.assertTrue(result["matched"])
        self.assertEqual(result["answer_score"], 5)

    def test_real_pt100_question_routes_to_pt100(self) -> None:
        result = find_model_answer_reference(
            question_text=(
                "측온저항체 PT100의 2선식, 3선식, "
                "4선식과 3선식 브리지 평형을 "
                "설명하시오."
            ),
            answer_text=(
                "NTC thermal runaway를 잘못 "
                "길게 설명하였다."
            ),
            question_type_eval=PRINCIPLE_TYPE,
        )

        self.assertTrue(result["matched"])
        self.assertFalse(result["ambiguous"])
        self.assertEqual(
            result["routing_status"],
            "matched",
        )
        self.assertEqual(
            selected_topic(result),
            PT100_TOPIC,
        )

    def test_ntc_ptc_only_question_does_not_route_pt100(self) -> None:
        result = find_model_answer_reference(
            question_text=(
                "NTC와 PTC thermistor의 특성과 "
                "thermal runaway를 설명하시오."
            ),
            question_type_eval=PRINCIPLE_TYPE,
        )

        self.assertNotEqual(
            selected_topic(result),
            PT100_TOPIC,
        )

    def test_thermistor_only_question_does_not_route_pt100(self) -> None:
        result = find_model_answer_reference(
            question_text=(
                "thermistor의 Steinhart-Hart 식을 "
                "설명하시오."
            ),
            question_type_eval=PRINCIPLE_TYPE,
        )

        self.assertNotEqual(
            selected_topic(result),
            PT100_TOPIC,
        )

    def test_explicit_pt100_comparison_keeps_pt100_candidate(
        self,
    ) -> None:
        result = find_model_answer_reference(
            question_text=(
                "PT100 RTD와 thermistor의 차이를 "
                "설명하시오."
            ),
            question_type_eval=PRINCIPLE_TYPE,
        )

        self.assertTrue(result["matched"])
        self.assertEqual(
            selected_topic(result),
            PT100_TOPIC,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
