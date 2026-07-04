# Scripts Directory Guide

이 문서는 `scripts/` 디렉터리의 역할과 파일 배치 기준을 설명한다.

`prof_eng_answer` 프로젝트에서 `scripts/`는 Rubric Bank 검증, Topic Pack authoring, 채점 Bot 운영, 감사 도구, 유지보수 도구를 담는 실행 스크립트 영역이다.

루트 `scripts/`에는 사람이 직접 실행하는 핵심 CLI와 검증 entrypoint만 둔다. 일회성 보정, 실험성 스크립트, 과거 migration 파일은 목적별 하위 디렉터리에 둔다.

---

## 1. Directory Policy

### 1.1 Root `scripts/`

루트에는 다음 성격의 파일만 둔다.

- 운영 또는 검증을 위해 직접 실행하는 CLI
- `rubric_manager.py`에서 호출되는 topic pack / generated bank entrypoint
- `rubric_manager.py validate-all`에서 호출되는 검증 entrypoint
- 사람이 자주 직접 실행하는 조회/확인 도구
- 명확한 회귀 테스트 또는 check script

루트에는 아래 성격의 파일을 새로 추가하지 않는다.

- 일회성 patch, apply, fix 스크립트
- 특정 날짜의 실험성 스크립트
- 데이터 import 또는 normalization 전용 스크립트
- 과거 migration 보관 파일
- 폐기 가능한 prototype

이런 파일은 목적에 따라 `maintenance/`, `migrations/`, `rubric_audit/`, `experiments/` 중 적절한 위치에 둔다.

---

## 2. Root Scripts

### `rubric_manager.py`

Rubric content와 Topic Pack을 관리하는 통합 CLI이다.

주요 용도:

- Rubric content 조회
- Topic Pack 생성, 검증, 리뷰, 상태 확인
- generated bank build/validation
- release 검증
- 내부 validator routing

대표 명령:

```bash
python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_manager.py validate-generated-pipeline
python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated
python3 scripts/rubric_manager.py topic-pack-status --all --include-frozen
```

---

### `generate_topic_sheet_from_readme.py`

Topic Pack README를 읽어 사람이 검토할 수 있는 Topic Sheet 후보를 생성하는 authoring 도구이다.

역할:

- `rubrics/topic_packs/<topic_id>/README.md`를 읽는다.
- 기존 topic source JSON을 참고 context로 읽는다.
- Markdown Topic Sheet 후보를 생성한다.
- JSON source는 직접 만들지 않는다.

입력:

```text
rubrics/topic_packs/<topic_id>/README.md
```

출력:

```text
docs/topic_sheets/<topic_id>.md
```

대표 명령:

```bash
python3 scripts/generate_topic_sheet_from_readme.py \
  --topic-id second_order_lag_response_by_damping_ratio \
  --model gemini-2.5-flash \
  --overwrite
```

이 스크립트의 결과물은 반드시 사람이 검토한 뒤 다음 단계로 넘긴다.

---

### `generate_topic_pack_from_sheet.py`

사람이 검토한 Topic Sheet를 바탕으로 topic pack source JSON 후보를 생성하는 authoring 도구이다.

역할:

- Topic Sheet를 읽는다.
- 기존 `fact_anchor.json`, `logic_check.json`, `model_answer.json`, `topic_importance.json`을 schema-lock template으로 사용한다.
- LLM이 schema를 바꾸지 못하도록 prompt와 post-process merge를 적용한다.
- `logic_check.json`에는 필수 fatal rule을 누락하지 않도록 보강한다.
- generated runtime file을 직접 만들지 않는다.

입력:

```text
docs/topic_sheets/<topic_id>.md
```

출력:

```text
rubrics/topic_packs/<topic_id>/fact_anchor.candidate.json
rubrics/topic_packs/<topic_id>/logic_check.candidate.json
rubrics/topic_packs/<topic_id>/model_answer.candidate.json
rubrics/topic_packs/<topic_id>/topic_importance.candidate.json
reports/topic_pack_generation_<topic_id>_<timestamp>_*.json
```

`--overwrite`를 쓰면 `.candidate.json` 대신 source JSON을 직접 갱신한다.

대표 명령:

```bash
python3 scripts/generate_topic_pack_from_sheet.py \
  --topic-id second_order_lag_response_by_damping_ratio \
  --sheet docs/topic_sheets/second_order_lag_response_by_damping_ratio.md \
  --model gemini-2.5-flash
```

---

### `build_generated_rubrics.py`

`rubrics/topic_packs/` source를 읽어 `rubrics/generated/*.generated.json`을 생성한다.

직접 실행할 수 있지만, 일반적으로는 아래 명령을 사용한다.

```bash
python3 scripts/rubric_manager.py validate-generated-pipeline
python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated
```

---

### `validate_generated_rubrics.py`

generated bank의 형식과 기본 참조 무결성을 검증한다.

일반적으로 `validate-generated-pipeline` 또는 `validate-topic-pack-release`에서 호출된다.

---

### `create_topic_pack.py`

새 topic pack source 디렉터리를 생성하는 도구이다.

일반적으로 직접 실행하기보다 `rubric_manager.py`를 통해 실행한다.

```bash
python3 scripts/rubric_manager.py create-topic-pack --topic-id <topic_id>
```

---

### `smoke_topic_pack.py`

특정 topic pack이 model answer routing과 topic matching에서 충분히 구분되는지 smoke test한다.

```bash
python3 scripts/rubric_manager.py smoke-topic-pack --topic-id <topic_id>
```

---

### `smoke_compare_rubric_bank_modes.py`

legacy bank와 generated bank의 채점 결과를 비교한다.

주요 용도:

- generated bank 전환 회귀 확인
- topic pack release 전 legacy/generated 차이 확인
- Logic Check fatal cap이 generated mode에서 적용되는지 확인

---

### `review_topic_pack.py`, `review_topic_pack_all.py`

Topic Pack source와 generated output을 검토하기 위한 review 도구이다.

```bash
python3 scripts/rubric_manager.py review-topic-pack --topic-id <topic_id>
python3 scripts/rubric_manager.py review-topic-pack-all --changed-only
```

---

### `topic_pack_status.py`

Topic Pack별 상태, hash, frozen/changed 여부를 확인한다.

```bash
python3 scripts/rubric_manager.py topic-pack-status --all --include-frozen
```

---

### `topic_review_llm.py`

Topic Pack authoring/review 도구가 공통으로 사용하는 LLM helper이다.

주요 역할:

- Gemini 호출
- LLM 응답 정규화
- JSON 추출 helper 제공
- authoring script의 provider 호출 공통화

일반 사용자가 직접 실행하는 entrypoint는 아니다.

---

### `run_prof_eng_bot.sh`

채점 Bot 실행용 shell wrapper이다.

주요 용도:

- 로컬 또는 서비스 환경에서 Bot 실행
- 환경 변수 및 실행 경로 정리
- Docker Compose entrypoint 역할

---

### `show_model_answer.py`

Model Answer Bank의 특정 모범 답안을 사람이 확인하기 위한 조회 도구이다.

주요 용도:

- topic별 모범 답안 확인
- question type별 답안 구조 확인
- Fact Anchor / Model Answer 보정 전후 내용 점검

---

## 3. Validation Entrypoints

`validate_*.py` 파일은 Rubric Bank와 채점 설정을 직접 검증하는 entrypoint이다.

루트에 유지하는 이유:

- 명령 경로가 단순하다.
- `rubric_manager.py validate-all`에서 호출하기 쉽다.
- 개별 validator를 독립 실행할 수 있다.
- CI 또는 운영 점검 명령으로 쓰기 좋다.

대표 validation script:

- `validate_config.py`
- `validate_difficulty_strategy.py`
- `validate_fact_anchor_bank.py`
- `validate_generated_rubrics.py`
- `validate_logic_check_bank.py`
- `validate_logic_check_de_policy.py`
- `validate_model_answer_bank.py`
- `validate_model_answer_relationships.py`
- `validate_model_fact_consistency.py`
- `validate_question_type_profile.py`
- `validate_question_type_taxonomy_v2.py`
- `validate_rubric_bank_content.py`
- `validate_rubric_bank_format.py`
- `validate_topic_pack_quality.py`
- `validate_topic_pack_release.py`
- `validate_topic_packs.py`

대표 실행 명령:

```bash
python3 scripts/validate_rubric_bank_format.py
python3 scripts/validate_rubric_bank_content.py
python3 scripts/rubric_manager.py validate-all
python3 scripts/rubric_manager.py validate-topic-pack-release
```

---

## 4. Check Scripts

`check_*.py` 파일은 특정 회귀 조건이나 참조 무결성을 빠르게 확인하기 위한 스크립트이다.

### `check_fact_anchor_id_references.py`

Fact Anchor ID 참조 관계를 확인한다.

주요 용도:

- Model Answer, Fact Anchor, relationship 관련 ID 참조 오류 탐지
- 삭제되거나 이름이 바뀐 anchor 참조 검출
- Fact Anchor support term 정리 후 회귀 확인

---

### `check_logic_check_de_claim_trust_regression.py`

Logic Check의 D/E claim trust 정책 회귀를 확인한다.

주요 용도:

- Logic Check가 topic truth gate로 동작하는지 확인
- D/E 영역 감점 정책이 의도대로 유지되는지 확인
- second-order damping sign/stability 관련 회귀 방지

---

### `check_rubric_bank_paths.py`

현재 runtime이 legacy bank와 generated bank 중 어느 경로를 사용하는지 확인한다.

```bash
python3 scripts/check_rubric_bank_paths.py
RUBRIC_BANK_MODE=generated python3 scripts/check_rubric_bank_paths.py
RUBRIC_BANK_MODE=legacy python3 scripts/check_rubric_bank_paths.py
```

---

## 5. Topic Pack Authoring Flow

새 topic을 추가할 때는 아래 순서를 따른다.

```text
README.md
  → Topic Sheet 후보
  → 사람이 Topic Sheet 검토
  → schema-locked JSON candidate
  → generated bank promote
  → smoke / Telegram 재채점 확인
```

명령 예시:

```bash
# topic pack source 생성
python3 scripts/rubric_manager.py create-topic-pack --topic-id <topic_id>

# README 작성
vim rubrics/topic_packs/<topic_id>/README.md

# README → Topic Sheet 후보 생성
python3 scripts/generate_topic_sheet_from_readme.py \
  --topic-id <topic_id> \
  --model gemini-2.5-flash \
  --overwrite

# 사람이 Topic Sheet 검토
vim docs/topic_sheets/<topic_id>.md

# Topic Sheet → JSON candidate 생성
python3 scripts/generate_topic_pack_from_sheet.py \
  --topic-id <topic_id> \
  --sheet docs/topic_sheets/<topic_id>.md \
  --model gemini-2.5-flash

# release 검증 및 generated promote
python3 scripts/rubric_manager.py validate-topic-pack-release --promote-generated

# smoke
python3 scripts/rubric_manager.py smoke-topic-pack --topic-id <topic_id>
```

주의:

- README에서 JSON으로 직행하지 않는다.
- Topic Sheet는 사람이 검토한다.
- generated bank는 직접 수정하지 않는다.
- source JSON 수정 후 `validate-topic-pack-release --promote-generated`로 generated를 갱신한다.

---

## 6. Subdirectories

### `rubric_content/`

Rubric content CRUD와 validator routing의 내부 구현 모듈이다.

루트의 `rubric_manager.py`는 이 디렉터리 기능을 호출하는 CLI entrypoint 역할을 한다.

---

### `validators/`

Rubric Bank validator의 내부 구현을 담는다.

예상 파일 성격:

- Rubric Bank format validator 구현
- Rubric Bank content validator 구현
- validator 공통 유틸리티

루트의 `validate_rubric_bank_format.py`, `validate_rubric_bank_content.py`는 이 내부 구현을 호출하는 얇은 entrypoint이다.

---

### `rubric_audit/`

Rubric Bank와 Model Answer Bank의 품질을 감사하거나 리포트를 생성하는 도구를 둔다.

예상 파일 성격:

- Fact Anchor 품질 감사
- Model Answer와 Fact Anchor 관계 감사
- priority minor issue 리포트
- Gemini 또는 외부 LLM 기반 감사 보조 도구
- rubric work pack 생성 도구

---

### `maintenance/`

문서, 인코딩, import, normalization 등 유지보수용 스크립트를 둔다.

예상 파일 성격:

- docs index 점검
- visible mojibake 스캔
- exam trend keyword import
- review design import
- model answer outline normalization

---

### `migrations/`

과거 데이터 보정, 구조 전환, 일회성 patch/apply 스크립트를 보관한다.

새로운 일회성 migration을 만들 때는 루트 `scripts/`에 두지 않는다.

---

### `experiments/`

특정 날짜나 목적의 실험성 스크립트와 산출물을 둔다.

실험이 운영 흐름에 편입되면 `maintenance/`, `rubric_audit/`, `validators/` 등으로 이동한다.

---

## 7. Where to Put New Scripts

| Script type | Location |
|---|---|
| 통합 CLI | `scripts/rubric_manager.py` |
| 전체 검증 entrypoint | `scripts/validate_*.py` |
| 특정 회귀 체크 | `scripts/check_*.py` |
| 사람이 자주 쓰는 조회 CLI | `scripts/` |
| Topic Pack authoring entrypoint | `scripts/` |
| Rubric content 내부 구현 | `scripts/rubric_content/` |
| Validator 내부 구현 | `scripts/validators/` |
| 감사 또는 리포트 생성 | `scripts/rubric_audit/` |
| 문서, 인코딩, import, 정규화 | `scripts/maintenance/` |
| 일회성 apply, patch, migration | `scripts/migrations/` |
| 실험성 작업 | `scripts/experiments/` |

---

## 8. Validation Before Commit

`scripts/`를 수정한 뒤에는 최소한 아래 검증을 수행한다.

```bash
python3 scripts/rubric_manager.py validate-all
git ls-files '*.py' | xargs python3 -m py_compile
git diff --check
```

Topic Pack authoring script를 수정했을 때:

```bash
python3 -m py_compile \
  scripts/generate_topic_sheet_from_readme.py \
  scripts/generate_topic_pack_from_sheet.py \
  scripts/rubric_manager.py \
  scripts/topic_review_llm.py

python3 scripts/generate_topic_sheet_from_readme.py \
  --topic-id second_order_lag_response_by_damping_ratio \
  --dry-run

python3 scripts/generate_topic_pack_from_sheet.py \
  --topic-id second_order_lag_response_by_damping_ratio \
  --sheet docs/topic_sheets/second_order_lag_response_by_damping_ratio.md \
  --dry-run
```

루트 `scripts/` 구성을 확인하려면 다음 명령을 사용한다.

```bash
git ls-files 'scripts/*.py' | sort
```

---

## 9. Current Root Script Intent

현재 루트 `scripts/`는 다음 원칙을 따른다.

- `rubric_manager.py`는 통합 CLI이다.
- `generate_topic_sheet_from_readme.py`는 README를 Topic Sheet 후보로 바꾸는 authoring CLI이다.
- `generate_topic_pack_from_sheet.py`는 Topic Sheet를 schema-locked JSON candidate로 바꾸는 authoring CLI이다.
- `build_generated_rubrics.py`, `validate_generated_rubrics.py`는 generated bank pipeline entrypoint이다.
- `validate_*.py`는 독립 실행 가능한 검증 entrypoint이다.
- `check_*.py`는 특정 회귀 또는 참조 무결성 확인 도구이다.
- `show_model_answer.py`는 사람이 직접 확인하는 조회 도구이다.
- 일회성 보정, 감사, import, migration 스크립트는 루트에 두지 않는다.
