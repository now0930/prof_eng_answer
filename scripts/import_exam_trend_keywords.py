#!/usr/bin/env python3
import argparse
import datetime as dt
import html
import json
import re
import urllib.request
from pathlib import Path


DEFAULT_URL = "https://now0930.pe.kr/wordpress/%ea%b8%b0%ed%9a%8d-%ec%82%b0%ec%97%85%ea%b3%84%ec%b8%a1%ec%a0%9c%ec%96%b4%ea%b8%b0%ec%88%a0%ec%82%ac-%ea%b8%b0%ec%b6%9c-%eb%8d%b0%ec%9d%b4%ed%84%b0-%ec%a0%95%eb%b0%80-%eb%b6%84%ec%84%9d-%ec%b5%9c/"


def load_json(path):
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"required json not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def fetch_text(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return raw.decode("utf-8", errors="replace")


def clean_html(raw):
    text = html.unescape(raw)
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\xa0", " ")
    return text


def find_json_candidates_with_summary_table(text):
    objects = []
    marker = '"summary_table"'
    pos = 0

    while True:
        idx = text.find(marker, pos)
        if idx < 0:
            break

        start = text.rfind("{", 0, idx)
        if start < 0:
            pos = idx + len(marker)
            continue

        depth = 0
        in_str = False
        esc = False
        end = None

        for i in range(start, len(text)):
            ch = text[i]

            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue

            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break

        if end:
            candidate = text[start:end]
            try:
                obj = json.loads(candidate)
                if isinstance(obj, dict) and "summary_table" in obj:
                    objects.append(obj)
            except Exception:
                pass

        pos = idx + len(marker)

    return objects


def choose_payload(candidates, prefer):
    if not candidates:
        raise SystemExit("summary_table JSON 후보를 찾지 못했습니다.")

    if prefer == "first":
        return candidates[0]

    if prefer == "max-topics":
        return max(candidates, key=lambda x: len(x.get("summary_table", [])))

    if prefer == "max-count":
        def total_count(obj):
            return sum(int(r.get("count", 0) or 0) for r in obj.get("summary_table", []))
        return max(candidates, key=total_count)

    return candidates[0]


def slugify_keyword(keyword):
    mapping = {
        "제어": "control",
        "계측": "measurement",
        "센서": "sensor",
        "통신": "communication",
        "네트워크": "network",
        "밸브": "valve",
        "오차": "error",
        "정밀도": "precision",
        "방폭": "explosion_proof",
        "안전": "safety",
        "유량계": "flowmeter",
        "온도": "temperature",
        "압력": "pressure",
        "차압": "differential_pressure",
        "스마트팩토리": "smart_factory",
        "디지털트윈": "digital_twin",
    }

    text = keyword
    for k, v in mapping.items():
        text = text.replace(k, v)

    text = text.lower()
    text = re.sub(r"[^a-z0-9가-힣]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "topic"


def match_keyword_rule(keyword, aliases, keyword_rules):
    haystack = " ".join([keyword] + list(aliases or [])).lower()

    for rule in keyword_rules.get("rules", []):
        for m in rule.get("match", []):
            if str(m).lower() in haystack:
                return rule

    return keyword_rules.get("default", {
        "types": ["DEFINE", "PRINCIPLE", "APPLICATION", "PROBLEM_SOLVE"],
        "facts": ["정의", "동작 원리", "적용 조건", "현장 주의사항", "개선 방향"],
    })


def priority_band(score):
    if score >= 0.70:
        return "high"
    if score >= 0.45:
        return "medium"
    return "low"


def build_profile(row, max_count, keyword_rules, question_type_criteria):
    keyword = row.get("keyword", "")
    aliases = row.get("synonyms", []) or []
    count = int(row.get("count", 0) or 0)
    recent = row.get("recent5_presence", []) or []
    relative_freq = float(row.get("relative_freq", 0) or 0)

    rule = match_keyword_rule(keyword, aliases, keyword_rules)
    types = rule.get("types", [])
    facts = rule.get("facts", [])

    count_score = count / max_count if max_count else 0
    recent_score = min(len(recent), 5) / 5
    priority_score = round(count_score * 0.6 + recent_score * 0.4, 3)

    qtypes = question_type_criteria.get("types", question_type_criteria)

    type_profiles = {}
    for qtype in types:
        criteria = qtypes.get(qtype, {})
        type_profiles[qtype] = {
            "name": criteria.get("name", qtype),
            "c_lens": criteria.get("c_lens", []),
            "d_common": [
                "현장 적용 조건을 제시했는가",
                "기존 설비, 비용, 운전 리스크를 고려했는가",
                "대안 비교 또는 설계 판단을 포함했는가",
            ],
            "e_common": [
                "배경-문제 요구-Fact-현장 적용이 연결되는가",
                "면접 추가 질문에 방어 가능한 근거를 제시했는가",
            ],
        }

    return {
        "topic_id": slugify_keyword(keyword),
        "keyword": keyword,
        "aliases": aliases,
        "count": count,
        "relative_freq": relative_freq,
        "recent5_presence": recent,
        "priority_score": priority_score,
        "priority_band": priority_band(priority_score),
        "expected_question_types": types,
        "fact_focus": facts,
        "type_profiles": type_profiles,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--html-file", default="")
    ap.add_argument("--prefer", choices=["first", "max-count", "max-topics"], default="first")
    ap.add_argument("--keyword-rules", default="rubrics/keyword_rules/industrial_instrumentation_control.json")
    ap.add_argument("--question-type-criteria", default="rubrics/question_type_criteria/default.json")
    ap.add_argument("--raw-out", default="rubrics/exam_trends/industrial_instrumentation_control_raw.json")
    ap.add_argument("--profile-out", default="rubrics/keyword_question_profiles/industrial_instrumentation_control.json")
    args = ap.parse_args()

    keyword_rules = load_json(args.keyword_rules)
    question_type_criteria = load_json(args.question_type_criteria)

    raw = Path(args.html_file).read_text(encoding="utf-8") if args.html_file else fetch_text(args.url)

    text = clean_html(raw)
    candidates = find_json_candidates_with_summary_table(text)
    payload = choose_payload(candidates, args.prefer)

    summary = payload.get("summary_table", [])
    if not summary:
        raise SystemExit("summary_table is empty")

    max_count = max(int(r.get("count", 0) or 0) for r in summary) or 1

    profiles = [
        build_profile(row, max_count, keyword_rules, question_type_criteria)
        for row in summary
    ]

    out = {
        "schema_version": "keyword_question_profile_v1",
        "source_url": args.url,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "json_candidates_found": len(candidates),
        "prefer": args.prefer,
        "keyword_rules_file": args.keyword_rules,
        "question_type_criteria_file": args.question_type_criteria,
        "question_type_criteria": question_type_criteria.get("types", question_type_criteria),
        "profiles": profiles,
        "predicted_next": payload.get("predicted_next", []),
        "study_priority": payload.get("study_priority", {}),
    }

    raw_path = Path(args.raw_out)
    profile_path = Path(args.profile_out)

    raw_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.parent.mkdir(parents=True, exist_ok=True)

    raw_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    profile_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"JSON candidates found: {len(candidates)}")
    print(f"keywords imported: {len(profiles)}")
    print(f"raw json saved: {raw_path}")
    print(f"keyword profiles saved: {profile_path}")

    for p in profiles[:10]:
        print(f"- {p['keyword']} / {p['priority_band']} / {', '.join(p['expected_question_types'])}")


if __name__ == "__main__":
    main()
