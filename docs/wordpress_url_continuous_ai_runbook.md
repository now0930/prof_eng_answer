# AI/Codex 실행 계약 — WordPress URL (텍스트·그림 참조)

**범위:** WordPress 본문 텍스트 및 그림·PDF 참조 메타데이터만 처리합니다. **서버에서 PDF 원문 읽기·다운로드·렌더링·텍스트 추출·그림 OCR을 하지 않습니다.** 이 작업을 의존성 설치나 향후 과제로 되살리지 마세요.

사람용 정책: [WordPress URL 지속 운영](wordpress_url_continuous_workflow.md). 기존 승인·검증: [연결 정책](wordpress_topic_pack_linking_policy.md), [View 계약](wordpress_topic_pack_view_contract.md), [Fact 적격성](fact_anchor_eligibility_policy.md), [AGENTS](../AGENTS.md).

## 구현 경로

| 범위 | 코드 | 계약 |
| --- | --- | --- |
| 게시글 1건 진입 | [wordpress_url_workflow.py](../scripts/wordpress_url_workflow.py) | 지정된 HTTPS WordPress permalink만 허용, 증분 저장, 비공개 백업과 상태 보고 |
| 본문·미디어 참조 | [wordpress_catalog.py](../scripts/wordpress_catalog.py) | 본문 HTML→텍스트, 그림/PDF 링크·메타데이터. URL 실행기에서 OCR 함수를 호출하지 않음 |
| 기존 Topic 검색 | [match_wordpress_posts_to_topic_packs.py](../scripts/match_wordpress_posts_to_topic_packs.py) | 본문과 기존 Topic 범위 비교; retrieval score는 승인 아님 |
| 링크 검토 | wordpress_catalog.review_topic_link() | 개별 reviewer, evidence, approval. 기존 승인/거절 덮어쓰기 금지 |
| Master 출처 | study/source_update.py | 별도 제안·revision/해시·승인 |
| 학습 | [build_wordpress_topic_packs.py](../scripts/build_wordpress_topic_packs.py) | 승인 Topic에 연결된 모든 글을 보존. 이미지/PDF 미추출 상태는 현행 URL 업무의 blocker가 아님 |
| 채점 자료 | rubrics/topic_packs/ 및 rubrics/generated/ | URL 입력만으로 Fact Anchor 또는 채점 기준 수정 금지 |

다른 독립 OCR 스크립트가 저장소에 남아 있어도 현재 URL 작업에서는 호출하지 않습니다. PDF/그림 링크만으로 기술 내용이 이해됐다고 주장하지 않습니다. 외부에서 변환하여 WordPress 본문에 기록된 텍스트와 그림 설명만 본문 자료로 검색됩니다.

## 실제 명령

~~~bash
# 본문 텍스트·그림/PDF 링크 참조 수집, 후보·상태 보고
python3 scripts/wordpress_url_workflow.py "https://now0930.pe.kr/wordpress/자기회로/"

# 기존 비공개 카탈로그 조회 (네트워크 없음)
python3 scripts/wordpress_url_workflow.py "https://now0930.pe.kr/wordpress/자기회로/" --offline

# 실제 reviewer·근거를 갖춘 Topic 링크 개별 승인
python3 scripts/wordpress_url_workflow.py "https://now0930.pe.kr/wordpress/자기회로/" --offline --topic-id ACTUAL_TOPIC_ID --decision approve --reviewer ACTUAL_REVIEWER --evidence "본문 제2절의 계측 원리와 Topic 소유 범위 비교"
~~~

기존 --skip-ocr 및 --refresh-assets 옵션은 삭제했습니다. 서버에는 Tesseract/Poppler 의존성이 필요하지 않습니다. 출처 업데이트·Fact 검증·채점 변경은 자동 승인이 아니라 **각각 별도의 명시적 심사**가 필요합니다.

## 단계별 정지·검증

1. WordPress permalink·카테고리·post ID 식별에 실패하면 차단합니다.
2. 원문 텍스트가 없고 그림/PDF 참조만 있으면, 링크를 저장할 수 있어도 그림의 사실 검증이나 Fact 승격은 보류합니다. **OCR을 대안 작업으로 제시하지 않습니다.**
3. 본문 해시, 게시글 메타데이터, 저장된 참조 URL·설명이 같으면 DB 수집을 건너뜁니다. 상대 참조는 permalink 기준으로 해석합니다. 같은 URL이 다른 게시글 ID로 나타나면 수동 확인을 위해 차단합니다. 변경 시 기존 승인·거절 및 검토 이력을 보존합니다.
4. 대상 글의 승인된 WordPress **본문 source** 유형·URL·버전이 Master와 일치해야 학습 bundle을 갱신합니다. 같은 Topic의 다른 승인 게시글도 보존하며 동일한 bundle은 다시 쓰지 않습니다. 검색과 bundle에서 과거 OCR 텍스트를 제외합니다.
5. 본문만으로 근거 부족한 Topic 후보는 보류합니다. WordPress 연결 승인과 채점 기준 승인은 독립 단계입니다.
6. DB 쓰기 전 저장소 외부 비공개 SQLite 백업을 만들고, 보고 JSON은 비공개 data/wordpress_url_intake/ 경로에 둡니다.
7. 사용하지 않은 OCR/PDF 기능에 대한 재구축·재검증·설치 과제는 생성하지 않습니다.

## 검증

~~~bash
python3 -m pytest -q tests/test_wordpress_url_workflow.py
python3 scripts/test_wordpress_topic_link_review_application.py
python3 scripts/test_match_wordpress_posts_to_topic_packs.py
python3 -B scripts/release_candidate.py validate
~~~

실행하지 않은 테스트·운영 배포를 완료라고 쓰지 않습니다. OCR 미실행은 정상 동작입니다. 운영 DB 쓰기·봇 재시작·main 브랜치 변경은 별도 작업입니다.

## 보고

URL, post ID, 변경 여부, 본문 인덱싱, 미디어 참조, Topic 후보 및 승인 상태, Master source, 학습 bundle, 독립 Fact 검증/보류, 비공개 백업, 검증 결과, 다음 작업 1순위를 출력합니다. **PDF/OCR 성공률·설치 필요성·OCR 재시도는 보고 항목에 포함하지 않습니다.**
