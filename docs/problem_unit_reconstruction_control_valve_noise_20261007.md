# Control-valve noise Topic Pack 문제 단위 감사

작성일: 2026-10-07
대상: `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`

## 판정

이 Pack의 10개 질문 패턴은 모두 직접적인 질문문으로 작성되어 있고, 공력/수력 소음의 발생부터 전달·저감·측정까지 control-valve noise라는 공통 도메인 안에 있다. 다만 이를 하나의 단일 예상문제로 취급하기에는 음향 기초, 다중 소음원 dB 계산, 저감 대책/운전평가라는 독립 문항 family가 함께 들어 있다.

따라서 현재 단계에서는 내용을 억지로 서로 연결하거나 새 topic을 활성화하지 않는다. 패턴별 필수 Anchor는 기존대로 보존하고, Pack 제목의 “통합 소음설계 절차”를 모든 개별 문항의 공통 요구처럼 채점하지 않도록 한다. 실제 Topic 분리와 Router owner 변경은 교차 owner 검토(Stage 6)에서 결정한다.

## 문제 패턴과 경계

| 패턴 | 예상문제 핵심 | 경계 판정 |
|---|---|---|
| 1 | Sound power/pressure, dB·dBA, spectrum | 음향 기초 단독 문항으로 성립; trim 설계 불필요 |
| 2 | 독립 소음원 logarithmic sum, doubling | 다중 소음원 계산문항으로 성립; 독립 음원 가정과 동일 조건을 요구에 명시 |
| 3 | Gas turbulent jet·choked regime·Mach | 공력소음 문항; gas sizing 산출은 Topic 7 handoff |
| 4 | 액체 난류·cavitation·flashing 소음 | 수력소음 비교문항; phase regime 판정은 Topic 8 handoff |
| 5 | 내부 음향파워에서 외부 SPL까지 전달 | 음향 전달/예측 문항; 측정 위치 조건을 보존 |
| 6 | 다공·다단 저소음 트림 선정 | 발생원 저감 문항; 용량·막힘·정비 tradeoff 포함 |
| 7 | Diffuser와 path treatment 비교 | 압력강하 분담과 전달경로 대책을 구분하는 대책 문항 |
| 8 | 운전점별 noise risk 평가 | operating-case 평가 문항; 패턴 3/4 handoff 값은 입력이지 sizing 재계산 요구가 아님 |
| 9 | Vendor prediction과 현장측정 차이 진단 | 검증/진단 문항; prediction과 현장 규제값을 무조건 등치하지 않음 |
| 10 | 입력-예측-대책-검증 절차 | 통합 workflow 문항; 이 패턴에서만 여러 family 결합을 요구 |

## 감사 신호와 조치

- Atomicity screen: 38 Anchors, 10 patterns, required-anchor union 38/38; 경고 `DISCONNECTED_QUESTION_FAMILIES`는 연결요소 크기 1·7·2.
- 경고는 Pattern 1 및 2가 나머지 대책/운전 family와 required Anchor를 공유하지 않는 구조를 가리킨다. 이 두 문제는 그 자체로 독립 문항이 가능하므로 연결성을 높이기 위해 불필요한 Anchor를 required로 추가하지 않았다.
- Pattern 10은 넓은 종합문제이므로 Pattern 1/2의 모든 정량 내용을 포함하도록 확대하지 않았다. 그 확장은 문항 의도에 없는 과잉 요구를 만들 수 있다.
- Source model의 `high_score_points`와 `common_missing_points`는 아직 Pack 공통 목록이다. Question Pattern별 채점 범위로 런타임이 분기된다고 주장하지 않는다. 실제 scoring projection에서 문항별 차등이 필요하면 별도 adapter/계약 변경과 회귀가 선행되어야 한다.
- 2개 이상의 인접 Pack이 noise prediction/mitigation을 handoff로 언급하지만, 이는 현재 noise 원리·대책 Pack의 중복 owner를 입증하지 않는다. Router와 topic_id는 바꾸지 않는다.

## 변경 및 검증

Source JSON/Topic Sheet 변경 없음. 이번 감사는 경계 판정과 후속 owner 검토 항목을 기록한다.

- `validate_topic_packs.py --topic-id ...`: PASS (전체 2,066 Anchor uniqueness 포함)
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS, warning 1건 (기존 deterministic topic aliases empty)
- `audit_topic_pack_atomicity.py --topic-id ... --json`: PASS, warning 1건 (`DISCONNECTED_QUESTION_FAMILIES`, 분할 미확정으로 유지)

## 다음 소유권 검토에서 결정할 사항

1. Pattern 1 음향 기초와 Pattern 2 다중 소음원 계산을 noise 통합 Pack 안의 선택 하위 문제로 유지할지, 독립 owner 후보로 분리할지.
2. Pattern 3–9를 하나의 noise engineering workflow의 독립 하위문항으로 유지할지.
3. 이 결정을 내리기 전에는 routing alias, canonical topic taxonomy, fatal/scoring authority를 변경하지 않는다.
