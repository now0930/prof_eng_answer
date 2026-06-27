#!/usr/bin/env python3
import json
import re
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
    if not text:
        return None

    text = str(text).strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    if start < 0:
        return None

    in_string = False
    escape = False
    depth = 0

    for i in range(start, len(text)):
        ch = text[i]

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
                candidate = text[start:i + 1]
                try:
                    return json.loads(candidate)
                except Exception:
                    return None

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


def _phase2_estimate_volume_level(text, image_count):
    stats = _phase2_text_stats(text)
    chars = stats["char_count"]
    lines = stats["line_count"]

    # 사진이 있으면 답안지 쪽수 근거로 우선 반영한다.
    # 단, 사진 3장이 있어도 OCR 텍스트 내용이 부족하면 내용 점수는 별도로 낮게 나온다.
    if image_count >= 3:
        return {
            "level": "three_page_level",
            "estimated_answer_sheet_pages": image_count,
            "cap": None,
            "reason": "답안 이미지 3장 이상으로 25점 문항 평균 분량 충족 가능성이 있다."
        }
    if image_count == 2:
        return {
            "level": "two_page_level",
            "estimated_answer_sheet_pages": 2,
            "cap": 17.0,
            "reason": "답안 이미지 2장 수준으로 기본 전개는 가능하나 25점 문항 평균 분량에는 다소 부족하다."
        }
    if image_count == 1:
        return {
            "level": "one_page_level",
            "estimated_answer_sheet_pages": 1,
            "cap": 13.0,
            "reason": "답안 이미지 1장 수준으로 부분 답안 상한을 적용한다."
        }

    # 이미지가 없으면 OCR/텍스트 길이로 보조 판단한다.
    if lines <= 5 or chars < 500:
        return {
            "level": "text_only_short_answer",
            "estimated_answer_sheet_pages": 0,
            "cap": 9.0,
            "reason": "답안 이미지 없이 텍스트가 1~5줄 또는 500자 미만이므로 요약 답안 상한을 적용한다."
        }
    if chars < 1000:
        return {
            "level": "less_than_one_page_text",
            "estimated_answer_sheet_pages": 0,
            "cap": 10.5,
            "reason": "답안 이미지 없이 텍스트 분량이 1쪽 미만 수준으로 판단되어 상한을 적용한다."
        }
    if chars < 1800:
        return {
            "level": "one_page_text",
            "estimated_answer_sheet_pages": 1,
            "cap": 13.0,
            "reason": "텍스트 기준 답안지 1쪽 수준으로 판단되어 부분 답안 상한을 적용한다."
        }
    if chars < 3000:
        return {
            "level": "two_page_text",
            "estimated_answer_sheet_pages": 2,
            "cap": 17.0,
            "reason": "텍스트 기준 답안지 2쪽 수준으로 판단되어 고득점 상한을 적용한다."
        }

    return {
        "level": "three_page_text",
        "estimated_answer_sheet_pages": 3,
        "cap": None,
        "reason": "텍스트 분량상 답안지 3쪽 수준의 전개 가능성이 있다."
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
            "strong": ["문제", "문제점", "원인", "발생", "영향", "위험", "소음", "진동", "침식", "손상", "불안정"],
            "weak": ["고장", "품질", "안전", "리스크"]
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

    image_count = _phase2_image_count(session_dir)
    volume = _phase2_estimate_volume_level(input_text, image_count)

    layer_scores = _phase2_layer_scores(input_text, scoring_model)
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
        "total_before_cap": total_before_cap,
        "applied_caps": applied_caps,
        "breakdown": layer_scores,
        "rater_results": _phase2_make_rater_results(total_score, max_score, raters),
        "strengths": [
            "핵심 용어가 일부 포함되어 있음" if input_text.strip() else "답안 내용 확인 필요"
        ],
        "weaknesses": [
            volume.get("reason", "답안 분량 판단 정보 부족"),
            "A/B/C/D/E 각 단계의 충분한 전개가 필요함"
        ],
        "missing_keywords": [],
        "rewrite_advice": [
            "배경 → 문제점 → Fact 기반 설명 → 현실적 대책 순서로 답안을 확장하세요.",
            "대책은 비용, 시간, 적용 가능성, 기존 설비 영향, 운전 리스크까지 연결하세요."
        ],
        "next_practice_focus": [
            "문제점 정의",
            "Fact anchor 5개 설명",
            "현실적 대책의 조건과 한계 제시"
        ],
        "legacy_grade_reference": legacy_result
    }

    grade = _phase2_add_display_aliases(grade)

    _phase2_json_write(session_dir / "grade.json", grade)
    _phase2_json_write(session_dir / "volume_evaluation.json", volume)

    print(
        "[agent] phase2 layered scoring applied: "
        f"{total_score}/{max_score}, volume={volume.get('level')}, session={session_dir.name}"
    )

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
        return legacy_result
