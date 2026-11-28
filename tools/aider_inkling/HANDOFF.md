# Aider–Inkling V6 업무 인수인계서

기준일 2026-11-28 · 설치 서버 245k · 실행 코드 기준 `8078279`

## 작업 위치와 구조

- GitHub의 `now0930/prof_eng_answer` 저장소에서 플랫폼은 `develop/aider-inkling` 브랜치의 `tools/aider_inkling/`에 있습니다.
- 서버 설치 경로는 `~/aider_inkling`입니다. 그 아래 `repo/`는 V6가 실제로 수정하는 채점 작업 폴더입니다. 설치 파일을 업데이트할 때 이 작업 폴더의 기존 변경을 보존합니다.
- `develop.sh`가 `develop.py`를 실행합니다. `planner.py`가 Gemini 또는 기존 Copilot 경로로 계획을 준비하고, `compiler.py`가 대상·심볼·정확한 변경을 검사합니다. 승인 후 `executor.py`가 Aider + 로컬 Inkling을 호출하고, `validator.py`가 변경 범위·결과 일치, 동일 답안 재채점, 전체 pytest를 확인합니다.
- 로컬 Ollama는 포트 11434, Inkling 프록시는 11435를 사용합니다. 검증기는 `~/hermes/validation/.venv-xdist/bin/python`을 사용합니다. 플랫폼은 로컬 채점 변경을 자동 커밋하거나 푸시하지 않습니다.

## 운영과 검증

1. 245k에서 `cd ~/aider_inkling` 후 `bash test_workflow.sh`와 `python3 -B -m unittest discover -s . -p test_ai_backends.py`를 실행합니다. 두 검사는 외부 API 호출 없이 실행됩니다.
2. Gemini 계획 생성에는 서버 셸의 `GEMINI_API_KEY`와 `V6_PLAN_PROVIDER=gemini`가 필요합니다. 무료 등급 테스트에는 무료 프로젝트에서 `V6_GEMINI_MODEL=gemini-3.1-flash-lite`를 지정합니다. `V6_EXTERNAL_PLAN_CONTEXT`는 외부로 보낼 승인된 추적 파일의 JSON 배열입니다. 첫 실호출은 개인 자료가 없는 합성 입력으로 확인합니다. 이전에 노출된 키의 폐기 여부는 확인되지 않았습니다.
3. `./develop.sh "개발 요청" --compile-only`로 계획을 생성합니다. 출력에 `V6 exact-edit preflight PASS`가 나오면 표시된 실행 폴더의 `plan.json`을 검토합니다. 파일, 심볼, 검색·교체 내용, 검증 대상을 확인합니다.
4. `./develop.sh --plan /경로/plan.json`을 실행하고 내용을 확인한 뒤 승인합니다. 저장 계획을 사용하면 계획 API가 다시 호출되지 않습니다. 실행 전 `git -C ~/aider_inkling/repo status --short`로 기존 작업을 확인하고, 검증용 편집은 가능하면 자체 Git 객체를 가진 독립 복제본에서 실행합니다.
5. 변경 범위 검사, 동일 답안 재채점, pytest 결과를 확인합니다. 산출물은 로컬 `runs/`와 `test_answers/runs/`, Aider 이력은 `aider_home/`에 남습니다. API 키, 개인 답안, 상세 로그와 모델 가중치는 저장소에 올리지 않습니다.

격리 실행 시 플랫폼 파일과 `repo/`를 같은 시험 디렉터리에 두고, 승인된 기준 답안을 그 디렉터리의 `test_answers/feedback_control.txt`에 복사합니다. `validate_answer.sh`는 스크립트가 있는 디렉터리에서 `repo/`를 찾습니다.

## 장애 대응과 남은 범위

- **Docker 안에서 Git 객체를 읽지 못할 때** 공유 객체를 참조하는 `git clone --shared` 대신 `git clone --no-local`로 자체 객체가 있는 검증용 복제본을 만듭니다.
- **범위 검사 실패** 실행 폴더의 변경 기록과 현재 작업 트리의 차이를 검토합니다. 기존 사용자 수정과 실행 중 변경을 구분한 뒤 재시도합니다.
- **복구** GitHub의 실행 코드 기준은 `8078279`입니다. 245k에서는 이 커밋의 플랫폼 파일만 복원하고, 실행 잠금과 기존 채점 작업 상태를 확인합니다.
- **검증 범위** `e25e42e`의 격리 복제본에서 신규 Gemini 계획 생성부터 V6 컴파일, Aider + 로컬 Inkling 편집, 동일 답안 재채점, 전체 오프라인 pytest까지 통과했습니다. 재채점은 **5.0 → 5.0/25**, 외부 채점 호출은 전후 각각 **0회**, pytest는 **1,718 passed, 2 skipped**였습니다. 실제 개발 요청 5~10건과 채점 품질·데이터 호환성 검증은 후속 항목입니다. OpenAI 전용 연결은 보류입니다.

[설치 안내](README.md) · [작업 기록](WORK_LOG.md) · [검증 기록](VALIDATION.md)
