#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "rubrics" / "topic_packs"
VALIDATOR = ROOT / "scripts" / "validate_topic_packs.py"

ALLOWED_IMPORTANCE = {
    "core",
    "must",
    "important",
    "optional",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8")
    )

    assert isinstance(value, dict), path
    return value


def main() -> None:
    subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
        ],
        cwd=ROOT,
        check=True,
    )

    global_ids: set[str] = set()

    pattern_strings = 0
    pattern_objects = 0
    outline_strings = 0
    outline_objects = 0
    core_anchor_count = 0

    for directory in sorted(
        PACK_ROOT.iterdir()
    ):
        if not directory.is_dir():
            continue

        fact = load_json(
            directory / "fact_anchor.json"
        )
        model = load_json(
            directory / "model_answer.json"
        )

        anchors = fact.get("anchors")
        assert isinstance(anchors, list)
        assert anchors

        local_ids: set[str] = set()

        for anchor in anchors:
            assert isinstance(anchor, dict)

            anchor_id = anchor.get(
                "anchor_id"
            )
            record_id = anchor.get("id")

            assert isinstance(anchor_id, str)
            assert anchor_id

            if record_id is not None:
                assert record_id == anchor_id

            assert anchor_id not in local_ids
            assert anchor_id not in global_ids

            local_ids.add(anchor_id)
            global_ids.add(anchor_id)

            importance = anchor.get(
                "importance"
            )

            if importance is not None:
                assert (
                    importance
                    in ALLOWED_IMPORTANCE
                )

                if importance == "core":
                    core_anchor_count += 1

        patterns = model.get(
            "expected_question_patterns"
        )
        assert isinstance(patterns, list)
        assert patterns

        for pattern in patterns:
            if isinstance(pattern, str):
                assert pattern.strip()
                pattern_strings += 1
                continue

            assert isinstance(pattern, dict)
            assert isinstance(
                pattern.get("pattern"),
                str,
            )
            assert pattern["pattern"].strip()

            for anchor_id in pattern.get(
                "required_anchor_ids",
                [],
            ):
                assert anchor_id in local_ids

            pattern_objects += 1

        outline = model.get(
            "recommended_outline"
        )
        assert isinstance(outline, list)
        assert outline

        for section in outline:
            if isinstance(section, str):
                assert section.strip()
                outline_strings += 1
                continue

            assert isinstance(section, dict)
            assert isinstance(
                section.get("section"),
                str,
            )
            assert isinstance(
                section.get("intent"),
                str,
            )

            for anchor_id in section.get(
                "anchor_refs",
                [],
            ):
                assert anchor_id in local_ids

            outline_objects += 1

    assert core_anchor_count > 0
    assert pattern_strings > 0
    assert pattern_objects > 0
    assert outline_strings > 0
    assert outline_objects > 0

    print(
        f"global_anchor_count="
        f"{len(global_ids)}"
    )
    print(
        f"core_anchor_count="
        f"{core_anchor_count}"
    )
    print(
        f"pattern_string_count="
        f"{pattern_strings}"
    )
    print(
        f"pattern_object_count="
        f"{pattern_objects}"
    )
    print(
        f"outline_string_count="
        f"{outline_strings}"
    )
    print(
        f"outline_object_count="
        f"{outline_objects}"
    )
    print(
        "PASS: id AND anchor_id "
        "ARE CONSISTENT"
    )
    print(
        "PASS: LOCAL AND GLOBAL "
        "ANCHOR IDS ARE UNIQUE"
    )
    print(
        "PASS: core FACT ANCHORS "
        "ARE SUPPORTED"
    )
    print(
        "PASS: STRING AND OBJECT "
        "MODEL ANSWER SCHEMAS"
    )
    print(
        "PASS: ALL RICH-SCHEMA "
        "ANCHOR REFERENCES EXIST"
    )


if __name__ == "__main__":
    main()
