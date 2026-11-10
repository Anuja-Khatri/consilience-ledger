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
import urllib.request

from labext.extraction.prompt import FEWSHOT, SYSTEM_PROMPT, PROMPT_VERSION


class MissingKeyError(RuntimeError):
    """Raised when a backend's API key is not in the environment."""


class ExtractorBackend:
    name: str  # exact model string, recorded in METHODS.md

    def extract(self, paper_text: str) -> list[dict]:
        raise NotImplementedError


def _parse_cards(text: str) -> list[dict]:
    """Parse a model reply into a list of card dicts, tolerant of code fences."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```", 2)[1]
        if t.startswith("json"):
            t = t[4:]
    start, end = t.find("["), t.rfind("]")
    if start == -1 or end == -1:
        return []
    return json.loads(t[start : end + 1])


class AnthropicBackend(ExtractorBackend):
    """Anthropic Messages API via stdlib urllib. UNTESTED pending an API key."""

    def __init__(self, model: str):
        self.name = model

    def extract(self, paper_text: str) -> list[dict]:
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise MissingKeyError("ANTHROPIC_API_KEY not set")
        messages = [dict(m) for m in FEWSHOT] + [{"role": "user", "content": f"Passage:\n{paper_text}"}]
        body = json.dumps(
            {"model": self.name, "max_tokens": 4096, "system": SYSTEM_PROMPT, "messages": messages}
        ).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        with urllib.request.urlopen(req) as resp:  # pragma: no cover (needs key)
            payload = json.loads(resp.read())
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
        body = json.dumps({"model": self.name, "messages": messages, "temperature": 0}).encode()
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=body,
            headers={"authorization": f"Bearer {key}", "content-type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:  # pragma: no cover (needs key)
            payload = json.loads(resp.read())
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
        return [AnthropicBackend("claude-sonnet-4-6"), OpenAIBackend("gpt-4.1")]
    if have_anthropic:
        return [AnthropicBackend("claude-sonnet-4-6"), AnthropicBackend("claude-haiku-4-5-20251001")]
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
