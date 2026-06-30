#!/usr/bin/env python3
"""Archive stale documentation and rewrite docs/README.md.

This script does not delete stale documents. It moves them under
docs/archive/<timestamp>/ so that history remains available.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

STALE_DOCS = [
    "current_grading_architecture.md",
    "docs/structure_review.md",
    "docs/migration_plan.md",
]

DOC_INDEX = """# Documentation Index

이 디렉터리는 현재 코드와 직접 연결되는 운영 문서를 중심으로 유지한다.

## 현재 기준 문서

| 문서 | 역할 |
|---|---|
| `operation_runbook.md` | Bot 운영, 재시작, 장애 대응 |
| `docker_compose_usage.md` | Docker Compose 기반 실행 방식 |
| `grading_architecture.md` | A/B/C/D/E 25점 채점 구조 |
| `question_type_taxonomy.md` | Question Type v2 기준 |
| `difficulty_and_selection_strategy.md` | 난이도와 문항 선택 전략 |
| `llm_provider.md` | Gemini/CLOVA provider 설정 |
| `rubric_authoring_guide.md` | Rubric Bank 작성과 수정 방법 |
| `model_answer_generator_prompt.md` | Model Answer 초안 생성 프롬프트 |
| `fact_anchor_generator_prompt.md` | Fact Anchor 초안 생성 프롬프트 |
| `topic_importance_generator_prompt.md` | Topic importance 초안 생성 프롬프트 |

## Archive

오래된 구조 설명, migration 기록, 현재 코드와 충돌할 수 있는 문서는 `docs/archive/` 아래로 이동한다.

현재 기준은 다음 순서로 판단한다.

1. 현재 Python 코드
2. 현재 JSON Rubric Bank
3. `README.md`
4. `docs/README.md`
5. 각 세부 docs 문서

## 검증 명령

```bash
python3 scripts/validate_model_fact_consistency.py
python3 scripts/rubric_manager.py validate-all
git diff --check
```
"""


def existing_targets() -> list[tuple[Path, Path]]:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_root = ROOT / "docs" / "archive" / stamp
    targets: list[tuple[Path, Path]] = []

    for rel_path in STALE_DOCS:
        src = ROOT / rel_path
        if src.exists():
            targets.append((src, archive_root / rel_path))

    return targets


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    targets = existing_targets()

    if args.dry_run:
        print("DRY RUN")
        if not targets:
            print("no stale docs found")
        for src, dst in targets:
            print("move:", src.relative_to(ROOT), "->", dst.relative_to(ROOT))
        print("rewrite: docs/README.md")
        return 0

    for src, dst in targets:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        print("moved:", src.relative_to(ROOT), "->", dst.relative_to(ROOT))

    docs_dir = ROOT / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    index_path = docs_dir / "README.md"
    index_path.write_text(DOC_INDEX, encoding="utf-8")
    print("wrote:", index_path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
