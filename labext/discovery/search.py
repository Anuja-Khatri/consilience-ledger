"""arXiv + Semantic Scholar search, cached, rate-capped, resumable (D12, CC-29).

Every response is cached to disk by query sha, so reruns are free. A global query cap
is enforced and recorded; polite sleeps between live calls. If Semantic Scholar is
unreachable, arXiv alone is used and the gap is recorded. A fetcher can be injected so
tests never hit the network.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def _default_fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "consilience-lab-extension/0.1"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


class SearchHarness:
    def __init__(self, cache_dir: str, max_queries: int = 30, sleep: float = 3.0, fetch=None):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.max_queries = max_queries
        self.sleep = sleep
        self.fetch = fetch or _default_fetch
        self.queries_run = 0
        self.capped = []

    def _cache_path(self, source: str, query: str) -> str:
        h = hashlib.sha256(f"{source}\x1f{query}".encode()).hexdigest()[:20]
        return os.path.join(self.cache_dir, f"{source}_{h}.json")

    def _get(self, source: str, query: str, build_url, parse):
        path = self._cache_path(source, query)
        if os.path.exists(path):
            with open(path) as fh:
                return json.load(fh)
        if self.queries_run >= self.max_queries:
            self.capped.append({"source": source, "query": query})
            return []
        if self.queries_run > 0:
            time.sleep(self.sleep)
        self.queries_run += 1
        try:
            raw = self.fetch(build_url(query))
            results = parse(raw)
        except Exception as exc:  # network error, parse error
            results = []
            self.capped.append({"source": source, "query": query, "error": str(exc)[:120]})
        with open(path, "w") as fh:
            json.dump(results, fh, indent=2, sort_keys=True)
        return results

    def arxiv(self, query: str, max_results: int = 10):
        def build(q):
            qs = urllib.parse.urlencode({"search_query": f"all:{q}", "max_results": max_results})
            return f"http://export.arxiv.org/api/query?{qs}"

        def parse(raw: bytes):
            ns = {"a": "http://www.w3.org/2005/Atom"}
            root = ET.fromstring(raw)
            out = []
            for e in root.findall("a:entry", ns):
                out.append({
                    "id": (e.findtext("a:id", default="", namespaces=ns)),
                    "title": (e.findtext("a:title", default="", namespaces=ns) or "").strip(),
                    "abstract": (e.findtext("a:summary", default="", namespaces=ns) or "").strip(),
                    "source": "arxiv",
                })
            return out

        return self._get("arxiv", query, build, parse)

    def semantic_scholar(self, query: str, max_results: int = 10):
        def build(q):
            qs = urllib.parse.urlencode({"query": q, "limit": max_results,
                                         "fields": "title,abstract,externalIds"})
            return f"https://api.semanticscholar.org/graph/v1/paper/search?{qs}"

        def parse(raw: bytes):
            data = json.loads(raw)
            out = []
            for p in data.get("data", []) or []:
                out.append({
                    "id": (p.get("externalIds") or {}).get("DOI") or p.get("paperId"),
                    "title": p.get("title") or "",
                    "abstract": p.get("abstract") or "",
                    "source": "semantic_scholar",
                })
            return out

        return self._get("semantic_scholar", query, build, parse)


__all__ = ["SearchHarness"]
