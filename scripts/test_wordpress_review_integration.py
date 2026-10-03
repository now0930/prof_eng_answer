from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import wordpress_catalog
from study.learning_runtime import _review_candidates
from study.master_topic_pack import load_master_topic_pack
from test_master_topic_pack_schema import _valid_record


def test_approved_catalog_change_flows_to_master_and_review_queue() -> None:
    topic_id = "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration"
    master = _valid_record()
    master["sources"] = []
    master["topic_id"] = topic_id
    master["legacy_topic_pack"]["source_root"] = f"rubrics/topic_packs/{topic_id}"
    for key in master["legacy_topic_pack"]["source_files"]:
        master["legacy_topic_pack"]["source_files"][key] = f"rubrics/topic_packs/{topic_id}/{key}.json"

    with tempfile.TemporaryDirectory(prefix="wordpress-review-integration-") as directory:
        repo = Path(directory)
        master_dir = repo / "master_topic_packs"
        master_dir.mkdir()
        (master_dir / f"{topic_id}.json").write_text(
            json.dumps(master), encoding="utf-8"
        )
        database = repo / "wordpress.sqlite3"
        with patch.object(wordpress_catalog, "ROOT", repo):
            connection = wordpress_catalog.initialize_database(database)
            cursor = connection.execute(
                "INSERT INTO sync_runs(started_at,category_url,category_id) VALUES(?,?,?)",
                ("2026-10-05T10:00:00+00:00", "https://example.org/category", 1),
            )
            run_id = cursor.lastrowid
            connection.execute(
                """INSERT INTO posts(post_id,category_id,slug,url,title,excerpt,content_html,
                   content_text,published_at,modified_at,featured_media_id,tags_json,
                   categories_json,content_sha256,last_seen_run)
                   VALUES(101,1,'sensor','https://example.org/sensor/','Sensor','','','','',
                   '',NULL,'[]','[]','post-hash',?)""",
                (run_id,),
            )
            connection.execute(
                """INSERT INTO sources(source_id,source_type,source_url,title,first_party,
                   version,updated_at,content_sha256) VALUES(?,?,?,?,1,?,?,?)""",
                (
                    "wp-post:101", "wordpress_post", "https://example.org/sensor/",
                    "Sensor v2", "v2", "2026-10-05T10:00:00+09:00", "hash-v2",
                ),
            )
            connection.execute(
                "INSERT INTO post_sources(post_id,source_id,link_text,position) VALUES(101,?,?,0)",
                ("wp-post:101", "Sensor"),
            )
            connection.execute(
                """INSERT INTO topic_links(post_id,topic_id,status,score,matched_terms_json,evidence)
                   VALUES(101,?,'approved',1.0,'[]','human approved')""",
                (topic_id,),
            )
            event_id = connection.execute(
                """INSERT INTO source_change_events(source_id,detected_at,old_sha256,new_sha256,
                   old_version,new_version,status) VALUES(?,?,?,?,?,?,'pending_topic_review')""",
                ("wp-post:101", "2026-10-05T10:00:00+00:00", "hash-v1", "hash-v2", "v1", "v2"),
            ).lastrowid
            assert wordpress_catalog.queue_proposals_for_approved_links(
                connection, "wp-post:101", event_id=event_id
            ) == 1
            connection.commit()
            proposal_id, status = connection.execute(
                "SELECT proposal_id,status FROM source_update_proposals WHERE event_id=?",
                (event_id,),
            ).fetchone()
            event_status = connection.execute(
                "SELECT status FROM source_change_events WHERE event_id=?", (event_id,)
            ).fetchone()[0]
            connection.close()
            assert status == "pending_approval"
            assert event_status == "pending_approval"

            attempt = {
                "topic_id": topic_id,
                "question_id": "q1",
                "question_text": "Explain the sensor.",
                "attempted_at": "2026-10-01T10:00:00+09:00",
                "last_reviewed_at": "2026-10-02T10:00:00+09:00",
                "next_review_at": "2026-10-30T10:00:00+09:00",
                "score": 19.0,
            }
            now = datetime.fromisoformat("2026-10-06T10:00:00+09:00")
            before = _review_candidates(
                [attempt], {topic_id: master}, {}, now=now, repository_root=repo
            )
            assert not any(item["reason"] == "recently_changed_topic" for item in before)

            wordpress_catalog.approve_master_proposal(database, proposal_id, "owner")
            approved = load_master_topic_pack(master_dir / f"{topic_id}.json")
            assert approved["revision"] == master["revision"] + 1
            assert approved["sources"][0]["updated_at"] == "2026-10-05T10:00:00+09:00"
            approved_candidates = _review_candidates(
                [attempt], {topic_id: approved}, {}, now=now, repository_root=repo
            )
            assert any(
                item["topic_id"] == topic_id and item["reason"] == "recently_changed_topic"
                for item in approved_candidates
            )
            connection = wordpress_catalog.initialize_database(database)
            assert connection.execute(
                "SELECT status FROM source_change_events WHERE event_id=?", (event_id,)
            ).fetchone()[0] == "applied"
            connection.close()


if __name__ == "__main__":
    test_approved_catalog_change_flows_to_master_and_review_queue()
    print("WORDPRESS_REVIEW_INTEGRATION_TESTS=1_PASS")
