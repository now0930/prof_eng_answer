from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import wordpress_catalog
from study.content_update import propose_content_update
from test_master_topic_pack_schema import _valid_record


def _proposal(master, suffix="a"):
    return propose_content_update(
        master,
        target={"source_key": "fact_anchor", "record_id": "fact-1", "field_path": ["statement"]},
        before_value="old",
        proposed_value=f"new-{suffix}",
        change_reason="source revision reviewed",
        evidence=[{
            "source_id": "wp-post-101",
            "source_url": "https://example.org/wp-content/uploads/pressure-sensor.pdf",
            "source_version": "v2",
            "source_content_sha256": "b" * 64,
            "locator": "PDF p. 4",
            "excerpt": "evidence excerpt",
        }],
        proposed_at="2026-10-05T10:00:00+09:00",
    )


def test_catalog_persists_decisions_without_writing_master_content() -> None:
    master = _valid_record()
    topic_id = master["topic_id"]
    with tempfile.TemporaryDirectory(prefix="wp-content-proposal-store-") as directory:
        repo = Path(directory)
        master_dir = repo / "master_topic_packs"
        master_dir.mkdir()
        master_path = master_dir / f"{topic_id}.json"
        master_path.write_text(json.dumps(master), encoding="utf-8")
        original_text = master_path.read_text(encoding="utf-8")
        database = repo / "catalog.sqlite3"
        with patch.object(wordpress_catalog, "ROOT", repo):
            proposal = _proposal(master)
            wordpress_catalog.save_content_update_proposal(database, proposal)
            listed = wordpress_catalog.list_content_update_proposals(database)
            assert len(listed) == 1
            assert listed[0]["status"] == "pending_approval"

            approved = wordpress_catalog.resolve_content_update_proposal(
                database,
                proposal["proposal_id"],
                decision="approve",
                reviewed_by="owner",
            )
            assert approved["status"] == "approved"
            assert approved["approved_by"] == "owner"
            assert master_path.read_text(encoding="utf-8") == original_text

            stale = _proposal(master, "stale")
            wordpress_catalog.save_content_update_proposal(database, stale)
            changed_master = dict(master, revision=master["revision"] + 1)
            master_path.write_text(json.dumps(changed_master), encoding="utf-8")
            try:
                wordpress_catalog.resolve_content_update_proposal(
                    database,
                    stale["proposal_id"],
                    decision="approve",
                    reviewed_by="owner",
                )
            except ValueError as exc:
                assert "stale" in str(exc)
            else:
                raise AssertionError("stale proposal should not be approved")
            assert next(
                item for item in wordpress_catalog.list_content_update_proposals(database)
                if item["proposal_id"] == stale["proposal_id"]
            )["status"] == "pending_approval"

            rejected = _proposal(changed_master, "reject")
            wordpress_catalog.save_content_update_proposal(database, rejected)
            result = wordpress_catalog.resolve_content_update_proposal(
                database,
                rejected["proposal_id"],
                decision="reject",
                reviewed_by="owner",
            )
            assert result["status"] == "rejected"


if __name__ == "__main__":
    test_catalog_persists_decisions_without_writing_master_content()
    print("WORDPRESS_CONTENT_PROPOSAL_STORE_TESTS=1_PASS")
