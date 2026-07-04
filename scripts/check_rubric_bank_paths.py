#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rubric_bank_paths import get_rubric_bank_report, require_rubric_bank_paths  # noqa: E402


def main() -> int:
    mode = os.getenv("RUBRIC_BANK_MODE", "legacy")

    try:
        require_rubric_bank_paths(mode)
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    print(json.dumps(get_rubric_bank_report(mode), ensure_ascii=False, indent=2))
    print()
    print(f"VALID: rubric bank paths mode={mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
