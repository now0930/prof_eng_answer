from pathlib import Path

import pytest

from grading.evidence.approved_fact_registry import load_approved_fact_registry
from grading.evidence.fact_grounded_contracts import FactGroundedContractError


ROOT = Path(__file__).resolve().parents[1]


def test_registry_has_only_explicitly_delegated_approved_facts():
    registry = load_approved_fact_registry(ROOT)
    assert len(registry["facts"]) == 3
    assert registry["approval_record"]["reviewer_id"] == "codex_with_user_delegation"
    assert all(row["score_effect"] == "none" for row in registry["facts"])


def test_registry_rejects_wrong_root():
    with pytest.raises(FactGroundedContractError):
        load_approved_fact_registry(Path("/tmp"))
