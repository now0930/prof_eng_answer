"""The bulk audit is exhaustive but must never claim semantic verification."""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_remaining_fact_contracts import audit  # noqa: E402
from triage_remaining_fact_recheck import triage  # noqa: E402
from local_fact_general_review import prompt_for  # noqa: E402


def test_every_remaining_row_has_one_contract_disposition() -> None:
    rows, summary = audit(ROOT)
    queue, _ = triage(ROOT)
    assert len(rows) == summary["audited_remaining"] == len(queue) - 20
    assert len({row["fact_id"] for row in rows}) == len(rows)
    assert all(row["technical_verdict"] == "NOT_ASSESSED" for row in rows)
    assert summary["contract_status_counts"].get("CONTRACT_ISSUE", 0) == 0
    assert sum(summary["contract_status_counts"].values()) == len(rows)


def test_audit_is_deterministic_and_registry_read_only() -> None:
    path = ROOT / "grading/evidence/approved_fact_registry.json"
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    assert audit(ROOT) == audit(ROOT)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before


def test_local_prompt_prohibits_source_verification_claims() -> None:
    prompt = prompt_for({"statement": "Sample general claim", "relation": {"conditions": ["when calibrated"]},
                         "verification_refs": [{"authority_type": "standard", "citation": "Example standard"}]},
                        {"statement": "Sample anchor"})
    assert "NOT opened sources" in prompt
    assert "source verification" in prompt
    assert "Sample general claim" in prompt
