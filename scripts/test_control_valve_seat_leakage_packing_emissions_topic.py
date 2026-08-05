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

TOPIC = 'control_valve_seat_leakage_shutoff_class_packing_fugitive_emissions'
TOPIC_1 = "control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe"
TOPIC_2 = "control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening"
TOPIC_3 = "control_valve_deadband_stiction_response_time_positioner_dynamic_performance"
TOPIC_4 = "control_valve_types_globe_rotary_body_actuator_selection"
TOPIC_5 = "control_valve_authority_rangeability_gain_installed_performance"
TOPIC_6 = "control_valve_sizing_cv_kv_reynolds_liquid_selection"
TOPIC_7 = "control_valve_gas_sizing_choked_flow_critical_pressure_ratio"
TOPIC_8 = "control_valve_cavitation_flashing_choked_flow_damage_prevention"
TOPIC_9 = "control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim"
TOPIC_10 = "balanced_trim_unbalanced_trim_structure_sealing_applications"
TOPIC_11 = "control_valve_positioner_ip_converter_booster_accessories_calibration"
TOPIC_12 = "smart_positioner_diagnostics_valve_signature_predictive_maintenance"

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"

EXPECTED_ANCHOR_IDS = ['internal_external_leakage_boundary', 'shutoff_class_purpose_scope', 'class_test_condition_dependency', 'shop_test_field_service_boundary', 'soft_metal_seat_tradeoff', 'single_double_seat_leakage_paths', 'balanced_trim_additional_leakage_path', 'seat_contact_geometry', 'seat_load_contact_stress_relation', 'insufficient_seat_load_leakage', 'excessive_seat_load_damage', 'pressure_direction_sealing', 'gas_liquid_test_medium_difference', 'test_pressure_temperature_duration_stabilization', 'volumetric_mass_bubble_basis', 'size_normalization_basis', 'ideal_gas_reference_conversion', 'bubble_count_conversion', 'seat_damage_erosion_wire_drawing', 'cavitation_flashing_damage_handoff', 'foreign_material_contamination', 'thermal_distortion_hot_leakage', 'misalignment_stem_guide_wear', 'surface_finish_lapping_hardness_coating', 'special_service_sealing_boundary', 'stem_shaft_packing_leakage_paths', 'packing_material_ring_arrangement', 'gland_geometry_compression', 'packing_leakage_friction_tradeoff', 'packing_consolidation_relaxation', 'live_loaded_packing_function', 'bellows_backup_packing_boundary', 'low_emission_qualification_field_boundary', 'fugitive_emission_source_monitoring', 'concentration_mass_emission_boundary', 'screening_bagging_quantification_methods', 'packing_adjustment_replacement_inspection', 'as_found_as_left_leakage', 'seat_packing_acceptance_separation', 'orientation_thermal_cycle_history', 'specification_test_lifecycle_workflow', 'measurement_calibration_detection_uncertainty', 'false_pass_false_fail_background', 'standard_edition_exact_citation', 'vendor_purchase_spec_alignment', 'topic1_topic3_topic10_boundary', 'topic11_topic12_topic14_boundary', 'topic15_topic16_standard_boundary']
EXPECTED_FATAL_IDS = ['internal_external_leakage_identical', 'class_guarantees_all_field_conditions', 'class_independent_of_test_conditions', 'higher_class_universally_better', 'soft_seat_always_zero_leakage', 'metal_seat_cannot_tight_shutoff', 'balanced_trim_has_no_extra_leakage', 'more_seat_load_always_better', 'seat_load_unrelated_to_actuator', 'pressure_direction_irrelevant', 'gas_liquid_leakage_numbers_directly_equal', 'bubble_volume_is_universal', 'gauge_pressure_valid_for_gas_reference', 'all_leakage_units_directly_comparable', 'packing_tightening_always_solves_leakage', 'packing_compression_has_no_friction_effect', 'live_loaded_packing_is_maintenance_free', 'bellows_eliminates_all_external_leakage', 'qualification_guarantees_field_emissions', 'concentration_equals_mass_emission', 'seat_test_proves_packing_emissions', 'as_left_only_is_sufficient', 'standard_edition_irrelevant', 'pst_automatically_proves_shutoff_class']
EXPECTED_MAJOR_IDS = ['fixed_leakage_class_all_services', 'fixed_test_pressure', 'fixed_test_medium', 'fixed_bubble_volume', 'fixed_seat_load', 'fixed_soft_seat_temperature', 'fixed_packing_compression', 'fixed_live_load_preload', 'fixed_emission_screening_threshold', 'fixed_repair_criterion', 'fixed_test_interval', 'fixed_measurement_uncertainty']

BROAD_ALIASES = {
    "leakage",
    "leak",
    "packing",
    "emission",
    "seat",
    "class",
    "seal",
    "valve",
    "test",
    "fugitive",
}

NEGATIVE_RULE_IDS = (
    "class_guarantees_all_field_conditions",
    "soft_seat_always_zero_leakage",
    "gauge_pressure_valid_for_gas_reference",
    "packing_tightening_always_solves_leakage",
    "qualification_guarantees_field_emissions",
    "pst_automatically_proves_shutoff_class",
)

SEMANTIC_CLUSTERS = {
    "leakage_path": (
        "internal through-seat leakage",
        "external atmospheric leakage",
        "seat leakage test",
        "packing fugitive-emission test",
    ),
    "class_condition": (
        "shutoff class",
        "test medium",
        "pressure direction",
        "temperature",
        "measurement basis",
    ),
    "seat_tradeoff": (
        "soft seat",
        "metal seat",
        "seat load",
        "contact stress",
        "reverse pressure",
    ),
    "conversion": (
        "volumetric",
        "mass",
        "bubble count",
        "absolute pressure",
        "absolute temperature",
    ),
    "damage": (
        "seat damage",
        "foreign material",
        "thermal distortion",
        "guide wear",
        "surface finish",
    ),
    "packing": (
        "packing compression",
        "gland load",
        "live-loaded packing",
        "bellows seal",
        "low-emission packing",
    ),
    "emission": (
        "fugitive emission",
        "screening",
        "bagging",
        "concentration",
        "mass-emission rate",
    ),
    "acceptance": (
        "as-found",
        "as-left",
        "detection limit",
        "uncertainty",
        "false pass",
    ),
    "workflow": (
        "specification",
        "shop test",
        "commissioning",
        "maintenance",
        "vendor guarantee",
    ),
}

POSITIVE_ANSWER = """
Internal through-seat leakage와 external atmospheric leakage를 구분하고,
seat leakage test와 packing fugitive-emission test를 별도 판정한다.
Shutoff class는 test medium, pressure direction, temperature와 measurement basis를
포함한 계약이다. Soft seat와 metal seat를 seat load, contact stress와 reverse pressure
조건으로 비교한다. Volumetric, mass와 bubble count leakage를 구분하고 gas 환산에는
absolute pressure와 absolute temperature를 사용한다. Seat damage, foreign material,
thermal distortion, guide wear와 surface finish를 진단한다. Packing compression,
gland load, live-loaded packing, bellows seal과 low-emission packing의 한계를 설명한다.
Fugitive emission은 screening과 bagging을 구분하고 concentration과 mass-emission rate를
혼동하지 않는다. As-found와 as-left를 같은 조건에서 비교하고 detection limit,
uncertainty와 false pass를 검토한다. Specification, shop test, commissioning,
maintenance, vendor guarantee와 purchaser acceptance를 연결한다.
"""

SAFE_ANSWER = """
Shutoff class는 지정된 shop-test condition의 acceptance이다. Internal through-seat
leakage와 external atmospheric leakage를 구분한다. Gas leakage 환산에는 absolute
pressure와 absolute temperature를 사용한다. Packing adjustment는 controlled gland
procedure로 수행하고 friction과 actuator demand를 확인한다. Low-emission qualification은
field installation을 자동 보증하지 않는다. As-found와 as-left, detection limit와
measurement uncertainty를 함께 기록한다. PST와 smart diagnostics는 보조 evidence이며
governing shutoff test와 Topic 15 proof-test requirement를 자동 대체하지 않는다.
"""


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def target_entry(filename: str, list_key: str) -> dict[str, Any]:
    rows = load_json(GENERATED_DIR / filename).get(list_key, [])
    matches = [
        row
        for row in rows
        if isinstance(row, dict) and row.get("topic_id") == TOPIC
    ]
    if len(matches) != 1:
        raise AssertionError(f"{filename} target count={len(matches)}")
    return matches[0]


def selected_topic(result: dict[str, Any]) -> str | None:
    primary = result.get("primary_reference") or {}
    return primary.get("topic_id") if isinstance(primary, dict) else None


def route_reference(
    question: str,
    topic_id: str,
    answer_text: str = "",
) -> dict[str, Any]:
    bank = load_json(GENERATED_DIR / "model_answers.generated.json")
    answer_by_topic = {
        row["topic_id"]: row
        for row in bank["answers"]
    }
    qtype = {
        "primary_type": {
            "id": answer_by_topic[topic_id]["question_type"],
            "confidence": "high",
        }
    }
    fact_eval = {
        "topic_id": topic_id,
        "matched": True,
        "confidence": "high",
    }
    return find_model_answer_reference(
        question_text=question,
        answer_text=answer_text,
        fact_eval=fact_eval,
        question_type_eval=qtype,
        bank=bank,
    )


def leakage_ratio(leakage: float, reference: float) -> float:
    if leakage < 0.0 or reference <= 0.0:
        raise ValueError
    return leakage / reference


def percent_allowable(leakage: float, allowable: float) -> float:
    if leakage < 0.0 or allowable <= 0.0:
        raise ValueError
    return 100.0 * leakage / allowable


def normalized_leakage(leakage: float, size_basis: float) -> float:
    if leakage < 0.0 or size_basis <= 0.0:
        raise ValueError
    return leakage / size_basis


def mass_flow(density: float, volume_flow: float) -> float:
    if density < 0.0 or volume_flow < 0.0:
        raise ValueError
    return density * volume_flow


def ideal_gas_reference(
    test_flow: float,
    test_pressure: float,
    reference_pressure: float,
    test_temperature: float,
    reference_temperature: float,
) -> float:
    if (
        test_flow < 0.0
        or test_pressure <= 0.0
        or reference_pressure <= 0.0
        or test_temperature <= 0.0
        or reference_temperature <= 0.0
    ):
        raise ValueError
    return (
        test_flow
        * test_pressure
        / reference_pressure
        * reference_temperature
        / test_temperature
    )


def bubble_rate(
    bubble_count: float,
    bubble_volume: float,
    duration: float,
) -> float:
    if (
        bubble_count < 0.0
        or bubble_volume <= 0.0
        or duration <= 0.0
    ):
        raise ValueError
    return bubble_count * bubble_volume / duration


def packing_compression(
    initial_height: float,
    installed_height: float,
) -> float:
    if (
        initial_height <= 0.0
        or installed_height < 0.0
        or installed_height > initial_height
    ):
        raise ValueError
    return (
        initial_height - installed_height
    ) / initial_height


def gland_stress(gland_force: float, effective_area: float) -> float:
    if gland_force < 0.0 or effective_area <= 0.0:
        raise ValueError
    return gland_force / effective_area


def baseline_delta(current: float, baseline: float) -> float:
    return current - baseline


def percent_change(current: float, baseline: float) -> float:
    if baseline == 0.0:
        raise ValueError
    return 100.0 * (
        current - baseline
    ) / abs(baseline)


def rate_of_change(
    first: float,
    second: float,
    t1: float,
    t2: float,
) -> float:
    if t2 <= t1:
        raise ValueError
    return (second - first) / (t2 - t1)


def uncertainty_aware_pass(
    measured: float,
    uncertainty: float,
    allowable: float,
) -> bool:
    if (
        measured < 0.0
        or uncertainty < 0.0
        or allowable < 0.0
    ):
        raise ValueError
    return measured + uncertainty <= allowable


def cluster_coverage(text: str) -> dict[str, bool]:
    normalized = " ".join(text.casefold().split())
    return {
        group: all(
            " ".join(marker.casefold().split()) in normalized
            for marker in markers
        )
        for group, markers in SEMANTIC_CLUSTERS.items()
    }


def matched_profile_key_terms(
    text: str,
    profile: dict[str, Any],
) -> list[str]:
    normalized = " ".join(text.casefold().split())
    terms = (
        profile.get("candidate_extraction") or {}
    ).get("key_terms") or []
    return [
        str(term)
        for term in terms
        if " ".join(str(term).casefold().split()) in normalized
    ]


def negative_samples() -> dict[str, str]:
    fact = load_json(SOURCE_DIR / "fact_anchor.json")
    by_id = {
        row["id"]: row
        for row in fact["fatal_wrong_claims"]
    }
    samples: dict[str, str] = {}
    for rule_id in NEGATIVE_RULE_IDS:
        row = by_id[rule_id]
        wrong = str(row.get("wrong_claim") or row.get("claim") or "")
        correction = str(
            row.get("correction")
            or row.get("correct_rule")
            or ""
        )
        samples[rule_id] = f"{wrong} {correction}"
    return samples


def assert_markers(
    testcase: unittest.TestCase,
    statement: str,
    markers: tuple[str, ...],
) -> None:
    folded = " ".join(statement.casefold().split())
    for marker in markers:
        testcase.assertIn(
            " ".join(marker.casefold().split()),
            folded,
        )


class GeneratedContractRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json(SOURCE_DIR / "fact_anchor.json")
        cls.logic = load_json(SOURCE_DIR / "logic_check.json")
        cls.model = load_json(SOURCE_DIR / "model_answer.json")
        cls.importance = load_json(SOURCE_DIR / "topic_importance.json")
        cls.gfact = target_entry("fact_anchors.generated.json", "topics")
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )
        cls.glogic = target_entry(
            "logic_checks.generated.json",
            "topic_logic_checks",
        )
        cls.gmodel = target_entry("model_answers.generated.json", "answers")
        cls.gimportance = target_entry(
            "topic_importance.generated.json",
            "topics",
        )
        cls.manifest = target_entry(
            "topic_pack_manifest.generated.json",
            "topics",
        )
        cls.by_id = {
            row["id"]: row["statement"]
            for row in cls.fact["anchors"]
        }

    def test_source_generated_and_dynamic_manifest_alignment(self) -> None:
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
            self.assertEqual(row["topic_id"], TOPIC)
        source_ids = sorted(
            path.name
            for path in (ROOT / "rubrics" / "topic_packs").iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
        manifest_ids = [
            row["topic_id"]
            for row in load_json(
                GENERATED_DIR / "topic_pack_manifest.generated.json"
            )["topics"]
        ]
        self.assertEqual(manifest_ids, source_ids)
        self.assertEqual(manifest_ids.count(TOPIC), 1)

    def test_exact_anchor_fatal_major_contract(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.fact["anchors"]],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.gfact["anchors"]],
            EXPECTED_ANCHOR_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.fact["fatal_wrong_claims"]],
            EXPECTED_FATAL_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.gfact["fatal_wrong_claims"]],
            EXPECTED_FATAL_IDS,
        )
        self.assertEqual(
            [row["id"] for row in self.profile["major_checks"]],
            EXPECTED_MAJOR_IDS,
        )

    def test_anchor_rows_exact_source_generated_alignment(self) -> None:
        source_by = {
            row["id"]: row
            for row in self.fact["anchors"]
        }
        generated_by = {
            row["id"]: row
            for row in self.gfact["anchors"]
        }
        for anchor_id in EXPECTED_ANCHOR_IDS:
            for key in (
                "id",
                "anchor_id",
                "statement",
                "keywords",
                "core_terms",
                "accepted_explanations",
                "rejected_explanations",
                "grading_notes",
                "source_basis",
                "claim",
            ):
                self.assertEqual(
                    generated_by[anchor_id].get(key),
                    source_by[anchor_id].get(key),
                )

    def test_fatal_rows_exact_source_generated_alignment(self) -> None:
        source_by = {
            row["id"]: row
            for row in self.fact["fatal_wrong_claims"]
        }
        generated_by = {
            row["id"]: row
            for row in self.gfact["fatal_wrong_claims"]
        }
        for rule_id in EXPECTED_FATAL_IDS:
            self.assertEqual(generated_by[rule_id], source_by[rule_id])
        self.assertEqual(
            self.profile["fatal_conditions"],
            self.fact["fatal_wrong_claims"],
        )

    def test_major_rows_exact_source_generated_alignment(self) -> None:
        self.assertEqual(
            self.profile["major_checks"],
            self.logic["llm_profile"]["major_checks"],
        )

    def test_semantic_score_and_deterministic_policy(self) -> None:
        self.assertFalse(self.glogic["enabled"])
        self.assertEqual(self.glogic["fatal_checks"], [])
        self.assertEqual(self.glogic["major_checks"], [])
        self.assertEqual(self.glogic["question_type_checks"], [])
        self.assertEqual(
            self.profile["candidate_extraction"]["rules"],
            [],
        )
        self.assertGreaterEqual(
            len(self.profile["candidate_extraction"]["key_terms"]),
            300,
        )
        policy = self.profile["score_policy"]
        self.assertFalse(policy["direct_score_application"])
        self.assertIsNone(policy["recommended_ceiling"])
        self.assertEqual(policy["direct_d_e_effect"], "none")
        self.assertEqual(policy["affected_layers"], ["C"])
        self.assertEqual(
            self.profile["output_contract"]["excluded_score_layers"],
            ["D", "E"],
        )

    def test_patterns_outline_aliases_and_importance(self) -> None:
        patterns = self.model["expected_question_patterns"]
        outlines = self.model["recommended_outline"]
        self.assertEqual(len(patterns), 10)
        self.assertEqual(len(outlines), 8)
        anchor_set = set(EXPECTED_ANCHOR_IDS)
        self.assertTrue(
            all(
                set(row["required_anchor_ids"]) <= anchor_set
                for row in patterns
            )
        )
        self.assertEqual(
            set().union(
                *(set(row["anchor_refs"]) for row in outlines)
            ),
            anchor_set,
        )
        aliases = {
            str(alias).casefold()
            for alias in self.model["routing_aliases"]
        }
        self.assertFalse(BROAD_ALIASES & aliases)
        self.assertEqual(
            self.gmodel["topic_aliases"],
            self.model["routing_aliases"],
        )
        self.assertEqual(
            self.gmodel["routing_aliases"],
            self.model["routing_aliases"],
        )
        self.assertEqual(self.gimportance, self.importance)
        self.assertEqual(self.importance["difficulty"], "FIELD_APPLICATION")
        self.assertEqual(
            self.importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )
        self.assertEqual(self.importance["question_type"], "COMPARE_SELECTION")

    def test_internal_external_leakage_markers(self) -> None:
        assert_markers(
            self,
            self.by_id["internal_external_leakage_boundary"],
            (
                "internal through-seat leakage",
                "external atmospheric leakage",
                "stem·shaft packing",
            ),
        )
        assert_markers(
            self,
            self.by_id["seat_packing_acceptance_separation"],
            (
                "seat leakage acceptance",
                "packing fugitive-emission acceptance",
                "별도 판정",
            ),
        )

    def test_class_and_shop_field_markers(self) -> None:
        assert_markers(
            self,
            self.by_id["shutoff_class_purpose_scope"],
            (
                "shutoff",
                "leakage class",
                "구매·검사 계약",
                "자동 보증하지 않는다",
            ),
        )
        assert_markers(
            self,
            self.by_id["class_test_condition_dependency"],
            (
                "test medium",
                "pressure direction",
                "temperature",
                "measurement basis",
            ),
        )
        assert_markers(
            self,
            self.by_id["shop_test_field_service_boundary"],
            (
                "shop shutoff test",
                "field operating leakage",
                "직접 동일시할 수 없다",
            ),
        )

    def test_soft_metal_and_balanced_trim_markers(self) -> None:
        assert_markers(
            self,
            self.by_id["soft_metal_seat_tradeoff"],
            (
                "soft seat",
                "metal seat",
                "temperature",
                "wear",
            ),
        )
        assert_markers(
            self,
            self.by_id["balanced_trim_additional_leakage_path"],
            (
                "balanced trim",
                "balance seal",
                "additional internal leakage path",
            ),
        )

    def test_seat_load_and_pressure_direction_markers(self) -> None:
        assert_markers(
            self,
            self.by_id["seat_load_contact_stress_relation"],
            (
                "seat load",
                "contact stress",
                "pressure direction",
            ),
        )
        assert_markers(
            self,
            self.by_id["insufficient_seat_load_leakage"],
            (
                "seat load가 부족",
                "shutoff leakage",
            ),
        )
        assert_markers(
            self,
            self.by_id["excessive_seat_load_damage"],
            (
                "seat load가 과도",
                "galling",
                "actuator demand",
            ),
        )
        assert_markers(
            self,
            self.by_id["pressure_direction_sealing"],
            (
                "pressure-assisted",
                "pressure-unbalanced",
                "reverse-pressure",
            ),
        )

    def test_medium_conversion_and_bubble_markers(self) -> None:
        assert_markers(
            self,
            self.by_id["gas_liquid_test_medium_difference"],
            (
                "gas",
                "liquid test medium",
                "compressibility",
                "detection method",
            ),
        )
        assert_markers(
            self,
            self.by_id["ideal_gas_reference_conversion"],
            (
                "absolute pressure",
                "absolute temperature",
            ),
        )
        assert_markers(
            self,
            self.by_id["bubble_count_conversion"],
            (
                "bubble count",
                "bubble volume",
                "counting duration",
                "pressure·temperature condition",
            ),
        )

    def test_damage_contamination_and_service_markers(self) -> None:
        assert_markers(
            self,
            self.by_id["seat_damage_erosion_wire_drawing"],
            (
                "seat damage",
                "wire drawing",
                "galling",
            ),
        )
        assert_markers(
            self,
            self.by_id["foreign_material_contamination"],
            (
                "foreign material",
                "polymerization product",
                "solid particle",
            ),
        )
        assert_markers(
            self,
            self.by_id["thermal_distortion_hot_leakage"],
            (
                "thermal distortion",
                "differential expansion",
                "hot operating condition",
            ),
        )
        assert_markers(
            self,
            self.by_id["special_service_sealing_boundary"],
            (
                "fire-safe",
                "high-temperature",
                "cryogenic",
                "topic 14",
            ),
        )

    def test_packing_design_and_friction_markers(self) -> None:
        assert_markers(
            self,
            self.by_id["stem_shaft_packing_leakage_paths"],
            (
                "sliding-stem packing",
                "rotary-shaft packing",
                "external leakage path",
            ),
        )
        assert_markers(
            self,
            self.by_id["packing_leakage_friction_tradeoff"],
            (
                "packing compression",
                "friction",
                "deadband",
                "actuator demand",
            ),
        )
        assert_markers(
            self,
            self.by_id["live_loaded_packing_function"],
            (
                "live-loaded packing",
                "spring range",
                "installed compression",
            ),
        )
        assert_markers(
            self,
            self.by_id["bellows_backup_packing_boundary"],
            (
                "bellows seal",
                "cycle life",
                "backup packing",
            ),
        )

    def test_fugitive_measurement_markers(self) -> None:
        assert_markers(
            self,
            self.by_id["fugitive_emission_source_monitoring"],
            (
                "fugitive emission",
                "monitoring point",
                "background",
            ),
        )
        assert_markers(
            self,
            self.by_id["concentration_mass_emission_boundary"],
            (
                "local concentration reading",
                "mass-emission rate",
                "동일한 물리량이 아니다",
            ),
        )
        assert_markers(
            self,
            self.by_id["screening_bagging_quantification_methods"],
            (
                "sniffing·screening",
                "bagging·enclosure",
                "정량화",
            ),
        )

    def test_as_found_uncertainty_and_workflow_markers(self) -> None:
        assert_markers(
            self,
            self.by_id["as_found_as_left_leakage"],
            (
                "as-found",
                "as-left",
                "같은",
                "medium",
                "pressure",
                "temperature",
                "method",
                "stabilization condition",
            ),
        )
        assert_markers(
            self,
            self.by_id["measurement_calibration_detection_uncertainty"],
            (
                "instrument calibration",
                "detection limit",
                "measurement uncertainty",
            ),
        )
        assert_markers(
            self,
            self.by_id["specification_test_lifecycle_workflow"],
            (
                "specification→selection→shop test",
                "commissioning",
                "maintenance→as-left verification",
            ),
        )

    def test_explicit_topic_handoff_boundaries(self) -> None:
        combined = (
            json.dumps(
                {
                    "fact": self.fact,
                    "logic": self.logic,
                    "model": self.model,
                },
                ensure_ascii=False,
            )
            + TOPIC_SHEET.read_text(encoding="utf-8")
        ).casefold()
        for marker in (
            "topic 1",
            "topic 3",
            "topic 8",
            "topic 10",
            "topic 11",
            "topic 12",
            "topic 14",
            "topic 15",
            "topic 16",
        ):
            self.assertIn(marker, combined)

    def test_section_aware_fatal_corrections(self) -> None:
        by_id = {
            row["id"]: row
            for row in self.fact["fatal_wrong_claims"]
        }
        checks: dict[str, tuple[str, ...]] = {
            "internal_external_leakage_identical": (
                "test method",
                "unit",
                "acceptance",
            ),
            "class_guarantees_all_field_conditions": (
                "shop-test condition",
                "field operating condition",
                "자동 보증하지 않는다",
            ),
            "more_seat_load_always_better": (
                "부족하면",
                "과도하면",
                "actuator demand",
            ),
            "gauge_pressure_valid_for_gas_reference": (
                "absolute pressure",
                "absolute temperature",
            ),
            "packing_tightening_always_solves_leakage": (
                "controlled gland procedure",
                "friction",
                "actuator demand",
            ),
            "live_loaded_packing_is_maintenance_free": (
                "spring range",
                "installed compression",
                "inspection",
            ),
            "bellows_eliminates_all_external_leakage": (
                "fatigue",
                "cycle-life",
                "backup packing",
            ),
            "qualification_guarantees_field_emissions": (
                "test cycle",
                "field installation",
                "maintenance",
                "자동 보증하지 않는다",
            ),
            "concentration_equals_mass_emission": (
                "species fraction",
                "mass-emission rate",
            ),
            "pst_automatically_proves_shutoff_class": (
                "governing shutoff test",
                "topic 15 proof-test requirement",
                "자동 대체하지 않는다",
            ),
        }
        for rule_id, markers in checks.items():
            correction = str(
                by_id[rule_id].get("correction")
                or by_id[rule_id].get("correct_rule")
                or ""
            )
            assert_markers(self, correction, markers)


class RouterRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = load_json(GENERATED_DIR / "model_answers.generated.json")
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
            TOPIC_10,
            TOPIC_11,
            TOPIC_12,
        ):
            if topic_id not in cls.answer_by_topic:
                raise AssertionError(f"missing topic {topic_id}")

    @classmethod
    def qtype(cls, topic_id: str) -> dict[str, Any]:
        return {
            "primary_type": {
                "id": cls.answer_by_topic[topic_id]["question_type"],
                "confidence": "high",
            }
        }

    @staticmethod
    def fact_eval(topic_id: str) -> dict[str, Any]:
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
            fact_eval=cls.fact_eval(topic_id),
            question_type_eval=cls.qtype(topic_id),
            bank=cls.bank,
        )

    def assert_primary(
        self,
        result: dict[str, Any],
        expected: str,
    ) -> None:
        self.assertTrue(result.get("matched"), msg=result)
        self.assertEqual(selected_topic(result), expected, msg=result)

    def test_internal_external_leakage_route(self) -> None:
        self.assert_primary(
            self.route(
                "Control valve internal through-seat leakage와 external "
                "stem packing atmospheric leakage를 구분하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_shutoff_class_condition_route(self) -> None:
        self.assert_primary(
            self.route(
                "Shutoff leakage class와 test medium, pressure direction, "
                "temperature, duration 및 measurement basis를 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_soft_metal_seat_route(self) -> None:
        self.assert_primary(
            self.route(
                "Soft seat와 metal seat의 tightness, temperature, wear와 "
                "chemical compatibility를 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_seat_load_pressure_direction_route(self) -> None:
        self.assert_primary(
            self.route(
                "Seat load, contact stress, pressure-assisted sealing과 "
                "reverse-pressure shutoff 영향을 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_gas_liquid_test_route(self) -> None:
        self.assert_primary(
            self.route(
                "Gas와 liquid valve leakage test medium, compressibility, "
                "viscosity와 detection method를 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_reference_conversion_route(self) -> None:
        self.assert_primary(
            self.route(
                "Gas leakage를 absolute pressure와 absolute temperature로 "
                "reference condition에 환산하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_bubble_count_route(self) -> None:
        self.assert_primary(
            self.route(
                "Bubble count, representative bubble volume와 counting duration으로 "
                "volumetric leakage를 계산하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_damage_diagnosis_route(self) -> None:
        self.assert_primary(
            self.route(
                "Seat erosion, wire drawing, foreign material, thermal distortion, "
                "stem bending과 guide wear leakage를 진단하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_packing_design_route(self) -> None:
        self.assert_primary(
            self.route(
                "Conventional, live-loaded, low-emission packing과 bellows seal의 "
                "leakage, friction와 maintenance를 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_fugitive_measurement_route(self) -> None:
        self.assert_primary(
            self.route(
                "Fugitive emission sniffing screening bagging, concentration와 "
                "mass-emission rate를 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_as_found_uncertainty_route(self) -> None:
        self.assert_primary(
            self.route(
                "As-found와 as-left leakage, detection limit, uncertainty와 "
                "false pass false fail을 평가하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_integrated_lifecycle_route(self) -> None:
        self.assert_primary(
            self.route(
                "Seat type, shutoff class, packing, emission requirement와 "
                "specification shop test maintenance lifecycle을 통합 선정하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_topic1_force_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Seat load, unbalanced force, packing friction과 fail-safe spring으로 "
                "actuator thrust를 산정하시오.",
                TOPIC_1,
            ),
            TOPIC_1,
        )

    def test_topic3_dynamic_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Packing friction, deadband, stiction, hysteresis와 response time을 "
                "동적으로 시험하고 tuning하시오.",
                TOPIC_3,
            ),
            TOPIC_3,
        )

    def test_topic4_body_actuator_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Globe, ball, butterfly valve body와 pneumatic electric hydraulic "
                "actuator type을 비교 선정하시오.",
                TOPIC_4,
            ),
            TOPIC_4,
        )

    def test_topic8_damage_physics_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Cavitation, flashing, choked liquid flow와 trim erosion damage "
                "prevention을 설명하시오.",
                TOPIC_8,
            ),
            TOPIC_8,
        )

    def test_topic10_trim_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Balanced trim과 unbalanced trim의 force balance, balance seal "
                "structure와 internal leakage path를 비교하시오.",
                TOPIC_10,
            ),
            TOPIC_10,
        )

    def test_topic11_positioner_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Positioner, I/P converter, volume booster와 zero span calibration을 "
                "설명하시오.",
                TOPIC_11,
            ),
            TOPIC_11,
        )

    def test_topic12_diagnostic_boundary(self) -> None:
        self.assert_primary(
            self.route(
                "Valve signature, travel-pressure trend와 smart positioner predictive "
                "maintenance workflow를 설명하시오.",
                TOPIC_12,
            ),
            TOPIC_12,
        )

    def test_question_only_routing_survives_answer_contamination(self) -> None:
        result = self.route(
            "Internal seat leakage, shutoff class test condition, packing "
            "fugitive-emission과 uncertainty를 비교하시오.",
            TOPIC,
            answer_text=(
                "Actuator thrust, cavitation, positioner calibration, valve signature, "
                "deadband stiction과 balanced trim을 상세히 기술한다."
            ),
        )
        self.assert_primary(result, TOPIC)
        aliases = {
            str(alias).casefold()
            for alias in self.answer_by_topic[TOPIC]["routing_aliases"]
        }
        self.assertFalse(BROAD_ALIASES & aliases)


class SeatLeakagePackingSemanticRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = target_entry(
            "logic_check_profiles.generated.json",
            "profiles",
        )

    def test_leakage_ratio_and_domain(self) -> None:
        self.assertTrue(
            math.isclose(
                leakage_ratio(2.0, 8.0),
                0.25,
                rel_tol=0.0,
                abs_tol=1e-12,
            )
        )
        with self.assertRaises(ValueError):
            leakage_ratio(-1.0, 1.0)
        with self.assertRaises(ValueError):
            leakage_ratio(1.0, 0.0)

    def test_percent_allowable_and_domain(self) -> None:
        self.assertEqual(percent_allowable(2.0, 8.0), 25.0)
        with self.assertRaises(ValueError):
            percent_allowable(1.0, 0.0)

    def test_normalized_leakage_and_domain(self) -> None:
        self.assertEqual(normalized_leakage(4.0, 2.0), 2.0)
        with self.assertRaises(ValueError):
            normalized_leakage(1.0, 0.0)

    def test_mass_flow_and_domain(self) -> None:
        self.assertEqual(mass_flow(2.0, 3.0), 6.0)
        with self.assertRaises(ValueError):
            mass_flow(-1.0, 1.0)

    def test_ideal_gas_reference_and_domain(self) -> None:
        self.assertEqual(
            ideal_gas_reference(
                10.0,
                200.0,
                100.0,
                400.0,
                300.0,
            ),
            15.0,
        )
        with self.assertRaises(ValueError):
            ideal_gas_reference(
                1.0,
                0.0,
                1.0,
                1.0,
                1.0,
            )

    def test_bubble_rate_and_domain(self) -> None:
        self.assertEqual(bubble_rate(10.0, 0.2, 4.0), 0.5)
        with self.assertRaises(ValueError):
            bubble_rate(1.0, 1.0, 0.0)

    def test_packing_compression_and_domain(self) -> None:
        self.assertTrue(
            math.isclose(
                packing_compression(10.0, 8.0),
                0.2,
                rel_tol=0.0,
                abs_tol=1e-12,
            )
        )
        with self.assertRaises(ValueError):
            packing_compression(0.0, 0.0)
        with self.assertRaises(ValueError):
            packing_compression(10.0, 11.0)

    def test_gland_stress_and_domain(self) -> None:
        self.assertEqual(gland_stress(20.0, 4.0), 5.0)
        with self.assertRaises(ValueError):
            gland_stress(1.0, 0.0)

    def test_baseline_delta_percent_and_rate(self) -> None:
        self.assertEqual(baseline_delta(8.0, 5.0), 3.0)
        self.assertEqual(percent_change(12.0, 10.0), 20.0)
        self.assertEqual(rate_of_change(10.0, 14.0, 2.0, 4.0), 2.0)
        with self.assertRaises(ValueError):
            percent_change(1.0, 0.0)
        with self.assertRaises(ValueError):
            rate_of_change(1.0, 2.0, 5.0, 5.0)

    def test_uncertainty_aware_acceptance(self) -> None:
        self.assertTrue(uncertainty_aware_pass(7.0, 1.0, 8.0))
        self.assertFalse(uncertainty_aware_pass(7.1, 1.0, 8.0))
        with self.assertRaises(ValueError):
            uncertainty_aware_pass(-1.0, 0.0, 1.0)

    def test_positive_sample_semantic_cluster_coverage(self) -> None:
        rows = cluster_coverage(POSITIVE_ANSWER)
        self.assertEqual(set(rows), set(SEMANTIC_CLUSTERS))
        self.assertTrue(all(rows.values()), msg=rows)

    def test_contextual_negative_candidate_extraction(self) -> None:
        samples = negative_samples()
        self.assertEqual(set(samples), set(NEGATIVE_RULE_IDS))
        for rule_id, answer_text in samples.items():
            with self.subTest(rule_id=rule_id):
                matched = matched_profile_key_terms(
                    answer_text,
                    self.profile,
                )
                self.assertGreaterEqual(
                    len(matched),
                    2,
                    msg={"rule_id": rule_id, "matched": matched},
                )
                candidates = extract_logic_evidence_candidates(
                    answer_text,
                    self.profile,
                )
                self.assertTrue(
                    candidates,
                    msg={"rule_id": rule_id, "matched": matched},
                )

    def test_mocked_fatal_verifier_contract(self) -> None:
        rule_id = "class_guarantees_all_field_conditions"
        answer_text = negative_samples()[rule_id]
        candidates = extract_logic_evidence_candidates(
            answer_text,
            self.profile,
        )
        self.assertTrue(candidates)
        mocked_fatal = {
            "verdict": "fatal",
            "confidence": 0.99,
            "reason": "Shutoff class를 모든 field condition의 guarantee로 단정한다.",
            "findings": [{
                "candidate_id": candidates[0]["id"],
                "rule_id": rule_id,
                "severity": "fatal",
                "message": "Universal shutoff-class guarantee",
                "correct_rule": (
                    "Shutoff class는 지정된 medium, pressure, direction, "
                    "temperature와 measurement basis의 shop-test acceptance이다."
                ),
            }],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked_fatal,
        ):
            result = verify_logic_with_llm(answer_text, TOPIC)
        self.assertTrue(result["fatal_error_detected"], msg=result)
        self.assertEqual(result["mode"], "fatal")
        self.assertEqual(
            result["findings"][0]["affected_layers"],
            ["C"],
        )

    def test_mocked_safe_verifier_contract(self) -> None:
        candidates = extract_logic_evidence_candidates(
            SAFE_ANSWER,
            self.profile,
        )
        self.assertTrue(candidates)
        mocked_safe = {
            "verdict": "pass",
            "confidence": 1.0,
            "reason": (
                "Leakage path, test conditions, field limitation, uncertainty와 "
                "Topic 경계를 유지한다."
            ),
            "findings": [],
        }
        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=mocked_safe,
        ):
            result = verify_logic_with_llm(SAFE_ANSWER, TOPIC)
        self.assertFalse(result["fatal_error_detected"], msg=result)
        self.assertEqual(result["mode"], "pass")
        self.assertIsNone(result["recommended_ceiling"])
        self.assertEqual(result["findings"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
