# WordPress 출처의 읽기 전용 Fact 후보 projection

## WordPress 출처 상태와 Fact 진위는 별도 판정

Master의 WordPress `verification_status`는 URL·버전·해시 등 **그 WordPress 자료의
동일성/최신성**만 뜻한다. Fact 자체의 `approved`/검증 여부를 대리하지 않는다.
WordPress 출처가 없거나 stale이어도 표준, 정부·공식 기술 문서, peer-reviewed
연구, 권위 있는 교재, 재현 가능한 계산 등 독립 근거가 Fact의 범위와 조건을
뒷받침하면 Fact를 검증할 수 있다. 이때 WordPress source 상태는 그대로 둔다.

반대로 출처가 없다는 사실이나 LLM의 확신만으로 `verified`/`approved`로 승격하지
않는다. 승인 Fact에는 `verification_refs`에 근거 종류, 식별 가능한 서지정보,
판본, 위치, 확인일, 해당 근거가 뒷받침하는 주장 범위를 기록한다. 근거가 주장의
일부만 지지하면 Fact 문구를 그 범위로 좁히고, 충돌하거나 최신성을 확인하지
못하면 `candidate` 또는 `conflict`로 남긴다. 외부 근거가 없어도 수학적으로
재현 가능한 항등식·계산은 가정, 식, 단위, 결과를 별도 근거로 남길 수 있다.

`source_refs`는 WordPress provenance가 있을 때만 채우며 비워 둘 수 있다. 참조가
존재해도 그 WordPress 자료의 현재성 검사는 별도 출처 감사이며 Fact 승인을 막지 않는다.
`verification_refs`는 Fact의 기술적 정오 판단 근거이며 승인된 Fact는 이를
기록하고 `verification_status=verified`로 표시한다. 두 필드는 서로 대체되지
않는다. 이 계약은 점수 효과를 부여하지 않으며(`score_effect=none`), 현행
deterministic grader에는 자동 반영되지 않는다.

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

초기 점검 당시 Master 출처 397건은 unverified 224건, stale 170건,
unavailable 3건, verified 0건이었다. 이후 사용자가 검토를 위임하여 대표 3개
Topic에서 확인한 post source 3건의 URL·버전·DB hash를 Master에 기록하고
verified로 갱신했다. 현재 상태는 verified 3건, unverified 221건,
stale 170건, unavailable 3건이다. Nyquist의 다른 이미지 source 17건은 여전히
Master 버전과 DB ETag가 달라 stale이다.

초기 대표 Topic Stage 1에는 28개 Fact가 등록됐으며, 이후 독립적인 전체 Topic Pack
Anchor 검토가 진행 중이다. 현재 registry는 1,033 records / 1,032 unique Topic–Anchor
mappings를 보유한다. 전체 현황과 미해결 수는
[`all_topic_fact_source_audit.md`](all_topic_fact_source_audit.md)에서 관리한다.
WordPress `source_refs`가 없어도 독립 근거가 주장을 뒷받침하면 Fact를 검증할 수 있다.
registry의 Fact는 승인된 입력 지식이지만 모두 `score_effect=none`이고 현행 B/C/D/E
점수 적용 경로에 자동 연결되지 않는다. 미해결 Anchor는 검토 완료 전까지
승인/verified로 간주하지 않는다.

집중 테스트는 합성 자료만 사용한다:
`python3 -m pytest -q tests/test_wordpress_fact_projection.py`.
운영 적용 전에는 개인 DB의 최신 snapshot과 Master 검증 상태를 재확인해야 한다.
