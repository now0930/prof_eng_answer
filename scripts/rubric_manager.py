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

# VALIDATE_TOPIC_PACK_RELEASE_COMMAND_PATCH
# Lightweight early dispatch for full topic_pack release validation.
try:
    import sys as _vtpr_sys
    if len(_vtpr_sys.argv) > 1 and _vtpr_sys.argv[1] == "validate-topic-pack-release":
        import importlib.util as _vtpr_importlib_util
        from pathlib import Path as _vtpr_Path

        _vtpr_path = _vtpr_Path(__file__).resolve().parent / "validate_topic_pack_release.py"
        _vtpr_spec = _vtpr_importlib_util.spec_from_file_location(
            "_validate_topic_pack_release_module",
            _vtpr_path,
        )
        if _vtpr_spec is None or _vtpr_spec.loader is None:
            raise RuntimeError(f"cannot load {_vtpr_path}")

        _vtpr_mod = _vtpr_importlib_util.module_from_spec(_vtpr_spec)
        _vtpr_spec.loader.exec_module(_vtpr_mod)

        raise SystemExit(_vtpr_mod.main(_vtpr_sys.argv[2:]))
except SystemExit:
    raise
except Exception as _vtpr_exc:
    raise SystemExit(f"validate-topic-pack-release dispatch failed: {_vtpr_exc}")
# END_VALIDATE_TOPIC_PACK_RELEASE_COMMAND_PATCH


# VALIDATE_TOPIC_PACK_QUALITY_COMMAND_PATCH
# Lightweight early dispatch for topic_pack authoring quality validation.
try:
    import sys as _vtpq_sys
    if len(_vtpq_sys.argv) > 1 and _vtpq_sys.argv[1] == "validate-topic-pack-quality":
        import importlib.util as _vtpq_importlib_util
        from pathlib import Path as _vtpq_Path

        _vtpq_path = _vtpq_Path(__file__).resolve().parent / "validate_topic_pack_quality.py"
        _vtpq_spec = _vtpq_importlib_util.spec_from_file_location(
            "_validate_topic_pack_quality_module",
            _vtpq_path,
        )
        if _vtpq_spec is None or _vtpq_spec.loader is None:
            raise RuntimeError(f"cannot load {_vtpq_path}")

        _vtpq_mod = _vtpq_importlib_util.module_from_spec(_vtpq_spec)
        _vtpq_spec.loader.exec_module(_vtpq_mod)

        raise SystemExit(_vtpq_mod.main(_vtpq_sys.argv[2:]))
except SystemExit:
    raise
except Exception as _vtpq_exc:
    raise SystemExit(f"validate-topic-pack-quality dispatch failed: {_vtpq_exc}")
# END_VALIDATE_TOPIC_PACK_QUALITY_COMMAND_PATCH


# SMOKE_TOPIC_PACK_COMMAND_PATCH
# Lightweight early dispatch for topic-pack routing smoke.
try:
    import sys as _stpg_sys
    if len(_stpg_sys.argv) > 1 and _stpg_sys.argv[1] == "smoke-topic-pack":
        import importlib.util as _stpg_importlib_util
        from pathlib import Path as _stpg_Path

        _stpg_path = _stpg_Path(__file__).resolve().parent / "smoke_topic_pack.py"
        _stpg_spec = _stpg_importlib_util.spec_from_file_location(
            "_smoke_topic_pack_module",
            _stpg_path,
        )
        if _stpg_spec is None or _stpg_spec.loader is None:
            raise RuntimeError(f"cannot load {_stpg_path}")

        _stpg_mod = _stpg_importlib_util.module_from_spec(_stpg_spec)
        _stpg_spec.loader.exec_module(_stpg_mod)

        raise SystemExit(_stpg_mod.main(_stpg_sys.argv[2:]))
except SystemExit:
    raise
except Exception as _stpg_exc:
    raise SystemExit(f"smoke-topic-pack dispatch failed: {_stpg_exc}")
# END_SMOKE_TOPIC_PACK_COMMAND_PATCH



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
