#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import logic_check_evaluator


BASELINE_SHA = "c526f2cb64f2f794df9195cd622949f17f6842e0"

DETERMINISTIC_TOPIC_ID = (
    "second_order_lag_response_by_damping_ratio"
)
PROFILE_ONLY_TOPIC_ID = (
    "feedback_system_closed_loop_"
    "sensitivity_steady_state_error"
)
STAGE22_TOPIC_ID = (
    "instrumentation_control_software_lifecycle_"
    "v_model_traceability_verification_validation"
)


def _grade(topic_id: str) -> dict:
    return {
        "topic_id": topic_id,
        "logic_check_topic_id": topic_id,
        "total_score": 20.0,
        "max_score": 25.0,
        "difficulty_strategy": {
            "topic_id": topic_id,
        },
    }


def _topic(
    topic_id: str,
    *,
    enabled: bool,
) -> dict:
    return {
        "topic_id": topic_id,
        "topic_name": topic_id,
        "topic_aliases": [],
        "enabled": enabled,
        "fatal_checks": [],
        "major_checks": [],
        "question_type_checks": [],
        "next_practice_points": [],
    }


def _profile_result(
    topic_id: str,
    *,
    findings: list[dict] | None = None,
) -> dict:
    rows = findings or []
    fatal = any(
        isinstance(row, dict)
        and row.get("severity") == "fatal"
        for row in rows
    )
    return {
        "applicable": True,
        "engine": "llm_verifier_profile_v1",
        "topic_id": topic_id,
        "verdict": "fatal" if fatal else "pass",
        "confidence": 0.99,
        "checks": [],
        "findings": rows,
        "fatal_error_detected": fatal,
        "recommended_ceiling": None,
        "mode": "fatal" if fatal else "pass",
        "reason": "dispatch contract fixture",
    }


class Stage22ProfileDispatchContractTest(
    unittest.TestCase
):
    """Pin baseline enabled semantics plus Stage22 profile capability.

    The generated logic bank uses:
    - enabled=True for deterministic-capable topics;
    - enabled=False for profile-only topics.

    Stage22 additionally allows an active profile on an enabled=True
    topic. That profile must not suppress deterministic checks or cause
    a second legacy/claim-verifier LLM pass.
    """

    @staticmethod
    def _write_bank(
        directory: str,
        topic_check: dict,
    ) -> Path:
        path = Path(directory) / "logic_checks.json"
        path.write_text(
            json.dumps(
                {
                    "version": (
                        "stage22_profile_dispatch_"
                        "contract_v2"
                    ),
                    "topic_logic_checks": [
                        topic_check,
                    ],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return path

    def test_generated_bank_preserves_enabled_semantics(
        self,
    ) -> None:
        bank = json.loads(
            logic_check_evaluator.DEFAULT_BANK.read_text(
                encoding="utf-8"
            )
        )
        topic_rows = bank.get("topic_logic_checks") or []

        by_topic: dict[str, list[dict]] = {}
        for row in topic_rows:
            if not isinstance(row, dict):
                continue
            topic_id = str(row.get("topic_id") or "")
            by_topic.setdefault(topic_id, []).append(row)

        for topic_id in (
            DETERMINISTIC_TOPIC_ID,
            PROFILE_ONLY_TOPIC_ID,
            STAGE22_TOPIC_ID,
        ):
            self.assertEqual(
                len(by_topic.get(topic_id, [])),
                1,
                msg=f"expected one generated row: {topic_id}",
            )

        self.assertIs(
            by_topic[DETERMINISTIC_TOPIC_ID][0].get(
                "enabled"
            ),
            True,
        )
        self.assertIs(
            by_topic[PROFILE_ONLY_TOPIC_ID][0].get(
                "enabled"
            ),
            False,
        )
        self.assertIs(
            by_topic[STAGE22_TOPIC_ID][0].get(
                "enabled"
            ),
            True,
        )

    def test_enabled_true_active_profile_keeps_deterministic_and_single_llm_route(
        self,
    ) -> None:
        answer = "ζ=1은 과감쇠라고 설명하였다."
        sentinel = {
            "id": "dispatch_contract_deterministic_fatal",
            "severity": "fatal",
            "message": "deterministic path executed",
            "correct_rule": (
                "enabled=True keeps deterministic checks"
            ),
            "affected_layers": ["C"],
            "recommended_ceiling": 10.0,
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            bank_path = self._write_bank(
                temp_dir,
                _topic(
                    DETERMINISTIC_TOPIC_ID,
                    enabled=True,
                ),
            )

            with patch(
                "logic_llm_verifier."
                "load_logic_check_profile",
                return_value={
                    "topic_id": DETERMINISTIC_TOPIC_ID,
                    "display_name": "Damping",
                    "enabled": True,
                    "next_practice_points": [],
                },
            ) as profile_loader, patch(
                "logic_llm_verifier."
                "verify_logic_with_llm",
                return_value=_profile_result(
                    DETERMINISTIC_TOPIC_ID,
                ),
            ) as profile_verifier, patch.object(
                logic_check_evaluator,
                "_evaluate_topic_fatal_checks_with_llm",
                side_effect=AssertionError(
                    "active profile reached legacy "
                    "semantic fallback"
                ),
            ) as legacy_fallback, patch.object(
                logic_check_evaluator,
                "_evaluate_second_order_deterministic_checks",
                return_value=[sentinel],
            ) as deterministic, patch.object(
                logic_check_evaluator,
                "_apply_second_order_claim_evaluator",
                side_effect=AssertionError(
                    "active profile triggered a second "
                    "claim-verifier route"
                ),
            ) as claim_evaluator:
                result = (
                    logic_check_evaluator
                    .evaluate_logic_checks(
                        answer,
                        grade=_grade(
                            DETERMINISTIC_TOPIC_ID
                        ),
                        bank_path=bank_path,
                    )
                )

        profile_loader.assert_called_once_with(
            DETERMINISTIC_TOPIC_ID
        )
        profile_verifier.assert_called_once()
        deterministic.assert_called_once_with(answer)
        legacy_fallback.assert_not_called()
        claim_evaluator.assert_not_called()

        self.assertTrue(
            result.get("fatal_error_detected")
        )
        self.assertEqual(
            result.get("mode"),
            "fatal",
        )
        self.assertIn(
            sentinel["id"],
            {
                row.get("id")
                for row in result.get("findings", [])
                if isinstance(row, dict)
            },
        )

    def test_enabled_false_active_profile_is_profile_only(
        self,
    ) -> None:
        answer = (
            "폐루프가 2차이면 Type 2 시스템이다."
        )
        profile_fatal = {
            "id": (
                "llm_profile_system_type_"
                "from_closed_loop_order"
            ),
            "source_rule_id": (
                "system_type_from_closed_loop_order"
            ),
            "severity": "fatal",
            "message": (
                "시스템 형을 폐루프 차수로 "
                "잘못 정의했다."
            ),
            "correct_rule": (
                "시스템 형은 개루프 L(s)의 "
                "원점 극 수이다."
            ),
            "affected_layers": ["C"],
            "evidence": answer,
            "confidence": 0.99,
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            bank_path = self._write_bank(
                temp_dir,
                _topic(
                    PROFILE_ONLY_TOPIC_ID,
                    enabled=False,
                ),
            )

            with patch(
                "logic_llm_verifier."
                "load_logic_check_profile",
                return_value={
                    "topic_id": PROFILE_ONLY_TOPIC_ID,
                    "display_name": "System Type",
                    "enabled": True,
                    "next_practice_points": [],
                },
            ) as profile_loader, patch(
                "logic_llm_verifier."
                "verify_logic_with_llm",
                return_value=_profile_result(
                    PROFILE_ONLY_TOPIC_ID,
                    findings=[profile_fatal],
                ),
            ) as profile_verifier, patch.object(
                logic_check_evaluator,
                "_evaluate_topic_fatal_checks_with_llm",
                side_effect=AssertionError(
                    "profile-only topic reached legacy "
                    "semantic fallback"
                ),
            ) as legacy_fallback, patch.object(
                logic_check_evaluator,
                "_evaluate_second_order_deterministic_checks",
                side_effect=AssertionError(
                    "profile-only topic reached "
                    "deterministic checks"
                ),
            ) as deterministic:
                result = (
                    logic_check_evaluator
                    .evaluate_logic_checks(
                        answer,
                        grade=_grade(
                            PROFILE_ONLY_TOPIC_ID
                        ),
                        bank_path=bank_path,
                    )
                )

        profile_loader.assert_called_once_with(
            PROFILE_ONLY_TOPIC_ID
        )
        profile_verifier.assert_called_once()
        legacy_fallback.assert_not_called()
        deterministic.assert_not_called()

        self.assertTrue(
            result.get("fatal_error_detected")
        )
        self.assertEqual(
            result.get("mode"),
            "fatal",
        )
        self.assertEqual(
            result.get("topic_id"),
            PROFILE_ONLY_TOPIC_ID,
        )
        self.assertIn(
            profile_fatal["source_rule_id"],
            {
                str(
                    row.get("source_rule_id")
                    or row.get("id")
                    or ""
                )
                for row in result.get("findings", [])
                if isinstance(row, dict)
            },
        )


if __name__ == "__main__":
    unittest.main()
