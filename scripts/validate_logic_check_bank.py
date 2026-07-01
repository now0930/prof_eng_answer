from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "rubrics" / "logic_checks" / "industrial_instrumentation_control.json"


def main() -> int:
    if not BANK.exists():
        print(f"ERROR: missing {BANK}")
        return 1

    data = json.loads(BANK.read_text(encoding="utf-8"))

    if not isinstance(data.get("topic_logic_checks"), list):
        print("ERROR: topic_logic_checks must be list")
        return 1

    ids = set()
    errors = 0

    for topic in data["topic_logic_checks"]:
        topic_id = topic.get("topic_id")
        if not topic_id:
            print("ERROR: topic_id missing")
            errors += 1
            continue

        for group in [
            "fatal_checks",
            "major_checks",
            "question_type_checks",
            "advanced_tradeoff_checks",
        ]:
            for check in topic.get(group, []):
                cid = check.get("id")
                if not cid:
                    print(f"ERROR: check id missing in {topic_id}/{group}")
                    errors += 1
                    continue

                full_id = f"{topic_id}:{cid}"
                if full_id in ids:
                    print(f"ERROR: duplicate id {full_id}")
                    errors += 1
                ids.add(full_id)

                if not check.get("message"):
                    print(f"ERROR: message missing in {full_id}")
                    errors += 1

    if errors:
        print(f"INVALID: errors={errors}")
        return 1

    print("VALID")
    print(f"bank: {BANK.relative_to(ROOT)}")
    print(f"topics: {len(data['topic_logic_checks'])}")
    print(f"checks: {len(ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
