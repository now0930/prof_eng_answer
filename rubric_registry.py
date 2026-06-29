from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


BASE_DIR = Path(__file__).resolve().parent

QUESTION_TYPE_PROFILE = BASE_DIR / "rubrics" / "question_types" / "default.json"
MODEL_ANSWER_BANK = BASE_DIR / "rubrics" / "model_answers" / "industrial_instrumentation_control.json"


def project_path(path: str | Path) -> Path:
    p = Path(path)
    if p.is_absolute():
        return p
    return BASE_DIR / p


def load_json(path: str | Path, default: Any = None) -> Any:
    p = project_path(path)
    if not p.exists():
        if default is not None:
            return default
        raise FileNotFoundError(str(p))
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(path: str | Path, data: Any) -> Path:
    p = project_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


def normalize_text(text: Any) -> str:
    text = "" if text is None else str(text)
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    return text.replace("_", "").replace("-", "")


def text_hits(text: str, terms: Iterable[Any]) -> List[str]:
    raw = text or ""
    nraw = normalize_text(raw)
    found: List[str] = []

    for term in terms or []:
        term = str(term).strip()
        if not term:
            continue

        nterm = normalize_text(term)
        if term in raw or term.lower() in raw.lower() or nterm in nraw:
            if term not in found:
                found.append(term)

    return found


def collect_topic_ids(obj: Any) -> set[str]:
    found: set[str] = set()

    def walk(x: Any) -> None:
        if isinstance(x, dict):
            for key, value in x.items():
                if "topic" in str(key).lower() and isinstance(value, str) and value.strip():
                    found.add(value.strip())
                walk(value)
        elif isinstance(x, list):
            for item in x:
                walk(item)

    walk(obj)
    return found


def load_question_type_profile(path: str | Path | None = None) -> Dict[str, Any]:
    candidates = []
    if path:
        candidates.append(project_path(path))
    candidates.append(QUESTION_TYPE_PROFILE)

    for p in candidates:
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue

    return {"version": "question_type_lens_empty", "policy": {}, "types": []}


def question_type_ids(profile: Optional[Dict[str, Any]] = None) -> List[str]:
    profile = profile or load_question_type_profile()
    types = profile.get("types", [])

    if isinstance(types, dict):
        return [str(key) for key in types.keys() if str(key).strip()]

    ids: List[str] = []
    if isinstance(types, list):
        for item in types:
            if isinstance(item, dict):
                qid = item.get("id") or item.get("question_type")
                if qid:
                    ids.append(str(qid))
            elif isinstance(item, str) and item.strip():
                ids.append(item.strip())

    return ids


def get_question_type(profile: Dict[str, Any], type_id: str) -> Optional[Dict[str, Any]]:
    types = profile.get("types", [])

    if isinstance(types, dict):
        item = types.get(type_id)
        if isinstance(item, dict):
            row = dict(item)
            row.setdefault("id", type_id)
            return row
        return None

    if isinstance(types, list):
        for item in types:
            if isinstance(item, dict) and (
                item.get("id") == type_id or item.get("question_type") == type_id
            ):
                return item

    return None


def load_model_answer_bank(path: str | Path | None = None) -> Dict[str, Any]:
    candidates = []
    if path:
        candidates.append(project_path(path))
    candidates.append(MODEL_ANSWER_BANK)

    for p in candidates:
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue

    return {
        "version": "model_answer_bank_empty",
        "subject": "unknown",
        "policy": {},
        "answers": [],
    }


def save_model_answer_bank(data: Dict[str, Any], path: str | Path | None = None) -> Path:
    return write_json(path or MODEL_ANSWER_BANK, data)


def model_answer_key(entry: Dict[str, Any]) -> str:
    """Return the stable unique key for a model answer.

    Model Answer Bank can contain multiple entries with the same
    topic_id + question_type after legacy types are normalized to v2.
    Therefore the stable unique key is id.
    """
    return str(entry.get("id", "")).strip()


def build_model_answer_id(topic_id: str, question_type: str, version: str = "v1") -> str:
    safe_topic = re.sub(r"[^a-zA-Z0-9_]+", "_", topic_id.strip()).strip("_")
    safe_type = re.sub(r"[^a-zA-Z0-9_]+", "_", question_type.strip()).strip("_")
    return f"{safe_topic}_{safe_type}_{version}"


def build_model_answer_template(topic_id: str, question_type: str, title: str) -> Dict[str, Any]:
    return {
        "id": build_model_answer_id(topic_id, question_type),
        "topic_id": topic_id,
        "question_type": question_type,
        "title": title,
        "question_examples": [
            "여기에 실제 기출 또는 예상 문제 문장을 입력한다."
        ],
        "topic_aliases": [
            "주제 매칭용 별칭을 입력한다. 예: Cv, 밸브계수"
        ],
        "expected_structure": [
            "1. 정의 또는 문제 진입",
            "2. 유형별 Fact 설명",
            "3. 현장 적용 의미",
            "4. 제언 또는 판단"
        ],
        "model_answer_outline": [
            "모범 답안의 핵심 문장을 bullet로 작성한다.",
            "정답 문장 매칭용이 아니라 구조와 깊이 기준으로 사용한다.",
            "현장 적용성, 비용, 운전, 안전, 유지보수 의미를 포함한다.",
            "기술사적 제언 또는 판단 기준을 제시한다."
        ],
        "high_score_features": [
            "유형별 Fact 설명이 구조적이다.",
            "현장 적용성과 제언이 연결된다.",
            "한계와 검증 기준이 포함된다."
        ],
        "low_score_patterns": [
            "키워드만 나열한다.",
            "현장 적용 의미가 없다.",
            "제언이나 판단 기준이 없다."
        ],
        "field_connection_points": [
            "설비 조건",
            "운전 조건",
            "비용",
            "안전",
            "유지보수",
            "검증 기준"
        ],
        "revision_notes": [
            f"created_at={datetime.now().isoformat(timespec='seconds')}",
            "초안 작성 후 validate_model_answer_bank.py로 검증한다."
        ]
    }


def validate_model_answer_bank(
    bank: Dict[str, Any],
    allowed_types: Optional[Iterable[str]] = None,
) -> List[str]:
    errors: List[str] = []
    required_top = ["version", "subject", "policy", "answers"]
    required_answer = [
        "id",
        "topic_id",
        "question_type",
        "title",
        "question_examples",
        "expected_structure",
        "model_answer_outline",
        "high_score_features",
        "low_score_patterns",
        "field_connection_points",
        "revision_notes",
    ]

    for key in required_top:
        if key not in bank:
            errors.append(f"top-level key missing: {key}")

    answers = bank.get("answers", [])
    if not isinstance(answers, list):
        errors.append("answers must be a list")
        return errors

    allowed = set(allowed_types or [])
    seen_ids: set[str] = set()
    seen_pairs: set[Tuple[str, str]] = set()

    for idx, item in enumerate(answers):
        prefix = f"answers[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: item must be object")
            continue

        for key in required_answer:
            if key not in item:
                errors.append(f"{prefix}: missing key: {key}")

        aid = str(item.get("id", ""))
        if not aid:
            errors.append(f"{prefix}: id is empty")
        elif aid in seen_ids:
            errors.append(f"{prefix}: duplicated id: {aid}")
        seen_ids.add(aid)

        qtype = str(item.get("question_type", ""))
        if allowed and qtype not in allowed:
            errors.append(f"{prefix}: unknown question_type: {qtype}")

        pair = model_answer_key(item)
        if pair in seen_pairs:
            errors.append(f"{prefix}: duplicated model_answer id: {pair}")
        seen_pairs.add(pair)

        for list_key in [
            "question_examples",
            "expected_structure",
            "model_answer_outline",
            "high_score_features",
            "low_score_patterns",
            "field_connection_points",
            "revision_notes",
        ]:
            value = item.get(list_key)
            if not isinstance(value, list) or not value:
                errors.append(f"{prefix}: {list_key} must be non-empty list")

        outline = item.get("model_answer_outline", [])
        if isinstance(outline, list) and len(outline) < 4:
            errors.append(f"{prefix}: model_answer_outline should have at least 4 bullets")

    return errors


def upsert_model_answer(bank: Dict[str, Any], entry: Dict[str, Any]) -> Dict[str, Any]:
    answers = bank.setdefault("answers", [])
    if not isinstance(answers, list):
        bank["answers"] = answers = []

    target_id = entry.get("id")
    for idx, old in enumerate(answers):
        if isinstance(old, dict) and old.get("id") == target_id:
            answers[idx] = entry
            return bank

    answers.append(entry)
    return bank
