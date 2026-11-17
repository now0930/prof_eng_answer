# S7 B7 — AI 작성 신규 시험 후보 20건 개별 기술 검토 (2026-11-17)

## 0. 결과 요약 및 권한 경계

이 문서는 **단일 AI 모델의 출처 보조 예비 검토**이며, 독립 검토자 두 명의 정답 검증이나 채점기 성능 평가가 아니다. 이전 테스트 [Actions #44011954575](https://github.com/now0930/prof_eng_answer/actions/runs/44011954575) (HEAD `5b468d9b987e5372354a027f82d4daab6704dc6a`)는 **2001 passed / 2 skipped, VALIDATION=PASS**, 8개 연구 Artifact 유지 상태를 확인했다. **이 문서와 함께 추가한 새 HEAD는 아직 CI 미검증이다.**

원본 비교: 같은 source-review SHA `7409e045c6837b818cafc110b507679b896d06ab`의 Registry 5개 Fact(원본 필수 조건 8개)와 비공개 AI 후보 20개(5 Fact × 4개 의도 유형). 자료 검토 결과:

- **14개: `RETAIN_RESEARCH_ONLY`** — 연구용 후보로만 보존. 사실 승인이나 정답 라벨이 아니다.
- **6개: `REWRITE_REQUIRED`** — 기술적으로 참인 부분진술·출처 없는 인용·평가 유형 불일치 등이 있어 문장 또는 검사 유형 변경 필요.
- **0개: 독립 전문가 승인/채점 사용.** 원본 Fact Anchor/Registry/Topic Pack/Ontology/Golden/정규 Claim parser 변경 없음.
- 외부 독립 검토와 별도 홀드아웃 확보 전까지 `score_admission=DISABLED`, `candidate_decision=HOLD`, `expert_benchmark_ready=false`.

커밋된 `calibration/s7_ai_20_case_provisional_review_v1.json`은 **후보 ID / 잠정판정 / 원인코드만** 기록한다. 원문 초안·원본 문장·수정 문장·작성자 기대 라벨은 저장소에 보관하지 않는다.

## 1. 20건 전수 검토표

각 셀은 `01`(기술적 일치 후보), `02`(역관계 후보), `03`(조건 누락 후보), `04`(인용·모호성 후보)를 나타낸다. `03`이라는 기계적 구분은 실제 정답 라벨이 아니다.

| 소스 Fact | 01 | 02 | 03 | 04 |
|---|---|---|---|---|
| `effective_unbalanced_area` | 보존: 실제 압력/구조별 유효면적 | 보존: 공칭 시트면적의 전칭 동일 주장 반박 | **재작성**: 범위가 지나치게 넓은 부분 정의 | **재작성**: 근거가 확인되지 않은 설명서 인용 |
| `sw06_baseline_approved_reference` | 보존: 시점·식별·공식 승인·변경참조 | 보존: 최신 파일=승인 기준선 오류 | **재작성**: 기록 일반론만으로 승인 기준선이라고 볼 수 없음 | 보존: 승인 여부 없는 인용 주장의 불확정성 |
| `deadband_definition_direction_reversal` | 보존: 방향 반전·출력 무변화·조립체/시험조건 | 보존: 입력 폭과 시간 지연의 물리량 혼동 | **재작성**: 조건 특정 없는 부분적으로 참인 정의 | 보존: 서로 다른 시험 조건의 수치는 비교 가능성이 미확정 |
| `sw04_v_model_definition` | 보존: 개발 단계와 대응 V&V 시험 단계 | 보존: 임의 개발–시험 단계 결합의 오류 | **재작성**: 소스 조건 ID 0개, '조건 누락' 유형 자체가 부적절 | 보존: 대응자료 없이 '추적성 확보'를 인용만 한 사례 |
| `nyquist_contour_and_mapping` | 보존: s-평면 RHP 폐경로의 L(s) 사상 | 보존: 정의역과 영상 평면 혼동 | **재작성**: L(jω) 자체는 참인 부분 설명; 완전 경로 설명 부재 | 보존: 용어가 원래 경로인지 영상 곡선인지 불명확 |

**6개 재작성 대상 정확한 ID**: `effective_unbalanced_area_ai_03`, `effective_unbalanced_area_ai_04`, `sw06_baseline_approved_reference_ai_03`, `deadband_definition_direction_reversal_ai_03`, `sw04_v_model_definition_ai_03`, `nyquist_contour_and_mapping_ai_03`.

### 명확한 규칙

**부분적으로 참인 단문은 잘못된 Fact와 동일하지 않다.** 요건을 말하지 않았다는 사실로 '거짓 관계' 판정을 하면 정밀도가 낮아진다. 구분할 상태는 `EQUIVALENT`, `PARTIAL_BUT_TRUE`, `CONTRADICTORY`, `QUOTED_OR_UNDETERMINED`가 적합하다. 단, 이 네 가지도 **연구용 후보 분류**이며 새로운 canonical 라벨·채점 규정으로 승인하지 않는다.

- Deadband은 **입력 방향 반전 직후 출력 변화가 없는 입력 구간**이 본질이며 시간 지연과 별개다. 조립체·시험 환경에 따라 관측값이 변한다.
- 형상 기준선은 **식별된 시점/형상정보에 대한 공식 승인·합의**가 중요하다. 최신 파일 하나만으로 승인된 기준선이라고 단정할 수 없다.
- V-Model의 원본 Registry는 **설계/개발과 대응 시험의 매핑**만 구조화했으며 **필수조건 ID=0개**다. 트레이스 기록 작성 여부는 별도 근거·범위가 있어야 한다.
- Nyquist의 `L(jω)` 설명 자체는 옳다. 그러나 안정도 기준을 사용하는 **s-평면 전체 우반평면 경로와 L(s) 사상**을 생략한 문장만으로 완전한 경로 관계가 증명되는 것은 아니다.
- 공칭 시트 면적과 **실효 불평형 면적이 같은 경우가 있을 수 있지만**, 항상 동일하다는 주장은 구조·스템 압력 면적을 무시한다.

## 2. 외부 대조 근거

이전 Registry Source Review의 출처 메타데이터를 확인하고, 다음 공식·교육 자료에서 일반 원리를 추가 교차 확인했다. 이 대조는 위 20문장에 대한 **독립적인 전문가별 개별 원문 서명 검증은 아니다**.

1. **Emerson Control Valve Handbook**, Chapter 5.11.1.1, unbalance force/net pressure differential/net unbalance area. https://stage.www.emerson.com/content/dam/emerson/en/final-control-fctl/isolation-valves/documents/control-valve-handbook-en-3661206.pdf
2. **NASA Configuration Management 6.5**, formally agreed/approved baseline for configuration items at a point in time. https://www.nasa.gov/reference/6-5-configuration-management/
3. **Emerson Control Valve Handbook**, deadband input reversal and observable output response (control-valve definition). https://www.acdamerica.net/documents/control_valve_handbook.pdf
4. **CMU Software Engineering Institute**, Using V Models for Testing (2013), corresponding development/testing phases. https://www.sei.cmu.edu/blog/using-v-models-for-testing/
5. **University of Washington lecture**, Nyquist criterion, complete RHP contour and complex mapping. https://faculty.washington.edu/chx/teaching/fbintro/lec24-nyquist-criterion/

## 3. 변경 파일 및 다음 게이트

- `calibration/s7_ai_20_case_provisional_review_v1.json` — ID 전용 20건 단일 AI 예비판정; 정답 라벨/답안 원문 없음.
- `tests/test_s7_ai_20_case_provisional_review.py` — 5×4 범위, 보존 14·재작성 6, V-Model 0 조건, 실제로 참인 부분진술을 거짓으로 취급하지 않는 검사, Score 비활성 및 비공개 텍스트 유출 방지.

**CI 재검증:** [validation.yml](https://github.com/now0930/prof_eng_answer/actions/workflows/validation.yml), branch `feat/claim-alignment-verification-20261114`, `run_s7_experiment=OFF`, `run_s7_alias_diagnostics=ON`. 새 HEAD에서 pytest, VALIDATION, 8개 연구 Artifact를 실제 확인할 때까지 PASS를 전용하지 않는다.

**다음 연구:** 수정이 필요한 6개 문장을 비공개 공간에서 재작성하고, 수정 전/후 사례가 같은 기술적 의미/역관계/누락을 유지하는지 외부 검토로 확인한다. 그 이후 별도 연구용 parser shadow에서 ANSWER로부터 직접 도출한 subject/predicate/object/조건 판정과 전문가 라벨을 비교한다. 원본 119 HOLD, B7/D2/D3 OPEN, PR #38 Draft 및 Grade 사용 DISABLED 유지.
