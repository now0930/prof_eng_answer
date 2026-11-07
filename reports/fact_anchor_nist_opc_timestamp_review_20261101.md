# Source verification: recalibration and timestamps (2026-11-01)

## eem_recalibration_interval_risk_history_and_cost_basis
Verdict: KEEP_BOUNDED. Primary source: NIST, *Recommended Calibration Interval*: https://www.nist.gov/calibrations/recommended-calibration-interval . NIST does not prescribe a universal fixed interval. Requirements, instrument stability, environmental conditions and longitudinal as-found/as-left results are pertinent. **Caution:** economic cost optimization is not directly established in this cited NIST text, so it must not be scored as a universal technical fact or mandatory part of the claim.

## historian_source_event_ingestion_processing_timestamps_distinguished
Verdict: KEEP_BOUNDED. Primary sources: OPC UA Part 4 §§7.11.3-7.11.4 https://reference.opcfoundation.org/specs/OPC-10000-4/7 and OPC UA Part 11 §4.5 https://reference.opcfoundation.org/specs/OPC-10000-11/4.5 . SourceTimestamp originates at the data source; ServerTimestamp reflects when the server received/knew the value. Downstream ingestion or processing time is a separate application-defined timestamp, **not** an additional mandatory OPC UA DataValue field. Not all historians retain both OPC timestamps.

## Inspection limits
Primary official HTML text checked against named facts only. Full Topic Pack paragraphs and any implementation-specific mappings remain unverified. Conditional verdicts do not authorize broad grading assertions.
