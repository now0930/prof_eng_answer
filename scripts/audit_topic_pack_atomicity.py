#!/usr/bin/env python3
"""Audit Topic Pack ownership cohesion and cross-topic contamination."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK_ROOT = ROOT / "rubrics" / "topic_packs"
DEFAULT_CLASSIFICATION = ROOT / "docs" / "topic_pack_classification.md"
TOKEN_RE = re.compile(r"[0-9a-z가-힣]+")
SPACE_RE = re.compile(r"\s+")
STOP_TOKENS = {
    "topic", "system", "control", "대한", "따라", "또는", "문제",
    "방법", "설명", "설명한다", "설명하시오", "적용", "관리", "검증",
    "기준", "고려", "위한", "으로", "에서", "통해", "한다", "있다",
}


@dataclass(frozen=True)
class AuditIssue:
    severity: str
    code: str
    topic_id: str
    message: str


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def _normalize_text(value: str) -> str:
    return SPACE_RE.sub(" ", str(value or "").casefold()).strip()


def _normalized_exact(value: str) -> str:
    return "".join(TOKEN_RE.findall(_normalize_text(value)))


def _walk_text(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from _walk_text(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_text(nested)


def _tokens(value: Any) -> set[str]:
    result: set[str] = set()
    for text in _walk_text(value):
        for token in TOKEN_RE.findall(text.casefold()):
            if len(token) > 1 and token not in STOP_TOKENS:
                result.add(token)
    return result


def _jaccard(left: Any, right: Any) -> float:
    left_tokens = _tokens(left)
    right_tokens = _tokens(right)
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / max(1, len(left_tokens | right_tokens))


def _pattern_text(pattern: Any) -> str:
    if isinstance(pattern, str):
        return pattern
    if isinstance(pattern, dict):
        return str(pattern.get("pattern") or "")
    return ""


def _anchor_statements(fact: dict[str, Any]) -> list[str]:
    result = []
    for anchor in fact.get("anchors", []):
        if isinstance(anchor, dict):
            statement = anchor.get("statement") or anchor.get("claim")
            if isinstance(statement, str) and statement.strip():
                result.append(statement)
    return result


def _truth_schema(logic: dict[str, Any]) -> list[str]:
    profile = logic.get("llm_profile")
    if not isinstance(profile, dict):
        return []
    truth = profile.get("truth_schema")
    if not isinstance(truth, list):
        return []
    return [row for row in truth if isinstance(row, str) and row.strip()]


def _question_components(patterns: list[Any]) -> list[list[int]]:
    refs = []
    for pattern in patterns:
        if not isinstance(pattern, dict):
            continue
        raw = pattern.get("required_anchor_ids")
        if isinstance(raw, list) and raw:
            refs.append({str(item) for item in raw if str(item).strip()})
    if len(refs) < 2:
        return [list(range(len(refs)))] if refs else []

    adjacency = [set() for _ in refs]
    for left in range(len(refs)):
        for right in range(left + 1, len(refs)):
            if refs[left] & refs[right]:
                adjacency[left].add(right)
                adjacency[right].add(left)

    components: list[list[int]] = []
    visited: set[int] = set()
    for start in range(len(refs)):
        if start in visited:
            continue
        component: list[int] = []
        stack = [start]
        visited.add(start)
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        components.append(sorted(component))
    return components


def _pack_documents(pack_dir: Path) -> dict[str, dict[str, Any]]:
    return {
        name: _load_json(pack_dir / name)
        for name in (
            "fact_anchor.json", "model_answer.json", "logic_check.json",
            "topic_importance.json",
        )
    }


def audit_topic_pack_inventory(
    pack_root: Path = DEFAULT_PACK_ROOT,
    *,
    classification_path: Path | None = DEFAULT_CLASSIFICATION,
    selected_topic_ids: set[str] | None = None,
) -> tuple[list[AuditIssue], dict[str, Any]]:
    all_pack_dirs = sorted(path for path in pack_root.iterdir() if path.is_dir())
    all_documents = {
        pack_dir.name: _pack_documents(pack_dir) for pack_dir in all_pack_dirs
    }
    selected = selected_topic_ids or set(all_documents)
    unknown = selected - set(all_documents)
    if unknown:
        raise ValueError(f"unknown topic_id: {', '.join(sorted(unknown))}")

    issues: list[AuditIssue] = []
    model_ids: defaultdict[str, list[str]] = defaultdict(list)
    aliases: defaultdict[str, set[str]] = defaultdict(set)
    positive_core: defaultdict[str, defaultdict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )

    for topic_id, documents in all_documents.items():
        fact = documents["fact_anchor.json"]
        model = documents["model_answer.json"]
        logic = documents["logic_check.json"]

        model_id = str(model.get("id") or "").strip()
        if model_id:
            model_ids[model_id].append(topic_id)
            if not (model_id == topic_id or model_id.startswith(f"{topic_id}_")) and topic_id in selected:
                issues.append(AuditIssue(
                    "ERROR", "MODEL_ID_OWNER_MISMATCH", topic_id,
                    f"model id {model_id!r} belongs to another owner",
                ))

        patterns = model.get("expected_question_patterns")
        if not isinstance(patterns, list):
            patterns = []
        for index, pattern in enumerate(patterns):
            if isinstance(pattern, str) and topic_id in selected:
                issues.append(AuditIssue(
                    "ERROR", "UNSCOPED_QUESTION_PATTERN", topic_id,
                    f"expected_question_patterns[{index}] has no required_anchor_ids",
                ))

        examples = model.get("question_examples")
        if isinstance(examples, list) and examples and patterns and topic_id in selected:
            alignment = _jaccard([_pattern_text(pattern) for pattern in patterns], examples)
            if alignment < 0.12:
                issues.append(AuditIssue(
                    "ERROR", "QUESTION_MIRROR_DIVERGENCE", topic_id,
                    f"expected patterns and question_examples vocabulary alignment={alignment:.3f}",
                ))

        routing_aliases = model.get("routing_aliases")
        topic_aliases = model.get("topic_aliases")
        if (
            isinstance(routing_aliases, list) and routing_aliases
            and isinstance(topic_aliases, list) and topic_aliases
            and topic_id in selected
        ):
            alignment = _jaccard(routing_aliases, topic_aliases)
            if alignment < 0.12:
                issues.append(AuditIssue(
                    "ERROR", "ALIAS_MIRROR_DIVERGENCE", topic_id,
                    f"routing_aliases and topic_aliases vocabulary alignment={alignment:.3f}",
                ))

        for alias_key in ("routing_aliases", "topic_aliases"):
            raw_aliases = model.get(alias_key)
            if not isinstance(raw_aliases, list):
                continue
            for alias in raw_aliases:
                if isinstance(alias, str):
                    normalized = _normalized_exact(alias)
                    if normalized:
                        aliases[normalized].add(topic_id)

        truth = _truth_schema(logic)
        anchor_statements = _anchor_statements(fact)
        if len(truth) >= 5 and len(anchor_statements) >= 5 and topic_id in selected:
            alignment = _jaccard(anchor_statements, truth)
            if alignment < 0.10:
                issues.append(AuditIssue(
                    "ERROR", "POSITIVE_EVIDENCE_DIVERGENCE", topic_id,
                    f"anchor statements and truth_schema vocabulary alignment={alignment:.3f}",
                ))

        for value in fact.get("core_facts", []):
            if isinstance(value, str) and len(value) >= 80:
                positive_core[_normalized_exact(value)][topic_id] += 1

        if topic_id in selected:
            anchor_count = len(fact.get("anchors", []))
            if anchor_count >= 40:
                issues.append(AuditIssue(
                    "WARN", "LARGE_ANCHOR_INVENTORY", topic_id,
                    f"{anchor_count} anchors require an ownership review",
                ))
            components = _question_components(patterns)
            if len(components) >= 3:
                issues.append(AuditIssue(
                    "WARN", "DISCONNECTED_QUESTION_FAMILIES", topic_id,
                    f"{len(components)} anchor-disconnected question families: "
                    + ", ".join(str(len(component)) for component in components),
                ))

    for model_id, owners in sorted(model_ids.items()):
        if len(set(owners)) >= 2:
            for owner in sorted(set(owners) & selected):
                issues.append(AuditIssue(
                    "ERROR", "DUPLICATE_MODEL_ID", owner,
                    f"model id {model_id!r} is shared by {', '.join(sorted(set(owners)))}",
                ))

    pair_alias_counts: Counter[tuple[str, str]] = Counter()
    for owners in aliases.values():
        ordered = sorted(owners)
        for left_index, left in enumerate(ordered):
            for right in ordered[left_index + 1:]:
                pair_alias_counts[(left, right)] += 1
    for (left, right), count in sorted(pair_alias_counts.items()):
        if count >= 2:
            for owner in ({left, right} & selected):
                issues.append(AuditIssue(
                    "WARN", "CROSS_TOPIC_ALIAS_COLLISION", owner,
                    f"{count} normalized aliases overlap with {right if owner == left else left}",
                ))

    pair_core_counts: Counter[tuple[str, str]] = Counter()
    for owners in positive_core.values():
        ordered = sorted(owners)
        for left_index, left in enumerate(ordered):
            for right in ordered[left_index + 1:]:
                pair_core_counts[(left, right)] += min(owners[left], owners[right])
    for (left, right), count in sorted(pair_core_counts.items()):
        if count >= 3:
            for owner in ({left, right} & selected):
                issues.append(AuditIssue(
                    "ERROR", "DUPLICATED_FOREIGN_CORE_FACTS", owner,
                    f"{count} long core facts are duplicated with {right if owner == left else left}",
                ))

    if classification_path is not None and classification_path.exists():
        classification = classification_path.read_text(encoding="utf-8")
        for topic_id in sorted(selected):
            if f"`{topic_id}`" not in classification:
                issues.append(AuditIssue(
                    "WARN", "CLASSIFICATION_TOPIC_MISSING", topic_id,
                    "topic_id is absent from topic_pack_classification.md",
                ))

    issues.sort(key=lambda issue: (issue.severity != "ERROR", issue.topic_id, issue.code))
    errors = sum(issue.severity == "ERROR" for issue in issues)
    warnings = sum(issue.severity == "WARN" for issue in issues)
    summary = {
        "version": "topic_pack_atomicity_audit_v1",
        "topic_count": len(all_documents),
        "selected_topic_count": len(selected),
        "error_count": errors,
        "warning_count": warnings,
        "decision": "FAIL" if errors else "PASS",
    }
    return issues, summary


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack-root", type=Path, default=DEFAULT_PACK_ROOT)
    parser.add_argument("--classification", type=Path, default=DEFAULT_CLASSIFICATION)
    parser.add_argument("--topic-id", action="append", default=[])
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--output", type=Path, help="write the JSON audit artifact")
    parser.add_argument("--strict-warnings", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        issues, summary = audit_topic_pack_inventory(
            args.pack_root,
            classification_path=args.classification,
            selected_topic_ids=set(args.topic_id) or None,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"TOPIC PACK ATOMICITY AUDIT ERROR: {exc}", file=sys.stderr)
        return 2

    payload = {"summary": summary, "issues": [asdict(issue) for issue in issues]}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if args.as_json:
        print(json.dumps(
            payload,
            ensure_ascii=False, indent=2,
        ))
    else:
        print("TOPIC PACK ATOMICITY AUDIT")
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
        for issue in issues:
            print(f"{issue.severity} {issue.code} [{issue.topic_id}] {issue.message}")

    if summary["error_count"]:
        return 1
    if args.strict_warnings and summary["warning_count"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
