import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

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


if __name__ == "__main__":
    unittest.main()
