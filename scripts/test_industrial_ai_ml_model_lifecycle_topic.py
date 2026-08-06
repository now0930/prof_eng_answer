#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC = "industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle"
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
    "ai_ml_dl_hierarchy",
    "anomaly_detection_score_threshold",
    "remaining_useful_life_uncertainty",
    "train_validation_test_separation",
    "chronological_group_split",
    "data_leakage",
    "class_imbalance",
    "precision_metric",
    "recall_metric",
    "f1_metric",
    "production_monitoring",
    "drift_types",
    "retraining_trigger",
    "explainability_limits",
    "human_review_fallback",
    "mlops_lifecycle",
}

REQUIRED_FATALS = {
    "accuracy_guarantees_safety",
    "train_test_same_data",
    "future_leakage_valid",
    "imbalance_accuracy_sufficient",
    "anomaly_score_certain_fault",
    "predictive_maintenance_prevents_all_failures",
    "rul_exact_date",
    "threshold_no_tradeoff",
    "retraining_always_improves",
    "explainability_proves_causality",
    "closed_loop_without_constraints",
    "mlops_ci_cd_guarantees_safety",
}

BROAD_ALIASES = {
    "ai", "ml", "machine learning", "deep learning", "anomaly",
    "prediction", "model", "training", "accuracy", "mlops"
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class SW12SourceContractTests(unittest.TestCase):
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

    def test_08_ai_ml_task_boundaries(self) -> None:
        for marker in (
            "AI·Machine Learning·Deep Learning",
            "Supervised·Unsupervised",
            "Classification, Regression, Forecasting",
            "Anomaly Detection",
        ):
            self.assertIn(marker, self.sheet)

    def test_09_split_leakage_imbalance_contracts(self) -> None:
        combined = json.dumps(
            {"fact": self.fact, "logic": self.logic},
            ensure_ascii=False,
        )
        for marker in (
            "chronological_group_split",
            "data_leakage",
            "class_imbalance",
            "train_test_same_data",
            "future_leakage_valid",
        ):
            self.assertIn(marker, combined)

    def test_10_metric_formula_markers(self) -> None:
        for marker in (
            r"\mathrm{Precision}",
            r"\mathrm{Recall}",
            r"F_1",
            r"FPR",
            r"MAE",
            r"RMSE",
            r"ECE",
            r"J(\tau)",
        ):
            self.assertIn(marker, self.sheet)

    def test_11_anomaly_rul_threshold_guards(self) -> None:
        combined = json.dumps(
            {"fact": self.fact, "logic": self.logic},
            ensure_ascii=False,
        )
        for marker in (
            "anomaly_score_certain_fault",
            "predictive_maintenance_prevents_all_failures",
            "rul_exact_date",
            "threshold_no_tradeoff",
        ):
            self.assertIn(marker, combined)

    def test_12_deployment_version_monitoring(self) -> None:
        for marker in (
            "Training–Serving",
            "Model·Dataset·Feature·Code·Threshold",
            "Monitoring",
            "Rollback",
        ):
            self.assertIn(marker, self.sheet + self.readme)

    def test_13_drift_retraining_explainability(self) -> None:
        combined = self.sheet + json.dumps(self.logic, ensure_ascii=False)
        for marker in (
            "Data Drift",
            "Concept Drift",
            "Champion–Challenger",
            "Explainability",
            "Human Review",
            "retraining_always_improves",
        ):
            self.assertIn(marker, combined)

    def test_14_sw11_sw13_boundaries(self) -> None:
        for marker in (
            "SW-11과의 경계",
            "SW-13과의 경계",
            "Historian",
            "Physical AI",
            "Closed-loop AI",
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
            10,
        )
        self.assertGreaterEqual(len(self.model["high_score_points"]), 14)

    def test_16_no_forbidden_runtime_output_contract(self) -> None:
        combined = self.readme + self.sheet
        self.assertIn("Generated Bank", combined)
        self.assertIn("Production Python", combined)
        self.assertNotIn("rubrics/generated/", self.readme)
        self.assertNotIn("model_answer_router.py", self.readme)


if __name__ == "__main__":
    unittest.main(verbosity=2)
