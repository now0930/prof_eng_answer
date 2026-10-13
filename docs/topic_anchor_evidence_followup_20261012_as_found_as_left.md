# As-found / as-left leakage Anchor 근거 재검토 (2026-10-12)

## 최초 검토 결과와 후속 정정

최초 검토 시 `as_found_as_left_leakage`의 보편적 동일조건 기록 문구는 **미검증**으로 판단했다.
이후 2026-10-12 근거 검토에서 해당 문구를 삭제하고, Emerson Lifecycle Services의 특정 repair-report 사례가
as-found/as-left 진단 상태와 정비 후 seat-leakage 시험 basis를 구분해 기록한 사실로 좁혔다.
현재 Anchor는 조건이 다른 결과를 직접 비교해 repair 효과를 단정할 수 없다고만 말하며, 모든 수리기록에 대한 보편 의무를 주장하지 않는다.

## 확인 근거와 한계

- FCI, *ANSI/FCI 70-2 Informational Sheet*: seat-tightness class는 defined test conditions의
  maximum allowable leakage benchmark라고 설명하며, 표준의 defined test procedure가 서로 다른
  valve offerings를 비교하도록 한다. 이는 시험 결과를 비교할 때 기준 조건이 중요하다는 점을
  뒷받침하지만, repair 전·후 비교 기록의 의무 또는 열거된 조건 전부를 동일하게 유지하라는
  요구사항을 직접 규정하지 않는다.
- FCI 공식 표준 목록은 ANSI/FCI 70-2:2021을 안내한다. 상세한 시험 매개변수는 적용 계약과 실제
  표준판을 확인해야 하며, 정보 시트만으로 시험 세부 조항을 추정하지 않는다.

## 최초 판정의 적용 범위

동일 조건 비교는 repair 효과를 해석하기 위한 합리적인 실무 원칙일 수 있지만, 현재 확보한
공식 근거만으로 이를 보편적 기록 의무로 확정하지 않는다. 문구를 유지하려면 applicable
maintenance/test procedure가 as-found/as-left 기록과 matching conditions를 요구하는지 확인해야
한다. 그렇지 않으면 “비교 목적이면 가능한 한 동일한 agreed test conditions로 측정하고, 조건이
달라지면 각 실제 조건을 함께 기록한다”처럼 조건부 문구로 수정하는 것이 적절하다.

위의 최초 판정은 예전의 보편적 기록 의무 문구에 대한 것이다. 이후 좁힌 사례 기반 Anchor는
`grading/evidence/approved_fact_registry.json`의
`valve_repair_report_example_separates_as_found_and_as_left_test_data`로 추적하며, score effect는 none이다.
따라서 회귀 테스트도 해당 사례와 한계만 검사하고, 동일조건 기록을 보편 의무로 요구하지 않는다.
