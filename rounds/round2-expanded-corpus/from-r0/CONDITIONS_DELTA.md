# Conditions-vector delta - PROPOSAL for Gate 1 (Anu freezes; Claude only proposes)

The v1 locked vector has exactly ten keys (lab-extension `labext/schema.py`):
electrolyte, ph, current_density, temperature, loading, substrate, protocol_tier,
prior_operation_duration, anneal_temperature, ir_correction. R0 proposes ONE change and
flags two keep-as-is decisions. Nothing here is applied; the vector freeze is Anu's
(locked plan item 3's letter).

## Proposed change D-1: refine `ir_correction` from boolean to a stated fraction
- v1 today: `ir_correction: Union[bool, "unstated"]` - records only corrected yes/no.
- Problem, sourced: B2 (PMC13707403, Molecules 2026, section 3) documents that for a single
  RuO2 electrode "the reported overpotential at 25 mA cm-2 slid continuously from 437 mV
  uncompensated down to 382 mV at full compensation, depending on which fraction the author
  chose," and that "the percentage of ohmic (iR) drop compensation applied to a polarization
  curve, a quantity often left unstated, has an outsized effect on the resulting
  overpotential." A boolean cannot distinguish 50%-compensated from 100%-compensated, yet
  that difference is ~55 mV on the same electrode - larger than the 13 mV floor and larger
  than the empirical ~22-51 mV MPS replicate floor.
- Proposal: replace the boolean with a stated fraction:
  `ir_correction: Union[IrCorrection, "unstated"]` where IrCorrection carries
  `fraction: float in [0,1]` (0 = uncompensated, 1 = full) OR an enum
  `{none, partial_stated, full, unstated}` if a number is not given. Default stays `unstated`.
  A claim that says "iR-corrected" without a fraction maps to `partial_stated` (or
  `fraction=unstated`), which is treated as a comparability DEFECT, not a silent equality.
- Why this is honest, not derived: the value must still come from a quoted Methods sentence
  on the card (methods-level attribution rule, strategy section 5); nothing is inferred.
- Independent support from the data: MPS, the richest structured source, has NO iR-compensation
  field at all (MPS_SURVEY.md section 4). The fraction is under-reported even in machine-stated
  data, so the ledger must model its absence explicitly rather than assume comparability.

## Keep-as-is K-1: `temperature` stays a key (do not drop)
B2's matched-basis requirement is "1 M KOH, room temperature" - temperature is part of the
match. MPS leaves temperature unstated (section 4), so most cards will carry
`temperature = unstated`; that is the correct, honest state and a comparability defect when
two cards differ or omit it. Keep the key; do not default it to room_temperature silently.

## Keep-as-is K-2: `current_density` stays; add a units note for the MPS adapter
MPS stores overpotential at a current THRESHOLD in amperes (I.A) plus a per-sample
`measurement_area`; literature states mA/cm2-geo. The key is unchanged, but the R1 MPS adapter
must convert area->mA/cm2-geo before blocking (OQ-R0-8). No vector change; an adapter task.

## Net proposed vector (if D-1 accepted): still ten keys
electrolyte, ph, current_density, temperature, loading, substrate, protocol_tier,
prior_operation_duration, anneal_temperature, **ir_correction (fraction-valued)**.
The key count and names are unchanged; only `ir_correction`'s value type is widened. This is
the minimal change that lets the ledger represent the single largest hidden variable B2
documents.
