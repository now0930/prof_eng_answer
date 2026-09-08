#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

try:
    from audit_topic_pack_atomicity import audit_topic_pack_inventory
except ModuleNotFoundError:  # python -m unittest scripts.test_...
    from scripts.audit_topic_pack_atomicity import audit_topic_pack_inventory


ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "rubrics" / "topic_packs"


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def make_pack(
    root: Path,
    topic_id: str,
    *,
    model_id: str | None = None,
    string_pattern: bool = False,
    divergent_questions: bool = False,
    divergent_aliases: bool = False,
    divergent_truth: bool = False,
    core_facts: list[str] | None = None,
    unmanaged_status: bool = False,
) -> None:
    pack = root / topic_id
    pack.mkdir(parents=True)
    anchors = [
        {
            "anchor_id": f"{topic_id}_a{index}",
            "statement": f"{topic_id} voltage current signal principle {index}",
        }
        for index in range(5)
    ]
    pattern: object
    if string_pattern:
        pattern = f"{topic_id}의 원리를 설명하시오."
    else:
        pattern = {
            "pattern": f"{topic_id} voltage current 원리를 설명하시오.",
            "required_anchor_ids": [anchors[0]["anchor_id"]],
        }
    examples = (
        ["unrelated migration backup question"]
        if divergent_questions
        else [f"{topic_id} voltage current 원리를 설명하시오."]
    )
    routing = [f"{topic_id} voltage", f"{topic_id} current"]
    legacy_aliases = (
        ["unrelated migration", "unrelated backup"]
        if divergent_aliases
        else list(routing)
    )
    truth = (
        [f"unrelated migration backup restore lifecycle {index}" for index in range(5)]
        if divergent_truth
        else [f"{topic_id} voltage current signal principle {index}" for index in range(5)]
    )
    write_json(
        pack / "fact_anchor.json",
        {
            "topic_id": topic_id,
            "anchors": anchors,
            "core_facts": core_facts or [],
        },
    )
    write_json(
        pack / "model_answer.json",
        {
            "topic_id": topic_id,
            "id": model_id or f"{topic_id}_PRINCIPLE_v1",
            "expected_question_patterns": [pattern],
            "question_examples": examples,
            "routing_aliases": routing,
            "topic_aliases": legacy_aliases,
        },
    )
    write_json(
        pack / "logic_check.json",
        {"topic_id": topic_id, "llm_profile": {"truth_schema": truth}},
    )
    write_json(pack / "topic_importance.json", {"topic_id": topic_id})
    if unmanaged_status:
        write_json(
            pack / "topic_status.json",
            {"schema_version": "topic_status.v1", "status": "draft"},
        )


class TopicPackAtomicityAuditTests(unittest.TestCase):
    def audit(self, root: Path):
        classification = root / "classification.md"
        classification.write_text(
            "\n".join(f"`{path.name}`" for path in root.iterdir() if path.is_dir()),
            encoding="utf-8",
        )
        return audit_topic_pack_inventory(root, classification_path=classification)

    def test_coherent_pack_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "packs"
            root.mkdir()
            make_pack(root, "coherent_topic")
            issues, summary = self.audit(root)
            self.assertEqual(summary["decision"], "PASS")
            self.assertFalse([issue for issue in issues if issue.severity == "ERROR"])

    def test_foreign_model_id_and_duplicate_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "packs"
            root.mkdir()
            make_pack(root, "first_topic", model_id="second_topic")
            make_pack(root, "second_topic", model_id="second_topic")
            issues, _ = self.audit(root)
            codes = {issue.code for issue in issues}
            self.assertIn("MODEL_ID_OWNER_MISMATCH", codes)
            self.assertIn("DUPLICATE_MODEL_ID", codes)

    def test_unscoped_string_pattern_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "packs"
            root.mkdir()
            make_pack(root, "string_topic", string_pattern=True)
            issues, _ = self.audit(root)
            self.assertIn("UNSCOPED_QUESTION_PATTERN", {issue.code for issue in issues})

    def test_unmanaged_status_metadata_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "packs"
            root.mkdir()
            make_pack(root, "stale_status_topic", unmanaged_status=True)
            issues, _ = self.audit(root)
            self.assertIn(
                "UNMANAGED_TOPIC_STATUS_METADATA",
                {issue.code for issue in issues},
            )

    def test_modern_legacy_mirror_divergence_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "packs"
            root.mkdir()
            make_pack(
                root,
                "mirror_topic",
                divergent_questions=True,
                divergent_aliases=True,
            )
            issues, _ = self.audit(root)
            codes = {issue.code for issue in issues}
            self.assertIn("QUESTION_MIRROR_DIVERGENCE", codes)
            self.assertIn("ALIAS_MIRROR_DIVERGENCE", codes)

    def test_truth_schema_divergence_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "packs"
            root.mkdir()
            make_pack(root, "truth_topic", divergent_truth=True)
            issues, _ = self.audit(root)
            self.assertIn("POSITIVE_EVIDENCE_DIVERGENCE", {issue.code for issue in issues})

    def test_duplicated_long_core_facts_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "packs"
            root.mkdir()
            shared = [
                "shared foreign fact " + str(index) + " " + ("evidence " * 15)
                for index in range(3)
            ]
            make_pack(root, "left_topic", core_facts=shared)
            make_pack(root, "right_topic", core_facts=shared)
            issues, _ = self.audit(root)
            self.assertIn("DUPLICATED_FOREIGN_CORE_FACTS", {issue.code for issue in issues})


class RepositoryAtomicityRegressionTests(unittest.TestCase):
    def load(self, topic_id: str, name: str) -> dict:
        return json.loads((PACK_ROOT / topic_id / name).read_text(encoding="utf-8"))

    def assert_fact_logic_projection(self, topic_id: str) -> None:
        fact = self.load(topic_id, "fact_anchor.json")
        logic = self.load(topic_id, "logic_check.json")
        statements = [row["statement"] for row in fact["anchors"]]
        self.assertEqual(fact["core_facts"], statements)
        self.assertEqual(logic["llm_profile"]["truth_schema"], statements)

    def test_inventory_has_no_unscoped_question_pattern(self) -> None:
        for path in PACK_ROOT.glob("*/model_answer.json"):
            model = json.loads(path.read_text(encoding="utf-8"))
            for row in model["expected_question_patterns"]:
                self.assertIsInstance(row, dict, path.parent.name)
                self.assertTrue(row.get("required_anchor_ids"), path.parent.name)

    def test_p0_fact_logic_mirrors_follow_local_owner(self) -> None:
        for topic_id in (
            "control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing",
            "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization",
            "nyquist_stability_criterion_gain_phase_margin",
            "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration",
        ):
            with self.subTest(topic_id=topic_id):
                self.assert_fact_logic_projection(topic_id)

    def test_nyquist_questions_do_not_contain_routh_artifacts(self) -> None:
        model = self.load("nyquist_stability_criterion_gain_phase_margin", "model_answer.json")
        text = json.dumps(model["expected_question_patterns"], ensure_ascii=False).casefold()
        for artifact in ("routh", "한 행 전체가 0", "실수부가 -α"):
            self.assertNotIn(artifact, text)

    def test_thermistor_positive_mirrors_do_not_claim_rtd_owner(self) -> None:
        topic_id = "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization"
        fact = self.load(topic_id, "fact_anchor.json")
        model = self.load(topic_id, "model_answer.json")
        logic = self.load(topic_id, "logic_check.json")
        positive = " ".join([
            fact["title_ko"],
            *fact["core_facts"],
            model["title_ko"],
            *(row["pattern"] for row in model["expected_question_patterns"]),
            logic["llm_profile"]["display_name"],
            *logic["llm_profile"]["truth_schema"],
        ]).casefold()
        self.assertNotIn("pt100", positive)
        self.assertNotIn("rtd 온도센서의 측정원리", positive)


if __name__ == "__main__":
    unittest.main(verbosity=2)
