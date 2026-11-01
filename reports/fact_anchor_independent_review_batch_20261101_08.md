# Independent technical fact review batch 08 — Routh-Hurwitz stability

Review: 2026-11-01. Prior independently reviewed: 143; added 7; cumulative 150/1,290; unreviewed 1,140. New verdicts: KEEP_BOUNDED 6; REVISE_REQUIRED 1. One substantive mathematical over-generalization was found; its underlying correct portion is retained as proposed replacement, not silently promoted.

Authoritative original primary teaching sources:
- Xu Chen, University of Washington, Lecture 10: Stability Analysis: the Routh-Hurwitz Approach, web updated 2026-10-23, https://faculty.washington.edu/chx/teaching/fbintro/lec10-routh-hurwitz-stability/ (sections Quick checks, Constructing the Routh array, Special cases 1 and 2, Summary).
- Åström & Murray, Feedback Systems 2nd Ed., Caltech-hosted manuscript, Ch. 6, Proposition 6.3, https://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-linsys_06Oct18.pdf. The theorem states that Lyapunov stability for zero-real-part eigenvalues requires scalar Jordan blocks. Text extraction viewed; the web PDF page-image screenshot timed out, so record the visual-access limitation explicitly.

### 1. routh_asymptotic_stability_open_lhp — KEEP_BOUNDED
- Original: 연속시간 선형시불변 폐루프 시스템의 점근안정 조건은 특성방정식의 모든 근이 열린 좌반평면에 존재하는 것이다.
- Source section: UW Natural response; Quick checks
- Independent comparison: For finite-dimensional autonomous continuous-time LTI dynamics, all poles strictly LHP yield asymptotic/exponential decay.
- Original conditions: finite_dimensional_lti_model

### 2. routh_first_column_sign_changes_rhp_count — KEEP_BOUNDED
- Original: 정규 Routh 배열에서 첫 열의 부호 변화 횟수는 중복도를 포함한 특성다항식의 우반평면 근 개수와 같다. 허수축 근 특수 경우는 별도로 판정해야 한다.
- Source section: UW Constructing the Routh array; zero row cases
- Independent comparison: First-column sign changes count RHP roots, subject to explicit exceptional-pivot and imaginary-axis handling.
- Original conditions: imaginary_axis_special_cases_handled

### 3. routh_positive_coefficients_not_sufficient — KEEP_BOUNDED
- Original: 실계수 특성다항식을 양의 최고차항으로 정규화하면 모든 계수가 양수인 것은 안정의 필요조건이지만 3차 이상에서는 일반적으로 충분조건이 아니다.
- Source section: UW Quick checks; positive coefficient counterexample
- Independent comparison: Positive coefficients are necessary for strict Hurwitz stability after positive-leading-coefficient normalization, not sufficient at cubic order and higher.
- Original conditions: positive_leading_coefficient_normalized

### 4. routh_zero_first_column_epsilon_limit — KEEP_BOUNDED
- Original: 행의 첫 원소만 0이고 행 전체가 0이 아니면 첫 원소를 ε>0으로 두고 배열을 계산한 뒤 ε→0⁺ 극한의 첫 열 부호변화를 판정한다.
- Source section: UW Special case 1
- Independent comparison: A zero first entry with other nonzero row entries uses ε>0 and positive-side sign limit.
- Original conditions: row_not_entirely_zero

### 5. routh_all_zero_row_auxiliary_polynomial — KEEP_BOUNDED
- Original: Routh 배열의 한 행 전체가 0이면 바로 위 행으로 보조다항식 A(s)를 만들고 dA(s)/ds의 계수를 0행에 대입해 배열 계산을 계속한다.
- Source section: UW Special case 2
- Independent comparison: Whole zero row means make A(s) from immediately preceding row and replace the zero row by dA(s)/ds coefficients.
- Original conditions: auxiliary_polynomial_formed_from_row_above

### 6. routh_imaginary_axis_roots_stability_class — REVISE_REQUIRED
- Original: 우반평면 근이 없고 허수축 근이 단순근이면 비점근 임계안정 가능성을 검토할 수 있으나, 허수축 중복근은 선형 자율계의 안정성을 깨뜨린다.
- Source section: UW Special case 2; Caltech Feedback Systems Ch.6 Proposition 6.3
- Independent comparison: Original blanket assertion that every repeated imaginary-axis root makes every linear autonomous system unstable is false for diagonalizable repeated imaginary-axis eigenvalues. Stability depends on the Jordan block structure, not simply algebraic multiplicity.
- Original conditions: all_other_roots_in_open_left_half_plane
- Proposed scientifically corrected statement (NOT applied to canonical Registry/Topic Pack): If all eigenvalues have nonpositive real part, a linear autonomous state-space system is Lyapunov stable exactly when each imaginary-axis eigenvalue is semisimple (all Jordan blocks of size 1). Repeated semisimple imaginary-axis eigenvalues can remain stable but are not asymptotically stable; nontrivial Jordan blocks at zero-real-part eigenvalues give instability.

### 7. routh_does_not_return_exact_pole_locations — KEEP_BOUNDED
- Original: Routh 배열은 특성다항식의 우반평면 근 개수와 안정 조건을 판정하지만 일반적으로 근의 정확한 위치, 감쇠비 또는 안정여유를 직접 산출하지 않는다.
- Source section: UW Why avoid computing every pole; Constructing the Routh array
- Independent comparison: Routh determines RHP counts and gain-range inequalities but does not directly calculate all pole coordinates or damping ratios.
- Original conditions: standard_routh_analysis


## Release and safety boundaries
- Keep existing 276 noncore/scoped/duplicate/generalization reference exclusions.
- Add the one source-reviewed correction requirement to separate scoring-hold overlay, bringing the total to 43, pending corrected Fact and regression validation.
- No claim that existing Registry or Master Packs have been updated or that tests and release gate passed. Historic verification_status=verified does not supersede this source-review status.
- Still source-unreviewed after this batch: 1,140 Fact IDs.
