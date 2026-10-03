from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from study.content_update import (
    ContentUpdateError,
    propose_content_update,
    validate_content_update_proposal,
)
from test_master_topic_pack_schema import _valid_record


def _evidence(**overrides):
    value = {
        "source_id": "wp-post-101",
        "source_url": "https://example.org/wp-content/uploads/pressure-sensor.pdf",
        "source_version": "v2-2026-10-05",
        "source_content_sha256": "a" * 64,
        "locator": "PDF p. 4, 측정 원리",
        "excerpt": "제안 내용의 근거가 되는 원문 발췌",
    }
    value.update(overrides)
    return value


def test_content_update_proposal_is_evidence_linked_and_non_mutating() -> None:
    master = _valid_record()
    before = copy.deepcopy(master)
    proposal = propose_content_update(
        master,
        target={"source_key": "fact_anchor", "record_id": "fact-1", "field_path": ["statement"]},
        before_value="기존 설명",
        proposed_value="수정 제안 설명",
        change_reason="WordPress 원문 개정 반영",
        evidence=[_evidence()],
        proposed_at="2026-10-05T10:00:00+09:00",
    )
    assert master == before
    assert proposal["topic_id"] == master["topic_id"]
    assert proposal["base_revision"] == master["revision"]
    assert proposal["affected_views"] == ["grading", "training", "diagnosis"]
    assert proposal["status"] == "pending_approval"
    assert proposal["approval_required"] is True
    assert validate_content_update_proposal(proposal) == proposal

    schema = json.loads((ROOT / "schemas/content_update_proposal.schema.json").read_text(encoding="utf-8"))
    assert set(schema["required"]) == set(proposal)
    assert schema["additionalProperties"] is False


def test_content_update_rejects_unlinked_or_mismatched_evidence() -> None:
    master = _valid_record()
    kwargs = {
        "target": {"source_key": "model_answer", "record_id": "answer-1", "field_path": ["summary"]},
        "before_value": "old",
        "proposed_value": "new",
        "change_reason": "source correction",
        "proposed_at": "2026-10-05T10:00:00+09:00",
    }
    for evidence in (
        [_evidence(source_id="unlinked-source")],
        [_evidence(source_url="https://wrong.example/source.pdf")],
        [_evidence(source_content_sha256="not-a-hash")],
    ):
        try:
            propose_content_update(master, evidence=evidence, **kwargs)
        except ContentUpdateError:
            pass
        else:
            raise AssertionError("invalid source evidence was accepted")


def test_content_update_is_pending_only_and_requires_a_target_view() -> None:
    proposal = {
        "schema_version": "content-update-proposal-v1",
        "proposal_id": "proposal-1",
        "topic_id": "sensor_topic_id",
        "base_revision": 1,
        "proposed_at": "2026-10-05T10:00:00+09:00",
        "target": {"source_key": "fact_anchor", "record_id": "f1", "field_path": ["statement"]},
        "before_value": "old",
        "proposed_value": "new",
        "change_reason": "correction",
        "evidence": [_evidence()],
        "affected_views": ["training"],
        "status": "approved",
        "approval_required": True,
    }
    try:
        validate_content_update_proposal(proposal)
    except ContentUpdateError:
        pass
    else:
        raise AssertionError("approved status must not be forged into a pending proposal")


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"CONTENT_UPDATE_PROPOSAL_TESTS={len(tests)}_PASS")
