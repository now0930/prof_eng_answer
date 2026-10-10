# 전체 Topic Pack Fact 출처 감사 (2026-10-10)

`rubrics/topic_packs`의 86개 Pack, 2,073개 Anchor를 비공개 WordPress source DB와
Master source reference에 대조했다. 재실행 명령은 다음과 같다.

```bash
python3 scripts/audit_all_topic_fact_sources.py --database /path/to/private/wordpress_sources.sqlite3
```

대상 DB는 read-only로 열며 보고서에는 Topic ID와 개수만 저장한다. 문장 원문,
추출 본문, 개인 답안, DB 경로는 보고서에 넣지 않는다. anchor statement의 단어가
현재 버전의 first-party 추출 본문에 포함되는 비율은 검토 우선순위 신호다. 의미가
맞다는 보증이나 자동 승인 기준으로 쓰지 않는다.

| 결과 | Anchor 수 |
|---|---:|
| first-party 추출 본문이 연결된 source에서 80% 이상 단어 신호 | 31 |
| 같은 조건에서 50–79% 신호 | 338 |
| 같은 조건에서 50% 미만 신호 | 804 |
| first-party 추출 본문 없음 | 900 |
| 합계 | 2,073 |

Master의 source reference 397건은 현재 DB와 비교해 `verified` 3, `unverified` 221,
`stale` 170, `unavailable` 3이다. 대표 3건은 사용자 위임 검토 후 승인 Fact
registry에 등록했고, 나머지 83개 Topic에는 승인 Fact를 만들지 않았다. 31건의
강한 단어 신호도 모두 승인으로 간주하지 않았다. 특히 여러 topic의 source가
오래된 버전이거나 추출문이 없어, 출처 본문과 개별 anchor의 기술 의미를 연결할
근거가 부족하다.

Topic별 집계와 위 수치의 재현 가능한 원자료는
[`full_topic_fact_source_audit_20261010.json`](../reports/full_topic_fact_source_audit_20261010.json)에
있다. 새 점수 경로는 아직 켜지지 않았으며, 승인 Fact 3개도 `score_effect=none`이다.
기존 점수에 기여시키려면 Topic별 demand-to-fact mapping과 Stage 5 점수 adapter,
독립 답안 평가가 뒤따라야 한다.
