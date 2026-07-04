from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from rubric_content.common import ROOT


PIPELINE_SCRIPTS = [
    "scripts/validate_topic_packs.py",
    "scripts/build_generated_rubrics.py",
    "scripts/validate_generated_rubrics.py",
]

AUDIT_SCRIPT = "scripts/audit_generated_vs_runtime.py"
TOPIC_ID_AUDIT_SCRIPT = "scripts/audit_topic_id_consistency.py"


def run_script(path: str) -> int:
    script = ROOT / path

    if not script.exists():
        print("ERROR missing:", path)
        return 1

    print("RUN:", path)
    return subprocess.call([sys.executable, str(script)], cwd=str(ROOT))


def py_compile_pipeline_scripts() -> int:
    files = [ROOT / path for path in PIPELINE_SCRIPTS]
    existing = [str(path) for path in files if path.exists()]

    if len(existing) != len(files):
        missing = [str(path.relative_to(ROOT)) for path in files if not path.exists()]
        print("ERROR missing pipeline scripts:", ", ".join(missing))
        return 1

    print("RUN: py_compile topic pack pipeline")
    return subprocess.call([sys.executable, "-m", "py_compile", *existing], cwd=str(ROOT))


def cmd_validate_topic_packs(_args: argparse.Namespace) -> int:
    rc = py_compile_pipeline_scripts()
    rc = max(rc, run_script("scripts/validate_topic_packs.py"))
    return rc


def cmd_build_generated_rubrics(_args: argparse.Namespace) -> int:
    rc = py_compile_pipeline_scripts()
    rc = max(rc, run_script("scripts/build_generated_rubrics.py"))
    return rc


def cmd_validate_generated_rubrics(_args: argparse.Namespace) -> int:
    rc = py_compile_pipeline_scripts()
    rc = max(rc, run_script("scripts/validate_generated_rubrics.py"))
    return rc


def cmd_validate_generated_pipeline(_args: argparse.Namespace) -> int:
    rc = py_compile_pipeline_scripts()

    for script in PIPELINE_SCRIPTS:
        rc = max(rc, run_script(script))

    if rc == 0:
        print("GENERATED PIPELINE VALID")

    return rc


def cmd_audit_generated_vs_runtime(_args: argparse.Namespace) -> int:
    rc = py_compile_pipeline_scripts()

    audit_path = ROOT / AUDIT_SCRIPT
    if not audit_path.exists():
        print("ERROR missing:", AUDIT_SCRIPT)
        return 1

    print("RUN:", AUDIT_SCRIPT)
    rc = max(rc, subprocess.call([sys.executable, str(audit_path)], cwd=str(ROOT)))
    return rc


def cmd_audit_topic_id_consistency(_args: argparse.Namespace) -> int:
    rc = py_compile_pipeline_scripts()

    audit_path = ROOT / TOPIC_ID_AUDIT_SCRIPT
    if not audit_path.exists():
        print("ERROR missing:", TOPIC_ID_AUDIT_SCRIPT)
        return 1

    print("RUN:", TOPIC_ID_AUDIT_SCRIPT)
    rc = max(rc, subprocess.call([sys.executable, str(audit_path)], cwd=str(ROOT)))
    return rc


def add_parser(sub) -> None:
    p = sub.add_parser(
        "validate-topic-packs",
        help="Validate rubrics/topic_packs source files",
    )
    p.set_defaults(func=cmd_validate_topic_packs)

    p = sub.add_parser(
        "build-generated-rubrics",
        help="Build rubrics/generated/*.generated.json from topic packs",
    )
    p.set_defaults(func=cmd_build_generated_rubrics)

    p = sub.add_parser(
        "validate-generated-rubrics",
        help="Validate rubrics/generated outputs",
    )
    p.set_defaults(func=cmd_validate_generated_rubrics)

    p = sub.add_parser(
        "validate-generated-pipeline",
        help="Validate topic packs, build generated rubrics, then validate generated outputs",
    )
    p.set_defaults(func=cmd_validate_generated_pipeline)


    p = sub.add_parser(
        "audit-generated-vs-runtime",
        help="Audit generated rubric banks against current runtime JSON files",
    )
    p.set_defaults(func=cmd_audit_generated_vs_runtime)


    p = sub.add_parser(
        "audit-topic-id-consistency",
        help="Audit topic_id coverage across topic packs, generated files, and runtime JSON files",
    )
    p.set_defaults(func=cmd_audit_topic_id_consistency)
