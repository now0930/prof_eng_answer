"""Stage 2 source boundary: metadata match is not grading approval."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sqlite3
import tempfile

import pytest

from study.wordpress_fact_projection import (
    WordPressFactProjectionError,
    load_source_catalog_read_only,
    project_claim_candidate,
    project_source_readiness,
)


ROOT = Path(__file__).resolve().parents[1]
TOPIC = "second_order_system_resonance_frequency_response"
SOURCE_ID = "fixture:post:1"
POST_URL = "https://example.org/wordpress/resonance/"
SOURCE_TEXT = "공진은 감쇠비 조건에 따라 달라진다."


def master(verified: bool = True) -> dict:
    value = json.loads((ROOT / "master_topic_packs" / f"{TOPIC}.json").read_text())
    value["sources"] = [{
        "source_id": SOURCE_ID, "source_type": "wordpress_post", "wordpress_url": POST_URL,
        "title": "합성 출처", "version": "1", "page": None, "section": "body",
        "content_sha256": "a" * 64,
        "updated_at": "2026-10-10T00:00:00+00:00",
        "verification_status": "verified" if verified else "unverified",
    }]
    return value


def catalog() -> dict:
    return {SOURCE_ID: {
        "source_id": SOURCE_ID, "source_url": POST_URL, "version": "1",
        "content_sha256": "a" * 64, "fetch_status": "available",
        "extracted_text": SOURCE_TEXT,
    }}


def claim() -> dict:
    return {
        "schema_version": "wordpress-claim-v1", "claim_id": "FACT-SYNTHETIC-001",
        "topic_id": TOPIC, "claim_type": "condition", "claim_text": SOURCE_TEXT,
        "evidence": [{
            "source_id": SOURCE_ID, "source_url": POST_URL, "source_version": "1",
            "source_content_sha256": "a" * 64, "locator": "section:body", "excerpt": SOURCE_TEXT,
        }],
        "target": {"source_key": "fact_anchor", "record_id": "fixture_anchor"},
        "review_status": "approved", "score_effect": "none",
    }


def binding() -> dict:
    return {
        "claim_id": "FACT-SYNTHETIC-001", "fact_id": "resonance_condition",
        "subject": "resonance", "predicate": "depends_on", "object": "damping_ratio",
        "conditions": ["second_order_system"],
    }


def test_source_readiness_distinguishes_verified_unverified_and_stale() -> None:
    assert project_source_readiness(master(), catalog())[0]["status"] == "verified"
    assert project_source_readiness(master(False), catalog())[0]["status"] == "unverified"
    no_baseline_hash = master()
    del no_baseline_hash["sources"][0]["content_sha256"]
    assert project_source_readiness(no_baseline_hash, catalog())[0]["status"] == "unverified"
    mismatched_hash = master()
    mismatched_hash["sources"][0]["content_sha256"] = "b" * 64
    assert project_source_readiness(mismatched_hash, catalog())[0]["status"] == "stale"
    changed = copy.deepcopy(catalog())
    changed[SOURCE_ID]["version"] = "2"
    assert project_source_readiness(master(), changed)[0]["status"] == "stale"
    changed[SOURCE_ID]["fetch_status"] = "metadata_only"
    assert project_source_readiness(master(), changed)[0]["status"] == "unavailable"


def test_claim_projection_remains_candidate_even_with_approved_claim() -> None:
    projected = project_claim_candidate(master(), claim(), binding(), catalog())
    assert projected["review_status"] == "candidate"
    assert projected["score_effect"] == "none"
    assert projected["source_refs"][0]["source_sha256"] == "a" * 64
    assert "fatal" not in projected and "score" not in projected


def test_claim_projection_rejects_unverified_or_changed_source() -> None:
    with pytest.raises(WordPressFactProjectionError, match="unverified"):
        project_claim_candidate(master(False), claim(), binding(), catalog())
    changed = copy.deepcopy(catalog())
    changed[SOURCE_ID]["extracted_text"] = "다른 원문"
    with pytest.raises(WordPressFactProjectionError, match="excerpt"):
        project_claim_candidate(master(), claim(), binding(), changed)
    changed = copy.deepcopy(claim())
    changed["evidence"][0]["source_content_sha256"] = "b" * 64
    with pytest.raises(WordPressFactProjectionError, match="revision"):
        project_claim_candidate(master(), changed, binding(), catalog())


def test_private_catalog_loader_is_read_only_and_scoped() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "sources.sqlite3"
        with sqlite3.connect(path) as connection:
            connection.execute(
                "CREATE TABLE sources (source_id TEXT, source_url TEXT, version TEXT, "
                "content_sha256 TEXT, fetch_status TEXT, extracted_text TEXT)"
            )
            connection.execute("INSERT INTO sources VALUES (?,?,?,?,?,?)", (
                SOURCE_ID, POST_URL, "1", "a" * 64, "available", SOURCE_TEXT,
            ))
        rows = load_source_catalog_read_only(path, {SOURCE_ID})
        assert list(rows) == [SOURCE_ID]
        assert project_source_readiness(master(), rows)[0]["status"] == "verified"
        with sqlite3.connect(path) as connection:
            assert connection.execute("SELECT count(*) FROM sources").fetchone()[0] == 1
