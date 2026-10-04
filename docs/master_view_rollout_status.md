# Master / View 작업 상태와 운영 반영 조건

기준일: 2026-10-04. 작업 브랜치: `codex/study-structure-learning-layer`.

| 단계 | 결과 | 확인 방법 |
| --- | --- | --- |
| 시작 전 GitHub push | 완료 | 작업 브랜치 push: 최신 상태 |
| 비공개 자료 별도 백업 | 완료 | SQLite `PRAGMA integrity_check=ok`, OCR JSON 48개와 별도 백업 대조 |
| Master / 세 View 구조 | 완료 | `study/topic_views.py`, `tests/test_topic_views.py` |
| 학습 이력 / 2문제 Queue | 완료 | `study/training_history.py`, `study/review_queue.py` |
| 실제 WordPress HTML → Master → View | 완료 | `tests/test_master_view_private_end_to_end.py` |
| 확정 점수 → 이력 → Queue → `/review done` | 로컬 검증 완료 | 위 비공개 자료 연동 테스트; 임시 SQLite만 사용 |
| 운영 배포 | 미실행 | 아래 운영 경로·release gate 조건 확인 필요 |
| 실제 Telegram 화면 | 미확인 | 운영 배포 및 endpoint 확인 뒤 실행 |

별도 백업 위치는
`/home/now0930/chatgpt_project/private_backups/2026-10-04_master_view_before_rollout`이다.
Git에서는 제외된다. 백업 대상은 WordPress SQLite catalog, OCR Topic JSON,
수동 검토 CSV, 기존 로컬 DB 백업, 생성된 rubric 보고서다. SQLite는 `.backup`
명령으로 일관된 사본을 만들었고, 소스 JSON·CSV·기존 백업은 대조했다.
Python 캐시 같은 재생성 가능한 파일은 포함하지 않았다.

## 운영 환경에서 확인된 차이

- 운영 컨테이너 `prof_eng_answer_bot`은
  `/home/now0930/hermes/workspace`를 bind mount한다. 로컬 작업 디렉터리와
  다르다. 운영 체크아웃의 현재 commit은 `1f541e7` (`main`), 이번 작업의
  기준 commit은 `ac32a1e` 이후다.
- 운영 체크아웃에는 추적되지 않은 파일이 다수 있어 덮어쓰기나 강제 reset은
  허용되지 않는다.
- 컨테이너의 `/workspace/prof_eng_answer`에는 Master JSON, WordPress OCR
  묶음, 학습 이력 DB, `study/topic_views.py`가 현재 없다. 정확도 Gate의
  `reports/expert_accuracy_report.json`도 작업 체크아웃에는 없다. 포함된
  `expert_accuracy_seed_current.json`을 Gate에 적용하면 `HOLD`다.
- 이 차이 때문에 코드 push만으로 운영 `/review`가 바뀌지 않는다. 저장소
  브랜치를 `main`에 반영하고, 비공개 자료를 별도 절차로 운영 볼륨에 설치하고,
  release gate와 endpoint 검증을 마친 뒤 재기동해야 한다.

## 운영 반영 체크리스트

1. 운영 체크아웃의 추적되지 않은 파일과 DB를 백업하고, 새 코드와 충돌하는
   경로를 확인한다. `git reset --hard`, 강제 push, 데이터 파일 덮어쓰기를 하지 않는다.
2. 작업 브랜치를 `main`에 반영할 때 변경 범위와 기존 Grader 릴리스 정책을
   다시 확인한다. 운영 checkout은 `main`을 사용하므로 작업 브랜치 push만으로
   업데이트되지 않는다.
3. 비공개 WordPress catalog 및 OCR 묶음을 운영 데이터 경로로 이전한다.
   Master가 가리키는 출처 ID·URL·버전·본문 해시를 이전 뒤 검증한다.
4. `docs/operation_runbook.md`의 정확도 Gate, release qualification 및
   deployment proof를 충족한다. 현재 seed 보고서가 `HOLD`이므로 새 실행의
   정확도 검증 결과가 `READY`가 되기 전에는 배포하지 않는다.
5. 컨테이너 재생성 후 `engine_commit`, Master 수, OCR 묶음 수, View 로딩,
   `/review`의 원문·검토 대기 주석·점수 불변을 확인한다. 실제 Telegram
   전송은 운영 대상 사용자와 감시 방식을 확인한 뒤 endpoint smoke로 수행한다.
6. 배포가 실패하면 운영 runbook의 rollback 절차에 따라 이전 이미지·코드와
   DB 백업을 복원하고 실패 단계를 기록한다.

현재 WordPress 원문과 미확정 주석의 기술적 검토는 보류 중이다. 이 상태를
운영 배포의 승인이나 채점 기준 승인으로 간주하지 않는다.
