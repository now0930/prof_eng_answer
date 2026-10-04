"""Review provenance, retry, and transaction boundaries against a real catalog."""
from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

import wordpress_catalog as catalog


def test_review_application() -> None:
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "catalog.sqlite3"
        connection = catalog.initialize_database(database)
        connection.execute("INSERT INTO sync_runs(run_id,started_at,category_url,category_id) VALUES(1,'now','https://example.org',1)")
        connection.execute("""INSERT INTO posts(post_id,category_id,slug,url,title,excerpt,
            content_html,content_text,tags_json,categories_json,content_sha256,last_seen_run)
            VALUES(1,1,'post','https://example.org/post','post','','','','[]','[]','hash',1)""")
        connection.execute("""INSERT INTO sources(source_id,source_type,source_url,title,first_party)
            VALUES('wp-post:1','wordpress_post','https://example.org/post','post',1)""")
        connection.executemany("INSERT INTO post_sources VALUES(1,'wp-post:1','post',?)", [(0,), (1,)])
        connection.execute("INSERT INTO topic_links(post_id,topic_id,status,score,matched_terms_json,evidence) VALUES(1,'topic_alpha','pending_review',0.5,'[]','retrieval hint')")
        connection.commit()
        connection.close()
        with patch.object(catalog, "topic_catalog", return_value=[{"topic_id": "topic_alpha"}]), \
             patch.object(catalog, "materialize_waiting_proposals", return_value=0), \
             patch.object(catalog, "queue_source_proposal", side_effect=RuntimeError("queue failed")):
            try:
                catalog.review_topic_link(database, 1, "topic_alpha", "approve", reviewed_by="codex:delegated", evidence="Reviewed scope")
            except RuntimeError:
                pass
            else:
                raise AssertionError("queue failure was swallowed")
        with sqlite3.connect(database) as connection:
            assert connection.execute("SELECT status,reviewed_by FROM topic_links").fetchone() == ("pending_review", None)
        with patch.object(catalog, "topic_catalog", return_value=[{"topic_id": "topic_alpha"}]), \
             patch.object(catalog, "materialize_waiting_proposals", return_value=0), \
             patch.object(catalog, "queue_source_proposal", return_value="proposal") as queue:
            assert catalog.review_topic_link(database, 1, "topic_alpha", "approve", reviewed_by="codex:delegated", evidence="Reviewed scope") == 1
            assert queue.call_count == 1  # Same attachment at two positions is queued once.
            assert catalog.review_topic_link(database, 1, "topic_alpha", "approve", reviewed_by="different-reviewer") == 0
            assert queue.call_count == 1
            try:
                catalog.review_topic_link(database, 1, "topic_alpha", "reject")
            except ValueError:
                pass
            else:
                raise AssertionError("resolved decision was overwritten")
        with sqlite3.connect(database) as connection:
            status, reviewer, evidence = connection.execute("SELECT status,reviewed_by,evidence FROM topic_links").fetchone()
            assert status == "approved" and reviewer == "codex:delegated"
            assert evidence == "retrieval hint\nReviewed scope"


if __name__ == "__main__":
    test_review_application()
    print("WORDPRESS_TOPIC_LINK_REVIEW_APPLICATION_TESTS=1_PASS")
