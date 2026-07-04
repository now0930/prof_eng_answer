from __future__ import annotations

import os
from pathlib import Path
from typing import Literal


BASE_DIR = Path(__file__).resolve().parent

RubricBankMode = Literal["legacy", "generated"]

_ALLOWED_MODES = {"legacy", "generated"}

_LEGACY_PATHS = {
    "fact_anchors": "rubrics/fact_anchors/industrial_instrumentation_control.json",
    "model_answers": "rubrics/model_answers/industrial_instrumentation_control.json",
    "topic_importance": "rubrics/topic_importance/industrial_instrumentation_control.json",
    "logic_checks": "rubrics/logic_checks/industrial_instrumentation_control.json",
    "logic_check_profiles": "rubrics/logic_check_profiles/industrial_instrumentation_control.json",
}

_GENERATED_PATHS = {
    "fact_anchors": "rubrics/generated/fact_anchors.generated.json",
    "model_answers": "rubrics/generated/model_answers.generated.json",
    "topic_importance": "rubrics/generated/topic_importance.generated.json",
    "logic_checks": "rubrics/generated/logic_checks.generated.json",
    "logic_check_profiles": "rubrics/generated/logic_check_profiles.generated.json",
    "topic_pack_manifest": "rubrics/generated/topic_pack_manifest.generated.json",
}


def get_rubric_bank_mode() -> RubricBankMode:
    mode = os.getenv("RUBRIC_BANK_MODE", "legacy").strip().lower()

    if mode not in _ALLOWED_MODES:
        raise ValueError(
            "Invalid RUBRIC_BANK_MODE={!r}. Allowed values: {}".format(
                mode,
                ", ".join(sorted(_ALLOWED_MODES)),
            )
        )

    return mode  # type: ignore[return-value]


def get_rubric_bank_path_map(mode: str | None = None) -> dict[str, Path]:
    resolved_mode = (mode or get_rubric_bank_mode()).strip().lower()

    if resolved_mode not in _ALLOWED_MODES:
        raise ValueError(
            "Invalid rubric bank mode={!r}. Allowed values: {}".format(
                resolved_mode,
                ", ".join(sorted(_ALLOWED_MODES)),
            )
        )

    raw_paths = _GENERATED_PATHS if resolved_mode == "generated" else _LEGACY_PATHS

    return {
        name: BASE_DIR / rel_path
        for name, rel_path in raw_paths.items()
    }


def resolve_rubric_bank_path(bank_name: str, mode: str | None = None) -> Path:
    path_map = get_rubric_bank_path_map(mode)

    if bank_name not in path_map:
        raise KeyError(
            "Unknown rubric bank={!r}. Available banks: {}".format(
                bank_name,
                ", ".join(sorted(path_map)),
            )
        )

    return path_map[bank_name]


def require_rubric_bank_paths(mode: str | None = None) -> dict[str, Path]:
    path_map = get_rubric_bank_path_map(mode)

    missing = {
        name: path
        for name, path in path_map.items()
        if not path.exists()
    }

    if missing:
        details = "\n".join(
            f"- {name}: {path}"
            for name, path in sorted(missing.items())
        )
        raise FileNotFoundError(
            "Missing rubric bank files for mode={!r}:\n{}".format(
                mode or get_rubric_bank_mode(),
                details,
            )
        )

    return path_map


def get_rubric_bank_report(mode: str | None = None) -> dict[str, object]:
    resolved_mode = mode or get_rubric_bank_mode()
    path_map = get_rubric_bank_path_map(resolved_mode)

    return {
        "mode": resolved_mode,
        "base_dir": str(BASE_DIR),
        "paths": {
            name: {
                "path": str(path),
                "exists": path.exists(),
            }
            for name, path in sorted(path_map.items())
        },
    }


if __name__ == "__main__":
    import json

    print(
        json.dumps(
            get_rubric_bank_report(),
            ensure_ascii=False,
            indent=2,
        )
    )
