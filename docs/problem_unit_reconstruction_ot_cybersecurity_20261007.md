# OT Cybersecurity Topic Pack 문제 단위 보충 감사

## 범위와 수정

대상은 `ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response` (10 patterns, 40 Fact Anchors)다.

- 10개 pattern에 문제별 intent를 추가했다.
- SUC, secure configuration baseline, IDS/IPS monitoring, security change control 및 lifecycle decommissioning Anchor를 각각 관련 architecture, access, monitoring, patch/change, recovery 문항에 연결했다. Required union은 40/40이다.
- High-score, common-missing 및 importance 기준을 P1–P10 문제 범위에 연결하고 P7–P10 공급망·탐지·사고대응·복구의 고득점 기준을 보완했다.
- SW-06 운영변경/Backup, SW-07 통신기능, SW-08 네트워크 복원력과의 owner handoff를 유지했다. Question Type, aliases, routing 권한, fatal 및 deterministic 처리에는 변경이 없다.

## 경계 판정과 잔여 신호

이 Pack은 OT cybersecurity라는 하나의 통합 domain 아래 10개의 서로 다른 예상문항을 보유한다. Atomicity audit은 연결요소 8개 및 40-anchor 대형 inventory 경고를 계속 보고한다. 요구가 다른 패턴 사이에 Anchor를 인위적으로 연결하지 않고 현행 owner를 보존했으며, Stage 6 cross-topic ownership 검토에서 domain 분리 여부를 판단할 후보로 남긴다. 경고 2건은 오류가 아니다.

## 검증

- 새 범위/intent/anchor contract test 통과.
- 기존 OT Cybersecurity focused regression: 41/41 PASS.
- Scoped release validation PASS; generated output은 사전 snapshot으로 복원했다.
- schema validation PASS, quality errors 0 / warnings 0.
- atomicity audit은 error 0, 경고 2건(위 연결요소·대형 inventory)을 유지한다.
- 기술 규격별 compliance 검증 또는 사람의 의미 승인을 뜻하지 않는다.
