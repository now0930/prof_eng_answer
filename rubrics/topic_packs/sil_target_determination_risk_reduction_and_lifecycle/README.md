# 목표 SIL 결정·요구 위험감소·플랜트 안전수명주기

- Topic ID: `sil_target_determination_risk_reduction_and_lifecycle`
- Question type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `HIGH`
- Selection importance: `CORE_MUST_PREPARE`

## Scope

위험 시나리오와 허용위험에서 필요한 위험감소량을 산정하고 목표 SIL을 SIF에 할당한 뒤 PFDavg 또는 PFH 검증과 운전·시험·변경관리로 인계하는 전체 판단 흐름을 소유한다.

## Ownership

- **OWNED**: SIS·SIF·SIL의 역할과 목표 SIL이 개별 SIF의 위험감소 요구사항이라는 시스템 경계를 소유한다.
- **OWNED**: 위험 시나리오, 허용위험, 기존 IPL, 요구 RRF, 목표 PFDavg·PFH와 SIL band로 이어지는 결정 흐름을 소유한다.
- **OWNED**: Risk graph·LOPA·정량위험평가의 적용 수준과 결과 검증, SRS 및 운전 수명주기 인계를 소유한다. 보정값이나 matrix 분류는 적용 지침과 조직 기준으로 확인한다.
- **EXCLUDED**: HAZOP node 작성법과 LOPA IPL 적격성의 상세 계산은 hazop_lopa_ipl_risk_reduction_sil_target_allocation Topic으로 인계한다.
- **EXCLUDED**: 투표구조·Markov·FTA·RBD·beta factor의 상세 신뢰도 계산은 functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh Topic으로 인계한다.
- **EXCLUDED**: ESD 밸브·액추에이터·PST의 상세 설계와 시험 절차는 final_control_element_sil_sis_esd_valve_partial_stroke_test Topic으로 인계한다.

## Technical anchors

## 대표 문제와 채점 범위

이 Pack은 SIL과 관련된 네 개의 출제 가능한 문제 형태를 포괄하지만, 한 답안이 네 형태의
전체 내용을 모두 다뤄야 한다는 뜻은 아니다. 문항을 먼저 분류하고
`model_answer.json`의 해당 pattern `required_anchor_ids`만 필수범위로 적용한다.

| 문제 형태 | 핵심 범위 |
|---|---|
| SIL 결정·플랜트 운영·최신 이슈 | 위험 시나리오부터 요구 RRF/목표 SIL, achieved 검증, 시험·운전·MOC 및 AI/OT 연결까지 |
| 허용위험·기존 보호계층 기반 목표 SIL 산정 | 시나리오, 허용위험, IPL 적격성, 잔여빈도, RRF, 목표 성능지표와 SIL band |
| Risk graph·LOPA·QRA 비교 | 자료수준·적용범위·불확실성 및 기존 IPL 처리의 차이 |
| Demand mode·PFDavg/PFH·검증 | mode 선택, 목표 지표 및 전체 SIF achieved 검증 |

`high_score_points`, `common_missing_points`, importance unlock 조건은 위 표의 모든 항목을
모든 질문에 공통 요구하지 않도록 패턴 번호를 명시한다. Fatal 오답은 학생이 해당 주장을
실제로 했을 때만 판정하며, 주제 밖 세부사항을 언급하지 않은 것 자체는 감점 근거가 아니다.

### SIS·SIF·SIL 경계

SIS는 하나 이상의 SIF로 구성되고 SIL은 특정 위험 시나리오를 담당하는 개별 SIF에 요구되는 안전무결성 수준이다. SIL을 SIS 전체나 인증 부품 하나의 절대 안전등급으로 취급하지 않는다.

### 위험 시나리오 경계

목표 SIL은 initiating event, 운전조건, consequence endpoint와 필요한 safe state가 명확한 위험 시나리오별로 결정한다. 서로 다른 원인이나 결과를 한 빈도로 뭉치지 않는다.

### 허용위험과 ALARP

허용 가능한 사건빈도 또는 위험 기준은 조직이 승인한 개인·사회적 위험 기준과 consequence category에 따라 정한다. ALARP에서는 관련 good practice와 추가 위험저감조치를 우선 검토하고, 조치를 시행하지 않을 때는 비용·시간 등의 희생이 얻는 위험감소에 비해 현저히 불균형하다는 근거를 제시한다. 단순 비용·편익 최적화만으로 추가 조치를 배제하지 않는다.

### SIL 결정 방법 선정

Risk graph와 LOPA는 SIL 할당에 쓰일 수 있는 서로 다른 방법이다. HSE 자료에서 LOPA는 시나리오별 빈도·IPL·허용빈도를 다루는 반정량 방법이며, risk graph는 더 단순한 대안으로 screening 또는 해당 지침의 범위에서 단독 평가에 쓸 수 있다. QRA는 필요할 때 정량 위험평가로 선택한다. 방법은 적용 지침, 시나리오 복잡성, 자료 품질과 조직 기준에 맞춰 고르고 보정값·matrix 기준을 보편값처럼 단정하지 않는다.

### 기초빈도와 조건부 수정인자

보호계층 적용 전 시나리오 빈도는 initiating event frequency에 실제 노출시간, 점화확률, 재실확률 등 해당 시나리오에 필요한 enabling condition과 conditional modifier를 곱해 산정한다.

### 기존 IPL의 독립성과 신뢰성

기존 보호수단은 specificity, independence, dependability와 auditability를 만족할 때만 IPL credit을 부여하며 BPCS·alarm·operator action·SIS가 센서, 전원, 로직 또는 인력을 공유하면 종속성과 공통원인을 반영한다.

### SIF 전 잔여 사건빈도

SIF 적용 전 잔여 사건빈도 F_residual은 initiating event frequency와 조건부 수정인자 및 인정 가능한 기존 IPL의 PFD를 곱하여 구한다. 보호수단의 효과를 consequence와 PFD 양쪽에 중복 반영하지 않는다.

### 요구 위험감소율 산정

잔여 사건빈도 F_residual이 허용 사건빈도 F_tolerable보다 크면 SIF가 제공해야 할 최소 위험감소율은 RRF_required = F_residual / F_tolerable이다.

### 목표 PFDavg 관계

저요구 모드에서 목표 평균 요구고장확률은 PFDavg_target <= 1 / RRF_required = F_tolerable / F_residual로 정한다. 빈도끼리의 비이므로 무차원이며 허용빈도와 기초빈도를 곱하지 않는다.

### SIL band 매핑

요구 RRF 또는 목표 PFDavg·PFH를 적용 표준의 SIL band에 매핑하되 경계값, 운전 mode와 조직의 보수적 rounding 규칙을 기록한다. 목표 SIL과 실제 설계가 달성한 SIL을 구분한다.

### Demand mode와 성능지표 선택

Low-demand와 high-demand 또는 continuous mode는 위험고장 발견 시점이 아니라 안전기능의 요구빈도와 기능이 연속적으로 작동하는지에 따라 구분한다. 저요구에는 PFDavg, 고요구·연속에는 PFH를 사용한다.

### 달성 SIL 정량검증

설계 검증은 센서·logic solver·final element의 위험고장률, architecture, diagnostic coverage, proof-test interval과 coverage, repair time, common cause와 mission time을 적용해 전체 SIF의 PFDavg 또는 PFH를 계산한다.

### Proof test와 PST 역할

Full proof test는 정상 diagnostics가 찾지 못한 위험고장을 정해진 coverage와 acceptance criteria에 따라 검출하며, 발견된 고장은 별도로 복구하고 재시험한다. PST는 검출 가능한 일부 밸브 고장에만 효과가 있으므로 full proof test를 자동 대체하거나 MTTR을 본질적으로 단축하지 않는다.

### SRS와 안전수명주기 인계

결정 결과를 SIF 경계, safe state, trip setpoint, response time, target SIL, demand mode, test interval·coverage, bypass와 복구 요구사항을 포함한 SRS로 인계하고 설계·검증·운전·폐기 단계까지 추적한다.

### 운전·MOC·재검증

운전 중에는 proof-test 수행률, as-found failure, bypass 시간, demand와 spurious trip, 부품 변경과 설정 변경을 기록한다. 공정·위험·시험주기·부품·software 변경은 MOC 영향평가를 거치고, 위험 시나리오 또는 기존 설계 가정에 영향이 있는 경우 관련 LOPA·SIL allocation·SIL verification을 필요한 범위에서 재검토한다.

### OT 보안·AI와 기능안전 경계

OT 보안은 안전·신뢰성 제약과 함께 관리하고, 사이버 위협이 SIS/SIF의 가용성과 안전기능 독립성에 미치는 영향을 기능안전 검토에 연결한다. AI 생성 코드는 안전기능 검증을 대신하지 않는다. 안전 관련 코드 변경에 AI를 사용하면 프로젝트의 안전수명주기와 변경관리 기준에 따라 요구사항 추적, 형상·무결성 관리, 적격한 독립 검토·시험과 승인된 배포를 적용하도록 권고한다. 이를 IEC의 AI 전용 직접 요구사항으로 단정하지 않는다.

## 결정론적 machine contract

Issue #1의 원본·교정 답안 쌍을 기준으로 다음 7개 Fact Anchor를 canonical relation으로
판정한다: SIS/SIF/SIL scope, 요구 RRF, 목표 PFDavg, demand mode, achieved SIL 검증,
MOC 재검증, AI·OT 기능안전 경계. 같은 anchor의 lexical hit보다 canonical 관계가
우선하며 원본의 fatal 4건은 `WRONG`, 교정 답안의 빈도비·PST·실제 SIF 계산 관계는
정상 evidence로 유지한다. 특정 답안 전체 문자열이나 점수 예외는 사용하지 않는다.

## Handoffs

- `hazop_lopa_ipl_risk_reduction_sil_target_allocation` — HAZOP에서 LOPA scenario 전환, IPL 적격성 및 상세 잔여빈도 계산이 요구될 때: HAZOP·LOPA·IPL 세부 절차와 계산을 인계한다.
- `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh` — PFDavg·PFH, voting architecture, CCF의 상세 정량모델이 요구될 때: 신뢰도 모델과 수식 검증을 인계한다.
- `final_control_element_sil_sis_esd_valve_partial_stroke_test` — ESD valve package, PST와 full-stroke proof test의 상세 설계가 요구될 때: Final element 구성·고장모드·시험 절차를 인계한다.
- `sis_sil_safety_software_independence_systematic_failure_verification_validation` — Safety software systematic capability와 V&V가 주 요구일 때: 안전 software lifecycle과 독립 V&V를 인계한다.
- `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` — OT cybersecurity architecture와 incident response가 주 요구일 때: 보안 방어구조와 운영 대응을 인계한다.

## Standards and sources

- IEC 61508 (project-controlled applicable edition) — 기능안전, SIL 성능지표와 안전수명주기 원칙
- IEC 61511 (project-controlled applicable edition) — 공정산업 SIS의 SIL 결정·SRS·운전 및 유지보수 수명주기
- IEC 62443 series (project-controlled applicable edition) — OT 보안 변경과 기능안전 경계의 연계

## Compiler contract

- Generated from a validated Topic Spec.
- File structure and schema are owned by repository code.
- Runtime donor dependency: `false`.
