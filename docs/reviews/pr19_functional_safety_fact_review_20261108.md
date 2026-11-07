# PR #19 — SIL / SIS-LOPA / MC/DC 내용 검토 (비승인·근거 대조용)

> 상태: REVIEW EVIDENCE ONLY. 이 문서는 원문 교정 방향을 독립 출처와 대조한 검토 기록이다. Golden 라벨의 변경이나 채점 승격 승인, 운영 READY 증거가 아니다. 기존 Fact Anchor의 승인 상태·source hash·scoring exclusion을 변경하지 않는다.
>
> 대상: PR #19, `codex/review-question-answer-20261107`. 검토 자료: `calibration/sil_target_operations_overgrading_regression.json`, `calibration/sis_lopa_architecture_overgrading_regression.json`, `calibration/mcdc_vmodel_sil_overgrading_regression.json`, `calibration/expert_accuracy_golden.jsonl`.

## 1. 공통 평가 경계

1. A/B/C의 기술적 사실·요구판정은 승인된 결정론적 근거로만 확정한다. 외부 자료는 **검토 참고**이지 자동으로 SUPPORTED 또는 Golden 변경 근거가 되지 않는다.
2. D/E의 Argon 제안은 프로그램이 증거와 상한을 확인한 후 반영한다. 결함을 해제하거나 정답 점수를 만드는 권한이 없다.
3. 표준의 적용 판본·산업 분야·요구모드에 따라 상세 요구가 달라질 수 있으므로, 한 분야의 규정을 전체 IEC 61508/61511의 절대 규칙으로 확대하지 않는다.

## 2. SIL 결정·운영: 반드시 구분할 기술적 사실

- **대상과 기능**: SIL은 개별 안전계장기능(SIF)의 목표 및 달성 안전무결성을 검증하는 데 사용된다. SIF는 센서 → 로직 솔버 → 최종요소의 전체 기능 경계로 보아야 한다. SIS 전체에 일률적인 SIL 하나를 부여하는 설명보다 SIF별 적용이 정확하다.
- **LOPA의 정량 관계**: 위험 시나리오별 기존 IPL을 평가한 뒤, 잔여 요구빈도 `f_residual` [1/time]와 허용 사건빈도 `f_tolerable` [1/time]를 구분한다. 낮은 요구모드에서 해당 SIF가 제공해야 하는 목표가 `PFDavg_target <= f_tolerable / f_residual`인 형태라면 **비율이 무차원**이어야 한다. 반대로 `PFDavg <= f_tolerable × f_residual`은 양변의 단위가 달라 잘못된 식이다. 이 표현은 간단화한 단일 시나리오 모델로서 IPL 독립성·조건부 영향·다중 시나리오를 별도 평가해야 한다.
- **요구모드와 고장검출은 별개**: Low demand에서는 평균 요구 시 실패확률인 `PFDavg`(무차원), high demand/continuous mode에서는 `PFH`(시간당 위험고장 지표)를 사용한다. 요구모드를 “고장 발생 직후 확인 가능 여부”로 정의하면 안 된다. 구체적인 계량 척도와 해석은 적용 IEC 판본/분야의 요구를 따르며 high-demand에서의 모델 선택은 별도 검토한다.
- **수명주기**: Proof-test interval, proof-test coverage, 진단 및 정비·변경관리 조건이 실제 달성 PFDavg에 영향을 준다. 제품 인증 때의 시험 조건만으로 모든 현장 SIF의 검사주기를 확정할 수 없다. `PST`(partial-stroke test)는 일부 위험 미검출 고장을 발견하는 시험으로서 검출범위와 잔여 미검출 고장을 다뤄야 한다. `PST가 자동으로 MTTR을 단축한다`고 단정하지 않는다.
- **구조 대 정량**: `λ` 또는 `PFH`는 시간 역수(보통 1/h), `PFDavg`는 무차원이다. 따라서 `λ_SIS < PFDavg`와 같은 직접 크기 비교는 부적절하다. 전체 SIF 평가에는 서브시스템 아키텍처·CCF·진단범위·안전상태·응답시간 등을 함께 확인한다.
- **과도한 절대화 금지**: 특정 SIL에서 “무조건 SIS 층을 추가”하거나 “SIL 3/4이면 항상 전체 재설계”라고 단정하지 말고 목표 SIL과 달성 SIL의 갭 및 설계 제약을 검토한다.

자료 근거:
- [Yokogawa: Effects on PFDavg](https://www.yokogawa.com/eu/library/resources/white-papers/effects-on-pfdavg/) — 완전한 SIF 경계, PFDavg, proof-test 조건 변경과 재계산
- [ISA: Creating a LOPA Project Report](https://www.isa.org/intech-home/2022/december-2022/departments/creating-a-lopa-project-report) — 원인/결과별 시나리오, IPL, 요구 RRF와 SIL 결정
- [Yokogawa: Functional Safety Consultancy](https://www.yokogawa.com/solutions/products-and-services/consulting/functional-safety-consultancy-services/) — 요구 SIL 결정과 달성 SIL 검증, SRS 요구사항 구분
- [ISA: Understanding SIL, proof test coverage and PFDavg](https://www-prod.isa.org/web/acom/article/safety-understanding-sil-cpt-pfdavg) — proof-test coverage 및 진단 범위의 차이

**대응할 보류 사례**
- `sil_target_operations_issue1`: 위 식·검출/요구모드·PST/정비 구분 및 이미 확인된 Fatal은 유지. Golden의 `proof_test_diagnostics_reliability` 최신 저장 값은 **WRONG**이며 과거 PR 댓글의 PARTIAL 서술과 다르다. Golden을 조용히 바꾸지 말고 소스 기준을 재확인한다.
- `sis_lopa_architecture_issue1`: 사고원인·결과, 기존 IPL 독립성, 단위/확률, SIF 기능 경계를 분리한다. 정량 `λ` 대 `PFD` 차원 오류를 성공으로 바꾸지 않는다.

## 3. V-Model / MISRA / MC/DC

- **MISRA는 언어/코딩 가이드라인**이며 단위시험 실행 도구(xUnit 등)가 아니다. 적용 지침과 정적분석의 준수근거는 단위시험 결과·통합시험 결과와 구분해야 한다.
- **단위·통합·시스템시험은 개발/검증 단계**이고, random hardware integrity(PFDavg/PFH), architectural constraints(HFT), systematic capability는 안전무결성의 서로 다른 평가 축이다. 이를 1:1로 연결해 “단위시험=Random Integrity”, “통합시험=HFT” 등으로 표현하면 범주 오류다.
- **V-Model은 추적성과 검증 체계를 제공**하지만 그 자체만으로 특정 SIL 달성을 보증하지 않는다.
- **MC/DC의 적용은 표준 및 안전중요 구성요소 범위에 의존**한다. 예를 들어 NASA의 안전중요 소프트웨어 요구는 100% MC/DC를 명시하지만, 이것을 모든 IEC SIL 3/4 프로그램의 무조건적인 보편 규칙으로 일반화할 수 없다. 대상 표준·판본·시험 증거·적용예외를 구분해야 한다.

자료 근거:
- [MISRA compliance](https://misra.org.uk/compliance/) — MISRA의 성격과 준수 입증 요소
- [NASA SWE-219](https://swehb.nasa.gov/spaces/SWEHBVD/pages/105709626/SWE-219%2B-%2BCode%2BCoverage%2Bfor%2BSafety%2BCritical%2BSoftware) — NASA 안전중요 소프트웨어 MC/DC 요구의 구체적 적용 사례
- [ISA LOPA report](https://www.isa.org/intech-home/2022/december-2022/departments/creating-a-lopa-project-report) — 공정 안전 분석/배정과 별개의 소프트웨어 검증 절차

**대응할 보류 사례**
- `mcdc_vmodel_sil_issue1`: MISRA, HFT, Random Hardware Integrity, MC/DC의 범주 오류를 보존하고 기존 4개 Fatal 검출 결과를 유지한다. `sw04_integration_test`의 미해결 분류는 실제 Grade의 claim/span/계약을 검토하고 판단한다. 단순 키워드 존재로 충족으로 올리지 않는다.

## 4. 계장 전원·접지·차폐 사례의 구조적 차단

`model_reference_08_instrumentation_power_grounding_shielding_ups_ground_loop_emc`의 질문 계약은 5개 Anchor를 요구하나 **5개 모두 채점 사용이 차단**되어 있다:

| Required Anchor | 현재 보류/제외 원인 |
|---|---|
| `ipgse_scope_chain` | 승인 원문 범위 부족(source hold) |
| `ipgse_power_quality_scope` | 승인 원문 범위 부족(source hold) |
| `ipgse_emi_coupling_paths` | 원문 대조·개정 보류(revision hold) |
| `ipgse_diagnostic_workflow` | 세부 사실 우선순위 낮음(scoring exclusion) |
| `ipgse_final_verification` | 승인 원문 범위 부족(source hold) |

같은 Topic에 다른 채점 가능 Anchor가 있다는 이유만으로 위 5개를 **자동 대체하거나 scoring exclusion을 해제하지 않는다**. 필요한 경우 공식 문헌의 직접 근거·문장별 적용 조건을 작성하고 사용자/권위 있는 승인 절차 후 Topic/Question 계약을 재검토한다. 현 단계에서는 `ABSTAIN` 및 `HOLD`가 올바른 fail-closed 결과다.

## 5. 다음 조치와 미해결 증거

1. 운영 비공개 `grade.json`의 실제 claim/span/요구 ID를 3개 안전 사례와 대조하여 **정답 인식 실패인지 기술 오류인지** 분류한다. 대조 없이 점수 보정 금지.
2. `wp-post:9529` 승인 Master와 비공개 artifact/백업 버전을 대조해 소스 소유자의 승인 없는 갱신을 금한다.
3. 수정 후 실제 48건 **uncached** 공급자 재평가, 정확도 READY, 반복 안정성 STABLE, 최신 commit CI SUCCESS를 각각 확인한다.
4. 해당 결과 전에는 운영 manifest를 `READY`로 직접 변경하지 않고 배포도 하지 않는다.

이 문서의 권고는 기술 검토 메모일 뿐 정식 source promotion 또는 expert Golden adjudication이 아니다.
