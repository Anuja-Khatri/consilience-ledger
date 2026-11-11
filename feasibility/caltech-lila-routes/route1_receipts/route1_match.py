#!/usr/bin/env python3
"""Route 1 baseline match - independent reproduction.

Inputs (neither is committed as bytes into this repo; both are external reads):
  - Lila screening CSV (committed upstream clone):
        upstream/lila_oer_manuscript/data/oer_exp_data.csv
  - MPS H2SO4 1.0 M sample export produced by feasibility/sql/04_export_h2so4_1M_samples.sql
    run against the local read-only `mps` PostgreSQL database, e.g.:
        psql -d mps --csv -f feasibility/sql/04_export_h2so4_1M_samples.sql > db_h2so4_1M.csv

Composition match: identical element set, every element fraction within tol (t=0.05),
normalised to the nonzero cations (oxygen excluded on both sides). Mirrors
feasibility/analysis/match.py / match2.py.

Usage: python3 route1_match.py LILA_CSV DB_EXPORT_CSV OUT_DIR
Emits: pairs_t05.csv (one row per matched Lila-row/DB-sample pair) and
       matched_db_ids.txt (distinct matched DB sample ids).
Prints the baseline counts (expected: 1125 Lila rows, 69273 DB samples,
7115 pairs, 1881 distinct DB samples).
"""
import csv, json, ast, sys
from collections import defaultdict

LILA, DB, OUT = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("/")
TOL = 0.05

def norm(d):
    nz = {k: float(v) for k, v in d.items() if float(v) > 0.0}
    s = sum(nz.values())
    return {k: v / s for k, v in nz.items()} if s > 0 else None

lila = []
with open(LILA) as f:
    for i, r in enumerate(csv.DictReader(f)):
        n = norm(ast.literal_eval(r["composition"]))
        if n:
            lila.append({"i": i, "comp": n, "elset": frozenset(n), "anneal": r.get("anneal_T")})

db = []
with open(DB) as f:
    for r in csv.DictReader(f):
        n = norm(json.loads(r["comp"]))
        if n:
            db.append({"comp": n, "elset": frozenset(n), "label": r["sample_label"], "id": r["sample_id"]})

print(f"Lila rows (valid comp): {len(lila)}")
print(f"DB samples (H2SO4 1M, valid comp): {len(db)}")

db_by_set = defaultdict(list)
for d in db:
    db_by_set[d["elset"]].append(d)

def match(l, d, t):
    return all(abs(l["comp"][e] - d["comp"][e]) <= t for e in l["elset"])

pairs, dbids = [], set()
for l in lila:
    for d in db_by_set.get(l["elset"], []):
        if match(l, d, TOL):
            pairs.append((l["i"], l["anneal"], d["id"], d["label"], "-".join(sorted(l["elset"]))))
            dbids.add(d["id"])

print(f"pairs t={TOL}: {len(pairs)} | distinct DB samples: {len(dbids)}")
with open(f"{OUT}/pairs_t05.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lila_row", "lila_anneal", "db_sample_id", "db_label", "elsys"])
    w.writerows(pairs)
with open(f"{OUT}/matched_db_ids.txt", "w") as f:
    for x in sorted(dbids):
        f.write(x + "\n")
