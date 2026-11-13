# 문서 안내

**사람은 [프로젝트 소개](../README.md)부터**, 코드·파일을 확인할 AI/Codex는 **[AI·개발자용 구현 참조](ai_implementation_reference.md)**부터 읽으세요.
문서보다 현재 커밋의 코드·설정·테스트가 실제 동작을 결정합니다.

| 알고 싶은 것 | 문서 |
| --- | --- |
| 전체 연결과 데이터 권한 | [시스템 구조](system_architecture.md) |
| 채점 점수·문제 유형 | [채점 구조](grading_architecture.md), [문제 유형](question_type_taxonomy.md) |
| 학습·복습 | [학습 루프](answer_review_loop_policy.md), [학습 계층](learning_layer.md) |
| Topic Pack 구조·수정 | [Topic Pack 구조](topic_pack_architecture.md), [작성·승인](topic_pack_workflow.md) |
| 채점 가능한 Fact 기준 | [Fact Anchor 적격성](fact_anchor_eligibility_policy.md) |
| Master와 WordPress | [Master/View](master_view_architecture.md), [WordPress/View](wordpress_topic_pack_view_contract.md), [OCR](wordpress_topic_pack_ocr.md) |
| 공개·비공개 데이터와 보고서 | [데이터·보고서 인벤토리](data_reports_inventory.md) |
| 비공개 데이터 백업 | [백업/복원](private_runtime_backup.md) |
| 운영·배포 | [운영 절차](operation_runbook.md), [Compose](docker_compose_usage.md) |
| 개발 단계·이력 | [로드맵](development_roadmap.md), `../reports/`, `archive/` |
| **AI/Codex 구현 탐색과 문서 동기화** | **[AI 구현 지도](ai_implementation_reference.md)**, [AGENTS](../AGENTS.md) |

## 주의할 경계

- **채점 원본** `rubrics/topic_packs/`과 **생성 bank** `rubrics/generated/`는 다릅니다. 생성물을 직접 편집하지 않습니다.
- WordPress OCR·Master 출처 연결·AI 모범답안은 **학습 자료**이지 자동 승인된 채점 사실이 아닙니다.
- 학습 이력과 복습 안내는 **확정 점수를 수정하지 않습니다.**
- `data/` 및 `reports/`는 공개 추적 파일과 비공개 실행 파일이 섞일 수 있습니다.
- 날짜가 붙은 보고서 수치·과거 `archive/` 문서는 현재 구현 증명이 아닙니다.
- **배포용 코드 검증은 오프라인 전체 pytest**입니다. Accuracy/Qualification 유료 호출을 필수 Gate로 되살리지 않습니다.

새 문서는 이 표에 연결하고, 사람용 요약에는 사용법·주의사항만 간단히 남깁니다. 상세 파일·함수·예외는 AI 참조 또는 해당 기술 문서에 둡니다.
