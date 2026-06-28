#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "rubrics" / "question_types" / "v2_professional_engineer.json"

REQUIRED_TYPES = {
    "PRINCIPLE_INTERPRETATION",
    "DIAGNOSIS_ACTION",
    "COMPARE_SELECTION",
    "IMPLEMENTATION_EVALUATION",
}

REQUIRED_TYPE_FIELDS = {
    "name_ko",
    "absorbs_legacy_types",
    "intent",
    "selection_signals",
    "c_fact_focus",
    "d_field_judgement_focus",
    "sub_criteria",
}

def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))

    types = data.get("types")
    if not isinstance(types, dict):
        raise SystemExit("types must be an object")

    actual = set(types)
    if actual != REQUIRED_TYPES:
        raise SystemExit(f"unexpected types: {sorted(actual)}")

    for type_id, profile in types.items():
        missing = REQUIRED_TYPE_FIELDS - set(profile)
        if missing:
            raise SystemExit(f"{type_id} missing fields: {sorted(missing)}")

        for key in [
            "absorbs_legacy_types",
            "selection_signals",
            "c_fact_focus",
            "d_field_judgement_focus",
            "sub_criteria",
        ]:
            value = profile.get(key)
            if not isinstance(value, list) or not value:
                raise SystemExit(f"{type_id}.{key} must be a non-empty list")

    mapping = data.get("legacy_mapping")
    if not isinstance(mapping, dict):
        raise SystemExit("legacy_mapping must be an object")

    if mapping.get("DEFINE", "MISSING") is not None:
        raise SystemExit("DEFINE must map to null")

    for legacy, mapped in mapping.items():
        if mapped is not None and mapped not in REQUIRED_TYPES:
            raise SystemExit(f"invalid legacy mapping: {legacy} -> {mapped}")

    fallback = data.get("fallback_type")
    if fallback not in REQUIRED_TYPES:
        raise SystemExit(f"invalid fallback_type: {fallback}")

    print("VALID")
    print("types:", len(types))
    for type_id in sorted(types):
        print("-", type_id, types[type_id]["name_ko"])

if __name__ == "__main__":
    main()
