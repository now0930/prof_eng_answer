#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "rubrics" / "topic_packs"

ALLOWED_SEVERITY = {"fatal", "major", "minor", "warn", "info"}
ALLOWED_IMPORTANCE = {"must", "important", "optional"}
ALLOWED_QUESTION_TYPES = {
    "DEFINE",
    "PRINCIPLE",
    "PRINCIPLE_INTERPRETATION",
    "STRUCTURE",
    "COMPARE",
    "COMPARE_SELECTION",
    "DIAGNOSIS_ACTION",
    "IMPLEMENTATION_EVALUATION",
    "PROBLEM_SOLVE",
    "CAUSE_ACTION",
    "PROCEDURE",
    "CALC_DESIGN",
    "APPLICATION",
    "EVALUATION",
    "UNKNOWN",
}
ALLOWED_DIFFICULTY = {
    "BASIC_CONCEPT",
    "FIELD_APPLICATION",
    "DESIGN_EVALUATION",
    "THEORY_CORE",
    "UNKNOWN",
}

MODEL_ANSWER_SCHEMA_VERSION = "topic_pack.model_answer.v1"
TOPIC_IMPORTANCE_SCHEMA_VERSION = "topic_pack.topic_importance.v1"

MODEL_ANSWER_REQUIRED_KEYS = {
    "schema_version",
    "topic_id",
    "title_ko",
    "question_type",
    "expected_question_patterns",
    "recommended_outline",
    "high_score_points",
    "common_missing_points",
    "routing_aliases",
    "routing_field_points",
}

MODEL_ANSWER_LEGACY_ROOT_KEYS = {
    "model_answer",
    "high_score_elements",
    "common_mistakes",
}

TOPIC_IMPORTANCE_REQUIRED_KEYS = {
    "schema_version",
    "topic_id",
    "difficulty",
    "selection_importance",
    "question_type",
    "high_band_unlock_conditions",
    "note",
}


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(1)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"{path}: invalid JSON: {e}")

    if not isinstance(data, dict):
        fail(f"{path}: root must be object")

    return data


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{label}: must be object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{label}: must be list")
    return value


def require_str(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label}: required non-empty string")
    return value


def require_keys(data: dict[str, Any], keys: set[str], label: str) -> None:
    missing = sorted(key for key in keys if key not in data)
    if missing:
        fail(f"{label}: missing required keys: {', '.join(missing)}")


def reject_keys(data: dict[str, Any], keys: set[str], label: str) -> None:
    found = sorted(key for key in keys if key in data)
    if found:
        fail(f"{label}: legacy/unsupported root keys: {', '.join(found)}")


def require_schema_version(data: dict[str, Any], expected: str, label: str) -> None:
    actual = require_str(data.get("schema_version"), f"{label}: schema_version")
    if actual != expected:
        fail(f"{label}: schema_version must be {expected}, got {actual}")


def require_str_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    items = require_list(value, label)
    if not allow_empty and not items:
        fail(f"{label}: must not be empty")

    result: list[str] = []
    for idx, item in enumerate(items):
        result.append(require_str(item, f"{label}[{idx}]"))

    return result


def validate_fact_anchor(pack_dir: Path, topic_id: str, global_anchor_ids: set[str]) -> set[str]:
    path = pack_dir / "fact_anchor.json"
    if not path.exists():
        fail(f"{pack_dir}: missing fact_anchor.json")

    data = load_json(path)

    if data.get("topic_id") != topic_id:
        fail(f"{path}: topic_id must match directory name: {topic_id}")

    anchors = require_list(data.get("anchors"), f"{path}: anchors")
    if not anchors:
        fail(f"{path}: anchors must not be empty")

    local_anchor_ids: set[str] = set()

    for idx, raw_anchor in enumerate(anchors):
        anchor = require_object(raw_anchor, f"{path}: anchors[{idx}]")
        anchor_id = require_str(anchor.get("anchor_id"), f"{path}: anchors[{idx}].anchor_id")

        if anchor_id in local_anchor_ids:
            fail(f"{path}: duplicate local anchor_id: {anchor_id}")

        if anchor_id in global_anchor_ids:
            fail(f"{path}: duplicate global anchor_id: {anchor_id}")

        local_anchor_ids.add(anchor_id)
        global_anchor_ids.add(anchor_id)

        importance = anchor.get("importance")
        if importance is not None and importance not in ALLOWED_IMPORTANCE:
            fail(f"{path}: anchor {anchor_id} invalid importance: {importance}")

        core_terms = anchor.get("core_terms")
        if core_terms is not None:
            require_list(core_terms, f"{path}: anchor {anchor_id}.core_terms")

        require_str(anchor.get("statement"), f"{path}: anchor {anchor_id}.statement")

    return local_anchor_ids


def validate_model_answer(pack_dir: Path, topic_id: str, anchor_ids: set[str]) -> None:
    path = pack_dir / "model_answer.json"
    if not path.exists():
        fail(f"{pack_dir}: missing model_answer.json")

    data = load_json(path)
    require_keys(data, MODEL_ANSWER_REQUIRED_KEYS, str(path))
    reject_keys(data, MODEL_ANSWER_LEGACY_ROOT_KEYS, str(path))
    require_schema_version(data, MODEL_ANSWER_SCHEMA_VERSION, str(path))

    if data.get("topic_id") != topic_id:
        fail(f"{path}: topic_id must match directory name: {topic_id}")

    require_str(data.get("title_ko"), f"{path}: title_ko")

    qtype = data.get("question_type")
    if qtype not in ALLOWED_QUESTION_TYPES:
        fail(f"{path}: invalid question_type: {qtype}")

    require_str_list(data.get("expected_question_patterns"), f"{path}: expected_question_patterns")
    require_str_list(data.get("high_score_points"), f"{path}: high_score_points")
    require_str_list(data.get("common_missing_points"), f"{path}: common_missing_points")
    require_str_list(data.get("routing_aliases"), f"{path}: routing_aliases")
    require_str_list(data.get("routing_field_points"), f"{path}: routing_field_points")

    outline = require_list(data.get("recommended_outline"), f"{path}: recommended_outline")
    if not outline:
        fail(f"{path}: recommended_outline must not be empty")

    for idx, raw_section in enumerate(outline):
        section = require_object(raw_section, f"{path}: recommended_outline[{idx}]")
        require_str(section.get("section"), f"{path}: recommended_outline[{idx}].section")
        require_str(section.get("intent"), f"{path}: recommended_outline[{idx}].intent")

        refs = section.get("anchor_refs", [])
        if refs is None:
            refs = []
        refs = require_list(refs, f"{path}: recommended_outline[{idx}].anchor_refs")

        for ref_idx, ref in enumerate(refs):
            ref = require_str(ref, f"{path}: recommended_outline[{idx}].anchor_refs[{ref_idx}]")
            if ref not in anchor_ids:
                fail(f"{path}: outline[{idx}] references missing anchor_id: {ref}")


def validate_topic_importance(pack_dir: Path, topic_id: str) -> None:
    path = pack_dir / "topic_importance.json"
    if not path.exists():
        fail(f"{pack_dir}: missing topic_importance.json")

    data = load_json(path)
    require_keys(data, TOPIC_IMPORTANCE_REQUIRED_KEYS, str(path))
    require_schema_version(data, TOPIC_IMPORTANCE_SCHEMA_VERSION, str(path))

    if data.get("topic_id") != topic_id:
        fail(f"{path}: topic_id must match directory name: {topic_id}")

    difficulty = data.get("difficulty")
    if difficulty not in ALLOWED_DIFFICULTY:
        fail(f"{path}: invalid difficulty: {difficulty}")

    require_str(data.get("selection_importance"), f"{path}: selection_importance")

    qtype = data.get("question_type")
    if qtype not in ALLOWED_QUESTION_TYPES:
        fail(f"{path}: invalid question_type: {qtype}")

    require_str_list(
        data.get("high_band_unlock_conditions"),
        f"{path}: high_band_unlock_conditions",
    )
    require_str(data.get("note"), f"{path}: note")


def validate_check_list(checks: Any, label: str) -> None:
    checks = require_list(checks, label)

    for idx, raw_check in enumerate(checks):
        check = require_object(raw_check, f"{label}[{idx}]")
        check_id = require_str(check.get("id", check.get("check_id")), f"{label}[{idx}].id")

        severity = check.get("severity")
        if severity is not None and severity not in ALLOWED_SEVERITY:
            fail(f"{label}: check {check_id} invalid severity: {severity}")

        if "wrong_patterns" in check:
            require_list(check.get("wrong_patterns"), f"{label}: check {check_id}.wrong_patterns")

        if "required_patterns" in check:
            require_list(check.get("required_patterns"), f"{label}: check {check_id}.required_patterns")

        if "message" in check:
            require_str(check.get("message"), f"{label}: check {check_id}.message")

        if "condition" in check:
            require_str(check.get("condition"), f"{label}: check {check_id}.condition")

        if "reason" in check:
            require_str(check.get("reason"), f"{label}: check {check_id}.reason")


def validate_logic_check(pack_dir: Path, topic_id: str) -> None:
    path = pack_dir / "logic_check.json"
    if not path.exists():
        fail(f"{pack_dir}: missing logic_check.json")

    old_path = pack_dir / "logic_check_profile.json"
    if old_path.exists():
        fail(f"{pack_dir}: old file remains. Rename/remove logic_check_profile.json and use logic_check.json")

    data = load_json(path)

    if data.get("topic_id") != topic_id:
        fail(f"{path}: topic_id must match directory name: {topic_id}")

    deterministic = require_object(
        data.get("deterministic_checks"),
        f"{path}: deterministic_checks",
    )

    llm_profile = require_object(
        data.get("llm_profile"),
        f"{path}: llm_profile",
    )

    topic_aliases = deterministic.get("topic_aliases", [])
    if topic_aliases is not None:
        require_list(topic_aliases, f"{path}: deterministic_checks.topic_aliases")

    validate_check_list(
        deterministic.get("fatal_checks", []),
        f"{path}: deterministic_checks.fatal_checks",
    )
    validate_check_list(
        deterministic.get("major_checks", []),
        f"{path}: deterministic_checks.major_checks",
    )
    validate_check_list(
        deterministic.get("question_type_checks", []),
        f"{path}: deterministic_checks.question_type_checks",
    )

    next_practice_points = deterministic.get("next_practice_points", [])
    if next_practice_points is not None:
        require_list(
            next_practice_points,
            f"{path}: deterministic_checks.next_practice_points",
        )

    de_claim_trust = deterministic.get("de_claim_trust", {})
    if de_claim_trust is not None:
        require_object(
            de_claim_trust,
            f"{path}: deterministic_checks.de_claim_trust",
        )

    truth_schema = llm_profile.get("truth_schema")
    if truth_schema is not None and not isinstance(truth_schema, (dict, list)):
        fail(f"{path}: llm_profile.truth_schema must be object or list")

    if "fatal_conditions" in llm_profile:
        require_list(
            llm_profile.get("fatal_conditions"),
            f"{path}: llm_profile.fatal_conditions",
        )

    if "safe_conditions" in llm_profile:
        require_list(
            llm_profile.get("safe_conditions"),
            f"{path}: llm_profile.safe_conditions",
        )

    if "candidate_extraction" in llm_profile:
        require_object(
            llm_profile.get("candidate_extraction"),
            f"{path}: llm_profile.candidate_extraction",
        )

    if "output_contract" in llm_profile:
        require_object(
            llm_profile.get("output_contract"),
            f"{path}: llm_profile.output_contract",
        )

    if "cap_policy" in llm_profile:
        require_object(
            llm_profile.get("cap_policy"),
            f"{path}: llm_profile.cap_policy",
        )


def validate_pack(pack_dir: Path, global_anchor_ids: set[str]) -> None:
    topic_id = pack_dir.name

    anchor_ids = validate_fact_anchor(pack_dir, topic_id, global_anchor_ids)
    validate_model_answer(pack_dir, topic_id, anchor_ids)
    validate_topic_importance(pack_dir, topic_id)
    validate_logic_check(pack_dir, topic_id)


def main() -> int:
    if not PACK_ROOT.exists():
        print("VALID: no topic_packs directory")
        return 0

    pack_dirs = sorted(p for p in PACK_ROOT.iterdir() if p.is_dir())
    global_anchor_ids: set[str] = set()

    for pack_dir in pack_dirs:
        validate_pack(pack_dir, global_anchor_ids)

    print("VALID: topic packs")
    print(f"packs: {len(pack_dirs)}")
    print(f"anchors: {len(global_anchor_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
