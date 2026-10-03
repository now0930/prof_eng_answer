from __future__ import annotations

import copy
import sys


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from study.master_topic_pack import MasterTopicPackError, validate_source_reference
from study.source_update import SourceUpdateError, apply_approved_source_update, find_topics_for_source, propose_source_update
from test_master_topic_pack_schema import _valid_record


def _reference(**overrides):
    result = {
        "source_id": "wp-post-101",
        "source_type": "wordpress_post",
        "wordpress_url": "https://example.org/pressure-sensor/",
        "source_url": "https://example.org/wp-content/uploads/pressure-sensor.pdf",
        "title": "압전식 센서 정리",
        "version": "2026-10-03",
        "page": 4,
        "section": "측정 원리",
        "updated_at": "2026-10-03T09:00:00+09:00",
        "verification_status": "verified",
    }
    result.update(overrides)
    return result


def test_wordpress_reference_contract_requires_source_identity_and_url() -> None:
    assert validate_source_reference(_reference())["source_id"] == "wp-post-101"
    for bad in (_reference(wordpress_url=None), _reference(source_type="unknown"), _reference(updated_at="yesterday")):
        try:
            validate_source_reference(bad)
        except MasterTopicPackError:
            pass
        else:
            raise AssertionError("invalid source reference was accepted")


def test_source_update_requires_approval_and_revision_match() -> None:
    master = _valid_record()
    original = copy.deepcopy(master)
    proposal = propose_source_update(master, _reference(title="Updated title"), proposed_at="2026-10-04T10:00:00+09:00")
    assert proposal["status"] == "pending_approval"
    assert master == original
    try:
        apply_approved_source_update(master, proposal, approved_by=None)
    except SourceUpdateError as exc:
        assert "approver" in str(exc)
    else:
        raise AssertionError("proposal applied without approval identity")

    updated = apply_approved_source_update(master, proposal, approved_by="owner")
    assert updated["revision"] == master["revision"] + 1
    assert updated["sources"][0]["title"] == "Updated title"
    stale_proposal = dict(proposal, base_revision=master["revision"] + 1)
    try:
        apply_approved_source_update(master, stale_proposal, approved_by="owner")
    except SourceUpdateError as exc:
        assert "revision" in str(exc)
    else:
        raise AssertionError("stale proposal was accepted")


def test_source_to_topic_lookup_supports_change_discovery() -> None:
    master = _valid_record()
    assert find_topics_for_source([master], "wp-post-101") == [master["topic_id"]]
    assert find_topics_for_source([master], "missing-source") == []


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"WORDPRESS_SOURCE_TESTS={len(tests)}_PASS")
