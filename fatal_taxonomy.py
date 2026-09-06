"""Validation and lookup for deterministic fatal ownership taxonomy."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


VERSION = "fatal_taxonomy_v1"
PATH = Path(__file__).resolve().parent / "grading_ontology" / "fatal_taxonomy.json"
_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class FatalTaxonomyError(ValueError):
    pass


def load_fatal_taxonomy(path: Path = PATH) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if set(payload) != {"version", "entries"} or payload["version"] != VERSION:
        raise FatalTaxonomyError("fatal taxonomy envelope mismatch")
    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        raise FatalTaxonomyError("fatal taxonomy entries must not be empty")
    result: dict[str, dict[str, Any]] = {}
    required = {
        "fatal_id", "invariant_code", "error_class",
        "ontology_owner", "topic_owner",
    }
    invariant_codes: set[str] = set()
    for index, row in enumerate(entries):
        if not isinstance(row, dict) or set(row) != required:
            raise FatalTaxonomyError(f"entries[{index}] fields mismatch")
        if any(not _ID.fullmatch(str(row[key])) for key in required):
            raise FatalTaxonomyError(f"entries[{index}] has invalid identifier")
        fatal_id = row["fatal_id"]
        invariant_code = row["invariant_code"]
        if fatal_id in result or invariant_code in invariant_codes:
            raise FatalTaxonomyError("fatal and invariant owners must be unique")
        topic_path = PATH.parent.parent / "rubrics" / "topic_packs" / row["topic_owner"]
        if not topic_path.is_dir():
            raise FatalTaxonomyError(f"unknown topic owner: {row['topic_owner']}")
        result[fatal_id] = dict(row)
        invariant_codes.add(invariant_code)
    return result
