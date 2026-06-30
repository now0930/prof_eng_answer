#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"

VALID_TYPES = {
    "COMPARE_SELECTION",
    "DIAGNOSIS_ACTION",
    "IMPLEMENTATION_EVALUATION",
    "PRINCIPLE_INTERPRETATION",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug_to_title(topic_id: str) -> str:
    return topic_id.replace("_", " ")


def split_topic_sections(text: str):
    pattern = re.compile(r"^##\s+(?:\d+[.]\s+)?([A-Za-z0-9_]+)\s*$", re.M)
    matches = list(pattern.finditer(text))
    sections = []
    for idx, match in enumerate(matches):
        topic_id = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections.append((topic_id, text[start:end]))
    return sections


def extract_subsection(section: str, heading: str) -> str:
    pattern = re.compile(r"^###\s+" + re.escape(heading) + r"\s*$", re.M)
    match = pattern.search(section)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^###\s+", section[start:], re.M)
    end = start + next_match.start() if next_match else len(section)
    return section[start:end].strip()


def first_nonempty(block: str) -> str:
    for line in block.splitlines():
        text = line.strip()
        if text:
            return text
    return ""


def bullet_lines(block: str):
    out = []
    for line in block.splitlines():
        text = line.strip()
        if text.startswith("- "):
            out.append(text[2:].strip())
    return out


def numbered_titles(block: str):
    out = []
    for line in block.splitlines():
        text = line.strip()
        match = re.match(r"^\d+[.)]\s+(.+)$", text)
        if match:
            title = match.group(1).strip()
            if not title.startswith("-"):
                out.append(title)
    return out


def parse_model_structure(block: str):
    expected = numbered_titles(block)
    outline = bullet_lines(block)

    if not expected:
        expected = ["배경", "핵심 원리", "구성 또는 절차", "적용 기준", "현장 고려사항"]

    if len(outline) < 4:
        for title in expected:
            outline.append(title + "를 기술사 답안 구조에 맞게 설명한다.")
            if len(outline) >= 4:
                break

    return expected[:8], outline[:12]


def terms_from_text(text: str):
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9_.+-]*|[가-힣]{2,}", text)
    seen = []
    for word in words:
        if word not in seen:
            seen.append(word)
    return seen[:8] or ["핵심", "원리", "적용"]


def parse_fact_anchors(block: str, topic_id: str):
    raw = []
    cur_name = None
    cur_expected = ""

    for line in block.splitlines():
        text = line.strip()
        match = re.match(r"^\d+[.)]\s+(.+)$", text)
        if match:
            if cur_name:
                raw.append((cur_name, cur_expected.strip()))
            cur_name = match.group(1).strip()
            cur_expected = ""
            continue
        if cur_name and text.startswith("- "):
            cur_expected += " " + text[2:].strip()

    if cur_name:
        raw.append((cur_name, cur_expected.strip()))

    anchors = []
    for idx, item in enumerate(raw[:5], 1):
        name, expected = item
        if not expected:
            expected = name + "를 사실 기반으로 설명한다."
        terms = terms_from_text(name + " " + expected)
        anchors.append({
            "id": "F" + str(idx),
            "name": name,
            "expected": expected,
            "core_terms": terms[:6],
            "support_terms": terms[6:12],
        })

    while len(anchors) < 5:
        idx = len(anchors) + 1
        anchors.append({
            "id": "F" + str(idx),
            "name": "핵심 fact " + str(idx),
            "expected": topic_id + "의 핵심 개념을 사실 기반으로 설명한다.",
            "core_terms": terms_from_text(topic_id),
            "support_terms": [],
        })

    return anchors


def derive_high_score_features(anchors):
    out = []
    for anchor in anchors[:3]:
        out.append(anchor["name"] + "를 정확한 용어와 현장 적용 관점으로 설명한다.")
    while len(out) < 3:
        out.append("핵심 원리, 한계, 적용 기준을 구분하여 설명한다.")
    return out[:5]


def existing_model_by_topic(model_bank):
    out = {}
    for answer in model_bank.get("answers", []):
        out[answer.get("topic_id")] = answer
    return out


def existing_fact_by_topic(fact_bank):
    out = {}
    for topic in fact_bank.get("topics", []):
        out[topic.get("topic_id")] = topic
    return out


def upsert_answer(model_bank, topic_id, qtype, question, expected, outline, anchors, risks):
    old = existing_model_by_topic(model_bank).get(topic_id, {})
    answer_id = topic_id + "_" + qtype + "_v1"

    item = dict(old)
    item["id"] = old.get("id", answer_id)
    item["topic_id"] = topic_id
    item["question_type"] = qtype
    item["title"] = old.get("title") or slug_to_title(topic_id)
    item["question_examples"] = old.get("question_examples") or ([question] if question else [])
    if question and question not in item["question_examples"]:
        item["question_examples"] = [question] + item["question_examples"]
    item["topic_aliases"] = old.get("topic_aliases") or []
    item["expected_structure"] = expected
    item["model_answer_outline"] = outline
    item["high_score_features"] = old.get("high_score_features") or derive_high_score_features(anchors)
    item["low_score_patterns"] = risks[:5] if risks else old.get("low_score_patterns") or [
        "핵심 용어를 정의하지 않고 나열만 하면 안 된다.",
        "적용 조건과 한계 조건을 누락하면 안 된다.",
        "현장 적용 기준 없이 원리만 설명하면 안 된다.",
    ]
    item["field_connection_points"] = old.get("field_connection_points") or []
    item["revision_notes"] = [
        "updated_at=" + datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "imported_from=review_design_markdown",
        "review design markdown에서 Model Answer와 Fact Anchor를 생성함.",
    ]

    answers = model_bank.setdefault("answers", [])
    for idx, answer in enumerate(answers):
        if answer.get("topic_id") == topic_id:
            answers[idx] = item
            return item
    answers.append(item)
    return item


def upsert_fact(fact_bank, topic_id, question, anchors):
    old = existing_fact_by_topic(fact_bank).get(topic_id, {})
    item = dict(old)
    item["topic_id"] = topic_id
    item["name"] = old.get("name") or slug_to_title(topic_id)
    item["triggers"] = old.get("triggers") or terms_from_text(question)[:8]
    item["aliases"] = old.get("aliases") or []
    item["anchors"] = anchors

    topics = fact_bank.setdefault("topics", [])
    for idx, topic in enumerate(topics):
        if topic.get("topic_id") == topic_id:
            topics[idx] = item
            return item
    topics.append(item)
    return item


def import_design(path):
    text = Path(path).read_text(encoding="utf-8")
    model_bank = load_json(MODEL_PATH)
    fact_bank = load_json(FACT_PATH)

    sections = split_topic_sections(text)
    if not sections:
        raise SystemExit("ERROR: design topic section not found")

    imported = 0

    for topic_id, section in sections:
        qtype = first_nonempty(extract_subsection(section, "question_type"))
        if qtype not in VALID_TYPES:
            print("skip, invalid question_type:", topic_id, qtype)
            continue

        question = first_nonempty(extract_subsection(section, "권장 문제 예시"))
        model_block = extract_subsection(section, "Model Answer 핵심 구조")
        fact_block = extract_subsection(section, "Fact Anchor 후보")
        risk_block = extract_subsection(section, "risk")

        expected, outline = parse_model_structure(model_block)
        anchors = parse_fact_anchors(fact_block, topic_id)
        risks = bullet_lines(risk_block)

        upsert_answer(model_bank, topic_id, qtype, question, expected, outline, anchors, risks)
        upsert_fact(fact_bank, topic_id, question, anchors)

        print("model upserted:", topic_id + "_" + qtype + "_v1")
        print("fact upserted:", topic_id)
        imported += 1

    save_json(MODEL_PATH, model_bank)
    save_json(FACT_PATH, fact_bank)
    print("imported topics:", imported)


def main():
    if len(sys.argv) != 2:
        print("usage: python3 scripts/import_review_design.py <review_design.md>")
        raise SystemExit(2)
    import_design(sys.argv[1])


if __name__ == "__main__":
    main()
