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
LEVELS = {"LOW", "PASS", "HIGH"}


class QTypeGoldenCompleteContractTest(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *args],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_complete_contract_validator_passes(self) -> None:
        proc = self.run_validator("--require-complete")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("QTYPE_GOLDEN_CONTRACT=PASS", proc.stdout)
        self.assertIn("QTYPE_GOLDEN_COMPLETE=PASS", proc.stdout)

    def test_non_complete_mode_still_validates_collections(self) -> None:
        proc = self.run_validator()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("QTYPE_GOLDEN_COLLECTION_CONTRACT=PASS", proc.stdout)

    def test_manifest_is_complete_12_case_state(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["state"], "COMPLETE_12_CASES")
        self.assertEqual(manifest["integrated_case_count"], 12)
        self.assertEqual(set(manifest["question_types"]), set(QTYPES))
        self.assertEqual(
            manifest["integration_state"]["release_gate"],
            "DEFERRED_TO_NEXT_MASTER_STEP",
        )
        self.assertEqual(
            manifest["integration_state"]["production_acceptance"],
            "NOT_YET_RUN",
        )

    def test_each_qtype_has_exact_low_pass_high(self) -> None:
        total = 0
        for qtype, rel_path in QTYPES.items():
            payload = json.loads((ROOT / rel_path).read_text(encoding="utf-8"))
            self.assertEqual(payload["question_type"], qtype)
            cases = payload["cases"]
            self.assertEqual(len(cases), 3)
            self.assertEqual({case["answer_level"] for case in cases}, LEVELS)
            self.assertEqual(len({case["case_id"] for case in cases}), 3)
            total += len(cases)
        self.assertEqual(total, 12)

    def test_level_threshold_contract_is_preserved(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        levels = manifest["score_policy"]["level_contract"]
        self.assertEqual(levels["LOW"]["total_max_exclusive"], 15.0)
        self.assertEqual(levels["PASS"]["total_min_inclusive"], 15.0)
        self.assertEqual(levels["PASS"]["total_max_exclusive"], 20.0)
        self.assertEqual(levels["HIGH"]["total_min_inclusive"], 20.0)
        self.assertEqual(levels["HIGH"]["total_max_inclusive"], 25.0)

    def test_release_complete_gate_is_still_deferred(self) -> None:
        release_text = (REPO / "scripts" / "validate_release.sh").read_text(encoding="utf-8")
        self.assertNotIn(
            "validate_qtype_golden_set.py --require-complete",
            release_text,
        )


if __name__ == "__main__":
    unittest.main()
