# Claim Alignment 보완 프로젝트 — 구현/검증 상태

**브랜치:** `feat/claim-alignment-verification-20261114`  
**기준:** `codex/data-reports-inventory-20261113` (base `7e3b1471`), 2026-11-14  
**관리:** [Epic #32](https://github.com/now0930/prof_eng_answer/issues/32), [#33](https://github.com/now0930/prof_eng_answer/issues/33), [#34](https://github.com/now0930/prof_eng_answer/issues/34), [#35](https://github.com/now0930/prof_eng_answer/issues/35), [#36](https://github.com/now0930/prof_eng_answer/issues/36), [#37](https://github.com/now0930/prof_eng_answer/issues/37)

> **최신 실행 증빙 (2026-11-14):** 기존 검증 커밋
> `dd8098bfb7df907a09eb3a8960a3eceeba57a027`의
> [GitHub Actions #43552790853](https://github.com/now0930/prof_eng_answer/actions/runs/43552790853)
> 결과는 **VALIDATION=PASS, 1,685 passed, 2 skipped**이다.
> 아래 과거 '미실행' 표현은 당시 기록이며 최신 S5/S6 판정을 대신하지 않는다.
> **그 이후 커밋한 S7 신규 구현은 아직 PASS 검증되지 않았다.**
> 점수 반영·운영 배포 금지 유지.

## S7 독립 정확도 연구 (신규; 재검증 전)

- [S7 독립 검토 프로토콜](claim_alignment_s7_review_protocol_20261114.md) 문서화.
- 기존 `calibration/expert_accuracy_golden.jsonl`에서 **48건/31 Topic/5 질문 유형** 확인(45 reviewed, 3 adjudicated, demand 141건). 기존 전문가 라벨과 Fact Anchor ID는 자동 매핑 금지.
- `claim_alignment_s7_benchmark.py`: 기존 검증 Fact·Answer span 기반의 후보를 **비공개 독립 리뷰**에 연결. 명시적 `CREDITABLE/NOT_CREDITABLE/UNRESOLVED`와 Provenance 없으면 미검증. 연구용 결과만 산출, `score_admission=DISABLED`.
- `scripts/evaluate_claim_alignment_s7.py`: 전문가 Golden의 기존 점수·오합격 기준선과 새로운 S7 후보 집계를 분리한 **offline 실험**. 원문 답안·미검증 라벨을 공개 출력하지 않는다.
- `tests/test_claim_alignment_s7_benchmark.py`, `tests/test_claim_alignment_s7_experiment.py`: forged/stale candidate·리뷰 누락·인용 가능한 신원·골든 source 격리·OFF only 재현 등 테스트 추가.
- Actions `run_s7_experiment` 입력은 **기본 OFF/수동 체크 시만** 동작한다. 선택적 연구 실험의 실패를 기존 필수 Release Gate의 실패로 새롭게 정의하지 않는다.
- 새 전체 pytest/Release Gate 검증 전 **S7 완료 또는 채점 정확도 상승**을 주장하지 않는다.

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
| 5 | 합성 정답/조건누락/부정/오답/disabled Logic·LLM 근거 오류 회귀 | `tests/test_claim_alignment_*.py`, `tests/test_semantic_alignment_bridge.py` | **PASS @ dd8098 (S7 신규 코드는 재검증 필요)** |
| 6 | 전체 오프라인 pytest 기반 Release Validation | `python3 -B scripts/release_candidate.py validate` | **PASS @ dd8098: 1,685 passed, 2 skipped** |
| 7 | 실험 정확도 평가 및 A/B/C 점수 반영 가능성 검증 | #33/#35/#37 | **독립 검토 계약/48건 Golden 연구 실험 구현, 신규 테스트 미실행, A/B/C 반영 미활성** |
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

## 2026-11-14 S5c — Canonical 출처·점수 패리티 강화 (검증 미실행)

- `claim_alignment_engine.py`: 원문 답안 SHA 이외에 **문제 SHA, Canonical Evidence 전체 지문, 결정론적 파서 출처**를 검증하도록 강화. 서로 다른 Topic의 `qualifiers.owner_topic_id`가 붙은 Claim은 해당 Fact에 연결하지 않는다.
- `semantic_alignment_bridge.py`: 재파싱 독립 확인 시 Claim의 Topic 소유권도 대조한다.
- `tests/test_claim_alignment_contract.py`: 서로 다른 문제의 문서 재사용, 서명 없는 수정, 의미 평가기를 가장한 결정론적 문서, 다른 Topic Claim 유입을 모두 거부하는 부정 테스트 추가.
- `tests/test_semantic_alignment_bridge.py`: Topic 소유권 교차 사용 방지 테스트 추가.
- `tests/test_claim_alignment_primary_shadow.py`: 기존 열전대 사례에 더해 PID, 차압 유량, SIL 오류 사례를 독립 실행해 OFF/SHADOW 동등성을 검증하도록 테스트 확대.
- **패리티 검사 수정:** `score_breakdown`은 실제 Primary Grade 결과에 존재하지 않는 키이므로, 비교 대상에서 제외하고 `breakdown`, `score_range`, `qualitative_de_evaluation`, `emc_no_gain_guard`, `resolution_review`를 비교한다. 대응 `scripts/audit_claim_alignment.py`도 같은 정책으로 확장했다.
- **테스트 결과:** 소스 파일/검증 케이스 추가까지 GitHub 커밋. 전체 실행 또는 GitHub Actions 결과는 현재 확인되지 않았으며 **S5/S6 PASS로 판정하지 않는다**. Score-bearing S7 admission은 여전히 미구현·비활성.

## 2026-11-14 S5b/S7-shadow — 재파싱 및 누락 후보 감사 (검증 미실행)

- **S5b:** `semantic_alignment_bridge.py`가 `EXACT_RELATION` 감사값을 그대로 신뢰하지 않고, 원문 질문/답안으로 **결정론적 Canonical Claim을 다시 추출**한 뒤 Claim ID, span, asserted 문맥, 관계·극성·조건을 승인 Fact와 재대조한다. 독립 재추출로 확인하지 못하면 `PENDING/fresh_canonical_relation_not_confirmed`. 원문 위조·인용·부정·파서 실패·Claim ID 불일치에 대한 합성 회귀 테스트를 추가했다. 모델 해석은 계속 score-neutral.
- **S7-shadow 준비:** `claim_alignment_recall_audit.py`는 승인 Registry에 대응하는 `EXACT_RELATION`이지만 기존 요구사항 평가가 `MISSING/PARTIAL/UNKNOWN`인 경우를 `REVIEW_POTENTIAL_RECALL_MISS`로 식별한다. 이는 **사람/독립 데이터 라벨 검토 대상**일 뿐 `SATISFIED`로 승격하거나 점수를 변경하지 않는다.
- `WRONG`은 `BLOCKED_EXISTING_WRONG`, 기존 `SATISFIED`는 `ALREADY_SATISFIED`, Registry 미검증은 `NOT_VERIFIED`, Machine Contract 불일치는 `HOLD_SOURCE_CONTRACT_CONFLICT`로 구분한다. 동일 Span 중복, 엉뚱한 요구사항, 조건 미충족을 새 점수 근거로 사용하지 않는다.
- Primary `shadow` 응답에는 원문 텍스트를 기록하지 않고 `recall_review.candidate_count/disposition_counts/score_effect=none`만 남긴다. OFF/SHADOW 비교의 A~E·Fatal·상한·verdict 무변경 원칙은 유지한다.
- **검증 차단:** 프로젝트 전체 로컬 체크아웃을 확보하지 못했으며 현재 연결에 `workflow_dispatch` 실행 액션이 없다. 작성된 테스트의 실제 PASS 및 `release_candidate.py validate` 완료를 주장하지 않는다. S7 점수 반영 모드 `admit_verified`는 여전히 미구현·미활성. Draft PR 유지.

실행 대상:

```bash
python3 -B -m pytest -q tests/test_claim_alignment_contract.py \
  tests/test_claim_alignment_primary_shadow.py \
  tests/test_semantic_alignment_bridge.py \
  tests/test_claim_alignment_recall_audit.py
python3 -B scripts/release_candidate.py validate
```

## 2026-11-14 S5 보강 — 출처 결박과 부정 회귀 (검증 미실행)

- `semantic_alignment_bridge.py`: 기존 answer SHA, fact snapshot 외에 **Claim Alignment 전체 계약/지문**을 검증하고, `VERIFIED_REGISTRY_RELATION` 주장이 실제 승인 Registry Fact의 Topic·legacy Anchor·출처·공통 관계와 일치하는지 재대조한다. 위조된 관계를 유효한 새 fingerprint로 감싼 경우에도 `PENDING/source_relation_mismatch`로 취급한다. 점수 영향은 계속 없음.
- `logic_rule_adapter.py`: `deterministic_checks`가 없거나 disabled이면 규칙을 투영하지 않는다. 별도 최상위 profile의 `fatal_checks`를 빈 deterministic list 대신 활성화하지 않는다. `enabled`가 생략된 **실제 중첩 deterministic profile**은 기존 평가기의 기본 활성 정책에 맞게 유지한다.
- `tests/test_semantic_alignment_bridge.py`: 위조 관계, 출처 위조, 변경된 audit 지문 반례를 추가했다. 합성 Fact fixture에도 Registry 원천 관계를 명시해 무근거 관계의 승인 사례를 제거했다.
- `tests/test_claim_alignment_contract.py`: 최상위-only/빈/disabled deterministic profile과 정상 중첩 profile의 구분 검증을 추가했다.
- 이 변경은 **S5 테스트 코드 추가/수정**이지 실행 완료가 아니다. S6 전체 release validation은 **미실행**이고, S7 `admit_verified`는 **아직 미구현/미활성**이다. Draft PR 상태와 운영 불변 정책을 유지한다.

## 2026-11-14 추가 통합 결과

- Fact Relation은 **승인된 Registry**에서 선택한다. Registry와 Machine Contract의 관계가 다르면 `machine_relation_differs=true`로 보고하고, 승인된 Fact를 임의 수정하거나 오류 경중을 단정하지 않는다.
- `claim_alignment_engine._compare`는 검증 Registry의 주장·조건·극성과 답안 Claim을 비교한다. "항상/무조건/언제나"처럼 절대적 양화사가 붙으면 기존 Logic Check의 판단이 필요하므로 동일한 주어·관계·대상이라는 이유만으로 `EXACT_RELATION`을 부여하지 않는다.
- private `run_semantic_assist_private.py`에서 원래의 독립 LLM 검토 후 `claim_alignment_audit`를 별도 생성한다. 승인 Fact snapshot, 질문/답안 SHA, source span, quote, 독립 검토를 연결한다. **외부 API 사용 여부는 이 도구의 기존 Validation Credential 및 live API 정책이 결정한다**. 이 코드 작성 과정에는 실사용 LLM 호출이 없었다.
- `semantic_admission.py`는 유효한 원문 인용과 동일한 span의 결정론적 Exact Relation을 동시에 요구한다. **이미 확정된 관계의 정합성 확인**이며 미검증 문장 변형을 새 정답으로 승격하는 기능은 아니다.
- Shadow 실패 시 기존 A/B/C/D/E, WRONG/Fatal/ceiling과 verdict는 그대로 유지한다. 전체 release validation 미실행 상태이므로 운영 반영/Issue CLOSE 금지.

**현재 코드 상태:** 원천 정규화·검증 출처 기반 Claim 비교·독립 LLM 감사 연결·Primary Shadow·합성 회귀 테스트 파일 작성까지 GitHub 브랜치에 커밋했다. 실행 검증과 실제 점수 반영 성능 입증은 완료하지 않았다.
