from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.replay_sil_issue1_session import (
    EXPECTED_AXES,
    EXPECTED_FATAL_RULES,
    run,
)


EXPECTED_ARTIFACTS = {
    "grade.json",
    "input.raw.txt",
    "input.txt",
    "logic_check_evaluation.json",
    "question_demand_contract.json",
    "replay_manifest.json",
    "submission_normalization.json",
    "telegram.txt",
}


def test_issue1_session_replay_persists_consistent_boundaries() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        output_dir = Path(temporary) / "session"
        manifest = run(output_dir)

        assert {path.name for path in output_dir.iterdir()} == EXPECTED_ARTIFACTS
        persisted_manifest = json.loads(
            (output_dir / "replay_manifest.json").read_text(encoding="utf-8")
        )
        assert persisted_manifest == manifest
        assert manifest["core"]["requirement_ids"] == EXPECTED_AXES
        assert manifest["core"]["fatal_rule_ids"] == EXPECTED_FATAL_RULES

        grade = json.loads(
            (output_dir / "grade.json").read_text(encoding="utf-8")
        )
        assert grade["confidence"] == "medium"
        assert grade["total_score"] <= 14.5
        assert grade["passing_score_allowed"] is False
        assert grade["strong_verdict_allowed"] is False
        assert grade["requirements_full_credit_allowed"] is False

        telegram = (output_dir / "telegram.txt").read_text(encoding="utf-8")
        assert "요구사항 언급률: 87.5%" in telegram
        assert "요구사항 정확 충족률: 12.5%" in telegram
        assert "전체 판정: strong" not in telegram
        assert "요구사항 충족률: 100%" not in telegram


def test_issue1_session_replay_is_deterministic() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        first = run(root / "first")
        second = run(root / "second")

        assert first["core_sha256"] == second["core_sha256"]
        assert first["core"] == second["core"]


def test_compose_runtime_uses_production_workspace_contract() -> None:
    compose = (REPO / "docker-compose.example.yml").read_text(encoding="utf-8")

    assert "nousresearch/hermes-agent:latest" in compose
    assert ".:/workspace/prof_eng_answer" in compose
    assert "working_dir: /workspace/prof_eng_answer" in compose
    assert "/workspace/prof_eng_answer/scripts/run_prof_eng_bot.sh" in compose


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    for name, test in tests:
        test()
        print(f"PASS: {name}")
    print(f"PASS: {len(tests)}/{len(tests)} SIL runtime replay checks")


if __name__ == "__main__":
    main()
