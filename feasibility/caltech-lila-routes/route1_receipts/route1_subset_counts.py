#!/usr/bin/env python3
"""Route 1 (d): CP4 @ +100 uA subset counts - independent reproduction.

Inputs:
  - pairs_t05.csv         (from route1_match.py)
  - db_h2so4_1M.csv       (the MPS export; sample_id -> comp)
  - cp4_100ua_ids.txt     distinct matched sample ids with a CP4 row at
                          current_abs = +0.0001 A (= +100 uA), produced by:
      psql -d mps --csv -c "select distinct f.sample_id from r0survey.acid_cp_fom f
        join r0survey.acid_sp a on a.sample_id=f.sample_id and a.technique=f.technique
        join public_release.process pr on pr.id=a.proc_id
        join public_release.process_detail pd on pd.id=pr.process_detail_id
        where f.eta_v_ave is not null and f.electrolyte='H2SO4(aq)'
          and jsonb_typeof(f.comp)='object' and (pd.parameters::jsonb->>'concentration')='1'
          and f.technique='CP4' and (pd.parameters::jsonb->>'current_abs')='0.0001'
          and f.sample_id::text in (<the 1881 matched ids>)" > cp4_100ua_ids.txt

Usage: python3 route1_subset_counts.py PAIRS_CSV DB_EXPORT_CSV CP4_IDS_TXT LILA_CSV
"""
import csv, json, ast, sys

PAIRS, DB, CP4, LILA = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

cp4 = {x.strip() for x in open(CP4) if x.strip()}
pairs = list(csv.reader(open(PAIRS)))[1:]
dbcomp = {r["sample_id"]: r["comp"] for r in csv.DictReader(open(DB))}
lcomp = {}
with open(LILA) as f:
    for i, r in enumerate(csv.DictReader(f)):
        lcomp[str(i)] = r["composition"]

def nkey(cstr, raw):
    d = ast.literal_eval(cstr) if raw else json.loads(cstr)
    nz = {k: float(v) for k, v in d.items() if float(v) > 0}
    s = sum(nz.values())
    return tuple(sorted((k, round(v / s, 6)) for k, v in nz.items()))

inv = [p for p in pairs if p[2] in cp4]                       # pairs whose DB sample is CP4@+100uA
db_samples = {p[2] for p in inv}
lila_rows = {p[0] for p in inv}

print("CP4 @ +100 uA matched samples:", len(cp4))
print("pairs involving >=1 such sample:", len(inv))
print("distinct matched (Lila) compositions:",
      len({nkey(lcomp[r], True) for r in lila_rows}))
# For reference only (not the headline figure):
print("  [ref] distinct DB-side compositions:",
      len({nkey(dbcomp[s], False) for s in db_samples}))
print("  [ref] distinct element systems:",
      len({frozenset(k for k, v in json.loads(dbcomp[s]).items() if float(v) > 0) for s in db_samples}))
