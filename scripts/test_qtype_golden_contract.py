from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "calibration" / "qtype_golden"
VALIDATOR = REPO / "scripts" / "validate_qtype_golden_set.py"

QTYPES = {
    "PRINCIPLE_INTERPRETATION": "cases/principle_interpretation.json",
    "COMPARE_SELECTION": "cases/compare_selection.json",
    "DIAGNOSIS_ACTION": "cases/diagnosis_action.json",
    "IMPLEMENTATION_EVALUATION": "cases/implementation_evaluation.json",
}


class QTypeGoldenG0ContractTest(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *args],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_g0_contract_passes(self) -> None:
        proc = self.run_validator()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("QTYPE_GOLDEN_CONTRACT=PASS", proc.stdout)

    def test_g0_is_intentionally_incomplete(self) -> None:
        proc = self.run_validator("--require-complete")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("complete Golden Set requires exactly 3 cases", proc.stderr)

    def test_four_qtypes_and_five_lanes(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["question_types"]), set(QTYPES))
        self.assertEqual(set(manifest["parallel_plan"]["lanes"]), {"A", "B", "C", "D", "E"})
        self.assertEqual(manifest["parallel_plan"]["lanes"]["E"]["role"], "REGRESSION_RUNNER")

    def test_g0_case_files_are_empty_and_lane_owned(self) -> None:
        lanes = set()
        for qtype, rel_path in QTYPES.items():
            payload = json.loads((ROOT / rel_path).read_text(encoding="utf-8"))
            self.assertEqual(payload["question_type"], qtype)
            self.assertEqual(payload["cases"], [])
            self.assertNotIn(payload["lane"], lanes)
            lanes.add(payload["lane"])
        self.assertEqual(lanes, {"A", "B", "C", "D"})

    def test_level_threshold_contract(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        levels = manifest["score_policy"]["level_contract"]
        self.assertEqual(levels["LOW"]["total_max_exclusive"], 15.0)
        self.assertEqual(levels["PASS"]["total_min_inclusive"], 15.0)
        self.assertEqual(levels["PASS"]["total_max_exclusive"], 20.0)
        self.assertEqual(levels["HIGH"]["total_min_inclusive"], 20.0)
        self.assertEqual(levels["HIGH"]["total_max_inclusive"], 25.0)

    def test_release_complete_gate_is_deferred(self) -> None:
        text = (REPO / "scripts" / "validate_release.sh").read_text(encoding="utf-8")
        self.assertNotIn("validate_qtype_golden_set.py --require-complete", text)


if __name__ == "__main__":
    unittest.main()
