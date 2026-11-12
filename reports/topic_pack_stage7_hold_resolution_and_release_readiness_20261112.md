# Stage 7 — 잔여 HOLD 해소 및 Generated Release 준비

- 일자: 2026-11-12
- 저장소: `/home/now0930/hermes/workspace/prof_eng_answer`
- 브랜치: `codex/topic-pack-evidence-policy-20261111`
- 시작 HEAD: `8827219d1356da9b055cf8c9f5777c01a465dc52`
- 기준 보고서: Stage 3·4·5·6; 전체 55 Anchor, 그중 Stage 6 검토 HOLD 11
- Promote/deploy/commit/push: 수행 안 함

## 요약

Stage 6에서 HOLD라고 분류한 11개를 기술 정확성, 기존 승인 근거, 일반 채점 적용범위로 나누어 대조했다. 9건은 이미 승인·검증된 Registry Fact와 제한된 Canonical 문구로 기술 근거가 확인됐다. #33은 기술적으로 확인됐고 기존 duplicate exclusion이 실제 runtime 경로에서 작동한다. #19는 현재 Canonical의 모든 reset 조건을 뒷받침할 직접 source와 Registry Fact가 없다. #51은 좁은 approved Registry Fact와 더 넓은 Canonical/promotion review 범위가 맞지 않아 변경을 보류했다.

기술적으로 승인된 #12의 Registry 정의에 맞춰 Canonical, Logic Check, Model Answer를 한 번 수정했다. 공식 promotion builder로 기존 Bode Topic source hash 한 건을 다시 계산했다. 기존 104개 promotion ID, Fact statement hash, source review와 authorities는 유지됐다. Generated Builder는 격리된 임시 디렉터리에서 6개 projection을 만들었고, 내용 차이는 기존 #24 수정과 새 #12 수정 및 파생 content-version metadata뿐이었다. 실제 Generated Bank는 바꾸지 않았다.

## 1. Git 기준선 및 변경 보호

작업 시작 시 branch는 지정한 `codex/topic-pack-evidence-policy-20261111`, HEAD는 위 값, unmerged index는 0이었다. 아래 staged·unstaged·untracked 변경은 시작 시 존재했고 보존했다.

- 기존 staged/unstaged: `docs/private_runtime_backup.md`, `docs/topic_pack_workflow.md`, cavitation Topic Sheet, Master JSON, Stage 5 promotion review JSON, 80-row review CSV, cavitation Canonical 3파일, workflow/tool/test 파일
- 기존 untracked: Stage 2 ZIP 및 Stage 3~6 보고서, concision 감사, private-backup 스크립트
- Stage 7 변경: Bode `fact_anchor.json`, `logic_check.json`, `model_answer.json`; 공식 Builder를 통한 promotion artifact source hash 1행; 본 보고서
- `rubrics/generated/` runtime file 변경: 0

사용자 변경을 reset/clean하거나 stage하지 않았다. commit, push, 운영 bot 변경·재시작도 하지 않았다.

## 2. HOLD 11건별 판정

파일 필드 위치는 각 `rubrics/topic_packs/{topic_id}/fact_anchor.json#/anchors[anchor_id]`다. “KEEP_BOUNDED”는 기술적으로 확인되어 현행 조건을 유지한다는 뜻이며, 이 보고서에서 새 promotion/점수 가산을 했다는 뜻이 아니다. Registry는 총 1,524개 Fact를 검증했으며, 아래 중 10개 ID는 이미 `review_status=approved`, `verification_status=verified`, `score_effect=none` 기록을 갖고 있었다. #19는 Registry Fact가 없다.

| # / Anchor | 기술 정확성 및 source | 채점 적격성 / 중복 | 최종 HOLD 처리 및 변경 |
|---:|---|---|---|
| 1 `acl_calibrator_isolation_workflow` | Fluke 725Ex 매뉴얼과 Fluke mode 설명은 source/measure/simulate의 전원·결선 차이를 지지한다. Canonical도 실제 calibrator 모드·외부 loop supply 확인으로 제한돼 있다. Registry approved/verified. | calibrator 운영 절차이며 특정 기기/단자에 적용할 때 제조사 지침을 따라야 함. 별도 Fact/score group 추가 없음. | **기술 HOLD 해소: KEEP_BOUNDED.** Canonical 유지; 신규 promotion 없음. |
| 6 `residual_effective_area` | `Fᵣ=ΔP·Aᵣ`는 정압차와 유효 투영면적의 힘 관계. Emerson/Fisher Handbook와 `F=pA` 유도가 이를 지지한다. `Aᵣ`는 제조사 구조에 의존한다. Registry approved/verified. | 면적을 보편 상수로 취급하지 않는 현재 문구가 핵심 조건. 기존 balanced-trim owner 유지. | **기술 HOLD 해소: KEEP_BOUNDED.** 수식·단위조건·제조사 한정 유지. |
| 9 `open_loop_closed_loop_roles` | 음의 단위가 아닌 scalar feedback에서 `L=GH`, `T=G/(1+GH)`; `L/(1+L)`은 `H=1`인 특수 경우다. Registry에 명시적 블록도 대수 유도/승인 기록이 있으며 Anchor가 일치한다. | 일반 제어공학 원리; 기존 Bode owner. 점수 가중치나 새 scoring group 없음. | **기술 HOLD 해소: KEEP.** 추가 서류나 외부 표준 승인 없이 기존 승인 Fact와 계산 근거 사용. |
| 10 `pole_zero_magnitude_slopes` | 1차 LHP zero/pole의 점근 크기기울기 ±20 dB/dec이며 중복 차수는 누적한다. Registry에 20log₁₀(10)=20 dB/dec 유도가 승인돼 있고 Anchor의 LHP 조건과 일치한다. | 원점 요소/절점 이후 적용 범위를 구분; 기존 owner/weight 그대로. | **기술 HOLD 해소: KEEP.** 추가 promotion 없음. |
| 12 `closed_loop_bandwidth` | MathWorks 정의는 low-pass 응답에서 DC gain 대비 70.79%까지 떨어지는 첫 주파수(−3 dB). Registry에는 정확한 `1/√2` 반전력 관계, 유한·비영 DC 크기 및 첫 주파수 조건이 approved/verified로 있다. | `T(s)`의 폐루프 상대 대역폭으로, 개루프 `ω_gc`와 항등적으로 같지 않다. 기존 Bode owner, 점수 구조 불변. | **기술 HOLD 해소 및 Canonical 수정 1건.** 전후 문구는 §3. 신규 Fact approval/promotion 없음. |
| 19 `sw02_trip_latch_reset` | 기존 source는 “일반 산업 제어공학”뿐이며 Registry Fact가 없다. HSE 기계안전 지침은 비상정지 reset은 수동으로 하고 이후 정상 조작부로 재기동한다고 안내한다. 이 자료는 기계 emergency-stop 문맥을 지지하지만 모든 공정 trip의 원인 제거, 조작권한, “Reset edge”를 보편 필수조건으로 입증하지 않는다. | 현재 문장의 전 조건을 일반적인 채점 기준으로 적용할 source 범위 부족. 별도 Fact/owner 없음. | **HOLD 유지.** Canonical/Logic을 억지로 확장 승인하지 않음. HSE 기계안전 한정 수정 또는 공정 SIS/시퀀스 원문과 독립 검토가 필요. |
| 29 `large_step_test_pneumatic_capacity` | Emerson/Fisher Handbook 6판 및 IEC 60534-9의 step test 범위는 지정한 100% step 입력과 방향에서 assembly의 full travel 완료시간을 재는 것이다. 결과만으로 공압 고장이나 small-signal 동특성을 단정하지 않는 조건이 Canonical/Registry에 있다. | 측정 정의는 보편적으로 설명 가능; 수치 합격시간·모든 시운전에 시험 의무를 부과하지 않음. | **기술 HOLD 해소: KEEP_BOUNDED.** 기존 검토된 Registry Fact와 문구 유지. |
| 33 `pressure_ratio_direction` | 정의 `x=ΔP/P₁`, P₁ 고정·절대압 기준에서 P₂ 감소 시 x 증가. Emerson sizing 문서 및 계산식에 맞고 Registry approved/verified. | 기존 `duplicate_scoring_requirement` exclusion이 활성 적용됨. 반복 점수요건으로 다시 가산하지 않음. | **HOLD를 기존 일반채점 제외로 종결.** exclusion/Anchor 삭제 변경 없음. |
| 40 `selection_environment_process` | Vaisala 공식 자료는 요구 습도량·범위, 온도·압력, 응축·오염·설치·응답 조건을 기기 model limits와 대조하고 단일 기기가 모든 application에 맞지 않는다고 한다. Registry approved/verified. | 현재 Canonical은 구체 정격을 model-specific으로 제한하고 hazardous-area certification도 별도 적용기준으로 확인한다. | **기술 HOLD 해소: KEEP_BOUNDED.** 제조사 한계를 보편 수치로 바꾸지 않음. |
| 51 `operations_moc_revalidation` | HSE COMAH C&I 지침은 해당 assessment context에서 SIS 정비, proof-test 주기 근거, SIS modification 절차의 입증을 요구한다. 하지만 Registry statement는 “모든 trend field가 보편 mandatory log item은 아니다”라고 한정한다. Canonical에는 광범위한 항목 기록 및 공정·위험·주기·부품·software 변경 전부의 MOC가 적혀 있다. | 기존 104 promotion ledger에는 이 Fact가 포함되고, 별도의 source-review 보고서는 현재 넓은 Canonical 문구를 `KEEP_BOUNDED`로 pin한다. Registry의 좁은 approved statement와 충돌한다. 현재 `excluded_from_scoring`은 false다. | **HOLD 유지.** Canonical 또는 승인 기록을 임의로 덮어쓰면 안 된다. HSE 적용범위에 맞춘 새 source review, 관련 approval/statement hash의 정식 갱신 및 기존 pin 영향 검토가 필요. 현 pin/approval은 수정하지 않음. |
| 52 `proximity_airgap_target_error` | ifm의 target·sensing distance 자료와 installation guide, Allegro gear sensor 자료가 target 재질·기하·operating gap에 따른 detection margin 변화의 bounded relation을 지지한다. Registry approved/verified. | Canonical은 inductive gear-tooth application 및 제조사 assured range로 제한하고 보편 dropout threshold를 만들지 않는다. | **기술 HOLD 해소: KEEP_BOUNDED.** 특정 제품 수치·한계를 추가하지 않음. |

### HOLD 처리 집계

- 최초 report HOLD: 11
- 기술 HOLD를 기존 승인 근거로 해소하고 KEEP_BOUNDED/KEEP: 8건 (#1, #6, #9, #10, #12, #29, #40, #52)
- 기존 duplicate exclusion으로 처리: 1건 (#33)
- 계속 HOLD: 2건 (#19 source scope 없음, #51 Canonical/Registry/promotion scope 불일치)
- 신규 공식 Fact 승인: 0
- 신규 scoring promotion: 0
- #12 Canonical 수정: 1

이것은 Stage 6 문서상 처분의 재평가다. Registry의 `score_effect=none`, 기존 Fact IDs, weights, Score Groups, Fatal Rules 및 Golden을 변경하지 않았다. #24의 기존 runtime revision hold는 그대로 활성이고, #33 duplicate exclusion도 활성임을 `excluded_from_scoring()`로 확인했다. 나머지 Stage 6 HOLD 분류는 당시 report 상태였고 전부 active overlay에 실려 있던 것은 아니다. #19와 #51을 기존 runtime overlay에 추가하지 않았으므로 이 두 Canonical은 runtime exclusion으로 차단되지 않는다. 특히 #51은 기존 104 promotion과 충돌하는 신규 hold를 덧씌우지 않고, 승인을 손상시키지 않는 정식 amendment가 없다는 잔여 차단 사유로 보고한다.

## 3. Canonical 반영 — #12

`fact_anchor.json`의 `statement` 및 `accepted_explanations`, `logic_check.json`의 `truth_schema` 항목, `model_answer.json`의 패턴 4 고득점 설명을 같은 저역통과 정의로 맞췄다.

**변경 전**

> 일반적인 저역통과형 폐루프 시스템의 대역폭은 `|T(jω_BW)|=|T(0)|/√2`가 되는 상대 −3.0103 dB 주파수로 정의한다.

**변경 후**

> 저역통과형 폐루프 응답의 정확한 반전력 대역폭 `ω_BW`는 DC 크기가 유한하고 0이 아닐 때 `|T(jω_BW)|=|T(0)|/√2`가 되는 첫 주파수이다(−3.0103 dB).

이는 이미 승인된 Registry Fact와 일치하며 다중 교차에서 첫 교차를 분명히 한다. 수식의 단위 없는 비, DC 기준, 저역통과 조건 및 `ω_gc`와의 구분을 보존했다. 신규 formal approval은 만들지 않았다.

## 4. Legacy 승인 및 Source Hash

- `approved_fact_registry.py`는 Registry 형식, delegated approval provenance, 각 Fact의 `approved`/`verified`, source locator 및 Master 연결을 검증한다. Registry 데이터에 대한 신규 승인/수정은 없었다.
- `promote_reviewed_fact_anchors.py`의 default check는 104 IDs·statement/source-review 조건은 유지했지만 #12 수정으로 Bode Topic file hash가 바뀌어 최초 check는 exit 1이었다.
- deterministic builder의 old/new 결과를 비교한 뒤 기존 공식 `--write` 경로를 실행했다. 결과: `canonical_promotions=104 mode=write`, 재검사 `canonical_promotions=104 mode=check` (exit 0).
- 바뀐 ledger row는 기존 `bode_decibel_and_log_frequency_properties` 1개다. `statement_sha256`, Fact ID, Anchor/Topic, source review, authorities는 동일하고 전체 Bode Topic source hash만 `6102678627bd33170a695d5bab119b575a53338bcf860ad7f5d8a57ad886e7d4`에서 `a647d5bad2d73a100d832f00d3739424b55d213a770aeb79cf7dd66bc94a09df`로 갱신됐다. 이는 승인 재작성이나 새 Fact promotion이 아니라 기존 source pin을 현재 Canonical과 다시 결속한 공식 builder 결과다.
- #51의 기존 promotion entry와 source review는 변경하지 않았다. 해당 row가 broader Anchor text를 pin하고 있어 Registry의 narrow Fact와 scope를 조정하려면 source review/approval에 대한 별도의 실제 재검토가 필요하다.

## 5. 임시 Generated Build와 비교

공식 `build_generated_rubrics`를 Python temporary directory로 redirect하여 빌드했다. 기존 `rubrics/generated/` 파일을 쓰지 않았으며, builder의 freshness helper와 byte comparison을 이용했다. 기존 generated version은 `sha256-1320c4ce20f2d4b9060071c23f78c8c7282b65868f87adda47eaf0411d550904`; 현재 Canonical 예상 version은 `sha256-82a18d562b116491ab950e3b5ce55397559c04a12fee688604d2acaf7563a829`다.

| 파일 | 차이 분류 | 현재 stale | 예상 내용 |
|---|---|---:|---|
| `fact_anchors.generated.json` | Anchor content + 파생 trigger text + version | 예 | #24의 `P₂<Pᵥ` 및 포화 경계 수정, #12의 DC 대비 첫 반전력 주파수 정의, 전체 version 변경 |
| `model_answers.generated.json` | 고득점 설명 + version | 예 | 기존 #24 답안 정정과 #12 패턴 4의 first `1/√2` crossing 설명, version 변경 |
| `topic_importance.generated.json` | version metadata만 | 예 | Topic importance 값 변화 없음 |
| `logic_checks.generated.json` | version metadata만 | 예 | 이 projection의 실질 필드 변화 없음 |
| `logic_check_profiles.generated.json` | logic/truth content + version | 예 | Bode #12 truth schema; cavitation #24 truth/fatal/safe condition; version 변경 |
| `topic_pack_manifest.generated.json` | version metadata만 | 예 | Topic 목록·개별 ID 추가/삭제 없이 version 변경 |

임시 생성본에서 #24 Canonical 사실은 `P₂<Pᵥ`, `P₂=Pᵥ` 경계 구분으로 표시됐다. active revision overlay는 generated bank와 별도이며 `excluded_from_scoring(topic_id, anchor_id, fact_id)`에서 #24가 `True`인 것을 확인했다. 따라서 #24는 정정 문구가 생성될 예정이어도 revision hold가 해제되거나 scoring 승격되었다고 볼 수 없다. #33 duplicate exclusion 역시 `True`였다. 나머지 11 HOLD 대상 중 #19/#51은 현재 runtime exclusion 함수가 `False`를 반환하는 점을 release risk로 명시한다.

비교에서 예상하지 못한 다른 Topic/Score ID, weight, Fatal Rule, importance value 변경은 발견하지 않았다. 버전 문자열 외 metadata는 변경되지 않았다. 실제 promote는 하지 않았으므로 위 내용은 임시 산출물 예측이다.

## 6. 검증 결과

| 검증 | Stage 7 실제 결과 |
|---|---|
| `scripts/audit_topic_pack_content.py` | PASS; 89 topics, 89 masters, 767 questions, 2,096 anchors; exit 0 |
| `python3 scripts/rubric_manager.py validate-all` | ALL VALID; Topic Pack/Registry 관련 validator PASS |
| `scripts/validate_master_topic_packs.py` | PASS; 89 packs |
| promotion ledger check | PASS; 104 entries; ID와 statement hash 보존 |
| runtime exclusion 확인 | #24 revision hold `True`, #33 duplicate exclusion `True`; #19/#51 active exclusion `False` |
| 전체 오프라인 pytest | **1,620 passed / 0 failed / 1 skipped**, exit 0, 394.56초 |
| freshness helper | FAIL/exit 1; 6개 Generated output이 현재 Canonical과 다름 |
| non-promote Release Gate | `PROMOTE_GENERATED=0 RUN_SMOKE_TOPIC_PACKS=0 RUN_GRADING_REPRODUCIBILITY=0 scripts/validate_release.sh`; **exit 1**. 하위 freshness test 2개 실패; 두 테스트 모두 6개 stale 파일 불일치를 검출 |
| `git diff --check` | 통과. 본 untracked 보고서는 별도 whitespace scan 0개 오류 |

Freshness 테스트는 기존 운영 Projection이 source와 다르다는 실제 불일치를 정확히 검출했다. 이를 약화하거나 제거하지 않았다. 전체 pytest 결과는 Stage 7에서 새로 실행한 결과이며 Stage 5 기준선과 일치한다.

## 7. Release 준비 및 다음 절차

현재 상태는 **Generated release 준비 완료, 실제 Generated Bank 동기화 전, Release Gate FAIL**이다. 기술 수정과 검증은 끝났으나 현재 runtime bank는 기존 버전이다. 이 단계의 명시적 제한 때문에 promote하지 않았다.

실제 promote를 승인받은 후 적용할 절차:

1. promote 직전 현재 6개 `rubrics/generated/*.json`과 promotion ledger를 별도 backup에 복사하고 hash를 기록한다. 기존 staged/unstaged 사용자 변경을 Git restore로 덮지 않는다.
2. `python3 scripts/rubric_manager.py validate-topic-pack-release --all --promote-generated`의 공식 transaction으로만 생성 projection을 반영한다.
3. 이 보고서의 임시 diff 기대치와 실제 diff를 비교한다. #24/#12, 해당 Logic/Profile/Answer 및 version/hash 외 변경이 있으면 배포 중지.
4. `python3 scripts/promote_reviewed_fact_anchors.py`, `python3 scripts/rubric_manager.py validate-all`, Master/Topic projection validators, 전체 오프라인 pytest, freshness helper 및 non-promote Release Gate를 다시 실행한다. freshness가 pass해도 `#19/#51` active overlay 상태는 별도 승인/정리 전에는 변경하지 않는다.
5. 실패 시 백업한 6개 generated 파일만 정확히 복구하고, hash·freshness를 재검증한다. Canonical이나 다른 staged 파일을 통째로 checkout/reset하지 않는다. 복구된 이전 bank는 Canonical과 stale이므로 Release Gate는 FAIL로 유지한다.

이번 Stage 7에서는 1–5의 실제 Promote 및 rollback이 필요하지 않아 수행하지 않았다. 운영 배포, 운영 Bot 변경, commit, push도 수행하지 않았다.
