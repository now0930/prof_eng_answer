#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = ROOT / "rubrics" / "generated"
PACK_ROOT = ROOT / "rubrics" / "topic_packs"

REQUIRED_GENERATED_FILES = [
    "fact_anchors.generated.json",
    "model_answers.generated.json",
    "topic_importance.generated.json",
    "logic_checks.generated.json",
    "logic_check_profiles.generated.json",
    "topic_pack_manifest.generated.json",
]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(1)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing file: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"invalid JSON: {path}: {e}")

    if not isinstance(data, dict):
        fail(f"root must be object: {path}")

    return data


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{label}: must be list")
    return value


def collect_topic_pack_ids() -> set[str]:
    if not PACK_ROOT.exists():
        return set()

    return {
        p.name
        for p in PACK_ROOT.iterdir()
        if p.is_dir()
    }


def collect_topic_ids_from_list(items: list[Any], label: str) -> set[str]:
    topic_ids: set[str] = set()

    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            fail(f"{label}[{idx}]: must be object")

        topic_id = item.get("topic_id")
        if not isinstance(topic_id, str) or not topic_id.strip():
            fail(f"{label}[{idx}].topic_id required")

        if topic_id in topic_ids:
            fail(f"{label}: duplicate topic_id: {topic_id}")

        topic_ids.add(topic_id)

    return topic_ids


def main() -> int:
    if not GENERATED_DIR.exists():
        fail(f"generated directory not found: {GENERATED_DIR}")

    for name in REQUIRED_GENERATED_FILES:
        path = GENERATED_DIR / name
        if not path.exists():
            fail(f"missing generated file: {path}")

    pack_topic_ids = collect_topic_pack_ids()
    if not pack_topic_ids:
        fail("no topic pack ids found")

    fact = load_json(GENERATED_DIR / "fact_anchors.generated.json")
    model = load_json(GENERATED_DIR / "model_answers.generated.json")
    importance = load_json(GENERATED_DIR / "topic_importance.generated.json")
    logic = load_json(GENERATED_DIR / "logic_checks.generated.json")
    profiles = load_json(GENERATED_DIR / "logic_check_profiles.generated.json")
    manifest = load_json(GENERATED_DIR / "topic_pack_manifest.generated.json")

    fact_ids = collect_topic_ids_from_list(
        require_list(fact.get("topics"), "fact_anchors.generated.json topics"),
        "fact_anchors.generated.json topics",
    )
    model_ids = collect_topic_ids_from_list(
        require_list(model.get("answers"), "model_answers.generated.json answers"),
        "model_answers.generated.json answers",
    )
    importance_ids = collect_topic_ids_from_list(
        require_list(importance.get("topics"), "topic_importance.generated.json topics"),
        "topic_importance.generated.json topics",
    )
    logic_ids = collect_topic_ids_from_list(
        require_list(logic.get("topic_logic_checks"), "logic_checks.generated.json topic_logic_checks"),
        "logic_checks.generated.json topic_logic_checks",
    )
    profile_ids = collect_topic_ids_from_list(
        require_list(profiles.get("profiles"), "logic_check_profiles.generated.json profiles"),
        "logic_check_profiles.generated.json profiles",
    )
    manifest_ids = collect_topic_ids_from_list(
        require_list(manifest.get("topics"), "topic_pack_manifest.generated.json topics"),
        "topic_pack_manifest.generated.json topics",
    )

    generated_sets = {
        "fact_anchors": fact_ids,
        "model_answers": model_ids,
        "topic_importance": importance_ids,
        "logic_checks": logic_ids,
        "logic_check_profiles": profile_ids,
        "manifest": manifest_ids,
    }

    for name, ids in generated_sets.items():
        missing = pack_topic_ids - ids
        extra = ids - pack_topic_ids

        if missing:
            fail(f"{name}: missing topic ids from generated output: {sorted(missing)}")
        if extra:
            fail(f"{name}: generated output has unknown topic ids: {sorted(extra)}")

    print("VALID: generated rubrics")
    print(f"topics: {len(pack_topic_ids)}")
    for topic_id in sorted(pack_topic_ids):
        print(f"- {topic_id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
