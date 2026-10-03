"""Read private, OCR-enriched WordPress source packs for learning consumers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PACK_SCHEMA_VERSION = "wordpress-topic-pack-v1"


def load_wordpress_topic_pack(repository_root: str | Path, topic_id: str) -> dict[str, Any] | None:
    """Load a local, private OCR source pack; never affects grading inputs."""
    root = Path(repository_root).resolve()
    path = (root / "data" / "wordpress_topic_packs" / f"{topic_id}.json").resolve()
    if not path.is_relative_to(root / "data"):
        raise ValueError("WordPress Topic Pack path escapes the private data directory")
    if not path.is_file():
        return None
    try:
        pack = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not read private WordPress Topic Pack: {path.name}") from exc
    if (
        not isinstance(pack, dict)
        or pack.get("schema_version") != PACK_SCHEMA_VERSION
        or pack.get("topic_id") != topic_id
        or not isinstance(pack.get("sources"), list)
    ):
        raise ValueError(f"private WordPress Topic Pack contract failed: {path.name}")
    for source in pack["sources"]:
        if not isinstance(source, dict) or source.get("verification_status") != "unverified":
            raise ValueError(f"invalid source record in private WordPress Topic Pack: {path.name}")
    return pack
