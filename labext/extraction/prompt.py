"""The materials-OER extraction prompt. The model reads and types; it never judges.

PROMPT_VERSION enters the cache key, so changing the prompt invalidates cached runs.
"""

PROMPT_VERSION = "materials-oer-extract-v0"

SYSTEM_PROMPT = """You extract scientific claims from a materials electrochemistry
paper into typed JSON. You read and type. You never judge, compare, or editorialise.

Rules:
- Extract ONLY primary statements the paper makes about its OWN results. Exclude any
  claim the paper makes about another paper's results (primary statements only).
- Extract from text and tables. Most conditions live in tables; a table row inherits
  conditions stated in its headers or caption. Figures are out of scope in v1.
- Copy the exact source sentence verbatim into source_sentence. For a table, use the
  caption or header sentence plus a table locator.
- NEVER infer an unstated condition. Do not derive pH from electrolyte. Do not turn an
  absent "room temperature" into a number. If a condition is not stated, write the
  string "unstated". If the paper states "room temperature", use "room_temperature".
- For a performance or stability number, fill the quantity block and the ten-key
  conditions block. Report the value exactly as stated, with its unit and any stated
  uncertainty. A range like "0.3 to 0.7" uses bound=approx, value=midpoint,
  uncertainty_kind=stated_range, uncertainty=half-width. "~" or "approximately" uses
  bound=approx.
- Output a JSON array of claim cards conforming to the claim card v2 schema. No prose.
"""

# Golden few-shots are appended at call time from this list.
FEWSHOT = [
    {
        "role": "user",
        "content": "Passage: The IrO2 catalyst exhibited an overpotential of 320 mV at "
        "10 mA/cm2 in 0.5 M H2SO4 at room temperature, with iR correction applied.",
    },
    {
        "role": "assistant",
        "content": '[{"claim_id":"EX1","claim_kind":"performance_value",'
        '"commitment_direction":"asserts","causal_direction":"independent",'
        '"physical_scale":"molecular","measurability":"measurable_now",'
        '"measurable_with":"cp_chronopotentiometry","subject":"IrO2",'
        '"relation":"has_overpotential","object":"overpotential","domain":"materials_oer",'
        '"source_sentence":"The IrO2 catalyst exhibited an overpotential of 320 mV at '
        '10 mA/cm2 in 0.5 M H2SO4 at room temperature, with iR correction applied.",'
        '"source_document":"example","provenance_hash":"ex1",'
        '"axis":"overpotential_at_current_density",'
        '"quantity":{"value":320,"unit":"mV","uncertainty":null,'
        '"uncertainty_kind":"none_stated","bound":"exact"},'
        '"conditions":{"electrolyte":{"identity":"H2SO4","concentration":{"value":0.5,'
        '"unit":"mol/L"}},"ph":"unstated","current_density":{"value":10,"unit":"mA/cm^2",'
        '"normalization":"geometric"},"temperature":"room_temperature","loading":"unstated",'
        '"substrate":"unstated","protocol_tier":"unstated","prior_operation_duration":'
        '"unstated","anneal_temperature":"unstated","ir_correction":true}}]',
    },
]
