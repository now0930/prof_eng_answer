from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import grading_agents
from grading_identity import (
    build_grading_identity,
)
from question_contract import (
    apply_question_contract_to_fact_evaluation,
    apply_question_contract_to_model_reference,
    apply_question_contract_to_question_type,
    build_question_contract,
    confirm_question_contract,
    load_question_contract,
    persist_question_contract,
    validate_question_contract,
)


TARGET_TOPIC = (
    "control_valve_fluid_forces_"
    "unbalance_friction_actuator_"
    "sizing_fail_safe"
)

INCIDENT_SESSION = Path(
    "data/sessions/20260717_114330_5960502198"
)


def load_incident() -> tuple[
    str,
    dict,
]:
    raw_text = INCIDENT_SESSION.joinpath(
        "input.txt"
    ).read_text(
        encoding="utf-8",
        errors="replace",
    )

    subject_rubric = json.loads(
        INCIDENT_SESSION.joinpath(
            "subject_rubric_snapshot.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    return raw_text, subject_rubric


class QuestionContractUnitTests(
    unittest.TestCase
):
    def test_auto_confirmed_contract_is_stable(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            session_dir = Path(tmp)
            rubric_path = (
                session_dir
                / "subject_rubric_snapshot.json"
            )
            rubric = {
                "name": "test rubric",
                "version": "v1",
                "question_type_profile": (
                    "rubrics/test.json"
                ),
            }
            rubric_path.write_text(
                json.dumps(
                    rubric,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            identity = (
                build_grading_identity(
                    "문제",
                    "답안",
                ).to_dict()
            )

            qtype = {
                "question_type": (
                    "PRINCIPLE_INTERPRETATION"
                ),
                "primary_type": {
                    "id": (
                        "PRINCIPLE_INTERPRETATION"
                    )
                },
                "confidence": "high",
                "status": "locked",
                "question_type_locked": True,
                "source": (
                    "deterministic_question_router"
                ),
                "matched_rules": [
                    "principle"
                ],
            }

            fact_eval = {
                "topic_id": TARGET_TOPIC,
            }
            model_ref = {
                "matched": True,
                "primary_reference": {
                    "topic_id": TARGET_TOPIC,
                },
            }

            first = build_question_contract(
                grading_identity=identity,
                question_type_evaluation=qtype,
                fact_evaluation=fact_eval,
                model_answer_reference=model_ref,
                rubric_snapshot_path=(
                    rubric_path
                ),
                subject_rubric=rubric,
            )
            second = build_question_contract(
                grading_identity=identity,
                question_type_evaluation=qtype,
                fact_evaluation=fact_eval,
                model_answer_reference=model_ref,
                rubric_snapshot_path=(
                    rubric_path
                ),
                subject_rubric=rubric,
            )

            self.assertEqual(
                first,
                second,
            )
            self.assertEqual(
                first["confirmation"][
                    "status"
                ],
                "auto_confirmed",
            )
            self.assertFalse(
                first["confirmation"][
                    "required"
                ]
            )
            self.assertIsNone(
                first["confirmation"][
                    "confirmed_at"
                ]
            )
            self.assertEqual(
                first["lens"],
                "PRINCIPLE_INTERPRETATION",
            )
            self.assertEqual(
                first["routing"][
                    "canonical_topic_id"
                ],
                TARGET_TOPIC,
            )

            validate_question_contract(
                first
            )

    def test_provisional_contract_is_pending(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            path = (
                Path(tmp)
                / "subject_rubric_snapshot.json"
            )
            path.write_text(
                json.dumps(
                    {
                        "name": "test",
                        "version": "v1",
                    }
                ),
                encoding="utf-8",
            )

            contract = build_question_contract(
                grading_identity=(
                    build_grading_identity(
                        "문제",
                        "답안",
                    ).to_dict()
                ),
                question_type_evaluation={
                    "question_type": "GENERAL",
                    "confidence": "low",
                    "status": "provisional",
                    "question_type_locked": (
                        False
                    ),
                    "source": "fallback",
                    "matched_rules": [],
                },
                fact_evaluation={},
                model_answer_reference={},
                rubric_snapshot_path=path,
                subject_rubric={},
            )

            self.assertEqual(
                contract["confirmation"][
                    "status"
                ],
                "pending",
            )
            self.assertTrue(
                contract["confirmation"][
                    "required"
                ]
            )

    def test_manual_confirmation_preserves_identity(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            path = (
                Path(tmp)
                / "subject_rubric_snapshot.json"
            )
            path.write_text(
                json.dumps(
                    {
                        "name": "test",
                        "version": "v1",
                    }
                ),
                encoding="utf-8",
            )

            contract = build_question_contract(
                grading_identity=(
                    build_grading_identity(
                        "문제",
                        "답안",
                    ).to_dict()
                ),
                question_type_evaluation={
                    "question_type": "GENERAL",
                    "confidence": "medium",
                    "status": "provisional",
                    "question_type_locked": (
                        False
                    ),
                    "source": (
                        "deterministic_question_router"
                    ),
                    "matched_rules": [],
                },
                fact_evaluation={},
                model_answer_reference={},
                rubric_snapshot_path=path,
                subject_rubric={},
            )

            identity_before = dict(
                contract[
                    "immutable_identity"
                ]
            )
            hash_before = contract[
                "contract_hash"
            ]

            confirmed = (
                confirm_question_contract(
                    contract,
                    question_type=(
                        "PRINCIPLE_INTERPRETATION"
                    ),
                    actor="operator:test",
                    method="focused_test",
                    confirmed_at=(
                        "2026-07-18T00:00:00+00:00"
                    ),
                )
            )

            self.assertEqual(
                confirmed[
                    "immutable_identity"
                ],
                identity_before,
            )
            self.assertNotEqual(
                confirmed[
                    "contract_hash"
                ],
                hash_before,
            )
            self.assertEqual(
                confirmed["revision"],
                2,
            )
            self.assertEqual(
                confirmed["lens"],
                "PRINCIPLE_INTERPRETATION",
            )
            self.assertEqual(
                confirmed["confirmation"][
                    "status"
                ],
                "manual_confirmed",
            )
            self.assertEqual(
                confirmed["confirmation"][
                    "actor"
                ],
                "operator:test",
            )
            self.assertEqual(
                len(
                    confirmed[
                        "confirmation"
                    ]["audit"]
                ),
                1,
            )

    def test_persist_load_and_apply_roundtrip(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            session_dir = Path(tmp)
            rubric_path = (
                session_dir
                / "subject_rubric_snapshot.json"
            )
            rubric_path.write_text(
                json.dumps(
                    {
                        "name": "test",
                        "version": "v1",
                    }
                ),
                encoding="utf-8",
            )

            contract = build_question_contract(
                grading_identity=(
                    build_grading_identity(
                        "문제",
                        "답안",
                    ).to_dict()
                ),
                question_type_evaluation={
                    "question_type": (
                        "PRINCIPLE_INTERPRETATION"
                    ),
                    "confidence": "high",
                    "status": "locked",
                    "question_type_locked": True,
                    "source": (
                        "deterministic_question_router"
                    ),
                    "matched_rules": [
                        "principle"
                    ],
                },
                fact_evaluation={
                    "topic_id": TARGET_TOPIC,
                },
                model_answer_reference={
                    "matched": True,
                    "primary_reference": {
                        "topic_id": TARGET_TOPIC,
                    },
                },
                rubric_snapshot_path=(
                    rubric_path
                ),
                subject_rubric={},
            )

            persisted = (
                persist_question_contract(
                    session_dir,
                    contract,
                )
            )
            loaded = load_question_contract(
                session_dir
            )

            self.assertTrue(
                persisted.exists()
            )
            self.assertEqual(
                loaded,
                contract,
            )

            qtype = (
                apply_question_contract_to_question_type(
                    {
                        "primary_type": {
                            "id": "GENERAL"
                        }
                    },
                    loaded,
                )
            )
            fact_eval = (
                apply_question_contract_to_fact_evaluation(
                    {},
                    loaded,
                )
            )
            model_ref = (
                apply_question_contract_to_model_reference(
                    {
                        "primary_reference": {
                            "topic_id": (
                                "wrong_topic"
                            )
                        }
                    },
                    loaded,
                )
            )

            self.assertEqual(
                qtype["question_type"],
                "PRINCIPLE_INTERPRETATION",
            )
            self.assertTrue(
                qtype[
                    "question_type_locked"
                ]
            )
            self.assertEqual(
                fact_eval["topic_id"],
                TARGET_TOPIC,
            )
            self.assertEqual(
                model_ref[
                    "primary_reference"
                ]["topic_id"],
                TARGET_TOPIC,
            )


class QuestionContractIntegrationTests(
    unittest.TestCase
):
    def test_real_incident_contract(
        self,
    ):
        raw_text, subject_rubric = (
            load_incident()
        )
        question_text = (
            grading_agents
            ._phase3_extract_question_text(
                raw_text
            )
        )
        answer_text = (
            grading_agents
            ._phase3_extract_answer_text(
                raw_text
            )
        )
        identity = (
            build_grading_identity(
                question_text,
                answer_text,
            ).to_dict()
        )

        with tempfile.TemporaryDirectory() as tmp:
            session_dir = Path(tmp)
            rubric_path = (
                session_dir
                / "subject_rubric_snapshot.json"
            )
            rubric_path.write_text(
                json.dumps(
                    subject_rubric,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            with mock.patch.dict(
                os.environ,
                {
                    "RUBRIC_BANK_MODE": (
                        "generated"
                    )
                },
                clear=False,
            ):
                fact_eval = (
                    grading_agents
                    ._phase3_evaluate_fact_anchors(
                        raw_text,
                        subject_rubric,
                    )
                )
                qtype = (
                    grading_agents
                    ._phase9_run_question_type_lens(
                        input_text=raw_text,
                        answer_text=answer_text,
                        subject_rubric=(
                            subject_rubric
                        ),
                        session_dir=session_dir,
                    )
                )
                model_ref = (
                    grading_agents
                    ._phase10_run_model_answer_reference(
                        input_text=raw_text,
                        answer_text=answer_text,
                        question_type_eval=qtype,
                        fact_eval=fact_eval,
                        subject_rubric=(
                            subject_rubric
                        ),
                        session_dir=session_dir,
                    )
                )

            contract = build_question_contract(
                grading_identity=identity,
                question_type_evaluation=qtype,
                fact_evaluation=fact_eval,
                model_answer_reference=model_ref,
                rubric_snapshot_path=(
                    rubric_path
                ),
                subject_rubric=subject_rubric,
            )

            persist_question_contract(
                session_dir,
                contract,
            )
            loaded = load_question_contract(
                session_dir
            )

            self.assertEqual(
                loaded["lens"],
                "PRINCIPLE_INTERPRETATION",
            )
            self.assertEqual(
                loaded["routing"][
                    "canonical_topic_id"
                ],
                TARGET_TOPIC,
            )
            self.assertEqual(
                loaded[
                    "immutable_identity"
                ]["question_hash"],
                identity["question_hash"],
            )
            self.assertEqual(
                loaded[
                    "immutable_identity"
                ]["submission_hash"],
                identity[
                    "submission_hash"
                ],
            )
            self.assertEqual(
                loaded["confirmation"][
                    "status"
                ],
                "auto_confirmed",
            )

    def test_production_consumes_persisted_contract_before_gemini(
        self,
    ):
        source = Path(
            "grading_agents.py"
        ).read_text(
            encoding="utf-8"
        )

        build_position = source.index(
            "question_contract = "
            "build_question_contract("
        )
        persist_position = source.index(
            "persist_question_contract("
        )
        load_position = source.index(
            "question_contract = "
            "load_question_contract("
        )
        apply_position = source.index(
            "apply_question_contract_to_"
            "question_type("
        )
        gemini_position = source.index(
            "gemini_eval = "
            "_phase6_run_gemini_semantic_"
            "grader("
        )

        self.assertLess(
            build_position,
            persist_position,
        )
        self.assertLess(
            persist_position,
            load_position,
        )
        self.assertLess(
            load_position,
            apply_position,
        )
        self.assertLess(
            apply_position,
            gemini_position,
        )
        self.assertIn(
            '"question_contract": '
            "question_contract",
            source,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
