"""Phase 2: dual-model extraction, agreement gate, review queue, pilot.

The language model reads and types claims into the Part IV schema; it never judges.
Two independent model runs are diffed. A pair that is field-exact after
canonicalisation is AGREED-PROVISIONAL; everything else goes to the review queue as
one markdown file per contested claim for Anu to approve or reject. All model outputs
are cached to disk (jsonl) so reruns are free and resumable (D3).

API keys come from environment variables only (D14). No .env file is ever read
(Anu standing ruling). If no key is present, the non-API parts still run and the
block is logged.
"""
