#!/usr/bin/env python3
from __future__ import annotations

import re
import shlex
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
RELEASE_SCRIPT = SCRIPTS_DIR / "validate_release.sh"

_ASSIGNMENT_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*=.*$"
)
_TEST_PATH_RE = re.compile(
    r"^scripts/test_[A-Za-z0-9_]+\.py$"
)
_TEST_MODULE_RE = re.compile(
    r"^(scripts\.test_[A-Za-z0-9_]+)"
)


def logical_shell_lines(text: str) -> list[str]:
    lines: list[str] = []
    buffer = ""

    for raw_line in text.splitlines():
        stripped = raw_line.rstrip()

        if stripped.endswith("\\"):
            buffer += stripped[:-1] + " "
            continue

        line = buffer + stripped
        buffer = ""

        if line.strip():
            lines.append(line)

    if buffer.strip():
        lines.append(buffer)

    return lines


def _command_start(tokens: list[str]) -> int | None:
    index = 0

    while (
        index < len(tokens)
        and _ASSIGNMENT_RE.match(tokens[index])
    ):
        index += 1

    if index >= len(tokens):
        return None

    return index


def _python_argument_start(
    tokens: list[str],
    command_index: int,
) -> int:
    index = command_index + 1

    while index < len(tokens):
        token = tokens[index]

        if token in {"-B", "-E", "-I", "-O", "-OO", "-s", "-S", "-u"}:
            index += 1
            continue

        if token in {"-W", "-X"}:
            index += 2
            continue

        break

    return index


def collect_executed_test_paths(
    release_text: str,
) -> set[str]:
    executed: set[str] = set()

    for line in logical_shell_lines(release_text):
        try:
            tokens = shlex.split(
                line,
                comments=True,
                posix=True,
            )
        except ValueError:
            continue

        if not tokens:
            continue

        command_index = _command_start(tokens)

        if command_index is None:
            continue

        command = Path(tokens[command_index]).name

        if command not in {"python", "python3"}:
            continue

        arg_index = _python_argument_start(
            tokens,
            command_index,
        )
        args = tokens[arg_index:]

        if not args:
            continue

        first = args[0]

        if _TEST_PATH_RE.match(first):
            executed.add(first)
            continue

        if len(args) >= 2 and args[:2] == ["-m", "unittest"]:
            for token in args[2:]:
                match = _TEST_MODULE_RE.match(token)

                if not match:
                    continue

                module = match.group(1)
                executed.add(
                    module.replace(".", "/") + ".py"
                )

            continue

        if len(args) >= 2 and args[:2] == ["-m", "pytest"]:
            for token in args[2:]:
                candidate = token.split("::", 1)[0]

                if _TEST_PATH_RE.match(candidate):
                    executed.add(candidate)

    return executed


def discover_test_paths(root: Path) -> list[str]:
    scripts_dir = root / "scripts"

    return sorted(
        path.relative_to(root).as_posix()
        for path in scripts_dir.glob("test_*.py")
    )


def find_missing_test_paths(
    root: Path,
    release_text: str,
) -> list[str]:
    discovered = discover_test_paths(root)
    executed = collect_executed_test_paths(
        release_text
    )

    return [
        path
        for path in discovered
        if path not in executed
    ]


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
    test_paths = discover_test_paths(ROOT)

    if not test_paths:
        print("ERROR: no test modules found under scripts/")
        return 1

    executed = collect_executed_test_paths(
        release_text
    )
    missing = find_missing_test_paths(
        ROOT,
        release_text,
    )

    print("=== Release test execution coverage validation ===")

    for path in test_paths:
        state = (
            "COVERED"
            if path in executed
            else "MISSING"
        )
        print(f"{state}: {path}")

    print()
    print(f"test modules: {len(test_paths)}")
    print(f"covered: {len(test_paths) - len(missing)}")
    print(f"missing: {len(missing)}")

    if missing:
        print()
        print(
            "ERROR: validate_release.sh does not execute "
            "test modules:"
        )

        for path in missing:
            print(f"- {path}")

        return 1

    print("ALL RELEASE TEST MODULES COVERED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
