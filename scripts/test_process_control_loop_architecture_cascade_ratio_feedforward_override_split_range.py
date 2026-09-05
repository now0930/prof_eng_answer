#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "process_control_loop_architecture_cascade_ratio_feedforward_override_split_range"
TOPIC_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
TOPIC_SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"

RELATED_TOPIC_IDS = {
    "feedback_system_closed_loop_sensitivity_steady_state_error",
    "pid_controller_tuning_sequence_gain_effects",
    "lqr_optimal_state_feedback_riccati_weighting_design",
    "state_feedback_reference_tracking_prefilter_integral_action",
    "state_space_controllability_observability_pole_placement",
    "control_valve_authority_rangeability_gain_installed_performance",
    "control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening",
}

REQUIRED_ANCHOR_IDS = {
    "process_loop_signal_chain",
    "single_loop_architecture",
    "cascade_structure",
    "cascade_secondary_faster",
    "cascade_disturbance_condition",
    "ratio_control_structure",
    "ratio_scaling_and_low_flow",
    "feedforward_principle",
    "feedforward_feedback_combination",
    "override_selective_control",
    "override_tracking_antiwindup",
    "split_range_control",
    "split_range_transition_design",
    "architecture_selection_criteria",
    "loop_interaction_coordination",
    "field_implementation_validation",
}

REQUIRED_FATAL_IDS = {
    "cascade_secondary_slower_is_better",
    "cascade_signal_direction_reversed",
    "cascade_extra_measurement_always_improves",
    "ratio_independent_setpoints",
    "feedforward_no_disturbance_measurement",
    "feedforward_makes_feedback_unnecessary",
    "override_averages_outputs",
    "override_high_selector_always_safe",
    "split_range_equals_override",
    "split_range_transition_automatic",
    "multiloop_complexity_always_better",
}

FORBIDDEN_BROAD_ALIASES = {
    "pid",
    "feedback",
    "control",
    "process control",
    "control valve",
    "valve",
    "state space",
    "lqr",
    "plc",
    "dcs",
    "scada",
}


def load_json(name: str) -> dict:
    return json.loads((TOPIC_DIR / name).read_text(encoding="utf-8"))


def normalize_alias(value: str) -> str:
    text = value.casefold().replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


class ProcessControlLoopArchitectureTopicTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_json("model_answer.json")
        cls.fact = load_json("fact_anchor.json")
        cls.logic = load_json("logic_check.json")
        cls.importance = load_json("topic_importance.json")
        cls.sheet = TOPIC_SHEET.read_text(encoding="utf-8")

    def test_schema_topic_id_and_question_type(self) -> None:
        expected_schema = {
            "model_answer": "topic_pack.model_answer.v1",
            "fact_anchor": "topic_pack.fact_anchor.v1",
            "logic_check": "topic_pack.logic_check.v1",
            "topic_importance": "topic_pack.topic_importance.v1",
        }
        objects = {
            "model_answer": self.model,
            "fact_anchor": self.fact,
            "logic_check": self.logic,
            "topic_importance": self.importance,
        }
        for name, obj in objects.items():
            self.assertEqual(obj["schema_version"], expected_schema[name])
            self.assertEqual(obj["topic_id"], TOPIC_ID)

        self.assertEqual(self.model["question_type"], "COMPARE_SELECTION")
        self.assertEqual(self.fact["question_type_hint"], "COMPARE_SELECTION")
        self.assertEqual(self.importance["question_type"], "COMPARE_SELECTION")
        self.assertEqual(self.importance["difficulty"], "THEORY_CORE")
        self.assertEqual(
            self.importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )

    def test_anchor_contract_and_importance_distribution(self) -> None:
        anchors = self.fact["anchors"]
        ids = [row["anchor_id"] for row in anchors]

        self.assertEqual(len(anchors), 16)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), REQUIRED_ANCHOR_IDS)

        for row in anchors:
            self.assertEqual(row["id"], row["anchor_id"])
            self.assertIn(
                row["importance"],
                {"core", "must", "important", "optional"},
            )
            self.assertTrue(row["statement"].strip())
            self.assertTrue(row["core_terms"])
            self.assertTrue(row["accepted_explanations"])
            self.assertTrue(row["rejected_explanations"])

        counts = Counter(row["importance"] for row in anchors)
        self.assertEqual(counts["must"], 12)
        self.assertEqual(counts["important"], 4)
        self.assertEqual(counts["core"], 0)
        self.assertEqual(counts["optional"], 0)

    def test_model_outline_anchor_refs_are_complete(self) -> None:
        anchor_ids = {row["anchor_id"] for row in self.fact["anchors"]}
        outline = self.model["recommended_outline"]

        self.assertEqual(len(outline), 8)

        referenced = set()
        for section in outline:
            self.assertTrue(section["section"].strip())
            self.assertTrue(section["intent"].strip())
            refs = section["anchor_refs"]
            self.assertTrue(refs)
            self.assertTrue(set(refs) <= anchor_ids)
            referenced.update(refs)

        self.assertEqual(referenced, anchor_ids)

    def test_cascade_semantic_contract(self) -> None:
        rows = {row["anchor_id"]: row["statement"] for row in self.fact["anchors"]}

        structure = rows["cascade_structure"]
        self.assertIn("primary(master) controller의 출력", structure)
        self.assertIn("secondary(slave) controller의 설정값", structure)
        self.assertIn("최종제어요소를 직접 조작", structure)

        speed = rows["cascade_secondary_faster"]
        self.assertIn("secondary loop가 primary loop보다 충분히 빠르게", speed)
        self.assertIn("특정 속도비", speed)

        disturbance = rows["cascade_disturbance_condition"]
        self.assertIn("primary PV보다 먼저 감지", disturbance)
        self.assertIn("자동으로 개선", disturbance)

    def test_ratio_semantic_contract(self) -> None:
        rows = {row["anchor_id"]: row["statement"] for row in self.fact["anchors"]}

        ratio = rows["ratio_control_structure"]
        self.assertIn("wild/master stream", ratio)
        self.assertIn("controlled-flow setpoint", ratio)
        self.assertIn("SP_c=R·F_w", ratio)

        low = rows["ratio_scaling_and_low_flow"]
        self.assertIn("단위·범위", low)
        self.assertIn("0에 가까운", low)
        self.assertIn("low-flow logic", low)

    def test_feedforward_semantic_contract(self) -> None:
        rows = {row["anchor_id"]: row["statement"] for row in self.fact["anchors"]}

        ff = rows["feedforward_principle"]
        self.assertIn("측정 가능한 외란", ff)
        self.assertIn("G_ff=-G_d/G_u", ff)
        self.assertIn("인과성", ff)
        self.assertIn("model uncertainty", ff)

        combo = rows["feedforward_feedback_combination"]
        self.assertIn("미측정 외란", combo)
        self.assertIn("모델오차", combo)
        self.assertIn("feedback", combo)

    def test_override_semantic_contract(self) -> None:
        rows = {row["anchor_id"]: row["statement"] for row in self.fact["anchors"]}

        override = rows["override_selective_control"]
        self.assertIn("high/low selector", override)
        self.assertIn("제한조건", override)

        tracking = rows["override_tracking_antiwindup"]
        self.assertIn("external reset feedback", tracking)
        self.assertIn("output tracking", tracking)
        self.assertIn("anti-windup", tracking)
        self.assertIn("bumpless transfer", tracking)

    def test_split_range_semantic_contract(self) -> None:
        rows = {row["anchor_id"]: row["statement"] for row in self.fact["anchors"]}

        split = rows["split_range_control"]
        self.assertIn("하나의 controller output", split)
        self.assertIn("둘 이상의 최종제어요소", split)

        transition = rows["split_range_transition_design"]
        self.assertIn("deadband", transition)
        self.assertIn("overlap", transition)
        self.assertIn("installed gain", transition)
        self.assertIn("transition test", transition)

    def test_fatal_contract_is_direct_and_unique(self) -> None:
        fatals = self.fact["fatal_wrong_claims"]
        ids = [row["id"] for row in fatals]

        self.assertEqual(len(fatals), 11)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), REQUIRED_FATAL_IDS)

        for row in fatals:
            self.assertIn("직접 주장", row["claim"])
            self.assertTrue(row["correction"].strip())

        self.assertFalse(self.logic["deterministic_checks"]["enabled"])
        self.assertEqual(
            self.logic["llm_profile"]["cap_policy"]["fatal_recommended_ceiling"],
            10.0,
        )

    def test_routing_aliases_are_specific_and_not_exact_cross_topic_duplicates(self) -> None:
        aliases = self.model["routing_aliases"]
        normalized = [normalize_alias(value) for value in aliases]

        self.assertEqual(len(normalized), len(set(normalized)))
        self.assertFalse(FORBIDDEN_BROAD_ALIASES & set(normalized))

        new_aliases = set(normalized)
        duplicate_rows: list[tuple[str, str]] = []

        pack_root = ROOT / "rubrics" / "topic_packs"
        for pack in pack_root.iterdir():
            if not pack.is_dir() or pack.name == TOPIC_ID:
                continue
            path = pack / "model_answer.json"
            if not path.exists():
                continue
            obj = json.loads(path.read_text(encoding="utf-8"))
            for alias in obj.get("routing_aliases", []):
                normalized_other = normalize_alias(alias)
                if normalized_other in new_aliases:
                    duplicate_rows.append((pack.name, alias))

        self.assertEqual(
            duplicate_rows,
            [],
            f"exact routing alias duplicates: {duplicate_rows}",
        )

    def test_related_topic_ownership_boundary_is_explicit(self) -> None:
        for topic_id in RELATED_TOPIC_IDS:
            self.assertIn(topic_id, self.sheet)

        self.assertIn("이 Topic의 직접 ownership", self.sheet)
        self.assertIn("기존 Topic ownership 유지", self.sheet)
        self.assertIn("PID P/I/D gain", self.sheet)
        self.assertIn("state-space", self.sheet)
        self.assertIn("valve authority", self.sheet)

    def test_field_selection_and_legacy_requirements_are_present(self) -> None:
        anchors = {row["anchor_id"]: row["statement"] for row in self.fact["anchors"]}

        selection = anchors["architecture_selection_criteria"]
        for token in (
            "외란의 측정 가능성",
            "내부 동특성의 속도",
            "안전·제약조건",
            "loop interaction",
            "비용",
            "기존 DCS/PLC",
        ):
            self.assertIn(token, selection)

        field = anchors["field_implementation_validation"]
        for token in (
            "anti-windup",
            "sensor failure",
            "startup/shutdown",
            "trend/step/disturbance test",
            "변경비용",
        ):
            self.assertIn(token, field)

    def test_topic_is_registered_as_theory_core_policy(self) -> None:
        self.assertEqual(
            self.importance.get("difficulty"),
            "THEORY_CORE",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
