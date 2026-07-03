#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
README = DOCS / "README.md"

CODE_BACKED_DOCS = {
    "operation_runbook.md": [
        "bot.py",
        "docker-compose.yaml",
        "docker-compose.example.yml",
    ],
    "docker_compose_usage.md": [
        "docker-compose.yaml",
        "docker-compose.example.yml",
        "scripts/run_prof_eng_bot.sh",
    ],
    "grading_architecture.md": [
        "grading_agents.py",
        "grading_config.py",
        "rubrics/scoring_model/default.json",
        "rubrics/raters/layered_default.json",
    ],
    "question_type_taxonomy.md": [
        "question_type_taxonomy.py",
        "question_type_output_adapter.py",
        "question_type_coverage_adapter.py",
        "rubrics/question_types/default.json",
    ],
    "difficulty_and_selection_strategy.md": [
        "difficulty_strategy.py",
        "difficulty_output_adapter.py",
        "difficulty_score_ceiling.py",
        "rubrics/difficulty_profiles/default.json",
        "rubrics/topic_importance/industrial_instrumentation_control.json",
        "rubrics/exam_selection/default.json",
    ],
    "llm_provider.md": [
        "llm_provider_router.py",
        "llm_provider_settings.py",
        "gemini_grader.py",
        "clova_grader.py",
    ],
    "rubric_authoring_guide.md": [
        "rubric_registry.py",
        "scripts/rubric_manager.py",
        "rubrics/model_answers/industrial_instrumentation_control.json",
        "rubrics/fact_anchors/industrial_instrumentation_control.json",
        "rubrics/topic_importance/industrial_instrumentation_control.json",
    ],
    "model_answer_generator_prompt.md": [
        "scripts/rubric_manager.py",
        "rubrics/model_answers/industrial_instrumentation_control.json",
    ],
    "fact_anchor_generator_prompt.md": [
        "scripts/rubric_manager.py",
        "rubrics/fact_anchors/industrial_instrumentation_control.json",
    ],
    "topic_importance_generator_prompt.md": [
        "scripts/rubric_manager.py",
        "rubrics/topic_importance/industrial_instrumentation_control.json",
    ],
}

STRUCTURE_REFERENCE_DOCS = {
    "migration_plan.md": "구조 변경 및 migration 기록. active code 설명이 아니라 history/reference.",
    "structure_review.md": "과거 구조 검토 문서. active code 설명이 아니라 구조 이해용 reference.",
}

REQUIRED_JSON = [
    "rubrics/active_profile.json",
    "rubrics/scoring_model/default.json",
    "rubrics/subjects/industrial_instrumentation_control.json",
    "rubrics/raters/layered_default.json",
    "rubrics/question_types/default.json",
    "rubrics/fact_anchors/industrial_instrumentation_control.json",
    "rubrics/model_answers/industrial_instrumentation_control.json",
    "rubrics/topic_importance/industrial_instrumentation_control.json",
    "rubrics/difficulty_profiles/default.json",
    "rubrics/exam_selection/default.json",
    "rubrics/originality/default.json",
    "schemas/grade_schema.json",
    "schemas/answer_structure_schema.json",
]

REQUIRED_COMMANDS = [
    "list-model-answers",
    "new-model-answer",
    "promote-model-answer",
    "delete-model-answer",
    "validate-model-answers",
    "list-fact-anchors",
    "new-fact-anchor-topic",
    "promote-fact-anchor-topic",
    "delete-fact-anchor-topic",
    "validate-fact-anchors",
    "list-topic-importance",
    "new-topic-importance",
    "promote-topic-importance",
    "delete-topic-importance",
    "validate-topic-importance",
    "validate-all",
]


def fail(msg: str) -> None:
    print("FAIL:", msg)


def ok(msg: str) -> None:
    print("OK:", msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def existing_docs() -> list[str]:
    return sorted(p.name for p in DOCS.glob("*.md"))


def cli_help() -> str:
    p = subprocess.run(
        [sys.executable, "scripts/rubric_manager.py", "--help"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return p.stdout


def main() -> int:
    rc = 0

    if not README.exists():
        fail("docs/README.md missing")
        return 1

    readme = read(README)
    docs = existing_docs()

    print("== docs files ==")
    for name in docs:
        print("-", name)

    print("\n== docs/README coverage ==")
    for name in docs:
        if f"`{name}`" not in readme:
            fail(f"docs/README.md does not mention {name}")
            rc = 1
        else:
            ok(f"README mentions {name}")

    print("\n== code-backed docs ==")
    for doc, refs in CODE_BACKED_DOCS.items():
        doc_path = DOCS / doc
        if not doc_path.exists():
            fail(f"{doc} missing")
            rc = 1
            continue

        missing_refs = [ref for ref in refs if not (ROOT / ref).exists()]
        if missing_refs:
            fail(f"{doc} references expected code/json not present: {missing_refs}")
            rc = 1
        else:
            ok(f"{doc} has backing code/json files")

    print("\n== structure/reference docs ==")
    for doc, reason in STRUCTURE_REFERENCE_DOCS.items():
        if (DOCS / doc).exists():
            if f"`{doc}`" not in readme:
                fail(f"{doc} exists but not classified in README")
                rc = 1
            else:
                ok(f"{doc} kept as reference: {reason}")

    print("\n== JSON files mentioned by README ==")
    for rel in REQUIRED_JSON:
        if rel in readme:
            if not (ROOT / rel).exists():
                fail(f"README mentions missing JSON: {rel}")
                rc = 1
            else:
                ok(f"JSON exists: {rel}")

    print("\n== rubric_manager commands ==")
    help_text = cli_help()
    for cmd in REQUIRED_COMMANDS:
        if cmd in readme:
            if cmd not in help_text:
                fail(f"README mentions command not in CLI: {cmd}")
                rc = 1
            else:
                ok(f"CLI command exists: {cmd}")

    print("\n== docs with no classification ==")
    classified = set(CODE_BACKED_DOCS) | set(STRUCTURE_REFERENCE_DOCS) | {"README.md"}
    for doc in docs:
        if doc not in classified:
            fail(f"{doc} is not classified as code-backed or reference")
            rc = 1

    print("\n== stale active wording candidates ==")
    stale_patterns = [
        r"10개 문제유형",
        r"DEFINE, COMPARE, CALC_DESIGN",
        r"question_type.*PROCEDURE",
        r"대표 legacy 성격",
    ]
    targets = [README] + sorted(DOCS.glob("*.md"))
    for path in targets:
        text = read(path)
        for pattern in stale_patterns:
            if re.search(pattern, text):
                fail(f"stale wording candidate in {path.relative_to(ROOT)}: {pattern}")
                rc = 1

    if rc == 0:
        print("\nDOC AUDIT PASSED")
    else:
        print("\nDOC AUDIT FAILED")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
