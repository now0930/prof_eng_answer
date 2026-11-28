import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import ai_backends
import ollama_backend


class BackendTests(unittest.TestCase):
    def test_planner_profile_has_explicit_context(self):
        planner = ai_backends.PlanBackend.from_env({
            "V6_OLLAMA_PLAN_MODEL": "local-model",
            "V6_OLLAMA_PLAN_CONTEXT": '["grading/example.py"]',
        })
        self.assertEqual(
            planner.argv[2:],
            ["plan", "--model", "local-model", "--context", "grading/example.py"],
        )

    def test_planner_profile_requires_context(self):
        with self.assertRaisesRegex(ValueError, "PLAN_CONTEXT"):
            ai_backends.PlanBackend.from_env({"V6_OLLAMA_PLAN_MODEL": "local-model"})

    def test_editor_rejects_two_selected_backends(self):
        with self.assertRaisesRegex(ValueError, "one nonempty edit backend"):
            ai_backends.EditBackend.from_env({
                "V6_OLLAMA_EDIT_MODEL": "local-model",
                "V6_EDITOR_COMMAND": json.dumps([ai_backends.sys.executable]),
            })

    def test_remote_ollama_model_is_rejected_before_chat(self):
        with patch.object(ollama_backend, "request", return_value={"models": []}) as request:
            with self.assertRaisesRegex(ValueError, "local GGUF"):
                ollama_backend.generate("remote:cloud", "prompt", {})
            request.assert_called_once_with("/api/tags")

    def test_unapproved_model_output_preserves_target(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "target.py"
            task = Path(temp) / "task.md"
            target.write_text("x = 1\n", encoding="utf-8")
            task.write_text("Update x from 1 to 2.", encoding="utf-8")
            approved = hashlib.sha256(b"x = 2\n").hexdigest()
            args = argparse.Namespace(model="local", task=task, target=target)
            with (
                patch.object(ollama_backend, "workspace_file", return_value=target),
                patch.object(ollama_backend, "generate", return_value={"edits": [{"search": "x = 1\n", "replace": "x = 3\n"}]}),
                patch.dict(os.environ, {"V6_EXPECTED_SHA256": approved, "V6_APPROVED_EDITS": "[]"}),
            ):
                with self.assertRaisesRegex(ValueError, "compiled exact edit"):
                    ollama_backend.edit(args)
            self.assertEqual(target.read_bytes(), b"x = 1\n")

    def test_approved_model_output_replaces_target(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "target.py"
            target.write_bytes(b"x = 1\n")
            edits = [{"search": "x = 1", "replace": "x = 2"}]
            args = argparse.Namespace(model="local", target=target)
            with (
                patch.object(ollama_backend, "workspace_file", return_value=target),
                patch.object(ollama_backend, "generate", return_value={"edits": edits}),
                patch.dict(os.environ, {
                    "V6_EXPECTED_SHA256": hashlib.sha256(b"x = 2\n").hexdigest(),
                    "V6_APPROVED_EDITS": json.dumps(edits),
                }),
            ):
                ollama_backend.edit(args)
            self.assertEqual(target.read_bytes(), b"x = 2\n")

    def test_local_plan_keeps_explicit_context_in_request(self):
        args = argparse.Namespace(model="local", context=["grading/example.py"])
        with (
            patch.object(ollama_backend, "workspace_file") as workspace_file,
            patch.object(ollama_backend, "generate", return_value={"tasks": []}) as generate,
            patch("sys.stdin", io.StringIO("Explain the change")),
            patch("sys.stdout", new_callable=io.StringIO) as stdout,
        ):
            workspace_file.return_value.read_text.return_value = "def score(): pass"
            ollama_backend.plan(args)
            self.assertEqual(json.loads(stdout.getvalue()), {"tasks": []})
            self.assertIn('"grading/example.py": "def score(): pass"', generate.call_args.args[1])


if __name__ == "__main__":
    unittest.main()
