# 산업계측제어기술사 2027~2030 공식 출제기준 Topic Pack Coverage

## 1. 목적

이 문서는 산업계측제어기술사 2027~2030 필기 공식 출제기준 33개 세부항목에 대해
현재 69개 Topic Pack의 실제 의미 범위를 기준으로 coverage 수준을 평가한다.

공식 기준과 Topic Pack 분류는 다음 문서를 기준으로 한다.

- `docs/exam_scope/industrial_instrumentation_control_2027_2030_criteria.md`
- `docs/topic_pack_classification.md`

## 2. 판정 원칙

- `COVERED`: 현재 Topic Pack 집합이 해당 공식 criterion의 핵심 범위를 독립 답안 수준으로 실질적으로 설명할 수 있다.
- `PARTIAL`: 관련 Topic은 있으나 공식 criterion의 일부 핵심 범위가 빠져 있거나 다른 Topic의 부수 범위로만 존재한다.
- `GAP`: 현재 Topic Pack 집합에 해당 criterion의 실질적 답안 근거가 없다.
- Topic 개수 또는 PRIMARY Topic 보유 여부만으로 자동 판정하지 않는다.
- PRIMARY와 SECONDARY Topic의 README, Fact, Model evidence를 공식 criterion의 의미 범위와 비교한다.
- 내부 `IC-2027-W-*` ID는 repository 관리용 ID이며 한국산업인력공단의 공식 식별자가 아니다.
- Coverage는 Question Type과 독립된 축이다.

Stage 3B semantic coverage review SHA-256: `59c670736c94f98d57cd8e0fb2c63537112b46cbdd0cfdf723525bfe344dc27f`

## 3. 전체 현황

확장 전 frozen baseline과 69개 Topic Pack 통합 후 semantic 재감사 결과는 다음과 같다.

| 시점 | COVERED | PARTIAL | GAP | TOTAL |
|---|---:|---:|---:|---:|
| 확장 전 baseline | 16 | 8 | 9 | 33 |
| 확장 후 현재 | **30** | **2** | **1** | **33** |

확장 후 미완전 criterion은 `IC-2027-W-4-2`, `IC-2027-W-5-1`, `IC-2027-W-5-2` 3개다.
Roadmap 인접문맥은 planning evidence로만 사용하며 실제 Topic source 의미가 없으면 coverage로 자동 승격하지 않는다.
## 4. 공식 세부항목 Coverage Matrix

| ID | 공식 세부항목 | Coverage | Confidence | PRIMARY | SECONDARY |
|---|---|:---:|:---:|---:|---:|
| `IC-2027-W-1-1` | 제어시스템의 전달함수 | **COVERED** | MEDIUM | 1 | 6 |
| `IC-2027-W-1-2` | 제어시스템의 보상요소 | **COVERED** | HIGH | 1 | 4 |
| `IC-2027-W-1-3` | 제어시스템의 응답특성 | **COVERED** | HIGH | 6 | 5 |
| `IC-2027-W-1-4` | 전자기기의 오차 발생요인과 대책 | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-2-1` | 측정센서(온도, 압력, 습도, 액위, 수위, 속도, 위치 등), 계측기의 작동원리 및 선정기준 | **COVERED** | HIGH | 11 | 3 |
| `IC-2027-W-2-2` | 비접촉 방법(초음파, 광 등)을 통한 측정원리 및 알고리즘 | **COVERED** | HIGH | 3 | 0 |
| `IC-2027-W-2-3` | 측정 시 오차발생 원인과 대책 | **COVERED** | HIGH | 1 | 10 |
| `IC-2027-W-2-4` | 제어밸브의 작동원리 및 기능 | **COVERED** | HIGH | 5 | 10 |
| `IC-2027-W-2-5` | 구동기(공압, 모터 등)의 작동원리 및 기능 | **COVERED** | HIGH | 2 | 4 |
| `IC-2027-W-2-6` | 계측제어기기의 전원 및 접지방식 | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-2-7` | 계측제어기기에 관한 유·무선 통신, 규약 | **COVERED** | HIGH | 1 | 1 |
| `IC-2027-W-2-8` | 계측제어기기 및 시스템 설계 규정 | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-3-1` | 유체제어(온도, 압력, 유량, 수위 등)에 관한 기본요소와 설계요소 | **COVERED** | MEDIUM | 8 | 3 |
| `IC-2027-W-3-2` | 제어시스템(분산제어시스템, 원격제어시스템(SCADA), PLC, PC기반 등) 설계요소 | **COVERED** | HIGH | 2 | 2 |
| `IC-2027-W-3-3` | 제어기기 및 시스템의 통신방식 | **COVERED** | HIGH | 1 | 2 |
| `IC-2027-W-3-4` | 단일루프 제어 및 다중루프 제어설계 | **COVERED** | HIGH | 4 | 3 |
| `IC-2027-W-3-5` | PI, PID 등 제어 및 Parameter 설정 | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-3-6` | 제어논리 설계 및 논리도 작성 | **COVERED** | HIGH | 1 | 1 |
| `IC-2027-W-3-7` | 공정제어 계측(P&ID) 설계 | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-3-8` | 계측제어시스템의 소프트웨어 개발, 생산 및 검증 | **COVERED** | HIGH | 1 | 4 |
| `IC-2027-W-3-9` | 계측제어시스템의 하드웨어 개발, 생산 및 검증 | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-3-10` | 계측제어시스템의 환경 검증시험 및 대책(온도, 습도, 전자기파 등) | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-4-1` | 가용도(availability), 신뢰도(reliability) | **COVERED** | HIGH | 0 | 2 |
| `IC-2027-W-4-2` | 가스, 정유, 철도, 발전, 건축 등 위험 환경에서 고려해야 할 제어요소 및 대책 | **PARTIAL** | HIGH | 1 | 0 |
| `IC-2027-W-4-3` | 안전, 방재 등 재난대비 목적의 계측제어시스템 설계 | **COVERED** | HIGH | 2 | 2 |
| `IC-2027-W-4-4` | 프로젝트 관리(원가, 인력, 수행일정 등) | **COVERED** | HIGH | 2 | 0 |
| `IC-2027-W-4-5` | 생산관리(원가, 인력, 수행일정 등) | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-4-6` | 제어시스템의 운영 및 관리 | **COVERED** | HIGH | 3 | 8 |
| `IC-2027-W-4-7` | 제어기기 및 시스템의 사이버 보안 및 대책 | **COVERED** | HIGH | 1 | 0 |
| `IC-2027-W-4-8` | 제어기기 및 시스템의 수명주기 관리방법 | **COVERED** | HIGH | 1 | 6 |
| `IC-2027-W-4-9` | 계측제어설비 설치 및 기술기준 | **COVERED** | HIGH | 1 | 1 |
| `IC-2027-W-5-1` | 계측제어 관련 신기술(로봇, 인공지능, IoT, 스마트팩토리, 양자컴퓨팅 등) | **PARTIAL** | HIGH | 3 | 0 |
| `IC-2027-W-5-2` | 계측제어 관련 동향 | **GAP** | HIGH | 0 | 0 |

## 5. PARTIAL 상세

### `IC-2027-W-4-2` 가스, 정유, 철도, 발전, 건축 등 위험 환경에서 고려해야 할 제어요소 및 대책

- 판정: **PARTIAL**
- 근거: 새 Topic은 Zone/EPL/Ex marking, 방폭방식, intrinsic safety entity/barrier/wiring 등 가스·정유의 폭발위험 환경을 강하게 닫는다. 그러나 공식 문구는 철도·발전·건축 등을 포함한 위험 환경 전반의 제어요소와 대책을 요구한다.
- 잔여범위: 철도·발전·건축 등 비폭발 위험환경의 fail-safe, environmental/functional hazard, 적용별 제어대책을 별도 보강할 필요가 있다.
- 신규 직접 Topic:
  - `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`

### `IC-2027-W-5-1` 계측제어 관련 신기술(로봇, 인공지능, IoT, 스마트팩토리, 양자컴퓨팅 등)

- 판정: **PARTIAL**
- 근거: 기존 AI/ML·Physical AI·robot·digital twin에 IIoT/Smart Factory Device→Edge→Platform→Enterprise/Cloud, semantic interoperability, Digital Thread가 추가되어 큰 공백은 줄었다. 그러나 공식 예시에 명시된 양자컴퓨팅 및 기타 신기술 축은 여전히 정적 Topic coverage가 없다.
- 잔여범위: 양자컴퓨팅 등 emerging technology의 최소 개념·계측제어 적용·한계/성숙도 평가 축이 필요하다.
- 신규 직접 Topic:
  - `industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread`

## 6. GAP 상세

### `IC-2027-W-5-2` 계측제어 관련 동향

- 판정: **GAP**
- 근거: 새 source Topic이 없고 roadmap도 의도적으로 정적 Topic 대신 DYNAMIC_REVIEW_LANE을 지정했다. Roadmap proximity/context hit는 planning evidence이지 현재 Topic Pack coverage evidence가 아니다.
- 잔여범위: 최신 동향·법령·표준을 주기적으로 갱신하는 별도 dynamic review workflow가 필요하다.
- 현재 직접 Topic: 없음
## 7. COVERED 해석상 주의점

- `IC-2027-W-4-1` 가용도·신뢰도는 PRIMARY Topic이 없지만,
  PLC/DCS/SCADA architecture와 industrial network resilience의 실제 evidence가
  MTBF, MTTR, availability, redundancy, SPOF, common-cause failure를 충분히 다루므로 COVERED로 판정한다.
- PRIMARY Topic 수가 0이라는 사실만으로 GAP을 의미하지 않는다.
- 반대로 관련 Topic이 존재해도 공식 criterion의 핵심 범위를 다루지 못하면 PARTIAL이다.

## 8. Source 정합성 별도 이슈

- `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`의
  model evidence에는 열전대와 RTD 내용이 혼재하는 정합성 이슈가 확인되어 있다.
- 이 source 정합성 이슈는 `IC-2027-W-2-1`의 COVERED 판정을 뒤집는 coverage blocker가 아니며 별도 source repair 대상으로 유지한다.
- Topic source repair는 coverage 분류 작업과 분리하여 별도 수행한다.

## 9. 확장 후 잔여범위 및 다음 단계

69개 Topic Pack 기준 semantic coverage는 `COVERED 30 / PARTIAL 2 / GAP 1`이다.

잔여범위는 다음 3개 criterion으로 한정한다.

- `IC-2027-W-4-2` **PARTIAL**: 방폭·본질안전은 확보했으나 철도·발전·건축 등 비폭발 위험환경의 적용별 제어요소와 대책이 남아 있다.
- `IC-2027-W-5-1` **PARTIAL**: AI/ML·Physical AI·Digital Twin·IIoT/Smart Factory는 확보했으나 양자컴퓨팅 등 기타 emerging technology 축이 남아 있다.
- `IC-2027-W-5-2` **GAP**: 정적 Topic Pack이 아니라 최신 동향·법령·표준을 주기적으로 갱신하는 `DYNAMIC_REVIEW_LANE`으로 관리한다.

다음 단계는 이 문서를 read-only로 재감사한 뒤 documentation-only commit 여부를 결정한다.
Question Type, Topic Pack source, generated rubric은 이 coverage 문서 갱신 단계에서 변경하지 않는다.
