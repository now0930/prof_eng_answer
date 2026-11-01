# Independent engineering fact source review batch 07 — Root locus

Review date: 2026-11-01. Claim-specific source: Xu Chen (University of Washington), Lecture 13, The Root Locus Technique (web revision September 28, 2026), https://faculty.washington.edu/chx/teaching/fbintro/lec13-root-locus-technique/. Inspected sections Defining the root locus, Sketching rules, Refining the sketch, Imaginary-axis crossings and Summary. Original claims were compared separately, not merely assigned a source by similarity.

Previously independently reviewed: 135 / 1,290; new source-checked: 8; cumulative 143 / 1,290; unreviewed: 1,147. Outcomes: 8 KEEP_BOUNDED, 0 REVISE, 0 REJECT. K is assumed real positive, loop scalar LTI, and standard negative feedback; these rules cannot be generalized without these mathematical assumptions.

### 1. `root_locus_closed_loop_pole_gain_relationship` — KEEP_BOUNDED
- Statement: 표준 단위 음의 피드백에서 개루프 KG(s)H(s)의 근궤적은 폐루프 특성방정식 1+KG(s)H(s)=0의 근이 이득 K에 따라 이동하는 궤적이다.
- Primary pedagogical derivation: § Defining the root locus; 1+KGH=0, https://faculty.washington.edu/chx/teaching/fbintro/lec13-root-locus-technique/
- Independent comparison: Course text explicitly defines roots of closed-loop characteristic equation as K varies in positive-real-gain standard negative feedback.
- Applicability: scalar_lti_loop; positive_real_gain_parameter

### 2. `root_locus_definition` — KEEP_BOUNDED
- Statement: 표준 양의 이득 근궤적은 K가 0에서 무한대로 변할 때 폐루프 극점이 s-평면에 그리는 궤적이다.
- Primary pedagogical derivation: § Defining the root locus; § Summary, https://faculty.washington.edu/chx/teaching/fbintro/lec13-root-locus-technique/
- Independent comparison: Defines the positive-gain root locus as the full set of closed-loop poles while K moves from zero toward infinity.
- Applicability: standard_scalar_feedback_loop

### 3. `root_locus_start_end_points` — KEEP_BOUNDED
- Statement: 표준 proper 전달함수의 n개 근궤적 가지는 개루프 극점에서 시작해 m개의 유한 개루프 영점과 n−m개의 영점(무한대)으로 끝난다.
- Primary pedagogical derivation: § Sketching rules, Starting and ending points, https://faculty.washington.edu/chx/teaching/fbintro/lec13-root-locus-technique/
- Independent comparison: Shows n branches starting at n open-loop poles and ending at m finite zeros plus n-m zeros at infinity, n>=m.
- Applicability: n_greater_or_equal_m; multiplicity_counted

### 4. `root_locus_real_axis_segment_rule` — KEEP_BOUNDED
- Statement: 표준 양의 이득 실수계 근궤적에서 실수축의 한 점 오른쪽에 있는 실수 개루프 극점과 영점 수가 홀수인 구간이 실수축 근궤적이다.
- Primary pedagogical derivation: § Sketching rules, Real-axis segments; § Summary, https://faculty.washington.edu/chx/teaching/fbintro/lec13-root-locus-technique/
- Independent comparison: Explicit count of real zeros and poles on a point's right as odd for standard real-coefficient positive-gain root locus.
- Applicability: real_coefficients; positive_gain

### 5. `root_locus_breakaway_breakin_points` — KEEP_BOUNDED
- Statement: 실수축 이탈·진입점 후보는 K(s)=−1/[G(s)H(s)]에서 dK/ds=0인 점으로 구하며, 실제 근궤적 구간과 중복근 조건을 확인해 유효성을 판정한다.
- Primary pedagogical derivation: § Refining the sketch; § Summary, https://faculty.washington.edu/chx/teaching/fbintro/lec13-root-locus-technique/
- Independent comparison: Determines candidates by dK/dsigma=0, with only actual locus points and common-root conditions counting.
- Applicability: candidate_on_real_axis; characteristic_equation_satisfied

### 6. `root_locus_imaginary_axis_crossing` — KEEP_BOUNDED
- Statement: 근궤적의 허수축 교차점과 해당 임계 이득은 특성방정식에 s=jω를 대입하거나 Routh 배열의 경계조건으로 구한다.
- Primary pedagogical derivation: § Imaginary-axis crossings, https://faculty.washington.edu/chx/teaching/fbintro/lec13-root-locus-technique/
- Independent comparison: Explicitly applies s=jω to characteristic polynomial and Routh critical row for boundary gain.
- Applicability: real_gain_parameter; crossing_frequency_real_nonnegative

### 7. `root_locus_gain_from_magnitude_condition` — KEEP_BOUNDED
- Statement: 표준 양의 이득 근궤적의 설계점 s_d가 각도조건을 만족하면 이득은 K=1/|G(s_d)H(s_d)|로 계산한다.
- Primary pedagogical derivation: § Defining the root locus, Magnitude condition, https://faculty.washington.edu/chx/teaching/fbintro/lec13-root-locus-technique/
- Independent comparison: Explicit K = 1/|G(s)H(s)| after the phase condition; consistent positive K.
- Applicability: angle_condition_satisfied; positive_real_gain

### 8. `root_locus_angle_condition` — KEEP_BOUNDED
- Statement: 표준 음의 피드백에서 양의 이득 근궤적의 점은 ∠G(s)H(s)=(2q+1)180°의 홀수배 위상조건을 만족한다.
- Primary pedagogical derivation: § Defining the root locus, Angle condition, https://faculty.washington.edu/chx/teaching/fbintro/lec13-root-locus-technique/
- Independent comparison: Explicit odd multiple of 180° for negative feedback and K>0.
- Applicability: standard_negative_feedback; phase_unwrapped_consistently


Earlier 276 screened exclusions and 42 source-revision holds are unchanged. This review is neither a fresh check of 1,147 pending facts nor a proof of release validation. No scoring engine tests, generated view rebuild, or main integration were run. Status 'verified' in old Registry remains a historical field, not an independent verification claim for pending Queue.
