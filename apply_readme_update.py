#!/usr/bin/env python3
from pathlib import Path

readme = Path("README.md")
section_path = Path("current_grading_architecture.md")

start = "<!-- CURRENT_GRADING_ARCHITECTURE_START -->"
end = "<!-- CURRENT_GRADING_ARCHITECTURE_END -->"

if not section_path.exists():
    raise SystemExit(f"section file not found: {section_path}")

section = section_path.read_text(encoding="utf-8").strip() + "\n"

if readme.exists():
    text = readme.read_text(encoding="utf-8")
else:
    text = "# 기술사 답안 채점 Telegram Bot\n"

if start in text and end in text:
    before = text.split(start, 1)[0].rstrip()
    after = text.split(end, 1)[1].lstrip()
    updated = before + "\n\n" + section + "\n\n" + after
else:
    updated = text.rstrip() + "\n\n" + section

readme.write_text(updated.rstrip() + "\n", encoding="utf-8")
print("README.md updated")
