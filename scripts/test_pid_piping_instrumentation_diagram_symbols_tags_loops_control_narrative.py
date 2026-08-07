#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
PID_CONTROLLER_TOPIC = "pid_controller_tuning_sequence_gain_effects"


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


def normalize_alias(value: str) -> str:
    text = value.casefold().replace("_", " ").replace("-", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


class TestPidPipingInstrumentationDiagramTopic(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.model = load("model_answer.json")
        cls.logic = load("logic_check.json")
        cls.importance = load("topic_importance.json")
        cls.anchors = cls.fact["anchors"]
        cls.anchor_by_id = {row["id"]: row for row in cls.anchors}

    def test_identity_and_classification(self) -> None:
        self.assertEqual(self.fact["topic_id"], TOPIC_ID)
        self.assertEqual(self.model["topic_id"], TOPIC_ID)
        self.assertEqual(self.logic["topic_id"], TOPIC_ID)
        self.assertEqual(self.importance["topic_id"], TOPIC_ID)
        self.assertEqual(
            self.model["question_type"],
            "IMPLEMENTATION_EVALUATION",
        )
        self.assertEqual(
            self.fact["question_type_hint"],
            "IMPLEMENTATION_EVALUATION",
        )
        self.assertEqual(
            self.importance["question_type"],
            "IMPLEMENTATION_EVALUATION",
        )
        self.assertEqual(
            self.importance["difficulty"],
            "DESIGN_EVALUATION",
        )
        self.assertEqual(
            self.importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )

    def test_anchor_inventory_and_importance(self) -> None:
        ids = [row["id"] for row in self.anchors]
        self.assertEqual(len(ids), 24)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            sum(row["importance"] == "must" for row in self.anchors),
            19,
        )
        self.assertEqual(
            sum(row["importance"] == "important" for row in self.anchors),
            5,
        )
        self.assertTrue(
            all(row["id"] == row["anchor_id"] for row in self.anchors)
        )

    def test_pid_is_piping_instrumentation_not_controller_tuning(self) -> None:
        scope = self.anchor_by_id["pid_definition_scope"]["statement"]
        boundary = self.anchor_by_id["pid_not_pid_controller"]["statement"]
        self.assertIn("Piping and Instrumentation Diagram", scope)
        self.assertIn("배관계장도", scope)
        self.assertIn("PID 제어기", boundary)
        self.assertIn("구분", boundary)
        self.assertIn("bare PID", boundary)

    def test_pfd_and_layout_boundaries(self) -> None:
        pfd = self.anchor_by_id["pfd_pid_difference"]["statement"]
        layout = self.anchor_by_id["pid_not_physical_layout"]["statement"]
        self.assertIn("PFD", pfd)
        self.assertIn("상세도", pfd)
        self.assertIn("layout", layout)
        self.assertIn("축척", layout)
        self.assertIn("별도 문서", layout)

    def test_tag_loop_symbol_and_legend_contract(self) -> None:
        tag = self.anchor_by_id["instrument_tag_function_letters"]["statement"]
        loop = self.anchor_by_id["loop_number_identity"]["statement"]
        symbol = self.anchor_by_id[
            "instrument_symbol_location_convention"
        ]["statement"]
        legend = self.anchor_by_id[
            "legend_project_convention_priority"
        ]["statement"]
        self.assertIn("측정변수", tag)
        self.assertIn("기능", tag)
        self.assertIn("loop", tag)
        self.assertIn("numbering convention", loop)
        self.assertIn("field", symbol)
        self.assertIn("control room", symbol)
        self.assertIn("legend", legend)
        self.assertIn("engineering specification", legend)

    def test_signal_line_is_not_universal_symbol_claim(self) -> None:
        text = self.anchor_by_id["signal_line_legend"]["statement"]
        self.assertIn("pneumatic", text)
        self.assertIn("electrical", text)
        self.assertIn("data", text)
        self.assertIn("보편적 의미를 단정하지 않고", text)
        self.assertIn("legend", text)

    def test_measurement_feedback_and_final_element_chain(self) -> None:
        measurement = self.anchor_by_id["measurement_loop_chain"]["statement"]
        feedback = self.anchor_by_id[
            "feedback_control_loop_chain"
        ]["statement"]
        valve = self.anchor_by_id[
            "control_valve_pid_representation"
        ]["statement"]
        self.assertIn("process tapping", measurement)
        self.assertIn("transmitter", measurement)
        self.assertIn("controller", feedback)
        self.assertIn("final control element", feedback)
        self.assertIn("actuator", valve)
        self.assertIn("positioner", valve)
        self.assertIn("fail action", valve)

    def test_related_document_ownership_boundaries(self) -> None:
        alarm = self.anchor_by_id["alarm_trip_interlock_boundary"]["statement"]
        loop = self.anchor_by_id["pid_loop_diagram_relation"]["statement"]
        logic = self.anchor_by_id["pid_logic_diagram_relation"]["statement"]
        narrative = self.anchor_by_id[
            "pid_control_narrative_relation"
        ]["statement"]
        self.assertIn("Cause & Effect", alarm)
        self.assertIn("logic diagram", alarm)
        self.assertIn("배선", loop)
        self.assertIn("I/O channel", loop)
        self.assertIn("interlock", logic)
        self.assertIn("Control narrative", narrative)
        self.assertIn("운전 의도", narrative)

    def test_cross_document_consistency(self) -> None:
        idx = self.anchor_by_id[
            "pid_instrument_index_io_relation"
        ]["statement"]
        line = self.anchor_by_id["pid_line_list_spec_relation"]["statement"]
        review = self.anchor_by_id[
            "design_review_cross_document_consistency"
        ]["statement"]
        self.assertIn("Instrument Index", idx)
        self.assertIn("I/O List", idx)
        self.assertIn("Line List", line)
        self.assertIn("piping class", line)
        self.assertIn("PFD", review)
        self.assertIn("Cause & Effect", review)
        self.assertIn("정합성", review)

    def test_revision_moc_walkdown_asbuilt_lifecycle(self) -> None:
        moc = self.anchor_by_id[
            "revision_moc_document_control"
        ]["statement"]
        field = self.anchor_by_id[
            "field_verification_asbuilt"
        ]["statement"]
        lifecycle = self.anchor_by_id["pid_lifecycle_use"]["statement"]
        self.assertIn("revision", moc)
        self.assertIn("MOC", moc)
        self.assertIn("as-built", moc)
        self.assertIn("walkdown", field)
        self.assertIn("redline", field)
        self.assertIn("commissioning", lifecycle)

    def test_fatal_and_safe_contract(self) -> None:
        fatal_ids = {
            row["id"] for row in self.fact["fatal_wrong_claims"]
        }
        self.assertEqual(len(fatal_ids), 12)
        self.assertIn("pid_equals_pfd", fatal_ids)
        self.assertIn("pid_equals_pid_controller", fatal_ids)
        self.assertIn("dashed_line_always_electrical", fatal_ids)
        self.assertIn("informal_redline_is_asbuilt", fatal_ids)
        self.assertEqual(len(self.fact["safe_expressions"]), 14)

    def test_expected_patterns_and_outline_references(self) -> None:
        anchor_ids = set(self.anchor_by_id)
        patterns = self.model["expected_question_patterns"]
        outline = self.model["recommended_outline"]
        self.assertEqual(len(patterns), 10)
        self.assertEqual(len(outline), 8)
        for row in patterns:
            self.assertTrue(set(row["required_anchor_ids"]) <= anchor_ids)
        covered = set()
        for row in outline:
            refs = set(row["anchor_refs"])
            self.assertTrue(refs <= anchor_ids)
            covered |= refs
        self.assertEqual(covered, anchor_ids)

    def test_logic_check_is_semantic_only_and_aliases_match(self) -> None:
        det = self.logic["deterministic_checks"]
        profile = self.logic["llm_profile"]
        self.assertFalse(det["enabled"])
        self.assertEqual(det["fatal_checks"], [])
        self.assertEqual(det["major_checks"], [])
        self.assertEqual(det["question_type_checks"], [])
        self.assertEqual(
            det["topic_aliases"],
            self.model["routing_aliases"],
        )
        self.assertTrue(profile["enabled"])
        self.assertFalse(
            profile["score_policy"]["direct_score_application"]
        )
        self.assertEqual(
            profile["score_policy"]["affected_layers"],
            ["C"],
        )
        self.assertEqual(len(profile["truth_schema"]), 24)
        self.assertEqual(len(profile["fatal_conditions"]), 12)
        self.assertEqual(len(profile["major_checks"]), 10)

    def test_pand_id_aliases_are_disambiguated_and_unique(self) -> None:
        aliases = self.model["routing_aliases"]
        normalized = [normalize_alias(value) for value in aliases]
        self.assertEqual(len(aliases), 18)
        self.assertEqual(len(normalized), len(set(normalized)))
        self.assertNotIn("pid", set(normalized))
        for alias in aliases:
            lower = alias.casefold()
            self.assertTrue(
                "p&id" in lower
                or "piping" in lower
                or "배관" in alias
                or "계장도" in alias,
                alias,
            )

    def test_no_exact_normalized_alias_collision_with_pid_controller(self) -> None:
        other_path = (
            ROOT
            / "rubrics"
            / "topic_packs"
            / PID_CONTROLLER_TOPIC
            / "model_answer.json"
        )
        other = json.loads(other_path.read_text(encoding="utf-8"))
        ours = {
            normalize_alias(value)
            for value in self.model["routing_aliases"]
        }
        theirs = {
            normalize_alias(value)
            for value in other["routing_aliases"]
        }
        self.assertFalse(ours & theirs)
        self.assertNotIn("pid", ours)

    def test_question_type_taxonomy_remains_existing_value(self) -> None:
        self.assertEqual(
            self.model["question_type"],
            "IMPLEMENTATION_EVALUATION",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
