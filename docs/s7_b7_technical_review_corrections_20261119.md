# S7 B7 — 기술 원문 대조 정정안 (연구용 / 승인·채점 불가)

- 확인 대상: PR #38 `feat/claim-alignment-verification-20261114`의 공개 `calibration/s7_b7_expert_review_packet_v1.json`.
- 문서 생성 이유: 37개 고유 synthetic 답안의 **기술적 오류 및 이전 AI 검토의 과잉판정**을 바로잡고, 표준의 정확한 조항과 **수정된 참인 기술 표현**을 명시한다.
- 상태: `PRE_REVIEW_TECHNICAL_PROPOSAL`. **독립 전문가/서브에이전트 결과가 아니며, 사람이 서명한 Gold Label이 아니다.** 이 문서 하나로 `REVIEWED`/정답 승인/Fact 승격/채점권한 변경 불가.
- 원본 40개 probe는 **반례 품질 테스트가 목적**이다. 오답을 참으로 바꿔 원본 데이터셋을 훼손하지 않는다. 오답 probe의 교정된 **정답 근거 문구**는 아래에 별도 표기한다. 원본 packet SHA-256이 검증기에 고정돼 있으므로 원본 JSON/비공개 blind packet/Registry를 임의 수정하지 않는다.
- 평가단위: 원본 **case의 문맥·Claim 관계**, 전체 답안 verdict, 인용·부정·정정 여부는 별도. 핵심 관계의 일부가 맞아도 전체 완전 정답으로 자동 승격 금지.
- 정확한 고유집합: 원본 40행에서 동일 Topic·Fact·답안의 exact duplicate인 `effective_unbalanced_area__04`, `sw04_v_model_definition__04`, `nyquist_contour_and_mapping__04`를 제외한 **37개**. 본 표에서 **작성자 case_kind는 판정 근거가 아니다**.

## 우선 확정한 기술 명제 — 채점에 바로 넣지 않는 교정 기준

1. **Deadband**: 입력 방향을 반전한 뒤 **관측 출력에 변화가 나타나지 않는 입력 변수의 유한 범위**다. 따라서 dead time(입력 변화~응답 시작까지의 **시간 간격**)과 다르다. Stiction은 정지마찰로 인한 sticking/slip-jump 등과 관련되며 deadband와 동일한 정의가 아니다.
2. **Configuration baseline**: 제품·서비스의 **특정 시점의 특성**을 정하는 **승인된 configuration information**으로 수명주기 활동의 기준이 된다. '최신'이나 '단순 합의'만으로 승인되었다고 단정할 수 없다. 정정 출처 위치는 **ISO 9000:2015 §3.10.7** (오기는 **§3.10.12**); ISO 10007:2017 §3.2도 구분.
3. **Effective (net) unbalance area**: 정해진 밸브 구조/압력조건에서 순 유체 압력 불평형력을 계산하는 **등가 유효 면적**으로 `F_unbalance = ΔP_net × A_unbalance,net` 형태에 사용한다. **Single-seated flow-up**에서는 port area일 수 있고, 다른 배치에서는 stem area·balanced trim의 잔여 unbalance 등을 고려한다. '항상 같음'과 '완전히 무관' 양쪽 절대 주장은 불가.
4. **V-Model**: 개발 활동과 대응 시험·검증·확인 활동 사이의 관계를 나타내는 **모형**이다. 단계를 하나의 시험으로 대체하지 않으며 검증활동의 실제 순차성/겹침은 프로젝트 맥락에 따른다.
5. **Nyquist**: **s-평면**에서 RHP를 둘러싸는 경로 `Γ`를 선택하고, 각 `s ∈ Γ`를 `L(s)`로 사상해 **이미지 경로** `L(Γ)`를 얻는다. 허수축 부분의 이미지가 `L(jω)` 주파수응답이다(무한원호/허수축 극점 detour는 시스템 조건에 따라 처리). 입력 `Γ`와 출력 `L(Γ)`는 다른 객체다.

## 독립 출처 및 근거

- IEC 60534-9:2007 §3.2/§3.3, dead band / dead time: https://webstore.iec.ch/en/publication/2477 ; 이용 가능한 표준 본문 preview https://preview.sist.si/sist-preview/20602/14d2628760e445a8b2cd305482d2620f/SIST-EN-60534-9-2008.pdf
- ISO/TC 176, `Terms in TC 176 Standards Alphabetical Listing` (2022-09-29), PDF p.8: https://committee.iso.org/files/live/sites/tc176sc1/files/Terms%20in%20TC%20176%20Standards%20Alphabetical%20Listing%20V1%202022%2009%2029.pdf ; ISO 9000:2015 §3.10.7 / ISO 10007:2017 §3.2.
- NIST SP 800-171 Rev.3 §03.04.01, documented / formally reviewed / agreed-upon baseline: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html
- Emerson Fisher `Control Valve Handbook` 6th ed. §5.11.1.1 / Figure 5.2: https://www.emerson.kr/is/content/emerson/ko/final-control/flow-controls/valves/documents/control-valve-handbook-en-3661206.pdf
- CMU SEI, `Using V Models for Testing`, Traditional V Model: https://www.sei.cmu.edu/blog/using-v-models-for-testing/
- ETH Zürich, `Control Systems I Lecture 9: The Nyquist Condition`, Nyquist contour and image: https://ethz.ch/content/dam/ethz/special-interest/mavt/dynamic-systems-n-control/idsc-dam/Lectures/Control-Systems-1/Lectures/L1809_Nyquistplot.pdf
- UIUC ECE 486, Lecture 18 (Nyquist mapping): https://courses.physics.illinois.edu/ece486/fa2026/documentation/handbook/lec18.html

## 37개 사례의 정정된 사전 검토 판정

다음 표는 **기술적 진술의 검토 의견**이다. `CORE_RELATION_CORRECT`는 해당 관계 진술이 지지된다는 뜻이지 **전체 Fact 충족·정답·점수 허용**을 뜻하지 않는다. `FALSE*`와 `MIXED*`는 의도적 오답 반례를 원본에서 삭제하거나 참으로 바꾸라는 의미가 아니다.

### A. Deadband

출처: IEC 60534-9:2007 §3.2–3.3; IEC 60534-4 (dead-band test)

| 원본 Case ID | 사전 판정 | 기술 수정·해석 근거 |
|---|---|---|
| `deadband_definition_direction_reversal__01` | `CORE_RELATION_CORRECT` | 방향 반전 후 **입력 변수가 일정 범위 변하는 동안** 관측 출력이 변하지 않는다는 설명으로 핵심 정의 충족; 관측 변수를 명시하면 더 좋음 |
| `deadband_definition_direction_reversal__02` | `AMBIGUOUS` | '반전하는 순간 출력이 따라오지 않는 범위'는 지연 시간으로 오인 가능 → '입력 방향을 반전한 뒤 출력 변화가 관측되기 전까지의 **입력신호 변화 범위**' |
| `deadband_definition_direction_reversal__03` | `FALSE_COUNTEREXAMPLE` | 반전과 무관·출력 반드시 변함은 정의에 반함. 부정 시험용으로 **원문 보존** |
| `deadband_definition_direction_reversal__04` | `CORE_RELATION_CORRECT` | Topic이 제어밸브로 고정된 경우 정의와 일치. 원래 __01과 답안 문자열은 다르므로 별도 유지 |
| `deadband_definition_direction_reversal__05` | `CORE_RELATION_PLUS_EXTRA` | 기본 정의는 옳음; '시험조건에 따라 달라짐'은 input/output 선택·부하·시행 조건을 특정한 별도 명제 |
| `deadband_definition_direction_reversal__06` | `QUOTATION_NOT_ASSERTED` | 정의의 인용 여부만 말함. 인용된 문장을 본인 주장의 Fact로 자동 승인 금지 |
| `deadband_definition_direction_reversal__07` | `MIXED_CONTRADICTORY` | 첫 문장은 정의와 일치, 두 번째는 방향 반전과 무관하다고 하여 충돌. 전체 정답 처리 금지 |
| `deadband_definition_direction_reversal__08` | `FALSE_OVERGENERALIZATION` | deadband/stiction은 관련될 수 있어도 동의어 아님. stiction은 정지마찰·stick-slip 거동, deadband는 비응답 입력 구간 |

### B. Configuration baseline

출처: ISO 9000:2015 §3.10.7; ISO 10007:2017 §3.2; NIST SP 800-171 Rev.3 §03.04.01

| 원본 Case ID | 사전 판정 | 기술 수정·해석 근거 |
|---|---|---|
| `sw06_baseline_approved_reference__01` | `PARTIAL_TRUE` | 승인 및 변경의 참조기준 역할은 맞지만 특정 시점의 구성 정보 및 수명주기 기준이라는 정의 요소는 생략 |
| `sw06_baseline_approved_reference__02` | `PARTIAL_SCOPE` | '합의된'은 NIST baseline 문맥에서 검토·합의와 관련되나 ISO의 **approved**와 자동 동치 아님. 문서화/검토/승인 상태 확인 필요 |
| `sw06_baseline_approved_reference__03` | `FALSE_COUNTEREXAMPLE` | 기준선이 변경관리 기준이 아니고 최신 파일이라는 설명은 오답. 부정 시험용 원문 유지 |
| `sw06_baseline_approved_reference__04` | `PARTIAL_TRUE` | 변경관리 기준 역할은 참. 승인과 특정 시점 구성 정보가 생략 |
| `sw06_baseline_approved_reference__05` | `PARTIAL_TRUE` | 변경관리 준거는 참; '승인 기록 별도 확인'은 합리적인 provenance 확인 지침이나 정의를 완성하지는 않음 |
| `sw06_baseline_approved_reference__06` | `QUOTED_UNVERIFIED` | 정의 인용과 실제 승인 기록 미확인을 구별. 특정 기준선의 승인을 실증한 답안 아님 |
| `sw06_baseline_approved_reference__07` | `TRUE_CORE_UNSUPPORTED_UNIVERSAL` | '형상 기준선은 변경관리의 기준'은 참. '최신 파일은 승인 기준선이 아니다'는 **보편적 부정**으로 근거 없음. **직접 자기모순이라고 단정한 이전 검토를 정정**: 최신 파일도 정식 승인됐다면 기준선일 수 있음 |
| `sw06_baseline_approved_reference__08` | `FALSE_COUNTEREXAMPLE` | 최신 파일이라는 이유만으로 자동 승인되지 않음. 승인 절차·기록이 필요 |

### C. Effective unbalance area

출처: Emerson Fisher Control Valve Handbook 6th ed. §5.11.1.1 (Unbalance Force)

| 원본 Case ID | 사전 판정 | 기술 수정·해석 근거 |
|---|---|---|
| `effective_unbalanced_area__01` | `PARTIAL_TRUE` | 압력 작용면·구조 의존성은 참이나 **net axial pressure force 계산에 쓰이는 equivalent area**라는 정의 누락 |
| `effective_unbalanced_area__02` | `AMBIGUOUS` | 면적이 '불평형력에 작용'한다는 표현은 힘/압력 관계를 뒤바꾸기 쉬움 → '유체 차압이 밸브 플러그에 만드는 순불평형력을 산출하는 등가 유효 면적' |
| `effective_unbalanced_area__03` | `FALSE_ABSOLUTE` | 공칭 시트/포트 면적과 항상 무관하다는 주장은 단일 시트 flow-up 구조의 port-area 사례로 반박됨 |
| `effective_unbalanced_area__05` | `PARTIAL_TRUE` | 구조에 따라 달라지고 시트 면적과 항상 같지는 않다는 것은 참. 힘-차압-등가면적의 정량 관계를 보완 |
| `effective_unbalanced_area__06` | `QUOTED_NOT_ASSERTED` | '항상 같다'는 인용을 미확인이라고 한 것; 이 문장 자체로 단순 오답 주장이나 정의 제시로 처리 금지 |
| `effective_unbalanced_area__07` | `TRUE_CORE_PLUS_FALSE_EXTRA` | 구조 의존성은 참, 시트 면적과 **항상 같다**는 절대 주장은 거짓. 전체 정답 불가 |
| `effective_unbalanced_area__08` | `FALSE_COUNTEREXAMPLE` | 구조와 무관하다는 설명은 stem/port/balanced trim에 따른 실효 면적 차이를 부정 |

### D. V-Model

출처: CMU SEI Using V Models for Testing (2013), Traditional V Model

| 원본 Case ID | 사전 판정 | 기술 수정·해석 근거 |
|---|---|---|
| `sw04_v_model_definition__01` | `CORE_RELATION_CORRECT` | 개발 단계와 대응 시험 단계의 매핑을 표현함. 원본 Topic Anchor의 초기 시험 준비까지 모두 표현했다는 뜻은 아님 |
| `sw04_v_model_definition__02` | `CORE_RELATION_CORRECT` | 개발과 시험·검증 단계 간 추적성은 관련 핵심 관계를 올바르게 설명 |
| `sw04_v_model_definition__03` | `FALSE_GENERALIZATION` | '시험 단계가 개발 단계를 정의한다'는 일반 V-Model 정의가 아님. 일부 TDD 사례와 혼동 금지 |
| `sw04_v_model_definition__05` | `CORE_RELATION_PLUS_EXTRA` | 개발·시험 대응성은 참; 프로젝트별 세부 시험 내용 차이도 가능. 추가 문장의 적용 범위를 별도 판독 |
| `sw04_v_model_definition__06` | `QUOTATION_NOT_ASSERTED` | 인용했다고 보고하고 산출물 내용은 제시하지 않음; 인용 텍스트를 본인의 독립 명제로 인정하지 않음 |
| `sw04_v_model_definition__07` | `MIXED_CONTRADICTORY` | 대응 관계는 참이나 '설계 단계는 시험과 무관'이라는 절이 V-Model의 대응 검증 취지와 모순 |
| `sw04_v_model_definition__08` | `FALSE_COUNTEREXAMPLE` | 모든 개발 단계를 동일한 단일 시험으로 대체한다는 설명은 V-Model 취지와 반대 |

### E. Nyquist contour & mapping

출처: ETH Zürich Control Systems I Lecture 9, pp.17–20; UIUC ECE 486 Lecture 18

| 원본 Case ID | 사전 판정 | 기술 수정·해석 근거 |
|---|---|---|
| `nyquist_contour_and_mapping__01` | `CORE_RELATION_CORRECT` | s-평면의 열린 우반평면을 감싸는 contour를 복소함수 L(s)에 사상한다는 관계가 올바름 |
| `nyquist_contour_and_mapping__02` | `INCORRECT_OR_AMBIGUOUS_DOMAIN` | 'Nyquist 궤적을 L(s)에 대입'은 입력 s-경로와 이미지 L(s) 궤적을 혼동. → '**s-평면 Nyquist 경로의 각 s를 L(s)에 대입하여** 복소평면 사상 궤적을 얻는다' |
| `nyquist_contour_and_mapping__03` | `FALSE_COUNTEREXAMPLE` | 일반 RHP Nyquist contour가 LHP만 둘러싼다는 설명은 잘못 |
| `nyquist_contour_and_mapping__05` | `CONDITIONAL_PARTIAL` | s-평면 contour의 허수축 구간과 L(jω) 주파수 응답의 **상(image)** 관계를 구별. '주파수응답이 contour 일부 구간'은 다른 평면을 섞어 설명하여 보완 필요 |
| `nyquist_contour_and_mapping__06` | `QUOTED_NOT_ASSERTED` | 우반평면 경로 문구를 인용하되 적용 조건 검토를 요구. 인용 자체를 주장 Fact로 자동 채점 금지 |
| `nyquist_contour_and_mapping__07` | `MIXED_CONTRADICTORY` | 같은 s-평면 경로가 RHP를 둘러싼다/그렇지 않다는 직접 모순 |
| `nyquist_contour_and_mapping__08` | `WRONG_EQUIVALENCE_CONTEXT_UNCLEAR` | 주파수응답 L(jω)와 s-평면 전체 contour는 동일 대상이 아님. 다만 '~단정한다'는 **귀속/인용 표현**일 가능성 있으므로 assertion-context는 별도로 판정. 앞선 단정적 '작성자 기술오류' 분류를 조건부로 정정 |

## 사전 검토 정정 및 승인 경계

- **이전 검토에서의 명시적 정정 #1**: `sw06_baseline_approved_reference__07`은 두 절의 *직접 자기모순*이 아니다. 두 번째 절이 승인된 최신 파일의 가능성을 배제하는 **무근거 보편 부정**이다. 혼합 답안으로는 부적합하되 '문장 A와 B가 논리적으로 부정 관계'라는 증거는 없다.
- **이전 검토에서의 명시적 정정 #2**: `nyquist_contour_and_mapping__08`은 기술 내용의 등가 주장은 부정확하지만, '~라고 단정한다'는 문장 화행은 인용/귀속인지 작성자 주장인지 불명확하다. 독립 review에선 assertion context를 따로 기록해야 한다.
- **이전 검토에서의 명시적 정정 #3**: `sw06_baseline_approved_reference__02`의 '합의된'은 NIST 문맥에서 baseline 형성 요소로 타당할 수 있으므로 무조건 거짓으로 간주하지 않는다. ISO의 **승인(approved)** 충족 여부는 별도.
- **이전 검토에서의 명시적 정정 #4**: `effective_unbalanced_area__03`은 **seat/port 면적과 원천적으로 무관**이라는 절대 부정이 문제이지, 모든 설계에서 seat 면적과 반드시 일치해야 한다는 뜻이 아니다.

## 추후 다중 검토 및 안전한 반영 계약

현재 이 환경에서는 **실제 독립 서브에이전트를 호출하지 않았으므로** 독립 다중판정 완료를 주장할 수 없다. Codex에서 세 역할을 서로의 중간 결론 없이 **서로 다른 세 context**로 실행해야 한다.
- `ENGINEERING_REVIEW`: 각 진술의 물리적 참거짓·조건·예외·원문 locator를 검증하고 별도 이견 문서 제출
- `LINGUISTIC_REVIEW`: 인용/부정/수정/귀속과 입력-출력 변수·전체 verdict/Claim verdict 관계 심사
- `ADVERSARIAL_REVIEW`: 반례를 만들어 과잉인정/과잉배제 위험 및 source mismatch 확인
- **통합**: 세 역할의 disagreement 표를 먼저 만들고 결론 충돌은 `HOLD`. Codex 자신·LLM 간 합의는 **human independent reviewer provenance를 대체하지 않는다**.

### 편집 금지·해제 조건

`calibration/s7_b7_expert_review_packet_v1.json`, source Registry, Topic Pack, Generated, 운영 grading 코드, private reviewer packet/result를 이 문서의 제안만으로 변경 금지. 원본 synthetic 오답은 *negative probe*로 남긴다. 공식 source locator를 Registry에서 수정할 경우 별도 provenance·approval·고정 SHA/비공개 packet 호환성 검토가 먼저 필요하다. D2/D3 기존 증거도 새 HEAD에 그대로 적용한 것으로 주장하지 않는다.

**현재 상태**: `accuracy_status=NOT_ESTABLISHED`, `source_match_proven=false`, `reviewed=0/37`, `pending=37/37`, `score_admission=DISABLED`, `score_effect=none`, B7 OPEN, 119 HOLD, PR #38 Draft·미병합.
