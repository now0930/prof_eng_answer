from __future__ import annotations

import argparse
import subprocess
import sys

from rubric_content.common import ROOT
from rubric_content.topic_importance import cmd_validate_topic_importance


def run_script(entry) -> int:
    if isinstance(entry, tuple):
        path, extra_args = entry
    else:
        path, extra_args = entry, []

    script = ROOT / path
    if not script.exists():
        print("SKIP missing:", path)
        return 0

    print("RUN:", path)
    return subprocess.call([sys.executable, str(script), *extra_args], cwd=str(ROOT))

def cmd_validate_all(_args: argparse.Namespace) -> int:
    scripts = [
        "scripts/validate_question_type_profile.py",
        "scripts/validate_model_answer_bank.py",
        ("scripts/validate_model_answer_relationships.py", ["--fail-on-major"]),
        "scripts/validate_config.py",
        "scripts/validate_fact_anchor_bank.py",
    ]

    rc = 0
    for script in scripts:
        rc = max(rc, run_script(script))

    print("RUN: scripts/validate_rubric_bank_format.py")
    subprocess.run([sys.executable, "scripts/validate_rubric_bank_format.py"], check=True)
    print("RUN: scripts/validate_rubric_bank_content.py")
    subprocess.run([sys.executable, "scripts/validate_rubric_bank_content.py"], check=True)
    print("RUN: validate-topic-importance")
    rc = max(rc, cmd_validate_topic_importance(argparse.Namespace(bank=None)))

    print("RUN: py_compile")
    files = [
        "rubric_registry.py",
        "question_type_router.py",
        "model_answer_router.py",
        "originality_grader.py",
        "gemini_grader.py",
        "grading_config.py",
        "grading_agents.py",
        "difficulty_strategy.py",
        "difficulty_output_adapter.py",
        "difficulty_score_ceiling.py",
        "question_type_taxonomy.py",
        "question_type_coverage_adapter.py",
        "question_type_coverage_score_adjuster.py",
        "semantic_question_type_prompt.py",
        "semantic_question_type_postprocess.py",
        "scripts/rubric_manager.py",
        "scripts/rubric_content/common.py",
        "scripts/rubric_content/question_types.py",
        "scripts/rubric_content/model_answers.py",
        "scripts/rubric_content/fact_anchors.py",
        "scripts/rubric_content/topic_importance.py",
        "scripts/rubric_content/validators.py",
        "bot.py",
    ]
    existing = [str(ROOT / f) for f in files if (ROOT / f).exists()]
    rc = max(rc, subprocess.call([sys.executable, "-m", "py_compile", *existing]))

    if rc == 0:
        print("ALL VALID")
    return rc


def add_parser(sub) -> None:
    p = sub.add_parser("validate-all", help="Run all rubric validators and py_compile")
    p.set_defaults(func=cmd_validate_all)
