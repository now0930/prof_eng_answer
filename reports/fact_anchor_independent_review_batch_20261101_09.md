# Independent source review batch 09 — standard second-order resonance (2026-11-01)

## Scope and provenance
Exact target: `rubrics/topic_packs/second_order_system_resonance_frequency_response/fact_anchor.json`, existing branch `codex/essay-boundary-calibration-20261028`. Five anchors F1–F5 inspected. Source comparison is claim-scoped; **not** an approval or change of Registry `verification_status`, nor a release gate result. Cross-check previously reviewed IDs before incrementing a cumulative unique-ID coverage count.

Primary instructional sources:
- MIT Department of Mechanical Engineering, lecture *The Frequency Response of a Second-Order System*, section 1.3 (equations 3–4 and resonance peak): https://sites.mit.edu/meche2004/wp-content/uploads/2019/10/Lecture_All.pdf
- University of Washington, Xu Chen, *Lecture 7: From Step Response to System Parameters*: https://faculty.washington.edu/chx/teaching/fbintro/lec07-second-order-step-response/
- Engineering LibreTexts, *Frequency Response of Damped Second Order Systems*, equation 10.11 and surrounding scope: https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Signal_Processing_and_Modeling/Introduction_to_Linear_Time-Invariant_Dynamic_Systems_for_Students_of_Engineering_%28Hallauer%29/10%253A_Second_Order_Systems/10.02%253A_Frequency_Response_of_Damped_Second_Order_Systems
- MIT 18.03 *Frequency response*, section 16.3: https://math.mit.edu/classes/18.03/sup/sup16.pdf

## Exact anchor decisions
| Anchor | Claim summary | Review | Grounding and bounded scope |
|---|---|---|---|
| F1 | `G(s)=Kωn²/(s²+2ζωn s+ωn²)`, `s=jω` | KEEP_BOUNDED | MIT lecture sec. 1.3, standard unity-DC-gain two-pole **zero-free** LTI low-pass form; with arbitrary scalar K it is DC gain K. Not a generic expression for all second-order plants with zeros or delay. |
| F2 | `|G(jω)|/K=1/sqrt((1-r²)²+(2ζr)²)` | KEEP_BOUNDED with wording fix | MIT sec. 1.3 equation 3. In full generality use `|G(jω)|/|K|` for nonzero real K; current `/K` silently presumes K>0. Recommend explicitly `K>0` or normalize by `|K|`. |
| F3 | Finite positive-frequency resonance `ωr=ωn√(1−2ζ²)` for `0<ζ<1/√2` | KEEP_BOUNDED | MIT sec. 1.3, LibreTexts Eq. 10.11. For ζ=0 ideal unbounded pole response; at ζ=1/√2 maximum moves to DC, not a positive-frequency resonant peak. Applicable only to the canonical all-pole low-pass form. |
| F4 | Distinguish transient damped oscillation `ωd` and forced-response peak `ωr`; overshoot range wider than resonance | KEEP_BOUNDED | UW Lecture 7 for ωd, peak/overshoot; MIT sec. 1.3 for ωr. Overshoot statement assumes standard unit-step zero-free second-order system, positive gain and usual initial conditions. Not universal for systems with zeros, feedforward or delay. |
| F5 | Resonance necessarily connected with vibration/noise amplification, control-loop instability, and equipment damage risk | REVISE_SCOPE | MIT sec. 1.3 establishes frequency-selective amplification and potential unwanted mechanical vibration, but does **not** establish that a resonant peak implies closed-loop instability, noise amplification in every context, or actual damage. Reword: resonance *can* amplify disturbances near its peak; depending on loop structure, excitation and mechanical limits, it may degrade performance or create design risks. Evaluate closed-loop stability separately by poles/margins. Do not use categorical harm as a required general grading fact. |

## Safety and release boundary
- No source Topic Pack, Registry, generated rubric, or scoring code mutated.
- Propose F2 gain-sign qualification and F5 scope-limited revision only; no silent canonical approval.
- This batch is five **claim comparisons**, not asserted five **previously unreviewed** unique Queue IDs. Prior batch-08 coverage remains 150/1290 independently reviewed until deduplicated against the original ledger.
- No pytest or validate_release execution, no claims of passing gates. Preserve working-tree changes on other checkouts.