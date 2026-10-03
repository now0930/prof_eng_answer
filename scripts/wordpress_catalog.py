#!/usr/bin/env python3
"""Build a local searchable catalog of one WordPress category and its sources.

The catalog stores public post text and source metadata in SQLite. First-party
PDFs are downloaded to a temporary directory, digitally extracted page by
page, then locally OCRed with Tesseract (Korean and English) where needed.
Binary assets are never copied into the database. Topic links are suggestions
that require review before a Master Topic Pack update proposal is created.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import stat
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlparse, urlunparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT))
from study.master_topic_pack import (
    load_legacy_topic_sources,
    validate_master_topic_pack,
)
from study.content_update import (
    approve_content_update,
    apply_approved_content_update,
    mark_content_update_applied,
    reject_content_update,
    validate_content_update_against_master,
    validate_content_update_proposal,
)
from study.source_update import apply_approved_source_update, propose_source_update


DEFAULT_CATEGORY_URL = (
    "https://now0930.pe.kr/wordpress/category/"
    "%ec%82%b0%ec%97%85%ea%b3%84%ec%b8%a1%ec%a0%9c%ec%96%b4%ea%b8%b0%ec%88%a0%ec%82%ac/"
)
DEFAULT_DB = ROOT / "data" / "wordpress_sources.sqlite3"
USER_AGENT = "prof-eng-answer-source-catalog/1.0 (+local personal knowledge index)"
ALLOWED_HOST = "now0930.pe.kr"
MAX_DOWNLOAD_BYTES = 128 * 1024 * 1024
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".tif", ".tiff"}
HTML_SUFFIXES = {".htm", ".html", ".xhtml"}
PDF_SUFFIXES = {".pdf"}
STOP_WORDS = {
    "the", "and", "for", "with", "from", "into", "about", "using", "based",
    "industrial", "instrumentation", "control", "system", "systems", "design",
    "guide", "chapter", "lesson", "study", "summary", "overview", "개요",
    "정리", "설명", "기술", "산업", "계측", "제어", "시스템", "방법", "기준",
}


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS sync_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    category_url TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    expected_posts INTEGER NOT NULL DEFAULT 0,
    posts_seen INTEGER NOT NULL DEFAULT 0,
    sources_seen INTEGER NOT NULL DEFAULT 0,
    pdfs_ocred INTEGER NOT NULL DEFAULT 0,
    errors INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS posts (
    post_id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    slug TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    excerpt TEXT NOT NULL,
    content_html TEXT NOT NULL,
    content_text TEXT NOT NULL,
    published_at TEXT,
    modified_at TEXT,
    featured_media_id INTEGER,
    tags_json TEXT NOT NULL,
    categories_json TEXT NOT NULL,
    content_sha256 TEXT NOT NULL,
    last_seen_run INTEGER NOT NULL REFERENCES sync_runs(run_id)
);
CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL CHECK(source_type IN
      ('wordpress_post','wordpress_page','pdf','image','overleaf','html','other')),
    source_url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    mime_type TEXT,
    media_id INTEGER,
    file_name TEXT,
    first_party INTEGER NOT NULL CHECK(first_party IN (0,1)),
    version TEXT,
    updated_at TEXT,
    content_sha256 TEXT,
    byte_size INTEGER,
    fetch_status TEXT NOT NULL DEFAULT 'metadata_only',
    extraction_status TEXT NOT NULL DEFAULT 'not_applicable',
    extraction_method TEXT,
    page_count INTEGER,
    extracted_text TEXT,
    indexed_at TEXT
);
CREATE TABLE IF NOT EXISTS topics (
    topic_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    terms_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS post_sources (
    post_id INTEGER NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,
    source_id TEXT NOT NULL REFERENCES sources(source_id) ON DELETE CASCADE,
    link_text TEXT,
    position INTEGER NOT NULL,
    PRIMARY KEY(post_id, source_id, position)
);
CREATE TABLE IF NOT EXISTS topic_links (
    post_id INTEGER NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,
    topic_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pending_review','approved','rejected')),
    score REAL NOT NULL,
    matched_terms_json TEXT NOT NULL,
    evidence TEXT NOT NULL,
    reviewed_by TEXT,
    reviewed_at TEXT,
    PRIMARY KEY(post_id, topic_id)
);
CREATE TABLE IF NOT EXISTS sync_errors (
    run_id INTEGER NOT NULL REFERENCES sync_runs(run_id) ON DELETE CASCADE,
    source_url TEXT,
    stage TEXT NOT NULL,
    error TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS source_change_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    detected_at TEXT NOT NULL,
    old_sha256 TEXT,
    new_sha256 TEXT,
    old_version TEXT,
    new_version TEXT,
    status TEXT NOT NULL CHECK(status IN ('pending_topic_review','pending_approval','approved','applied'))
);
CREATE TABLE IF NOT EXISTS source_update_proposals (
    proposal_id TEXT PRIMARY KEY,
    event_id INTEGER REFERENCES source_change_events(event_id),
    topic_id TEXT NOT NULL,
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    base_revision INTEGER NOT NULL,
    proposal_json TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('waiting_for_master','pending_approval','applied')),
    created_at TEXT NOT NULL,
    approved_by TEXT,
    approved_at TEXT
);
CREATE TABLE IF NOT EXISTS content_update_proposals (
    proposal_id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    base_revision INTEGER NOT NULL,
    proposal_json TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pending_approval','approved','rejected','candidate_ready','applied')),
    created_at TEXT NOT NULL,
    resolved_by TEXT,
    resolved_at TEXT,
    candidate_path TEXT
);
CREATE INDEX IF NOT EXISTS idx_posts_modified ON posts(modified_at);
CREATE INDEX IF NOT EXISTS idx_sources_type_status ON sources(source_type, extraction_status);
CREATE INDEX IF NOT EXISTS idx_topic_links_review ON topic_links(status, score DESC);
CREATE VIRTUAL TABLE IF NOT EXISTS source_search USING fts5(
    source_id UNINDEXED, title, text, tokenize='unicode61 remove_diacritics 2'
);
"""


class PageParser(HTMLParser):
    """Extract readable post text and linked media without external parsers."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text_parts: list[str] = []
        self.links: list[tuple[str, str]] = []
        self._skip_depth = 0
        self._active_link: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
        if tag == "a":
            href = values.get("href")
            self._active_link = [href or "", ""]
        if tag in {"img", "source", "video", "audio"}:
            candidates = [
                values.get("data-orig-file"), values.get("data-large-file"),
                values.get("data-src"), values.get("src"),
            ]
            selected = next((value for value in candidates if value), None)
            if not selected:
                source_set = values.get("data-srcset") or values.get("srcset") or ""
                parsed = []
                for candidate in source_set.split(","):
                    pieces = candidate.strip().split()
                    if pieces:
                        size = 0
                        if len(pieces) > 1:
                            number = re.match(r"(\d+)(?:w|x)$", pieces[1])
                            if number:
                                size = int(number.group(1))
                        parsed.append((size, pieces[0]))
                if parsed:
                    selected = max(parsed)[1]
            if selected:
                self.links.append((selected, values.get("alt") or values.get("title") or ""))

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._active_link is not None:
            url, label = self._active_link
            if url:
                self.links.append((url, label.strip()))
            self._active_link = None
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        value = " ".join(data.split())
        if value:
            self.text_parts.append(value)
            if self._active_link is not None:
                self._active_link[1] += " " + value


def _request(url: str, *, max_bytes: int | None = None) -> tuple[bytes, Any]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=50) as response:
        length = response.headers.get("Content-Length")
        if max_bytes is not None and length and int(length) > max_bytes:
            raise ValueError(f"download exceeds {max_bytes} bytes")
        payload = response.read(max_bytes + 1 if max_bytes is not None else -1)
        if max_bytes is not None and len(payload) > max_bytes:
            raise ValueError(f"download exceeds {max_bytes} bytes")
        return payload, response.headers


def _request_json(url: str) -> tuple[Any, Any]:
    payload, headers = _request(url)
    return json.loads(payload.decode("utf-8")), headers


def discover_category_id(category_url: str) -> int:
    _, headers = _request(category_url)
    link_header = headers.get("Link", "")
    match = re.search(r"wp-json/wp/v2/categories/(\d+)", link_header)
    if match:
        return int(match.group(1))
    parsed = urlparse(category_url)
    slug = unquote(parsed.path.rstrip("/").split("/")[-1])
    rest = f"{parsed.scheme}://{parsed.netloc}/wordpress/wp-json/wp/v2/categories?slug={quote(slug)}"
    categories, _ = _request_json(rest)
    if len(categories) != 1:
        raise RuntimeError(f"could not resolve one WordPress category for {slug!r}")
    return int(categories[0]["id"])


def fetch_category_posts(category_url: str, category_id: int) -> tuple[list[dict[str, Any]], int]:
    parsed = urlparse(category_url)
    api_root = f"{parsed.scheme}://{parsed.netloc}/wordpress/wp-json/wp/v2/posts"
    first_url = f"{api_root}?categories={category_id}&per_page=100&page=1&_embed=1"
    first, headers = _request_json(first_url)
    total_pages = int(headers.get("X-WP-TotalPages", "1"))
    posts = list(first)
    for page in range(2, total_pages + 1):
        result, _ = _request_json(
            f"{api_root}?categories={category_id}&per_page=100&page={page}&_embed=1"
        )
        posts.extend(result)
        time.sleep(0.1)
    expected = int(headers.get("X-WP-Total", str(len(posts))))
    if len(posts) != expected:
        raise RuntimeError(f"WordPress pagination incomplete: fetched {len(posts)} of {expected}")
    return posts, expected


def fetch_media_metadata(category_url: str) -> dict[str, dict[str, Any]]:
    parsed = urlparse(category_url)
    api_root = f"{parsed.scheme}://{parsed.netloc}/wordpress/wp-json/wp/v2/media"
    url = f"{api_root}?per_page=100&page=1&_fields=id,date_gmt,modified_gmt,mime_type,source_url,title,media_details"
    first, headers = _request_json(url)
    pages = int(headers.get("X-WP-TotalPages", "1"))
    result = list(first)
    for page in range(2, pages + 1):
        items, _ = _request_json(
            f"{api_root}?per_page=100&page={page}&_fields=id,date_gmt,modified_gmt,mime_type,source_url,title,media_details"
        )
        result.extend(items)
        time.sleep(0.05)
    media_by_url: dict[str, dict[str, Any]] = {}
    for item in result:
        modified = item.get("modified_gmt") or item.get("date_gmt") or item.get("date")
        title = _plain_text(item.get("title", {}).get("rendered", ""))[0].strip()
        base = {
            "media_id": item["id"],
            "modified": modified,
            "mime_type": item.get("mime_type"),
            "title": title,
            "byte_size": item.get("media_details", {}).get("filesize"),
        }
        source_url = canonical_url(item.get("source_url", ""))
        if source_url:
            media_by_url[source_url] = base
        for size in item.get("media_details", {}).get("sizes", {}).values():
            sized_url = canonical_url(size.get("source_url", ""))
            if sized_url:
                media_by_url[sized_url] = base
    return media_by_url


def update_media_metadata(connection: sqlite3.Connection, media: dict[str, dict[str, Any]]) -> int:
    changed = 0
    for url, metadata in media.items():
        source = connection.execute(
            "SELECT source_id,source_type,version FROM sources WHERE source_url=?", (url,)
        ).fetchone()
        if not source:
            continue
        source_id, source_type, old_version = source
        new_version = metadata.get("modified")
        if old_version and new_version and old_version != new_version and source_type != "pdf":
            event = connection.execute(
                """INSERT INTO source_change_events(source_id,detected_at,old_sha256,new_sha256,
                     old_version,new_version,status)
                   VALUES(?,datetime('now'),NULL,NULL,?,?, 'pending_topic_review')""",
                (source_id, old_version, new_version),
            )
            event_id = int(event.lastrowid)
            if queue_proposals_for_approved_links(connection, source_id, event_id):
                connection.execute(
                    "UPDATE source_change_events SET status='pending_approval' WHERE event_id=?", (event_id,)
                )
            changed += 1
        connection.execute(
            """UPDATE sources SET media_id=?,mime_type=COALESCE(?,mime_type),
                 title=CASE WHEN title='' OR title=file_name THEN ? ELSE title END,
                 version=COALESCE(?,version),updated_at=COALESCE(?,updated_at),
                 byte_size=COALESCE(?,byte_size)
               WHERE source_id=?""",
            (metadata.get("media_id"), metadata.get("mime_type"), metadata.get("title"),
             new_version, new_version, metadata.get("byte_size"), source_id),
        )
    connection.commit()
    return changed


def canonical_url(url: str) -> str | None:
    raw = html.unescape(url.strip())
    parsed = urlparse(raw)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return None
    host = parsed.netloc.lower().split(":", 1)[0]
    query = "" if host == ALLOWED_HOST and "/wp-content/uploads/" in parsed.path else parsed.query
    path = quote(parsed.path, safe="/%:@!$&'()*+,;=-._~%")
    query = quote(query, safe="/%:@!$&'()*+,;=-._~%?&=")
    clean = parsed._replace(path=path, fragment="", query=query)
    return urlunparse(clean)


def classify_source(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower().split(":", 1)[0]
    path = unquote(parsed.path).lower()
    suffix = Path(path).suffix
    if "overleaf.com" in host:
        return "overleaf"
    if suffix in PDF_SUFFIXES:
        return "pdf"
    if suffix in IMAGE_SUFFIXES:
        return "image"
    if suffix in HTML_SUFFIXES:
        return "html"
    return "other"


def source_identifier(url: str) -> str:
    return "wpurl:" + hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]


def _plain_text(markup: str) -> tuple[str, list[tuple[str, str]]]:
    parser = PageParser()
    parser.feed(markup)
    parser.close()
    return "\n".join(parser.text_parts), parser.links


def _decode_term(term: dict[str, Any]) -> str:
    return re.sub(r"<[^>]+>", "", html.unescape(str(term.get("name") or ""))).strip()


def post_taxonomy(post: dict[str, Any]) -> tuple[list[str], list[str]]:
    tags: list[str] = []
    categories: list[str] = []
    embedded = post.get("_embedded", {}).get("wp:term", [])
    for group in embedded:
        for term in group:
            label = _decode_term(term)
            if not label:
                continue
            target = categories if term.get("taxonomy") == "category" else tags
            if label not in target:
                target.append(label)
    return sorted(tags), sorted(categories)


def _tokens(value: str) -> set[str]:
    normalized = value.casefold().replace("_", " ").replace("-", " ")
    return {
        token for token in re.findall(r"[a-z0-9]+|[가-힣]{2,}", normalized)
        if token not in STOP_WORDS and len(token) > 1
    }


def topic_catalog() -> list[dict[str, Any]]:
    topics: list[dict[str, Any]] = []
    for readme in sorted((ROOT / "rubrics" / "topic_packs").glob("*/README.md")):
        topic_id = readme.parent.name
        first_heading = next(
            (line.lstrip("# ").strip() for line in readme.read_text(encoding="utf-8").splitlines() if line.startswith("# ")),
            topic_id,
        )
        terms = _tokens(topic_id.replace("_", " ")) | _tokens(first_heading)
        topics.append({"topic_id": topic_id, "title": first_heading, "terms": terms})
    return topics


def match_topics(title: str, excerpt: str, tags: list[str], topics: list[dict[str, Any]]) -> list[tuple[str, float, list[str]]]:
    post_terms = _tokens(" ".join([title, excerpt, *tags]))
    ranked: list[tuple[str, float, list[str]]] = []
    for topic in topics:
        shared = sorted(post_terms & topic["terms"])
        if not shared:
            continue
        # A ranking signal only; this is deliberately not presented as a
        # calibrated probability of a correct human topic assignment.
        score = min(1.0, len(shared) / max(5.0, len(topic["terms"]) ** 0.5 * 2.0))
        if len(shared) >= 2 or any(len(term) >= 7 for term in shared):
            ranked.append((topic["topic_id"], round(score, 4), shared))
    return sorted(ranked, key=lambda item: (-item[1], item[0]))[:5]


def initialize_database(database: Path) -> sqlite3.Connection:
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database)
    connection.executescript(SCHEMA)
    connection.execute("PRAGMA journal_mode=WAL")
    columns = {row[1] for row in connection.execute("PRAGMA table_info(sources)")}
    if "media_id" not in columns:
        connection.execute("ALTER TABLE sources ADD COLUMN media_id INTEGER")
    topic_columns = {row[1] for row in connection.execute("PRAGMA table_info(topic_links)")}
    for column in ("reviewed_by", "reviewed_at"):
        if column not in topic_columns:
            connection.execute(f"ALTER TABLE topic_links ADD COLUMN {column} TEXT")
    proposal_columns = {row[1] for row in connection.execute("PRAGMA table_info(source_update_proposals)")}
    for column in ("approved_by", "approved_at"):
        if column not in proposal_columns:
            connection.execute(f"ALTER TABLE source_update_proposals ADD COLUMN {column} TEXT")
    content_proposal_columns = {row[1] for row in connection.execute("PRAGMA table_info(content_update_proposals)")}
    content_proposal_sql = connection.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='content_update_proposals'"
    ).fetchone()[0]
    if "'applied'" not in content_proposal_sql:
        connection.execute(
            """CREATE TABLE content_update_proposals_new (
                proposal_id TEXT PRIMARY KEY,
                topic_id TEXT NOT NULL,
                base_revision INTEGER NOT NULL,
                proposal_json TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('pending_approval','approved','rejected','candidate_ready','applied')),
                created_at TEXT NOT NULL,
                resolved_by TEXT,
                resolved_at TEXT,
                candidate_path TEXT
            )"""
        )
        candidate_column = "candidate_path" if "candidate_path" in content_proposal_columns else "NULL"
        connection.execute(
            f"""INSERT INTO content_update_proposals_new
                (proposal_id,topic_id,base_revision,proposal_json,status,created_at,resolved_by,resolved_at,candidate_path)
                SELECT proposal_id,topic_id,base_revision,proposal_json,status,created_at,resolved_by,resolved_at,{candidate_column}
                FROM content_update_proposals"""
        )
        connection.execute("DROP TABLE content_update_proposals")
        connection.execute("ALTER TABLE content_update_proposals_new RENAME TO content_update_proposals")
    elif "candidate_path" not in content_proposal_columns:
        connection.execute("ALTER TABLE content_update_proposals ADD COLUMN candidate_path TEXT")
    connection.execute("PRAGMA user_version=2")
    return connection


def _iso_timestamp(value: str | None) -> str | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = parsedate_to_datetime(value)
        except (TypeError, ValueError, OverflowError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.isoformat()


def _source_reference(row: tuple[Any, ...]) -> dict[str, Any]:
    source_id, source_type, source_url, title, version, updated_at, wordpress_url = row
    return {
        "source_id": source_id,
        "source_type": source_type,
        "wordpress_url": wordpress_url or source_url,
        "source_url": source_url,
        "title": title or source_url,
        "version": version or "unversioned",
        "page": None,
        "section": None,
        "updated_at": _iso_timestamp(updated_at),
        "verification_status": "unverified",
    }


def queue_source_proposal(
    connection: sqlite3.Connection,
    source_id: str,
    topic_id: str,
    *,
    event_id: int | None = None,
) -> str:
    row = connection.execute(
        """SELECT s.source_id,s.source_type,s.source_url,s.title,s.version,s.updated_at,p.url
           FROM sources s LEFT JOIN post_sources ps ON ps.source_id=s.source_id
           LEFT JOIN posts p ON p.post_id=ps.post_id
           WHERE s.source_id=? ORDER BY p.post_id LIMIT 1""",
        (source_id,),
    ).fetchone()
    if not row:
        raise ValueError(f"source does not exist: {source_id}")
    reference = _source_reference(row)
    master_path = ROOT / "master_topic_packs" / f"{topic_id}.json"
    proposal_id = "catalog-" + hashlib.sha256(
        f"{source_id}:{topic_id}:{event_id or 0}".encode("utf-8")
    ).hexdigest()[:24]
    if not master_path.is_file():
        proposal = {
            "proposal_id": proposal_id,
            "topic_id": topic_id,
            "source_id": source_id,
            "source_reference": reference,
            "status": "waiting_for_master",
            "approval_required": True,
        }
        connection.execute(
            """INSERT OR IGNORE INTO source_update_proposals
               (proposal_id,event_id,topic_id,source_id,base_revision,proposal_json,status,created_at)
               VALUES(?,?,?,?,0,?,'waiting_for_master',datetime('now'))""",
            (proposal_id, event_id, topic_id, source_id, json.dumps(proposal, ensure_ascii=False)),
        )
        return proposal_id
    master = json.loads(master_path.read_text(encoding="utf-8"))
    validate_master_topic_pack(master)
    existing = next((item for item in master["sources"] if item["source_id"] == source_id), None)
    if existing == reference:
        connection.execute(
            "UPDATE source_update_proposals SET status='applied' WHERE proposal_id=? AND status='waiting_for_master'",
            (proposal_id,),
        )
        return "already_current"
    proposal = propose_source_update(master, reference, proposed_at=datetime.now(timezone.utc).isoformat())
    proposal["proposal_id"] = proposal_id
    connection.execute(
        """INSERT INTO source_update_proposals
           (proposal_id,event_id,topic_id,source_id,base_revision,proposal_json,status,created_at)
           VALUES(?,?,?,?,?,?,?,datetime('now'))
           ON CONFLICT(proposal_id) DO UPDATE SET event_id=excluded.event_id,
             base_revision=excluded.base_revision,proposal_json=excluded.proposal_json,status=excluded.status""",
        (proposal_id, event_id, topic_id, source_id, master["revision"],
         json.dumps(proposal, ensure_ascii=False), "pending_approval"),
    )
    return proposal_id


def queue_proposals_for_approved_links(
    connection: sqlite3.Connection, source_id: str, event_id: int | None = None
) -> int:
    topics = connection.execute(
        """SELECT DISTINCT t.topic_id FROM post_sources ps
           JOIN topic_links t ON t.post_id=ps.post_id
           WHERE ps.source_id=? AND t.status='approved' ORDER BY t.topic_id""",
        (source_id,),
    ).fetchall()
    for (topic_id,) in topics:
        queue_source_proposal(connection, source_id, topic_id, event_id=event_id)
    if event_id is not None and topics:
        refresh_change_event_status(connection, event_id)
    return len(topics)


def refresh_change_event_status(connection: sqlite3.Connection, event_id: int) -> None:
    statuses = {
        row[0] for row in connection.execute(
            "SELECT status FROM source_update_proposals WHERE event_id=?", (event_id,)
        )
    }
    if "pending_approval" in statuses or "waiting_for_master" in statuses:
        status = "pending_approval"
    elif "waiting_for_master" in statuses:
        status = "waiting_for_master"
    elif statuses and statuses <= {"applied"}:
        status = "applied"
    else:
        status = "pending_topic_review"
    connection.execute("UPDATE source_change_events SET status=? WHERE event_id=?", (status, event_id))


def materialize_waiting_proposals(connection: sqlite3.Connection) -> int:
    rows = connection.execute(
        "SELECT proposal_id,source_id,topic_id,event_id FROM source_update_proposals WHERE status='waiting_for_master'"
    ).fetchall()
    updated = 0
    for old_id, source_id, topic_id, event_id in rows:
        master_path = ROOT / "master_topic_packs" / f"{topic_id}.json"
        if not master_path.is_file():
            continue
        current = queue_source_proposal(connection, source_id, topic_id, event_id=event_id)
        if current != "already_current":
            updated += 1
        if event_id is not None:
            refresh_change_event_status(connection, event_id)
    return updated


def review_topic_link(database: Path, post_id: int, topic_id: str, decision: str) -> int:
    if decision not in {"approve", "reject"}:
        raise ValueError("decision must be approve or reject")
    connection = initialize_database(database)
    status = "approved" if decision == "approve" else "rejected"
    reviewer = os.environ.get("USER") or "local-user"
    reviewed_at = datetime.now(timezone.utc).isoformat()
    cursor = connection.execute(
        "UPDATE topic_links SET status=?,reviewed_by=?,reviewed_at=? WHERE post_id=? AND topic_id=? AND status='pending_review'",
        (status, reviewer, reviewed_at, post_id, topic_id),
    )
    if cursor.rowcount == 0 and decision == "approve":
        if topic_id not in {topic["topic_id"] for topic in topic_catalog()}:
            connection.close()
            raise ValueError(f"unknown Topic ID: {topic_id}")
        post_exists = connection.execute("SELECT 1 FROM posts WHERE post_id=?", (post_id,)).fetchone()
        if not post_exists:
            connection.close()
            raise ValueError(f"post not found: {post_id}")
        connection.execute(
            """INSERT INTO topic_links(post_id,topic_id,status,score,matched_terms_json,evidence,reviewed_by,reviewed_at)
               VALUES(?,?,'approved',1.0,'[]','manual human topic mapping',?,?)""",
            (post_id, topic_id, reviewer, reviewed_at),
        )
    elif cursor.rowcount != 1:
        connection.close()
        raise ValueError("no pending topic-link candidate matched the post/topic pair")
    queued = 0
    if decision == "approve":
        sources = connection.execute(
            "SELECT source_id FROM post_sources WHERE post_id=? ORDER BY position", (post_id,)
        ).fetchall()
        for (source_id,) in sources:
            queue_source_proposal(connection, source_id, topic_id)
            queued += 1
    materialize_waiting_proposals(connection)
    connection.commit()
    connection.close()
    return queued


def approve_master_proposal(database: Path, proposal_id: str, approved_by: str) -> None:
    connection = initialize_database(database)
    row = connection.execute(
        "SELECT topic_id,proposal_json,status FROM source_update_proposals WHERE proposal_id=?",
        (proposal_id,),
    ).fetchone()
    if not row:
        connection.close()
        raise ValueError(f"proposal not found: {proposal_id}")
    topic_id, proposal_json, status = row
    if status != "pending_approval":
        connection.close()
        raise ValueError(f"proposal is not ready for approval: {status}")
    master_path = ROOT / "master_topic_packs" / f"{topic_id}.json"
    master = json.loads(master_path.read_text(encoding="utf-8"))
    updated = apply_approved_source_update(master, json.loads(proposal_json), approved_by=approved_by)
    temporary = master_path.with_suffix(master_path.suffix + ".tmp")
    temporary.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(master_path)
    connection.execute(
        "UPDATE source_update_proposals SET status='applied',approved_by=?,approved_at=? WHERE proposal_id=?",
        (approved_by, datetime.now(timezone.utc).isoformat(), proposal_id),
    )
    event_id = connection.execute(
        "SELECT event_id FROM source_update_proposals WHERE proposal_id=?", (proposal_id,)
    ).fetchone()[0]
    if event_id is not None:
        refresh_change_event_status(connection, event_id)
    # Applying one reference advances the Master revision. Rebase the remaining
    # still-pending references to the new revision; each still needs approval.
    remaining = connection.execute(
        """SELECT source_id,event_id FROM source_update_proposals
           WHERE topic_id=? AND status='pending_approval' AND base_revision<>?""",
        (topic_id, updated["revision"]),
    ).fetchall()
    for source_id, pending_event_id in remaining:
        queue_source_proposal(connection, source_id, topic_id, event_id=pending_event_id)
    connection.commit()
    connection.close()


def save_content_update_proposal(database: Path, proposal: dict[str, Any]) -> None:
    """Persist a validated content proposal without changing Topic files."""
    validate_content_update_proposal(proposal)
    if proposal["status"] != "pending_approval":
        raise ValueError("only pending content proposals may be submitted")
    master_path = ROOT / "master_topic_packs" / f"{proposal['topic_id']}.json"
    if not master_path.is_file():
        raise ValueError(f"Master Topic Pack does not exist: {proposal['topic_id']}")
    master = json.loads(master_path.read_text(encoding="utf-8"))
    validate_master_topic_pack(master)
    if master["revision"] != proposal["base_revision"]:
        raise ValueError("content proposal base revision does not match the current Master")
    validate_content_update_against_master(master, proposal)
    connection = initialize_database(database)
    try:
        connection.execute(
            """INSERT INTO content_update_proposals
               (proposal_id,topic_id,base_revision,proposal_json,status,created_at)
               VALUES(?,?,?,?,?,?)""",
            (
                proposal["proposal_id"], proposal["topic_id"], proposal["base_revision"],
                json.dumps(proposal, ensure_ascii=False, sort_keys=True), proposal["status"],
                proposal["proposed_at"],
            ),
        )
        connection.commit()
    finally:
        connection.close()


def resolve_content_update_proposal(
    database: Path,
    proposal_id: str,
    *,
    decision: str,
    reviewed_by: str,
) -> dict[str, Any]:
    """Approve/reject one proposal record; approval does not apply content."""
    if decision not in {"approve", "reject"}:
        raise ValueError("decision must be approve or reject")
    if not isinstance(reviewed_by, str) or not reviewed_by.strip():
        raise ValueError("an explicit reviewer identity is required")
    connection = initialize_database(database)
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT proposal_json,status FROM content_update_proposals WHERE proposal_id=?",
            (proposal_id,),
        ).fetchone()
        if not row:
            raise ValueError(f"content proposal not found: {proposal_id}")
        proposal_json, status = row
        if status != "pending_approval":
            raise ValueError(f"content proposal is not pending approval: {status}")
        proposal = json.loads(proposal_json)
        now = datetime.now(timezone.utc).isoformat()
        if decision == "approve":
            master_path = ROOT / "master_topic_packs" / f"{proposal['topic_id']}.json"
            if not master_path.is_file():
                raise ValueError("Master Topic Pack disappeared before proposal review")
            master = json.loads(master_path.read_text(encoding="utf-8"))
            validate_master_topic_pack(master)
            if master["revision"] != proposal["base_revision"]:
                raise ValueError("content proposal became stale before approval")
            resolved = approve_content_update(
                master, proposal, approved_by=reviewed_by, approved_at=now
            )
        else:
            resolved = reject_content_update(proposal, rejected_by=reviewed_by, rejected_at=now)
        connection.execute(
            """UPDATE content_update_proposals SET proposal_json=?,status=?,resolved_by=?,resolved_at=?
               WHERE proposal_id=? AND status='pending_approval'""",
            (
                json.dumps(resolved, ensure_ascii=False, sort_keys=True), resolved["status"],
                reviewed_by.strip(), now, proposal_id,
            ),
        )
        connection.commit()
        return resolved
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def list_content_update_proposals(database: Path, limit: int = 50) -> list[dict[str, Any]]:
    connection = initialize_database(database)
    try:
        rows = connection.execute(
            """SELECT proposal_json FROM content_update_proposals
               ORDER BY created_at,proposal_id LIMIT ?""",
            (limit,),
        ).fetchall()
        return [json.loads(row[0]) for row in rows]
    finally:
        connection.close()


def prepare_content_update_candidate(
    database: Path,
    proposal_id: str,
    *,
    candidate_root: Path | None = None,
) -> Path:
    """Write an isolated review bundle; never modifies canonical Topic files."""
    if not re.fullmatch(r"[A-Za-z0-9._-]+", proposal_id):
        raise ValueError("proposal_id contains unsafe path characters")
    repo_root = ROOT.resolve()
    output_root = (candidate_root or (repo_root / "data" / "content_update_candidates")).resolve()
    if output_root == repo_root or not output_root.is_relative_to(repo_root):
        raise ValueError("candidate_root must be a child of the repository")
    output_root.mkdir(parents=True, exist_ok=True)
    candidate_path = output_root / proposal_id
    if candidate_path.exists():
        raise ValueError(f"candidate bundle already exists: {candidate_path}")

    connection = initialize_database(database)
    temporary_path: Path | None = None
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT topic_id,proposal_json,status FROM content_update_proposals WHERE proposal_id=?",
            (proposal_id,),
        ).fetchone()
        if not row:
            raise ValueError(f"content proposal not found: {proposal_id}")
        topic_id, proposal_json, status = row
        if status != "approved":
            raise ValueError(f"content proposal must be approved first: {status}")
        proposal = json.loads(proposal_json)
        if proposal.get("topic_id") != topic_id:
            raise ValueError("stored proposal topic_id does not match its catalog row")
        master_path = repo_root / "master_topic_packs" / f"{topic_id}.json"
        master = json.loads(master_path.read_text(encoding="utf-8"))
        validate_master_topic_pack(master)
        source_payloads = load_legacy_topic_sources(repo_root, master)
        candidate = apply_approved_content_update(
            master,
            source_payloads,
            proposal,
            candidate_ready_at=datetime.now(timezone.utc).isoformat(),
        )

        temporary_path = Path(tempfile.mkdtemp(prefix=".content-candidate-", dir=output_root))
        artifact_hashes: dict[str, str] = {}

        def write_artifact(relative_path: str, value: dict[str, Any]) -> None:
            target_path = temporary_path / relative_path
            resolved_target = target_path.resolve()
            if not resolved_target.is_relative_to(temporary_path.resolve()):
                raise ValueError("candidate artifact path escapes bundle")
            target_path.parent.mkdir(parents=True, exist_ok=True)
            content = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
            target_path.write_bytes(content)
            artifact_hashes[relative_path] = hashlib.sha256(content).hexdigest()

        write_artifact(f"master_topic_packs/{topic_id}.json", candidate["master"])
        for source_key, relative_path in candidate["master"]["legacy_topic_pack"]["source_files"].items():
            write_artifact(relative_path, candidate["source_payloads"][source_key])
        write_artifact(f"proposals/{proposal_id}.json", candidate["proposal"])
        manifest = {
            "bundle_version": "content-update-candidate-v1",
            "proposal_id": proposal_id,
            "topic_id": topic_id,
            "base_revision": master["revision"],
            "candidate_revision": candidate["master"]["revision"],
            "affected_views": candidate["proposal"]["affected_views"],
            "application_status": "candidate_only_not_applied",
            "files_sha256": artifact_hashes,
        }
        manifest_path = temporary_path / "manifest.json"
        manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
        manifest_path.write_bytes(manifest_bytes)
        os.replace(temporary_path, candidate_path)
        temporary_path = None

        connection.execute(
            """UPDATE content_update_proposals
               SET proposal_json=?,status='candidate_ready',candidate_path=?
               WHERE proposal_id=? AND status='approved'""",
            (
                json.dumps(candidate["proposal"], ensure_ascii=False, sort_keys=True),
                str(candidate_path.relative_to(repo_root)),
                proposal_id,
            ),
        )
        connection.commit()
        return candidate_path
    except Exception:
        connection.rollback()
        raise
    finally:
        if temporary_path is not None:
            shutil.rmtree(temporary_path, ignore_errors=True)
        connection.close()


def _write_bytes_atomically(path: Path, content: bytes, mode: int) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.content-update-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except Exception:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def apply_content_update_candidate(
    database: Path,
    proposal_id: str,
    *,
    applied_by: str,
) -> dict[str, Any]:
    """Apply one reviewed candidate after full provenance and revision checks."""
    if not isinstance(applied_by, str) or not applied_by.strip():
        raise ValueError("an explicit apply identity is required")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", proposal_id):
        raise ValueError("proposal_id contains unsafe path characters")
    repo_root = ROOT.resolve()
    connection = initialize_database(database)
    replaced: list[tuple[Path, bytes, int]] = []
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            """SELECT topic_id,proposal_json,status,candidate_path
               FROM content_update_proposals WHERE proposal_id=?""",
            (proposal_id,),
        ).fetchone()
        if not row:
            raise ValueError(f"content proposal not found: {proposal_id}")
        topic_id, proposal_json, status, relative_candidate_path = row
        if status != "candidate_ready" or not relative_candidate_path:
            raise ValueError("content proposal must have a reviewed candidate bundle")
        proposal = json.loads(proposal_json)
        if proposal.get("topic_id") != topic_id or proposal.get("proposal_id") != proposal_id:
            raise ValueError("stored candidate identity does not match its catalog row")
        candidate_unresolved = repo_root / relative_candidate_path
        if candidate_unresolved.is_symlink():
            raise ValueError("candidate bundle must not be a symlink")
        candidate_path = candidate_unresolved.resolve()
        if not candidate_path.is_relative_to(repo_root) or candidate_path.name != proposal_id:
            raise ValueError("candidate bundle path is outside the repository or has an invalid name")
        manifest_path = candidate_path / "manifest.json"
        if manifest_path.is_symlink():
            raise ValueError("candidate manifest must not be a symlink")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if (
            manifest.get("bundle_version") != "content-update-candidate-v1"
            or manifest.get("proposal_id") != proposal_id
            or manifest.get("application_status") != "candidate_only_not_applied"
        ):
            raise ValueError("candidate manifest identity/status is invalid")

        master_unresolved = repo_root / "master_topic_packs" / f"{topic_id}.json"
        if master_unresolved.is_symlink():
            raise ValueError("canonical Master path must not be a symlink")
        master_path = master_unresolved.resolve()
        if not master_path.is_relative_to(repo_root):
            raise ValueError("canonical Master path escapes the repository")
        master_bytes = master_path.read_bytes()
        master = json.loads(master_bytes)
        validate_master_topic_pack(master)
        source_payloads = load_legacy_topic_sources(repo_root, master)
        if manifest.get("base_revision") != master["revision"]:
            raise ValueError("candidate is stale against the current Master revision")
        if manifest.get("affected_views") != proposal.get("affected_views"):
            raise ValueError("candidate manifest affected_views do not match the proposal")

        approved_proposal = copy.deepcopy(proposal)
        approved_proposal["status"] = "approved"
        approved_proposal.pop("candidate_ready_at", None)
        approved_proposal.pop("candidate_revision", None)
        expected = apply_approved_content_update(
            master,
            source_payloads,
            approved_proposal,
            candidate_ready_at=proposal["candidate_ready_at"],
        )
        if expected["master"]["revision"] != manifest.get("candidate_revision"):
            raise ValueError("candidate revision does not match regenerated result")
        if expected["proposal"] != proposal:
            raise ValueError("stored proposal differs from regenerated candidate")

        expected_files = {
            f"master_topic_packs/{topic_id}.json": expected["master"],
            f"proposals/{proposal_id}.json": expected["proposal"],
        }
        for source_key, relative_path in expected["master"]["legacy_topic_pack"]["source_files"].items():
            expected_files[relative_path] = expected["source_payloads"][source_key]
        listed_files = manifest.get("files_sha256")
        if not isinstance(listed_files, dict) or set(listed_files) != set(expected_files):
            raise ValueError("candidate manifest file inventory is incomplete or unexpected")
        for relative_path, expected_payload in expected_files.items():
            bundle_file_unresolved = candidate_path / relative_path
            if bundle_file_unresolved.is_symlink():
                raise ValueError(f"candidate artifact must not be a symlink: {relative_path}")
            bundle_file = bundle_file_unresolved.resolve()
            if not bundle_file.is_relative_to(candidate_path):
                raise ValueError("candidate file path escapes its bundle")
            content = bundle_file.read_bytes()
            if hashlib.sha256(content).hexdigest() != listed_files[relative_path]:
                raise ValueError(f"candidate artifact hash mismatch: {relative_path}")
            if json.loads(content) != expected_payload:
                raise ValueError(f"candidate artifact differs from regenerated result: {relative_path}")

        target_key = proposal["target"]["source_key"]
        source_unresolved = repo_root / master["legacy_topic_pack"]["source_files"][target_key]
        if source_unresolved.is_symlink():
            raise ValueError("canonical Topic source path must not be a symlink")
        source_path = source_unresolved.resolve()
        if not source_path.is_relative_to(repo_root):
            raise ValueError("canonical Topic/Master paths must be regular repository files")
        original_source_bytes = source_path.read_bytes()
        original_source = json.loads(original_source_bytes)
        if original_source != source_payloads[target_key]:
            raise ValueError("canonical Topic source changed during candidate validation")
        writes = [
            (source_path, (json.dumps(expected["source_payloads"][target_key], ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")),
            (master_path, (json.dumps(expected["master"], ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")),
        ]
        originals = {
            source_path: (original_source_bytes, stat.S_IMODE(source_path.stat().st_mode)),
            master_path: (master_bytes, stat.S_IMODE(master_path.stat().st_mode)),
        }
        # Recheck both originals immediately before the first replacement.
        if any(path.read_bytes() != originals[path][0] for path, _ in writes):
            raise ValueError("canonical Topic/Master changed during apply preflight")
        for path, content in writes:
            _write_bytes_atomically(path, content, originals[path][1])
            replaced.append((path, originals[path][0], originals[path][1]))

        applied = mark_content_update_applied(
            proposal,
            applied_by=applied_by,
            applied_at=datetime.now(timezone.utc).isoformat(),
        )
        cursor = connection.execute(
            """UPDATE content_update_proposals
               SET proposal_json=?,status='applied',resolved_by=?,resolved_at=?
               WHERE proposal_id=? AND status='candidate_ready'""",
            (
                json.dumps(applied, ensure_ascii=False, sort_keys=True),
                applied_by.strip(), applied["applied_at"], proposal_id,
            ),
        )
        if cursor.rowcount != 1:
            raise ValueError("candidate status changed during apply")
        connection.commit()
        return {"proposal": applied, "master": expected["master"], "applied_files": [str(path) for path, _ in writes]}
    except Exception:
        connection.rollback()
        rollback_errors = []
        for path, content, mode in reversed(replaced):
            try:
                _write_bytes_atomically(path, content, mode)
            except Exception as exc:
                rollback_errors.append(f"{path}: {exc}")
        if rollback_errors:
            raise RuntimeError("content update failed and rollback was incomplete: " + "; ".join(rollback_errors))
        raise
    finally:
        connection.close()


def show_content_update_proposals(database: Path, limit: int = 50) -> None:
    proposals = list_content_update_proposals(database, limit)
    print("CONTENT_UPDATE_PROPOSALS")
    for proposal in proposals:
        target = proposal["target"]
        print(
            f"{proposal['proposal_id']}\t{proposal['status']}\t{proposal['topic_id']}\t"
            f"{target['source_key']}:{target['record_id']}.{'.'.join(target['field_path'])}\t"
            f"views={','.join(proposal['affected_views'])}"
        )
    print(f"CONTENT_UPDATE_PROPOSALS_TOTAL={len(proposals)}")


def list_pending(database: Path, limit: int = 50) -> None:
    connection = initialize_database(database)
    rows = connection.execute(
        """SELECT t.post_id,p.title,p.url,t.topic_id,t.score,t.matched_terms_json
           FROM topic_links t JOIN posts p USING(post_id)
           WHERE t.status='pending_review' ORDER BY t.score DESC,p.post_id LIMIT ?""",
        (limit,),
    ).fetchall()
    proposals = connection.execute(
        """SELECT proposal_id,topic_id,source_id,status FROM source_update_proposals
           WHERE status!='applied' ORDER BY created_at LIMIT ?""",
        (limit,),
    ).fetchall()
    unmatched = connection.execute(
        """SELECT p.post_id,p.title,p.url FROM posts p
           WHERE NOT EXISTS(SELECT 1 FROM topic_links t WHERE t.post_id=p.post_id)
           ORDER BY p.post_id LIMIT ?""",
        (limit,),
    ).fetchall()
    connection.close()
    print("PENDING_TOPIC_LINKS")
    for post_id, title, url, topic_id, score, terms in rows:
        print(json.dumps({"post_id": post_id, "title": title, "url": url,
                          "topic_id": topic_id, "lexical_score": score,
                          "matched_terms": json.loads(terms)}, ensure_ascii=False))
    print("PENDING_MASTER_PROPOSALS")
    for proposal in proposals:
        print(json.dumps(dict(zip(("proposal_id", "topic_id", "source_id", "status"), proposal)), ensure_ascii=False))
    print("UNMATCHED_POSTS")
    for post_id, title, url in unmatched:
        print(json.dumps({"post_id": post_id, "title": title, "url": url}, ensure_ascii=False))


def _store_post(
    connection: sqlite3.Connection,
    post: dict[str, Any],
    category_id: int,
    run_id: int,
    topics: list[dict[str, Any]],
) -> tuple[int, list[tuple[str, str, int]]]:
    post_id = int(post["id"])
    title = _plain_text(post["title"]["rendered"])[0].strip()
    excerpt = _plain_text(post.get("excerpt", {}).get("rendered", ""))[0].strip()
    content_html = str(post.get("content", {}).get("rendered", ""))
    content_text, raw_links = _plain_text(content_html)
    known_urls = {canonical_url(url) for url, _label in raw_links}
    for match in re.findall(r"https?://[^\s<>\"'\]\)]+", content_text):
        url = canonical_url(match.rstrip(".,;:!?"))
        if url and url not in known_urls and classify_source(url) != "other":
            raw_links.append((url, "URL in post text"))
            known_urls.add(url)
    featured = post.get("_embedded", {}).get("wp:featuredmedia", [])
    if featured:
        featured_url = featured[0].get("source_url")
        if featured_url:
            raw_links.insert(0, (featured_url, featured[0].get("alt_text") or "Featured image"))
    tags, categories = post_taxonomy(post)
    digest = hashlib.sha256(content_html.encode("utf-8")).hexdigest()
    previous = connection.execute(
        "SELECT content_sha256 FROM posts WHERE post_id=?", (post_id,)
    ).fetchone()
    change_event_id: int | None = None
    connection.execute(
        """INSERT INTO posts(post_id,category_id,slug,url,title,excerpt,content_html,content_text,
             published_at,modified_at,featured_media_id,tags_json,categories_json,content_sha256,last_seen_run)
           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
           ON CONFLICT(post_id) DO UPDATE SET category_id=excluded.category_id,slug=excluded.slug,
             url=excluded.url,title=excluded.title,excerpt=excluded.excerpt,content_html=excluded.content_html,
             content_text=excluded.content_text,published_at=excluded.published_at,modified_at=excluded.modified_at,
             featured_media_id=excluded.featured_media_id,tags_json=excluded.tags_json,
             categories_json=excluded.categories_json,content_sha256=excluded.content_sha256,
             last_seen_run=excluded.last_seen_run""",
        (
            post_id, category_id, post.get("slug", ""), post["link"], title, excerpt,
            content_html, content_text, post.get("date_gmt") or post.get("date"),
            post.get("modified_gmt") or post.get("modified"), post.get("featured_media") or None,
            json.dumps(tags, ensure_ascii=False), json.dumps(categories, ensure_ascii=False), digest, run_id,
        ),
    )
    connection.execute("DELETE FROM post_sources WHERE post_id=?", (post_id,))
    connection.execute("DELETE FROM topic_links WHERE post_id=? AND status='pending_review'", (post_id,))
    connection.execute("DELETE FROM source_search WHERE source_id=?", (f"wp-post:{post_id}",))
    connection.execute(
        """INSERT INTO sources(source_id,source_type,source_url,title,mime_type,file_name,first_party,
             version,updated_at,content_sha256,fetch_status,extraction_status,extraction_method,
             extracted_text,indexed_at)
           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))
           ON CONFLICT(source_url) DO UPDATE SET title=excluded.title,version=excluded.version,
             updated_at=excluded.updated_at,content_sha256=excluded.content_sha256,fetch_status='available',
             extraction_status='extracted',extraction_method='wordpress_rest_html',extracted_text=excluded.extracted_text,
             indexed_at=datetime('now')""",
        (f"wp-post:{post_id}", "wordpress_post", post["link"], title or post.get("slug", "post"),
         "text/html", None, 1, digest, post.get("modified_gmt") or post.get("modified"), digest,
         "available", "extracted", "wordpress_rest_html", content_text),
    )
    if previous and previous[0] != digest:
        change = connection.execute(
            """INSERT INTO source_change_events(source_id,detected_at,old_sha256,new_sha256,
                 old_version,new_version,status) VALUES(?,datetime('now'),?,?,?,?,'pending_topic_review')""",
            (f"wp-post:{post_id}", previous[0], digest, None, post.get("modified_gmt") or post.get("modified")),
        )
        change_event_id = int(change.lastrowid)
    connection.execute(
        "INSERT INTO post_sources(post_id,source_id,link_text,position) VALUES(?,?,?,0)",
        (post_id, f"wp-post:{post_id}", title),
    )
    connection.execute(
        "INSERT INTO source_search(source_id,title,text) VALUES(?,?,?)",
        (f"wp-post:{post_id}", title, content_text),
    )
    for index, (raw_url, link_text) in enumerate(raw_links, start=1):
        url = canonical_url(raw_url)
        if not url:
            continue
        source_type = classify_source(url)
        if source_type == "other":
            continue
        source_id = source_identifier(url)
        parsed = urlparse(url)
        host = parsed.netloc.lower().split(":", 1)[0]
        first_party = host == ALLOWED_HOST or host.endswith("." + ALLOWED_HOST)
        file_name = unquote(Path(parsed.path).name) or title
        connection.execute(
            """INSERT INTO sources(source_id,source_type,source_url,title,file_name,first_party,
                 fetch_status,extraction_status)
               VALUES(?,?,?,?,?,?,?,?)
               ON CONFLICT(source_url) DO UPDATE SET title=CASE WHEN sources.title='' THEN excluded.title ELSE sources.title END""",
            (source_id, source_type, url, link_text or file_name, file_name, int(first_party),
             "metadata_only", "pending" if source_type == "pdf" and first_party else "metadata_only"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO post_sources(post_id,source_id,link_text,position) VALUES(?,?,?,?)",
            (post_id, source_id, link_text or None, index),
        )
    for topic_id, score, matched_terms in match_topics(title, excerpt, tags, topics):
        connection.execute(
            """INSERT INTO topic_links(post_id,topic_id,status,score,matched_terms_json,evidence)
               VALUES(?,?,'pending_review',?,?,?)
               ON CONFLICT(post_id,topic_id) DO UPDATE SET score=excluded.score,
                 matched_terms_json=excluded.matched_terms_json,evidence=excluded.evidence
               WHERE topic_links.status='pending_review'""",
            (post_id, topic_id, score, json.dumps(matched_terms, ensure_ascii=False),
             "title/excerpt/tag token overlap; human review required"),
        )
    if change_event_id is not None:
        source_ids = connection.execute(
            "SELECT source_id FROM post_sources WHERE post_id=?", (post_id,)
        ).fetchall()
        queued = 0
        for (linked_source_id,) in source_ids:
            queued += queue_proposals_for_approved_links(
                connection, linked_source_id, change_event_id
            )
        if queued:
            refresh_change_event_status(connection, change_event_id)
    return post_id, [(url, label, index) for index, (url, label) in enumerate(raw_links, start=1) if canonical_url(url)]


def _run(command: list[str], *, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)


def pdf_text(
    pdf_path: Path,
    *,
    tesseract: str,
    tessdata: Path | None,
    language: str,
    ocr_workers: int,
    ocr_dpi: int,
) -> tuple[str, int, str]:
    info = _run(["pdfinfo", str(pdf_path)])
    if info.returncode:
        raise RuntimeError((info.stderr or "pdfinfo failed").strip()[:500])
    pages_match = re.search(r"^Pages:\s+(\d+)", info.stdout, re.MULTILINE)
    if not pages_match:
        raise RuntimeError("pdf page count is missing")
    pages = int(pages_match.group(1))
    text_parts: list[str] = []
    methods: set[str] = set()
    digital = _run(["pdftotext", "-layout", str(pdf_path), "-"], timeout=300)
    digital_pages = digital.stdout.split("\f") if digital.returncode == 0 else []
    env = os.environ.copy()
    env["OMP_THREAD_LIMIT"] = "1"
    if tessdata:
        env["TESSDATA_PREFIX"] = str(tessdata)
    ocr_results: dict[int, str] = {}
    ocr_pages = [
        page for page in range(1, pages + 1)
        if page > len(digital_pages) or len(re.sub(r"\s+", "", digital_pages[page - 1])) < 40
    ]

    def recognize_page(page: int) -> tuple[int, str]:
        with tempfile.TemporaryDirectory(prefix="wp_pdf_page_") as temp_dir:
            prefix = str(Path(temp_dir) / "page")
            render = _run([
                "pdftoppm", "-f", str(page), "-l", str(page), "-r", str(ocr_dpi),
                "-png", "-singlefile", str(pdf_path), prefix,
            ], timeout=180)
            image_path = Path(prefix + ".png")
            if render.returncode or not image_path.exists():
                raise RuntimeError((render.stderr or "PDF page rendering failed").strip()[:500])
            command = [tesseract, str(image_path), "stdout", "-l", language, "--psm", "3"]
            if tessdata:
                command.extend(["--tessdata-dir", str(tessdata)])
            result = subprocess.run(command, text=True, capture_output=True, timeout=180, env=env, check=False)
            if result.returncode:
                raise RuntimeError((result.stderr or "Tesseract OCR failed").strip()[:500])
            return page, result.stdout.strip()

    if ocr_pages:
        with ThreadPoolExecutor(max_workers=max(1, ocr_workers)) as executor:
            pending = [executor.submit(recognize_page, page) for page in ocr_pages]
            for future in as_completed(pending):
                page, result = future.result()
                ocr_results[page] = result
    for page in range(1, pages + 1):
        page_text = digital_pages[page - 1].strip() if page <= len(digital_pages) else ""
        useful = len(re.sub(r"\s+", "", page_text)) >= 40
        if useful:
            methods.add("pdftotext")
        else:
            page_text = ocr_results.get(page, "")
            if page_text:
                methods.add("tesseract_ocr")
        text_parts.append(f"[Page {page}]\n{page_text}" if page_text else f"[Page {page}]\n")
    return "\n\n".join(text_parts), pages, "+".join(sorted(methods)) or "empty"


def index_first_party_pdfs(
    connection: sqlite3.Connection,
    run_id: int,
    *,
    tesseract: str,
    tessdata: Path | None,
    language: str,
    delay: float,
    limit: int | None = None,
    refresh_changed: bool = True,
    ocr_workers: int = 3,
    ocr_dpi: int = 180,
) -> tuple[int, int]:
    statuses = "'pending','error','stale','extracted'" if refresh_changed else "'pending','error','stale'"
    query = (
        """SELECT source_id,source_url,title FROM sources
           WHERE source_type='pdf' AND first_party=1
             AND extraction_status IN (""" + statuses + ") ORDER BY source_url"
    )
    if limit is not None:
        query += " LIMIT ?"
        candidates = connection.execute(query, (limit,)).fetchall()
    else:
        candidates = connection.execute(query).fetchall()
    completed = errors = 0
    for source_id, url, title in candidates:
        try:
            data, headers = _request(url, max_bytes=MAX_DOWNLOAD_BYTES)
            if not data.startswith(b"%PDF-"):
                raise ValueError("response content is not a PDF")
            digest = hashlib.sha256(data).hexdigest()
            prior = connection.execute(
                "SELECT content_sha256,extraction_status,version FROM sources WHERE source_id=?", (source_id,)
            ).fetchone()
            if prior and prior[0] == digest and prior[1] == "extracted":
                completed += 1
                continue
            with tempfile.TemporaryDirectory(prefix="wp_pdf_") as temp_dir:
                pdf_path = Path(temp_dir) / "source.pdf"
                pdf_path.write_bytes(data)
                text, pages, method = pdf_text(
                    pdf_path, tesseract=tesseract, tessdata=tessdata, language=language,
                    ocr_workers=ocr_workers, ocr_dpi=ocr_dpi,
                )
            connection.execute("DELETE FROM source_search WHERE source_id=?", (source_id,))
            connection.execute(
                """UPDATE sources SET content_sha256=?,byte_size=?,version=?,updated_at=?,fetch_status='available',
                     extraction_status='extracted',extraction_method=?,page_count=?,extracted_text=?,indexed_at=datetime('now')
                   WHERE source_id=?""",
                (digest, len(data), headers.get("ETag") or headers.get("Last-Modified") or digest,
                 headers.get("Last-Modified"), method, pages, text, source_id),
            )
            if prior and prior[0] and prior[0] != digest:
                event = connection.execute(
                    """INSERT INTO source_change_events(source_id,detected_at,old_sha256,new_sha256,
                         old_version,new_version,status)
                       VALUES(?,datetime('now'),?,?,?,?, 'pending_topic_review')""",
                    (source_id, prior[0], digest, prior[2], headers.get("ETag") or headers.get("Last-Modified") or digest),
                )
                event_id = int(event.lastrowid)
                if queue_proposals_for_approved_links(connection, source_id, event_id):
                    connection.execute(
                        "UPDATE source_change_events SET status='pending_approval' WHERE event_id=?",
                        (event_id,),
                    )
            connection.execute("INSERT INTO source_search(source_id,title,text) VALUES(?,?,?)", (source_id, title, text))
            connection.commit()
            completed += 1
            print(f"PDF_OK {completed}/{len(candidates)} pages={pages} method={method} title={title[:72]}")
        except Exception as exc:
            connection.execute(
                "UPDATE sources SET fetch_status='error',extraction_status='error',indexed_at=datetime('now') WHERE source_id=?",
                (source_id,),
            )
            connection.execute(
                "INSERT INTO sync_errors(run_id,source_url,stage,error) VALUES(?,?,?,?)",
            (run_id, url, "pdf_ocr", f"{type(exc).__name__}: {exc}"[:1000]),
            )
            connection.commit()
            errors += 1
            print(f"PDF_ERROR {url}: {type(exc).__name__}: {str(exc)[:180]}")
        time.sleep(delay)
    return completed, errors


def sync(args: argparse.Namespace) -> int:
    category_id = discover_category_id(args.category_url)
    posts, expected = fetch_category_posts(args.category_url, category_id)
    connection = initialize_database(args.database)
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    cursor = connection.execute(
        "INSERT INTO sync_runs(started_at,category_url,category_id,expected_posts) VALUES(?,?,?,?)",
        (started, args.category_url, category_id, expected),
    )
    run_id = int(cursor.lastrowid)
    topics = topic_catalog()
    for topic in topics:
        connection.execute(
            """INSERT INTO topics(topic_id,title,terms_json) VALUES(?,?,?)
               ON CONFLICT(topic_id) DO UPDATE SET title=excluded.title,terms_json=excluded.terms_json""",
            (topic["topic_id"], topic["title"], json.dumps(sorted(topic["terms"]), ensure_ascii=False)),
        )
    for post in posts:
        _store_post(connection, post, category_id, run_id, topics)
    connection.commit()
    media_metadata = fetch_media_metadata(args.category_url)
    changed_media = update_media_metadata(connection, media_metadata)
    materialize_waiting_proposals(connection)
    print(f"POSTS_STORED={len(posts)} TOPICS_IN_CATALOG={len(topics)} CATEGORY_ID={category_id}")
    print("ASSETS=" + str(connection.execute("SELECT count(*) FROM sources WHERE source_type!='wordpress_post'").fetchone()[0]))
    print("PDF_FIRST_PARTY=" + str(connection.execute("SELECT count(*) FROM sources WHERE source_type='pdf' AND first_party=1").fetchone()[0]))
    print(f"WORDPRESS_MEDIA_METADATA={len(media_metadata)} CHANGED_MEDIA={changed_media}")
    tesseract = args.tesseract or os.environ.get("TESSERACT_CMD") or shutil.which("tesseract")
    tessdata = args.tessdata or (Path(os.environ["TESSDATA_PREFIX"]) if os.environ.get("TESSDATA_PREFIX") else None)
    pdf_count = pdf_errors = 0
    if args.ocr:
        if not tesseract:
            raise RuntimeError("Tesseract not found; install it or pass --tesseract /path/to/tesseract")
        pdf_count, pdf_errors = index_first_party_pdfs(
            connection, run_id, tesseract=tesseract, tessdata=tessdata,
            language=args.language, delay=args.delay, limit=args.limit_pdfs,
            refresh_changed=not args.skip_pdf_refresh,
            ocr_workers=args.ocr_workers, ocr_dpi=args.ocr_dpi,
        )
    pending = connection.execute("SELECT count(*) FROM topic_links WHERE status='pending_review'").fetchone()[0]
    unresolved = connection.execute(
        "SELECT count(*) FROM posts p WHERE NOT EXISTS(SELECT 1 FROM topic_links t WHERE t.post_id=p.post_id)"
    ).fetchone()[0]
    source_count = connection.execute("SELECT count(*) FROM sources").fetchone()[0]
    connection.execute(
            "UPDATE sync_runs SET finished_at=?,posts_seen=?,sources_seen=?,pdfs_ocred=?,errors=? WHERE run_id=?",
        (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), len(posts), source_count, pdf_count, pdf_errors, run_id),
    )
    connection.commit()
    connection.close()
    print(f"SOURCES_TOTAL={source_count} TOPIC_LINKS_PENDING_REVIEW={pending} POSTS_WITHOUT_CANDIDATE={unresolved}")
    print(f"PDFS_PROCESSED={pdf_count} PDF_ERRORS={pdf_errors} DATABASE={args.database}")
    return 0 if pdf_errors == 0 else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category-url", default=DEFAULT_CATEGORY_URL)
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--ocr", action="store_true", help="Download and index linked first-party PDFs")
    parser.add_argument("--tesseract", help="Local Tesseract executable; defaults to TESSERACT_CMD or PATH")
    parser.add_argument("--tessdata", type=Path, help="Tesseract language-data directory")
    parser.add_argument("--language", default="kor+eng")
    parser.add_argument("--delay", type=float, default=0.15, help="Pause between PDF downloads")
    parser.add_argument("--limit-pdfs", type=int, help="Limit PDFs for an initial OCR check; omit to process all")
    parser.add_argument("--skip-pdf-refresh", action="store_true", help="Process pending PDFs only; do not re-fetch extracted PDFs")
    parser.add_argument("--ocr-workers", type=int, default=3, help="Parallel local OCR page workers")
    parser.add_argument("--ocr-dpi", type=int, default=180, help="Rendered page resolution for OCR")
    parser.add_argument("--review-topic-link", nargs=3, metavar=("POST_ID", "TOPIC_ID", "approve|reject"))
    parser.add_argument("--approve-proposal", help="Apply one pending Master update proposal by ID")
    parser.add_argument("--approved-by", help="Required explicit approver identity for --approve-proposal")
    parser.add_argument("--list-content-proposals", action="store_true", help="List curated Topic-content proposals")
    parser.add_argument("--approve-content-proposal", help="Approve a content proposal for candidate preparation; does not write Topic files")
    parser.add_argument("--reject-content-proposal", help="Reject a pending content proposal")
    parser.add_argument("--reviewed-by", help="Required reviewer identity for content proposal decisions")
    parser.add_argument("--prepare-content-candidate", help="Build an isolated candidate bundle from an approved proposal")
    parser.add_argument("--apply-content-candidate", help="Apply a reviewed candidate to canonical Topic/Master files")
    parser.add_argument("--applied-by", help="Required explicit identity for --apply-content-candidate")
    parser.add_argument("--candidate-root", type=Path, help="Repository-local directory for candidate bundles")
    parser.add_argument("--list-pending", action="store_true", help="List candidate links and Master proposals")
    parser.add_argument("--limit", type=int, default=50, help="Maximum pending rows to display")
    args = parser.parse_args()
    if args.review_topic_link:
        post_id, topic_id, decision = args.review_topic_link
        queued = review_topic_link(args.database, int(post_id), topic_id, decision)
        print(f"TOPIC_LINK={decision} MASTER_PROPOSALS_QUEUED={queued}")
        return 0
    if args.approve_proposal:
        if not args.approved_by:
            parser.error("--approved-by is required with --approve-proposal")
        approve_master_proposal(args.database, args.approve_proposal, args.approved_by)
        print(f"MASTER_PROPOSAL_APPLIED={args.approve_proposal}")
        return 0
    if args.approve_content_proposal:
        if not args.reviewed_by:
            parser.error("--reviewed-by is required with --approve-content-proposal")
        proposal = resolve_content_update_proposal(
            args.database,
            args.approve_content_proposal,
            decision="approve",
            reviewed_by=args.reviewed_by,
        )
        print(f"CONTENT_PROPOSAL_APPROVED={proposal['proposal_id']} CONTENT_WRITTEN=false")
        return 0
    if args.reject_content_proposal:
        if not args.reviewed_by:
            parser.error("--reviewed-by is required with --reject-content-proposal")
        proposal = resolve_content_update_proposal(
            args.database,
            args.reject_content_proposal,
            decision="reject",
            reviewed_by=args.reviewed_by,
        )
        print(f"CONTENT_PROPOSAL_REJECTED={proposal['proposal_id']}")
        return 0
    if args.prepare_content_candidate:
        candidate_path = prepare_content_update_candidate(
            args.database,
            args.prepare_content_candidate,
            candidate_root=args.candidate_root,
        )
        print(f"CONTENT_CANDIDATE_READY={candidate_path}")
        print("CANONICAL_TOPIC_FILES_CHANGED=false")
        return 0
    if args.apply_content_candidate:
        if not args.applied_by:
            parser.error("--applied-by is required with --apply-content-candidate")
        result = apply_content_update_candidate(
            args.database,
            args.apply_content_candidate,
            applied_by=args.applied_by,
        )
        print(f"CONTENT_CANDIDATE_APPLIED={result['proposal']['proposal_id']}")
        print(f"MASTER_REVISION={result['master']['revision']}")
        for path in result["applied_files"]:
            print(f"APPLIED_FILE={path}")
        return 0
    if args.list_content_proposals:
        show_content_update_proposals(args.database, args.limit)
        return 0
    if args.list_pending:
        list_pending(args.database, args.limit)
        return 0
    return sync(args)


if __name__ == "__main__":
    raise SystemExit(main())
