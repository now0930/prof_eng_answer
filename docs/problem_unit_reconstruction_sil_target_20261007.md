# SIL 목표 결정 Topic Pack 문제 단위·coverage 재검토

일자: 2026-10-07
대상: `sil_target_determination_risk_reduction_and_lifecycle`
감사 기준: `docs/topic_pack_problem_unit_screen_20261006.csv`의 coverage 재검토 후보

## 판정

하나의 SIL 의사결정 학습 단위로 유지한다. 이 단위는 위험 시나리오에서 요구 SIL을 도출하고
실제 SIF의 설계·운전 증거로 이어지는 흐름이다. 다만 대표 문제 4종은 목적이 다르므로
각 답안의 필수 앵커는 해당 pattern의 `required_anchor_ids`만으로 제한한다.

## 대표 패턴과 필수 범위

| # | 문제 형태 | 필수 앵커 수 | 요지 |
|---:|---|---:|---|
| 1 | SIL 결정방법 + 실제 플랜트 운영 + 최신 이슈 | 14 | 위험 시나리오·허용위험·IPL·잔여빈도부터 목표 SIL, achieved 검증, 시험·운전·MOC·AI/OT까지 |
| 2 | 허용위험·기존 보호계층으로 RRF 및 목표 SIL 결정 | 9 | SIS/SIF 경계, 시나리오, tolerable risk, IPL, residual frequency, RRF/PFD 관계, mode와 SIL band |
| 3 | Risk graph·LOPA·QRA 비교 | 4 | 적용범위, 시나리오, 허용위험 및 LOPA에서의 IPL 조건 |
| 4 | Demand mode별 PFDavg/PFH 및 achieved 검증 | 4 | mode, target metric, SIL band와 전체 SIF 정량검증 |

전체 anchor 16개 중 패턴 required-anchor union은 14개(87.5%)다. `initiating_frequency_modifiers`와
`srs_lifecycle_handoff`는 답안 구조와 확장 참고로 남긴다. 관련 패턴에서 구체 설명이 유용할 수
있으나, 현재 네 질문의 공통 누락 감점 항목으로 삼지 않는다. 87.5%는 직접 연결률일 뿐
내용의 정확도·완성도 점수는 아니다.

## 확인된 문제와 수정

- 패턴 1은 실제 질문이 위험 감소 흐름, 플랜트 proof test/운전, 최신 AI·OT 이슈를 묻는데도
  기존 required list에서 hazard scenario, tolerable risk, 기존 IPL, residual frequency,
  SIL band 및 PST/proof test anchor가 빠져 있었다. 해당 핵심 흐름을 연결했다.
- 패턴 2는 RRF를 목표 SIL로 옮기는 질문인데 목표 PFD 관계와 mode 선택이 빠져 있었다.
  두 앵커를 추가해 빈도비-무차원 위험감소-성능지표 매핑을 검증할 수 있게 했다.
- 패턴 3은 방법 비교이며 패턴 1의 운전·시험·MOC·보안/AI 조건을 요구하지 않는다.
  패턴 4 역시 SIL 결정방법 비교나 lifecycle 세부를 공통으로 요구하지 않는다.
  Global high-score/common-missing 문구를 패턴별로 한정했다.
- 기존 5개 fatal 기술오류는 유지했다. 이는 잘못된 주장이 실제 답안에 나타날 때만 적용하며,
  PST·시험주기 같은 내용을 언급하지 않은 사실을 그 자체로 감점하지 않도록 README에 명시했다.
- Question Type, scoring contract, Router, deterministic scoring, fatal IDs와 release gates는
  변경하지 않았다.

## 검증 한계

검증은 source schema, 패턴-앵커 참조, 품질 및 scoped release pipeline을 대상으로 한다.
Runtime grader가 모든 상황에서 pattern별 필수앵커 경계를 강제한다는 새로운 코드를 추가한
것은 아니며, 기존 소비 계약을 건드리지 않고 Topic Pack과 authoring 문서에 평가 범위를
명시했다.
