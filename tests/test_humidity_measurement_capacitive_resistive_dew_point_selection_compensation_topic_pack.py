from __future__ import annotations

import json
import unittest
from pathlib import Path


TOPIC_ID = "humidity_measurement_capacitive_resistive_dew_point_selection_compensation"
REPO = Path(__file__).resolve().parents[1]
PACK = REPO / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = REPO / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class HumidityMeasurementTopicPackTest(unittest.TestCase):
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

    def test_02_anchor_integrity_global_id_recovery_and_outline_coverage(self) -> None:
        anchors = self.fact["anchors"]
        ids = [row["id"] for row in anchors]
        global_ids = [row["anchor_id"] for row in anchors]

        self.assertEqual(len(anchors), 22)
        self.assertEqual(len(set(ids)), 22)
        self.assertEqual(len(set(global_ids)), 22)

        self.assertIn("humidity_lifecycle_maintainability_selection", ids)
        self.assertNotIn("lifecycle_maintainability_selection", ids)
        self.assertIn("humidity_lifecycle_maintainability_selection", global_ids)
        self.assertNotIn("lifecycle_maintainability_selection", global_ids)

        covered: set[str] = set()
        for row in self.model["recommended_outline"]:
            refs = row["anchor_refs"]
            self.assertTrue(set(refs) <= set(ids))
            covered.update(refs)

        self.assertEqual(len(self.model["recommended_outline"]), 8)
        self.assertEqual(covered, set(ids))

    def test_03_humidity_parameter_definitions_and_temperature_dependence(self) -> None:
        for term in (
            "RH[%] = 100·P_w/P_ws(T)",
            "absolute humidity",
            "ρ_v = P_w/(R_v T)",
            "dew point",
            "frost point",
            "pressure dew point",
            "temperature",
        ):
            self.assertIn(term, self.serialized)

        fatal_by_id = {row["id"]: row for row in self.fact["fatal_wrong_claims"]}
        self.assertIn(
            "P_w/P_ws(T)",
            fatal_by_id["humidity_fatal_rh_absolute_same"]["correction"],
        )
        self.assertIn(
            "온도변화로 RH가 달라질 수 있다",
            fatal_by_id["humidity_fatal_rh_temperature_independent"]["correction"],
        )
        self.assertIn(
            "condensation이 시작되는 온도",
            fatal_by_id["humidity_fatal_dew_point_equals_rh"]["correction"],
        )

    def test_04_capacitive_and_resistive_transduction_remain_distinct(self) -> None:
        for term in (
            "capacitive humidity sensor",
            "polymer dielectric",
            "dielectric constant",
            "capacitance",
            "resistive humidity sensor",
            "hygroscopic",
            "resistance",
            "impedance",
            "AC excitation",
        ):
            self.assertIn(term.casefold(), self.serialized.casefold())

        fatal_by_id = {row["id"]: row for row in self.fact["fatal_wrong_claims"]}
        self.assertIn(
            "capacitance 변화를 측정",
            fatal_by_id["humidity_fatal_capacitive_resistance"]["correction"],
        )
        self.assertIn(
            "resistance 또는 impedance",
            fatal_by_id["humidity_fatal_resistive_capacitance"]["correction"],
        )

    def test_05_chilled_mirror_psychrometric_and_pressure_dewpoint_boundaries(self) -> None:
        for term in (
            "chilled mirror",
            "reflected light",
            "condensation onset",
            "mirror temperature",
            "psychrometric",
            "wet bulb",
            "dry bulb",
            "pressure dew point",
        ):
            self.assertIn(term.casefold(), self.serialized.casefold())

        self.assertIn(
            "Wet-bulb temperature를 dew point와 동일시하지 않는다.",
            self.sheet,
        )

        fatal_by_id = {row["id"]: row for row in self.fact["fatal_wrong_claims"]}
        self.assertIn(
            "pressure condition",
            fatal_by_id["humidity_fatal_pressure_dewpoint_same"]["correction"],
        )

    def test_06_temperature_condensation_warmed_probe_and_low_humidity_selection(self) -> None:
        for term in (
            "sensor surface temperature",
            "self-heating",
            "condensation",
            "warmed probe",
            "heated sensor",
            "actual RH",
            "low humidity",
            "trace moisture",
        ):
            self.assertIn(term.casefold(), self.serialized.casefold())

        fatal_by_id = {row["id"]: row for row in self.fact["fatal_wrong_claims"]}
        self.assertIn(
            "temperature",
            fatal_by_id["humidity_fatal_no_temperature_comp"]["correction"].casefold(),
        )
        self.assertIn(
            "ambient/process temperature",
            fatal_by_id["humidity_fatal_warmed_probe_direct_rh"]["correction"],
        )
        self.assertIn(
            "dew/frost-point",
            fatal_by_id["humidity_fatal_low_rh_always_capacitive"]["correction"],
        )

    def test_07_hysteresis_drift_contamination_and_calibration_contract(self) -> None:
        for term in (
            "hysteresis",
            "long-term drift",
            "chemical exposure",
            "contamination",
            "recovery",
            "calibration",
            "traceability",
            "equilibration",
        ):
            self.assertIn(term.casefold(), self.serialized.casefold())

        fatal_by_id = {row["id"]: row for row in self.fact["fatal_wrong_claims"]}
        self.assertIn(
            "recovery",
            fatal_by_id["humidity_fatal_condensation_no_effect"]["correction"].casefold(),
        )
        self.assertIn(
            "equilibration time",
            fatal_by_id["humidity_fatal_calibration_no_equilibrium"]["correction"],
        )

    def test_08_selection_and_lifecycle_field_application_contract(self) -> None:
        for term in (
            "process temperature",
            "pressure",
            "contaminants",
            "condensation",
            "response time",
            "hazardous area",
            "maintainability",
            "spare",
            "shutdown",
            "lifecycle cost",
        ):
            self.assertIn(term.casefold(), self.serialized.casefold())

        self.assertIn(
            "humidity_lifecycle_maintainability_selection",
            self.serialized,
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
            "passive_sensor_resistive_capacitive_inductive_transduction",
            "rtd_temperature_sensor_principle_pt100_wiring_compensation",
            "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization",
            "thermocouple_temperature_sensor_seebeck_reference_junction_compensation",
            "calibration_error_accuracy_precision",
            "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection",
        )
        for neighbor in neighbors:
            self.assertIn(neighbor, self.sheet)

        self.assertIn("Historical frequency: 근거가 없어 사용하지 않음", self.sheet)
        self.assertIn(
            "제품별 RH accuracy, exact sensing range, recovery time, heater temperature, calibration interval과 chemical-resistance 수치는 일반 법칙으로 사용하지 않는다.",
            self.sheet,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
