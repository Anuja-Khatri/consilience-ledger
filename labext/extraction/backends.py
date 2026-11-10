"""Extraction model backends. Keys from environment variables only (D14).

Real backends (Anthropic, OpenAI) are implemented but raise ``MissingKeyError`` when
their key is absent from the environment, so the non-API pipeline still runs and the
block is logged. A ``MockBackend`` drives the tests deterministically.

Model selection (D3): prefer one Anthropic + one non-Anthropic if a second family's
key exists; otherwise two different Anthropic model versions. Exact model strings are
recorded in METHODS.md.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

from labext.extraction.prompt import FEWSHOT, SYSTEM_PROMPT, PROMPT_VERSION


class MissingKeyError(RuntimeError):
    """Raised when a backend's API key is not in the environment."""


def _post_json(url: str, headers: dict, payload: dict, retries: int = 4) -> dict:
    """POST JSON with exponential backoff on transient errors (CC-16)."""
    body = json.dumps(payload).encode()
    delay = 2.0
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code in (429, 500, 502, 503, 529) and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise last  # pragma: no cover


class ExtractorBackend:
    name: str  # exact model string, recorded in METHODS.md

    def extract(self, paper_text: str) -> list[dict]:
        raise NotImplementedError


def _salvage_objects(s: str) -> list[dict]:
    """Extract top-level {...} JSON objects by brace matching; skip any that fail to
    parse (e.g. a truncated trailing object). Tolerates max_tokens truncation."""
    out = []
    depth = 0
    start = None
    in_str = False
    esc = False
    for i, ch in enumerate(s):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    try:
                        out.append(json.loads(s[start : i + 1]))
                    except Exception:
                        pass
                    start = None
    return out


def _parse_cards(text: str) -> list[dict]:
    """Parse a model reply into a list of card dicts, tolerant of code fences and of
    max_tokens truncation. Never raises: an unparseable reply yields what can be salvaged."""
    t = text.strip()
    if t.startswith("```"):
        parts = t.split("```")
        if len(parts) >= 2:
            t = parts[1]
            if t.startswith("json"):
                t = t[4:]
    start = t.find("[")
    end = t.rfind("]")
    if start != -1 and end > start:
        try:
            data = json.loads(t[start : end + 1])
            return data if isinstance(data, list) else [data]
        except Exception:
            pass
    # fall back to brace-matched salvage of whatever complete objects exist
    return _salvage_objects(t[start:] if start != -1 else t)


class AnthropicBackend(ExtractorBackend):
    """Anthropic Messages API via stdlib urllib. UNTESTED pending an API key."""

    def __init__(self, model: str):
        self.name = model

    def extract(self, paper_text: str) -> list[dict]:
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise MissingKeyError("ANTHROPIC_API_KEY not set")
        messages = [dict(m) for m in FEWSHOT] + [{"role": "user", "content": f"Passage:\n{paper_text}"}]
        payload = _post_json(
            "https://api.anthropic.com/v1/messages",
            {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            {"model": self.name, "max_tokens": 8192, "system": SYSTEM_PROMPT, "messages": messages},
        )
        text = "".join(block.get("text", "") for block in payload.get("content", []))
        return _parse_cards(text)


class OpenAIBackend(ExtractorBackend):
    """OpenAI Chat Completions via stdlib urllib. UNTESTED pending an API key."""

    def __init__(self, model: str):
        self.name = model

    def extract(self, paper_text: str) -> list[dict]:
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise MissingKeyError("OPENAI_API_KEY not set")
        messages = (
            [{"role": "system", "content": SYSTEM_PROMPT}]
            + [dict(m) for m in FEWSHOT]
            + [{"role": "user", "content": f"Passage:\n{paper_text}"}]
        )
        payload = _post_json(
            "https://api.openai.com/v1/chat/completions",
            {"authorization": f"Bearer {key}", "content-type": "application/json"},
            {"model": self.name, "messages": messages, "temperature": 0},
        )
        text = payload["choices"][0]["message"]["content"]
        return _parse_cards(text)


class MockBackend(ExtractorBackend):
    """Deterministic backend for tests. Maps paper_id -> list of card dicts."""

    def __init__(self, name: str, scripts: dict[str, list[dict]]):
        self.name = name
        self.scripts = scripts
        self.calls = 0

    def extract(self, paper_text: str) -> list[dict]:
        self.calls += 1
        return self.scripts.get(paper_text, [])


def select_backends() -> list[ExtractorBackend]:
    """Pick two backends per D3 from whatever keys exist in the environment.

    Returns an empty list and leaves the caller to log the block if no key is set.
    """
    have_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))
    have_openai = bool(os.environ.get("OPENAI_API_KEY"))
    if have_anthropic and have_openai:
        return [AnthropicBackend("claude-sonnet-5"), OpenAIBackend("gpt-4.1")]
    if have_anthropic:
        return [AnthropicBackend("claude-sonnet-5"), AnthropicBackend("claude-haiku-4-5-20251001")]
    return []


__all__ = [
    "MissingKeyError",
    "ExtractorBackend",
    "AnthropicBackend",
    "OpenAIBackend",
    "MockBackend",
    "select_backends",
    "PROMPT_VERSION",
]
