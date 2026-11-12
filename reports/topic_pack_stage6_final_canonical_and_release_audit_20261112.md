# Stage 6 — Fact Anchor 잔여 개선 및 Release Gate 감사

- 검토일: 2026-11-12
- 저장소: `/home/now0930/hermes/workspace/prof_eng_answer`
- 브랜치: `codex/topic-pack-evidence-policy-20261111`
- 기준: Stage 3·4·5 보고서 및 현재 Topic Pack Canonical, Registry, overlays, 생성기 계약
- 범위: 기존 검토 55개 Anchor. Fact Pack/Generated Bank/운영 데이터는 수정하지 않음.

## 결론 및 건수

Stage 5의 55건 분류를 모두 다시 대조하고 잔여 23개 수정 권고 및 11개 보류를 개별 재판정했다. 기존 Stage 5의 #24 조건 교정은 Canonical에 반영된 사실로 계승하며 재수정하지 않았다. 이번 단계에서 신규 Canonical 수정은 0건이다. 확인한 기술 권고 대부분은 현재 문구에 이미 적용되어 있거나, 보편적 채점 사실로 만들기에는 출처 적용범위·source hash·승인 pin이 부족하다. 안전한 추가 문구 변경이나 점수 권한 변경은 하지 않았다.

| 결과 | 건수 | 해석 |
|---|---:|---|
| 검토 대상 | 55 | Stage 2 CSV와 기존 inventory의 고유 Topic/Anchor |
| 기술 검토 완료 | 55 | Stage 3/4/5 개별 검토 계승; Stage 6에서 보완 원문 확인한 항목은 아래 표기 |
| Stage 5 기준 분류 | 유지 18 / 수정권고 24 / 제외 2 / 보류 11 | 이전 단계의 55건 시작 분류 |
| 최종 KEEP 또는 SIMPLIFY, Canonical 변경 없이 유지 | 41 | 기존 유지 18 + 잔여 권고 중 유지 22 + 기존 hold #50의 bounded 유지 판정 |
| 실제 Canonical 수정 | 1 | Stage 5 #24 조건 수정; Stage 6 신규 0 |
| 일반 채점 제외 | 2 | 기존 제외 2건; overlay 유지, Anchor 삭제 없음 |
| 최종 HOLD | 11 | 기존 hold 10건 유지 + #51 권고 건을 scope/hash 충돌로 hold; #50은 bounded 유지로 재판정 |
| 신규 Canonical 수정 | 0 | 이번 단계에서 추가한 수정 없음 |
| 신규 공식 Fact 승인 | 0 | 기술 확인을 승인/배포 승인으로 간주하지 않음 |
| Canonical 반영(누계) | 1 | Stage 5 #24 `P₂<Pᵥ`; Stage 6 신규 0 |
| Generated Bank 동기화 | 0 | 6개 stale projection은 의도적으로 미-promote 상태 |
| 운영 배포 | 0 | 수행하지 않음 |

처분표의 KEEP/SIMPLIFY/SPLIT/MOVE_PRIVATE/MERGE_CANDIDATE/HOLD는 기술 콘텐츠 권고다. `유지`는 Fact를 채점 승인했다는 뜻이 아니다. 이 작업은 개인별 오개념·학습 기록을 발견하거나 보고서로 옮기지 않았다. 기존 공개 Topic 내용에 개인 학습 정보가 없음을 개인별 기록 검토로 주장하지 않는다.

## 1. 기준선 및 보호 상태

브랜치는 지정 브랜치를 유지했다. 작업 시작 시 staged·unstaged·untracked 변경이 있었고, 이를 원상복구·정리·덮어쓰기하지 않았다. 기존 Stage 5의 `approve-topic --approval-only`, cavitation Topic 변경, private-backup 도구 및 보고서 파일을 사용자 변경으로 보존했다. Git unmerged index 항목은 0이었다. 이 감사에서 `git add`, reset, clean, commit, push, generated promote 및 운영 배포는 수행하지 않았다.

Stage 5에서 실행된 전체 pytest의 실제 결과는 **1,620 passed / 0 failed / 1 skipped**였다. 이번 단계는 코드·채점 동작을 변경하지 않았으므로 전체 pytest를 불필요하게 반복하지 않았다. 아래에서 Stage 6에서 새로 실행한 감사 결과와 Stage 5의 재사용 결과를 구분한다.

## 2. 잔여 수정 권고 23건 재판정

세부 경로는 `rubrics/topic_packs/{topic_id}/fact_anchor.json`의 `anchors[anchor_id]`이며, 같은 anchor의 `logic_check.json`, `model_answer.json`은 별도 필드/점수 owner 변경이 필요한 경우에만 동기화 대상이다. 각 행의 원문은 변경하지 않았으므로 현재 Canonical 원문을 그대로 최종 문구로 유지한다. Stage 3/4/5 보고서에는 행별 원문 및 이전 권고가 보존되어 있다.

| # / Anchor | 기술 검토와 현재 문구 판단 | 기존 채점·참조 영향 | Stage 6 판정 및 제안 | 추가 필요 |
|---:|---|---|---|---|
| 11 `gain_phase_crossover_frequencies` | 현재 정의는 `|L(jω_gc)|=1` 및 위상 `−(2k+1)180°`; 두 교차 조건을 구분한다. 다중 교차 가능성을 배제하는 표현은 확인되지 않음. MathWorks `margin` 정의와 다중 교차 취급을 대조했다. | 기존 Bode Topic owner; 새 score group 없음. | **KEEP** — 기존 문구 유지. 유일 교차 가정/추가 점수 항목을 넣지 않음. | 없음 |
| 13 `sw06_impact_analysis_multidisciplinary` | NIST SP 800-82 Rev.3의 OT 변경 영향 검토 및 OSHA PSM MOC의 covered-process 범위가 근거. 기존 권고의 적용 범위 한정 유지. | configuration Topic의 기존 owner; 특정 관할 규정의 보편 승격 금지. | **KEEP** — 현재 조건부 guidance 유지; 법적 보편 의무로 확대하지 않음. | 공식 PDF hash를 Topic source record에 결속하려면 정식 source review 필요. |
| 14 `sw06_change_implementation_plan` | 변경 계획·기록·시험은 위험 기반; OSHA PSM 요구는 적용 대상 공정 한정. | 기존 owner, 고정된 보편 시험목록 추가 없음. | **KEEP** — 기존 조건부 문구 유지. | 동일 source-hash 결속 필요. |
| 15 `sw06_risk_based_regression` | NIST는 변경 영향에 맞춘 검증을 지지하나 모든 변경에 같은 회귀시험 세트를 요구하지 않는다. | 기존 owner; 점수 중복 없음. | **KEEP** — 고정 시험 집합을 만들지 않고 risk-based 조건 보존. | 동일 source-hash 결속 필요. |
| 16 `sw06_backup_scope_and_consistency` | NIST SP 800-82 Rev.3 및 2026년 SP 1339의 자산 중요도·백업·복구 관점과 합치. 주기·대상은 자산 및 위험에 좌우됨. | 기존 configuration/maintenance 참조; 배포·복구 조건 영향 없음. | **KEEP** — 현재 범위 유지, 모든 자산에 동일 주기 강제하지 않음. | NIST 원문 hash를 source ledger에 고정하는 별도 검토. |
| 17 `sw06_migration_discovery_dependency_inventory` | OT asset/configuration inventory는 기준선으로 유효; 모든 종속성의 완전 목록 보장은 일반 원칙으로 도출되지 않음. | 기존 owner; 새로운 무조건 완전성 요구는 scoring 중복 위험. | **KEEP** — 현재 Canonical이 site-specific 추가조사와 NIST inventory를 이미 분리한다. 더 줄이면 적용 경계가 사라짐. | 없음; source hash 기록은 별도 절차. |
| 18 `sw02_transition_guard` | Stage 5에서 검증한 대표 command-based SFC guard 식이며 자동·시간·process-condition 전이 예외도 인정한다. | 기존 sequence logic owner; 승인된 registry 사실의 문구와 정합. | **KEEP** — 기존 bounded 문구 유지. | 없음 |
| 26 `control_valve_commissioning_characteristic_verification` | Stage 5에서 검증한 현장 특성 확인의 적용 범위는 측정된 설치 특성/평가이며 모든 밸브에 전 특성시험을 강제하지 않는다. | 기존 control-valve owner; Registry의 확인된 bounded statement와 정합. | **KEEP** — 조건부 field verification 유지. | 없음 |
| 28 `stiction_limit_cycle_path` | Stiction이 limit cycle로 이어질 수 있으나 마찰·공정·제어기·구동기 동특성에 의존한다. | 기존 deadband/stiction topic; 별도 필수점수 분할 불필요. | **KEEP** — 가능성/조건부 인과로 유지. | 없음 |
| 37 `eem_auto_zero_ratiometric` | Autozero/chopper는 offset·drift를 낮출 수 있지만 ripple/glitch 및 bandwidth tradeoff가 있고, ratiometric cancellation은 excitation/reference의 비율 관계가 맞을 때 성립한다. | 기존 electronics owner; 검토된 Registry fact와 일치하며 별도 score owner 없음. | **KEEP** — 기술 수단과 적용 조건 유지. | 검토된 source records 유지; 새로운 승격 불필요. |
| 38 `eem_layout_local_mitigation` | return-current 경로/배치가 noise에 영향을 주며 ground split은 보편 처방이 아니다. | 기존 electronics owner; 일반 layout 요구와 중복 점수 위험 없음. | **KEEP** — topology-specific 예외 유지. | 없음 |
| 39 `fsrm_markov_state_transition` | Markov 전이율 모델은 상태 정의 및 시간/무기억 가정에 종속된다. | 기존 reliability owner; 가정 밖 적용은 부정확한 해석 위험. | **KEEP** — 현재 조건을 유지하고 분할하지 않음. | 수치 검증 문제를 추가할 경우 별도 scoring contract 필요. |
| 41 `lead_lag_implementation_validation` | 구현 검증은 요구사항, 모델 및 실제 구현에 의존. 특정 도구/시험 절차를 보편화할 근거 없음. | 기존 lead-lag owner; 기존 점수 권한/weight 불변. | **KEEP** — 요구사항 기반 범위 유지. | 없음 |
| 42 `state_lqr_tracking_prefilter_lqi` | LQR 오차좌표/추종, prefilter 및 LQI 적분 동작의 서로 다른 조건을 유지해야 함. prefilter는 robust zero 보장이 아니고 LQI에는 안정화 가능성과 windup 고려가 필요하다. | 기존 LQR owner; 개념을 분할 가산하지 않음. | **KEEP** — 현재 조건과 한계 유지, 추가 축약 시 필수 구분이 손실될 수 있음. | 방정식/구현 예제를 채점화할 때 독립 검토 필요. |
| 44 `alignment_occlusion_geometry` | 삼각측량은 송·수광 광선과 설치 기준선/가림에 종속된다. | 기존 optical owner; 범용 센서 적격성 유지. | **KEEP** — geometry 및 occlusion 조건 보존. | 없음 |
| 45 `tof_timing_jitter_resolution` | 직접 ToF의 거리 관계는 `R=cδt/(2n)`이며 지연·jitter가 분해능/불확도에 들어간다. 광학 매질의 굴절률 조건을 유지. | 기존 optical owner; 정확한 단위·왕복 시간 factor 2 보존. | **KEEP** — 수식/조건을 축약하지 않음. | 제품별 사양은 source-specific 검토 필요. |
| 46 `multipath_mixed_pixel_error` | AMCW ToF 다중 경로/혼합 픽셀은 복수 반사 신호의 혼합으로 거리 오류를 낼 수 있다. Optica 논문과 제조사 자료 대조. | 기존 optical owner; 별도 점수 승격 없음. | **KEEP** — 가능성 표현을 유지, 모든 픽셀의 필연 오류로 일반화하지 않음. | 없음 |
| 48 `pid_line_list_spec_relation` | Line List는 프로젝트 산출물/도면·사양 연계에 유용하지만 범위와 필드가 프로젝트별로 달라 보편 단일 형식으로 정의할 수 없음. | 기존 P&ID topic; 기존 점수 owner를 넘지 않음. | **KEEP** — 현재 Canonical이 Line List 적용 여부를 프로젝트 설계 기준에 조건화하고 Autodesk 예를 비보편으로 표시한다. | 표준/프로젝트 명시 항목을 채점 요구로 넣을 때 근거 필요. |
| 49 `loop_interaction_coordination` | 다중 루프 결합은 공정/제어 구조에 따라 상호작용하며 강결합 MIMO 조건은 단일 SISO 규칙으로 축약할 수 없음. | 기존 process-control owner; score group 변경 없음. | **KEEP** — 현재 경계 유지. | 설계 대상이 특정되지 않은 수치 요구는 추가 검증 필요. |
| 51 `operations_moc_revalidation` | HSE COMAH guidance는 관련 사업자에게 SIS 정비, proof-test 주기 근거 및 modification 절차를 입증하도록 안내한다. 이는 보편 법령이 아니다. 현재 Canonical은 proof-test·bypass·demand·spurious trip 기록과 공정/위험/시험주기/부품/software 변경 시 MOC 및 필요한 경우 LOPA/SIL 재검토까지 묶어 HSE 근거보다 넓다. | `method_selection`과 함께 기존 SIS owner를 참조. 관련 Registry fact/promotion pin의 좁은 문구와 Canonical의 hash 일치 문제가 있어 자동으로 수정하면 기존 승인/해시 증거를 깨뜨릴 수 있음. | **HOLD** — 축약 제안은 HSE COMAH 지침의 범위로 한정하고, 사이트의 관리 절차/위험 영향에 따른 검토·재검증으로 표현. 이번에는 승인 pin/source review와 함께 갱신할 공식 경로가 확인되지 않아 Canonical을 수정하지 않음. | 독립 AI source review, Topic source hash 재결속, 기존 promotion record 처리 및 회귀 검증 필요. |
| 53 `state_tracking_implementation_validation` | 상태 feedback tracking의 구현 타당성은 모델, 좌표, reference path 및 구현 조건에 따름. | 기존 state-feedback owner; LQR Fact와 점수 이중계상 금지. | **KEEP** — 현재 범위 유지, 별도 owner/weight 만들지 않음. | 없음 |
| 54 `thermocouple_type_material_range_atmosphere_selection` | 열전대 형식 선택은 재료 조합, 온도 범위, 분위기 및 구성 한계에 달림. NIST의 형식/범위별 교정 맥락과 부합. | 기존 thermocouple owner; 특정 타입의 정확도/범위를 보편화하지 않음. | **KEEP** — 재료·범위·분위기 조건 보존. | 타입별 수치 정격을 추가하면 제조사/표준 확인 필요. |
| 55 `thermocouple_calibration_tolerance_uncertainty_drift` | 교정 불확도는 기준기/비교·고정점 방법, 반복성 및 적용 조건에 따라 예산화해야 하며 tolerance와 uncertainty는 같은 값이 아니다. NIST calibration 자료 대조. | 기존 thermocouple owner; 허용오차와 측정불확도 혼동 방지. | **KEEP** — 방법별 불확도와 tolerance 구분 유지. | 특정 정확도 수치는 추적 가능한 calibration certificate/표준 근거 필요. |

### 잔여 23건 전체 판정 요약

- 현재 Canonical은 Stage 3/4 권고의 기술적 제한을 이미 포함해 추가 수정하지 않은 항목이 다수다. Stage 5의 #24와 달리 새 수정이 필요한 기술 오류를 이번 근거로 확정하지 못했다.
- #51은 실제 scope 문제를 확인했으나 기존 promoted fact statement/hash와 Canonical 문구가 다르며, 독립 승인/기존 pin 업데이트 없이 고치면 source approval 계약을 우회하거나 깨뜨릴 수 있다. 따라서 수정 후보를 구체화하고 보류했다.
- 위 신규 검토는 기술 판단이다. 점수 owner, 일반 채점 가산, 승인 및 배포 상태를 바꾸지 않았다.

## 3. 기존 보류 11건 재판정

| # / Anchor | 기술 사실·채점 적격성·중복 판단 | 최종 상태 | 영향/다음 조건 |
|---:|---|---|---|
| 1 `acl_calibrator_isolation_workflow` | 교정기 전류 루프 연결/절연 확인은 타당하나 단자 구성·능동/수동 입력·제조사 절차에 종속. 범용 채점 정답으로 세부 절차화 불가. | **근거 부족으로 보류** | vendor/device setup을 일반 Anchor에 승격하지 않음. model-specific source와 적용 구성 필요. |
| 6 `residual_effective_area` | balanced trim 힘 평형은 유효 압력 면적과 trim/seat 형상에 의존. 기하가 주어지지 않은 단일 보편 residual-area 식은 부정확. | **근거 부족으로 보류** | 기하/압력 전달 경로를 확정하는 도면·제조사 원문 없이 scoring fact로 두지 않음. |
| 9 `open_loop_closed_loop_roles` | 선형 unity-feedback 관계 `T=G/(1+GH)`는 블록도 대수식으로 성립(분모/신호 정의 조건). 기술적으로 일반성이 충분하다. | **근거 부족으로 보류(채점)** | 기술식은 맞지만 Stage 3/4에서 확인한 독립 source/review hash 및 score pin이 없고, 이번에 그 승인 절차를 완료하지 않았다. 점수 admission 없음. |
| 10 `pole_zero_magnitude_slopes` | 실수 단순 pole/zero의 점근 Bode 크기 기울기는 각각 ±20 dB/decade, 주파수 decade 변화 기준이며 복합/중복 pole은 누적된다. | **근거 부족으로 보류(채점)** | 수학적 관계는 타당하나 공식 source/review hash와 scoring pin 미완료. 점수 admission 없음. |
| 12 `closed_loop_bandwidth` | 폐루프 저역통과 응답의 −3 dB bandwidth는 DC gain 대비 `1/√2` 크기 지점으로 정의할 수 있다. 임의의 응답/비단조 다중 교차에선 첫 교차 또는 정의된 band가 필요. MathWorks 공식 정의 대조. | **수정 후 유지 가능(기술)** | 제안: `저역통과 폐루프에서 DC gain의 1/√2가 되는 지정 교차주파수(다중 교차면 정의한 통과대역 기준)`으로 범위를 밝혀야 함. 이번엔 기존 approval/hash에 맞춘 source review가 없으므로 Canonical 수정과 점수 승격은 보류. |
| 19 `sw02_trip_latch_reset` | 래치 reset 조건·우선순위는 설계 요구, 위험분석, 장치/프로젝트별로 결정된다. 연결 Registry Fact 없음. | **근거 부족으로 보류** | 공통 reset 조건을 지어내지 않음; 안전 요구·cause/effect 근거 필요. |
| 29 `large_step_test_pneumatic_capacity` | pneumatic capacity/large-step 시험 결과는 actuator, supply, tubing, positioner, stroke/test criterion에 의존; 특정 표준/제품 시험 범위와 일반 scoring을 혼동하면 안 됨. | **근거 부족으로 보류** | 보편적인 합격시간이나 시험 의무를 두지 않음. 현재 Anchor 설명 보존. 기존 overlay 변경 없음. |
| 33 `pressure_ratio_direction` | 가스 밸브 압력비/임계비 방향은 절대압력과 제조사 sizing convention의 정의가 전제돼야 한다. Stage 5에서 duplicate-scoring concern이 기록됨. | **근거 부족으로 보류** | 55건 최종 분류는 기존 HOLD 11건을 보존. 이 처분으로 overlay/status를 변경하지 않음. |
| 40 `selection_environment_process` | 습도 센서 선택의 일반 변수는 측정 범위·환경·응답/유지관리이며 구체 측정원리·정격은 기기 한계에 종속. | **근거 부족으로 보류** | 현재 일반 원칙은 교육 설명에 둘 수 있으나 특정 센서 정답·정격 source review 전 score admission 없음. |
| 50 `method_selection` | SIL 결정에서 risk graph/LOPA 사용은 HSE 안내와 합치나 HSE 문맥/위험기준·IPL 가정에 의존. 기존 공식 promoted record가 이를 위험기반·방법별 범위로 한정함. | **유지 가능** | 이미 검토·승인된 좁은 Registry 문구 및 promotion pin만 유지. 신규 승인 없음; HSE guidance를 모든 관할의 의무로 만들지 않음. |
| 52 `proximity_airgap_target_error` | proximity speed sensor gap/target 형상은 sensing principle과 제품별 거리/재료 한계에 종속. 보편적인 air gap 정답 불가. | **근거 부족으로 보류** | 정확한 sensor family/target data sheet 없이 score admission 불가. |

보류 재판정은 기술 상태와 scoring state를 분리한다. #9/#10/#12의 원리는 기술적으로 타당해졌지만 그 사실만으로 Registry pin, allowlist, 일반 채점 점수 권한 또는 배포 승인을 추가하지 않았다. #12는 현재 문구가 다중 교차 응답을 충분히 명시하는지 source-hash가 연결된 Canonical review가 필요하다.

## 4. Legacy Fact 공식 승인 계약

- `approve-topic --approval-only`는 managed Topic의 검토 상태를 release/promote와 분리하기 위한 Stage 5 기능이다. Legacy Topic Pack Fact Registry 승인 기능이 아니다.
- `grading/evidence/approved_fact_registry.py`는 registry version, delegated approval record, reviewer/date/scope, 각 Fact의 `approved`/`verified`, ID 고유성, Master Topic 연결 등을 **검증**한다. 그 자체가 reviewer 승인 행위를 수행하지 않는다.
- Verified Fact의 근거·locator·적용조건 요건은 `grading/evidence/fact_grounded_contracts.py` 및 Fact Anchor eligibility policy가 결정한다.
- Legacy scoring promotion 경로는 `scripts/promote_reviewed_fact_anchors.py`의 allowlist/promotion artifact 및 canonical statement/anchor/topic/hash/source-record 일치 검사다. Stage 5 기준 104개 기존 promotion은 `--check`에서 확인되었으나, 이는 신규 Fact 승인이 아니며 이 단계에서 실행·변경하지 않았다.
- Source registry 상태 `approved/verified`만으로 일반 scoring admission이 되지 않는다. revision hold, duplicate/exclusion overlay 및 exact promotion pin을 각각 보존해야 한다. managed Topic approval, Fact source review, scoring eligibility, generated projection, release는 별개의 문턱이다.
- Stage 6에서 신규 공식 승인은 0. 허위 승인 기록 작성, 승인 상태 직접 변경, source hash 우회, Fatal Rule 무효화 및 기존 approval pin 변경을 수행하지 않았다.

## 5. Generated Bank stale 원인 및 Release Gate

Stage 5 Canonical의 cavitation #24 수정으로 Topic Pack source content/version이 바뀌었다. Builder는 모든 generated view에 content-derived version/manifest를 기록하므로 Topic 고유 Projection 외에도 6개 파일의 version/hash metadata가 달라진다. 현재 생성된 파일은 이전 snapshot이며 Canonical을 반영하지 않는다.

| Generated view | stale 판정 원인 | Canonical / 운영 영향 |
|---|---|---|
| `fact_anchors.generated.json` | content-derived source version 및 cavitation Anchor projection 불일치 | runtime fact snapshot은 기존; 이번에 변경 안 함 |
| `model_answers.generated.json` | source version 및 cavitation answer feature | 기존 snapshot 유지 |
| `topic_importance.generated.json` | source version metadata | 내용 변경 없이 version stale |
| `logic_checks.generated.json` | source version metadata | #24의 updated logic 미반영 |
| `logic_check_profiles.generated.json` | source version 및 truth/correction profile | #24 update 미반영 |
| `topic_pack_manifest.generated.json` | Topic Pack source manifest/hash 변경 | source set version stale |

정확한 freshness 검사 조건은 builder가 임시 디렉터리에 생성한 projection과 committed generated files의 byte-for-byte 비교다. 검사는 생성물을 repo에 쓰지 않는다. `scripts/check_generated_rubrics_freshness.py` Stage 5 실행은 6개 파일 모두 stale로 보고했고, `scripts/validate_release.sh`의 freshness 하위 검증 2건이 실패해 Release Gate 종료 코드 1이었다. 원인은 검증이 불일치한 Canonical/generated snapshot을 올바르게 검출한 것이며, 테스트 오류 또는 정책상 완화 대상으로 보지 않았다.

Stage 6에서는 콘텐츠 감사와 freshness checker를 재실행했고 non-promote 전체 Release Gate 및 전체 pytest는 재실행하지 않았다. Stage 5에서 같은 Canonical baseline 기준 전체 pytest 1,620/0/1, Master 89, 2,096 Anchor, `validate-all`, Topic release validation을 완료했다. Stage 6 source-only 재검증 `python3 -B scripts/audit_topic_pack_content.py`: **PASS**, `topics=89 masters=89 questions=767 anchors=2096` (exit 0). Freshness checker는 exit 1로 6 stale outputs를 다시 보고했다. 신규 Canonical/코드 변경이 없어 전체 pytest와 non-promote Gate를 반복하지 않았다. 따라서 최종 Release Gate 상태는 **FAIL (Stage 5 전체 Gate의 실제 종료 코드 1; Stage 6 freshness check exit 1)**이며 PASS라고 보고하지 않는다. Promote 후 재생성·검증은 이후 별도 승인된 단계가 필요하다.

## 6. 최종 Anchor disposition (55)

“수정 권고” 항목은 #24를 제외하고 Stage 6에서 위 23개 상세 재판정을 받았다. “보류” 11개는 §3에 있다. 나머지 기존 유지·제외 결과는 Stage 5에서 확인된 overlay를 그대로 계승한다.

| # | Topic ID / Anchor ID | 최종 처분 | Canonical / scoring 메모 |
|---:|---|---|---|
| 1 | `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` / `acl_calibrator_isolation_workflow` | HOLD | §3 device/procedure scope 보류 |
| 2 | `balanced_trim_unbalanced_trim_structure_sealing_applications` / `control_valve_balanced_unbalanced_scope` | 기존 일반채점 제외 | duplicate overlay 유지; 삭제 없음 |
| 3 | `balanced_trim_unbalanced_trim_structure_sealing_applications` / `nominal_seat_area_boundary` | KEEP | 기존 결정 유지 |
| 4 | `balanced_trim_unbalanced_trim_structure_sealing_applications` / `force_direction_sign_convention` | KEEP | 기존 결정 유지 |
| 5 | `balanced_trim_unbalanced_trim_structure_sealing_applications` / `balanced_trim_pressure_communication` | KEEP | 기존 결정 유지 |
| 6 | `balanced_trim_unbalanced_trim_structure_sealing_applications` / `residual_effective_area` | HOLD | §3 기하/압력 경로 미정 |
| 7 | `balanced_trim_unbalanced_trim_structure_sealing_applications` / `ideal_full_balance_boundary` | KEEP | 기존 결정 유지 |
| 8 | `balanced_trim_unbalanced_trim_structure_sealing_applications` / `balance_seal_leakage_path` | KEEP | 기존 결정 유지 |
| 9 | `bode_frequency_response_stability_margin_bandwidth` / `open_loop_closed_loop_roles` | HOLD | 기술식은 타당, scoring/source review 미완료 |
| 10 | `bode_frequency_response_stability_margin_bandwidth` / `pole_zero_magnitude_slopes` | HOLD | 기술식은 타당, scoring/source review 미완료 |
| 11 | `bode_frequency_response_stability_margin_bandwidth` / `gain_phase_crossover_frequencies` | KEEP | §2 |
| 12 | `bode_frequency_response_stability_margin_bandwidth` / `closed_loop_bandwidth` | HOLD | 문구의 다중 교차 처리 source review 필요 |
| 13 | `configuration_change_release_backup_rollback_migration_obsolescence_management` / `sw06_impact_analysis_multidisciplinary` | KEEP | §2 범위 한정 |
| 14 | `configuration_change_release_backup_rollback_migration_obsolescence_management` / `sw06_change_implementation_plan` | KEEP | §2 범위 한정 |
| 15 | `configuration_change_release_backup_rollback_migration_obsolescence_management` / `sw06_risk_based_regression` | KEEP | §2 위험기반 |
| 16 | `configuration_change_release_backup_rollback_migration_obsolescence_management` / `sw06_backup_scope_and_consistency` | KEEP | §2 위험/자산 조건 |
| 17 | `configuration_change_release_backup_rollback_migration_obsolescence_management` / `sw06_migration_discovery_dependency_inventory` | KEEP | 완전 식별 보장 금지; 현재 한정 유지 |
| 18 | `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` / `sw02_transition_guard` | KEEP | bounded SFC 표현 유지 |
| 19 | `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` / `sw02_trip_latch_reset` | HOLD | reset 설계 근거 없음 |
| 20 | `control_system_operations_maintenance_calibration_inspection_spares_kpi` / `maintenance_configuration_backup_change_handoff` | KEEP | Stage 4 NIST 검토 계승 |
| 21 | `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `liquid_pressure_profile_scope` | 기존 일반채점 제외 | 중복 overlay 유지; 삭제 없음 |
| 22 | `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `fl_direction_and_cavitation_susceptibility` | KEEP | 기존 범위 한정 유지 |
| 23 | `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `liquid_choked_flow_not_zero` | KEEP | 기존 결정 유지 |
| 24 | `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `flashing_classification` | SIMPLIFY (Stage 5 complete) | `P₂<Pᵥ`; `P₂=Pᵥ` 포화 경계; score revision hold 유지 |
| 25 | `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `reduce_total_pressure_drop_prevention` | KEEP | 기존 조건부 예방 문구 유지 |
| 26 | `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening` / `control_valve_commissioning_characteristic_verification` | KEEP | Stage 5 bounded 검토 계승 |
| 27 | `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` / `stick_slip_repeated_motion` | KEEP | 기존 결정 유지 |
| 28 | `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` / `stiction_limit_cycle_path` | KEEP | §2 조건부 인과 |
| 29 | `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` / `large_step_test_pneumatic_capacity` | HOLD | 시험/제품 한정; general scoring source review 미완료 |
| 30 | `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` / `positioner_closed_loop_position_feedback` | KEEP | 기존 결정 유지 |
| 31 | `control_valve_deadband_stiction_response_time_positioner_dynamic_performance` / `hunting_multicausal_diagnosis` | KEEP | 기존 결정 유지 |
| 32 | `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` / `absolute_temperature_required` | KEEP | 기존 결정 유지 |
| 33 | `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` / `pressure_ratio_direction` | HOLD | 기존 hold 보존, overlay 수정 없음 |
| 34 | `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` / `choked_flow_not_zero_flow` | KEEP | 기존 결정 유지 |
| 35 | `control_valve_gas_sizing_choked_flow_critical_pressure_ratio` / `choked_flow_downstream_independence` | KEEP | 기존 결정 유지 |
| 36 | `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error` / `dp_level_calibration_lrv_urv` | KEEP | 기존 결정 유지 |
| 37 | `electronics_error_noise_drift_tolerance_aging_power_mitigation` / `eem_auto_zero_ratiometric` | KEEP | §2 topology/ratio 조건 |
| 38 | `electronics_error_noise_drift_tolerance_aging_power_mitigation` / `eem_layout_local_mitigation` | KEEP | §2 ground split 일반화 금지 |
| 39 | `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` / `fsrm_markov_state_transition` | KEEP | §2 가정 조건 |
| 40 | `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` / `selection_environment_process` | HOLD | 센서 정격/device source 필요 |
| 41 | `lead_lag_compensator_phase_margin_steady_state_error` / `lead_lag_implementation_validation` | KEEP | 요구사항/구현 종속 |
| 42 | `lqr_optimal_state_feedback_riccati_weighting_design` / `state_lqr_tracking_prefilter_lqi` | KEEP | 수식·조건·개념 구분 유지 |
| 43 | `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` / `triangulation_range_resolution_tradeoff` | KEEP | 기존 결정 유지 |
| 44 | `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` / `alignment_occlusion_geometry` | KEEP | 기하/가림 경계 |
| 45 | `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` / `tof_timing_jitter_resolution` | KEEP | `cδt/(2n)` 및 조건 유지 |
| 46 | `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` / `multipath_mixed_pixel_error` | KEEP | 오류 가능성 한정 |
| 47 | `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_patch_management` | KEEP | Stage 4 NIST 제한 유지 |
| 48 | `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative` / `pid_line_list_spec_relation` | KEEP | 프로젝트 조건부 문구 유지 |
| 49 | `process_control_loop_architecture_cascade_ratio_feedforward_override_split_range` / `loop_interaction_coordination` | KEEP | SISO/MIMO 경계 유지 |
| 50 | `sil_target_determination_risk_reduction_and_lifecycle` / `method_selection` | KEEP | 기존 scoped promotion 기록 범위만 인정 |
| 51 | `sil_target_determination_risk_reduction_and_lifecycle` / `operations_moc_revalidation` | HOLD | 넓은 Canonical/좁은 pinned statement 불일치; §2 |
| 52 | `speed_rotation_measurement_encoder_proximity_tachometer_selection_error` / `proximity_airgap_target_error` | HOLD | 기종별 airgap/target 근거 필요 |
| 53 | `state_feedback_reference_tracking_prefilter_integral_action` / `state_tracking_implementation_validation` | KEEP | 구현/모델 조건, 별도 가산 없음 |
| 54 | `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` / `thermocouple_type_material_range_atmosphere_selection` | KEEP | 타입/분위기 조건 |
| 55 | `thermocouple_temperature_sensor_seebeck_reference_junction_compensation` / `thermocouple_calibration_tolerance_uncertainty_drift` | KEEP | tolerance/uncertainty 구분 |

표는 기존 55개 decision set을 유지한다. #9/#10의 수식이 기술적으로 타당하다고 확인했지만 source review/hash와 승인된 scoring path가 완성되지 않아 HOLD를 유지했다. 신규 공식 scoring promotion은 0이다. 기존 general-scoring exclusion은 2건 그대로이며, 기존 holds 11건도 별도 category로 유지된다.

## 7. 검증 및 종료 상태

| 검증 | 실제 결과 | 상태 |
|---|---|---|
| Branch / conflict | 지정 branch; unmerged index 0 | PASS |
| Existing content audit `python3 -B scripts/audit_topic_pack_content.py` | topics 89, masters 89, questions 767, anchors 2,096; exit 0 | PASS |
| Topic JSON/schema/Registry/source hash | Stage 5 기준선 재사용; Stage 6 Canonical 수정 없음 | Stage 5 PASS; 신규 전체 재실행 없음 |
| Master structure 89 / Topic projection 2,096 | Stage 5 기준선 재사용 | Stage 5 PASS |
| Deterministic scoring, Fatal, owner/weight/Golden regressions | 채점 코드·Canonical 수정 없음; Stage 5 focused and full suite results reused | Stage 5 PASS |
| Full offline pytest | **1,620 passed, 0 failed, 1 skipped**, Stage 5 run; Stage 6 rerun 0 | PASS at unchanged baseline |
| Generated freshness / Release Gate | Stage 6 freshness check exit **1**; 6 stale outputs. Stage 5 non-promote Release Gate exit **1**; 2 freshness tests failed | **FAIL; no bypass** |
| Generated promote / deployment | 0 | Not performed |

작업 종료 시 diff review는 기존 사용자 staged/unstaged 변경을 포함하므로 그 파일들을 정리·stage하지 않았다. 신규 보고서 외에 Stage 6에서 source/code/generated/runtime 파일 변경은 0이다. Existing staged/unstaged/untracked changes were preserved. Commit/push were not performed.

## 참고한 공식 기술자료

- NIST SP 800-82 Rev.3, [publication page](https://csrc.nist.gov/pubs/sp/800/82/r3/final) 및 [official PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf); OT 보안·변경·백업 guidance.
- NIST SP 1339, [official publication](https://csrc.nist.gov/pubs/sp/1339/final), OT backup quick-start.
- MathWorks [gain/phase margin and crossover definition](https://www.mathworks.com/help/control/ref/dynamicsystem.margin.html), [bandwidth definition](https://www.mathworks.com/help/ident/ref/dynamicsystem.bandwidth.html).
- Analog Devices [zero-drift amplifiers](https://www.analog.com/en/resources/analog-dialogue/articles/how-to-use-zero-drift-amplifiers-in-wider-bandwidth-applications.html), [differential amplifier resistor matching](https://www.analog.com/media/en/technical-documentation/application-notes/an-589.pdf), and [sensor excitation/ratiometric measurement](https://www.analog.com/cn/resources/analog-dialogue/articles/transducer-sensor-excitation-and-measurement-techniques.html).
- Optica [AMCW ToF multipath paper](https://opg.optica.org/ol/abstract.cfm?uri=ol-39-6-1705).
- HSE [risk graph/LOPA report](https://www.hse.gov.uk/offshore/assets/docs/inspection-of-loss-of-containment.pdf), [functional safety inspection guide](https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf), and [COMAH C&I assessment guidance](https://www.hse.gov.uk/comah/sragtech/discguidciindex.htm). HSE material is jurisdiction/context specific; examples are not stated as universal legal requirements.
- NIST [thermocouple calibration services](https://www.nist.gov/pml/sensor-science/temperature-humidity/thermocouples-calibrations-services) and [uncertainty budget publication](https://www.nist.gov/publications/uncertainty-budgets-comparison-calibrations-thermocouples).
