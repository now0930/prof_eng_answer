# WordPress Chapter 20 두 글의 출처 갱신과 Topic 경계

검토일: 2026-10-14 (KST). 대상은 [후반부: 변위·에코·기타 레벨 방식](https://now0930.pe.kr/wordpress/lessons-in-industrial-instrumentation-chapter-20/)과 [전반부: 직시·정수압·차압](https://now0930.pe.kr/wordpress/chapter-20/)이다. 두 글은 **제목이 같아도 다른 글**이며 post ID와 source ID로 구분한다. 이 문서는 출처 연결과 Topic 소유권 결정이다. 글의 모든 기술 사실을 검증하거나 Grading View에 자동 승격한 기록은 아니다.

## DB 반영 결과

| 글 | post ID | 반영 내용 | 기존 승인 연결 |
|---|---:|---|---|
| 후반부 | 9745 | 신규 게시글, HTML 평문 9,819자, 자체 PDF 9쪽 디지털 추출 11,003자 | 없음 |
| 전반부 | 9529 | HTML 재조회·해시 갱신, 평문 10,119자; 비교 결과 하이픈 13곳이 대시로 치환 | 차압식 레벨 Topic 유지 |

- 운영 비공개 DB: `/home/now0930/hermes/workspace/prof_eng_answer/data/wordpress_sources.sqlite3`. 갱신 전 SQLite 백업과 수집 원문·갱신 보고서는 `backups/wordpress_chapter20_20261014T001507Z/`에 보관한다. DB는 공개 Git에 포함하지 않는다.
- DB 글 수 309 → 310, 무관 글과 승인·거절 연결 보존, `PRAGMA integrity_check=ok`, 외래키 오류 없음. 기존 전반부의 승인 연결에 대한 WordPress Source bundle을 재생성했다.
- 전체 Source Pack 검증에서 이전부터 누락된 Topic 인벤토리 4행을 발견해 현재 정본으로 보강했다. 기존 `second_order_system_modeling_electromechanical_analogy` 링크도 삭제하지 않았다. 최종 `validate_wordpress_source_pack.py` PASS: 글 310, 출처 1,370, Topic 86, 링크 638(승인 222, 대기 7). 이 정합성 보강은 Topic Pack의 내용 수정이나 새 Pack 생성을 뜻하지 않는다.
- 신규 PDF source `wpurl:8e19947172bd7a314ff2ae0f8809684b`는 `pdftotext`로 추출했다. 이미지 OCR 또는 기술 사실 검증을 통과했다는 뜻은 아니다. 두 글의 HTML과 PDF는 출처로 보존한다.
- 전반부의 구두점 변경으로 Master source update proposal `catalog-56ec66d504a18d85e060180e`가 `pending_approval`이다. 제안은 출처 버전 갱신용이며 Master의 Fact·채점 기준은 변경하지 않았다.
- 신규 글의 레이더·초음파·광학·로드셀·수동형 센서 연결 5건은 `pending_review`다. 현재 승인 연결이 없으므로 이 글은 아직 Training/Grading용 승인 Source bundle에 들어가지 않는다.

## 문제 단위 소유권 판단

| 원문 범위 | 판단 | 이유·경계 |
|---|---|---|
| 전반부 정수압, 폐쇄탱크 DP, Wet Leg, Remote Seal, 밀도 계산, 계면 | **기존 차압식 레벨 Pack 유지** | 이미 승인 연결과 Chapter 20 보강이 있으며 질문군이 동일하다. 구두점 차이로 Pack Fact를 재작성하지 않는다. |
| 전반부 Sight Glass, Float, Bubbler | **기존 관리형 draft 후보를 계속 검토** | `rubrics/topic_pack_candidates/`에 각 독립 질문군 초안이 있다. 현재 운영 Pack으로 승격하지 않는다. |
| 후반부 Ultrasonic, 자유공간 Radar, Laser ToF, Load Cell 원리, 일반 정전용량 원리 | **기존 Pack에 출처 추가 후보** | 이미 소유 Topic이 있다. 다만 Laser 글은 ToF 적용만, 로드셀 글은 탱크 중량 적용만, 수동 센서 글은 `C=εA/d` 원리만 뒷받침한다. 이 글 하나로 기존 Pack 전체를 검증하지 않는다. |
| 후반부 GWR의 probe-guided wave 및 계면 | **기존 GWR draft 후보 활용** | 별도 `guided_wave_radar_level_measurement_tdr_interface_application` 후보가 있다. 자유공간 Radar 문제의 필수 Fact로 합치지 않는다. |
| 후반부 고정 Displacer의 부력·Torque Tube·밀도·계면·Wet/Dry calibration | **독립 운영 Topic Pack으로 승격** | Float의 위치 추종, DP의 정수압과 다른 측정 사슬이다. `displacer_level_buoyancy_torque_tube_density_interface_calibration`은 사용자 검토 완료 선언 후 `approve-topic --reviewer now0930`으로 승인했고, 질문별 필요 Fact를 분리했다. |
| 후반부 Capacitive Level, Radiation Level, Magnetostrictive, Weight→Level, Stilling Well | **출처 기록·추가 근거 대기** | 각 기술의 레벨 적용 설명이 짧다. 일반 센서 Pack에 레벨 전용 적용·안전 조건을 무조건 요구하지 않는다. 독립 질문의 범위와 기술 사실을 검증한 뒤 새 Pack 또는 기존 Pack 보강을 결정한다. |

## 검토가 필요한 원문 표현

- 후반부의 `X-ray 또는 Gamma-ray` 설명과 `Radiation Source는 항상 ... Always-on` 설명을 하나의 무조건 규칙으로 채점에 넣지 않는다. 소스 종류별 조건과 안전 요구를 별도 확인해야 한다.
- Echo 방식에서 Gas 조성·압력·온도 영향은 초음파와 레이더에 동일한 크기로 적용할 수 없다. 현재 문장을 기종 공통 필수 답안으로 만들지 않는다.
- 전반부 `Tank Expert System` 3압력 탭 식은 탭 위치·액체 밀도 가정, 설치수두 조건을 포함해야 한다. 기존 DP Pack이 이 경계를 이미 설명한다.
- 출처 HTML이 PDF보다 읽기 쉬워도 출처 표현과 기술적으로 검증된 Fact를 구별한다. 수식·조건이 불명확하면 원문 참조로만 보관한다.

## 다음 구현 경계

1. 승인된 기존 Topic에 한해서 새 글의 **해당 절**을 source link로 검토한다. 자동 키워드 유사도만으로 승인하지 않는다.
2. Displacer 예상문제 3종, Fact 7개, 정상/오답 경계, Float/DP handoff를 [Topic Sheet](../topic_sheets/displacer_level_buoyancy_torque_tube_density_interface_calibration.md)와 `rubrics/topic_packs/displacer_level_buoyancy_torque_tube_density_interface_calibration/`에 반영했다. 사용자 검토 선언을 `topic_status.json`의 `reviewer=now0930`, `review_method=human`, 승인 source hash로 기록했다. 후보 경로는 제거하고 generated 뱅크 6종에 반영했다.
3. 승격 당시 라우팅 별칭·분야 단서 최소 개수 부족으로 첫 승인 시도가 실패하여 Displacer 전용 표현만 보강한 뒤 승인했다. 승인 후 Pack source 문구를 수정하면 hash gate가 차단하므로 최종 승인 source는 변경하지 않았다. [회귀 테스트](../../tests/test_displacer_level_topic_release.py)는 승인 hash, 질문별 요구 범위와 6개 뱅크 포함 여부를 확인한다. 실제 운영 배포·실제 답안 채점 품질은 별도 점검 대상이다.

## 2026-10-14 운영 승격 후 출처 연결

- 비공개 DB에 새 운영 Topic 인벤토리를 등록하고 post `9745`의 **20.4–20.4.7 Displacer 절에 한정한** 링크를 승인했다. 검토자는 `codex:source-scope-after-user-pack-review`로 기록해 사용자의 Pack 검토 선언과 AI의 출처 범위 판단을 혼동하지 않았다.
- 변경 전 DB 백업은 비공개 `backups/wordpress_displacer_link_20261014T053340Z/`에 저장했다. 비공개 Source bundle은 HTML 1건(9,819자)과 자사 PDF 디지털 텍스트 1건(11,003자)으로 생성했다. 이미지 OCR 완료를 주장하지 않는다.
- Master 레코드의 두 출처 모두 `training_scope=text_ranges`로 20.4 절만 포함하며 `verification_status=unverified`를 유지한다. 출처 링크 승인은 글 전체의 기술 사실 승인이나 Master 내용 자동 수정이 아니다. DB source update proposal 2건은 별도 절차가 필요하다.
- 비공개 DB 검증은 posts 310, sources 1,370, topics 87, links 639(approved 223, pending 7)로 PASS했다. Master–Grading/Training/Diagnosis 구조 감사도 topics 87 / masters 87로 PASS했다.
