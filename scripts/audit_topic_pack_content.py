#!/usr/bin/env python3
"""Audit active question units and all three Master projections without private text."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from study.master_topic_pack import (
    grading_compatibility_payload,
    load_master_topic_pack,
    project_diagnosis,
    project_training,
)


def audit(root: Path = ROOT) -> dict:
    pack_root = root / "rubrics/topic_packs"
    master_root = root / "master_topic_packs"
    ids = {p.name for p in pack_root.iterdir() if p.is_dir() and (p / "model_answer.json").is_file()}
    master_ids = {p.stem for p in master_root.glob("*.json")}
    errors = []
    if ids != master_ids:
        errors.append(f"Topic/Master inventory differs: missing_master={sorted(ids-master_ids)}, orphan_master={sorted(master_ids-ids)}")
    rows = []
    legacy_intent_omissions = 0
    for topic_id in sorted(ids & master_ids):
        pack_dir = pack_root / topic_id
        source_paths = [pack_dir / f"{key}.json" for key in ("fact_anchor", "logic_check", "model_answer", "topic_importance")]
        source = [json.loads(path.read_text(encoding="utf-8")) for path in source_paths]
        facts, _, model, _ = source
        anchors = {item["anchor_id"] for item in facts["anchors"]}
        patterns = model["expected_question_patterns"]
        covered = set()
        questions = []
        for index, pattern in enumerate(patterns, 1):
            question = pattern["pattern"].strip()
            required = set(pattern["required_anchor_ids"])
            if not question or not required:
                errors.append(f"{topic_id}: question {index} lacks text or required anchors")
            if not pattern.get("intent", "").strip():
                legacy_intent_omissions += 1
            if required - anchors:
                errors.append(f"{topic_id}: question {index} has unknown anchors {sorted(required-anchors)}")
            covered.update(required)
            questions.append({"number": index, "question": question, "required_anchor_ids": sorted(required)})
        if len({q["question"] for q in questions}) != len(questions):
            errors.append(f"{topic_id}: duplicate representative questions")
        master = load_master_topic_pack(master_root / f"{topic_id}.json")
        grading = grading_compatibility_payload(root, master)
        training = project_training(root, master)
        diagnosis = project_diagnosis(root, master)
        for key, payload in zip(("fact_anchor", "logic_check", "model_answer", "topic_importance"), source):
            if grading[key] != payload:
                errors.append(f"{topic_id}: Grading projection differs from canonical {key}")
        if training["topic_id"] != topic_id or diagnosis["topic_id"] != topic_id:
            errors.append(f"{topic_id}: Training/Diagnosis topic identity differs")
        if training["question_patterns"] != patterns or training["fact_anchors"] != facts["anchors"]:
            errors.append(f"{topic_id}: Training question/fact projection differs")
        if diagnosis["fact_anchors"] != facts["anchors"] or diagnosis["score_effect"] != "none":
            errors.append(f"{topic_id}: Diagnosis fact projection or score isolation differs")
        sheet = root / "docs/topic_sheets" / f"{topic_id}.md"
        if not sheet.is_file():
            errors.append(f"{topic_id}: Topic Sheet missing")
        rows.append({
            "topic_id": topic_id,
            "title": model["title_ko"],
            "question_count": len(questions),
            "anchor_count": len(anchors),
            "required_anchor_union_count": len(covered),
            "context_anchor_count": len(anchors-covered),
            "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
            "wordpress_source_reference_count": len(master["sources"]),
            "questions": questions,
        })
    return {
        "schema_version": "topic-pack-content-audit-v1",
        "active_topic_count": len(ids),
        "master_topic_count": len(master_ids),
        "question_count": sum(row["question_count"] for row in rows),
        "anchor_count": sum(row["anchor_count"] for row in rows),
        "legacy_intent_omissions": legacy_intent_omissions,
        "errors": errors,
        "topics": rows,
    }


def render_markdown(result: dict) -> str:
    lines = [
        "# 전체 Topic Pack 내용·View 연결 감사",
        "",
        "2026-10-07 기준. 현재 운영 Topic Pack의 질문 단위, 필수 Fact Anchor 및 Master의 세 View 연결을 전수 검사한다.",
        "대표 질문은 내부 예상문항이며 공식 기출문항이나 출제기준으로 단정하지 않는다.",
        "",
        f"- 운영 Topic {result['active_topic_count']}개 / Master {result['master_topic_count']}개",
        f"- 대표 질문 {result['question_count']}개 / Fact Anchor {result['anchor_count']}개",
        f"- 구조·projection 오류 {len(result['errors'])}건",
        f"- 기존 스키마에서 선택사항인 `intent` 미기재 질문 {result['legacy_intent_omissions']}개. 질문 문장과 필수 Anchor는 모두 연결됨.",
        "- 비공개 WordPress 본문은 이 감사 결과에 포함하지 않는다. `sources=[]`는 검증된 연결 출처가 아직 없음을 뜻한다.",
        "",
        "| Topic ID | 질문 | Anchor | 질문 필수 연결 | 문맥·선택 지식 | WordPress 출처 참조 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in result["topics"]:
        lines.append(
            f"| `{row['topic_id']}` | {row['question_count']} | {row['anchor_count']} | "
            f"{row['required_anchor_union_count']} | {row['context_anchor_count']} | "
            f"{row['wordpress_source_reference_count']} |"
        )
    lines += [
        "",
        "`문맥·선택 지식`은 미연결 오류가 아니다. 모든 대표 질문에 동일한 지식을 필수로 요구하지 않도록 남긴 Anchor다.",
        "Source 파일별 SHA-256과 질문별 필수 Anchor는 `audit()` 결과로 재생성할 수 있다.",
        "",
        "## 판정 경계",
        "",
        "- Grading View는 승인된 기존 Topic Pack의 네 소스와 정확히 같은 payload를 읽는다.",
        "- Training View는 질문 패턴과 Fact Anchor를 읽고, 비공개 출처가 없으면 검증 상태를 표시한다.",
        "- Diagnosis View는 Fact Anchor를 읽으며 `score_effect=none`이다.",
        "- 6개 신규·수정 후보는 `rubrics/topic_pack_candidates/`에 보존했으며 사람 승인 전 운영 목록에 포함하지 않는다.",
        "- 이 감사의 PASS는 구조와 추적성 검증이다. 모든 공학 문장의 외부 진위 검증이나 사람의 내용 승인을 대신하지 않는다.",
        "",
        "실행: `python3 -B scripts/audit_topic_pack_content.py`",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="write a public, source-text-free Markdown inventory")
    args = parser.parse_args()
    result = audit()
    if args.report is not None:
        args.report.write_text(render_markdown(result), encoding="utf-8")
    print(f"TOPIC_CONTENT_AUDIT={'PASS' if not result['errors'] else 'FAIL'} topics={result['active_topic_count']} masters={result['master_topic_count']} questions={result['question_count']} anchors={result['anchor_count']}")
    for error in result["errors"]:
        print(f"ERROR: {error}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
