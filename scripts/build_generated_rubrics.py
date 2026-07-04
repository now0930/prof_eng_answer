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


def build_model_answers(packs: list[dict[str, Any]], version: str) -> dict[str, Any]:
    return {
        "version": f"{version}-generated-topic-pack-model-answers",
        "subject": SUBJECT,
        "schema_version": "generated.model_answers.v1",
        "source": "rubrics/topic_packs/*/model_answer.json",
        "runtime_status": "generated_candidate_not_yet_runtime_default",
        "answers": [
            pack["model_answer"]
            for pack in packs
        ],
    }


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
