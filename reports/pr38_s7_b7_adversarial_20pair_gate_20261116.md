# PR #38 · S7 B7 우선 20개 Fact의 오답·역방향 도전 사례 (2026-11-16)

> **코드 구현 완료 / 새 HEAD 테스트 및 도전 실험은 아직 미실행 / Fact Alias 승인 0건.** 이전 Actions [#43857497079](https://github.com/now0930/prof_eng_answer/actions/runs/43857497079)의 `VALIDATION=PASS`는 **기존 `ed8713d` HEAD**의 결과이며, 이 보고서의 새 HEAD를 검증한 결과가 아니다.

## 배경과 범위

- S7 47 Golden graded + 1 expected policy abstention → 179 Alias `ID_NOT_FOUND` 투영(119 unique Fact), `score_admission=DISABLED`. 기존 Registry와 119 Fact 원문/근거 ID 연결 성공. 각 Fact Alias의 기술적 동등성은 아직 승인되지 않았다.
- 우선심사 대상 20개는 broad Predicate 위험 18 + formula/direction 위험 11의 **9개 중복을 제외한 합집합**이다. 기존 [20 Fact별 의미·오인정 반례 심사](./pr38_s7_b7_priority20_claim_semantics_review_20261116.md)도 20 HOLD 상태다.
- **새 `calibration/s7_alias_negative_claim_challenge_v1.json`**: 20개 고유 `(owner_topic_id, fact_id)` 각각에 대해 **작성자가 새로 구성한 정합 주장 1건과 의도적 반례 1건**, 총 40개 연구용 텍스트. 우선 예: `N_cw=Z−P` vs `N_cw=P−Z`, `F_residual/F_tolerable` vs 역수, `PFDavg≤1/RRF` vs `≥`, 4선식 리드검출 구분, RTD/열전대 참조점 누락, fail-close 무조건 안전이라는 오류 등.
- **엄격한 라벨 한계**: 위 40개 문장은 **`AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED`**이고 독립 전문가 표준정답 데이터가 아니다. 47 Golden에 포함된 원문 답안을 복사하지 않았다. 실험 출력에는 사례 ID·Relation ID·결과 카운트만 기록하며 40개 문장 본문이나 기존 47 Golden 답안 원문을 넣지 않는다.

## 새 진단·보호 구현

- `scripts/evaluate_s7_alias_negative_challenge.py`: 선택 실험의 `s7_alias_source_review.json`(179 projections/119 source Fact/전체 HOLD)을 엄격히 검증 후, **현행 실제** `analyze_claim_alignment`(기존 deterministic canonical parser + source-verified Fact projection)을 총 40개 초안에 대해 호출한다. 새로운 Ontology alias, synthetic matcher, 채점 override를 현업 코드에 주입하지 않는다.
- Fact ID/owner/source Fact와 실제 verified `relation`과 다르면 즉시 실패. 실제 source-review artifact가 현재 git HEAD와 다르면 실행 차단. 출력은 별도 runner 임시 경로에 새 파일을 권한 0600으로 만들며 repo·Topic·Registry·score DB를 수정하지 않는다.
- 결과에는 각 20개 Fact의 Positive/Negative `EXACT_RELATION`, `CONDITION_GAP`, `CONTRADICTION_CANDIDATE`, `UNRESOLVED`만 기록. **정상 인식 0일 때 오인정 0이어도 정확하다고 평가하지 않는** `NO_POSITIVE_COVERAGE_INCONCLUSIVE` 상태를 명시한다.
- 초안 라벨에 독립 전문가 교차판정이 없으므로 `measured_precision`, `measured_recall`, `measured_accuracy`는 항상 `null`; `accuracy_claim=NOT_ESTABLISHED`. 반례를 `EXACT_RELATION`으로 인식한 사례가 하나라도 생기면 `NEGATIVE_EXACT_REVIEW_REQUIRED`, exit 2. 하지만 선택 연구 step만 non-gating이며 FAIL은 로그에서 반드시 별도 관찰해야 한다.
- `tests/test_s7_alias_negative_challenge.py`: 정확도 과장 방지, 반례 exact 차단, 미승인 source 차단, source ID 변경 거부, fake matcher 테스트 및 실제 승인 Registry 관계에 20 ID가 존재하는지 검사. **테스트 삭제·skip·xfail 없음**.
- `.github/workflows/validation.yml`: 기존 **Replay 47 Golden cases and audit 179 missing aliases (research only)** = ON일 때 이전 두 Artifact와 함께 `s7-alias-negative-challenge`를 업로드(7일 보관). 해당 선택 workflow를 **다시 수동 실행해야** 현 HEAD의 실측 결과가 생긴다.

## 이번에 결론 내리면 안 되는 것

| 항목 | 현 단계 결론 |
|---|---|
| 20×2 실험 fixture 준비 | 코드·데이터 작성 (아직 실행 전) |
| 실험 결과에서 false-positive 0 | 아직 수집 전, 실제 0이어도 positive recall=0이면 불충분 |
| 동일한 Fact 20건 Alias 승인 | **0건 / HOLD=20** |
| 전체 119개 Fact 기술검증 | **미완료 (나머지 99건 미검토)** |
| `EXACT_RELATION` 증가 | **주장 금지**, 별도 실측 필요 |
| 결정론적 채점 성능 개선 | **검증되지 않음**, 본 변경은 채점 정책에 영향 없음 |

## 차후 증거 게이트

1. 현재 HEAD에서 GitHub Actions `validation`을 수동 실행, alias replay 옵션 ON. 전체 pytest 및 Release `VALIDATION=PASS`, 179/119 기존 기준선 재현, 119-Registry source join, 신규 40-draft adversarial probe의 status·두 카운트 확인.
2. 정합 주장에도 `EXACT_RELATION=0`이면 Alias coverage 자체가 없는 상태. 이를 false-positive 방어 성공으로 표현하지 말 것. 필요하면 후보별 독립 전문 라벨/ID 의미의 ontology 정합을 따로 설계.
3. 기술적 정합성·조건·부호·반례·출처 판정이 실제로 끝난 ID만 최소 lexical map 변경을 별도 승인 검토 대상으로 삼고, A–C/D–E·Fatal/WRONG·Ceiling·합격정책·`score_admission=DISABLED`는 고정.
4. PR #38 Draft, Issue #39 Open 유지. main 미병합·운영 미배포·서비스 재시작 금지.

