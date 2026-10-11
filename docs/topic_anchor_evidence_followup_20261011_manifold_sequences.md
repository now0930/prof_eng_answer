# DP transmitter manifold sequence anchors: evidence disposition (2026-10-11)

Scope: the two unverified anchors in `dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation`:

- `manifold_isolation_sequence`
- `manifold_return_sequence`

## Disposition

Both anchors remain **unverified**. The cited learning material documents the listed H–equalize–L–bleed sequence and its reverse, but the Topic Pack currently states them as generic operating rules. Available evidence does not establish one universally applicable sequence for every three-valve manifold, transmitter model, process arrangement, or work task. Because this is a safety-relevant operation, neither anchor was added to the approved Fact registry and the already human-approved Topic Pack was not edited.

The ambiguity is material:

- The educational text *Lessons in Industrial Instrumentation*, Chapter 19, p. 816, describes a conventional three-valve manifold with a separate transmitter bleed fitting. It recommends closing the high-pressure block, opening the equalizer, closing the low-pressure block, and opening the bleed last; its return example closes the bleed, opens the low-pressure block, closes the equalizer, and opens the high-pressure block last. This establishes a documented teaching example, not that every manufacturer or approved site procedure prescribes that same sequence.
- Emerson/Rosemount's 3051 Reference Manual 00809-0100-4774, §3.6.4, pp. 72–77, gives a model- and task-specific three-/five-valve procedure for zero trim at static line pressure. For its three-valve procedure it first closes the low-side isolation, opens the equalizer, then after zeroing closes the equalizer and reopens the low-side isolation. This is not the same task as removal for maintenance and must not be treated as a direct contradiction; it demonstrates why the task and device procedure must be specified.
- Foxboro/S-Series IDP10S manual MI 020-602, §2, pp. 45–46, gives an out-of-operation procedure for its flow-piping/optional bypass arrangement: close downstream, close upstream, open bypass, then carefully vent residual pressure. This is a different arrangement and likewise is not a direct substitute for a conventional three-valve manifold procedure.
- Emerson/Rosemount's 2051 Reference Manual 00809-0100-4101, Table 2-7, describes a low-side-isolate/equalize sequence for zeroing the transmitter, and then closes the equalizing valve to return to measurement. This is a zeroing task and does not establish the isolation-for-maintenance sequence.
- Yokogawa EJ differential-pressure transmitter manual IM 01C25B01-01E describes installation/setup with both stop valves closed and equalizing open to prevent one-sided overload; it directs the reader to the model's startup procedure. This further supports using the applicable instrument manual rather than a generic sequence.
- A conventional three-valve manifold has H and L block valves plus one equalizing valve. Bleed/vent is an additional connection or a separate vent valve; it is not a fourth valve in the three-valve definition. Equipment configuration must therefore be stated before assigning a bleed step.

## Required treatment

Keep both current Topic Pack anchors unresolved pending a content approval. If later revised, identify the sequence explicitly as a particular documented example, separate the bleed fitting from the three manifold valves, and state that the installed OEM instructions, process hazard controls, and approved site procedure govern actual work. Do not score a candidate as wrong merely for following a different approved manufacturer/site sequence.

Sources checked:

- [Kuphaldt, *Lessons in Industrial Instrumentation*, Version 1.0, Chapter 19](https://www.ibiblio.org/kuphaldt/socratic/sinst/book/liii_1v0.pdf)
- [Emerson/Rosemount 3051 Reference Manual 00809-0100-4774](https://www.emerson.com/content/dam/emerson/en/measurement-instrumentation/technical/products/pressure/documents/dl-rmt-3051-pressure-transmitter-76002.pdf)
- [Foxboro IDP10S Manual MI 020-602](https://cth.ca/wp-content/uploads/2017/11/mi_020-602_h.pdf)
- [Emerson/Rosemount 2051 Reference Manual 00809-0100-4101](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/dl-rmt-00809-0100-4101.pdf)
- [Yokogawa EJ110B/EJ310B/EJ430B/EJX series manual IM 01C25B01-01E](https://www.mercon-automation.com/files/attachments/Instrukcja_Yokogawa_EJ_110_120_130_310_430_440_EN.pdf)
