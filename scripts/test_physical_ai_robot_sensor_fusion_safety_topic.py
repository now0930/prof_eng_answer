#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC = "physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"

FILES = {
    "readme": PACK / "README.md",
    "fact": PACK / "fact_anchor.json",
    "logic": PACK / "logic_check.json",
    "model": PACK / "model_answer.json",
    "importance": PACK / "topic_importance.json",
    "sheet": SHEET,
}

REQUIRED_ANCHORS = {
    "physical_ai_definition",
    "industrial_robot_architecture",
    "sensor_complementarity",
    "timestamp_and_synchronization",
    "calibration_coordinate_frame",
    "fusion_uncertainty",
    "common_cause_and_fault_detection",
    "state_estimation",
    "slam_relation",
    "digital_twin_fidelity",
    "digital_twin_synchronization",
    "synthetic_data_domain_gap",
    "closed_loop_ai",
    "latency_deadline_budget",
    "safety_envelope",
    "safe_state_fallback_degraded_mode",
    "functional_safety_separation",
    "runtime_monitoring_change_control",
}

REQUIRED_FATALS = {
    "digital_twin_always_identical",
    "sensor_fusion_eliminates_failures",
    "accuracy_guarantees_physical_safety",
    "edge_ai_removes_network_cybersecurity",
    "collaborative_robot_inherently_safe",
    "time_calibration_irrelevant",
    "slam_certifies_collision_safety",
    "simulation_pass_proves_real_world",
    "synthetic_data_replaces_real_data",
    "planner_direct_actuation_no_guard",
    "safe_state_fallback_unnecessary",
    "human_override_unnecessary",
    "redundancy_removes_common_cause",
    "uncontrolled_online_learning",
}

BROAD_ALIASES = {
    "physical ai", "robot", "sensor", "fusion", "digital twin",
    "slam", "safety", "edge ai", "autonomous", "planning"
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class SW13SourceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json(FILES["fact"])
        cls.logic = load_json(FILES["logic"])
        cls.model = load_json(FILES["model"])
        cls.importance = load_json(FILES["importance"])
        cls.sheet = FILES["sheet"].read_text(encoding="utf-8")
        cls.readme = FILES["readme"].read_text(encoding="utf-8")

    def test_01_all_allowed_files_exist(self) -> None:
        for name, path in FILES.items():
            with self.subTest(name=name):
                self.assertTrue(path.is_file(), path)

    def test_02_topic_and_modern_root_contracts(self) -> None:
        for row in (self.fact, self.logic, self.model, self.importance):
            self.assertEqual(row["topic_id"], TOPIC)
        self.assertEqual(self.fact["schema_version"], "fact_anchor.v1")
        self.assertEqual(self.logic["schema_version"], "topic_pack.logic_check.v1")
        self.assertEqual(self.model["schema_version"], "topic_pack.model_answer.v1")
        self.assertEqual(
            self.importance["schema_version"],
            "topic_pack.topic_importance.v1",
        )

    def test_03_anchor_schema_and_counts(self) -> None:
        self.assertEqual(len(self.fact["anchors"]), 30)
        required = {
            "id", "anchor_id", "statement", "importance", "keywords",
            "core_terms", "accepted_explanations", "rejected_explanations",
            "grading_notes", "source_basis", "claim", "description",
        }
        for row in self.fact["anchors"]:
            self.assertTrue(required.issubset(row))
            self.assertEqual(row["id"], row["anchor_id"])
            self.assertEqual(row["statement"], row["claim"])
            self.assertEqual(row["claim"], row["description"])

    def test_04_fatal_and_major_contracts(self) -> None:
        self.assertEqual(len(self.fact["fatal_wrong_claims"]), 16)
        profile = self.logic["llm_profile"]
        self.assertEqual(len(profile["fatal_conditions"]), 16)
        self.assertEqual(len(profile["major_checks"]), 12)
        self.assertGreaterEqual(len(profile["false_positive_cautions"]), 16)
        for row in self.fact["fatal_wrong_claims"]:
            self.assertEqual(row["severity"], "fatal")
            self.assertEqual(row["affected_layers"], ["C"])

    def test_05_required_anchor_and_fatal_ids(self) -> None:
        anchor_ids = {row["id"] for row in self.fact["anchors"]}
        fatal_ids = {row["id"] for row in self.fact["fatal_wrong_claims"]}
        self.assertTrue(REQUIRED_ANCHORS.issubset(anchor_ids))
        self.assertTrue(REQUIRED_FATALS.issubset(fatal_ids))

    def test_06_llm_profile_single_owner_contract(self) -> None:
        deterministic = self.logic["deterministic_checks"]
        self.assertFalse(deterministic["enabled"])
        self.assertEqual(deterministic["fatal_checks"], [])
        self.assertEqual(deterministic["major_checks"], [])
        self.assertEqual(deterministic["question_type_checks"], [])
        profile = self.logic["llm_profile"]
        self.assertTrue(profile["enabled"])
        self.assertEqual(profile["candidate_extraction"]["rules"], [])
        self.assertFalse(profile["score_policy"]["direct_score_application"])
        self.assertEqual(profile["score_policy"]["direct_d_e_effect"], "none")
        self.assertEqual(profile["score_policy"]["affected_layers"], ["C"])

    def test_07_model_anchor_reference_contract(self) -> None:
        anchor_ids = {row["id"] for row in self.fact["anchors"]}
        self.assertEqual(len(self.model["expected_question_patterns"]), 10)
        self.assertEqual(len(self.model["recommended_outline"]), 8)
        outline_union = set()
        for row in self.model["expected_question_patterns"]:
            self.assertTrue(set(row["required_anchor_ids"]) <= anchor_ids)
        for row in self.model["recommended_outline"]:
            refs = set(row["anchor_refs"])
            self.assertTrue(refs <= anchor_ids)
            outline_union.update(refs)
        self.assertEqual(outline_union, anchor_ids)

    def test_08_physical_ai_robot_boundary(self) -> None:
        for marker in (
            "Sensor–Actuator Closed Loop",
            "Industrial Robot System",
            "Tool, Payload",
            "Closed-loop AI",
        ):
            self.assertIn(marker, self.sheet)

    def test_09_sensor_fusion_contracts(self) -> None:
        combined = self.sheet + json.dumps(self.logic, ensure_ascii=False)
        for marker in (
            "Timestamp",
            "Intrinsic·Extrinsic Calibration",
            "Covariance",
            "Common Cause",
            "Residual",
            "sensor_fusion_eliminates_failures",
        ):
            self.assertIn(marker, combined)

    def test_10_state_slam_world_model(self) -> None:
        for marker in (
            "State Estimation",
            "Localization",
            "SLAM",
            "Observability",
            "World Model",
        ):
            self.assertIn(marker, self.sheet)

    def test_11_twin_simulation_domain_gap(self) -> None:
        combined = self.sheet + json.dumps(self.logic, ensure_ascii=False)
        for marker in (
            "Fidelity",
            "Stale Twin",
            "Scenario Coverage",
            "Domain Gap",
            "digital_twin_always_identical",
            "simulation_pass_proves_real_world",
        ):
            self.assertIn(marker, combined)

    def test_12_formula_markers(self) -> None:
        for marker in (
            r"{}^{A}\mathbf{p}",
            r"w_i=\frac{1}{\sigma_i^2}",
            r"\mathbf{K}_{k}",
            r"d_k^2",
            r"T_{\mathrm{loop}}",
            r"e_{\mathrm{twin}}",
            r"\mathcal{X}_{\mathrm{safe}}",
        ):
            self.assertIn(marker, self.sheet)

    def test_13_safety_control_guards(self) -> None:
        combined = self.sheet + json.dumps(self.logic, ensure_ascii=False)
        for marker in (
            "Safety Envelope",
            "Safe State",
            "Fallback",
            "Degraded Mode",
            "Supervisory Control",
            "Human Override",
            "planner_direct_actuation_no_guard",
        ):
            self.assertIn(marker, combined)

    def test_14_sw05_sw12_boundaries(self) -> None:
        for marker in (
            "SW-12와의 경계",
            "SW-05와의 경계",
            "Data Leakage",
            "Safety Software Lifecycle",
            "물리적 위험",
        ):
            self.assertIn(marker, self.sheet)

    def test_15_routing_and_importance_depth(self) -> None:
        aliases = self.model["routing_aliases"]
        self.assertEqual(len(aliases), 14)
        normalized = {row.strip().lower() for row in aliases}
        self.assertTrue(BROAD_ALIASES.isdisjoint(normalized))
        self.assertEqual(self.importance["difficulty"], "THEORY_CORE")
        self.assertEqual(
            self.importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )
        self.assertEqual(
            self.importance["question_type"],
            "PRINCIPLE_INTERPRETATION",
        )
        self.assertGreaterEqual(
            len(self.importance["high_band_unlock_conditions"]),
            12,
        )
        self.assertGreaterEqual(len(self.model["high_score_points"]), 16)

    def test_16_no_forbidden_runtime_output_contract(self) -> None:
        combined = self.readme + self.sheet
        self.assertIn("Generated Bank", combined)
        self.assertIn("Production Python", combined)
        self.assertNotIn("rubrics/generated/", self.readme)
        self.assertNotIn("model_answer_router.py", self.readme)


if __name__ == "__main__":
    unittest.main(verbosity=2)
