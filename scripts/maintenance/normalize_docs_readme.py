from __future__ import annotations

from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS_README = ROOT / "docs" / "README.md"


CANONICAL = """# Docs Index

이 디렉터리는 `prof_eng_answer`의 운영, 채점 구조, provider, Question Type, Difficulty, Rubric Bank 문서를 보관한다.

## 1. 문서 우선순위

문서끼리 설명이 충돌하면 다음 순서로 판단한다.

1. 현재 Python 코드
2. 현재 JSON Rubric Bank
3. 루트 `README.md`
4. `docs/README.md`
5. 각 세부 docs 문서
6. migration/reference 문서

현재 실행 코드와 충돌하는 오래된 설계 설명은 운영 기준으로 사용하지 않는다.

## 2. 현재 기준 문서

| 문서 | 단일 책임 | 주요 근거 파일 |
|---|---|---|
| `operation_runbook.md` | 운영 점검, 재시작, 장애 대응 | `bot.py`, Docker Compose, logs |
| `docker_compose_usage.md` | Compose 기반 실행 방식 | `docker-compose.*`, `prof_eng_answer_bot` |
| `grading_architecture.md` | 채점 pipeline과 A/B/C/D/E 구조 | `grading_agents.py`, `rubrics/scoring_model/default.json` |
| `question_type_taxonomy.md` | Question Type v2 taxonomy와 coverage | `question_type_taxonomy.py`, `rubrics/question_types/default.json` |
| `difficulty_and_selection_strategy.md` | Difficulty Profile, ceiling, 문항 선택 전략 | `difficulty_strategy.py`, `difficulty_score_ceiling.py`, `rubrics/difficulty_profiles/default.json` |
| `llm_provider.md` | Gemini/CLOVA/Ollama provider 구조 | `llm_provider_router.py`, `llm_provider_settings.py`, `gemini_grader.py`, `clova_grader.py` |
| `rubric_authoring_guide.md` | Rubric JSON Bank 수정·검증 절차 | `scripts/rubric_manager.py`, `rubrics/*` |

## 3. LLM 생성 보조 문서

아래 문서는 코드가 직접 실행하는 문서가 아니라, JSON 초안을 만들 때 쓰는 작업 보조 문서다.

| 문서 | 대상 JSON | 설명 |
|---|---|---|
| `fact_anchor_generator_prompt.md` | `rubrics/fact_anchors/` | 주제별 핵심 Fact, 수식, 판정 기준, 감점 위험 요소 초안 작성용 |
| `model_answer_generator_prompt.md` | `rubrics/model_answers/` | 모범 답안 Bank 초안, 답안 구조, 고득점 요소 작성용 |
| `topic_importance_generator_prompt.md` | `rubrics/topic_importance/` | 주제 중요도, 선택 전략, 반복 출제 가능성 초안 작성용 |

이 문서들은 현재 채점 코드가 직접 읽는 기준 문서는 아니므로 active 문서 목록에서는 제외하고 `docs/archive/`에 보관한다.

## 4. Reference 문서

| 문서 | 성격 |
|---|---|
| `migration_plan.md` | 구조 변경 및 migration 기록 |
| `structure_review.md` | 과거 구조 검토와 설계 판단 기록 |

이 문서들은 현재 실행 코드와 1:1로 맞지 않을 수 있다. 운영 판단에는 현재 기준 문서를 우선한다.

## 5. 문서 중복 관리 원칙

- 루트 `README.md`는 전체 지도와 빠른 기준만 둔다.
- `docs/README.md`는 문서 목록과 우선순위만 둔다.
- 운영 명령은 `operation_runbook.md`를 기준으로 한다.
- Compose 세부 명령은 `docker_compose_usage.md`에 둔다.
- 채점 로직 설명은 `grading_architecture.md`에 둔다.
- Question Type 설명은 `question_type_taxonomy.md`에 둔다.
- Difficulty와 ceiling 설명은 `difficulty_and_selection_strategy.md`에 둔다.
- Rubric Bank 수정 절차는 `rubric_authoring_guide.md`에 둔다.

## 6. 문서 정합성 점검

```bash
cd ~/hermes/workspace/prof_eng_answer

# README가 참조하는 docs 파일 존재 여부 확인
grep -oE 'docs/[A-Za-z0-9_./-]+\\.md' README.md | sort -u | while read -r f; do
  [ -f "$f" ] || echo "MISSING: $f"
done

# Markdown fence 균형 확인
python3 - <<'PY'
from pathlib import Path
import re

bad = False
for p in [Path("README.md")] + sorted(Path("docs").glob("*.md")):
    s = p.read_text(encoding="utf-8")
    ticks = len(re.findall(r"^```", s, flags=re.MULTILINE))
    if ticks % 2:
        print(f"ERROR: unbalanced fences in {p}")
        bad = True

raise SystemExit(1 if bad else 0)
