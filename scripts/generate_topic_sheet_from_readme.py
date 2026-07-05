#!/usr/bin/env python3
"""Generate a human-reviewable Topic Sheet candidate from a topic-pack README.md.

This script is an authoring tool, not a runtime grading component.

Flow:
  rubrics/topic_packs/<topic_id>/README.md
    -> docs/topic_sheets/<topic_id>.md

Important:
  - This script does NOT generate JSON source files.
  - It only creates a Markdown Topic Sheet candidate for human review.
  - After review, use generate_topic_pack_from_sheet.py to create schema-locked JSON drafts.
  - If Gemini returns JSON-like wrapper output, this script will repair once and
    reject invalid Topic Sheet output instead of saving a broken file.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

try:
    from topic_review_llm import gemini_generate
except Exception as exc:  # pragma: no cover
    gemini_generate = None  # type: ignore[assignment]
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


DEFAULT_GENERATION_MODEL = (
    os.getenv("TOPIC_SHEET_GENERATION_GEMINI_MODEL")
    or os.getenv("TOPIC_PACK_GENERATION_GEMINI_MODEL")
    or os.getenv("TOPIC_REVIEW_GEMINI_MODEL")
    or os.getenv("GEMINI_MODEL")
    or "gemini-2.5-flash"
)


REQUIRED_SECTIONS = [
    "## 1. Topic metadata",
    "## 2. Core correct facts",
    "## 3. Acceptable answer expressions",
    "## 4. Fatal wrong claims",
    "## 5. Warn-level weak claims",
    "## 6. False positive cautions",
    "## 7. Regex candidate patterns",
    "## 8. fact_anchor.json generation guidance",
    "## 9. logic_check.json generation guidance",
    "## 10. model_answer.json generation guidance",
    "## 11. topic_importance.json generation guidance",
    "## 12. Human review checklist",
]


SYSTEM_PROMPT = """너는 산업계측제어기술사 채점 Bot의 Topic Sheet authoring agent다.

출력 형식은 절대 규칙이다.

반드시 Markdown 문서만 출력한다.
JSON object를 출력하지 않는다.
JSON wrapper를 출력하지 않는다.
{"title": ..., "content": ...} 같은 형태를 절대 쓰지 않는다.
markdown fence를 쓰지 않는다.
첫 번째 non-empty line은 반드시 "# <Korean title> Topic Sheet" 형식이어야 한다.
"# title", "# content", "# topic id" 같은 wrapper-style heading을 쓰지 않는다.

역할:
- README.md는 사람이 작성한 검토 메모이다.
- README.md를 JSON으로 바꾸지 말고, 사람이 검토할 Topic Sheet 후보로 구조화한다.
- Topic Sheet는 이후 schema-locked JSON generator의 입력으로 사용된다.
- 정답 fact, 허용 표현, fatal 오류, warn 오류, false positive 주의사항, regex 후보를 반드시 분리한다.
- fatal rule은 정답 기준과 명시적으로 충돌하는 경우에만 제안한다.
- 단순 누락과 애매한 표현은 fatal이 아니라 warn 또는 보완점으로 둔다.

출력은 오직 Markdown Topic Sheet 본문이다.
"""


def project_root() -> Path:
    """Resolve the prof_eng_answer repository root."""
    for candidate in [ROOT, Path.cwd(), Path("/workspace/prof_eng_answer")]:
        if (candidate / "rubrics" / "topic_packs").exists():
            return candidate
    raise SystemExit("ERROR: project root not found. Run inside prof_eng_answer repo.")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def strip_markdown_fence(text: str) -> str:
    """Remove a full-document markdown fence when the model wraps the answer."""
    raw = str(text or "").strip()
    if not raw.startswith("```"):
        return raw

    lines = raw.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def build_existing_json_context(topic_dir: Path, *, max_chars_per_file: int = 3500) -> str:
    """Load current topic-pack source JSON files as reference context.

    The context is intentionally truncated and labelled as reference-only so the
    model does not imitate JSON output format.
    """
    blocks: list[str] = []

    for filename in [
        "fact_anchor.json",
        "logic_check.json",
        "model_answer.json",
        "topic_importance.json",
    ]:
        path = topic_dir / filename
        if not path.exists():
            continue

        content = read_text(path).strip()
        if len(content) > max_chars_per_file:
            content = content[:max_chars_per_file].rstrip() + "\n... <truncated reference JSON>"

        blocks.append(
            f"### Reference only: {filename}\n"
            "The following is source JSON context. Do not copy its output format. "
            "Use it only to understand existing topic scope and schema names.\n\n"
            "```json\n"
            f"{content}\n"
            "```"
        )

    if not blocks:
        return "No existing source JSON files were found."

    return "\n\n".join(blocks)


def build_prompt(topic_id: str, readme_text: str, existing_json_context: str) -> str:
    required = "\n".join(REQUIRED_SECTIONS)

    return f"""
Generate a Markdown Topic Sheet candidate for a professional engineering answer-grading rubric.

ABSOLUTE OUTPUT CONTRACT:
- Output Markdown only.
- Do not output JSON.
- Do not output a JSON wrapper.
- Do not output keys like title/content/topic_id as top-level JSON.
- Do not use markdown code fences around the whole answer.
- The first non-empty line must be: "# <Korean title> Topic Sheet"
- The document must contain every required section below exactly.

REQUIRED SECTIONS:
{required}

Topic ID:
{topic_id}

Content rules:
- Use the README as the primary source.
- Use existing JSON context only as reference, not as an output format.
- Separate correct facts, acceptable expressions, fatal wrong expressions, warn-level issues, false-positive cautions, and regex candidates.
- Preserve technical correctness.
- Do not invent a new topic if the README already defines the topic.
- Do not weaken fatal errors into normal warnings when they break the core theory.
- Do not make over-broad regex candidates that catch correct contrastive statements.
- Regex candidates are only candidates. They must still be reviewed by a human before being promoted into logic_check.json.
- README is not the runtime source of truth. Runtime source of truth remains topic-pack JSON and generated rubric bank.

Important control-engineering caution:
- If the topic is about damping-ratio time response, distinguish ζ=1 critical damping and repeated root.
- If the topic is about frequency response/resonance, distinguish ωr, ωd, ωn and the resonance existence condition ζ<1/√2.
- Do not confuse time-domain damped natural frequency ωd=ωn√(1-ζ²) with frequency-domain resonance frequency ωr=ωn√(1-2ζ²).
- Do not confuse overshoot condition 0<ζ<1 with resonant-peak condition 0<ζ<1/√2.
- Do not treat ζ=1/√2 as critical damping. Critical damping is ζ=1.

README input:
```markdown
{readme_text}
```

Existing source JSON context:
{existing_json_context}
""".strip()


def _json_value_to_markdown(value: Any, *, level: int = 2) -> str:
    """Best-effort conversion for structured JSON when used in repair context.

    Normal generation should not rely on this. Validation still enforces the
    final required section headings.
    """
    lines: list[str] = []

    if isinstance(value, dict):
        for key, item in value.items():
            title = str(key).replace("_", " ").strip()
            if isinstance(item, str):
                lines.append(f"{'#' * min(level, 6)} {title}")
                lines.append("")
                lines.append(item.strip())
                lines.append("")
            elif isinstance(item, list):
                lines.append(f"{'#' * min(level, 6)} {title}")
                lines.append("")
                lines.append(_json_value_to_markdown(item, level=level + 1))
                lines.append("")
            elif isinstance(item, dict):
                lines.append(f"{'#' * min(level, 6)} {title}")
                lines.append("")
                lines.append(_json_value_to_markdown(item, level=level + 1))
                lines.append("")
            elif item is not None:
                lines.append(f"- {title}: {item}")
        return "\n".join(lines).strip()

    if isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                rendered = _json_value_to_markdown(item, level=level + 1)
                if rendered:
                    lines.append(rendered)
                    lines.append("")
            else:
                lines.append(f"- {item}")
        return "\n".join(lines).strip()

    if value is None:
        return ""

    return str(value).strip()


def extract_markdown_from_llm_response(text: str) -> str:
    """Extract Markdown from Gemini output without hiding bad format.

    Preferred output is plain Markdown. JSON output is accepted only as an
    intermediate string for repair/validation; invalid headings will be rejected
    by validate_topic_sheet_markdown().
    """
    raw = strip_markdown_fence(str(text or "")).strip()
    if not raw:
        return ""

    if not raw.lstrip().startswith("{"):
        return raw

    decoder = json.JSONDecoder()
    start = raw.find("{")
    data: Any | None = None
    while start >= 0:
        try:
            data, _end = decoder.raw_decode(raw[start:])
            break
        except Exception:
            start = raw.find("{", start + 1)

    if data is None:
        return raw

    if isinstance(data, dict):
        # Common wrapper cases. If content itself is a string, use it. This
        # supports {"content": "# ..."} while still rejecting {"title": ..., "content": [...]}
        # later when required sections are missing.
        for key in ["markdown", "topic_sheet", "topicSheet", "document", "text"]:
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return strip_markdown_fence(value).strip()

        value = data.get("content")
        if isinstance(value, str) and value.strip():
            return strip_markdown_fence(value).strip()

        return _json_value_to_markdown(data)

    return str(data).strip()



def normalize_topic_sheet_markdown(content: str, topic_id: str) -> str:
    # Normalize common Gemini heading variants into the required Topic Sheet shape.
    raw = strip_markdown_fence(str(content or "")).strip()
    if not raw:
        return raw

    first_line = next((line.strip() for line in raw.splitlines() if line.strip()), "")
    has_all_required = all(section in raw for section in REQUIRED_SECTIONS)
    wrapper_heading = re.search(
        r"(?m)^#\s+(title|content|topic id|topic_id)\s*$",
        raw,
        flags=re.IGNORECASE,
    )

    if (
        first_line.startswith("# ")
        and "topic sheet" in first_line.lower()
        and has_all_required
        and not wrapper_heading
    ):
        return raw

    def heading_key(value: str) -> str:
        value = re.sub(r"^\s*#+\s*", "", str(value or "").strip())
        value = value.lower().replace("_", " ")
        value = re.sub(r"[^0-9a-z가-힣]+", " ", value)
        return re.sub(r"\s+", " ", value).strip()

    lines = raw.splitlines()
    sections: list[tuple[str, str]] = []
    current_heading: str | None = None
    buf: list[str] = []

    for line in lines:
        match = re.match(r"^\s*#{1,2}\s+(.+?)\s*$", line)
        if match:
            if current_heading is not None:
                sections.append((current_heading, "\n".join(buf).strip()))
            current_heading = match.group(1).strip()
            buf = []
        else:
            buf.append(line)

    if current_heading is not None:
        sections.append((current_heading, "\n".join(buf).strip()))

    if not sections:
        return raw

    by_key: dict[str, str] = {}
    for heading, body in sections:
        by_key[heading_key(heading)] = body.strip()

    title_body = by_key.get("title", "")
    title = next((line.strip("- ").strip() for line in title_body.splitlines() if line.strip()), "")
    if not title:
        title = "Topic Sheet"
    if "topic sheet" not in title.lower():
        title = f"{title} Topic Sheet"

    topic_body = by_key.get("topic id", "") or by_key.get("topicid", "")
    topic_value = next((line.strip("- ").strip() for line in topic_body.splitlines() if line.strip()), "")
    if not topic_value:
        topic_value = topic_id

    section_aliases = {
        "topic metadata": "## 1. Topic metadata",
        "core correct facts": "## 2. Core correct facts",
        "acceptable expressions": "## 3. Acceptable answer expressions",
        "acceptable answer expressions": "## 3. Acceptable answer expressions",
        "fatal wrong claims": "## 4. Fatal wrong claims",
        "warn level weak claims": "## 5. Warn-level weak claims",
        "weak claims": "## 5. Warn-level weak claims",
        "false positive cautions": "## 6. False positive cautions",
        "regex candidate patterns": "## 7. Regex candidate patterns",
        "regex candidates": "## 7. Regex candidate patterns",
        "fact anchor json guidance": "## 8. fact_anchor.json generation guidance",
        "fact anchor json generation guidance": "## 8. fact_anchor.json generation guidance",
        "fact anchor generation guidance": "## 8. fact_anchor.json generation guidance",
        "logic check json guidance": "## 9. logic_check.json generation guidance",
        "logic check json generation guidance": "## 9. logic_check.json generation guidance",
        "logic check generation guidance": "## 9. logic_check.json generation guidance",
        "model answer json guidance": "## 10. model_answer.json generation guidance",
        "model answer json generation guidance": "## 10. model_answer.json generation guidance",
        "model answer generation guidance": "## 10. model_answer.json generation guidance",
        "topic importance json guidance": "## 11. topic_importance.json generation guidance",
        "topic importance json generation guidance": "## 11. topic_importance.json generation guidance",
        "topic importance generation guidance": "## 11. topic_importance.json generation guidance",
        "human review checklist": "## 12. Human review checklist",
    }

    canonical_blocks: dict[str, str] = {}
    for heading, body in sections:
        canonical = section_aliases.get(heading_key(heading))
        if canonical:
            canonical_blocks[canonical] = body.strip()

    metadata = canonical_blocks.get("## 1. Topic metadata", "").strip()
    if not metadata:
        title_ko = title.replace(" Topic Sheet", "").strip()
        metadata = "\n".join(
            [
                f"- topic_id: {topic_value}",
                f"- title_ko: {title_ko}",
            ]
        )
    elif topic_id not in metadata:
        metadata = f"- topic_id: {topic_value}\n" + metadata

    canonical_blocks["## 1. Topic metadata"] = metadata

    out: list[str] = [f"# {title}", ""]
    for section in REQUIRED_SECTIONS:
        out.append(section)
        out.append("")
        body = canonical_blocks.get(section, "").strip()
        out.append(body if body else "- Not provided by model output.")
        out.append("")

    return "\n".join(out).strip()

def validate_topic_sheet_markdown(content: str, topic_id: str) -> tuple[bool, list[str]]:
    """Validate generated Topic Sheet shape before writing it."""
    errors: list[str] = []
    text = str(content or "").strip()

    if not text:
        return False, ["empty output"]

    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    lower_first = first_line.lower()

    if not first_line.startswith("# "):
        errors.append("first non-empty line must start with '# '")

    if "topic sheet" not in lower_first.lower():
        errors.append("first heading must be a Topic Sheet title")

    forbidden_first_headings = {"# title", "# content", "# topic id", "# topic_id"}
    if lower_first in forbidden_first_headings:
        errors.append(f"wrapper-style first heading is not allowed: {first_line}")

    if text.lstrip().startswith("{"):
        errors.append("JSON-like output is not allowed")

    if topic_id not in text:
        errors.append(f"topic_id not found in output: {topic_id}")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing required section: {section}")

    if re.search(r"(?m)^#\s+(title|content|topic id|topic_id)\s*$", text, flags=re.IGNORECASE):
        errors.append("wrapper-style headings # title/# content/# topic id are not allowed")

    return not errors, errors


def build_repair_prompt(topic_id: str, original_prompt: str, bad_content: str, validation_errors: list[str]) -> str:
    required = "\n".join(REQUIRED_SECTIONS)
    errors = "\n".join(f"- {e}" for e in validation_errors)
    return f"""
Your previous answer failed Topic Sheet validation.

Fix it now.

ABSOLUTE OUTPUT CONTRACT:
- Output Markdown only.
- Do not output JSON.
- Do not output a JSON wrapper.
- Do not use markdown fences.
- First non-empty line must be "# <Korean title> Topic Sheet".
- Include every required section exactly.

Required sections:
{required}

Topic ID that must appear:
{topic_id}

Validation errors:
{errors}

Previous invalid output:
```text
{bad_content[:12000]}
```

Rewrite the previous output into the exact required Markdown Topic Sheet format.
Do not summarize.
Do not explain.
Return only the corrected Markdown document.
""".strip()


def call_gemini_markdown(
    prompt: str,
    *,
    model: str | None,
    timeout: int | None,
    max_output_tokens: int | None,
) -> dict[str, Any]:
    if gemini_generate is None:
        raise SystemExit(f"ERROR: topic_review_llm import failed: {_IMPORT_ERROR}")

    response = gemini_generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        model=model,
        timeout=timeout,
        temperature=0.1,
        max_output_tokens=max_output_tokens,
    )

    content = extract_markdown_from_llm_response(str(response.get("content") or ""))
    return {
        "provider": response.get("provider"),
        "model": response.get("model"),
        "content": content,
        "raw_content": str(response.get("content") or ""),
    }


def call_markdown_llm(
    prompt: str,
    *,
    topic_id: str,
    model: str | None,
    timeout: int | None,
    max_output_tokens: int | None,
    allow_repair: bool = True,
) -> dict[str, Any]:
    """Call Gemini and return validated Markdown content."""
    first = call_gemini_markdown(
        prompt,
        model=model,
        timeout=timeout,
        max_output_tokens=max_output_tokens,
    )

    content = str(first.get("content") or "").strip()
    content = normalize_topic_sheet_markdown(content, topic_id)
    ok, errors = validate_topic_sheet_markdown(content, topic_id)
    if ok:
        first["content"] = content
        first["validation_errors"] = []
        first["repaired"] = False
        return first

    if not allow_repair:
        raise SystemExit(
            "ERROR: LLM output is not a valid Topic Sheet.\n"
            + "\n".join(f"- {e}" for e in errors)
            + "\n\nOutput preview:\n"
            + content[:2000]
        )

    repair_prompt = build_repair_prompt(topic_id, prompt, content, errors)
    repaired = call_gemini_markdown(
        repair_prompt,
        model=model,
        timeout=timeout,
        max_output_tokens=max_output_tokens,
    )

    repaired_content = str(repaired.get("content") or "").strip()
    repaired_content = normalize_topic_sheet_markdown(repaired_content, topic_id)
    ok2, errors2 = validate_topic_sheet_markdown(repaired_content, topic_id)
    if ok2:
        repaired["content"] = repaired_content
        repaired["validation_errors"] = []
        repaired["repaired"] = True
        repaired["first_invalid_content"] = content
        repaired["first_validation_errors"] = errors
        return repaired

    raise SystemExit(
        "ERROR: LLM output is still not a valid Topic Sheet after one repair attempt.\n"
        + "\nFirst validation errors:\n"
        + "\n".join(f"- {e}" for e in errors)
        + "\n\nSecond validation errors:\n"
        + "\n".join(f"- {e}" for e in errors2)
        + "\n\nSecond output preview:\n"
        + repaired_content[:3000]
    )


def save_prompt_report(report_dir: Path, stamp: str, topic_id: str, prompt: str) -> Path:
    path = report_dir / f"topic_sheet_generation_{topic_id}_{stamp}_prompt.md"
    write_text(
        path,
        "\n".join(
            [
                f"# Topic Sheet Generation Prompt: {topic_id}",
                "",
                f"timestamp: {stamp}",
                "",
                "```text",
                prompt,
                "```",
                "",
            ]
        ),
    )
    return path


def save_raw_report(
    report_dir: Path,
    stamp: str,
    topic_id: str,
    readme_path: Path,
    out_path: Path,
    result: dict[str, Any],
) -> Path:
    path = report_dir / f"topic_sheet_generation_{topic_id}_{stamp}_raw.json"
    data = {
        "topic_id": topic_id,
        "readme": str(readme_path),
        "out": str(out_path),
        "provider": result.get("provider"),
        "model": result.get("model"),
        "repaired": result.get("repaired"),
        "validation_errors": result.get("validation_errors"),
        "first_validation_errors": result.get("first_validation_errors"),
        "content": result.get("content"),
        "raw_content": result.get("raw_content"),
        "first_invalid_content": result.get("first_invalid_content"),
    }
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate a human-reviewable Topic Sheet candidate from a topic-pack README.md."
    )
    p.add_argument("--topic-id", required=True)
    p.add_argument(
        "--readme",
        default=None,
        help="README path. Default: rubrics/topic_packs/<topic-id>/README.md",
    )
    p.add_argument(
        "--out",
        default=None,
        help="Output Topic Sheet path. Default: docs/topic_sheets/<topic-id>.md",
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Only render and save prompt; do not call LLM.",
    )
    p.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print prompt to stdout. Implies no LLM call.",
    )
    p.add_argument(
        "--no-repair",
        action="store_true",
        help="Do not do the one-shot repair call when Gemini returns invalid Markdown.",
    )
    p.add_argument(
        "--model",
        default=DEFAULT_GENERATION_MODEL,
        help=(
            "Gemini model for Topic Sheet generation. "
            "Default: env TOPIC_SHEET_GENERATION_GEMINI_MODEL, "
            "then TOPIC_PACK_GENERATION_GEMINI_MODEL, "
            "then TOPIC_REVIEW_GEMINI_MODEL, then GEMINI_MODEL, "
            "then gemini-2.5-flash."
        ),
    )
    p.add_argument("--timeout", type=int, default=None)
    p.add_argument("--max-output-tokens", type=int, default=8192)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    root = project_root()
    topic_dir = root / "rubrics" / "topic_packs" / args.topic_id

    readme_path = Path(args.readme) if args.readme else topic_dir / "README.md"
    if not readme_path.is_absolute():
        readme_path = root / readme_path

    out_path = Path(args.out) if args.out else root / "docs" / "topic_sheets" / f"{args.topic_id}.md"
    if not out_path.is_absolute():
        out_path = root / out_path

    if not topic_dir.exists():
        raise SystemExit(f"ERROR: topic directory not found: {topic_dir}")

    if not readme_path.exists():
        raise SystemExit(f"ERROR: README not found: {readme_path}")

    if out_path.exists() and not args.overwrite:
        raise SystemExit(f"ERROR: output already exists. Use --overwrite: {out_path}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = root / "reports"

    readme_text = read_text(readme_path)
    existing_json_context = build_existing_json_context(topic_dir)
    prompt = build_prompt(args.topic_id, readme_text, existing_json_context)

    prompt_report = save_prompt_report(report_dir, stamp, args.topic_id, prompt)
    print(f"prompt: {prompt_report.relative_to(root)}")
    print(f"model: {args.model}")

    if args.print_prompt:
        print(prompt)
        return 0

    if args.dry_run:
        print("dry-run: LLM call skipped")
        return 0

    result = call_markdown_llm(
        prompt,
        topic_id=args.topic_id,
        model=args.model,
        timeout=args.timeout,
        max_output_tokens=args.max_output_tokens,
        allow_repair=not args.no_repair,
    )

    content = str(result["content"] or "").rstrip() + "\n"
    write_text(out_path, content)
    raw_report = save_raw_report(report_dir, stamp, args.topic_id, readme_path, out_path, result)

    print(f"wrote: {out_path.relative_to(root)}")
    print(f"raw: {raw_report.relative_to(root)}")
    if result.get("repaired"):
        print("NOTE: first Gemini output was invalid; saved one-shot repaired Markdown.")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
