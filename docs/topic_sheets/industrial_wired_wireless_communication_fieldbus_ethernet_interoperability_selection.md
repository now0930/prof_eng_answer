# Topic Sheet — 계측제어 유·무선 통신, Fieldbus, Industrial Ethernet 및 상호운용성

## 1. Topic metadata

- `topic_id`: `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`
- `SW_NUMBER`: `SW-07`
- `LANE`: `SOFTWARE_LLM_LANE_B`
- `question_type`: `COMPARE_SELECTION`
- `difficulty`: `DESIGN_EVALUATION`
- `selection_importance`: `HIGH`

### Ownership

SW-07은 계측제어 유·무선 통신의 구조, 기능, 장치통합, 상호운용성과 선정기준을 담당한다.

SW-08은 Latency, Jitter, Cycle time, Determinism, 시간동기와 정량적 장애복구 성능을 담당한다.

SW-09는 Authentication, 암호화, 접근통제, firewall, secure remote access와 cyber incident response를 담당한다.

## 2. Scope and representative questions

### 포함 범위

- Communication requirement와 multi-criteria selection
- Copper, fiber, serial communication과 physical layer 시공
- Bus, star, tree, ring, line, mesh topology
- HART, FOUNDATION Fieldbus, PROFIBUS PA
- Modbus RTU, Modbus TCP
- EtherNet/IP, PROFINET, EtherCAT
- OPC UA information model과 시스템 통합
- WirelessHART, ISA100.11a
- Gateway, protocol conversion과 semantic mapping
- Device profile, Device Description와 conformance/interoperability
- Commissioning, diagnostics와 brownfield transition
- Firmware·host·tool·license의 lifecycle compatibility

### 대표 문제

- 계측제어 시스템의 유·무선 통신방식 선정절차와 평가항목을 설명하시오.
- Copper, fiber 및 serial communication의 특성과 산업현장 적용 시 고려사항을 비교하시오.
- HART, FOUNDATION Fieldbus 및 PROFIBUS PA의 구조·기능과 선정기준을 비교하시오.
- Modbus RTU와 Modbus TCP의 차이 및 Gateway 적용 시 데이터 mapping 고려사항을 설명하시오.
- EtherNet/IP, PROFINET 및 EtherCAT의 구조와 상호운용성 확보방안을 비교하시오.
- OPC UA의 information model 기반 상호운용성과 Fieldbus와의 역할 차이를 설명하시오.
- WirelessHART와 ISA100.11a의 구성 및 산업현장 적용 시 고려사항을 설명하시오.
- Device profile, Device Description와 conformance certification이 상호운용성에 미치는 영향을 설명하시오.
- 산업 통신망 commissioning 절차와 다중 vendor 장치의 통합시험 항목을 설명하시오.
- Brownfield 제어시스템의 통신 protocol 전환 및 수명주기 호환성 관리방안을 설명하시오.

## 3. Core correct facts

- **sw07_communication_requirements** — 산업 통신방식 선정은 전송할 데이터의 종류·방향·갱신 필요성, 연결 장치 수, 거리, 환경, 가용성, 진단, 상호운용성, 유지보수성과 수명주기 요구를 먼저 정의한 뒤 수행해야 한다.
- **sw07_layered_view** — 통신시스템은 물리매체, 신호·링크, 전송·응용 프로토콜, 장치 프로파일과 정보모델의 계층으로 나누어 보아야 하며, 같은 케이블이나 Ethernet을 사용해도 상위 계층이 다르면 직접 상호운용되지 않을 수 있다.
- **sw07_selection_multicriteria** — 통신방식의 최종 선정은 기능 적합성, 설치환경, 기존 설비, 진단성, 엔지니어링 도구, 공급자 지원, 교육, 예비품, 확장성과 총수명주기비용을 함께 비교하는 다기준 의사결정이어야 한다.
- **sw07_copper_media** — Copper 매체는 설치와 접속이 용이하고 전원중첩 또는 기존 배선 활용이 가능할 수 있으나 거리, 대역폭, 전자기 간섭, 접지전위차, 피뢰와 케이블 규격을 고려해야 한다.
- **sw07_fiber_media** — 광섬유는 전자기 간섭과 접지전위차의 영향을 줄이고 장거리·전기적 절연에 유리하지만 광모듈, connector 관리, 굴곡반경, 오염, 접속손실, 수리기술과 전원 이중화를 고려해야 한다.
- **sw07_serial_communication** — Serial communication은 비트를 순차 전송하는 방식이며 물리계층의 전기적 규격, baud rate, character format, duplex, addressing과 상위 프로토콜을 구분하여 설계해야 한다.
- **sw07_rs485_multidrop** — RS-485 다중점 구성은 차동전송을 사용하지만 bus topology, 종단저항, bias, stub 길이, 공통모드 범위, 주소 중복과 접지·차폐를 올바르게 관리해야 한다.
- **sw07_topology_selection** — Bus, star, tree, ring, line, mesh 등의 topology는 배선량, 확장성, 단일고장 영향, 유지보수 접근성, 전원분배와 프로토콜 허용구조를 비교하여 선정해야 한다.
- **sw07_termination_grounding** — 산업 통신의 commissioning에는 cable type, polarity, shield, grounding, termination, connector, segment length와 전원품질 확인이 포함되어야 하며 논리 설정만으로 물리계층 검증을 대체할 수 없다.
- **sw07_fieldbus_concept** — Fieldbus는 다수의 현장장치와 제어시스템 사이에 측정값·명령·상태·진단을 디지털로 교환하고 장치구성 및 자산정보를 통합할 수 있게 하는 산업 통신체계이다.
- **sw07_hart_overlay** — HART는 기존 4–20 mA 아날로그 신호 위에 디지털 통신을 중첩하여 주 변수와 함께 설정·상태·추가 변수·진단정보를 교환할 수 있게 한다.
- **sw07_hart_multidrop** — HART multidrop 구성은 여러 장치의 디지털 통신을 한 쌍에 연결할 수 있지만 loop current 운용방식, 주소, polling, 전원과 사용 목적을 점대점 구성과 구분해야 한다.
- **sw07_foundation_fieldbus** — FOUNDATION Fieldbus는 현장장치의 통신, 표준화된 function block, 장치관리와 진단을 통합하며 segment 설계 시 전원, trunk·spur, terminator, barrier와 장치 수를 함께 검토해야 한다.
- **sw07_foundation_fieldbus_function_blocks** — FOUNDATION Fieldbus function block은 장치 기능과 제어 연산을 표준화하여 분산 실행과 상호연결을 지원하지만 실제 기능 호환성은 block 종류, parameter, schedule, host 지원과 인증범위를 확인해야 한다.
- **sw07_profibus_pa** — PROFIBUS PA는 공정계측용 fieldbus로서 PA device profile과 bus-powered 물리구성을 활용하며 DP/PA coupling 또는 linking device, segment 전원·terminator·방폭구성을 함께 설계해야 한다.
- **sw07_modbus_rtu** — Modbus RTU는 serial link에서 주소, function code, data와 오류검사를 교환하는 단순한 register 기반 프로토콜이며 register 의미·단위·scale·byte order는 장치 문서와 mapping에 의존한다.
- **sw07_modbus_tcp** — Modbus TCP는 Modbus application data를 TCP/IP 네트워크에서 교환하도록 mapping한 방식이며 IP 설계, unit identifier 사용, connection 관리와 register mapping을 별도로 확인해야 한다.
- **sw07_ethernetip_cip** — EtherNet/IP는 표준 Ethernet과 IP 위에서 CIP object·service·connection model을 사용하는 산업 통신이며 EDS, device profile, I/O connection과 controller·scanner 지원을 확인해야 한다.
- **sw07_profinet** — PROFINET은 Ethernet 기반 산업 자동화 통신으로 cyclic I/O, acyclic parameter·diagnostics와 engineering integration을 제공하며 device role, conformance class, profile, GSDML과 controller 지원을 확인해야 한다.
- **sw07_ethercat** — EtherCAT은 Ethernet frame이 line 또는 ring을 통과하는 동안 각 slave가 지정 데이터를 처리하는 구조를 사용하며 master configuration, process data mapping, ESI와 network topology 적합성을 확인해야 한다.
- **sw07_opcua** — OPC UA는 platform-independent service, address space, information model과 method·event·subscription을 제공하여 시스템 간 의미 있는 데이터 교환을 지원하는 상호운용 아키텍처이다.
- **sw07_opcua_role_boundary** — OPC UA는 controller·SCADA·MES·gateway·cloud 사이의 정보통합에 강점이 있지만 모든 현장 I/O bus를 자동 대체하거나 정량적 실시간성을 보장하는 것은 아니다.
- **sw07_wirelesshart** — WirelessHART는 HART device data를 무선 mesh로 전달하기 위한 산업 무선체계이며 field device, gateway, network manager, access point, join 절차와 기존 host 연계를 함께 고려해야 한다.
- **sw07_isa10011a** — ISA100.11a는 산업용 무선 sensor·actuator 통신을 위한 체계로서 field device, backbone router, gateway/system manager와 application mapping을 구성하며 지원 profile과 host integration을 확인해야 한다.
- **sw07_wireless_site_survey** — 산업 무선망은 배치 전에 site survey로 거리, 구조물, 차폐, 반사, 이동설비, 간섭원, 공존채널과 설치높이를 조사하고 설치 후 실제 link 상태를 검증해야 한다.
- **sw07_wireless_power_lifecycle** — Battery-powered 무선장치는 update 요구, 송신횟수, routing 역할, 온도, battery chemistry, 교체절차와 접근성을 고려하여 전원 수명과 유지보수 계획을 수립해야 한다.
- **sw07_gateway_role** — Gateway는 서로 다른 네트워크나 계층을 연결하고 주소·data type·status·quality·diagnostics를 mapping할 수 있지만 연결 양쪽의 기능과 장애모드를 이해해야 한다.
- **sw07_protocol_conversion** — Protocol conversion은 frame·address·data representation을 변환하는 것뿐 아니라 register, object, tag, unit, scale, quality, timestamp와 command semantics를 명시적으로 mapping해야 한다.
- **sw07_device_profile** — Device profile은 장치 class별 필수·선택 기능, parameter, status와 동작규칙을 공통화하여 host와 다중 vendor 장치의 기능 상호운용성을 높인다.
- **sw07_device_description** — Device Description은 장치 parameter, menu, range, unit, method와 diagnostics를 engineering tool 또는 host가 해석하도록 제공하는 통합정보이며 DD/EDD, GSD/GSDML, EDS, ESI 등은 protocol ecosystem별로 역할이 다르다.
- **sw07_interoperability_levels** — Interoperability는 물리 연결, protocol communication, data syntax, semantic meaning, device behavior와 engineering integration의 여러 수준으로 구분하여 검증해야 한다.
- **sw07_conformance_vs_interoperability** — Conformance test나 certification은 장치가 지정 규격을 충족함을 보여주지만 실제 controller·host·gateway·option 조합의 상호운용성은 integration test와 승인목록으로 확인해야 한다.
- **sw07_commissioning_workflow** — 통신 commissioning은 문서검토, physical inspection, address·name 설정, device description 등록, parameter·unit 확인, communication test, command·fail behavior, diagnostics와 기록갱신의 순서로 수행해야 한다.
- **sw07_addressing_naming** — IP, node address, station name, tag, device ID와 asset identifier는 중복 없이 관리하고 도면·database·controller·host 사이에서 일관되게 매핑해야 한다.
- **sw07_diagnostics_maintenance** — 통신 진단은 link·signal·error counter·device status·quality·gateway mapping과 host alarm을 계층별로 구분하고 baseline과 trend를 사용하여 물리, protocol, device, application 원인을 좁혀야 한다.
- **sw07_installed_base_transition** — 기존 4–20 mA, HART, serial, fieldbus와 Industrial Ethernet이 혼재하는 설비에서는 brownfield 조건, shutdown 가능시간, adapter·gateway, 병행운전, 교육과 spare를 고려하여 단계적으로 전환할 수 있다.
- **sw07_lifecycle_compatibility** — 통신수명주기 관리는 protocol version, device profile, firmware, controller·host revision, Device Description, engineering tool, OS, license와 gateway 지원조합을 compatibility matrix로 추적해야 한다.
- **sw07_vendor_tool_dependency** — 상호운용성과 유지보수성 평가는 vendor engineering tool, driver·library, license, source configuration export, diagnostic access와 지원종료 시 대체경로까지 포함해야 한다.
- **sw07_sw08_boundary** — SW-07은 통신방식의 구조·기능·상호운용성과 선정기준을 담당하고, latency, jitter, cycle time, determinism, 시간동기, network load와 정량적 장애복구 성능은 SW-08이 담당한다.
- **sw07_sw09_boundary** — SW-07은 통신기능과 상호운용성을 담당하고, 인증, 암호화, 접근통제, 방화벽, secure remote access, 보안감시와 침해대응은 SW-09가 담당한다.

## 4. Acceptable answer expressions

- 같은 물리매체나 Ethernet을 사용해도 상위 protocol과 profile이 다르면 직접 호환되지 않을 수 있다.
- 통신방식은 속도 하나가 아니라 기능, 환경, 기존 설비, 진단, 유지보수와 수명주기비용으로 선정한다.
- RS-485는 물리계층이고 Modbus RTU 등 응용 protocol과 구분한다.
- Copper는 설치성과 전원중첩에 유리할 수 있으나 EMI, 거리, 접지와 차폐를 검토한다.
- Fiber는 EMI와 전기적 절연에 유리하지만 광모듈·connector·전원과 수리기술을 관리한다.
- HART 점대점은 4–20 mA 위에 digital communication을 중첩할 수 있다.
- HART multidrop은 점대점과 주소·loop current·polling 운용을 구분한다.
- FOUNDATION Fieldbus와 PROFIBUS PA는 유사한 배선요소가 있어도 protocol과 profile이 달라 직접 교환되지 않는다.
- Modbus register의 의미와 scale은 장치별 mapping 문서로 확인한다.
- EtherNet/IP 상호운용성은 CIP object, profile와 EDS·controller 지원을 포함한다.
- PROFINET은 device role, profile, GSDML과 controller 지원범위를 함께 확인한다.
- EtherCAT은 구조와 process data mapping을 SW-07에서, 정량적 성능은 SW-08에서 다룬다.
- OPC UA는 information model 기반 시스템통합에 강점이 있지만 모든 fieldbus를 자동 대체하지 않는다.
- WirelessHART와 ISA100.11a는 별도 protocol ecosystem이므로 직접 상호교환을 가정하지 않는다.
- 산업 무선은 site survey, 간섭, antenna 배치와 실제 link 검증이 필요하다.
- Battery 수명은 update와 routing, 온도, 교체절차를 포함해 관리한다.
- Gateway는 주소와 data뿐 아니라 unit, quality, diagnostics와 장애상태 mapping을 검토한다.
- Device profile은 기능 상호운용성을 높이지만 optional feature와 host 지원을 확인해야 한다.
- Device Description은 engineering integration을 돕지만 protocol과 physical compatibility를 대체하지 않는다.
- Certification은 중요한 근거지만 실제 controller·host·gateway 조합의 integration test가 필요하다.
- Commissioning은 physical, address·name, parameter, normal communication, fail behavior와 문서갱신을 포함한다.
- Brownfield 설비는 gateway·adapter와 단계적 전환을 사용하여 기존 자산을 유지할 수 있다.
- Protocol version, firmware, profile, host, engineering tool와 license를 compatibility matrix로 관리한다.
- Latency, jitter, determinism, 시간동기와 복구시간은 SW-08에서 평가한다.
- 인증, 암호화, 접근통제, firewall와 사고대응은 SW-09에서 평가한다.

## 5. Fatal wrong claims

- **sw07_fatal_physical_connector_interoperability** — 같은 Ethernet connector와 IP 주소를 사용하면 모든 Industrial Ethernet 장치가 직접 상호운용된다.
교정: 물리 연결과 상위 protocol·profile·object·information model 적합성은 별도로 확인해야 한다.
- **sw07_fatal_rs485_is_protocol** — RS-485는 register 의미, 명령과 장치 profile까지 정의하는 완전한 응용 protocol이다.
교정: RS-485는 주로 전기적 물리계층 규격이며 Modbus RTU 등 상위 protocol과 구분해야 한다.
- **sw07_fatal_speed_only_selection** — 통신속도가 가장 높은 방식이 모든 계측제어 응용에서 최선이다.
교정: 기능, 환경, 기존 설비, 진단, 상호운용성, 유지보수와 수명주기비용을 함께 비교해야 한다.
- **sw07_fatal_fiber_solves_all** — 광섬유를 사용하면 통신장애, 전원고장과 모든 접지문제가 자동으로 제거된다.
교정: 광섬유는 EMI와 전기적 절연에 유리하지만 광모듈·connector·전원·시공과 유지보수 고장은 남는다.
- **sw07_fatal_hart_removes_analog** — HART를 적용하면 4–20 mA 아날로그 신호는 항상 제거되고 완전한 digital bus가 된다.
교정: 점대점 HART는 4–20 mA 위에 digital signal을 중첩할 수 있으며 multidrop은 별도 운용조건을 갖는다.
- **sw07_fatal_ff_pa_interchangeable** — FOUNDATION Fieldbus와 PROFIBUS PA는 배선이 유사하므로 장치를 서로 교환하여 사용할 수 있다.
교정: 물리구성이 유사할 수 있어도 protocol, profile, host integration과 engineering file이 달라 직접 호환되지 않는다.
- **sw07_fatal_modbus_self_describing** — Modbus register 번호만 알면 제조사와 무관하게 공학단위, scale과 tag 의미가 자동 결정된다.
교정: Modbus data meaning은 장치별 register map, data type, byte order, scale과 문서에 의존한다.
- **sw07_fatal_serial_to_tcp_plug** — Serial Modbus 장치를 Ethernet port에 연결하면 자동으로 Modbus TCP 장치가 된다.
교정: 물리연결과 application mapping이 다르므로 gateway 또는 native interface와 주소·register mapping이 필요하다.
- **sw07_fatal_ethernetip_is_ethernet_only** — EtherNet/IP는 Ethernet cable과 IP 주소만 정의하므로 CIP object와 profile은 필요 없다.
교정: EtherNet/IP 상호운용성은 CIP object·service·connection과 device profile·EDS 지원에 달려 있다.
- **sw07_fatal_profinet_is_profibus_tunnel** — PROFINET은 PROFIBUS telegram을 Ethernet cable로 그대로 전달하는 단순 converter 방식이다.
교정: PROFINET은 독자적인 Ethernet 기반 automation model과 device role, cyclic·acyclic service 및 GSDML을 사용한다.
- **sw07_fatal_ethercat_any_switch** — EtherCAT line에는 일반 office Ethernet switch를 임의로 삽입해도 network 구조와 device processing이 항상 동일하다.
교정: EtherCAT topology와 master·slave processing 규칙에 맞는 구성인지 확인해야 하며 임의의 switch 삽입을 일반화할 수 없다.
- **sw07_fatal_opcua_guarantees_field_realtime** — OPC UA를 사용하면 모든 field I/O bus와 별도의 실시간성 검토가 불필요하다.
교정: OPC UA는 정보모델과 시스템 통합에 강점이 있으나 fieldbus 대체와 정량적 실시간성은 요구별로 검토해야 한다.
- **sw07_fatal_wireless_no_survey** — 산업 무선은 케이블이 없으므로 site survey, 간섭과 antenna 배치 검토 없이 설치해도 된다.
교정: RF propagation, 구조물, 간섭, 공존채널과 실제 link 상태를 조사·검증해야 한다.
- **sw07_fatal_wireless_interchangeable** — WirelessHART와 ISA100.11a 장치는 2.4 GHz를 사용하므로 gateway 없이 직접 상호교환된다.
교정: 각 체계의 protocol, joining, application profile과 gateway·host 지원이 달라 직접 호환을 가정할 수 없다.
- **sw07_fatal_gateway_lossless** — Gateway를 설치하면 양쪽 protocol의 모든 parameter, diagnostics, quality와 command 의미가 손실 없이 자동 변환된다.
교정: Gateway mapping 범위와 unsupported function, quality·timeout·startup 처리 및 장애모드를 명시해야 한다.
- **sw07_fatal_profile_guarantees_all** — 같은 device profile을 지원하면 모든 optional function과 host engineering 기능이 자동으로 plug-and-play 된다.
교정: Profile version, optional feature, host support, Device Description와 실제 integration test가 필요하다.
- **sw07_fatal_certification_guarantees_combination** — 각 장치가 개별 certification을 받았으므로 어떤 controller·host·gateway 조합에서도 상호운용성이 보장된다.
교정: Conformance와 실제 조합의 interoperability는 다르므로 승인조합과 integration test를 확인해야 한다.
- **sw07_fatal_device_description_replaces_protocol** — Device Description 파일이 있으면 wiring, protocol stack, controller 지원과 device behavior 검토가 모두 필요 없다.
교정: Device Description은 parameter와 engineering integration을 돕지만 물리·protocol·profile·host 적합성을 대체하지 않는다.
- **sw07_fatal_same_protocol_all_versions** — 제품에 같은 protocol 이름이 표시되면 firmware, profile, controller와 engineering tool version에 관계없이 영구 호환된다.
교정: Version·profile·option·firmware·host·tool 조합을 compatibility matrix와 시험으로 확인해야 한다.
- **sw07_fatal_protocol_name_proves_performance_security** — Protocol 종류만 알면 latency, jitter, 복구시간과 인증·암호화 수준까지 자동으로 확정할 수 있다.
교정: 정량적 실시간·복구성능은 SW-08에서, 보안통제는 SW-09에서 별도 요구와 구성으로 평가해야 한다.

## 6. Warn-level weak claims

- **sw07_major_requirements_without_environment** — 데이터 종류와 protocol 이름만 제시하고 거리, 환경, 장치 수, 진단, 수명주기 요구를 누락한다.
보완: Communication requirement를 기능·환경·운영·수명주기 항목으로 구조화한다.
- **sw07_major_media_without_physical_rules** — Copper와 fiber의 장단점만 나열하고 termination, grounding, connector, transceiver와 시공조건을 설명하지 않는다.
보완: Physical media 선정과 commissioning 조건을 연결한다.
- **sw07_major_protocol_catalog_only** — HART, Fieldbus, Industrial Ethernet 명칭만 나열하고 역할·장치통합·선정기준을 비교하지 않는다.
보완: 각 protocol의 적용계층, data model, engineering integration과 brownfield 조건을 비교한다.
- **sw07_major_modbus_without_mapping** — Modbus를 개방형 protocol이라고만 설명하고 register map, data type, scale와 byte order를 누락한다.
보완: Device-specific mapping과 semantic validation을 포함한다.
- **sw07_major_gateway_without_semantics** — Gateway 연결만 제시하고 data direction, unit, quality, timeout와 unsupported function을 정의하지 않는다.
보완: Protocol conversion table과 장애상태 처리를 구체화한다.
- **sw07_major_profile_description_missing** — Protocol 호환성만 설명하고 device profile과 Device Description revision을 누락한다.
보완: 기능 profile, engineering file와 host 지원범위를 함께 확인한다.
- **sw07_major_certification_without_integration** — Certification 제품을 선정했다고만 쓰고 controller·host·gateway 조합의 integration test를 누락한다.
보완: Conformance와 interoperability를 구분하고 승인조합 시험을 수행한다.
- **sw07_major_commissioning_happy_path_only** — 정상값 표시만 확인하고 주소중복, 단선, timeout, device replacement와 fail behavior를 시험하지 않는다.
보완: Physical·logical·functional·fault commissioning을 단계화한다.
- **sw07_major_wireless_without_site_power** — 무선의 배선절감만 설명하고 site survey, 간섭, battery와 유지보수 접근성을 누락한다.
보완: RF와 전원 수명주기 조건을 선정기준에 포함한다.
- **sw07_major_lifecycle_without_matrix** — 초기 호환성만 확인하고 firmware, profile, host, tool, OS, license와 description revision의 장기 조합을 관리하지 않는다.
보완: Compatibility matrix와 교체·upgrade 절차를 유지한다.
- **sw07_major_brownfield_without_transition** — 신규 protocol의 장점만 설명하고 기존 4–20 mA·serial·fieldbus와의 coexistence, gateway와 shutdown 제약을 누락한다.
보완: Installed base를 반영한 단계적 전환방안을 제시한다.
- **sw07_major_boundary_blurring** — SW-07 답안을 latency·jitter·복구시간 또는 firewall·암호화·사고대응 중심으로 전개한다.
보완: SW-07은 구조·기능·상호운용·선정에 집중하고 SW-08·SW-09 경계를 명시한다.

## 7. False positive cautions

- Copper를 선정했다는 이유만으로 낮은 수준의 답안으로 보지 말고 거리·EMI·접지·수명주기 근거를 확인한다.
- Fiber를 사용하지 않았다는 이유만으로 오답 처리하지 말고 실제 거리와 전기적 절연 요구를 본다.
- HART를 4–20 mA와 함께 설명한 답안은 정상적인 점대점 구조로 인정한다.
- FOUNDATION Fieldbus와 PROFIBUS PA의 공통 물리요소를 언급해도 protocol과 profile 차이를 함께 설명하면 오류가 아니다.
- Modbus를 단순 protocol이라고 표현해도 register mapping과 data meaning 한계를 설명하면 인정한다.
- Industrial Ethernet protocol 중 하나만 선정해도 요구사항 기반 비교와 host 지원근거가 있으면 인정한다.
- OPC UA를 field device 가까이에 적용했다는 이유만으로 오답 처리하지 말고 역할과 실시간성 한계를 구분했는지 본다.
- WirelessHART 또는 ISA100.11a 중 하나만 채택해도 device·gateway·host ecosystem과 site 조건 근거가 있으면 인정한다.
- Gateway 사용 자체를 상호운용 실패로 보지 말고 semantic mapping과 장애상태 처리가 있는지 본다.
- Vendor-specific Device Description나 tool 사용 자체는 오류가 아니며 version·지원·exit 조건을 관리하면 인정한다.
- Certification을 상호운용성 근거로 제시하는 것은 맞으며 실제 조합시험을 완전히 대체한다고 단정할 때만 Fatal로 본다.
- Cycle time 또는 latency를 간단히 언급해도 주된 답안이 구조·기능·상호운용성 선정이면 SW-07로 인정한다.
- 보안기능의 존재를 선정조건으로 언급해도 인증·암호화·방화벽 설계가 주된 논지가 아니면 SW-07 경계 위반이 아니다.
- Brownfield에서 기존 serial 또는 4–20 mA를 유지하는 결정은 위험·비용·전환계획 근거가 있으면 인정한다.
- Protocol 이름의 한글·영문 표기와 대소문자 차이는 의미가 동일하면 허용한다.

## 8. Routing aliases and regex candidate patterns

### Routing aliases

- `계측제어 유무선 통신 Fieldbus Industrial Ethernet`
- `industrial wired wireless communication fieldbus ethernet`
- `산업 통신방식 선정 상호운용성`
- `communication media protocol interoperability selection`
- `copper fiber serial fieldbus selection`
- `구리 광섬유 직렬통신 선정`
- `HART FOUNDATION Fieldbus PROFIBUS PA 비교`
- `HART FF PROFIBUS PA interoperability`
- `Modbus RTU Modbus TCP gateway mapping`
- `Modbus register protocol conversion`
- `EtherNet/IP CIP EDS device profile`
- `PROFINET GSDML device integration`
- `EtherCAT ESI process data mapping`
- `OPC UA information model interoperability`
- `WirelessHART ISA100.11a gateway`
- `산업 무선 site survey battery lifecycle`
- `gateway protocol converter semantic mapping`
- `device profile device description interoperability`
- `DD EDD GSD GSDML EDS ESI`
- `field device commissioning communication`
- `brownfield communication migration gateway`
- `protocol firmware host compatibility matrix`
- `industrial communication topology termination grounding`
- `multi vendor device interoperability certification`
- `industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection`

### Narrow regex candidates

- `(HART|FOUNDATION Fieldbus|PROFIBUS PA).*(비교|선정|상호운용)`
- `(Modbus RTU|Modbus TCP).*(register|gateway|mapping)`
- `(EtherNet/IP|PROFINET|EtherCAT).*(profile|device|interoperability)`
- `(OPC UA).*(information model|상호운용)`
- `(WirelessHART|ISA100\.11a).*(gateway|site survey|battery)`
- `(device profile|Device Description|GSDML|EDS|ESI).*(호환|통합)`
- `(protocol conversion|gateway).*(unit|quality|semantic|timeout)`
- `(commissioning).*(address|parameter|fault|diagnostics)`

Broad 단독어 `communication`, `network`, `Ethernet`, `wireless`, `security`, `realtime`는 후보규칙으로 사용하지 않는다.

## 9. fact_anchor.json generation guidance

- 40개 anchor를 순서대로 유지한다.
- `id`와 `anchor_id`는 동일해야 한다.
- `core_facts`는 anchor statement 순서와 정확히 같아야 한다.
- Fatal은 20개이며 `affected_layers=["C"]`를 유지한다.
- Source basis는 산업 통신 표준체계와 현장 통합절차를 사용한다.
- SW-08과 SW-09 boundary anchor를 반드시 포함한다.

## 10. logic_check.json generation guidance

- `deterministic_checks.enabled=false`
- deterministic fatal·major rule은 비워 둔다.
- LLM semantic verification을 사용한다.
- Candidate rules는 비우고 compound key term을 충분히 제공한다.
- Fatal 20개와 Major 12개를 truth schema에 연결한다.
- Direct score application은 하지 않는다.
- Correctness owner는 C이며 D/E 직접 영향은 없다.
- Protocol 이름만으로 performance 또는 security를 확정하는 오류를 차단한다.

## 11. model_answer.json and topic_importance.json guidance

### model_answer.json

- Question type은 `COMPARE_SELECTION`
- 10개 question pattern
- 10개 대표 문제
- 8개 recommended outline
- Narrow compound routing alias
- High-score point는 구조·기능·interoperability·selection·commissioning·lifecycle을 연결한다.

### Question patterns

- **sw07_qp_communication_selection** — 통신 요구사항을 정의하고 유·무선 통신방식을 선정하는 문제
- **sw07_qp_media_serial** — Copper, fiber와 serial communication의 특성·선정·시공을 묻는 문제
- **sw07_qp_fieldbus_compare** — HART, FOUNDATION Fieldbus와 PROFIBUS PA를 비교하는 문제
- **sw07_qp_modbus_integration** — Modbus RTU/TCP와 gateway mapping을 설명하는 문제
- **sw07_qp_industrial_ethernet** — EtherNet/IP, PROFINET과 EtherCAT의 구조와 선정기준을 비교하는 문제
- **sw07_qp_opcua** — OPC UA information model과 산업 통합 적용을 묻는 문제
- **sw07_qp_wireless** — WirelessHART와 ISA100.11a 구조·선정·현장적용을 묻는 문제
- **sw07_qp_interoperability** — Device profile, Device Description, certification과 상호운용성을 묻는 문제
- **sw07_qp_commissioning_lifecycle** — 통신 commissioning과 수명주기 호환성 관리 문제
- **sw07_qp_brownfield_boundary** — 기존 설비 통신 전환과 SW-08·SW-09 경계를 묻는 문제

### Recommended outline

- **1. 요구사항과 선정 원칙** — 전송기능, 장치 수·거리·환경, 진단, 기존 설비, 유지보수와 수명주기 요구를 정의하고 다기준 선정절차를 제시한다.
- **2. 물리매체와 topology** — Copper·fiber·serial의 특성과 termination·grounding·topology를 연결한다.
- **3. Process Fieldbus** — HART, FOUNDATION Fieldbus와 PROFIBUS PA의 역할·구성·장치통합 차이를 설명한다.
- **4. Modbus와 Industrial Ethernet** — Modbus RTU/TCP, EtherNet/IP, PROFINET과 EtherCAT의 application model과 integration file을 비교한다.
- **5. OPC UA와 산업 무선** — OPC UA의 information model 역할과 WirelessHART·ISA100.11a의 구조·site survey·battery 조건을 설명한다.
- **6. 상호운용성과 Gateway** — Gateway·protocol conversion, device profile, Device Description, certification과 integration test를 연결한다.
- **7. Commissioning과 수명주기** — 주소·name·parameter·fault test, diagnostics, brownfield 전환과 compatibility matrix를 제시한다.
- **8. 결론과 ownership 경계** — 기능·상호운용성 중심 선정결론을 내리고 정량적 실시간성은 SW-08, 보안통제는 SW-09로 구분한다.

### topic_importance.json

- `difficulty=DESIGN_EVALUATION`
- `selection_importance=HIGH`
- High band는 protocol catalog가 아니라 비교·선정·상호운용성 검증을 요구한다.
- SW-08·SW-09 boundary가 없거나 Fatal 오류가 있으면 high band를 허용하지 않는다.

## 모범답안

### 1. 개요

산업계측제어 통신은 측정값과 명령을 전달하는 배선기술을 넘어 장치설정, 상태·진단, 자산정보와 시스템 간 의미를 연결하는 기반이다. 따라서 선정은 최고속도 중심이 아니라 데이터 종류와 방향, 장치 수, 거리, 설치환경, 기존 설비, 진단성, 상호운용성, 유지보수성과 수명주기비용을 먼저 정의한 뒤 수행해야 한다.

### 2. 물리매체와 Serial communication

Copper는 설치성과 기존 배선 활용에 유리하지만 거리, EMI, 접지전위차, 차폐와 피뢰를 검토해야 한다. Fiber는 전기적 절연과 EMI 내성에 유리하지만 광모듈·connector 오염·굴곡·접속손실·전원과 수리기술을 관리해야 한다. Serial 통신에서는 RS-485 같은 물리계층과 Modbus RTU 같은 응용 protocol을 구분하며 baud, parity, address, bus topology, termination, bias, stub와 grounding을 함께 확인한다.

### 3. HART와 Process Fieldbus

HART는 4–20 mA 위에 digital communication을 중첩하여 설정, 추가 변수와 diagnostics를 제공한다. 점대점과 multidrop은 loop current, 주소와 polling 운용이 다르다. FOUNDATION Fieldbus는 function block과 장치관리·진단을 통합하며 segment 전원, trunk·spur와 terminator를 설계한다. PROFIBUS PA는 PA profile과 DP/PA coupling 또는 linking device를 사용한다. 두 Fieldbus는 물리구성이 유사할 수 있어도 protocol, profile, host와 engineering file이 달라 직접 교환되지 않는다.

### 4. Modbus와 Industrial Ethernet

Modbus RTU/TCP는 단순하고 널리 사용되지만 register 의미, data type, byte order, unit와 scale가 장치 mapping에 의존한다. EtherNet/IP는 CIP object·service·connection과 EDS를, PROFINET은 device role·profile·GSDML을, EtherCAT은 master configuration·process data mapping·ESI를 확인해야 한다. 같은 Ethernet cable과 IP를 사용해도 application model과 device profile이 다르면 직접 상호운용되지 않는다.

### 5. OPC UA와 산업 무선

OPC UA는 address space와 information model로 data type, relationship, method, event와 subscription을 표현하여 SCADA, MES, gateway와 상위시스템 통합에 유리하다. 그러나 모든 field I/O bus와 정량적 실시간성을 자동 대체하지는 않는다. WirelessHART와 ISA100.11a는 각각 device, gateway와 network/system manager를 포함하는 별도 ecosystem이다. 무선 선정에는 site survey, 구조물과 간섭, antenna 배치, gateway 위치, battery 수명과 교체 접근성을 포함한다.

### 6. 상호운용성과 Gateway

상호운용성은 physical link, protocol frame, data syntax, semantic meaning, device behavior와 engineering integration의 여러 수준으로 확인한다. Gateway와 protocol converter는 address와 값만 전달하는 장치가 아니라 unit, scale, quality, timestamp, read/write 방향, timeout와 startup state를 mapping하는 경계이다. Device profile은 공통 기능을, Device Description은 parameter와 engineering menu를 제공한다. Certification은 규격 적합성의 근거이지만 실제 controller·host·gateway 조합은 integration test로 검증해야 한다.

### 7. Commissioning과 수명주기 관리

Commissioning은 문서검토와 cable·polarity·shield·termination 검사, address·station name 설정, Device Description 등록, parameter·unit 확인, 정상통신, command와 fail behavior, diagnostics와 문서갱신 순서로 수행한다. Brownfield에서는 기존 4–20 mA, HART, serial과 fieldbus를 gateway나 adapter로 공존시키고 shutdown 제약에 맞춰 단계 전환할 수 있다. 장기 운전에는 protocol version, profile, firmware, host, engineering tool, OS, license와 Device Description revision을 compatibility matrix로 관리한다.

### 8. 결론

적정 통신방식은 요구기능과 설치환경, 기존설비, 상호운용성 증거, commissioning 가능성, 공급자 지원과 총수명주기비용을 비교하여 선정한다. SW-07은 통신 구조·기능·상호운용성과 선정기준을 담당한다. Latency, jitter, cycle time, determinism, 시간동기와 정량적 장애복구는 SW-08에서 평가하고, 인증·암호화·접근통제·방화벽과 침해대응은 SW-09에서 평가한다.

## 12. Human review checklist

- [ ] Physical media와 application protocol을 구분했는가.
- [ ] RS-485와 Modbus RTU를 구분했는가.
- [ ] HART, FOUNDATION Fieldbus와 PROFIBUS PA의 역할 차이가 정확한가.
- [ ] Modbus register mapping의 의미 한계를 설명했는가.
- [ ] EtherNet/IP·PROFINET·EtherCAT의 profile과 engineering file을 구분했는가.
- [ ] OPC UA를 모든 fieldbus의 자동 대체로 설명하지 않았는가.
- [ ] Wireless site survey와 battery lifecycle을 포함했는가.
- [ ] Gateway semantic mapping과 unsupported function을 평가했는가.
- [ ] Device profile, Device Description와 certification을 구분했는가.
- [ ] Commissioning과 fault test를 포함했는가.
- [ ] Lifecycle compatibility matrix를 제시했는가.
- [ ] SW-08과 SW-09 ownership 경계를 유지했는가.
