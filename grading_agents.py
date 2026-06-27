#!/usr/bin/env python3
import json
import re
from datetime import datetime
from pathlib import Path


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


def rater_output_template(raters, first_item):
    rows = []
    for r in raters:
        rows.append({
            "rater_id": r["id"],
            "summary": f"{r['name']} 관점 총평",
            "scores": [
                {
                    "item": first_item,
                    "score": 0,
                    "reason": f"{r['name']} 관점 감점 또는 가점 이유"
                }
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
- JSON 하나만 출력한다.
- markdown code block을 쓰지 않는다.
- A, B, C 등급을 쓰지 않는다.
- 점수는 반드시 숫자로 쓴다.
- raters에는 다음 rater_id를 모두 포함한다: {json.dumps(rater_ids, ensure_ascii=False)}
- scores 배열에는 아래 rubric_items와 같은 항목명을 사용한다.
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
  "raters": {json.dumps(rater_output_template(raters, first_item), ensure_ascii=False, indent=2)},
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


def run_agent_pipeline(call_ollama_fn, raw_text, rubric, sid, image_count, session_dir, progress_fn=None):
    session_dir = Path(session_dir)
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

    question_analysis = build_question_analysis(analysis, rubric)
    evidence = build_evidence(analysis)
    grade = build_grade(analysis, rubric, sid, question_analysis, evidence, raters)
    grade["common_criteria_snapshot"] = common_criteria

    write_json(session_dir / "question_analysis.json", question_analysis)
    write_json(session_dir / "evidence.json", evidence)
    write_json(session_dir / "grade.json", grade)

    progress("채점자별 채점 파이프라인이 완료되었습니다.")
    return raw_result, grade
