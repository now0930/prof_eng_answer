# P2-A — Canonical Claim 계약 구조 확정 (2026-11-25)

기준 main `45c7d146e4673e885005c04535e65dc9b9d7c8a5`, tree `d06a43d7b36323b587e52086c495f12dcc8e9442`; P1-C checkpoint `92bb21bca46e1409fd48abd0d7d767e92fb6e62f`. Owner #40. **문서 전용 계약 확정; 기존 schema/ontology/runtime 변경 없음. 신규 진단 경로 score_admission=DISABLED, score_effect=none.** 이 표기는 정책이며 기존 JSON schema에 새 필드를 추가하는 명령이 아니다. P1-C 8개 후보는 승인 대기/미적용; 승인 Fact로 참조하지 않는다.

## 1. 실제 코드/스키마 근거

아래 파일은 해당 main SHA에서 직접 읽었다. 링크는 정본 위치이며 줄 번호는 그 SHA 기준이다.

| Source | 근거 범위 및 역할 |
|---|---|
| [canonical evidence schema](../schemas/canonical_grading_evidence_v1.schema.json) | 기존 Canonical Grading Evidence 1.0, evidence_only, score_effect none, strict fields |
| [canonical_grading_evidence.py](../grading/evidence/canonical_grading_evidence.py) | L19–78,88–104,141–252,256–288: authority key 금지, 원문 span, 정규화, 해시, claim identity |
| [canonical_claim_extractor.py](../grading/evidence/canonical_claim_extractor.py) | L47–124,131–157,258–326,378–449,510–618: 계약 중심 추출, 수량·수식, 조건/극성/문맥, unresolved |
| [topic_machine_contract.py](../grading/evidence/topic_machine_contract.py) | L46–234: strict owner, facts/rules, local references, invariant bindings |
| [fact-grounded schema](../schemas/fact_grounded_contract_v1.schema.json) / [validator](../grading/evidence/fact_grounded_contracts.py) | L87–195,199–261: Registry Fact relation, source/verification refs, question requirement/candidate/snapshot 별도 계약 |
| [approved_fact_registry.py](../grading/evidence/approved_fact_registry.py) | L15–53: 위임 승인 출처, 승인+verified, 고유 Fact ID, Master owner 검증; source_refs 현재성 별도 |
| [deterministic_requirement_evaluator.py](../grading/scoring/deterministic_requirement_evaluator.py) | L31–79,83–161,172–289: 기존 Machine Contract 관계 비교, 제외/범위, claim allocation, invariant 우선 |
| [fact_anchor_evidence_adapter.py](../grading/evidence/fact_anchor_evidence_adapter.py) | L158–234,638–754: 문항 범위 선택, lexical recall floor, owner+requirement 연결 |
| [cross_topic_question_contract.py](../grading/evidence/cross_topic_question_contract.py) | 기존 cross-topic selector/evidence; 신규 질문 범위 소유권 없음 |
| [quantity_dimension_evaluator.py](../grading/evidence/quantity_dimension_evaluator.py) | L64–90,174–260,264–350: 제한된 수량/차원 추출 및 검증 |
| [deterministic_primary_grader.py](../grading/scoring/deterministic_primary_grader.py) | L209–249: 실제 운영 경로; 기존 extractor/quantity/invariant/scope/evaluator/adapter/symbolic 연결 |
| [fact_anchor_scoring_exclusions.py](../grading/evidence/fact_anchor_scoring_exclusions.py) | L14–17,26–82,140–176: 네 계층 제외; 후보 HOLD statement hash 검사; 사실 거짓 판정과 다름 |
| [audit_relation_recognition.py](../scripts/audit_relation_recognition.py) | L22–111: 비채점 별도 진단, strict span/owner/조건/인용/상충 제한 |

## 2. 계약 경계와 identity

| 계층 | 기존 필드와 namespace | 확정 규칙 |
|---|---|---|
| Canonical Fact Anchor | topic_id + anchor_id (legacy 일부 id/anchor_id alias, 대문자 허용 가능), statement, importance, accepted/rejected, source_basis | 소유 Topic의 정본. 동일 ID 문자열이라도 다른 Topic이면 다른 항목. ID 대소문자 보존. |
| Registry Fact | 전역 fact_id, topic_id, optional legacy_anchor_id, revision, statement, relation.subject/predicate/object/conditions, source_refs, verification_refs, review/verification_status, score_effect=none | 명시적 topic_id+legacy_anchor_id로만 정본 연결. Registry relation에는 polarity가 **없다**; positive 기본값 부여나 부정 추론 금지. 승인/검증은 기술적 사실의 근거이지 채점 admission 아님. |
| Machine Contract | topic_machine_contract_v1; owner_topic_id, authority=deterministic_topic_contract, score_effect=downstream_deterministic_only; facts[*].fact_id/S/P/O/polarity/optional conditions | fact_id는 contract 내부 namespace. rule.required_fact_ids를 통해 연결. Registry fact_id와 자동 등치 금지. |
| Machine requirement | requirement_id, required_fact_ids, minimum_match_count, optional score_group_id/mention partial/contradiction policy/violation_only; invariant_bindings | owner + requirement_id. Anchor와 정확히 일치하는 경우만 direct Anchor join; 다른 ID는 명시 매핑 없이는 신규 scope/credit 금지. violation_only는 기존 invariant 전용. |
| Question scope | expected_question_patterns.required_anchor_ids, pass_required_anchor_ids, cross-topic contract; 별도 fact-grounded question contract의 fact_refs | 기존 선택 결과 및 owner 유지. 두 question contract 종류를 혼동하지 않는다. |
| Canonical Claim | answer-local claim_id, S/P/O/polarity/conditions, assertion_context, source_text/span, requirement_refs, qualifiers, extraction_confidence | Claim은 답안에 쓰인 관계이지 승인 사실이나 정답 판정이 아니다. qualifier owner는 추출 근거이며 권위 있는 소유권 증명이 아니다. |
| Diagnostic | 기존 audit status/reason/evidence_spans/score_effect | 새 진단에서 승인/배점/fatal/ceiling/운영 점수 투영 금지. |

기존 Registry 1,524 rows, 정본 2,096, P1-A 연결 1,522 unique anchors (574 미연결). P1-A의 한 Anchor에 두 Fact 및 한 legacy ID 없는 행을 보존한다. 이 수치는 P1-A 재사용이며 신규 전수 Machine join은 P2-B. ID가 같아도 relation의 의미가 다르면 mapping evidence가 필요하다.

### 직접 확인한 연결 사례 (고정 main)

1. Flow owner `flow_measurement_meter_principles_velocity_selection`, anchor/requirement `flow_volumetric_rate_area_integral`: question "유량과 유속의 정의 및 단면 평균유속, 체적유량 관계를 설명하시오." required_anchor_ids에 정확히 포함. Registry Fact ID도 같은 문자열이지만 relation=(volumetric_flow_rate, equals, cross_section_integral_of_normal_velocity), conditions=[defined_cross_section, continuum_flow]. Machine required Fact는 **volumetric_flow_from_area_average_velocity**, relation=(volumetric_flow, equivalent_to, area_average_velocity_product, positive), no conditions. 정본에 면적 적분과 Q=A*v_bar 모두 존재. 서로 관련 있으나 두 표현 전체 동치를 구조적 ID 동일성으로 간주하지 않는다.
2. 같은 Flow owner `flow_mass_rate_density_relation`: Registry Fact same ID, relation=(mass_flow_rate, equals, cross_section_integral_of_density_times_normal_velocity), conditions=[defined_cross_section,density_uniform_for_simplified_mdot_equals_rho_q]. Machine required facts=`mass_flow_density_volume_relation` (mass_flow,equivalent_to,density_volume_flow_product,positive,uniform_density), `mass_flow_distinct_from_volume_flow` (mass_flow,equivalent_to,volumetric_flow,negative), min=1. Registry 관계 하나를 두 Machine Fact나 전체 정답으로 자동 치환하지 않음.
3. FSRM owner `functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh`: rule `demand_mode_metric_selection` (3 required facts, min=2), `quantitative_verification_dimension` (3 facts, min=2). 이 두 ID는 해당 owner의 canonical anchors 및 explicit required_anchor_ids에 없음. 첫 ID와 같은 legacy_anchor_id가 SIL target owner의 Registry `sil_demand_mode_metric_selection`에 있으나 **다른 Topic이며 기존 independent revision HOLD**. 잘못된 owner join 또는 제외 우회 금지.
4. Feedback owner `feedback_system_closed_loop_sensitivity_steady_state_error`의 `feedback_parameter_sensitivity` → Registry `closed_loop_parameter_sensitivity@1` 명시적 링크는 있음. 해당 logic_check.json에는 machine_contract가 없음. P1-C 문구 후보도 미적용. 즉 승인 Fact가 있어도 이 경로의 직접 관계 인식은 NO_MACHINE_CONTRACT / RECOGNITION_UNCERTAIN.

네 exclusion JSON도 직접 읽어 owner+Anchor 키 합집합 276+80+80+103=539, 중복 0 확인. 예 1/2/4 키 미등재는 positive admission 승인이 아니다. 후보 HOLD의 source hash 재계산은 NOT_RUN.

## 3. Canonical Claim 필드 계약 (기존 schema 그대로)

| Field | 의미 / 검증 |
|---|---|
| subject / predicate / object | 명시된 주체/관계/대상 canonical ID; existing ontology + selected contract vocabulary. schema regex 검증은 ontology membership/engineering meaning을 보증하지 않음. |
| polarity | positive/negative; predicate 자체의 부정 의미와 별도 (does_not_guarantee, distinct_from, supplements 등). 단순 '않' 등장만으로 반전 금지. |
| conditions | canonical ID 배열; 반드시 어떤 관계에 귀속되는지 확인. 기존 extractor의 문장 단위 alias 수집은 귀속 증명 아님. |
| assertion_context | asserted/corrected만 채택 후보; quoted/rejected는 근거 기록만. correction 범위 불명확하면 abstain. |
| source_text / source_span | 답안 문자열의 정확한 start-inclusive/end-exclusive 문자 위치. answer[start:end]==source_text, 원문 재검증. |
| requirement_refs | 기존 schema 배열; 일반 extractor에서는 빈 배열. producer 제안만으로 question scope 확정 불가. |
| qualifiers | string-valued map; owner_topic_id, context_inferred_subject 등이 관측됨. inferred subject/누락 owner는 독립 검토 필요; 새 필드 강제하지 않음. |
| extraction_confidence | 0..1 범위의 추출 정보; 1.0이 기술 진실/승인/점수 보증 아님. |
| claim_id | normalized row hash 기반 자동 생성 또는 주어진 ID, evidence 문서 안에서 고유. Fact ID 아님. |
| document provenance | schema_version=1.0; marker=CANONICAL_GRADING_EVIDENCE_V1; source.mode/resolver_id/resolver_version, question_sha256/answer_sha256, evidence_sha256, summary.claim_count; authority=evidence_only, score_effect=none. |

기존 builder는 omitted polarity/context/confidence에 기본값을 부여하고 syntax를 검증한다. P2-B 합성 데이터는 이를 의미 판정으로 쓰지 않고 polarity/context/conditions를 명시적으로 제공한다. Registry provenance는 별도로 source_id/version/sha256/locator 및 verification authority/citation/locator/checked_at/supports_claim을 사용하며, answer span과 교환할 수 없다. P2-B 기록에는 고정 main/파일 blob/Fact ID+revision/질문 scope 근거, answer span, 결과 이유를 남긴다. 새 런타임 schema 없음.

## 4. 적용 범위 및 불확실 경계

| 유형 | 기존 구현 확인 | P2-B/C 비채점 기준 |
|---|---|---|
| 명시 관계 | evaluator S/P/O/polarity exact + fact condition subset | 명시 owner/scope/근거/조건을 갖춘 경우만 관계 일치. 조건 누락은 관계 불확실이지 정답/오답 자동 아님. |
| 반대 관계 | 기존 evaluator opposite polarity가 exact보다 우선, 일부 predicate closed-world object conflict | 조건이 같고 채택된 명시 반대만 confirmed contradiction; 다른 조건/대안 object는 의미상 상호 배타성 확인 없으면 불확실. 기존 운영 정책 변경 안 함. |
| 복합 조건 | extractor _conditions 문장 단위 aliases; pilot 조건 있는 Fact/Claim 모두 보류 | 조건 이름 일치만으로 귀속 확정 금지; AND/OR, 범위, 예외, 다른 절/문장 귀속 불명확이면 보류. |
| 부정/인용/정정 | regex assertion_context/polarity, corrected 채택 가능; audit은 인용 표식 있는 전체 span 제외 | 정정은 실제 채택된 부분이 분리 가능한 경우만. 인용/오개념 예시/가정은 긍정·부정 credit 근거 아님. |
| 상충 | 운영 evaluator opposite 우선, claim_id 1회 allocation; audit mixed support+contradiction는 uncertain | 상충·서로 다른 적용조건·모호한 대체 해석은 신규 진단에서 RECOGNITION_UNCERTAIN. 기존 fatal 등 별도 보존. |
| 단순 언급/용어 나열 | extractor mentioned/unspecified_detail, 기존 rule은 optional mention partial; pilot 완결 한국어 문장만 | 용어열은 관계 일치 근거 아님. 빈 답안만 현 pilot CONTENT_INSUFFICIENT; 관계 부재는 지식 부재가 아님. |
| 주체 상속 | extractor 문장 간 제한된 context inference, audit 상속 주체 제외 | 추론 주체 또는 owner 애매하면 보류, 질문으로 답안 사실 채워넣기 금지. |
| 추출 미완료 | extractor unresolved_spans 및 extraction_complete; evaluator false일 때 UNKNOWN; 운영 primary grader L237은 True를 전달하고 뒤에서 unresolved를 별도 처리 | 새 진단에서 운영의 True를 그대로 completeness 증명으로 사용하지 않음. parser omission/unknown은 RECOGNITION_UNCERTAIN; MISSING/WRONG 강제 금지. |
| 질문 범위 | explicit similarity>=0.2, 미충족시 bounded derived projection 최대 12, cross-topic 우선 | P2-B direct explicit 질문부터 시작, derived/mismatch 분리; #34 소유 경계 유지. |
| scope/owner | evaluator key 자체에는 owner가 없고 allocation은 claim_id 단위; ordinary requirement scope는 canonical Anchor ID에 적용 | 신규 진단은 owner+exact Anchor/rule 명시 확인, scope 모호함은 보류. 독립 invariant 기존 예외를 지우지 않음. |
| 수식·단위 | quantity ontology 4 quantities/2 dimensions/7 relations; dimension check on adopted positive claims; DP symbolic formula side output narrow grammar | 차원 일치≠수치/단위환산/수식 동치. 변수 정의, 환산, domain, 가정, sign 검증 전 확정 금지. symbolic candidate_status는 canonical evidence의 verdict 아님. |
| 기술적 관계 coverage | ontology 180 engineering concepts, 36 canonical predicates (파일 직접 읽음; quantity relations 별도), Registry predicate vocabulary와 동일하지 않음 | 없는 ID를 임의 추가/alias 치환하지 않음. #33 추출·#35 관계 평가 개선은 별도 owner. |

## 5. 기존 동작과 P2 비채점 정책을 구분

운영 경로: route → canonical extractor → quantity + engineering invariants → cross-topic 또는 Anchor adapter → deterministic requirement evaluator → augment → symbolic formula candidates. 기존 evaluator SATISFIED/PARTIAL/WRONG/MISSING/UNKNOWN 및 findings의 downstream 사용, lexical recall floor(MISSING→PARTIAL 조건부; EMC canonical-only 제외), existing invariant/fatal/ceiling은 변경 금지. P2는 별도 audit 경로의 score_effect none만 사용한다. 기존 Machine Contract의 downstream authority를 evidence-only로 덮어쓰지 않는다.

현재 audit는 CONFIRMED_RELATION / CONFIRMED_CONTRADICTION / RECOGNITION_UNCERTAIN / CONTENT_INSUFFICIENT를 사용한다. UNKNOWN/ABSTAIN은 개념적 보류 원칙이며 새로운 enum을 런타임에 추가하지 않는다. P2-A에서 코드 변경하지 않았으므로 기존 guard가 위 모든 목표를 구현했다고 주장하지 않는다.

## 6. P2-B 착수 계약 (합성 검증 설계; 아직 실행 아님)

1. **대상 선정**: main 고정, existing canonical owner+anchor, exact Machine requirement, required Fact 참조, approved/verified Registry의 explicit legacy link 및 관계 의미를 각각 대조. 네 exclusion에서 topic+anchor 및 Registry fact_id 모두 확인. 명시적으로 선택된 질문 required_anchor_ids 우선. 계약 부재/owner mismatch/동일 문자열만인 경우 별도 coverage gap, 평가 분모 제외 사유 기록. 기존 45개는 역사적 #46 보고의 분모이며 P2-B에서 재집계; 전수 2,096 기술 재검토 금지.
2. **구조화 입력 시험**: 기존 Machine Fact의 명시 polarity/conditions를 사용한 human-authored canonical evidence, 실제 정답/반대, 다른 owner, 누락/다른 조건, quoted/rejected/corrected, mixed, mention, invalid span을 별도로 구성. validator/evaluator/audit의 권한과 결과를 분리 기록. Production evaluator 동작과 보수적 진단 기대가 다른 경우 discrepancy로 기록, 기대값 강제 변경 금지.
3. **자연어 추출 시험**: 같은 사실을 명시 서술, 동등표현, 반대, 조건 생략, 인용·정정, 용어열, 상충, 수식·단위(적용되는 경우)로 구성. answer span, extracted tuple/condition/context/owner, unresolved, 기대 relation과 실제 진단을 분리 저장. 구조화 입력 성공률과 자연어 추출 성공률 합산 금지.
4. **검증 지표**: eligible denominator, skipped/reason, structured match/opposite/unknown, natural extraction exact or valid equivalent/coverage, false confirmation, false contradiction, uncertain, scope mismatch, relation discrepancy. 조건·인용·상충 등 보류에 대한 별도 confusion counts; 근거 없는 긍정 인정과 오답 단정 모두 방지. 수기 기대는 실행 결과와 구분.
5. **안전 게이트**: 신규 score_admission=DISABLED, score_effect=none, 119 HOLD/D4/기존 A–E/배점/fatal/ceiling/exclusion/143 답안 보호. 8개 P1-C 후보/새 Fact/새 schema/ontology 추가 없음. 실패 시 #33 extraction, #34 scope, #35 relation/grounded_attempt, #48 별도 이슈로 귀속. 최소 1개 실패를 고치기 위해 개별 keyword/regex 누적하거나 runtime 승격하지 않음. P2-C에서 진단 검증. 코드 변경 필요 시 별도 승인 및 동일 SHA regression.

### 기존 검증 이력과 이번 한계

[#46 진단 보고](pr46_relation_recognition_reassessment.md)의 과거 baseline c8f21e8...에서 16 Topic, 113 machine facts, 72 positive rules, 54 direct owner/anchor joins 중 45 exclusion 통과; 6 structured correct/6 opposite 비교 성공, 6 natural paraphrase 인정 0. 이 결과는 이번 실행 결과가 아니다. P2-A는 정적 코드/스키마/파일 직접 열람, 대표 4개 연결 사례와 exclusion 539 키 집계만 수행. 전체 machine inventory 재집계/런타임 validator/pytest/143 replay/validate-all/새 Actions/hold 해시 재계산 NOT_RUN. Firecrawl 미사용. main/production/Registry/Generated/ledger/정본/권한 미변경.

**P2-A 계약 문서 확정 완료, P2-B 실행 대기. Issue #40 OPEN; PR #49 Draft.**
