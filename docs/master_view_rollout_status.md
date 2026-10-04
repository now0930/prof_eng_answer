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
| 운영 배포 | 완료 | `d7d08ee`, 결정론적 권한·채점 smoke·최종 스크립트 `RESULT=PASS` |
| 운영 컨테이너 복습 흐름 | 완료 | 실제 비공개 HTML, 임시 학습 이력 DB를 이용한 end-to-end PASS |
| Telegram 연결 | 완료 | 메시지 전송 없는 `getMe` 검사 PASS |
| 실제 사용자 채팅 화면 | 미확인 | 사용자 채팅에 시험 메시지를 보내지 않음 |

별도 백업 위치는
`/home/now0930/chatgpt_project/private_backups/2026-10-04_master_view_before_rollout`이다.
Git에서는 제외된다. 백업 대상은 WordPress SQLite catalog, OCR Topic JSON,
수동 검토 CSV, 기존 로컬 DB 백업, 생성된 rubric 보고서다. SQLite는 `.backup`
명령으로 일관된 사본을 만들었고, 소스 JSON·CSV·기존 백업은 대조했다.
Python 캐시 같은 재생성 가능한 파일은 포함하지 않았다.

## 운영 환경과 배포 결과

- 운영 컨테이너 `prof_eng_answer_bot`은
  `/home/now0930/hermes/workspace`를 bind mount한다. `main` PR #2와 배포
  스크립트 수정 PR #3이 병합되었고, 각각의 PR CI 및 `main` CI가 통과했다.
- 운영 코드 commit은 `d7d08ee1dfa5a4ef53494e4495c32a5fd3550a61`이다.
  Master 49개와 비공개 WordPress OCR 묶음 48개를 읽는다. 비공개 SQLite
  catalog는 `PRAGMA integrity_check=ok`이고 설치 사본의 해시가 백업과 같다.
- 운영 채점 모드는 `DETERMINISTIC_GRADING_PRIMARY=true`다. 현재 코드의
  결정론적 Authority Gate는 `READY`이고 컨테이너 smoke가 통과했다.
  Provider 기반 정확도 seed 보고서는 별도 Gate에서 `HOLD`다.
- 첫 배포 스크립트 실행에서는 패키지 이동 전의 import 경로가 남아 마지막
  권한 확인이 실패했다. PR #3에서 경로를 수정하고 CI를 통과시킨 뒤 재실행해
  `RUNTIME_AUTHORITY=DETERMINISTIC_PRIMARY`, `RESULT=PASS`를 확인했다.
- 배포 전 운영 `.env`와 데이터·reports·추적되지 않은 파일을 저장소 밖
  `/home/now0930/chatgpt_project/private_backups/2026-10-04_prod_premerge`에
  백업했다. 데이터 중 호스트 사용자가 읽을 수 없던 캐시 파일은 Docker를
  통해 보완했으며, 세션·환경설정은 사본을 대조했다.
- 테스트는 운영 컨테이너에서 임시 DB와 메시지 전송 mock을 사용했다.
  실제 사용자 채팅에 `/review`를 전송해 화면을 확인하지는 않았다.

## 다음 운영 점검

1. 실제 사용자 채팅에서 `/review`를 열어 표시를 확인한다. 운영 컨테이너의
   프로그램·데이터·API 연결은 이미 검증되었지만 이 화면 확인은 남아 있다.
2. 최초 실사용 채점 뒤 `data/training_history.sqlite3` 생성과 다음날 Queue
   유지·갱신을 확인한다. 통합 시험은 임시 DB로 수행했다.
3. WordPress 원문과 미확정 주석은 이후 사용자 또는 다른 LLM이 검토한다.
   검토 전에는 canonical 채점 기준으로 승격하지 않는다.

현재 WordPress 원문과 미확정 주석의 기술적 검토는 보류 중이다. 이 상태를
운영 배포의 승인이나 채점 기준 승인으로 간주하지 않는다.
