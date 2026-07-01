#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "reports"

RELATIONSHIP_CSV = REPORT_DIR / "model_answer_relationship_validation.csv"
RELATIONSHIP_ANALYSIS_CSV = REPORT_DIR / "model_answer_relationship_minor_analysis.csv"
PRIORITY_MINOR_MD = REPORT_DIR / "model_answer_relationship_priority_minors.md"
FACT_ANCHOR_AUDIT_CSV = REPORT_DIR / "fact_anchor_quality_audit.csv"
AUDIT_SUMMARY_MD = REPORT_DIR / "rubric_audit_summary.md"


@dataclass
class CommandResult:
    name: str
    returncode: int
    stdout: str
    stderr: str


@dataclass
class SeverityCount:
    major: int = 0
    minor: int = 0
    total: int = 0


@dataclass
class PriorityCount:
    p1: int = 0
    p2: int = 0
    p3: int = 0
    total: int = 0


@dataclass
class RubricAuditSummary:
    fact_anchor: SeverityCount
    model_answer_relationship: SeverityCount
    model_answer_analysis: PriorityCount
    priority_minor: int
    validate_all_ok: bool
    status: str
    commands: list[CommandResult]


def run_command(name: str, args: list[str], *, allow_failure: bool = False) -> CommandResult:
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    result = CommandResult(
        name=name,
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )

    if proc.returncode != 0 and not allow_failure:
        print(proc.stdout)
        print(proc.stderr)
        raise SystemExit(f"ERROR: command failed: {name}")

    return result


def count_severity_csv(path: Path) -> SeverityCount:
    if not path.exists():
        return SeverityCount()

    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    count = SeverityCount(total=len(rows))

    for row in rows:
        severity = (
            row.get("severity")
            or row.get("level")
            or row.get("Severity")
            or row.get("LEVEL")
            or ""
        ).upper()

        if severity == "MAJOR":
            count.major += 1
        elif severity == "MINOR":
            count.minor += 1

    return count


def count_priority_csv(path: Path) -> PriorityCount:
    if not path.exists():
        return PriorityCount()

    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    count = PriorityCount(total=len(rows))

    for row in rows:
        priority = (row.get("priority") or "").upper()

        if priority == "P1":
            count.p1 += 1
        elif priority == "P2":
            count.p2 += 1
        elif priority == "P3":
            count.p3 += 1

    return count


def parse_priority_minor_count(*texts: str) -> int:
    for text in texts:
        match = re.search(r"priority\s+MINOR\s*:\s*(\d+)", text)
        if match:
            return int(match.group(1))

    if PRIORITY_MINOR_MD.exists():
        text = PRIORITY_MINOR_MD.read_text(encoding="utf-8")
        match = re.search(r"priority\s+MINOR\s*:\s*(\d+)", text)
        if match:
            return int(match.group(1))

    return -1


def write_summary(summary: RubricAuditSummary) -> None:
    REPORT_DIR.mkdir(exist_ok=True)

    lines = [
        "# Rubric Audit Summary",
        "",
        f"- status: **{summary.status}**",
        f"- validate-all: {'OK' if summary.validate_all_ok else 'FAIL'}",
        "",
        "## Fact Anchor quality",
        "",
        f"- MAJOR: {summary.fact_anchor.major}",
        f"- MINOR: {summary.fact_anchor.minor}",
        f"- total rows: {summary.fact_anchor.total}",
        "",
        "## Model Answer relationship",
        "",
        f"- MAJOR: {summary.model_answer_relationship.major}",
        f"- MINOR: {summary.model_answer_relationship.minor}",
        f"- total rows: {summary.model_answer_relationship.total}",
        "",
        "## Model Answer minor analysis",
        "",
        f"- total: {summary.model_answer_analysis.total}",
        f"- P1: {summary.model_answer_analysis.p1}",
        f"- P2: {summary.model_answer_analysis.p2}",
        f"- P3: {summary.model_answer_analysis.p3}",
        "",
        "## Priority minor gate",
        "",
        f"- priority MINOR: {summary.priority_minor}",
        "",
        "## Gate rule",
        "",
        "PASS 조건:",
        "",
        "1. Fact Anchor MAJOR = 0",
        "2. Model Answer relationship MAJOR = 0",
        "3. validate-all = OK",
        "4. priority MINOR = 0",
        "",
        "남은 일반 MINOR는 advisory로 유지한다.",
        "",
        "## Commands",
        "",
    ]

    for command in summary.commands:
        lines.append(f"- `{command.name}`: returncode={command.returncode}")

    AUDIT_SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def audit_rubric_quality() -> RubricAuditSummary:
    commands: list[CommandResult] = []

    steps: list[tuple[str, list[str], bool]] = [
        ("validate_fact_anchor_bank", ["python3", "scripts/validate_fact_anchor_bank.py"], False),
        ("audit_fact_anchor_quality", ["python3", "scripts/audit_fact_anchor_quality.py"], False),
        ("validate_model_answer_bank", ["python3", "scripts/validate_model_answer_bank.py"], False),
        ("validate_model_answer_relationships", ["python3", "scripts/validate_model_answer_relationships.py"], False),
        (
            "analyze_model_answer_relationship_minors",
            ["python3", "scripts/rubric_audit/analyze_model_answer_relationship_minors.py"],
            False,
        ),
        ("validate_all", ["python3", "scripts/rubric_manager.py", "validate-all"], False),
        ("report_priority_minor_relationships", ["python3", "scripts/report_priority_minor_relationships.py"], True),
    ]

    for name, args, allow_failure in steps:
        print(f"RUN: {name}")
        result = run_command(name, args, allow_failure=allow_failure)
        commands.append(result)

        if result.stdout.strip():
            print(result.stdout.rstrip())

        if result.stderr.strip():
            print(result.stderr.rstrip())

    fact_anchor = count_severity_csv(FACT_ANCHOR_AUDIT_CSV)
    relationship = count_severity_csv(RELATIONSHIP_CSV)
    analysis = count_priority_csv(RELATIONSHIP_ANALYSIS_CSV)

    priority_result = next((item for item in commands if item.name == "report_priority_minor_relationships"), None)
    priority_minor = parse_priority_minor_count(
        priority_result.stdout if priority_result else "",
        priority_result.stderr if priority_result else "",
    )

    validate_all = next((item for item in commands if item.name == "validate_all"), None)
    validate_all_ok = bool(validate_all and validate_all.returncode == 0)

    passed = (
        fact_anchor.major == 0
        and relationship.major == 0
        and validate_all_ok
        and priority_minor == 0
    )

    summary = RubricAuditSummary(
        fact_anchor=fact_anchor,
        model_answer_relationship=relationship,
        model_answer_analysis=analysis,
        priority_minor=priority_minor,
        validate_all_ok=validate_all_ok,
        status="PASS" if passed else "FAIL",
        commands=commands,
    )

    write_summary(summary)

    print()
    print("=== Rubric audit summary ===")
    print("status:", summary.status)
    print(f"Fact Anchor: MAJOR={fact_anchor.major}, MINOR={fact_anchor.minor}")
    print(f"Model Answer relationship: MAJOR={relationship.major}, MINOR={relationship.minor}")
    print(f"Model Answer analysis: total={analysis.total}, P1={analysis.p1}, P2={analysis.p2}, P3={analysis.p3}")
    print("priority MINOR:", priority_minor)
    print("validate-all:", "OK" if validate_all_ok else "FAIL")
    print("wrote:", AUDIT_SUMMARY_MD)

    if not passed:
        raise SystemExit(1)

    return summary


def main() -> int:
    audit_rubric_quality()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
