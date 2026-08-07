# 계측제어 시스템 설계기준, Code·Standard·Specification 및 Deviation 관리

- Topic ID: `instrumentation_system_design_basis_codes_standards_specification_deviation_management`
- Official criterion: `IC-2027-W-2-8`
- Question Type: `IMPLEMENTATION_EVALUATION`
- Difficulty: `DESIGN_EVALUATION`
- Selection importance: `NORMAL`
- Historical frequency: 근거가 없어 사용하지 않음

## Scope

이 Topic은 계측제어 시스템의 설계기준을 실제 프로젝트 requirement로 전개하는 방법을 다룬다.

핵심 흐름은 다음과 같다.

`Governing requirements → Design Basis → Specification/Data Sheet → Vendor compliance/deviation → approval/disposition → verification → as-built baseline`

중심 내용은 다음과 같다.

1. Design Basis와 Design Criteria의 기능
2. Code, Standard, Specification의 역할과 적용근거
3. 적용표준 register, 판본과 document precedence
4. 공정·성능·환경·architecture·interface 설계입력
5. 계장 문서의 정합성
6. Vendor deviation과 Technical Bid Evaluation
7. Deviation의 impact/risk, approval, disposition, closure
8. Project change와 MOC의 경계
9. FAT/SAT/commissioning 및 as-built traceability

## Ownership boundary

이 Topic은 특정 개별 기술표준의 세부 요구사항을 모두 소유하지 않는다.

- 위험장소 방폭 선정 상세: `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
- SIS/SIL software 독립성·systematic failure·V&V: `sis_sil_safety_software_independence_systematic_failure_verification_validation`
- Software V-model/traceability 상세: `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`
- Project engineering document/FAT/SAT 상세: `control_software_project_engineering_documents_fat_sat_commissioning_acceptance`
- P&ID symbol/tag/control narrative 상세: `pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative`
- Configuration release/backup/rollback 상세: `configuration_change_release_backup_rollback_migration_obsolescence_management`

이 Topic은 위 주제를 대체하지 않고, 계측제어 **설계 governing basis와 deviation governance의 연결**만 소유한다.

## Standards treatment

표준 번호 자체를 암기점수로 사용하지 않는다.

예를 들어 ISA-5.1은 계장 symbol·identification, ISA-20 계열은 instrument specification form의 대표적 산업 기준으로 활용할 수 있다. IEC 61511은 SIS lifecycle의 specification·design·installation·operation·maintenance라는 lifecycle 관점을 보여주는 대표 사례다.

그러나 실제 프로젝트에서 어떤 법규·표준·판본이 강제되는지는 관할 법규, 계약, 발주처 기준과 project cut-off를 확인해 결정해야 한다. 특정 표준의 최신판이 모든 기존설비에 자동 소급된다고 단정하지 않는다.

## Grading direction

고득점 답안은 표준명을 많이 쓰는 답안이 아니다.

설계 입력이 어떻게 requirement가 되고, Vendor가 어떻게 compliance/deviation을 제시하며, deviation이 어떻게 평가·승인·문서갱신되고, 최종적으로 FAT/SAT·as-built evidence로 닫히는지를 설명해야 한다.

비용, 실현가능성, 기존설비 영향도 함께 본다. Legacy retrofit에서는 신규기준의 무조건적 전면적용보다 안전·법규·interface·shutdown·spare·교육·변경비용을 종합평가하고 필요한 deviation/MOC와 단계적 적용방안을 제시하는 설명을 허용한다.
