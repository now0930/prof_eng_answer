#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOPIC = 'control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing'
SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"

EXPECTED_ANCHOR_IDS = ['maintenance_scope_boundary', 'work_permit_isolation_depressurization', 'as_found_condition_record', 'symptom_failure_mode_triage', 'external_cause_elimination', 'controlled_removal_marking', 'disassembly_sequence_traceability', 'cleaning_contamination_control', 'trim_stem_guide_body_inspection', 'dimensional_acceptance_criteria', 'repair_replace_lapping_decision', 'packing_gasket_seal_restoration', 'reassembly_alignment_torque', 'seat_endpoint_travel_restoration', 'pressure_boundary_test', 'seat_leakage_test', 'stroke_friction_hysteresis_test', 'fail_action_accessory_function_test', 'root_cause_evidence_handoff', 'return_to_service_as_left_record']
EXPECTED_FATAL_IDS = ['maintenance_without_isolation', 'as_left_only_sufficient', 'packing_tightening_always_solves_leakage', 'lapping_always_restores_seat', 'pressure_test_proves_all_leakage', 'seat_test_proves_external_tightness', 'positioner_calibration_equals_overhaul', 'replace_parts_without_failure_evidence', 'reuse_gasket_packing_unconditionally', 'fail_action_visual_check_only', 'mechanical_stop_used_for_seat_load', 'return_service_without_final_walkdown']
EXPECTED_MAJOR_IDS = ['fixed_overhaul_interval', 'fixed_lapping_allowance', 'fixed_packing_preload', 'fixed_pressure_test_value', 'fixed_leak_test_condition', 'fixed_stroke_acceptance', 'replace_all_trim_by_default', 'external_causes_ignored', 'no_specialist_handoff', 'maintenance_record_without_conditions']
EXPECTED_ALIASES = ['control valve maintenance inspection overhaul testing', 'control valve troubleshooting repair reassembly', 'control valve disassembly inspection reassembly sequence', 'control valve overhaul procedure', 'control valve maintenance procedure', 'control valve post maintenance testing', 'control valve pressure leak stroke test', 'control valve repair replace lapping decision', 'control valve as found as left maintenance record', 'control valve 반복고장 원인분석', '제어밸브 정비 절차', '제어밸브 점검 분해 조립 시험', '제어밸브 overhaul', '제어밸브 고장진단', '제어밸브 정비 후 시험', '제어밸브 누설 stroke fail action 시험']

HANDOFF_TOPIC_IDS = (
    'control_system_operations_maintenance_calibration_inspection_spares_kpi',
    'control_valve_positioner_ip_converter_booster_accessories_calibration',
    'control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions',
    'control_valve_selection_process_pressure_temperature_flow_media_lifecycle',
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def generated_target(
    filename: str,
    list_key: str,
) -> dict[str, Any] | None:
    path = GENERATED_DIR / filename
    if not path.is_file():
        return None
    rows = load_json(path).get(list_key, [])
    matches = [
        row
        for row in rows
        if isinstance(row, dict) and row.get("topic_id") == TOPIC
    ]
    if not matches:
        return None
    if len(matches) != 1:
        raise AssertionError(
            f"{filename} target count={len(matches)}"
        )
    return matches[0]


def handoff_registry_matches(
    points: list[Any],
    topic_id: str,
) -> list[Any]:
    pattern = re.compile(
        rf"^\s*`?{re.escape(topic_id)}`?\s+hand-off\b",
        re.IGNORECASE,
    )
    return [
        point
        for point in points
        if pattern.search(str(point))
    ]


class SourceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.readme = (SOURCE_DIR / "README.md").read_text(
            encoding="utf-8"
        )
        cls.fact = load_json(SOURCE_DIR / "fact_anchor.json")
        cls.logic = load_json(SOURCE_DIR / "logic_check.json")
        cls.model = load_json(SOURCE_DIR / "model_answer.json")
        cls.importance = load_json(
            SOURCE_DIR / "topic_importance.json"
        )

    def test_required_files_and_identity(self) -> None:
        expected_files = {
            "README.md",
            "fact_anchor.json",
            "logic_check.json",
            "model_answer.json",
            "topic_importance.json",
        }
        self.assertEqual(
            {path.name for path in SOURCE_DIR.iterdir()},
            expected_files,
        )
        for payload in (
            self.fact,
            self.logic,
            self.model,
            self.importance,
        ):
            self.assertEqual(payload["topic_id"], TOPIC)
        self.assertEqual(
            self.model["question_type"],
            "IMPLEMENTATION_EVALUATION",
        )
        self.assertEqual(
            self.importance["question_type"],
            "IMPLEMENTATION_EVALUATION",
        )

    def test_anchor_and_fatal_contract(self) -> None:
        anchors = self.fact["anchors"]
        self.assertEqual(
            [row["id"] for row in anchors],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(
            [row["anchor_id"] for row in anchors],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(len(anchors), 20)
        for row in anchors:
            self.assertEqual(row["statement"], row["claim"])
            self.assertIn(row["statement"], row["keywords"])
            self.assertIn(row["id"], row["core_terms"])
            self.assertTrue(row["accepted_explanations"])
            self.assertTrue(row["rejected_explanations"])
        fatal = self.fact["fatal_wrong_claims"]
        self.assertEqual(
            [row["id"] for row in fatal],
            EXPECTED_FATAL_IDS,
        )

    def test_model_answer_contract(self) -> None:
        patterns = self.model["expected_question_patterns"]
        outlines = self.model["recommended_outline"]
        aliases = self.model["routing_aliases"]
        points = self.model["routing_field_points"]
        anchor_set = set(EXPECTED_ANCHOR_IDS)
        self.assertEqual(len(patterns), 6)
        self.assertEqual(len(outlines), 8)
        self.assertEqual(aliases, EXPECTED_ALIASES)
        self.assertEqual(len(aliases), 16)
        self.assertTrue(
            all(
                set(row["required_anchor_ids"]) <= anchor_set
                for row in patterns
            )
        )
        self.assertTrue(
            all(
                set(row["anchor_refs"]) <= anchor_set
                for row in outlines
            )
        )
        covered = set().union(
            *(
                set(row["required_anchor_ids"])
                for row in patterns
            )
        )
        self.assertEqual(covered, anchor_set)
        for topic_id in HANDOFF_TOPIC_IDS:
            self.assertEqual(
                len(handoff_registry_matches(points, topic_id)),
                1,
            )

    def test_logic_profile_contract(self) -> None:
        deterministic = self.logic["deterministic_checks"]
        profile = self.logic["llm_profile"]
        self.assertFalse(deterministic["enabled"])
        self.assertEqual(
            deterministic["question_type"],
            "IMPLEMENTATION_EVALUATION",
        )
        terms = (
            profile.get("candidate_extraction") or {}
        ).get("key_terms") or []
        term_text = "\n".join(str(term) for term in terms)
        for anchor_id in EXPECTED_ANCHOR_IDS:
            self.assertIn(anchor_id, term_text)
        self.assertNotIn("fatal_checks", profile)
        major = profile.get("major_checks") or []
        self.assertEqual(
            [row["id"] for row in major],
            EXPECTED_MAJOR_IDS,
        )

    def test_boundary_and_readme_contract(self) -> None:
        corpus = "\n".join([
            self.readme,
            json.dumps(self.fact, ensure_ascii=False),
            json.dumps(self.logic, ensure_ascii=False),
            json.dumps(self.model, ensure_ascii=False),
            json.dumps(self.importance, ensure_ascii=False),
        ])
        for topic_id in HANDOFF_TOPIC_IDS:
            self.assertIn(topic_id, corpus)
        self.assertNotRegex(
            corpus,
            r"Topic\s+(?:1[0-9]|[1-9])\s+hand-off",
        )
        for marker in (
            "작업허가",
            "as-found",
            "분해",
            "repair",
            "reassembly",
            "pressure",
            "seat leakage",
            "stroke",
            "fail-action",
            "as-left",
        ):
            self.assertIn(marker.casefold(), corpus.casefold())

    def test_importance_contract(self) -> None:
        self.assertEqual(
            self.importance["difficulty"],
            "FIELD_APPLICATION",
        )
        self.assertEqual(
            self.importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )
        self.assertEqual(
            len(self.importance["high_band_unlock_conditions"]),
            8,
        )


class GeneratedProjectionTests(unittest.TestCase):
    def test_generated_projection_when_available(self) -> None:
        targets = {
            "fact": generated_target(
                "fact_anchors.generated.json",
                "topics",
            ),
            "profile": generated_target(
                "logic_check_profiles.generated.json",
                "profiles",
            ),
            "logic": generated_target(
                "logic_checks.generated.json",
                "topic_logic_checks",
            ),
            "model": generated_target(
                "model_answers.generated.json",
                "answers",
            ),
            "importance": generated_target(
                "topic_importance.generated.json",
                "topics",
            ),
            "manifest": generated_target(
                "topic_pack_manifest.generated.json",
                "topics",
            ),
        }
        if any(value is None for value in targets.values()):
            self.skipTest("generated rebuild pending")
        self.assertEqual(
            [row["id"] for row in targets["fact"]["anchors"]],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(
            [
                row["id"]
                for row in targets["fact"]["fatal_wrong_claims"]
            ],
            EXPECTED_FATAL_IDS,
        )
        self.assertNotIn("fatal_checks", targets["profile"])
        self.assertEqual(
            [
                row["id"]
                for row in (
                    targets["profile"].get("major_checks") or []
                )
            ],
            EXPECTED_MAJOR_IDS,
        )
        self.assertEqual(
            targets["model"]["routing_aliases"],
            EXPECTED_ALIASES,
        )
        self.assertEqual(
            len(targets["model"]["expected_question_patterns"]),
            6,
        )
        self.assertEqual(
            len(targets["model"]["recommended_outline"]),
            8,
        )
        self.assertEqual(
            targets["importance"]["question_type"],
            "IMPLEMENTATION_EVALUATION",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
