from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.check_grading_integrity_drift import DEFAULT_BASELINE, check


EXPECTED_DIGEST = "afab409840e5b405daa73c58c88c9c10fc3ebd9c474cf05fa2d2bce08cb3c143"


def test_committed_integrity_baseline_has_no_drift() -> None:
    report = check()

    assert report["status"] == "PASS"
    assert report["semantic_sha256"] == EXPECTED_DIGEST
    assert report["semantic"]["regression_ids"] == [
        "SIL-TARGET-OPERATIONS-OVERGRADING-01",
        "SIS-LOPA-ARCHITECTURE-OVERGRADING-01",
        "MCDC-VMODEL-SIL-OVERGRADING-01",
    ]
    assert len(report["semantic"]["routing"]) == 4


def test_baseline_fingerprint_detects_semantic_expectation_change() -> None:
    baseline = json.loads(DEFAULT_BASELINE.read_text(encoding="utf-8"))
    baseline["expected_semantic_sha256"] = "0" * 64

    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "tampered.json"
        path.write_text(json.dumps(baseline, ensure_ascii=False), encoding="utf-8")
        try:
            check(path)
        except AssertionError as error:
            assert "semantic drift" in str(error)
        else:
            raise AssertionError("tampered drift fingerprint was accepted")


def test_neighbor_topics_do_not_acquire_issue1_owner() -> None:
    report = check()
    routing = {row["id"]: row for row in report["semantic"]["routing"]}

    assert routing["reactor_lopa_architecture_neighbor"]["topic_id"] == (
        "hazop_lopa_ipl_risk_reduction_sil_target_allocation"
    )
    assert routing["pst_final_element_neighbor"]["topic_id"] is None
    assert routing["mcdc_software_neighbor"]["topic_id"] is None


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    for name, test in tests:
        test()
        print(f"PASS: {name}")
    print(f"PASS: {len(tests)}/{len(tests)} grading integrity drift checks")


if __name__ == "__main__":
    main()
