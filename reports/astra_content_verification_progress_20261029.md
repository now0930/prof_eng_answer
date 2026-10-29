# Astra Topic Pack 내용 검증 진행 기록 — 2026-10-29

## 현재 범위

- 현재 운영 Pack 89개, Anchor 2,093개.
- 기존 `grading/evidence/approved_fact_registry.json`에는 `verified` Fact 1,522행이 있으며 현재 Anchor ID와 일치하는 고유 ID는 1,520개다. 나머지 573개 ID는 이 등록부에 없다. 기존 등록부의 검증을 이번 Astra 작업으로 소급 표시하지 않는다.
- 이번 Astra 직접 재검토: 2차계 Pack 3개, 19개 Anchor. 모두 기존 등록부에 이미 있었다. 그중 적용조건 보완 3개, 출처 페이지 진술 미확인 1개. 별도 source·generated 수정이나 승인 상태 변경은 하지 않았다.
- 미등록 ID 첫 배치 10개: 구조적 소유 경계 6개, 기술 문장 4개. 이 배치 후 읽지 않은 미등록 ID는 563개다. 미등록이 곧 오류라는 뜻은 아니다.

## 2차계 19개 재검토 결과

| Pack | Anchor | 판정 | 필요한 후속 작업 |
| --- | --- | --- | --- |
| `second_order_system_resonance_frequency_response` | F1, F4 | 기술 내용 적합 | 표준 zero-free 모델의 적용범위 유지 |
| 동일 | F2 | 보완 필요 | 실수 `K≠0`인 일반식은 `|G(jω)|/|K|`; `/K`를 쓸 경우 `K>0` 명시 |
| 동일 | F3 | 보완 필요 | 유한 양의 주파수 peak `0<ζ<1/√2`; `ζ=0`은 비유계 공진, `ζ=1/√2`는 DC 경계 |
| 동일 | F5 | 조건부 적합 | 공진이 곧 폐루프 불안정의 충분조건이라는 식으로 해석하지 않음 |
| `second_order_lag_response_by_damping_ratio` | `so2_overdamped_response` | 보완 필요 | “느리다”는 동일 `ωn`·표준 zero-free·영초기조건 계단응답 비교로 한정 |
| 동일 | 나머지 8개 | 기술 내용 적합 | `model_answer.json`의 극점 실수부 표현은 복소극점 구간으로 한정; `logic_check.json`의 임계감쇠 최속 수렴은 비교조건 명시 |
| `second_order_system_modeling_electromechanical_analogy` | Anchor 01–04 | 기술 내용 적합 | 전기·기계 대응은 수학적 유사성임을 유지 |
| 동일 | Anchor 05 | 기술식 적합·출처 진술 미확인 | 차원 검산 `H·C/s²=V`는 맞으나 특정 PDF 2쪽의 문구 대조가 필요 |

독립 근거: [Illinois ECE486 Lecture 6](https://courses.physics.illinois.edu/ece486/sp2025/documentation/handbook/lec06.html), [Illinois ECE486 Lecture 7](https://courses.physics.illinois.edu/ece486/sp2025/documentation/handbook/lec07.html), [Hallauer 저자의 2차계 주파수응답 교재](https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Signal_Processing_and_Modeling/Introduction_to_Linear_Time-Invariant_Dynamic_Systems_for_Students_of_Engineering_%28Hallauer%29/10%253A_Second_Order_Systems/10.02%253A_Frequency_Response_of_Damped_Second_Order_Systems), [MIT 6.101 Lecture 1](https://web.mit.edu/6.101/www/s2019/handouts/L01.pdf). Astra가 출처를 대조했고, 본 작업에서 Illinois·Hallauer·MIT 페이지 접근을 다시 확인했다. 세부 판정은 Astra의 직접 검토 결과로 기록하며 전체 89개 완료 주장에 사용하지 않는다.

## 미등록 ID 첫 10개

| Anchor ID | 분류 | 판정·후속 작업 |
| --- | --- | --- |
| `actuator_sizing_topic1_handoff`, `body_cage_guide_topic4_handoff`, `leakage_packing_topic13_boundary`, `severe_service_material_topic14_boundary` | 저장소 내부 소유 계약 | `balanced_trim_unbalanced_trim_structure_sealing_applications`의 Topic Sheet·대상 Pack을 대조했다. 외부 공학 사실로 verified 처리하지 않고 canonical Topic ID를 병기할 것. |
| `sw06_sw04_boundary`, `sw06_sw09_boundary` | 저장소 내부 소유 계약 | `configuration_change_release_backup_rollback_migration_obsolescence_management`의 Topic Sheet·대상 Pack을 대조했다. 내부 번호를 학생 필수 지식으로 요구하지 않을 것. |
| `chl_scope_chain` | 조건부 기술 문장 | [NASA Product Realization](https://www.nasa.gov/reference/5-0-product-realization/)과 부합하나 열거를 유일한 의무 순서로 단정하지 않을 것. |
| `chl_architecture_partitioning` | 조건부 기술 문장 | [TI digital I/O](https://www.ti.com/technologies/digital-io.html), [NASA Interface Management](https://www.nasa.gov/reference/6-3-interface-management/)와 부합하나 블록 분할은 설계 예시다. |
| `chl_interface_definition` | 기술 문장 적합 | NASA Interface Management의 인터페이스 명세·호환성 검증과 부합한다. |
| `chl_power_budget` | 근거 보강 필요 | [Siemens PSU6200](https://press.siemens.com/global/en/pressrelease/new-power-supply-wide-variety-applications)에서 시동 부하와 overload reserve를 확인했으나 문장의 나머지 조건은 원문 대조가 부족하다. |

이번 검토만으로 기존 Pack·승인 Fact Registry·generated Bank를 수정하지 않는다. 특히 구조적 소유 경계를 기술 Fact로 승격하지 않는다. 정정 문구는 대응 문항의 정상·오답·경계 회귀를 확보한 뒤 별도 변경으로 적용한다.

## 미등록 ID 다음 20개 — Control Hardware Lifecycle

Astra가 `control_hardware_lifecycle_panel_architecture_component_selection_production_verification`의 다음 20개 Anchor를 출처별로 대조했다. **기술 지침 적합 14, 부분 근거 2, 내부 소유 계약 4**로 분류했다. 누적 미등록 ID 검토는 30개, 읽지 않은 ID는 543개다. 전체 Anchor 승인으로 해석하지 않는다.

| 분류 | Anchor ID | 근거·판정 경계 |
| --- | --- | --- |
| 내부 계약 | `chl_tolerance_stack_boundary`, `chl_grounding_emc_boundary`, `chl_field_installation_boundary`, `chl_environmental_qualification_boundary` | 다른 Pack과의 책임 분담이며 외부 물리 Fact가 아니다. |
| 부분 근거 | `chl_dfm_dfa` | 제조 계획·공정관리 방향은 지지되나 공구 접근·오삽입·repair/rework 전부의 직접 1차 근거는 미확인. |
| 부분 근거 | `chl_production_test_coverage` | 제품별 production acceptance 계획이 시험 범위를 결정하며 설계시험 일부 반복도 가능하다. “전체 설계검증을 반복하지 않는다”를 무조건적 금지로 해석하지 않을 것. |
| 적용조건부 기술 지침 적합 | `chl_power_protection`, `chl_component_selection_multicriteria`, `chl_obsolescence_availability`, `chl_thermal_design`, `chl_panel_layout`, `chl_io_selection`, `chl_communication_interface`, `chl_connector_terminal_selection`, `chl_prototype_not_production`, `chl_design_review`, `chl_prototype_design_verification`, `chl_incoming_material_control`, `chl_work_instruction_process_control`, `chl_eol_test` | 설계·부품·생산 단계별 합리적 검토 축이다. 모든 제품에 같은 부품·시험·수치를 강제하는 보편 규칙으로 승격하지 않는다. |

대표 1차 근거: [TI industrial power-path protection](https://www.ti.com/document-viewer/lit/html/SSZTAP4/GUID-54BCCB68-1DED-4886-B2A6-3B1D911E7502), [NASA EEEE Parts](https://sma.nasa.gov/sma-disciplines/eee-parts), [NASA Product Realization](https://www.nasa.gov/reference/5-0-product-realization/), [NASA Interface Management](https://www.nasa.gov/reference/6-3-interface-management/), [Siemens TX-I/O engineering](https://support.industry.siemens.com/cs/attachments/109785252/A6V10097438.pdf), [Rittal enclosure cooling](https://www.rittal.com/imf/none/5_3079/Rittal_Enclosure_and_Process_Cooling_5_3079/), [TE connector selector](https://www.te.com/content/dam/te-com/custom/media/connector-selector/docs/ict-connector-selector-en.pdf), [JPL final test clause](https://supplierportal.jpl.nasa.gov/qcprint.php?clause=QC134). NASA-STD-8739.4A 구판은 현재 의무 규정이 아니라 공정관리의 역사적 근거로만 취급한다.

## 미등록 ID 31–70번 — Hardware/Control Logic/Project Documents

Astra가 40개를 추가 검토했다. **적합 21, 조건 보강 8, 기술 정의 수정 1, 내부 소유 계약 9, 추가 근거 필요 1**이다. 누적 검토 70/573, 미검토 503개다. 자세한 출처 범위는 아래 분류에 따르며 source·generated·승인 Registry는 아직 바꾸지 않았다.

| Topic | 판정 | Anchor ID와 조치 |
| --- | --- | --- |
| `control_hardware_lifecycle_panel_architecture_component_selection_production_verification` | 적합 3·조건 보강 1 | `chl_test_fixture_control`, `chl_nonconformance_rework`, `chl_change_impact`; `chl_release_gate`는 compliance 또는 승인 waiver/deviation과 잔여 위험 인수를 허용. |
| 동일 | 내부 계약 2 | `chl_fat_boundary`, `chl_software_lifecycle_boundary`; 사실 Registry에 넣지 않음. |
| `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` | 기술 정의 수정 1 | `sw02_watchdog`: heartbeat 부재뿐 아니라 PLC task 실행시간·deadline 초과 감시도 포함. |
| 동일 | 조건 보강 3 | `sw02_override`의 bypass 배타성은 Pack 내부 용어로 한정; `sw02_trip_latch_reset`의 reset 정책과 `sw02_abnormal_transition_prevention`의 one-hot은 설계 요구에 따른 선택. |
| 동일 | 적합 6 | `sw02_shutdown_classes`, `sw02_command_arbitration`, `sw02_signal_quality`, `sw02_restart_recovery`, `sw02_degraded_mode`, `sw02_scan_edge_memory`. |
| 동일 | 내부 계약 3 | `sw02_scope_operational_logic`, `sw02_sw03_boundary`, `sw02_sw05_boundary`. |
| `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` | 적합 12 | `sw10_feasibility`, `sw10_scope_baseline`, `sw10_schedule_dependencies`, `sw10_cost_change_control`, `sw10_urs`, `sw10_io_list`, `sw10_tag_list`, `sw10_alarm_list`, `sw10_interlock_list`, `sw10_cause_effect`, `sw10_logic_diagram`, `sw10_test_specification`; 각 항목은 프로젝트별 문서·시험 범위에 맞춰 적용. |
| 동일 | 조건 보강 4 | `sw10_frs`, `sw10_fds`, `sw10_sds`, `sw10_document_hierarchy_traceability`: URS→FRS→FDS→SDS는 가능한 예시이지 보편적 의무 체인이 아님. |
| 동일 | 추가 근거 1 | `sw10_control_philosophy`: 열거된 내용 전체를 지지하는 산업계 1차 원문 미확인. |
| 동일 | 내부 계약 4 | `sw10_scope_project_execution`, `sw10_sw04_boundary`, `sw10_sw02_boundary`, `sw10_sw03_boundary`. |

대표 1차 근거: [NASA Product Verification](https://www.nasa.gov/reference/5-3-product-verification/), [NASA Requirements Management](https://www.nasa.gov/reference/6-2-requirements-management/), [HSE Control Systems](https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm), [CODESYS Task Object](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_f_reference_task.html), [OPC Foundation StatusCode](https://reference.opcfoundation.org/specs/OPC-10000-4/7.11.5), [NASA Technical Planning](https://www.nasa.gov/reference/6-1-technical-planning/), [EU GMP Annex 15](https://health.ec.europa.eu/document/download/7c6c5b3c-4902-46ea-b7ab-7608682fb68d_en?filename=2015-10_annex15.pdf), [Siemens CEM](https://support.industry.siemens.com/cs/attachments/109973506/p7lm100b_en-US.pdf). 분야별 원칙을 교차 확인한 것이며 NASA·EU 문서의 적용 의무를 모든 산업설비에 전가하지 않는다.

## Astra 체크포인트 71–110번 — 정식 승인 전 임시 기록

Astra가 71–110번 40개를 읽고 두 차례 체크포인트를 보냈으나, 최종 보고서 작성 전에 사용량 제한으로 중단되었다. 따라서 이 묶음은 **검토 초안**이며 70개 완료 누계에 넣지 않는다. 다음 저비용 검토자가 원문 locator와 ID 목록을 재확인한 뒤 확정한다.

- 71–90: `sw10_site_integration_test`부터 `sw10_change_punch_closure`까지 프로젝트 검증·인수 항목은 NASA Product Integration/Verification/Transition과 대체로 부합. `maintenance_scope_boundary`는 내부 소유 계약. Control Valve 정비의 작업허가·격리·분해·오염관리·trim/packing 점검은 [Emerson Control Valve Handbook](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf)과 대조했다. `external_cause_elimination`은 고정 순서가 아닌 진단 휴리스틱이며, 래핑은 OEM 승인 형상·재질에 한정한다.
- 91–110: seat endpoint·stroke/friction·fail action·as-left 기록은 제조사 시험계획에 따른 검증 항목이다. `pressure_boundary_test`는 정비 범위·OEM·코드가 요구할 때만 실시한다. 내부 Topic handoff가 다수 포함되며 외부 기술 Fact로 승인하지 않는다. `orientation_thermal_cycle_history`는 온도 반복시험의 직접 근거가 부족하다. `specification_test_lifecycle_workflow`는 예시 흐름이지 필수 고정 순서가 아니다.

2026-10-29 사용자 변경: 이후 일상 검토·승인에는 Astra를 계속 쓰지 않고 deterministic gate + 출처 대조를 수행하는 저비용 AI 검토자를 사용한다. 이 보고서의 Astra 판정을 소급해 새 모델의 승인으로 바꾸지 않는다.
