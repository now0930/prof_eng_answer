# 선별 40건 보완 진행 기록 (2026-10-29)

이 문서는 `selected_fact_recheck_results_20261029.md`의 40건(문구·조건 6, 근거·연결 14, 내부 계약 2, 보류 18)에 대한 **적용 진행 기록**이다. 원 감사표의 판정을 소급해서 VERIFIED로 바꾸지 않는다. 특히 공개 원문이 접근 불가하거나 공개 표준 요약만으로 세부 주장을 증명할 수 없는 Fact는 운영 승인 근거가 아니다.

## 적용한 변경

- 문구·조건 6건: 과감쇠 응답의 비교 범위, 2차계 유한 공진 조건, 반전력점과 관용적 −3 dB, 적분 상태추적 입력 차원, 경보 shelving, 경보 rationalization의 보편 단정을 한정했다. 관련 Topic Pack 표현도 동기화했다.
- 내부 계약 2건: 기술 사실 Registry에서 제외하고 `docs/internal_topic_ownership_contracts.md`에 보존했다.
- 근거·연결: 독립 소음원 3건의 산술 유도를 명시하고 ISO 3747이 직접 증명하지 않는 내용을 인용하지 않도록 했다. 2층 계면 차압 유도의 상부 탭 압력 오류, NASA RUL 논문 제목, Rockwell 경보 매뉴얼 문서번호·URL·쪽수, ISA 계장선/루프 번호 자료의 깨진 URL을 수정했다. FAT/SAT 및 ISO 15848 형식시험 문구를 공개 근거가 지지하는 범위로 한정했다.
- 보류 중 일부: 위험장소 검사·정비 기록의 보편 체크리스트 주장을 적용 설비·보호방식·현장 절차에 따른 조건부 내용으로 좁혔다.
- 추가 원문 대조: Fluke 725Ex의 source/simulate, ISA/PAS 경보철학, NASA 질량유량 식, Cisco PTP clock/BMCA/holdover, IEEE TSN, IEC 온도·EMC 시험 범위, FHWA 와전류 탐침, SAP 생산계획 자료를 각각 해당 Fact의 조건에 맞춰 연결하거나 문구를 한정했다. 공개 원문 범위를 넘어서는 보편적 단정은 제거했다.
- 역사적 HOLD 표의 CSV 행 번호와 Fact ID가 어긋난 17건을 바로잡고, 검증 스크립트가 행 번호·ID의 일치를 확인하도록 했다. 기존 triage 원본의 판정은 변경하지 않았다.

## 2026-10-30 일반 원리 기준 후속 판정

- 과거 HOLD 18건은 `fact_recheck_general_principle_resolution_20261030.md`에서 현재 문장 기준으로 재판정했다. 17건은 일반 공학 원리와 적용조건 수준에서 확인했고, 특정 Emerson 수리보고서 1건은 승인 Fact에서 제거해 업계의 시험조건 비교 원칙으로 대체했다. 상세 표준 조항·회사별 양식·일률적 기록 의무를 승인했다는 의미가 아니다.
- `liquid_in_glass_thermometer_calibration_is_immersion_condition_specific`는 별도 P0 lineage 문제로, 이 18건의 HOLD에는 속하지 않는다. 무리하게 thermocouple/RTD Anchor에 연결하지 않고 독립·비채점 사실로 유지한다.

## 검증 상태

- `pytest -q tests/test_approved_fact_registry.py scripts/test_triage_approved_fact_recheck.py -x`: 396 PASS.
- `python3 -B scripts/rubric_manager.py validate-all`: PASS.
- `python3 -B scripts/rubric_manager.py validate-topic-pack-release --all --promote-generated`: PASS. 생성물은 공식 명령으로 갱신했다.
- `PROMOTE_GENERATED=0 scripts/validate_release.sh`: PASS (2026-10-30). 진행 중 FAT/SAT와 온도시험의 변경된 조건부 문구를 옛 키워드로 검사하던 회귀 2건을 계약에 맞게 수정하고 처음부터 재실행했다. 선택 실행형 10회 P0 재현성 게이트는 기본값에 따라 SKIP이며 PASS로 간주하지 않는다.
- 일반 원리 재판정 후 `python3 -B scripts/rubric_manager.py validate-topic-pack-release --all --promote-generated`: PASS. `python3 -B scripts/rubric_manager.py validate-all`: PASS. `PROMOTE_GENERATED=0 scripts/validate_release.sh`: PASS (2026-10-30, 최종 변경 기준). `scripts/test_triage_approved_fact_recheck.py` 6 PASS, 등록부 pytest 391 PASS, 밸브·산업망·생산관리 집중 회귀 PASS.

40건의 **처분 기준 및 source·generated 검증**은 완료했다. 이 문서의 완료는 일반 원리 수준의 사실 확인과 코드 회귀 통과를 뜻하며, 유료 표준의 모든 세부 조항이나 실제 설비의 적합성 인증을 뜻하지 않는다. 기존 사용자 수정인 `README.md`, `docs/operational_quality_checksheet.md`는 이 작업의 소유 범위에서 제외한다.
