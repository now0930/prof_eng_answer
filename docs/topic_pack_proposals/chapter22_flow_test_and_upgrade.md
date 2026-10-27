# Chapter 22 유량 Topic 시험·보강 제안

상태: **두 Pack 모두 사용자 검토·승인 완료(2026-10-27)**. `approve-topic --reviewer now0930`으로 승인 해시를 기록하고 `rubrics/generated/`를 도구로 재생성했다. 운영 컨테이너 반영 여부는 별도 확인이 필요하다. 출처는 [WordPress Chapter 22-1](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-22-1/)의 HTML이다. 첨부된 외부 교재 PDF는 OCR·Fact 승격 대상에서 제외한다.

## 재현 시험

`grading.scoring.deterministic_primary_grader.grade_deterministically`에 아래의 합성 질문·답안을 입력했다. 개인 세션 답안은 사용하지 않았다.

| 질문 축 | 질문만의 라우팅 | 결정론 결과 | 원인 |
| --- | --- | --- | --- |
| 차압식과 층류식의 차압–유량 관계·적용 조건 | 기존 배관 유량 Topic | 4.5/25, 선택된 DP 요구 `MISSING` | 질문 계약이 차압식 Anchor 하나만 선택하고 층류식을 소유하지 않음. 답안에 DP 설명이 있어도 canonical claim 추출 0건으로 기존 DP 요구까지 누락 처리됨. |
| 직사각형/V-notch 위어의 수두–유량 및 플룸 수몰 | 무관한 유공압 Topic | 4.5/25, 무관한 유공압 요구 4건 `MISSING` | 개수로 독립 owner가 운영 Pack에 없음. 유사도 fallback을 정답 Topic으로 해석할 수 없음. |

위 점수는 정답 수준의 라벨이 아니다. 현재 시스템의 오판정 증거다. Answer-sensitive routing은 금지하고, 문제문만으로 Topic 소유를 확정해야 한다.

## 로컬 후보 재채점 결과

| 합성 답안 | 변경 전 | 변경 후 | 요구 판정 |
| --- | ---: | ---: | --- |
| 차압식·층류식 관계와 조건 설명 | 4.5/25 | 16.0/25 | `SATISFIED 4` |
| 두 관계만 적고 적용조건 생략 | 별도 측정 없음 | 15.0/25 | `SATISFIED 2, MISSING 2` |
| 관계를 서로 뒤바꿈 | 별도 측정 없음 | 4.5/25 | `WRONG 2, MISSING 2` |
| 위어 2형식과 플룸 수몰의 조건부 관계 설명 | 4.5/25, 유공압 오연결 | 16.0/25, 개수로 초안 선택 | `SATISFIED 3` |
| 위어 지수 뒤바꿈·플룸 수몰 보정 불필요 주장 | 별도 측정 없음 | 4.5/25 | `WRONG 3` |

이 값은 개인 답안의 재채점이 아니라 공개 사실로 만든 짧은 합성 답안의 **로컬 결과**다. 특히 관계만 적은 짧은 답안의 15점은 현행 `technically_adequate_score_floor` 영향이 있어 별도 채점 일관성 점검 대상이다. 운영 컨테이너가 갱신되었다는 증거로 해석하지 않는다.

## 배관 유량 Pack 변경 후보

대상: `flow_measurement_meter_principles_velocity_selection`. 기존 `flow_dp_primary_element_conditions` Anchor의 조건부 제곱근 관계를 보존한다.

1. 독립 Anchor `flow_laminar_pressure_relation` 추가: 원형 관의 충분히 발달한 정상 층류·뉴턴 유체 등 전제에서 `Q = πr⁴Δp/(8μL)`이며, 정해진 관·유체 조건에서 `Q ∝ Δp`다. 기존 차압식 조임부의 `Q ∝ √Δp`와 혼동하지 않는다.
2. 별도 조건 Anchor `flow_dp_conversion_conditions`, `flow_laminar_regime_conditions`를 질문 계약에 포함해, 관계식만 적은 답안과 계수·점도·기하·유동조건까지 적은 답안을 구별한다.
3. 관계 주장에 대해 `proportional_to` canonical predicate를 쓰고, 뒤이은 짧은 조건 문장은 **한 개의 명시적 앞 문장 주어**가 있을 때만 `requires/qualified_by`로 연결한다. 다른 물리법칙 주장에는 주어를 자동 상속하지 않는다.
4. 정답·조건 누락·역전 오답(`DP 조임부 Q∝Δp`, `층류 저항 Q∝√Δp`)을 회귀로 고정했다. 기체의 실제/기준 체적유량은 이번 질문 요구에 포함되지 않아 별도 보류했다.

기술 근거: [NIST 유량계 개요](https://www.nist.gov/programs-projects/understanding-flow-meters), [NIST 기체 유량 기준 단위](https://www.nist.gov/pml/owm/metric-si/unit-conversion/pressure-and-gas-flow-unit-conversions), [NIST 기체 유량 표준](https://www.nist.gov/laboratories/tools-instruments/gas-flow-standards).

## 개수로 Topic 변경 후보

`rubric_manager.py add-topic`으로 관리 초안을 만들고 source JSON·Master 참조·정답/역전 오답 테스트를 작성했다. 사용자 검토·승인 후 `approve-topic`으로 승인 해시를 기록했다. 현재 코드의 question-only router는 source 디렉터리를 탐색하므로 승인과 release 검증이 모두 통과한 작업트리만 배포해야 한다.

기술 근거: [USGS 위어 수두–유량 관계](https://pubs.usgs.gov/wri/1992/4028/report.pdf), [USGS 플룸 수몰 보정](https://pubs.usgs.gov/twri/twri3-a14/pdf/twri_3-A14_a.pdf).

## 적용 게이트

Pack 변경 시 기존 사람 승인 해시가 무효화된다. 이 변경은 사용자가 README·source JSON·질문별 Anchor·오답 경계를 검토해 승인했으며, `approve-topic`으로 두 해시를 기록했다. 집중 회귀 11건, `validate-topic-pack-release --all`, `PROMOTE_GENERATED=0 scripts/validate_release.sh`, `rubric_manager.py validate-all`은 통과했다. 로컬 기본 generated 경로에서 재채점은 정답 16.0/25, 관계 역전 오답 4.5/25(두 문항 공통)였다. 운영 컨테이너 반영 여부는 별도로 확인해야 한다.
