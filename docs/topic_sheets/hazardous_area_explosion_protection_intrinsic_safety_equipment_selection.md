# 위험장소 방폭 방식, 본질안전 회로 및 계측기기 선정

## 0. Topic identity

- Topic ID: `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
- Official criterion: `IC-2027-W-4-2`
- Official scope label: 위험 환경 제어요소/대책
- Question Type: `COMPARE_SELECTION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Historical frequency: 근거가 없어 사용하지 않음
- Grading mode: LLM semantic review 중심
- Deterministic fatal keyword rule: 사용하지 않음

## 1. 출제 의도

이 Topic은 위험장소에서 계측·제어기기를 안전하게 선정하는 능력을 평가한다.
핵심은 방폭 명칭의 나열이 아니다.
`위험장소 분류 → 요구 EPL → 보호방식 비교 → Ex marking 및 인증조건 확인 → 본질안전 loop 정합 → 설치·검사`의 흐름을 설명해야 한다.

## 2. 핵심 범위

1. 폭발성 분위기의 존재 가능성과 지속시간에 따른 위험장소 분류
2. 가스·증기 Zone 0/1/2와 분진 Zone 20/21/22
3. Zone과 EPL Ga/Gb/Gc, Da/Db/Dc의 연결
4. Ex marking, 물질 그룹, 온도조건, marked ambient range
5. Ex d, Ex e, Ex i, Ex p의 보호원리와 선정조건
6. Ex m, 분진용 Ex t의 기본 적용개념
7. Ex ia, Ex ib, Ex ic 보호수준 차이
8. 본질안전 field apparatus, associated apparatus, barrier/isolator, cable
9. Entity parameter: `Uo ≤ Ui`, `Io ≤ Ii`, `Po ≤ Pi`
10. 케이블 포함 정전용량·인덕턴스와 `Co`, `Lo` 또는 인증서의 system limit
11. Zener barrier와 galvanic isolator의 절연·접지·유지보수 차이
12. IS/non-IS 배선 분리·식별·차폐·접지
13. certificate special conditions, control drawing, cable gland와 단자조건
14. IP·부식·진동·재질 등 환경 적합성의 별도 검토
15. 위험장소 도면·기기목록·인증서·IS calculation·검사/정비 이력

## 3. 선정 논리

### 3.1 먼저 위험장소를 분류한다

Zone은 폭발성 분위기의 존재 빈도와 지속시간을 나타낸다.
가스·증기와 가연성 분진은 서로 다른 Zone 체계를 사용하므로 혼용하지 않는다.
분류 결과는 필요한 EPL과 보호방식 선정의 시작점이다.

### 3.2 Zone을 EPL 요구로 변환한다

일반적인 EPL 선정 관계는 다음과 같다.

- Gas: Zone 0 → Ga, Zone 1 → Ga/Gb, Zone 2 → Ga/Gb/Gc
- Dust: Zone 20 → Da, Zone 21 → Da/Db, Zone 22 → Da/Db/Dc

단, 실제 적용은 해당 기기의 인증 표기와 인증서 조건을 기준으로 최종 확인한다.

### 3.3 보호방식의 원리를 비교한다

- `Ex d`: 내부 폭발압력을 견디고 화염이 외부로 전파되지 않도록 한다.
- `Ex e`: 정상 및 규정 조건에서 점화원이 생길 가능성을 낮추도록 절연·접속·온도상승을 강화한다.
- `Ex i`: 회로의 전기·열 에너지를 제한하여 규정된 고장조건에서도 점화를 방지한다.
- `Ex p`: 보호가스 퍼지와 과압을 이용하고 필요한 감시·인터록을 구성한다.
- `Ex m`: 점화원이 될 수 있는 부품을 컴파운드로 봉입한다.
- `Ex t`: 분진 침입 방지와 표면온도 제한을 이용한다.

보호방식 이름만 보고 Zone을 결정하지 않는다.
인증된 EPL과 전체 marking을 확인한다.

## 4. 본질안전 계측루프

본질안전은 현장기기 하나의 특성이 아니라 loop system의 적합성이다.

`Field IS apparatus → cable → barrier/galvanic isolator 또는 associated apparatus → safe-area circuit`

Entity parameter 방식의 기본 방향은 다음과 같다.

- `Uo ≤ Ui`
- `Io ≤ Ii`
- `Po ≤ Pi`
- 현장기기와 cable의 정전용량 합 ≤ 인증된 `Co` 또는 certificate limit
- 현장기기와 cable의 인덕턴스 합 ≤ 인증된 `Lo` 또는 certificate limit

C와 L을 동시에 사용하는 경우에는 단순히 개별 최대값만 적용하지 않고 certificate/control drawing이 정한 동시 조합 제한을 우선한다.

## 5. Zener barrier와 galvanic isolator

Zener barrier는 고장 에너지를 제한·우회하는 구조이므로 인증된 접지·등전위 조건이 중요하다.
Galvanic isolator는 전기적 절연을 제공하여 safe side와 IS side를 분리한다.
두 방식은 전원, 정확도, 접지, loop resistance, 유지보수 및 인증조건이 다르므로 설비조건에 따라 비교한다.
어느 방식이 항상 우월하다고 단정하지 않는다.

## 6. 설치와 인증조건

기기가 인증되었다고 설치 전체가 자동 적합해지는 것은 아니다.
다음을 함께 확인한다.

- Ex marking과 EPL
- gas/dust group
- temperature class 또는 maximum surface temperature
- marked ambient range
- certificate special condition
- cable gland, blanking element, terminal 조건
- IS/non-IS segregation과 identification
- shield/earth 방식
- IP, corrosion, vibration, material compatibility

## 7. 유지관리

위험장소 도면, 기기목록, certificate, control drawing, IS calculation, 설치검사 및 정비기록을 유지한다.
기기·barrier·cable·gland·배선경로가 변경되면 기존 적합성을 그대로 가정하지 않고 다시 확인한다.

## 8. 인접 Topic과의 ownership 경계

### 본 Topic이 소유하는 범위

- 위험장소 분류와 방폭기기 선정
- Ex protection method 비교
- intrinsic safety system과 Entity parameter
- 인증·배선·설치 적합성

### 본 Topic이 소유하지 않는 범위

- `sis_sil_safety_software_independence_systematic_failure_verification_validation`: SIL, SIS software independence, systematic failure, verification/validation
- `final_control_element_sil_sis_esd_valve_partial_stroke_test`: ESD valve와 final element SIL/PST
- OT cybersecurity 또는 industrial network의 보안·통신 성능
- 공정 전체의 화재·폭발 위험성 평가 또는 비전기 점화원 전반

SIS가 방폭설비와 같은 현장에 존재할 수는 있으나 `Explosion protection`과 `Functional safety integrity`는 동일 개념이 아니다.

## 9. 표준 기반

답안은 적용 관할의 현행 채택표준과 인증조건을 확인하는 것을 원칙으로 한다.
기술적 기준축으로 다음 IEC 60079 계열 범위를 사용한다.

- IEC 60079-0: 일반 요구사항
- IEC 60079-10-1: 가스 위험장소 분류
- IEC 60079-10-2: 분진 위험장소 분류
- IEC 60079-11: intrinsic safety `i`
- IEC 60079-14: 설계·기기선정·설치
- IEC 60079-17: 검사·정비
- IEC 60079-25: intrinsically safe electrical systems
- IEC 60079-31: dust ignition protection by enclosure `t`

특정 판년을 암기 점수요소로 사용하지 않는다.
인증서와 적용 관할의 현행 요구가 우선한다.

## 10. 고득점 답안 구조

1. 위험장소 분류의 목적
2. Gas/Dust Zone과 EPL
3. 주요 protection method 원리 비교
4. intrinsic safety level과 loop 구성
5. Entity parameter와 cable C/L
6. barrier vs isolator
7. marking/certificate/installation 확인
8. inspection, maintenance, change verification

## 11. Fatal 오개념

- Zone 0에서 아무 Ex 기기나 사용할 수 있다고 단정
- 본질안전을 무전원 회로로 정의
- ia/ib/ic를 동일 보호수준으로 취급
- `Uo ≥ Ui` 등 Entity parameter 방향을 반대로 설명
- cable C/L을 무시
- Ex d가 내부 폭발 자체를 원천 차단한다고 설명
- IP rating을 방폭 인증과 동일시
- certificate가 있으면 gland·배선·special condition을 무시해도 된다고 설명
- 본질안전이면 모든 활선 작업이 무조건 허용된다고 설명

## 12. STEP 1 authoring decision

- Question Type: `COMPARE_SELECTION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- 근거: 위험장소 분류와 보호방식의 지식만이 아니라 실제 장비·loop·인증조건의 비교·선정이 중심이다.
- Historical frequency: 사용하지 않음
