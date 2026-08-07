from __future__ import annotations

import json
import unittest
from pathlib import Path


TOPIC_ID = "speed_rotation_measurement_encoder_proximity_tachometer_selection_error"
REPO = Path(__file__).resolve().parents[1]
PACK = REPO / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = REPO / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class SpeedRotationMeasurementTopicPackTest(unittest.TestCase):
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

    def test_03_speed_equations_and_effective_count_contract(self) -> None:
        for term in (
            "ω = 2πn/60",
            "n[rpm] = 60f/N_eff",
            "n = 60m/(N_eff·Δt)",
            "n = 60/(N_eff·T_c)",
            "PPR",
            "CPR",
            "x1/x2/x4",
        ):
            self.assertIn(term, self.serialized)

        fatal_by_id = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }
        self.assertIn(
            "n = 60f/N_eff",
            fatal_by_id["speed_fatal_frequency_direct_rpm"]["correction"],
        )
        self.assertIn(
            "N_eff",
            fatal_by_id["speed_fatal_ppr_ignore_decode"]["correction"],
        )

    def test_04_incremental_quadrature_index_and_absolute_are_distinct(self) -> None:
        for term in (
            "incremental encoder",
            "quadrature",
            "A channel",
            "B channel",
            "direction",
            "Z channel",
            "index pulse",
            "absolute encoder",
            "digital word",
        ):
            self.assertIn(term, self.serialized)

        fatal_by_id = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }
        self.assertIn(
            "방향",
            fatal_by_id["speed_fatal_quadrature_no_direction"]["correction"],
        )
        self.assertIn(
            "multi-turn absolute position",
            fatal_by_id["speed_fatal_index_absolute"]["correction"],
        )

    def test_05_low_speed_resolution_and_frequency_limit_tradeoff(self) -> None:
        for term in (
            "counting window",
            "quantization",
            "period measurement",
            "timer resolution",
            "maximum frequency",
            "PLC high-speed counter",
        ):
            self.assertIn(term.casefold(), self.serialized.casefold())

        fatal_by_id = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }
        self.assertIn(
            "period/reciprocal",
            fatal_by_id["speed_fatal_fixed_window_no_low_speed_error"]["correction"],
        )
        self.assertIn(
            "frequency limit",
            fatal_by_id["speed_fatal_more_ppr_always_better"]["correction"],
        )

    def test_06_proximity_gear_tooth_and_variable_reluctance_principles(self) -> None:
        for term in (
            "inductive proximity",
            "eddy current",
            "metal target",
            "n = 60f/Z",
            "variable reluctance",
            "induced voltage",
            "air gap",
            "low speed",
        ):
            self.assertIn(term.casefold(), self.serialized.casefold())

        fatal_by_id = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }
        self.assertIn(
            "target",
            fatal_by_id["speed_fatal_proximity_any_target"]["correction"].casefold(),
        )
        self.assertIn(
            "air gap",
            fatal_by_id["speed_fatal_vr_low_speed_constant"]["correction"].casefold(),
        )

    def test_07_tachogenerator_and_digital_tachometer_boundary(self) -> None:
        for term in (
            "DC tachogenerator",
            "V_t ≈ K_t·n",
            "polarity",
            "brush",
            "commutator",
            "digital tachometer",
            "pulse count",
        ):
            self.assertIn(term.casefold(), self.serialized.casefold())

        fatal_by_id = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }
        self.assertIn(
            "속도에 대체로 비례",
            fatal_by_id["speed_fatal_tacho_constant_voltage"]["correction"],
        )
        self.assertIn(
            "polarity",
            fatal_by_id["speed_fatal_tacho_no_direction"]["correction"],
        )

    def test_08_selection_mounting_and_electrical_error_contract(self) -> None:
        for term in (
            "minimum speed",
            "maximum speed",
            "overspeed",
            "direction",
            "absolute position",
            "resolution",
            "misalignment",
            "runout",
            "coupling",
            "shielding",
            "grounding",
            "line driver",
            "lifecycle cost",
        ):
            self.assertIn(term.casefold(), self.serialized.casefold())

        fatal_by_id = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }
        self.assertIn(
            "misalignment",
            fatal_by_id["speed_fatal_mounting_no_error"]["correction"].casefold(),
        )
        self.assertIn(
            "pulse dropout",
            fatal_by_id["speed_fatal_mounting_no_error"]["correction"].casefold(),
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
            "lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error",
            "passive_sensor_resistive_capacitive_inductive_transduction",
            "physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control",
            "calibration_error_accuracy_precision",
            "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection",
            "industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience",
        )
        for neighbor in neighbors:
            self.assertIn(neighbor, self.sheet)

        self.assertIn("Historical frequency: 근거가 없어 사용하지 않음", self.sheet)
        self.assertIn(
            "제품별 PPR, sensing distance, maximum RPM, K_t와 정확도 수치는 일반 법칙으로 사용하지 않는다.",
            self.sheet,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
