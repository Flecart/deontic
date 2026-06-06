#!/usr/bin/env python3
"""Thin, pluggable LLM adapter for the eval harness.

`complete(system, user)` -> Completion(text, input_tokens, output_tokens, latency_s).

Provider via env `DEONTIC_LLM_PROVIDER`; if unset it auto-detects from the keys
present: `anthropic` (ANTHROPIC_API_KEY) → `openai` (OPENAI_API_KEY) →
`openrouter` (OPENROUTER_API_KEY). Model via `DEONTIC_LLM_MODEL` (per-provider
default below). The adapter is deliberately minimal — the arms own their
prompting; this just does one round-trip and reports usage so metrics.py can
compute cost.

The OpenAI-compatible branch (openai / openrouter) uses stdlib urllib so it has
no third-party dependency. The Anthropic branch uses the official SDK.
"""
from __future__ import annotations

import json
import os
import time
import urllib.request
from dataclasses import dataclass


@dataclass
class Completion:
    text: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_s: float = 0.0


def _detect_provider() -> str:
    p = os.environ.get("DEONTIC_LLM_PROVIDER")
    if p:
        return p
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("OPENROUTER_API_KEY"):
        return "openrouter"
    raise SystemExit("no LLM key found (set ANTHROPIC_API_KEY / OPENAI_API_KEY / "
                     "OPENROUTER_API_KEY, or DEONTIC_LLM_PROVIDER)")


PROVIDER = _detect_provider()
_DEFAULT_MODEL = {"anthropic": "claude-opus-4-8",
                  "openai": "gpt-4.1",
                  "openrouter": "anthropic/claude-opus-4-8"}
MODEL = os.environ.get("DEONTIC_LLM_MODEL", _DEFAULT_MODEL.get(PROVIDER, "gpt-4.1"))
EFFORT = os.environ.get("DEONTIC_LLM_EFFORT", "medium")  # anthropic only

_OAI_ENDPOINT = {"openai": "https://api.openai.com/v1/chat/completions",
                 "openrouter": "https://openrouter.ai/api/v1/chat/completions"}
_OAI_KEYENV = {"openai": "OPENAI_API_KEY", "openrouter": "OPENROUTER_API_KEY"}

_client = None


def complete(system: str, user: str, max_tokens: int = 4096) -> Completion:
    if PROVIDER == "anthropic":
        return _complete_anthropic(system, user, max_tokens)
    if PROVIDER in ("openai", "openrouter"):
        return _complete_openai(system, user, max_tokens)
    raise SystemExit(f"unknown DEONTIC_LLM_PROVIDER={PROVIDER!r}")


def _complete_anthropic(system: str, user: str, max_tokens: int) -> Completion:
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic()
    t0 = time.monotonic()
    resp = _client.messages.create(
        model=MODEL, max_tokens=max_tokens,
        thinking={"type": "adaptive"}, output_config={"effort": EFFORT},
        system=system, messages=[{"role": "user", "content": user}],
    )
    latency = time.monotonic() - t0
    text = next((b.text for b in resp.content if b.type == "text"), "")
    u = resp.usage
    return Completion(text, getattr(u, "input_tokens", 0),
                      getattr(u, "output_tokens", 0), latency)


def _complete_openai(system: str, user: str, max_tokens: int) -> Completion:
    key = os.environ[_OAI_KEYENV[PROVIDER]]
    body = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        # Force a JSON object back so the harness's parser is deterministic.
        "response_format": {"type": "json_object"},
        "max_completion_tokens": max_tokens,
    }
    req = urllib.request.Request(
        _OAI_ENDPOINT[PROVIDER],
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode("utf-8"))
    latency = time.monotonic() - t0
    text = data["choices"][0]["message"]["content"] or ""
    u = data.get("usage", {})
    return Completion(text, u.get("prompt_tokens", 0),
                      u.get("completion_tokens", 0), latency)
