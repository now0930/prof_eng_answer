from __future__ import annotations

import json
import sqlite3
import tempfile
from pathlib import Path

from match_wordpress_posts_to_topic_packs import (
    build_topic_documents,
    rank_topics,
    retrieve_posts,
)


def _make_topic(root: Path, topic_id: str, heading: str, fact: str) -> None:
    folder = root / topic_id
    folder.mkdir(parents=True)
    (folder / "README.md").write_text(f"# {heading}\n\n{fact}\n", encoding="utf-8")
    (folder / "fact_anchor.json").write_text(
        json.dumps({"topic_id": topic_id, "core_facts": [fact]}, ensure_ascii=False),
        encoding="utf-8",
    )


def _make_database(path: Path, content: str = "UART start bit parity bit baud rate serial communication") -> None:
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        CREATE TABLE posts (
            post_id INTEGER PRIMARY KEY, title TEXT, url TEXT, excerpt TEXT,
            tags_json TEXT, content_text TEXT, content_sha256 TEXT
        );
        CREATE TABLE topic_links (
            post_id INTEGER, topic_id TEXT, status TEXT
        );
        CREATE TABLE sources (
            source_id TEXT PRIMARY KEY, source_type TEXT, title TEXT,
            content_sha256 TEXT, extracted_text TEXT, extraction_status TEXT,
            first_party INTEGER
        );
        CREATE TABLE post_sources (
            post_id INTEGER, source_id TEXT, position INTEGER
        );
        """
    )
    connection.execute(
        "INSERT INTO posts VALUES(1,?,?,?,?,?,?)",
        ("UART", "https://example.test/1", "", "[]", content, "body-sha"),
    )
    connection.execute(
        "INSERT INTO topic_links VALUES(1,'old_candidate','pending_review')"
    )
    connection.commit()
    connection.close()


def test_full_catalog_retrieval_is_ranked_cached_and_invalidated() -> None:
    with tempfile.TemporaryDirectory(prefix="wordpress-topic-retrieval-") as directory:
        root = Path(directory)
        topics = root / "topics"
        topics.mkdir()
        _make_topic(topics, "serial_communication", "Serial Communication", "UART start bit parity bit baud rate")
        _make_topic(topics, "temperature_measurement", "Temperature Measurement", "thermocouple reference junction")
        database = root / "catalog.sqlite3"
        _make_database(database)
        cache = root / "cache.sqlite3"

        docs, index_hash = build_topic_documents(topics)
        assert len(docs) == 2
        assert index_hash
        ranked = rank_topics("UART start bit parity bit baud rate", docs)
        assert ranked[0]["topic_id"] == "serial_communication"

        first = retrieve_posts(database, topics, cache)
        assert first["topic_count"] == 2
        assert first["cache_misses"] == 1
        assert first["posts"][0]["candidates"][0]["topic_id"] == "serial_communication"
        assert any(
            item.get("included_as") == "existing_pending_review"
            for item in first["posts"][0]["candidates"]
        )
        second = retrieve_posts(database, topics, cache)
        assert second["cache_hits"] == 1
        connection = sqlite3.connect(database)
        connection.execute(
            "UPDATE posts SET content_text=?,content_sha256=? WHERE post_id=1",
            ("thermocouple reference junction", "new-body-sha"),
        )
        connection.commit()
        connection.close()
        third = retrieve_posts(database, topics, cache)
        assert third["cache_misses"] == 1
        assert third["posts"][0]["candidates"][0]["topic_id"] == "temperature_measurement"


if __name__ == "__main__":
    test_full_catalog_retrieval_is_ranked_cached_and_invalidated()
    print("WORDPRESS_TOPIC_RETRIEVAL_TESTS=1_PASS")
