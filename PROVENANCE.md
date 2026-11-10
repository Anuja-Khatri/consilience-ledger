# PROVENANCE

Every vendored file is a COPY from a pinned source (spec II.2). Lila manuscript
data is never committed; it is loaded at runtime (CC-28, Anu ruling OQ-3).

## Upstream sources and pins (recorded at vendor time)
| Repo | Pin (sha) | How obtained | License |
|---|---|---|---|
| theconsilience-engine | 71f60a25a198762d6cac932b5a34d0a1fe555815 | local checkout ~/theconsilience-engine (verified) | Apache-2.0 (Anu's own; copying unrestricted) |
| lab-gate | 3e0185a60d60ceae01cb4d116c9b43c6ac71d085 | cloned from github.com/Anuja-Khatri/lab-gate into ../upstream/lab-gate, checked out 3e0185a | MIT (Anu's own) |
| consilience-verification | 275dba8d8a123eb6588d7e3ebd9a439313e6ab8c | local checkout, frozen (Phase 7) | MIT |
| helao-async | ba910c4c2bdcbcbc49476e32a5b20ca0abb93529 | local ~/lila-gate/helao-async (Phase 10) | MIT |
| lila_oer_manuscript | 92a773790b684786cb8956e3c2cac668043850cb | cloned into ../upstream/lila_oer_manuscript (Phase 5) | code MIT; data CC-BY-4.0. DATA NOT COMMITTED. |

## Vendored files (vendor/)
| Vendored path | Source repo @ pin | Source path | Modified? |
|---|---|---|---|
| vendor/engine/judge/** | theconsilience-engine @ 71f60a2 | judge/** | matching/vf2_typed.py ONLY: added `conditions_compatible` (lab-extension addition, clearly marked). All other files unchanged (grading/four_rung_ladder.py, equivocation/lexical_ablation.py, testability/capability_map_lookup.py, hash/determinism_check.py, schema/*.json). |
| vendor/labgate/units.py | lab-gate @ 3e0185a | gate/boundary/units.py | unchanged |
| vendor/labgate/sim_ext/oersim.py | lab-gate @ 3e0185a | sim_ext/oersim.py | ONE line changed: `from sim_ext.accounting` -> `from .accounting` (vendored package path). Runs the real OERSIM on Lila's real oer13_cps dataset with pyzstd + the pure-Python calc_eta fallback (no helao/numpy needed). |
| vendor/labgate/sim_ext/accounting.py | lab-gate @ 3e0185a | sim_ext/accounting.py | unchanged |

Derived work in this repo (labext/, schema/, rules/, domainpack/, tests/) is
original and licensed MIT (D2). The demo repos consilience-demo and miu-demo are
Anu's own code with no LICENSE file; any port from them is authorized by spec III.3
and relicensed MIT (Anu ruling OQ-4).
