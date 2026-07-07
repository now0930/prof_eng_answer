#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from rubric_content.topic_importance import (  # noqa: E402
    build_topic_importance_template,
    validate_topic_importance_bank_data,
)
from validators.rubric_bank.validate_content import (  # noqa: E402
    validate_topic_importance,
)


class TopicImportanceScopeValidationTest(unittest.TestCase):
    def test_explicit_umbrella_scope_is_accepted(self) -> None:
        errors: list[str] = []
        warnings: list[str] = []

        summary = validate_topic_importance(
            {
                "topics": [
                    {
                        "topic_id": "control_theory_general",
                        "topic_scope": "umbrella_strategy",
                    }
                ]
            },
            {"pid_control"},
            errors,
            warnings,
        )

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(
            summary["umbrella_topics"],
            ["control_theory_general"],
        )

    def test_unmarked_non_fact_topic_is_rejected(self) -> None:
        errors: list[str] = []
        warnings: list[str] = []

        validate_topic_importance(
            {
                "topics": [
                    {
                        "topic_id": "control_theory_general",
                    }
                ]
            },
            {"pid_control"},
            errors,
            warnings,
        )

        self.assertEqual(warnings, [])
        self.assertTrue(
            any(
                "must declare topic_scope=umbrella_strategy" in error
                for error in errors
            ),
            errors,
        )

    def test_fact_topic_cannot_claim_umbrella_scope(self) -> None:
        errors: list[str] = []
        warnings: list[str] = []

        validate_topic_importance(
            {
                "topics": [
                    {
                        "topic_id": "pid_control",
                        "topic_scope": "umbrella_strategy",
                    }
                ]
            },
            {"pid_control"},
            errors,
            warnings,
        )

        self.assertEqual(warnings, [])
        self.assertTrue(
            any(
                "cannot declare topic_scope=umbrella_strategy" in error
                for error in errors
            ),
            errors,
        )

    def test_invalid_scope_is_rejected_by_content_validator(self) -> None:
        errors: list[str] = []
        warnings: list[str] = []

        validate_topic_importance(
            {
                "topics": [
                    {
                        "topic_id": "sample",
                        "topic_scope": "broad_topic",
                    }
                ]
            },
            {"pid_control"},
            errors,
            warnings,
        )

        self.assertTrue(
            any(
                "invalid topic_scope: broad_topic" in error
                for error in errors
            ),
            errors,
        )

    def test_invalid_scope_is_rejected_by_standalone_validator(self) -> None:
        errors = validate_topic_importance_bank_data(
            {
                "topics": [
                    {
                        "topic_id": "sample",
                        "topic_scope": "broad_topic",
                        "label": "Sample",
                        "aliases": ["sample"],
                        "difficulty": "FIELD_APPLICATION",
                        "selection_importance": "NORMAL",
                    }
                ]
            }
        )

        self.assertTrue(
            any(
                "invalid topic_scope: broad_topic" in error
                for error in errors
            ),
            errors,
        )

    def test_template_declares_fact_topic_scope(self) -> None:
        template = build_topic_importance_template(
            "sample_topic",
            "Sample Topic",
            "FIELD_APPLICATION",
        )

        self.assertEqual(
            template["topic_scope"],
            "fact_topic",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
