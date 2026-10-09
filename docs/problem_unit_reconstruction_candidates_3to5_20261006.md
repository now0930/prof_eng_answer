# 1차 후보 3–5번 Problem Unit 재구성 검토

검토일: 2026-10-06
대상: hardware lifecycle, software project/FAT-SAT, HMI/SCADA
상태: **경계·coverage 설계 검토 — Pack source와 routing 변경 없음**

이 문서의 질문은 지식으로 구성한 예상 문제 후보이며 확인된 기출 문항이 아니다.
공식 분류/기출로 오인해 표기하지 않는다.

## 1. Hardware lifecycle / panel / production verification

대상 Pack: `control_hardware_lifecycle_panel_architecture_component_selection_production_verification`
현황: 35 Anchor, 10 patterns. 핵심 답안 흐름은 요구사항→architecture/interface→component
selection→design verification→manufacturability/production control→production verification→release다.

### 중심 종합 Problem Unit 후보

> **산업 제어 Hardware의 요구사항을 architecture와 부품선정으로 구체화하고, 설계검증부터
> 생산검증·변경관리·release까지의 수명주기와 추적성을 설명하시오.**

| 요구 축 | 필요한 연결 지식 | 기존 Anchor/패턴 소유 | coverage 판정 |
|---|---|---|---|
| 요구·설계기준 구체화 | 요구 분해, 양방향 추적, interface, design review, verification plan | `chl_scope_chain`, `chl_requirement_traceability`, `chl_design_review`, `chl_verification_plan` (#1/#6) | 종합 문제에 필요한 backbone 있음 |
| Hardware 구조/선정 | panel partitioning, power/protection, I/O·communication, thermal/layout, derating·lifecycle | `chl_architecture_partitioning`, `chl_interface_definition`, `chl_power_budget`, `chl_io_selection`, `chl_component_selection_multicriteria`, `chl_derating_rule` (#2–4) | 세부 선택문제가 별도로 성립하므로 종합문제는 대표 항목만 요구 |
| 설계검증과 qualification 경계 | prototype/DV, environmental qualification, FAT/SAT가 무엇을 입증하고 못 하는지 | `chl_prototype_design_verification`, `chl_environmental_qualification_boundary`, `chl_fat_boundary` (#5/#10) | 구분 기준을 중심 unit에 유지 |
| 제조 준비와 양산검증 | DFM/DFA, BOM/configuration, incoming/process control, EOL coverage, fixture, NCR/rework | `chl_dfm_dfa`, `chl_bom_configuration`, `chl_incoming_material_control`, `chl_production_test_coverage`, `chl_test_fixture_control`, `chl_eol_test`, `chl_nonconformance_rework` (#5/#7/#8) | 생산검증은 설계검증과 다른 증거·표본화 문제로 별도 unit 후보 |
| 변경·release | impact, affected requirement/test, re-verification, release gate | `chl_change_impact`, `chl_release_gate` (#9) | 종합문제의 폐루프에 필요 |

### 독립 단위 후보와 판정

- #2 panel architecture, #3 derating/component selection, #4 I/O·통신 선정을 각각 독립
  설계문제로 구성할 수 있다. 하나의 예상문제에 합치면 평가 대상이 과도하게 넓어진다.
- #5/#7/#8 production verification은 하나의 생산준비·EOL 문제 묶음으로 합칠 수 있다.
- #6 verification vs validation은 요구추적/검증계획 문제로 #1과 합치는 게 가능하나,
  별도 정의 비교문제로도 성립한다.
- #9 substitution/change impact는 #1의 lifecycle release chain에 속할 수 있으나,
  영향분석·재검증 범위 선정이라는 별도 판단문제다.
- #10 DV / environmental qualification / FAT-SAT는 owner handoff를 포함한 경계비교
  문제다. SAT/FAT project acceptance는 SW-10, 환경시험 상세는 qualification Topic으로
  넘기는 현재 README의 ownership을 보존한다.

**제안:** 단일 시험 패턴 10개를 다 대표 패턴으로 간주하지 않는다. 현재 Pack을 lifecycle
종합 문제로 대표하고, panel/component/design 및 production verification을 별도 예상
문제군으로 분류한다. 즉시 분할할지는 inventory alias, 평가 view의 ID 참조를 확인한 뒤
결정한다.

## 2. Software project / engineering documents / FAT-SAT / commissioning

대상 Pack: `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`
현황: 34 Anchor, 10 patterns. README는 SW-10을 프로젝트 산출물, 현장 검증, 계약 인수
owner로 규정하고 SW lifecycle(V-Model), interlock/Alarm 메커니즘과 구분한다.

### 중심 종합 Problem Unit 후보

> **제어시스템 프로젝트에서 사용자 요구와 설계문서의 추적성을 확보하고, FAT·SAT·Loop/
> integration test·commissioning·performance test를 거쳐 인수·인계하는 절차와 증적을
> 설명하시오.**

| 요구 축 | 필요한 연결 지식 | 기존 패턴 | 판정 |
|---|---|---|---|
| 프로젝트 실행 기반 | scope, schedule/dependency, cost/change control | #1 | 프로젝트관리 독립 주제. 종합 문제 배경으로만 둘지 이 Pack이 책임질지 ID/README에 명시해야 함 |
| 요구·문서 추적 | URS→FRS→FDS→SDS, I/O/tag/alarm/interlock/C&E, 양방향 traceability | #2/#3 | 둘은 같은 문서관리 unit으로 합칠 수 있지만 list 목적 차이로 하위 변형 필요 |
| 시험환경과 경계 | test specification, FAT/SAT, 검출범위·환경·한계 | #4 | 독립 비교형 Problem Unit. 기존 SW-04/03 시험과 중복하지 않도록 프로젝트 수용시험으로 한정 |
| 현장 검증 순서 | loop test, site integration, commissioning, configuration/backup | #5/#6 | 동일 현장 검증 흐름으로 묶을 수 있음. Commissioning 자체의 안전·품질 절차는 출처 확인 필요 |
| 성능·인수 | measurable performance criteria, acceptance evidence | #7 | 별도 acceptance decision 문제 가능. 기준값을 출처 없이 수치화하지 않음 |
| Punch/as-built/handover | 결함 closure, as-built, backup/restore, handover package | #8 | 프로젝트 종결 unit. 현장시험과 연결되나 독립 요구로도 성립 |
| 변경·재시험 | impact analysis, baseline update, affected test/retest, close-out | #9 | 공통 lifecycle closure에 연결 |
| 전 과정 통합 | 위 요구 전반의 traceability | #10 | 총괄 종합문제. 단독으로 유지 가능하나 세부 1–9의 대체는 아님 |

**제안:** Pack 목적은 #10과 가장 잘 맞는다. #1의 일반 프로젝트관리 범위, #2–3 문서
taxonomy, #4–9 현장시험/인수는 답안 backbone에 연결되지만 독립 예상문제군이다. 중심
Problem Unit은 “문서추적→FAT/SAT 및 현장시험→성능/인수→기록/변경종결”로 제한하고,
scope/cost와 각 개별 list 비교는 secondary candidate로 분리 검토한다.

## 3. HMI / SCADA / Alarm / setpoint / trip / interlock / SOE

대상 Pack: `hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management`
현황: 31 Anchor, 10 patterns, 5 disconnected families. README에 이미 ownership이 명시돼
있다: 운전자 정보/Alarm/Setpoint/SOE/Audit는 이 Topic, Trip·Interlock 실행논리는 SW-02,
일반 V&V는 SW-04, 프로젝트 인수는 SW-10, SIL은 SW-05.

### 중심 Problem Unit 후보

> **운전자 정보 시스템에서 HMI 화면계층, Alarm lifecycle과 운전자 대응, SOE·감사기록 및
> 권한통제를 연계하여 비정상상황 대응성을 확보하는 설계·운영 방안을 설명하시오.**

| 요구 축 | 필요한 연결 지식 | 기존 패턴 | 판정 |
|---|---|---|---|
| HMI/SCADA·화면 | architecture/data quality, high-performance HMI, display hierarchy/context | #1/#2 | HMI 설계 problem unit; 정보 품질을 포함하면 한 답안 축으로 연결 가능 |
| Alarm lifecycle | philosophy/rationalization, priority, response time, deadband/delay, shelving/suppression, flood/KPI | #3/#4/#5/#9 | 독립된 Alarm-management unit. #3–5–9는 lifecycle 한 축, #4는 설정기준 심화 |
| 운전자 설정값·보호경계 | setpoint/alarm/trip/interlock 값의 의미·governance 및 SW-02 실행 owner handoff | #6 | 독립 governance 문제. trip/interlock logic 자체를 이 Pack에 가져오지 않음 |
| 기록·상태·감사 | SOE/time sync/first-out/historian, audit trail, operator authority | #7/#8 | 이벤트 기록과 권한 문제를 결합할 수 있으나 별도 예상문제도 성립 |
| 비정상 운전 | alarm response + high-performance HMI + data quality | #10 | 중심 운영 Problem Unit. #1/#2/#3/#9을 연결하는 종합문제 후보 |

**제안:** 가장 응집력 있는 중심은 #10 abnormal situation management다. #1/#2의 HMI,
#3/#4/#5/#9 Alarm lifecycle은 이를 구성하는 connected knowledge. #6 setpoint governance와
#7/#8 SOE/audit/authority는 독립 답안으로도 성립하므로 중심 문제 하나의 필수 범위로
모두 강제하지 않는다. Trip·Interlock은 이름에 포함돼 있더라도 SW-02의 execution logic을
소유한다는 기존 경계를 유지한다.

## 4. 공통 수정 안전조건

1. 위 판정은 source JSON/Topic Sheet를 바꾸지 않은 구조 검토이며, 기술 정확성 승인이 아니다.
2. 10개 패턴 중 동일 답안 backbone의 변형만 한 Problem Unit의 `expected_question_patterns`
   로 둔다. 교재에 같이 있거나 같은 시스템을 쓴다는 이유로 합치지 않는다.
3. Pack을 좁히거나 분할하기 전 existing topic owner, canonical taxonomy, Router aliases,
   classifier tests, grading/training/diagnosis projection 참조를 조사한다.
4. 세 후보는 README·Topic Sheet·JSON 간 세부 source/anchor alignment가 필요한 부분이
   있다. 큰 범위 변화는 관리 workflow, focused test, full validator와 regression을 거친다.
5. 기존 A/B/C/D/E 및 deterministic scoring, canonical Question Type, Router authority,
   fatal handling, golden tests, release gates는 변경하지 않는다.
