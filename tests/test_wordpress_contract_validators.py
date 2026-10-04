from __future__ import annotations

import csv
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validate_wordpress_decisions import BASE_COLUMNS, DECISION_COLUMNS, validate_decisions
from scripts.validate_wordpress_source_pack import validate_source_pack
from study.wordpress_claims import WordPressClaimError, validate_wordpress_claim


def _write(path: Path, fields: list[str], row: dict[str, str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerow(row)


def _base_row() -> dict[str, str]:
    return {field: "" for field in BASE_COLUMNS} | {
        "post_id": "1",
        "link_status": "pending_review",
        "candidate_topic_id": "example_topic_id",
        "decision_status": "deferred",
    }


def test_decision_validator_allows_pending_dry_run(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    decisions = tmp_path / "decisions.csv"
    row = _base_row()
    _write(source, BASE_COLUMNS, row)
    _write(decisions, BASE_COLUMNS + DECISION_COLUMNS, row | {field: "" for field in DECISION_COLUMNS})
    result = validate_decisions(source, decisions)
    assert result["valid"] is True
    assert result["counts"]["decision:pending"] == 1


def test_decision_validator_rejects_approval_without_evidence(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    decisions = tmp_path / "decisions.csv"
    row = _base_row()
    _write(source, BASE_COLUMNS, row)
    decision = row | {
        "suggested_decision": "approve",
        "final_decision": "approve",
        "final_topic_id": "example_topic_id",
        "reviewed_by": "reviewer",
        "reviewed_at": "2026-10-05T00:00:00+09:00",
        "final_evidence": "",
        "final_notes": "",
    }
    _write(decisions, BASE_COLUMNS + DECISION_COLUMNS, decision)
    result = validate_decisions(source, decisions, topic_pack_root=tmp_path)
    assert result["valid"] is False
    assert any("final_evidence" in error for error in result["errors"])


def test_source_pack_validator_is_read_only_and_checks_external_text(tmp_path: Path) -> None:
    database = tmp_path / "catalog.sqlite3"
    connection = sqlite3.connect(database)
    connection.executescript(
        """
        CREATE TABLE posts (post_id INTEGER PRIMARY KEY);
        CREATE TABLE sources (source_id TEXT PRIMARY KEY, source_type TEXT, source_url TEXT,
          first_party INTEGER, fetch_status TEXT, extraction_status TEXT,
          extraction_method TEXT, extracted_text TEXT);
        CREATE TABLE post_sources (post_id INTEGER, source_id TEXT);
        CREATE TABLE topics (topic_id TEXT PRIMARY KEY);
        CREATE TABLE topic_links (post_id INTEGER, topic_id TEXT, status TEXT);
        INSERT INTO posts VALUES (1);
        INSERT INTO sources VALUES ('wp-post:1','wordpress_post','https://now0930.pe.kr/wordpress/x',1,'available','extracted','wordpress_rest_html','text');
        INSERT INTO topics VALUES ('example_topic');
        INSERT INTO topic_links VALUES (1,'example_topic','pending_review');
        """
    )
    connection.commit()
    connection.close()
    result = validate_source_pack(database, tmp_path / "masters")
    assert result["valid"] is True
    assert result["integrity"] == "ok"


def test_wordpress_claim_requires_provenance_and_no_score_effect() -> None:
    evidence = {
        "source_id": "wp-post:1",
        "source_url": "https://now0930.pe.kr/wordpress/example",
        "source_version": "2026-10-05T00:00:00+00:00",
        "source_content_sha256": "a" * 64,
        "locator": "Chapter 1, section 2",
        "excerpt": "A reviewed technical claim.",
    }
    claim = {
        "schema_version": "wordpress-claim-v1",
        "claim_id": "FACT-EXAMPLE-001",
        "topic_id": "example_topic_id",
        "claim_type": "definition",
        "claim_text": "A reviewed technical claim.",
        "evidence": [evidence],
        "target": {"source_key": "fact_anchor", "record_id": "FACT-EXAMPLE-001"},
        "review_status": "human_review_required",
        "score_effect": "none",
    }
    assert validate_wordpress_claim(claim)["claim_id"] == "FACT-EXAMPLE-001"
    claim["score_effect"] = "grading"
    try:
        validate_wordpress_claim(claim)
    except WordPressClaimError:
        pass
    else:
        raise AssertionError("score-affecting WordPress claim must be rejected")
