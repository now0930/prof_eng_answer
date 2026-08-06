# SW-04 Topic Sheet

## 1. Topic 식별

- Topic ID: `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`
- 한글 주제: 계측제어 소프트웨어 수명주기, V-Model, 추적성, 검증 및 확인
- Lane ownership: SOFTWARE_LLM_LANE_A
- Question type: PROCEDURE
- Difficulty: DESIGN_EVALUATION
- Selection importance: CORE_MUST_PREPARE

## 2. 포함 범위

SW-04는 일반 계측제어 소프트웨어의 개발 수명주기와 V&V 체계를 소유한다. 요구사항에서 시작하여 아키텍처, 상세설계, 구현, 단위·통합·시스템시험, 추적성, 결함·변경관리와 승인 증적으로 연결한다.

### 포함

- Requirement specification
- System architecture와 Software architecture
- Detailed design와 Coding standard
- Unit, Integration, System test
- Verification와 Validation
- Requirement Traceability Matrix
- Static analysis와 Dynamic analysis
- Regression test
- Simulation, HIL와 Fault injection
- Defect management
- Review, Approval와 V&V evidence

### 제외

- SIL 산정, PFDavg·PFH, Safety Integrity, Safety independence와 체계적 고장 통제는 SW-05
- FAT·SAT·Loop test·시운전·성능시험·Acceptance·Handover는 SW-10
- HMI·SCADA Alarm·SOE와 운전자 권한은 SW-03
- Sequence·Interlock·Trip 상태전이와 Fail-safe 운전논리는 SW-02

## 3. V-Model 핵심

V-Model은 문서를 순서대로 만드는 그림이 아니다. 좌측에서 정의한 요구사항과 설계결정을 우측의 시험과 확인활동으로 검증하도록 대응시킨다. 시험은 코딩 종료 후 처음 준비하는 것이 아니라 요구사항과 설계가 정해지는 시점부터 목적, 환경, 입력, 예상결과와 판정기준을 준비한다.

```text
사용목적·사용자 요구   ↔ Validation / System test
System requirement     ↔ System verification
System·SW architecture ↔ Integration test
Detailed design        ↔ Unit test
Implementation         ↔ Static·dynamic analysis
```

## 4. Requirements Specification

요구사항은 식별 가능하고 명확하며 일관되고 시험 가능해야 한다. 기능과 성능뿐 아니라 인터페이스, 운전모드, 초기화, 정지·재시작, 예외처리, 통신장애, 데이터 품질, timing과 자원제약을 포함한다.

좋은 요구사항은 다음 요소를 가진다.

- 고유 식별자
- 조건과 trigger
- 입력과 출력
- 정상·비정상 반응
- 측정 단위와 허용오차
- 적용 운전모드
- 검증방법과 acceptance criteria

## 5. Architecture와 Detailed Design

System architecture는 HW·SW·통신·외부시스템의 기능배분, 인터페이스, 데이터흐름과 고장경계를 정의한다. Software architecture는 모듈, task, 상태, 데이터 소유권, 통신, 진단과 자원배분을 정의한다. Detailed design은 알고리즘, 상태전이, I/O 처리, 예외와 경계조건을 구현 가능한 수준으로 구체화한다.

아키텍처 검토에서는 단순 블록 수보다 인터페이스 불일치, timing, race condition, common resource, fault propagation과 recovery path를 확인한다.

## 6. Coding Standard와 Configuration Baseline

Coding standard는 명명과 서식뿐 아니라 자료형, 초기화, 범위, 금지구문, 복잡도, 예외처리, defensive coding, comment와 review 기준을 포함한다. Requirement, design, source, library, compiler, test tool와 환경은 식별된 baseline으로 관리해야 동일 시험을 재현할 수 있다.

## 7. 시험 수준

### Unit test

함수, 모듈, FB 등 최소 설계단위의 정상·경계·오류 경로를 격리해 확인한다. stub, driver와 harness로 외부 의존성을 통제할 수 있다.

### Integration test

모듈·task·통신·DB·장치 interface 사이의 데이터형, 순서, timing, timeout, retry와 오류전파를 확인한다.

### System test

통합된 시스템이 end-to-end 요구사항, 운전모드, 성능, 장애복구와 외부시스템 연계를 충족하는지 확인한다.

## 8. Verification와 Validation

Verification은 산출물이 해당 단계의 명세와 설계기준에 맞는지를 확인한다. Validation은 실제 또는 대표 운전환경에서 시스템이 의도된 사용목적과 사용자 요구를 충족하는지를 확인한다. 한쪽의 성공은 다른 쪽을 자동 보장하지 않는다.

```text
Verification: Are we building the product right?
Validation:   Are we building the right product?
```

## 9. Requirement Traceability Matrix

RTM은 단순 요구사항-시험 번호표가 아니다. Requirement에서 architecture, design, code, test case와 result로 이동하는 순방향 추적과, test result에서 requirement로 돌아가는 역방향 추적을 제공한다.

양방향 추적으로 다음을 찾는다.

- 시험되지 않은 요구사항
- 요구사항 근거가 없는 설계·코드
- 요구사항 근거가 없는 시험
- 변경 후 갱신되지 않은 시험과 결과
- 실패 또는 미실행 상태의 요구사항

## 10. Static·Dynamic·Regression

Static analysis는 프로그램을 실행하지 않고 규칙, control flow, data flow, complexity, 미초기화와 unreachable code를 분석한다. Dynamic analysis는 실제 실행 중 path, timing, memory·resource, interface와 응답을 관찰한다. Regression test는 변경영향 분석을 바탕으로 새 기능과 기존 기능의 비퇴행을 확인한다.

## 11. Simulation·HIL·Fault Injection

Simulation은 plant 또는 device model로 정상·비정상 시나리오를 반복하지만 model fidelity와 가정을 관리해야 한다. HIL은 실제 제어 HW 또는 실행환경을 real-time plant model과 closed loop로 연결하여 I/O, timing, network와 control action을 시험한다.

Fault injection은 sensor open, stuck value, range error, communication delay·loss, corrupted data, power recovery와 task overrun 등을 통제된 환경에서 주입한다. 목적은 단순 실패 유발이 아니라 detection, isolation, fallback, alarm, recovery와 evidence를 확인하는 것이다.

## 12. Defect·Change·Regression 폐루프

실패시험은 삭제하지 않는다. Defect record에는 재현조건, 영향, severity, 원인, 수정버전, 재시험과 closure evidence를 남긴다. Requirement·design·code·environment 변경은 impact analysis, approval, baseline·RTM 갱신과 regression을 거친다.

```text
Defect 발견
→ 원인분석
→ 변경요청과 영향분석
→ 승인
→ 수정과 baseline 갱신
→ 관련 시험·회귀시험
→ RTM 및 증적 갱신
→ closure
```

## 13. Review와 Approval

Review는 역할, 입력자료, 기준, 지적사항과 조치확인을 갖는다. Approval은 승인권자가 exit criteria와 residual defect를 확인한 뒤 산출물 baseline을 승인하는 행위이다. 작성자의 self-check만으로 공식 review와 approval을 대체하지 않는다.

## 14. 대표 Fatal 오답

1. **오답:** Verification과 Validation은 완전히 같은 활동이다.
   - **정정:** Verification은 단계 산출물의 명세 적합성을, Validation은 의도된 사용목적과 사용자 요구 충족을 확인하며 상호보완적이다.

2. **오답:** Validation은 코딩 표준 준수 여부만 확인하는 활동이다.
   - **정정:** 코딩 표준 준수는 Verification의 일부가 될 수 있으나 Validation은 통합 시스템의 사용목적과 사용자 요구 충족을 확인한다.

3. **오답:** V-Model에서는 모든 코딩이 끝난 뒤에 시험을 처음 계획한다.
   - **정정:** V-Model은 개발 초기부터 각 요구사항·설계 단계에 대응하는 시험과 수용기준을 함께 준비한다.

4. **오답:** 요구사항에서 시험 번호로 한 번 연결하면 양방향 RTM이 완성된다.
   - **정정:** RTM은 요구사항에서 설계·코드·시험·결과로의 순방향과 시험·결과에서 요구사항으로의 역방향 추적을 모두 제공해야 한다.

5. **오답:** 모든 단위시험이 통과하면 통합시험과 시스템시험은 필요 없다.
   - **정정:** 단위시험은 최소 설계단위를 검증하며 모듈 상호작용과 end-to-end 요구사항은 통합시험과 시스템시험으로 별도 확인한다.

6. **오답:** 정적분석은 프로그램을 실행하여 입력과 출력을 측정하는 시험이다.
   - **정정:** 정적분석은 프로그램을 실행하지 않고 코드·모델의 규칙, 흐름, 복잡도와 잠재결함을 분석한다.

7. **오답:** 동적분석은 프로그램을 실행하지 않는 문서 검토이다.
   - **정정:** 동적분석은 실행된 소프트웨어의 경로, 시간, 자원과 반응을 입력 조건별로 관찰한다.

8. **오답:** 회귀시험은 새로 추가된 기능만 시험하면 된다.
   - **정정:** 회귀시험은 변경 기능과 함께 영향받을 수 있는 기존 기능·인터페이스의 유지 여부를 확인한다.

9. **오답:** 시뮬레이션 결과는 실제 현장과 항상 완전히 동일하다.
   - **정정:** Simulation은 모델 기반이므로 모델 가정과 한계를 평가하고 필요하면 HIL·현장 단계의 추가 검증으로 보완한다.

10. **오답:** HIL은 반드시 실제 생산설비를 가동해야만 수행할 수 있다.
   - **정정:** HIL은 실제 제어 HW 또는 실행환경을 실시간 plant 모델과 폐루프로 연결하여 실제 plant 가동 없이 HW·SW 상호작용을 검증할 수 있다.

11. **오답:** 결함주입은 파괴시험이므로 소프트웨어 시험에는 사용할 수 없다.
   - **정정:** Fault injection은 통제된 환경에서 센서·통신·전원·데이터·task 이상을 주입해 검출·격리·복구를 검증한다.

12. **오답:** 시험이 실패하면 예상결과를 실제 결과로 바꾸어 통과 처리하면 된다.
   - **정정:** 시험 전 고정한 예상결과와 판정기준을 유지하고 실패는 결함 또는 승인된 요구사항 변경으로 추적해야 한다.

13. **오답:** 코드 리뷰를 수행하면 동적 시험과 시스템시험을 모두 생략할 수 있다.
   - **정정:** Review와 정적분석은 실행 기반 시험을 보완하지만 대체하지 않으며 요구사항 수준에 맞는 동적·통합·시스템 시험이 필요하다.

14. **오답:** 시험결과에 대상 버전과 시험환경을 기록하지 않아도 재현할 수 있다.
   - **정정:** 시험대상 baseline, HW·OS·firmware·tool과 설정을 식별해야 결과의 재현성과 감사가능성을 확보할 수 있다.

15. **오답:** 작은 변경은 영향분석과 회귀시험을 항상 생략할 수 있다.
   - **정정:** 변경 규모와 무관하게 영향범위를 평가하고 그 결과에 따라 RTM·산출물·회귀시험 범위를 갱신해야 한다.

16. **오답:** 일반 소프트웨어 V&V를 완료하면 별도 Safety lifecycle 없이 SIS의 SIL 충족이 자동으로 증명된다.
   - **정정:** SW-04의 일반 V&V와 SW-05의 Safety Integrity, 독립성, 체계적 고장 통제와 Safety V&V를 구분해야 한다.

## 15. 답안 작성 구조

1. SW-04의 목적과 SW-05·SW-10 경계
2. 시험 가능한 Requirement specification
3. V-Model 좌·우 대응
4. Architecture·Detailed design·Coding standard
5. Unit·Integration·System test
6. Verification·Validation·RTM
7. Static·Dynamic·Regression과 Simulation·HIL·Fault injection
8. Defect·Change·Review·Approval와 증적

## 16. Focused regression 관점

- 직접 오답 문장만 deterministic fatal pattern과 일치한다.
- 인용 뒤 정정한 문장은 fatal로 보지 않는다.
- SW-05 Safety lifecycle 단독 문항과 SW-10 FAT·SAT 단독 문항은 SW-04 routing positive로 보지 않는다.
- V-Model, RTM, 시험수준, 분석·회귀, HIL·Fault injection의 semantic group을 각각 확인한다.
- source JSON 4개와 Markdown, focused test만 Lane A Topic-local commit에 포함한다.
