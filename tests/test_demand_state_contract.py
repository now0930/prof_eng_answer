import unittest
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from demand_state_contract import (
    normalize_internal_state,
    normalize_state,
    resolve_states,
)


class DemandStateContractTests(unittest.TestCase):
    def test_aliases_have_one_canonical_meaning(self):
        self.assertEqual(normalize_state("present"), "CORRECT")
        self.assertEqual(normalize_state("incorrect"), "WRONG")
        self.assertEqual(normalize_state("absent"), "MISSING")
        self.assertEqual(normalize_internal_state("wrong"), "incorrect")

    def test_unknown_is_prediction_only(self):
        with self.assertRaises(ValueError):
            normalize_state("unknown")
        self.assertEqual(normalize_state("unknown", allow_unknown=True), "UNKNOWN")

    def test_conservative_precedence_is_deterministic(self):
        self.assertEqual(resolve_states(["correct", "partial"]), "PARTIAL")
        self.assertEqual(resolve_states(["missing", "wrong"]), "WRONG")


if __name__ == "__main__":
    unittest.main()
