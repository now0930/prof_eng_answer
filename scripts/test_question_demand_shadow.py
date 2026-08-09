from __future__ import annotations

import ast
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import grading_agents
import question_demand_shadow as qds


BASE_DIR = Path(__file__).resolve().parents[1]


class QuestionDemandShadowUnitTest(unittest.TestCase):
    def test_disabled_by_default_has_no_llm_dependency(self):
        with mock.patch.dict(
            os.environ,
            {"QUESTION_DEMAND_SHADOW_ENABLED": ""},
            clear=False,
        ):
            result = qds.extract_question_demands(
                "RTD와 열전대를 비교하시오."
            )

        self.assertFalse(result["ok"])
        self.assertFalse(result["enabled"])
        self.assertEqual(result["status"], "disabled")
        self.assertEqual(result["demands"], [])
        self.assertEqual(result["routing_effect"], "none")
        self.assertEqual(result["score_effect"], "none")
        self.assertFalse(result["student_answer_used"])
        self.assertFalse(result["topic_selection_performed"])

    def test_valid_llm_result_is_normalized_and_deduplicated(self):
        def fake_llm(prompt):
            self.assertIn("RTD와 열전대", prompt)
            return {
                "demands": [
                    {
                        "id": "anything",
                        "text": "RTD 측정원리",
                        "topic_id": "must_not_survive",
                    },
                    {
                        "id": "anything2",
                        "text": "열전대 측정원리",
                    },
                    {
                        "id": "anything3",
                        "text": "RTD 측정원리",
                    },
                ]
            }

        result = qds.extract_question_demands(
            "RTD와 열전대의 측정원리를 비교하시오.",
            llm_call=fake_llm,
            enabled=True,
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "ok")
        self.assertEqual(
            result["demands"],
            [
                {"id": "D1", "text": "RTD 측정원리"},
                {"id": "D2", "text": "열전대 측정원리"},
            ],
        )
        self.assertNotIn(
            "topic_id",
            result["demands"][0],
        )
        self.assertFalse(
            result["topic_selection_performed"]
        )

    def test_llm_exception_returns_safe_shadow_fallback(self):
        def fail_llm(_prompt):
            raise RuntimeError("simulated shadow failure")

        result = qds.extract_question_demands(
            "PID 튜닝 순서를 설명하시오.",
            llm_call=fail_llm,
            enabled=True,
        )

        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["demands"], [])
        self.assertEqual(result["routing_effect"], "none")
        self.assertEqual(result["score_effect"], "none")

    def test_malformed_payload_returns_safe_shadow_fallback(self):
        result = qds.extract_question_demands(
            "2차 시스템을 설명하시오.",
            llm_call=lambda _prompt: {"not_demands": []},
            enabled=True,
        )

        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["demand_count"], 0)

    def test_max_demand_limit_is_enforced(self):
        payload = {
            "demands": [
                {"text": f"요구사항 {i}"}
                for i in range(20)
            ]
        }

        result = qds.extract_question_demands(
            "복합 문제",
            llm_call=lambda _prompt: payload,
            max_demands=4,
            enabled=True,
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["demand_count"], 4)


class QuestionDemandShadowPersistenceTest(unittest.TestCase):
    def test_phase10_shadow_disabled_has_zero_persistence_side_effect(self):
        with mock.patch(
            "question_demand_shadow.extract_question_demands",
            return_value={
                "version": qds.QUESTION_DEMAND_SHADOW_VERSION,
                "shadow": True,
                "enabled": False,
                "status": "disabled",
                "ok": False,
                "mode": "question_demand_decomposition_only",
                "demands": [],
                "demand_count": 0,
                "error": "disabled",
                "routing_effect": "none",
                "score_effect": "none",
                "student_answer_used": False,
                "topic_selection_performed": False,
            },
        ), mock.patch.object(
            grading_agents,
            "_phase2_json_write",
        ) as write_mock:
            result = (
                grading_agents
                ._phase10_run_question_demand_shadow(
                    "문제",
                    Path("/not/used"),
                )
            )

        self.assertEqual(result["status"], "disabled")
        write_mock.assert_not_called()

    def test_phase10_shadow_persists_separately(self):
        fake = {
            "version": qds.QUESTION_DEMAND_SHADOW_VERSION,
            "shadow": True,
            "enabled": True,
            "status": "ok",
            "ok": True,
            "mode": "question_demand_decomposition_only",
            "demands": [
                {"id": "D1", "text": "측정원리 설명"}
            ],
            "demand_count": 1,
            "error": "",
            "routing_effect": "none",
            "score_effect": "none",
            "student_answer_used": False,
            "topic_selection_performed": False,
        }

        with tempfile.TemporaryDirectory() as tmp:
            session_dir = Path(tmp)
            with mock.patch(
                "question_demand_shadow.extract_question_demands",
                return_value=fake,
            ):
                result = (
                    grading_agents
                    ._phase10_run_question_demand_shadow(
                        "센서의 측정원리를 설명하시오.",
                        session_dir,
                    )
                )

            persisted = (
                session_dir
                / qds.QUESTION_DEMAND_SHADOW_FILE
            )
            self.assertTrue(persisted.exists())
            self.assertEqual(result, fake)
            self.assertFalse(
                (session_dir / "model_answer_reference.json")
                .exists()
            )

    def test_persistence_failure_does_not_raise(self):
        with mock.patch(
            "question_demand_shadow.extract_question_demands",
            return_value={
                "version": qds.QUESTION_DEMAND_SHADOW_VERSION,
                "shadow": True,
                "enabled": True,
                "status": "ok",
                "ok": True,
                "mode": "question_demand_decomposition_only",
                "demands": [
                    {"id": "D1", "text": "요구사항"}
                ],
                "demand_count": 1,
                "error": "",
                "routing_effect": "none",
                "score_effect": "none",
                "student_answer_used": False,
                "topic_selection_performed": False,
            },
        ), mock.patch.object(
            grading_agents,
            "_phase2_json_write",
            side_effect=OSError("simulated write failure"),
        ):
            result = (
                grading_agents
                ._phase10_run_question_demand_shadow(
                    "문제",
                    Path("/not/used"),
                )
            )

        self.assertIsInstance(result, dict)
        self.assertEqual(result["routing_effect"], "none")


class Phase10IsolationStaticContractTest(unittest.TestCase):
    def test_shadow_call_is_guarded_and_only_handed_to_semantic_shadow(self):
        path = BASE_DIR / "grading_agents.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))

        fn = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name
            == "_phase10_run_model_answer_reference"
        )

        parents = {}
        for parent in ast.walk(fn):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent

        shadow_calls = [
            node
            for node in ast.walk(fn)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id
                == "_phase10_run_question_demand_shadow"
            )
        ]
        self.assertEqual(len(shadow_calls), 1)

        call = shadow_calls[0]
        assign = parents.get(call)
        self.assertIsInstance(assign, ast.Assign)
        self.assertEqual(len(assign.targets), 1)
        self.assertIsInstance(assign.targets[0], ast.Name)
        self.assertEqual(
            assign.targets[0].id,
            "question_demand_shadow_result",
        )

        cur = assign
        guarded = False
        while cur in parents:
            cur = parents[cur]
            if isinstance(cur, ast.Try):
                guarded = True
                break
        self.assertTrue(guarded)

        semantic_calls = [
            node
            for node in ast.walk(fn)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id
                == "_phase10_run_semantic_router_shadow"
            )
        ]
        self.assertEqual(len(semantic_calls), 1)

        semantic_call = semantic_calls[0]
        handoff_values = [
            kw.value
            for kw in semantic_call.keywords
            if kw.arg == "question_demand_result"
        ]
        self.assertEqual(len(handoff_values), 1)

        names = [
            node.id
            for node in ast.walk(handoff_values[0])
            if isinstance(node, ast.Name)
        ]
        self.assertIn(
            "question_demand_shadow_result",
            names,
        )

        returns = [
            node
            for node in ast.walk(fn)
            if isinstance(node, ast.Return)
        ]
        # Stage 6 may return the parallel model-answer-reference result
        # after attaching multi_topic_grading_context. The isolation
        # contract is that Question Demand itself is not returned or handed
        # to scoring; it is handed only to the Semantic Router.
        self.assertTrue(
            any(
                isinstance(node.value, ast.Name)
                and node.value.id == "model_answer_reference_result"
                for node in returns
            )
        )
        self.assertFalse(
            any(
                isinstance(node.value, ast.Name)
                and node.value.id in {
                    "question_demand_shadow_result",
                    "semantic_router_shadow_result",
                }
                for node in returns
            )
        )

    def test_shadow_module_has_no_answer_text_parameter(self):
        tree = ast.parse(
            (BASE_DIR / "question_demand_shadow.py")
            .read_text(encoding="utf-8")
        )

        fn = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "extract_question_demands"
        )
        arg_names = {
            arg.arg
            for arg in (
                list(fn.args.posonlyargs)
                + list(fn.args.args)
                + list(fn.args.kwonlyargs)
            )
        }

        self.assertEqual(
            arg_names,
            {
                "question_text",
                "llm_call",
                "max_demands",
                "enabled",
            },
        )
        self.assertNotIn("answer_text", arg_names)



import json as _qd_cache_json
from pathlib import Path as _QdCachePath
import tempfile as _qd_cache_tempfile
import unittest as _qd_cache_unittest
from unittest.mock import patch as _qd_cache_patch
import question_demand_shadow as _qd_cache_qd


class QuestionDemandAuthoritativeCacheRegression(
    _qd_cache_unittest.TestCase
):
    def _roots(self):
        tmp = _qd_cache_tempfile.TemporaryDirectory()
        root = _QdCachePath(tmp.name)
        return tmp, root / "canonical", root / "runtime"

    def test_confirmed_canonical_bypasses_llm(self) -> None:
        tmp, canonical, runtime = self._roots()
        self.addCleanup(tmp.cleanup)
        question = "동일 질문"
        key = _qd_cache_qd.question_demand_cache_key(
            question,
            max_demands=12,
        )
        entry = {
            "cache_version": _qd_cache_qd.QUESTION_DEMAND_CACHE_VERSION,
            "prompt_contract_version": (
                _qd_cache_qd.QUESTION_DEMAND_PROMPT_CONTRACT_VERSION
            ),
            "cache_key": key,
            "question_sha256": (
                _qd_cache_qd._question_demand_question_sha256(question)
            ),
            "max_demands": 12,
            "confirmation_status": "confirmed",
            "source": "unit_test_confirmed",
            "demands": [
                {"id": "D1", "text": "원인을 진단한다"},
                {"id": "D2", "text": "대책을 설명한다"},
            ],
        }
        _qd_cache_qd._write_json_atomic(
            canonical / f"{key}.json",
            entry,
        )

        calls = {"n": 0}

        def llm(_prompt):
            calls["n"] += 1
            return {"demands": [{"text": "호출되면 실패"}]}

        with (
            _qd_cache_patch.object(
                _qd_cache_qd,
                "QUESTION_DEMAND_CANONICAL_DIR",
                canonical,
            ),
            _qd_cache_patch.object(
                _qd_cache_qd,
                "QUESTION_DEMAND_RUNTIME_CACHE_DIR",
                runtime,
            ),
        ):
            result = _qd_cache_qd.extract_question_demands(
                question,
                llm_call=llm,
                enabled=True,
            )

        self.assertEqual(calls["n"], 0)
        self.assertEqual(result["demand_count"], 2)
        self.assertEqual(
            result["cache_source"],
            "confirmed_canonical",
        )
        self.assertEqual(
            result["confirmation_status"],
            "confirmed",
        )
        self.assertEqual(
            result["engine"],
            "question_demand_authoritative_cache",
        )

    def test_pending_first_success_is_reused(self) -> None:
        tmp, canonical, runtime = self._roots()
        self.addCleanup(tmp.cleanup)
        question = "새로운 질문"
        calls = {"first": 0, "second": 0}

        def first_llm(_prompt):
            calls["first"] += 1
            return {
                "demands": [
                    {"text": "첫 요구사항"},
                    {"text": "둘째 요구사항"},
                ]
            }

        def second_llm(_prompt):
            calls["second"] += 1
            return {"demands": [{"text": "다른 결과"}]}

        with (
            _qd_cache_patch.object(
                _qd_cache_qd,
                "QUESTION_DEMAND_CANONICAL_DIR",
                canonical,
            ),
            _qd_cache_patch.object(
                _qd_cache_qd,
                "QUESTION_DEMAND_RUNTIME_CACHE_DIR",
                runtime,
            ),
        ):
            first = _qd_cache_qd.extract_question_demands(
                question,
                llm_call=first_llm,
                enabled=True,
            )
            second = _qd_cache_qd.extract_question_demands(
                question,
                llm_call=second_llm,
                enabled=True,
            )

        self.assertEqual(calls["first"], 1)
        self.assertEqual(calls["second"], 0)
        self.assertEqual(first["demands"], second["demands"])
        self.assertEqual(first["confirmation_status"], "pending")
        self.assertEqual(second["cache_source"], "runtime_cache")

    def test_corrupt_runtime_entry_fails_open_and_replaces(self) -> None:
        tmp, canonical, runtime = self._roots()
        self.addCleanup(tmp.cleanup)
        question = "손상 캐시 질문"
        key = _qd_cache_qd.question_demand_cache_key(
            question,
            max_demands=12,
        )
        runtime.mkdir(parents=True, exist_ok=True)
        (runtime / f"{key}.json").write_text(
            "{broken",
            encoding="utf-8",
        )

        calls = {"n": 0}

        def llm(_prompt):
            calls["n"] += 1
            return {"demands": [{"text": "복구 요구사항"}]}

        with (
            _qd_cache_patch.object(
                _qd_cache_qd,
                "QUESTION_DEMAND_CANONICAL_DIR",
                canonical,
            ),
            _qd_cache_patch.object(
                _qd_cache_qd,
                "QUESTION_DEMAND_RUNTIME_CACHE_DIR",
                runtime,
            ),
        ):
            result = _qd_cache_qd.extract_question_demands(
                question,
                llm_call=llm,
                enabled=True,
            )

        self.assertEqual(calls["n"], 1)
        self.assertEqual(result["demand_count"], 1)
        repaired = _qd_cache_json.loads(
            (runtime / f"{key}.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(repaired["confirmation_status"], "pending")

    def test_pending_cache_permission_failure_is_fail_open(
        self,
    ) -> None:
        tmp, canonical, runtime = self._roots()
        self.addCleanup(tmp.cleanup)

        calls = {"n": 0}

        def llm(_prompt):
            calls["n"] += 1
            return {"demands": [{"text": "정상 요구사항"}]}

        with (
            _qd_cache_patch.object(
                _qd_cache_qd,
                "QUESTION_DEMAND_CANONICAL_DIR",
                canonical,
            ),
            _qd_cache_patch.object(
                _qd_cache_qd,
                "QUESTION_DEMAND_RUNTIME_CACHE_DIR",
                runtime,
            ),
            _qd_cache_patch.object(
                _qd_cache_qd,
                "_write_json_atomic",
                side_effect=PermissionError(
                    "simulated cache permission failure"
                ),
            ),
        ):
            result = _qd_cache_qd.extract_question_demands(
                "권한 실패 질문",
                llm_call=llm,
                enabled=True,
            )

        self.assertEqual(calls["n"], 1)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["demand_count"], 1)
        self.assertEqual(
            result["cache_source"],
            "runtime_cache_write_failed",
        )
        self.assertEqual(
            result["confirmation_status"],
            "pending_unpersisted",
        )
        self.assertEqual(
            result["cache_write_status"],
            "failed",
        )
        self.assertIn(
            "PermissionError",
            result["cache_write_error"],
        )

    def test_cache_key_excludes_answer_and_routing_by_construction(
        self,
    ) -> None:
        annotations = str(
            _qd_cache_qd.question_demand_cache_key.__annotations__
        )
        self.assertNotIn("answer", annotations.lower())
        self.assertNotIn("routing", annotations.lower())
        self.assertEqual(
            _qd_cache_qd.question_demand_cache_key(
                " Q ",
                max_demands=12,
            ),
            _qd_cache_qd.question_demand_cache_key(
                "Q",
                max_demands=12,
            ),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
