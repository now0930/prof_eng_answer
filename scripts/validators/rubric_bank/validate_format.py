#!/usr/bin/env python3
"""
Rubric Bank format validator.

Scope:
- file existence
- JSON parseability
- root object type
- expected top-level collection key
- non-empty collection
- basic item object shape

This validator intentionally does not validate semantic correctness.
Semantic/cross-reference checks belong to the later content validation phase.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = REPO_ROOT / "reports" / "rubric_bank"
REPORT_PATH = REPORT_DIR / "format_validation.json"


@dataclass(frozen=True)
class RubricFileSpec:
    name: str
    path: str
    required_any_keys: tuple[str, ...]
    expected_collection_types: tuple[type, ...] = (list, dict)


RUBRIC_FILES: tuple[RubricFileSpec, ...] = (
    RubricFileSpec(
        name="scoring_model",
        path="rubrics/scoring_model/default.json",
        required_any_keys=("layers", "scoring_layers"),
    ),
    RubricFileSpec(
        name="rater_profile",
        path="rubrics/raters/layered_default.json",
        required_any_keys=("raters", "rater_weights", "weights", "layer_weights"),
    ),
    RubricFileSpec(
        name="question_type_profile",
        path="rubrics/question_types/default.json",
        required_any_keys=("types", "question_types"),
    ),
    RubricFileSpec(
        name="model_answer_bank",
        path="rubrics/model_answers/industrial_instrumentation_control.json",
        required_any_keys=("answers", "model_answers"),
    ),
    RubricFileSpec(
        name="fact_anchor_bank",
        path="rubrics/fact_anchors/industrial_instrumentation_control.json",
        required_any_keys=("topics", "fact_anchors"),
    ),
    RubricFileSpec(
        name="topic_importance",
        path="rubrics/topic_importance/industrial_instrumentation_control.json",
        required_any_keys=("topics", "topic_importance", "importance"),
    ),
    RubricFileSpec(
        name="logic_check_bank",
        path="rubrics/logic_checks/industrial_instrumentation_control.json",
        required_any_keys=("topic_logic_checks", "topics", "logic_checks"),
    ),
    RubricFileSpec(
        name="logic_check_profile",
        path="rubrics/logic_check_profiles/industrial_instrumentation_control.json",
        required_any_keys=("topics", "profiles", "logic_check_profiles"),
    ),
)


def load_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, "file not found"
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: line={exc.lineno} col={exc.colno} msg={exc.msg}"
    except UnicodeDecodeError as exc:
        return None, f"encoding error: {exc}"
    except OSError as exc:
        return None, f"read error: {exc}"


def find_collection_key(data: dict[str, Any], spec: RubricFileSpec) -> str | None:
    for key in spec.required_any_keys:
        if key in data:
            return key
    return None


def collection_size(value: Any) -> int:
    if isinstance(value, (list, dict)):
        return len(value)
    return 0


def count_object_items(value: Any) -> tuple[int, int]:
    if isinstance(value, list):
        total = len(value)
        object_count = sum(1 for item in value if isinstance(item, dict))
        return total, object_count

    if isinstance(value, dict):
        total = len(value)
        object_count = sum(1 for item in value.values() if isinstance(item, dict))
        return total, object_count

    return 0, 0


def detect_version(data: dict[str, Any]) -> str | None:
    version = data.get("version") or data.get("schema_version")
    if isinstance(version, str):
        return version
    return None


def validate_one(spec: RubricFileSpec) -> dict[str, Any]:
    path = REPO_ROOT / spec.path
    result: dict[str, Any] = {
        "name": spec.name,
        "path": spec.path,
        "valid": False,
        "errors": [],
        "warnings": [],
        "summary": {},
    }

    data, error = load_json(path)
    if error:
        result["errors"].append(error)
        return result

    if not isinstance(data, dict):
        result["errors"].append(
            f"root must be object/dict, got {type(data).__name__}"
        )
        return result

    collection_key = find_collection_key(data, spec)
    if collection_key is None:
        result["errors"].append(
            "missing expected top-level key; expected one of: "
            + ", ".join(spec.required_any_keys)
        )
        result["summary"]["available_keys"] = sorted(data.keys())
        return result

    collection = data.get(collection_key)

    if not isinstance(collection, spec.expected_collection_types):
        expected_names = ", ".join(t.__name__ for t in spec.expected_collection_types)
        result["errors"].append(
            f"{collection_key} must be one of ({expected_names}), "
            f"got {type(collection).__name__}"
        )
        return result

    size = collection_size(collection)
    if size == 0:
        result["errors"].append(f"{collection_key} must not be empty")
        return result

    total_items, object_items = count_object_items(collection)
    if total_items > 0 and object_items == 0:
        result["warnings"].append(
            f"{collection_key} has no object-like items; this may be intentional "
            "for mapping-style files, but should be reviewed"
        )

    if isinstance(collection, list) and object_items != total_items:
        result["errors"].append(
            f"{collection_key} list items must be objects: "
            f"object_items={object_items}, total_items={total_items}"
        )
        return result

    result["valid"] = True
    result["summary"] = {
        "root_keys": sorted(data.keys()),
        "collection_key": collection_key,
        "collection_type": type(collection).__name__,
        "collection_size": size,
        "object_items": object_items,
        "version": detect_version(data),
    }

    if detect_version(data) is None:
        result["warnings"].append("version/schema_version is missing")

    return result


def main() -> int:
    results = [validate_one(spec) for spec in RUBRIC_FILES]
    errors = [
        f"{item['name']}: {error}"
        for item in results
        for error in item["errors"]
    ]

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(
            {
                "valid": not errors,
                "checked_files": len(results),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    if errors:
        print("INVALID: Rubric Bank format")
        for error in errors:
            print(f"- {error}")
        print(f"Wrote: {REPORT_PATH}")
        return 1

    print("VALID: Rubric Bank format")
    for item in results:
        summary = item["summary"]
        warnings = item["warnings"]
        line = (
            f"- {item['name']} | {item['path']} | "
            f"{summary['collection_key']}={summary['collection_size']} | "
            f"type={summary['collection_type']}"
        )
        version = summary.get("version")
        if version:
            line += f" | version={version}"
        print(line)

        for warning in warnings:
            print(f"  WARN: {warning}")

    print(f"Wrote: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
