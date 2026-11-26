# P2-B8 — LLM Claim 추출 실험 결과

## 판정

`PARTIAL_OR_UNRESOLVED`. 기존 결정론적 A의 기준 결과를 재현했고, Canonical Claim Schema를 사용하는 연구 전용 B 어댑터와 A 우선 C 결합기를 구현·모의 검증했다. **실제 LLM 호출은 하지 않았으므로 B/C의 데이터셋 성능은 측정하지 않았다.** P2-B 전체 완료 또는 P2-C 진입 근거가 아니다.

## 입력과 재현성

- 브랜치: `docs/issue40-canonical-claim-next-phase-20261125`
- 실험 전 HEAD: `cf90a5423e3b179aef97d2c7c6c5afa742f8a57a` (최신 원격과 일치)
- 계약 SHA-256: `3471bfed4d2b73f71006d6a565cf5909417c16e42be7b1aa14d5c6f6e394cb2d`
- 111건 원본 SHA-256: `bf75899e302c5cb9736332fe230a914d0cd0d57d09c8d59e6328910267e60ee9`
- 검토 36건 SHA-256: `16acea86da65f53d6e17956a975fec9a3722ce6312411c03454f04132833ad2b`
- **정정(P2-B8L, 2026-11-26):** 원본 B8 계약이 지정한 fidelity 대상 경로는 실제로 `reports/p2b_b7_claim_fidelity_targets_20261126.json`이다. 해당 경로가 누락됐다는 이전 문장은 잘못이었다. 파일 SHA-256은 `05800ed92f408fe7aace4e9259235a91f29865dfddc96473525f50c14d728bbc`이며 28 target/16 control subset 검증은 읽기 전용으로 수행했다. 원본 계약과 기대값은 수정하지 않았다.
- 데이터는 64 structured + 47 natural + reviewed label view 36 = 147 case rows다. natural 83행 중 `flow_mass_rate_density_relation/condition_omitted`와 `GEN-10`은 Topic·질문·답안 입력이 같아 **고유 natural 입력은 82개**다. 28 target과 16 control은 기존 데이터의 부분집합이며 추가 표본으로 더하지 않았다.
- natural fixture의 Topic ID는 5개다. B8L에서는 파일럿 균형 단위를 6개 기존 기술 관계로 개정했으며 Topic 수 조건으로 해석하지 않는다.

## A/B/C 결과

| Arm / 집합 | 건수 | 기대 판정 일치 | 실행 오류 | 결과 |
|---|---:|---:|---:|---|
| A, structured | 64 | 57 | 0 | 결정론적 기준선 |
| A, 기존 natural | 47 | 38 | 0 | 결정론적 기준선 |
| A, reviewed generalization | 36 | 17 | 0 | 같은 원본의 검토 라벨 view |
| A, natural 합계(행 단위) | 83 | 55 | 0 | 82개 고유 입력, 1개 중복 입력 |
| A, focus target | 28 | 1 | 0 | fixture-relative; 정확도 지표 아님 |
| A, defense controls | 16 | 16 | 0 | fixture-relative; 정확도 지표 아님 |
| B, 실제 LLM | 0 | NOT_RUN | 0 requests | 키·모델·승인 예산 미설정, 6-topic pilot 불일치 |
| C, 실제 B 보완 | 0 | NOT_RUN | 0 requests | B 호출 결과 없음 |

전체 A 147행의 기존 기준 재생과 현재 경로를 Case ID별 대조한 결과 관측 상태 차이는 0건이다. B/C의 잘못 추출한 실제 Claim 수, 보류율, precision/recall은 **측정 불가**다. 모의 결과를 모델 성능으로 해석하지 않았다.

## 구현 및 fidelity 방어

- `grading/evidence/p2b8_llm_claim_extractor.py`: 기존 Canonical Evidence Schema를 사용한다. 프롬프트에는 질문, 답안, Topic scope 및 Topic contract·기존 ontology에서 유도한 허용 ID/별칭만 넣는다. case ID, 기대 label/Claim, 정답 Fact tuple, 점수 정보는 보내지 않는다. 원문 span, 필수 필드, polarity/context, topic 소유권, 조건 ID와 중복 span을 엄격히 검사한다. `requirement_refs`는 비워 두고 소유 Topic은 로컬에서 부여한다.
- `grading/evidence/gemini_semantic_provider.py`: score-neutral Claim extraction request envelope만 추가했다. live 호출은 `VALIDATION_LIVE_API=1`, 별도 validation 키, 명시 모델과 budget, 고정 SHA의 합성 fixture가 필요하다. 전용 provider factory는 contract의 6-topic 조건을 확인하며 case ID·label을 payload에 넣지 않는다. 생산 키 fallback은 허용하지 않는다.
- `scripts/audit_relation_recognition.py`: 연구용 Canonical Evidence override를 선택적으로 받는다. 기본 결정론 경로는 그대로 두고 질문/답안 fingerprint, 기존 Schema 및 owner를 다시 검증한다.
- `evaluate_extracted_evidence()`는 원시 contract 비교와 source-grounded 결과를 분리한다. fidelity `FAIL` 또는 `NOT_ESTABLISHED`이면 raw match도 grounded 확정으로 올리지 않는다. 현재 fidelity 검사기는 의미 proof `PASS`를 생성하지 않으므로 의미 정합성은 아직 확립되지 않았다.
- C 결합기는 A의 명시적 unresolved span 안에서만 B를 보충하고 A와 겹치거나 이미 있는 관계는 추가하지 않는다. fixture 단위 테스트만 수행했고 전체 C 재생은 하지 않았다.
- mock probe: GEN-09의 “합”을 승인된 곱 관계로 잘못 구조화한 응답은 `CLAIM_FIDELITY_FAILURE`로 보류됐다. GEN-26 영문 mock은 raw comparator에서 관계 후보가 나왔지만, semantic fidelity proof가 없어 grounded 결과는 `RECOGNITION_UNCERTAIN`이다. 두 probe 모두 운영 영향은 `score_admission=DISABLED`, `score_effect=none`이다.
- 20개 P2-B8 테스트는 기존 Gemini transport envelope, 입력/출력 격리, 잘못된 ID·authority field·span·조건·문맥·duplicate·timeout·인용·용어 나열, GEN-09/26 차단, C의 unresolved-only 보완, live fail-closed를 검사했다. 이는 모의 계약 검증이지 의미 정확도 평가가 아니다.

## 외부 호출과 보호 답안 143건

- 실제 LLM 호출: `NOT_RUN`, model/version 없음, request 0, 비용 `$0`.
- 호출하지 않은 이유: validation 키·모델·승인 예산 및 live opt-in이 설정되지 않았다. 또한 제공 fixture가 5 Topic이라 계약의 6-topic pilot balanced sampling을 만들 수 없다.
- 보호 답안 143건: `NOT_RUN`. `/mnt/data`, Codex attachments 및 기존 workspace에서 입력 자료/재생 명령 후보를 파일명 기준으로 찾아 복구하지 못했다. 과거 `/tmp` 결과 스냅샷을 원본 입력이나 새 replay 증거로 사용하지 않았다. 비공개 답안은 provider에 보내지 않았다.

## 검증

- Focused: `python3 -B -m pytest -q tests/test_p2b_b8_llm_claim_extractor.py tests/test_audit_relation_recognition.py tests/test_canonical_grading_evidence.py` — **50 passed** (after final fail-closed additions).
- P2-B8 module: **20 passed**.
- 전체 pytest: `python3 -B -m pytest -q` — **1,731 passed, 2 skipped**, exit 0.
- 전체 pytest는 최종 B8 소스/테스트에서 `1,733 passed, 2 skipped`, exit 0.
- 최종 코드가 커밋된 `7c43dd6a1a2ef2d51749391cd7ff753ce87b4108`에서 `python3 -B scripts/rubric_manager.py validate-all` — `ALL VALID`, exit 0.
- 같은 커밋에서 `python3 -B scripts/check_generated_rubrics_freshness.py` — `GENERATED RUBRICS FRESH: 6 files match a clean rebuild`, exit 0.
- 같은 커밋에서 `python3 -B scripts/rubric_manager.py validate-topic-pack-release --all` — **PASS**, 89 packs / 2,096 anchors; smoke `SKIPPED`(검증기 기본 동작), Generated snapshot restored.
- 같은 커밋에서 live API off, qualitative DE off, `PROMOTE_GENERATED=0`으로 `scripts/validate_release.sh` — **PASS**, exit 0.
- Python Release Candidate는 첫 dirty-worktree 시도에서 `HOLD`, exit 2였고, clean commit `7c43dd6a1a2ef2d51749391cd7ff753ce87b4108`에서 재실행하여 **`VALIDATION=PASS`**, `1,733 passed, 2 skipped`, exit 0. Manifest: `/tmp/p2b-issue40/reports/release_candidates/20261126T012908Z_7c43dd6a1a2e_pytest/manifest.json`; SHA-256 `ba67041e4cb6940e6d83deb468a00bb72bccfdd091d51388edcfe233e5884c2f`.
- 동일 SHA GitHub Actions: 당시 미실행. 원격 push 후 최종 브랜치 HEAD용 실행 결과를 Issue #40/PR #49에 기록한다.

## 불변성 및 게이트

Fact Anchor, Topic Pack, Registry, Generated 파일, scoring policy/evaluator, A~E, 25점 배점, Fatal/WRONG/Ceiling을 변경하지 않았다. 수정 범위는 Gemini request envelope, 비채점 audit override, P2-B8 연구 adapter/runner/tests/reports다. `119 HOLD`, D4, `score_admission=DISABLED`, `score_effect=none`, Draft PR #49, main 병합 금지 상태를 유지한다.

### 미완료 게이트

1. B/C 실제 LLM 비교 및 승인된 사용량/비용 실측
2. 6-topic 조건을 충족하는 올바른 검증 fixture 및 누락된 target artifact 경로 정정
3. 143 보호 답안의 입력과 재생 명령을 권한 있는 비공개 환경에서 복구·재생
4. B9 독립 의미 검증, B10 P2-B 최종 게이트

따라서 P2-B8은 구현·모의 시험 부분 완료일 뿐이고 P2-B 전체는 미완료, P2-C는 차단 상태다. 정확도 및 human semantic validation은 `NOT_ESTABLISHED`다.

## P2-B8L 후속 정정 및 현행 상태

위 A/B/C 표와 mock/미실행 기록은 원본 B8 실행 시점의 역사적 결과다. 후속 B8L에서 확인된 오류·변경은 다음과 같다.

- 원본 B8 계약의 fidelity 대상은 처음부터 `reports/p2b_b7_claim_fidelity_targets_20261126.json`이었다. “B8 target 파일 누락”이라고 한 이전 문장과 runner 주석은 잘못된 설명이었다. 경로 및 28/16 subset은 그대로 검증했고, 원본 계약은 수정하지 않았다.
- 원본 B8의 live 파일럿 설명은 6 Topic을 요구했지만 제공 시험에는 5 Topic만 있다. B8L은 원본 계약을 보존하고 별도 `p2b_b8l_experiment_contract_20261126.json`으로 범위를 개정해 지정된 12건을 6개 기존 Requirement 관계(관계별 2건), 5개 Topic에서 선택한다.
- 현재 runner는 `--live-pilot`으로 12건을 실제 실행·기록할 수 있다. B 응답을 C에서 재사용하며 C를 위해 추가 호출하지 않는다. API 자격증명/opt-in과 승인 예산 외에 model별 input/output 요율이 없거나 예상 예약 비용이 예산을 넘으면 호출 전에 중단한다.
- 원문 fidelity `FAIL`은 이제 `FAIL`로 유지한다. 근거 없는 일반 자연어 등은 `NOT_ESTABLISHED`로 남고 grounded PASS 경로는 추가되지 않았다.
- C는 A가 claim과 같은 구간을 명시적으로 unresolved로 표시한 경우, 동일 입력에서 B가 보완 관계를 내더라도 해당 불완전 A 조각 때문에 차단되지 않도록 한다. A의 기존 관계는 동일 tuple 중복이거나 unresolved 외부의 관계이면 보존한다.

최신 실행 수치, B8L live 준비 결과와 검증 증거는 `reports/p2b_b8l_experiment_results_20261126.md` 및 `reports/p2b_b8l_comparison_20261126.json`을 기준으로 한다.
