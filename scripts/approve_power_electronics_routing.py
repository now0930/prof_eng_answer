#!/usr/bin/env python3
"""Review and, only after explicit interactive confirmation, approve one routing fix."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "power_electronics_converters_motor_drive_control"
CONFIRMATION = "APPROVE PLC/DCS/SCADA ROUTING"
FOCUSED_TESTS = [
    "tests.test_priority_bundle_risk_golden",
    "tests.test_deterministic_topic_router",
    "scripts.test_plc_dcs_scada_remote_io_architecture_redundancy_topic",
    "scripts.test_power_electronics_ontology_contract",
]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.topic_pack_status import load_status, topic_pack_dir  # noqa: E402


def run(
    command: list[str],
    *,
    capture: bool = False,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    print("$", " ".join(command), flush=True)
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        check=False,
        capture_output=capture,
        env=env,
    )


def print_review_summary() -> str:
    pack_dir = topic_pack_dir(ROOT, TOPIC_ID)
    status = load_status(pack_dir, TOPIC_ID)
    model_answer = json.loads(
        (pack_dir / "model_answer.json").read_text(encoding="utf-8")
    )
    block_term_rows = [
        {
            "pattern": row.get("pattern", ""),
            "block_terms": row.get("routing_exclusive_block_terms", []),
        }
        for row in model_answer.get("expected_question_patterns", [])
        if row.get("routing_exclusive")
    ]

    print("TOPIC:", TOPIC_ID)
    print("CURRENT SOURCE HASH:", status.get("_current_hash"))
    print("PREVIOUSLY APPROVED HASH:", status.get("approved_source_hash"))
    print("CURRENT STATUS:", status.get("status"), status.get("review_state"))
    print(
        "APPROVAL MATCHES SOURCE:",
        "yes"
        if status.get("content_hash") == status.get("_current_hash")
        and status.get("approved_source_hash") == status.get("_current_hash")
        else "no",
    )
    print("EXCLUSIVE PATTERNS:", len(block_term_rows))
    for row in block_term_rows:
        print("-", row["pattern"])
        print("  added boundary terms: PLC / DCS / SCADA")

    print("\nROUTING EXAMPLE:")
    example_question = "PLC, DCS, SCADA의 제어 아키텍처별 역할을 비교하시오."
    print("question:", example_question)
    route_result = run(
        [
            sys.executable,
            "-B",
            "-c",
            (
                "import json; from grading.routing.deterministic_topic_router "
                "import route_question_topics; print(json.dumps("
                "route_question_topics(" + repr(example_question) + "), "
                "ensure_ascii=False))"
            ),
        ],
        capture=True,
    )
    if route_result.stdout:
        print(route_result.stdout.strip())
    if route_result.returncode != 0:
        if route_result.stderr:
            print(route_result.stderr.strip())
        raise SystemExit(route_result.returncode)

    print("\nREVIEW POINT:")
    print(
        "복합 질문(예: PLC 제어와 인버터를 함께 묻는 문제)도 전력전자 배타 라우팅에서 "
        "제외될 수 있습니다. 해당 복합 질문은 테스트로 전부 포괄하지 않습니다."
    )
    print("\nFOCUSED REGRESSION:")
    test_result = run(
        [sys.executable, "-B", "-m", "unittest", "-v", *FOCUSED_TESTS],
        capture=True,
    )
    output = (test_result.stdout or "") + (test_result.stderr or "")
    print(output.rstrip())
    if test_result.returncode != 0:
        raise SystemExit(test_result.returncode)
    return str(status.get("_current_hash"))


def approve(reviewer: str, expected_hash: str) -> None:
    if not sys.stdin.isatty():
        raise SystemExit(
            "ERROR: approval requires an interactive terminal; no changes made."
        )

    print("\nThis will update topic_status.json and promote generated Topic Pack banks.")
    print("It will NOT commit or push.")
    print("Type this exact phrase to continue:")
    print(CONFIRMATION)
    if input("> ").strip() != CONFIRMATION:
        raise SystemExit("Approval not confirmed; no changes made.")

    current = load_status(topic_pack_dir(ROOT, TOPIC_ID), TOPIC_ID)
    if current.get("_current_hash") != expected_hash:
        raise SystemExit("ERROR: Topic Pack changed after review; no approval recorded.")

    approval_result = run(
        [
            sys.executable,
            "scripts/rubric_manager.py",
            "approve-topic",
            "--topic-id",
            TOPIC_ID,
            "--reviewer",
            reviewer,
        ]
    )
    if approval_result.returncode != 0:
        raise SystemExit(approval_result.returncode)

    for command in (
        [
            sys.executable,
            "scripts/rubric_manager.py",
            "validate-topic-pack-release",
            "--all",
        ],
        ["bash", "scripts/validate_release.sh"],
    ):
        env = None
        if command[0] == "bash" and command[-1] == "scripts/validate_release.sh":
            env = os.environ.copy()
            env.update(
                {
                    "PROMOTE_GENERATED": "0",
                    "RUN_SMOKE_TOPIC_PACKS": "0",
                    "RUN_GRADING_REPRODUCIBILITY": "0",
                }
            )
        result = run(command, env=env)
        if result.returncode != 0:
            raise SystemExit(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Show evidence for the PLC/DCS/SCADA routing change. "
            "Default is review-only; approval requires explicit interactive confirmation."
        )
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="after showing evidence/tests, request explicit interactive approval",
    )
    parser.add_argument(
        "--reviewer",
        default="",
        help="human reviewer identifier; required with --approve",
    )
    args = parser.parse_args()
    if args.approve and not args.reviewer.strip():
        parser.error("--reviewer is required with --approve")

    reviewed_hash = print_review_summary()
    if not args.approve:
        print("\nREVIEW ONLY: no Topic status, generated files, or git refs changed.")
        print("After reviewing the output, run with --approve --reviewer <your-id>.")
        return 0

    approve(args.reviewer.strip(), reviewed_hash)
    print("APPROVAL AND RELEASE VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
