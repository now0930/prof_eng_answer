from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from study.master_topic_pack import grading_compatibility_payload, project_grading
from test_master_topic_pack_schema import _valid_record


def test_grading_projection_matches_legacy_sources_without_mutation() -> None:
    with tempfile.TemporaryDirectory(prefix="master-topic-projection-") as temp_dir:
        _test_grading_projection_matches_legacy_sources_without_mutation(Path(temp_dir))


def _test_grading_projection_matches_legacy_sources_without_mutation(tmp_path: Path) -> None:
    master = _valid_record()
    expected = {}
    for key, relative in master["legacy_topic_pack"]["source_files"].items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"topic_id": master["topic_id"], "source_key": key, "content": [key]}
        path.write_text(json.dumps(payload), encoding="utf-8")
        expected[key] = payload

    original = copy.deepcopy(master)
    projected = project_grading(tmp_path, master)
    assert projected["projection_id"] == "grading-projection-v1"
    assert projected["authority"] == "existing_topic_pack"
    assert projected["topic_id"] == master["topic_id"]
    assert projected["sources"] == expected
    assert grading_compatibility_payload(tmp_path, master) == expected
    assert master == original

    projected["sources"]["fact_anchor"]["content"].append("projection-only")
    assert expected["fact_anchor"]["content"] == ["fact_anchor"]


def test_grading_projection_fails_on_mismatched_legacy_topic_id() -> None:
    with tempfile.TemporaryDirectory(prefix="master-topic-mismatch-") as temp_dir:
        _test_grading_projection_fails_on_mismatched_legacy_topic_id(Path(temp_dir))


def _test_grading_projection_fails_on_mismatched_legacy_topic_id(tmp_path: Path) -> None:
    master = _valid_record()
    for key, relative in master["legacy_topic_pack"]["source_files"].items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        payload_topic_id = "wrong_topic_id" if key == "logic_check" else master["topic_id"]
        path.write_text(json.dumps({"topic_id": payload_topic_id}), encoding="utf-8")
    try:
        project_grading(tmp_path, master)
    except ValueError as exc:
        assert "topic_id mismatch" in str(exc)
    else:
        raise AssertionError("projection accepted a source owned by another topic")


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"MASTER_TOPIC_PACK_PROJECTION_TESTS={len(tests)}_PASS")
