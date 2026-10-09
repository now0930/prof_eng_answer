# LVDT/RVDT Topic Pack 문제 단위 감사

작성일: 2026-10-07
대상: `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error`

## 판정

이 Pack은 LVDT의 차동변압기 원리·신호조절·오차와 RVDT 회전각 측정을 다루는 독립 센서 주제로 유지한다. 14개 예상 질문과 예시는 서로 일치하며, 원자성 감사 경고도 없다. 단, 이 주제 안의 세부 질문마다 요구 지식은 다르므로 고득점·누락·중요도 조건을 질문별로 한정했다.

LVDT와 스트레인 게이지식 변위센서 비교 질문은 plausible한 비교 문항이나 기존 계약에는 LVDT 쪽 Anchor만 있었다. 상세 스트레인 게이지 회로를 이 Pack에 복제하지 않고, 두 센서의 변환원리 차이만 담은 supporting-level Anchor를 추가했다. 상세 브리지·보상·게이지율·탄성체 설계는 기존 스트레인 게이지·로드셀 Topic의 owner로 남긴다.

## 수정

- required Anchor union에서 빠졌던 `lvdt_demodulated_zero_offset`을 영점 잔류전압 패턴 8에 연결했다. 원시 센서 AC null residual과 신호조절기 복조 후 DC offset은 별도 현상이므로 구분을 유지한다.
- 비교 문항에 `lvdt_vs_strain_gauge_displacement_principle`을 추가해 LVDT 자기결합/차동전압과 스트레인 게이지 변형/저항변화/브리지 변환을 간결하게 대비했다. 공식 문서에 원리를 대조했고, 별도 스트레인 게이지 설계 detail은 이 Pack에 들여오지 않았다.
- 14개 권장 답안 outline을 section/intent/anchor_refs 구조로 바꾸어 22개 Anchor 전부가 답안 구조에도 추적되게 했다.
- `high_score_points`, `common_missing_points`, importance unlock을 질문 패턴별 범위로 한정했다. 기본구조·영점·복조·여자·선형범위·현장 오차·RVDT 비교가 서로 무관한 문항에 필수로 번지지 않게 했다.
- 요구사항 Topic Sheet와 README의 Anchor/Fatal 수량을 Source 계약(22 Anchor, 10 Fatal)에 맞추고, Logic Check에 비교 원리 truth를 연결했다. Source의 Fatal 10건 중 null residual 부정 주장이 누락돼 있던 점도 기존 Logic Check의 10개 fatal conditions와 일치시켰다.
- Topic ID, Question Type, routing aliases/authority, 기존 fatal scoring behavior, deterministic authority, 점수계약은 변경하지 않았다.

## 검증

- Schema validation: PASS; 전체 source inventory 87 Pack / 2,067 Anchor 확인.
- Topic quality (`--require-logic-check`): PASS, errors 0, warnings 0.
- Atomicity audit: PASS, warnings 0.
- 14 patterns / 14 examples 일치.
- Required-anchor union: 22/22; outline Anchor refs: 22/22; 외부/미정의 Anchor 참조 0.
- Fatal Wrong Claim: 10개; Logic Check fatal conditions: 10개.
- Scoped release: PASS; generated pipeline PASS, smoke SKIPPED. validator가 generated files를 사전 snapshot으로 복원했다.
- 전용 LVDT/RVDT regression 파일은 `tests/`, `scripts/` 최상위에서 찾지 못해 실행하지 않았다.
- `git diff --check`: PASS.

## 출처 및 경계

- [TE Connectivity LVDT Tutorial](https://www.te.com/en/products/sensors/position-sensors/resources/lvdt-tutorial.html): 코일·가동철심 구조, 교류 여자, 직렬 역접속, 차동 AC 출력과 위상 방향.
- [NI Measuring Strain with Strain Gages](https://www.ni.com/getting-started/set-up-hardware/data-acquisition/i/strain-gages): 저항 변화 및 Wheatstone bridge 측정원리.

출처는 비교 앵커의 원리 확인에만 사용했으며 제품별 수치나 라우팅을 변경하지 않았다. 본 감사는 Source 구조 검토이며 Topic Pack 내용의 사용자 최종승인을 대신하지 않는다.
