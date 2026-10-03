from __future__ import annotations

import copy
import sys
from datetime import datetime


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from study.master_topic_pack import (
    MasterTopicPackError,
    load_master_topic_pack,
    project_diagnosis,
    project_training,
    validate_source_reference,
)
from study.learning_runtime import _review_candidates
from study.source_update import SourceUpdateError, apply_approved_source_update, find_topics_for_source, preview_source_update, propose_source_update
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
    previewed = preview_source_update(master, proposal)
    assert previewed["revision"] == master["revision"] + 1
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


def test_only_approved_wordpress_source_change_enters_review_candidates() -> None:
    master = _valid_record()
    master["sources"] = []
    attempt = {
        "topic_id": master["topic_id"],
        "question_id": "question-1",
        "question_text": "Explain the topic.",
        "attempted_at": "2026-10-01T10:00:00+09:00",
        "last_reviewed_at": "2026-10-02T10:00:00+09:00",
        "next_review_at": "2026-10-30T10:00:00+09:00",
        "score": 19.0,
    }
    now = datetime.fromisoformat("2026-10-06T10:00:00+09:00")
    pending = propose_source_update(
        master,
        _reference(version="v2", updated_at="2026-10-05T10:00:00+09:00"),
        proposed_at="2026-10-05T10:01:00+09:00",
    )
    assert not master["sources"]
    before_approval = _review_candidates(
        [attempt], {master["topic_id"]: master}, {}, now=now, repository_root=ROOT
    )
    assert not any(item["reason"] == "recently_changed_topic" for item in before_approval)

    approved_master = apply_approved_source_update(master, pending, approved_by="owner")
    after_approval = _review_candidates(
        [attempt], {approved_master["topic_id"]: approved_master}, {}, now=now, repository_root=ROOT
    )
    assert any(
        item["topic_id"] == master["topic_id"] and item["reason"] == "recently_changed_topic"
        for item in after_approval
    )
    assert not master["sources"]


def test_source_reference_approval_does_not_rewrite_any_view_content() -> None:
    topic_id = "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration"
    master = load_master_topic_pack(ROOT / "master_topic_packs" / f"{topic_id}.json")
    before = {
        "training": project_training(ROOT, master),
        "diagnosis": project_diagnosis(ROOT, master),
    }
    reference = _reference(
        source_id="wp-contract-provenance-only",
        wordpress_url="https://example.org/approved-reference/",
        source_url="https://example.org/approved-reference.pdf",
        updated_at="2026-10-05T10:00:00+09:00",
    )
    proposal = propose_source_update(
        master, reference, proposed_at="2026-10-05T10:01:00+09:00"
    )
    updated = apply_approved_source_update(master, proposal, approved_by="owner")
    after = {
        "training": project_training(ROOT, updated),
        "diagnosis": project_diagnosis(ROOT, updated),
    }
    assert after == before


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"WORDPRESS_SOURCE_TESTS={len(tests)}_PASS")
