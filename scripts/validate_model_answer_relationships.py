#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
REPORT_DIR = ROOT / "reports"

# 큰 흐름 검증용 카테고리.
# expected_structure, model_answer_outline, high_score_features 사이의
# 표현 차이를 흡수하기 위한 약한 의미 분류이다.
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "intro": [
        "개요", "정의", "개념", "배경", "목적", "필요", "역할", "의미",
        "도입", "문제의식",
    ],
    "principle": [
        "원리", "동작", "메커니즘", "이론", "관계", "특성", "특징",
        "공식", "변수", "응답", "안정", "제어", "측정", "신호",
    ],
    "structure": [
        "구성", "구조", "요소", "분류", "종류", "방식", "시스템",
        "장치", "센서", "계기", "밸브", "제어기", "모듈",
    ],
    "criteria": [
        "기준", "비교", "선정", "평가", "판정", "계산", "설계",
        "사양", "범위", "정밀도", "정확도", "오차", "성능", "지표",
    ],
    "risk": [
        "문제", "문제점", "한계", "원인", "영향", "리스크", "주의",
        "고장", "열화", "노이즈", "간섭", "불안정", "위험", "오류",
    ],
    "action": [
        "대책", "개선", "방안", "절차", "방법", "조치", "진단",
        "보정", "보상", "튜닝", "검토", "적용", "운전", "유지보수",
    ],
    "field": [
        "현장", "공정", "설비", "운영", "운전", "유지보수", "안전",
        "비용", "실현", "기존", "노후", "적용성", "관리", "결론",
    ],
}

GENERIC_TOKENS = {
    "설명", "정리", "제시", "검토", "중심", "통해", "따라", "대한",
    "관점", "기반", "주요", "핵심", "관련", "해당", "구분", "연결",
    "조건", "사항", "내용", "흐름", "답안", "모범", "기술", "작성",
    "한다", "된다", "있다", "위해", "까지", "또는", "그리고",
}

NUMBERING_RE = re.compile(r"^\s*\d{1,2}[.)]\s*")
TOKEN_RE = re.compile(r"[가-힣A-Za-z0-9]{2,}")


@dataclass
class Issue:
    severity: str
    relation: str
    answer_id: str
    topic_id: str
    message: str
    detail: str
    score: float | None = None


def load_bank(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]

    if isinstance(data, dict):
        answers = data.get("answers", [])
        if isinstance(answers, list):
            return [x for x in answers if isinstance(x, dict)]

    raise SystemExit(f"ERROR: unsupported model answer bank format: {path}")


def clean_text(text: Any) -> str:
    s = str(text or "").strip()
    s = NUMBERING_RE.sub("", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def tokenize(text: Any) -> set[str]:
    s = clean_text(text).lower()
    toks = set(TOKEN_RE.findall(s))
    toks = {t for t in toks if t not in GENERIC_TOKENS and len(t) >= 2}
    return toks


def categories(text: Any) -> set[str]:
    s = clean_text(text)
    out: set[str] = set()
    for cat, keys in CATEGORY_KEYWORDS.items():
        if any(k in s for k in keys):
            out.add(cat)
    return out


def similarity(a: Any, b: Any) -> float:
    ta = tokenize(a)
    tb = tokenize(b)
    ca = categories(a)
    cb = categories(b)

    token_score = 0.0
    if ta and tb:
        token_score = len(ta & tb) / len(ta | tb)

    category_score = 0.0
    if ca and cb:
        category_score = len(ca & cb) / len(ca | cb)

    left_key = normalized_duplicate_key(clean_text(a))
    right_key = normalized_duplicate_key(clean_text(b))

    containment_score = 0.0

    # expected_structure의 짧은 목차 문구에는 조사·어미가 없지만,
    # outline에는 "개요에서", "준비 사항으로"처럼 붙어서 나타난다.
    # 공백·구두점을 제거한 전체 문구가 포함되면 직접 매칭으로 본다.
    # 한 글자 약어(P, I, D 등)는 과매칭 방지를 위해 제외한다.
    if (
        len(left_key) >= 2
        and len(right_key) >= 2
        and (
            left_key in right_key
            or right_key in left_key
        )
    ):
        containment_score = 1.0

    # outline은 큰 흐름이고 feature는 세부 문장이므로
    # category 일치에 더 큰 가중치를 준다.
    return max(
        containment_score,
        token_score,
        category_score * 0.75 + token_score * 0.25,
    )


def best_match_score(source: str, targets: list[str]) -> tuple[float, str]:
    if not targets:
        return 0.0, ""

    scored = [(similarity(source, t), t) for t in targets]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0]


def list_clean(row: dict[str, Any], key: str) -> list[str]:
    values = row.get(key, [])
    if not isinstance(values, list):
        return []
    return [clean_text(x) for x in values if clean_text(x)]


def normalized_duplicate_key(text: str) -> str:
    s = clean_text(text).lower()
    s = re.sub(r"[^\w가-힣A-Za-z0-9]+", "", s)
    return s


def detect_duplicates(items: list[str]) -> list[str]:
    seen: set[str] = set()
    dups: list[str] = []
    for item in items:
        key = normalized_duplicate_key(item)
        if key in seen:
            dups.append(item)
        seen.add(key)
    return dups


def order_score(expected: list[str], outline: list[str]) -> float:
    """
    expected_structure의 순서가 outline에서 대체로 유지되는지 본다.
    완전한 문장 매칭이 아니라 best match index의 증가 여부를 본다.
    """
    if not expected or not outline:
        return 0.0

    matched_indexes: list[int] = []
    for e in expected:
        scores = [(similarity(e, o), idx) for idx, o in enumerate(outline)]
        scores.sort(key=lambda x: x[0], reverse=True)
        best_score, best_idx = scores[0]
        if best_score >= 0.22:
            matched_indexes.append(best_idx)

    if len(matched_indexes) <= 1:
        return 1.0

    ok = 0
    total = 0
    for a, b in zip(matched_indexes, matched_indexes[1:]):
        total += 1
        if a <= b:
            ok += 1

    return ok / total if total else 1.0


def severity_from_coverage(coverage: float, major_threshold: float, minor_threshold: float) -> str:
    if coverage < major_threshold:
        return "MAJOR"
    if coverage < minor_threshold:
        return "MINOR"
    return "OK"


def validate_expected_vs_outline(row: dict[str, Any]) -> list[Issue]:
    answer_id = str(row.get("id", ""))
    topic_id = str(row.get("topic_id", ""))
    expected = list_clean(row, "expected_structure")
    outline = list_clean(row, "model_answer_outline")

    issues: list[Issue] = []

    if not expected:
        issues.append(Issue(
            "MAJOR",
            "expected_structure_vs_model_answer_outline",
            answer_id,
            topic_id,
            "expected_structure가 비어 있음",
            "expected_structure는 답안 전개 목차 기준이므로 비어 있으면 outline 정합성을 판단할 수 없음",
            0.0,
        ))
        return issues

    if not outline:
        issues.append(Issue(
            "MAJOR",
            "expected_structure_vs_model_answer_outline",
            answer_id,
            topic_id,
            "model_answer_outline이 비어 있음",
            "model_answer_outline은 expected_structure를 따라가는 큰 답안 흐름이어야 함",
            0.0,
        ))
        return issues

    missing: list[str] = []
    weak: list[str] = []
    matched_count = 0

    for e in expected:
        score, target = best_match_score(e, outline)

        if score >= 0.30:
            matched_count += 1
        elif score >= 0.20:
            weak.append(f"{e} -> 약한 매칭: {target} ({score:.2f})")
            matched_count += 0.5
        else:
            missing.append(f"{e} -> 매칭 없음")

    coverage = matched_count / len(expected)
    sev = severity_from_coverage(coverage, major_threshold=0.65, minor_threshold=0.85)

    if sev != "OK":
        issues.append(Issue(
            sev,
            "expected_structure_vs_model_answer_outline",
            answer_id,
            topic_id,
            f"expected_structure 대비 model_answer_outline coverage 부족: {coverage:.2f}",
            "; ".join(missing + weak),
            coverage,
        ))

    # outline이 expected_structure에 없는 흐름을 많이 포함하면 역할 이탈 가능성이 있음
    extras: list[str] = []
    for o in outline:
        score, target = best_match_score(o, expected)
        if score < 0.18:
            extras.append(f"{o} -> expected_structure 근거 약함")

    if len(extras) >= 2:
        issues.append(Issue(
            "MINOR",
            "expected_structure_vs_model_answer_outline",
            answer_id,
            topic_id,
            "model_answer_outline에 expected_structure와 약하게 연결된 항목이 많음",
            "; ".join(extras[:8]),
            None,
        ))

    oscore = order_score(expected, outline)
    if oscore < 0.75 and len(expected) >= 4 and len(outline) >= 4:
        issues.append(Issue(
            "MINOR",
            "expected_structure_vs_model_answer_outline",
            answer_id,
            topic_id,
            f"expected_structure와 model_answer_outline의 전개 순서가 다소 어긋남: {oscore:.2f}",
            "expected_structure의 흐름 순서와 outline의 best-match 순서를 비교한 결과",
            oscore,
        ))

    return issues


def validate_outline_vs_high_score(row: dict[str, Any]) -> list[Issue]:
    answer_id = str(row.get("id", ""))
    topic_id = str(row.get("topic_id", ""))
    outline = list_clean(row, "model_answer_outline")
    features = list_clean(row, "high_score_features")

    issues: list[Issue] = []

    if not outline:
        issues.append(Issue(
            "MAJOR",
            "model_answer_outline_vs_high_score_features",
            answer_id,
            topic_id,
            "model_answer_outline이 비어 있음",
            "high_score_features의 상위 흐름을 판단할 수 없음",
            0.0,
        ))
        return issues

    if not features:
        issues.append(Issue(
            "MAJOR",
            "model_answer_outline_vs_high_score_features",
            answer_id,
            topic_id,
            "high_score_features가 비어 있음",
            "고득점 조건이 없으면 outline과 정합성을 검증할 수 없음",
            0.0,
        ))
        return issues

    unsupported: list[str] = []
    weak: list[str] = []
    matched_count = 0

    for f in features:
        score, target = best_match_score(f, outline)

        if score >= 0.28:
            matched_count += 1
        elif score >= 0.18:
            weak.append(f"{f} -> 약한 상위 흐름: {target} ({score:.2f})")
            matched_count += 0.5
        else:
            unsupported.append(f"{f} -> outline 상위 흐름 없음")

    coverage = matched_count / len(features)
    sev = severity_from_coverage(coverage, major_threshold=0.60, minor_threshold=0.80)

    if sev != "OK":
        issues.append(Issue(
            sev,
            "model_answer_outline_vs_high_score_features",
            answer_id,
            topic_id,
            f"high_score_features 대비 model_answer_outline coverage 부족: {coverage:.2f}",
            "; ".join(unsupported + weak),
            coverage,
        ))

    # outline 항목이 어떤 high_score_feature와도 연결되지 않으면 너무 일반적이거나 불필요한 흐름일 수 있음
    orphan_outline: list[str] = []
    for o in outline:
        score, target = best_match_score(o, features)
        if score < 0.15:
            orphan_outline.append(f"{o} -> high_score_features 근거 약함")

    if len(orphan_outline) >= 2:
        issues.append(Issue(
            "MINOR",
            "model_answer_outline_vs_high_score_features",
            answer_id,
            topic_id,
            "model_answer_outline에 high_score_features와 연결이 약한 항목이 많음",
            "; ".join(orphan_outline[:8]),
            None,
        ))

    # high_score_features가 outline과 완전히 같은 문장으로 반복되면 역할 중복
    role_overlap: list[str] = []
    outline_keys = {normalized_duplicate_key(x) for x in outline}
    for f in features:
        if normalized_duplicate_key(f) in outline_keys:
            role_overlap.append(f)

    if role_overlap:
        issues.append(Issue(
            "MINOR",
            "model_answer_outline_vs_high_score_features",
            answer_id,
            topic_id,
            "high_score_features가 model_answer_outline과 동일 문장으로 반복됨",
            "; ".join(role_overlap[:8]),
            None,
        ))

    return issues


def validate_style(row: dict[str, Any]) -> list[Issue]:
    answer_id = str(row.get("id", ""))
    topic_id = str(row.get("topic_id", ""))
    outline = list_clean(row, "model_answer_outline")
    issues: list[Issue] = []

    if len(outline) > 6:
        issues.append(Issue(
            "MINOR",
            "model_answer_outline_style",
            answer_id,
            topic_id,
            f"model_answer_outline 항목이 6개 초과: {len(outline)}개",
            "outline은 큰 흐름만 남기고 6개 이하로 압축 필요",
            float(len(outline)),
        ))

    dups = detect_duplicates(outline)
    if dups:
        issues.append(Issue(
            "MINOR",
            "model_answer_outline_style",
            answer_id,
            topic_id,
            "model_answer_outline에 동일/중복 항목이 있음",
            "; ".join(dups[:8]),
            None,
        ))

    numbered = [x for x in outline if NUMBERING_RE.match(str(x))]
    if numbered:
        issues.append(Issue(
            "MINOR",
            "model_answer_outline_style",
            answer_id,
            topic_id,
            "model_answer_outline에 번호 목차 표현이 남아 있음",
            "; ".join(numbered[:8]),
            None,
        ))

    return issues


def write_csv(path: Path, issues: list[Issue]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "severity", "relation", "answer_id", "topic_id",
                "message", "detail", "score",
            ],
        )
        w.writeheader()
        for x in issues:
            w.writerow({
                "severity": x.severity,
                "relation": x.relation,
                "answer_id": x.answer_id,
                "topic_id": x.topic_id,
                "message": x.message,
                "detail": x.detail,
                "score": "" if x.score is None else f"{x.score:.3f}",
            })


def write_md(path: Path, issues: list[Issue], total_answers: int) -> None:
    counts: dict[str, int] = {"MAJOR": 0, "MINOR": 0, "OK": 0}
    for x in issues:
        counts[x.severity] = counts.get(x.severity, 0) + 1

    lines: list[str] = []
    lines.append("# Model Answer Relationship Validation")
    lines.append("")
    lines.append(f"- total_answers: {total_answers}")
    lines.append(f"- MAJOR: {counts.get('MAJOR', 0)}")
    lines.append(f"- MINOR: {counts.get('MINOR', 0)}")
    lines.append("")

    if not issues:
        lines.append("No relationship issues found.")
    else:
        for sev in ("MAJOR", "MINOR"):
            group = [x for x in issues if x.severity == sev]
            if not group:
                continue

            lines.append(f"## {sev}")
            lines.append("")
            for x in group:
                lines.append(f"### {x.answer_id} | {x.topic_id}")
                lines.append(f"- relation: `{x.relation}`")
                lines.append(f"- message: {x.message}")
                if x.score is not None:
                    lines.append(f"- score: {x.score:.3f}")
                if x.detail:
                    lines.append(f"- detail: {x.detail}")
                lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--model-path",
        default=str(DEFAULT_MODEL_PATH),
        help="model answer bank json path",
    )
    ap.add_argument(
        "--fail-on-major",
        action="store_true",
        help="exit 1 when MAJOR issue exists",
    )
    args = ap.parse_args()

    model_path = Path(args.model_path)
    answers = load_bank(model_path)

    issues: list[Issue] = []

    for row in answers:
        issues.extend(validate_style(row))
        issues.extend(validate_expected_vs_outline(row))
        issues.extend(validate_outline_vs_high_score(row))

    issues = [x for x in issues if x.severity != "OK"]

    REPORT_DIR.mkdir(exist_ok=True)
    csv_path = REPORT_DIR / "model_answer_relationship_validation.csv"
    md_path = REPORT_DIR / "model_answer_relationship_validation.md"

    write_csv(csv_path, issues)
    write_md(md_path, issues, total_answers=len(answers))

    major = sum(1 for x in issues if x.severity == "MAJOR")
    minor = sum(1 for x in issues if x.severity == "MINOR")

    print("=== Model answer relationship validation ===")
    print("answers:", len(answers))
    print("MAJOR :", major)
    print("MINOR :", minor)
    print("Wrote :", md_path)
    print("Wrote :", csv_path)

    if issues:
        print("")
        print("Top issues:")
        for x in issues[:20]:
            score = "" if x.score is None else f" score={x.score:.2f}"
            print(f"- {x.severity} {x.relation} {x.answer_id} | {x.topic_id}{score} :: {x.message}")

    if args.fail_on_major and major:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
