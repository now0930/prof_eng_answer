#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from topic_review_llm import extract_json_object, gemini_generate, get_topic_review_llm_settings  # noqa: E402


PACK_FILES = [
    "README.md",
    "fact_anchor.json",
    "model_answer.json",
    "topic_importance.json",
    "logic_check.json",
]

VALID_REVIEW_LEVELS = {"pass", "minor", "major", "blocker"}


def _project_root() -> Path:
    here = Path(__file__).resolve()
    candidates = [here.parents[1], Path.cwd(), Path("/workspace/prof_eng_answer")]
    for candidate in candidates:
        if (candidate / "rubrics" / "topic_packs").exists():
            return candidate
    raise SystemExit("ERROR: project root not found. Run from prof_eng_answer repo.")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_pack(root: Path, topic_id: str) -> dict[str, Any]:
    pack_dir = root / "rubrics" / "topic_packs" / topic_id
    if not pack_dir.exists():
        raise SystemExit(f"ERROR: topic pack not found: {pack_dir}")

    files: dict[str, str] = {}
    parsed_json: dict[str, Any] = {}

    for filename in PACK_FILES:
        path = pack_dir / filename
        if not path.exists():
            files[filename] = "<MISSING>"
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        files[filename] = text

        if path.suffix == ".json":
            try:
                parsed_json[filename] = json.loads(text)
            except json.JSONDecodeError as exc:
                parsed_json[filename] = {
                    "_parse_error": str(exc),
                    "_raw_preview": text[:2000],
                }

    return {
        "topic_id": topic_id,
        "pack_dir": str(pack_dir),
        "files": files,
        "parsed_json": parsed_json,
    }


def _listify(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _compact_json(value: Any, max_chars: int = 12000) -> str:
    text = json.dumps(value, ensure_ascii=False, indent=2)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n[TRUNCATED]\n"


def _extract_fact_guardrails(pack: dict[str, Any]) -> dict[str, Any]:
    parsed = pack.get("parsed_json") or {}
    fact_anchor = parsed.get("fact_anchor.json") or {}
    model_answer = parsed.get("model_answer.json") or {}
    topic_importance = parsed.get("topic_importance.json") or {}
    logic_check = parsed.get("logic_check.json") or {}

    return {
        "topic_id": pack.get("topic_id"),
        "canonical_fact_anchor": fact_anchor,
        "model_answer_under_review": model_answer,
        "topic_importance_under_review": topic_importance,
        "logic_check_under_review": logic_check,
    }


def _json_schema_text() -> str:
    return json.dumps(
        {
            "review_level": "pass|minor|major|blocker",
            "summary": "한 문단 요약. 이 값은 반드시 문자열이다.",
            "issues": [
                {
                    "severity": "minor|major|blocker",
                    "file": "fact_anchor.json|model_answer.json|topic_importance.json|logic_check.json|cross-file",
                    "message": "문제 설명",
                    "recommendation": "수정 제안",
                    "evidence": "topic_pack 안에서 확인한 근거",
                }
            ],
            "fact_anchor_consistency": {
                "status": "pass|watch|fail",
                "notes": ["fact_anchor를 기준으로 한 정합성 검토"],
            },
            "model_answer_review": {
                "status": "pass|watch|fail",
                "missing_high_score_points": [],
                "unsafe_or_overstated_points": [],
                "notes": [],
            },
            "routing_review": {
                "status": "pass|watch|fail",
                "strong_terms": [],
                "possible_alias_pollution": ["오염 가능 alias 또는 불완전한 공식 일부 alias"],
                "missing_aliases": ["추가하면 좋은 alias. 오염 alias를 여기에 넣지 말 것"],
            },
            "logic_check_review": {
                "status": "not_needed|pass|watch|fail",
                "notes": [],
            },
            "topic_importance_review": {
                "status": "pass|watch|fail",
                "notes": [],
            },
            "recommended_actions": [],
        },
        ensure_ascii=False,
        indent=2,
    )


def _system_prompt() -> str:
    return "\n".join(
        [
            "너는 산업계측제어기술사 topic_pack의 보조 감사자(auditor)다.",
            "너는 topic_pack을 채점하거나 승인하지 않는다.",
            "너는 새로운 기술 사실을 생성하지 않는다.",
            "fact_anchor.json을 canonical source of truth로 간주한다.",
            "model_answer.json, topic_importance.json, logic_check.json, routing term이 fact_anchor와 일관되는지만 검토한다.",
            "확실하지 않은 내용은 단정하지 말고 watch 또는 검토 필요로 표시한다.",
            "출력은 반드시 유효한 JSON object 하나만 한다.",
            "markdown fence, 설명문, 주석, 학습 질문, 튜터식 요약을 절대 출력하지 않는다.",
        ]
    )


def _build_prompt(pack: dict[str, Any], max_context_chars: int) -> str:
    guardrails = _extract_fact_guardrails(pack)
    schema = _json_schema_text()

    raw_files = {
        name: (pack.get("files") or {}).get(name, "<MISSING>")
        for name in PACK_FILES
    }

    raw_text = json.dumps(raw_files, ensure_ascii=False, indent=2)
    if len(raw_text) > max_context_chars:
        raw_text = raw_text[:max_context_chars] + "\n[TRUNCATED]\n"

    return "\n".join(
        [
            "아래 topic_pack을 fact_anchor 기준으로 감사하라.",
            "",
            "중요 원칙:",
            "- fact_anchor.json에 있는 사실을 기준으로 삼는다.",
            "- fact_anchor와 다른 새로운 공식/조건/해석을 만들지 않는다.",
            "- topic_pack이 이미 올바른 사실을 포함하면 그 사실을 바꾸라고 제안하지 않는다.",
            "- review_level은 자동 release 판정이 아니라 LLM 의견이다.",
            "- 불완전한 공식 일부 alias는 missing_aliases가 아니라 possible_alias_pollution에 넣는다.",
            "- 예: canonical 공식이 ωr=ωn√(1−2ζ²)인데 alias가 ωr=ωn이면 pollution/watch 대상으로 본다.",
            "",
            "감사 초점:",
            "1. fact_anchor와 model_answer의 모순",
            "2. routing_aliases / field_connection_points의 오염 가능성",
            "3. topic_importance의 난이도/고득점 unlock 조건 적정성",
            "4. logic_check 필요 여부 및 topic 적합성",
            "5. 기술사 답안 관점의 누락 포인트",
            "",
            "반드시 아래 JSON schema와 호환되는 JSON object만 출력하라.",
            "",
            "JSON schema:",
            schema,
            "",
            "compact canonical context:",
            _compact_json(guardrails),
            "",
            "raw topic_pack files:",
            raw_text,
        ]
    )


def _review_schema_errors(data: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["review is not a JSON object"]

    level = data.get("review_level")
    if level is None:
        level = data.get("verdict")
        if isinstance(level, str):
            data["review_level"] = level

    if not isinstance(level, str) or level.strip().lower() not in VALID_REVIEW_LEVELS:
        errors.append(f"invalid review_level: {level!r}")

    summary = data.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        errors.append("summary must be a non-empty string")

    if not isinstance(data.get("issues"), list):
        errors.append("issues must be a list")

    for key in [
        "fact_anchor_consistency",
        "model_answer_review",
        "routing_review",
        "logic_check_review",
        "topic_importance_review",
    ]:
        value = data.get(key)
        if not isinstance(value, dict):
            errors.append(f"{key} must be an object")
            continue
        status = value.get("status")
        if not isinstance(status, str) or not status.strip():
            errors.append(f"{key}.status must be a non-empty string")

    if not isinstance(data.get("recommended_actions"), list):
        errors.append("recommended_actions must be a list")

    return errors


def _repair_with_gemini(
    *,
    original_prompt: str,
    raw_content: str,
    schema_errors: list[str],
    model: str | None,
    timeout: int | None,
    temperature: float | None,
    max_output_tokens: int | None,
) -> tuple[dict[str, Any] | None, str | None, str]:
    if os.getenv("TOPIC_REVIEW_REPAIR_JSON", "1").strip() == "0":
        return None, "json repair disabled", ""

    repair_prompt = "\n".join(
        [
            "이전 topic_pack review 응답이 JSON schema를 만족하지 못했다.",
            "원래 topic_pack 검토를 다시 수행하여 유효한 JSON object 하나만 출력하라.",
            "빈 객체, markdown, 설명문은 금지다.",
            "",
            "schema errors:",
            json.dumps(schema_errors, ensure_ascii=False, indent=2),
            "",
            "required JSON schema:",
            _json_schema_text(),
            "",
            "original review prompt:",
            original_prompt[:50000],
            "",
            "previous invalid response:",
            raw_content[:12000],
        ]
    )

    response = gemini_generate(
        system_prompt=_system_prompt(),
        user_prompt=repair_prompt,
        model=model,
        timeout=timeout,
        temperature=0.0 if temperature is None else min(float(temperature), 0.1),
        max_output_tokens=max_output_tokens,
    )

    repair_content = str(response.get("content", ""))
    parsed, parse_error = extract_json_object(repair_content)
    return parsed, parse_error, repair_content


def _normalize_review(parsed: dict[str, Any]) -> dict[str, Any]:
    data = dict(parsed)

    if "review_level" not in data and isinstance(data.get("verdict"), str):
        data["review_level"] = data["verdict"]

    data["review_level"] = str(data.get("review_level", "")).strip().lower()
    data["summary"] = str(data.get("summary", "")).strip()

    if not isinstance(data.get("issues"), list):
        data["issues"] = []

    defaults = {
        "fact_anchor_consistency": {"status": "unknown", "notes": []},
        "model_answer_review": {
            "status": "unknown",
            "missing_high_score_points": [],
            "unsafe_or_overstated_points": [],
            "notes": [],
        },
        "routing_review": {
            "status": "unknown",
            "strong_terms": [],
            "possible_alias_pollution": [],
            "missing_aliases": [],
        },
        "logic_check_review": {"status": "unknown", "notes": []},
        "topic_importance_review": {"status": "unknown", "notes": []},
    }

    for key, default in defaults.items():
        if not isinstance(data.get(key), dict):
            data[key] = default

    if not isinstance(data.get("recommended_actions"), list):
        data["recommended_actions"] = []

    return data


def _invalid_review(
    *,
    parse_error: str | None,
    schema_errors: list[str],
    raw_content: str,
) -> dict[str, Any]:
    return {
        "review_level": "parse_error",
        "summary": "Gemini 응답을 유효한 topic review JSON으로 변환하지 못했습니다.",
        "issues": [
            {
                "severity": "major",
                "file": "llm_response",
                "message": "; ".join([x for x in [parse_error, *schema_errors] if x]),
                "recommendation": "프롬프트, 모델, max context 길이를 조정하고 다시 실행하세요.",
                "evidence": raw_content[:1000],
            }
        ],
        "fact_anchor_consistency": {"status": "unknown", "notes": []},
        "model_answer_review": {
            "status": "unknown",
            "missing_high_score_points": [],
            "unsafe_or_overstated_points": [],
            "notes": [],
        },
        "routing_review": {
            "status": "unknown",
            "strong_terms": [],
            "possible_alias_pollution": [],
            "missing_aliases": [],
        },
        "logic_check_review": {"status": "unknown", "notes": []},
        "topic_importance_review": {"status": "unknown", "notes": []},
        "recommended_actions": [],
    }


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _section_lines(review: dict[str, Any], key: str) -> list[str]:
    value = review.get(key)
    lines: list[str] = []
    if isinstance(value, dict):
        if value.get("status"):
            lines.append(f"- status: {value.get('status')}")
        for sub_key, sub_value in value.items():
            if sub_key == "status":
                continue
            lines.append(f"- {sub_key}: {sub_value}")
    else:
        lines.append(str(value))
    return lines


def _review_to_markdown(report: dict[str, Any]) -> str:
    review = report.get("review") or {}
    metadata = report.get("metadata") or {}

    lines = [
        f"# Topic Pack Gemini Review: {metadata.get('topic_id', '')}",
        "",
        "## Metadata",
        "",
        f"- provider: {metadata.get('provider', '')}",
        f"- model: {metadata.get('model', '')}",
        f"- response_mime_type: {metadata.get('response_mime_type', '')}",
        f"- review_level: {review.get('review_level', '')}",
        f"- generated_at: {metadata.get('generated_at', '')}",
        "",
        "## Summary",
        "",
        str(review.get("summary", "")).strip() or "(empty)",
        "",
        "## Issues",
        "",
    ]

    issues = _as_list(review.get("issues"))
    if not issues:
        lines.append("- 없음")
    else:
        for issue in issues:
            if isinstance(issue, dict):
                lines.append(
                    f"- **{issue.get('severity', '')}** `{issue.get('file', '')}`: "
                    f"{issue.get('message', '')} / 제안: {issue.get('recommendation', '')}"
                )
            else:
                lines.append(f"- {issue}")

    sections = [
        ("Fact Anchor Consistency", "fact_anchor_consistency"),
        ("Model Answer Review", "model_answer_review"),
        ("Routing Review", "routing_review"),
        ("Logic Check Review", "logic_check_review"),
        ("Topic Importance Review", "topic_importance_review"),
    ]

    for title, key in sections:
        lines.extend(["", f"## {title}", ""])
        lines.extend(_section_lines(review, key))

    lines.extend(["", "## Recommended Actions", ""])
    actions = _as_list(review.get("recommended_actions"))
    if not actions:
        lines.append("- 없음")
    else:
        for action in actions:
            lines.append(f"- {action}")

    lines.append("")
    return "\n".join(lines)


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Review a topic_pack with Gemini.")
    parser.add_argument("--topic-id", required=True, help="topic id under rubrics/topic_packs")
    parser.add_argument("--output-dir", default="reports", help="report output directory")
    parser.add_argument("--model", default=None, help="override TOPIC_REVIEW_GEMINI_MODEL/GEMINI_MODEL")
    parser.add_argument("--timeout", type=int, default=None, help="override topic review timeout")
    parser.add_argument("--temperature", type=float, default=None, help="override topic review temperature")
    parser.add_argument("--max-output-tokens", type=int, default=None, help="override Gemini maxOutputTokens; default 8192")
    parser.add_argument(
        "--max-context-chars",
        type=int,
        default=int(os.getenv("TOPIC_REVIEW_MAX_CONTEXT_CHARS", "60000")),
        help="maximum raw topic_pack context chars sent to Gemini",
    )
    parser.add_argument("--print-prompt", action="store_true", help="print prompt and exit without calling Gemini")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    root = _project_root()
    pack = _read_pack(root, args.topic_id)
    prompt = _build_prompt(pack, args.max_context_chars)
    system_prompt = _system_prompt()

    settings = get_topic_review_llm_settings(
        model=args.model,
        timeout=args.timeout,
        temperature=args.temperature,
        max_output_tokens=args.max_output_tokens,
    )

    if args.print_prompt:
        print("SYSTEM:")
        print(system_prompt)
        print("\nUSER:")
        print(prompt)
        return 0

    print("TOPIC PACK GEMINI REVIEW")
    print("provider:", settings.provider)
    print("model:", settings.model)
    print("response_mime_type:", settings.response_mime_type)
    print("topic_id:", args.topic_id)

    response = gemini_generate(
        system_prompt=system_prompt,
        user_prompt=prompt,
        model=args.model,
        timeout=args.timeout,
        temperature=args.temperature,
        max_output_tokens=args.max_output_tokens,
    )

    content = str(response.get("content", ""))
    parsed, parse_error = extract_json_object(content)
    schema_errors = _review_schema_errors(parsed) if parsed is not None else ["initial response is not a JSON object"]
    repair_content = ""

    if parsed is None or schema_errors:
        repaired, repair_error, repair_content = _repair_with_gemini(
            original_prompt=prompt,
            raw_content=content,
            schema_errors=schema_errors if schema_errors else [parse_error or "parse error"],
            model=args.model,
            timeout=args.timeout,
            temperature=args.temperature,
            max_output_tokens=args.max_output_tokens,
        )
        if repaired is not None:
            parsed = repaired
            parse_error = None
            schema_errors = _review_schema_errors(parsed)
        else:
            parse_error = f"initial parse error: {parse_error}; repair error: {repair_error}"

    if parsed is None or schema_errors:
        review = _invalid_review(
            parse_error=parse_error,
            schema_errors=schema_errors,
            raw_content=content,
        )
    else:
        review = _normalize_review(parsed)

    out_dir = root / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = _timestamp()
    base = f"topic_pack_gemini_review_{args.topic_id}_{ts}"
    json_path = out_dir / f"{base}.json"
    md_path = out_dir / f"{base}.md"

    report = {
        "metadata": {
            "topic_id": args.topic_id,
            "provider": response.get("provider"),
            "model": response.get("model"),
            "temperature": response.get("temperature"),
            "timeout": response.get("timeout"),
            "max_output_tokens": response.get("max_output_tokens"),
            "response_mime_type": response.get("response_mime_type"),
            "generated_at": ts,
            "schema_errors": schema_errors,
        },
        "review": review,
        "raw_content": content,
        "repair_content": repair_content,
    }

    _write_json(json_path, report)
    md_path.write_text(_review_to_markdown(report), encoding="utf-8")

    print()
    print("review_level:", review.get("review_level"))
    print("summary:", review.get("summary"))
    print("issues:", len(_as_list(review.get("issues"))))
    if schema_errors:
        print("schema_errors:", schema_errors)
    print()
    print("wrote:", json_path)
    print("wrote:", md_path)

    level = str(review.get("review_level", "")).lower()
    if level in {"blocker", "parse_error"}:
        return 2
    if level == "major":
        return 1 if os.getenv("TOPIC_REVIEW_FAIL_ON_MAJOR", "0") == "1" else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
