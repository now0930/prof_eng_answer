# 문서 운영 정책: 사람용 + AI용

사람은 [프로젝트 소개](../README.md) → [문서 인덱스](README.md) 순서로,
AI/Codex는 [구현 참조](ai_implementation_reference.md) → [작업 정책](../AGENTS.md) → 실제 코드·스키마·테스트 순서로 읽습니다.

## 두 문서의 책임

| 구분 | 사람용 | AI·개발자용 |
| --- | --- | --- |
| 목적 | 무엇을 하는지, 어떻게 사용하는지 | 코드가 어떻게 동작하며 무엇을 변경할 수 있는지 |
| 표현 | 짧은 설명, 사용 순서, 주의사항 | 파일·함수·입출력·상태·예외·source-of-truth |
| 연결 | README → 주제별 ‘사람용 핵심’ | AI 구현 지도 → 해당 상세 계약 → 코드와 focused regression |
| 금지 | 내부 필드·실험 로그를 본문에 중복 나열 | 계획을 구현 완료라고 하거나 LLM 의견을 채점 승인으로 추정 |

이번에 현재 지침 문서의 상단에 사람용 핵심을 배치하고,
기존 기술 계약은 삭제하지 않고 AI·개발자용 참조와 연결했습니다.
문서를 수정할 때 같은 사실을 양쪽에 상세히 중복하지 않습니다.

## 전체 문서 분류 (2026-11-13 지정 브랜치)

기준 인벤토리는 Git 추적 Markdown **549개**였습니다. 첫 문서 관리 정책 추가 후 550개였으며, 이번 WordPress 지속 운영 정책·AI 실행 계약 2개를 더하면 **552개**입니다.
이는 특정 커밋의 파일 인벤토리로, 운영 서버의 비공개 파일 수와 다릅니다.

| 종류 | 파일 수 | 유지 정책 |
| --- | ---: | --- |
| `docs/` 최상위 현행 지침·설계 | 기존 62개 + 이 정책 1개 + WordPress 운영 문서 2개 | 요약·AI 연결 및 확인된 정책 불일치 수정 |
| `docs/` 최상위 과거 감사·단계 기록 | 99개 | 당시 증거·수치 보존 |
| `docs/exam_scope/` | 5개 | 출제기준 내부 매핑과 당시 Topic 수 구분 |
| `docs/topic_sheets/` | 94개 | 원본 작성·검토 내용 보존 |
| `docs/archive/` / `docs/reviews/` / `docs/topic_pack_proposals/` | 10 / 5 / 1개 | 과거 기록·검토·제안 보존 |
| `rubrics/topic_packs/`의 canonical README | 89개 | hash·승인 영향 때문에 일괄 수정 금지 |
| `rubrics/topic_pack_candidates/` | 8개 | 채점 미승격 후보 기록 보존 |
| `reports/` | 161개 | 감사 당시 결과 보존. 새 결과는 새 보고서에 작성 |
| `calibration/` | 10개 | 안내 2개 현행화, 8개 과거 심사 기록 보존 |
| `scripts/` | 2개 | CLI·오프라인 pytest·검토 정책 현행화 |
| 루트 문서 | 3개 | 사람용 README·AI 작업 정책·D/E 계약 |

**보존 ≠ 검토 누락:** 과거 `READY/HOLD`, Topic 69·71·78·82·86개, 재현성 검사 수행 여부는
그 시점의 결과입니다. 현행 코드의 필수 배포 승인 조건으로 되살리지 않습니다.
Topic Sheet·canonical README는 단순 설명 변경에도 콘텐츠 승인·hash가 영향을 받을 수 있어
독립된 authoring 절차 없이는 일괄 재작성하지 않습니다.

## 현재 주제별 상세 문서 64개

다음은 이번에 사람용 요약, 구현 링크 또는 정책 정정이 적용된 **현행 지침·설계** 범위입니다.
경로가 존재하고 문서 경계·주요 정책을 점검한 것이며, 모든 과거 기술 수치·외부 자료를
독립적으로 재실험했다는 뜻은 아닙니다.

| 문서 | 분야 | 성격 |
| --- | --- | --- |
| [`README.md`](README.md) | 통합 | 현행 안내·계약 |
| [`TOPIC_ROUTER.md`](TOPIC_ROUTER.md) | Topic·Router | 계획·이력/계약 혼합 |
| [`accuracy_release_gate.md`](accuracy_release_gate.md) | 채점·Fact | 현행 안내·계약 |
| [`ai_implementation_reference.md`](ai_implementation_reference.md) | 통합 | 현행 안내·계약 |
| [`answer_review_loop_policy.md`](answer_review_loop_policy.md) | 학습·출처 | 현행 안내·계약 |
| [`cross_topic_question_contract.md`](cross_topic_question_contract.md) | 채점·Fact | 현행 안내·계약 |
| [`data_reports_inventory.md`](data_reports_inventory.md) | 통합 | 현행 안내·계약 |
| [`deterministic_grading_completion_plan.md`](deterministic_grading_completion_plan.md) | 채점·Fact | 계획·이력/계약 혼합 |
| [`deterministic_grading_transition.md`](deterministic_grading_transition.md) | 채점·Fact | 계획·이력/계약 혼합 |
| [`development_roadmap.md`](development_roadmap.md) | 통합 | 계획·이력/계약 혼합 |
| [`difficulty_and_selection_strategy.md`](difficulty_and_selection_strategy.md) | 채점·Fact | 현행 안내·계약 |
| [`docker_compose_usage.md`](docker_compose_usage.md) | 운영·검증 | 현행 안내·계약 |
| [`essay_grading_boundary_work.md`](essay_grading_boundary_work.md) | 운영·검증 | 현행 안내·계약 |
| [`expert_calibration_dataset_contract.md`](expert_calibration_dataset_contract.md) | 채점·Fact | 현행 안내·계약 |
| [`fact_anchor_blocked_chatgpt_review_guide.md`](fact_anchor_blocked_chatgpt_review_guide.md) | 채점·Fact | 현행 안내·계약 |
| [`fact_anchor_content_review_handoff.md`](fact_anchor_content_review_handoff.md) | 채점·Fact | 계획·이력/계약 혼합 |
| [`fact_anchor_eligibility_policy.md`](fact_anchor_eligibility_policy.md) | 채점·Fact | 현행 안내·계약 |
| [`fact_candidate_resolver_v1.md`](fact_candidate_resolver_v1.md) | 채점·Fact | 현행 안내·계약 |
| [`fact_grounded_contract_v1.md`](fact_grounded_contract_v1.md) | 채점·Fact | 현행 안내·계약 |
| [`fact_grounded_deterministic_grading_plan.md`](fact_grounded_deterministic_grading_plan.md) | 채점·Fact | 계획·이력/계약 혼합 |
| [`fact_question_compiler_v1.md`](fact_question_compiler_v1.md) | 채점·Fact | 현행 안내·계약 |
| [`fact_source_projection_v1.md`](fact_source_projection_v1.md) | 채점·Fact | 현행 안내·계약 |
| [`grading_architecture.md`](grading_architecture.md) | 채점·Fact | 현행 안내·계약 |
| [`grading_integrity_drift_runbook.md`](grading_integrity_drift_runbook.md) | 채점·Fact | 현행 안내·계약 |
| [`grading_quality_roadmap.md`](grading_quality_roadmap.md) | 채점·Fact | 계획·이력/계약 혼합 |
| [`internal_topic_ownership_contracts.md`](internal_topic_ownership_contracts.md) | Topic·Router | 현행 안내·계약 |
| [`learning_layer.md`](learning_layer.md) | 학습·출처 | 현행 안내·계약 |
| [`llm_provider.md`](llm_provider.md) | 채점·Fact | 현행 안내·계약 |
| [`logic_check_json_generator_prompt.md`](logic_check_json_generator_prompt.md) | 채점·Fact | 계획·이력/계약 혼합 |
| [`logic_check_profile_generator_prompt.md`](logic_check_profile_generator_prompt.md) | 채점·Fact | 계획·이력/계약 혼합 |
| [`logic_check_profiles_readme.md`](logic_check_profiles_readme.md) | 채점·Fact | 현행 안내·계약 |
| [`master_topic_pack_contract.md`](master_topic_pack_contract.md) | 학습·출처 | 현행 안내·계약 |
| [`master_view_architecture.md`](master_view_architecture.md) | 학습·출처 | 현행 안내·계약 |
| [`operation_runbook.md`](operation_runbook.md) | 운영·검증 | 현행 안내·계약 |
| [`operational_quality_checksheet.md`](operational_quality_checksheet.md) | 운영·검증 | 현행 안내·계약 |
| [`private_runtime_backup.md`](private_runtime_backup.md) | 운영·검증 | 현행 안내·계약 |
| [`python_layout.md`](python_layout.md) | 운영·검증 | 현행 안내·계약 |
| [`qualitative_de_shadow.md`](qualitative_de_shadow.md) | 채점·Fact | 계획·이력/계약 혼합 |
| [`question_type_taxonomy.md`](question_type_taxonomy.md) | 채점·Fact | 현행 안내·계약 |
| [`rubric_authoring_guide.md`](rubric_authoring_guide.md) | 채점·Fact | 현행 안내·계약 |
| [`semantic_assist_roadmap.md`](semantic_assist_roadmap.md) | 운영·검증 | 계획·이력/계약 혼합 |
| [`system_architecture.md`](system_architecture.md) | 통합 | 현행 안내·계약 |
| [`topic_learning_authoring.md`](topic_learning_authoring.md) | 학습·출처 | 현행 안내·계약 |
| [`topic_learning_synthesis_contract.md`](topic_learning_synthesis_contract.md) | 학습·출처 | 현행 안내·계약 |
| [`topic_learning_synthesis_plan.md`](topic_learning_synthesis_plan.md) | 학습·출처 | 계획·이력/계약 혼합 |
| [`topic_learning_synthesis_validation.md`](topic_learning_synthesis_validation.md) | 학습·출처 | 현행 안내·계약 |
| [`topic_pack_architecture.md`](topic_pack_architecture.md) | Topic·Router | 현행 안내·계약 |
| [`topic_pack_atomicity.md`](topic_pack_atomicity.md) | Topic·Router | 현행 안내·계약 |
| [`topic_pack_workflow.md`](topic_pack_workflow.md) | Topic·Router | 현행 안내·계약 |
| [`topic_router_v2.md`](topic_router_v2.md) | Topic·Router | 계획·이력/계약 혼합 |
| [`topic_router_v2_design.md`](topic_router_v2_design.md) | Topic·Router | 계획·이력/계약 혼합 |
| [`validation_api_cost_policy.md`](validation_api_cost_policy.md) | 운영·검증 | 현행 안내·계약 |
| [`wordpress_review_topic_contract.md`](wordpress_review_topic_contract.md) | 학습·출처 | 현행 안내·계약 |
| [`wordpress_topic_full_catalog_retrieval.md`](wordpress_topic_full_catalog_retrieval.md) | 학습·출처 | 현행 안내·계약 |
| [`wordpress_topic_link_confirmed_only_policy.md`](wordpress_topic_link_confirmed_only_policy.md) | 학습·출처 | 현행 안내·계약 |
| [`wordpress_topic_link_decision_application_workflow.md`](wordpress_topic_link_decision_application_workflow.md) | 학습·출처 | 현행 안내·계약 |
| [`wordpress_topic_link_llm_review_guide.md`](wordpress_topic_link_llm_review_guide.md) | 학습·출처 | 현행 안내·계약 |
| [`wordpress_topic_link_second_llm_improvement_work_instruction.md`](wordpress_topic_link_second_llm_improvement_work_instruction.md) | 학습·출처 | 현행 안내·계약 |
| [`wordpress_topic_link_third_review_work_instruction.md`](wordpress_topic_link_third_review_work_instruction.md) | 학습·출처 | 현행 안내·계약 |
| [`wordpress_topic_pack_linking_policy.md`](wordpress_topic_pack_linking_policy.md) | 학습·출처 | 현행 안내·계약 |
| [`wordpress_topic_pack_ocr.md`](wordpress_topic_pack_ocr.md) | 학습·출처 | 현행 안내·계약 |
| [`wordpress_topic_pack_view_contract.md`](wordpress_topic_pack_view_contract.md) | 학습·출처 | 현행 안내·계약 |

| [`wordpress_url_continuous_workflow.md`](wordpress_url_continuous_workflow.md) | 학습·출처 | 사람용 반복 운영 정책 |
| [`wordpress_url_continuous_ai_runbook.md`](wordpress_url_continuous_ai_runbook.md) | 학습·출처 | AI·Codex 실행 계약 및 방향 감시 |

## 코드에 맞춰 고치는 순서

1. 같은 Git 브랜치의 실제 코드·`.env.example`·source JSON·관련 테스트를 확인합니다.
2. 배점·Fact 승인·Reviewer·Topic Pack source/생성 bank·Master/Training 권한을 구분합니다.
3. 사람용에는 목적·순서·주의점을 3~5문장으로 요약하고, AI용은 정확한 코드 경로·검증 방법을 둡니다.
4. 배포용 **필수 코드 검증은 전체 오프라인 pytest**입니다. Accuracy·Authority·Stability 및 유료 qualification은 선택 진단입니다.
5. 제거된 전용 10회 동일 입력 채점 검사를 필수 CI·Release·보고 항목으로 복원하지 않습니다.
6. 개인 답안·세션·OCR 원문·운영 DB·`.env`는 Git에 올리지 않습니다. Git 변경이 운영 배포를 증명하지 않습니다.
7. 수정 후 Markdown 링크·파일 경로·승인·hash 영향·실제 테스트 결과를 구분해 보고합니다.

## 남는 검증 경계

이 정리는 **현행 설명 문서의 이해도·연결·발견된 정책 충돌을 개선**한 것입니다.
모든 출제기준의 최신 외부 원문 재대조, 과거 161개 감사 보고서의 수학적 재검증,
전체 89개 Topic README의 기술 내용 재승인, 전체 pytest 실행을 수행했다는 뜻은 아닙니다.
그런 검증은 별도 작업이며, 과거 기록은 변경하지 않고 새 근거를 추가해야 합니다.
