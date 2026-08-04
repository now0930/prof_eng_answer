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

TOPIC = 'control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim'
TOPIC_2 = 'control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening'
TOPIC_3 = 'control_valve_deadband_stiction_response_time_positioner_dynamic_performance'
TOPIC_4 = 'control_valve_types_globe_rotary_body_actuator_selection'
TOPIC_5 = 'control_valve_authority_rangeability_gain_installed_performance'
TOPIC_6 = 'control_valve_sizing_cv_kv_reynolds_liquid_selection'
TOPIC_7 = 'control_valve_gas_sizing_choked_flow_critical_pressure_ratio'
TOPIC_8 = 'control_valve_cavitation_flashing_choked_flow_damage_prevention'

SOURCE_DIR = ROOT / "rubrics" / "topic_packs" / TOPIC
GENERATED_DIR = ROOT / "rubrics" / "generated"
TOPIC_SHEET = (
    ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"
)

EXPECTED_ANCHOR_IDS = ['control_valve_noise_scope', 'process_flow_vs_accessory_noise', 'source_path_receiver_hierarchy', 'sound_power_level_definition', 'sound_pressure_level_definition', 'decibel_logarithmic_scale', 'independent_source_logarithmic_sum', 'identical_source_doubling', 'pressure_amplitude_doubling', 'overall_spectrum_octave_distinction', 'a_weighting_dba_meaning', 'sound_power_pressure_boundary', 'aerodynamic_turbulent_jet_noise', 'aerodynamic_expansion_shock_noise', 'gas_choked_regime_noise_input', 'gas_outlet_velocity_mach_geometry', 'topic7_aerodynamic_noise_handoff', 'hydrodynamic_turbulence_noise', 'cavitation_bubble_collapse_noise', 'flashing_two_phase_noise', 'topic8_hydrodynamic_noise_handoff', 'acoustic_power_pipe_radiation_path', 'pipe_transmission_loss_dependency', 'external_spl_observation_condition', 'prediction_standard_vendor_method', 'multi_hole_jet_division', 'multi_stage_pressure_ratio_velocity_control', 'diffuser_pressure_drop_distribution', 'silencer_insulation_enclosure_path_treatment', 'valve_size_capacity_velocity_tradeoff', 'low_noise_trim_capacity_rangeability_tradeoff', 'plugging_erosion_maintenance_tradeoff', 'operating_case_noise_matrix', 'multiple_source_parallel_bypass_combination', 'field_measurement_background_correction', 'prediction_measurement_gap_diagnosis', 'occupational_limit_local_standard', 'vendor_crosscheck_noise']
EXPECTED_FATAL_IDS = ['control_valve_sound_power_equals_sound_pressure', 'control_valve_db_levels_arithmetic_sum', 'control_valve_identical_source_doubling_plus_six_db', 'control_valve_pressure_doubling_plus_three_db', 'control_valve_dba_equals_unweighted_db', 'control_valve_overall_level_equals_spectrum', 'control_valve_distance_does_not_affect_spl', 'control_valve_gas_noise_independent_of_flow_pressure', 'control_valve_choked_gas_means_no_noise', 'control_valve_universal_outlet_mach_limit', 'control_valve_cavitation_noise_equals_flashing_noise', 'control_valve_hydrodynamic_noise_only_cavitation', 'control_valve_flashing_noise_is_bubble_collapse', 'control_valve_pipe_transmission_loss_irrelevant', 'control_valve_insulation_always_reduces_all_noise', 'control_valve_low_noise_trim_eliminates_noise', 'control_valve_larger_size_always_quieter', 'control_valve_diffuser_has_no_capacity_effect', 'control_valve_mitigation_reductions_arithmetic_sum', 'control_valve_single_normal_noise_case_sufficient', 'control_valve_universal_dba_limit']
EXPECTED_MAJOR_IDS = ['control_valve_exact_iec_noise_equation_without_edition', 'control_valve_fixed_acoustic_efficiency_factor', 'control_valve_fixed_peak_frequency', 'control_valve_fixed_pipe_transmission_loss', 'control_valve_fixed_mach_acceptance_threshold', 'control_valve_fixed_low_noise_stage_hole_design', 'control_valve_field_measurement_without_conditions', 'control_valve_independent_source_assumption_without_check', 'control_valve_prediction_exact_field_guarantee']

BROAD_ALIASES = {
    "noise",
    "dB",
    "dBA",
    "sound",
    "sound pressure",
    "sound power",
    "Mach",
    "silencer",
    "diffuser",
    "low-noise trim",
    "aerodynamic",
    "hydrodynamic",
}

POSITIVE_ANSWER = """
Process-flow noise와 actuator·positioner accessory noise를 구분한다.
Source path receiver hierarchy를 적용한다. Sound power level은 acoustic
power ratio의 10 log10이고 sound pressure level은 rms acoustic pressure
ratio의 20 log10이다. Independent source는 logarithmic level sum으로
결합하고 identical source doubling은 plus 3 dB이다. Overall level,
octave band와 A weighting dBA를 구분한다. Aerodynamic noise는
compressible turbulent jet, high pressure ratio, choked gas와 shock
related noise를 검토하고 Topic 7 gas capacity, xT xTP, expansion factor Y,
selected travel을 인계한다. Hydrodynamic turbulence noise, cavitation
bubble collapse와 flashing persistent two phase flow를 구분하고 Topic 8
liquid choked, FL FP FLP를 인계한다. Internal acoustic power, pipe wall,
pipe transmission loss, external SPL, distance와 measurement location을
검토한다. Multi hole trim의 jet division, multi stage trim의 pressure
ratio staging과 velocity control, diffuser pressure drop distribution,
silencer acoustic insulation enclosure를 비교한다. Minimum normal
maximum과 startup shutdown, parallel valve logarithmic combination,
field noise measurement, background correction, vendor noise prediction과
selected travel을 교차 검증한다. Topic 10, Topic 11, Topic 14와 Topic 16
경계를 유지한다.
""".strip()

SAFE_ANSWER = """
Sound power와 sound pressure는 서로 다른 acoustic quantity이다.
Independent source level은 logarithmic sum으로 합산한다. 동일 source
두 개는 약 3 dB 증가하고 pressure amplitude 두 배는 약 6 dB 증가한다.
Aerodynamic turbulent jet와 hydrodynamic cavitation·flashing을 구분한다.
Pipe transmission loss와 external SPL observation condition을 적용한다.
""".strip()

NEGATIVE_SAMPLES = {
    "control_valve_sound_power_equals_sound_pressure": (
        "sound power level, acoustic power, source energy, sound pressure "
        "level, observation point와 transmission loss를 설명하지만 두 "
        "quantity는 항상 동일하다고 주장한다."
    ),
    "control_valve_db_levels_arithmetic_sum": (
        "independent source, logarithmic level sum, multiple noise sources, "
        "energy addition과 dB를 설명하지만 level을 산술합한다고 주장한다."
    ),
    "control_valve_identical_source_doubling_plus_six_db": (
        "identical source doubling, two independent sources, power doubling, "
        "logarithmic addition과 plus 3 dB를 설명하지만 실제 증가는 "
        "6 dB라고 주장한다."
    ),
    "control_valve_flashing_noise_is_bubble_collapse": (
        "flashing noise, persistent two phase flow, droplet impact, broadband "
        "noise와 vibration을 설명하지만 핵심은 bubble collapse라고 "
        "주장한다."
    ),
    "control_valve_pipe_transmission_loss_irrelevant": (
        "internal acoustic power, pipe wall, sound radiation, pipe "
        "transmission loss와 external sound를 설명하지만 transmission "
        "loss는 불필요하다고 주장한다."
    ),
    "control_valve_low_noise_trim_eliminates_noise": (
        "low noise trim tradeoff, Cv capacity, rangeability, noise reduction과 "
        "trim selection을 설명하지만 모든 condition에서 noise를 "
        "0으로 만든다고 주장한다."
    ),
}

SEMANTIC_CLUSTERS = {
    "quantity": (
        "sound power level",
        "10 log10",
        "sound pressure level",
        "20 log10",
    ),
    "level_sum": (
        "independent source",
        "logarithmic level sum",
        "identical source doubling",
        "plus 3 db",
    ),
    "spectrum": (
        "overall level",
        "octave band",
        "a weighting dba",
    ),
    "aerodynamic": (
        "aerodynamic noise",
        "compressible turbulent jet",
        "choked gas",
        "shock related noise",
    ),
    "hydrodynamic": (
        "hydrodynamic turbulence noise",
        "cavitation bubble collapse",
        "flashing persistent two phase flow",
    ),
    "handoff": (
        "topic 7",
        "xt xtp",
        "topic 8",
        "fl fp flp",
    ),
    "transmission": (
        "internal acoustic power",
        "pipe transmission loss",
        "external spl",
        "measurement location",
    ),
    "mitigation": (
        "multi hole trim",
        "jet division",
        "multi stage trim",
        "velocity control",
        "diffuser pressure drop distribution",
    ),
    "cases": (
        "minimum normal maximum",
        "startup shutdown",
        "parallel valve logarithmic combination",
        "background correction",
    ),
    "boundaries": (
        "topic 10",
        "topic 11",
        "topic 14",
        "topic 16",
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


def sound_power_level(
    power: float,
    reference: float,
) -> float:
    if power <= 0 or reference <= 0:
        raise ValueError
    return 10.0 * math.log10(power / reference)


def sound_pressure_level(
    pressure: float,
    reference: float,
) -> float:
    if pressure <= 0 or reference <= 0:
        raise ValueError
    return 20.0 * math.log10(
        pressure / reference
    )


def level_sum(
    levels: list[float],
) -> float:
    if not levels:
        raise ValueError
    return 10.0 * math.log10(
        sum(
            10.0 ** (level / 10.0)
            for level in levels
        )
    )


def a_weighted_sum(
    levels: list[float],
    corrections: list[float],
) -> float:
    if (
        not levels
        or len(levels) != len(corrections)
    ):
        raise ValueError
    return 10.0 * math.log10(
        sum(
            10.0
            ** ((level + correction) / 10.0)
            for level, correction in zip(
                levels,
                corrections,
            )
        )
    )


def distance_correct(
    level1: float,
    r1: float,
    r2: float,
) -> float:
    if r1 <= 0 or r2 <= 0:
        raise ValueError
    return level1 - 20.0 * math.log10(
        r2 / r1
    )


def external_level(
    internal: float,
    transmission_loss: float,
    correction: float = 0.0,
) -> float:
    if transmission_loss < 0:
        raise ValueError
    return (
        internal
        - transmission_loss
        + correction
    )


def apply_distinct_mitigations(
    base_level: float,
    reductions: list[tuple[str, float]],
) -> float:
    seen: set[str] = set()
    total_reduction = 0.0
    for mechanism, reduction in reductions:
        if not mechanism or reduction < 0:
            raise ValueError
        if mechanism in seen:
            raise ValueError
        seen.add(mechanism)
        total_reduction += reduction
    return base_level - total_reduction


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
            21,
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
            "PRINCIPLE_INTERPRETATION",
        )

    def test_acoustic_quantity_marker_contracts(
        self,
    ) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        for marker in (
            "10·log10",
            "source-energy",
        ):
            self.assertIn(
                marker,
                by_id[
                    "sound_power_level_definition"
                ],
            )
        for marker in (
            "20·log10",
            "observation-point",
        ):
            self.assertIn(
                marker,
                by_id[
                    "sound_pressure_level_definition"
                ],
            )
        self.assertIn(
            "3.01 dB",
            by_id[
                "identical_source_doubling"
            ],
        )
        self.assertIn(
            "6.02 dB",
            by_id[
                "pressure_amplitude_doubling"
            ],
        )
        self.assertIn(
            "frequency-weighted",
            by_id[
                "a_weighting_dba_meaning"
            ],
        )

    def test_aerodynamic_marker_and_topic7_handoff(
        self,
    ) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        self.assertIn(
            "compressible jet",
            by_id[
                "aerodynamic_turbulent_jet_noise"
            ],
        )
        self.assertIn(
            "shock-related noise",
            by_id[
                "aerodynamic_expansion_shock_noise"
            ],
        )
        handoff = by_id[
            "topic7_aerodynamic_noise_handoff"
        ]
        for marker in (
            "Topic 7",
            "xT",
            "xTP",
            "selected travel",
        ):
            self.assertIn(marker, handoff)

    def test_hydrodynamic_marker_and_topic8_handoff(
        self,
    ) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        self.assertIn(
            "Single-phase liquid",
            by_id[
                "hydrodynamic_turbulence_noise"
            ],
        )
        self.assertIn(
            "bubble collapse",
            by_id[
                "cavitation_bubble_collapse_noise"
            ],
        )
        self.assertIn(
            "persistent two-phase flow",
            by_id[
                "flashing_two_phase_noise"
            ],
        )
        handoff = by_id[
            "topic8_hydrodynamic_noise_handoff"
        ]
        for marker in (
            "Topic 8",
            "liquid choked",
            "FL",
        ):
            self.assertIn(marker, handoff)

    def test_propagation_and_mitigation_markers(
        self,
    ) -> None:
        by_id = {
            row["id"]: row["statement"]
            for row in self.fact["anchors"]
        }
        self.assertIn(
            "pipe wall",
            by_id[
                "acoustic_power_pipe_radiation_path"
            ],
        )
        self.assertIn(
            "Pipe transmission loss",
            by_id[
                "pipe_transmission_loss_dependency"
            ],
        )
        self.assertIn(
            "Multi-hole",
            by_id[
                "multi_hole_jet_division"
            ],
        )
        self.assertIn(
            "Multi-stage",
            by_id[
                "multi_stage_pressure_ratio_velocity_control"
            ],
        )
        self.assertIn(
            "Diffuser",
            by_id[
                "diffuser_pressure_drop_distribution"
            ],
        )

    def test_operating_measurement_and_literal_boundaries(
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
            "Minimum",
            "normal",
            "maximum",
            "startup",
            "shutdown",
            "background correction",
            "Topic 10",
            "Topic 11",
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
            "control_valve_sound_power_equals_sound_pressure":
                "서로 다른 acoustic quantity",
            "control_valve_db_levels_arithmetic_sum":
                "10·log10",
            "control_valve_identical_source_doubling_plus_six_db":
                "3.01 dB",
            "control_valve_pressure_doubling_plus_three_db":
                "6.02 dB",
            "control_valve_dba_equals_unweighted_db":
                "frequency weighting",
            "control_valve_choked_gas_means_no_noise":
                "zero flow가 아니며",
            "control_valve_flashing_noise_is_bubble_collapse":
                "persistent two-phase flow",
            "control_valve_pipe_transmission_loss_irrelevant":
                "pipe transmission loss",
            "control_valve_low_noise_trim_eliminates_noise":
                "0으로 보장하지 않는다",
            "control_valve_single_normal_noise_case_sufficient":
                "Minimum·normal·maximum",
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
            TOPIC_2,
            TOPIC_3,
            TOPIC_4,
            TOPIC_5,
            TOPIC_6,
            TOPIC_7,
            TOPIC_8,
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

    def test_acoustic_quantities_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Control valve의 sound power, sound pressure, dB, dBA와 octave spectrum을 구분하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_multiple_source_logarithmic_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Parallel valve 두 대의 independent source level을 logarithmic sum으로 계산하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_aerodynamic_noise_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Choked gas valve의 turbulent jet, shock-cell, outlet Mach와 aerodynamic noise를 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_hydrodynamic_noise_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Liquid turbulence, cavitation bubble collapse와 flashing two-phase noise를 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_transmission_external_spl_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Internal acoustic power가 pipe transmission loss를 거쳐 external SPL로 방사되는 과정을 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_low_noise_trim_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Multi-hole jet division과 multi-stage pressure-ratio·velocity control 저소음 트림을 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_diffuser_and_path_treatment_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Diffuser의 pressure-drop 분담과 silencer·insulation·enclosure를 비교하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_operating_case_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Minimum·normal·maximum 및 startup·shutdown condition별 valve noise를 평가하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_measurement_gap_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Vendor octave prediction과 field dBA measurement의 차이 및 background correction을 진단하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_integrated_noise_selection_route(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Gas·liquid regime, selected travel, low-noise trim과 pipe treatment를 이용한 valve noise 대책을 설명하시오.",
                TOPIC,
            ),
            TOPIC,
        )

    def test_topic7_gas_capacity_boundary(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Gas standard volume, Fγ, xT, xTP와 expansion factor Y를 이용한 choked capacity sizing을 설명하시오.",
                TOPIC_7,
            ),
            TOPIC_7,
        )

    def test_topic8_liquid_regime_boundary(
        self,
    ) -> None:
        self.assert_primary(
            self.route(
                "Pvc, Pv, P2, FF, FL과 FLP로 cavitation, flashing과 liquid choked limit를 판정하시오.",
                TOPIC_8,
            ),
            TOPIC_8,
        )

    def test_topic2_to_topic6_boundaries(
        self,
    ) -> None:
        cases = [
            (
                "Linear, equal-percentage와 quick-opening characteristic를 비교하시오.",
                TOPIC_2,
            ),
            (
                "Deadband, stiction, response time과 positioner hunting을 설명하시오.",
                TOPIC_3,
            ),
            (
                "Globe·rotary body와 pneumatic·electric actuator를 비교하시오.",
                TOPIC_4,
            ),
            (
                "Valve Authority, rangeability와 installed gain을 설명하시오.",
                TOPIC_5,
            ),
            (
                "비초크 액체 Cv·Kv, SG와 Reynolds correction을 설명하시오.",
                TOPIC_6,
            ),
        ]
        for question, expected in cases:
            with self.subTest(
                expected=expected
            ):
                self.assert_primary(
                    self.route(
                        question,
                        expected,
                    ),
                    expected,
                )

    def test_question_only_routing_survives_answer_contamination(
        self,
    ) -> None:
        result = self.route(
            "Gas Fγ, xT, xTP와 expansion factor Y를 이용한 choked capacity sizing을 설명하시오.",
            TOPIC_7,
            answer_text=(
                "sound power, sound pressure, dBA, "
                "aerodynamic noise, pipe transmission "
                "loss, multi-stage low-noise trim과 "
                "background correction을 상세히 쓴다."
            ),
        )
        self.assert_primary(
            result,
            TOPIC_7,
        )
        aliases = set(
            self.answer_by_topic[
                TOPIC
            ]["routing_aliases"]
        )
        self.assertFalse(
            BROAD_ALIASES & aliases
        )


class AcousticFormulaSemanticRegressionTests(
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

    def test_sound_power_numeric_domain_and_direction(
        self,
    ) -> None:
        self.assertTrue(
            math.isclose(
                sound_power_level(
                    1.0,
                    1.0,
                ),
                0.0,
            )
        )
        self.assertTrue(
            math.isclose(
                sound_power_level(
                    2.0,
                    1.0,
                ),
                10.0
                * math.log10(2.0),
            )
        )
        self.assertTrue(
            math.isclose(
                sound_power_level(
                    10.0,
                    1.0,
                ),
                10.0,
            )
        )
        with self.assertRaises(
            ValueError
        ):
            sound_power_level(
                0.0,
                1.0,
            )

    def test_sound_pressure_numeric_domain_and_direction(
        self,
    ) -> None:
        self.assertTrue(
            math.isclose(
                sound_pressure_level(
                    1.0,
                    1.0,
                ),
                0.0,
            )
        )
        self.assertTrue(
            math.isclose(
                sound_pressure_level(
                    2.0,
                    1.0,
                ),
                20.0
                * math.log10(2.0),
            )
        )
        self.assertTrue(
            math.isclose(
                sound_pressure_level(
                    10.0,
                    1.0,
                ),
                20.0,
            )
        )
        with self.assertRaises(
            ValueError
        ):
            sound_pressure_level(
                1.0,
                0.0,
            )

    def test_independent_level_sum_identity_and_monotonicity(
        self,
    ) -> None:
        self.assertTrue(
            math.isclose(
                level_sum([80.0]),
                80.0,
            )
        )
        self.assertGreater(
            level_sum(
                [80.0, 70.0]
            ),
            80.0,
        )
        self.assertLess(
            level_sum(
                [80.0, 70.0]
            ),
            90.0,
        )
        with self.assertRaises(
            ValueError
        ):
            level_sum([])

    def test_identical_source_count_contract(
        self,
    ) -> None:
        self.assertTrue(
            math.isclose(
                level_sum(
                    [80.0, 80.0]
                ),
                80.0
                + 10.0
                * math.log10(2.0),
            )
        )
        self.assertTrue(
            math.isclose(
                level_sum(
                    [80.0] * 10
                ),
                90.0,
            )
        )

    def test_a_weighted_sum_direction_and_domain(
        self,
    ) -> None:
        unweighted = level_sum(
            [80.0, 80.0]
        )
        weighted = a_weighted_sum(
            [80.0, 80.0],
            [-3.0, 0.0],
        )
        self.assertLess(
            weighted,
            unweighted,
        )
        with self.assertRaises(
            ValueError
        ):
            a_weighted_sum(
                [80.0],
                [],
            )

    def test_conditional_distance_direction_and_domain(
        self,
    ) -> None:
        at_two = distance_correct(
            90.0,
            1.0,
            2.0,
        )
        at_four = distance_correct(
            90.0,
            1.0,
            4.0,
        )
        self.assertTrue(
            math.isclose(
                at_two,
                90.0
                - 20.0
                * math.log10(2.0),
            )
        )
        self.assertLess(
            at_four,
            at_two,
        )
        with self.assertRaises(
            ValueError
        ):
            distance_correct(
                90.0,
                0.0,
                2.0,
            )

    def test_transmission_loss_direction_and_domain(
        self,
    ) -> None:
        self.assertLess(
            external_level(
                100.0,
                20.0,
            ),
            external_level(
                100.0,
                10.0,
            ),
        )
        with self.assertRaises(
            ValueError
        ):
            external_level(
                100.0,
                -1.0,
            )

    def test_distinct_mitigation_no_double_count_contract(
        self,
    ) -> None:
        result = apply_distinct_mitigations(
            100.0,
            [
                ("source_trim", 5.0),
                ("pipe_insulation", 3.0),
            ],
        )
        self.assertTrue(
            math.isclose(
                result,
                92.0,
            )
        )
        with self.assertRaises(
            ValueError
        ):
            apply_distinct_mitigations(
                100.0,
                [
                    ("source_trim", 5.0),
                    ("source_trim", 3.0),
                ],
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
            "control_valve_db_levels_arithmetic_sum"
        )
        answer_text = (
            "independent source, logarithmic level sum, "
            "multiple noise sources, energy addition과 "
            "dB를 설명하면서 level은 산술합한다고 "
            "주장한다."
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
                "Independent source dB level을 "
                "산술합하였다."
            ),
            "findings": [{
                "candidate_id":
                    candidates[0]["id"],
                "rule_id": rule_id,
                "severity": "fatal",
                "message":
                    "Decibel arithmetic-sum error",
                "correct_rule": (
                    "Independent source level은 "
                    "10·log10[Σ10^(Li/10)] 구조로 "
                    "합산한다."
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
                "Sound power·pressure와 "
                "logarithmic level을 정확히 "
                "구분하였다."
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
