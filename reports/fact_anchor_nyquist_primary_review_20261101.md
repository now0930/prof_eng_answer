# Independent source review — Nyquist 3-anchor batch (2026-11-01)

Branch: codex/essay-boundary-calibration-20261028
Review method: independent comparison against original educational/official documentation, with sign conventions and applicability stated explicitly. These results are bounded validations, not blanket certification of every wording in source Topic Packs.

| fact_id | verdict | evidence and constraints |
|---|---|---|
| argument_principle_pnz_relation | KEEP_BOUNDED | University of Michigan CTMS, Frequency Domain Methods (https://ctms.engin.umich.edu/CTMS/index.php?example=Introduction&section=ControlFrequency) explicitly gives Z=P+N when clockwise encirclements count positive; with counterclockwise-positive convention Z=P-N. Must specify sign convention, closed-loop characteristic equation 1+L(s)=0 and relevant Nyquist contour. |
| nyquist_minus_one_critical_point | KEEP_BOUNDED | MathWorks documentation, Nyquist response (https://www.mathworks.com/help/control/ref/dynamicsystem.nyquist.html) and Control System Toolbox reference (https://www.mathworks.com/help/releases/r2024b/pdf_doc/control/control_ref.pdf): -1+j0 is critical point for standard negative-feedback characteristic 1+L=0; does not carry over unchanged to arbitrary sign conventions. |
| stable_open_loop_special_case | KEEP_BOUNDED | University of Michigan CTMS (same source): when P=0, closed-loop asymptotic stability requires no net encirclement (N=0) and no imaginary-axis closed-loop poles; condition is a special case, not a general claim for open-loop unstable systems. |

Review caution: no source-document review of the complete Topic Pack phrasing or all linked citations was performed in this batch; stronger universal claims must be separately revised before granting grading authority.
