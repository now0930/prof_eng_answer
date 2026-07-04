#!/usr/bin/env python3
"""
Create a new topic_pack scaffold.

This script intentionally creates schema-valid starter files, not a complete
expert-quality rubric. Replace TODO text before using the topic in production.

Examples:

  python3 scripts/create_topic_pack.py \
    --topic-id second_order_system_settling_time_overshoot \
    --title "2차 시스템 정착시간과 오버슈트" \
    --question-type PRINCIPLE_INTERPRETATION

  python3 scripts/rubric_manager.py create-topic-pack \
    --topic-id second_order_system_settling_time_overshoot \
    --title "2차 시스템 정착시간과 오버슈트"
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TOPIC_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_]*[a-z0-9]$")


def _project_root() -> Path:
    here = Path(__file__).resolve()
    candidates = [
        here.parents[1],
        Path.cwd(),
        Path("/workspace/prof_eng_answer"),
    ]

    for candidate in candidates:
        if (candidate / "rubrics" / "topic_packs").exists():
            return candidate

    raise SystemExit("ERROR: project root not found. Run from prof_eng_answer repo.")


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _topic_words(topic_id: str) -> str:
    return topic_id.replace("_", " ")


def _default_question_examples(title: str) -> list[str]:
    return [
        f"{title}에 대해 설명하시오.",
        f"{title}의 핵심 원리와 현장 적용 시 고려사항을 설명하시오.",
        f"{title}의 문제점과 개선 방안을 설명하시오.",
    ]


def _build_readme(topic_id: str, title: str, question_type: str) -> str:
    return f"""# {title}

## Topic ID

`{topic_id}`

## Question type

`{question_type}`

## 작성 상태

이 파일들은 `scripts/create_topic_pack.py`로 생성된 scaffold입니다.
실제 사용 전 아래 항목을 반드시 보강하세요.

## 보강 체크리스트

- [ ] fact_anchor.json의 TODO anchor를 실제 fact 기준으로 교체
- [ ] model_answer.json의 recommended_outline 보강
- [ ] high_score_points / common_missing_points 보강
- [ ] routing_aliases / routing_field_points 정리
- [ ] topic_importance.json의 난이도·선택전략 확정
- [ ] logic_check.json의 fatal_checks / major_checks 보강
- [ ] validate-generated-pipeline 실행
- [ ] smoke-topic 또는 수동 smoke로 primary/difficulty/logic_check topic 확인

## 대표 질문 예시

1. {title}에 대해 설명하시오.
2. {title}의 핵심 원리와 현장 적용 시 고려사항을 설명하시오.
3. {title}의 문제점과 개선 방안을 설명하시오.
"""


def _build_model_answer(topic_id: str, title: str, question_type: str) -> dict[str, Any]:
    question_examples = _default_question_examples(title)

    return {
        "topic_id": topic_id,
        "title": title,
        "question_type": question_type,
        "question_examples": question_examples,
        "recommended_outline": {
            "sections": [
                "배경 및 문제 요구",
                "핵심 개념과 정의",
                "원리·구성·판단 기준",
                "현장 적용 및 설계 고려사항",
                "문제점·개선 방향",
                "결론",
            ],
            "intents": [
                f"{title}이 필요한 배경과 출제 의도를 설명한다.",
                f"{title}의 핵심 정의와 주요 변수를 명확히 제시한다.",
                "원리, 구성 요소, 판단 기준을 구조적으로 전개한다.",
                "현장 적용 시 비용, 운전성, 유지보수성, 기존 설비 영향을 연결한다.",
                "대표적인 오류, 한계, 개선 방향을 제시한다.",
                "기술사 답안 관점에서 핵심 판단 기준을 정리한다.",
            ],
        },
        "high_score_points": [
            "핵심 정의와 적용 범위를 명확히 제시한다.",
            "주요 변수, 조건, 판단 기준을 구조적으로 설명한다.",
            "수식 또는 도식이 필요한 경우 의미와 함께 제시한다.",
            "현장 적용성, 비용, 유지보수, 기존 설비 영향을 연결한다.",
            "오해하기 쉬운 개념이나 fatal 오류를 구분한다.",
        ],
        "common_missing_points": [
            "정의만 쓰고 판단 기준이나 적용 조건을 설명하지 않음",
            "키워드 나열에 그치고 원리와 현장 의미를 연결하지 않음",
            "비용, 실현 가능성, 기존 설비 영향 등 실무 고려가 없음",
            "유사 개념과의 차이를 구분하지 않음",
        ],
        "routing_aliases": [
            title,
            *question_examples,
            topic_id,
            _topic_words(topic_id),
        ],
        "routing_field_points": [
            title,
            topic_id,
            _topic_words(topic_id),
        ],
        "revision_notes": [
            "created_by=scripts/create_topic_pack.py",
            "TODO: replace scaffold content with reviewed topic-specific rubric.",
        ],
    }


def _build_fact_anchor(topic_id: str, title: str) -> dict[str, Any]:
    anchors = []
    for idx, label in enumerate(
        [
            "핵심 정의",
            "주요 원리",
            "판단 조건",
            "현장 적용",
            "오류 및 한계",
        ],
        start=1,
    ):
        statement = f"TODO: {title}의 {label}에 대한 fact anchor를 작성한다."
        anchors.append(
            {
                "anchor_id": f"{topic_id}_anchor_{idx:02d}",
                "statement": statement,
                "expected": statement,
                "keywords": [title],
                "required": idx <= 3,
                "weight": 1.0,
            }
        )

    return {
        "topic_id": topic_id,
        "title": title,
        "anchors": anchors,
        "revision_notes": [
            "created_by=scripts/create_topic_pack.py",
            "TODO: replace scaffold anchors with verified facts.",
        ],
    }


def _build_topic_importance(topic_id: str, title: str, difficulty: str, importance: str) -> dict[str, Any]:
    return {
        "topic_id": topic_id,
        "topic_label": title,
        "difficulty": difficulty,
        "difficulty_label": difficulty,
        "selection_importance": importance,
        "selection_policy": None,
        "minimum_attempt_floor": None,
        "target_score": None,
        "excellent_score_band": [21, 25] if difficulty == "THEORY_CORE" else [18, 25],
        "default_score_ceiling": None,
        "requires_band_unlock": difficulty == "THEORY_CORE",
        "high_band_unlock_conditions": [
            "핵심 정의와 기본 모델을 정확히 제시한다.",
            "주요 판단 조건과 적용 범위를 설명한다.",
            "현장 적용성과 한계, 개선 방향을 연결한다.",
            "fatal logic error가 없다.",
        ],
        "omission_risk": "medium",
        "fatal_error_risk": "medium",
        "score_ceiling_policy": None,
        "note": f"TODO: {title}의 난이도, 선택 중요도, 고득점 unlock 조건을 검토한다.",
        "revision_notes": [
            "created_by=scripts/create_topic_pack.py",
            "TODO: review topic importance policy.",
        ],
    }


def _build_logic_check(topic_id: str, title: str, question_type: str, difficulty: str) -> dict[str, Any]:
    return {
        "topic_id": topic_id,
        "title": title,
        "deterministic_checks": {
            "enabled": True,
            "difficulty_profile": difficulty,
            "topic_name": title,
            "topic_aliases": [
                title,
                topic_id,
                _topic_words(topic_id),
            ],
            "question_type": question_type,
            "fatal_checks": [
                {
                    "id": f"{topic_id}_fatal_01",
                    "description": f"TODO: {title}에서 반드시 피해야 할 fatal 오류를 정의한다.",
                    "patterns": [],
                    "message": "핵심 개념 오류가 의심됩니다.",
                }
            ],
            "major_checks": [
                {
                    "id": f"{topic_id}_major_01",
                    "description": f"TODO: {title}에서 주요 누락 항목을 정의한다.",
                    "patterns": [],
                    "message": "주요 설명 축이 부족합니다.",
                }
            ],
            "question_type_checks": [
                {
                    "id": f"{topic_id}_qtype_01",
                    "description": f"{question_type} 답안 구조가 문제 요구와 맞는지 확인한다.",
                    "patterns": [],
                    "message": "문제 유형에 맞는 답안 전개가 필요합니다.",
                }
            ],
            "next_practice_points": [
                f"{title}의 핵심 정의와 판단 기준 정리",
                "fact anchor 기반 답안 전개",
                "현장 적용성과 개선 방안 연결",
            ],
            "de_claim_trust": [],
        },
        "llm_profile": {
            "enabled": True,
            "focus": [
                "fact anchor 충족 여부",
                "논리 전개와 현장 적용성",
                "fatal 오류 또는 유사 개념 혼동 여부",
            ],
        },
        "revision_notes": [
            "created_by=scripts/create_topic_pack.py",
            "TODO: replace placeholder deterministic checks.",
        ],
    }


def create_topic_pack(args: argparse.Namespace) -> Path:
    if not TOPIC_ID_RE.match(args.topic_id):
        raise SystemExit(
            "ERROR: topic_id must match ^[a-z0-9][a-z0-9_]*[a-z0-9]$ "
            "(lowercase snake_case)."
        )

    root = _project_root()
    pack_dir = root / "rubrics" / "topic_packs" / args.topic_id

    if pack_dir.exists() and not args.overwrite:
        raise SystemExit(
            f"ERROR: topic pack already exists: {pack_dir}\n"
            "Use --overwrite only if you intentionally want to replace scaffold files."
        )

    pack_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "README.md": _build_readme(args.topic_id, args.title, args.question_type),
        "model_answer.json": _build_model_answer(args.topic_id, args.title, args.question_type),
        "fact_anchor.json": _build_fact_anchor(args.topic_id, args.title),
        "topic_importance.json": _build_topic_importance(
            args.topic_id,
            args.title,
            args.difficulty,
            args.importance,
        ),
        "logic_check.json": _build_logic_check(
            args.topic_id,
            args.title,
            args.question_type,
            args.difficulty,
        ),
    }

    for filename, payload in files.items():
        path = pack_dir / filename
        if isinstance(payload, dict):
            _write_json(path, payload)
        else:
            _write_text(path, payload)

    return pack_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a topic_pack scaffold.")
    parser.add_argument("--topic-id", required=True, help="lowercase snake_case topic id")
    parser.add_argument("--title", required=True, help="Korean topic title")
    parser.add_argument(
        "--question-type",
        default="PRINCIPLE_INTERPRETATION",
        help="question type used by model_answer and logic_check",
    )
    parser.add_argument(
        "--difficulty",
        default="THEORY_CORE",
        help="topic importance difficulty profile",
    )
    parser.add_argument(
        "--importance",
        default="CORE_MUST_PREPARE",
        help="topic selection importance",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="overwrite an existing topic pack scaffold",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    pack_dir = create_topic_pack(args)

    print("CREATED TOPIC PACK")
    print("path:", pack_dir)
    print()
    print("files:")
    for filename in [
        "README.md",
        "fact_anchor.json",
        "model_answer.json",
        "topic_importance.json",
        "logic_check.json",
    ]:
        print(" -", pack_dir / filename)

    print()
    print("NEXT:")
    print("  1. Replace TODO content with reviewed topic-specific rubric.")
    print("  2. Add precise routing_aliases and routing_field_points.")
    print("  3. Run: python3 scripts/rubric_manager.py validate-generated-pipeline")
    print("  4. Run routing smoke before commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
