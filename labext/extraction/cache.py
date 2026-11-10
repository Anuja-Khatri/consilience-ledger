"""Disk cache for model outputs (D3). One jsonl per (paper, model). Resumable."""

from __future__ import annotations

import hashlib
import json
import os
import re


def cache_key(model: str, prompt_version: str, paper_sha: str) -> str:
    return hashlib.sha256(f"{model}\x1f{prompt_version}\x1f{paper_sha}".encode()).hexdigest()


def _safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name)


class JsonlCache:
    def __init__(self, directory: str):
        self.dir = directory
        os.makedirs(self.dir, exist_ok=True)

    def path(self, paper_id: str, model: str) -> str:
        return os.path.join(self.dir, f"{_safe(paper_id)}__{_safe(model)}.jsonl")

    def load(self, paper_id: str, model: str):
        p = self.path(paper_id, model)
        if not os.path.exists(p):
            return None
        with open(p, "r") as fh:
            return [json.loads(line) for line in fh if line.strip()]

    def save(self, paper_id: str, model: str, records: list) -> str:
        p = self.path(paper_id, model)
        with open(p, "w") as fh:
            for rec in records:
                fh.write(json.dumps(rec, sort_keys=True))
                fh.write("\n")
        return p
