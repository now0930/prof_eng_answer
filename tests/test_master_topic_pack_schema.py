from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from study.master_topic_pack import MasterTopicPackError, validate_master_topic_pack


def _valid_record() -> dict:
    topic_id = "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration"
    source_root = f"rubrics/topic_packs/{topic_id}"
    return {
        "schema_version": "master-topic-pack-v1",
        "topic_id": topic_id,
        "title_ko": "압전식 센서",
        "revision": 1,
        "legacy_topic_pack": {
            "source_root": source_root,
            "source_files": {
                "fact_anchor": f"{source_root}/fact_anchor.json",
                "logic_check": f"{source_root}/logic_check.json",
                "model_answer": f"{source_root}/model_answer.json",
                "topic_importance": f"{source_root}/topic_importance.json",
            },
        },
        "projections": {
            "grading": {
                "projection_id": "grading-projection-v1",
                "authority": "existing_topic_pack",
                "source_keys": ["fact_anchor", "logic_check", "model_answer", "topic_importance"],
            },
            "training": {
                "projection_id": "training-projection-v1",
                "content_sources": ["fact_anchor", "model_answer"],
                "daily_target": 2,
            },
            "diagnosis": {
                "projection_id": "diagnosis-projection-v1",
                "content_sources": ["fact_anchor", "logic_check"],
                "dimensions": ["format", "content", "reasoning", "application", "verification"],
            },
        },
        "sources": [{
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
        }],
        "source_update_policy": {"mode": "proposal_only", "approval_required": True},
    }


def test_master_schema_is_versioned_and_strict() -> None:
    schema = json.loads((ROOT / "schemas/master_topic_pack.schema.json").read_text(encoding="utf-8"))
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["properties"]["schema_version"]["const"] == "master-topic-pack-v1"
    assert set(schema["required"]) == set(_valid_record())
    assert schema["additionalProperties"] is False
    validate_master_topic_pack(_valid_record())


def test_schema_rejects_missing_grading_source_and_unsafe_path() -> None:
    record = _valid_record()
    del record["legacy_topic_pack"]["source_files"]["logic_check"]
    try:
        validate_master_topic_pack(record)
    except MasterTopicPackError:
        pass
    else:
        raise AssertionError("missing required grading source was accepted")

    record = _valid_record()
    record["legacy_topic_pack"]["source_root"] = "../outside"
    try:
        validate_master_topic_pack(record)
    except MasterTopicPackError:
        pass
    else:
        raise AssertionError("unsafe relative path was accepted")


def test_wordpress_source_requires_valid_url_and_user_approval_policy() -> None:
    record = _valid_record()
    record["sources"][0]["wordpress_url"] = None
    try:
        validate_master_topic_pack(record)
    except MasterTopicPackError:
        pass
    else:
        raise AssertionError("WordPress reference without URL was accepted")

    record = _valid_record()
    record["source_update_policy"]["approval_required"] = False
    try:
        validate_master_topic_pack(record)
    except MasterTopicPackError:
        pass
    else:
        raise AssertionError("unapproved automatic source updates were accepted")


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"MASTER_TOPIC_PACK_SCHEMA_TESTS={len(tests)}_PASS")
