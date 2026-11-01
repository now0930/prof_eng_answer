# NIST SP 800-82 Rev. 3 — 12 canonical Fact Anchor claim checks (2026-11-01)

Authority: National Institute of Standards and Technology, NIST Special Publication 800-82 Rev. 3 (September 2023); official text and PDF page screenshots compared. URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf

Reviewer: GPT-6 (AI); original source statements read from canonical `rubrics/topic_packs/` branch; check date 2026-11-01. NIST guidance is not generally a legally compulsory rule for every plant or jurisdiction. Only underlying general OT security design principles can inform a general-scoring anchor; editions, specific implementation and checklists should never be promoted merely because a NIST recommendation appears.

## 1. nist_80082r3_application_allowlisting_restricts_host_execution

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_allowlisting`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 application allowlisting을 host에서 실행이 허용된 application을 제한하는 추가 보호수단으로 설명하며, 올바르게 구성하면 비인가 application이 host에서 실행되지 않는다고 명시한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §5.2.5.1 p.77, PDF page index 93 visually inspected
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** KEEP_BOUNDED
- Source-to-claim limitation/counterexample: Allowlisting restricts which applications can execute, subject to correct rules and predeployment testing. Not a universal compulsory security control.

## 2. nist_80082r3_ot_patch_sandbox_window_recovery_plan

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_patch_management`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 가능한 경우 OT patch를 sandbox/test 환경에서 production 전에 시험하고, 환경의 scheduled maintenance window에 적용을 계획하며 대상 OT component/system의 recovery plan을 마련하도록 권고한다. OT zone·tier별 availability 차이는 patch 적용 가능성에도 영향을 준다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §5.2.5.2 p.77–78, PDF index 93 screenshot
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** KEEP_BOUNDED
- Source-to-claim limitation/counterexample: Whenever possible, patch in a test environment, schedule maintenance windows, and plan recovery; exceptions exist where operations and vulnerability severity require other mitigation.

## 3. nist_80082r3_ot_least_privilege_and_separation_of_duties

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_least_privilege`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 RBAC 같은 논리적 접근통제가 separation of duties와 least privilege를 지원하며 OT 사용자 권한을 각자의 업무에 필요한 범위로 제한할 수 있다고 설명한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §6.2.1.1 pp.98–99, PDF index 115 screenshot
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** KEEP_BOUNDED
- Source-to-claim limitation/counterexample: RBAC and role limits can enforce least privilege and separation of duties. Organizational safety access needs may alter controls; not universal RBAC implementation.

## 4. nist_80082r3_ot_network_segmentation_basis_performance_safety

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_segmentation`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 IT·OT 장치를 관리권한, trust level, 기능 중요도, data flow, 위치 등의 기준으로 구분·분리하도록 권고하며, levels·tiers·zones를 이용한 segmentation으로 접근을 제어하면서 운전성능과 안전을 고려한다. Firewall 규칙은 인접 segment 사이의 허용 연결로 제한한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §5.2.1 pp.71–73 and §6.2.1.3 p.102, PDF index 118 screenshot
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** KEEP_BOUNDED
- Source-to-claim limitation/counterexample: Segmentation by function/trust/criticality and explicit allowed inter-zone flows protects OT, subject to performance, safety and system-specific physical/logical architecture.

## 5. nist_80082r3_ot_remote_access_justification_scope_and_revoke

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_remote_access`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 원격접속 요청·활성화 절차를 문서화·공유하고, 정당한 business need가 있는 경우에만 필요한 범위로 제공하며 안전·보안통제를 우회하지 않도록 한다. 필요 종료 후 권한을 제거하고 원격활동을 모니터링하도록 권고한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §6.2.10 pp.122–123, PDF index 139 screenshot
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** KEEP_BOUNDED
- Source-to-claim limitation/counterexample: Remote access should be justified, limited to need, not bypass safety, monitored, and withdrawn when no longer required. NIST recommendation not jurisdiction-neutral legal obligation.

## 6. nist_80082r3_ot_risk_assessment_threat_vulnerability_impact_likelihood

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_risk_assessment`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 OT 위험평가에서 위협과 취약성, 그로 인한 피해 및 불리한 사건의 발생가능성을 식별·평가하고, 물리적·디지털 영향과 공정·안전 영향을 함께 고려하도록 안내한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §4.1.2 p.51, PDF index 67 screenshot
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** KEEP_BOUNDED
- Source-to-claim limitation/counterexample: Risk assessment identifies threats, vulnerabilities, potential harm/impact, and likelihood, including physical process and digital safety consequences.

## 7. nist_80082r3_ot_supply_chain_risks_contracts_assessments_response

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_supply_chain_risk`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 OT 공급망 위험의 예로 counterfeit, 무단 생산, 악의적 내부자, tampering, theft, 악성 software·hardware 삽입과 부실한 제조·개발 관행을 들며, 이를 식별·평가·관리하고 공급자·제3자 계약, 평가, response·recovery planning도 다루도록 한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §6.1.6 p.96, PDF index 112 screenshot
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** KEEP_BOUNDED
- Source-to-claim limitation/counterexample: Supply risks include counterfeit/tampering/malicious component and poor development, and supplier contracts, assessment and response; SBOM and authentication mechanisms are optional examples.

## 8. nist_80082r3_ot_recovery_objectives_and_continuity_plans

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_business_continuity`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 사이버 사고로 인한 중대한 운영중단에 대비해 OT 조직이 Business continuity(BCP)와 재해복구계획(DRP)을 마련하고, 복구목표에서 재가동 전 인명·환경 안전을 우선하도록 설명한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §3.3.9 p.42, PDF index 58 screenshot; §6.2.4.5 p.114–115
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** KEEP_BOUNDED
- Source-to-claim limitation/counterexample: Define recovery objectives, BCP/DRP and safety-first restart. Exact RTO/RPO and plan scope from site function, not universally prescriptive.

## 9. nist_80082r3_ot_recovery_preincident_state_backups_and_plan_tests

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_trusted_recovery`
- **Exact original statement:** Trusted recovery를 위한 NIST SP 800-82 Rev. 3의 OT 복구 권고는 사이버 사고에 손상된 자산·서비스를 사고 전 상태로 되돌리고, 관련 system state·data·configuration·program을 정기 백업하며 복구계획을 조직에 적절한 주기로 시험하도록 한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §3.3.9 p.42–43, PDF index 58; §6.2.4.3 p.113
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** KEEP_BOUNDED
- Source-to-claim limitation/counterexample: Restore necessary OT states/data/configurations/programs with tested backup processes. Actual physical process states may not safely be replayed blindly; preincident digital state is not automatic process restart state.

## 10. nist_80082r3_ot_risk_based_backup_plan_and_immutable_storage

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_backup_recovery_security`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 위험기반 OT backup plan에 백업 대상 파일, 주기, 복제본 수, 위치(예: offline 또는 off-site)와 보존기간을 정하도록 설명하며, immutable storage는 read-only 방식의 데이터 무결성 보강 선택지로 제시한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), Appendix E §E.3.1–E.3.2 pp.210–211, PDF index 227 screenshot
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** KEEP_BOUNDED
- Source-to-claim limitation/counterexample: Backup plan parameters include file types, interval, copies, locations and retention; immutable read-only storage is an OPTIONAL integrity mitigation, not compulsory.

## 11. nist_80082r3_ot_configuration_management_aligned_with_moc

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_security_change_control`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 OT 구성관리 절차가 조직의 MOC(Management of Change) 관행과 정렬되어야 한다고 설명한다. 시스템 수명주기 동안 구성을 초기화·변경·모니터링·감사하고, OT에 변경을 배포하기 전 문서화·시험·승인하는 절차를 적용한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §6.2.4.2 pp.111–112, PDF index 127
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** HOLD_UNPROVEN_MOC_EQUIVALENCE
- Source-to-claim limitation/counterexample: Source directly establishes lifecycle configuration changes, tests and approvals, but the precise requirement to align configuration management with organizational 'MOC' is not directly established by this clause.

## 12. nist_80082r3_ot_mfa_remote_access_with_environmental_constraints

- Canonical topic/anchor: `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` / `sw09_mfa`
- **Exact original statement:** NIST SP 800-82 Rev. 3은 두 개 이상의 authentication factor를 MFA로 정의하고 OT 원격접속의 accepted best practice로 제시한다. 다만 OT component의 factor 지원 여부, 접속 유형과 보완통제를 고려해 적용 위치·요건을 정하도록 한다.
- **Primary source:** NIST SP 800-82r3 (September 2023), §6.2.10 p.123, PDF index 139
- Source URL: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf
- **Technical verification decision:** HOLD_OVERSTATED_BEST_PRACTICE
- Source-to-claim limitation/counterexample: NIST says MFA should be considered for OT remote access; the original phrase accepted best practice and factor definition need a separate original-source cross-check to certify as a universal technical rule.


## Audit policy

10 `KEEP_BOUNDED` rows may be marked original-source reviewed; 2 `HOLD_*` items remain `NOT_PERFORMED` in CSV for additional original verification. No Topic Pack JSON, generated bank, scoring overlay or release validation was changed. Technical confirmation is separate from general-score admission policy.