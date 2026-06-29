from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

MODEL_ANSWER_BANK = ROOT / "rubrics" / "model_answers" / "industrial_instrumentation_control.json"
FACT_ANCHOR_BANK = ROOT / "rubrics" / "fact_anchors" / "industrial_instrumentation_control.json"
TOPIC_IMPORTANCE_BANK = ROOT / "rubrics" / "topic_importance" / "industrial_instrumentation_control.json"

CANDIDATE_ROOT = ROOT / "rubrics" / "content_candidates"


def project_path(path: str | Path | None, default_path: Path) -> Path:
    if path is None:
        return default_path
    p = Path(path)
    if p.is_absolute():
        return p
    return ROOT / p


def read_json(path: str | Path) -> Any:
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(path: str | Path, data: Any) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


def backup_file(path: str | Path) -> Path:
    p = Path(path)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = ROOT / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f"{p.name}.before_update.{stamp}"
    backup.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    return backup


def listify(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return [str(value).strip()] if str(value).strip() else []


def candidate_path(kind: str, name: str) -> Path:
    return CANDIDATE_ROOT / kind / f"{name}.json"


def print_next_steps(candidate: Path, promote_command: str) -> None:
    print("created:", candidate)
    print()
    print("다음 순서:")
    print(f"1) vim {candidate}")
    print(f"2) python3 scripts/rubric_manager.py {promote_command} --candidate {candidate}")
    print("3) python3 scripts/rubric_manager.py validate-all")
