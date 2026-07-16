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


PT100_TOPIC = "rtd_temperature_sensor_principle_pt100_wiring_compensation"

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



import json as _strain_router_json
import unittest as _strain_router_unittest
from pathlib import Path as _StrainRouterPath

from model_answer_router import (
    find_model_answer_reference as _strain_find_model_answer_reference,
)


class StrainGaugeLoadCellRoutingRegressionTests(
    _strain_router_unittest.TestCase
):
    STRAIN_TOPIC = (
        "strain_gauge_load_cell_wheatstone_bridge_"
        "temperature_compensation_error"
    )
    PASSIVE_TOPIC = (
        "passive_sensor_resistive_capacitive_"
        "inductive_transduction"
    )
    RTD_TOPIC = (
        "rtd_temperature_sensor_principle_"
        "pt100_wiring_compensation"
    )
    THERMISTOR_TOPIC = (
        "thermistor_temperature_sensor_ntc_ptc_"
        "characteristics_measurement_linearization"
    )
    THERMOCOUPLE_TOPIC = (
        "thermocouple_temperature_sensor_seebeck_"
        "reference_junction_compensation"
    )
    TEMPERATURE_ERROR_TOPIC = (
        "temperature_measurement_error_heat_transfer"
    )

    @classmethod
    def setUpClass(cls):
        root = _StrainRouterPath(__file__).resolve().parents[1]
        bank_path = (
            root
            / "rubrics"
            / "generated"
            / "model_answers.generated.json"
        )

        cls.bank = _strain_router_json.loads(
            bank_path.read_text(encoding="utf-8")
        )
        answers = cls.bank.get("answers")

        if not isinstance(answers, list):
            raise AssertionError(
                "generated model-answer bank has no answers list"
            )

        cls.answer_by_topic = {
            item["topic_id"]: item
            for item in answers
            if isinstance(item, dict)
            and isinstance(item.get("topic_id"), str)
        }

        required_topics = {
            cls.STRAIN_TOPIC,
            cls.PASSIVE_TOPIC,
            cls.RTD_TOPIC,
            cls.THERMISTOR_TOPIC,
            cls.THERMOCOUPLE_TOPIC,
            cls.TEMPERATURE_ERROR_TOPIC,
        }

        missing = sorted(
            required_topics - set(cls.answer_by_topic)
        )

        if missing:
            raise AssertionError(
                f"required Generated Topics are missing: {missing}"
            )

    @classmethod
    def _question_type_eval(cls, topic_id):
        question_type = (
            cls.answer_by_topic[topic_id].get("question_type")
            or "GENERAL"
        )

        return {
            "primary_type": {
                "id": question_type,
                "confidence": "high",
            }
        }

    @staticmethod
    def _fact_eval(topic_id):
        return {
            "topic_id": topic_id,
            "matched": True,
            "confidence": "high",
        }

    @classmethod
    def _route(
        cls,
        question,
        *,
        answer_text="",
        fact_topic=None,
        question_type_topic=None,
    ):
        return _strain_find_model_answer_reference(
            question_text=question,
            answer_text=answer_text,
            question_type_eval=(
                cls._question_type_eval(question_type_topic)
                if question_type_topic is not None
                else None
            ),
            fact_eval=(
                cls._fact_eval(fact_topic)
                if fact_topic is not None
                else None
            ),
            bank=cls.bank,
        )

    @classmethod
    def _topic_ids(cls, value):
        found = []

        def append(candidate):
            if (
                isinstance(candidate, str)
                and candidate in cls.answer_by_topic
                and candidate not in found
            ):
                found.append(candidate)

        def walk(child):
            if isinstance(child, str):
                append(child)
                return

            if isinstance(child, dict):
                priority_keys = (
                    "primary_reference",
                    "answer",
                    "candidates",
                    "topic_id",
                    "id",
                )
                visited = set()

                for key in priority_keys:
                    if key in child:
                        visited.add(key)
                        walk(child[key])

                for key, nested in child.items():
                    if key not in visited:
                        walk(nested)

                return

            if isinstance(child, (list, tuple)):
                for nested in child:
                    walk(nested)

        walk(value)
        return found

    @classmethod
    def _primary_topic(cls, result):
        primary = result.get("primary_reference")

        if isinstance(primary, dict):
            for key in ("topic_id", "id"):
                candidate = primary.get(key)

                if (
                    isinstance(candidate, str)
                    and candidate in cls.answer_by_topic
                ):
                    return candidate

        ids = cls._topic_ids(primary)
        return ids[0] if ids else None

    def assertPrimaryTopic(self, result, expected_topic):
        self.assertTrue(
            result.get("matched"),
            msg=result,
        )
        self.assertEqual(
            self._primary_topic(result),
            expected_topic,
            msg=result,
        )

    def assertTopicNotRouted(self, result, forbidden_topic):
        self.assertNotIn(
            forbidden_topic,
            self._topic_ids(result),
            msg=result,
        )

    def test_exact_question_example_routes_without_pipeline_context(self):
        result = self._route(
            "스트레인 게이지의 저항변화 원리와 "
            "게이지율을 설명하시오."
        )

        self.assertPrimaryTopic(
            result,
            self.STRAIN_TOPIC,
        )

    def test_pipeline_direct_strain_question_routes_with_fact_context(self):
        result = self._route(
            "스트레인 게이지의 게이지율과 "
            "저항변화 원리를 설명하시오.",
            fact_topic=self.STRAIN_TOPIC,
            question_type_topic=self.STRAIN_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.STRAIN_TOPIC,
        )

    def test_pipeline_strain_centered_mixed_question_keeps_primary(self):
        result = self._route(
            "저항형 센서를 비교하되 스트레인 게이지의 "
            "게이지율, 휘트스톤 브리지와 로드셀 적용을 "
            "중심으로 설명하시오.",
            fact_topic=self.STRAIN_TOPIC,
            question_type_topic=self.STRAIN_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.STRAIN_TOPIC,
        )

    def test_pipeline_strain_ignores_temperature_answer_terms(self):
        result = self._route(
            "스트레인 게이지식 로드셀의 브리지, "
            "mV/V 감도와 온도보상을 설명하시오.",
            answer_text=(
                "비교를 위해 RTD와 thermistor의 "
                "저항 변화도 간단히 언급한다."
            ),
            fact_topic=self.STRAIN_TOPIC,
            question_type_topic=self.STRAIN_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.STRAIN_TOPIC,
        )
        self.assertTopicNotRouted(
            result,
            self.RTD_TOPIC,
        )
        self.assertTopicNotRouted(
            result,
            self.THERMISTOR_TOPIC,
        )

    def test_legacy_passive_question_only_is_unmatched_without_leak(self):
        question = (
            "저항형, 용량형, 유도형 수동센서의 "
            "변환원리를 비교하시오."
        )

        question_only = self._route(question)

        self.assertFalse(
            question_only.get("matched"),
            msg=question_only,
        )
        self.assertIsNone(
            self._primary_topic(question_only),
            msg=question_only,
        )
        self.assertTopicNotRouted(
            question_only,
            self.STRAIN_TOPIC,
        )

        pipeline = self._route(
            question,
            fact_topic=self.PASSIVE_TOPIC,
            question_type_topic=self.PASSIVE_TOPIC,
        )

        self.assertPrimaryTopic(
            pipeline,
            self.PASSIVE_TOPIC,
        )
        self.assertTopicNotRouted(
            pipeline,
            self.STRAIN_TOPIC,
        )

    def test_legacy_temperature_error_is_unmatched_without_leak(self):
        question = (
            "온도 측정에서 열전도, 대류, 복사와 "
            "삽입오차 및 응답지연을 설명하시오."
        )

        question_only = self._route(question)

        self.assertFalse(
            question_only.get("matched"),
            msg=question_only,
        )
        self.assertIsNone(
            self._primary_topic(question_only),
            msg=question_only,
        )
        self.assertTopicNotRouted(
            question_only,
            self.STRAIN_TOPIC,
        )

        pipeline = self._route(
            question,
            fact_topic=self.TEMPERATURE_ERROR_TOPIC,
            question_type_topic=self.TEMPERATURE_ERROR_TOPIC,
        )

        self.assertPrimaryTopic(
            pipeline,
            self.TEMPERATURE_ERROR_TOPIC,
        )
        self.assertTopicNotRouted(
            pipeline,
            self.STRAIN_TOPIC,
        )

    def test_temperature_sensor_topics_do_not_leak_to_strain(self):
        cases = [
            (
                self.RTD_TOPIC,
                "RTD와 Pt100의 측정원리 및 "
                "2선식·3선식·4선식 보상을 설명하시오.",
                "다른 저항형 센서 예로 스트레인 게이지와 "
                "로드셀의 브리지를 일부 언급한다.",
            ),
            (
                self.THERMISTOR_TOPIC,
                "NTC와 PTC thermistor의 특성과 "
                "선형화 방법을 설명하시오.",
                "",
            ),
            (
                self.THERMOCOUPLE_TOPIC,
                "열전대의 Seebeck 효과와 "
                "기준접점 보상을 설명하시오.",
                "",
            ),
        ]

        for expected_topic, question, answer_text in cases:
            with self.subTest(topic=expected_topic):
                result = self._route(
                    question,
                    answer_text=answer_text,
                    fact_topic=expected_topic,
                    question_type_topic=expected_topic,
                )

                self.assertPrimaryTopic(
                    result,
                    expected_topic,
                )
                self.assertTopicNotRouted(
                    result,
                    self.STRAIN_TOPIC,
                )


THERMOCOUPLE_TOPIC = 'thermocouple_temperature_sensor_seebeck_reference_junction_compensation'

class ThermocoupleRoutingRegressionTest(unittest.TestCase):

    def test_real_thermocouple_question_routes_to_thermocouple(self):
        result = find_model_answer_reference(
            question_text='열전대의 Seebeck 효과, 측정접점과 기준접점, 냉접점 보상 및 보상도선을 설명하시오.',
            answer_text='열전대는 서로 다른 두 도체와 접점 온도차로 열기전력을 발생시킨다. 기준접점 온도를 측정하여 냉접점 보상하고 종류별 표준표로 온도를 환산한다.',
            question_type_eval=PRINCIPLE_TYPE,
        )
        primary = result.get("primary_reference") or {}
        candidate_topics = [
            candidate.get("answer", {}).get("topic_id")
            for candidate in result.get("candidates", [])
            if isinstance(candidate, dict)
        ]

        self.assertTrue(result.get("matched"))
        self.assertEqual(
            primary.get("topic_id"),
            THERMOCOUPLE_TOPIC,
        )


    def test_explicit_thermocouple_comparison_keeps_thermocouple_candidate(self):
        result = find_model_answer_reference(
            question_text='열전대와 RTD를 비교하되 열전대의 Seebeck 효과, 기준접점 보상, 연장도선과 보상도선을 중심으로 설명하시오.',
            answer_text='열전대는 온도차에 따른 mV 열기전력을 이용하고 RTD는 여자전류로 저항을 측정한다. 열전대에는 기준접점 보상과 전용 보상도선이 필요하다.',
            question_type_eval=PRINCIPLE_TYPE,
        )
        primary = result.get("primary_reference") or {}
        candidate_topics = [
            candidate.get("answer", {}).get("topic_id")
            for candidate in result.get("candidates", [])
            if isinstance(candidate, dict)
        ]

        self.assertTrue(result.get("matched"))
        self.assertEqual(
            primary.get("topic_id"),
            THERMOCOUPLE_TOPIC,
        )


    def test_rtd_only_question_does_not_retain_thermocouple_candidate(self):
        result = find_model_answer_reference(
            question_text='Pt100 RTD의 저항-온도 관계와 3선식 및 4선식 리드선 보상 방법을 설명하시오.',
            answer_text='Pt100은 저항식 온도센서이며 3선식은 리드저항의 대칭을 가정하고 4선식은 Kelvin 방식으로 측정한다.',
            question_type_eval=PRINCIPLE_TYPE,
        )
        primary = result.get("primary_reference") or {}
        candidate_topics = [
            candidate.get("answer", {}).get("topic_id")
            for candidate in result.get("candidates", [])
            if isinstance(candidate, dict)
        ]

        self.assertNotEqual(
            primary.get("topic_id"),
            THERMOCOUPLE_TOPIC,
        )
        self.assertNotIn(
            THERMOCOUPLE_TOPIC,
            candidate_topics,
        )


    def _route_for_thermistor_regression(
        self,
        question_text,
        answer_text="",
    ):
        from model_answer_router import (
            find_model_answer_reference,
        )

        return find_model_answer_reference(
            question_text=question_text,
            answer_text=answer_text,
            question_type_eval={
                "question_type":
                    "PRINCIPLE_INTERPRETATION",
                "predicted_type":
                    "PRINCIPLE_INTERPRETATION",
                "confidence":
                    "high",
            },
        )

    def _thermistor_regression_topic_ids(
        self,
        value,
    ):
        topic_ids = set()

        def visit(node):
            if isinstance(node, dict):
                topic_id = node.get("topic_id")

                if isinstance(topic_id, str):
                    topic_ids.add(topic_id)

                for child in node.values():
                    visit(child)

            elif isinstance(node, list):
                for child in node:
                    visit(child)

        visit(value)

        return topic_ids

    def _assert_thermistor_primary(
        self,
        result,
    ):
        thermistor_topic = (
            "thermistor_temperature_sensor_"
            "ntc_ptc_characteristics_measurement_linearization"
        )

        primary = (
            result.get("primary_reference")
            or {}
        )

        topic_ids = (
            self
            ._thermistor_regression_topic_ids(
                result
            )
        )

        self.assertTrue(
            result.get("matched")
        )

        self.assertEqual(
            primary.get("topic_id"),
            thermistor_topic,
        )

        self.assertIn(
            thermistor_topic,
            topic_ids,
        )

        return topic_ids

    def test_thermistor_only_question_does_not_retain_thermocouple_candidate(
        self,
    ):
        thermocouple_topic = (
            "thermocouple_temperature_sensor_"
            "seebeck_reference_junction_compensation"
        )

        result = self._route_for_thermistor_regression(
            (
                "NTC Thermistor의 온도에 따른 저항 감소, "
                "B-상수 식과 Steinhart-Hart 선형화를 설명하시오."
            )
        )

        topic_ids = self._assert_thermistor_primary(
            result
        )

        self.assertNotIn(
            thermocouple_topic,
            topic_ids,
        )

    def test_ptc_thermistor_question_routes_to_thermistor(
        self,
    ):
        result = self._route_for_thermistor_regression(
            (
                "PTC Thermistor의 전이온도, 저항 증가와 "
                "과전류 보호 및 자기조절 히터 특성을 설명하시오."
            )
        )

        self._assert_thermistor_primary(
            result
        )

    def test_explicit_thermistor_comparison_keeps_thermistor_primary(
        self,
    ):
        rtd_topic = (
            "rtd_temperature_sensor_principle_"
            "pt100_wiring_compensation"
        )

        result = self._route_for_thermistor_regression(
            (
                "Thermistor와 RTD를 비교하되 Thermistor의 "
                "NTC·PTC 특성, B-상수, 비선형성과 자기발열을 "
                "중심으로 설명하시오."
            )
        )

        topic_ids = self._assert_thermistor_primary(
            result
        )

        self.assertIn(
            rtd_topic,
            topic_ids,
        )

    def test_rtd_and_thermocouple_only_questions_exclude_thermistor(
        self,
    ):
        thermistor_topic = (
            "thermistor_temperature_sensor_"
            "ntc_ptc_characteristics_measurement_linearization"
        )

        questions = (
            (
                "Pt100 RTD의 금속 저항온도계수와 "
                "2선식, 3선식, 4선식 리드선 보상을 설명하시오."
            ),
            (
                "열전대의 Seebeck 효과, 측정접점과 기준접점, "
                "냉접점 보상 및 보상도선을 설명하시오."
            ),
        )

        for question_text in questions:
            with self.subTest(
                question=question_text
            ):
                result = (
                    self
                    ._route_for_thermistor_regression(
                        question_text
                    )
                )

                primary = (
                    result.get("primary_reference")
                    or {}
                )

                topic_ids = (
                    self
                    ._thermistor_regression_topic_ids(
                        result
                    )
                )

                self.assertNotEqual(
                    primary.get("topic_id"),
                    thermistor_topic,
                )

                self.assertNotIn(
                    thermistor_topic,
                    topic_ids,
                )

    def test_thermistor_question_survives_foreign_answer_contamination(
        self,
    ):
        result = self._route_for_thermistor_regression(
            (
                "Thermistor의 NTC·PTC 저항-온도 특성과 "
                "자기발열 및 선형화 방법을 설명하시오."
            ),
            (
                "Pt100은 0℃에서 100 Ω이며 3선식으로 "
                "리드선 저항을 보상한다. 열전대는 Seebeck 효과와 "
                "냉접점 보상을 사용한다."
            ),
        )

        self._assert_thermistor_primary(
            result
        )


    def test_thermocouple_question_survives_rtd_answer_contamination(self):
        result = find_model_answer_reference(
            question_text='열전대의 Seebeck 효과, 측정접점과 기준접점 보상 원리를 설명하시오.',
            answer_text='Pt100은 0도에서 100옴이며 3선식 브리지와 4선식 Kelvin 측정으로 리드선 저항을 보상한다.',
            question_type_eval=PRINCIPLE_TYPE,
        )
        primary = result.get("primary_reference") or {}
        candidate_topics = [
            candidate.get("answer", {}).get("topic_id")
            for candidate in result.get("candidates", [])
            if isinstance(candidate, dict)
        ]

        self.assertTrue(result.get("matched"))
        self.assertEqual(
            primary.get("topic_id"),
            THERMOCOUPLE_TOPIC,
        )
class RouterTestFileStructureRegressionTest(unittest.TestCase):
    def test_main_guard_is_final_top_level_statement(self):
        import ast
        from pathlib import Path

        path = Path(__file__)
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )

        main_nodes = [
            node
            for node in tree.body
            if (
                isinstance(node, ast.If)
                and isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "__name__"
                and len(node.test.ops) == 1
                and isinstance(node.test.ops[0], ast.Eq)
                and len(node.test.comparators) == 1
                and isinstance(
                    node.test.comparators[0],
                    ast.Constant,
                )
                and node.test.comparators[0].value == "__main__"
            )
        ]

        self.assertEqual(
            len(main_nodes),
            1,
            msg="router test file must contain one __main__ guard",
        )
        self.assertIs(
            tree.body[-1],
            main_nodes[0],
            msg=(
                "__main__ guard must remain the final top-level "
                "statement so direct execution discovers every test"
            ),
        )


class PiezoelectricRoutingRegressionTests(
    StrainGaugeLoadCellRoutingRegressionTests
):
    PIEZO_TOPIC = (
        "piezoelectric_sensor_charge_amplifier_"
        "dynamic_force_pressure_acceleration"
    )

    test_exact_question_example_routes_without_pipeline_context = None
    test_legacy_passive_question_only_is_unmatched_without_leak = None
    test_legacy_temperature_error_is_unmatched_without_leak = None
    test_pipeline_direct_strain_question_routes_with_fact_context = None
    test_pipeline_strain_centered_mixed_question_keeps_primary = None
    test_pipeline_strain_ignores_temperature_answer_terms = None
    test_temperature_sensor_topics_do_not_leak_to_strain = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if cls.PIEZO_TOPIC not in cls.answer_by_topic:
            raise AssertionError(
                "Piezoelectric Generated Topic is missing"
            )

    def test_exact_piezoelectric_question_examples_route_without_context(
        self,
    ):
        questions = [
            "압전식 센서의 측정원리와 특징을 설명하시오.",
            "압전센서용 전하증폭기의 원리와 "
            "설계요소를 설명하시오.",
            "전하출력형 압전센서와 IEPE 센서를 비교하시오.",
            "압전센서의 전기적 등가회로와 "
            "정적 측정의 한계를 설명하시오.",
        ]

        for question in questions:
            with self.subTest(question=question):
                result = self._route(question)

                self.assertPrimaryTopic(
                    result,
                    self.PIEZO_TOPIC,
                )

    def test_pipeline_rephrased_piezoelectric_question_routes(self):
        result = self._route(
            "압전소자의 Q=dF 관계, 전하증폭기, "
            "IEPE 신호처리와 동적 측정대역을 설명하시오.",
            fact_topic=self.PIEZO_TOPIC,
            question_type_topic=self.PIEZO_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.PIEZO_TOPIC,
        )

    def test_pipeline_piezoelectric_centered_load_cell_comparison(
        self,
    ):
        result = self._route(
            "스트레인 게이지식 로드셀과 비교하여 "
            "압전식 힘센서의 전하증폭기, 정적 측정 한계와 "
            "동적 힘 측정 장점을 설명하시오.",
            fact_topic=self.PIEZO_TOPIC,
            question_type_topic=self.PIEZO_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.PIEZO_TOPIC,
        )

    def test_pipeline_strain_centered_question_keeps_strain_primary(
        self,
    ):
        result = self._route(
            "스트레인 게이지식 로드셀의 게이지율, "
            "Wheatstone bridge, mV/V와 크리프를 설명하시오.",
            answer_text=(
                "비교대상으로 압전식 힘센서와 "
                "전하증폭기를 짧게 언급한다."
            ),
            fact_topic=self.STRAIN_TOPIC,
            question_type_topic=self.STRAIN_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.STRAIN_TOPIC,
        )
        self.assertTopicNotRouted(
            result,
            self.PIEZO_TOPIC,
        )

    def test_generic_passive_question_boundary(self):
        question = (
            "저항형, 용량형, 유도형 수동센서의 "
            "변환원리를 비교하시오."
        )

        question_only = self._route(question)

        self.assertFalse(
            question_only.get("matched"),
            msg=question_only,
        )
        self.assertIsNone(
            self._primary_topic(question_only),
            msg=question_only,
        )
        self.assertTopicNotRouted(
            question_only,
            self.PIEZO_TOPIC,
        )

        pipeline = self._route(
            question,
            fact_topic=self.PASSIVE_TOPIC,
            question_type_topic=self.PASSIVE_TOPIC,
        )

        self.assertPrimaryTopic(
            pipeline,
            self.PASSIVE_TOPIC,
        )
        self.assertTopicNotRouted(
            pipeline,
            self.PIEZO_TOPIC,
        )

    def test_temperature_sensor_topics_do_not_leak_to_piezoelectric(
        self,
    ):
        cases = [
            (
                self.RTD_TOPIC,
                "RTD와 Pt100의 측정원리 및 "
                "2선식·3선식·4선식 배선보상을 설명하시오.",
                "압전센서의 전하출력과 비교한다.",
            ),
            (
                self.THERMISTOR_TOPIC,
                "NTC와 PTC thermistor의 특성과 "
                "선형화 방법을 설명하시오.",
                "",
            ),
            (
                self.THERMOCOUPLE_TOPIC,
                "열전대의 Seebeck 효과와 "
                "기준접점 보상을 설명하시오.",
                "",
            ),
        ]

        for expected_topic, question, answer_text in cases:
            with self.subTest(topic=expected_topic):
                result = self._route(
                    question,
                    answer_text=answer_text,
                    fact_topic=expected_topic,
                    question_type_topic=expected_topic,
                )

                self.assertPrimaryTopic(
                    result,
                    expected_topic,
                )
                self.assertTopicNotRouted(
                    result,
                    self.PIEZO_TOPIC,
                )

    def test_temperature_measurement_error_does_not_leak_to_piezoelectric(
        self,
    ):
        result = self._route(
            "온도 측정에서 열전도, 대류, 복사, "
            "삽입오차와 응답지연을 설명하시오.",
            fact_topic=self.TEMPERATURE_ERROR_TOPIC,
            question_type_topic=self.TEMPERATURE_ERROR_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.TEMPERATURE_ERROR_TOPIC,
        )
        self.assertTopicNotRouted(
            result,
            self.PIEZO_TOPIC,
        )

    def test_accelerometer_question_keeps_piezoelectric_primary(self):
        result = self._route(
            "압전 가속도계의 원리, 주파수응답과 "
            "설치방법을 설명하시오."
        )

        self.assertPrimaryTopic(
            result,
            self.PIEZO_TOPIC,
        )



class LVDTRVDTRoutingRegressionTests(
    StrainGaugeLoadCellRoutingRegressionTests
):
    LVDT_TOPIC = (
        "lvdt_rvdt_differential_transformer_"
        "demodulation_displacement_angle_error"
    )
    PIEZO_TOPIC = (
        "piezoelectric_sensor_charge_amplifier_"
        "dynamic_force_pressure_acceleration"
    )

    test_exact_question_example_routes_without_pipeline_context = None
    test_legacy_passive_question_only_is_unmatched_without_leak = None
    test_legacy_temperature_error_is_unmatched_without_leak = None
    test_pipeline_direct_strain_question_routes_with_fact_context = None
    test_pipeline_strain_centered_mixed_question_keeps_primary = None
    test_pipeline_strain_ignores_temperature_answer_terms = None
    test_temperature_sensor_topics_do_not_leak_to_strain = None

    def test_exact_lvdt_questions_route_without_context(self):
        lvdt_answer = self.answer_by_topic[self.LVDT_TOPIC]
        passive_answer = self.answer_by_topic[self.PASSIVE_TOPIC]

        self.assertNotIn(
            "LVDT",
            lvdt_answer.get("routing_aliases", []),
        )
        self.assertIn(
            "LVDT",
            passive_answer.get("routing_aliases", []),
        )

        questions = [
            "LVDT의 원리와 특징을 설명하시오.",
            (
                "차동변압기식 변위센서의 구조와 "
                "동작원리를 설명하시오."
            ),
            (
                "LVDT 신호조절에서 위상민감 복조가 "
                "필요한 이유를 설명하시오."
            ),
            (
                "LVDT의 영점 잔류전압 원인과 "
                "대책을 설명하시오."
            ),
        ]

        for question in questions:
            with self.subTest(question=question):
                result = self._route(question)

                self.assertPrimaryTopic(
                    result,
                    self.LVDT_TOPIC,
                )

    def test_exact_rvdt_question_routes_without_context(self):
        result = self._route(
            "RVDT의 원리와 회전각 측정 특성을 설명하시오."
        )

        self.assertPrimaryTopic(
            result,
            self.LVDT_TOPIC,
        )

    def test_pipeline_rephrased_lvdt_question_routes(self):
        result = self._route(
            (
                "1차 교류 여자, 두 2차 코일의 직렬 역접속, "
                "Eo=Es1-Es2와 위상민감 복조를 이용한 "
                "변위 측정을 설명하시오."
            ),
            fact_topic=self.LVDT_TOPIC,
            question_type_topic=self.LVDT_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.LVDT_TOPIC,
        )

    def test_lvdt_centered_strain_comparison_keeps_lvdt_primary(self):
        result = self._route(
            (
                "LVDT와 스트레인 게이지식 변위센서를 비교하되 "
                "LVDT의 가동 철심, 차동출력, 위상민감 복조와 "
                "선형범위를 중심으로 설명하시오."
            ),
            fact_topic=self.LVDT_TOPIC,
            question_type_topic=self.LVDT_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.LVDT_TOPIC,
        )

    def test_lvdt_centered_passive_comparison_keeps_lvdt_primary(self):
        result = self._route(
            (
                "일반 유도형 수동센서와 비교하여 LVDT의 "
                "1차 교류 여자, 직렬 역접속, 가동 철심과 "
                "차동출력을 중심으로 설명하시오."
            ),
            fact_topic=self.LVDT_TOPIC,
            question_type_topic=self.LVDT_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.LVDT_TOPIC,
        )

    def test_generic_passive_question_does_not_leak_to_lvdt(self):
        question = (
            "저항형, 용량형, 유도형 수동센서의 "
            "변환원리를 비교하시오."
        )

        question_only = self._route(question)

        self.assertFalse(
            question_only.get("matched"),
            msg=question_only,
        )
        self.assertIsNone(
            self._primary_topic(question_only),
            msg=question_only,
        )
        self.assertTopicNotRouted(
            question_only,
            self.LVDT_TOPIC,
        )

        pipeline = self._route(
            question,
            fact_topic=self.PASSIVE_TOPIC,
            question_type_topic=self.PASSIVE_TOPIC,
        )

        self.assertPrimaryTopic(
            pipeline,
            self.PASSIVE_TOPIC,
        )
        self.assertTopicNotRouted(
            pipeline,
            self.LVDT_TOPIC,
        )

    def test_strain_question_does_not_leak_to_lvdt(self):
        result = self._route(
            (
                "스트레인 게이지식 로드셀의 게이지율, "
                "Wheatstone bridge, mV/V 감도와 "
                "크리프를 설명하시오."
            ),
            answer_text=(
                "비교대상으로 LVDT의 가동 철심과 "
                "차동출력을 짧게 언급한다."
            ),
            fact_topic=self.STRAIN_TOPIC,
            question_type_topic=self.STRAIN_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.STRAIN_TOPIC,
        )
        self.assertTopicNotRouted(
            result,
            self.LVDT_TOPIC,
        )

    def test_piezoelectric_question_does_not_leak_to_lvdt(self):
        result = self._route(
            (
                "압전식 힘센서의 직접 압전효과, Q=dF, "
                "전하증폭기와 동적 측정대역을 설명하시오."
            ),
            answer_text=(
                "비교대상으로 LVDT의 변위 측정과 "
                "위상민감 복조를 짧게 언급한다."
            ),
            fact_topic=self.PIEZO_TOPIC,
            question_type_topic=self.PIEZO_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.PIEZO_TOPIC,
        )
        self.assertTopicNotRouted(
            result,
            self.LVDT_TOPIC,
        )

    def test_lvdt_question_survives_foreign_answer_contamination(self):
        result = self._route(
            (
                "LVDT의 교류 여자, 직렬 역접속, 영점, "
                "출력 진폭·위상과 위상민감 복조를 설명하시오."
            ),
            answer_text=(
                "스트레인 게이지의 Wheatstone bridge와 mV/V, "
                "압전센서의 Q=dF와 전하증폭기를 잘못 길게 설명한다."
            ),
            fact_topic=self.LVDT_TOPIC,
            question_type_topic=self.LVDT_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.LVDT_TOPIC,
        )
        self.assertTopicNotRouted(
            result,
            self.STRAIN_TOPIC,
        )
        self.assertTopicNotRouted(
            result,
            self.PIEZO_TOPIC,
        )

    def test_rvdt_question_survives_foreign_answer_contamination(self):
        result = self._route(
            (
                "RVDT의 차동변압기 원리, 출력 진폭과 위상, "
                "제한된 회전각 측정범위를 설명하시오."
            ),
            answer_text=(
                "일반 저항형·용량형 수동센서의 "
                "변환원리를 잘못 중심으로 설명한다."
            ),
            fact_topic=self.LVDT_TOPIC,
            question_type_topic=self.LVDT_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.LVDT_TOPIC,
        )
        self.assertTopicNotRouted(
            result,
            self.PASSIVE_TOPIC,
        )



# CONTROL_VALVE_FLUID_FORCE_ROUTING_REGRESSION
class ControlValveFluidForceRoutingRegressionTests(
    StrainGaugeLoadCellRoutingRegressionTests
):
    CONTROL_VALVE_TOPIC = (
        "control_valve_fluid_forces_unbalance_"
        "friction_actuator_sizing_fail_safe"
    )

    test_exact_question_example_routes_without_pipeline_context = None
    test_legacy_passive_question_only_is_unmatched_without_leak = None
    test_legacy_temperature_error_is_unmatched_without_leak = None
    test_pipeline_direct_strain_question_routes_with_fact_context = None
    test_pipeline_strain_centered_mixed_question_keeps_primary = None
    test_pipeline_strain_ignores_temperature_answer_terms = None
    test_temperature_sensor_topics_do_not_leak_to_strain = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if cls.CONTROL_VALVE_TOPIC not in cls.answer_by_topic:
            raise AssertionError(
                "Control-valve Generated Topic is missing"
            )

    def test_exact_control_valve_aliases_route_without_context(self):
        result = self._route(
            "제어밸브 유체력과 밸브 불평형력을 설명하고 "
            "FTO, FTC, pressure tends to open과 "
            "pressure tends to close를 비교하시오."
        )

        self.assertPrimaryTopic(
            result,
            self.CONTROL_VALVE_TOPIC,
        )

    def test_control_valve_free_body_routes_with_pipeline_context(self):
        result = self._route(
            "글로브 제어밸브 플러그와 스템의 자유물체도에서 "
            "압력력, 패킹 마찰력, 스프링력과 시트 하중을 "
            "설명하시오.",
            fact_topic=self.CONTROL_VALVE_TOPIC,
            question_type_topic=self.CONTROL_VALVE_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.CONTROL_VALVE_TOPIC,
        )

    def test_control_valve_fto_ftc_routes_with_pipeline_context(self):
        result = self._route(
            "제어밸브의 FTO와 FTC를 플러그 형상, 시트 위치, "
            "P1과 P2 및 유효 압력면적으로 설명하시오.",
            fact_topic=self.CONTROL_VALVE_TOPIC,
            question_type_topic=self.CONTROL_VALVE_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.CONTROL_VALVE_TOPIC,
        )

    def test_control_valve_balanced_trim_routes_with_pipeline_context(self):
        result = self._route(
            "Balanced trim과 unbalanced trim의 잔류 불평형력, "
            "balance seal 마찰과 액추에이터 요구추력을 "
            "비교하시오.",
            fact_topic=self.CONTROL_VALVE_TOPIC,
            question_type_topic=self.CONTROL_VALVE_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.CONTROL_VALVE_TOPIC,
        )

    def test_control_valve_fail_close_routes_with_pipeline_context(self):
        result = self._route(
            "공압식 제어밸브의 Bench set, 스프링 예압, "
            "breakaway friction과 Fail-Close 힘 조건을 "
            "설명하시오.",
            fact_topic=self.CONTROL_VALVE_TOPIC,
            question_type_topic=self.CONTROL_VALVE_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.CONTROL_VALVE_TOPIC,
        )

    def test_control_valve_stiction_routes_with_pipeline_context(self):
        result = self._route(
            "제어밸브의 패킹 마찰과 가이드 마찰, "
            "breakaway friction, deadband와 stiction의 "
            "관계를 설명하시오.",
            fact_topic=self.CONTROL_VALVE_TOPIC,
            question_type_topic=self.CONTROL_VALVE_TOPIC,
        )

        self.assertPrimaryTopic(
            result,
            self.CONTROL_VALVE_TOPIC,
        )


if __name__ == "__main__":
    unittest.main()
