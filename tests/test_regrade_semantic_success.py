import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from grading.quality.production_grade_gate import ProductionGradeFailure
from scripts import regrade_expert_accuracy_seed as regrade
from scripts.regrade_expert_accuracy_seed import _require_semantic_success


class RegradeSemanticSuccessTests(unittest.TestCase):
    def test_valid_semantic_result_passes(self):
        _require_semantic_success({
            "gemini_semantic_evaluation": {"ok": True, "parsed": {"layers": []}}
        }, "case-1")

    def test_provider_error_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "semantic provider failure"):
            _require_semantic_success({
                "gemini_semantic_evaluation": {
                    "ok": False, "parsed": None, "error": "HTTP 429"
                }
            }, "case-1")

    def test_missing_semantic_result_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "semantic provider failure"):
            _require_semantic_success({}, "case-1")


class RegradeProductionCollectionTests(unittest.TestCase):
    def test_collects_failures_for_all_cases_without_publishing_partial_predictions(self):
        cases = [{"case_id": "bad"}, {"case_id": "good"}]
        inspected = []

        def fake_grade(case, output_dir, image_count, **kwargs):
            inspected.append(case["case_id"])
            if case["case_id"] == "bad":
                raise ProductionGradeFailure(
                    "production grading incomplete: case=bad, reason=unresolved_requirement"
                )
            return {"total_score": 11.0}

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "results"
            with patch.dict("os.environ", {
                "VALIDATION_LIVE_API": "1",
                "VALIDATION_GEMINI_API_KEY": "independent-test-validation-key",
                "GEMINI_API_KEY": "different-fake-production-key",
            }, clear=False), patch.object(regrade, "load_jsonl", return_value=cases), patch.object(
                regrade, "_grade", side_effect=fake_grade
            ), patch.object(
                regrade, "prediction_from_grade",
                side_effect=lambda case_id, grade: {"case_id": case_id},
            ), patch.object(sys, "argv", [
                "regrade_expert_accuracy_seed.py", "--output-dir", str(output),
                "--require-production-success", "--collect-failures",
            ]):
                with self.assertRaises(SystemExit) as raised:
                    regrade.main()
            self.assertNotEqual(raised.exception.code, 0)
            self.assertEqual(inspected, ["bad", "good"])
            self.assertFalse((output / "predictions.jsonl").exists())
            rows = [
                json.loads(line) for line in
                (output / "case_results.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual([row["status"] for row in rows], ["FAILED", "PASS"])
            self.assertEqual(rows[0]["reason_code"], "unresolved_requirement")
            self.assertNotIn("answer", str(rows))

    def test_provider_exception_does_not_leak_private_message_to_case_report(self):
        error = RuntimeError("private answer and secret provider payload")
        self.assertEqual(regrade._safe_failure_reason(error), "execution_error")

    def test_failed_production_grade_remains_available_for_private_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "rubrics").mkdir()
            (root / "rubrics" / "default.json").write_text("{}", encoding="utf-8")
            grade = {
                "marker": "DETERMINISTIC_GRADING_PRIMARY_V1",
                "llm_verdict_authority": 0,
                "external_llm_required_for_verdict": False,
                "llm_score_authority": "none",
            }
            with patch.object(regrade, "ROOT", root), patch.object(
                regrade, "_fixture_input", return_value="문제: 예시\\n답안: 합성 답안"
            ), patch.object(
                regrade, "normalize_grade_submission",
                return_value={"normalized_text": "문제: 예시\\n답안: 합성 답안"},
            ), patch.object(
                regrade, "run_agent_pipeline", return_value=("{}", grade)
            ), patch.object(
                regrade, "reconcile_grade_score", side_effect=lambda **kw: kw["parsed"]
            ), patch.object(
                regrade, "finalize_grade_after_score_reconciliation",
                side_effect=lambda value: value,
            ), patch.object(
                regrade, "attach_submission_normalization",
                side_effect=lambda value, _: value,
            ):
                with self.assertRaisesRegex(
                    ProductionGradeFailure, "argon_de_not_authoritative"
                ):
                    regrade._grade(
                        {"case_id": "synthetic"}, root / "output", 0,
                        require_production_success=True,
                    )
            self.assertTrue((root / "output" / "synthetic" / "grade.json").is_file())


if __name__ == "__main__":
    unittest.main()
