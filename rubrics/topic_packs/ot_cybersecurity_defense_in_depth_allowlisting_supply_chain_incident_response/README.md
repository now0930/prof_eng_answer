# SW-09 — OT 사이버보안, 심층방어, Allowlisting, 공급망 보안 및 사고대응

- `topic_id`: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response`
- `LANE`: `SOFTWARE_LLM_LANE_B`
- `question_type`: `PROBLEM_SOLVE`
- `difficulty`: `DESIGN_EVALUATION`
- `selection_importance`: `HIGH`

## 범위와 Ownership

SW-09는 OT의 cyber threat, defense in depth, Zone and Conduit, segmentation, Industrial DMZ, Firewall, unidirectional gateway, IDS·IPS, Allowlisting, least privilege, Authentication·Authorization, secure remote access, Patch·Vulnerability, Legacy compensating control, Supply chain, SBOM, Removable media, Logging, Incident response, trusted recovery와 Business continuity를 담당한다.

- **SW-06 경계**: SW-06은 일반 Configuration·MOC·Release·Backup·Rollback·Migration 운영체계를 담당한다. SW-09는 위협에 견디는 backup, compromised state 제거와 trusted recovery를 담당한다.
- **SW-07 경계**: SW-07은 Protocol 구조·기능, 물리매체, Device Profile과 상호운용성을 담당한다. SW-09는 Authentication, encryption, access control, Firewall와 intrusion response를 담당한다.
- **SW-08 경계**: SW-08은 Latency, Jitter, Determinism, 시간동기 정확도, 장애복구시간과 network resilience를 담당한다. SW-09는 malicious action에 대한 탐지·격리·eradication·trusted recovery를 담당한다.

## 대표 문제

1. IT 보안과 OT 보안의 차이를 가용성, 안전 및 공정연속성 관점에서 설명하시오.
2. IEC 62443의 Zone and Conduit 개념을 활용한 OT 심층방어 구조를 설명하시오.
3. Industrial DMZ, Firewall 및 Unidirectional gateway의 역할과 적용조건을 비교하시오.
4. OT 환경의 Application Allowlisting, Least privilege, Authentication 및 Authorization을 설명하시오.
5. Vendor 원격 유지보수에 Jump server, MFA와 Session recording을 적용하는 방안을 제시하시오.
6. Legacy 제어시스템의 Patch 및 Vulnerability 관리와 Compensating control을 설명하시오.
7. OT 공급망 보안에서 Supplier assurance, SBOM과 Firmware integrity의 관계를 설명하시오.
8. 이동식매체, Logging, 시간동기화와 침해탐지 관리방안을 설명하시오.
9. OT Cyber incident의 Detection, Containment, Eradication 및 Recovery 절차를 설명하시오.
10. Ransomware에 대비한 Backup, Trusted recovery와 Business continuity 방안을 제시하시오.

## 핵심 Fact Anchor

- **sw09_security_objectives** — OT 보안은 기밀성만이 아니라 가용성, 안전, 무결성, 공정연속성 및 복구가능성을 함께 보호하며 통제 적용 시 공정위험과 운전제약을 우선 평가해야 한다.
- **sw09_asset_inventory** — Asset inventory는 PLC, DCS, SIS, HMI, historian, engineering workstation, network device, firmware, software, account, communication path와 owner를 식별하고 상태를 최신으로 유지해야 한다.
- **sw09_criticality_classification** — 자산은 공정안전, 생산영향, 복구시간, 외부연결, 취약성 및 대체가능성에 따라 criticality를 분류하여 보호우선순위와 대응수준을 결정해야 한다.
- **sw09_risk_assessment** — OT cyber risk assessment는 threat, vulnerability, consequence, existing safeguard와 residual risk를 공정 시나리오와 연결하고 허용기준 및 처리계획을 정해야 한다.
- **sw09_system_under_consideration** — 보안 설계는 보호대상 System under Consideration의 경계, 기능, data flow, trust boundary, 외부의존성과 책임조직을 먼저 정의해야 한다.
- **sw09_zone_conduit** — Zone and conduit는 유사한 보안요구와 기능을 가진 자산을 Zone으로 묶고 Zone 간 허용 통신을 Conduit로 제한하여 trust boundary와 정책집행점을 만든다.
- **sw09_segmentation** — Segmentation은 업무·제어·안전·원격접속·무선·vendor 영역의 blast radius와 lateral movement를 줄이도록 논리·물리 경계를 설계하고 우회경로를 차단해야 한다.
- **sw09_industrial_dmz** — Industrial DMZ는 IT와 OT 사이의 직접 세션을 최소화하고 historian relay, patch staging, remote access broker와 file transfer 같은 중계기능을 분리 배치해야 한다.
- **sw09_firewall_policy** — Firewall 정책은 default deny를 기반으로 source, destination, service, direction, purpose, owner와 expiry를 문서화하고 rule review와 로그검증으로 최소허용을 유지해야 한다.
- **sw09_unidirectional_gateway** — Unidirectional gateway는 물리적 단방향 data flow가 필요한 경계에서 attack path를 줄이지만 데이터반환, 제어명령, 유지보수와 가용성 요구를 별도로 설계해야 한다.
- **sw09_ids_ips_monitoring** — IDS와 IPS는 protocol, asset baseline, anomaly와 signature를 이용해 탐지·차단을 보조하지만 tuning, false positive, fail-open/fail-close와 공정영향을 검증해야 한다.
- **sw09_allowlisting** — Application allowlisting은 승인된 executable, script, library와 실행조건만 허용하여 미승인 코드 실행을 줄이며 update, emergency change와 learning mode를 통제해야 한다.
- **sw09_least_privilege** — Least privilege는 사용자, service, application과 device에 업무수행에 필요한 최소권한·최소기간만 부여하고 정기 review와 privileged activity monitoring을 수행해야 한다.
- **sw09_authentication** — Authentication은 사용자·장치·서비스의 신원을 검증하는 과정이며 credential 보호, account lifecycle, lockout와 exception handling을 포함해야 한다.
- **sw09_authorization** — Authorization은 인증된 주체가 수행할 수 있는 action과 resource를 role, attribute 또는 policy로 제한하며 separation of duties를 고려해야 한다.
- **sw09_remote_access** — Remote access는 business need, 승인, time window, source, destination, protocol과 session owner를 제한하고 direct inbound exposure를 피해야 한다.
- **sw09_jump_server** — Jump server는 remote user와 OT target 사이의 관리경로를 집중시키며 hardened host, isolated credential, logging, malware control과 session termination을 제공해야 한다.
- **sw09_mfa** — MFA는 특히 remote와 privileged access의 account takeover 위험을 줄이지만 target authorization, endpoint trust, session control과 recovery 절차를 대체하지 않는다.
- **sw09_secure_remote_session** — 원격 접속은 암호화, 명시적 승인, 강한 인증, 최소권한, file transfer 통제, concurrent session 제한, inactivity timeout과 비상차단을 적용하고, 위험도·접속방식·대상 장치의 기술적 특성에 따라 화면 기록, 명령 기록, protocol transaction log, engineering change audit 또는 jump server session recording 중 적절한 수단이나 조합으로 모든 접속·변경행위를 사용자·시간·대상·결과와 연결하여 재구성 가능한 audit trail을 확보해야 한다.
- **sw09_patch_management** — OT patch management는 vulnerability severity뿐 아니라 exploitability, exposure, safety·availability 영향, vendor support, test evidence, outage window와 rollback을 평가하여 우선순위를 정해야 한다.
- **sw09_vulnerability_management** — Vulnerability management는 discovery, validation, risk ranking, remediation·mitigation, exception approval, verification와 closure evidence를 반복 수행해야 한다.
- **sw09_legacy_compensating_control** — Legacy system이 patch, MFA 또는 modern protocol을 지원하지 못하면 segmentation, allowlisting, access broker, monitoring, physical control와 reduced service 같은 compensating control을 위험기반으로 적용해야 한다.
- **sw09_secure_configuration_baseline** — Secure configuration baseline은 service, port, account, protocol, logging, removable media와 security feature의 승인상태를 정의하고 drift를 탐지해야 한다.
- **sw09_security_change_control** — 보안 관련 변경은 SW-06의 일반 MOC·Release 절차와 연계하되 threat exposure, rule impact, credential, logging, rollback와 emergency exception을 보안관점에서 검토해야 한다.
- **sw09_supply_chain_risk** — Supply chain risk management는 supplier, integrator, component, update channel, subcontractor와 service dependency의 위협을 식별하고 계약·검증·대체전략으로 관리해야 한다.
- **sw09_supplier_assurance** — Supplier assurance는 secure development, vulnerability disclosure, update support, remote support, breach notification, provenance와 end-of-life 책임을 계약 및 evidence로 확인해야 한다.
- **sw09_sbom** — SBOM은 software component와 dependency 식별을 지원하지만 vulnerability 존재여부, exploitability, configuration, runtime exposure와 authenticity를 별도 검증해야 한다.
- **sw09_software_firmware_integrity** — Software와 firmware는 trusted source, hash·digital signature, secure transfer, version compatibility, rollback protection와 installation evidence로 무결성과 출처를 확인해야 한다.
- **sw09_removable_media** — Removable media는 승인매체, owner, purpose, write protection, scanning station, content hash, transfer log, quarantine와 disposal 절차로 통제해야 한다.
- **sw09_logging** — Logging은 authentication, privilege use, configuration change, remote session, security alert, process anomaly와 recovery action을 source identity와 결과까지 기록해야 한다.
- **sw09_time_synchronization_forensics** — 보안 로그와 packet·process event는 공통 time source, clock health와 timezone policy를 유지하여 사건순서와 인과관계를 재구성할 수 있어야 한다.
- **sw09_detection_triage** — Detection과 triage는 network, endpoint, authentication, process deviation와 operator report를 correlation하여 severity, scope, safety impact와 false positive를 신속히 판단해야 한다.
- **sw09_incident_response_plan** — Incident response plan은 역할, 연락체계, decision authority, safety coordination, evidence handling, vendor interface, legal·regulatory escalation과 communication을 사전 정의해야 한다.
- **sw09_containment_eradication** — Containment는 확산과 공정위험을 제한하고 eradication은 persistence, malicious account, altered logic와 compromised component를 제거하며 각각 운전영향을 평가해야 한다.
- **sw09_trusted_recovery** — Trusted recovery는 clean baseline, verified backup, credential reset, integrity check, staged restore, heightened monitoring와 acceptance criterion을 통해 신뢰 가능한 상태로 복구해야 한다.
- **sw09_backup_recovery_security** — 보안 목적 Backup은 offline 또는 immutable copy, 분리 credential, retention, encryption, malware exposure 관리와 정기 restore test를 포함해야 한다.
- **sw09_business_continuity** — Business continuity는 cyber incident 중 안전정지, local control, manual operation, reduced production, alternate communication과 recovery priority를 정의해야 한다.
- **sw09_safety_coordination** — Cyber response는 SIS·interlock·emergency shutdown의 독립성과 기능을 유지하고 안전담당자 승인 없이 보호기능을 우회하거나 비활성화해서는 안 된다.
- **sw09_exercise_metrics** — Tabletop, technical drill과 recovery exercise는 realistic scenario로 역할·의사결정·통신·복구를 시험하고 MTTD, MTTC(Mean Time to Contain: 탐지 시점 또는 조직이 공식적으로 사용하는 사고 선언 시점부터 영향받은 Zone·Account·Remote Session·Network Path 등의 확산 경로가 차단되고 추가 전파가 억제된 시점까지), recovery success와 overdue action을 개선지표로 관리해야 한다.
- **sw09_lifecycle_decommissioning** — 자산 폐기·교체 시 account, certificate, key, remote path, license, data, backup, supplier access와 inventory record를 제거·갱신하여 잔존 attack path를 없애야 한다.

## 핵심 Fatal 오류

- **sw09_fatal_it_controls_direct**: IT 보안통제는 가용성·안전·운전영향 검토 없이 OT에 그대로 즉시 적용해야 한다.
  - 교정: OT는 공정안전과 가용성 제약을 포함해 위험기반으로 통제를 적용해야 한다.
- **sw09_fatal_inventory_optional**: 자산목록이 없어도 방화벽과 백신만 있으면 OT 보안관리가 가능하다.
  - 교정: 자산·버전·연결·owner를 알아야 위험과 통제를 관리할 수 있다.
- **sw09_fatal_flat_network_safe**: Flat network는 통신이 단순하므로 segmentation보다 보안성이 높다.
  - 교정: Segmentation과 zone-conduit로 lateral movement와 blast radius를 줄여야 한다.
- **sw09_fatal_dmz_any_any**: Industrial DMZ가 있으면 IT와 OT 사이 any-any 양방향 연결도 안전하다.
  - 교정: DMZ는 직접세션을 줄이고 중계서비스와 최소허용 정책을 적용해야 한다.
- **sw09_fatal_firewall_perimeter_only**: 경계 Firewall 한 대가 있으면 내부 access control과 monitoring은 불필요하다.
  - 교정: 심층방어는 경계·내부구간·endpoint·identity·monitoring 통제를 결합한다.
- **sw09_fatal_ids_prevents_all**: IDS 또는 IPS를 설치하면 모든 침해가 자동 예방되고 tuning도 필요 없다.
  - 교정: 탐지·차단 한계와 false positive, 공정영향을 검증해야 한다.
- **sw09_fatal_allowlisting_solves_all**: Allowlisting을 적용하면 malware, insider와 공급망 위험이 모두 제거된다.
  - 교정: Allowlisting은 미승인 실행을 줄이는 한 계층이며 유지관리와 다른 통제가 필요하다.
- **sw09_fatal_shared_admin**: 운영편의를 위해 모든 엔지니어가 공용 administrator 계정을 사용하는 것이 적절하다.
  - 교정: 개인 식별계정, least privilege, 역할분리와 privileged activity monitoring이 필요하다.
- **sw09_fatal_auth_equals_authz**: Authentication에 성공하면 Authorization 검토 없이 모든 제어명령을 허용해도 된다.
  - 교정: 신원검증과 권한결정을 분리하고 최소권한을 적용해야 한다.
- **sw09_fatal_direct_vendor_access**: Vendor가 인터넷에서 PLC로 상시 직접 접속하게 하면 신속한 유지보수와 보안을 동시에 달성한다.
  - 교정: 승인된 시간제 remote access, jump server, MFA, 기록과 target 제한이 필요하다.
- **sw09_fatal_mfa_only**: MFA만 적용하면 endpoint 상태와 session 통제 없이도 remote access가 완전히 안전하다.
  - 교정: MFA는 endpoint trust, authorization, session monitoring과 결합해야 한다.
- **sw09_fatal_patch_immediate_universal**: 최신 patch는 시험과 rollback 준비 없이 모든 OT 자산에 즉시 적용해야 한다.
  - 교정: Exploitability와 운전영향, vendor support, test와 rollback을 평가해야 한다.
- **sw09_fatal_legacy_no_control**: Legacy system은 기능제약 때문에 보안통제를 전혀 적용할 수 없다.
  - 교정: Segmentation, allowlisting, broker, monitoring과 physical control 같은 보완통제를 적용한다.
- **sw09_fatal_compensating_zero_risk**: Compensating control을 하나 적용하면 원래 취약점의 residual risk는 0이 된다.
  - 교정: 보완통제의 coverage와 residual risk를 평가하고 정기 검증해야 한다.
- **sw09_fatal_sbom_proves_secure**: SBOM이 제공되면 제품의 모든 component가 신뢰되고 취약점이 없다는 뜻이다.
  - 교정: SBOM은 구성요소 가시성을 제공할 뿐 위험·진위·노출은 별도 검증한다.
- **sw09_fatal_signed_is_safe**: Digital signature가 유효한 firmware는 취약점과 악성기능이 절대 없다.
  - 교정: 서명은 출처와 무결성의 한 증거이며 보안성과 호환성은 별도 검토한다.
- **sw09_fatal_usb_scan_complete**: 이동식매체를 백신으로 한 번 검사하면 이후 사용과 이동경로는 통제할 필요가 없다.
  - 교정: 승인·격리·hash·transfer log·재검사와 폐기까지 관리해야 한다.
- **sw09_fatal_logs_without_time**: 장치별 시간이 달라도 로그파일만 모으면 사건순서와 원인을 정확히 재구성할 수 있다.
  - 교정: 공통 time source와 clock health가 포렌식 timeline에 필요하다.
- **sw09_fatal_online_backup_ransomware**: 운영망에 항상 연결된 writable backup만 있으면 ransomware와 destructive attack 복구가 보장된다.
  - 교정: Offline·immutable copy, 분리 credential과 restore test가 필요하다.
- **sw09_fatal_restore_equals_eradication**: Backup restore가 성공하면 persistence, stolen credential과 altered logic도 자동 제거되어 incident가 종결된다.
  - 교정: Containment·eradication·credential reset·integrity verification 후 trusted recovery를 수행해야 한다.

## Warn/Major 수준의 부족한 표현

- **sw09_major_asset_scope_missing**: 자산목록을 언급하지만 firmware, account, data flow, owner와 criticality가 빠진다.
  - 보완: 물리·논리 자산, 책임자와 공정중요도를 함께 관리한다.
- **sw09_major_zone_conduit_missing**: 방화벽 제품만 나열하고 Zone, Conduit, trust boundary와 허용 data flow가 없다.
  - 보완: SUC와 data flow를 기준으로 구역·경계를 설계한다.
- **sw09_major_remote_session_missing**: MFA만 제시하고 jump server, 승인시간, target 제한 또는 사용자·시간·대상·결과를 재구성할 수 있는 활동기록·audit trail이 없다.
  - 보완: Remote session의 시작부터 종료까지 통제하고, 접속방식에 적합한 화면·명령·transaction·engineering change·jump server 기록 중 적절한 수단 또는 조합으로 사용자·시간·대상·결과가 연결되는 재구성 가능한 audit trail을 확보한다.
- **sw09_major_patch_exception_missing**: Patch 적용만 설명하고 시험, outage, rollback, exception과 보완통제가 없다.
  - 보완: 위험기반 patch decision과 미적용 보완책을 제시한다.
- **sw09_major_legacy_control_missing**: Legacy 문제를 언급하지만 compensating control과 residual risk 관리가 없다.
  - 보완: 기술제약에 맞는 다층 보완통제를 설계한다.
- **sw09_major_supply_contract_missing**: 공급망 위험을 언급하지만 계약요건, provenance, support와 breach notification이 없다.
  - 보완: Supplier assurance evidence와 책임을 계약화한다.
- **sw09_major_sbom_use_missing**: SBOM을 요구하지만 vulnerability correlation, exposure와 update action으로 연결하지 않는다.
  - 보완: SBOM을 위험판정과 response workflow에 연결한다.
- **sw09_major_media_workflow_missing**: USB 금지만 제시하고 승인, scanning station, transfer log와 exception이 없다.
  - 보완: 사용 가능한 통제 workflow를 설계한다.
- **sw09_major_logging_usecase_missing**: 로그 수집만 제시하고 time sync, retention, correlation, alert와 response owner가 없다.
  - 보완: 탐지 use case와 forensic evidence 요구를 정의한다.
- **sw09_major_incident_role_missing**: Incident 단계는 나열하지만 운전·안전·보안·vendor 역할과 decision authority가 없다.
  - 보완: 역할·연락·승인·evidence handling을 사전 정의한다.
- **sw09_major_trusted_restore_missing**: Backup은 언급하지만 offline/immutable copy, credential 분리, restore test와 clean recovery가 없다.
  - 보완: 공격에 견디는 backup과 trusted recovery를 검증한다.
- **sw09_major_exercise_metric_missing**: 정책과 절차만 있고 tabletop, technical drill, recovery exercise와 개선지표가 없거나, MTTC를 확장어와 측정 시작·종료 경계 없이 약어로만 나열한다.
  - 보완: 훈련결과와 MTTD, MTTC(Mean Time to Contain: 탐지 또는 공식 사고 선언부터 확산 경로 차단과 추가 전파 억제 완료까지), 복구성공률을 개선조치로 연결한다.

## False positive 주의사항

- Availability와 safety를 우선한다고 해서 confidentiality를 무시한 것으로 단정하지 말고 위험균형을 설명했는지 확인한다.
- Zone이 반드시 물리적으로 분리되어야 하는 것은 아니며 논리통제와 독립성이 요구를 충족하면 인정한다.
- 모든 OT 경계에 DMZ가 필요한 것은 아니므로 data flow와 trust boundary에 따른 대안을 인정한다.
- Firewall에서 일부 양방향 세션을 허용해도 업무목적·최소범위·상태추적이 명확하면 무조건 오류로 보지 않는다.
- Unidirectional gateway가 적합하지 않은 양방향 제어·유지보수 요구에서는 다른 통제를 선택한 답안을 인정한다.
- IPS를 inline으로 쓰지 않아도 공정위험 때문에 passive IDS를 선택하고 대응절차를 갖추면 인정한다.
- Allowlisting이 모든 장치에 적용되지 않아도 지원대상·예외·보완통제가 명확하면 인정한다.
- MFA를 적용하지 못하는 legacy target은 jump server에서 강제하고 내부권한을 제한하는 설계를 인정한다.
- 화면 녹화가 없더라도 Engineering Change Audit과 Protocol Transaction Log로 사용자·시간·대상·결과가 충분히 추적되면 원격 활동기록 누락으로 판정하지 않는다.
- GUI가 없는 장치에서 Command Log와 Session Metadata로 동일 수준의 추적성과 재구성 가능한 Audit Trail을 확보한 경우를 인정한다.
- MTTC 대신 Mean Time to Contain, Time to Containment, Containment Completion Time 또는 확산 억제 완료시간을 사용해도 측정 시작·종료 경계를 명확히 제시하면 동등 표현으로 인정한다.
- Patch를 즉시 적용하지 않아도 exploitability, exposure, 시험과 compensating control 근거가 있으면 인정한다.
- SBOM 형식이나 표준명이 달라도 component·version·dependency와 vulnerability response에 활용하면 인정한다.
- Removable media를 완전 금지하지 않아도 승인된 operational workflow와 evidence가 있으면 인정한다.
- Backup이 online copy를 포함해도 별도 offline 또는 immutable recovery tier와 분리 credential이 있으면 인정한다.
- Containment를 위해 network isolation을 사용해도 safety·availability 평가와 eradication 후속절차가 있으면 인정한다.
- Business continuity에서 hold-last 또는 manual mode를 제시해도 hazard analysis와 시간제한이 있으면 인정한다.
- SW-06 변경·Backup, SW-07 통신, SW-08 복원력을 언급해도 cyber threat와 control 관점의 근거로 제한되면 범위이탈로 보지 않는다.

## Question pattern

- **sw09_qp_security_difference**: IT와 OT 보안의 목적·제약·우선순위 차이를 설명하는 문제
- **sw09_qp_architecture**: Asset inventory, risk assessment, Zone and Conduit 기반 심층방어 구조를 설계하는 문제
- **sw09_qp_dmz_boundary**: Industrial DMZ, Firewall와 Unidirectional gateway의 역할·선정조건을 비교하는 문제
- **sw09_qp_access_control**: Allowlisting, least privilege, authentication과 authorization을 설명하는 문제
- **sw09_qp_remote_access**: Vendor remote access에 Jump server, MFA와 session control을 적용하는 문제
- **sw09_qp_patch_legacy**: Patch·Vulnerability 관리와 Legacy compensating control을 설계하는 문제
- **sw09_qp_supply_chain**: Supply chain, supplier assurance, SBOM과 firmware integrity를 설명하는 문제
- **sw09_qp_media_monitoring**: Removable media, logging, time synchronization과 detection을 설계하는 문제
- **sw09_qp_incident_response**: OT incident의 detection·containment·eradication·recovery 절차를 설명하는 문제
- **sw09_qp_recovery_continuity**: Cyber resilient backup, trusted recovery와 business continuity를 설계하는 문제

## Routing alias

- OT 사이버보안 심층방어 공급망 사고대응
- operational technology defense in depth incident response
- OT asset inventory zone conduit security architecture
- industrial DMZ firewall unidirectional gateway design
- OT application allowlisting least privilege access control
- industrial remote access jump server MFA session recording
- OT patch vulnerability legacy compensating control
- industrial control system supply chain risk management
- SBOM firmware integrity vendor assurance for control systems
- removable media logging monitoring incident triage OT
- OT cyber incident containment eradication trusted recovery
- offline immutable backup business continuity industrial control
- IEC 62443 zone conduit security level architecture
- NIST SP 800-82 OT security controls
- PLC DCS SIS cybersecurity segmentation
- vendor remote maintenance security control
- OT privileged access management engineering workstation
- industrial cybersecurity tabletop recovery exercise
- legacy PLC security compensating safeguards
- cyber safety coordination SIS interlock protection
- OT security monitoring forensic timeline time synchronization
- supply chain SBOM vulnerability disclosure support lifecycle
- industrial control ransomware recovery clean baseline
- OT defense architecture risk assessment data flow
- ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response

## 모범답안

### 1. 보안목표와 자산경계

OT는 생산과 안전을 직접 제어하므로 기밀성만이 아니라 가용성, 무결성, 안전과 복구가능성을 함께 보호해야 한다. 먼저 PLC, DCS, SIS, HMI, historian, engineering workstation, network device, firmware, account와 data flow를 inventory화한다. 공정영향과 복구우선순위로 criticality를 정하고 SUC와 trust boundary를 확정한다.

### 2. 위험평가와 심층방어

Threat, vulnerability, consequence와 existing safeguard를 공정 시나리오에 연결한다. 유사한 보안요구의 자산을 Zone으로 구성하고 Zone 간 허용 통신만 Conduit로 통제한다. Segmentation은 lateral movement와 blast radius를 줄이며 물리·논리 우회경로와 common access path까지 확인해야 한다.

### 3. 경계통제와 감시

IT와 OT 사이 직접세션을 줄이기 위해 Industrial DMZ에 historian relay, patch staging, remote access broker와 file transfer 기능을 분리한다. Firewall은 default deny와 업무목적·owner·expiry를 가진 최소허용 rule로 운영한다. 필요한 경우 unidirectional gateway를 적용하고 IDS·IPS는 false positive와 공정영향을 검증한다.

### 4. Endpoint·Identity·Remote access

Engineering workstation과 server에는 Application Allowlisting과 secure baseline을 적용한다. 사용자·service·application에는 least privilege를 적용하고 Authentication과 Authorization을 구분한다. Vendor 원격접속은 승인된 time window에 Jump server와 MFA를 거쳐 수행하며, 위험도와 접속방식에 적합한 화면·명령·transaction·engineering change·jump server 기록 중 적절한 수단 또는 조합으로 활동을 추적하고 file transfer 통제와 emergency termination을 적용한다.

### 5. Patch·Legacy·공급망

Patch와 vulnerability는 CVSS만이 아니라 exploitability, exposure, safety·availability 영향, vendor support, 시험과 rollback을 종합해 처리한다. Patch가 불가능한 legacy system은 segmentation, allowlisting, access broker, monitoring과 physical control로 보완한다. Supplier에는 secure development, vulnerability disclosure, update support와 breach notification을 계약하고 SBOM과 firmware provenance를 검증한다.

### 6. 이동식매체와 탐지

Removable media는 승인매체, scanning station, write protection, content hash, transfer log와 quarantine으로 통제한다. Authentication, privileged action, configuration change, remote session, network alert와 process anomaly를 기록한다. 모든 event는 공통 time source와 clock health를 이용해 correlation하고 triage에서 scope, severity와 safety impact를 판단한다.

### 7. 사고대응과 안전조정

Incident response plan에는 운전·안전·보안·vendor의 역할과 decision authority를 정의한다. Detection 후 containment로 확산과 공정영향을 제한하고 eradication으로 persistence, malicious account와 altered logic을 제거한다. 대응 중 SIS, interlock과 emergency shutdown의 독립성을 유지하고 evidence를 보존한다.

### 8. Trusted recovery와 지속성

Restore는 incident 종결과 같지 않다. Offline 또는 immutable backup, 분리 credential, clean baseline, integrity check, credential reset과 staged restore를 통해 trusted recovery를 수행한다. Business continuity에는 안전정지, local·manual operation, reduced production과 recovery priority를 포함한다. Tabletop과 technical drill로 MTTD와 MTTC(Mean Time to Contain)를 관리하며, MTTC의 시작은 탐지 또는 공식 사고 선언, 종료는 확산 경로 차단과 추가 전파 억제 완료로 정의하고 restore success와 미완료 개선조치를 함께 관리한다.

## Focused regressions

- Metadata와 schema version 일관성
- 40개 Fact Anchor 및 20개 Fatal 계약
- Deterministic check 비활성화와 LLM semantic verification
- C 계층 single-owner score contract
- Zone·Conduit·DMZ·Allowlisting·Jump server·MFA·SBOM·Incident response 정확성
- SW-06·SW-07·SW-08 ownership 경계
- Topic Sheet 12개 section과 전체 모범답안
- 정확히 7개 source 파일 및 EOF newline
