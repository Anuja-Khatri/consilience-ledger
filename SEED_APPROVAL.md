# SEED_APPROVAL.md - safety seed, one row per rule for Anu to approve or reject

The PROPOSED seed is `safety_format/seed/registry_proposed.yaml`. It is **NOT activated** - the live
screen still loads `safety_format/seed/registry.yaml`. This file is for review only. Same rule ids,
kinds, predicates and bound VALUES as the active v0; only the SOURCES were made exact (or explicitly
labelled generic). Harmless public-standard EHS content only; the dual-use denylist scan passes on it.

Instrument protection limits are from Lila's published paper/SI **only where that paper states them**.
It states operating VALUES (anneals up to ~700 C; 10 mA/cm^2 screening), not protection ceilings, so
every instrument BOUND below is labelled **generic**, to be refined to the exact instrument spec if
provided.

| rule | what it checks | value | source basis | exact citation (proposed) | approve? / reject? / change value |
|---|---|---|---|---|---|
| **SB1** | anneal temp ceiling | ≤ 1100 C | generic (no Lila limit) | GENERIC muffle/box-furnace ceiling (standard ~1100–1200 C); Lila anneals reach ~700 C (arXiv:2609.30133) | ___ |
| **SB2** | current-density ceiling | ≤ 1000 mA/cm² | generic (no Lila limit) | GENERIC potentiostat compliance; Lila screens at 10 mA/cm² (arXiv:2609.30133) | ___ |
| **SB3** | acid volume per run | ≤ 500 mL | operating policy | Internal benign consumables cap (not a hazard limit); no external citation | ___ |
| **SC1** | oxidizer + organic solvent forbidden | combo | public reference | Prudent Practices in the Laboratory (NRC, Nat. Acad. Press, 2011), Ch. 6; OSHA 29 CFR 1910.1450 App. A | ___ |
| **SC2** | strong acid + strong base forbidden | combo | public reference | Prudent Practices in the Laboratory (NRC, 2011), Ch. 6; OSHA 29 CFR 1910.1450 | ___ |
| **SC3** | water-reactive + aqueous forbidden | combo | public reference | Prudent Practices in the Laboratory (NRC, 2011), Ch. 6 (water-reactive chemicals); OSHA 29 CFR 1910.1450 App. A | ___ |

Decision per row: **approve** (adopt as written), **reject**, or **change value** (write the number /
citation you want). On approval of all rows, `registry_proposed.yaml` replaces `registry.yaml` and the
version is bumped from `safety-seed-v0`; nothing is activated until you sign here.

Signed (Anu): ______________________  date: __________
