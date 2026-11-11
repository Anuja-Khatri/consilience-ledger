"""R0 B1 harvest census (research only, NOT pipeline code).

Runs the preregistered queries in r0/HARVEST_PREREG.md verbatim against the
official Europe PMC REST API and the arXiv export API, counting acidic-OER
records per active metal (Pd, Ru, Ir) with the open-access subset. Raw API
responses are cached under r0/harvest/raw/ so the counts are reproducible.

ChemRxiv's public API sits behind a Cloudflare JS bot-challenge that returns
403 to any non-browser client (curl and WebFetch both blocked on 2026-11-10);
its exact query is recorded for Anu in FOR_ANU.md rather than worked around.
"""
import json, os, time, urllib.parse, urllib.request, re

R0 = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(R0, "harvest", "raw")
os.makedirs(RAW, exist_ok=True)

UA = "consilience-ledger-r0/0.2 (research census; mailto:anujakhatri3009@gmail.com)"

# --- Preregistered Europe PMC query (HARVEST_PREREG.md, verbatim base) ---
EPMC_BASE = ('("oxygen evolution" OR OER) AND '
             '(acidic OR "sulfuric acid" OR "perchloric acid" OR "0.5 M H2SO4" OR "0.1 M HClO4") AND '
             '(overpotential OR "current density" OR stability) AND '
             '(palladium OR ruthenium OR iridium OR Pd OR Ru OR Ir)')
EPMC_METAL = {"Pd": "(palladium OR Pd)", "Ru": "(ruthenium OR Ru)", "Ir": "(iridium OR Ir)"}

# --- Preregistered arXiv query (HARVEST_PREREG.md, verbatim) ---
ARXIV_FULL = ('all:"oxygen evolution" AND all:acidic AND '
              '(all:palladium OR all:ruthenium OR all:iridium) AND '
              '(all:overpotential OR all:electrocatalyst)')
ARXIV_METAL = {"Pd": "palladium", "Ru": "ruthenium", "Ir": "iridium"}


def fetch(url, cache_name, retries=5):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                body = r.read()
            with open(os.path.join(RAW, cache_name), "wb") as f:
                f.write(body)
            return body
        except Exception as e:  # transient EBI 500/503, network hiccups
            last = e
            time.sleep(5 * (attempt + 1))
    raise last


def epmc_count(query, cache_name):
    url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="
           + urllib.parse.quote(query) + "&format=json&resultType=idlist&pageSize=1")
    return json.loads(fetch(url, cache_name)).get("hitCount")


def arxiv_count(query, cache_name):
    url = ("https://export.arxiv.org/api/query?search_query="
           + urllib.parse.quote(query) + "&max_results=1")
    raw = fetch(url, cache_name).decode("utf-8", "replace")
    m = re.search(r"<opensearch:totalResults[^>]*>(\d+)<", raw)
    return int(m.group(1)) if m else None


census = {"generated": "2026-11-10", "europe_pmc": {}, "arxiv": {},
          "chemrxiv": {"status": "BLOCKED: Cloudflare JS challenge (403) to all non-browser clients; see FOR_ANU.md"}}

# Europe PMC: base total + OA subset, and per-metal (total + OA)
census["europe_pmc"]["_base_all_metals"] = {
    "query": EPMC_BASE,
    "total": epmc_count(EPMC_BASE, "epmc_base_total.json"), }
time.sleep(1)
census["europe_pmc"]["_base_all_metals"]["open_access"] = epmc_count(
    EPMC_BASE + " AND (OPEN_ACCESS:y)", "epmc_base_oa.json")
time.sleep(1)
for metal, term in EPMC_METAL.items():
    q = f"{EPMC_BASE} AND {term}"
    total = epmc_count(q, f"epmc_{metal}_total.json"); time.sleep(1)
    oa = epmc_count(q + " AND (OPEN_ACCESS:y)", f"epmc_{metal}_oa.json"); time.sleep(1)
    census["europe_pmc"][metal] = {"total": total, "open_access": oa}

# arXiv: full prereg query + per-metal slices (all arXiv full text is OA)
census["arxiv"]["_full_query"] = {
    "query": ARXIV_FULL,
    "total": arxiv_count(ARXIV_FULL, "arxiv_full.xml")}
time.sleep(3)
for metal, mterm in ARXIV_METAL.items():
    q = f'all:"oxygen evolution" AND all:acidic AND all:{mterm} AND (all:overpotential OR all:electrocatalyst)'
    census["arxiv"][metal] = {"total": arxiv_count(q, f"arxiv_{metal}.xml")}
    time.sleep(3)

json.dump(census, open(os.path.join(R0, "harvest", "census.json"), "w"), indent=2)
print(json.dumps(census, indent=2))
