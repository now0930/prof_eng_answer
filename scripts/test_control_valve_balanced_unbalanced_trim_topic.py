#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logic_llm_verifier import (
    extract_logic_evidence_candidates,
    verify_logic_with_llm,
)
from model_answer_router import find_model_answer_reference

TOPIC = 'balanced_trim_unbalanced_trim_structure_sealing_applications'
TOPIC_1 = 'control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe'
TOPIC_2 = 'control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening'
TOPIC_3 = 'control_valve_deadband_stiction_response_time_positioner_dynamic_performance'
TOPIC_4 = 'control_valve_types_globe_rotary_body_actuator_selection'
TOPIC_5 = 'control_valve_authority_rangeability_gain_installed_performance'
TOPIC_6 = 'control_valve_sizing_cv_kv_reynolds_liquid_selection'
TOPIC_7 = 'control_valve_gas_sizing_choked_flow_critical_pressure_ratio'
TOPIC_8 = 'control_valve_cavitation_flashing_choked_flow_damage_prevention'
TOPIC_9 = 'control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim'

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"

EXPECTED_ANCHOR_IDS = ['control_valve_balanced_unbalanced_scope', 'trim_pressure_boundary_terms', 'unbalanced_trim_direct_pressure_loading', 'effective_unbalanced_area', 'nominal_seat_area_boundary', 'unbalanced_force_equation', 'force_direction_sign_convention', 'balanced_trim_pressure_communication', 'balance_hole_passage_function', 'balanced_trim_residual_force', 'residual_effective_area', 'ideal_full_balance_boundary', 'force_reduction_ratio_conditional', 'cage_guided_balanced_plug_structure', 'balance_seal_function', 'balance_seal_loading', 'balance_seal_friction', 'breakaway_running_friction_boundary', 'balance_seal_leakage_path', 'seat_leakage_path_boundary', 'pressure_equalization_transient', 'passage_plugging_dynamic_imbalance', 'flow_direction_geometry_dependency', 'seat_load_shutoff_margin_boundary', 'actuator_sizing_topic1_handoff', 'dynamic_friction_topic3_handoff', 'body_cage_guide_topic4_handoff', 'low_noise_trim_topic9_boundary', 'leakage_packing_topic13_boundary', 'severe_service_material_topic14_boundary', 'clean_high_dp_large_size_application', 'dirty_slurry_particulate_limit', 'high_temperature_cryogenic_seal_limit', 'fluid_compatibility_seal_degradation', 'operating_case_force_matrix', 'vendor_cutaway_force_table_crosscheck']
EXPECTED_FATAL_IDS = ['control_valve_balanced_unbalanced_same_structure', 'control_valve_balanced_trim_zero_force_all_cases', 'control_valve_nominal_seat_area_always_effective_area', 'control_valve_balance_holes_instant_complete_equalization', 'control_valve_balance_seal_same_as_seat_seal', 'control_valve_balance_leakage_equals_seat_leakage', 'control_valve_balanced_trim_no_seal_friction', 'control_valve_seal_friction_assists_motion', 'control_valve_flow_to_open_universal_force_sign', 'control_valve_unbalanced_trim_never_high_dp', 'control_valve_balanced_trim_required_all_high_dp', 'control_valve_balanced_trim_always_lower_seat_leakage', 'control_valve_balanced_trim_eliminates_cavitation_noise', 'control_valve_balanced_trim_needs_no_actuator_margin', 'control_valve_balance_chamber_dynamics_irrelevant', 'control_valve_passage_plugging_no_force_effect', 'control_valve_any_seal_all_temperature_fluids', 'control_valve_balanced_trim_no_maintenance', 'control_valve_single_normal_case_sufficient', 'control_valve_residual_force_ignored_in_actuator_input']
EXPECTED_MAJOR_IDS = ['control_valve_fixed_actuator_reduction_percentage', 'control_valve_fixed_residual_area_ratio', 'control_valve_fixed_balance_seal_friction_coefficient', 'control_valve_fixed_seal_temperature_pressure_limit', 'control_valve_fixed_particle_size_limit', 'control_valve_fixed_leakage_class_by_trim_type', 'control_valve_fixed_flow_direction_force_sign', 'control_valve_fixed_balance_hole_geometry', 'control_valve_vendor_force_table_without_basis']

BROAD_ALIASES = {
    "balanced",
    "unbalanced",
    "trim",
    "seal",
    "plug",
    "cage",
    "force",
    "pressure",
    "leakage",
    "flow-to-open",
    "flow-to-close",
}

POSITIVE_ANSWER = """
Balanced trim과 unbalanced trim을 structure와 pressure boundary로 비교한다.
Unbalanced trim은 differential pressure가 effective unbalanced area에
작용하므로 Fu equals delta P times Au로 평가한다. Nominal seat area와
effective area를 구분한다. Balanced trim은 balance hole과 pressure
communication path를 사용하지만 residual effective area가 남을 수
있으므로 Fr equals delta P times Ar로 평가한다. Positive stem axis와
actual pressure geometry로 force sign을 정한다. Cage guided balanced
plug, balance chamber와 balance seal을 설명한다. Balance seal과 seat
seal을 구분하고 balance seal leakage와 seat leakage를 별도 path로
평가한다. Balance seal friction은 plug motion을 반대하며 breakaway
friction과 running friction을 구분한다. Rapid stroke의 pressure
equalization transient와 dirty service의 balance passage plugging을
검토한다. Clean high differential pressure, dirty particulate, high
temperature와 cryogenic service를 비교한다. Minimum normal maximum과
startup shutdown force matrix를 작성한다. Topic 1 actuator sizing,
Topic 3 dynamic friction, Topic 4 general body cage, Topic 9 low noise trim,
Topic 13 seat leakage packing, Topic 14 severe service material과 Topic 16
package workflow 경계를 유지한다. Vendor cutaway, effective area force
table, seal limit와 maintenance data를 crosscheck한다.
""".strip()

SAFE_ANSWER = """
Balanced trim은 pressure communication path를 사용하지만 residual
effective area와 residual force가 남을 수 있다. Effective unbalanced
area와 nominal seat area를 구분한다. Balance seal과 seat seal,
balance seal leakage와 seat leakage를 분리한다. Seal friction은 motion을
반대하며 passage plugging과 pressure equalization transient를 검토한다.
""".strip()

NEGATIVE_SAMPLES = {
    "control_valve_balanced_trim_zero_force_all_cases": (
        "balanced trim, residual force, residual effective area, ideal full "
        "balance와 pressure communication을 설명하지만 모든 pressure, "
        "travel과 transient에서 force가 정확히 zero라고 주장한다."
    ),
    "control_valve_nominal_seat_area_always_effective_area": (
        "effective unbalanced area, nominal seat area, pressure field, net "
        "axial force와 equivalent projected area를 설명하지만 두 면적은 "
        "항상 동일하다고 주장한다."
    ),
    "control_valve_balance_seal_same_as_seat_seal": (
        "balance seal function, balance chamber boundary, seat seal, pressure "
        "boundary와 seal ring을 설명하지만 balance seal과 seat seal은 "
        "같은 위치와 기능이라고 주장한다."
    ),
    "control_valve_seal_friction_assists_motion": (
        "balance seal friction, plug motion, actuator force input, seal drag와 "
        "breakaway friction을 설명하지만 friction은 항상 motion을 "
        "돕는다고 주장한다."
    ),
    "control_valve_passage_plugging_no_force_effect": (
        "balance passage plugging, pressure communication loss, residual force "
        "change, dynamic imbalance와 particulate를 설명하지만 plugging은 "
        "force와 response에 영향이 없다고 주장한다."
    ),
    "control_valve_residual_force_ignored_in_actuator_input": (
        "residual pressure force, balance seal friction, seat load, spring "
        "force, actuator inputs와 shutoff margin을 설명하지만 residual "
        "force와 seal friction은 actuator input에서 무시한다고 주장한다."
    ),
}

SEMANTIC_CLUSTERS = {
    "structure": (
        "balanced trim",
        "unbalanced trim",
        "pressure boundary",
    ),
    "force": (
        "effective unbalanced area",
        "fu equals delta p times au",
        "fr equals delta p times ar",
    ),
    "balance": (
        "balance hole",
        "pressure communication path",
        "residual effective area",
    ),
    "seal": (
        "balance seal",
        "seat seal",
        "balance seal leakage",
        "seat leakage",
    ),
    "friction": (
        "seal friction",
        "plug motion을 반대",
        "breakaway friction",
        "running friction",
    ),
    "dynamic": (
        "pressure equalization transient",
        "balance passage plugging",
    ),
    "application": (
        "clean high differential pressure",
        "dirty particulate",
        "high temperature",
        "cryogenic",
    ),
    "cases": (
        "minimum normal maximum",
        "startup shutdown",
    ),
    "handoffs": (
        "topic 1",
        "topic 3",
        "topic 4",
        "topic 9",
        "topic 13",
        "topic 14",
        "topic 16",
    ),
    "verification": (
        "vendor cutaway",
        "effective area force table",
        "seal limit",
        "maintenance data",
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def target_entry(
    filename: str,
    list_key: str,
) -> dict[str, Any]:
    rows = load_json(GENERATED_DIR / filename).get(
        list_key,
        [],
    )
    matches = [
        row
        for row in rows
        if (
            isinstance(row, dict)
            and row.get("topic_id") == TOPIC
        )
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"{filename} target count={len(matches)}"
        )
    return matches[0]


def selected_topic(
    result: dict[str, Any],
) -> str | None:
    primary = result.get("primary_reference") or {}
    return (
        primary.get("topic_id")
        if isinstance(primary, dict)
        else None
    )


def pressure_force(
    delta_p: float,
    area: float,
) -> float:
    if delta_p < 0 or area < 0:
        raise ValueError
    return delta_p * area


def signed_force(
    delta_p: float,
    area: float,
    sign: int,
) -> float:
    if sign not in {-1, 1}:
        raise ValueError
    return sign * pressure_force(
        delta_p,
        area,
    )


def force_ratio(
    delta_p: float,
    residual_area: float,
    unbalanced_area: float,
) -> float:
    if unbalanced_area <= 0:
        raise ValueError
    fu = pressure_force(
        delta_p,
        unbalanced_area,
    )
    fr = pressure_force(
        delta_p,
        residual_area,
    )
    if fu == 0:
        raise ValueError
    return fr / fu


def seal_friction(
    magnitude: float,
    velocity: float,
) -> float:
    if magnitude < 0:
        raise ValueError
    if velocity > 0:
        return -magnitude
    if velocity < 0:
        return magnitude
    return 0.0


def actuator_components(
    pressure: float,
    seat: float,
    packing: float,
    balance_seal: float,
    spring: float,
    margin: float,
) -> float:
    return (
        pressure
        + seat
        + packing
        + balance_seal
        + spring
        + margin
    )


def cluster_coverage(
    text: str,
) -> dict[str, bool]:
    normalized = " ".join(
        text.casefold().split()
    )
    return {
        group: all(
            " ".join(
                marker.casefold().split()
            ) in normalized
            for marker in markers
        )
        for group, markers
        in SEMANTIC_CLUSTERS.items()
    }


def matched_profile_key_terms(
    text: str,
    profile: dict[str, Any],
) -> list[str]:
    normalized = " ".join(
        text.casefold().split()
    )
    terms = (
        (profile.get("candidate_extraction") or {})
        .get("key_terms")
        or []
    )
    return [
        str(term)
        for term in terms
        if " ".join(
            str(term).casefold().split()
        ) in normalized
    ]


class GeneratedContractRegressionTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json(
            SOURCE_DIR / "fact_anchor.json"
        )
        cls.logic = load_json(
            SOURCE_DIR / "logic_check.json"
        )
        cls.model = load_json(
            SOURCE_DIR / "model_answer.json"
        )
        cls.importance = load_json(
            SOURCE_DIR / "topic_importance.json"
        )
        cls.gfact = target_entry(
            "fact_anchors.generated.json",
            "topics",
        )
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.glogic = target_entry(
            "logic_checks.generated.json",
            "topic_logic_checks",
        )
        cls.gmodel = target_entry(
            "model_answers.generated.json",
            "answers",
        )
        cls.gimportance = target_entry(
            "topic_importance.generated.json",
            "topics",
        )
        cls.manifest = target_entry(
            "topic_pack_manifest.generated.json",
            "topics",
        )

    def test_source_generated_and_dynamic_manifest_alignment(
        self,
    ) -> None:
        for row in (
            self.fact,
            self.logic,
            self.model,
            self.importance,
            self.gfact,
            self.profile,
            self.glogic,
            self.gmodel,
            self.gimportance,
            self.manifest,
        ):
            self.assertEqual(
                row["topic_id"],
                TOPIC,
            )
        source_ids = sorted(
            path.name
            for path in (
                ROOT / "rubrics" / "topic_packs"
            ).iterdir()
            if (
                path.is_dir()
                and not path.name.startswith(".")
            )
        )
        manifest_ids = [
            row["topic_id"]
            for row in load_json(
                GENERATED_DIR
                / "topic_pack_manifest.generated.json"
            )["topics"]
        ]
        self.assertEqual(
            manifest_ids,
            source_ids,
        )
        self.assertEqual(
            manifest_ids.count(TOPIC),
            1,
        )

    def test_exact_anchor_fatal_major_contract(
        self,
    ) -> None:
        self.assertEqual(
            [
                row["id"]
                for row in self.fact["anchors"]
            ],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(
            [
                row["id"]
                for row in self.gfact["anchors"]
            ],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(
            [
                row["id"]
                for row
                in self.fact["fatal_wrong_claims"]
            ],
            EXPECTED_FATAL_IDS,
        )
        self.assertEqual(
            [
                row["id"]
                for row
                in self.profile["major_checks"]
            ],
            EXPECTED_MAJOR_IDS,
        )
        self.assertEqual(
            len(
                self.profile[
                    "fatal_conditions"
                ]
            ),
            20,
        )

    def test_semantic_score_and_deterministic_policy(
        self,
    ) -> None:
        self.assertFalse(
            self.glogic["enabled"]
        )
        self.assertEqual(
            self.glogic["fatal_checks"],
            [],
        )
        self.assertEqual(
            self.glogic["major_checks"],
            [],
        )
        self.assertEqual(
            self.profile[
                "candidate_extraction"
            ]["rules"],
            [],
        )
        policy = self.profile["score_policy"]
        self.assertFalse(
            policy["direct_score_application"]
        )
        self.assertIsNone(
            policy["recommended_ceiling"]
        )
        self.assertEqual(
            policy["direct_d_e_effect"],
            "none",
        )
        self.assertEqual(
            policy["affected_layers"],
            ["C"],
        )
        self.assertEqual(
            self.profile["output_contract"][
                "excluded_score_layers"
            ],
            ["D", "E"],
        )

    def test_patterns_outline_aliases_and_importance(
        self,
    ) -> None:
        patterns = self.model[
            "expected_question_patterns"
        ]
        outlines = self.model[
            "recommended_outline"
        ]
        self.assertEqual(len(patterns), 10)
        self.assertEqual(len(outlines), 8)
        anchors = set(EXPECTED_ANCHOR_IDS)
        self.assertTrue(
            all(
                set(
                    row[
                        "required_anchor_ids"
                    ]
                )
                <= anchors
                for row in patterns
            )
        )
        self.assertEqual(
            set().union(
                *(
                    set(row["anchor_refs"])
                    for row in outlines
                )
            ),
            anchors,
        )
        aliases = self.model[
            "routing_aliases"
        ]
        self.assertFalse(
            BROAD_ALIASES & set(aliases)
        )
        self.assertEqual(
            self.gmodel["topic_aliases"],
            aliases,
        )
        self.assertEqual(
            self.gmodel["routing_aliases"],
            aliases,
        )
        self.assertEqual(
            self.gimportance,
            self.importance,
        )
        self.assertEqual(
            self.importance["difficulty"],
            "FIELD_APPLICATION",
        )
        self.assertEqual(
            self.importance["question_type"],
            "COMPARE_SELECTION",
        )

    def test_force_area_marker_contracts(
        self,
    ) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        self.assertIn(
            "Fu=ΔP·Au",
            by_id["unbalanced_force_equation"],
        )
        self.assertIn(
            "Fr=ΔP·Ar",
            by_id["residual_effective_area"],
        )
        self.assertIn(
            "|Fr|/|Fu|=Ar/Au",
            by_id[
                "force_reduction_ratio_conditional"
            ],
        )
        self.assertIn(
            "positive stem axis",
            by_id[
                "force_direction_sign_convention"
            ],
        )

    def test_balance_structure_marker_contracts(
        self,
    ) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        self.assertIn(
            "pressure communication path",
            by_id[
                "balanced_trim_pressure_communication"
            ],
        )
        self.assertIn(
            "Balance hole·passage",
            by_id[
                "balance_hole_passage_function"
            ],
        )
        self.assertIn(
            "Cage-guided balanced plug",
            by_id[
                "cage_guided_balanced_plug_structure"
            ],
        )
        self.assertIn(
            "ideal full-balance",
            by_id[
                "ideal_full_balance_boundary"
            ],
        )

    def test_seal_friction_and_leakage_markers(
        self,
    ) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        self.assertIn(
            "seat seal",
            by_id["balance_seal_function"],
        )
        self.assertIn(
            "plug motion을 반대",
            by_id["balance_seal_friction"],
        )
        self.assertIn(
            "internal leakage path",
            by_id[
                "balance_seal_leakage_path"
            ],
        )
        self.assertIn(
            "closed seat boundary leakage",
            by_id[
                "seat_leakage_path_boundary"
            ],
        )

    def test_transient_application_and_operating_markers(
        self,
    ) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        self.assertIn(
            "Rapid stroke",
            by_id[
                "pressure_equalization_transient"
            ],
        )
        self.assertIn(
            "Balance passage plugging",
            by_id[
                "passage_plugging_dynamic_imbalance"
            ],
        )
        self.assertIn(
            "Clean high-ΔP",
            by_id[
                "clean_high_dp_large_size_application"
            ],
        )
        self.assertIn(
            "Dirty·slurry·particulate",
            by_id[
                "dirty_slurry_particulate_limit"
            ],
        )
        self.assertIn(
            "Minimum·normal·maximum",
            by_id[
                "operating_case_force_matrix"
            ],
        )

    def test_explicit_topic_handoff_boundaries(
        self,
    ) -> None:
        combined = json.dumps(
            {
                "fact": self.fact,
                "logic": self.logic,
                "model": self.model,
            },
            ensure_ascii=False,
        ) + TOPIC_SHEET.read_text(
            encoding="utf-8"
        )
        for marker in (
            "Topic 1",
            "Topic 3",
            "Topic 4",
            "Topic 9",
            "Topic 13",
            "Topic 14",
            "Topic 16",
        ):
            self.assertIn(
                marker,
                combined,
            )

    def test_section_aware_fatal_corrections(
        self,
    ) -> None:
        by_id = {
            row["id"]: row
            for row
            in self.fact[
                "fatal_wrong_claims"
            ]
        }
        checks = {
            "control_valve_balanced_trim_zero_force_all_cases":
                "residual effective area",
            "control_valve_nominal_seat_area_always_effective_area":
                "actual pressure boundary",
            "control_valve_balance_holes_instant_complete_equalization":
                "passage conductance",
            "control_valve_balance_seal_same_as_seat_seal":
                "shutoff boundary",
            "control_valve_balance_leakage_equals_seat_leakage":
                "rating basis",
            "control_valve_balanced_trim_no_seal_friction":
                "plug motion을 반대",
            "control_valve_seal_friction_assists_motion":
                "Fbs·v≤0",
            "control_valve_flow_to_open_universal_force_sign":
                "actual plug",
            "control_valve_passage_plugging_no_force_effect":
                "pressure communication",
            "control_valve_single_normal_case_sufficient":
                "Minimum·normal·maximum",
            "control_valve_residual_force_ignored_in_actuator_input":
                "actuator input",
        }
        for rule_id, marker in checks.items():
            correction = str(
                by_id[rule_id].get(
                    "correction"
                )
                or by_id[rule_id].get(
                    "correct_rule"
                )
                or ""
            )
            self.assertIn(
                marker,
                correction,
            )


class RouterRegressionTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = load_json(
            GENERATED_DIR
            / "model_answers.generated.json"
        )
        cls.answer_by_topic = {
            row["topic_id"]: row
            for row in cls.bank["answers"]
        }
        for topic_id in (
            TOPIC,
            TOPIC_1,
            TOPIC_2,
            TOPIC_3,
            TOPIC_4,
            TOPIC_5,
            TOPIC_6,
            TOPIC_7,
            TOPIC_8,
            TOPIC_9,
        ):
            if topic_id not in cls.answer_by_topic:
                raise AssertionError(
                    f"missing topic {topic_id}"
                )

    @classmethod
    def qtype(
        cls,
        topic_id: str,
    ) -> dict[str, Any]:
        return {
            "primary_type": {
                "id": cls.answer_by_topic[
                    topic_id
                ]["question_type"],
                "confidence": "high",
            }
        }

    @staticmethod
    def fact_eval(
        topic_id: str,
    ) -> dict[str, Any]:
        return {
            "topic_id": topic_id,
            "matched": True,
            "confidence": "high",
        }

    @classmethod
    def route(
        cls,
        question: str,
        topic_id: str,
        answer_text: str = "",
    ) -> dict[str, Any]:
        return find_model_answer_reference(
            question_text=question,
            answer_text=answer_text,
            fact_eval=cls.fact_eval(
                topic_id
            ),
            question_type_eval=cls.qtype(
                topic_id
            ),
            bank=cls.bank,
        )

    def assert_primary(
        self,
        result: dict[str, Any],
        expected: str,
    ) -> None:
        self.assertTrue(
            result.get("matched"),
            msg=result,
        )
        self.assertEqual(
            selected_topic(result),
            expected,
            msg=result,
        )

    def test_compare_structure_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Balanced trim과 unbalanced trim을 pressure path, effective area, residual force와 sealing 구조로 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_force_equation_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Fu=ΔP·Au와 Fr=ΔP·Ar, effective unbalanced area와 sign convention을 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_balance_passage_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Balance hole·passage와 cage-guided balanced plug의 pressure equalization 원리를 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_balance_and_seat_seal_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Balance seal, seat seal, internal balance leakage와 shutoff leakage를 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_seal_friction_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Balance-seal friction, breakaway·running friction과 actuator force input을 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_clean_high_dp_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Clean high-ΔP, large-size service의 balanced·unbalanced trim 선정기준을 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_dirty_particulate_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Dirty slurry particulate service에서 balance passage plugging과 seal wear를 고려한 trim 선정을 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_temperature_seal_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "High-temperature와 cryogenic balanced trim의 seal material, clearance와 leakage limit를 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_operating_case_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Minimum normal maximum 및 startup shutdown case별 residual force와 seal loading을 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_integrated_selection_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Structure, pressure force, balance seal, leakage, service condition과 lifecycle을 이용해 trim을 선정하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_topic1_actuator_sizing_boundary(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Worst-case unbalanced force, packing friction, seat load와 fail-safe spring으로 actuator thrust를 산정하시오.",
                TOPIC_1,
            ),
            TOPIC_1,
        )

    def test_topic3_dynamic_friction_boundary(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Deadband, stiction, hysteresis, breakaway delay와 positioner compensation을 진단하시오.",
                TOPIC_3,
            ),
            TOPIC_3,
        )

    def test_topic4_body_cage_boundary(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Globe·rotary body, general plug·cage·guide와 actuator type을 비교 선정하시오.",
                TOPIC_4,
            ),
            TOPIC_4,
        )

    def test_topic8_damage_boundary(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Pvc, Pv, FF, FL과 FLP로 cavitation, flashing과 liquid choked damage를 판정하시오.",
                TOPIC_8,
            ),
            TOPIC_8,
        )

    def test_topic9_noise_boundary(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Aerodynamic·hydrodynamic noise, multi-hole low-noise trim과 pipe transmission loss를 설명하시오.",
                TOPIC_9,
            ),
            TOPIC_9,
        )

    def test_question_only_routing_survives_answer_contamination(
        self,
    ) -> None:
        result = self.route(
            "Worst-case force와 fail-safe spring을 이용해 pneumatic actuator를 정량 sizing하시오.",
            TOPIC_1,
            answer_text=(
                "balanced trim pressure communication, "
                "residual effective area, balance seal, "
                "passage plugging과 cryogenic seal limit를 "
                "상세히 서술한다."
            ),
        )
        self.assert_primary(
            result,
            TOPIC_1,
        )
        aliases = set(
            self.answer_by_topic[
                TOPIC
            ]["routing_aliases"]
        )
        self.assertFalse(
            BROAD_ALIASES & aliases
        )


class ForceSealingSemanticRegressionTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.fact = load_json(
            SOURCE_DIR / "fact_anchor.json"
        )

    def test_unbalanced_force_numeric_domain_and_direction(
        self,
    ) -> None:
        self.assertEqual(
            pressure_force(0.0, 2.0),
            0.0,
        )
        self.assertEqual(
            pressure_force(10.0, 0.0),
            0.0,
        )
        self.assertGreater(
            pressure_force(20.0, 2.0),
            pressure_force(10.0, 2.0),
        )
        self.assertGreater(
            pressure_force(10.0, 3.0),
            pressure_force(10.0, 2.0),
        )
        with self.assertRaises(
            ValueError
        ):
            pressure_force(-1.0, 1.0)
        with self.assertRaises(
            ValueError
        ):
            pressure_force(1.0, -1.0)

    def test_residual_force_zero_and_positive_area(
        self,
    ) -> None:
        self.assertEqual(
            pressure_force(10.0, 0.0),
            0.0,
        )
        self.assertGreater(
            pressure_force(10.0, 1.0),
            0.0,
        )

    def test_balanced_force_reduction_condition(
        self,
    ) -> None:
        fu = pressure_force(10.0, 4.0)
        fr = pressure_force(10.0, 1.0)
        self.assertLess(fr, fu)
        self.assertFalse(
            pressure_force(10.0, 5.0)
            < pressure_force(10.0, 4.0)
        )

    def test_force_area_ratio_condition(
        self,
    ) -> None:
        self.assertTrue(
            math.isclose(
                force_ratio(
                    10.0,
                    1.0,
                    4.0,
                ),
                0.25,
            )
        )
        with self.assertRaises(
            ValueError
        ):
            force_ratio(
                10.0,
                1.0,
                0.0,
            )

    def test_sign_convention_reversal(
        self,
    ) -> None:
        positive = signed_force(
            10.0,
            2.0,
            1,
        )
        negative = signed_force(
            10.0,
            2.0,
            -1,
        )
        self.assertEqual(
            positive,
            -negative,
        )
        self.assertEqual(
            abs(positive),
            abs(negative),
        )
        with self.assertRaises(
            ValueError
        ):
            signed_force(
                10.0,
                2.0,
                0,
            )

    def test_seal_friction_opposes_motion(
        self,
    ) -> None:
        for velocity in (2.0, -2.0):
            force = seal_friction(
                5.0,
                velocity,
            )
            self.assertLessEqual(
                force * velocity,
                0.0,
            )
        self.assertEqual(
            seal_friction(5.0, 0.0),
            0.0,
        )
        with self.assertRaises(
            ValueError
        ):
            seal_friction(
                -1.0,
                1.0,
            )

    def test_breakaway_running_boundary(
        self,
    ) -> None:
        breakaway = 8.0
        running = 5.0
        self.assertGreaterEqual(
            breakaway,
            running,
        )
        self.assertNotEqual(
            breakaway / running,
            1.0,
        )

    def test_actuator_component_separation(
        self,
    ) -> None:
        self.assertEqual(
            actuator_components(
                10.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
            ),
            30.0,
        )
        without_balance_seal = (
            actuator_components(
                10.0,
                2.0,
                3.0,
                0.0,
                5.0,
                6.0,
            )
        )
        self.assertEqual(
            30.0 - without_balance_seal,
            4.0,
        )

    def test_positive_sample_semantic_cluster_coverage(
        self,
    ) -> None:
        rows = cluster_coverage(
            POSITIVE_ANSWER
        )
        self.assertEqual(
            set(rows),
            set(SEMANTIC_CLUSTERS),
        )
        self.assertTrue(
            all(rows.values()),
            msg=rows,
        )

    def test_contextual_negative_candidate_extraction(
        self,
    ) -> None:
        fatal_set = {
            row["id"]
            for row
            in self.fact[
                "fatal_wrong_claims"
            ]
        }
        self.assertTrue(
            set(NEGATIVE_SAMPLES)
            <= fatal_set
        )
        for rule_id, answer_text in (
            NEGATIVE_SAMPLES.items()
        ):
            with self.subTest(
                rule_id=rule_id
            ):
                matched = (
                    matched_profile_key_terms(
                        answer_text,
                        self.profile,
                    )
                )
                self.assertGreaterEqual(
                    len(matched),
                    3,
                    msg={
                        "rule_id": rule_id,
                        "matched": matched,
                    },
                )
                candidates = (
                    extract_logic_evidence_candidates(
                        answer_text,
                        self.profile,
                    )
                )
                self.assertTrue(
                    candidates,
                    msg={
                        "rule_id": rule_id,
                        "matched": matched,
                    },
                )

    def test_mocked_fatal_and_safe_verifier_contracts(
        self,
    ) -> None:
        rule_id = (
            "control_valve_balanced_trim_zero_force_all_cases"
        )
        answer_text = (
            "balanced trim, residual force, residual effective "
            "area, ideal full balance와 pressure communication을 "
            "설명하지만 모든 pressure, travel과 transient에서 "
            "force가 정확히 zero라고 주장한다."
        )
        candidates = (
            extract_logic_evidence_candidates(
                answer_text,
                self.profile,
            )
        )
        self.assertTrue(candidates)
        mocked_fatal = {
            "verdict": "fatal",
            "confidence": 0.99,
            "reason": (
                "Balanced trim을 모든 조건의 "
                "zero-force trim으로 단정하였다."
            ),
            "findings": [{
                "candidate_id":
                    candidates[0]["id"],
                "rule_id": rule_id,
                "severity": "fatal",
                "message":
                    "Universal zero-force claim",
                "correct_rule": (
                    "Balanced trim에도 residual effective "
                    "area와 transient pressure imbalance가 "
                    "남을 수 있다."
                ),
            }],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked_fatal,
        ):
            fatal_result = (
                verify_logic_with_llm(
                    answer_text,
                    TOPIC,
                )
            )
        self.assertTrue(
            fatal_result[
                "fatal_error_detected"
            ],
            msg=fatal_result,
        )
        self.assertEqual(
            fatal_result["mode"],
            "fatal",
        )
        self.assertEqual(
            fatal_result["findings"][0][
                "affected_layers"
            ],
            ["C"],
        )
        self.assertEqual(
            fatal_result[
                "recommended_ceiling"
            ],
            10.0,
        )

        mocked_safe = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": (
                "Residual force와 seal·leakage "
                "경계를 정확히 구분하였다."
            ),
            "findings": [],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked_safe,
        ):
            safe_result = (
                verify_logic_with_llm(
                    SAFE_ANSWER,
                    TOPIC,
                )
            )
        self.assertFalse(
            safe_result[
                "fatal_error_detected"
            ],
            msg=safe_result,
        )
        self.assertEqual(
            safe_result["mode"],
            "pass",
        )
        self.assertIsNone(
            safe_result[
                "recommended_ceiling"
            ]
        )
        self.assertEqual(
            safe_result["findings"],
            [],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
