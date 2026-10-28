# Astra review: vibratory gyroscope

- Decision: APPROVE after corrections.
- Reviewer: Astra (`gpt-6-astra`), AI review; not human review.
- Authorization: user explicitly delegated content review and approval to Astra on 2026-10-28.
- Topic: `vibratory_gyroscope_coriolis_angular_rate_sensing`.
- Reviewed: README, four source JSON files, Topic Sheet and Master source reference.

## Evidence

WordPress post 8253, “코리올리 힘, 가속도”, public HTML modified 2026-10-28T12:38:29Z, section 1. Source URL and HTML SHA-256 are recorded in the Topic Sheet and Master. Astra fetched and read the HTML and independently compared the [Analog Devices technical explanation](https://www.analog.com/en/resources/analog-dialogue/articles/imems-angular-rate-sensing-gyroscope.html).

## Findings resolved

1. Sinusoidal drive has time-varying velocity v(t). The force relation is instantaneous; inversion requires nonzero speed. Constant drive amplitude/frequency establishes velocity amplitude, not constant instantaneous velocity. Corrected Anchor 03, outline and review notes.
2. RPM and rad/s are convertible angular-rate units. Topic separation is by sensing mechanism and problem scope. Removed RPM-only error interpretation.
3. The source does not establish a universal left/right rotation convention. Retained magnitude relationships and explicit coordinate/force definitions; no automatic sign-based fatal rule.

## Boundaries and residual limits

Three representative questions cover acceleration, drive/sense-axis response and angular-rate conversion. Coriolis mass flow and encoder shaft sensing retain their existing owners. HTML/PDF/image originals were not modified. The Master source remains unverified raw material; source-level approval does not fabricate independent Fact Registry verification. Automatic wrong-pattern checks remain disabled until independently tested. Runtime inclusion follows source hash and release gates.
