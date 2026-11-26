#!/usr/bin/env python3
"""Path-only guard against accidentally publishing known private data locations.

No secret/content scanning: review the diff and all outgoing commits separately.
"""
from __future__ import annotations

import argparse
import subprocess
import sys

PRIVATE_PREFIXES = (
    "data/sessions", "data/final_grade_cache", "data/user_settings",
    "data/wordpress_topic_packs", "data/fact_anchor_review_staging",
    "data/topic_learning_authoring", "data/topic_learning_synthesis",
    "reports/release_candidates", "reports/telegram_regrade_batches",
    "reports/fact_anchor_blocked_436_chatgpt_batches_20261104",
    "wordpress_docs", "private", "private_data", "data/private",
    "reports/private", "logs", "backups", "reports/backups",
)
PRIVATE_EXACT = {
    "data/state.json",
    "reports/fact_anchor_blocked_436_chatgpt_20261104.csv",
}
DB_ENDINGS = (".sqlite", ".sqlite3", ".db", ".dump")


def is_private_path(path: str) -> bool:
    path = path.casefold()
    parts = path.split("/")
    name = parts[-1]
    if path in PRIVATE_EXACT:
        return True
    if any(path == p or path.startswith(p + "/") for p in PRIVATE_PREFIXES):
        return True
    if name == ".env" or (name.startswith(".env.") and path != ".env.example"):
        return True
    if any(name.endswith(ext) or ext + "-" in name for ext in DB_ENDINGS):
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tree", help="Check a commit/tree instead of the index")
    args = parser.parse_args()
    if args.tree:
        cmd = ["git", "ls-tree", "-r", "--name-only", "-z", args.tree, "--"]
    else:
        cmd = ["git", "ls-files", "-z"]
    try:
        raw = subprocess.check_output(cmd)
    except (OSError, subprocess.CalledProcessError):
        print("Private path guard: Git inventory failed.", file=sys.stderr)
        return 2
    count = sum(is_private_path(p.decode("utf-8", "surrogateescape"))
                for p in raw.split(b"\0") if p)
    if count:
        # Do not print potentially sensitive file names into CI/public logs.
        print(f"Private path guard: {count} disallowed tracked path(s). "
              "Inspect the Git inventory locally; do not publish.", file=sys.stderr)
        return 1
    print("Private path guard: PASS (paths only; content/history not checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
