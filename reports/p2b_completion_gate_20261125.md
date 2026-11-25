# P2-B 완료 게이트 — 2026-11-25

## 판정: PARTIAL_OR_UNRESOLVED — P2-C 진입 차단

P2-B3–B5의 허용된 비채점 변경과 시험은 수행했다. 하지만 완료 게이트는 통과하지 못했다.

### 통과한 항목

- 역사적 111건 재실행 완료, 실행 오류 0.
- 수정 fixture 111건 재생 완료, 실행 오류 0.
- RRF 조건 생략과 Claim의 미근거 조건 추가를 구분했다. 원본 fixture는 보존했다.
- 기존 mixed 6건의 정책 차이를 `POLICY_DIFFERENCE_ACCEPTED`로 별도 기록했고 운영의 모순/WRONG 우선 규칙은 유지했다.
- 신규 36건 개발 probe 재생 완료, 실행 오류 0. 입력 라벨은 독립 검증되지 않았다.
- 보호 답안 143건의 before/after snapshot을 실제 비교했으며 0행 차이였다. snapshot SHA는 동일했으나 기록 파일에 코드 SHA가 없어 정확한 SHA 귀속은 제한된다.
- Focused pytest: `32 passed`.
- Topic Pack `validate-all`: `ALL VALID`.
- 운영 점수 연결 없음: `score_admission=DISABLED`, `score_effect=none`.

### 미통과 또는 제한

- 새 36건 probe에서 19개 개발자 provisional 관계/모순 기대가 `RECOGNITION_UNCERTAIN`으로 남았다. 이는 오답을 억지 확정하지 않은 결과이나 일반화 능력 입증에는 부족하다.
- 검토 반영 111건의 자연어 관계 기대 중 8개 paraphrase/formula가 계속 보류됐다.
- 자연어 기대 라벨과 일반화 라벨은 독립 전문가가 검토하지 않았다. 정확도/precision/recall은 `NOT_ESTABLISHED`.
- Protected replay는 동일성 증거가 있으나 실행 metadata가 없어 현 작업의 최종 코드 SHA에 대한 완전한 재현 증거는 아니다.
- 전체 pytest: 1,708 passed, 2 skipped.
- `validate-all`: `ALL VALID`; Generated freshness: 6개 생성 파일이 clean rebuild와 일치.
- Topic Pack Release Gate: PASS (89 packs/2,096 anchors; optional smoke SKIPPED).
- `PROMOTE_GENERATED=0 scripts/validate_release.sh`: 종료 코드 0. 스크립트는 aggregate `VALIDATION` marker를 출력하지 않았으므로 marker 성공을 주장하지 않는다.
- Release Candidate는 dirty worktree에서 한 차례 실행되어 HOLD(exit 2)되었다. clean commit SHA에서 다시 실행해야 하며, 최종 manifest와 결과는 Issue #40에 연결한다. GitHub Actions도 final SHA에서 아직 실행하지 않았다.

### 판단 근거와 다음 단계

저장소 작업계획의 이전 P2-B 체크포인트는 조건·범위 위험과 자연어 20건의 보류를 P2-C 차단 사유로 명시했다. 이번 변경은 위험을 더 잘 분리하고, 수정 fixture 일치 95→97을 보였지만 8개 자연어 관계와 신규 probe의 19개 관계/모순이 남아 기존 종료 조건을 충족하지 않는다. 따라서 P2-B를 완료로 표시하지 않고 P2-C를 시작하지 않는다.

독립 전문가 라벨 생성, 기술 정본·Registry 변경, 운영 채점 반영, P2-C 작업은 수행하지 않았다. 추가 개선은 이 제한이 해소되고 재현 가능한 보호 회귀 및 최종 SHA 검증 증거가 갖춰진 뒤 별도 단계로 결정해야 한다.
