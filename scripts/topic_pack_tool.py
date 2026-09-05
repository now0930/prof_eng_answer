from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.topic_pack_contract import (  # noqa: E402
    ContractIssue,
    TOPIC_ROOT,
    clone_json,
    load_json,
    load_profile,
    validate_against_schema,
    validate_profile,
    validate_spec,
)

SOURCE_FILES = (
    "README.md",
    "fact_anchor.json",
    "logic_check.json",
    "model_answer.json",
    "topic_importance.json",
)
SUPPORTED_PROJECTION_MODES = {
    "EXACT",
    "PROFILE",
    "PROFILE_SCHEMA",
    "RENDERED",
    "FIXED",
    "VALIDATION_ONLY",
}
FORBIDDEN_RUNTIME_KEYS = {
    "source_topic",
    "source_path",
    "donor_topic",
    "donor_path",
}

_KEY_ALIASES: dict[str, tuple[str, ...]] = {
    "id": ("id", "rule_id", "anchor_id", "condition_id", "claim_id"),
    "candidate_id": ("candidate_id", "id", "rule_id"),
    "rule_id": ("rule_id", "id"),
    "anchor_id": ("anchor_id", "id"),
    "condition_id": ("condition_id", "id"),
    "claim_id": ("claim_id", "id"),
    "title": ("title", "section", "pattern"),
    "statement": ("statement", "claim", "content", "condition", "message"),
    "claim": ("claim", "statement", "condition", "message", "content"),
    "condition": ("condition", "claim", "statement", "message", "content"),
    "message": ("message", "claim", "statement", "content", "check"),
    "content": ("content", "statement", "claim", "expected", "purpose"),
    "check": ("check", "condition", "statement", "claim"),
    "expected": ("expected", "correct_rule", "content", "purpose"),
    "correct_rule": ("correct_rule", "expected", "content"),
    "rationale": ("rationale", "reason", "purpose"),
    "reason": ("reason", "rationale", "purpose"),
    "purpose": ("purpose", "rationale", "content"),
    "keywords": ("keywords", "tags"),
    "tags": ("tags", "keywords"),
    "pattern": ("pattern", "title", "statement"),
    "section": ("section", "title"),
    "required_anchor_ids": ("required_anchor_ids", "anchor_ids"),
    "anchor_ids": ("anchor_ids", "required_anchor_ids"),
    "aliases": ("aliases", "routing_aliases"),
    "topic_id": ("topic_id",),
    "trigger": ("trigger",),
    "scope": ("scope",),
}


def _issue(code: str, path: str, message: str) -> ContractIssue:
    return ContractIssue(code, path, message)


def _issue_dicts(issues: Sequence[ContractIssue]) -> list[dict[str, str]]:
    return [issue.to_dict() for issue in issues]


def _result(
    *,
    passed: bool,
    command: str,
    topic_id: str = "",
    profile_id: str = "",
    issues: Sequence[ContractIssue] = (),
    **extra: Any,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "result": "PASS" if passed else "FAIL",
        "command": command,
        "topic_id": topic_id,
        "profile_id": profile_id,
        "issue_count": len(issues),
        "issues": _issue_dicts(issues),
    }
    payload.update(extra)
    return payload


def _load_spec(path: Path) -> tuple[dict[str, Any] | None, list[ContractIssue]]:
    try:
        value = load_json(path)
    except Exception as error:
        return None, [
            _issue(
                "TP001_SPEC_SCHEMA_INVALID",
                "$",
                f"cannot read spec JSON: {type(error).__name__}: {error}",
            )
        ]
    if not isinstance(value, dict):
        return None, [
            _issue(
                "TP001_SPEC_SCHEMA_INVALID",
                "$",
                "spec root must be an object",
            )
        ]
    return value, []


def _load_profile_for_spec(
    spec: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, list[ContractIssue]]:
    profile_id = spec.get("profile_id")
    if not isinstance(profile_id, str) or not profile_id:
        return None, [
            _issue(
                "TP002_PROFILE_NOT_FOUND",
                "$.profile_id",
                "profile_id is missing or invalid",
            )
        ]
    try:
        profile = load_profile(profile_id)
    except Exception as error:
        return None, [
            _issue(
                "TP002_PROFILE_NOT_FOUND",
                "$.profile_id",
                f"cannot load profile {profile_id}: {type(error).__name__}: {error}",
            )
        ]
    return profile, []


def _parse_target(target: str) -> tuple[str, str]:
    """Parse only an explicit canonical JSON target."""
    value = target.strip()
    match = re.match(
        r"^(fact_anchor\.json|logic_check\.json|"
        r"model_answer\.json|topic_importance\.json)\s+(\$.*)$",
        value,
    )
    if not match:
        raise ValueError(f"not an explicit JSON target: {target}")
    return match.group(1), match.group(2)


def _walk_key_paths(
    value: Any,
    *,
    path: str = "$",
) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            rows.append((child_path, str(key)))
            rows.extend(_walk_key_paths(child, path=child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            rows.extend(
                _walk_key_paths(
                    child,
                    path=f"{path}[{index}]",
                )
            )
    return rows


def _resolve_projection_targets(
    target: str,
    profile: Mapping[str, Any],
) -> list[dict[str, str]]:
    canonical_files = profile.get("canonical_files")
    if not isinstance(canonical_files, Mapping):
        canonical_files = {}

    value = target.strip()
    try:
        file_name, json_path = _parse_target(value)
    except ValueError:
        pass
    else:
        return [
            {
                "kind": "JSON_PATH",
                "file": file_name,
                "path": json_path,
            }
        ]

    if value == "all four JSON top-level topic_id":
        return [
            {
                "kind": "JSON_PATH",
                "file": str(file_name),
                "path": "$.topic_id",
            }
            for file_name in sorted(canonical_files)
        ]

    if value == "all supported title fields and README H1":
        targets: list[dict[str, str]] = []
        for file_name, contract in canonical_files.items():
            if not isinstance(contract, Mapping):
                continue
            template = contract.get("template")
            for json_path, key in _walk_key_paths(template):
                if key in {"title", "title_ko", "topic_title"}:
                    targets.append(
                        {
                            "kind": "JSON_PATH",
                            "file": str(file_name),
                            "path": json_path,
                        }
                    )
        targets.append(
            {
                "kind": "README_H1",
                "file": "README.md",
                "path": "H1",
            }
        )
        return targets

    if value == "README adjacent Topic section":
        return [
            {
                "kind": "README_SECTION",
                "file": "README.md",
                "path": "ADJACENT_TOPIC_SECTION",
            }
        ]

    if value == "model_answer.json approved routing field":
        return [
            {
                "kind": "JSON_PATH",
                "file": "model_answer.json",
                "path": "$.routing_aliases",
            }
        ]

    if value == "generic validator expected destination registry":
        return [
            {
                "kind": "VALIDATION_ONLY",
                "file": "",
                "path": "HANDOFF_DESTINATION_REGISTRY",
            }
        ]

    if value == "model_answer.json and topic_importance.json":
        return [
            {
                "kind": "JSON_PATH",
                "file": "model_answer.json",
                "path": "$.question_type",
            },
            {
                "kind": "JSON_PATH",
                "file": "topic_importance.json",
                "path": "$.question_type",
            },
        ]

    raise ValueError(
        f"unsupported projection target grammar: {target}"
    )


def _json_path_tokens(path: str) -> list[str | int]:
    if path == "$":
        return []
    if not path.startswith("$."):
        raise ValueError(f"unsupported JSON path: {path}")

    tokens: list[str | int] = []
    cursor = 2
    key = ""
    while cursor < len(path):
        character = path[cursor]
        if character == ".":
            if not key:
                raise ValueError(f"empty JSON path token: {path}")
            tokens.append(key)
            key = ""
            cursor += 1
            continue
        if character == "[":
            if key:
                tokens.append(key)
                key = ""
            close = path.find("]", cursor)
            if close < 0:
                raise ValueError(f"unclosed JSON path index: {path}")
            raw_index = path[cursor + 1 : close]
            if not raw_index.isdigit():
                raise ValueError(f"non-numeric JSON path index: {path}")
            tokens.append(int(raw_index))
            cursor = close + 1
            if cursor < len(path) and path[cursor] == ".":
                cursor += 1
            continue
        key += character
        cursor += 1

    if key:
        tokens.append(key)
    return tokens


def _nested_get(value: Any, path: str) -> Any:
    current = value
    for token in _json_path_tokens(path):
        if isinstance(token, int):
            if not isinstance(current, list) or token >= len(current):
                raise KeyError(path)
            current = current[token]
        else:
            if not isinstance(current, Mapping) or token not in current:
                raise KeyError(path)
            current = current[token]
    return current


def _nested_set(document: Any, path: str, value: Any) -> Any:
    tokens = _json_path_tokens(path)
    if not tokens:
        return clone_json(value)

    current = document
    for index, token in enumerate(tokens[:-1]):
        next_token = tokens[index + 1]
        if isinstance(token, int):
            if not isinstance(current, list):
                raise TypeError(f"expected list at {path}")
            while len(current) <= token:
                current.append([] if isinstance(next_token, int) else {})
            current = current[token]
        else:
            if not isinstance(current, dict):
                raise TypeError(f"expected object at {path}")
            if token not in current or not isinstance(current[token], (dict, list)):
                current[token] = [] if isinstance(next_token, int) else {}
            current = current[token]

    final = tokens[-1]
    if isinstance(final, int):
        if not isinstance(current, list):
            raise TypeError(f"expected list at {path}")
        while len(current) <= final:
            current.append(None)
        current[final] = clone_json(value)
    else:
        if not isinstance(current, dict):
            raise TypeError(f"expected object at {path}")
        current[final] = clone_json(value)
    return document


def _schema_at_path(schema: Mapping[str, Any], path: str) -> Mapping[str, Any]:
    current: Mapping[str, Any] = schema
    for token in _json_path_tokens(path):
        if isinstance(token, int):
            child = current.get("items")
        else:
            properties = current.get("properties")
            child = properties.get(token) if isinstance(properties, Mapping) else None
        if not isinstance(child, Mapping):
            return {}
        current = child
    return current


def _source_value_for_key(source: Mapping[str, Any], key: str) -> Any:
    if key in source:
        return source[key]
    for alias in _KEY_ALIASES.get(key, (key,)):
        if alias in source:
            return source[alias]
    return None


def _coerce_to_schema(
    value: Any,
    schema: Mapping[str, Any],
    template: Any = None,
) -> Any:
    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        expected_type = next(
            (item for item in expected_type if item != "null"),
            expected_type[0] if expected_type else None,
        )

    if expected_type == "object" or isinstance(schema.get("properties"), Mapping):
        source = value if isinstance(value, Mapping) else {}
        base = template if isinstance(template, Mapping) else {}
        properties = schema.get("properties")
        if not isinstance(properties, Mapping):
            properties = {}
        required = schema.get("required")
        required_keys = set(required) if isinstance(required, list) else set()

        output: dict[str, Any] = {}
        for key, child_schema in properties.items():
            if not isinstance(child_schema, Mapping):
                child_schema = {}
            candidate = _source_value_for_key(source, str(key))
            if candidate is None and key in base:
                candidate = base[key]
            if candidate is None and key not in required_keys:
                continue
            output[str(key)] = _coerce_to_schema(
                candidate,
                child_schema,
                base.get(key),
            )

        additional = schema.get("additionalProperties", True)
        if additional is not False:
            for key, child in source.items():
                if key not in output:
                    output[str(key)] = clone_json(child)
        return output

    if expected_type == "array" or "items" in schema:
        item_schema = schema.get("items")
        if not isinstance(item_schema, Mapping):
            item_schema = {}
        source_items = value if isinstance(value, list) else []
        template_items = template if isinstance(template, list) else []
        template_item = template_items[0] if template_items else None
        return [
            _coerce_to_schema(item, item_schema, template_item)
            for item in source_items
        ]

    if expected_type == "string":
        if isinstance(value, str):
            return value
        if value is None:
            return template if isinstance(template, str) else ""
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, sort_keys=True)
        return str(value)

    if expected_type == "integer":
        if isinstance(value, bool):
            return 0
        if isinstance(value, int):
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            return template if isinstance(template, int) else 0

    if expected_type == "number":
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value
        try:
            return float(value)
        except (TypeError, ValueError):
            return template if isinstance(template, (int, float)) else 0

    if expected_type == "boolean":
        if isinstance(value, bool):
            return value
        return bool(value) if value is not None else bool(template)

    if expected_type == "null":
        return None

    return clone_json(value if value is not None else template)


def _render_typed_records(
    records: Any,
    *,
    target_template: Any,
    target_schema: Mapping[str, Any],
    canonical_item: Mapping[str, Any] | None,
) -> Any:
    if not isinstance(records, list):
        return _coerce_to_schema(records, target_schema, target_template)

    if canonical_item is not None:
        item_schema = canonical_item.get("item_schema")
        item_template = canonical_item.get("item_template")
        if isinstance(item_schema, Mapping):
            return [
                _coerce_to_schema(item, item_schema, item_template)
                for item in records
            ]

    return _coerce_to_schema(records, target_schema, target_template)


def _render_handoffs(
    handoffs: Any,
    target_template: Any,
    target_schema: Mapping[str, Any],
) -> Any:
    if not isinstance(handoffs, list):
        handoffs = []

    if isinstance(target_template, list):
        if target_template and isinstance(target_template[0], str):
            rendered = [
                (
                    f"{item.get('topic_id', '')}: "
                    f"{item.get('trigger', '')} — "
                    f"{item.get('scope', '')}"
                ).strip()
                for item in handoffs
                if isinstance(item, Mapping)
            ]
            return _coerce_to_schema(rendered, target_schema, target_template)
        return _coerce_to_schema(handoffs, target_schema, target_template)

    if isinstance(target_template, str):
        rendered_text = "\n".join(
            (
                f"- {item.get('topic_id', '')}: "
                f"{item.get('trigger', '')} — "
                f"{item.get('scope', '')}"
            )
            for item in handoffs
            if isinstance(item, Mapping)
        )
        return _coerce_to_schema(rendered_text, target_schema, target_template)

    return _coerce_to_schema(handoffs, target_schema, target_template)


def _render_ownership(
    ownership: Any,
    target_template: Any,
    target_schema: Mapping[str, Any],
) -> Any:
    if not isinstance(ownership, list):
        ownership = []

    if isinstance(target_template, list):
        if target_template and isinstance(target_template[0], str):
            rendered = [
                f"[{item.get('kind', '')}] {item.get('statement', '')}".strip()
                for item in ownership
                if isinstance(item, Mapping)
            ]
            return _coerce_to_schema(rendered, target_schema, target_template)
        return _coerce_to_schema(ownership, target_schema, target_template)

    if isinstance(target_template, str):
        rendered_text = "\n".join(
            f"- [{item.get('kind', '')}] {item.get('statement', '')}".strip()
            for item in ownership
            if isinstance(item, Mapping)
        )
        return _coerce_to_schema(rendered_text, target_schema, target_template)

    return _coerce_to_schema(ownership, target_schema, target_template)


def _canonical_item_for_target(
    profile: Mapping[str, Any],
    target_file: str,
    target_path: str,
) -> Mapping[str, Any] | None:
    items = profile.get("canonical_items")
    if not isinstance(items, Mapping):
        return None
    for item in items.values():
        if not isinstance(item, Mapping):
            continue
        if item.get("target_file") == target_file and item.get("target_path") == target_path:
            return item
    return None


def _validate_projection_registry(
    profile: Mapping[str, Any],
    spec: Mapping[str, Any],
) -> list[ContractIssue]:
    issues: list[ContractIssue] = []
    projections = profile.get("projections")
    fixed_values = profile.get("fixed_values")
    canonical_files = profile.get("canonical_files")

    if not isinstance(projections, list):
        return [
            _issue(
                "TP008_RENDER_SCHEMA_INVALID",
                "$.projections",
                "profile projections must be an array",
            )
        ]
    if not isinstance(fixed_values, Mapping):
        fixed_values = {}
    if not isinstance(canonical_files, Mapping):
        canonical_files = {}

    for index, projection in enumerate(projections):
        path = f"$.projections[{index}]"
        if not isinstance(projection, Mapping):
            issues.append(
                _issue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    path,
                    "projection must be an object",
                )
            )
            continue

        field = projection.get("spec_field")
        mode = projection.get("projection_mode")
        target = projection.get("target")

        if mode not in SUPPORTED_PROJECTION_MODES:
            issues.append(
                _issue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    f"{path}.projection_mode",
                    f"unsupported projection mode: {mode}",
                )
            )
            continue

        if not isinstance(field, str) or not field:
            issues.append(
                _issue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    f"{path}.spec_field",
                    "projection field is missing",
                )
            )
            continue

        if mode == "FIXED":
            if field not in fixed_values:
                issues.append(
                    _issue(
                        "TP008_RENDER_SCHEMA_INVALID",
                        f"{path}.spec_field",
                        "FIXED field is absent from "
                        f"profile.fixed_values: {field}",
                    )
                )
        elif field not in spec:
            issues.append(
                _issue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    f"{path}.spec_field",
                    f"projection field is absent from spec: {field}",
                )
            )

        try:
            targets = _resolve_projection_targets(
                str(target or ""),
                profile,
            )
        except ValueError as error:
            issues.append(
                _issue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    f"{path}.target",
                    str(error),
                )
            )
            continue

        if mode == "VALIDATION_ONLY":
            if not all(
                item["kind"] == "VALIDATION_ONLY"
                for item in targets
            ):
                issues.append(
                    _issue(
                        "TP008_RENDER_SCHEMA_INVALID",
                        f"{path}.target",
                        "VALIDATION_ONLY mode must resolve to "
                        "a validation-only target",
                    )
                )
            continue

        for item in targets:
            kind = item["kind"]
            if kind == "JSON_PATH":
                if item["file"] not in canonical_files:
                    issues.append(
                        _issue(
                            "TP008_RENDER_SCHEMA_INVALID",
                            f"{path}.target",
                            "projection target is not a "
                            f"canonical JSON file: {item['file']}",
                        )
                    )
                if not item["path"].startswith("$"):
                    issues.append(
                        _issue(
                            "TP008_RENDER_SCHEMA_INVALID",
                            f"{path}.target",
                            "invalid target JSON path: "
                            f"{item['path']}",
                        )
                    )
            elif kind not in {
                "README_H1",
                "README_SECTION",
            }:
                issues.append(
                    _issue(
                        "TP008_RENDER_SCHEMA_INVALID",
                        f"{path}.target",
                        "unsupported resolved target kind: "
                        f"{kind}",
                    )
                )
    return issues


def plan_spec(
    spec: Mapping[str, Any],
    profile: Mapping[str, Any],
    *,
    topic_root: Path = TOPIC_ROOT,
) -> dict[str, Any]:
    issues = list(validate_profile(profile))
    issues.extend(validate_spec(spec, profile, topic_root=topic_root))
    issues.extend(_validate_projection_registry(profile, spec))

    topic_id = str(spec.get("topic_id") or "")
    profile_id = str(spec.get("profile_id") or "")
    planned_paths = [
        (topic_root / topic_id / file_name).as_posix()
        for file_name in SOURCE_FILES
    ]
    return _result(
        passed=not issues,
        command="plan",
        topic_id=topic_id,
        profile_id=profile_id,
        issues=issues,
        planned_paths=planned_paths,
        source_file_count=len(SOURCE_FILES),
        repository_mutation=False,
        runtime_donor_dependency=False,
    )


def plan_topic(
    spec_path: Path,
    *,
    topic_root: Path = TOPIC_ROOT,
) -> dict[str, Any]:
    spec, issues = _load_spec(spec_path)
    if spec is None:
        return _result(
            passed=False,
            command="plan",
            issues=issues,
            repository_mutation=False,
        )
    profile, profile_issues = _load_profile_for_spec(spec)
    if profile is None:
        return _result(
            passed=False,
            command="plan",
            topic_id=str(spec.get("topic_id") or ""),
            profile_id=str(spec.get("profile_id") or ""),
            issues=profile_issues,
            repository_mutation=False,
        )
    return plan_spec(spec, profile, topic_root=topic_root)


def _render_readme(spec: Mapping[str, Any]) -> str:
    ownership = spec.get("ownership_statements")
    handoffs = spec.get("handoffs")
    standards = spec.get("standards_and_sources")
    anchors = spec.get("anchors")

    lines = [
        f"# {spec.get('title_ko', '')}",
        "",
        f"- Topic ID: `{spec.get('topic_id', '')}`",
        f"- Question type: `{spec.get('question_type', '')}`",
        f"- Difficulty: `{spec.get('difficulty', '')}`",
        f"- Selection importance: `{spec.get('selection_importance', '')}`",
        "",
        "## Scope",
        "",
        str(spec.get("scope_summary") or ""),
        "",
        "## Ownership",
        "",
    ]

    if isinstance(ownership, list):
        for item in ownership:
            if isinstance(item, Mapping):
                lines.append(
                    f"- **{item.get('kind', '')}**: "
                    f"{item.get('statement', '')}"
                )

    lines.extend(["", "## Technical anchors", ""])
    if isinstance(anchors, list):
        for item in anchors:
            if isinstance(item, Mapping):
                lines.extend([
                    f"### {item.get('title', '')}",
                    "",
                    str(item.get("content") or ""),
                    "",
                ])

    lines.extend(["## Handoffs", ""])
    if isinstance(handoffs, list) and handoffs:
        for item in handoffs:
            if isinstance(item, Mapping):
                lines.append(
                    f"- `{item.get('topic_id', '')}` — "
                    f"{item.get('trigger', '')}: "
                    f"{item.get('scope', '')}"
                )
    else:
        lines.append("- None")

    if isinstance(standards, list) and standards:
        lines.extend(["", "## Standards and sources", ""])
        for item in standards:
            if isinstance(item, Mapping):
                lines.append(
                    f"- {item.get('reference', '')} "
                    f"({item.get('edition', '')}) — "
                    f"{item.get('relevance', '')}"
                )

    lines.extend([
        "",
        "## Compiler contract",
        "",
        "- Generated from a validated Topic Spec.",
        "- File structure and schema are owned by repository code.",
        "- Runtime donor dependency: `false`.",
        "",
    ])
    return "\n".join(lines)


def render_topic(
    spec: Mapping[str, Any],
    profile: Mapping[str, Any],
) -> dict[str, str]:
    canonical_files = profile.get("canonical_files")
    if not isinstance(canonical_files, Mapping):
        raise ValueError(
            "profile canonical_files must be an object"
        )

    documents: dict[str, Any] = {}
    for file_name, contract in canonical_files.items():
        if not isinstance(contract, Mapping):
            raise ValueError(
                f"invalid canonical file contract: {file_name}"
            )
        documents[str(file_name)] = clone_json(
            contract.get("template")
        )

    projections = profile.get("projections")
    fixed_values = profile.get("fixed_values")
    if not isinstance(projections, list):
        raise ValueError(
            "profile projections must be an array"
        )
    if not isinstance(fixed_values, Mapping):
        fixed_values = {}

    for projection in projections:
        if not isinstance(projection, Mapping):
            raise ValueError("projection must be an object")

        field = str(projection.get("spec_field") or "")
        mode = str(
            projection.get("projection_mode") or ""
        )
        target_text = str(
            projection.get("target") or ""
        )
        targets = _resolve_projection_targets(
            target_text,
            profile,
        )

        if mode == "VALIDATION_ONLY":
            continue

        source_value = (
            fixed_values.get(field)
            if mode == "FIXED"
            else spec.get(field)
        )

        for target in targets:
            kind = target["kind"]
            if kind in {
                "README_H1",
                "README_SECTION",
            }:
                # README is rendered once from the typed Topic Spec.
                continue
            if kind != "JSON_PATH":
                raise ValueError(
                    "unsupported resolved target kind: "
                    f"{kind}"
                )

            target_file = target["file"]
            target_path = target["path"]
            if target_file not in documents:
                raise ValueError(
                    "projection target file is not canonical: "
                    + target_file
                )

            document = documents[target_file]
            file_contract = canonical_files[target_file]
            shape_schema = file_contract.get(
                "shape_schema"
            )
            if not isinstance(shape_schema, Mapping):
                shape_schema = {}

            try:
                target_template = _nested_get(
                    document,
                    target_path,
                )
            except KeyError:
                target_template = None

            target_schema = _schema_at_path(
                shape_schema,
                target_path,
            )
            canonical_item = (
                _canonical_item_for_target(
                    profile,
                    target_file,
                    target_path,
                )
            )

            if (
                field == "handoffs"
                and target_file
                == "model_answer.json"
                and target_path
                == "$.routing_aliases"
            ):
                rendered_handoffs = _render_handoffs(
                    source_value,
                    target_template,
                    target_schema,
                )
                current = target_template
                if (
                    isinstance(current, list)
                    and isinstance(
                        rendered_handoffs,
                        list,
                    )
                ):
                    combined: list[Any] = []
                    for item in [
                        *current,
                        *rendered_handoffs,
                    ]:
                        if item not in combined:
                            combined.append(item)
                    rendered = _coerce_to_schema(
                        combined,
                        target_schema,
                        target_template,
                    )
                else:
                    rendered = rendered_handoffs

            elif mode == "PROFILE_SCHEMA":
                rendered = _render_typed_records(
                    source_value,
                    target_template=target_template,
                    target_schema=target_schema,
                    canonical_item=canonical_item,
                )

            elif mode == "RENDERED":
                if field == "handoffs":
                    rendered = _render_handoffs(
                        source_value,
                        target_template,
                        target_schema,
                    )
                else:
                    rendered = _render_typed_records(
                        source_value,
                        target_template=target_template,
                        target_schema=target_schema,
                        canonical_item=canonical_item,
                    )

            elif mode in {
                "EXACT",
                "PROFILE",
                "FIXED",
            }:
                rendered = _coerce_to_schema(
                    source_value,
                    target_schema,
                    target_template,
                )

            else:
                raise ValueError(
                    f"unsupported projection mode: {mode}"
                )

            documents[target_file] = _nested_set(
                document,
                target_path,
                rendered,
            )

    rendered_files = {
        "README.md": _render_readme(spec)
    }
    for file_name, document in documents.items():
        rendered_files[file_name] = (
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )

    return {
        name: rendered_files[name]
        for name in SOURCE_FILES
    }


def validate_rendered_topic(
    topic_dir: Path,
    profile: Mapping[str, Any],
) -> list[ContractIssue]:
    issues: list[ContractIssue] = []
    actual_files = sorted(
        path.name
        for path in topic_dir.iterdir()
        if path.is_file()
    ) if topic_dir.is_dir() else []
    if actual_files != sorted(SOURCE_FILES):
        issues.append(
            _issue(
                "TP010_FOCUSED_VALIDATION_FAILED",
                "$",
                f"rendered source file set mismatch: {actual_files}",
            )
        )
        return issues

    canonical_files = profile.get("canonical_files")
    canonical_items = profile.get("canonical_items")
    if not isinstance(canonical_files, Mapping):
        canonical_files = {}
    if not isinstance(canonical_items, Mapping):
        canonical_items = {}

    documents: dict[str, Any] = {}
    for file_name, contract in canonical_files.items():
        path = topic_dir / str(file_name)
        try:
            document = load_json(path)
        except Exception as error:
            issues.append(
                _issue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    f"$.{file_name}",
                    f"cannot parse rendered JSON: {type(error).__name__}: {error}",
                )
            )
            continue
        documents[str(file_name)] = document
        if not isinstance(contract, Mapping):
            continue
        schema = contract.get("shape_schema")
        if isinstance(schema, Mapping):
            issues.extend(
                validate_against_schema(
                    document,
                    schema,
                    code="TP008_RENDER_SCHEMA_INVALID",
                    path=f"$.{file_name}",
                )
            )
        required_keys = contract.get("required_top_level_keys")
        if isinstance(required_keys, list) and isinstance(document, Mapping):
            missing = [key for key in required_keys if key not in document]
            if missing:
                issues.append(
                    _issue(
                        "TP008_RENDER_SCHEMA_INVALID",
                        f"$.{file_name}",
                        "missing required top-level keys: "
                        + ",".join(map(str, missing)),
                    )
                )

    for logical_name, item_contract in canonical_items.items():
        if not isinstance(item_contract, Mapping):
            continue
        file_name = item_contract.get("target_file")
        target_path = item_contract.get("target_path")
        item_schema = item_contract.get("item_schema")
        if (
            not isinstance(file_name, str)
            or not isinstance(target_path, str)
            or not isinstance(item_schema, Mapping)
            or file_name not in documents
        ):
            continue
        try:
            values = _nested_get(documents[file_name], target_path)
        except KeyError:
            issues.append(
                _issue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    f"$.canonical_items.{logical_name}",
                    f"rendered target path is missing: {file_name} {target_path}",
                )
            )
            continue
        if not isinstance(values, list):
            issues.append(
                _issue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    f"$.canonical_items.{logical_name}",
                    "canonical item target must be an array",
                )
            )
            continue
        for index, item in enumerate(values):
            issues.extend(
                validate_against_schema(
                    item,
                    item_schema,
                    code="TP008_RENDER_SCHEMA_INVALID",
                    path=f"$.canonical_items.{logical_name}[{index}]",
                )
            )

    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in sorted(topic_dir.iterdir())
        if path.is_file()
    )
    for forbidden in sorted(FORBIDDEN_RUNTIME_KEYS):
        if re.search(rf'["\']{re.escape(forbidden)}["\']\s*:', combined):
            issues.append(
                _issue(
                    "TP009_FORBIDDEN_RESIDUE",
                    "$",
                    f"rendered source contains forbidden runtime key: {forbidden}",
                )
            )
    return issues


def _write_rendered_files(
    topic_dir: Path,
    rendered_files: Mapping[str, str],
) -> None:
    topic_dir.mkdir(parents=True, exist_ok=False)
    for file_name in SOURCE_FILES:
        (topic_dir / file_name).write_text(
            rendered_files[file_name],
            encoding="utf-8",
        )


def _fsync_tree(root: Path) -> None:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            with path.open("rb") as file_obj:
                os.fsync(file_obj.fileno())
    directory_fd = os.open(root, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def _atomic_install(
    staged_topic_dir: Path,
    target_topic_dir: Path,
    *,
    fail_after_rename: bool = False,
) -> None:
    if target_topic_dir.exists():
        raise FileExistsError(f"target topic already exists: {target_topic_dir}")

    target_topic_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary_target = Path(
        tempfile.mkdtemp(
            prefix=f".{target_topic_dir.name}.stage17d.",
            dir=target_topic_dir.parent,
        )
    )
    renamed = False
    try:
        for source in staged_topic_dir.iterdir():
            if source.is_file():
                shutil.copy2(source, temporary_target / source.name)
        _fsync_tree(temporary_target)
        os.replace(temporary_target, target_topic_dir)
        renamed = True
        if fail_after_rename:
            raise RuntimeError("injected failure after atomic rename")
    except Exception:
        if renamed and target_topic_dir.exists():
            shutil.rmtree(target_topic_dir)
        elif temporary_target.exists():
            shutil.rmtree(temporary_target)
        raise


def build_spec(
    spec: Mapping[str, Any],
    profile: Mapping[str, Any],
    *,
    output_root: Path,
    topic_root: Path = TOPIC_ROOT,
    install: bool = False,
    fail_after_rename: bool = False,
) -> dict[str, Any]:
    plan = plan_spec(spec, profile, topic_root=topic_root)
    if plan["result"] != "PASS":
        plan["command"] = "build"
        plan["repository_mutation"] = False
        return plan

    topic_id = str(spec.get("topic_id") or "")
    profile_id = str(spec.get("profile_id") or "")
    staged_topic_dir = output_root / topic_id
    issues: list[ContractIssue] = []

    if staged_topic_dir.exists():
        issues.append(
            _issue(
                "TP011_SCOPE_VIOLATION",
                "$.output_root",
                f"staged topic directory already exists: {staged_topic_dir}",
            )
        )
        return _result(
            passed=False,
            command="build",
            topic_id=topic_id,
            profile_id=profile_id,
            issues=issues,
            staged_topic_dir=staged_topic_dir.as_posix(),
            installed=False,
            repository_mutation=False,
        )

    try:
        rendered_files = render_topic(spec, profile)
        output_root.mkdir(parents=True, exist_ok=True)
        _write_rendered_files(staged_topic_dir, rendered_files)
        issues.extend(validate_rendered_topic(staged_topic_dir, profile))
    except Exception as error:
        if staged_topic_dir.exists():
            shutil.rmtree(staged_topic_dir)
        issues.append(
            _issue(
                "TP010_FOCUSED_VALIDATION_FAILED",
                "$",
                f"render/build failed: {type(error).__name__}: {error}",
            )
        )

    if issues:
        return _result(
            passed=False,
            command="build",
            topic_id=topic_id,
            profile_id=profile_id,
            issues=issues,
            staged_topic_dir=staged_topic_dir.as_posix(),
            installed=False,
            repository_mutation=False,
        )

    installed = False
    target_topic_dir = topic_root / topic_id
    if install:
        try:
            _atomic_install(
                staged_topic_dir,
                target_topic_dir,
                fail_after_rename=fail_after_rename,
            )
            installed = True
        except Exception as error:
            issues.append(
                _issue(
                    "TP012_ATOMIC_INSTALL_FAILED",
                    "$.topic_id",
                    f"atomic install failed: {type(error).__name__}: {error}",
                )
            )

    return _result(
        passed=not issues,
        command="build",
        topic_id=topic_id,
        profile_id=profile_id,
        issues=issues,
        staged_topic_dir=staged_topic_dir.as_posix(),
        rendered_files=list(SOURCE_FILES),
        rendered_file_count=len(SOURCE_FILES),
        installed=installed,
        installed_topic_dir=target_topic_dir.as_posix() if installed else "",
        repository_mutation=installed,
        install_requested=install,
        atomic_install_strategy="SAME_FILESYSTEM_TEMP_DIRECTORY_RENAME",
        runtime_donor_dependency=False,
    )


def build_topic(
    spec_path: Path,
    *,
    output_root: Path,
    topic_root: Path = TOPIC_ROOT,
    install: bool = False,
    fail_after_rename: bool = False,
) -> dict[str, Any]:
    spec, issues = _load_spec(spec_path)
    if spec is None:
        return _result(
            passed=False,
            command="build",
            issues=issues,
            installed=False,
            repository_mutation=False,
        )
    profile, profile_issues = _load_profile_for_spec(spec)
    if profile is None:
        return _result(
            passed=False,
            command="build",
            topic_id=str(spec.get("topic_id") or ""),
            profile_id=str(spec.get("profile_id") or ""),
            issues=profile_issues,
            installed=False,
            repository_mutation=False,
        )
    return build_spec(
        spec,
        profile,
        output_root=output_root,
        topic_root=topic_root,
        install=install,
        fail_after_rename=fail_after_rename,
    )



RELEASE_ENTRYPOINT = (
    REPO_ROOT / "scripts" / "validate_topic_pack_release.py"
)
RELEASE_OUTPUT_ROOTS = ("calibration", "docs", "reports", "rubrics")
TOPIC_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def _git_run(
    repo_root: Path,
    *arguments: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def _git_status_rows(repo_root: Path) -> list[tuple[str, str]]:
    completed = subprocess.run(
        [
            "git",
            "status",
            "--porcelain=v1",
            "-z",
            "--untracked-files=all",
        ],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "git status failed: "
            + completed.stderr.decode(
                "utf-8",
                errors="replace",
            )
        )

    entries = completed.stdout.decode(
        "utf-8",
        errors="surrogateescape",
    ).split("\0")
    rows: list[tuple[str, str]] = []
    index = 0

    while index < len(entries):
        entry = entries[index]
        index += 1
        if not entry:
            continue
        code = entry[:2]
        path = entry[3:]
        if code[0] in {"R", "C"}:
            path = entries[index]
            index += 1
        rows.append((code, path))

    return rows


def _tracked_snapshot(
    repo_root: Path,
) -> dict[str, tuple[bytes, int]]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "git ls-files failed: "
            + completed.stderr.decode(
                "utf-8",
                errors="replace",
            )
        )

    paths = completed.stdout.decode(
        "utf-8",
        errors="surrogateescape",
    ).split("\0")
    snapshot: dict[str, tuple[bytes, int]] = {}

    for relative in paths:
        if not relative:
            continue
        path = repo_root / relative
        snapshot[relative] = (
            path.read_bytes(),
            path.stat().st_mode & 0o777,
        )

    return snapshot


def _release_failure_code(output: str) -> str:
    folded = output.casefold()
    if "projection" in folded or "mismatch" in folded:
        return "TP014_PROJECTION_MISMATCH"
    if (
        "generated" in folded
        or "rebuild" in folded
        or "rubric_manager" in folded
    ):
        return "TP013_GENERATED_REBUILD_FAILED"
    return "TP015_RELEASE_VALIDATION_FAILED"


def _release_argv(entrypoint: Path, topic_id: str) -> list[str]:
    if entrypoint.suffix == ".py":
        return [
            sys.executable,
            entrypoint.as_posix(),
            "--topic-id",
            topic_id,
            "--promote-generated",
        ]
    return [
        "bash",
        entrypoint.as_posix(),
        "--topic-id",
        topic_id,
    ]


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.is_dir():
        shutil.rmtree(path)


def _cleanup_empty_parents(
    path: Path,
    *,
    stop: Path,
) -> None:
    current = path.parent
    while current != stop and stop in current.parents:
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent


def _rollback_release(
    *,
    repo_root: Path,
    topic_dir: Path,
    tracked_before: Mapping[str, tuple[bytes, int]],
    untracked_before: set[str],
    fail_rollback: bool = False,
) -> tuple[bool, list[str]]:
    if fail_rollback:
        raise RuntimeError("injected release rollback failure")

    restored: list[str] = []
    current_status = _git_status_rows(repo_root)
    current_untracked = {
        path
        for code, path in current_status
        if code == "??"
    }

    for relative, (payload, mode) in tracked_before.items():
        path = repo_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != payload:
            path.write_bytes(payload)
            restored.append(relative)
        os.chmod(path, mode)

    for relative in sorted(
        current_untracked - untracked_before,
        key=lambda value: (
            len(Path(value).parts),
            value,
        ),
        reverse=True,
    ):
        path = repo_root / relative
        if path.exists() or path.is_symlink():
            _remove_path(path)
            restored.append(relative)
            _cleanup_empty_parents(path, stop=repo_root)

    if topic_dir.exists():
        _remove_path(topic_dir)
        restored.append(
            topic_dir.relative_to(repo_root).as_posix()
        )

    after_status = _git_status_rows(repo_root)
    tracked_dirty_after = [
        (code, path)
        for code, path in after_status
        if code != "??"
    ]
    after_untracked = {
        path
        for code, path in after_status
        if code == "??"
    }
    source_prefix = (
        topic_dir.relative_to(repo_root).as_posix()
        + "/"
    )
    expected_untracked = {
        path
        for path in untracked_before
        if not path.startswith(source_prefix)
    }

    passed = all([
        not tracked_dirty_after,
        after_untracked == expected_untracked,
        not topic_dir.exists(),
    ])
    return passed, sorted(set(restored))


def release_topic(
    topic_id: str,
    *,
    repo_root: Path = REPO_ROOT,
    release_entrypoint: Path | None = None,
    runner: Any = subprocess.run,
    fail_rollback: bool = False,
) -> dict[str, Any]:
    topic_root = repo_root / "rubrics" / "topic_packs"
    topic_dir = topic_root / topic_id
    entrypoint = (
        release_entrypoint
        if release_entrypoint is not None
        else repo_root / "scripts" / "validate_topic_pack_release.py"
    )

    issues: list[ContractIssue] = []
    if TOPIC_ID_PATTERN.fullmatch(topic_id) is None:
        issues.append(
            _issue(
                "TP015_RELEASE_VALIDATION_FAILED",
                "$.topic_id",
                "topic_id must match ^[a-z0-9]+(?:_[a-z0-9]+)*$",
            )
        )
    elif not topic_dir.is_dir():
        issues.append(
            _issue(
                "TP015_RELEASE_VALIDATION_FAILED",
                "$.topic_id",
                f"topic source directory does not exist: {topic_dir}",
            )
        )
    else:
        actual_files = sorted(
            path.name
            for path in topic_dir.iterdir()
            if path.is_file()
        )
        if actual_files != sorted(SOURCE_FILES):
            issues.append(
                _issue(
                    "TP015_RELEASE_VALIDATION_FAILED",
                    "$.topic_id",
                    "topic source directory must contain exactly "
                    + ", ".join(SOURCE_FILES),
                )
            )

    if issues:
        return _result(
            passed=False,
            command="release",
            topic_id=topic_id,
            issues=issues,
            repository_mutation=False,
            release_entrypoint=entrypoint.as_posix(),
            adapter_topic_option="--topic",
            entrypoint_topic_option="--topic-id",
            release_exit_code=None,
            rollback_performed=False,
            rollback_pass=None,
            source_removed_on_failure=False,
            runtime_donor_dependency=False,
        )

    try:
        status_before = _git_status_rows(repo_root)
        tracked_before = _tracked_snapshot(repo_root)
    except Exception as error:
        issues.append(
            _issue(
                "TP015_RELEASE_VALIDATION_FAILED",
                "$",
                f"cannot capture release prestate: "
                f"{type(error).__name__}: {error}",
            )
        )
        return _result(
            passed=False,
            command="release",
            topic_id=topic_id,
            issues=issues,
            repository_mutation=False,
            release_entrypoint=entrypoint.as_posix(),
            adapter_topic_option="--topic",
            entrypoint_topic_option="--topic-id",
            release_exit_code=None,
            rollback_performed=False,
            rollback_pass=None,
            source_removed_on_failure=False,
            runtime_donor_dependency=False,
        )

    tracked_dirty_before = [
        (code, path)
        for code, path in status_before
        if code != "??"
    ]
    untracked_before = {
        path
        for code, path in status_before
        if code == "??"
    }
    topic_prefix = (
        topic_dir.relative_to(repo_root).as_posix()
        + "/"
    )
    expected_source_paths = {
        topic_prefix + file_name
        for file_name in SOURCE_FILES
    }

    if tracked_dirty_before:
        issues.append(
            _issue(
                "TP016_LEGACY_MUTATION_FORBIDDEN",
                "$",
                "release requires a clean tracked worktree",
            )
        )
    elif not expected_source_paths.issubset(
        untracked_before
    ):
        issues.append(
            _issue(
                "TP016_LEGACY_MUTATION_FORBIDDEN",
                "$.topic_id",
                "release adapter only accepts a newly installed "
                "untracked compiler-managed topic",
            )
        )
    elif not entrypoint.is_file():
        issues.append(
            _issue(
                "TP015_RELEASE_VALIDATION_FAILED",
                "$.release_entrypoint",
                f"release entrypoint does not exist: {entrypoint}",
            )
        )

    if issues:
        return _result(
            passed=False,
            command="release",
            topic_id=topic_id,
            issues=issues,
            repository_mutation=False,
            release_entrypoint=entrypoint.as_posix(),
            adapter_topic_option="--topic",
            entrypoint_topic_option="--topic-id",
            release_exit_code=None,
            rollback_performed=False,
            rollback_pass=None,
            source_removed_on_failure=False,
            runtime_donor_dependency=False,
        )

    argv = _release_argv(entrypoint, topic_id)
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    try:
        completed = runner(
            argv,
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            env=environment,
        )
        release_exit_code = int(completed.returncode)
        release_output = str(completed.stdout or "")
    except Exception as error:
        release_exit_code = 1
        release_output = (
            f"release invocation failed: "
            f"{type(error).__name__}: {error}"
        )

    status_after = _git_status_rows(repo_root)
    tracked_dirty_after = [
        path
        for code, path in status_after
        if code != "??"
    ]
    untracked_after = {
        path
        for code, path in status_after
        if code == "??"
    }
    changed_tracked_paths = sorted(
        set(tracked_dirty_after)
    )
    new_untracked_paths = sorted(
        untracked_after - untracked_before
    )
    legacy_mutation_paths = sorted(
        path
        for path in changed_tracked_paths
        if path.startswith("rubrics/topic_packs/")
        and not path.startswith(topic_prefix)
    )
    scope_violation_paths = sorted(
        path
        for path in (
            changed_tracked_paths + new_untracked_paths
        )
        if not path.startswith(RELEASE_OUTPUT_ROOTS)
    )

    if release_exit_code != 0:
        issues.append(
            _issue(
                _release_failure_code(release_output),
                "$.release_entrypoint",
                "targeted release failed with exit code "
                f"{release_exit_code}: "
                + release_output.strip()[-2000:],
            )
        )
    if legacy_mutation_paths:
        issues.append(
            _issue(
                "TP016_LEGACY_MUTATION_FORBIDDEN",
                "$.release_scope",
                "release changed legacy topic source paths: "
                + ", ".join(legacy_mutation_paths),
            )
        )
    if scope_violation_paths:
        issues.append(
            _issue(
                "TP016_LEGACY_MUTATION_FORBIDDEN",
                "$.release_scope",
                "release changed paths outside calibration/docs/"
                "reports/rubrics: "
                + ", ".join(scope_violation_paths),
            )
        )

    if not issues:
        return _result(
            passed=True,
            command="release",
            topic_id=topic_id,
            issues=(),
            repository_mutation=bool(
                changed_tracked_paths
                or new_untracked_paths
            ),
            release_entrypoint=entrypoint.as_posix(),
            release_argv=argv,
            adapter_topic_option="--topic",
            entrypoint_topic_option="--topic-id",
            release_exit_code=release_exit_code,
            changed_tracked_paths=changed_tracked_paths,
            new_untracked_paths=new_untracked_paths,
            legacy_mutation_paths=[],
            rollback_performed=False,
            rollback_pass=None,
            source_removed_on_failure=False,
            runtime_donor_dependency=False,
        )

    rollback_performed = True
    rollback_pass = False
    restored_paths: list[str] = []
    rollback_error = ""

    try:
        rollback_pass, restored_paths = _rollback_release(
            repo_root=repo_root,
            topic_dir=topic_dir,
            tracked_before=tracked_before,
            untracked_before=untracked_before,
            fail_rollback=fail_rollback,
        )
    except Exception as error:
        rollback_error = (
            f"{type(error).__name__}: {error}"
        )

    if not rollback_pass:
        issues.append(
            _issue(
                "TP016_LEGACY_MUTATION_FORBIDDEN",
                "$.rollback",
                "release rollback failed"
                + (
                    f": {rollback_error}"
                    if rollback_error
                    else ""
                ),
            )
        )

    return _result(
        passed=False,
        command="release",
        topic_id=topic_id,
        issues=issues,
        repository_mutation=(
            False if rollback_pass else "ROLLBACK_FAILED"
        ),
        release_entrypoint=entrypoint.as_posix(),
        release_argv=argv,
        adapter_topic_option="--topic",
        entrypoint_topic_option="--topic-id",
        release_exit_code=release_exit_code,
        changed_tracked_paths=changed_tracked_paths,
        new_untracked_paths=new_untracked_paths,
        legacy_mutation_paths=legacy_mutation_paths,
        rollback_performed=rollback_performed,
        rollback_pass=rollback_pass,
        rollback_restored_paths=restored_paths,
        source_removed_on_failure=(
            rollback_pass and not topic_dir.exists()
        ),
        runtime_donor_dependency=False,
    )



def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Plan and build compiler-managed Topic Packs from "
            "technical-content specifications."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser(
        "plan",
        help="validate a Topic Spec without repository mutation",
    )
    plan_parser.add_argument("--spec", required=True, type=Path)
    plan_parser.add_argument("--json", action="store_true")

    build_parser = subparsers.add_parser(
        "build",
        help="render a Topic Pack to /tmp and optionally install it",
    )
    build_parser.add_argument("--spec", required=True, type=Path)
    build_parser.add_argument("--output-root", type=Path, default=None)
    build_parser.add_argument(
        "--install",
        action="store_true",
        help="atomically install the new topic into rubrics/topic_packs",
    )
    build_parser.add_argument("--json", action="store_true")

    release_parser = subparsers.add_parser(
        "release",
        help=(
            "run the existing targeted release entrypoint for a "
            "new compiler-managed topic"
        ),
    )
    release_parser.add_argument("--topic", required=True)
    release_parser.add_argument("--json", action="store_true")
    return parser


def _print_result(payload: Mapping[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return

    print(f"RESULT={payload.get('result')}")
    print(f"COMMAND={payload.get('command')}")
    print(f"TOPIC_ID={payload.get('topic_id') or 'NONE'}")
    print(f"PROFILE_ID={payload.get('profile_id') or 'NONE'}")
    print(f"ISSUE_COUNT={payload.get('issue_count', 0)}")
    if payload.get("command") == "build":
        print(f"STAGED_TOPIC_DIR={payload.get('staged_topic_dir') or 'NONE'}")
        print(f"INSTALLED={'YES' if payload.get('installed') else 'NO'}")
    if payload.get("command") == "release":
        print(
            "RELEASE_EXIT_CODE="
            f"{payload.get('release_exit_code')}"
        )
        print(
            "ROLLBACK_PERFORMED="
            f"{'YES' if payload.get('rollback_performed') else 'NO'}"
        )
        rollback_pass = payload.get("rollback_pass")
        print(
            "ROLLBACK_PASS="
            + (
                "N/A"
                if rollback_pass is None
                else ("YES" if rollback_pass else "NO")
            )
        )
    issues = payload.get("issues")
    if isinstance(issues, list) and issues:
        for issue in issues:
            if isinstance(issue, Mapping):
                print(
                    "ISSUE="
                    f"{issue.get('error_code')}\t"
                    f"{issue.get('path')}\t"
                    f"{issue.get('message')}"
                )


def main(argv: Sequence[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command == "plan":
        payload = plan_topic(args.spec)
        _print_result(payload, as_json=args.json)
        return 0 if payload["result"] == "PASS" else 2

    if args.command == "release":
        payload = release_topic(args.topic)
        _print_result(payload, as_json=args.json)
        return 0 if payload["result"] == "PASS" else 2

    output_root = args.output_root
    if output_root is None:
        output_root = Path(
            tempfile.mkdtemp(
                prefix="topic_pack_build_",
                dir="/tmp",
            )
        )
    payload = build_topic(
        args.spec,
        output_root=output_root,
        install=args.install,
    )
    _print_result(payload, as_json=args.json)
    return 0 if payload["result"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
