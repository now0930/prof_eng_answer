from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from study.master_topic_pack import MasterTopicPackError, load_master_topic_pack, load_legacy_topic_sources


def validate_directory(root: Path) -> int:
    master_dir = root / "master_topic_packs"
    paths = sorted(master_dir.glob("*.json"))
    if not paths:
        raise MasterTopicPackError(f"no Master Topic Packs found under {master_dir}")
    seen_topics: set[str] = set()
    for path in paths:
        master = load_master_topic_pack(path)
        if path.stem != master["topic_id"]:
            raise MasterTopicPackError(f"filename/topic_id mismatch: {path}")
        if master["topic_id"] in seen_topics:
            raise MasterTopicPackError(f"duplicate topic_id: {master['topic_id']}")
        seen_topics.add(master["topic_id"])
        load_legacy_topic_sources(root, master)
    return len(paths)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate additive Master Topic Pack records")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        count = validate_directory(args.root.resolve())
    except (MasterTopicPackError, OSError) as exc:
        print(f"MASTER_TOPIC_PACK_VALIDATION=FAIL: {exc}")
        return 2
    print(f"MASTER_TOPIC_PACK_VALIDATION=PASS count={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
