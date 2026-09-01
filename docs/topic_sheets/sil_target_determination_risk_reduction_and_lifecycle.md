# 목표 SIL 결정·요구 위험감소·플랜트 안전수명주기

## 1. Topic metadata

- Topic ID: `sil_target_determination_risk_reduction_and_lifecycle`
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `FIELD_APPLICATION`
- 대표 문제: SIL 결정 방법을 설명하고 실제 플랜트 운영 및 최신 산업 이슈와 연계하여 설명하시오.

## 2. Scope and ownership

이 Topic은 위험 시나리오와 허용위험으로부터 필요한 위험감소량을 정하고, 목표 SIL을 개별 SIF에 할당한 뒤 설계 검증과 운전 수명주기로 인계하는 전체 흐름을 소유한다.

직접 소유하는 8개 요구 축은 다음과 같다.

1. `system_scope_and_sil_role`: SIS·SIF·SIL의 역할과 기능 경계
2. `risk_scenario_and_tolerable_target`: 위험 시나리오와 허용위험
3. `existing_ipl_and_independence`: 기존 IPL의 적격성·독립성·공통원인
4. `required_rrf_and_target_sil`: 잔여빈도, 요구 RRF와 목표 SIL
5. `demand_mode_metric_selection`: Demand mode와 PFDavg·PFH 선택
6. `quantitative_verification_dimension`: 관계식 차원과 achieved SIL 검증
7. `proof_test_diagnostics_reliability`: Diagnostics·PST·full proof test·repair
8. `operations_moc_security_ai_lifecycle`: 운전·MOC·보안·AI 수명주기

## 3. Core correct facts

- 목표 SIL은 SIS 전체나 인증 부품이 아니라 위험 시나리오별 개별 SIF에 할당한다.
- `F_residual`은 initiating event frequency에 조건부 수정인자와 적격한 기존 IPL의 PFD를 곱해 구한다.
- `RRF_required = F_residual / F_tolerable`이다.
- 저요구 모드에서 `PFDavg_target <= 1/RRF_required = F_tolerable/F_residual`이다.
- Demand mode는 위험고장 발견 시점이 아니라 안전기능 요구빈도와 연속작동 여부로 구분한다.
- Target SIL과 achieved SIL을 구분하고, 후자는 전체 SIF의 PFDavg 또는 PFH와 정성 제약으로 검증한다.
- PST는 일부 위험고장만 검출하며 full proof test를 자동 대체하거나 MTTR을 자동 단축하지 않는다.
- 시험주기는 실제 SIF 계산과 운전자료로 정하고, 인증서의 가정은 적용조건으로 검토한다.

## 4. Fatal wrong claims

- 목표 PFDavg를 두 빈도의 곱으로 계산한다.
- High/low demand를 고장 검출시점으로 구분한다.
- Component SIL 인증만으로 전체 SIF의 SIL 달성을 증명한다.
- PST가 full proof test를 대체하거나 MTTR을 자동으로 줄인다고 단정한다.
- 인증서 시험주기를 모든 현장의 최소 또는 최적 시험주기로 취급한다.

Fatal 판정은 실제 주장과 문맥을 검증해야 하며, 오답 예시를 부정하고 정답을 제시한 문장은 제외한다.

## 5. Field judgement

- Risk graph, calibrated risk graph, LOPA와 QRA는 입력자료와 불확실성 수준에 맞게 선정한다.
- 설계 가정은 SRS에 남기고 proof-test compliance, as-found failure, bypass, demand와 spurious trip 자료로 확인한다.
- 공정·부품·설정·software·시험주기 변경은 MOC와 SIL 재검증으로 연결한다.
- OT 보안과 AI 변경은 승인경계, 무결성, 독립 V&V, traceability와 rollback evidence를 유지한다.

## 6. Adjacent Topic handoff

- `hazop_lopa_ipl_risk_reduction_sil_target_allocation`: HAZOP·LOPA·IPL 상세
- `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh`: 구조·CCF·PFD/PFH 상세 계산
- `final_control_element_sil_sis_esd_valve_partial_stroke_test`: ESD valve·PST·proof test 상세
- `sis_sil_safety_software_independence_systematic_failure_verification_validation`: Safety software와 systematic failure
- `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response`: OT 보안 방어구조와 incident response

## 7. Routing boundary

- `SIL 결정 방법`, `목표 SIL 결정`, `SIL 결정과 플랜트 운영`과 같은 일반 문제는 이 Topic이 소유한다.
- HAZOP·LOPA 상세, voting·Markov·CCF, ESD valve·PST 또는 safety software가 문제의 주 요구이면 해당 인접 Topic이 우선한다.
- 라우팅은 문제문만 사용하고 학생 답안의 키워드로 Topic을 변경하지 않는다.

## 8. Human review checklist

- 문제의 명시 요구만 required anchor로 투영했는가.
- 관계식의 분자·분모와 단위가 맞는가.
- Demand mode와 diagnostic detectability를 구분했는가.
- Target과 achieved SIL을 구분했는가.
- 최신 이슈가 검증 가능한 lifecycle 통제로 연결되는가.
- 인접 Topic의 세부사항을 일반 SIL 문제의 필수 요구로 확장하지 않았는가.
