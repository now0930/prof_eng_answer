# Scripts Directory Guide

이 문서는 `scripts/` 디렉터리의 역할과 파일 배치 기준을 설명한다.

`prof_eng_answer` 프로젝트에서 `scripts/`는 Rubric Bank 검증, 채점 Bot 운영, 감사 도구, 유지보수 도구를 담는 실행 스크립트 영역이다.

루트 `scripts/`에는 사람이 직접 실행하는 핵심 CLI와 검증 entrypoint만 둔다. 일회성 보정, 감사, import, migration, 실험 스크립트는 목적별 하위 디렉터리에 둔다.

---

## 1. Directory Policy

### Root `scripts/`

루트에는 다음 성격의 파일만 둔다.

- 운영 또는 검증을 위해 직접 실행하는 CLI
- `rubric_manager.py validate-all`에서 호출되는 검증 entrypoint
- 사람이 자주 직접 실행하는 조회/확인 도구
- 명확한 회귀 테스트 또는 체크 스크립트

루트에는 아래 성격의 파일을 새로 추가하지 않는다.

- 일회성 patch, apply, fix 스크립트
- 특정 날짜의 실험성 스크립트
- 외부 감사나 리포트 생성 전용 스크립트
- 데이터 import 또는 normalization 전용 스크립트
- 과거 migration 보관 파일

이런 파일은 목적에 따라 `maintenance/`, `migrations/`, `rubric_audit/`, `experiments/` 중 적절한 위치에 둔다.

---

## 2. Root Scripts

### `rubric_manager.py`

Rubric content 관리용 메인 CLI이다.

주요 용도는 다음과 같다.

- Rubric content 조회
- Rubric content CRUD
- 전체 검증 실행
- 내부 validator 라우팅

대표 실행 명령은 다음과 같다.

    python3 scripts/rubric_manager.py validate-all

---

### `run_prof_eng_bot.sh`

채점 Bot 실행용 shell wrapper이다.

주요 용도는 다음과 같다.

- 로컬 또는 서비스 환경에서 Bot 실행
- 환경 변수 및 실행 경로를 정리한 운영 entrypoint 제공

---

### `show_model_answer.py`

Model Answer Bank의 특정 모범 답안을 사람이 확인하기 위한 조회 도구이다.

주요 용도는 다음과 같다.

- topic별 모범 답안 확인
- question type별 답안 구조 확인
- 채점 기준, Fact Anchor, Model Answer 보정 전후 내용 점검

---

### `test_rubric_content_crud.py`

Rubric content CRUD 동작을 확인하는 회귀 테스트 스크립트이다.

현재는 사람이 직접 실행할 수 있는 스크립트로 루트에 둔다. 향후 테스트 체계가 커지면 `tests/`로 이동할 수 있다.

---

## 3. Validation Entrypoints

`validate_*.py` 파일은 Rubric Bank와 채점 설정을 직접 검증하는 entrypoint이다.

현재 루트에 유지하는 이유는 다음과 같다.

- 명령 경로가 단순하다.
- `rubric_manager.py validate-all`에서 호출하기 쉽다.
- 개별 validator를 독립적으로 실행할 수 있다.
- CI 또는 운영 점검 명령으로 쓰기 좋다.

현재 validation script는 다음과 같다.

- `validate_config.py`
- `validate_difficulty_strategy.py`
- `validate_fact_anchor_bank.py`
- `validate_logic_check_bank.py`
- `validate_logic_check_de_policy.py`
- `validate_model_answer_bank.py`
- `validate_model_answer_relationships.py`
- `validate_model_fact_consistency.py`
- `validate_question_type_profile.py`
- `validate_question_type_taxonomy_v2.py`
- `validate_rubric_bank_content.py`
- `validate_rubric_bank_format.py`

대표 실행 명령은 다음과 같다.

    python3 scripts/validate_rubric_bank_format.py
    python3 scripts/validate_rubric_bank_content.py
    python3 scripts/rubric_manager.py validate-all

---

## 4. Check Scripts

`check_*.py` 파일은 특정 회귀 조건이나 참조 무결성을 빠르게 확인하기 위한 스크립트이다.

### `check_fact_anchor_id_references.py`

Fact Anchor ID 참조 관계를 확인한다.

주요 용도는 다음과 같다.

- Model Answer, Fact Anchor, relationship 관련 ID 참조 오류 탐지
- 삭제되거나 이름이 바뀐 anchor 참조 검출
- Fact Anchor support term 정리 후 회귀 확인

---

### `check_logic_check_de_claim_trust_regression.py`

Logic Check의 D/E claim trust 정책 회귀를 확인한다.

주요 용도는 다음과 같다.

- Logic Check가 topic truth gate로 동작하는지 확인
- D/E 영역 감점 정책이 의도대로 유지되는지 확인
- second-order damping sign/stability 관련 회귀 방지

---

## 5. Subdirectories

### `rubric_content/`

Rubric content CRUD와 validator 라우팅의 내부 구현 모듈이다.

루트의 `rubric_manager.py`는 이 디렉터리의 기능을 호출하는 CLI entrypoint 역할을 한다.

일반 사용자는 보통 이 디렉터리의 모듈을 직접 실행하지 않는다.

---

### `validators/`

Rubric Bank validator의 내부 구현을 담는다.

예상되는 파일 성격은 다음과 같다.

- Rubric Bank format validator 구현
- Rubric Bank content validator 구현
- validator 공통 유틸리티

루트의 `validate_rubric_bank_format.py`, `validate_rubric_bank_content.py`는 이 내부 구현을 호출하는 얇은 entrypoint이다.

---

### `rubric_audit/`

Rubric Bank와 Model Answer Bank의 품질을 감사하거나 리포트를 생성하는 도구를 둔다.

예상되는 파일 성격은 다음과 같다.

- Fact Anchor 품질 감사
- Model Answer와 Fact Anchor 관계 감사
- priority minor issue 리포트
- Gemini 또는 외부 LLM 기반 감사 보조 도구
- rubric work pack 생성 도구

이 디렉터리의 스크립트는 일반 검증 루틴이라기보다 분석과 감사 목적의 도구이다.

---

### `maintenance/`

문서, 인코딩, import, normalization 등 유지보수용 스크립트를 둔다.

예상되는 파일 성격은 다음과 같다.

- docs index 점검
- visible mojibake 스캔
- exam trend keyword import
- review design import
- model answer outline normalization

운영 검증 루틴이 아닌 유지보수 작업은 이 디렉터리에 둔다.

---

### `migrations/`

과거 데이터 보정, 구조 전환, 일회성 patch/apply 스크립트를 보관한다.

예상되는 파일 성격은 다음과 같다.

- Fact Anchor 일괄 보정
- Model Answer relationship 보정
- 과거 구조에서 현재 구조로 넘어오기 위한 migration 스크립트

새로운 일회성 migration을 만들 때는 루트 `scripts/`에 두지 말고 이 디렉터리에 둔다.

---

### `experiments/`

특정 날짜나 목적의 실험성 스크립트와 산출물을 둔다.

예상되는 파일 성격은 다음과 같다.

- 특정 cleanup 실험
- 특정 validator 실험
- 폐기 가능성이 있는 검증 또는 보정 prototype

실험이 운영 흐름에 편입되면 `maintenance/`, `rubric_audit/`, `validators/` 등으로 이동한다.

---

## 6. Where to Put New Scripts

새 스크립트를 만들 때는 아래 기준을 따른다.

| Script type | Location |
|---|---|
| 전체 검증 entrypoint | `scripts/validate_*.py` |
| 특정 회귀 체크 | `scripts/check_*.py` |
| 사람이 자주 쓰는 조회 CLI | `scripts/` |
| Rubric content 내부 구현 | `scripts/rubric_content/` |
| Validator 내부 구현 | `scripts/validators/` |
| 감사 또는 리포트 생성 | `scripts/rubric_audit/` |
| 문서, 인코딩, import, 정규화 | `scripts/maintenance/` |
| 일회성 apply, patch, migration | `scripts/migrations/` |
| 실험성 작업 | `scripts/experiments/` |

---

## 7. Validation Before Commit

`scripts/`를 수정한 뒤에는 최소한 아래 검증을 수행한다.

    python3 scripts/rubric_manager.py validate-all
    git ls-files '*.py' | xargs python3 -m py_compile
    git diff --check

루트 `scripts/` 구성을 확인하려면 다음 명령을 사용한다.

    git ls-files 'scripts/*.py' | sort

원격 `main` 기준의 루트 스크립트 구성을 확인하려면 다음 명령을 사용한다.

    git fetch origin
    git ls-tree -r --name-only origin/main | grep '^scripts/[^/]*\.py$' | sort

---

## 8. Current Root Script Intent

현재 루트 `scripts/`는 다음 원칙을 따른다.

- `rubric_manager.py`는 통합 CLI이다.
- `validate_*.py`는 독립 실행 가능한 검증 entrypoint이다.
- `check_*.py`는 특정 회귀 또는 참조 무결성 확인 도구이다.
- `show_model_answer.py`는 사람이 직접 확인하는 조회 도구이다.
- `test_rubric_content_crud.py`는 Rubric content CRUD 회귀 테스트이다.
- 일회성 보정, 감사, import, migration 스크립트는 루트에 두지 않는다.

이 기준을 유지하면 `scripts/` 루트는 검증과 운영 중심으로 유지되고, 보조 도구는 목적별 하위 디렉터리에서 관리된다.
