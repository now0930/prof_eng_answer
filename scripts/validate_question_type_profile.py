import json
from pathlib import Path

path = Path("rubrics/question_types/default.json")
data = json.loads(path.read_text(encoding="utf-8"))

errors = []

types = data.get("types", [])
if len(types) != 10:
    errors.append(f"types 개수가 10개가 아님: {len(types)}")

ids = set()
for qt in types:
    qid = qt.get("id")
    if not qid:
        errors.append("id 없음")
        continue

    if qid in ids:
        errors.append(f"id 중복: {qid}")
    ids.add(qid)

    for key in ["name", "triggers", "c_lens", "c_required_elements", "weak_answer_pattern", "high_score_pattern"]:
        if key not in qt:
            errors.append(f"{qid}: {key} 없음")

    if not qt.get("triggers"):
        errors.append(f"{qid}: triggers 비어 있음")

    if not qt.get("c_required_elements"):
        errors.append(f"{qid}: c_required_elements 비어 있음")

if errors:
    print("INVALID")
    for e in errors:
        print("-", e)
    raise SystemExit(1)

print("VALID")
print("types:", len(types))
for qt in types:
    print("-", qt["id"], qt["name"])
