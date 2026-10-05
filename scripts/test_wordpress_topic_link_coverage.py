"""Tests for the approved-link coverage KPI."""
from __future__ import annotations

import tempfile
from pathlib import Path

import wordpress_catalog as catalog


def test_topic_link_coverage() -> None:
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "catalog.sqlite3"
        connection = catalog.initialize_database(database)
        connection.execute(
            "INSERT INTO sync_runs(run_id,started_at,category_url,category_id) VALUES(1,'now','https://example.org',1)"
        )
        connection.executemany(
            "INSERT INTO topics(topic_id,title,terms_json) VALUES(?,?, '[]')",
            [
                ("topic_approved", "Approved pack"),
                ("topic_pending", "Pending-only pack"),
                ("topic_rejected", "Rejected-only pack"),
                ("topic_empty", "No-candidate pack"),
            ],
        )
        for post_id in range(1, 5):
            connection.execute(
                """INSERT INTO posts(post_id,category_id,slug,url,title,excerpt,
                   content_html,content_text,tags_json,categories_json,content_sha256,last_seen_run)
                   VALUES(?,1,?,?,?,'','','','[]','[]','hash',1)""",
                (post_id, f"post-{post_id}", f"https://example.org/{post_id}", f"post {post_id}"),
            )
        connection.executemany(
            """INSERT INTO topic_links(post_id,topic_id,status,score,matched_terms_json,evidence)
               VALUES(?,?,?,0,'[]','test')""",
            [
                (1, "topic_approved", "approved"),
                (2, "topic_pending", "pending_review"),
                (3, "topic_rejected", "rejected"),
            ],
        )
        connection.commit()
        connection.close()

        report = catalog.topic_link_coverage(database)
        assert report == {
            "schema_version": "wordpress-topic-link-coverage-v2",
            "metric": "wordpress_posts_without_approved_topic_pack_link",
            "definition": "Count WordPress posts with zero approved Topic Pack links; pending and rejected candidate pairs are not links.",
            "total_posts": 4,
            "posts_with_approved_link": 1,
            "posts_without_approved_link": 3,
            "posts_without_approved_link_percent": 75.0,
            "unlinked_with_pending_candidates": 1,
            "unlinked_with_rejected_candidates_only": 1,
            "unlinked_without_candidates": 1,
            "topic_pack_metric": "topic_packs_without_approved_blog_contribution",
            "topic_pack_definition": "Count existing Topic Packs with zero distinct WordPress posts in approved link status; this is a catalog coverage gap, not proof that no blog can contribute.",
            "total_topic_packs": 4,
            "topic_packs_with_approved_blog_contribution": 1,
            "topic_packs_without_approved_blog_contribution": 3,
            "topic_packs_without_approved_blog_contribution_percent": 75.0,
            "topic_pack_contribution_gaps": [
                {
                    "topic_id": "topic_empty",
                    "title": "No-candidate pack",
                    "approved_contributing_posts": 0,
                    "pending_candidate_posts": 0,
                    "pending_candidate_links": 0,
                    "rejected_candidate_posts": 0,
                    "rejected_candidate_links": 0,
                    "contribution_status": "no_candidates",
                },
                {
                    "topic_id": "topic_pending",
                    "title": "Pending-only pack",
                    "approved_contributing_posts": 0,
                    "pending_candidate_posts": 1,
                    "pending_candidate_links": 1,
                    "rejected_candidate_posts": 0,
                    "rejected_candidate_links": 0,
                    "contribution_status": "pending_candidates",
                },
                {
                    "topic_id": "topic_rejected",
                    "title": "Rejected-only pack",
                    "approved_contributing_posts": 0,
                    "pending_candidate_posts": 0,
                    "pending_candidate_links": 0,
                    "rejected_candidate_posts": 1,
                    "rejected_candidate_links": 1,
                    "contribution_status": "rejected_candidates_only",
                },
            ],
            "topic_pack_coverage": [
                {
                    "topic_id": "topic_approved",
                    "title": "Approved pack",
                    "approved_contributing_posts": 1,
                    "pending_candidate_posts": 0,
                    "pending_candidate_links": 0,
                    "rejected_candidate_posts": 0,
                    "rejected_candidate_links": 0,
                    "contribution_status": "covered",
                },
                {
                    "topic_id": "topic_empty",
                    "title": "No-candidate pack",
                    "approved_contributing_posts": 0,
                    "pending_candidate_posts": 0,
                    "pending_candidate_links": 0,
                    "rejected_candidate_posts": 0,
                    "rejected_candidate_links": 0,
                    "contribution_status": "no_candidates",
                },
                {
                    "topic_id": "topic_pending",
                    "title": "Pending-only pack",
                    "approved_contributing_posts": 0,
                    "pending_candidate_posts": 1,
                    "pending_candidate_links": 1,
                    "rejected_candidate_posts": 0,
                    "rejected_candidate_links": 0,
                    "contribution_status": "pending_candidates",
                },
                {
                    "topic_id": "topic_rejected",
                    "title": "Rejected-only pack",
                    "approved_contributing_posts": 0,
                    "pending_candidate_posts": 0,
                    "pending_candidate_links": 0,
                    "rejected_candidate_posts": 1,
                    "rejected_candidate_links": 1,
                    "contribution_status": "rejected_candidates_only",
                },
            ],
        }


if __name__ == "__main__":
    test_topic_link_coverage()
    print("WORDPRESS_TOPIC_LINK_COVERAGE_TESTS=1_PASS")
