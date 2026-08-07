from __future__ import annotations

import json
import unittest
from pathlib import Path


TOPIC_ID = "pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error"
REPO = Path(__file__).resolve().parents[1]
PACK = REPO / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = REPO / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class PressureMeasurementSensorTopicPackTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.logic = load("logic_check.json")
        cls.model = load("model_answer.json")
        cls.importance = load("topic_importance.json")
        cls.readme = (PACK / "README.md").read_text(encoding="utf-8")
        cls.sheet = SHEET.read_text(encoding="utf-8")
        cls.serialized = json.dumps(
            {
                "fact": cls.fact,
                "logic": cls.logic,
                "model": cls.model,
                "importance": cls.importance,
            },
            ensure_ascii=False,
        )

    def test_01_identity_question_type_and_difficulty_contract(self) -> None:
        for obj in (self.fact, self.logic, self.model, self.importance):
            self.assertEqual(obj["topic_id"], TOPIC_ID)

        self.assertEqual(self.fact["question_type_hint"], "PRINCIPLE_INTERPRETATION")
        self.assertEqual(self.model["question_type"], "PRINCIPLE_INTERPRETATION")
        self.assertEqual(self.importance["question_type"], "PRINCIPLE_INTERPRETATION")
        self.assertEqual(self.importance["difficulty"], "FIELD_APPLICATION")
        self.assertEqual(self.importance["selection_importance"], "NORMAL")

    def test_02_anchor_integrity_and_outline_full_coverage(self) -> None:
        anchors = self.fact["anchors"]
        anchor_ids = [row["id"] for row in anchors]
        self.assertEqual(len(anchors), 22)
        self.assertEqual(len(set(anchor_ids)), 22)

        outline = self.model["recommended_outline"]
        self.assertEqual(len(outline), 8)

        covered: set[str] = set()
        for row in outline:
            refs = row["anchor_refs"]
            self.assertTrue(refs)
            self.assertTrue(set(refs) <= set(anchor_ids))
            covered.update(refs)

        self.assertEqual(covered, set(anchor_ids))

    def test_03_pressure_reference_and_basic_equations(self) -> None:
        for term in (
            "absolute pressure",
            "gauge pressure",
            "differential pressure",
            "P_abs = P_gauge + P_atm",
            "ΔP = P_H - P_L",
        ):
            self.assertIn(term, self.serialized)

        fatal_by_id = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }
        self.assertIn("진공 기준", fatal_by_id["pressure_fatal_abs_gauge_same"]["correction"])
        self.assertIn("대기압 기준", fatal_by_id["pressure_fatal_abs_gauge_same"]["correction"])
        self.assertIn("차", fatal_by_id["pressure_fatal_dp_sum"]["correction"])

    def test_04_bourdon_and_diaphragm_physical_principles_remain_distinct(self) -> None:
        required = (
            "Bourdon tube",
            "elastic deformation",
            "oval cross-section",
            "diaphragm",
            "pressure difference",
            "diaphragm seal",
            "fill fluid",
        )
        for term in required:
            self.assertIn(term, self.serialized)

        combined = self.sheet + "\n" + self.readme
        self.assertIn("Diaphragm sensing element", combined)
        self.assertIn("Diaphragm seal", combined)

    def test_05_piezoresistive_bridge_and_static_measurement_contract(self) -> None:
        for term in (
            "piezoresistive",
            "Wheatstone bridge",
            "resistance change",
            "static pressure",
            "temperature compensation",
            "excitation",
        ):
            self.assertIn(term, self.serialized)

        fatal_by_id = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }
        self.assertIn(
            "정적 및 저주파 압력 측정이 가능",
            fatal_by_id["pressure_fatal_piezoresistive_no_static"]["correction"],
        )
        self.assertIn(
            "piezoelectric",
            fatal_by_id["pressure_fatal_piezoresistive_no_excitation"]["correction"],
        )

    def test_06_dp_static_pressure_and_dp_level_ownership_boundary(self) -> None:
        for term in (
            "DP transmitter",
            "high side",
            "low side",
            "static line pressure",
            "zero effect",
            "span effect",
        ):
            self.assertIn(term, self.serialized)

        self.assertIn(
            "특정 model의 %값을 모든 DP transmitter의 공통 공식으로 사용하지 않는다.",
            self.sheet,
        )
        self.assertIn(
            "differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error",
            self.sheet,
        )

        for term in ("Hydrostatic level", "Density compensation", "Wet leg", "Dry leg"):
            self.assertIn(term, self.sheet)

    def test_07_selection_mechanical_limits_and_total_performance(self) -> None:
        for term in (
            "URL",
            "LRL",
            "turndown",
            "maximum working pressure",
            "overrange",
            "burst pressure",
            "wetted material",
            "reference accuracy",
            "total performance",
        ):
            self.assertIn(term.casefold(), self.serialized.casefold())

        fatal_by_id = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }
        self.assertIn(
            "별도 한계",
            fatal_by_id["pressure_fatal_range_equals_burst"]["correction"],
        )
        self.assertIn(
            "total performance",
            fatal_by_id["pressure_fatal_accuracy_only"]["correction"],
        )

    def test_08_zero_span_impulse_line_and_dynamic_error_contract(self) -> None:
        for term in (
            "zero shift",
            "span shift",
            "zero trim",
            "impulse line",
            "leak",
            "blockage",
            "gas pocket",
            "pulsation",
            "vibration",
            "response time",
        ):
            self.assertIn(term, self.serialized)

        fatal_by_id = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }
        self.assertIn(
            "span",
            fatal_by_id["pressure_fatal_zero_trim_fixes_span"]["correction"].casefold(),
        )
        self.assertIn(
            "누설",
            fatal_by_id["pressure_fatal_impulse_line_no_effect"]["correction"],
        )

    def test_09_llm_guardrails_aliases_and_neighbor_ownership(self) -> None:
        det = self.logic["deterministic_checks"]
        profile = self.logic["llm_profile"]

        self.assertFalse(det["enabled"])
        self.assertEqual(det["fatal_checks"], [])
        self.assertEqual(det["major_checks"], [])
        self.assertEqual(det["question_type_checks"], [])
        self.assertTrue(profile["enabled"])
        self.assertFalse(profile["candidate_extraction"]["enabled"])
        self.assertEqual(profile["candidate_extraction"]["rules"], [])
        self.assertFalse(profile["score_policy"]["direct_score_application"])
        self.assertEqual(profile["score_policy"]["direct_d_e_effect"], "none")
        self.assertEqual(profile["score_policy"]["affected_layers"], ["C"])

        aliases = self.model["routing_aliases"]
        self.assertEqual(len(aliases), 18)
        normalized = [" ".join(a.casefold().split()) for a in aliases]
        self.assertEqual(len(normalized), len(set(normalized)))

        neighbors = (
            "differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error",
            "strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error",
            "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration",
            "passive_sensor_resistive_capacitive_inductive_transduction",
            "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection",
            "calibration_error_accuracy_precision",
        )
        for neighbor in neighbors:
            self.assertIn(neighbor, self.sheet)

        self.assertIn("Historical frequency: 근거가 없어 사용하지 않음", self.sheet)
        self.assertIn("제품별 수치 사양은 일반 법칙으로 사용하지 않는다.", self.sheet)


if __name__ == "__main__":
    unittest.main(verbosity=2)
