from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
import urllib.request

from grading.quality import validation_api_budget as budget


class FakeResponse:
    def __init__(self, payload):
        self.data = json.dumps(payload).encode("utf-8")
        self.status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, size=-1):
        if size is None or size < 0:
            data, self.data = self.data, b""
            return data
        data, self.data = self.data[:size], self.data[size:]
        return data


class ValidationApiBudgetTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.env = {
            "VALIDATION_API_BUDGET_DB": str(Path(self.temporary.name) / "budget.sqlite3"),
            "VALIDATION_MAX_LIVE_GRADES": "5",
            "VALIDATION_MAX_HTTP_CALLS": "8",
            "VALIDATION_MAX_TOTAL_TOKENS": "500",
        }
        self.patch_env = patch.dict("os.environ", self.env, clear=False)
        self.patch_env.start()

    def tearDown(self):
        self.patch_env.stop()
        self.temporary.cleanup()

    def test_grade_and_http_caps_are_shared_across_threads(self):
        outcomes = []
        lock = threading.Lock()

        def reserve():
            try:
                budget.reserve_grade()
                value = "PASS"
            except budget.ValidationBudgetExceeded:
                value = "BLOCKED"
            with lock:
                outcomes.append(value)

        threads = [threading.Thread(target=reserve) for _ in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(outcomes.count("PASS"), 5)
        self.assertEqual(budget.summary()["totals"]["grades"], 5)

        http_outcomes = []

        def reserve_http():
            try:
                budget.reserve_http("gemini", "gemini-4-argon")
                value = "PASS"
            except budget.ValidationBudgetExceeded:
                value = "BLOCKED"
            with lock:
                http_outcomes.append(value)

        threads = [threading.Thread(target=reserve_http) for _ in range(12)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(http_outcomes.count("PASS"), 8)
        self.assertEqual(budget.summary()["totals"]["http_calls"], 8)

    def test_token_reservation_rejects_request_before_provider_generation(self):
        with self.assertRaisesRegex(budget.ValidationBudgetExceeded, "token_budget"):
            budget.reserve_tokens(501)
        self.assertEqual(budget.summary()["totals"]["reserved_tokens"], 0)

    def test_token_rejection_does_not_consume_generation_http_budget(self):
        with self.assertRaisesRegex(budget.ValidationBudgetExceeded, "token_budget"):
            budget.reserve_generation_request("gemini", "gemini-4-argon", 501)
        self.assertEqual(budget.summary()["totals"]["http_calls"], 0)

    def test_clova_live_request_is_blocked_before_http_without_token_preflight(self):
        calls = []

        def fake_urlopen(request, *args, **kwargs):
            calls.append(request)
            return FakeResponse({"result": {"message": {"content": "{}"}}})

        with patch.object(urllib.request, "urlopen", side_effect=fake_urlopen):
            budget.install_http_meter()
            request = urllib.request.Request(
                "https://clovastudio.stream.ntruss.com/testapp/v2/tasks/abc",
                data=b"{}", method="POST",
            )
            with self.assertRaisesRegex(budget.ValidationBudgetExceeded, "preflight_unsupported"):
                urllib.request.urlopen(request)
        self.assertEqual(calls, [])
        self.assertEqual(budget.summary()["totals"]["http_calls"], 0)

    def test_provider_usage_reconciles_reserved_cap_without_persisting_text(self):
        reservation = budget.reserve_tokens(150)
        budget.update_reservation_identity(reservation, "gemini", "gemini-4-argon")
        budget.settle_tokens(reservation, "gemini", "gemini-4-argon", {
            "usage": {
                "total_input_tokens": 50,
                "total_output_tokens": 30,
                "total_thought_tokens": 10,
                "total_tokens": 90,
            }
        })
        report = budget.summary()
        self.assertEqual(report["totals"]["actual_tokens"], 90)
        self.assertEqual(report["totals"]["reserved_tokens"], 0)
        self.assertEqual(report["totals"]["input_tokens"], 50)
        self.assertEqual(report["totals"]["thought_tokens"], 10)
        self.assertFalse(report["case_text_or_credentials_persisted"])

    def test_missing_provider_usage_keeps_worst_case_reservation(self):
        reservation = budget.reserve_tokens(120)
        budget.settle_tokens(reservation, "gemini", "gemini-4-argon", {"status": "completed"})
        report = budget.summary()
        self.assertEqual(report["totals"]["actual_tokens"], 0)
        self.assertEqual(report["totals"]["reserved_tokens"], 120)
        self.assertEqual(report["totals"]["usage_unknown_calls"], 1)

    def test_http_meter_counts_counttokens_and_generation_and_records_actual_usage(self):
        replies = [
            {"totalTokens": 40},
            {"usageMetadata": {
                "promptTokenCount": 40,
                "candidatesTokenCount": 25,
                "thoughtsTokenCount": 5,
                "totalTokenCount": 70,
            }, "candidates": []},
        ]
        calls = []

        def fake_urlopen(request, *args, **kwargs):
            calls.append(request.full_url if isinstance(request, urllib.request.Request) else str(request))
            return FakeResponse(replies.pop(0))

        with patch.object(urllib.request, "urlopen", side_effect=fake_urlopen):
            budget.install_http_meter()
            request = urllib.request.Request(
                "https://generativelanguage.googleapis.com/v1beta/interactions",
                data=json.dumps({
                    "model": "gemini-4-argon",
                    "input": "safe test prompt",
                    "generation_config": {"max_output_tokens": 100},
                    "response_format": {"type": "text"},
                }).encode(),
                headers={"x-goog-api-key": "not-persisted-test-key"},
                method="POST",
            )
            with urllib.request.urlopen(request) as response:
                json.load(response)

        self.assertEqual(len(calls), 2)
        self.assertIn(":countTokens", calls[0])
        self.assertEqual(budget.summary()["totals"]["http_calls"], 2)
        self.assertEqual(budget.summary()["totals"]["actual_tokens"], 70)
        saved = Path(self.env["VALIDATION_API_BUDGET_DB"]).read_bytes()
        self.assertNotIn(b"safe test prompt", saved)
        self.assertNotIn(b"not-persisted-test-key", saved)

    def test_api_smoke_default_is_no_network_plan(self):
        from scripts import run_validation_api_smoke

        with patch("urllib.request.urlopen") as urlopen:
            with tempfile.TemporaryDirectory() as external:
                result = run_validation_api_smoke.main([
                    "--case-id", "sil_target_operations_issue1",
                    "--case-id", "sis_lopa_architecture_issue1",
                    "--case-id", "mcdc_vmodel_sil_issue1",
                    "--output-dir", str(Path(external) / "smoke"),
                ])
        self.assertEqual(result, 0)
        urlopen.assert_not_called()

    def test_api_smoke_live_mode_requires_isolated_validation_opt_in(self):
        from scripts import run_validation_api_smoke

        cases = [
            "sil_target_operations_issue1",
            "sis_lopa_architecture_issue1",
            "mcdc_vmodel_sil_issue1",
        ]
        with tempfile.TemporaryDirectory() as external, patch.dict("os.environ", {}, clear=True), patch(
            "scripts.run_validation_api_smoke.subprocess.run"
        ) as run:
            args = ["--output-dir", str(Path(external) / "smoke"), "--execute-live"]
            for case_id in cases:
                args.extend(("--case-id", case_id))
            result = run_validation_api_smoke.main(args)
        self.assertEqual(result, 2)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
