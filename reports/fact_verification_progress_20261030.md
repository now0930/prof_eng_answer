# Fact Anchor 사실 확인 진행 기록 (2026-10-30)

## 기준과 진행 상태

`remaining_fact_review_actions_20261030.csv`의 1,272건은 **이전 Registry의 검토 스냅샷**이다. 선별 모델의 판단만으로 `verified`를 재승인하거나 Anchor를 삭제하지 않는다. 공통 원리·적용 조건을 1차 규격, 공식 기술문서 또는 재현 가능한 식과 대조하고, 제품 고유 수치·내부 분류를 보편적인 시험 정답으로 사용하지 않는다는 기준을 적용한다.

| 판정 | 건수 | 조치 |
| --- | ---: | --- |
| 내부 학습 분류라 채점 Fact에서 제거 | 1 | `repository_sw_topic_contract_separates_transport_data_integration_and_model_use`와 `topic_boundary_transport_model`을 Registry·Pack Fact·Logic·모범답안에서 제거; SW-07/11/12 소유 구분은 Pack README의 라우팅 설명에 보존 |
| 선별 모델 오탐을 1차 표준 범위로 재확인 | 2 | 아래 PFDavg와 제어밸브 유량식 사례. 삭제·승격 없음 |
| 나머지 개별 근거·조건 확인 | 1,269 | 기존 승인 상태는 유지하되 이번 전수 *재검증 완료*로 표시하지 않음 |

이 기록의 1건 제거는 1,272건 중 1건이며, 1,269건의 사실 확인이 아직 남아 있다. 나머지 2건도 표준의 공개 범위와 기존 조건을 확인한 사례이지 완전한 규격 본문 검토를 뜻하지 않는다. 작업 전 보고서의 `1,272` 집계와 Registry 해시는 역사적 스냅샷으로 남기며 현행 Registry에는 그대로 적용하지 않는다.

현행 Registry(`6cb08f35cdf9a9a80a11ffa2d6252ab43769deb21c7667586bbf537ec708d0d5`)로 다시 만든 [잔여 Queue](remaining_fact_current_queue_20261030.csv)와 [계약 감사](remaining_fact_current_contract_audit_20261030.csv)는 첫 배치 20건을 뺀 1,271건을 포함한다. 계약 형식은 727건 PASS, 544건 SCOPE_REVIEW, 누락 Anchor 0건이다. 이 숫자는 **기술적 사실 승인 수치가 아니다.**

## 오탐 대조

- `sil_target_pfd_relation`: 모델이 PFDavg에 시간 역수 차원이 있다고 주장했으나, IEC 61508-1 공개 미리보기는 저수요 모드의 평균 요구고장**확률**과 고수요·연속 모드의 시간당 위험고장**빈도**를 분리한다. 따라서 차원 지적은 삭제 근거가 아니다. 출처: https://webstore.iec.ch/en/iec_catalog/product/preview/?id=L3B1Yi9wZGYvcHJldmlldy9pbmZvX2llYzYxNTA4LTF7ZWQyLjB9Yi5wZGY
- `control_valve_required_cv_inverse_sqrt_pressure_drop`: 모델은 난류 등 적용 조건이 없다고 보았으나 Registry의 조건 필드에 단상·비기화 액체와 기본 난류 크기 선정식이 있다. IEC 60534-2-1은 비압축성 유체의 식과 비난류 보정을 구별한다. 무조건적인 역제곱근 법칙으로 확대하지 않는다. 출처: https://webstore.iec.ch/en/publication/2461

## 운영 경계

제거한 항목은 저장소 내부의 Topic 소유 규칙이지 업계 기술 사실이 아니다. Registry Fact의 `score_effect`는 `none`이었지만 Pack의 `must` Anchor·모범답안·major Logic에 들어 있어 오히려 수험생 답안 평가에 섞일 수 있었다. 소스와 generated를 정식 CLI로 함께 갱신하고 회귀 검증한다. 다른 1,269건은 일반원리 후보라는 이유만으로 일괄 승인하거나, 제조사 출처라는 이유만으로 일괄 삭제하지 않는다.
