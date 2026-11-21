# PR #38 Fact Anchor 작업 인계 — 2026-11-16

대상 저장소: https://github.com/now0930/prof_eng_answer
기존 PR: https://github.com/now0930/prof_eng_answer/pull/38 (Draft)
진행 관리: https://github.com/now0930/prof_eng_answer/issues/39
브랜치: `feat/claim-alignment-verification-20261114`
이 문서 작성 직전 원격 HEAD: `078f750a6ce526a44845d4cd530ff69572fa5a88`

## 현재 상태

- 최초 48개 후보 중 18개 단문 적용, 30개 보류. [보류 ID별 사유](pr38_fact_sentence_hold_review_20261116.md)를 먼저 읽는다. 30개 중 2개는 기존 scoring exclusion을 유지한다.
- 적용된 18개는 표시용 `statement`를 짧게 하고, 채점에는 예전 전체 문장을 `expected`와 `sentence_compatibility`를 통해 유지한다. 기존 첫 accepted explanation 순서도 보존한다. Claim 분리와 채점 참조 정리는 미완료다.
- 원격 `078f750a6ce526a44845d4cd530ff69572fa5a88`의 파일 트리는 로컬 검증 커밋 `5adbc9bbba15aa1b39b4ab902f34396fc3401825`와 동일하다. 로컬에서 전체 오프라인 pytest **1793 passed, 2 skipped, 0 failed**, `VALIDATION=PASS`. 원격 SHA에서 별도 실행한 결과는 아니다. Topic Pack 전체 통합과 Generated 6개 freshness 통과, 집중 pytest 50 passed.
- 검토 작업에는 `gpt-6-luna` 구성이 요청됐으나 해당 검토 에이전트는 GPT-6이라고만 자가 식별하여 정확한 배포 모델 ID를 독립 확인하지 못했다. 각 보고서의 출처와 리뷰 provenance를 확인하고, 정확한 모델 ID가 필요한 승인 기록을 허위로 작성하지 않는다.
- PR은 Draft·미병합·운영 미배포다. 현재 구현이나 테스트 통과를 30개 Fact의 기술 승인이나 Claim 작업 완료로 해석하지 않는다.

## 시작 점검

1. 원격 PR의 실제 HEAD와 브랜치·Draft 상태를 확인하고 이 문서 작성 이후 변경이 있으면 조사한다. 별도 기존 작업물·비공개 DB·운영 checkout을 덮어쓰지 않는다. 필요하면 별도 clone/worktree를 사용한다.
2. `AGENTS.md`, `docs/topic_pack_workflow.md`, `docs/fact_anchor_eligibility_policy.md`를 완독하고, `reports/pr38_fact_sentence_hold_review_20261116.md`, `reports/pr38_sentence_compatibility_20261116.md`, `scripts/audit_fact_anchor_sentence_sync.py`, `grading/evidence/fact_anchor_compatibility.py`와 관련 테스트를 읽는다.
3. `python3 -B scripts/audit_fact_anchor_sentence_sync.py --summary-only`와 generated freshness 검사로 현재 상태를 확인한다. 기존 인계 시점의 18/30 수치는 실제 HEAD와 대조하며 과거 결과를 새 HEAD 검증으로 오인하지 않는다.

## 이어서 할 일

- 30건을 ID별로 독립적인 원문 출처, 단위, 적용 조건, 중복 Owner, scoring exclusion과 기존 인정 설명에 대조한다. 근거가 불충분하거나 필수 조건을 잃는 제안은 HOLD를 유지한다. 현재 2건의 제외는 자동 해제하지 않는다.
- 특히 feedback 후보처럼 기존 첫 accepted explanation이 이전 statement와 다른 경우, 그 설명이나 순서를 바꿔 기존 호환 검증을 통과시키지 않는다. 필요하다면 기존 채점 동작과 감사·승인 정책을 유지하는 호환 설계를 근거와 반례 테스트로 먼저 검토한다. 정책 변경이 필요한 경우 임의 변경하지 않는다.
- 열전대의 기준접점 및 비선형성, encoder 채널 주파수와 decoded event rate, 최종값 정리의 극점 조건 등 필수 경계를 보존한다. 검토 모델의 정확한 ID와 출처·조건을 실제 확인한 범위로 기록하고 불확실한 Fact는 승인하지 않는다.
- 안전하게 검증 가능한 단문만 적용하고, 관련 원문·채점 참조·accepted explanation·Generated·라우팅·D/E axis의 차이를 검증한다. 기존 배제·가중치·Goldens·A/B/C 결정론적 권한·D/E 권한·Fatal/WRONG 기준을 바꾸거나 테스트를 삭제, skip, xfail 또는 quarantine하지 않는다.
- 단문화가 정리된 뒤 기존 Claim 정리 및 Source–Generated 채점 영향 분석으로 복귀한다. Claim 분리·중복 제거는 기존 점수와 소유권을 임의로 변경하지 않는다.
- Generated JSON은 직접 수정하지 말고 `python3 scripts/rubric_manager.py validate-topic-pack-release --all --promote-generated`로 생성한다. `python3 -B scripts/check_generated_rubrics_freshness.py`, 해당 focused pytest, `git diff --check`, 전체 오프라인 `python3 -B scripts/release_candidate.py validate`를 실행한다. 채점 코드 변경 시 AGENTS.md의 `PROMOTE_GENERATED=0 scripts/validate_release.sh`와 `python3 scripts/rubric_manager.py validate-all`도 실행한다.
- 실제 통과·실패·건너뜀·종료 코드, 실행 SHA와 manifest를 기록한다. 변경을 기존 브랜치에 커밋·푸시하고 원격 HEAD를 확인한다. PR #38과 Issue #39에는 증거가 있는 범위만 기록하며 나머지는 열린 상태로 둔다.

기존 `prof_eng_answer` 디렉터리, 운영 Telegram 봇과 실제 사용자 데이터, `main`은 수정하지 않는다. PR은 Draft로 유지하고 병합·운영 배포·봇 재시작을 하지 않는다. 새로운 Accuracy Gate나 별도의 READY 필수 조건은 추가하지 않는다. 이 작업의 필수 코드 검증 기준은 전체 오프라인 pytest다.
