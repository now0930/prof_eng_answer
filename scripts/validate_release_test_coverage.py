#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
RELEASE_SCRIPT = SCRIPTS_DIR / "validate_release.sh"


def main() -> int:
    if not RELEASE_SCRIPT.exists():
        print(
            "ERROR: release validation script is missing: "
            f"{RELEASE_SCRIPT}"
        )
        return 1

    release_text = RELEASE_SCRIPT.read_text(
        encoding="utf-8"
    )

    test_files = sorted(
        SCRIPTS_DIR.glob("test_*.py")
    )

    if not test_files:
        print("ERROR: no test modules found under scripts/")
        return 1

    missing: list[Path] = []

    print("=== Release test coverage validation ===")

    for path in test_files:
        relative = path.relative_to(ROOT).as_posix()
        module = relative.removesuffix(".py").replace("/", ".")

        covered = (
            relative in release_text
            or module in release_text
        )

        state = "COVERED" if covered else "MISSING"
        print(f"{state}: {relative}")

        if not covered:
            missing.append(path)

    print()
    print(f"test modules: {len(test_files)}")
    print(f"covered: {len(test_files) - len(missing)}")
    print(f"missing: {len(missing)}")

    if missing:
        print()
        print("ERROR: validate_release.sh omits test modules:")

        for path in missing:
            print(f"- {path.relative_to(ROOT)}")

        return 1

    print("ALL RELEASE TEST MODULES COVERED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
