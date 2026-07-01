#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


ROOT_README_SECTION = """<!-- RUBRIC_AUDIT_WORKFLOW_START -->
## Rubric audit workflow

Rubric 변경 후에는 다음 audit 명령으로 Fact Anchor, Model Answer Bank, Model Answer relationship, priority minor gate를 함께 검증한다.

```bash
python3 scripts/rubric_audit/run_rubric_audit.py
```

운영 통과 기준은 다음과 같다.

```text
Fact Anchor MAJOR = 0
Model Answer relationship MAJOR = 0
validate-all = OK
priority MINOR = 0
```

일반 `MINOR`는 advisory로 유지할 수 있다. `MINOR`를 0으로 만들기 위해 model answer를 과도하게 늘리거나 validator에 과적합하지 않는다.

대표 산출물은 다음 파일에 기록된다.

```text
reports/rubric_audit_summary.md
reports/model_answer_relationship_validation.md
reports/model_answer_relationship_minor_analysis.md
reports/model_answer_relationship_priority_minors.md
reports/fact_anchor_quality_audit.md
```

관련 audit 도구는 `scripts/rubric_audit/`에 모아둔다.
<!-- RUBRIC_AUDIT_WORKFLOW_END -->
"""


SCRIPTS_README_SECTION = """<!-- RUBRIC_AUDIT_TOOLS_START -->
## Rubric audit tools

Rubric 품질 검증 관련 도구는 `scripts/rubric_audit/`에 모아둔다.

```bash
python3 scripts/rubric_audit/run_rubric_audit.py
```

통과 기준:

```text
Fact Anchor MAJOR = 0
Model Answer relationship MAJOR = 0
validate-all = OK
priority MINOR = 0
```
<!-- RUBRIC_AUDIT_TOOLS_END -->
"""


def upsert_section(path: Path, section: str, start: str, end: str, *, create: bool = False) -> bool:
    if not path.exists():
        if not create:
            return False
        text = f"# {path.stem}\n"
    else:
        text = path.read_text(encoding="utf-8")

    if start in text and end in text:
        before = text.split(start)[0].rstrip()
        after = text.split(end, 1)[1].lstrip()
        new_text = before + "\n\n" + section.strip() + "\n\n" + after
    else:
        new_text = text.rstrip() + "\n\n" + section.strip() + "\n"

    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    root_readme = ROOT / "README.md"
    scripts_readme = ROOT / "scripts" / "README.md"

    updated_root = upsert_section(
        root_readme,
        ROOT_README_SECTION,
        "<!-- RUBRIC_AUDIT_WORKFLOW_START -->",
        "<!-- RUBRIC_AUDIT_WORKFLOW_END -->",
        create=True,
    )

    updated_scripts = upsert_section(
        scripts_readme,
        SCRIPTS_README_SECTION,
        "<!-- RUBRIC_AUDIT_TOOLS_START -->",
        "<!-- RUBRIC_AUDIT_TOOLS_END -->",
        create=False,
    )

    print("updated:", root_readme if updated_root else "skip README.md")
    print("updated:", scripts_readme if updated_scripts else "skip scripts/README.md")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
