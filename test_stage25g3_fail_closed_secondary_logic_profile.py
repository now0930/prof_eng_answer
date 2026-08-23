from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import logic_check_evaluator as evaluator

PRIMARY = (
    "instrumentation_control_software_lifecycle_"
    "v_model_traceability_verification_validation"
)
SECONDARY = (
    "sis_sil_safety_software_independence_"
    "systematic_failure_verification_validation"
)
ACTIVATION_ID = "sw05_claim_triggered_secondary_profile_v1"
SIL_FATAL_ID = "sw05_fatal_sil_expanded_as_safety_instrument_level"
VOTING_FATAL_ID = "sw05_fatal_software_test_mapped_to_voting_architecture"


def topic_check(topic_id: str) -> dict:
    return {
        "topic_id": topic_id,
        "topic_name": topic_id,
        "enabled": False,
        "topic_aliases": [topic_id],
        "fatal_checks": [],
        "major_checks": [],
        "question_type_checks": [],
        "next_practice_points": [],
    }


def profile(topic_id: str, activation: bool) -> dict:
    rules = []
    if activation:
        rules = [
            {
                "id": ACTIVATION_ID,
                "activation_scope": (
                    "claim_triggered_secondary_profile_v1"
                ),
                "strong_pattern_groups": [
                    {"id": "sil", "patterns": [r"(?<![A-Za-z0-9_])SIL(?![A-Za-z0-9_])"]},
                    {"id": "hft", "patterns": [r"(?<![A-Za-z0-9_])HFT(?![A-Za-z0-9_])"]},
                    {
                        "id": "voting",
                        "patterns": [r"(?<![A-Za-z0-9_])1oo2(?![A-Za-z0-9_])", r"(?<![A-Za-z0-9_])2oo3(?![A-Za-z0-9_])"],
                    },
                ],
                "relation_pattern_groups": [
                    {
                        "id": "systematic",
                        "patterns": [
                            r"systematic\s+failure",
                            r"체계적\s*고장",
                        ],
                    }
                ],
                "min_strong_groups": 2,
                "single_strong_requires_relation_group": True,
                "max_secondary_profiles": 1,
                "score_effect_requirement": "diagnostic_only",
            }
        ]

    return {
        "topic_id": topic_id,
        "enabled": True,
        "display_name": topic_id,
        "difficulty": "THEORY_CORE",
        "cap_policy": {},
        "secondary_profile_activation": {
            "rules": rules,
            "key_terms": [],
            "max_candidates": 12,
            "nearby_window": 1,
        },
        "fatal_conditions": [],
        "major_checks": [],
        "truth_schema": [],
        "safe_conditions": [],
        "false_positive_cautions": [],
        "next_practice_points": [],
        "feedback_templates": {},
        "output_contract": {"finding_fields": ["id", "severity"]},
        "score_policy": {
            "direct_score_application": False,
            "affected_layers": ["B", "C"],
            "direct_d_e_effect": "none",
        },
    }


class Stage25G3Test(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.logic_bank = root / "logic.json"
        self.profile_bank = root / "profiles.json"

        self.logic_bank.write_text(
            json.dumps(
                {
                    "topic_logic_checks": [
                        topic_check(PRIMARY),
                        topic_check(SECONDARY),
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.profile_bank.write_text(
            json.dumps(
                {
                    "profiles": [
                        profile(PRIMARY, False),
                        profile(SECONDARY, True),
                    ]
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def fake_verify(_answer: str, topic_id: str, **_kwargs) -> dict:
        finding = []
        if topic_id == SECONDARY:
            finding = [
                {
                    "id": SIL_FATAL_ID,
                    "rule_id": SIL_FATAL_ID,
                    "source_rule_id": SIL_FATAL_ID,
                    "severity": "fatal",
                    "message": "SIL 약어 오정의",
                    "correct_rule": "SIL은 Safety Integrity Level이다.",
                    "affected_layers": ["C"],
                }
            ]
        return {
            "findings": finding,
            "canonical_axis_alignment_evaluation": {
                "version": "canonical_axis_alignment_v1",
                "alignments": [],
            },
        }

    def evaluate(self, text: str) -> dict:
        with patch(
            "logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH",
            self.profile_bank,
        ), patch(
            "logic_llm_verifier.verify_logic_with_llm",
            side_effect=self.fake_verify,
        ):
            return evaluator.evaluate_logic_checks(
                text,
                {
                    "logic_check_topic_id": PRIMARY,
                    "topic_id": PRIMARY,
                },
                self.logic_bank,
            )

    def test_secondary_selected_and_merged(self) -> None:
        result = self.evaluate(
            "[문제] V-Model을 설명하시오.\n"
            "[답안] SIL은 Safety Instrument Level이며 "
            "HFT는 체계적 고장 검증에 사용한다."
        )
        self.assertEqual(result["topic_id"], PRIMARY)
        self.assertEqual(
            result["evaluated_topic_ids"],
            [PRIMARY, SECONDARY],
        )
        self.assertTrue(result["fatal_error_detected"])
        self.assertEqual(result["mode"], "fatal")
        secondary = [
            row
            for row in result["findings"]
            if row.get("secondary_profile")
        ]
        self.assertEqual([row["id"] for row in secondary], [SIL_FATAL_ID])
        self.assertEqual(secondary[0]["source_topic_id"], SECONDARY)
        self.assertEqual(
            result["score_policy"]["secondary_profile_score_effect"],
            "diagnostic_only",
        )
        self.assertFalse(
            result["score_policy"][
                "secondary_profile_direct_score_application"
            ]
        )

    def test_normal_vmodel_not_selected(self) -> None:
        result = self.evaluate(
            "[문제] V-Model을 설명하시오.\n"
            "[답안] 요구사항, 단위시험, 통합시험, 시스템시험을 "
            "양방향 RTM으로 추적한다."
        )
        self.assertNotIn("secondary_profile_selection", result)
        self.assertFalse(result["fatal_error_detected"])

    def test_rule_authority_does_not_require_profile_score_effect(self) -> None:
        secondary_profile = profile(SECONDARY, True)
        self.assertNotIn(
            "score_effect",
            secondary_profile["score_policy"],
        )
        rule = secondary_profile[
            "secondary_profile_activation"
        ]["rules"][0]
        self.assertEqual(
            rule["score_effect_requirement"],
            "diagnostic_only",
        )

        with patch(
            "logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH",
            self.profile_bank,
        ):
            selected = (
                evaluator._select_claim_triggered_secondary_profiles(
                    "SIL은 Safety Instrument Level이며 HFT는 체계적 고장이다.",
                    PRIMARY,
                    [
                        topic_check(PRIMARY),
                        topic_check(SECONDARY),
                    ],
                )
            )

        self.assertEqual(
            [row["topic_id"] for row in selected],
            [SECONDARY],
        )
        self.assertEqual(
            selected[0]["score_effect"],
            "diagnostic_only",
        )

    def test_ascii_token_boundaries_match_korean_suffixes(self) -> None:
        rule = profile(SECONDARY, True)[
            "secondary_profile_activation"
        ]["rules"][0]
        match = evaluator._secondary_profile_rule_match(
            "SIL은 Safety Instrument Level이며 HFT는 체계적 고장 검증이다.",
            rule,
        )
        self.assertTrue(match["matched"])
        self.assertEqual(
            set(match["strong_groups"]),
            {"sil", "hft"},
        )
        self.assertEqual(
            match["relation_groups"],
            ["systematic"],
        )

    def test_controls_fail_closed(self) -> None:
        rule = profile(SECONDARY, True)[
            "secondary_profile_activation"
        ]["rules"][0]
        controls = [
            "HIL은 실제 제어기와 실시간 Plant Model을 연결한다.",
            "FAT SAT Loop test와 시운전 절차를 설명한다.",
            "HMI SCADA Alarm rationalization을 설명한다.",
            "2차계 감쇠비와 오버슈트 관계를 설명한다.",
            "정적분석, 동적분석과 회귀시험을 설명한다.",
            "V-Model의 단위시험과 통합시험을 설명한다.",
        ]
        for text in controls:
            with self.subTest(text=text):
                match = evaluator._secondary_profile_rule_match(
                    text,
                    rule,
                )
                self.assertFalse(match["matched"])

    def test_source_contract(self) -> None:
        source = json.loads(
            (
                Path(__file__).resolve().parent
                / "rubrics"
                / "topic_packs"
                / SECONDARY
                / "logic_check.json"
            ).read_text(encoding="utf-8")
        )
        det_ids = {
            row.get("id")
            for row in source["deterministic_checks"]["fatal_checks"]
            if isinstance(row, dict)
        }
        self.assertIn(SIL_FATAL_ID, det_ids)
        self.assertIn(VOTING_FATAL_ID, det_ids)
        rules = source["llm_profile"]["secondary_profile_activation"]["rules"]
        self.assertEqual(
            sum(
                isinstance(row, dict)
                and row.get("id") == ACTIVATION_ID
                for row in rules
            ),
            1,
        )


if __name__ == "__main__":
    unittest.main()
