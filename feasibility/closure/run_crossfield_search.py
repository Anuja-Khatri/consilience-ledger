"""Test 2 runner: vocabulary-stripped SHORT structural queries -> arXiv + Semantic Scholar,
cached + resumable, cap 40 query-calls. Target: durability via an operando-formed nanostructure."""
import json, os, re, subprocess, urllib.parse
CACHE="feasibility/closure/cache"; os.makedirs(CACHE, exist_ok=True)
CAP=40
# vocabulary-stripped structural queries (2-5 words; system-specific nouns In/Mn/Pd dropped)
QUERIES=[
 "operando nanostructure formation durability",
 "needle nanostructure electrocatalyst stability",
 "morphology durability oxide electrocatalyst",
 "operando structural evolution oxygen evolution",
 "anisotropic nanostructure corrosion stability",
 "nanostructure stability acidic oxygen evolution",
 "self-reconstruction catalyst durability",
 "operando restructuring stability electrode",
 "nanoneedle oxide stability catalysis",
 "structure-induced durability electrocatalyst",
]
def curl(url):
    return subprocess.run(["curl","-sL","-A","Mozilla/5.0","--max-time","40",url],
                          capture_output=True,text=True).stdout
def slug(s): return re.sub(r'[^a-z0-9]+','_',s.lower())[:40]
calls=0; results=[]
for q in QUERIES:
    # --- arXiv (cond-mat + physics.chem-ph) ---
    if calls<CAP:
        f=f"{CACHE}/arxiv_{slug(q)}.xml"
        if not os.path.exists(f):
            cat="(cat:cond-mat.mtrl-sci+OR+cat:physics.chem-ph)"
            url=("http://export.arxiv.org/api/query?search_query="+cat+"+AND+all:"+
                 urllib.parse.quote(q)+"&max_results=6")
            open(f,"w").write(curl(url)); calls+=1
        xml=open(f).read()
        for m in re.finditer(r"<entry>.*?<title>(.*?)</title>.*?</entry>", xml, re.S):
            t=re.sub(r'\s+',' ',m.group(1)).strip()
            if t and t.lower()!="arxiv query results": results.append(("arxiv",q,t))
    # --- Semantic Scholar (FoS: Materials Science, Chemistry) ---
    if calls<CAP:
        f=f"{CACHE}/s2_{slug(q)}.json"
        if not os.path.exists(f):
            url=("https://api.semanticscholar.org/graph/v1/paper/search?query="+
                 urllib.parse.quote(q)+"&fields=title,fieldsOfStudy,year&limit=6"
                 "&fieldsOfStudy=Materials Science,Chemistry")
            open(f,"w").write(curl(url)); calls+=1
        try:
            d=json.loads(open(f).read())
            for p in d.get("data",[]) or []:
                if p.get("title"): results.append(("s2",q,p["title"].strip()))
        except Exception: pass
print(f"query-calls used: {calls} (cap {CAP})")
print(f"candidates retrieved: {len(results)}")
# on-topic by title?
ONT=re.compile(r"oxid|electrocataly|oxygen evolution|\bOER\b|corros|dissol|degrad|durab|stabil|"
   r"nanostructur|morpholog|operando|catalyst|electrode|water oxidation|perovskite|irid|ruthen|"
   r"overpotential|electrochemic|acidic|alkaline|thin film|\bphase\b|crystal|surface|reconstruct|"
   r"spinel|hydroxide|electroly", re.I)
on=[r for r in results if ONT.search(r[2])]
print(f"on-topic by title: {len(on)}/{len(results)} = {len(on)/max(1,len(results)):.0%}")
json.dump([{"source":s,"query":q,"title":t,"on_topic":bool(ONT.search(t))} for s,q,t in results],
          open("feasibility/closure/test2_candidates.json","w"), indent=2)
print("saved feasibility/closure/test2_candidates.json")
# show a sample
for s,q,t in results[:25]: print(f"  [{s}] {'OK' if ONT.search(t) else '--'} {t[:85]}")
