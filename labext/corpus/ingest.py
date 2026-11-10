"""PDF and text ingestion with sha provenance."""

from __future__ import annotations

import hashlib
import os


def file_sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def pdf_to_text(path: str) -> str:
    from pypdf import PdfReader

    reader = PdfReader(path)
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def ingest(path: str, out_dir: str) -> dict:
    """Extract text from a PDF (or read a .txt) and cache it. Returns provenance."""
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(path))[0]
    if path.lower().endswith(".pdf"):
        text = pdf_to_text(path)
    else:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    out_path = os.path.join(out_dir, base + ".txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return {
        "source_path": path,
        "text_path": out_path,
        "source_sha256": file_sha(path),
        "text_sha256": text_sha(text),
        "n_chars": len(text),
    }
