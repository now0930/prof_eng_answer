"""Read-only WordPress source and claim projection; never promotes grading facts."""

from __future__ import annotations

from pathlib import Path
import re
import sqlite3
from typing import Any

from grading.evidence.fact_grounded_contracts import VERSION, validate_fact
from .master_topic_pack import validate_master_topic_pack
from .wordpress_claims import validate_wordpress_claim


class WordPressFactProjectionError(ValueError):
    """A source, claim or explicit relation binding cannot be safely projected."""


def load_source_catalog_read_only(database_path: str | Path, source_ids: set[str]) -> dict[str, dict[str, Any]]:
    """Load only requested private source rows; do not create or update the DB."""
    path = Path(database_path).resolve()
    if not path.is_file():
        raise WordPressFactProjectionError("source database is unavailable")
    connection = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
    try:
        connection.execute("PRAGMA query_only=ON")
        rows = {}
        for source_id in sorted(source_ids):
            row = connection.execute(
                "SELECT source_id,source_url,version,content_sha256,fetch_status,extracted_text "
                "FROM sources WHERE source_id=?", (source_id,),
            ).fetchone()
            if row is not None:
                rows[source_id] = dict(zip(
                    ("source_id", "source_url", "version", "content_sha256", "fetch_status", "extracted_text"), row,
                ))
        return rows
    finally:
        connection.close()


def project_source_readiness(master: dict[str, Any], catalog: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Compare Master references to private source metadata without copying text."""
    validate_master_topic_pack(master)
    result: list[dict[str, Any]] = []
    for ref in master["sources"]:
        row = catalog.get(ref["source_id"])
        status = "unavailable"
        digest = None
        if row is not None:
            digest = row.get("content_sha256")
            if row.get("fetch_status") == "available" and isinstance(digest, str) and re.fullmatch(r"[0-9a-fA-F]{64}", digest):
                expected_url = ref.get("source_url") or ref["wordpress_url"]
                if expected_url != row.get("source_url") or str(ref["version"]) != str(row.get("version")):
                    status = "stale"
                elif ref.get("content_sha256") and ref["content_sha256"].lower() != digest.lower():
                    status = "stale"
                elif ref["verification_status"] == "verified":
                    status = "verified" if ref.get("content_sha256") else "unverified"
                elif ref["verification_status"] == "stale":
                    status = "stale"
                elif ref["verification_status"] == "unavailable":
                    status = "unavailable"
                else:
                    status = "unverified"
        result.append({
            "topic_id": master["topic_id"], "source_id": ref["source_id"],
            "status": status, "source_sha256": digest, "score_effect": "none",
        })
    return result


def project_claim_candidate(
    master: dict[str, Any], claim: dict[str, Any], binding: dict[str, Any],
    catalog: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Project an explicitly bound claim as a candidate, never an approved fact."""
    validate_master_topic_pack(master)
    validate_wordpress_claim(claim)
    if claim["topic_id"] != master["topic_id"]:
        raise WordPressFactProjectionError("claim topic does not match Master")
    if claim["review_status"] != "approved":
        raise WordPressFactProjectionError("claim has no content approval")
    required = {"claim_id", "fact_id", "subject", "predicate", "object", "conditions"}
    if not isinstance(binding, dict) or set(binding) != required or binding["claim_id"] != claim["claim_id"]:
        raise WordPressFactProjectionError("explicit relation binding is missing or mismatched")
    refs_by_id = {ref["source_id"]: ref for ref in master["sources"]}
    readiness = {row["source_id"]: row for row in project_source_readiness(master, catalog)}
    source_refs = []
    for evidence in claim["evidence"]:
        source_id = evidence["source_id"]
        master_ref = refs_by_id.get(source_id)
        row = catalog.get(source_id)
        if master_ref is None or row is None or readiness[source_id]["status"] != "verified":
            raise WordPressFactProjectionError("source is missing, stale or unverified")
        if (
            evidence["source_url"] != row["source_url"]
            or str(evidence["source_version"]) != str(row["version"])
            or evidence["source_content_sha256"].lower() != row["content_sha256"].lower()
        ):
            raise WordPressFactProjectionError("claim evidence does not match source revision")
        source_text = row.get("extracted_text")
        if not isinstance(source_text, str) or evidence["excerpt"] not in source_text:
            raise WordPressFactProjectionError("claim excerpt not found in source text")
        source_refs.append({
            "source_id": source_id, "source_version": str(row["version"]),
            "source_sha256": row["content_sha256"].lower(), "locator": evidence["locator"],
        })
    fact = {
        "schema_version": VERSION, "fact_id": binding["fact_id"], "topic_id": master["topic_id"],
        "statement": claim["claim_text"],
        "relation": {key: binding[key] for key in ("subject", "predicate", "object", "conditions")},
        "source_refs": source_refs, "review_status": "candidate", "revision": 1,
        "score_effect": "none",
    }
    return validate_fact(fact)
