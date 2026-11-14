# Claim Alignment 보완 프로젝트 — 구현/검증 상태

**브랜치:** `feat/claim-alignment-verification-20261114`  
**기준:** `codex/data-reports-inventory-20261113` (base `7e3b1471`), 2026-11-14  
**관리:** [Epic #32](https://github.com/now0930/prof_eng_answer/issues/32), [#33](https://github.com/now0930/prof_eng_answer/issues/33), [#34](https://github.com/now0930/prof_eng_answer/issues/34), [#35](https://github.com/now0930/prof_eng_answer/issues/35), [#36](https://github.com/now0930/prof_eng_answer/issues/36), [#37](https://github.com/now0930/prof_eng_answer/issues/37)

## 목적과 불변 규칙

Fact Anchor(올바른 기술 사실), 사용자 답안(자유 서술), Logic Check(오류/금지 관계)를 공통 Claim으로 **투영**하고 의미 비교 근거를 추적한다. 본 구현은 **검증된 Fact/Logic/Question Contract의 기존 권한을 변경하지 않는다**. A/B/C 결정론적 확정, D/E LLM 제안·프로그램 검증, 배점 A3/B6/C8/D6/E2, Fact Approval/Scoring Exclusion, Fatal/score ceiling, 합격 참고선 및 `release_candidate.py validate` 필수 정책을 유지한다.

- **source-preserving:** `rubrics/topic_packs/*/fact_anchor.json` 및 `logic_check.json`은 변경하지 않는다. 검증·승인된 `approved_fact_registry.json`의 `legacy_anchor_id`와 Topic/질문 범위를 먼저 대조하고, 존재하면 해당 구조화 관계를 우선 투영한다. Registry Fact가 없으면 Machine Contract를 **미검증 진단 관계**로만 보존한다. 읽어낼 수 없는 자연어 Fact를 **추측하여 정답 관계로 만들지 않는다**.
- **source role isolation:** Fact=기준, Answer=주장, Logic=승인된 오류 규칙. Logic의 Regex를 신규 Fatal 엔진으로 복제하지 않는다. disabled Logic Checker를 활성화하지 않는다.
- **score-neutral boundary:** `claim_alignment_contract.py` 결과에 `score_effect=none`, `authority=audit_only`를 강제한다. 모델이 반환하는 supported/partial/contradicted는 점수·Wrong·Fatal이 아니다.
- **privacy:** Claim/Audit는 원문 answer 대신 SHA-256/offset/ID/개수만 공개 로그로 남기며, private source는 기존 session 보관 정책을 따른다.
- **failure behavior:** 감사 경로의 오류는 `status=ERROR` + 비식별 예외 클래스만 기록하고 기존 score/verdict를 변경하지 않는다.

## 단계와 작업 현황

| 단계 | 목적 | 주요 파일 | 상태 |
| --- | --- | --- | --- |
| 0 | 기준 브랜치 확인·신규 작업 브랜치 생성 | GitHub branch | **완료** |
| 1 | Fact/Logic 공통 관계 투영·스키마 검증 | `claim_alignment_contract.py`, `fact_claim_adapter.py`, `logic_rule_adapter.py` | **구현됨 · 검증 Registry 우선** |
| 2 | 답안 Canonical Claim과 관계 비교·불확실 처리 | `claim_alignment_engine.py` | **구현됨** |
| 3 | LLM 제안과 독립 검토 결과를 검증 Registry/원문 위치에 연결 | `semantic_admission.py`, `semantic_alignment_bridge.py`, `fact_unresolved_queue.py`, `run_semantic_assist_private.py` | **score-neutral 구현됨** |
| 4 | Primary Grader에 비침습적 shadow 경로 추가 | `deterministic_primary_grader.py` | **구현됨, 기본 OFF** |
| 5 | 합성 정답/조건누락/부정/오답/disabled Logic·LLM 근거 오류 회귀 | `tests/test_claim_alignment_*.py`, `tests/test_semantic_alignment_bridge.py` | **작성됨, 실행 결과 미확인** |
| 6 | 전체 오프라인 pytest 기반 Release Validation | `python3 -B scripts/release_candidate.py validate` | **미실행; PASS 주장 금지** |
| 7 | 실험 정확도 평가 및 A/B/C 점수 반영 가능성 검증 | #33/#35/#37 | **추가 연구/검증 필요, 미활성** |
| 8 | 운영 배포 전 백업·격리 복원·smoke | #23 | **미진행, 운영 서버 불변** |

## 호출과 출력

- 기본: `CLAIM_ALIGNMENT_MODE=off` — 기존 응답 구조·최종 점수 그대로.
- 점수 중립 감사: `CLAIM_ALIGNMENT_MODE=shadow` — `grade_deterministically()` 결과에 `claim_alignment_audit`의 `status`, `summary`, `fingerprint`, `score_effect`만 추가.
- `CLAIM_ALIGNMENT_MODE=admit_verified`는 **아직 지원하지 않는다**. 두 LLM의 동의나 구조 일치만으로 확정된 기술적 사실을 만들어서는 안 된다. 기존 Private Semantic Assist는 `semantic_alignment_bridge`를 통해 `ALIGNED_WITH_DETERMINISTIC_EVIDENCE/PENDING` 감사 결과를 생성하지만 **둘 다 최종 채점 권한은 없다**. 다과목 반례와 의미적 검증을 통과한 경우에만 score-bearing 도입을 검토한다.
- `scripts/audit_claim_alignment.py`는 synthetic `{question_text,answer_text}` case를 받아 동일 입력의 OFF/SHADOW 결과를 비교한다. 이미 존재하는 출력을 덮어쓰지 않으며 private output을 0600으로 생성한다.

## 예상 테스트

```bash
python3 -B -m pytest -q \
  tests/test_claim_alignment_contract.py \
  tests/test_claim_alignment_primary_shadow.py \
  tests/test_canonical_grading_evidence.py \
  tests/test_canonical_claim_extractor.py \
  tests/test_deterministic_primary_grader.py \
  tests/test_semantic_alignment_bridge.py

python3 -B scripts/release_candidate.py validate
```

Github Actions는 `workflow_dispatch` 수동으로만 실행되며 현재 환경은 실행/배포 머신이 아니다. **실제 전체 pytest 결과를 수집하지 않은 상태에서 RELEASE PASS 또는 FIXED라고 기재하지 않는다**.

## 안전성 위험과 다음 단계

1. 기계 구조화 관계가 없는 Fact Anchor에 대해 무리하게 NLP 분해하면 실제 조건이 사라지거나 논리 오류가 발생한다. **판정 불가** 상태를 명시한다.
2. Logic Check의 많은 규칙은 단일 subject/predicate/object가 아니라 조건부 위반/복합 제약이다. 모든 Logic을 동일 원자 Claim으로 강제하지 말고 Rule ID/적용 조건/검증된 결함 연결을 분리한다.
3. LLM의 semantic agreement는 의미 해석의 지표일 뿐 물리적 사실의 독립 검증이 아니다. 현재 `unresolved_semantic_assist.py`와 `fact_semantic_review.py`는 `score_effect=none`을 유지한다.
4. 위 Shadow 결과가 정상인 것을 확인한 다음, **요구사항별 독립 전문가 라벨과 통제된 반례**로 False Acceptance/False Rejection을 검증할 때에만 score-bearing admission을 설계한다. 현재 필수 배포 Gate는 전체 오프라인 pytest이며 Accuracy·Authority·Stability/유료 Qualification을 새 필수 Gate로 추가하지 않는다.
5. 기존 [Issue #36](https://github.com/now0930/prof_eng_answer/issues/36)의 Gemini D/E `duplicate_positive_evidence`는 이 Claim Alignment와 별도 원인·분리된 테스트 대상이다.

**범위 정직성:** 이 작업 브랜치는 현재 공통 형식·분석·비침습적 shadow까지 구현한다. 모든 과목의 자유로운 동등 표현을 LLM이 평가하여 A/B/C 점수에 반영하는 운영 기능은 아직 완성된 것으로 선언하지 않는다.

## 2026-11-14 추가 통합 결과

- Fact Relation은 **승인된 Registry**에서 선택한다. Registry와 Machine Contract의 관계가 다르면 `machine_relation_differs=true`로 보고하고, 승인된 Fact를 임의 수정하거나 오류 경중을 단정하지 않는다.
- `claim_alignment_engine._compare`는 검증 Registry의 주장·조건·극성과 답안 Claim을 비교한다. "항상/무조건/언제나"처럼 절대적 양화사가 붙으면 기존 Logic Check의 판단이 필요하므로 동일한 주어·관계·대상이라는 이유만으로 `EXACT_RELATION`을 부여하지 않는다.
- private `run_semantic_assist_private.py`에서 원래의 독립 LLM 검토 후 `claim_alignment_audit`를 별도 생성한다. 승인 Fact snapshot, 질문/답안 SHA, source span, quote, 독립 검토를 연결한다. **외부 API 사용 여부는 이 도구의 기존 Validation Credential 및 live API 정책이 결정한다**. 이 코드 작성 과정에는 실사용 LLM 호출이 없었다.
- `semantic_admission.py`는 유효한 원문 인용과 동일한 span의 결정론적 Exact Relation을 동시에 요구한다. **이미 확정된 관계의 정합성 확인**이며 미검증 문장 변형을 새 정답으로 승격하는 기능은 아니다.
- Shadow 실패 시 기존 A/B/C/D/E, WRONG/Fatal/ceiling과 verdict는 그대로 유지한다. 전체 release validation 미실행 상태이므로 운영 반영/Issue CLOSE 금지.

**현재 코드 상태:** 원천 정규화·검증 출처 기반 Claim 비교·독립 LLM 감사 연결·Primary Shadow·합성 회귀 테스트 파일 작성까지 GitHub 브랜치에 커밋했다. 실행 검증과 실제 점수 반영 성능 입증은 완료하지 않았다.
