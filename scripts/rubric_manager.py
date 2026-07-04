#!/usr/bin/env python3

from __future__ import annotations

# CREATE_TOPIC_PACK_COMMAND_PATCH
# Lightweight early dispatch so rubric_manager.py can expose the scaffold
# generator without depending on the manager's internal command table shape.
try:
    import sys as _ctpg_sys
    if len(_ctpg_sys.argv) > 1 and _ctpg_sys.argv[1] == "create-topic-pack":
        import importlib.util as _ctpg_importlib_util
        from pathlib import Path as _ctpg_Path

        _ctpg_path = _ctpg_Path(__file__).resolve().parent / "create_topic_pack.py"
        _ctpg_spec = _ctpg_importlib_util.spec_from_file_location(
            "_create_topic_pack_module",
            _ctpg_path,
        )
        if _ctpg_spec is None or _ctpg_spec.loader is None:
            raise RuntimeError(f"cannot load {_ctpg_path}")

        _ctpg_mod = _ctpg_importlib_util.module_from_spec(_ctpg_spec)
        _ctpg_spec.loader.exec_module(_ctpg_mod)

        raise SystemExit(_ctpg_mod.main(_ctpg_sys.argv[2:]))
except SystemExit:
    raise
except Exception as _ctpg_exc:
    raise SystemExit(f"create-topic-pack dispatch failed: {_ctpg_exc}")
# END_CREATE_TOPIC_PACK_COMMAND_PATCH


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
