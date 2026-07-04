#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

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
        description="Rubric content management helper"
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
