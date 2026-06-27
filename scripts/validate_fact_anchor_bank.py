import json
from pathlib import Path

path = Path("rubrics/fact_anchors/industrial_instrumentation_control.json")
data = json.loads(path.read_text(encoding="utf-8"))

errors = []

topics = data.get("topics", [])
if not topics:
    errors.append("topics가 비어 있음")

ids = set()
for topic in topics:
    tid = topic.get("topic_id")
    if not tid:
        errors.append("topic_id 없음")
        continue

    if tid in ids:
        errors.append(f"topic_id 중복: {tid}")
    ids.add(tid)

    anchors = topic.get("anchors", [])
    if len(anchors) != 5:
        errors.append(f"{tid}: anchors 개수가 5개가 아님: {len(anchors)}")

    for a in anchors:
        for key in ["id", "name", "expected", "core_terms", "support_terms"]:
            if key not in a:
                errors.append(f"{tid}/{a.get('id')}: {key} 없음")

        if not a.get("core_terms"):
            errors.append(f"{tid}/{a.get('id')}: core_terms 비어 있음")

if errors:
    print("INVALID")
    for e in errors:
        print("-", e)
    raise SystemExit(1)

print("VALID")
print("topics:", len(topics))
for t in topics:
    print("-", t.get("topic_id"), t.get("name"))
