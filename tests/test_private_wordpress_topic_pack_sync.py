"""Private body sync must reject stale or corrupt sources without Git data."""

import hashlib
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from sync_private_wordpress_topic_packs import sync


TOPIC = "thermistor_temperature_sensor_ntc_ptc_characteristics_measurement_linearization"


def _fixture(tmp_path):
    source = tmp_path / "private"
    source.mkdir()
    target = tmp_path / "checkout"
    (target / "master_topic_packs").mkdir(parents=True)
    master_file = ROOT / "master_topic_packs" / f"{TOPIC}.json"
    master = json.loads(master_file.read_text())
    (target / "master_topic_packs" / master_file.name).write_text(json.dumps(master))
    ref = next(row for row in master["sources"] if row["source_id"] == "wp-post:9752")
    body = "Private training source text"
    row = {
        "source_id": ref["source_id"], "source_type": ref["source_type"],
        "wordpress_url": ref["wordpress_url"], "source_url": ref["wordpress_url"],
        "version": ref["version"], "extraction_status": "extracted",
        "extraction_method": "wordpress_rest_html", "extracted_text": body,
        "extracted_text_sha256": hashlib.sha256(body.encode()).hexdigest(),
    }
    payload = {"topic_id": TOPIC, "private": True, "sources": [row]}
    bundle = source / f"{TOPIC}.json"
    bundle.write_text(json.dumps(payload))
    return source, target, bundle, payload


def test_private_sync_restores_text_and_is_idempotent(tmp_path):
    source, target, bundle, _ = _fixture(tmp_path)
    assert sync(source, target, [TOPIC], verify_only=True) == [TOPIC]
    assert not (target / "data").exists()
    assert sync(source, target, [TOPIC]) == [TOPIC]
    restored = target / "data" / "wordpress_topic_packs" / bundle.name
    assert json.loads(restored.read_text())["sources"][0]["extracted_text"] == "Private training source text"
    assert restored.stat().st_mode & 0o777 == 0o600
    assert sync(source, target, [TOPIC]) == [TOPIC]


@pytest.mark.parametrize("mutation", ["version", "hash", "unlinked"])
def test_private_sync_rejects_unapproved_or_corrupt_body(tmp_path, mutation):
    source, target, bundle, payload = _fixture(tmp_path)
    row = payload["sources"][0]
    if mutation == "version":
        row["version"] = "new-unapproved-version"
    elif mutation == "hash":
        row["extracted_text"] = "changed without digest"
    else:
        row["source_id"] = "wp-post:unapproved"
    bundle.write_text(json.dumps(payload))
    with pytest.raises(ValueError):
        sync(source, target, [TOPIC])
    assert not (target / "data" / "wordpress_topic_packs" / bundle.name).exists()


def test_private_sync_refuses_to_replace_existing_body(tmp_path):
    source, target, bundle, payload = _fixture(tmp_path)
    sync(source, target, [TOPIC])
    payload["sources"][0]["extracted_text"] = "other valid body"
    payload["sources"][0]["extracted_text_sha256"] = hashlib.sha256(b"other valid body").hexdigest()
    bundle.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="reconcile manually"):
        sync(source, target, [TOPIC])
