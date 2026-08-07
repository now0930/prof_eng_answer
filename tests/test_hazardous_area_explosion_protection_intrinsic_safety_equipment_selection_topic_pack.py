#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

TOPIC_ID = "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection"
EXPECTED_QUESTION_TYPE = "COMPARE_SELECTION"
EXPECTED_DIFFICULTY = "FIELD_APPLICATION"
EXPECTED_SELECTION_IMPORTANCE = "NORMAL"
EXPECTED_ANCHOR_COUNT = 22
EXPECTED_FATAL_COUNT = 13
EXPECTED_ALIAS_COUNT = 18
EXPECTED_OUTLINE_COUNT = 8


class HazardousAreaExplosionProtectionTopicPackTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repo = Path(__file__).resolve().parents[1]
        cls.pack = cls.repo / "rubrics" / "topic_packs" / TOPIC_ID
        cls.sheet = cls.repo / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"
        cls.fact = cls._load("fact_anchor.json")
        cls.logic = cls._load("logic_check.json")
        cls.model = cls._load("model_answer.json")
        cls.importance = cls._load("topic_importance.json")
        cls.readme = (cls.pack / "README.md").read_text(encoding="utf-8")
        cls.sheet_text = cls.sheet.read_text(encoding="utf-8")

    @classmethod
    def _load(cls, name: str) -> dict:
        path = cls.pack / name
        if not path.is_file():
            raise AssertionError(f"missing Topic Pack source: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def test_01_identity_question_type_and_difficulty_contract(self) -> None:
        for name, data in (
            ("fact_anchor.json", self.fact),
            ("logic_check.json", self.logic),
            ("model_answer.json", self.model),
            ("topic_importance.json", self.importance),
        ):
            with self.subTest(name=name):
                self.assertEqual(data["topic_id"], TOPIC_ID)

        self.assertEqual(self.fact["question_type_hint"], EXPECTED_QUESTION_TYPE)
        self.assertEqual(self.model["question_type"], EXPECTED_QUESTION_TYPE)
        self.assertEqual(self.importance["question_type"], EXPECTED_QUESTION_TYPE)
        self.assertEqual(self.importance["difficulty"], EXPECTED_DIFFICULTY)
        self.assertEqual(self.logic["llm_profile"]["difficulty"], EXPECTED_DIFFICULTY)
        self.assertEqual(
            self.importance["selection_importance"], EXPECTED_SELECTION_IMPORTANCE
        )
        self.assertIn("historical_frequency_not_used", self.importance["revision_notes"])

    def test_02_anchor_integrity_and_outline_full_coverage(self) -> None:
        anchors = self.fact["anchors"]
        self.assertEqual(len(anchors), EXPECTED_ANCHOR_COUNT)
        ids = [a["id"] for a in anchors]
        self.assertEqual(len(ids), len(set(ids)))
        for anchor in anchors:
            self.assertEqual(anchor["id"], anchor["anchor_id"])
            self.assertIn(anchor["importance"], {"core", "important"})
            self.assertTrue(anchor["statement"].strip())

        outline = self.model["recommended_outline"]
        self.assertEqual(len(outline), EXPECTED_OUTLINE_COUNT)
        refs = [ref for section in outline for ref in section["anchor_refs"]]
        self.assertEqual(set(refs), set(ids))
        self.assertEqual(len(refs), len(set(refs)))

    def test_03_zone_epl_and_ex_marking_selection_chain(self) -> None:
        truth = "\n".join(self.logic["llm_profile"]["truth_schema"])
        required = (
            "Zone 0",
            "Zone 1",
            "Zone 2",
            "Zone 20",
            "Zone 21",
            "Zone 22",
            "Ga",
            "Gb",
            "Gc",
            "Da",
            "Db",
            "Dc",
            "Ex 표시",
            "EPL",
            "그룹",
            "주위온도",
            "인증서 조건",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, truth)

        anchor_map = {a["id"]: a["statement"] for a in self.fact["anchors"]}
        self.assertIn("가스", anchor_map["gas_zone_0_1_2_meaning"])
        self.assertIn("분진", anchor_map["dust_zone_20_21_22_meaning"])
        self.assertIn("별도로 평가", anchor_map["dust_zone_20_21_22_meaning"])
        self.assertIn("Zone만 보는 것이 아니라", anchor_map["ex_marking_selection_chain"])

    def test_04_ex_protection_methods_keep_distinct_physical_principles(self) -> None:
        anchor_map = {a["id"]: a["statement"] for a in self.fact["anchors"]}
        expected_tokens = {
            "flameproof_ex_d_principle": ("Ex d", "폭발압력", "화염"),
            "increased_safety_ex_e_principle": ("Ex e", "아크", "절연"),
            "intrinsic_safety_ex_i_principle": ("Ex i", "에너지", "고장조건"),
            "pressurization_ex_p_principle": ("Ex p", "퍼지", "과압"),
        }
        for anchor_id, tokens in expected_tokens.items():
            statement = anchor_map[anchor_id]
            for token in tokens:
                with self.subTest(anchor_id=anchor_id, token=token):
                    self.assertIn(token, statement)

        self.assertIn(
            "내부 점화를 원천적으로 없애는 방식은 아니다",
            anchor_map["flameproof_ex_d_principle"],
        )

    def test_05_intrinsic_safety_entity_direction_and_loop_boundary(self) -> None:
        anchor_map = {a["id"]: a["statement"] for a in self.fact["anchors"]}
        entity = anchor_map["entity_voltage_current_power_compatibility"]
        for expr in ("Uo≤Ui", "Io≤Ii", "Po≤Pi"):
            self.assertIn(expr, entity)

        system = anchor_map["is_system_components"]
        for token in ("본질안전 기기", "관련기기", "barrier/galvanic isolator", "배선"):
            self.assertIn(token, system)
        self.assertIn("전체 루프가 자동 적합", system)

        cable = anchor_map["entity_capacitance_inductance_cable"]
        for token in ("케이블", "Co", "Lo", "정전용량", "인덕턴스"):
            self.assertIn(token, cable)

    def test_06_barrier_wiring_certificate_environment_and_lifecycle(self) -> None:
        anchor_map = {a["id"]: a["statement"] for a in self.fact["anchors"]}
        barrier = anchor_map["zener_barrier_galvanic_isolator_selection"]
        for token in ("Zener barrier", "galvanic isolator", "절연", "접지", "유지보수"):
            self.assertIn(token, barrier)

        wiring = anchor_map["is_wiring_segregation_identification"]
        for token in ("분리", "식별", "차폐", "접지"):
            self.assertIn(token, wiring)

        certificate = anchor_map["certificate_special_conditions_control_drawing"]
        for token in ("특수사용조건", "control drawing", "cable gland", "주위온도"):
            self.assertIn(token, certificate)

        environment = anchor_map["ex_environmental_suitability_independent_check"]
        for token in ("IP 등급", "부식", "진동", "별도로 확인"):
            self.assertIn(token, environment)

        lifecycle = anchor_map["inspection_maintenance_documentation"]
        for token in ("도면", "인증서", "루프 계산", "검사", "정비", "변경"):
            self.assertIn(token, lifecycle)

    def test_07_llm_semantic_guardrails_without_deterministic_fatal_scoring(self) -> None:
        deterministic = self.logic["deterministic_checks"]
        profile = self.logic["llm_profile"]
        self.assertFalse(deterministic["enabled"])
        self.assertEqual(deterministic["fatal_checks"], [])
        self.assertEqual(deterministic["major_checks"], [])
        self.assertEqual(deterministic["question_type_checks"], [])
        self.assertTrue(profile["enabled"])
        self.assertFalse(profile["candidate_extraction"]["enabled"])
        self.assertEqual(profile["candidate_extraction"]["rules"], [])
        self.assertFalse(profile["score_policy"]["direct_score_application"])
        self.assertEqual(profile["score_policy"]["direct_d_e_effect"], "none")
        self.assertEqual(len(profile["fatal_conditions"]), EXPECTED_FATAL_COUNT)
        self.assertEqual(len(profile["truth_schema"]), EXPECTED_ANCHOR_COUNT)
        fatal_ids = [item["id"] for item in profile["fatal_conditions"]]
        self.assertEqual(len(fatal_ids), len(set(fatal_ids)))
        self.assertTrue(all(item["severity"] == "fatal" for item in profile["fatal_conditions"]))

    def test_08_routing_aliases_are_unique_and_scope_is_hazardous_area_selection(self) -> None:
        model_aliases = self.model["routing_aliases"]
        logic_aliases = self.logic["deterministic_checks"]["topic_aliases"]
        self.assertEqual(len(model_aliases), EXPECTED_ALIAS_COUNT)
        self.assertEqual(model_aliases, logic_aliases)
        self.assertEqual(len(model_aliases), len(set(model_aliases)))

        alias_text = "\n".join(model_aliases).lower()
        for term in ("hazardous", "방폭", "intrinsic safety", "본질안전"):
            self.assertIn(term.lower(), alias_text)

        # SIS/SIL may appear only as an explicit exclusion/caution, not as a routing owner.
        self.assertNotRegex(alias_text, re.compile(r"\bsis\b|\bsil\b", re.IGNORECASE))
        boundary_text = "\n".join(self.model["common_missing_points"])
        self.assertIn("SIS/SIL", boundary_text)
        self.assertIn("혼합", boundary_text)

    def test_09_topic_sheet_and_readme_preserve_authoring_scope(self) -> None:
        combined = self.sheet_text + "\n" + self.readme
        for token in (
            TOPIC_ID,
            "COMPARE_SELECTION",
            "FIELD_APPLICATION",
            "Zone",
            "EPL",
            "Ex d",
            "Ex e",
            "Ex i",
            "Ex p",
            "Uo",
            "Ui",
            "Zener barrier",
            "galvanic isolator",
        ):
            with self.subTest(token=token):
                self.assertIn(token, combined)


if __name__ == "__main__":
    unittest.main(verbosity=2)
