# S7 Registry Formula Shadow — 제한된 수식 인식 연구 (2026-11-16)

**상태: 코드 작성, 새 HEAD 전체 CI 미검증, HOLD 119개 유지.**

## 목적

Actions #43867828959에서 40개의 작성자 초안(정합 주장 20 / 반례 20)은 현재 canonical Claim extractor로 0개 EXACT_RELATION을 기록했다. 별도로 source-review에서 검증된 Fact 관계를 투영해도, canonical parser의 Machine Contract 후보와 Ontology ID coverage가 맞지 않아 목표 관계가 추출되지 않는다. 무분별한 새 is/equals/maps Alias는 오답 인식 위험이 있다.

이번 작업은 **운영 파서·Machine Contract·Ontology·Registry를 전혀 수정하지 않는** 독립 연구용 수식 패턴 검사기를 추가한다. 선택한 6개 고유 검증 Registry Fact의 Owner/Source ID/Subject/Predicate/Object/Polarity/전체 Condition ID가 기존 source-review와 정확히 일치할 때만 검사한다.

## 대상

| 기술 범위 | 고유 Fact | 제한된 문자 표면 검사 |
|---|---|---|
| 밸브 불평형 힘 | unbalanced_force_equation | ΔP × Au와 ΔP / Au 구별 |
| LOPA/SIL 요구 RRF | hazop_lopa_required_rrf, required_rrf_relation | F_residual/F_tolerable과 역수 구별 |
| 목표 PFD | hazop_lopa_pfdavg_rrf_relation, target_pfd_relation | PFDavg <= 1/RRF와 >= 구별 |
| Nyquist | argument_principle_pnz_relation | 시계방향 양수 N_cw=Z-P와 N_cw=P-Z 구별 |

총 6개 Relation × (작성자 정합/오류 초안) 2문장 = **12개 문장 표면 비교**만 수행한다. 나머지 14개 Relation에는 신규 인식 규칙을 추가하지 않았다.

## 중요한 제한

- EXPECTED_FORMULA_SYNTAX는 수학 표기의 **패턴 후보**이며 정답 승인이나 EXACT_RELATION이 아니다.
- 동시 기록하는 qualifier_cue_present_not_validated는 오직 문장 중 조건 관련 문자 단서의 존재를 뜻한다. 실제 공정 조건, 같은 사건과 시간 기준, 수식의 정의역을 증명하지 않는다.
- 40개 초안은 독립 전문가가 판정한 라벨이 아니므로 measured_precision / measured_recall / measured_accuracy는 계속 null.
- 오답 초안이 기대 수식 패턴과 일치하면 COUNTEREXAMPLE_PATTERN_COLLISION_REVIEW로 기록하고 스크립트는 exit 2. 워크플로에서 연구 step은 continue-on-error이므로 반드시 해당 step과 Artifact를 독립 확인한다.
- Registry source ID, Relation, Condition 중 어느 것이라도 달라지면 중단한다. 기존 HOLD를 ACCEPT로 변경하는 것도 차단한다.
- 출력 Artifact는 case/Fact/Source ID, Formula Family, 패턴 결과 및 조건 단서 존재 여부만 기록하며 학습자 답안 원문이나 테스트 문장 원문은 저장하지 않는다.
- A~E 점수, Fatal, WRONG, ceiling, 합격선, Fact SUPPORTED 상태 및 score_admission은 변경하지 않는다.

## 검증 순서

기존 PR #38의 feat/claim-alignment-verification-20261114에서 validation workflow를 수동 실행하며, Replay 47 Golden cases and audit 179 missing aliases (research only)를 ON으로 유지한다. 아래를 분리 확인한다.

1. 전체 pytest 및 Release Validation PASS 여부 (새 HEAD SHA 기준).
2. 47 Golden + 예상 1 abstention, 179 Alias gap/119 unique source 동일 여부.
3. 기존 negative-challenge Artifact의 canonical EXACT positive=0/negative=0은 여전히 별도 측정.
4. 새 s7-registry-formula-shadow Artifact에서 6개 수식 표면 후보와 역방향 패턴 결과 확인.
5. 새로운 Alias 승인이나 점수 반영은 금지. 독립 expert label과 조건/부정/단위/서술형 변형 테스트 후 별도 단계로 심사.

**지금은 Parser의 실제 자연어 인식률을 개선했다고 주장하지 않는다.** 이 단계는 전체 ID 자동 확장의 위험을 피하면서 검증된 Source Relation과 수식의 방향성 검사 연결을 시험하는 연구용 발판이다. B7 / D2 / D3는 OPEN, PR은 Draft이며 main 병합·운영 배포·서비스 재시작은 금지한다.
