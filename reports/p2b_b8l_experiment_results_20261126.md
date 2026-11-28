# P2-B8L — 실제 LLM 비교 파일럿 실행 결과

## 결과 상태

`LIVE_NOT_RUN` — 허용된 실제 LLM 호출은 0건이다. 환경에서 `VALIDATION_LIVE_API`, 전용 `VALIDATION_GEMINI_API_KEY`, `P2B8_GEMINI_MODEL`, 승인 예산 및 모델별 input/output 요율이 모두 설정되지 않았다. runner를 `--live-pilot`로 실행했으며 fail-closed 사유는 `live_api_not_opted_in`이었다. 키 값은 읽거나 출력하지 않았다.

따라서 이번 결과는 A 기준선 재현, B/C live 실행 준비 및 비용/프롬프트/결과 기록 구현의 검증이다. B/C 실제 성능이나 독립 의미 정확도 측정이 아니다.

## 실행 계약과 입력

- 실행 기준 commit: `8adf54e5364b8c304e7d703d08a7662222564ffb` (B8L runner와 B8 계약 v2 반영 후).
- 수정 코드 파일 SHA-256은 결과 JSON `code_file_sha256`에 기록.
- B8 계약 v2 SHA-256: `d4454b06b78dcf330696fa089e40c1ebb36600a7b555e0a8ce90c979cecd5672`; B8L 동반 계약 SHA-256: `8ba2341eebc9a77c5696d4569392d0ac46dcfe7a0534eb0ca3700739a28af47f`.
- 원본 B8 계약 v1은 이전 commit history에 보존했다. 원격에서 반영된 v2는 원래 6 Topic 균형 요구를 **6개 기존 기술 관계별 2건**, 5 Topic의 합성 공개 fixture 표본으로 명시적으로 개정하고 83행/82개 고유 입력 수를 기록한다. 동반 B8L 계약은 비용 사전검사와 실행 보호를 상세화한다. v2 구현 상태는 `IMPLEMENTED_LIVE_NOT_RUN`이다.
- 파일럿 ID: GEN-01/04, GEN-07/09, GEN-14/15, GEN-20/22, GEN-26/27, GEN-34/35. 기대 라벨은 provider 요청에 넣지 않았다.
- 사용된 공개 합성 데이터: 구조화 64, 자연어 47, 검토 일반화 36 = 총 147행. 자연어는 83행/82개 고유 입력이며 `GEN-10`과 `flow_mass_rate_density_relation/condition_omitted`가 같은 입력이다. 28개 focus 및 16개 controls는 기존 subset이라 추가 표본이 아니다.
- B8 계약 v2의 fidelity 대상은 `reports/p2b_b7_claim_fidelity_targets_20261126.json`이며, 이전 “B8 대상 파일 누락” 설명은 잘못이었다. 파일 SHA-256은 `05800ed92f408fe7aace4e9259235a91f29865dfddc96473525f50c14d728bbc`다. 원본 fixture 문장과 기대 판정은 바꾸지 않았다.

## A/B/C 측정

| 평가 | 실행 결과 | 해석 |
|---|---:|---|
| A 구조화 기준 64 | 57 일치, 0 실행 오류 | fixture-relative 기준선 |
| A 자연어 83행 | 55 일치, 0 실행 오류 | 82개 고유 입력, 중복 행은 라벨 단위로 보존 |
| A focus 28 | 1 일치 | 개발 fixture 상대 결과 |
| A 방어 control 16 | 16 일치 | 개발 fixture 상대 결과 |
| A의 원래 실행과 현재 재생 | 147행 중 상태 차이 0 | 기존 결정론 기준선 재현 |
| B live | 0 요청, 0 Claim | `LIVE_NOT_RUN`; 모델명 없음 |
| C live | 0 추가 요청 | `LIVE_NOT_RUN`; B 추출을 재사용하도록 구성 |

live 결과가 없으므로 잘못 추출된 Claim 수, B/C 보류율, false-support/false-contradiction 및 응답 일치도는 **측정 불가**다. 요청/응답 토큰 0, 호출 비용 `$0`, 요청 응답시간 해당 없음은 실제 미호출 결과이며 모델 단가 성능값이 아니다.

## B8L 구현 및 방어

- 선택된 12개 사례와 6개 기존 관계 매핑, 공개 fixture hash를 사전 검증한다. provider payload는 질문, 답안, Topic 및 기존 허용 어휘만 포함하며 case ID, 기대 판정/Claim, target Fact, requirement state와 점수 정보는 전달하지 않는다.
- Gemini transport는 요청 1회당 raw response SHA-256, usage metadata token 수, latency를 수집한다. Claim 추출 응답 출력은 최대 2,048 token으로 제한한다.
- `P2B8_APPROVED_BUDGET_USD`를 총 상한으로 사용하고 model별 input/output 단가가 추가 제공되어야 한다. UTF-8 요청 크기와 출력 상한을 이용한 최대 비용 예약을 호출 전에 검사한다. 다음 요청이 예산을 넘길 수 있으면 네트워크 호출 전에 중단한다. 결과 비용은 provider usage 기준과 보수적 예약 대체값을 분리한다.
- B의 동일 응답은 C에서 재사용해 추가 호출을 하지 않는다. C는 A의 유효 unresolved span 안에서만 보완하고, 불완전 A 조각과 중복 관계를 구분한다. unresolved 밖의 A 관계를 교체하지 않는다.
- 검증 가능한 연산자 불일치는 fidelity `FAIL`로 유지된다. GEN-09 모의 추가↔곱 왜곡은 `FAIL`/grounded `RECOGNITION_UNCERTAIN`. GEN-26의 모의 raw 관계 후보는 semantic fidelity가 입증되지 않아 grounded 보류. 이는 모의 계약 시험이지 LLM 결과가 아니다. 미검증 자연어에 대해 새 `PASS` 경로를 만들지 않았다.
- B8L은 `score_admission=DISABLED`, `score_effect=none`을 출력한다.
- 재생 JSON SHA-256: `b5399afd645f2f9bd65e4311eac6adff96db6b2dda144cfa21f6e296849b7c9f`; JSON에는 실행 HEAD, 두 계약 해시, fixture 입력 해시와 코드 파일 해시를 기록했다.

## 보호 답안 143건

보호 답안 입력과 원래 재생 명령은 복구되지 않아 replay는 `NOT_RUN`이다. 확인된 `answer_candidates.json` 첨부는 메타데이터상 9개 사례여서 143건 replay 입력으로 사용할 수 없었다. 개인 답안 내용은 출력하거나 외부 provider에 전송하지 않았다. 저장소의 과거 “143건 변경 0” 기록은 이번 SHA의 replay 증거로 재사용하지 않았다.

## 테스트와 게이트

- Focused: `python3 -B -m pytest -q tests/test_p2b_b8_llm_claim_extractor.py tests/test_audit_relation_recognition.py tests/test_canonical_grading_evidence.py` — **52 passed**.
- B8L 전체 회귀: 기존 64 구조화 + 83 자연어행(47+36), focus 28, controls 16을 같은 runner에서 재생, 실행 오류 0; 원본 기준 대비 A 상태 차이 0.
- 추가 방어: 예산 부족 시 transport 호출 0, fixture hash/6 관계 균형, labels/case ID payload 제외, B response cache, C의 mention/incomplete A supplement, GEN-09 fidelity FAIL 보존.
- `python3 -B scripts/rubric_manager.py validate-all` — PASS (`ALL VALID`).
- `python3 -B scripts/check_generated_rubrics_freshness.py` — PASS (6 Generated files match clean rebuild).
- `python3 -B scripts/rubric_manager.py validate-topic-pack-release --all` — PASS (89 Topic Packs / 2,096 anchors; Generated pipeline and quality PASS; smoke was SKIPPED by verifier; generated snapshots restored; worktree clean).
- `PROMOTE_GENERATED=0 scripts/validate_release.sh` with live API disabled — exit code **0**. The script completed its release checks; full counted pytest evidence below is from the RC manifest.
- `VALIDATION_LIVE_API=0 QUALITATIVE_DE_MODE=off PROMOTE_GENERATED=0 python3 -B scripts/release_candidate.py validate` — PASS on implementation commit `d82220a9b8b72e5e238e2108df7456f05ed3d0f4`: **1,735 passed, 2 skipped**, 0 failed; manifest `reports/release_candidates/20261126T022833Z_d82220a9b8b7_pytest/manifest.json` (SHA-256 `1e2bc5298d58d62a8c278b011341e807992e2ab7aecffddd0bcbedb8d81273ed`).
- A prior attempted `python3 scripts/validate_release.sh` was an invocation error (Python syntax error); it was rerun correctly through the shell and exited 0.

The final evidence tree is separately Release Candidate-validated and manually dispatched through GitHub Actions; the exact final SHA, manifest and run URL are recorded in Issue #40 and Draft PR #49. Release evidence from earlier SHAs is not reused as final-SHA evidence.

## 결론 및 미완료

B8L 파일럿 경로와 기록 기능은 구현·모의 방어시험을 통과했지만 실제 LLM 비교는 미실행이다. 이는 P2-B8L의 실제 성능 검증 완료가 아니다. 실제 사용에는 전용 검증 키, 정확한 모델, 명시 승인 예산 및 해당 모델의 승인된 input/output 단가 설정이 필요하다. 143 보호 답안 clean replay도 비공개 입력/명령을 확보할 때까지 보류한다. 독립 의미 정확도 `NOT_ESTABLISHED`; P2-B 전체는 미완료; B9/B10 및 보호 답안 replay 전 P2-C 진입 금지다.
