# Topic Sheet — 형상관리, 변경관리, Release, Backup, Rollback, Migration 및 Obsolescence 관리

## 1. Topic metadata

- Topic ID: `configuration_change_release_backup_rollback_migration_obsolescence_management`
- SW 번호: `SW-06`
- Lane: `SOFTWARE_LLM_LANE_B`
- Question type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `NORMAL`
- Grading mode: semantic LLM verification
- Deterministic checks: disabled
- Candidate extraction rules: empty
- Fact Anchor: 40
- Fatal: 20
- Major/Warn: 12
- Expected question patterns: 10
- Recommended outline: 8

### Ownership

- SW-04: 요구사항, 설계, 구현, 개발 시험, 독립 V&V와 개발 수명주기
- SW-06: 운영 형상, MOC, Release, Regression, Backup, Restore, Rollback, Migration와 Obsolescence
- SW-09: 보안위협, 인증·접근통제, 방화벽, 악성코드, 공급망 공격과 사이버 사고대응

## 2. Scope and representative questions

### 포함 범위

- Configuration Item와 형상식별
- Baseline과 Version control
- 형상상태기록과 As-built consistency
- Management of Change
- Impact analysis와 위험기반 승인
- Release package와 승인 Artifact
- Risk-based Regression과 현장 인수
- Backup, Restore, Rollback과 Disaster recovery
- Migration discovery, compatibility, data transformation
- Cutover, Parallel operation와 post-cutover stabilization
- Legacy, Obsolescence, Spare, Vendor lock-in, License와 Firmware compatibility
- 긴급변경, 문서화, 교육과 지식이전

### 대표 문제

- 산업용 제어시스템의 형상관리와 변경관리 절차를 설명하시오.
- Configuration Item과 Baseline의 개념 및 As-built consistency 확보방법을 설명하시오.
- 제어시스템 Software Release 관리절차와 Release package의 구성항목을 설명하시오.
- 변경 작업 시 Backup, Restore 및 Rollback의 차이와 적용절차를 설명하시오.
- PLC·DCS 변경 후 Regression 시험범위와 현장 인수기준을 설명하시오.
- Legacy 제어시스템 Migration 절차와 Cutover 시 고려사항을 설명하시오.
- Big-bang, 단계적 전환 및 Parallel operation을 비교하고 선정기준을 제시하시오.
- 제어시스템 Obsolescence 관리와 예비품·Firmware·License 수명주기 대책을 설명하시오.
- Vendor lock-in 위험과 장기 운전연속성 확보방안을 설명하시오.
- 긴급변경과 일반변경의 MOC 통제 차이 및 사후관리 방법을 설명하시오.

## 3. Core correct facts

1. `sw06_configuration_item_scope` — Configuration Item(CI)은 식별·변경·상태기록의 통제를 받아야 하는 하드웨어, 소프트웨어, 펌웨어, 설정값, 화면, 데이터 구조, 인터페이스, 문서와 라이선스 등의 관리 단위이다.
2. `sw06_configuration_identification_relationship` — 형상식별은 CI의 고유 식별자, 버전, 위치, 소유자, 의존관계, 승인상태와 적용 설비를 추적할 수 있게 정의하는 활동이다.
3. `sw06_baseline_approved_reference` — Baseline은 검토와 승인을 거쳐 이후 변경의 기준이 되는 특정 시점의 형상 집합이며 단순히 가장 최신 파일이나 최근 백업을 뜻하지 않는다.
4. `sw06_version_control_status_accounting` — Version control은 변경 이력과 작성자를 기록하는 도구이고, 형상상태기록은 승인·배포·설치·폐기 상태까지 보고해야 하므로 Version control만으로 전체 형상관리가 완성되지는 않는다.
5. `sw06_as_built_consistency` — As-built consistency는 저장소의 승인 형상, 현장에 실제 설치된 형상, 백업본과 관련 문서가 서로 일치하고 그 차이를 설명할 수 있는 상태이다.
6. `sw06_moc_trigger_and_scope` — Management of Change(MOC)는 운전·안전·품질·환경·보안·유지보수 또는 규제 영향이 있는 영구·임시·긴급 변경을 식별하고 통제하는 운영 절차이다.
7. `sw06_change_request_problem_objective` — 변경요청은 현상, 변경 목적, 대상 CI, 기대효과, 위험, 우선순위, 요청자와 완료기준을 명확히 해야 한다.
8. `sw06_impact_analysis_multidisciplinary` — Impact analysis는 변경 대상뿐 아니라 연동 로직, 통신, HMI, historian, 보고서, 알람, 안전기능, 절차, 교육, 예비품, 라이선스와 복구계획에 미치는 영향을 다학제적으로 검토해야 한다.
9. `sw06_risk_based_approval_authority` — 변경 승인권한과 검토 깊이는 위험도, 설비 중요도, 변경 범위와 가역성에 따라 정하고 요청·검토·승인·배포 역할을 가능한 범위에서 분리한다.
10. `sw06_change_implementation_plan` — 변경 실행계획은 작업 순서, 인력, 도구, 운전조건, 정지창, 통신방법, 백업, 검증, 중단기준, Rollback과 책임자를 포함해야 한다.
11. `sw06_pre_change_backup_restore_readiness` — 변경 전 Backup은 대상 CI와 의존 데이터를 포함해 복구 가능한 형태로 확보하고, 사용 도구·버전·권한·매체와 Restore 절차의 실행 가능성을 확인해야 한다.
12. `sw06_release_package_content` — Release package는 승인된 실행물과 source, 버전·checksum, 변경목록, 의존성, 설치절차, 시험결과, Backup·Rollback 절차, 알려진 제약과 승인기록을 포함해야 한다.
13. `sw06_release_control_authorized_artifact` — Release control은 승인된 동일 artifact만 지정 환경에 배포되도록 식별·보관·전달·설치·확인하고 임의 재빌드 또는 현장 직접수정을 방지하는 활동이다.
14. `sw06_risk_based_regression` — Regression은 변경이 기존 기능과 인터페이스를 훼손하지 않았는지 확인하는 위험기반 재시험이며, 영향분석으로 범위를 정하고 변경 기능·인접 기능·핵심 운전 시나리오를 포함한다.
15. `sw06_release_acceptance_and_asbuilt_update` — Release 완료는 설치 성공만이 아니라 기능·알람·인터페이스·운전성 확인, 이상 유무 감시, 문서와 As-built 갱신, 사용자 인수와 변경종결을 포함한다.
16. `sw06_rollback_preplanned_criteria` — Rollback은 변경 전 정의한 trigger, 허용시간, 복귀대상 baseline, 데이터 처리, 책임자와 의사결정권한에 따라 수행하는 계획된 이전 형상 복귀이다.
17. `sw06_restore_rollback_distinction` — Restore는 Backup으로부터 데이터·설정·시스템을 재구성하는 복구 행위이고, Rollback은 변경을 철회하여 승인된 이전 release 또는 baseline으로 되돌리는 변경관리 결정이다.
18. `sw06_irreversible_change_forward_recovery` — 데이터 변환, 장비 교체 또는 외부 인터페이스 변경처럼 완전한 Rollback이 불가능한 변경은 사전에 가역성 한계를 밝히고 checkpoint, reconciliation, forward recovery 또는 대체운전 방안을 준비해야 한다.
19. `sw06_backup_scope_and_consistency` — Backup 범위는 프로그램 파일뿐 아니라 설정, 레시피, 데이터베이스, 화면, 인증서·키의 적절한 보관정보, 펌웨어, 드라이버, 라이선스, 설치도구와 복구 문서를 포함하고 상호 일관된 시점으로 관리해야 한다.
20. `sw06_backup_integrity_separation_retention` — Backup은 무결성 확인, 접근통제, 원본 장애와 분리된 보관, 세대별 보존과 보존기간을 적용하고 정상본이 손상본으로 덮어써지지 않게 관리해야 한다.
21. `sw06_restore_test_recovery_evidence` — Backup의 유효성은 정기적인 Restore 시험 또는 대표 복구훈련으로 확인하고 복구시간, 누락 의존성, 절차 오류와 결과 증적을 기록해야 한다.
22. `sw06_disaster_recovery_objectives` — Disaster recovery는 시스템 중요도와 공정 허용중단에 따라 복구 우선순위, 목표 복구시간, 허용 데이터 손실, 대체운전, 인력·장비·예비품과 통신체계를 정의한다.
23. `sw06_migration_discovery_dependency_inventory` — Migration은 기존 시스템의 CI, 인터페이스, 데이터, timing, custom logic, 운전절차, 라이선스, 예비품과 숨은 의존성을 먼저 조사하여 범위와 제약을 확정해야 한다.
24. `sw06_compatibility_matrix` — Migration과 upgrade 전에는 하드웨어, OS, application, firmware, driver, protocol option, database와 license의 지원 조합을 Compatibility matrix로 확인해야 한다.
25. `sw06_data_configuration_transformation_validation` — 데이터·설정 Migration은 mapping, 변환규칙, 단위·범위·encoding, 누락·중복 처리, checksum·record count·sample 비교와 운전 의미 검증을 포함해야 한다.
26. `sw06_migration_strategy_selection` — Migration 방식은 일괄 Cutover, 단계적 전환, Parallel operation, pilot 또는 hybrid 중 공정 중단 허용시간, 인터페이스 복잡도, 가역성, 비용과 위험을 비교하여 선정한다.
27. `sw06_parallel_operation_controls` — Parallel operation은 결과 비교와 복귀 여지를 제공하지만 이중 입력, 제어권 충돌, 데이터 불일치, 운전자 혼란과 공통원인 오류를 통제해야 한다.
28. `sw06_cutover_freeze_gonogo` — Cutover 전에는 변경 freeze, 최종 동기화, Backup, readiness checklist, 승인, 연락망, go/no-go 기준, Rollback 가능시간과 공정 안전조건을 확인해야 한다.
29. `sw06_post_cutover_stabilization_decommission` — Cutover 후에는 성능·알람·통신·데이터 정합성을 집중 감시하고 안정화 기준을 충족한 뒤 기존 시스템을 보존·격리·폐기하며 기록과 책임을 종결한다.
30. `sw06_legacy_system_risk_based_management` — Legacy system은 오래되었다는 이유만으로 즉시 폐기하거나 무기한 유지할 대상이 아니라 고장·지원·보안·예비품·지식·호환성·중단위험을 평가하여 유지, 보강, 격리, 교체 또는 Migration을 결정한다.
31. `sw06_obsolescence_proactive_process` — Obsolescence 관리는 단종 공지 이후 구매하는 활동이 아니라 수명주기 상태를 감시하고 영향·발생시점·대안을 평가하여 사전 계획하는 지속적 프로세스이다.
32. `sw06_obsolescence_mitigation_options` — Obsolescence 대응은 last-time buy, lifetime buy, repair, approved substitute, redesign, emulation, cannibalization, service contract와 Migration을 위험·비용·기간에 따라 조합한다.
33. `sw06_spare_lifecycle_management` — 예비품 관리는 수량뿐 아니라 호환 버전, 저장환경, 주기시험, 배터리·콘덴서 열화, firmware·license, 수리 가능성, 위치와 사용이력을 관리해야 한다.
34. `sw06_vendor_lockin_lifecycle_risk` — Vendor lock-in은 특정 공급자 종속 자체를 금지하는 개념이 아니라 데이터·설정 export, open interface, 대체품, 서비스조건, 소스·도구 접근성과 전환비용을 관리해야 하는 수명주기 위험이다.
35. `sw06_license_entitlement_continuity` — License 관리는 entitlement, 버전·장비 귀속, dongle·server 의존성, 갱신기한, 비상복구, 가상화·이전 권한과 공급자 종료 시 사용권을 확인하여 운전 연속성을 확보해야 한다.
36. `sw06_firmware_compatibility_control` — Firmware는 최신 버전 여부보다 승인된 하드웨어 revision, engineering tool, application, communication module과의 호환성, 변경내용, 복귀 가능성과 시험결과를 기준으로 선정한다.
37. `sw06_documentation_training_knowledge_retention` — 변경·Release·Migration 후에는 도면, cause and effect, alarm list, network·I/O list, backup 절차, 운영·정비 절차와 교육자료를 갱신하고 지식이 특정 개인에게만 남지 않게 해야 한다.
38. `sw06_emergency_change_retrospective_control` — 긴급변경은 안전과 생산복구를 위해 승인절차를 단축할 수 있지만 최소 권한·기록·Backup·검증·통신을 유지하고 사후 정식 검토와 baseline 반영을 해야 한다.
39. `sw06_sw04_boundary` — SW-06은 운영 중인 승인 형상의 변경·Release·복구·Migration 통제를 담당하고, 요구사항 개발, 설계검증, 독립 V&V와 개발 수명주기 자체는 SW-04가 담당한다.
40. `sw06_sw09_boundary` — SW-06의 Backup·Recovery는 운영 형상과 변경 복구체계를 중심으로 하고, 공격·침해·악성코드 대응, 보안통제와 사이버 사고복구는 SW-09가 담당한다.

## 4. Acceptable answer expressions

- Baseline은 최신본이 아니라 승인된 특정 형상 집합이다.
- Version control은 형상관리의 도구이지만 MOC와 Release control을 대체하지 않는다.
- 변경 크기가 작아도 공정 영향이 크면 강화된 영향분석과 검증이 필요하다.
- 저위험 표준변경은 승인된 표준절차에 따라 간소화할 수 있다.
- 긴급변경은 절차를 단축할 수 있으나 최소 기록과 사후검토가 필요하다.
- Backup 성공과 Restore 성공은 구분하며 정기적인 복구시험이 필요하다.
- Restore는 복구 행위이고 Rollback은 이전 승인 형상으로 복귀하는 변경관리 결정이다.
- Rollback이 불가능한 데이터 변환은 forward recovery와 reconciliation을 준비한다.
- Backup 범위는 프로그램뿐 아니라 설정, 데이터, firmware, tool과 license를 포함할 수 있다.
- 온라인 Backup도 보호와 분리가 충분하면 유효할 수 있으나 원본 장애와 독립된 사본을 검토한다.
- Regression 범위는 영향분석과 위험도에 따라 정하며 모든 변경에 무조건 전체시험을 요구하지 않는다.
- Release 완료에는 설치 후 확인, As-built 갱신과 사용자 인수가 포함된다.
- Parallel operation은 필수 방식이 아니며 공정 중단과 인터페이스 위험에 따라 선택한다.
- Big-bang Cutover도 충분한 준비와 Rollback 조건이 있으면 적절할 수 있다.
- 최신 firmware도 승인된 Compatibility matrix와 시험을 거치면 적용할 수 있다.
- Legacy system 유지도 보상통제와 수명주기 계획이 있으면 합리적일 수 있다.
- Vendor-specific 기능 사용 자체가 오류는 아니며 장기 지원성과 exit 조건을 관리한다.
- Last-time buy는 하나의 Obsolescence 완화수단이지만 저장수명과 장기대안을 함께 검토한다.
- RTO와 RPO는 시스템 중요도와 공정 허용중단에 맞게 정한다.
- SW-04의 V&V 산출물은 SW-06 Release acceptance의 입력으로 사용할 수 있다.
- 변경복구 목적의 Backup은 SW-06이 중심이고 침해사고 대응 목적은 SW-09가 중심이다.
- Rollback 과정에서 Backup Restore를 사용할 수 있으므로 두 개념은 연관되지만 동일하지 않다.
- License는 기술구성의 일부이자 법적 사용권이므로 복구와 Migration에서 확인한다.
- 현장 Download가 필요한 경우에도 승인 artifact와 설치 후 버전을 대조해야 한다.

## 5. Fatal wrong claims

1. **가장 최신 파일이나 최근 백업이 자동으로 승인 Baseline이다.**
   교정: Baseline은 식별된 형상 집합이 검토·승인되어 변경 기준으로 지정된 상태여야 한다.
2. **Version control을 사용하면 별도의 MOC, 영향분석과 승인이 필요 없다.**
   교정: Version control은 이력 도구이며 MOC의 위험평가, 승인, 실행·복구·종결 통제를 대체하지 않는다.
3. **설비가 정상 운전 중이면 저장소와 현장 형상의 불일치는 문제가 아니다.**
   교정: 운전 여부와 별개로 승인본·설치본·문서·백업의 일치성과 차이 추적이 필요하다.
4. **Setpoint나 한 줄 로직 같은 작은 변경은 영향분석과 Regression이 불필요하다.**
   교정: 변경 크기만으로 위험을 판단하지 말고 영향받는 기능, 인터페이스와 공정 결과를 기준으로 범위를 정한다.
5. **긴급변경은 기록, Backup, 승인과 사후검토를 모두 생략해도 된다.**
   교정: 긴급절차는 단축할 수 있지만 최소 통제와 사후 정식 MOC·Baseline 반영이 필요하다.
6. **실행파일을 현장에 복사하거나 Download하면 Release가 완료된다.**
   교정: 승인 artifact, 의존성, 설치·검증·Rollback, 인수와 As-built 갱신까지 통제해야 한다.
7. **같은 source를 현장에서 다시 build하면 승인된 Release artifact와 동일하다고 볼 수 있다.**
   교정: Build 환경과 dependency 차이를 고려하여 승인된 checksum·서명·artifact를 그대로 배포해야 한다.
8. **Backup 파일이 존재하거나 작업 로그가 성공이면 복구 가능성이 보장된다.**
   교정: Backup 범위·무결성·도구·라이선스·의존성을 확인하고 Restore 시험으로 복구성을 입증해야 한다.
9. **Restore와 Rollback은 동일한 행위이며 구분할 필요가 없다.**
   교정: Restore는 백업 기반 복구 행위이고 Rollback은 변경을 철회하여 이전 승인 형상으로 복귀하는 관리 결정이다.
10. **Rollback 계획은 장애가 발생한 후 이전 파일을 찾아 복사하면 충분하다.**
   교정: 변경 전에 trigger, 시간제한, 대상 baseline, 데이터 처리와 의사결정권한을 정해야 한다.
11. **모든 변경은 이전 파일만 다시 설치하면 데이터와 외부 인터페이스까지 완전히 복구된다.**
   교정: 비가역 변경은 checkpoint, reconciliation, forward recovery와 대체운전을 사전에 준비해야 한다.
12. **공간 절약을 위해 항상 최신 Backup 한 벌만 남기고 이전 세대는 덮어쓰는 것이 최선이다.**
   교정: 손상·오배포가 정상본을 덮어쓸 수 있으므로 세대별 보존과 분리·무결성 통제가 필요하다.
13. **Disaster recovery는 Backup 저장 위치만 정하면 완성된다.**
   교정: 복구 우선순위, 목표시간·데이터손실, 자원, 대체운전, 통신과 훈련이 함께 필요하다.
14. **새 시스템이 부팅되고 화면이 열리면 Migration은 성공이다.**
   교정: 기능, 인터페이스, 알람, 데이터·설정 정합성, 성능, 운전 인수와 안정화 기준을 확인해야 한다.
15. **OS, application, firmware와 driver를 각각 최신으로 올리면 상호 호환성이 자동 보장된다.**
   교정: 지원 Compatibility matrix와 통합시험으로 승인된 조합을 확인해야 한다.
16. **신·구 시스템을 동시에 연결해 Parallel operation하면 항상 안전성과 신뢰성이 높아진다.**
   교정: 제어권 충돌, 이중입력, 데이터 불일치와 운전자 혼란을 통제할 때만 장점을 얻을 수 있다.
17. **Cutover 일정이 승인되면 readiness, Backup 또는 Rollback 조건이 미충족이어도 진행해야 한다.**
   교정: Go/no-go 기준과 공정 안전조건을 충족하지 못하면 연기 또는 중단해야 한다.
18. **Legacy system은 모두 즉시 교체해야 하거나, 현재 운전 중이므로 무기한 유지해도 된다.**
   교정: 지원성·안전·가용성·비용·교체위험을 비교하여 유지·보강·교체·Migration을 결정한다.
19. **Obsolescence 관리는 Vendor EOL 공지가 나온 뒤 예비품을 사는 활동이다.**
   교정: 수명주기 상태, lead time, 영향과 완화대안을 사전에 감시·계획하는 지속 프로세스다.
20. **최신 firmware는 항상 가장 안전하고 호환성이 높으므로 시험 없이 즉시 적용해야 한다.**
   교정: 하드웨어 revision, engineering tool, 통신모듈, release note, downgrade 가능성과 시험결과를 확인해야 한다.

## 6. Warn-level weak claims

1. **CI 목록은 제시했으나 버전·소유자·설비 매핑·의존관계가 없다.**
   보강: CI 간 관계와 설치대상까지 추적해야 형상식별이 완성된다.
2. **MOC 절차를 승인 단계 중심으로만 설명하고 영향분석 범위를 제시하지 않는다.**
   보강: 연동 로직·통신·운전·안전·문서·복구 영향까지 연결한다.
3. **Backup 주기와 매체는 설명했으나 Restore 시험과 복구 증적이 없다.**
   보강: 대표 복구훈련으로 도구·의존성·복구시간을 확인한다.
4. **Rollback 필요성은 언급했으나 trigger, 허용시간, 대상 baseline과 의사결정권한이 없다.**
   보강: 사전 go/no-go 및 중단 기준을 구체화한다.
5. **Release package와 시험은 설명했으나 설치 후 As-built 갱신과 변경종결이 없다.**
   보강: 현장 버전 확인, 문서 갱신, 사용자 인수와 종결을 포함한다.
6. **변경 후 시험한다고만 쓰고 변경 기능·인접 기능·핵심 운전 시나리오의 범위를 제시하지 않는다.**
   보강: 영향분석 기반 risk-based regression 범위를 제시한다.
7. **Migration 절차는 설명했으나 기존 interface, custom logic, tool, license와 숨은 의존성 조사가 없다.**
   보강: Discovery와 compatibility matrix를 전환 이전에 수행한다.
8. **데이터를 이관한다고만 쓰고 mapping, 단위·encoding, record count와 sample 비교가 없다.**
   보강: 정량·정성 reconciliation 기준을 둔다.
9. **Parallel operation의 장점만 설명하고 어느 시스템이 최종 제어권을 갖는지 정하지 않는다.**
   보강: 전환규칙, 제어권, 이중입력 방지와 운영절차를 명확히 한다.
10. **Obsolescence 대책을 예비품 구매로만 제시한다.**
   보강: 저장수명·시험·수리·대체품·redesign·Migration과 장기 비용을 함께 비교한다.
11. **Vendor lock-in을 비용 문제로만 설명하고 데이터 export, tool 접근, 대체품과 전환계획을 제시하지 않는다.**
   보강: 계약·아키텍처·데이터 portability로 exit 가능성을 관리한다.
12. **Migration·복구계획에서 software license, dongle, license server와 이전권한을 누락한다.**
   보강: 기술적 복구와 법적 entitlement를 함께 확인한다.

## 7. False positive cautions

- ‘최신 firmware가 항상 옳지 않다’는 설명과 검증 후 최신 firmware를 채택하는 설명을 구분한다.
- Parallel operation을 선택하지 않았다는 이유만으로 Migration 답안을 오답 처리하지 않는다.
- 전체 Regression을 하지 않았다는 이유만으로 오답 처리하지 말고 영향분석 기반 범위가 있는지 본다.
- Emergency change의 expedited approval을 무승인 변경과 동일하게 보지 않는다.
- Backup이 온라인이라는 사실만으로 부적절하다고 단정하지 말고 분리·접근통제·세대보존을 본다.
- Rollback 불가를 인정하고 forward recovery를 준비한 답안을 오답 처리하지 않는다.
- Vendor-specific solution을 사용했다는 이유만으로 Vendor lock-in 관리 실패로 판정하지 않는다.
- Legacy system을 유지한다는 이유만으로 오답 처리하지 말고 위험평가와 보상통제를 확인한다.
- Restore와 Rollback을 함께 설명한 답안은 목적 구분이 있으면 정답으로 인정한다.
- SW-04의 V&V 용어를 언급해도 Release acceptance와 연결한 경우 SW-06 경계 위반으로 보지 않는다.
- SW-09의 보안 Backup을 언급해도 주된 논지가 운영 변경복구이면 SW-06 답안으로 인정할 수 있다.
- Cold, warm, hot standby 또는 DR site의 명칭은 시스템 맥락 없이 단정적으로 채점하지 않는다.
- Checksum, signature, hash 중 하나를 사용해 artifact 동일성을 설명하면 동등 표현으로 인정한다.
- MOC의 승인단계를 조직 규모에 맞게 간소화한 답안은 위험기반 근거가 있으면 인정한다.
- Obsolescence 대책으로 예비품을 제시한 것 자체는 맞으며 그것만으로 충분하다고 단정할 때만 부족으로 본다.

## 8. Routing aliases and regex candidate patterns

### Routing aliases

- `형상관리 변경관리 릴리스 백업 롤백`
- `configuration management change management release rollback`
- `configuration item baseline version control`
- `관리 기준선 형상항목 버전관리`
- `Management of Change MOC software change`
- `제어시스템 변경 승인 영향분석`
- `release control release package deployment`
- `PLC DCS software release management`
- `backup restore rollback disaster recovery`
- `제어시스템 백업 복구 롤백`
- `as-built configuration consistency`
- `현장 프로그램 저장소 일치성`
- `migration cutover parallel operation`
- `시스템 마이그레이션 컷오버 병행운전`
- `legacy system migration management`
- `레거시 시스템 전환`
- `obsolescence management lifecycle`
- `단종 노후화 수명주기 관리`
- `firmware compatibility matrix`
- `펌웨어 호환성 버전 조합`
- `vendor lock-in license lifecycle`
- `벤더 종속 라이선스 관리`
- `spare lifecycle last time buy`
- `예비품 수명주기 단종 대응`
- `configuration_change_release_backup_rollback_migration_obsolescence_management`

### Narrow regex candidates

아래 정규식은 검토 후보 추출용이다. Hit만으로 Fatal을 확정하지 않는다.

- `(?i)(baseline).*(latest|newest|최근).*(같|동일|자동)`
- `(?i)(version control|git).*(MOC|change management).*(불필요|대체)`
- `(?i)(backup).*(있|성공).*(restore|복구).*(보장|완료)`
- `(?i)(restore).*(rollback).*(같|동일)`
- `(?i)(latest|최신).*(firmware|driver|OS).*(always|항상).*(compatible|호환)`
- `(?i)(migration|cutover).*(boot|화면).*(성공|완료)`
- `(?i)(parallel operation|병행운전).*(always|항상).*(safe|안전|reliable|신뢰)`
- `(?i)(legacy).*(always|모두).*(replace|교체|유지)`
- `(?i)(obsolescence|단종).*(EOL|공지).*(후|이후).*(시작|관리)`
- `(?i)(emergency change|긴급변경).*(record|기록|approval|승인).*(불필요|생략)`

Negation, 인용, 반론, 조건절과 문맥을 반드시 확인한다.

## 9. fact_anchor.json generation guidance

- Schema: `fact_anchor.v1`
- Root keys: schema_version, topic_id, title_ko, question_type_hint, anchors, fatal_wrong_claims, safe_expressions, revision_notes, topic_label, core_facts
- Anchor ID는 repository 전체에서 unique해야 한다.
- `id`와 `anchor_id`는 동일하게 둔다.
- Importance는 `core` 또는 `important`를 사용한다.
- 각 Anchor에 statement, keywords, core_terms, accepted_explanations, rejected_explanations, grading_notes와 source_basis를 둔다.
- core_facts는 Anchor statement와 동일한 순서를 유지한다.
- Fatal은 severity=`fatal`, affected_layers=`["C"]`로 둔다.

## 10. logic_check.json generation guidance

- Schema: `topic_pack.logic_check.v1`
- deterministic_checks.enabled=false
- deterministic fatal_checks와 major_checks는 빈 배열
- topic_aliases는 SW-06 좁은 표현만 사용
- llm_profile.enabled=true
- candidate_extraction.rules=[]
- candidate_extraction.key_terms는 CI·Baseline·MOC·Release·Backup·Rollback·Migration·Obsolescence 맥락을 충분히 포함
- truth_schema는 Anchor statement와 동일한 순서
- Fatal 20개는 반드시 answer evidence와 context를 확인
- Major 12개는 핵심 방향은 맞지만 조건·절차·검증이 누락된 경우에만 적용
- direct_score_application=false
- C가 correctness의 canonical owner
- D와 E에 Logic Check 결과를 직접 반영하지 않는다.

## 11. model_answer.json and topic_importance.json guidance

### model_answer.json

- Schema: `topic_pack.model_answer.v1`
- question_type: `IMPLEMENTATION_EVALUATION`
- expected_question_patterns: 10개 rich object
- recommended_outline: 8개 object
- high_score_points: 15개
- common_missing_points: 14개
- routing_aliases: 25개
- routing_field_points: 32개
- Broad `software`, `lifecycle`, `V&V`, `cybersecurity`, `network` 단독 alias 금지
- 모든 required_anchor_ids와 anchor_refs는 SW-06 local Anchor만 참조

### Question patterns

- `sw06_qp_configuration_management`: 형상관리, CI, Baseline, Version control과 As-built consistency를 묻는 문제
  Required anchors: `sw06_configuration_item_scope`, `sw06_configuration_identification_relationship`, `sw06_baseline_approved_reference`, `sw06_version_control_status_accounting`, `sw06_as_built_consistency`
- `sw06_qp_moc_procedure`: 변경관리 또는 MOC 절차와 영향분석·승인을 묻는 문제
  Required anchors: `sw06_moc_trigger_and_scope`, `sw06_change_request_problem_objective`, `sw06_impact_analysis_multidisciplinary`, `sw06_risk_based_approval_authority`, `sw06_change_implementation_plan`, `sw06_emergency_change_retrospective_control`
- `sw06_qp_release_control`: Release package, 배포, Regression과 인수를 묻는 문제
  Required anchors: `sw06_release_package_content`, `sw06_release_control_authorized_artifact`, `sw06_risk_based_regression`, `sw06_release_acceptance_and_asbuilt_update`
- `sw06_qp_backup_restore_rollback`: Backup, Restore, Rollback과 Disaster recovery를 비교하는 문제
  Required anchors: `sw06_pre_change_backup_restore_readiness`, `sw06_rollback_preplanned_criteria`, `sw06_restore_rollback_distinction`, `sw06_backup_scope_and_consistency`, `sw06_backup_integrity_separation_retention`, `sw06_restore_test_recovery_evidence`, `sw06_disaster_recovery_objectives`
- `sw06_qp_migration_process`: Legacy system Migration 절차와 데이터·설정 이관을 묻는 문제
  Required anchors: `sw06_migration_discovery_dependency_inventory`, `sw06_compatibility_matrix`, `sw06_data_configuration_transformation_validation`, `sw06_migration_strategy_selection`, `sw06_cutover_freeze_gonogo`, `sw06_post_cutover_stabilization_decommission`
- `sw06_qp_parallel_operation`: Big-bang, 단계적 전환과 Parallel operation을 비교하는 문제
  Required anchors: `sw06_migration_strategy_selection`, `sw06_parallel_operation_controls`, `sw06_cutover_freeze_gonogo`, `sw06_rollback_preplanned_criteria`
- `sw06_qp_legacy_obsolescence`: Legacy와 Obsolescence 수명주기 관리대책을 묻는 문제
  Required anchors: `sw06_legacy_system_risk_based_management`, `sw06_obsolescence_proactive_process`, `sw06_obsolescence_mitigation_options`, `sw06_spare_lifecycle_management`
- `sw06_qp_vendor_license_firmware`: Vendor lock-in, License와 Firmware compatibility를 묻는 문제
  Required anchors: `sw06_vendor_lockin_lifecycle_risk`, `sw06_license_entitlement_continuity`, `sw06_firmware_compatibility_control`, `sw06_compatibility_matrix`
- `sw06_qp_emergency_change`: 긴급변경의 통제와 사후검토를 묻는 문제
  Required anchors: `sw06_moc_trigger_and_scope`, `sw06_change_implementation_plan`, `sw06_pre_change_backup_restore_readiness`, `sw06_emergency_change_retrospective_control`
- `sw06_qp_ownership_boundary`: SW-04 개발 V&V 및 SW-09 보안사고대응과의 경계를 묻는 문제
  Required anchors: `sw06_risk_based_regression`, `sw06_sw04_boundary`, `sw06_sw09_boundary`, `sw06_disaster_recovery_objectives`

### Recommended outline

1. **1. 배경과 필요성** — 제어시스템은 장기간 운전되며 작은 변경도 공정·안전·품질에 영향을 주므로 승인된 형상과 복구 가능성을 유지해야 한다.
   Anchor refs: `sw06_configuration_item_scope`, `sw06_moc_trigger_and_scope`, `sw06_legacy_system_risk_based_management`
2. **2. 형상 기준선** — CI 식별, Baseline 승인, Version control, 상태기록과 As-built consistency의 관계를 설명한다.
   Anchor refs: `sw06_configuration_identification_relationship`, `sw06_baseline_approved_reference`, `sw06_version_control_status_accounting`, `sw06_as_built_consistency`
3. **3. 변경관리 절차** — 변경요청, 영향분석, 위험기반 승인, 실행계획과 긴급변경의 사후통제를 제시한다.
   Anchor refs: `sw06_change_request_problem_objective`, `sw06_impact_analysis_multidisciplinary`, `sw06_risk_based_approval_authority`, `sw06_change_implementation_plan`, `sw06_emergency_change_retrospective_control`
4. **4. Release와 Regression** — Release package, 승인 artifact, risk-based Regression, 현장 인수와 As-built 갱신을 연결한다.
   Anchor refs: `sw06_release_package_content`, `sw06_release_control_authorized_artifact`, `sw06_risk_based_regression`, `sw06_release_acceptance_and_asbuilt_update`
5. **5. Backup·Restore·Rollback** — 변경 전 Backup, 세대·무결성 관리, Restore 시험, Rollback 기준과 비가역 변경대책을 구분한다.
   Anchor refs: `sw06_pre_change_backup_restore_readiness`, `sw06_rollback_preplanned_criteria`, `sw06_restore_rollback_distinction`, `sw06_irreversible_change_forward_recovery`, `sw06_backup_integrity_separation_retention`, `sw06_restore_test_recovery_evidence`
6. **6. Migration과 Cutover** — Discovery, Compatibility matrix, 데이터 변환, 전환방식, Parallel operation, go/no-go와 안정화를 설명한다.
   Anchor refs: `sw06_migration_discovery_dependency_inventory`, `sw06_compatibility_matrix`, `sw06_data_configuration_transformation_validation`, `sw06_migration_strategy_selection`, `sw06_parallel_operation_controls`, `sw06_cutover_freeze_gonogo`, `sw06_post_cutover_stabilization_decommission`
7. **7. Legacy·Obsolescence 관리** — 위험기반 Legacy 판단, proactive Obsolescence, 예비품, Vendor lock-in, License와 Firmware 수명주기를 설명한다.
   Anchor refs: `sw06_legacy_system_risk_based_management`, `sw06_obsolescence_proactive_process`, `sw06_obsolescence_mitigation_options`, `sw06_spare_lifecycle_management`, `sw06_vendor_lockin_lifecycle_risk`, `sw06_license_entitlement_continuity`, `sw06_firmware_compatibility_control`
8. **8. 운영 종결과 경계** — 문서·교육·지식이전, 변경종결과 SW-04·SW-09 ownership 경계를 명시한다.
   Anchor refs: `sw06_documentation_training_knowledge_retention`, `sw06_sw04_boundary`, `sw06_sw09_boundary`

### topic_importance.json

- Schema: `topic_pack.topic_importance.v1`
- difficulty: `DESIGN_EVALUATION`
- selection_importance: `NORMAL`
- question_type: `IMPLEMENTATION_EVALUATION`
- High band는 형상-변경-Release-복구-Migration-Obsolescence를 단순 나열하지 않고 운영 폐루프로 연결해야 한다.
- SW-04와 SW-09 경계를 명시해야 한다.

## 모범답안

### 1. 개요

산업용 제어시스템은 PLC, DCS, SCADA, HMI, historian, 통신장치와 현장기기로 구성되며 수십 년간 운전된다. 이 기간에 Logic, Setpoint, Alarm, Firmware, OS, Driver, License와 Hardware가 반복적으로 변경된다. 따라서 운영 이후의 핵심은 최신 기술을 무조건 적용하는 것이 아니라 승인된 형상을 식별하고, 변경 위험을 통제하며, 실패 시 복구할 수 있는 상태를 유지하는 것이다.

### 2. 형상관리

Configuration Item은 식별과 변경통제가 필요한 관리 단위이다. 프로그램 Source와 실행물뿐 아니라 Firmware, 설정값, HMI 화면, Recipe, Database schema, Interface, 도면, 절차서와 License도 포함할 수 있다. 각 CI에는 고유 ID, Version, Owner, 설치설비, 의존관계와 승인상태를 부여한다.

Baseline은 검토와 승인을 거쳐 이후 변경의 기준이 된 특정 형상 집합이다. 가장 최근 파일이나 최근 Backup과 같지 않다. Version control은 변경 이력을 보존하는 도구이지만 승인, 배포, 설치상태와 As-built consistency까지 자동으로 보장하지 않는다. 따라서 저장소 승인본, 현장 설치본, Backup과 문서의 Version 또는 Checksum을 주기적으로 대조한다.

### 3. 변경관리와 Release

MOC는 변경요청, 영향분석, 위험기반 승인, 실행계획, 사전 Backup, 설치, Regression, 현장 인수와 종결의 순서로 수행한다. 영향분석은 변경 대상 Logic뿐 아니라 연동설비, HMI, Alarm, Historian, 통신, 안전기능, 운전절차, 교육, License와 복구방안까지 검토한다.

Release package에는 승인된 Source와 실행물, Version·Checksum, 변경목록, 의존성, 설치절차, 시험결과, 알려진 제약, Backup·Rollback 절차와 승인기록을 포함한다. 현장에서는 승인 Artifact와 설치 후 Version을 확인한다. Regression은 모든 기능을 무조건 재시험하는 절차가 아니라 영향분석에 따라 변경 기능, 인접 기능, Interface와 핵심 운전 시나리오를 재확인하는 위험기반 시험이다. 이는 개발 수명주기와 독립 V&V를 담당하는 SW-04와 구분된다.

### 4. Backup, Restore와 Rollback

Backup은 프로그램 파일뿐 아니라 설정, Recipe, Database, Firmware, Driver, Engineering tool, License와 복구문서를 일관된 시점으로 보존해야 한다. Backup은 무결성, 접근통제, 원본 장애와의 분리, 세대보존과 보존기간을 관리한다. Backup 작업 성공만으로 복구 가능성이 보장되지 않으므로 정기적인 Restore 시험과 복구훈련으로 도구, 의존성, 복구시간과 절차를 검증한다.

Restore는 Backup으로부터 시스템이나 데이터를 재구성하는 행위이다. Rollback은 변경을 철회하고 이전 승인 Release 또는 Baseline으로 되돌리는 관리결정이다. Rollback trigger, 허용시간, 대상 Baseline, 데이터 처리와 의사결정권한은 변경 전에 정한다. 비가역 데이터 변환이나 장비교체는 Forward recovery, Checkpoint, Reconciliation과 대체운전을 준비한다.

### 5. Migration과 Cutover

Migration은 먼저 기존 CI, Interface, Data, Timing, Custom logic, License와 숨은 의존성을 조사한다. Hardware, OS, Application, Firmware, Driver, Database와 License 조합은 Compatibility matrix로 확인한다. Data와 Configuration은 Mapping, 단위, 범위, Encoding, Record count, Checksum과 Sample 비교로 정합성을 검증한다.

전환방식은 Big-bang, 단계적 전환, Parallel operation 또는 Pilot 중 공정 중단시간, 위험, 비용, Interface 복잡도와 가역성을 비교하여 선택한다. Parallel operation은 결과 비교와 복귀 가능성을 제공하지만 이중입력, 제어권 충돌, 데이터 불일치와 운전자 혼란을 통제해야 한다. Cutover 전에는 Change freeze, 최종 동기화, Backup, Readiness checklist, Go/No-go 기준과 Rollback window를 확인한다. 전환 후에는 Alarm, 통신, 성능과 Data 정합성을 집중 감시한 뒤 안정화 기준을 충족하고 기존 시스템을 보존·격리·폐기한다.

### 6. Legacy와 Obsolescence 관리

Legacy system은 오래되었다는 이유만으로 즉시 교체하거나 운전 중이라는 이유로 무기한 유지하지 않는다. 지원종료, 고장률, 예비품, 지식, 호환성, License, 보안과 중단위험을 평가하여 유지, 보강, 격리, 교체 또는 Migration을 결정한다.

Obsolescence 관리는 Vendor EOL 공지 이후 대응하는 활동이 아니다. 수명주기 상태와 Lead time을 지속적으로 감시하고 Last-time buy, Repair, Substitute, Redesign, Emulation, Service contract와 Migration을 비용·위험·기간에 따라 조합한다. Spare는 수량 외에도 저장환경, 주기시험, 열화, Firmware와 License 호환성을 관리한다. Vendor lock-in은 특정 Vendor 사용 자체의 오류가 아니라 Data export, Open interface, Tool 접근성, 대체품, 계약조건과 전환비용을 관리해야 하는 수명주기 위험이다.

### 7. 긴급변경과 경계

긴급변경은 승인절차를 단축할 수 있으나 최소 권한, 기록, Backup, 검증과 통신을 유지하고 사후 정식 MOC와 Baseline 반영을 수행한다. 변경 후에는 도면, Alarm list, Network·I/O list, Backup 절차, 운영·정비 절차와 교육자료를 갱신한다.

SW-06은 운영 이후의 형상·변경·Release·복구·Migration을 담당한다. 요구사항 개발, 설계검증과 독립 V&V는 SW-04가 담당한다. Backup이 보안사고 대응과 침해복구를 중심으로 제시되면 SW-09가 담당하며, SW-06은 운영 변경 실패와 시스템 장애에 대한 복구관리 체계를 중심으로 평가한다.

### 8. 결론

SW-06의 핵심은 승인된 Baseline을 중심으로 변경 전 위험을 분석하고, 동일한 Release를 재현 가능하게 배포하며, Backup의 Restore 가능성과 Rollback 조건을 입증하고, Legacy·Obsolescence를 장기 수명주기 관점에서 관리하는 것이다. 이를 통해 변경으로 인한 비계획 정지와 As-built 불일치를 줄이고 제어시스템의 운전연속성을 확보한다.


## 12. Human review checklist

- [ ] Topic ID와 SW 번호가 정확하다.
- [ ] SW-04를 개발 수명주기와 V&V owner로 남겼다.
- [ ] SW-09를 보안위협과 사이버 사고대응 owner로 남겼다.
- [ ] CI와 Baseline을 최신 파일과 구분했다.
- [ ] Version control과 MOC·Release control을 구분했다.
- [ ] Backup 성공과 Restore 성공을 구분했다.
- [ ] Restore와 Rollback을 구분했다.
- [ ] Rollback trigger와 비가역 변경대책이 있다.
- [ ] Migration에 dependency와 compatibility matrix가 있다.
- [ ] Data reconciliation과 Cutover go/no-go가 있다.
- [ ] Parallel operation의 제어권 위험을 설명했다.
- [ ] Obsolescence를 proactive lifecycle process로 설명했다.
- [ ] Spare, Vendor lock-in, License와 Firmware compatibility가 포함되었다.
- [ ] Deterministic checks가 disabled이다.
- [ ] Candidate rules가 비어 있다.
- [ ] Fatal은 C layer single owner이다.
- [ ] Generated, Router, production과 다른 Topic을 수정하지 않는다.
