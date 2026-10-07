# FTA/Markov/RBD Topic Pack 문제 단위·coverage 재검토

일자: 2026-10-07
대상: `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh`
감사 기준: `docs/topic_pack_problem_unit_screen_20261006.csv`의 coverage 재검토 후보

## 판정

일반 기능안전 하드웨어 신뢰도 모델링이라는 하나의 학습 지식영역으로 유지한다. 8개
대표 패턴은 그 안에서 서로 다른 문제 단위(모델 비교, 성능지표, voting/CCF, 시험·진단,
전체 SIF, systematic 경계, 입력자료)를 대표한다. 모든 문제에 모든 앵커를 공통 요구하지
않으며 pattern별 `required_anchor_ids`가 해당 문항의 필수 범위다.

## 패턴별 필수범위

| # | 문제 형태 | 필수 앵커 수 | 검토 |
|---:|---|---:|---|
| 1 | RBD·FTA·Markov 비교와 적용 | 5 | RBD 성공경로와 직렬·병렬, FTA Top Event, Markov 상태전이, 모델 목적 경계 |
| 2 | PFDavg·PFH와 demand mode 구분 | 3 | 지표 정의와 mode 선택; 근사공식 사용을 요구하지 않으므로 근사조건을 필수에서 제외 |
| 3 | 1oo1·1oo2·2oo2·2oo3 voting 특성 | 4 | voting trade-off, HFT 단독 한계, CCF 및 β-factor |
| 4 | CCF·진단·Proof Test가 PFDavg에 미치는 영향 | 4 | CCF, β-factor, DC/PTC 구분, 시험주기와 잠복고장 노출 |
| 5 | Sensor–Logic–Final Element 전체 SIF 평가 | 3 | 전체 경계, 구성품 인증 한계, 계산 가정 기록 |
| 6 | 정량 hardware vs systematic integrity | 3 | 정량·체계적 경계와 구성요소/HFT 단독 보증 한계 |
| 7 | Proof Test와 PST의 검출범위 | 4 | 검출 목적, interval, 부분시험 잔류고장, DC/PTC 구분 |
| 8 | 계산 입력·가정·한계·검증 | 3 | 근사조건, CCF 완화 가정, 데이터·가정 문서화 |

현재 pattern required-anchor union은 26개 중 22개(84.6%)다. 다음 4개는 학습상 유용한
확장·심화 사실이나 현재 문구만으로 모든 답안에 필수라고 단정하지 않는다.

- `fsrm_minimal_cut_set`: FTA 심화 산출물. 질문이 cut set 분석을 요구할 때 다룬다.
- `fsrm_markov_complexity`: 모델 선택의 심화 장단점. 비교 답안의 기본 설명을 대체하지 않는다.
- `fsrm_one_oo_one_low_demand_approximation`: 실제 근사식을 사용하는 계산문항에서 적용한다.
- `fsrm_rrf_relationship`: Target SIL/위험 할당의 상세는 인접 SIL target pack이 우선 소유한다.

이 비율은 문항 연결률이지 지식 완성도나 점수 기준이 아니다.

## 수정 사항

- Pattern 1에 RBD의 직렬·병렬 성공경로 앵커를 추가했다. RBD 기본 모델 설명의 핵심이어서
  비교·적용 문제의 필수 지식으로 판단했다.
- Pattern 2에서 `fsrm_approximation_conditions`를 제거했다. PFDavg와 PFH의 적용 mode를
  설명하는 문항은 특정 1oo1 근사식을 쓰지 않아도 답할 수 있다. 해당 앵커는 계산 가정
  문항인 Pattern 8에 남겼다.
- 12개의 전역 고득점·10개의 공통 누락 서술을 패턴별로 다시 작성했다. 예를 들어 Pattern 1의
  모델 비교 답안에서 CCF/PST/전체 SIF 계산을 빠뜨렸다는 이유로 감점하지 않는다.
- 기존 anchor 26개, fatal 조건, Question Type, Router, scoring contract 및 deterministic
  authority는 변경하지 않았다.

## 검증 한계

Topic Pack schema·quality·generated release와 관련 구조 테스트를 검증한다. Runtime grader가
모든 경우 pattern별 범위를 강제한다는 새로운 코드를 만들지는 않았다. 현재 작업은 source
계약과 Topic Sheet에 범위를 명시하고, protected grader 코드는 보존한다.
