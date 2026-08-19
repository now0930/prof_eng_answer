from __future__ import annotations

import ast
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from grade_submission_normalizer import (
    normalize_grade_submission,
    normalize_pipeline_call,
)


class GradeSubmissionNormalizerTest(
    unittest.TestCase
):
    def test_normal_answer_is_preserved(
        self,
    ) -> None:
        source = (
            "문제: PID 제어기의 특성을 "
            "설명하시오.\n"
            "1. 개요\n"
            "비례·적분·미분 동작을 설명한다."
        )
        result = normalize_grade_submission(
            source
        )
        self.assertEqual(
            result["normalized_text"],
            source,
        )
        self.assertFalse(result["changed"])

    def test_nested_grade_uses_last_submission(
        self,
    ) -> None:
        source = (
            "[2026-08-19 오후 2:00] "
            "이 대원: /grade\n"
            "문제: 이전 문제\n"
            "이전 답안\n"
            "[2026-08-19 오후 2:01] "
            "Bot name: 채점기: 안내\n"
            "이 메시지는 제거되어야 한다.\n"
            "[2026-08-19 오후 2:02] "
            "이 대원: /grade\n"
            "문제: 최종 문제\n"
            "최종 답안\n"
            "끝.\n"
            "[2026-08-19 오후 2:03] "
            "Bot name: 채점기: 채점 시작\n"
            "채점 엔진 안내\n"
        )
        result = normalize_grade_submission(
            source
        )
        self.assertEqual(
            result["normalized_text"],
            "문제: 최종 문제\n최종 답안",
        )
        self.assertIn(
            "nested_grade_segments_removed",
            result["events"],
        )
        self.assertNotIn(
            "이전 문제",
            result["normalized_text"],
        )
        self.assertNotIn(
            "채점 엔진",
            result["normalized_text"],
        )

    def test_idempotent(self) -> None:
        source = (
            "[2026-08-19 오후 3:05] "
            "이 대원: /grade\n"
            "문제: V-model을 설명하시오.\n"
            "답안 내용\n"
            "끝.\n"
        )
        first = normalize_grade_submission(
            source
        )
        second = normalize_grade_submission(
            first["normalized_text"]
        )
        self.assertEqual(
            first["normalized_text"],
            second["normalized_text"],
        )

    def test_kwargs_pipeline_call_normalized(
        self,
    ) -> None:
        def target(*args, **kwargs):
            return args, kwargs

        args, kwargs, evidence = (
            normalize_pipeline_call(
                target,
                (),
                {
                    "raw_text": (
                        "/grade\n"
                        "문제: 최종 문제\n"
                        "최종 답안\n"
                        "끝."
                    )
                },
            )
        )
        self.assertEqual(args, ())
        self.assertEqual(
            kwargs["raw_text"],
            "문제: 최종 문제\n최종 답안",
        )
        self.assertTrue(evidence["changed"])


class FinalGradeReuseTest(
    unittest.TestCase
):
    def _identity_and_contract(
        self,
        root: Path,
    ):
        from grading_identity import (
            build_grading_identity,
        )
        from question_contract import (
            build_question_contract,
        )

        identity = build_grading_identity(
            "V-model 검증 방안을 설명하시오.",
            "단위시험, 통합시험, 시스템시험을 설명한다.",
        ).to_dict()

        snapshot = root / "rubric_snapshot.json"
        snapshot.write_text(
            json.dumps(
                {
                    "version": "stage18b1-test",
                    "items": [],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        contract = build_question_contract(
            grading_identity=identity,
            question_type_evaluation={
                "primary_type": {
                    "id": "PROCEDURE",
                },
                "question_type": "PROCEDURE",
                "confidence": "high",
                "status": "locked",
                "question_type_locked": True,
                "source": "question_type_router",
                "matched_rules": ["stage18b1-test"],
            },
            fact_evaluation={
                "topic_id": "SW-TEST",
            },
            model_answer_reference={
                "primary_reference": {
                    "topic_id": "SW-TEST",
                },
            },
            rubric_snapshot_path=snapshot,
            subject_rubric={
                "name": "stage18b1-test",
                "version": "1",
            },
        )

        return identity, contract

    def test_final_grade_cache_round_trip(
        self,
    ) -> None:
        import grading_agents

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            identity, contract = (
                self._identity_and_contract(
                    root
                )
            )
            cache_dir = root / "final_grade_cache"
            grade = {
                "total_score": 14.23,
                "final_total_score": 14.23,
                "breakdown": [
                    {
                        "layer_id": "A",
                        "score": 2.0,
                    },
                    {
                        "layer_id": "B",
                        "score": 3.0,
                    },
                    {
                        "layer_id": "C",
                        "score": 4.0,
                    },
                    {
                        "layer_id": "D",
                        "score": 4.0,
                    },
                    {
                        "layer_id": "E",
                        "score": 1.23,
                    },
                ],
                "strong_verdict_allowed": False,
                "requirements_full_credit_allowed": (
                    False
                ),
                "grading_identity": identity,
                "question_contract": contract,
            }

            with mock.patch.object(
                grading_agents,
                "_STAGE18B1_FINAL_GRADE_CACHE_DIR",
                cache_dir,
            ):
                stored = (
                    grading_agents
                    ._stage18b1_store_final_grade_cache(
                        grade
                    )
                )
                self.assertTrue(stored)

                first = (
                    grading_agents
                    ._stage18b1_load_final_grade_cache(
                        grading_identity=identity,
                        question_contract=contract,
                    )
                )
                self.assertEqual(first, grade)

                first["total_score"] = 99.0

                second = (
                    grading_agents
                    ._stage18b1_load_final_grade_cache(
                        grading_identity=identity,
                        question_contract=contract,
                    )
                )
                self.assertEqual(
                    second["total_score"],
                    14.23,
                )
                self.assertEqual(
                    len(list(cache_dir.glob("*.json"))),
                    1,
                )

    def test_production_path_cache_boundaries(
        self,
    ) -> None:
        import grading_agents

        source = Path(
            grading_agents.__file__
        ).read_text(encoding="utf-8")
        tree = ast.parse(source)

        def call_name(node):
            target = node.func
            parts = []
            while isinstance(
                target,
                ast.Attribute,
            ):
                parts.append(target.attr)
                target = target.value
            if isinstance(target, ast.Name):
                parts.append(target.id)
            return ".".join(
                reversed(parts)
            ).rsplit(".", 1)[-1]

        functions = [
            node
            for node in ast.walk(tree)
            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
        ]

        contract_owners = []
        for function in functions:
            calls = [
                (
                    call_name(node),
                    node.lineno,
                )
                for node in ast.walk(function)
                if isinstance(node, ast.Call)
            ]
            names = {
                name for name, _ in calls
            }
            if {
                "resolve_question_contract_cache",
                "persist_question_contract",
                "_stage18b1_load_final_grade_cache",
            }.issubset(names):
                contract_owners.append(
                    calls
                )

        self.assertEqual(
            len(contract_owners),
            1,
        )

        calls = contract_owners[0]
        persist_line = min(
            line
            for name, line in calls
            if name == "persist_question_contract"
        )
        load_line = min(
            line
            for name, line in calls
            if name
            == "_stage18b1_load_final_grade_cache"
        )
        self.assertLess(
            persist_line,
            load_line,
        )

        wrappers = []
        for function in functions:
            if function.name != "run_agent_pipeline":
                continue

            calls = [
                (
                    call_name(node),
                    node.lineno,
                )
                for node in ast.walk(function)
                if isinstance(node, ast.Call)
            ]
            names = {
                name for name, _ in calls
            }
            if {
                "_STAGE17E5_PREVIOUS_RUN_AGENT_PIPELINE",
                "_stage17e5_finalize_pipeline_result",
                "_stage18b1_store_final_grade_cache",
            }.issubset(names):
                wrappers.append(calls)

        self.assertEqual(len(wrappers), 1)
        wrapper_calls = wrappers[0]
        finalize_line = min(
            line
            for name, line in wrapper_calls
            if name
            == "_stage17e5_finalize_pipeline_result"
        )
        store_line = min(
            line
            for name, line in wrapper_calls
            if name
            == "_stage18b1_store_final_grade_cache"
        )
        self.assertLess(
            finalize_line,
            store_line,
        )


if __name__ == "__main__":
    unittest.main()
