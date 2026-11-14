"""Project active Logic Check references; this adapter NEVER raises a fatal itself."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]


def project_logic_rules(topic_ids: Iterable[str]) -> list[dict[str, Any]]:
    """Preserve existing enabled flags, severity and rule ownership."""
    result: list[dict[str, Any]] = []
    for topic in sorted(set(topic_ids)):
        path = ROOT / "rubrics" / "topic_packs" / topic / "logic_check.json"
        if not path.is_file():
            continue
        profile = json.loads(path.read_text(encoding="utf-8"))
        checks = profile.get("deterministic_checks")
        # A missing/disabled deterministic profile is not evidence of active
        # rules. In particular, do not fall back to top-level LLM profile
        # examples when the deterministic list is explicitly empty.
        if not isinstance(checks, dict) or not bool(checks.get("enabled", True)):
            continue
        fatal_rules = checks.get("fatal_checks") or []
        major_rules = checks.get("major_checks") or []
        if not isinstance(fatal_rules, list) or not isinstance(major_rules, list):
            continue
        rules = [*fatal_rules, *major_rules]
        seen = set()
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            rid = str(rule.get("id") or "").strip()
            if not rid or rid in seen:
                continue
            seen.add(rid)
            result.append({
                "owner_topic_id": topic,
                "rule_id": rid,
                "severity": str(rule.get("severity") or "major"),
                "source": "logic_check.json",
                "active_profile": True,
                "authority": "existing_logic_evaluator_only",
            })
    return result
