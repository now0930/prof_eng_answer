#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "rubrics" / "topic_packs"
OUT_DIR = ROOT / "rubrics" / "generated"

SUBJECT = "industrial_instrumentation_control"


def fail(msg: str) -> None:
    raise SystemExit(f"ERROR: {msg}")


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


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote: {path}")


def now_version() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_topic_pack(pack_dir: Path) -> dict[str, Any]:
    topic_id = pack_dir.name

    fact_anchor = load_json(pack_dir / "fact_anchor.json")
    model_answer = load_json(pack_dir / "model_answer.json")
    topic_importance = load_json(pack_dir / "topic_importance.json")
    logic_check = load_json(pack_dir / "logic_check.json")

    for name, data in [
        ("fact_anchor.json", fact_anchor),
        ("model_answer.json", model_answer),
        ("topic_importance.json", topic_importance),
        ("logic_check.json", logic_check),
    ]:
        if data.get("topic_id") != topic_id:
            fail(f"{pack_dir / name}: topic_id mismatch. expected={topic_id}, actual={data.get('topic_id')}")

    return {
        "topic_id": topic_id,
        "fact_anchor": fact_anchor,
        "model_answer": model_answer,
        "topic_importance": topic_importance,
        "logic_check": logic_check,
    }


def build_fact_anchors(packs: list[dict[str, Any]], version: str) -> dict[str, Any]:
    return {
        "version": f"{version}-generated-topic-pack-fact-anchors",
        "subject": SUBJECT,
        "schema_version": "generated.fact_anchors.v1",
        "source": "rubrics/topic_packs/*/fact_anchor.json",
        "runtime_status": "generated_candidate_not_yet_runtime_default",
        "topics": [
            pack["fact_anchor"]
            for pack in packs
        ],
    }


def _as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = value.strip()
        return [value] if value else []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            if isinstance(item, str):
                s = item.strip()
                if s:
                    out.append(s)
            elif isinstance(item, dict):
                # For outline-like objects, prefer human-readable intent/section.
                for key in ("intent", "section", "name", "title", "text"):
                    v = item.get(key)
                    if isinstance(v, str) and v.strip():
                        out.append(v.strip())
                        break
        return out
    return []


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        value = value.strip()
        if not value:
            continue
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def _outline_sections(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for item in value:
        if isinstance(item, dict):
            section = item.get("section")
            if isinstance(section, str) and section.strip():
                out.append(section.strip())
        elif isinstance(item, str) and item.strip():
            out.append(item.strip())
    return _unique(out)


def _outline_intents(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for item in value:
        if isinstance(item, dict):
            intent = item.get("intent") or item.get("section")
            if isinstance(intent, str) and intent.strip():
                out.append(intent.strip())
        elif isinstance(item, str) and item.strip():
            out.append(item.strip())
    return _unique(out)


def _extract_fact_anchor_terms(fact_anchor: dict[str, Any]) -> list[str]:
    terms: list[str] = []

    def visit(obj: Any) -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                key_l = str(key).lower()
                if key_l in {
                    "topic_aliases",
                    "aliases",
                    "keywords",
                    "core_terms",
                    "support_terms",
                    "field_terms",
                    "field_keywords",
                    "core_terms_found",
                    "support_terms_found",
                }:
                    terms.extend(_as_str_list(value))
                else:
                    visit(value)
        elif isinstance(obj, list):
            for item in obj:
                visit(item)

    visit(fact_anchor)
    return _unique(terms)


def normalize_model_answer_for_runtime(pack: dict[str, Any]) -> dict[str, Any]:
    topic_id = pack["topic_id"]
    model_answer = dict(pack["model_answer"])
    fact_anchor = pack.get("fact_anchor") if isinstance(pack.get("fact_anchor"), dict) else {}

    title = (
        model_answer.get("title")
        or model_answer.get("title_ko")
        or model_answer.get("name")
        or topic_id
    )

    question_examples = (
        _as_str_list(model_answer.get("question_examples"))
        or _as_str_list(model_answer.get("expected_question_patterns"))
    )

    recommended_outline = model_answer.get("recommended_outline")

    expected_structure = (
        _as_str_list(model_answer.get("expected_structure"))
        or _outline_sections(recommended_outline)
    )

    model_answer_outline = (
        _as_str_list(model_answer.get("model_answer_outline"))
        or _outline_intents(recommended_outline)
    )

    high_score_features = (
        _as_str_list(model_answer.get("high_score_features"))
        or _as_str_list(model_answer.get("high_score_points"))
    )

    low_score_patterns = (
        _as_str_list(model_answer.get("low_score_patterns"))
        or _as_str_list(model_answer.get("common_missing_points"))
    )

    topic_aliases = _unique(
        _as_str_list(model_answer.get("topic_aliases"))
        + _as_str_list(model_answer.get("aliases"))
        + _as_str_list(model_answer.get("title"))
        + _as_str_list(model_answer.get("title_ko"))
        + question_examples
        + [topic_id, topic_id.replace("_", " ")]
        + _extract_fact_anchor_terms(fact_anchor)
    )

    field_connection_points = _unique(
        _as_str_list(model_answer.get("field_connection_points"))
        + _as_str_list(model_answer.get("field_keywords"))
        + _as_str_list(model_answer.get("practical_keywords"))
        + _extract_fact_anchor_terms(fact_anchor)
    )

    runtime_answer = dict(model_answer)
    runtime_answer.update(
        {
            "id": model_answer.get("id") or f"{topic_id}_COMPARE_v1",
            "topic_id": topic_id,
            "question_type": model_answer.get("question_type") or "COMPARE_SELECTION",
            "title": title,
            "question_examples": question_examples,
            "topic_aliases": topic_aliases,
            "expected_structure": expected_structure,
            "model_answer_outline": model_answer_outline,
            "high_score_features": high_score_features,
            "low_score_patterns": low_score_patterns,
            "field_connection_points": field_connection_points,
            "revision_notes": _as_str_list(model_answer.get("revision_notes")),
            "source_schema_version": model_answer.get("schema_version"),
        }
    )

    return runtime_answer


def build_model_answers(packs: list[dict[str, Any]], version: str) -> dict[str, Any]:
    return {
        "version": f"{version}-generated-topic-pack-model-answers",
        "subject": SUBJECT,
        "schema_version": "generated.model_answers.v1",
        "source": "rubrics/topic_packs/*/model_answer.json",
        "runtime_status": "generated_candidate_not_yet_runtime_default",
        "answers": [
            normalize_model_answer_for_runtime(pack)
            for pack in packs
        ],
    }

# BEGIN GENERATED_ROUTING_ALIAS_FIELDS_PATCH
_ORIGINAL_BUILD_MODEL_ANSWERS = build_model_answers


def _generated_routing_unique(values):
    seen = set()
    out = []
    for value in values or []:
        text = str(value or "").strip()
        if not text:
            continue
        if text in seen:
            continue
        seen.add(text)
        out.append(text)
    return out


def _generated_routing_filter_generic_terms(values):
    noise = {
        "",
        "시스템",
        "차계",
        "표준",
        "보통",
        "대해",
        "형태로",
        "조건",
        "실수",
        "있지만",
        "같은",
        "개념",
        "판단",
        "해석형",
        "모범",
        "답안",
        "response",
        "condition",
        "design",
        "sensor",
        "damping",
        "stability",
        "confusion",
        "low-pass",
        "magnitude",
        "amplitude ratio",
        "frequency ratio",
        "natural frequency",
        "transfer function",
        "second order",
        "K",
        "+2",
        "/(s",
        "G(s",
    }

    out = []
    for value in values or []:
        text = str(value or "").strip()
        if not text:
            continue
        if text in noise:
            continue
        if len(text) <= 1 and text not in {"ζ"}:
            continue
        out.append(text)
    return _generated_routing_unique(out)


def _generated_pack_model_answer_map(packs):
    mapping = {}
    for pack in packs or []:
        if not isinstance(pack, dict):
            continue

        topic_id = pack.get("topic_id")
        model_answer = pack.get("model_answer") or {}

        if topic_id and isinstance(model_answer, dict):
            mapping[str(topic_id)] = model_answer

    return mapping


def _generated_fallback_routing_aliases(answer):
    values = [
        answer.get("title"),
        *(answer.get("question_examples") or []),
        answer.get("topic_id"),
        str(answer.get("topic_id") or "").replace("_", " "),
        *(answer.get("topic_aliases") or []),
    ]
    return _generated_routing_filter_generic_terms(values)[:40]


def _generated_fallback_routing_field_points(answer):
    values = answer.get("field_connection_points") or []
    return _generated_routing_filter_generic_terms(values)[:50]


def _generated_apply_data_driven_routing_fields(bank, packs):
    pack_model_answers = _generated_pack_model_answer_map(packs)

    for answer in bank.get("answers", []) or []:
        topic_id = str(answer.get("topic_id") or "")
        pack_model_answer = pack_model_answers.get(topic_id) or {}

        routing_aliases = pack_model_answer.get("routing_aliases")
        routing_field_points = pack_model_answer.get("routing_field_points")

        if isinstance(routing_aliases, list) and routing_aliases:
            answer["topic_aliases"] = _generated_routing_filter_generic_terms(routing_aliases)
        else:
            answer["topic_aliases"] = _generated_fallback_routing_aliases(answer)

        if isinstance(routing_field_points, list) and routing_field_points:
            answer["field_connection_points"] = _generated_routing_filter_generic_terms(routing_field_points)
        else:
            answer["field_connection_points"] = _generated_fallback_routing_field_points(answer)

    return bank


def build_model_answers(packs, version):
    bank = _ORIGINAL_BUILD_MODEL_ANSWERS(packs, version)
    return _generated_apply_data_driven_routing_fields(bank, packs)


# END GENERATED_ROUTING_ALIAS_FIELDS_PATCH


def build_topic_importance(packs: list[dict[str, Any]], version: str) -> dict[str, Any]:
    return {
        "version": f"{version}-generated-topic-pack-importance",
        "subject": SUBJECT,
        "schema_version": "generated.topic_importance.v1",
        "source": "rubrics/topic_packs/*/topic_importance.json",
        "runtime_status": "generated_candidate_not_yet_runtime_default",
        "topics": [
            pack["topic_importance"]
            for pack in packs
        ],
    }


def build_logic_checks(packs: list[dict[str, Any]], version: str) -> dict[str, Any]:
    topic_logic_checks: list[dict[str, Any]] = []

    for pack in packs:
        topic_id = pack["topic_id"]
        logic_check = pack["logic_check"]
        deterministic = logic_check.get("deterministic_checks")

        if not isinstance(deterministic, dict):
            fail(f"{topic_id}: logic_check.deterministic_checks must be object")

        entry = {
            "topic_id": topic_id,
            **deterministic,
        }
        topic_logic_checks.append(entry)

    return {
        "version": f"{version}-generated-topic-pack-logic-checks",
        "description": "Generated deterministic logic check bank from topic_packs. Do not edit manually.",
        "schema_version": "generated.logic_checks.v1",
        "subject": SUBJECT,
        "source": "rubrics/topic_packs/*/logic_check.json:deterministic_checks",
        "runtime_status": "generated_candidate_not_yet_runtime_default",
        "topic_logic_checks": topic_logic_checks,
    }


def build_logic_check_profiles(packs: list[dict[str, Any]], version: str) -> dict[str, Any]:
    profiles: list[dict[str, Any]] = []

    for pack in packs:
        topic_id = pack["topic_id"]
        logic_check = pack["logic_check"]
        llm_profile = logic_check.get("llm_profile")

        if not isinstance(llm_profile, dict):
            fail(f"{topic_id}: logic_check.llm_profile must be object")

        entry = {
            "topic_id": topic_id,
            **llm_profile,
        }
        profiles.append(entry)

    return {
        "version": f"{version}-generated-topic-pack-logic-check-profiles",
        "description": "Generated LLM logic verifier profile bank from topic_packs. Do not edit manually.",
        "schema_version": "generated.logic_check_profiles.v1",
        "subject": SUBJECT,
        "source": "rubrics/topic_packs/*/logic_check.json:llm_profile",
        "runtime_status": "generated_candidate_not_yet_runtime_default",
        "profiles": profiles,
    }


def build_manifest(packs: list[dict[str, Any]], version: str) -> dict[str, Any]:
    return {
        "version": f"{version}-generated-topic-pack-manifest",
        "schema_version": "generated.topic_pack_manifest.v1",
        "subject": SUBJECT,
        "source": "rubrics/topic_packs",
        "runtime_status": "generated_candidate_not_yet_runtime_default",
        "topic_count": len(packs),
        "topics": [
            {
                "topic_id": pack["topic_id"],
                "files": [
                    "fact_anchor.json",
                    "model_answer.json",
                    "topic_importance.json",
                    "logic_check.json",
                    "README.md",
                ],
            }
            for pack in packs
        ],
    }


def main() -> int:
    if not PACK_ROOT.exists():
        fail(f"topic pack directory not found: {PACK_ROOT}")

    pack_dirs = sorted(p for p in PACK_ROOT.iterdir() if p.is_dir())

    if not pack_dirs:
        fail(f"no topic packs found under {PACK_ROOT}")

    packs = [load_topic_pack(pack_dir) for pack_dir in pack_dirs]

    topic_ids = [pack["topic_id"] for pack in packs]
    if len(topic_ids) != len(set(topic_ids)):
        fail("duplicate topic_id in topic packs")

    version = now_version()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    write_json(OUT_DIR / "fact_anchors.generated.json", build_fact_anchors(packs, version))
    write_json(OUT_DIR / "model_answers.generated.json", build_model_answers(packs, version))
    write_json(OUT_DIR / "topic_importance.generated.json", build_topic_importance(packs, version))
    write_json(OUT_DIR / "logic_checks.generated.json", build_logic_checks(packs, version))
    write_json(OUT_DIR / "logic_check_profiles.generated.json", build_logic_check_profiles(packs, version))
    write_json(OUT_DIR / "topic_pack_manifest.generated.json", build_manifest(packs, version))

    print()
    print("GENERATED OK")
    print(f"topics: {len(packs)}")
    for topic_id in topic_ids:
        print(f"- {topic_id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
