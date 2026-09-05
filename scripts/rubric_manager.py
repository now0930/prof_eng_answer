#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


EXTERNAL_COMMANDS = {
    "add-topic": "topic_pack_workflow_controller.py",
    "approve-topic": "topic_pack_workflow_controller.py",
    "create-topic-pack": "create_topic_pack.py",
    "generate-topic-pack-from-sheet": "generate_topic_pack_from_sheet.py",
    "review-topic-pack": "review_topic_pack.py",
    "review-topic-pack-all": "review_topic_pack_all.py",
    "smoke-topic-pack": "smoke_topic_pack.py",
    "topic-pack-status": "topic_pack_status.py",
    "validate-topic-pack-quality": "validate_topic_pack_quality.py",
    "validate-topic-pack-release": "validate_topic_pack_release.py",
}


def _dispatch_external_command() -> None:
    if len(sys.argv) < 2:
        return
    command = sys.argv[1]
    module_name = EXTERNAL_COMMANDS.get(command)
    if module_name is None:
        return
    path = Path(__file__).resolve().parent / module_name
    try:
        spec = importlib.util.spec_from_file_location(
            f"_rubric_manager_{command.replace('-', '_')}",
            path,
        )
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        argv = sys.argv[1:] if module_name == "topic_pack_workflow_controller.py" else sys.argv[2:]
        raise SystemExit(module.main(argv))
    except SystemExit:
        raise
    except Exception as exc:
        raise SystemExit(f"{command} dispatch failed: {exc}") from exc


_dispatch_external_command()

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from rubric_content import fact_anchors  # noqa: E402
from rubric_content import model_answers  # noqa: E402
from rubric_content import question_types  # noqa: E402
from rubric_content import topic_importance  # noqa: E402
from rubric_content import validators  # noqa: E402
from rubric_content import topic_pack_pipeline  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rubric content management helper",
        epilog=(
            "Topic workflow commands: add-topic, approve-topic, "
            "create-topic-pack, generate-topic-pack-from-sheet, "
            "validate-topic-pack-release, smoke-topic-pack"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    question_types.add_parser(sub)
    model_answers.add_parsers(sub)
    fact_anchors.add_parsers(sub)
    topic_importance.add_parsers(sub)
    validators.add_parser(sub)
    topic_pack_pipeline.add_parser(sub)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
