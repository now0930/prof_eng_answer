# S7 B7 — AI 후보 6개 문장 수정 및 수정 전후 비교 (2026-11-17)

## 현재 완료 범위

이전 검증 실행은 [Actions #44016852050](https://github.com/now0930/prof_eng_answer/actions/runs/44016852050), HEAD `fc0014f77f42e25bd4aa2d6bff7c5f833d5c057a`, **2006 passed / 2 skipped / VALIDATION=PASS**였다. 이번 단계는 `REWRITE_REQUIRED` 6개 문장을 실제 수정한 뒤, 원본 20개 초안과 분리 보관하고 같은 Legacy Fact·원본 Source 관계에 연결했다. **현재 새 코드의 CI 검증 결과는 아직 없다.**

**완료:** 비공개 원문/수정안 6쌍 작성 및 별도 지역 데이터 preflight(원본 candidate ID 6/6 일치, 과거 후보 20문장과 새 문장 중복 0, 수정안 내부 중복 0, Source SHA 일치, V-Model 조건 0개 유지) 실행 성공.

**미완료:** 실제 두 전문가의 독립 기술적 판정, 각 문장에서 관계/조건의 자동 추출, 외부 테스트 집합, 정량 정확도 또는 기존 채점기로의 사용. 보존 14건은 그대로 연구용 미검증 후보이며 수정안 6건도 **정답 승격되지 않았다**.

비공개 파일(사용자 개인 작업 공간; GitHub에 올리지 않음):

- `s7_private_six_revised_candidates_20261117.json`: 6개 실제 수정 전후 문장, 출처/관계 ID, 수정 의도, 단일 AI 평가 기록
- `s7_six_rewrite_before_after_private_review_20261117.md`: 한국어 6개 개별 비교와 원본 소스 관계
- 이 두 파일은 개인 원본 텍스트를 포함하며 GitHub Issue/PR/Actions에 첨부하지 않는다.

GitHub에는 아래만 포함:

- `calibration/s7_six_ai_candidate_revision_manifest_v1.json` — 후보 ID / 새 연구용 역할 코드 / 소스 조건 개수 / 변경 이유 / 미검증 상태만 기재한 metadata
- `tests/test_s7_six_ai_candidate_revision_manifest.py` — 기존 20개 잠정 판정에 속한 정확히 6건과 연결, 조건 수 보전, 2개 부분참 진술 및 V-Model의 zero-conditions 관리, automatic scoring/CI 유출 방어

## 6개 후보별 수정 의도

| 후보 ID 끝 | 기존 오류 | 수정 후 연구용 시험 역할 | 독립 판정 |
|---|---|---|---|
| `effective_unbalanced_area_ai_03` | 실제 플러그·스템 압력 작용면 부족 | `CONDITION_SCOPE_UNSPECIFIED` — 압력차와 축방향 힘의 설명은 남기고 기하 구조 조건은 비명시 | 미검증 |
| `effective_unbalanced_area_ai_04` | 존재가 확인되지 않은 설명서를 실제 인용 | `HYPOTHETICAL_QUOTE_UNVERIFIED` — 가상 문서·구조조건 미제시라고 명시 | 미검증 |
| `sw06_baseline_approved_reference_ai_03` | 형상정보 식별 및 공식 승인·합의/시점 누락 | `CONDITION_SCOPE_UNSPECIFIED` — 설계 기록의 일부 기능만 말한 진술 | 미검증 |
| `deadband_definition_direction_reversal_ai_03` | 정성 정의를 특정 정량 시험조건 누락만으로 거짓 취급할 위험 | `PARTIAL_TRUE_TEST_SCOPE_UNSPECIFIED` — 입력 반전·무출력 구간은 정성적으로 정의하되 수치 일반화 없음 | 미검증 |
| `sw04_v_model_definition_ai_03` | source condition ID 0개인데 누락된 조건이라고 오분류 | `RELATION_MAPPING_UNSPECIFIED` — 개발/시험 단계의 존재만 말하고 대응 관계는 미설명 | 미검증 |
| `nyquist_contour_and_mapping_ai_03` | `L(jω)` 부분 진술을 오류로 처리할 위험 | `PARTIAL_TRUE_FULL_CONTOUR_UNSPECIFIED` — 주파수 응답 부분은 말하지만 전체 우반평면 폐경로의 `L(s)` 사상 설명은 없음 | 미검증 |

6개 모두 **점수 불반영**. 특히 `PARTIAL_TRUE`는 `CONTRADICTORY`가 아니다. '일부 조건을 언급하지 않음'은 곧바로 '기술적 거짓'을 의미하지 않는다. 이후 답안 평가에서는 `관계 충족`, `관계 부분 증거`, `실제 모순`, `판정 보류`를 먼저 분리해야 한다. 이 문장은 **연구 방향**이지 canonical 라벨·채점 규칙의 개정이 아니다.

## 소스와 외부 교차 대조

Source Review의 기존 Registry 관계(원본 source SHA `7409e045c6837b818cafc110b507679b896d06ab`)에 다음 공개 근거를 교차 대조했다.

- Emerson, *Control Valve Handbook*: 데드밴드는 **입력 방향 반전 후 출력 반응이 보이지 않는 입력 구간**이며 정량 시험의 입력·출력 변수와 부하 조건을 특정해야 한다. https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf
- NASA Configuration Management 6.5: 형상 기준선은 특정 시점의 식별된 형상항목 속성에 대한 합의된 설명과 변경의 기준이다. https://www.nasa.gov/reference/6-5-configuration-management/
- CMU SEI, *Using V Models for Testing*: V-Model은 개발 산출물과 검증/확인 활동의 **대응**을 강조한다. https://www.sei.cmu.edu/blog/using-v-models-for-testing/
- University of Washington, Nyquist criterion lecture: 전체 우반평면 경로 및 각 부분의 `L(s)` 사상을 주파수 응답 구간과 구별한다. https://faculty.washington.edu/chx/teaching/fbintro/lec24-nyquist-criterion/

위 근거 확인은 독립 전문가 2인의 case-by-case 정답 인증과 다르다. 원본 Registry의 원문 진술·조건을 임의 추가/교체하지 않았다.

## 다음 단계와 CI 게이트

1. 현재 브랜치의 새 HEAD에서 `validation.yml` 실행 — `run_s7_experiment=OFF`, `run_s7_alias_diagnostics=ON`. 새 단위시험 및 기존 S7 8개 Artifact를 확인한다.
2. 수정 전/후 6쌍과 새 AI 작성 20개 후보 전체를 별도 독립 연구 검토에 제공한다. 이때 작성자 예상 역할을 검토자에게 숨긴다.
3. 원본 Registry에서의 주체·관계·객체·조건을 **실제 답안에서 추출하는 shadow evaluator**의 별도 연구 패스가 필요하다. 원본 Source ID를 답안 인식 결과로 복사해 넣는 것은 성능 평가가 아니다.
4. 혼합된 문장·부정·인용·누락·동의어를 포함한 외부 검증 샘플에서 오검출을 확인한다. 자동 정답이나 파서 정확도 측정은 전문가 라벨 확보 후에만 수행한다.

**고정:** Original Fact Anchor/Registry/Ontology/Topic Pack/Golden/Deterministic A~C Scoring 변경 없음. 119 HOLD, `score_admission=DISABLED`, B7/D2/D3 OPEN, PR #38 Draft, 미검증 후보 20개 독립 홀드아웃/채점 사용 금지, 자동 Alias 승격/병합/배포 금지.
