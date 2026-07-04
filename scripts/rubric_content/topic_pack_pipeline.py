from __future__ import annotations

import argparse
import subprocess
import sys

from rubric_content.common import ROOT


PIPELINE_SCRIPTS = [
    "scripts/validate_topic_packs.py",
    "scripts/build_generated_rubrics.py",
    "scripts/validate_generated_rubrics.py",
]

OPTIONAL_AUDIT_SCRIPTS = {
    "audit-generated-vs-runtime": "scripts/audit_generated_vs_runtime.py",
    "audit-topic-id-consistency": "scripts/audit_topic_id_consistency.py",
    "audit-generated-runtime-schema": "scripts/audit_generated_runtime_schema.py",
    "audit-rubric-path-usage": "scripts/audit_rubric_path_usage.py",
}


def _script_exists(path: str) -> bool:
    return (ROOT / path).exists()


def run_script(path: str) -> int:
    script = ROOT / path

    if not script.exists():
        print("ERROR missing:", path)
        return 1

    print("RUN:", path)
    return subprocess.call([sys.executable, str(script)], cwd=str(ROOT))


def py_compile_existing_scripts(paths: list[str]) -> int:
    existing = [str(ROOT / path) for path in paths if _script_exists(path)]
    missing = [path for path in paths if not _script_exists(path)]

    if missing:
        print("ERROR missing scripts:", ", ".join(missing))
        return 1

    if not existing:
        return 0

    print("RUN: py_compile")
    for path in paths:
        print(" -", path)

    return subprocess.call([sys.executable, "-m", "py_compile", *existing], cwd=str(ROOT))


def cmd_validate_topic_packs(_args: argparse.Namespace) -> int:
    paths = ["scripts/validate_topic_packs.py"]
    rc = py_compile_existing_scripts(paths)
    rc = max(rc, run_script("scripts/validate_topic_packs.py"))
    return rc


def cmd_build_generated_rubrics(_args: argparse.Namespace) -> int:
    paths = ["scripts/build_generated_rubrics.py"]
    rc = py_compile_existing_scripts(paths)
    rc = max(rc, run_script("scripts/build_generated_rubrics.py"))
    return rc


def cmd_validate_generated_rubrics(_args: argparse.Namespace) -> int:
    paths = ["scripts/validate_generated_rubrics.py"]
    rc = py_compile_existing_scripts(paths)
    rc = max(rc, run_script("scripts/validate_generated_rubrics.py"))
    return rc


def cmd_validate_generated_pipeline(_args: argparse.Namespace) -> int:
    rc = py_compile_existing_scripts(PIPELINE_SCRIPTS)

    for script in PIPELINE_SCRIPTS:
        rc = max(rc, run_script(script))

    if rc == 0:
        print("GENERATED PIPELINE VALID")

    return rc


def cmd_audit_generated_vs_runtime(_args: argparse.Namespace) -> int:
    path = OPTIONAL_AUDIT_SCRIPTS["audit-generated-vs-runtime"]
    rc = py_compile_existing_scripts([path])
    rc = max(rc, run_script(path))
    return rc


def cmd_audit_topic_id_consistency(_args: argparse.Namespace) -> int:
    path = OPTIONAL_AUDIT_SCRIPTS["audit-topic-id-consistency"]
    rc = py_compile_existing_scripts([path])
    rc = max(rc, run_script(path))
    return rc


def cmd_audit_generated_runtime_schema(_args: argparse.Namespace) -> int:
    path = OPTIONAL_AUDIT_SCRIPTS["audit-generated-runtime-schema"]
    rc = py_compile_existing_scripts([path])
    rc = max(rc, run_script(path))
    return rc


def cmd_audit_rubric_path_usage(_args: argparse.Namespace) -> int:
    path = OPTIONAL_AUDIT_SCRIPTS["audit-rubric-path-usage"]
    rc = py_compile_existing_scripts([path])
    rc = max(rc, run_script(path))
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

    p = sub.add_parser(
        "audit-generated-runtime-schema",
        help="Audit generated JSON top-level schema compatibility with runtime JSON files",
    )
    p.set_defaults(func=cmd_audit_generated_runtime_schema)

    p = sub.add_parser(
        "audit-rubric-path-usage",
        help="Audit source files for direct runtime rubric JSON path usage",
    )
    p.set_defaults(func=cmd_audit_rubric_path_usage)
