"""Conservative precedence for bulk Fact screening."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from adjudicate_remaining_fact_review import action_for  # noqa: E402


def _contract(flags: str = "", status: str = "CONTRACT_PASS") -> dict:
    return {"flags": flags, "contract_status": status}


def _model(verdict: str = "GENERAL_OK", status: str = "MODEL_SCREENED") -> dict:
    return {"verdict": verdict, "status": status}


def test_model_cannot_override_source_and_numeric_flags() -> None:
    assert action_for(_contract("universal_wording_vendor_only"), _model()) == "SOURCE_SCOPE_REVIEW"
    assert action_for(_contract("company_or_model_scope_check"), _model()) == "SOURCE_SCOPE_REVIEW"
    assert action_for(_contract("standard_scope_check;numeric_condition_check"), _model()) == "SOURCE_SCOPE_REVIEW"
    assert action_for(_contract("numeric_condition_check"), _model()) == "NUMERIC_CONDITION_REVIEW"


def test_model_narrow_uncertain_or_error_stays_open() -> None:
    assert action_for(_contract(), _model("NARROW")) == "NARROW_CLAIM_REVIEW"
    assert action_for(_contract(), _model("UNCERTAIN")) == "HOLD_UNCERTAIN"
    assert action_for(_contract(), _model(status="MODEL_ERROR")) == "HOLD_CONTRACT_OR_MODEL_ERROR"
    assert action_for(_contract(status="CONTRACT_ISSUE"), _model()) == "HOLD_CONTRACT_OR_MODEL_ERROR"
    assert action_for(_contract(), _model()) == "GENERAL_PRINCIPLE_CANDIDATE"


def test_committed_full_review_is_complete_but_not_reapproved() -> None:
    with (ROOT / "reports/remaining_fact_review_actions_20261030.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    summary = json.loads((ROOT / "reports/remaining_fact_review_actions_20261030.json").read_text(encoding="utf-8"))
    assert len(rows) == summary["rows"] == 1272
    assert len({row["fact_id"] for row in rows}) == 1272
    assert summary["review_action_counts"] == {
        "GENERAL_PRINCIPLE_CANDIDATE": 663,
        "NARROW_CLAIM_REVIEW": 29,
        "NUMERIC_CONDITION_REVIEW": 230,
        "SOURCE_SCOPE_REVIEW": 350,
    }
    assert summary["final_technical_approvals"] == 0
    assert all(row["technical_verification"] == "NOT_SOURCE_VERIFIED" for row in rows)
