from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC_SCHEMA_PATH = REPO_ROOT / "schemas" / "topic_pack_spec.schema.json"
PROFILE_SCHEMA_PATH = REPO_ROOT / "schemas" / "topic_pack_profile.schema.json"
PROFILE_ROOT = REPO_ROOT / "rubrics" / "topic_profiles"
TOPIC_ROOT = REPO_ROOT / "rubrics" / "topic_packs"

SOURCE_FILES = (
    "README.md",
    "fact_anchor.json",
    "logic_check.json",
    "model_answer.json",
    "topic_importance.json",
)

COUNT_FIELDS = (
    "anchors",
    "fatal_wrong_claims",
    "major_checks",
    "question_patterns",
    "recommended_outline",
    "routing_aliases",
    "high_band_unlock_conditions",
    "revision_notes",
)

FIXED_FINDING_FIELDS = (
    "candidate_id",
    "rule_id",
    "severity",
    "message",
    "correct_rule",
)

ERROR_CODES: Mapping[str, str] = {
    "TP001_SPEC_SCHEMA_INVALID": "spec JSON does not match canonical schema",
    "TP002_PROFILE_NOT_FOUND": "profile_id does not resolve or does not match the spec",
    "TP003_TOPIC_ID_COLLISION": "target topic already exists",
    "TP004_COUNT_MISMATCH": "declared and actual content counts differ",
    "TP005_ANCHOR_REFERENCE_INVALID": "anchor identifiers are duplicated or unresolved",
    "TP006_HANDOFF_DESTINATION_INVALID": "typed handoff destination does not exist",
    "TP007_ALIAS_COLLISION": "routing alias conflicts with an existing topic",
    "TP008_RENDER_SCHEMA_INVALID": "profile or rendered source violates its schema",
    "TP009_FORBIDDEN_RESIDUE": "unapproved donor or topic reference remains",
    "TP010_FOCUSED_VALIDATION_FAILED": "generic source validator failed",
    "TP011_SCOPE_VIOLATION": "mutation escaped planned paths",
    "TP012_ATOMIC_INSTALL_FAILED": "atomic install or rollback failed",
    "TP013_GENERATED_REBUILD_FAILED": "generated banks were not rebuilt",
    "TP014_PROJECTION_MISMATCH": "source and generated projection differ",
    "TP015_RELEASE_VALIDATION_FAILED": "release validation failed",
    "TP016_LEGACY_MUTATION_FORBIDDEN": "compiler attempted to rewrite a legacy topic",
}


@dataclass(frozen=True)
class ContractIssue:
    code: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "error_code": self.code,
            "path": self.path,
            "message": self.message,
        }


class TopicPackContractError(ValueError):
    def __init__(self, issues: Sequence[ContractIssue]) -> None:
        self.issues = tuple(issues)
        super().__init__(
            "; ".join(
                f"{issue.code} {issue.path}: {issue.message}"
                for issue in self.issues
            )
        )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_profile(
    profile_id: str,
    *,
    profile_root: Path = PROFILE_ROOT,
) -> dict[str, Any]:
    path = profile_root / f"{profile_id}.json"
    if not path.is_file():
        raise TopicPackContractError(
            [
                ContractIssue(
                    "TP002_PROFILE_NOT_FOUND",
                    "$.profile_id",
                    f"profile does not exist: {path}",
                )
            ]
        )
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise TopicPackContractError(
            [
                ContractIssue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    "$",
                    "profile root must be an object",
                )
            ]
        )
    return payload


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _resolve_ref(
    root_schema: Mapping[str, Any],
    reference: str,
) -> Mapping[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"only local refs are supported: {reference}")
    current: Any = root_schema
    for token in reference[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, Mapping) or token not in current:
            raise KeyError(reference)
        current = current[token]
    if not isinstance(current, Mapping):
        raise TypeError(f"schema ref is not an object: {reference}")
    return current


def _validate_node(
    value: Any,
    schema: Mapping[str, Any],
    root_schema: Mapping[str, Any],
    path: str,
    code: str,
    issues: list[ContractIssue],
) -> None:
    if "$ref" in schema:
        try:
            resolved = _resolve_ref(root_schema, str(schema["$ref"]))
        except Exception as error:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"invalid schema reference {schema['$ref']!r}: {error}",
                )
            )
            return
        _validate_node(value, resolved, root_schema, path, code, issues)
        return

    for branch in schema.get("allOf", []):
        if isinstance(branch, Mapping):
            _validate_node(value, branch, root_schema, path, code, issues)

    any_of = schema.get("anyOf")
    if isinstance(any_of, list):
        matches = 0
        for branch in any_of:
            branch_issues: list[ContractIssue] = []
            if isinstance(branch, Mapping):
                _validate_node(
                    value,
                    branch,
                    root_schema,
                    path,
                    code,
                    branch_issues,
                )
            if not branch_issues:
                matches += 1
        if matches == 0:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    "value does not satisfy any allowed schema variant",
                )
            )
            return

    one_of = schema.get("oneOf")
    if isinstance(one_of, list):
        matches = 0
        for branch in one_of:
            branch_issues: list[ContractIssue] = []
            if isinstance(branch, Mapping):
                _validate_node(
                    value,
                    branch,
                    root_schema,
                    path,
                    code,
                    branch_issues,
                )
            if not branch_issues:
                matches += 1
        if matches != 1:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"value must satisfy one variant; matched {matches}",
                )
            )
            return

    expected_type = schema.get("type")
    if isinstance(expected_type, str):
        if not _json_type_matches(value, expected_type):
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"expected {expected_type}, got {type(value).__name__}",
                )
            )
            return
    elif isinstance(expected_type, list):
        if not any(
            isinstance(item, str)
            and _json_type_matches(value, item)
            for item in expected_type
        ):
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"value does not match allowed types {expected_type}",
                )
            )
            return

    if "const" in schema and value != schema["const"]:
        issues.append(
            ContractIssue(
                code,
                path,
                f"expected constant {schema['const']!r}",
            )
        )

    enum_values = schema.get("enum")
    if isinstance(enum_values, list) and value not in enum_values:
        issues.append(
            ContractIssue(
                code,
                path,
                f"value is not one of {enum_values!r}",
            )
        )

    if isinstance(value, str):
        minimum = schema.get("minLength")
        maximum = schema.get("maxLength")
        pattern = schema.get("pattern")
        if isinstance(minimum, int) and len(value) < minimum:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"string length {len(value)} is below {minimum}",
                )
            )
        if isinstance(maximum, int) and len(value) > maximum:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"string length {len(value)} exceeds {maximum}",
                )
            )
        if isinstance(pattern, str) and re.fullmatch(pattern, value) is None:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"value does not match pattern {pattern!r}",
                )
            )

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if isinstance(minimum, (int, float)) and value < minimum:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"value {value} is below minimum {minimum}",
                )
            )
        if isinstance(maximum, (int, float)) and value > maximum:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"value {value} exceeds maximum {maximum}",
                )
            )

    if isinstance(value, list):
        minimum = schema.get("minItems")
        maximum = schema.get("maxItems")
        if isinstance(minimum, int) and len(value) < minimum:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"array length {len(value)} is below {minimum}",
                )
            )
        if isinstance(maximum, int) and len(value) > maximum:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"array length {len(value)} exceeds {maximum}",
                )
            )
        if schema.get("uniqueItems") is True:
            encoded = [
                json.dumps(
                    item,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                for item in value
            ]
            if len(encoded) != len(set(encoded)):
                issues.append(
                    ContractIssue(code, path, "array items must be unique")
                )
        items_schema = schema.get("items")
        if isinstance(items_schema, Mapping):
            for index, item in enumerate(value):
                _validate_node(
                    item,
                    items_schema,
                    root_schema,
                    f"{path}[{index}]",
                    code,
                    issues,
                )

    if isinstance(value, dict):
        required = schema.get("required")
        if isinstance(required, list):
            for key in required:
                if key not in value:
                    issues.append(
                        ContractIssue(
                            code,
                            f"{path}.{key}",
                            "required property is missing",
                        )
                    )

        minimum = schema.get("minProperties")
        if isinstance(minimum, int) and len(value) < minimum:
            issues.append(
                ContractIssue(
                    code,
                    path,
                    f"object property count {len(value)} is below {minimum}",
                )
            )

        properties = schema.get("properties")
        if not isinstance(properties, Mapping):
            properties = {}

        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in properties and isinstance(properties[key], Mapping):
                _validate_node(
                    child,
                    properties[key],
                    root_schema,
                    child_path,
                    code,
                    issues,
                )
                continue

            additional = schema.get("additionalProperties", True)
            if additional is False:
                issues.append(
                    ContractIssue(
                        code,
                        child_path,
                        "additional property is not allowed",
                    )
                )
            elif isinstance(additional, Mapping):
                _validate_node(
                    child,
                    additional,
                    root_schema,
                    child_path,
                    code,
                    issues,
                )


def validate_against_schema(
    value: Any,
    schema: Mapping[str, Any],
    *,
    code: str,
    path: str = "$",
) -> list[ContractIssue]:
    issues: list[ContractIssue] = []
    _validate_node(value, schema, schema, path, code, issues)
    return issues


def _duplicate_values(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def _collect_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(_collect_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(_collect_keys(child))
    return keys


def validate_profile(
    profile: Mapping[str, Any],
    *,
    profile_schema: Mapping[str, Any] | None = None,
) -> list[ContractIssue]:
    schema = (
        dict(profile_schema)
        if profile_schema is not None
        else load_json(PROFILE_SCHEMA_PATH)
    )
    issues = validate_against_schema(
        profile,
        schema,
        code="TP008_RENDER_SCHEMA_INVALID",
    )

    source_files = tuple(profile.get("source_files") or ())
    if source_files != SOURCE_FILES:
        issues.append(
            ContractIssue(
                "TP008_RENDER_SCHEMA_INVALID",
                "$.source_files",
                f"expected exact source order {SOURCE_FILES!r}",
            )
        )

    fixed_values = profile.get("fixed_values")
    if isinstance(fixed_values, Mapping):
        finding_fields = tuple(
            fixed_values.get("finding_fields") or ()
        )
        if finding_fields != FIXED_FINDING_FIELDS:
            issues.append(
                ContractIssue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    "$.fixed_values.finding_fields",
                    f"expected {FIXED_FINDING_FIELDS!r}",
                )
            )

    canonical_files = profile.get("canonical_files")
    if isinstance(canonical_files, Mapping):
        if set(canonical_files) != set(SOURCE_FILES[1:]):
            issues.append(
                ContractIssue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    "$.canonical_files",
                    "canonical files must cover four JSON source files",
                )
            )

    canonical_items = profile.get("canonical_items")
    required_items = {
        "anchors",
        "fatal_wrong_claims",
        "fatal_conditions",
        "major_checks",
        "finding_fields",
        "question_patterns",
        "recommended_outline",
        "routing_aliases",
        "high_band_unlock_conditions",
        "revision_notes",
    }
    if isinstance(canonical_items, Mapping):
        if set(canonical_items) != required_items:
            issues.append(
                ContractIssue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    "$.canonical_items",
                    "canonical item set does not match v1 profile",
                )
            )

    forbidden_keys = {
        "source_topic",
        "source_path",
        "donor_topic",
        "donor_path",
    }
    present_forbidden = _collect_keys(profile) & forbidden_keys
    if present_forbidden:
        issues.append(
            ContractIssue(
                "TP009_FORBIDDEN_RESIDUE",
                "$",
                "profile contains runtime donor keys: "
                + ",".join(sorted(present_forbidden)),
            )
        )

    policies = profile.get("policies")
    if isinstance(policies, Mapping):
        if policies.get("runtime_donor_dependency") is not False:
            issues.append(
                ContractIssue(
                    "TP009_FORBIDDEN_RESIDUE",
                    "$.policies.runtime_donor_dependency",
                    "runtime donor dependency must be false",
                )
            )
        if policies.get("new_dependency_allowed") is not False:
            issues.append(
                ContractIssue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    "$.policies.new_dependency_allowed",
                    "v1 profile must not add a runtime dependency",
                )
            )

    error_codes = profile.get("error_codes")
    if isinstance(error_codes, list):
        codes = {
            str(item.get("error_code"))
            for item in error_codes
            if isinstance(item, Mapping)
        }
        if codes != set(ERROR_CODES):
            issues.append(
                ContractIssue(
                    "TP008_RENDER_SCHEMA_INVALID",
                    "$.error_codes",
                    "profile error registry must match contract library",
                )
            )

    return issues


def _existing_alias_owner_map(
    topic_root: Path,
    *,
    excluded_topic_id: str,
) -> dict[str, str]:
    owners: dict[str, str] = {}
    if not topic_root.is_dir():
        return owners

    for topic_dir in sorted(topic_root.iterdir()):
        if not topic_dir.is_dir() or topic_dir.name == excluded_topic_id:
            continue
        model_path = topic_dir / "model_answer.json"
        if not model_path.is_file():
            continue
        try:
            model = load_json(model_path)
        except Exception:
            continue
        aliases = model.get("routing_aliases")
        if not isinstance(aliases, list):
            continue
        for alias in aliases:
            if not isinstance(alias, str):
                continue
            normalized = " ".join(alias.casefold().split())
            if normalized:
                owners.setdefault(normalized, topic_dir.name)
    return owners


def validate_spec(
    spec: Mapping[str, Any],
    profile: Mapping[str, Any],
    *,
    spec_schema: Mapping[str, Any] | None = None,
    topic_root: Path = TOPIC_ROOT,
    allow_existing_target: bool = False,
) -> list[ContractIssue]:
    schema = (
        dict(spec_schema)
        if spec_schema is not None
        else load_json(SPEC_SCHEMA_PATH)
    )
    issues = validate_against_schema(
        spec,
        schema,
        code="TP001_SPEC_SCHEMA_INVALID",
    )

    if spec.get("profile_id") != profile.get("profile_id"):
        issues.append(
            ContractIssue(
                "TP002_PROFILE_NOT_FOUND",
                "$.profile_id",
                "spec profile_id does not match loaded profile",
            )
        )
    if spec.get("question_type") != profile.get("question_type"):
        issues.append(
            ContractIssue(
                "TP002_PROFILE_NOT_FOUND",
                "$.question_type",
                "spec question_type does not match loaded profile",
            )
        )

    topic_id = str(spec.get("topic_id") or "")
    if (
        topic_id
        and not allow_existing_target
        and (topic_root / topic_id).exists()
    ):
        issues.append(
            ContractIssue(
                "TP003_TOPIC_ID_COLLISION",
                "$.topic_id",
                f"target topic already exists: {topic_id}",
            )
        )

    counts = spec.get("counts")
    if isinstance(counts, Mapping):
        for field in COUNT_FIELDS:
            expected = counts.get(field)
            actual = spec.get(field)
            if (
                isinstance(expected, int)
                and isinstance(actual, list)
                and expected != len(actual)
            ):
                issues.append(
                    ContractIssue(
                        "TP004_COUNT_MISMATCH",
                        f"$.counts.{field}",
                        f"declared {expected}, actual {len(actual)}",
                    )
                )

    anchors = spec.get("anchors")
    anchor_ids: list[str] = []
    if isinstance(anchors, list):
        anchor_ids = [
            str(item.get("id"))
            for item in anchors
            if isinstance(item, Mapping)
            and isinstance(item.get("id"), str)
        ]
        for duplicate in sorted(_duplicate_values(anchor_ids)):
            issues.append(
                ContractIssue(
                    "TP005_ANCHOR_REFERENCE_INVALID",
                    "$.anchors",
                    f"duplicate anchor id: {duplicate}",
                )
            )

    anchor_id_set = set(anchor_ids)
    for field, reference_key in (
        ("question_patterns", "required_anchor_ids"),
        ("recommended_outline", "anchor_ids"),
    ):
        records = spec.get(field)
        if not isinstance(records, list):
            continue
        for index, record in enumerate(records):
            if not isinstance(record, Mapping):
                continue
            references = record.get(reference_key)
            if not isinstance(references, list):
                continue
            for reference in references:
                if reference not in anchor_id_set:
                    issues.append(
                        ContractIssue(
                            "TP005_ANCHOR_REFERENCE_INVALID",
                            f"$.{field}[{index}].{reference_key}",
                            f"unknown anchor id: {reference}",
                        )
                    )

    for field in (
        "fatal_wrong_claims",
        "major_checks",
        "question_patterns",
    ):
        records = spec.get(field)
        if not isinstance(records, list):
            continue
        ids = [
            str(record.get("id"))
            for record in records
            if isinstance(record, Mapping)
            and isinstance(record.get("id"), str)
        ]
        for duplicate in sorted(_duplicate_values(ids)):
            issues.append(
                ContractIssue(
                    "TP005_ANCHOR_REFERENCE_INVALID",
                    f"$.{field}",
                    f"duplicate record id: {duplicate}",
                )
            )

    handoffs = spec.get("handoffs")
    if isinstance(handoffs, list):
        for index, handoff in enumerate(handoffs):
            if not isinstance(handoff, Mapping):
                continue
            destination = handoff.get("topic_id")
            if not isinstance(destination, str):
                continue
            if destination == topic_id:
                issues.append(
                    ContractIssue(
                        "TP006_HANDOFF_DESTINATION_INVALID",
                        f"$.handoffs[{index}].topic_id",
                        "handoff destination cannot be current topic",
                    )
                )
            elif not (topic_root / destination).is_dir():
                issues.append(
                    ContractIssue(
                        "TP006_HANDOFF_DESTINATION_INVALID",
                        f"$.handoffs[{index}].topic_id",
                        f"handoff destination does not exist: {destination}",
                    )
                )

    aliases = spec.get("routing_aliases")
    if isinstance(aliases, list):
        owners = _existing_alias_owner_map(
            topic_root,
            excluded_topic_id=topic_id,
        )
        for index, alias in enumerate(aliases):
            if not isinstance(alias, str):
                continue
            normalized = " ".join(alias.casefold().split())
            owner = owners.get(normalized)
            if owner:
                issues.append(
                    ContractIssue(
                        "TP007_ALIAS_COLLISION",
                        f"$.routing_aliases[{index}]",
                        f"alias is already owned by {owner}: {alias}",
                    )
                )

    return issues


def raise_for_issues(issues: Sequence[ContractIssue]) -> None:
    if issues:
        raise TopicPackContractError(issues)


def issue_codes(issues: Iterable[ContractIssue]) -> set[str]:
    return {issue.code for issue in issues}


def format_issues(issues: Iterable[ContractIssue]) -> str:
    return "\n".join(
        f"{issue.code}\t{issue.path}\t{issue.message}"
        for issue in issues
    )


def clone_json(value: Any) -> Any:
    return copy.deepcopy(value)
