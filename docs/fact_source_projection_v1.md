# WordPress 출처의 읽기 전용 Fact 후보 projection

Stage 2의 현재 구현은 `study/wordpress_fact_projection.py`다. Master의 출처 참조와
비공개 WordPress catalog를 `source_id`로 대조하고 URL·버전·콘텐츠 SHA-256 및
본문 발췌 근거를 확인한다. DB 접근은 `mode=ro`와 `query_only`를 사용한다.
본문이나 개인 DB를 Git에 복사하지 않는다.
Master 출처 계약에는 선택적 `content_sha256`을 추가했다. 기존 Master를 일괄
갱신하지 않으며 승인된 기준 hash가 없으면 `verified`로 판단하지 않는다.

| 결과 | 뜻 | Fact 승격 |
|---|---|---|
| `verified` | Master 검증 상태와 DB URL·버전·hash가 맞고 본문을 읽을 수 있음 | 자동 승격 불가 |
| `unverified` | 기술 출처 연결은 있으나 Master 검증 상태가 미확정 | 불가 |
| `stale` | URL·버전 불일치 또는 Master가 stale로 표기 | 불가 |
| `unavailable` | DB 자료 부재, 추출 불가 또는 hash 부재 | 불가 |

이미 승인된 WordPress *claim*에 명시적 관계 binding을 제공해도 출력은 항상
`review_status=candidate`, `score_effect=none`인 Fact 후보이다. 출처 연결 승인,
claim 승인, Fact의 정오 승인, 실제 Grading View 적용은 서로 다른 단계다. 특히
LLM이 만든 관계 binding은 원문과 일치해도 기술 사실 승인으로 취급하지 않는다.
후보는 기존 content update proposal과 사람 승인 절차를 통과해야 한다.

2026-10-10의 비공개 DB 읽기 전용 점검 집계(원문 미보관): 86개 Master의 출처 참조
397건 가운데 `unverified` 224건, `stale` 170건, `unavailable` 3건,
`verified` 0건. 대표 세 Topic은 SIL 목표 결정 4건 전부 unverified, V-Model
4건 전부 unverified, Nyquist 20건 중 stale 17건·unverified 3건이다.
따라서 이 단계에서 대표 Topic의 채점용 Fact를 갱신했다고 주장할 수 없다.

집중 테스트는 합성 자료만 사용한다:
`python3 -m pytest -q tests/test_wordpress_fact_projection.py`.
운영 적용 전에는 개인 DB의 최신 snapshot과 Master 검증 상태를 재확인해야 한다.
