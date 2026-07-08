from rubric_registry import load_fact_anchor_bank
#!/usr/bin/env python3
import json
import re
import traceback
from datetime import datetime
from pathlib import Path
from grading_config import load_active_config, save_active_config_snapshots


BASE_DIR = Path(__file__).resolve().parent
RATERS_FILE = BASE_DIR / "rubrics" / "raters" / "default.json"


DEFAULT_RATERS = [
    {
        "id": "professor",
        "name": "교수 채점자",
        "character": "",
        "focus": [],
        "scoring_style": "",
        "enabled": True
    },
    {
        "id": "professional_engineer",
        "name": "기술사 채점자",
        "character": "",
        "focus": [],
        "scoring_style": "",
        "enabled": True
    },
    {
        "id": "executive",
        "name": "회사 임원 채점자",
        "character": "",
        "focus": [],
        "scoring_style": "",
        "enabled": True
    }
]



def default_common_criteria():
    return [
        {
            "id": "answer_relevance",
            "name": "문제 요구사항 충족",
            "description": "문제가 요구한 사항에 직접 답했는지 본다.",
            "weight_hint": 20
        },
        {
            "id": "technical_accuracy",
            "name": "전문용어·핵심 키워드 정확성",
            "description": "전문용어와 핵심 키워드를 정확히 사용했는지 본다.",
            "weight_hint": 15
        },
        {
            "id": "logical_structure",
            "name": "논리 구조와 답안 구성",
            "description": "목차, 소제목, 전개, 결론이 체계적인지 본다.",
            "weight_hint": 15
        },
        {
            "id": "practical_application",
            "name": "실무 적용성",
            "description": "현장 적용 방법과 관리 관점이 있는지 본다.",
            "weight_hint": 15
        }
    ]


def load_rater_config():
    config = {
        "version": "fallback",
        "source_file": str(RATERS_FILE),
        "common_criteria": default_common_criteria(),
        "raters": DEFAULT_RATERS
    }

    if not RATERS_FILE.exists():
        return config

    try:
        data = json.loads(RATERS_FILE.read_text(encoding="utf-8"))

        common_criteria = data.get("common_criteria", [])
        if not isinstance(common_criteria, list) or not common_criteria:
            common_criteria = default_common_criteria()

        raters = data.get("raters", [])
        clean_raters = []

        if isinstance(raters, list):
            for r in raters:
                if not isinstance(r, dict):
                    continue
                if r.get("enabled", True) is False:
                    continue

                rid = str(r.get("id", "")).strip()
                name = str(r.get("name", "")).strip()

                if not rid or not name:
                    continue

                clean_raters.append({
                    "id": rid,
                    "name": name,
                    "character": str(r.get("character", "") or ""),
                    "focus": r.get("focus", []) if isinstance(r.get("focus", []), list) else [],
                    "scoring_style": str(r.get("scoring_style", "") or ""),
                    "enabled": True
                })

        if not clean_raters:
            clean_raters = DEFAULT_RATERS

        return {
            "version": data.get("version", "unknown"),
            "description": data.get("description", ""),
            "source_basis": data.get("source_basis", []),
            "scoring_targets": data.get("scoring_targets", {}),
            "source_file": str(RATERS_FILE),
            "common_criteria": common_criteria,
            "raters": clean_raters
        }

    except Exception:
        return config


def load_raters():
    return load_rater_config()["raters"]


def common_criteria_prompt_block(common_criteria):
    if not isinstance(common_criteria, list) or not common_criteria:
        common_criteria = default_common_criteria()

    lines = []
    for idx, c in enumerate(common_criteria, start=1):
        if not isinstance(c, dict):
            continue
        name = c.get("name", c.get("id", f"기준 {idx}"))
        desc = c.get("description", "")
        weight = c.get("weight_hint", "")
        lines.append(f"{idx}. {name}")
        lines.append(f"- 설명: {desc}")
        if weight != "":
            lines.append(f"- 비중 참고값: {weight}")
    return "\n".join(lines)


def extract_json(text):
    """
    LLM 응답에서 JSON object를 최대한 견고하게 추출한다.

    지원 범위:
    - raw JSON
    - ```json fenced block
    - 설명문 안에 포함된 첫 번째 {...}
    - 배열/객체 닫힘 누락 같은 일부 malformed JSON 자동 보정

    실패 시 None을 반환한다.
    """
    import json
    import re

    if text is None:
        return None

    raw = str(text).strip()
    if not raw:
        return None

    def strip_fence(value: str) -> str:
        value = value.strip()

        fenced = re.search(
            r"```(?:json|JSON)?\s*(.*?)```",
            value,
            flags=re.DOTALL,
        )
        if fenced:
            return fenced.group(1).strip()

        if value.startswith("```") and value.endswith("```"):
            lines = value.splitlines()
            if len(lines) >= 3:
                return "\n".join(lines[1:-1]).strip()

        return value

    def find_balanced_object(value: str) -> str | None:
        start_pos = value.find("{")
        if start_pos < 0:
            return None

        depth = 0
        in_string = False
        escape = False

        for i in range(start_pos, len(value)):
            ch = value[i]

            if escape:
                escape = False
                continue

            if ch == "\\":
                escape = True
                continue

            if ch == '"':
                in_string = not in_string
                continue

            if in_string:
                continue

            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return value[start_pos:i + 1]

        return value[start_pos:]

    def remove_trailing_commas(value: str) -> str:
        return re.sub(r",\s*([}\]])", r"\1", value)

    def escape_latex_backslashes_in_strings(value: str) -> str:
        """
        LLM이 JSON 문자열 안에 LaTeX 수식(\\omega, \\zeta, \\frac 등)을
        그대로 넣는 경우 json.loads가 실패하거나 문자열이 깨진다.

        JSON 문자열 내부에서 LaTeX 명령으로 보이는 backslash를
        literal backslash로 보존하기 위해 \\ 로 보정한다.
        단, quote/backslash/slash/unicode escape는 유지한다.
        """
        out = []
        in_string = False
        escape = False
        i = 0

        while i < len(value):
            ch = value[i]

            if escape:
                prev = "\\"
                nxt = ch
                after = value[i + 1] if i + 1 < len(value) else ""

                # JSON structural escapes that should remain as-is.
                if nxt in ['"', "\\", "/"]:
                    out.append(prev)
                    out.append(nxt)

                # Keep valid unicode escape as-is: \uXXXX
                elif nxt == "u" and i + 4 < len(value):
                    hex_part = value[i + 1:i + 5]
                    if all(c in "0123456789abcdefABCDEF" for c in hex_part):
                        out.append(prev)
                        out.append(nxt)
                    else:
                        out.append("\\\\")
                        out.append(nxt)

                # LaTeX commands such as \frac, \theta, \beta, \nu, \rho.
                # Some first letters overlap with JSON escapes.
                elif nxt.isalpha():
                    out.append("\\\\")
                    out.append(nxt)

                # Standard JSON escapes for non-LaTeX content.
                elif nxt in ["b", "f", "n", "r", "t"]:
                    out.append(prev)
                    out.append(nxt)

                # Invalid JSON escape: preserve literal backslash.
                else:
                    out.append("\\\\")
                    out.append(nxt)

                escape = False
                i += 1
                continue

            if ch == "\\" and in_string:
                escape = True
                i += 1
                continue

            if ch == '"':
                in_string = not in_string

            out.append(ch)
            i += 1

        if escape:
            out.append("\\\\")

        return "".join(out)

    def close_missing_containers(value: str) -> str:
        """
        모델이 배열을 닫지 않고 객체를 닫는 경우를 보정한다.
        예:
            "items": [
              "a",
              "b"
            },
        가 되어야 하는데
            "items": [
              "a",
              "b"
            },
        에서 ]가 빠져
            "items": [
              "a",
              "b"
            },
        비슷한 형태로 깨지는 경우를 복구한다.

        실제 동작:
        - '}'를 만났는데 stack top이 '['이면 먼저 ']'를 삽입한다.
        - 파일 끝에서 남은 stack을 닫는다.
        """
        out = []
        stack = []
        in_string = False
        escape = False

        for ch in value:
            if escape:
                out.append(ch)
                escape = False
                continue

            if ch == "\\":
                out.append(ch)
                escape = True
                continue

            if ch == '"':
                out.append(ch)
                in_string = not in_string
                continue

            if in_string:
                out.append(ch)
                continue

            if ch == "{":
                stack.append("{")
                out.append(ch)
                continue

            if ch == "[":
                stack.append("[")
                out.append(ch)
                continue

            if ch == "}":
                while stack and stack[-1] == "[":
                    out.append("]")
                    stack.pop()

                if stack and stack[-1] == "{":
                    stack.pop()

                out.append(ch)
                continue

            if ch == "]":
                while stack and stack[-1] == "{":
                    out.append("}")
                    stack.pop()

                if stack and stack[-1] == "[":
                    stack.pop()

                out.append(ch)
                continue

            out.append(ch)

        while stack:
            opener = stack.pop()
            out.append("}" if opener == "{" else "]")

        return "".join(out)

    def try_load(value: str):
        value = value.strip()
        if not value:
            return None

        try:
            return json.loads(value)
        except Exception:
            return None

    candidates = []

    fenced = strip_fence(raw)
    candidates.append(raw)
    candidates.append(fenced)

    obj = find_balanced_object(fenced)
    if obj:
        candidates.append(obj)

    obj_raw = find_balanced_object(raw)
    if obj_raw:
        candidates.append(obj_raw)

    expanded = []

    for candidate in candidates:
        if not candidate:
            continue

        repaired = close_missing_containers(candidate)
        repaired_no_trailing = remove_trailing_commas(repaired)

        expanded.append(candidate)
        expanded.append(remove_trailing_commas(candidate))
        expanded.append(repaired)
        expanded.append(repaired_no_trailing)

        escaped = escape_latex_backslashes_in_strings(candidate)
        escaped_repaired = close_missing_containers(escaped)
        escaped_repaired_no_trailing = remove_trailing_commas(escaped_repaired)

        expanded.append(escaped)
        expanded.append(remove_trailing_commas(escaped))
        expanded.append(escaped_repaired)
        expanded.append(escaped_repaired_no_trailing)

    seen = set()

    for candidate in expanded:
        candidate = candidate.strip()
        if not candidate or candidate in seen:
            continue

        seen.add(candidate)

        parsed = try_load(candidate)
        if parsed is not None:
            return parsed

    return None



def write_json(path, data):
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def clean_text(value, limit=300):
    if value is None:
        return ""
    text = str(value)
    text = text.replace("\\rightarrow", "→")
    text = text.replace("$ightarrow$", "→")
    text = text.replace("$", "")
    text = text.replace("\\", "")
    return text[:limit]


def short_list(values, limit=5):
    if not isinstance(values, list):
        return []
    return [clean_text(x, 120) for x in values[:limit]]


def rubric_items(rubric):
    items = rubric.get("items", []) if isinstance(rubric, dict) else []
    result = []

    for item in items:
        result.append({
            "name": item.get("name", "항목"),
            "points": float(item.get("points", 0)),
            "criteria": item.get("criteria", [])
        })

    return result


def rubric_total_points(rubric):
    if isinstance(rubric, dict):
        if "total_points" in rubric:
            return float(rubric["total_points"])
        items = rubric_items(rubric)
        if items:
            return sum(x["points"] for x in items)
    return 25.0


def scoring_targets(max_score):
    max_score = float(max_score)
    return {
        "official_pass_score": round(max_score * 0.60, 2),
        "practical_target_score": round(max_score * 0.70, 2),
        "high_score_target": round(max_score * 0.80, 2)
    }


def rater_prompt_block(raters):
    lines = []
    for idx, r in enumerate(raters, start=1):
        character = r.get("character") or "상세 캐릭터 미지정. 현재는 이름과 역할만 기준으로 보수적으로 채점한다."
        focus = r.get("focus") or []
        scoring_style = r.get("scoring_style") or "상세 채점 성향 미지정."

        lines.append(f"{idx}. {r['id']} / {r['name']}")
        lines.append(f"- character: {character}")
        lines.append(f"- focus: {', '.join(focus) if focus else '미지정'}")
        lines.append(f"- scoring_style: {scoring_style}")

    return "\n".join(lines)


def rater_output_template(raters, item_names):
    if not item_names:
        item_names = ["종합 평가"]

    rows = []
    for r in raters:
        rows.append({
            "rater_id": r["id"],
            "summary": f"{r['name']} 관점 총평",
            "scores": [
                {
                    "item": item_name,
                    "score": 0,
                    "reason": f"{r['name']} 관점에서 본 {item_name} 점수 사유"
                }
                for item_name in item_names
            ]
        })
    return rows


def build_prompt(raw_text, rubric, sid, image_count, raters, common_criteria=None):
    items = rubric_items(rubric)
    item_names = [x["name"] for x in items]
    max_score = rubric_total_points(rubric)
    targets = scoring_targets(max_score)
    first_item = item_names[0] if item_names else "종합 평가"
    rater_ids = [r["id"] for r in raters]

    return f"""
너는 기술사 논술형 답안 3인 채점위원회 분석 보조자다.
최종 grade.json은 Python 시스템이 만들 것이므로, 올바른 JSON 분석값만 작성한다.

3인이 공통으로 보는 기준:
{common_criteria_prompt_block(common_criteria)}

채점위원 명세:
{rater_prompt_block(raters)}

중요:
- 채점자 캐릭터는 rubrics/raters/default.json에서 관리된다.
- character, focus, scoring_style이 비어 있으면 이름과 역할만 기준으로 보수적으로 채점한다.
- 3인 공통 기준은 모든 채점자에게 동일하게 적용한다.
- 채점자 명세가 있으면 공통 기준 위에 각 채점자 성향으로 가중 판단한다.

점수 기준:
- 각 채점자는 {max_score}점 만점으로 채점한다.
- 공식 합격선: {targets["official_pass_score"]}점
- 실전 목표선: {targets["practical_target_score"]}점
- 고득점 기준: {targets["high_score_target"]}점

절대 규칙:
- 최상위 필드는 problem, subject, topic, question_type, demand_verbs, expected_structure, required_perspectives, expected_keywords, detected_keywords, detected_perspectives, evidence_quotes, missing_expected_parts, strengths, weaknesses, rewrite_advice, raters, one_line_summary, grade_confidence만 사용한다.
- analysis, feedback, revised_answer_template, revised_answer, template, answer_template 같은 임의 최상위 필드를 절대 쓰지 않는다.
- 모범답안, 수정답안, 예시답안은 출력하지 않는다.
- raters 배열에는 모든 채점자를 포함한다.
- 각 rater 객체는 rater_id, summary, scores만 사용한다.
- 각 rater의 scores 배열에는 rubric_items의 모든 항목을 빠짐없이 포함한다.
- 각 score는 0 이상 해당 항목 max 이하의 숫자여야 한다.
- JSON 하나만 출력한다.
- markdown code block을 쓰지 않는다.
- A, B, C 등급을 쓰지 않는다.
- 점수는 반드시 숫자로 쓴다.
- raters에는 다음 rater_id를 모두 포함한다: {json.dumps(rater_ids, ensure_ascii=False)}
- 각 채점자의 scores 배열에는 rubric_items의 모든 항목을 빠짐없이 포함한다.
- scores 배열에는 아래 rubric_items와 같은 항목명을 정확히 사용한다.
- scores 배열 원소는 반드시 object만 사용한다.
- scores 배열 안에 문자열을 넣지 않는다.
- OCR 답안에 없는 내용을 장점이나 점수 근거로 쓰지 않는다.

세션 ID: {sid}
첨부 이미지 수: {image_count}

rubric_items:
{json.dumps(item_names, ensure_ascii=False)}

rubric:
{json.dumps(rubric, ensure_ascii=False)}

사용자 원문:
{raw_text}

출력 JSON 형식:
{{
  "problem": "문제 원문",
  "subject": "추정 과목명 또는 unknown",
  "topic": "핵심 주제",
  "question_type": "explain|compare|discuss|countermeasure|procedure|cause_prevention|unknown",
  "demand_verbs": ["설명하시오"],
  "expected_structure": ["개념", "본론", "결론"],
  "required_perspectives": ["품질", "안전", "공정", "원가", "유지관리"],
  "expected_keywords": ["키워드1", "키워드2"],
  "detected_keywords": ["답안에 실제 있는 키워드"],
  "detected_perspectives": ["답안에 실제 있는 관점"],
  "evidence_quotes": ["답안에 실제 있는 짧은 근거 문장"],
  "missing_expected_parts": ["누락 항목"],
  "strengths": ["장점"],
  "weaknesses": ["약점"],
  "rewrite_advice": ["보완 방향"],
  "raters": {json.dumps(rater_output_template(raters, item_names), ensure_ascii=False, indent=2)},
  "one_line_summary": "한 줄 총평",
  "grade_confidence": "high|medium|low"
}}
""".strip()


def fallback_analysis():
    return {
        "problem": "",
        "subject": "unknown",
        "topic": "unknown",
        "question_type": "unknown",
        "demand_verbs": [],
        "expected_structure": [],
        "required_perspectives": [],
        "expected_keywords": [],
        "detected_keywords": [],
        "detected_perspectives": [],
        "evidence_quotes": [],
        "missing_expected_parts": [],
        "strengths": [],
        "weaknesses": ["모델 응답 JSON 파싱 실패"],
        "rewrite_advice": ["문제 요구 구조에 맞춰 답안을 재작성할 것"],
        "raters": [],
        "one_line_summary": "모델 분석 실패로 보수적 채점을 적용함.",
        "grade_confidence": "low"
    }


def build_question_analysis(analysis, rubric):
    return {
        "problem": clean_text(analysis.get("problem")),
        "point_allocated": rubric_total_points(rubric),
        "subject": clean_text(analysis.get("subject"), 80) or "unknown",
        "topic": clean_text(analysis.get("topic"), 80) or "unknown",
        "question_type": clean_text(analysis.get("question_type"), 40) or "unknown",
        "demand_verbs": short_list(analysis.get("demand_verbs"), 5),
        "expected_structure": short_list(analysis.get("expected_structure"), 5),
        "required_perspectives": short_list(analysis.get("required_perspectives"), 5),
        "expected_keywords": short_list(analysis.get("expected_keywords"), 8),
        "answer_text_detected": True,
        "analysis_confidence": clean_text(analysis.get("grade_confidence"), 20) or "medium",
        "notes": []
    }


def build_evidence(analysis):
    return {
        "detected_keywords": short_list(analysis.get("detected_keywords"), 10),
        "detected_structure": short_list(analysis.get("expected_structure"), 5),
        "detected_perspectives": short_list(analysis.get("detected_perspectives"), 5),
        "evidence_quotes": [
            {
                "quote": clean_text(q, 100),
                "supports": []
            }
            for q in short_list(analysis.get("evidence_quotes"), 3)
        ],
        "missing_expected_parts": short_list(analysis.get("missing_expected_parts"), 8),
        "missing_or_unclear": [],
        "answer_depth_assessment": "short",
        "evidence_confidence": clean_text(analysis.get("grade_confidence"), 20) or "medium"
    }


def get_rater_analysis(analysis, rater_id):
    raters = analysis.get("raters", [])
    if isinstance(raters, list):
        for r in raters:
            if isinstance(r, dict) and r.get("rater_id") == rater_id:
                return r
    return {
        "rater_id": rater_id,
        "summary": "모델이 해당 채점자 분석을 누락하여 보수적 기본 채점을 적용함.",
        "scores": []
    }


def score_map_from_rows(rows):
    result = {}
    if not isinstance(rows, list):
        return result

    for row in rows:
        if not isinstance(row, dict):
            continue

        item = clean_text(row.get("item"), 120).strip()
        if not item:
            continue

        try:
            score = float(row.get("score", 0))
        except Exception:
            score = 0.0

        result[item] = {
            "score": score,
            "reason": clean_text(row.get("reason"), 180)
        }

    return result


def find_score_for_item(score_map, item_name):
    if item_name in score_map:
        return score_map[item_name]

    for key, value in score_map.items():
        if item_name in key or key in item_name:
            return value

    return None


def build_breakdown(rater_analysis, rubric):
    items = rubric_items(rubric)
    max_total = rubric_total_points(rubric)
    score_map = score_map_from_rows(rater_analysis.get("scores", []))

    if not items:
        score = round(max_total * 0.52, 2)
        return score, [
            {
                "item": "종합 평가",
                "score": score,
                "max": max_total,
                "reason": "채점 항목이 없어 보수적 종합 점수를 적용함.",
                "evidence_used": []
            }
        ]

    breakdown = []
    for item in items:
        name = item["name"]
        max_item = item["points"]
        matched = find_score_for_item(score_map, name)

        if matched:
            score = max(0.0, min(float(matched["score"]), max_item))
            reason = matched["reason"] or "항목 기준에 따라 부분 점수 부여."
        else:
            score = round(max_item * 0.52, 2)
            reason = "모델이 해당 항목 점수를 누락하여 보수적 기본 점수를 적용함."

        breakdown.append({
            "item": name,
            "score": round(score, 2),
            "max": max_item,
            "reason": reason,
            "evidence_used": []
        })

    total = round(sum(float(x["score"]) for x in breakdown), 2)
    return total, breakdown


def average(values):
    values = list(values)
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)


def build_rater_results(analysis, rubric, raters):
    max_score = rubric_total_points(rubric)
    targets = scoring_targets(max_score)
    results = []

    for rater in raters:
        ra = get_rater_analysis(analysis, rater["id"])
        total, breakdown = build_breakdown(ra, rubric)

        results.append({
            "rater_id": rater["id"],
            "rater_name": rater["name"],
            "character": rater.get("character", ""),
            "focus": rater.get("focus", []),
            "scoring_style": rater.get("scoring_style", ""),
            "total_score": total,
            "max_score": max_score,
            "official_pass_score": targets["official_pass_score"],
            "official_pass_met": total >= targets["official_pass_score"],
            "practical_target_score": targets["practical_target_score"],
            "practical_target_met": total >= targets["practical_target_score"],
            "high_score_target": targets["high_score_target"],
            "high_score_met": total >= targets["high_score_target"],
            "summary": clean_text(ra.get("summary"), 220),
            "breakdown": breakdown
        })

    return results


def build_average_breakdown(rater_results, rubric):
    items = rubric_items(rubric)
    result = []

    for item in items:
        name = item["name"]
        scores = []
        for r in rater_results:
            for b in r.get("breakdown", []):
                if b.get("item") == name:
                    scores.append(float(b.get("score", 0)))

        result.append({
            "item": name,
            "score": average(scores),
            "max": item["points"],
            "reason": "채점자별 항목 점수 평균.",
            "evidence_used": []
        })

    return result


def build_grade(analysis, rubric, sid, question_analysis, evidence, raters):
    max_score = rubric_total_points(rubric)
    targets = scoring_targets(max_score)

    rater_results = build_rater_results(analysis, rubric, raters)
    totals = [float(r["total_score"]) for r in rater_results]
    avg_score = average(totals)

    official_met = avg_score >= targets["official_pass_score"]
    practical_met = avg_score >= targets["practical_target_score"]
    high_met = avg_score >= targets["high_score_target"]

    if practical_met:
        committee_summary = f"채점자 평균 {avg_score}/{max_score}로 실전 목표 {targets['practical_target_score']}점 이상입니다."
    elif official_met:
        committee_summary = f"채점자 평균 {avg_score}/{max_score}로 공식 합격선은 넘었지만 실전 목표에는 미달입니다."
    else:
        committee_summary = f"채점자 평균 {avg_score}/{max_score}로 공식 합격선 {targets['official_pass_score']}점 미만입니다."

    confidence = clean_text(analysis.get("grade_confidence"), 20) or "medium"
    if confidence not in ["high", "medium", "low"]:
        confidence = "medium"

    score_low = max(0, int(min(totals))) if totals else max(0, int(avg_score) - 2)
    score_high = min(int(max_score), int(max(totals))) if totals else min(int(max_score), int(avg_score) + 2)

    return {
        "session_id": sid,
        "rubric_type": "configurable_rater_committee_rubric",
        "rater_config_file": str(RATERS_FILE),
        "total_score": avg_score,
        "max_score": max_score,
        "score_range": f"{score_low}~{score_high}",
        "official_pass_score": targets["official_pass_score"],
        "practical_target_score": targets["practical_target_score"],
        "high_score_target": targets["high_score_target"],
        "passing_target_score": targets["official_pass_score"],
        "official_pass_met": official_met,
        "practical_target_met": practical_met,
        "high_score_met": high_met,
        "average_target_met": practical_met,
        "all_official_pass_met": all(r["official_pass_met"] for r in rater_results),
        "all_practical_target_met": all(r["practical_target_met"] for r in rater_results),
        "all_high_score_met": all(r["high_score_met"] for r in rater_results),
        "rater_results": rater_results,
        "grade_confidence": confidence,
        "one_line_summary": clean_text(analysis.get("one_line_summary"), 220) or committee_summary,
        "committee_summary": committee_summary,
        "breakdown": build_average_breakdown(rater_results, rubric),
        "strengths": short_list(analysis.get("strengths"), 5),
        "weaknesses": short_list(analysis.get("weaknesses"), 5),
        "missing_keywords": short_list(analysis.get("missing_expected_parts"), 8),
        "rewrite_advice": short_list(analysis.get("rewrite_advice"), 3),
        "model_answer_outline": question_analysis.get("expected_structure", []),
        "next_practice_focus": short_list(analysis.get("rewrite_advice"), 3),
        "audit_note": "채점자 캐릭터는 외부 JSON 명세에서 로드하며, 최종 점수는 Python이 채점자 평균으로 산출했습니다.",
        "question_analysis_summary": {
            "topic": question_analysis.get("topic"),
            "question_type": question_analysis.get("question_type"),
            "analysis_confidence": question_analysis.get("analysis_confidence")
        },
        "evidence_summary": {
            "detected_keywords": evidence.get("detected_keywords", []),
            "missing_expected_parts": evidence.get("missing_expected_parts", []),
            "evidence_confidence": evidence.get("evidence_confidence")
        },
        "agent_pipeline": {
            "version": "2026-06-27-agent-v5-configurable-raters",
            "logical_steps": [
                "load_rater_config",
                "question_analysis",
                "answer_evidence_extraction",
                "rater_analysis",
                "python_assembled_committee_grade"
            ],
            "physical_llm_calls": 1,
            "created_at": datetime.now().isoformat(timespec="seconds")
        }
    }



def flatten_text_values(value, limit=40):
    result = []

    def walk(x):
        if len(result) >= limit:
            return
        if isinstance(x, str):
            if x.strip():
                result.append(x.strip())
        elif isinstance(x, list):
            for y in x:
                walk(y)
        elif isinstance(x, dict):
            for y in x.values():
                walk(y)

    walk(value)
    return result


def normalize_analysis_schema(analysis):
    if not isinstance(analysis, dict):
        return fallback_analysis()

    # 모델이 우리가 요구한 schema 대신
    # {"analysis": ..., "feedback": ..., "model_answer_guidance": ...}
    # 형태로 응답한 경우를 표준 schema로 보정한다.
    nested_analysis = analysis.get("analysis", {})
    feedback = analysis.get("feedback", {})
    guidance = analysis.get("model_answer_guidance", {})
    revised = analysis.get("revised_answer_template", {})

    if isinstance(nested_analysis, dict):
        analysis.setdefault("topic", nested_analysis.get("topic", ""))
        analysis.setdefault("subject", nested_analysis.get("subject", "unknown"))
        analysis.setdefault("question_type", nested_analysis.get("question_type", "unknown"))

        keywords = nested_analysis.get("keywords", [])
        if isinstance(keywords, list):
            analysis.setdefault("expected_keywords", keywords)
            analysis.setdefault("detected_keywords", keywords)

        if nested_analysis.get("evaluation"):
            analysis.setdefault("one_line_summary", clean_text(nested_analysis.get("evaluation"), 220))

    if isinstance(feedback, dict):
        analysis.setdefault("strengths", feedback.get("strengths", []))
        analysis.setdefault("weaknesses", feedback.get("weaknesses", []))

        advice = feedback.get("improvement_suggestions", [])
        if not advice:
            advice = feedback.get("rewrite_advice", [])
        analysis.setdefault("rewrite_advice", advice)

        if feedback.get("overall_assessment"):
            analysis.setdefault("one_line_summary", clean_text(feedback.get("overall_assessment"), 220))

    expected_structure = analysis.get("expected_structure", [])
    if not expected_structure:
        if isinstance(guidance, dict) and guidance.get("structure"):
            expected_structure = [guidance.get("structure")]
        elif isinstance(revised, dict):
            expected_structure = list(revised.keys())[:5]
        else:
            expected_structure = ["정의", "원인", "영향", "대책", "결론"]
        analysis["expected_structure"] = expected_structure

    if not analysis.get("evidence_quotes"):
        quotes = []
        for x in flatten_text_values(feedback, 10):
            if len(x) <= 160:
                quotes.append(x)
        analysis["evidence_quotes"] = quotes[:3]

    analysis.setdefault("missing_expected_parts", analysis.get("weaknesses", [])[:5])
    analysis.setdefault("grade_confidence", "medium")
    analysis.setdefault("raters", analysis.get("raters", []))

    return analysis


def collect_keywords_from_rubric(rubric):
    profile = rubric.get("subject_profile", {}) if isinstance(rubric, dict) else {}
    keywords = []

    def add(value):
        if not value:
            return
        if isinstance(value, str):
            parts = [value]
            for sep in ["=", "/", ","]:
                new_parts = []
                for p in parts:
                    new_parts.extend(p.split(sep))
                parts = new_parts
            for p in parts:
                p = p.strip()
                if len(p) >= 2 and p not in keywords:
                    keywords.append(p)
        elif isinstance(value, list):
            for x in value:
                add(x)
        elif isinstance(value, dict):
            for x in value.values():
                add(x)

    for group in profile.get("keyword_groups", []):
        if isinstance(group, dict):
            add(group.get("keywords", []))

    add(profile.get("user_added_keywords", []))
    add(profile.get("weak_signal_keywords", []))

    pqa = profile.get("past_question_analysis", {})
    if isinstance(pqa, dict):
        for row in pqa.get("top_keywords", []):
            if isinstance(row, dict):
                add(row.get("keyword"))
                add(row.get("synonyms", []))
        for row in pqa.get("core_topics", []):
            if isinstance(row, dict):
                add(row.get("topic"))
                add(row.get("keywords", []))
        for row in pqa.get("predicted_next_topics", []):
            if isinstance(row, dict):
                add(row.get("topic"))
                add(row.get("keywords", []))

    return keywords


def item_specific_keywords(item_name, rubric):
    all_keywords = collect_keywords_from_rubric(rubric)
    name = str(item_name)

    if "계측" in name or "센서" in name or "전자측정" in name:
        markers = [
            "계측", "센서", "온도", "열전대", "RTD", "압력", "차압", "유량", "레벨",
            "오차", "정확도", "정밀도", "교정", "검교정", "4-20mA", "A/D", "D/A",
            "노이즈", "접지", "차폐", "불확도", "트랜스미터"
        ]
    elif "자동제어" in name or "제어시스템" in name:
        markers = [
            "제어", "제어시스템", "PID", "전달함수", "상태방정식", "안정도",
            "PLC", "DCS", "SCADA", "HMI", "인터록", "알람", "이중화",
            "피드백", "피드포워드", "응답", "보상기", "모터", "인버터"
        ]
    elif "계장" in name or "산업통신" in name or "안전" in name or "보안" in name:
        markers = [
            "계장", "P&ID", "Loop", "I/O", "제어밸브", "Control Valve", "Cv",
            "캐비테이션", "포지셔너", "밸브", "Modbus", "HART", "Profibus",
            "Profinet", "OPC UA", "IIoT", "SIS", "SIL", "ESD", "방폭",
            "OT 보안", "화이트리스트", "방화벽", "산업보안"
        ]
    elif "기술사적" in name or "논리" in name or "완성도" in name:
        markers = [
            "원인", "메커니즘", "영향", "대책", "장점", "단점", "한계",
            "유의사항", "결론", "리스크", "품질", "안전", "공정", "원가",
            "유지관리", "경제성", "신뢰성", "가용성"
        ]
    else:
        markers = all_keywords[:80]

    selected = []
    for k in all_keywords + markers:
        if not k:
            continue
        k = str(k).strip()
        if len(k) >= 2 and k not in selected:
            selected.append(k)

    return selected


def find_keyword_matches(text, keywords, limit=10):
    hay = str(text).lower()
    matches = []

    for k in keywords:
        kk = str(k).strip()
        if len(kk) < 2:
            continue
        if kk.lower() in hay and kk not in matches:
            matches.append(kk)
        if len(matches) >= limit:
            break

    return matches


def infer_item_score(raw_text, item_name, max_item, rubric):
    text = str(raw_text)
    keywords = item_specific_keywords(item_name, rubric)
    matches = find_keyword_matches(text, keywords, limit=12)

    structure_terms = [
        "정의", "원인", "메커니즘", "영향", "문제점", "대책", "방지", "결론",
        "또한", "따라서", "첫째", "둘째", "셋째", "유의사항", "적용"
    ]
    structure_hits = find_keyword_matches(text, structure_terms, limit=10)

    length = len(text)

    score = float(max_item) * 0.38

    if matches:
        score += min(len(matches), 7) * float(max_item) * 0.055
    else:
        score -= float(max_item) * 0.08

    if length >= 250:
        score += float(max_item) * 0.07
    if length >= 500:
        score += float(max_item) * 0.05
    if len(structure_hits) >= 3:
        score += float(max_item) * 0.06

    # 문제 요구사항 항목은 답안이 존재하고 관련 키워드가 있으면 최소한 부분점수를 인정
    if "문제 요구사항" in str(item_name) or "출제범위" in str(item_name):
        if length >= 120:
            score = max(score, float(max_item) * 0.55)
        if matches:
            score = max(score, float(max_item) * 0.62)

    # 완성도 항목은 구조가 약하면 상한을 낮춘다
    if "완성도" in str(item_name) or "논리" in str(item_name):
        if len(structure_hits) < 3:
            score = min(score, float(max_item) * 0.62)

    score = max(0.0, min(score, float(max_item) * 0.88))
    score = round(score, 2)

    if matches:
        reason = f"모델 점수 누락으로 Python 보정 채점. 답안에서 {', '.join(matches[:6])} 키워드를 확인하여 부분 점수를 부여함."
    else:
        reason = "모델 점수 누락으로 Python 보정 채점. 해당 항목의 직접 키워드가 부족하여 보수적으로 산정함."

    if structure_hits and ("완성도" in str(item_name) or "논리" in str(item_name)):
        reason += f" 구조 신호({', '.join(structure_hits[:4])})를 함께 고려함."

    return score, reason, matches


def ensure_rater_scores(analysis, rubric, raters, raw_text):
    if not isinstance(analysis, dict):
        analysis = fallback_analysis()

    items = rubric_items(rubric)
    if not items:
        items = [{"name": "종합 평가", "points": rubric_total_points(rubric), "criteria": []}]

    existing = {}
    for r in analysis.get("raters", []):
        if not isinstance(r, dict):
            continue
        rid = r.get("rater_id")
        if rid:
            existing[rid] = r

    feedback = analysis.get("feedback", {})
    base_summary = analysis.get("one_line_summary", "")
    if not base_summary and isinstance(feedback, dict):
        base_summary = feedback.get("overall_assessment", "")
    if not base_summary:
        base_summary = "모델이 채점자별 스키마를 지키지 않아 Python이 항목별 보정 채점을 수행함."

    fixed_raters = []

    for rater in raters:
        rid = rater["id"]
        old = existing.get(rid, {})
        old_scores = {}
        for row in old.get("scores", []):
            if isinstance(row, dict) and row.get("item"):
                old_scores[row.get("item")] = row

        scores = []
        for item in items:
            item_name = item["name"]
            max_item = float(item["points"])

            if item_name in old_scores:
                row = old_scores[item_name]
                try:
                    score = float(row.get("score", 0))
                except Exception:
                    score = 0.0
                score = max(0.0, min(score, max_item))
                reason = clean_text(row.get("reason"), 180) or "모델이 제공한 항목별 사유."
            else:
                score, reason, _matches = infer_item_score(raw_text, item_name, max_item, rubric)

            scores.append({
                "item": item_name,
                "score": score,
                "reason": reason
            })

        fixed_raters.append({
            "rater_id": rid,
            "summary": clean_text(old.get("summary") or base_summary, 220),
            "scores": scores
        })

    analysis["raters"] = fixed_raters

    # detected_keywords도 Python 기준으로 보강
    detected = analysis.get("detected_keywords", [])
    if not isinstance(detected, list):
        detected = []
    auto_matches = find_keyword_matches(raw_text, collect_keywords_from_rubric(rubric), limit=20)
    for k in auto_matches:
        if k not in detected:
            detected.append(k)
    analysis["detected_keywords"] = detected[:20]

    return analysis

def _legacy_run_agent_pipeline(call_ollama_fn, raw_text, rubric, sid, image_count, session_dir, progress_fn=None):
    session_dir = Path(session_dir)
    # Phase 1: load active grading configuration and save snapshots.
    active_config = load_active_config(BASE_DIR)
    save_active_config_snapshots(session_dir, active_config)
    print("[agent] active_profile, scoring_model, subject_rubric, layered_rater snapshots saved.")

    session_dir.mkdir(parents=True, exist_ok=True)

    def progress(msg):
        print(f"[agent] {msg}", flush=True)
        if progress_fn:
            try:
                progress_fn(msg)
            except Exception:
                pass

    rater_config = load_rater_config()
    raters = rater_config["raters"]
    common_criteria = rater_config.get("common_criteria", [])

    write_json(session_dir / "rubric_snapshot.json", rubric)
    write_json(session_dir / "rater_snapshot.json", {
        "source_file": str(RATERS_FILE),
        "config_version": rater_config.get("version"),
        "source_basis": rater_config.get("source_basis", []),
        "scoring_targets": rater_config.get("scoring_targets", {}),
        "common_criteria": common_criteria,
        "raters": raters
    })

    progress(f"1/4 채점자 명세 {len(raters)}명을 불러옵니다.")
    progress("2/4 문제 분석, 3/4 답안 근거 추출, 4/4 채점자별 채점을 수행합니다.")

    prompt = build_prompt(raw_text, rubric, sid, image_count, raters, common_criteria)

    (session_dir / "question_analysis_prompt.txt").write_text(prompt, encoding="utf-8")
    (session_dir / "evidence_prompt.txt").write_text(prompt, encoding="utf-8")
    (session_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

    raw_result = call_ollama_fn(prompt)

    (session_dir / "question_analysis_raw.txt").write_text(raw_result, encoding="utf-8")
    (session_dir / "evidence_raw.txt").write_text(raw_result, encoding="utf-8")
    (session_dir / "grade_raw.txt").write_text(raw_result, encoding="utf-8")

    analysis = extract_json(raw_result)
    if not isinstance(analysis, dict):
        analysis = fallback_analysis()
        progress("모델 분석 JSON 파싱에 실패하여 fallback 채점을 적용합니다.")

    analysis = normalize_analysis_schema(analysis)
    analysis = ensure_rater_scores(analysis, rubric, raters, raw_text)

    question_analysis = build_question_analysis(analysis, rubric)
    evidence = build_evidence(analysis)
    grade = build_grade(analysis, rubric, sid, question_analysis, evidence, raters)
    grade["common_criteria_snapshot"] = common_criteria

    write_json(session_dir / "question_analysis.json", question_analysis)
    write_json(session_dir / "evidence.json", evidence)
    write_json(session_dir / "grade.json", grade)

    progress("채점자별 채점 파이프라인이 완료되었습니다.")
    return raw_result, grade


# PHASE2_LAYERED_SCORING_WRAPPER
# 기존 채점 결과를 만든 뒤, active_profile/scoring_model 기준으로 A/B/C/D/E 후처리한다.

def _phase2_json_load(path, default=None):
    import json
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def _phase2_json_write(path, data):
    import json
    from pathlib import Path
    p = Path(path)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _phase2_latest_session_dir():
    from pathlib import Path
    base = Path(BASE_DIR) / "data" / "sessions"
    sessions = [p for p in base.glob("*") if p.is_dir()]
    if not sessions:
        return None
    return max(sessions, key=lambda p: p.stat().st_mtime)


def _phase2_text_stats(text):
    text = text or ""
    lines = [x for x in text.splitlines() if x.strip()]
    return {
        "char_count": len(text.strip()),
        "line_count": len(lines),
        "word_like_count": len(text.split())
    }


def _phase2_image_count(session_dir):
    from pathlib import Path
    img_dir = Path(session_dir) / "images"
    if not img_dir.exists():
        return 0
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    return len([p for p in img_dir.iterdir() if p.suffix.lower() in exts])


def _phase2_estimate_volume_level(answer_text, image_count=0):
    """답안 분량을 추정한다.

    정책:
    - 실제 업로드 이미지 장수(image_count)는 분량 계산에서 사용하지 않는다.
    - 답안 텍스트 안의 ASCII 표/도해 1개를 이미지 1장 분량으로 환산한다.
    - ASCII 표/도해 이미지 2장 분량을 답안지 1쪽으로 환산한다.
    - 1쪽 이하 또는 매우 짧은 텍스트는 cap 적용
    - 2쪽 이상으로 볼 수 있는 텍스트/ASCII 도해 답안은 분량만으로 감점하지 않음
    - Logic Check fatal cap은 이 함수가 아니라 별도 정책에서 처리함
    """
    _ = image_count  # 실제 업로드 이미지는 분량 계산에서 제외한다.

    text = str(answer_text or "").strip()
    lines = [line.rstrip() for line in text.splitlines()]
    nonempty_lines = [line.strip() for line in lines if line.strip()]
    line_count = len(nonempty_lines)
    compact_chars = len("".join(text.split()))

    def _is_ascii_visual_line(line):
        stripped = str(line or "").rstrip()
        if not stripped:
            return False

        if "+---" in stripped or "---+" in stripped:
            return True
        if stripped.count("|") >= 2:
            return True
        if "----" in stripped and ("+" in stripped or ">" in stripped):
            return True
        if "^ Im" in stripped or "-> Re" in stripped:
            return True

        visual_chars = sum(stripped.count(ch) for ch in "+-|_\\/^><")
        density = visual_chars / max(1, len(stripped))

        if len(stripped) >= 8 and density >= 0.28:
            return True

        return False

    def _count_ascii_visual_units(lines):
        """연속된 ASCII 표/도해 block을 이미지 장수로 환산한다.

        기준:
        - 감쇠비 비교 ASCII 표 정도를 이미지 1장으로 본다.
        - 큰 표/도해는 약 22줄당 이미지 1장으로 추가 환산한다.
        """
        units = 0
        block_lines = 0
        border_lines = 0

        def flush():
            nonlocal units, block_lines, border_lines
            if block_lines >= 6 or border_lines >= 3:
                units += max(1, (block_lines + 21) // 22)
            block_lines = 0
            border_lines = 0

        for line in list(lines) + [""]:
            if _is_ascii_visual_line(line):
                block_lines += 1
                if "+---" in line or "---+" in line or str(line).count("|") >= 2:
                    border_lines += 1
            else:
                flush()

        return units

    ascii_visual_units = _count_ascii_visual_units(lines)
    visual_pages = ascii_visual_units / 2.0

    if compact_chars < 500 and line_count <= 5 and ascii_visual_units == 0:
        return {
            "level": "text_only_short_answer",
            "estimated_answer_sheet_pages": 0,
            "cap": 9.0,
            "reason": "텍스트가 1~5줄 또는 500자 미만이므로 요약 답안 상한을 적용한다."
        }

    if compact_chars < 900 and line_count < 20:
        text_pages = 0.5
    elif compact_chars < 1500 and line_count < 45:
        text_pages = 1.0
    elif compact_chars < 2800 and line_count < 80:
        text_pages = 2.0
    else:
        text_pages = 3.0

    estimated_pages = max(text_pages, visual_pages)

    visual_note = ""
    if ascii_visual_units:
        visual_note = (
            f" ASCII 표/도해 {ascii_visual_units}개를 이미지 {ascii_visual_units}장 분량으로 환산하고, "
            f"ASCII 이미지 2장=답안지 1쪽 기준을 적용했다."
        )

    if estimated_pages < 1.0:
        return {
            "level": "less_than_one_page_text_ascii",
            "estimated_answer_sheet_pages": estimated_pages,
            "cap": 10.5,
            "reason": "답안 분량이 1쪽 미만 수준으로 판단되어 상한을 적용한다." + visual_note
        }

    if estimated_pages < 2.0:
        return {
            "level": "one_page_text_ascii",
            "estimated_answer_sheet_pages": estimated_pages,
            "cap": 13.0,
            "reason": "답안 분량이 1쪽 수준으로 판단되어 부분 답안 상한을 적용한다." + visual_note
        }

    if estimated_pages < 3.0:
        return {
            "level": "two_page_text_ascii",
            "estimated_answer_sheet_pages": estimated_pages,
            "cap": None,
            "reason": "답안 분량이 2쪽 수준으로 판단되며, 내용이 명확하면 분량만으로 감점하지 않는다." + visual_note
        }

    return {
        "level": "three_page_text_ascii",
        "estimated_answer_sheet_pages": estimated_pages,
        "cap": None,
        "reason": "답안 분량이 3쪽 이상 수준으로 판단되며, 분량만으로 감점하지 않는다." + visual_note
    }


def _phase2_has_any(text, terms):
    t = text or ""
    return any(term in t for term in terms)


def _phase2_count_terms(text, terms):
    t = text or ""
    found = []
    for term in terms:
        if term and term in t and term not in found:
            found.append(term)
    return found


def _phase2_score_ratio_by_terms(text, strong_terms, weak_terms=None):
    weak_terms = weak_terms or []
    strong = _phase2_count_terms(text, strong_terms)
    weak = _phase2_count_terms(text, weak_terms)

    score = 0.0
    score += min(len(strong) * 0.18, 0.75)
    score += min(len(weak) * 0.06, 0.20)

    if len(text.strip()) >= 250:
        score += 0.08
    if len(text.strip()) >= 700:
        score += 0.08
    if len(text.strip()) >= 1500:
        score += 0.05

    return min(score, 1.0), strong, weak


def _phase2_layer_scores(text, scoring_model):
    layers = scoring_model.get("layers", [])
    layer_by_id = {x.get("id"): x for x in layers}

    definitions = {
        "A": {
            "strong": ["배경", "개요", "정의", "목적", "필요성", "공정", "제어밸브", "계측", "제어"],
            "weak": ["설명", "관리", "운전"]
        },
        "B": {
            "strong": [
                "정의", "원리", "구성", "비교", "선정",
                "절차", "기준", "문제점", "원인", "대책",
                "적용", "평가"
            ],
            "weak": [
                "특징", "장단점", "조건", "영향",
                "검증", "결론"
            ]
        },
        "C": {
            "strong": ["압력", "차압", "국부", "포화증기압", "기포", "붕괴", "유속", "공동", "캐비테이션", "트림"],
            "weak": ["원리", "메커니즘", "정확도", "응답", "안정성", "신뢰성"]
        },
        "D": {
            "strong": ["대책", "방지", "개선", "설계", "사이징", "다단", "감압", "트림", "운전 조건", "유지보수", "정기보수"],
            "weak": ["비용", "시간", "적용", "기존 설비", "우선순위", "현실", "리스크"]
        },
        "E": {
            "strong": ["따라서", "그러므로", "결론", "우선", "단기", "중기", "장기", "검토", "판단"],
            "weak": ["면접", "근거", "한계", "조건"]
        }
    }

    result = []
    for layer_id in ["A", "B", "C", "D", "E"]:
        layer = layer_by_id.get(layer_id, {})
        max_points = float(layer.get("points", 0))
        name = layer.get("name", layer_id)
        d = definitions[layer_id]

        ratio, strong_found, weak_found = _phase2_score_ratio_by_terms(text, d["strong"], d["weak"])

        # 기본 보정: 짧은 답안은 각 항목 고득점 제한
        stats = _phase2_text_stats(text)
        if stats["char_count"] < 500:
            ratio = min(ratio, 0.55)
        if stats["line_count"] <= 5:
            ratio = min(ratio, 0.55)

        score = round(max_points * ratio, 2)

        if strong_found or weak_found:
            reason = "확인된 요소: " + ", ".join((strong_found + weak_found)[:8])
        else:
            reason = "해당 단계의 명확한 서술 근거가 부족함."

        result.append({
            "layer_id": layer_id,
            "item": f"{layer_id}. {name}",
            "score": score,
            "max": max_points,
            "reason": reason,
            "matched_terms": strong_found + weak_found
        })

    return result


def _phase2_apply_caps(layer_scores, volume):
    total_before = round(sum(float(x.get("score", 0)) for x in layer_scores), 2)
    cap = volume.get("cap")

    applied = []
    total_after = total_before

    if cap is not None and total_before > cap:
        scale = cap / total_before if total_before > 0 else 0
        for x in layer_scores:
            x["score_before_cap"] = x["score"]
            x["score"] = round(float(x["score"]) * scale, 2)
        total_after = round(sum(float(x.get("score", 0)) for x in layer_scores), 2)
        applied.append({
            "id": volume.get("level"),
            "cap": cap,
            "reason": volume.get("reason")
        })

    # Fact(C)가 낮으면 대책(D), 연결성(E)을 제한한다.
    by_id = {x.get("layer_id"): x for x in layer_scores}
    c = by_id.get("C")
    d = by_id.get("D")
    e = by_id.get("E")

    if c and d and e:
        c_score = float(c.get("score", 0))
        if c_score < 3.0:
            d_cap, e_cap = 2.0, 0.5
        elif c_score < 5.0:
            d_cap, e_cap = 3.0, 1.0
        elif c_score < 6.5:
            d_cap, e_cap = 4.5, 1.5
        else:
            d_cap, e_cap = None, None

        if d_cap is not None:
            if float(d.get("score", 0)) > d_cap:
                d["score_before_fact_cap"] = d["score"]
                d["score"] = d_cap
            if float(e.get("score", 0)) > e_cap:
                e["score_before_fact_cap"] = e["score"]
                e["score"] = e_cap
            applied.append({
                "id": "fact_score_limits_solution_and_connection",
                "reason": "Fact 기반 설명 점수가 낮아 대책 및 연결성 점수 상한을 적용함.",
                "c_score": c_score,
                "d_cap": d_cap,
                "e_cap": e_cap
            })

    total_after = round(sum(float(x.get("score", 0)) for x in layer_scores), 2)
    return total_before, total_after, applied


def _phase2_make_rater_results(total_score, max_score, raters):
    targets = {
        "official_pass_score": round(max_score * 0.60, 2),
        "practical_target_score": round(max_score * 0.70, 2),
        "high_score_target": round(max_score * 0.80, 2)
    }

    results = []
    for r in raters:
        rid = r.get("id")
        name = r.get("name", rid)

        if rid == "professor":
            perspective = "개념, 용어, fact 설명의 정확성을 중심으로 본 평가입니다."
        elif rid == "professional_engineer":
            perspective = "문제점, fact, 대책의 현장 연결성을 중심으로 본 평가입니다."
        elif rid == "executive":
            perspective = "비용, 시간, 적용 가능성, 기존 설비 영향 등 현실성을 중심으로 본 평가입니다."
        else:
            perspective = r.get("role", "")

        results.append({
            "rater_id": rid,
            "rater_name": name,
            "total_score": total_score,
            "max_score": max_score,
            "character": r.get("role", ""),
            "perspective": perspective,
            "official_pass_score": targets["official_pass_score"],
            "official_pass_met": total_score >= targets["official_pass_score"],
            "practical_target_score": targets["practical_target_score"],
            "practical_target_met": total_score >= targets["practical_target_score"],
            "high_score_target": targets["high_score_target"],
            "high_score_met": total_score >= targets["high_score_target"]
        })
    return results




def _phase2_add_display_aliases(grade):
    """
    bot.py의 기존 format_result가 기대하는 여러 key 이름을 함께 채워준다.
    채점 로직은 바꾸지 않고 Telegram 표시 누락만 보완한다.
    """
    if not isinstance(grade, dict):
        return grade

    summary = grade.get("summary") or grade.get("rater_summary") or ""
    confidence = grade.get("confidence") or "medium"

    grade["summary"] = summary
    grade["overall_comment"] = summary
    grade["overall_summary"] = summary
    grade["total_comment"] = summary
    grade["comment"] = summary

    grade["confidence"] = confidence
    grade["grade_confidence"] = confidence
    grade["confidence_level"] = confidence

    if grade.get("version") == "phase2_layered_scoring_v1":
        volume = grade.get("volume_evaluation") or {}
        volume_reason = volume.get("reason", "")
        if volume_reason:
            grade["grading_basis"] = volume_reason

    for r in grade.get("rater_results", []):
        perspective = (
            r.get("perspective")
            or r.get("character")
            or r.get("role")
            or ""
        )
        r["perspective"] = perspective
        r["comment"] = perspective
        r["reason"] = perspective
        r["character"] = r.get("character") or perspective

    return grade


# PHASE3_FACT_ANCHOR_SCORING
# C. 유형별 Fact 기반 내용 설명을 단순 키워드 매칭이 아니라 문제별 Fact Anchor 5개로 평가한다.

def _phase3_extract_question_text(raw_text):
    text = raw_text or ""
    if "답안:" in text:
        before = text.split("답안:", 1)[0]
    else:
        before = text

    if "문제:" in before:
        return before.split("문제:", 1)[1].strip()

    return before.strip()


def _phase3_extract_answer_text(raw_text):
    text = raw_text or ""
    if "답안:" in text:
        return text.split("답안:", 1)[1].strip()
    return text.strip()


def _phase3_contains_any(text, terms):
    text = text or ""
    return any(t in text for t in terms if t)


def _phase3_find_terms(text, terms):
    text = text or ""
    found = []
    for t in terms:
        if t and t in text and t not in found:
            found.append(t)
    return found



def _phase3_load_fact_anchor_bank(subject_rubric=None):
    import json
    from pathlib import Path

    candidates = []

    if isinstance(subject_rubric, dict):
        p = subject_rubric.get("fact_anchor_bank")
        if p:
            candidates.append(Path(p))

    candidates.extend([
        Path("rubrics/fact_anchors/industrial_instrumentation_control.json"),
        Path(__file__).resolve().parent / "rubrics" / "fact_anchors" / "industrial_instrumentation_control.json",
    ])

    for p in candidates:
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue

    return {"topics": []}


def _phase3_norm_text_for_anchor(text):
    return (text or "").lower().replace(" ", "").replace("_", "").replace("-", "")


def _phase3_anchor_term_matches(text, terms):
    raw = text or ""
    norm = _phase3_norm_text_for_anchor(raw)

    hits = []
    for term in terms or []:
        if not term:
            continue
        t_raw = str(term)
        t_norm = _phase3_norm_text_for_anchor(t_raw)

        if t_raw in raw or t_raw.lower() in raw.lower() or t_norm in norm:
            hits.append(t_raw)

    return hits



def _phase3_priority_value(value):
    """
    Fact Anchor topic priority를 정렬용 숫자로 변환한다.

    subject_rubric의 priority는 과거에는 숫자였지만,
    현재 profile에서는 "high" / "medium" / "low" 문자열일 수 있다.
    이 값은 anchor 후보 정렬의 tie-breaker로만 사용되므로
    실패시키지 않고 보수적으로 숫자화한다.
    """
    if value is None:
        return 0.0

    if isinstance(value, bool):
        return 1.0 if value else 0.0

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip().lower()

    label_map = {
        "critical": 4.0,
        "very_high": 4.0,
        "very-high": 4.0,
        "highest": 4.0,
        "high": 3.0,
        "medium": 2.0,
        "mid": 2.0,
        "normal": 2.0,
        "low": 1.0,
        "none": 0.0,
    }

    if text in label_map:
        return label_map[text]

    try:
        return float(text)
    except (TypeError, ValueError):
        return 0.0


def _phase3_select_fact_anchors_from_bank(question_text, answer_text, subject_rubric=None):
    bank = _phase3_load_fact_anchor_bank(subject_rubric)
    topics = bank.get("topics", [])

    combined = (question_text or "") + "\n" + (answer_text or "")

    scored = []
    for topic in topics:
        trigger_hits = _phase3_anchor_term_matches(combined, topic.get("triggers", []))
        alias_hits = _phase3_anchor_term_matches(combined, topic.get("aliases", []))

        if not trigger_hits:
            continue

        score = len(trigger_hits) * 10 + len(alias_hits) + _phase3_priority_value(topic.get("priority", 0)) / 100.0

        scored.append({
            "score": score,
            "topic": topic,
            "trigger_hits": trigger_hits,
            "alias_hits": alias_hits
        })

    if not scored:
        return None

    scored.sort(key=lambda x: x["score"], reverse=True)
    selected = scored[0]
    topic = selected["topic"]

    anchors = []
    for a in topic.get("anchors", []):
        aa = dict(a)
        aa["topic_id"] = topic.get("topic_id")
        aa["topic_name"] = topic.get("name")
        anchors.append(aa)

    return {
        "topic_id": topic.get("topic_id"),
        "topic_name": topic.get("name"),
        "source": "fact_anchor_bank",
        "trigger_hits": selected["trigger_hits"],
        "alias_hits": selected["alias_hits"],
        "anchors": anchors
    }

def _phase3_select_fact_anchors(question_text, answer_text, subject_rubric=None):
    q = question_text or ""
    a = answer_text or ""
    combined = q + "\n" + a

    bank_selected = _phase3_select_fact_anchors_from_bank(q, a, subject_rubric)
    if bank_selected:
        return bank_selected["anchors"]



    # Cv_VALVE_FLOW_COEFFICIENT_ANCHORS
    # Cv(Valve Flow Coefficient, 밸브 유량계수) 문제 전용 Fact Anchor
    combined_lower = combined.lower()
    if (
        "cv" in combined_lower
        or "c_v" in combined_lower
        or "유량계수" in combined
        or "flow coefficient" in combined_lower
        or "valve coefficient" in combined_lower
        or "밸브 coefficient" in combined_lower
    ):
        return [
            {
                "id": "F1",
                "name": "Cv의 정의",
                "expected": "Cv는 밸브의 유량 용량을 나타내는 유량계수이며, 밸브 사이징과 선정의 핵심 지표임을 설명한다.",
                "core_terms": ["Cv", "유량계수", "flow coefficient", "밸브 계수", "유량 용량", "용량계수"],
                "support_terms": ["제어밸브", "밸브", "사이징", "선정", "용량"]
            },
            {
                "id": "F2",
                "name": "표준 정의 조건",
                "expected": "Cv는 60°F 물이 밸브 전후 1 psi 차압에서 1분 동안 흐르는 US gpm 유량으로 정의된다는 표준 조건을 설명한다.",
                "core_terms": ["60°F", "60F", "물", "1 psi", "1psi", "gpm", "US gallon", "갤런"],
                "support_terms": ["차압", "분", "표준", "정의", "조건"]
            },
            {
                "id": "F3",
                "name": "유량·차압·비중 관계",
                "expected": "액체 기준 Q = Cv × sqrt(ΔP/SG) 또는 Cv = Q × sqrt(SG/ΔP) 관계를 설명하고, 유량은 Cv와 차압에 비례하고 비중에 영향을 받음을 설명한다.",
                "core_terms": ["Q", "ΔP", "차압", "SG", "비중", "sqrt", "제곱근", "루트"],
                "support_terms": ["유량", "압력강하", "압력 손실", "계산", "공식"]
            },
            {
                "id": "F4",
                "name": "밸브 선정과 제어성 영향",
                "expected": "Cv가 밸브 사이징, 개도, 제어성, 압력손실, 과대·과소 선정 문제와 연결됨을 설명한다.",
                "core_terms": ["사이징", "개도", "제어성", "압력손실", "과대", "과소", "선정"],
                "support_terms": ["헌팅", "분해능", "rangeability", "제어 불안정", "여유율"]
            },
            {
                "id": "F5",
                "name": "실무 적용 시 주의사항",
                "expected": "실제 적용에서는 유체 종류, 점도, 온도, 캐비테이션, 초크 유동, 배관 조건, 제조사 데이터, Kv와 단위 차이를 함께 검토해야 함을 설명한다.",
                "core_terms": ["점도", "온도", "캐비테이션", "초크", "choked", "배관", "제조사", "Kv", "단위"],
                "support_terms": ["실무", "검토", "보정", "조건", "데이터"]
            }
        ]

    # 1차 구현: 제어밸브 캐비테이션 문제를 명시 anchor로 처리.
    if _phase3_contains_any(combined, ["캐비테이션", "cavitation", "공동현상"]) and _phase3_contains_any(combined, ["제어밸브", "조절밸브", "Control Valve", "밸브"]):
        return [
            {
                "id": "F1",
                "name": "국부 압력 저하",
                "expected": "제어밸브 고차압 또는 유로 축소부에서 유속 증가로 국부 압력이 낮아지는 현상을 설명한다.",
                "core_terms": ["국부 압력", "압력 저하", "압력이 낮", "차압", "고차압", "유속", "축소부", "vena contracta"],
                "support_terms": ["제어밸브", "밸브", "유로", "압력"]
            },
            {
                "id": "F2",
                "name": "포화증기압 이하 기포 발생",
                "expected": "국부 압력이 액체의 포화증기압 이하가 되면 기포 또는 공동이 발생한다고 설명한다.",
                "core_terms": ["포화증기압", "증기압", "기포", "공동", "cavity", "발생"],
                "support_terms": ["액체", "압력", "낮"]
            },
            {
                "id": "F3",
                "name": "하류 압력 회복부 기포 붕괴",
                "expected": "하류 압력 회복 구간에서 기포가 급격히 붕괴하는 메커니즘을 설명한다.",
                "core_terms": ["하류", "압력 회복", "회복부", "기포 붕괴", "붕괴", "소멸"],
                "support_terms": ["압력", "기포"]
            },
            {
                "id": "F4",
                "name": "손상과 제어 문제",
                "expected": "기포 붕괴가 소음, 진동, 트림 침식, 밸브 손상, 제어 불안정을 유발한다고 설명한다.",
                "core_terms": ["소음", "진동", "침식", "손상", "트림", "제어 불안정", "불안정", "erosion"],
                "support_terms": ["밸브", "기포", "붕괴"]
            },
            {
                "id": "F5",
                "name": "방지대책의 설계 방향",
                "expected": "차압 분산, 다단 감압, anti-cavitation trim, 적정 사이징, 운전 조건 검토 등을 대책으로 연결한다.",
                "core_terms": ["차압", "다단", "감압", "방지 트림", "anti-cavitation", "사이징", "운전 조건", "트림"],
                "support_terms": ["대책", "방지", "적용", "검토"]
            }
        ]

    # 기본 anchor: 다른 문제에도 최소한 구조적으로 동작하게 한다.
    return [
        {
            "id": "F1",
            "name": "핵심 개념 정의",
            "expected": "문제의 핵심 기술 개념을 정확히 정의한다.",
            "core_terms": ["정의", "개념", "원리", "목적"],
            "support_terms": ["설명", "기술"]
        },
        {
            "id": "F2",
            "name": "발생 원인 또는 작동 원리",
            "expected": "문제에서 요구한 원인 또는 작동 원리를 인과관계로 설명한다.",
            "core_terms": ["원인", "발생", "원리", "메커니즘", "조건"],
            "support_terms": ["때문", "의해", "따라"]
        },
        {
            "id": "F3",
            "name": "문제점 또는 영향",
            "expected": "기술적 문제점, 품질·안전·운전 영향을 설명한다.",
            "core_terms": ["문제점", "영향", "위험", "고장", "품질", "안전", "운전"],
            "support_terms": ["리스크", "손실", "불안정"]
        },
        {
            "id": "F4",
            "name": "개선 또는 대책",
            "expected": "기술적으로 타당한 개선책 또는 대책을 제시한다.",
            "core_terms": ["대책", "개선", "방안", "방지", "설계", "관리"],
            "support_terms": ["적용", "검토", "선정"]
        },
        {
            "id": "F5",
            "name": "현실 적용 조건",
            "expected": "비용, 시간, 적용 가능성, 기존 설비 영향, 유지보수 조건을 고려한다.",
            "core_terms": ["비용", "시간", "적용 가능", "기존 설비", "유지보수", "정기보수"],
            "support_terms": ["현실", "우선순위", "리스크"]
        }
    ]



def _phase3_score_one_anchor(answer_text, anchor):
    """
    Fact Anchor 엄격 평가.

    0.0: 언급 없음
    0.3: 주변 키워드만 있음
    0.5: 핵심 키워드 일부만 있음
    0.6: 핵심 개념은 있으나 필수 조건/인과관계 부족
    0.8: 필수 조건과 인과관계가 대체로 맞음
    1.0: 핵심 개념, 조건, 인과관계, 문제 연결이 정확하고 간결함
    """
    text = answer_text or ""
    name = anchor.get("name", "")
    aid = anchor.get("id", "")

    core_found = _phase3_find_terms(text, anchor.get("core_terms", []))
    support_found = _phase3_find_terms(text, anchor.get("support_terms", []))

    def has_any(terms):
        return _phase3_contains_any(text, terms)

    level = 0.0
    judgement = "미언급"

    # F1. 국부 압력 저하
    if aid == "F1" or "국부 압력" in name:
        pressure_drop = has_any(["국부 압력", "압력 저하", "압력이 낮", "차압", "고차압"])
        mechanism = has_any(["유속", "축소부", "유로", "vena contracta"])

        if pressure_drop and mechanism:
            level = 0.9
            judgement = "압력 저하와 발생 조건을 대체로 설명"
        elif pressure_drop:
            level = 0.7
            judgement = "압력 저하 핵심은 언급했으나 메커니즘 설명은 부족"
        elif core_found:
            level = 0.5
            judgement = "관련 키워드 일부 언급"
        else:
            level = 0.0
            judgement = "미언급"

    # F2. 포화증기압 이하 기포 발생
    elif aid == "F2" or "포화증기압" in name:
        vapor_pressure = has_any(["포화증기압", "증기압"])
        bubble = has_any(["기포", "공동", "cavity"])
        below_condition = has_any(["이하", "낮", "저하"])

        if vapor_pressure and bubble and below_condition:
            level = 0.9
            judgement = "포화증기압 이하 조건과 기포 발생을 설명"
        elif vapor_pressure and bubble:
            level = 0.8
            judgement = "포화증기압과 기포 발생을 연결"
        elif bubble:
            level = 0.5
            judgement = "기포 발생은 언급했으나 포화증기압 조건 설명 부족"
        elif core_found:
            level = 0.4
            judgement = "관련 키워드 일부 언급"
        else:
            level = 0.0
            judgement = "미언급"

    # F3. 하류 압력 회복부 기포 붕괴
    elif aid == "F3" or "압력 회복" in name or "기포 붕괴" in name:
        collapse = has_any(["붕괴", "소멸", "collapse"])
        recovery = has_any(["하류", "압력 회복", "회복부"])
        rapid = has_any(["급격", "순간", "충격"])

        if collapse and recovery and rapid:
            level = 0.9
            judgement = "하류 압력 회복부의 급격한 기포 붕괴를 설명"
        elif collapse and recovery:
            level = 0.8
            judgement = "기포 붕괴 위치와 압력 회복 조건을 설명"
        elif collapse:
            level = 0.5
            judgement = "기포 붕괴는 언급했으나 하류 압력 회복 조건 설명 부족"
        elif core_found:
            level = 0.4
            judgement = "관련 키워드 일부 언급"
        else:
            level = 0.0
            judgement = "미언급"

    # F4. 손상과 제어 문제
    elif aid == "F4" or "손상" in name or "제어 문제" in name:
        symptom = _phase3_find_terms(text, ["소음", "진동"])
        damage = _phase3_find_terms(text, ["침식", "손상", "트림", "erosion"])
        control = _phase3_find_terms(text, ["제어 불안정", "불안정", "헌팅", "품질"])

        if symptom and damage and control:
            level = 0.9
            judgement = "소음·진동, 물리적 손상, 제어 문제를 모두 연결"
        elif symptom and damage:
            level = 0.75
            judgement = "소음·진동과 손상 영향을 설명"
        elif symptom:
            level = 0.6
            judgement = "소음·진동 영향은 설명했으나 손상·제어 문제 전개 부족"
        elif damage or control:
            level = 0.5
            judgement = "영향 일부 언급"
        else:
            level = 0.0
            judgement = "미언급"

    # F5. 방지대책의 설계 방향
    elif aid == "F5" or "방지대책" in name or "설계 방향" in name:
        pressure_solution = _phase3_find_terms(text, ["차압", "다단", "감압"])
        valve_solution = _phase3_find_terms(text, ["방지 트림", "anti-cavitation", "트림"])
        design_solution = _phase3_find_terms(text, ["사이징", "운전 조건", "밸브 선정", "Cv"])
        practical_solution = _phase3_find_terms(text, ["비용", "시간", "정기보수", "적용 가능", "기존 설비"])

        solution_groups = 0
        if pressure_solution:
            solution_groups += 1
        if valve_solution:
            solution_groups += 1
        if design_solution:
            solution_groups += 1
        if practical_solution:
            solution_groups += 1

        if solution_groups >= 4:
            level = 1.0
            judgement = "설계·운전·현실 적용 조건까지 대책을 제시"
        elif solution_groups == 3:
            level = 0.85
            judgement = "복수 대책과 설계 조건을 제시"
        elif solution_groups == 2:
            level = 0.65
            judgement = "대책 일부는 타당하나 설계 조건과 현실성 전개 부족"
        elif solution_groups == 1:
            level = 0.45
            judgement = "단일 대책 수준으로 제시"
        else:
            level = 0.0
            judgement = "미언급"

    # 일반 문제용 fallback
    else:
        core_count = len(core_found)
        support_count = len(support_found)

        if core_count == 0 and support_count == 0:
            level = 0.0
            judgement = "미언급"
        elif core_count == 0 and support_count > 0:
            level = 0.3
            judgement = "주변 키워드만 언급"
        elif core_count == 1:
            level = 0.5
            judgement = "핵심 일부 언급"
        elif core_count >= 2 and support_count >= 1:
            level = 0.7
            judgement = "핵심 개념 대체로 설명"
        elif core_count >= 2:
            level = 0.6
            judgement = "핵심 키워드는 있으나 설명 부족"

    # 매우 짧은 답안은 완전한 fact 설명으로 보지 않음
    if len(text.strip()) < 500:
        level = min(level, 0.8)

    return {
        "id": anchor.get("id"),
        "name": anchor.get("name"),
        "expected": anchor.get("expected"),
        "level": round(level, 2),
        "judgement": judgement,
        "core_terms_found": core_found,
        "support_terms_found": support_found
    }

def _phase3_evaluate_fact_anchors(raw_text, subject_rubric=None):
    question_text = _phase3_extract_question_text(raw_text)
    answer_text = _phase3_extract_answer_text(raw_text)

    anchors = _phase3_select_fact_anchors(question_text, answer_text, subject_rubric)
    results = [_phase3_score_one_anchor(answer_text, a) for a in anchors]

    avg = round(sum(x["level"] for x in results) / len(results), 3) if results else 0.0

    # C항목 8점 구성:
    # 핵심 개념 인지 3점, 정확한 설명 3점, 문제점 연결 1.5점, 간결성 0.5점
    concept_score = round(3.0 * avg, 2)

    accuracy_factor = avg
    if _phase3_contains_any(answer_text, ["포화증기압", "압력 회복", "하류", "침식", "사이징", "운전 조건"]):
        accuracy_factor = min(1.0, accuracy_factor + 0.1)
    accuracy_score = round(3.0 * accuracy_factor, 2)

    problem_link_factor = 0.0
    if _phase3_contains_any(answer_text, ["소음", "진동", "손상", "침식", "제어 불안정", "문제", "위험"]):
        problem_link_factor += 0.7
    if _phase3_contains_any(answer_text, ["따라서", "때문", "이로 인해", "유발", "발생"]):
        problem_link_factor += 0.3
    problem_link_score = round(1.5 * min(problem_link_factor, 1.0), 2)

    compactness_score = 0.5
    if len(answer_text.strip()) > 2500:
        compactness_score = 0.4
    if len(answer_text.strip()) < 80:
        compactness_score = 0.2

    total = round(concept_score + accuracy_score + problem_link_score + compactness_score, 2)
    total = min(total, 8.0)

    return {
        "version": "phase3_fact_anchor_v1",
        "question_text": question_text,
        "answer_char_count": len(answer_text.strip()),
        "anchor_count": len(results),
        "average_anchor_level": avg,
        "c_score": total,
        "c_score_detail": {
            "core_concept": concept_score,
            "accuracy": accuracy_score,
            "problem_link": problem_link_score,
            "compactness": compactness_score
        },
        "anchors": results
    }


def _phase3_evaluate_connections(raw_text):
    answer_text = _phase3_extract_answer_text(raw_text)

    background_terms = ["배경", "최근", "공정", "운전", "필요", "중요"]
    problem_terms = ["문제", "문제점", "원인", "소음", "진동", "손상", "불안정", "위험"]
    fact_terms = ["압력", "차압", "포화증기압", "기포", "붕괴", "원리", "메커니즘"]
    solution_terms = ["대책", "방지", "개선", "설계", "적용", "검토", "사이징", "운전 조건"]
    connector_terms = ["따라서", "그러므로", "이로 인해", "때문", "결과", "이를 위해", "우선"]

    has_background = _phase3_contains_any(answer_text, background_terms)
    has_problem = _phase3_contains_any(answer_text, problem_terms)
    has_fact = _phase3_contains_any(answer_text, fact_terms)
    has_solution = _phase3_contains_any(answer_text, solution_terms)
    has_connector = _phase3_contains_any(answer_text, connector_terms)

    def score_pair(a, b, name):
        if a and b and has_connector:
            return 1.0, f"{name} 연결이 명시적으로 드러남."
        if a and b:
            return 0.7, f"{name} 요소는 있으나 연결어가 약함."
        if a or b:
            return 0.3, f"{name} 한쪽 요소만 확인됨."
        return 0.0, f"{name} 연결 근거 부족."

    b_to_p, b_to_p_reason = score_pair(has_background, has_problem, "배경→문제 요구")
    p_to_f, p_to_f_reason = score_pair(has_problem, has_fact, "문제 요구→Fact")
    f_to_s, f_to_s_reason = score_pair(has_fact, has_solution, "Fact→현장 적용·제언")
    s_to_p, s_to_p_reason = score_pair(has_solution, has_problem, "제언→문제 요구 충족")

    avg = round((b_to_p + p_to_f + f_to_s + s_to_p) / 4, 3)

    return {
        "version": "phase3_connection_v1",
        "average_connection_level": avg,
        "e_score": round(2.0 * avg, 2),
        "checks": [
            {"id": "background_to_problem", "level": b_to_p, "reason": b_to_p_reason},
            {"id": "problem_to_fact", "level": p_to_f, "reason": p_to_f_reason},
            {"id": "fact_to_solution", "level": f_to_s, "reason": f_to_s_reason},
            {"id": "solution_to_problem", "level": s_to_p, "reason": s_to_p_reason}
        ]
    }


def _phase3_apply_fact_anchor_to_layer_scores(layer_scores, fact_eval):
    for item in layer_scores:
        if item.get("layer_id") == "C":
            item["score_before_fact_anchor"] = item.get("score")
            item["score"] = round(float(fact_eval.get("c_score", 0)), 2)
            item["reason"] = (
                f"Fact Anchor {fact_eval.get('anchor_count')}개 평가 평균 "
                f"{fact_eval.get('average_anchor_level')} 기준. "
                f"세부: {fact_eval.get('c_score_detail')}"
            )
            item["fact_anchor_summary"] = [
                {
                    "id": a.get("id"),
                    "name": a.get("name"),
                    "level": a.get("level"),
                    "judgement": a.get("judgement")
                }
                for a in fact_eval.get("anchors", [])
            ]
    return layer_scores


def _phase3_apply_connection_to_layer_scores(layer_scores, connection_eval):
    for item in layer_scores:
        if item.get("layer_id") == "E":
            item["score_before_connection_eval"] = item.get("score")
            item["score"] = round(float(connection_eval.get("e_score", 0)), 2)
            item["reason"] = (
                f"연결성 평균 {connection_eval.get('average_connection_level')} 기준. "
                + " / ".join(x.get("reason", "") for x in connection_eval.get("checks", []))
            )
    return layer_scores


def _phase3_make_interview_followup(fact_eval, connection_eval):
    questions = []

    for a in fact_eval.get("anchors", []):
        if float(a.get("level", 0)) < 0.8:
            questions.append(
                f"{a.get('name')}에 대해 면접에서 재질문 가능: {a.get('expected')}"
            )

    if float(connection_eval.get("average_connection_level", 0)) < 0.7:
        questions.append(
            "제시한 대책이 어떤 문제점을 해결하는지, 비용·시간·적용 가능성 관점에서 설명하시오."
        )

    return {
        "version": "phase3_interview_followup_v1",
        "questions": questions[:5]
    }


# PHASE4_RATER_WEIGHTED_SCORING
# 교수/기술사/기업 임원 점수를 동일 복사하지 않고 layer별 관점 차이를 반영한다.

def _phase4_rater_multiplier(rater_id, layer_id, grade):
    """
    rater별 layer 해석 차이.
    최종점수는 scoring_model.rater_weights_by_layer로 합성한다.
    """
    # 기본값
    table = {
        "professor": {
            "A": 1.00,
            "B": 1.08,
            "C": 1.10,
            "D": 0.85,
            "E": 0.95
        },
        "professional_engineer": {
            "A": 1.05,
            "B": 1.05,
            "C": 1.03,
            "D": 1.03,
            "E": 1.08
        },
        "executive": {
            "A": 0.95,
            "B": 0.85,
            "C": 0.82,
            "D": 1.10,
            "E": 1.02
        }
    }

    mult = table.get(rater_id, {}).get(layer_id, 1.0)

    # 현실성 요소가 거의 없으면 임원 D 점수는 가중을 낮춘다.
    if rater_id == "executive" and layer_id == "D":
        text_stats = grade.get("answer_text_stats") or {}
        weaknesses = " ".join(str(x) for x in grade.get("weaknesses", []))
        if text_stats.get("char_count", 0) < 500:
            mult = min(mult, 0.90)
        if "비용" not in weaknesses and "시간" not in weaknesses:
            # 약점 문구가 아니라 실제 답안에서 현실성 부족을 더 엄격히 보는 용도
            pass

    return mult


def _phase4_rater_layer_comment(rater_id, layer_id):
    comments = {
        "professor": {
            "A": "문제 진입과 개념 정의의 적절성을 봄.",
            "B": "문제 요구 해석·완전성의 개념적 정확성을 중점 평가함.",
            "C": "핵심 fact anchor와 용어 정확성을 중점 평가함.",
            "D": "대책의 이론적 타당성은 보되 현실 제약 평가는 제한적으로 반영함.",
            "E": "논리 연결과 설명 일관성을 평가함."
        },
        "professional_engineer": {
            "A": "현장 문제로 들어가는 흐름을 평가함.",
            "B": "문제점이 실제 설비·운전 문제로 정의되었는지 평가함.",
            "C": "fact 설명이 현장 문제를 설명하기에 충분한지 평가함.",
            "D": "대책이 설계·운전·유지보전에 적용 가능한지 평가함.",
            "E": "문제점, fact, 대책의 연결성과 면접 방어 가능성을 평가함."
        },
        "executive": {
            "A": "문제의 사업·운영상 중요성을 봄.",
            "B": "문제점이 운영 리스크로 명확히 드러나는지 평가함.",
            "C": "세부 이론보다 의사결정에 필요한 fact인지 평가함.",
            "D": "비용, 시간, 적용 가능성, 기존 설비 영향, 리스크 저감을 중점 평가함.",
            "E": "대책이 실제 문제 해결과 우선순위 판단으로 연결되는지 평가함."
        }
    }
    return comments.get(rater_id, {}).get(layer_id, "")


def _phase4_cap_layer_score(score, max_score):
    try:
        score = float(score)
        max_score = float(max_score)
    except Exception:
        return 0.0
    return round(max(0.0, min(score, max_score)), 2)


def _phase4_make_weighted_rater_matrix(grade, scoring_model, rater_profile):
    layer_scores = grade.get("breakdown", [])
    raters = []
    if rater_profile:
        raters = [r for r in rater_profile.get("raters", []) if r.get("enabled", True)]

    rater_layer_map = {}
    rater_results = []

    max_score = float(scoring_model.get("total_points", grade.get("max_score", 25)))
    official = round(max_score * 0.60, 2)
    practical = round(max_score * 0.70, 2)
    high = round(max_score * 0.80, 2)

    volume = grade.get("volume_evaluation") or {}
    volume_cap = volume.get("cap")

    for r in raters:
        rid = r.get("id")
        rname = r.get("name", rid)
        r_layers = []
        r_total = 0.0

        for layer in layer_scores:
            layer_id = layer.get("layer_id")
            base_score = float(layer.get("score", 0))
            layer_max = float(layer.get("max", 0))
            mult = _phase4_rater_multiplier(rid, layer_id, grade)
            r_score = _phase4_cap_layer_score(base_score * mult, layer_max)

            r_layers.append({
                "layer_id": layer_id,
                "item": layer.get("item"),
                "score": r_score,
                "max": layer_max,
                "base_score": base_score,
                "multiplier": mult,
                "comment": _phase4_rater_layer_comment(rid, layer_id)
            })
            r_total += r_score

        # 짧은 답안 volume cap은 채점자별 총점에도 적용
        if volume_cap is not None and r_total > float(volume_cap):
            scale = float(volume_cap) / r_total if r_total > 0 else 0
            for x in r_layers:
                x["score_before_volume_cap"] = x["score"]
                x["score"] = round(x["score"] * scale, 2)
            r_total = sum(x["score"] for x in r_layers)

        r_total = round(r_total, 2)
        rater_layer_map[rid] = r_layers

        if rid == "professor":
            perspective = "개념, 용어, fact anchor의 정확성을 중심으로 평가했습니다."
        elif rid == "professional_engineer":
            perspective = "문제점, fact, 대책의 현장 연결성과 설계 가능성을 중심으로 평가했습니다."
        elif rid == "executive":
            perspective = "비용, 시간, 적용 가능성, 기존 설비 영향, 운영 리스크 관점에서 평가했습니다."
        else:
            perspective = r.get("role", "")

        rater_results.append({
            "rater_id": rid,
            "rater_name": rname,
            "total_score": r_total,
            "max_score": max_score,
            "character": r.get("role", perspective),
            "perspective": perspective,
            "layer_scores": r_layers,
            "official_pass_score": official,
            "official_pass_met": r_total >= official,
            "practical_target_score": practical,
            "practical_target_met": r_total >= practical,
            "high_score_target": high,
            "high_score_met": r_total >= high
        })

    return rater_results, rater_layer_map


def _phase4_apply_rater_weighted_scoring(grade, scoring_model, rater_profile):
    if not isinstance(grade, dict):
        return grade

    weights_by_layer = scoring_model.get("rater_weights_by_layer", {})
    layer_scores = grade.get("breakdown", [])

    if not weights_by_layer or not layer_scores or not rater_profile:
        return grade

    rater_results, rater_layer_map = _phase4_make_weighted_rater_matrix(
        grade,
        scoring_model,
        rater_profile
    )

    # layer별 3인 가중 합성
    weighted_layers = []
    for layer in layer_scores:
        layer_id = layer.get("layer_id")
        weights = weights_by_layer.get(layer_id, {})

        weighted_score = 0.0
        weight_sum = 0.0

        for rid, w in weights.items():
            r_layers = rater_layer_map.get(rid, [])
            match = next((x for x in r_layers if x.get("layer_id") == layer_id), None)
            if match:
                weighted_score += float(match.get("score", 0)) * float(w)
                weight_sum += float(w)

        if weight_sum > 0:
            weighted_score = weighted_score / weight_sum
        else:
            weighted_score = float(layer.get("score", 0))

        new_layer = dict(layer)
        new_layer["score_before_rater_weight"] = layer.get("score")
        new_layer["score"] = round(weighted_score, 2)
        new_layer["rater_weighted"] = True
        new_layer["reason"] = (
            str(layer.get("reason", ""))
            + " / 3인 채점자 layer 가중 합성을 적용함."
        )
        weighted_layers.append(new_layer)

    weighted_total = round(sum(float(x.get("score", 0)) for x in weighted_layers), 2)

    # 최종 점수도 volume cap 초과 금지
    volume = grade.get("volume_evaluation") or {}
    volume_cap = volume.get("cap")
    applied = list(grade.get("applied_caps", []))

    if volume_cap is not None and weighted_total > float(volume_cap):
        scale = float(volume_cap) / weighted_total if weighted_total > 0 else 0
        for x in weighted_layers:
            x["score_before_final_volume_cap"] = x["score"]
            x["score"] = round(float(x["score"]) * scale, 2)

        weighted_total = round(sum(float(x.get("score", 0)) for x in weighted_layers), 2)
        applied.append({
            "id": "phase4_final_volume_cap",
            "cap": float(volume_cap),
            "reason": "3인 가중 합성 후에도 답안지 분량 상한을 초과하지 않도록 최종 cap을 적용함."
        })

    max_score = float(scoring_model.get("total_points", grade.get("max_score", 25)))
    official = round(max_score * 0.60, 2)
    practical = round(max_score * 0.70, 2)
    high = round(max_score * 0.80, 2)

    grade["version"] = "phase4_rater_weighted_v1"
    grade["breakdown"] = weighted_layers
    grade["rater_results"] = rater_results
    grade["rater_weighted_evaluation"] = {
        "version": "phase4_rater_weighted_v1",
        "weights_by_layer": weights_by_layer,
        "rater_layer_map": rater_layer_map,
        "weighted_layers": weighted_layers
    }

    grade["total_score"] = weighted_total
    grade["score_range"] = f"{int(weighted_total)}~{int(weighted_total)}"
    grade["official_pass_score"] = official
    grade["official_pass_met"] = weighted_total >= official
    grade["practical_target_score"] = practical
    grade["practical_target_met"] = weighted_total >= practical
    grade["high_score_target"] = high
    grade["high_score_met"] = weighted_total >= high
    grade["applied_caps"] = applied

    avg_rater = round(
        sum(float(r.get("total_score", 0)) for r in rater_results) / len(rater_results),
        2
    ) if rater_results else weighted_total

    grade["rater_summary"] = (
        f"교수·기술사·기업 임원 관점을 layer별 가중치로 합성했습니다. "
        f"3인 단순 평균은 {avg_rater}/{max_score}점, 최종 가중 점수는 {weighted_total}/{max_score}점입니다."
    )
    grade["summary"] = (
        f"A/B/C/D/E 구조, fact anchor, 연결성, 답안지 분량 cap, 3인 layer 가중 합성을 적용해 "
        f"{weighted_total}/{max_score}점으로 산정했습니다."
    )

    return grade


# PHASE6_GEMINI_SEMANTIC_GRADER
# Gemini가 A/B/C/D/E 의미 기반 원점수를 평가하고, Python은 cap/검증/3인 가중치를 적용한다.

def _phase6_clamp_score(score, max_score):
    try:
        score = float(score)
        max_score = float(max_score)
    except Exception:
        return 0.0
    return round(max(0.0, min(score, max_score)), 2)


def _phase6_get_layer_max(scoring_model):
    return {
        str(x.get("id")): float(x.get("points", 0))
        for x in scoring_model.get("layers", [])
    }


def _phase6_apply_gemini_layer_scores(layer_scores, gemini_eval, scoring_model):
    if not gemini_eval or not gemini_eval.get("ok"):
        return layer_scores

    parsed = gemini_eval.get("parsed") or {}
    gemini_layers = parsed.get("layers") or []
    max_by_layer = _phase6_get_layer_max(scoring_model)

    gemini_by_id = {
        str(x.get("layer_id")): x
        for x in gemini_layers
        if x.get("layer_id")
    }

    out = []
    for layer in layer_scores:
        layer_id = str(layer.get("layer_id"))
        g = gemini_by_id.get(layer_id)
        new_layer = dict(layer)

        if g:
            max_score = max_by_layer.get(layer_id, float(layer.get("max", 0)))
            g_score = _phase6_clamp_score(g.get("score", 0), max_score)

            score_guard = _phase6_limit_gemini_score(
                layer_id=layer_id,
                base_score=layer.get("score", 0),
                gemini_score=g_score,
                max_score=max_score,
            )
            effective_score = score_guard["effective_score"]

            new_layer["score_before_gemini"] = score_guard["base_score"]
            new_layer["score"] = effective_score
            new_layer["gemini_semantic_raw_score"] = (
                score_guard["raw_gemini_score"]
            )
            new_layer["gemini_semantic_score"] = effective_score
            new_layer["gemini_raise_cap"] = score_guard["raise_cap"]
            new_layer["gemini_adjustment_limited"] = (
                score_guard["raise_limited"]
            )
            new_layer["gemini_reason"] = g.get("reason", "")
            new_layer["gemini_evidence"] = g.get("evidence", [])

            limit_note = ""
            if score_guard["raise_limited"]:
                limit_note = (
                    f" / Gemini 상향폭을 {score_guard['raise_cap']}점으로 "
                    "제한함."
                )

            new_layer["reason"] = (
                f"Gemini 의미 평가: {g.get('reason', '')} "
                f"/ 기존 휴리스틱 근거: {layer.get('reason', '')}"
                f"{limit_note}"
            )

        out.append(new_layer)

    return out



# Gemini semantic grader는 기존 deterministic/fact 점수를 보완한다.
# 점수 하향은 그대로 반영하지만, 상향은 layer별 제한을 둔다.
_PHASE6_GEMINI_LAYER_RAISE_CAPS = {
    "A": 0.50,
    "B": 0.50,
    "C": 0.75,
    "D": 0.75,
    "E": 0.25,
}


def _phase6_limit_gemini_score(
    layer_id,
    base_score,
    gemini_score,
    max_score,
):
    try:
        maximum = max(0.0, float(max_score))
    except Exception:
        maximum = 0.0

    try:
        base = float(base_score)
    except Exception:
        base = 0.0

    try:
        raw_gemini = float(gemini_score)
    except Exception:
        raw_gemini = base

    base = max(0.0, min(maximum, base))
    raw_gemini = max(0.0, min(maximum, raw_gemini))

    raise_cap = float(
        _PHASE6_GEMINI_LAYER_RAISE_CAPS.get(
            str(layer_id),
            0.50,
        )
    )

    if raw_gemini <= base:
        effective = raw_gemini
        limited = False
    else:
        effective = min(raw_gemini, base + raise_cap)
        limited = effective < raw_gemini

    return {
        "base_score": round(base, 2),
        "raw_gemini_score": round(raw_gemini, 2),
        "effective_score": round(effective, 2),
        "raise_cap": round(raise_cap, 2),
        "raise_limited": limited,
    }

def _phase6_merge_gemini_feedback(grade, gemini_eval):
    if not gemini_eval or not gemini_eval.get("ok"):
        grade["gemini_semantic_evaluation"] = gemini_eval or {
            "ok": False,
            "error": "Gemini evaluation was not executed."
        }
        return grade

    parsed = gemini_eval.get("parsed") or {}

    grade["gemini_semantic_evaluation"] = {
        "ok": True,
        "model": gemini_eval.get("model"),
        "parsed": parsed,
        "raw_text": gemini_eval.get("raw_text", "")
    }

    if parsed.get("overall_comment"):
        grade["summary"] = parsed.get("overall_comment")

    if parsed.get("confidence"):
        # Gemini confidence는 "채점 판단 신뢰도"로 별도 보관한다.
        # OCR warning 등 시스템 신뢰도 low를 무조건 덮어쓰지 않는다.
        grade["gemini_confidence"] = parsed.get("confidence")

        volume = grade.get("volume_evaluation") or {}
        if not volume.get("ocr_warning"):
            grade["confidence"] = parsed.get("confidence")

    if parsed.get("improvement_advice"):
        existing = grade.get("rewrite_advice") or []
        merged = list(existing)
        for x in parsed.get("improvement_advice", []):
            if x not in merged:
                merged.append(x)
        grade["rewrite_advice"] = merged

    if parsed.get("risks"):
        existing = grade.get("weaknesses") or []
        merged = list(existing)
        for x in parsed.get("risks", []):
            if x not in merged:
                merged.append(x)
        grade["weaknesses"] = merged

    rater_comments = {
        x.get("rater_id"): x.get("comment")
        for x in parsed.get("rater_comments", [])
        if x.get("rater_id")
    }

    for r in grade.get("rater_results", []):
        rid = r.get("rater_id")
        if rid in rater_comments and rater_comments[rid]:
            r["gemini_comment"] = rater_comments[rid]
            r["perspective"] = rater_comments[rid]
            r["comment"] = rater_comments[rid]
            r["reason"] = rater_comments[rid]

    return grade


def _phase6_run_gemini_semantic_grader(
    input_text,
    answer_text,
    scoring_model,
    subject_rubric,
    rater_profile,
    volume,
    fact_eval,
    connection_eval,
    session_dir
):
    try:
        from gemini_grader import gemini_semantic_grade

        question_text = _phase3_extract_question_text(input_text)

        result = gemini_semantic_grade(
            question_text=question_text,
            answer_text=answer_text,
            scoring_model=scoring_model,
            subject_rubric=subject_rubric,
            rater_profile=rater_profile,
            volume=volume,
            fact_eval=fact_eval,
            connection_eval=connection_eval,
        )

        try:
            _phase2_json_write(session_dir / "gemini_semantic_evaluation.json", result)
            _phase2_json_write(session_dir / "question_type_evaluation.json", grade.get("question_type_evaluation", {}))
            _phase2_json_write(session_dir / "model_answer_reference.json", grade.get("model_answer_reference", {}))
            _phase2_json_write(session_dir / "originality_evaluation.json", grade.get("originality_evaluation", {}))
        except Exception:
            pass

        if result.get("ok"):
            print("[agent] Gemini semantic grader applied.")
        else:
            print(f"[agent] Gemini semantic grader failed: {result.get('error')}")

        return result

    except Exception as e:
        result = {
            "ok": False,
            "error": f"Gemini semantic grader exception: {e!r}",
            "parsed": None,
            "raw_text": ""
        }
        try:
            _phase2_json_write(session_dir / "gemini_semantic_evaluation.json", result)
            _phase2_json_write(session_dir / "originality_evaluation.json", grade.get("originality_evaluation", {}))
        except Exception:
            pass
        print(f"[agent] Gemini semantic grader exception: {e!r}")
        return result

def _phase2_resolve_logic_topic_id(
    model_answer_ref,
    grade,
    fact_eval,
):
    """Return the most precise available topic id for logic-check routing."""
    if isinstance(model_answer_ref, dict):
        primary = (
            model_answer_ref.get("primary_reference")
            or {}
        )

        if isinstance(primary, dict):
            topic_id = primary.get("topic_id")

            if topic_id:
                return topic_id

        candidates = (
            model_answer_ref.get("candidates")
            or []
        )

        if isinstance(candidates, list):
            for candidate in candidates:
                if not isinstance(candidate, dict):
                    continue

                answer = (
                    candidate.get("answer")
                    or {}
                )

                if not isinstance(answer, dict):
                    continue

                topic_id = answer.get("topic_id")

                if topic_id:
                    return topic_id

    if isinstance(grade, dict):
        topic_id = (
            grade.get("topic_id")
            or grade.get("inferred_topic_id")
        )

        if topic_id:
            return topic_id

    if isinstance(fact_eval, dict):
        topic_id = fact_eval.get("topic_id")

        if topic_id:
            return topic_id

    return None


def _phase2_resolve_difficulty_topic_id(
    fact_eval,
    model_answer_ref,
):
    """Return the best topic id for final difficulty-strategy routing."""
    if isinstance(fact_eval, dict):
        topic_id = fact_eval.get("topic_id")

        if topic_id:
            return topic_id

    if isinstance(model_answer_ref, dict):
        primary = (
            model_answer_ref.get("primary_reference")
            or {}
        )

        if isinstance(primary, dict):
            topic_id = primary.get("topic_id")

            if topic_id:
                return topic_id

        candidates = (
            model_answer_ref.get("candidates")
            or []
        )

        if isinstance(candidates, list):
            for candidate in candidates:
                if not isinstance(candidate, dict):
                    continue

                answer = (
                    candidate.get("answer")
                    or {}
                )

                if not isinstance(answer, dict):
                    continue

                topic_id = answer.get("topic_id")

                if topic_id:
                    return topic_id

    return None


def _phase2_postprocess_grade(legacy_result):
    from pathlib import Path
    from grading_config import load_active_config, save_active_config_snapshots

    session_dir = _phase2_latest_session_dir()
    if session_dir is None:
        print("[agent] phase2 skipped: session_dir not found.")
        return legacy_result

    session_dir = Path(session_dir)

    scoring_model = _phase2_json_load(session_dir / "scoring_model_snapshot.json")
    subject_rubric = _phase2_json_load(session_dir / "subject_rubric_snapshot.json")
    rater_profile = _phase2_json_load(session_dir / "layered_rater_snapshot.json")

    if not scoring_model or not rater_profile:
        print("[agent] phase2 snapshots missing. loading active_profile directly.")
        try:
            cfg = load_active_config(BASE_DIR)
            save_active_config_snapshots(session_dir, cfg)
            scoring_model = cfg["scoring_model"]
            subject_rubric = cfg["subject_rubric"]
            rater_profile = cfg["rater_profile"]
        except Exception as e:
            print(f"[agent] phase2 config load failed: {e!r}")
            return legacy_result

    input_text = ""
    input_path = session_dir / "input.txt"
    if input_path.exists():
        input_text = input_path.read_text(encoding="utf-8", errors="ignore")

    answer_text = _phase3_extract_answer_text(input_text)

    image_count = _phase2_image_count(session_dir)
    volume = _phase2_estimate_volume_level(answer_text, image_count)

    layer_scores = _phase2_layer_scores(answer_text, scoring_model)

    fact_eval = _phase3_evaluate_fact_anchors(input_text, subject_rubric)

    connection_eval = _phase3_evaluate_connections(input_text)
    interview_followup = _phase3_make_interview_followup(fact_eval, connection_eval)

    layer_scores = _phase3_apply_fact_anchor_to_layer_scores(layer_scores, fact_eval)
    layer_scores = _phase3_apply_connection_to_layer_scores(layer_scores, connection_eval)

    question_type_eval = _phase9_run_question_type_lens(
        input_text=input_text,
        answer_text=answer_text,
        subject_rubric=subject_rubric,
        session_dir=session_dir
    )

    subject_rubric_for_gemini = _phase9_subject_rubric_with_question_type_lens(
        subject_rubric,
        question_type_eval
    )

    model_answer_ref = _phase10_run_model_answer_reference(
        input_text=input_text,
        answer_text=answer_text,
        question_type_eval=question_type_eval,
        fact_eval=fact_eval,
        subject_rubric=subject_rubric,
        session_dir=session_dir
    )

    subject_rubric_for_gemini = _phase10_subject_rubric_with_model_answer_reference(
        subject_rubric_for_gemini,
        model_answer_ref
    )

    gemini_eval = _phase6_run_gemini_semantic_grader(
        input_text=input_text,
        answer_text=answer_text,
        scoring_model=scoring_model,
        subject_rubric=subject_rubric_for_gemini,
        rater_profile=rater_profile,
        volume=volume,
        fact_eval=fact_eval,
        connection_eval=connection_eval,
        session_dir=session_dir
    )

    layer_scores = _phase6_apply_gemini_layer_scores(layer_scores, gemini_eval, scoring_model)

    originality_eval = _phase8_run_originality_evaluator(
        input_text=input_text,
        answer_text=answer_text,
        layer_scores=layer_scores,
        volume=volume,
        fact_eval=fact_eval,
        connection_eval=connection_eval,
        session_dir=session_dir
    )

    layer_scores = _phase8_apply_originality_to_layer_scores(
        layer_scores=layer_scores,
        originality_eval=originality_eval,
        volume=volume
    )

    total_before_cap, total_after_cap, applied_caps = _phase2_apply_caps(layer_scores, volume)

    max_score = float(scoring_model.get("total_points", 25))
    total_score = round(total_after_cap, 2)

    score_range = f"{int(total_score)}~{int(total_score)}"

    official = round(max_score * 0.60, 2)
    practical = round(max_score * 0.70, 2)
    high = round(max_score * 0.80, 2)

    raters = []
    if rater_profile:
        raters = [r for r in rater_profile.get("raters", []) if r.get("enabled", True)]

    grade = {
        "version": "phase2_layered_scoring_v1",
        "total_score": total_score,
        "max_score": max_score,
        "score_range": score_range,
        "confidence": "medium",
        "official_pass_score": official,
        "official_pass_met": total_score >= official,
        "practical_target_score": practical,
        "practical_target_met": total_score >= practical,
        "high_score_target": high,
        "high_score_met": total_score >= high,
        "summary": (
            f"A/B/C/D/E 구조로 재산정한 결과 {total_score}/{max_score}점입니다. "
            f"분량 판단: {volume.get('level')}."
        ),
        "rater_summary": (
            f"답안지 쪽수 기준 분량 정책과 A/B/C/D/E 단계 평가를 적용했습니다. "
            f"현재 점수는 {total_score}/{max_score}점입니다."
        ),
        "volume_evaluation": volume,
        "answer_text_stats": _phase2_text_stats(answer_text),
        "fact_anchor_evaluation": fact_eval,
        "connection_evaluation": connection_eval,
        "interview_followup": interview_followup,
        "gemini_semantic_evaluation": gemini_eval,
        "question_type_evaluation": question_type_eval,
        "model_answer_reference": model_answer_ref,
        "originality_evaluation": originality_eval,
        "total_before_cap": total_before_cap,
        "applied_caps": applied_caps,
        "breakdown": layer_scores,
        "rater_results": _phase2_make_rater_results(total_score, max_score, raters),
        "strengths": [
            "핵심 용어가 일부 포함되어 있음" if input_text.strip() else "답안 내용 확인 필요"
        ],
        "weaknesses": (
            [volume.get("reason", "답안 분량 판단 정보 부족")]
            if volume.get("cap") is not None
            else []
        ) + [
            "A/B/C/D/E 각 단계의 충분한 전개가 필요함"
        ],
        "missing_keywords": [],
        "rewrite_advice": [
            "배경 → 문제 요구 → 유형별 Fact 기반 내용 설명 → 현장 적용·설계 판단·제언 순서로 답안을 확장하세요.",
            "대책은 비용, 시간, 적용 가능성, 기존 설비 영향, 운전 리스크까지 연결하세요."
        ],
        "next_practice_focus": [
            "문제 요구 해석·완전성",
            "유형별 Fact anchor 5개 설명",
            "현장 적용성, 제언, 기술사적 판단 제시"
        ],
        "legacy_grade_reference": legacy_result
    }

    grade = _phase4_apply_rater_weighted_scoring(grade, scoring_model, rater_profile)
    grade = _phase6_merge_gemini_feedback(grade, gemini_eval)
    grade = _phase9_merge_question_type_feedback(grade, question_type_eval)
    grade = _phase10_merge_model_answer_feedback(grade, model_answer_ref)
    grade = _phase8_merge_originality_feedback(grade, originality_eval)
    grade = _phase8b_enforce_final_volume_cap(grade)
    grade = _phase11_normalize_requirement_fact_labels(grade)
    grade = _phase14_compact_feedback_output(grade)
    try:
        from logic_check_evaluator import attach_logic_check_to_grade


        # PHASE3B_LOGIC_CHECK_TOPIC_ROUTING_PATCH
        # Logic check runs before the final difficulty strategy layer. Expose
        # the best known precise topic_id first, otherwise the logic checker can
        # fall back to a broader/neighboring topic based only on keyword overlap.
        _logic_topic_id = _phase2_resolve_logic_topic_id(
            model_answer_ref,
            grade,
            fact_eval,
        )

        if _logic_topic_id and isinstance(grade, dict):
            # Deliberately assign, not setdefault: a broad topic such as
            # second_order_system should not override the precise
            # model-answer reference topic.
            grade["topic_id"] = _logic_topic_id
            grade["inferred_topic_id"] = _logic_topic_id
            grade["logic_check_topic_id"] = _logic_topic_id

        grade = attach_logic_check_to_grade(grade, input_text)
        logic_eval = grade.get("logic_check_evaluation")

        if isinstance(logic_eval, dict):
            print(
                "[agent] phase3b logic check applied: "
                f"topic={logic_eval.get('topic_id')}, "
                f"mode={logic_eval.get('mode')}, "
                f"fatal={logic_eval.get('fatal_error_detected')}"
            )

            try:
                _phase2_json_write(session_dir / "logic_check_evaluation.json", logic_eval)
            except Exception:
                pass

    except Exception as e:
        print(f"[agent] phase3b logic check failed: {e!r}")



    grade = _phase15_hide_internal_metric_dict(grade)
    grade = _phase16_polish_final_output(grade)
    grade = _phase17_final_phrase_cleanup(grade)

    grade = _phase2_add_display_aliases(grade)

    _phase2_json_write(session_dir / "grade.json", grade)
    _phase2_json_write(session_dir / "volume_evaluation.json", volume)
    _phase2_json_write(session_dir / "fact_anchor_evaluation.json", fact_eval)
    _phase2_json_write(session_dir / "connection_evaluation.json", connection_eval)
    _phase2_json_write(session_dir / "interview_followup.json", interview_followup)
    _phase2_json_write(session_dir / "rater_weighted_evaluation.json", grade.get("rater_weighted_evaluation", {}))

    print(
        "[agent] phase2 layered scoring applied: "
        f"{total_score}/{max_score}, volume={volume.get('level')}, session={session_dir.name}"
    )

    # PHASE20_DIFFICULTY_SELECTION_OUTPUT_FINAL
    try:
        from difficulty_output_adapter import attach_difficulty_strategy_to_grade
        _question_for_difficulty_final = (
            locals().get("question")
            or locals().get("question_text")
            or locals().get("problem")
            or locals().get("exam_question")
        )

        # The phase2 postprocessor usually has input_text, fact_eval and
        # model_answer_ref in scope, but not a variable literally named
        # question/question_text. Derive the question explicitly so the
        # difficulty strategy layer can match topic_importance.
        if not _question_for_difficulty_final:
            try:
                _question_for_difficulty_final = _phase3_extract_question_text(input_text)
            except Exception:
                _question_for_difficulty_final = input_text

        # Expose the best known topic_id on the grade before difficulty
        # strategy runs. This is especially important for generated topic-pack
        # mode where the generated topic_importance bank may contain only one
        # precise topic_id.
        _difficulty_topic_id = _phase2_resolve_difficulty_topic_id(
            fact_eval,
            model_answer_ref,
        )

        if _difficulty_topic_id and isinstance(grade, dict):
            grade.setdefault("topic_id", _difficulty_topic_id)
            grade.setdefault("inferred_topic_id", _difficulty_topic_id)

        grade = attach_difficulty_strategy_to_grade(
            grade,
            question_text=_question_for_difficulty_final
        )
        _ds = grade.get("difficulty_strategy", {})
        print(
            "[agent] phase20 final difficulty strategy applied: "
            f"difficulty={_ds.get('difficulty')}, "
            f"importance={_ds.get('selection_importance')}, "
            f"topic={_ds.get('topic_id')}"
        )
    except Exception as e:
        print(f"[agent] phase20 final difficulty strategy skipped: {e!r}")
        try:
            print(traceback.format_exc())
        except Exception:
            pass

    # PHASE21_DIFFICULTY_SCORE_CEILING_FINAL_ORDERED
    try:
        from difficulty_score_ceiling import apply_difficulty_score_ceiling
        _answer_for_difficulty_final = (
            locals().get("answer")
            or locals().get("answer_text")
            or locals().get("student_answer")
            or locals().get("ocr_text")
            or locals().get("raw_text")
        )
        grade = apply_difficulty_score_ceiling(
            grade,
            question_text=_question_for_difficulty_final,
            answer_text=_answer_for_difficulty_final
        )
        _cap = grade.get("difficulty_ceiling_evaluation", {})
        print(
            "[agent] phase21 final difficulty ceiling evaluated: "
            f"mode={_cap.get('mode')}, "
            f"difficulty={_cap.get('difficulty')}, "
            f"original_score={_cap.get('original_score')}, "
            f"recommended_cap={_cap.get('recommended_cap')}, "
            f"capped_score={_cap.get('capped_score')}, "
            f"applied={_cap.get('cap_applied')}"
        )
    except Exception as e:
        print(f"[agent] phase21 final difficulty ceiling skipped: {e}")

    return grade



def _phase2_is_grade_dict(x):
    return (
        isinstance(x, dict)
        and (
            "total_score" in x
            or "breakdown" in x
            or "rater_results" in x
            or "score_range" in x
        )
    )


def run_agent_pipeline(*args, **kwargs):
    """
    Phase2 wrapper.

    기존 _legacy_run_agent_pipeline의 반환 형식을 보존한다.
    단, tuple/list 안에서 grade dict로 보이는 요소를 찾아
    phase2 결과로 교체한다.

    기존 반환 순서가 (grade, raw)인지 (raw, grade)인지 몰라도 동작하게 한다.
    """
    legacy_result = _legacy_run_agent_pipeline(*args, **kwargs)

    try:
        print("[agent] phase2 wrapper entered.")

        if isinstance(legacy_result, tuple):
            items = list(legacy_result)

            grade_indexes = [
                i for i, x in enumerate(items)
                if _phase2_is_grade_dict(x)
            ]

            if not grade_indexes:
                print("[agent] phase2 skipped: no grade dict found in tuple.")
                return legacy_result

            # 첫 번째 grade dict를 기준으로 phase2 계산
            processed_grade = _phase2_postprocess_grade(items[grade_indexes[0]])

            # tuple 안의 모든 grade dict를 phase2 결과로 교체
            for i in grade_indexes:
                items[i] = processed_grade

            print(f"[agent] phase2 replaced tuple grade indexes: {grade_indexes}")
            return tuple(items)

        if isinstance(legacy_result, list):
            items = list(legacy_result)

            grade_indexes = [
                i for i, x in enumerate(items)
                if _phase2_is_grade_dict(x)
            ]

            if not grade_indexes:
                print("[agent] phase2 skipped: no grade dict found in list.")
                return legacy_result

            processed_grade = _phase2_postprocess_grade(items[grade_indexes[0]])

            for i in grade_indexes:
                items[i] = processed_grade

            print(f"[agent] phase2 replaced list grade indexes: {grade_indexes}")
            return items

        if _phase2_is_grade_dict(legacy_result):
            return _phase2_postprocess_grade(legacy_result)

        print(f"[agent] phase2 skipped: unsupported legacy_result type={type(legacy_result)}")
        return legacy_result

    except Exception as e:
        print(f"[agent] phase2 postprocess failed: {e!r}")
        print(traceback.format_exc())
        return legacy_result



# ============================================================
# PHASE8_ORIGINALITY_JUDGMENT
# 기술사적 판단성 / 독창성 평가
# ============================================================

def _phase8_clamp(value, low=0.0, high=1.0):
    try:
        v = float(value)
    except Exception:
        return low
    return max(low, min(high, v))


def _phase8_normalize_originality_evaluation(parsed):
    """
    Normalize Gemini originality metadata against its own O1~O5 anchors.

    Gemini may return a raw score that contradicts both average_level and
    individual anchor levels. Anchor-derived score is therefore treated as
    the maximum score supported by the structured evidence.

    A model-reported score lower than the anchor-derived score is preserved
    as the conservative holistic judgment. The normalizer never raises the
    model-reported score.
    """
    if not isinstance(parsed, dict):
        return {}

    levels = []

    for row in parsed.get("anchors") or []:
        if not isinstance(row, dict):
            continue

        try:
            level = float(row.get("level"))
        except (TypeError, ValueError):
            continue

        levels.append(_phase8_clamp(level, 0.0, 1.0))

    # Preserve the original Gemini value for diagnostics. This function is
    # called both immediately after evaluation and again before applying the
    # D/E bonus, so prefer the already-preserved value on repeated calls.
    reported_candidate = parsed.get(
        "reported_raw_originality_score"
    )

    if reported_candidate is None:
        reported_candidate = parsed.get("raw_originality_score")

    reported_raw = None
    bounded_reported_raw = None

    try:
        if reported_candidate is not None:
            reported_raw = float(reported_candidate)
            bounded_reported_raw = _phase8_clamp(
                reported_raw,
                0.0,
                2.0,
            )
    except (TypeError, ValueError):
        reported_raw = None
        bounded_reported_raw = None

    structured_score_available = bool(levels)

    if levels:
        anchor_average = sum(levels) / len(levels)
        anchor_score = anchor_average * 2.0

        if bounded_reported_raw is None:
            effective_raw = anchor_score
            source = "anchor_derived"
        else:
            effective_raw = min(
                bounded_reported_raw,
                anchor_score,
            )
            source = (
                "reported_raw"
                if bounded_reported_raw <= anchor_score
                else "anchor_upper_bound"
            )

        parsed["average_level"] = round(anchor_average, 3)
        parsed["anchor_derived_originality_score"] = round(
            anchor_score,
            3,
        )
    else:
        average_candidate = parsed.get("average_level")
        average = 0.0

        if average_candidate is not None:
            try:
                average = float(average_candidate)
                average = _phase8_clamp(
                    average,
                    0.0,
                    1.0,
                )
                structured_score_available = True
            except (TypeError, ValueError):
                average = 0.0

        anchor_average = average
        anchor_score = average * 2.0

        if not structured_score_available:
            # A standalone raw score has no structured evidence supporting
            # it. Do not award originality points from that value alone.
            effective_raw = 0.0
            source = "no_structured_evidence"
        elif bounded_reported_raw is None:
            effective_raw = anchor_score
            source = "average_level_fallback"
        else:
            effective_raw = min(
                bounded_reported_raw,
                anchor_score,
            )
            source = (
                "reported_raw"
                if bounded_reported_raw <= anchor_score
                else "average_level_upper_bound"
            )

        parsed["average_level"] = round(anchor_average, 3)
        parsed["anchor_derived_originality_score"] = round(
            anchor_score,
            3,
        )

    parsed["reported_raw_originality_score"] = (
        round(reported_raw, 3)
        if reported_raw is not None
        else None
    )
    parsed["bounded_reported_raw_originality_score"] = (
        round(bounded_reported_raw, 3)
        if bounded_reported_raw is not None
        else None
    )
    parsed["raw_originality_score"] = round(effective_raw, 3)
    parsed["originality_score_source"] = source

    adjustment_applied = (
        reported_raw is not None
        and abs(reported_raw - effective_raw) > 1e-9
    )

    parsed["originality_score_consistency_adjustment"] = {
        "applied": adjustment_applied,
        "reported_raw_score": (
            round(reported_raw, 3)
            if reported_raw is not None
            else None
        ),
        "anchor_average_level": round(anchor_average, 3),
        "anchor_derived_score": round(anchor_score, 3),
        "effective_raw_score": round(effective_raw, 3),
        "policy": (
            "구조화된 O1~O5 anchor 또는 average_level이 지지하는 "
            "점수보다 Gemini raw 점수가 높으면 구조화 산출값으로 "
            "제한한다. 구조화 근거가 전혀 없으면 raw 점수만으로 "
            "가점을 부여하지 않으며, 더 낮은 Gemini 평가는 유지한다."
        ),
    }

    return parsed


def _phase8_get_layer_id(row):
    if not isinstance(row, dict):
        return ""
    for key in ("layer_id", "id", "code"):
        v = row.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip().upper()

    item = str(row.get("item") or row.get("name") or "")
    if item:
        first = item.strip()[:1].upper()
        if first in ("A", "B", "C", "D", "E"):
            return first
    return ""


def _phase8_find_layer(layer_scores, layer_id):
    target = str(layer_id).upper()
    for row in layer_scores or []:
        if _phase8_get_layer_id(row) == target:
            return row
    return None


def _phase8_layer_score(layer_scores, layer_id, default=0.0):
    row = _phase8_find_layer(layer_scores, layer_id)
    if not row:
        return default
    try:
        return float(row.get("score", default))
    except Exception:
        return default


def _phase8_layer_max(row, default):
    try:
        return float(row.get("max", default))
    except Exception:
        return default


def _phase8_add_reason(row, text):
    if not isinstance(row, dict):
        return
    old = str(row.get("reason") or "")
    if old:
        row["reason"] = old + " / " + text
    else:
        row["reason"] = text


def _phase8_fallback_originality_evaluation(answer_text):
    text = answer_text or ""

    checks = [
        (
            "O1",
            "문제 재해석 능력",
            ["단순히", "선정", "제어성", "운전성", "개도", "오선정", "정상 유량", "최소 유량", "최대 유량"]
        ),
        (
            "O2",
            "현장 조건 반영",
            ["기존 설비", "실제", "운전 개도", "설치 조건", "운전 조건", "배관 손실", "점도", "캐비테이션", "초크"]
        ),
        (
            "O3",
            "대안 비교와 trade-off",
            ["비용", "리스크", "공기", "교체", "수정", "trim", "트림", "튜닝", "차압 조정", "대안"]
        ),
        (
            "O4",
            "적용 우선순위 제시",
            ["우선", "먼저", "필요 시", "순서", "단계", "검토", "확인하고"]
        ),
        (
            "O5",
            "검증 가능성",
            ["확인", "검증", "trend", "트렌드", "hunting", "헌팅", "시험", "판정", "측정"]
        ),
    ]

    anchors = []
    levels = []

    for oid, name, terms in checks:
        found = [t for t in terms if t.lower() in text.lower()]
        if len(found) >= 4:
            level = 0.7
        elif len(found) >= 2:
            level = 0.5
        elif len(found) >= 1:
            level = 0.3
        else:
            level = 0.0

        anchors.append({
            "id": oid,
            "name": name,
            "level": level,
            "reason": "Gemini 독창성 평가 실패 시 사용한 보수적 fallback 평가입니다.",
            "evidence": found
        })
        levels.append(level)

    avg = sum(levels) / len(levels) if levels else 0.0

    return {
        "version": "originality_evaluator_v1_fallback",
        "confidence": "low",
        "overall_comment": "Gemini 독창성 평가를 사용할 수 없어 키워드 기반 보수 평가를 적용했습니다.",
        "anchors": anchors,
        "average_level": round(avg, 3),
        "raw_originality_score": round(avg * 2.0, 2),
        "technical_error_risk": False,
        "technical_error_reason": "",
        "false_originality_risk": False,
        "false_originality_reason": "",
        "improvement_advice": []
    }


def _phase8_run_originality_evaluator(input_text, answer_text, layer_scores, volume, fact_eval, connection_eval, session_dir=None):
    try:
        from originality_grader import gemini_originality_evaluate

        question_text = _phase3_extract_question_text(input_text)

        result = gemini_originality_evaluate(
            question_text=question_text,
            answer_text=answer_text,
            layer_scores=layer_scores,
            volume=volume,
            fact_eval=fact_eval,
            connection_eval=connection_eval,
        )

        if result.get("ok") and result.get("parsed"):
            parsed = result.get("parsed") or {}
        else:
            parsed = _phase8_fallback_originality_evaluation(answer_text)

        parsed = _phase8_normalize_originality_evaluation(parsed)

        eval_data = {
            "ok": result.get("ok"),
            "error": result.get("error", ""),
            "model": result.get("model", ""),
            "raw_text": result.get("raw_text", ""),
            "parsed": parsed
        }

        if session_dir is not None:
            try:
                _phase2_json_write(session_dir / "originality_evaluation.json", eval_data)
            except Exception:
                pass

        try:
            _phase2_log("[agent] phase8 originality evaluator applied.")
        except Exception:
            pass

        return eval_data

    except Exception as e:
        parsed = _phase8_fallback_originality_evaluation(answer_text)
        parsed = _phase8_normalize_originality_evaluation(parsed)
        eval_data = {
            "ok": False,
            "error": repr(e),
            "model": "",
            "raw_text": "",
            "parsed": parsed
        }

        try:
            _phase2_log(f"[agent] phase8 originality evaluator failed: {e!r}")
        except Exception:
            pass

        return eval_data


def _phase8_apply_originality_to_layer_scores(layer_scores, originality_eval, volume):
    parsed = (originality_eval or {}).get("parsed") or {}

    parsed = _phase8_normalize_originality_evaluation(parsed)

    raw_score = _phase8_clamp(
        parsed.get("raw_originality_score"),
        0.0,
        2.0,
    )

    c_score = _phase8_layer_score(layer_scores, "C", 0.0)
    d_score = _phase8_layer_score(layer_scores, "D", 0.0)

    applied_caps = []
    max_allowed = 2.0

    if c_score < 4.0:
        max_allowed = min(max_allowed, 0.5)
        applied_caps.append({
            "type": "fact_gate",
            "cap": 0.5,
            "reason": "C Fact 기반 설명이 4/8 미만이므로 독창성 가점을 제한함."
        })

    if d_score < 2.0:
        max_allowed = min(max_allowed, 0.8)
        applied_caps.append({
            "type": "countermeasure_gate",
            "cap": 0.8,
            "reason": "D 현장 적용·제언 점수가 2/6 미만이므로 독창성 가점을 제한함."
        })

    level = ""
    if isinstance(volume, dict):
        level = str(volume.get("level") or "")

    if level == "text_only_short_answer":
        max_allowed = min(max_allowed, 0.7)
        applied_caps.append({
            "type": "short_answer_gate",
            "cap": 0.7,
            "reason": "짧은 텍스트 답안은 독창성 판단 근거가 제한적이므로 가점을 제한함."
        })

    if parsed.get("technical_error_risk") is True:
        max_allowed = min(max_allowed, 0.0)
        applied_caps.append({
            "type": "technical_error_gate",
            "cap": 0.0,
            "reason": parsed.get("technical_error_reason") or "명백한 기술 오류 위험이 있어 독창성 가점을 인정하지 않음."
        })

    final_score = min(raw_score, max_allowed)

    target_d_bonus = round(final_score * 0.6, 3)
    target_e_bonus = round(final_score * 0.4, 3)

    d_row = _phase8_find_layer(layer_scores, "D")
    e_row = _phase8_find_layer(layer_scores, "E")

    actual_d_bonus = 0.0
    actual_e_bonus = 0.0

    if d_row is not None and target_d_bonus > 0:
        before = float(d_row.get("score", 0.0))
        maxv = _phase8_layer_max(d_row, 6.0)
        after = min(maxv, before + target_d_bonus)
        actual_d_bonus = round(after - before, 3)
        d_row["score"] = round(after, 3)
        _phase8_add_reason(
            d_row,
            f"독창성/기술사적 판단성 보정 +{actual_d_bonus:.2f}: {parsed.get('overall_comment', '')}"
        )

    if e_row is not None and target_e_bonus > 0:
        before = float(e_row.get("score", 0.0))
        maxv = _phase8_layer_max(e_row, 2.0)
        after = min(maxv, before + target_e_bonus)
        actual_e_bonus = round(after - before, 3)
        e_row["score"] = round(after, 3)
        _phase8_add_reason(
            e_row,
            f"독창성/기술사적 판단성 보정 +{actual_e_bonus:.2f}: {parsed.get('overall_comment', '')}"
        )

    parsed["raw_originality_score"] = round(raw_score, 3)
    parsed["max_allowed_after_gates"] = round(max_allowed, 3)
    parsed["final_originality_score"] = round(final_score, 3)
    parsed["applied_caps"] = applied_caps
    parsed["final_bonus_to_D"] = actual_d_bonus
    parsed["final_bonus_to_E"] = actual_e_bonus
    parsed["bonus_policy"] = "독창성은 별도 가산 총점이 아니라 D/E layer 안에서만 보정하며, 총점 25점을 초과하지 않는다."

    return layer_scores


def _phase8_merge_originality_feedback(grade, originality_eval):
    if not isinstance(grade, dict):
        return grade

    grade["originality_evaluation"] = originality_eval

    parsed = (originality_eval or {}).get("parsed") or {}
    final_score = parsed.get("final_originality_score")
    raw_score = parsed.get("raw_originality_score")
    comment = parsed.get("overall_comment") or ""

    if final_score is not None:
        grade["originality_score"] = final_score
        grade["originality_raw_score"] = raw_score

    if comment:
        old_summary = str(grade.get("summary") or "")
        add = f" 독창성/기술사적 판단성 평가는 {final_score}/2.0점으로 D/E 항목에 반영했습니다."
        if "독창성/기술사적 판단성" not in old_summary:
            grade["summary"] = (old_summary + add).strip()

    strengths = grade.get("strengths")
    if not isinstance(strengths, list):
        strengths = []
    weaknesses = grade.get("weaknesses")
    if not isinstance(weaknesses, list):
        weaknesses = []
    advice = grade.get("rewrite_advice")
    if not isinstance(advice, list):
        advice = []

    if final_score is not None:
        try:
            fs = float(final_score)
        except Exception:
            fs = 0.0

        if fs >= 1.2:
            strengths.append(f"독창성/기술사적 판단성: {final_score}/2.0 - {comment}")
        elif fs <= 0.5:
            weaknesses.append(f"독창성/기술사적 판단성 부족: {final_score}/2.0 - 현장 조건, 대안 비교, 우선순위, 검증 기준이 부족합니다.")
        else:
            weaknesses.append(f"독창성/기술사적 판단성 보통: {final_score}/2.0 - 일부 판단은 있으나 구체성이 더 필요합니다.")

    for item in parsed.get("improvement_advice") or []:
        if item and item not in advice:
            advice.append(item)

    if "현장 조건, 대안별 trade-off, 적용 우선순위, 검증 기준을 포함해 기술사적 판단성을 강화하세요." not in advice:
        advice.append("현장 조건, 대안별 trade-off, 적용 우선순위, 검증 기준을 포함해 기술사적 판단성을 강화하세요.")

    grade["strengths"] = strengths
    grade["weaknesses"] = weaknesses
    grade["rewrite_advice"] = advice

    return grade




# ============================================================
# PHASE8B_FINAL_CAP_ENFORCER
# 독창성/3인 가중 합성 이후에도 답안 분량 cap을 최종 강제 적용
# ============================================================

def _phase8b_enforce_final_volume_cap(grade):
    if not isinstance(grade, dict):
        return grade

    volume = grade.get("volume_evaluation") or {}
    cap = volume.get("cap")

    try:
        cap = float(cap)
    except Exception:
        return grade

    if cap <= 0:
        return grade

    try:
        total = float(grade.get("total_score", 0.0))
    except Exception:
        return grade

    if total > cap:
        before = total
        grade["total_score_before_final_cap"] = round(before, 3)
        grade["total_score"] = round(cap, 2)

        applied_caps = grade.get("applied_caps")
        if not isinstance(applied_caps, list):
            applied_caps = []

        applied_caps.append({
            "type": "final_volume_cap_after_originality",
            "cap": cap,
            "before": round(before, 3),
            "after": round(cap, 3),
            "reason": "독창성 보정 및 3인 가중 합성 이후에도 답안 분량 cap을 최종 점수에 강제 적용함."
        })

        grade["applied_caps"] = applied_caps

        summary = str(grade.get("summary") or "")
        note = f" ceiling 적용 전 가중 점수는 답안 분량 상한 {cap:g}점을 초과하지 않도록 보정했습니다."
        if "답안 분량 상한" not in summary:
            grade["summary"] = (summary + note).strip()

    return grade


# ============================================================
# PHASE9_QUESTION_TYPE_C_LENS
# 문제 유형은 C항목의 Fact 설명 방식 렌즈로만 사용
# ============================================================

def _phase9_run_question_type_lens(input_text, answer_text, subject_rubric=None, session_dir=None):
    try:
        from question_type_router import detect_question_type, load_question_type_profile

        question_text = _phase3_extract_question_text(input_text)

        profile_path = None
        if isinstance(subject_rubric, dict):
            profile_path = subject_rubric.get("question_type_profile")

        profile = load_question_type_profile(profile_path)

        result = detect_question_type(
            question_text=question_text,
            answer_text=answer_text,
            profile=profile
        )

        if session_dir is not None:
            try:
                _phase2_json_write(session_dir / "question_type_evaluation.json", result)
            except Exception:
                pass

        try:
            p = result.get("primary_type", {})
            _phase2_log(f"[agent] phase9 question type lens selected: {p.get('id')} ({p.get('name')})")
        except Exception:
            pass

        return result

    except Exception as e:
        fallback = {
            "version": "question_type_lens_v1_fallback",
            "confidence": "low",
            "primary_type": {
                "id": "GENERAL",
                "name": "일반 설명형",
                "c_lens": "문제 요구에 맞는 핵심 fact, 적용 범위, 한계, 실무 의미를 설명했는가",
                "c_required_elements": ["핵심 fact", "적용 범위", "한계", "실무 의미"],
                "weak_answer_pattern": "키워드만 나열하고 설명 구조와 현장 의미가 부족함",
                "high_score_pattern": "핵심 fact를 구조적으로 설명하고 현실 적용 의미까지 연결함"
            },
            "candidates": [],
            "error": repr(e),
            "interpretation": "문제 유형 렌즈 선택 실패로 GENERAL 렌즈를 적용함."
        }

        try:
            _phase2_log(f"[agent] phase9 question type lens failed: {e!r}")
        except Exception:
            pass

        return fallback


def _phase9_subject_rubric_with_question_type_lens(subject_rubric, question_type_eval):
    import copy

    if isinstance(subject_rubric, dict):
        data = copy.deepcopy(subject_rubric)
    else:
        data = {}

    data["question_type_evaluation"] = question_type_eval
    return data


def _phase9_merge_question_type_feedback(grade, question_type_eval):
    if not isinstance(grade, dict):
        return grade

    grade["question_type_evaluation"] = question_type_eval

    primary = (question_type_eval or {}).get("primary_type") or {}
    qid = primary.get("id")
    qname = primary.get("name")
    lens = primary.get("c_lens")

    if qid and qname:
        grade["question_type"] = qid
        grade["question_type_name"] = qname

    summary = str(grade.get("summary") or "")
    msg = f" 문제 유형은 {qid}({qname})로 판단하고, C항목은 해당 유형의 Fact 설명 렌즈로 평가했습니다."
    if qid and "문제 유형은" not in summary:
        grade["summary"] = (summary + msg).strip()

    advice = grade.get("rewrite_advice")
    if not isinstance(advice, list):
        advice = []

    if lens:
        tip = f"C항목 보완: {qname} 유형에서는 '{lens}'를 충족하도록 답안을 전개하세요."
        if tip not in advice:
            advice.append(tip)

    common_tip = "D/E항목 보완: 모든 문제 유형에서 현장 적용성, 문제 해결, 제언, 기술사적 판단성을 반드시 연결하세요."
    if common_tip not in advice:
        advice.append(common_tip)

    grade["rewrite_advice"] = advice

    return grade


# ============================================================
# PHASE10_MODEL_ANSWER_REFERENCE
# 모범 답안 Bank를 정답 매칭이 아니라 기준 답안으로 참조
# ============================================================

def _phase10_run_model_answer_reference(
    input_text,
    answer_text,
    question_type_eval,
    fact_eval,
    subject_rubric=None,
    session_dir=None
):
    try:
        from model_answer_router import load_model_answer_bank, find_model_answer_reference

        question_text = _phase3_extract_question_text(input_text)

        bank_path = None
        if isinstance(subject_rubric, dict):
            bank_path = subject_rubric.get("model_answer_bank")

        # Runtime bank mode guard:
        # In generated mode, ignore explicit legacy bank_path passed from subject_rubric/config
        # so load_model_answer_bank() can resolve rubrics/generated/model_answers.generated.json.
        import os as _os

        effective_bank_path = bank_path
        if _os.getenv("RUBRIC_BANK_MODE", "generated").strip().lower() == "generated":
            effective_bank_path = None

        bank = load_model_answer_bank(effective_bank_path)

        # Generated bank is often a narrow single-topic bank during migration.
        # If upstream question type detection falls back to GENERAL, do not let
        # that weak lens prevent the only generated topic-pack model answer from
        # being considered. This keeps generated-mode smoke tests focused on
        # topic-pack routing while leaving legacy behavior unchanged.
        if _os.getenv("RUBRIC_BANK_MODE", "generated").strip().lower() == "generated":
            try:
                answers = bank.get("answers", []) if isinstance(bank, dict) else []
                if len(answers) == 1 and isinstance(answers[0], dict):
                    only_answer = answers[0]
                    generated_topic_id = only_answer.get("topic_id")
                    generated_question_type = only_answer.get("question_type")

                    if isinstance(question_type_eval, dict) and generated_question_type:
                        primary = question_type_eval.get("primary_type")
                        primary_id = None
                        if isinstance(primary, dict):
                            primary_id = primary.get("id")

                        if not primary_id or str(primary_id).strip().upper() in {
                            "GENERAL",
                            "UNKNOWN",
                            "UNCLASSIFIED",
                            "NONE",
                        }:
                            question_type_eval = dict(question_type_eval)
                            primary = dict(primary or {})
                            primary["id"] = generated_question_type
                            primary.setdefault("name", "generated single-topic inferred type")
                            question_type_eval["primary_type"] = primary
                            question_type_eval["generated_single_topic_override"] = {
                                "applied": True,
                                "reason": "single generated model_answer with weak upstream question type",
                                "from_question_type": primary_id,
                                "to_question_type": generated_question_type,
                                "topic_id": generated_topic_id,
                            }

                    if isinstance(fact_eval, dict) and generated_topic_id and not fact_eval.get("topic_id"):
                        fact_eval = dict(fact_eval)
                        fact_eval["topic_id"] = generated_topic_id
                        fact_eval["generated_single_topic_override"] = {
                            "applied": True,
                            "reason": "single generated model_answer supplied missing fact_eval.topic_id",
                            "topic_id": generated_topic_id,
                        }
            except Exception:
                pass

        result = find_model_answer_reference(
            question_text=question_text,
            answer_text=answer_text,
            question_type_eval=question_type_eval,
            fact_eval=fact_eval,
            bank=bank
        )

        if session_dir is not None:
            try:
                _phase2_json_write(session_dir / "model_answer_reference.json", result)
            except Exception:
                pass

        try:
            ref = result.get("primary_reference") or {}
            if result.get("matched"):
                _phase2_log(
                    f"[agent] phase10 model answer reference selected: "
                    f"{ref.get('id')} ({ref.get('topic_id')} / {ref.get('question_type')})"
                )
            else:
                _phase2_log("[agent] phase10 model answer reference not matched.")
        except Exception:
            pass

        return result

    except Exception as e:
        fallback = {
            "version": "model_answer_reference_v1_fallback",
            "matched": False,
            "primary_reference": None,
            "candidates": [],
            "error": repr(e),
            "usage": "모범 답안 참조 실패. 기존 채점 기준만 적용함."
        }

        try:
            _phase2_log(f"[agent] phase10 model answer reference failed: {e!r}")
        except Exception:
            pass

        return fallback


def _phase10_subject_rubric_with_model_answer_reference(subject_rubric, model_answer_ref):
    import copy

    if isinstance(subject_rubric, dict):
        data = copy.deepcopy(subject_rubric)
    else:
        data = {}

    data["model_answer_reference"] = model_answer_ref
    return data


def _phase10_merge_model_answer_feedback(grade, model_answer_ref):
    if not isinstance(grade, dict):
        return grade

    grade["model_answer_reference"] = model_answer_ref

    if not isinstance(model_answer_ref, dict) or not model_answer_ref.get("matched"):
        return grade

    ref = model_answer_ref.get("primary_reference") or {}

    grade["model_answer_id"] = ref.get("id")
    grade["model_answer_topic_id"] = ref.get("topic_id")
    grade["model_answer_question_type"] = ref.get("question_type")

    summary = str(grade.get("summary") or "")
    title = ref.get("title") or ref.get("id")
    msg = f" 모범 답안 Bank에서는 '{title}'를 기준 답안으로 참조했으며, 동일 문장 매칭이 아니라 구조·깊이·현장 적용성 기준으로 활용했습니다."

    if "모범 답안 Bank" not in summary:
        grade["summary"] = (summary + msg).strip()

    advice = grade.get("rewrite_advice")
    if not isinstance(advice, list):
        advice = []

    expected = ref.get("expected_structure") or []
    if expected:
        tip = "모범 답안 구조 참고: " + " → ".join(str(x) for x in expected)
        if tip not in advice:
            advice.append(tip)

    field_points = ref.get("field_connection_points") or []
    if field_points:
        tip = "현장 연결 포인트 보완: " + ", ".join(str(x) for x in field_points[:8])
        if tip not in advice:
            advice.append(tip)

    low_patterns = ref.get("low_score_patterns") or []
    if low_patterns:
        tip = "피해야 할 저득점 패턴: " + " / ".join(str(x) for x in low_patterns[:3])
        if tip not in advice:
            advice.append(tip)

    grade["rewrite_advice"] = advice
    return grade


# ============================================================
# PHASE11_DISPLAY_LABEL_NORMALIZER
# 과거 '문제점' 중심 layer 명칭을 최종 표시에서 정규화
# ============================================================

def _phase11_normalize_requirement_fact_labels(grade):
    if not isinstance(grade, dict):
        return grade

    replace_map = {
        "B. 문제점 정의": "B. 문제 요구 해석·완전성",
        "C. Fact 기반 문제점 설명": "C. 유형별 Fact 기반 내용 설명",
        "문제 요구 해석·완전성": "문제 요구 해석·완전성",
        "Fact 기반 문제점 설명": "유형별 Fact 기반 내용 설명",
        "D. 현실적 대책·설계 판단": "D. 현장 적용·설계 판단·제언",
        "현실적 대책·설계 판단": "현장 적용·설계 판단·제언",
        "배경 → 문제점 → Fact 기반 설명 → 현실적 대책": "배경 → 문제 요구 → 유형별 Fact 기반 내용 설명 → 현장 적용·설계 판단·제언",
        "배경→문제점": "배경→문제 요구",
        "문제점→Fact": "문제 요구→Fact",
        "Fact→대책": "Fact→현장 적용·제언",
        "대책→문제점 해결": "제언→문제 요구 충족",
        "현실적 대책이 없음": "현장 적용성, 설계 판단, 제언이 부족함"
    }

    def fix_text(x):
        if not isinstance(x, str):
            return x
        for old, new in replace_map.items():
            x = x.replace(old, new)
        return x

    for key in ["summary", "overall_comment", "confidence_reason"]:
        if key in grade:
            grade[key] = fix_text(grade.get(key))

    for list_key in ["strengths", "weaknesses", "rewrite_advice", "next_practice_points"]:
        value = grade.get(list_key)
        if isinstance(value, list):
            grade[list_key] = [fix_text(v) for v in value]

    breakdown = grade.get("breakdown")
    if isinstance(breakdown, list):
        for row in breakdown:
            if isinstance(row, dict):
                for key in ["item", "name", "reason", "comment"]:
                    if key in row:
                        row[key] = fix_text(row.get(key))

    rater_scores = grade.get("rater_scores")
    if isinstance(rater_scores, list):
        for row in rater_scores:
            if isinstance(row, dict):
                for key in ["comment", "viewpoint", "reason", "summary"]:
                    if key in row:
                        row[key] = fix_text(row.get(key))

    return grade



# ============================================================
# PHASE14_COMPACT_FEEDBACK_OUTPUT
# Telegram 출력용 피드백 중복 제거 및 표현 정리
# 점수 계산에는 관여하지 않는다.
# ============================================================

def _phase14_compact_feedback_output(grade):
    if not isinstance(grade, dict):
        return grade

    replace_map = {
        "대책은 비용, 시간, 적용 가능성, 기존 설비 영향, 운전 리스크까지 연결하세요.":
            "현장 적용·제언은 비용, 시간, 적용 가능성, 기존 설비 영향, 운전 리스크까지 연결하세요.",
        "problem_link": "requirement_link",
        "Fact 기반 문제 요구 설명": "유형별 Fact 기반 내용 설명"
    }

    def fix_text(x):
        if not isinstance(x, str):
            return x
        for old, new in replace_map.items():
            x = x.replace(old, new)
        return x

    def fix_obj(obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                obj[k] = fix_obj(v)
            return obj
        if isinstance(obj, list):
            return [fix_obj(v) for v in obj]
        return fix_text(obj)

    grade = fix_obj(grade)

    # rewrite_advice가 너무 길어지는 문제를 완화한다.
    advice = grade.get("rewrite_advice")
    if isinstance(advice, list):
        cleaned = []
        seen = set()

        # 같은 의미의 안내가 여러 source에서 반복되는 경우 첫 항목만 유지
        for item in advice:
            if not isinstance(item, str):
                continue

            text = item.strip()
            if not text:
                continue

            # 지나치게 일반적인 반복 문구는 뒤쪽에서 우선 제거
            weak_generic = [
                "A/B/C/D/E 각 단계의 충분한 전개",
                "현장 조건, 대안별 trade-off",
                "기술사 답안은 '무엇인가'",
            ]

            key = text
            if key in seen:
                continue

            if any(w in text for w in weak_generic) and len(cleaned) >= 8:
                continue

            cleaned.append(text)
            seen.add(key)

        # Telegram 가독성을 위해 최대 10개로 제한
        grade["rewrite_advice"] = cleaned[:10]

    return grade


# ============================================================
# PHASE15_HIDE_INTERNAL_METRIC_DICT
# Telegram 출력에서 내부 fact metric dict 노출 제거
# 점수 계산에는 관여하지 않는다.
# ============================================================

def _phase15_hide_internal_metric_dict(grade):
    if not isinstance(grade, dict):
        return grade

    import re

    def fix_text(x):
        if not isinstance(x, str):
            return x

        # 내부 Python dict 형태의 세부 지표는 Telegram 출력에서 제거
        x = re.sub(
            r"\s*세부:\s*\{[^}]*\}",
            " 세부 지표는 핵심개념·정확성·요구 연결성·간결성을 종합 평가함.",
            x
        )

        # 어색한 표현 보정
        x = x.replace(
            "답안 분량이 지나치게 짧아 기술사 시험의 요구 수준을 충족하지 못함(과소평가 위험).",
            "답안 분량이 지나치게 짧아 기술사 시험의 요구 수준을 충족하지 못함."
        )
        x = x.replace(
            "답안 분량이 지나치게 짧아 기술사 시험의 요구 수준을 충족하지 못함(과소평가 위험)",
            "답안 분량이 지나치게 짧아 기술사 시험의 요구 수준을 충족하지 못함"
        )

        return x

    def walk(obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                obj[k] = walk(v)
            return obj
        if isinstance(obj, list):
            return [walk(v) for v in obj]
        return fix_text(obj)

    return walk(grade)


# ============================================================
# PHASE16_POLISH_FINAL_OUTPUT
# 최종 Telegram 출력 문구 보정
# 점수 계산에는 관여하지 않는다.
# ============================================================

def _phase16_polish_final_output(grade):
    if not isinstance(grade, dict):
        return grade

    def fix_text(x):
        if not isinstance(x, str):
            return x

        x = x.replace(
            "답안 분량 부족으로 인한 과소평가 위험이 있으나, 내용 자체가 기술사 수준의 깊이를 갖추지 못함",
            "답안 분량이 부족하고, 내용 자체도 기술사 수준의 깊이를 갖추지 못함"
        )
        x = x.replace(
            "답안 분량 부족으로 인한 과소평가 위험",
            "답안 분량 부족"
        )
        x = x.replace(
            "과소평가 위험이 있으나",
            "감점 요인이며"
        )
        x = x.replace(
            "과소평가 위험",
            "감점 요인"
        )

        x = x.replace(
            "기존 휴리스틱 근거: 확인된 요소: 설명",
            "기존 휴리스틱 근거: 일부 관련 표현만 확인됨"
        )
        x = x.replace(
            "기존 휴리스틱 근거: 확인된 요소: 문제",
            "기존 휴리스틱 근거: 문제 요구와 관련된 표현이 일부 확인됨"
        )

        x = x.replace(
            "유형별 Fact anchor 5개 설명",
            "유형별 핵심 Fact 5개 설명"
        )

        return x

    def walk(obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                obj[k] = walk(v)
            return obj
        if isinstance(obj, list):
            return [walk(v) for v in obj]
        return fix_text(obj)

    return walk(grade)


# ============================================================
# PHASE17_FINAL_PHRASE_CLEANUP
# 최종 잔여 표현 정리
# 점수 계산에는 관여하지 않는다.
# ============================================================

def _phase17_final_phrase_cleanup(grade):
    if not isinstance(grade, dict):
        return grade

    def fix_text(x):
        if not isinstance(x, str):
            return x

        replacements = {
            "답안의 분량이 매우 짧고 핵심 Fact가 누락되어 과소평가될 위험이 있음.":
                "답안의 분량이 매우 짧고 핵심 Fact가 누락되어 기술사 답안 요구 수준에 미달함.",
            "답안의 분량이 매우 짧고 핵심 Fact가 누락되어 과소평가될 위험이 있음":
                "답안의 분량이 매우 짧고 핵심 Fact가 누락되어 기술사 답안 요구 수준에 미달함",
            "핵심 Fact가 누락되어 과소평가될 위험이 있음":
                "핵심 Fact가 누락되어 기술사 답안 요구 수준에 미달함",
            "과소평가될 위험이 있음":
                "기술사 답안 요구 수준에 미달함",
            "과소평가될 위험":
                "기술사 답안 요구 수준 미달",
            "과소평가 위험":
                "감점 요인",
            "감점 요인이 있으나":
                "감점 요인이며",
        }

        for old, new in replacements.items():
            x = x.replace(old, new)

        return x

    def walk(obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                obj[k] = walk(v)
            return obj
        if isinstance(obj, list):
            return [walk(v) for v in obj]
        return fix_text(obj)

    return walk(grade)

