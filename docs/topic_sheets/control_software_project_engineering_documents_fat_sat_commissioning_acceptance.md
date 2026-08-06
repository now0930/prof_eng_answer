# SW-10 Topic Sheet

## 1. Topic 식별

- Topic ID: `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`
- 한글 주제: 제어 소프트웨어 프로젝트, 설계문서, FAT·SAT·시운전 및 인수
- Lane: `SOFTWARE_LLM_LANE_A`
- 난이도: `DESIGN_EVALUATION`
- 중요도: `CORE_MUST_PREPARE`

## 2. 포함 범위

SW-10은 실제 제어 소프트웨어 프로젝트의 착수, 엔지니어링 문서, 시험, 현장 적용과 계약 인수까지를 다룬다.

- Feasibility, Scope, Schedule, Cost와 변경관리
- Control philosophy, URS, FRS, FDS, SDS와 문서 추적성
- I/O, Tag, Alarm, Interlock list, Cause & Effect, Logic diagram
- Test specification, FAT, SAT, Loop test, Site integration test
- Commissioning, Performance test, Acceptance, Handover
- As-built document, Punch list, 구성 baseline, 백업·복구와 증적

## 3. 제외 범위와 ownership 경계

### SW-04로 이관

- 일반 계측제어 소프트웨어 V-Model
- 요구사항·아키텍처·코딩·단위·통합·시스템시험
- 일반 Verification·Validation, RTM, Static·Dynamic analysis

### SW-02로 이관

- Interlock·Trip 상태전이, Latch·Reset, Fail-safe의 실제 논리 메커니즘

### SW-03으로 이관

- Alarm philosophy, Rationalization, Priority, Deadband, Shelving, SOE 운전정보 원리

SW-10은 위 내용을 프로젝트 산출물, FAT·SAT·현장시험과 인수 증적으로 관리하지만 원리 자체를 소유하지 않는다.

## 4. 대표 출제문제

1. 제어 소프트웨어 프로젝트의 Feasibility, Scope, Schedule과 Cost 관리 절차를 설명하시오.
2. URS, FRS, FDS와 SDS의 목적과 상호 추적관계를 설명하시오.
3. I/O list, Tag list, Alarm list, Interlock list와 Cause & Effect의 역할을 비교하시오.
4. 제어시스템 FAT와 SAT의 목적, 시험환경, 시험항목과 한계를 비교하시오.
5. Loop test와 Site integration test의 대상, 절차와 판정기준을 설명하시오.
6. 제어시스템 Commissioning 절차와 단계별 안전·품질 관리사항을 설명하시오.
7. Performance test와 Acceptance의 기준 및 증적 관리방안을 설명하시오.
8. Punch list, As-built document와 Handover 관리방안을 설명하시오.
9. FAT 이후 변경 발생 시 영향분석, baseline 갱신과 재시험 절차를 설명하시오.
10. 제어 소프트웨어 프로젝트의 문서·시험·시운전·인수 전 과정을 연계하여 설명하시오.


## 5. 핵심 Fact 구조

34개 Fact Anchor는 다음 여덟 묶음으로 구성한다.

1. 프로젝트 범위와 인접 Topic 경계
2. Feasibility·Scope·Schedule·Cost
3. Control philosophy와 URS·FRS·FDS·SDS
4. I/O·Tag·Alarm·Interlock list와 C&E·Logic diagram
5. Test specification과 FAT·SAT
6. Loop·Site integration·Commissioning
7. Performance·Acceptance·Punch closure
8. As-built·Handover·구성 baseline

## 6. 필수 논리 관계

```text
URS → FRS → FDS → SDS → Test specification → Test result
        ↖──────── bidirectional traceability ────────↗
```

```text
FAT = 통제된 제작·공급자 환경의 기능·구성 검증
SAT = 실제 현장 설치·배선·인터페이스 검증
FAT PASS ≠ SAT 생략
```

```text
Loop test → Site integration test → Commissioning
          → Performance test → Acceptance → Handover
```

```text
Change/Punch
→ Impact analysis
→ Approval
→ Baseline·Document update
→ Selected regression/retest
→ Evidence review
→ Closure
```

## 7. 대표 Fatal 오류

- FAT와 SAT는 시험장소만 다를 뿐 완전히 같은 시험이다.
- FAT 합격만으로 실제 현장 배선과 설치환경까지 모두 검증된다.
- FAT에 합격하면 SAT는 생략해도 된다.
- Loop test는 HMI 화면의 값만 확인하면 완료된다.
- 안전조건과 사전점검이 완료되지 않아도 시운전을 먼저 시작할 수 있다.
- 성능시험은 정량적인 운전조건과 수용기준 없이 정상 동작만 보면 된다.
- 설치가 완료되면 시험결과와 문서가 없어도 자동으로 인수된다.
- Punch list 항목은 등급과 무관하게 인수 후 무기한 미완료로 남겨도 된다.
- As-built 문서는 최초 설계본을 그대로 제출해도 된다.
- URS, FRS, FDS와 SDS는 이름만 다르고 서로 대체 가능한 동일 문서이다.
- Cause & Effect는 Alarm 목록만 나열하는 문서이다.
- I/O list와 Tag list는 완전히 같은 목록이다.
- FAT 이후 소프트웨어를 변경해도 영향분석과 재시험은 필요 없다.
- 승인된 시험명세가 없어도 시험자의 경험만으로 FAT와 SAT 합격을 판정할 수 있다.
- 개별 장비가 정상이라면 시스템 간 Site integration test는 필요 없다.
- 일반 소프트웨어 V-Model과 단위시험 체계는 전적으로 SW-10의 현장 인수 범위이다.


## 8. Warn·Major 수준 부족사항

- 문서 이름만 나열하고 관점과 추적관계를 설명하지 않는다.
- FAT·SAT의 장소만 비교하고 대상·검출결함·한계를 누락한다.
- Loop test와 Site integration 범위를 구분하지 않는다.
- 시운전의 안전조건과 단계별 진입·종료기준이 없다.
- 성능시험의 정량조건과 Acceptance의 계약 수락조건이 없다.
- Punch closure, As-built 최종상태와 백업·복구 인계가 없다.

## 9. False positive 방지

- FAT·SAT를 언급하지 않은 답안이라도 문항이 문서체계만 요구하면 fatal로 판단하지 않는다.
- 오답 문장을 인용한 뒤 즉시 부정·정정한 경우 직접 오답으로 판정하지 않는다.
- FAT와 SAT의 일부 시험항목이 중복된다는 설명은 두 시험이 동일하다는 주장과 다르다.
- 조건부 인수 자체는 오류가 아니며 Punch 등급·책임·기한·승인이 없을 때 부족으로 본다.
- Simulation을 FAT에 사용하는 것은 허용되며 실제 현장조건을 완전히 대체한다고 할 때만 오류이다.
- 프로젝트 규모에 따라 문서가 통합될 수 있으나 URS·기능·설계·구현 관점과 추적성은 유지해야 한다.
- Loop test 범위가 최종 요소를 포함하지 않는 프로젝트도 있으므로 문항의 실제 경계를 고려한다.
- Performance test 지표는 공정별로 다르므로 특정 숫자의 누락만으로 오류 처리하지 않는다.
- SW-04·SW-02·SW-03을 비교 설명하는 것은 경계 침범이 아니며 ownership을 혼동할 때만 감점한다.
- 단순 누락은 fatal이 아니며 문항 핵심 요구와 답안 분량에 따라 major 또는 warn으로 평가한다.


## 10. Model Answer 구조

- **1. 프로젝트 목적과 SW-10 소유범위**: 실제 프로젝트 수행과 문서·현장시험·인수의 범위 및 SW-04·SW-02·SW-03 경계를 제시한다.
- **2. Feasibility·Scope·Schedule·Cost**: 프로젝트 착수와 baseline 관리의 판단항목을 설명한다.
- **3. 설계문서 계층과 추적성**: Control philosophy와 URS→FRS→FDS→SDS의 추상화 수준과 추적관계를 설명한다.
- **4. 엔지니어링 목록과 Logic 문서**: I/O·Tag·Alarm·Interlock list, Cause & Effect와 Logic diagram의 역할을 구분한다.
- **5. 시험명세와 FAT·SAT**: 시험명세의 판정기준과 FAT·SAT의 환경·검출결함·한계를 비교한다.
- **6. Loop·현장통합·시운전**: 신호경로, 시스템 간 연동과 단계별 기동 절차를 연결한다.
- **7. 성능시험·인수·Punch closure**: 정량 성능기준, 계약상 인수와 미결항목 폐루프를 설명한다.
- **8. As-built·Handover와 구성보존**: 최종 실제상태, 백업·복구, 증적·교육과 유지보수 이관을 정리한다.


## 11. Focused regression 설계

- Topic source schema와 34개 Anchor의 ID·importance 검증
- 16개 direct wrong claim의 deterministic pattern 검증
- 정정문·인용문과 단순 누락의 false positive 방지
- URS→FRS→FDS→SDS 추적성 관계
- FAT·SAT, Loop·Site integration, Performance·Acceptance 구분
- Commissioning 선행조건과 Punch closure 폐루프
- SW-04·SW-02·SW-03 경계 routing regression

## 12. 통합 단계 이관사항

Lane A에서는 generated bank, 전체 Router, cross-topic duplicate, validate-all, release validation과 container smoke를 수행하지 않는다. 네 Topic 완료 후 Lane 전체 검증과 branch push만 별도 수행하고, generated rebuild와 main 통합은 최종 통합 대화로 넘긴다.
