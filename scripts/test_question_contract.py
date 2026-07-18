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


class QuestionContractCacheTests(
    unittest.TestCase
):
    @staticmethod
    def _identity(
        answer: str = "답안",
    ) -> dict:
        return build_grading_identity(
            "동일한 문제",
            answer,
        ).to_dict()

    @staticmethod
    def _qtype(
        question_type: str,
        *,
        confidence: str = "high",
        status: str = "locked",
        locked: bool = True,
        source: str = (
            "deterministic_question_router"
        ),
    ) -> dict:
        return {
            "question_type": question_type,
            "primary_type": {
                "id": question_type,
            },
            "confidence": confidence,
            "status": status,
            "question_type_locked": locked,
            "source": source,
            "matched_rules": [
                "focused_test"
            ],
        }

    def _build(
        self,
        *,
        root: Path,
        question_type: str = (
            "PRINCIPLE_INTERPRETATION"
        ),
        answer: str = "답안",
        rubric_version: str = "v1",
        confidence: str = "high",
        status: str = "locked",
        locked: bool = True,
        source: str = (
            "deterministic_question_router"
        ),
    ) -> dict:
        from question_contract import (
            build_question_contract,
        )

        rubric = {
            "name": "cache test rubric",
            "version": rubric_version,
            "question_type_profile": (
                "rubrics/cache_test.json"
            ),
        }
        rubric_path = (
            root
            / (
                "subject_rubric_"
                + rubric_version
                + ".json"
            )
        )
        rubric_path.write_text(
            json.dumps(
                rubric,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return build_question_contract(
            grading_identity=self._identity(
                answer
            ),
            question_type_evaluation=(
                self._qtype(
                    question_type,
                    confidence=confidence,
                    status=status,
                    locked=locked,
                    source=source,
                )
            ),
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
            subject_rubric=rubric,
        )

    def test_cache_key_ignores_answer_and_tracks_rubric(
        self,
    ):
        from question_contract import (
            question_contract_cache_key,
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            first = self._build(
                root=root,
                answer="첫 답안",
                rubric_version="v1",
            )
            second = self._build(
                root=root,
                answer="다른 답안",
                rubric_version="v1",
            )
            changed_rubric = self._build(
                root=root,
                answer="첫 답안",
                rubric_version="v2",
            )

            self.assertEqual(
                first[
                    "immutable_identity"
                ]["question_hash"],
                second[
                    "immutable_identity"
                ]["question_hash"],
            )
            self.assertNotEqual(
                first[
                    "immutable_identity"
                ]["submission_hash"],
                second[
                    "immutable_identity"
                ]["submission_hash"],
            )
            self.assertEqual(
                question_contract_cache_key(
                    first
                ),
                question_contract_cache_key(
                    second
                ),
            )
            self.assertNotEqual(
                question_contract_cache_key(
                    first
                ),
                question_contract_cache_key(
                    changed_rubric
                ),
            )

    def test_cache_key_separates_rubric_bank_modes(
        self,
    ):
        import os
        from unittest import mock

        from question_contract import (
            build_question_contract,
            question_contract_cache_key,
            resolve_question_contract_cache,
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cache_dir = root / "cache"
            rubric = {
                "name": "cache mode test rubric",
                "version": "v1",
                "question_type_profile": (
                    "rubrics/cache_mode_test.json"
                ),
                "fact_anchor_bank": (
                    "rubrics/cache_mode_test.json"
                ),
                "model_answer_bank": (
                    "rubrics/cache_mode_test.json"
                ),
            }
            rubric_path = (
                root
                / "subject_rubric_mode.json"
            )
            rubric_path.write_text(
                json.dumps(
                    rubric,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )

            def build(
                mode: str,
                topic_id: str,
            ) -> dict:
                with mock.patch.dict(
                    os.environ,
                    {
                        "RUBRIC_BANK_MODE": mode,
                    },
                    clear=False,
                ):
                    return build_question_contract(
                        grading_identity=(
                            self._identity(
                                "동일 답안"
                            )
                        ),
                        question_type_evaluation=(
                            self._qtype(
                                "PRINCIPLE_INTERPRETATION"
                            )
                        ),
                        fact_evaluation={
                            "topic_id": topic_id,
                        },
                        model_answer_reference={
                            "matched": True,
                            "primary_reference": {
                                "topic_id": topic_id,
                            },
                        },
                        rubric_snapshot_path=(
                            rubric_path
                        ),
                        subject_rubric=rubric,
                    )

            legacy = build(
                "legacy",
                "legacy_topic",
            )
            generated = build(
                "generated",
                "generated_topic",
            )

            self.assertEqual(
                legacy["rubric"]["bank_mode"],
                "legacy",
            )
            self.assertEqual(
                generated["rubric"]["bank_mode"],
                "generated",
            )
            self.assertNotEqual(
                question_contract_cache_key(
                    legacy
                ),
                question_contract_cache_key(
                    generated
                ),
            )

            resolve_question_contract_cache(
                legacy,
                cache_dir=cache_dir,
            )
            resolved = (
                resolve_question_contract_cache(
                    generated,
                    cache_dir=cache_dir,
                )
            )

            self.assertFalse(
                resolved["cache"]["hit"]
            )
            self.assertEqual(
                resolved["cache"][
                    "authoritative_source"
                ],
                "candidate",
            )
            self.assertEqual(
                resolved["cache"][
                    "rubric_bank_mode"
                ],
                "generated",
            )
            self.assertEqual(
                resolved["routing"][
                    "canonical_topic_id"
                ],
                "generated_topic",
            )

    def test_cache_miss_writes_confirmed_candidate(
        self,
    ):
        from question_contract import (
            question_contract_cache_key,
            resolve_question_contract_cache,
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cache_dir = root / "cache"
            candidate = self._build(
                root=root
            )

            resolved = (
                resolve_question_contract_cache(
                    candidate,
                    cache_dir=cache_dir,
                )
            )

            metadata = resolved["cache"]
            key = question_contract_cache_key(
                candidate
            )
            cached_path = (
                cache_dir
                / f"{key}.json"
            )

            self.assertEqual(
                metadata["status"],
                "miss",
            )
            self.assertFalse(
                metadata["hit"]
            )
            self.assertTrue(
                metadata["cache_written"]
            )
            self.assertEqual(
                metadata[
                    "authoritative_source"
                ],
                "candidate",
            )
            self.assertTrue(
                cached_path.exists()
            )

    def test_cache_hit_reuses_confirmed_contract(
        self,
    ):
        from question_contract import (
            resolve_question_contract_cache,
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cache_dir = root / "cache"
            candidate = self._build(
                root=root
            )

            resolve_question_contract_cache(
                candidate,
                cache_dir=cache_dir,
            )
            resolved = (
                resolve_question_contract_cache(
                    candidate,
                    cache_dir=cache_dir,
                )
            )

            metadata = resolved["cache"]

            self.assertTrue(
                metadata["hit"]
            )
            self.assertEqual(
                metadata["status"],
                "hit",
            )
            self.assertEqual(
                metadata[
                    "authoritative_source"
                ],
                "confirmed_cache",
            )
            self.assertFalse(
                metadata[
                    "deviation_detected"
                ]
            )
            self.assertEqual(
                metadata["deviations"],
                [],
            )
            self.assertEqual(
                metadata["warning"],
                "",
            )

    def test_confirmed_cache_wins_on_routing_deviation(
        self,
    ):
        from question_contract import (
            resolve_question_contract_cache,
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cache_dir = root / "cache"

            cached_candidate = self._build(
                root=root,
                question_type=(
                    "PRINCIPLE_INTERPRETATION"
                ),
            )
            resolve_question_contract_cache(
                cached_candidate,
                cache_dir=cache_dir,
            )

            deviated_candidate = self._build(
                root=root,
                question_type=(
                    "COMPARE_SELECTION"
                ),
            )
            resolved = (
                resolve_question_contract_cache(
                    deviated_candidate,
                    cache_dir=cache_dir,
                )
            )

            metadata = resolved["cache"]
            fields = {
                item["field"]
                for item in metadata[
                    "deviations"
                ]
            }

            self.assertEqual(
                resolved["lens"],
                "PRINCIPLE_INTERPRETATION",
            )
            self.assertTrue(
                metadata[
                    "deviation_detected"
                ]
            )
            self.assertIn(
                "lens",
                fields,
            )
            self.assertIn(
                "question_type.id",
                fields,
            )
            self.assertEqual(
                metadata["score_effect"],
                "diagnostic_only",
            )
            self.assertFalse(
                metadata[
                    "direct_score_application"
                ]
            )
            self.assertTrue(
                metadata["warning"]
            )

    def test_pending_cache_is_not_authoritative(
        self,
    ):
        from question_contract import (
            question_contract_cache_key,
            resolve_question_contract_cache,
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cache_dir = root / "cache"
            cache_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            pending = self._build(
                root=root,
                confidence="medium",
                status="provisional",
                locked=False,
            )
            key = question_contract_cache_key(
                pending
            )
            path = (
                cache_dir
                / f"{key}.json"
            )
            path.write_text(
                json.dumps(
                    pending,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            confirmed = self._build(
                root=root,
                question_type=(
                    "COMPARE_SELECTION"
                ),
            )
            resolved = (
                resolve_question_contract_cache(
                    confirmed,
                    cache_dir=cache_dir,
                )
            )

            metadata = resolved["cache"]

            self.assertEqual(
                resolved["lens"],
                "COMPARE_SELECTION",
            )
            self.assertEqual(
                metadata["status"],
                "pending_cache_replaced",
            )
            self.assertEqual(
                metadata[
                    "authoritative_source"
                ],
                "candidate",
            )
            self.assertTrue(
                metadata["cache_written"]
            )

    def test_manual_confirmed_cache_is_authoritative(
        self,
    ):
        from question_contract import (
            confirm_question_contract,
            resolve_question_contract_cache,
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cache_dir = root / "cache"

            pending = self._build(
                root=root,
                confidence="medium",
                status="provisional",
                locked=False,
            )
            manual = (
                confirm_question_contract(
                    pending,
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

            resolve_question_contract_cache(
                manual,
                cache_dir=cache_dir,
            )

            changed = self._build(
                root=root,
                question_type=(
                    "COMPARE_SELECTION"
                ),
            )
            resolved = (
                resolve_question_contract_cache(
                    changed,
                    cache_dir=cache_dir,
                )
            )

            self.assertEqual(
                resolved["lens"],
                "PRINCIPLE_INTERPRETATION",
            )
            self.assertEqual(
                resolved["confirmation"][
                    "status"
                ],
                "manual_confirmed",
            )
            self.assertEqual(
                resolved["confirmation"][
                    "actor"
                ],
                "operator:test",
            )
            self.assertTrue(
                resolved["cache"][
                    "deviation_detected"
                ]
            )

    def test_production_resolves_cache_before_persist(
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
        resolve_position = source.index(
            "resolve_question_contract_cache("
        )
        persist_position = source.index(
            "persist_question_contract("
        )
        load_position = source.index(
            "question_contract = "
            "load_question_contract("
        )
        gemini_position = source.index(
            "gemini_eval = "
            "_phase6_run_gemini_semantic_"
            "grader("
        )

        self.assertLess(
            build_position,
            resolve_position,
        )
        self.assertLess(
            resolve_position,
            persist_position,
        )
        self.assertLess(
            persist_position,
            load_position,
        )
        self.assertLess(
            load_position,
            gemini_position,
        )
        self.assertIn(
            '"question_contract_cache": (',
            source,
        )
        self.assertIn(
            '"question_contract_deviation_warning": (',
            source,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
