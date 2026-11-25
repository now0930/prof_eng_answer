# P2-B7 실행 결과 — 2026-11-26

## 판정

P2-B7은 **부분 완료**다. 연구용 Claim 근거 정합성 검사와 두 개의 방어 개선을 구현하고 공개 합성 회귀를 실행했다. 등록된 28건 중 26건은 여전히 인식 보류이고, 비공개 보호 답안 143건을 새 코드 SHA에서 재생할 원본 입력이 없어 P2-B7 완료 게이트는 충족하지 못했다. P2-B 전체 완료와 P2-C 진입을 선언하지 않는다.

## 변경 및 실제 효과

- 기준: `84ccb704c1c70c51424ecf097baf86d0d55b7295`
- 구현 커밋: `e555e1267da5da1816951906b04537d2bd45ba78`
- `claim_fidelity_audit.py`가 원문 span/text, owner, assertion context, Claim tuple, 조건 및 명시 산술 연산을 판정 결과와 별도로 점검한다. 근거가 충분하지 않은 일치는 PASS로 승격하지 않고 `NOT_ESTABLISHED`로 남긴다.
- GEN-09의 “질량유량은 밀도와 체적유량의 합”은 추출기가 만든 `mass_flow equivalent_to volumetric_flow`가 기존 반대 관계 Fact와 충돌하는 것처럼 보였지만, 원문의 덧셈이 등가 관계를 입증하지 않는다. 최종 진단은 `RECOGNITION_UNCERTAIN / CLAIM_FIDELITY_FAILURE`; 실제 claim fidelity는 `FAIL / OPERATION_NOT_EQUIVALENCE`다. 이는 기술적 모순 판정으로 집계하지 않는다.
- GEN-26의 완결된 영어 문장은 `CONFIRMED_RELATION`으로 인식한다. 동사 없는 용어 나열과 인용문 방어 시험은 계속 `RECOGNITION_UNCERTAIN`이다.
- 수정된 추출/감사 경로는 진단 전용이다. `canonical_claim_extractor`와 결정론적 점수 산출 코드는 수정하지 않았다.

## 재생 결과

| 시험 집합 | 기준 결과 | 구현 SHA 결과 | 실행 오류 |
|---|---:|---:|---:|
| 기존 원본 111: 구조화 | 57/64 | 57/64 | 0 |
| 기존 원본 111: 자연어 | 38/47 | 38/47 | 0 |
| 검토 반영 111: 구조화 | 58/64 | 58/64 | 0 |
| 검토 반영 111: 자연어 | 39/47 | 39/47 | 0 |
| 원본 36 | 17/36 | 17/36 | 0 |
| 검토 반영 36 | 17/36 | 17/36 | 0 |
| 신규 인식 목표 28 | 목표 단위 종전 집계 없음 | 1 relation, 27 uncertain; fidelity 1 fail, 27 not established | 0 |
| 방어 사례 16 | 목표 단위 종전 집계 없음 | 1 relation, 15 uncertain | 0 |

111건과 36건에서 전체 일치 수는 기준선과 같지만 개별 관측 상태는 달라질 수 있다. 28건의 기대값 일치나 fixture 기반 수치는 독립 정확도 지표가 아니다. 개발자/ChatGPT 작성 라벨이며 독립 전문가 라벨은 0건이다.

## 테스트와 Gate

- Focused pytest: `43 passed`, exit 0.
- `rubric_manager.py validate-all`: PASS.
- Generated freshness: PASS, 6개 파일 재생성 결과와 일치.
- Topic Pack Release Gate: PASS. `smoke`는 `smoke_report` 부재로 SKIPPED.
- Release Candidate: 정확한 implementation commit `e555e1267da5da1816951906b04537d2bd45ba78`에서 `1713 passed, 0 failed, 2 skipped`, exit 0, `VALIDATION=PASS`.
- Actions는 최종 보고서 커밋 SHA에서 실행 예정이며 아직 미실행.
- 143개 보호 답안 재생: **NOT_RUN**. 로컬에서 찾은 이전 출력 snapshot은 같은 해시의 결과 파일일 뿐 입력 답안이 아니므로 새 SHA의 재생 증거로 재사용하지 않았다. 비공개 입력을 저장소에 복원하거나 재구성하지 않았다.

## 한계 및 보호 상태

- 목표 28건 중 GEN-26 외의 자연어 동등표현·수식·조건 귀속 문제는 여전히 보류다. 26건을 해결했다고 주장하지 않는다.
- `claim_fidelity=PASS`는 0건이다. 구조적 tuple/span 확인만으로 독립적인 source semantic entailment를 입증하지 않는다.
- 독립 정확도는 `NOT_ESTABLISHED`다.
- Fact Anchor, Registry, Generated, 119 HOLD, D4, A~E 권한, Fatal/WRONG/Ceiling, 배점은 변경하지 않았다.
- `score_admission=DISABLED`, `score_effect=none`; main merge, 배포, 봇 재시작은 하지 않았다.
- P2-B7 PARTIAL, P2-B 전체 NOT_COMPLETE, P2-C NOT_ENTERED.

기계 판독 집계와 해시는 `p2b_b7_execution_results_20261126.json`에 기록한다.
