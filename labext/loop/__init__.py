"""Stage 3 loop (Phases 10): a settleable fork compiles into an experiment card, the
card into a helao plan, the plan through the gate, executed on OERSIM, and the outcome
written back as a verdict. Plus the fork candidate table and the Human Review Dossier.

Card schema ported from miu-demo EXPERIMENT_SPEC.md, with two fixes: an explicit
``discriminating_power`` field (CC-27, not buried in prose) and an ``instrument_exists``
check against the OERSIM capability list before compilation (CC-25).
Every run artifact carries a SIM-NOT-CHEMISTRY disclaimer.
"""

SIM_NOT_CHEMISTRY = (
    "SIM-NOT-CHEMISTRY: OERSIM replays the public oer13_cps dataset shipped in helao-async "
    "(13 base metals, no palladium); not Lila's data. A simulated outcome is not a chemical "
    "measurement and licenses no chemical claim."
)
