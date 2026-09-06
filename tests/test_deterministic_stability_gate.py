import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


class DeterministicStabilityGateTests(unittest.TestCase):
    def test_two_full_replays_are_exact_and_provider_free(self):
        completed = subprocess.run(
            [sys.executable, "scripts/run_deterministic_stability_gate.py", "--require-stable"],
            cwd=REPO, check=True, capture_output=True, text=True,
        )
        report = json.loads(completed.stdout)
        self.assertEqual(report["decision"], "STABLE")
        self.assertEqual(report["provider_calls"], 0)
        self.assertEqual(report["run_count"], 2)


if __name__ == "__main__":
    unittest.main()
