# AI·개발자용 구현 참조

**대상:** `now0930/prof_eng_answer`, `codex/data-reports-inventory-20261113` 브랜치(2026-11-13 조사).
이 문서는 AI/Codex가 코드를 읽고 문서를 동기화하기 위한 **탐색 지도**이며 정책 변경 권한은 없습니다.
사람용 안내는 [README](../README.md), 개념 구조는 [시스템 구조](system_architecture.md), 자료 보관은 [인벤토리](data_reports_inventory.md)를 읽습니다.
작업 전 [AGENTS.md](../AGENTS.md)를 먼저 읽고 **실제 branch HEAD**와 환경 설정을 확인합니다.

## 1. 코드 진입점

| 기능 | 코드 또는 정본 | 확인 사항 |
| --- | --- | --- |
| Telegram 명령·세션 | [`bot.py`](../bot.py) | `/grade` 뒤 종료 표식 `끝.`, `/review` 수동 Topic 선택 |
| 채점 처리 | [`grading_agents.py`](../grading_agents.py) | 채점 경로·확정 결과; 현재 배포 환경 값을 추정하지 않음 |
| bank 경로 선택 | [`grading/rubrics/rubric_bank_paths.py`](../grading/rubrics/rubric_bank_paths.py) | `RUBRIC_BANK_MODE` 기본 `generated` |
| Topic 원본 | `rubrics/topic_packs/<topic_id>/` | Fact, Model, Logic, Importance와 일부 Topic의 demand 계약 |
| 생성 bank | `rubrics/generated/` | 채점 JSON 5개 + manifest 1개, 직접 편집 금지 |
| Master/View | [`study/master_topic_pack.py`](../study/master_topic_pack.py), [`study/topic_views.py`](../study/topic_views.py) | Grading View는 호환 projection이며 운영 Grader가 직접 소비하지 않음 |
| 학습·이력 | [`study/learning_runtime.py`](../study/learning_runtime.py), [`study/training_history.py`](../study/training_history.py) | 점수 확정 후 이력 별도 저장 |
| WordPress OCR | [`scripts/wordpress_catalog.py`](../scripts/wordpress_catalog.py), [`scripts/build_wordpress_topic_packs.py`](../scripts/build_wordpress_topic_packs.py) | 비공개, 승인된 출처 연결을 거쳐 학습만 |
| 배포용 회귀 | [`scripts/release_candidate.py`](../scripts/release_candidate.py) | 전체 오프라인 pytest, 승인된 정확한 격리만 허용 |
| 비공개 백업 | [`scripts/backup_private_runtime.py`](../scripts/backup_private_runtime.py) | SQLite online backup / 일반 파일 best-effort |

## 2. 채점과 학습의 실제 경로

```text
/grade → 문제/답안 수집 → "끝." → bot.py → grading_agents.py
                                            ↓
                   data/sessions/<sid>/grade.json (최종)
                                            ↓
             study.learning_runtime.record_completed_grade()
                ├─ data/training_history.sqlite3 (요약·복습)
                └─ data/sessions/<sid>/learning_history.json (저장 상태)

/review <topic_id 또는 이름> → Training/Feedback View + 이전 진단
/review done <topic_id> → 복습 상태 저장 (재채점 없음)
```

- `bot.py`는 `PROF_ENG_BASE_DIR`가 없으면 기본 `/workspace/prof_eng_answer`에 파일을 씁니다. 로컬 실행에서는 명시적으로 설정하세요.
- `.env.example`의 `DETERMINISTIC_GRADING_PRIMARY=false`는 **예시 기본값**입니다. `grading_agents.py`는 `enforce_requested_authority_mode()` 결과에 따라 deterministic primary 진입 여부를 결정합니다. 항상 결정론적 primary라고 설명하면 안 됩니다.
- 배점은 `rubrics/scoring_model/default.json`의 A/B/C/D/E **3/6/8/6/2**입니다. `QUALITATIVE_DE_MODE=argon`은 선택형 D/E 보조 계약입니다. [채점 권한](../GRADING_DIRECTION_CONTRACT.md).
- 확정 `grade.json`과 개인 원본 답안은 세션에 보존합니다. `TrainingHistoryStore`에는 학습자·문항·Topic·시각·최종 점수·요약 진단·복습 상태 등이 저장되며 **원본 답안 전문이나 grade.json 전체가 복제되지 않습니다.**
- `record_completed_grade`는 확정 점수 이후에 실행됩니다. 저장 실패는 이미 확정된 채점을 변경하지 않습니다. 날짜 큐 함수를 가진다는 이유로 Telegram `/review`가 일일 자동 큐를 사용한다고 말하지 마세요.
- 근거 테스트: [이력 기록](../tests/test_bot_learning_history_log.py), [복습·이력](../tests/test_training_history_and_review_queue.py).

## 3. Topic Pack, 출처, 승인

```text
rubrics/topic_packs/<topic_id> → 공식 builder → rubrics/generated/ → Grader

WordPress 글·첨부 → 비공개 카탈로그/OCR → 승인된 Topic·Master source
   → data/wordpress_topic_packs/<topic_id>.json → Training View → /review
   (자동 채점 사실 승격 금지)
```

- 검토 시점 [generated manifest](../rubrics/generated/topic_pack_manifest.generated.json)의 `topic_count=89`입니다. 이 수치는 기출문항 개수·Fact 적격성 전체 승인 수가 아닙니다.
- `study/topic_views.py`의 세 진입점: `grading_view`, `training_view`, `feedback_view`. Grading View는 현재 운영 점수 산출 경로가 아닌 **호환 projection**입니다.
- Master 정본과 스키마: `master_topic_packs/`, [`schemas/master_topic_pack.schema.json`](../schemas/master_topic_pack.schema.json).
- 생성 bank 바이트 일치 검사는 [`scripts/check_generated_rubrics_freshness.py`](../scripts/check_generated_rubrics_freshness.py). 격리된 재생성 결과와 6개 파일 비교.
- Source 변경은 [Topic Pack 절차](topic_pack_workflow.md)와 [Fact 적격성 정책](fact_anchor_eligibility_policy.md) 적용. AI reviewer 위임과 증거 요구는 [AGENTS.md](../AGENTS.md)를 우선합니다.
- WordPress source reference 승인과 **개별 기술 사실의 채점 승인**은 다른 단계입니다. 상세 [WordPress/View 계약](wordpress_topic_pack_view_contract.md).

### WordPress URL 반복 처리의 방향·코드 확인

- 사람용 원칙: [WordPress URL → Topic Pack 지속 운영 정책](wordpress_url_continuous_workflow.md).
- AI 실행 계약: [URL별 단계, 명령, 차단 조건·방향 이탈 감시](wordpress_url_continuous_ai_runbook.md).
- **현재 단일 URL → 전 단계 자동 실행 CLI는 미구현**. 카테고리 동기화와 post ID 기반 후보 검색, source/content 별도 승인으로 나누어 수행합니다.
- WordPress link 승인 ≠ Master source reference 승인 ≠ 채점 Fact 승인. source reference를 승인해도 generated grading bank는 바뀌지 않습니다.
- 같은 URL을 재처리할 때는 기존 post/source hash와 검토 이력을 먼저 확인합니다.

## 4. 저장 영역과 공개 경계

| 경로 | 책임 |
| --- | --- |
| `rubrics/topic_packs/`, `rubrics/generated/`, `master_topic_packs/` | 공개 원본/생성물/참조 |
| `data/question_contract_cache/` | Git에 추적된 공개 문제 계약 캐시 |
| `data/sessions/`, `data/training_history.sqlite3`, `data/final_grade_cache/` | 비공개 개인 기록·확정 결과 |
| `data/wordpress_topic_packs/`, WordPress SQLite·OCR | 비공개 학습·출처 자료 |
| `reports/` | 공개 감사와 비추적 실행 산출물 혼합 |
| `logs/`, 실제 `.env` | 비공개 운영 설정·로그 |

[인벤토리](data_reports_inventory.md)에 나오는 2026-11-13 파일 수는 당시 `main`/서버의 시점 자료입니다. 새 커밋의 실시간 수치가 아니므로 현재 `git ls-files`, 파일 상태, manifest를 다시 확인하기 전에는 최신으로 인용하지 않습니다.

### 백업 및 공개 경계

- `scripts/backup_private_runtime.py` 기본: `~/hermes/workspace/prof_eng_answer` → `~/hermes/private_backups/prof_eng_answer/`.
- 백업 포함: 존재하는 `data/`, `logs/`, `reports/`, `wordpress_docs/`, 일부 `.env`/Compose, 검색된 SQLite DB.
- SQLite는 `Connection.backup()` + 백업본 `PRAGMA quick_check`. 일반 세션·로그 파일은 실시간 **best-effort copy**이며 원자적 snapshot이 아닙니다.
- WordPress/Immich 등 외부 DB, Docker `/opt/data`, `gemini_script/`·`tmp/` 전체는 이 스크립트의 보장 범위 밖입니다.
- `manifest.status=OK`는 필수 확인 항목이나, 복원 검증 자체를 대신하지 않습니다. 미완전 과거 백업·단순 파일 수 일치는 증명이 아닙니다.
- 테스트 [백업 회귀](../tests/test_backup_private_runtime.py), 절차 [백업·복원](private_runtime_backup.md).
- 개인 답안, 데이터베이스, .env, 로그, 실제 백업 파일 목록·행 내용을 공개 커밋·이슈·문서로 보내지 않습니다.

## 5. AI/Codex 문서 수정 절차

1. `AGENTS.md`, 목표 정책 문서, 실제 파일/함수/테스트, branch HEAD를 읽습니다.
2. **구현·설정·검증된 사실**과 **계획·과거 감사·미구현 요구**를 분리합니다. 의심스러우면 구현 완료라고 단정하지 않습니다.
3. 사람용 README/인덱스는 **목적 → 사용하는 법 → 주의사항 → 상세 문서 링크**로 간결하게 작성합니다. 필드·예외·API는 본 참조 또는 기존 상세 계약으로 연결합니다.
4. 문서 작업에서는 코드, source JSON, generated bank, 사용자 기록을 변경하지 않습니다. Markdown 링크와 기존 실제 경로를 확인합니다.
5. 배포용 코드 검증은 [`scripts/release_candidate.py`](../scripts/release_candidate.py)의 **전체 offline pytest**입니다. 실패·제외·통과 개수를 실제 실행에서만 보고합니다. 유료 정확도/Qualification은 선택 진단이며 필수로 요구하지 않습니다.
6. 폐지된 전용 **동일 입력 10회 채점 검사**를 새 릴리스·CI·문서 필수 항목으로 복원하지 않습니다.
7. GitHub 문서 커밋, 운영 서버 checkout 갱신, 봇 프로세스 재시작은 **각각 별도 단계**입니다. 배포되지 않은 것을 배포 완료라고 쓰지 않습니다.

**참조 우선순위:** 현재 코드·실행 설정·원본 JSON → 생성 bank·회귀 → 현행 정책 문서 → 과거 보고서·archive.

## 6. 전체 문서 인벤토리와 유지 규칙

[사람·AI 문서 분리 정책과 전체 Markdown 분류(2026-11-13 당시 기준, 이후 지침 2개 추가)](document_governance.md)를 참조합니다. 현재 지침 62개, 2027~2030 출제범위 문서 5개, 보존해야 할 역사 기록·Topic Sheet·canonical Topic README를 구분합니다. 새 문서는 사람용 핵심과 기술 참조를 서로 연결하되 내용 승인·source hash는 건드리지 않습니다.
