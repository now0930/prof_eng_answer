# Documentation Update Notes

이 패키지는 `now0930/prof_eng_answer`의 Markdown 문서를 현재 코드 기준으로 정리한 교체본이다.

## 포함 파일

```text
README.md
docs/README.md
docs/grading_architecture.md
docs/operation_runbook.md
docs/docker_compose_usage.md
docs/difficulty_and_selection_strategy.md
docs/llm_provider.md
docs/question_type_taxonomy.md
docs/rubric_authoring_guide.md
scripts/rubric_audit/README.md
```

## 정리 기준

- 루트 `README.md`: 전체 지도와 빠른 기준만 유지
- `docs/README.md`: 문서 우선순위와 인덱스
- `operation_runbook.md`: 운영 점검·재시작·장애 대응
- `docker_compose_usage.md`: Compose 명령만 분리
- `grading_architecture.md`: 채점 pipeline과 A/B/C/D/E 구조
- `question_type_taxonomy.md`: Question Type v2만 설명
- `difficulty_and_selection_strategy.md`: Difficulty, ceiling, 선택 전략만 설명
- `llm_provider.md`: provider 구조와 `/provider` 명령만 설명
- `rubric_authoring_guide.md`: JSON Bank 수정·검증 절차
- `scripts/rubric_audit/README.md`: audit 도구 설명

## 적용 방법

Repository root에서 압축을 풀면 같은 경로로 덮어쓸 수 있다.

```bash
cd ~/hermes/workspace/prof_eng_answer
unzip /path/to/prof_eng_answer_docs_update.zip -d /tmp/prof_eng_answer_docs_update
cp -r /tmp/prof_eng_answer_docs_update/* .
```

적용 후 검증:

```bash
python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_audit/run_rubric_audit.py
git diff --check
git status --short
```
