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
from study.master_topic_pack import load_master_topic_pack, project_training
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
        for source_key, relative_path in master["legacy_topic_pack"]["source_files"].items():
            source_path = repo / relative_path
            source_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {"topic_id": topic_id}
            if source_key == "fact_anchor":
                payload["anchors"] = [{"id": "fact-1", "statement": "old"}]
            elif source_key == "model_answer":
                payload["question_examples"] = ["Example question"]
            source_path.write_text(json.dumps(payload), encoding="utf-8")
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

            candidate_path = wordpress_catalog.prepare_content_update_candidate(
                database,
                proposal["proposal_id"],
                candidate_root=repo / "candidates",
            )
            manifest = json.loads((candidate_path / "manifest.json").read_text(encoding="utf-8"))
            candidate_master = load_master_topic_pack(
                candidate_path / "master_topic_packs" / f"{topic_id}.json"
            )
            assert manifest["application_status"] == "candidate_only_not_applied"
            assert manifest["affected_views"] == ["grading", "training", "diagnosis"]
            assert candidate_master["revision"] == master["revision"] + 1
            candidate_training = project_training(candidate_path, candidate_master)
            assert candidate_training["fact_anchors"][0]["statement"] == "new-a"
            assert json.loads(
                (repo / master["legacy_topic_pack"]["source_files"]["fact_anchor"]).read_text(encoding="utf-8")
            )["anchors"][0]["statement"] == "old"
            candidate_row = next(
                item for item in wordpress_catalog.list_content_update_proposals(database)
                if item["proposal_id"] == proposal["proposal_id"]
            )
            assert candidate_row["status"] == "candidate_ready"
            proposal_artifact = candidate_path / "proposals" / f"{proposal['proposal_id']}.json"
            proposal_artifact_bytes = proposal_artifact.read_bytes()
            proposal_artifact.write_bytes(proposal_artifact_bytes + b" ")
            try:
                wordpress_catalog.apply_content_update_candidate(
                    database,
                    proposal["proposal_id"],
                    applied_by="owner",
                )
            except ValueError as exc:
                assert "hash mismatch" in str(exc)
            else:
                raise AssertionError("tampered candidate artifact must be rejected")
            finally:
                proposal_artifact.write_bytes(proposal_artifact_bytes)

            try:
                wordpress_catalog.prepare_content_update_candidate(
                    database,
                    proposal["proposal_id"],
                    candidate_root=repo / "candidates",
                )
            except ValueError as exc:
                assert "already exists" in str(exc)
            else:
                raise AssertionError("candidate generation must not overwrite an existing bundle")

            try:
                wordpress_catalog.apply_content_update_candidate(
                    database,
                    proposal["proposal_id"],
                    applied_by="",
                )
            except ValueError as exc:
                assert "explicit apply identity" in str(exc)
            else:
                raise AssertionError("canonical apply must require an explicit identity")

            source_path = repo / master["legacy_topic_pack"]["source_files"]["fact_anchor"]
            source_before_failed_apply = source_path.read_bytes()
            write_atomically = wordpress_catalog._write_bytes_atomically
            write_calls = 0

            def fail_second_write(path, content, mode):
                nonlocal write_calls
                write_calls += 1
                if write_calls == 2:
                    raise OSError("simulated Master replacement failure")
                write_atomically(path, content, mode)

            with patch.object(wordpress_catalog, "_write_bytes_atomically", side_effect=fail_second_write):
                try:
                    wordpress_catalog.apply_content_update_candidate(
                        database,
                        proposal["proposal_id"],
                        applied_by="owner",
                    )
                except OSError as exc:
                    assert "simulated" in str(exc)
                else:
                    raise AssertionError("simulated second-file failure should abort apply")
            assert write_calls == 3  # source write, failed Master write, source rollback
            assert source_path.read_bytes() == source_before_failed_apply
            assert master_path.read_text(encoding="utf-8") == original_text
            assert next(
                item for item in wordpress_catalog.list_content_update_proposals(database)
                if item["proposal_id"] == proposal["proposal_id"]
            )["status"] == "candidate_ready"

            applied = wordpress_catalog.apply_content_update_candidate(
                database,
                proposal["proposal_id"],
                applied_by="owner",
            )
            assert applied["proposal"]["status"] == "applied"
            assert applied["proposal"]["applied_by"] == "owner"
            assert applied["master"]["revision"] == master["revision"] + 1
            assert master_path.read_text(encoding="utf-8") != original_text
            source_after_apply = json.loads(
                (repo / master["legacy_topic_pack"]["source_files"]["fact_anchor"]).read_text(encoding="utf-8")
            )
            assert source_after_apply["anchors"][0]["statement"] == "new-a"
            applied_row = next(
                item for item in wordpress_catalog.list_content_update_proposals(database)
                if item["proposal_id"] == proposal["proposal_id"]
            )
            assert applied_row["status"] == "applied"

            stale = _proposal(applied["master"], "stale")
            wordpress_catalog.save_content_update_proposal(database, stale)
            changed_master = dict(applied["master"], revision=applied["master"]["revision"] + 1)
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


def test_catalog_migrates_proposal_status_for_applied_candidates() -> None:
    import sqlite3

    with tempfile.TemporaryDirectory(prefix="wp-content-proposal-migration-") as directory:
        database = Path(directory) / "catalog.sqlite3"
        connection = sqlite3.connect(database)
        connection.execute(
            """CREATE TABLE content_update_proposals (
                proposal_id TEXT PRIMARY KEY, topic_id TEXT NOT NULL,
                base_revision INTEGER NOT NULL, proposal_json TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('pending_approval','approved','rejected','candidate_ready')),
                created_at TEXT NOT NULL, resolved_by TEXT, resolved_at TEXT, candidate_path TEXT
            )"""
        )
        connection.execute(
            "INSERT INTO content_update_proposals VALUES (?,?,?,?,?,?,?,?,?)",
            ("proposal-1", "topic_example_id", 1, "{}", "candidate_ready", "2026-10-05", None, None, "candidates/proposal-1"),
        )
        connection.commit()
        connection.close()

        migrated = wordpress_catalog.initialize_database(database)
        try:
            migrated.execute(
                "UPDATE content_update_proposals SET status='applied' WHERE proposal_id='proposal-1'"
            )
            assert migrated.execute(
                "SELECT status,candidate_path FROM content_update_proposals WHERE proposal_id='proposal-1'"
            ).fetchone() == ("applied", "candidates/proposal-1")
        finally:
            migrated.close()


if __name__ == "__main__":
    test_catalog_persists_decisions_without_writing_master_content()
    test_catalog_migrates_proposal_status_for_applied_candidates()
    print("WORDPRESS_CONTENT_PROPOSAL_STORE_TESTS=2_PASS")
