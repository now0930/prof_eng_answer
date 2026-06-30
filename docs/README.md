# Documentation Index

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
