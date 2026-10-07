# Smart Positioner 진단 Topic Pack 보충 감사

## 범위와 판정

대상은 `smart_positioner_diagnostics_valve_signature_predictive_maintenance`이다. Screen inventory의 대형 Anchor 집합(44개) 경고를 확인한 보충 감사다. 이번 작업은 routing owner를 변경하거나 legacy pack의 공식 승인 상태를 가장하지 않는다.

## 확인 및 변경

- 10개 질문 패턴은 diagnostic data chain, signature mode, travel/pressure feature, pneumatic·sensor diagnosis, usage trend, confidence, maintenance strategy, workflow 및 asset integration으로 구분된다.
- 각 패턴 intent가 구체적이고 required Anchor union이 44/44로 전부 연결되어 있어 Anchor를 추가하지 않았다.
- High-score, common-missing 및 importance 조건에 P1–P10 적용 범위를 명시했다. 특히 Topic 13 leakage 및 Topic 15 PST handoff를 P10 경계 조건으로 두어 모든 문항의 요구조건처럼 확산되지 않게 했다.
- Question Type, routing aliases, required-anchor 연결, fatal/logic 처리와 evaluator 권한은 변경하지 않았다.

## 검증

- 전용 pattern-scope test: 3개 검증 항목.
- 기존 focused router/semantic regression: 46/46 PASS. Scoped release 경로에서 source/generated equality와 전체 87-topic source inventory가 동기화된 임시 projection으로 확인됐다.
- Schema validation PASS, quality errors 0 / warning 1; atomicity errors 0 / warning 1(`LARGE_ANCHOR_INVENTORY`, 44개). 10문항 owner 경계는 하나의 진단-검증-정비 흐름이며 전체 Anchor union 44/44인 사실을 확인했으나 inventory 경고는 그대로 기록한다.
- 기존 smart-positioner 회귀는 source와 generated projection 일치 및 전체 source inventory 일치를 요구한다. 현재 생성본이 원천 변경 전 snapshot이라 원천 편집 직후에는 stale projection 실패가 예상된다. 통합 검증 시 생성본을 임시 재생성해 테스트하고, 이번 작업에서 generated bank는 promote하지 않는다.
- 구조·내용 검증은 기술 표준 또는 현장별 기준의 전문가 승인을 뜻하지 않는다.
