#!/usr/bin/env python3
"""Compare committed runtime banks with a fresh, isolated Topic Pack build."""

from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
import tempfile
from unittest.mock import patch

import build_generated_rubrics as builder
from validate_generated_rubrics import REQUIRED_GENERATED_FILES


def check_generated(generated_dir: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="topic_pack_generated_check_") as temporary:
        fresh_dir = Path(temporary)
        with patch.object(builder, "OUT_DIR", fresh_dir), contextlib.redirect_stdout(io.StringIO()):
            builder.main()

        differences = []
        for filename in REQUIRED_GENERATED_FILES:
            committed = generated_dir / filename
            fresh = fresh_dir / filename
            if not committed.is_file() or committed.read_bytes() != fresh.read_bytes():
                differences.append(filename)
        return differences


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--generated-dir",
        type=Path,
        default=builder.OUT_DIR,
        help="Directory containing the committed generated bank (default: repository bank)",
    )
    args = parser.parse_args()
    differences = check_generated(args.generated_dir)
    if differences:
        print("STALE GENERATED RUBRICS: " + ", ".join(differences))
        print("Regenerate with: python3 scripts/rubric_manager.py validate-topic-pack-release --all --promote-generated")
        return 1
    print(f"GENERATED RUBRICS FRESH: {len(REQUIRED_GENERATED_FILES)} files match a clean rebuild")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
