"""Model registry + OpenAI-compatible client factory.

Swap models with `--model <name>`. A name is either a key in REGISTRY or an
ad-hoc `provider:model_id` (e.g. `openrouter:google/gemini-2.0-flash-001`).
Add a model by adding one line to REGISTRY.

Providers are OpenAI-compatible; OpenRouter is just a different base_url + key,
so the same code drives both. `stub` is an offline fake for smoke-testing the
harness without network or spend.
"""
from __future__ import annotations
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelSpec:
    name: str
    provider: str   # "openai" | "openrouter" | "stub"
    model_id: str
    # reasoning models (o-series) reject temperature / need different params
    reasoning: bool = False


PROVIDERS = {
    "openai":     {"base_url": None,                              "key_env": "OPENAI_API_KEY"},
    "openrouter": {"base_url": "https://openrouter.ai/api/v1",    "key_env": "OPENROUTER_API_KEY"},
    "stub":       {"base_url": None,                              "key_env": None},
}

# Short name -> spec. Extend freely.
REGISTRY: dict[str, ModelSpec] = {
    "gpt-4o":        ModelSpec("gpt-4o",        "openai", "gpt-4o"),
    "gpt-4o-mini":   ModelSpec("gpt-4o-mini",   "openai", "gpt-4o-mini"),
    "gpt-4.1":       ModelSpec("gpt-4.1",       "openai", "gpt-4.1"),
    "gpt-4.1-mini":  ModelSpec("gpt-4.1-mini",  "openai", "gpt-4.1-mini"),
    "o4-mini":       ModelSpec("o4-mini",       "openai", "o4-mini", reasoning=True),
    # modern agentic models (user-requested)
    "gpt-5.4":           ModelSpec("gpt-5.4",           "openai", "gpt-5.4", reasoning=True),
    "gpt-5.4-mini":      ModelSpec("gpt-5.4-mini",      "openai", "gpt-5.4-mini", reasoning=True),
    "qwen3.6":           ModelSpec("qwen3.6",           "openrouter", "qwen/qwen3.6-35b-a3b"),
    "deepseek-v4-flash": ModelSpec("deepseek-v4-flash", "openrouter", "deepseek/deepseek-v4-flash"),
    "grok-4.3":          ModelSpec("grok-4.3",          "openrouter", "x-ai/grok-4.3"),
    # OpenRouter (provider/model ids)
    "llama-3.3-70b":     ModelSpec("llama-3.3-70b",     "openrouter", "meta-llama/llama-3.3-70b-instruct"),
    "claude-3.5-sonnet": ModelSpec("claude-3.5-sonnet", "openrouter", "anthropic/claude-3.5-sonnet"),
    "deepseek-chat":     ModelSpec("deepseek-chat",     "openrouter", "deepseek/deepseek-chat"),
    "qwen-2.5-72b":      ModelSpec("qwen-2.5-72b",      "openrouter", "qwen/qwen-2.5-72b-instruct"),
    "gemini-2.0-flash":  ModelSpec("gemini-2.0-flash",  "openrouter", "google/gemini-2.0-flash-001"),
    # offline plumbing test
    "stub":          ModelSpec("stub",          "stub",   "stub"),
}


def resolve(name: str) -> ModelSpec:
    if name in REGISTRY:
        return REGISTRY[name]
    if ":" in name:
        provider, model_id = name.split(":", 1)
        if provider not in PROVIDERS:
            raise SystemExit(f"unknown provider '{provider}' (use {list(PROVIDERS)})")
        return ModelSpec(name, provider, model_id)
    raise SystemExit(
        f"unknown model '{name}'. Known: {list(REGISTRY)}; or use 'provider:model_id'.")


def make_client(spec: ModelSpec):
    """Return an OpenAI-compatible client (or a StubClient for offline runs)."""
    if spec.provider == "stub":
        return StubClient()
    from openai import OpenAI
    cfg = PROVIDERS[spec.provider]
    key = os.environ.get(cfg["key_env"])
    if not key:
        raise SystemExit(
            f"environment variable {cfg['key_env']} is not set "
            f"(needed for provider '{spec.provider}').")
    # Bound each request so one hung connection (seen on OpenRouter) can't stall
    # the whole sweep; the SDK still retries transient failures a few times.
    return OpenAI(api_key=key, base_url=cfg["base_url"], timeout=90.0, max_retries=3)


# ── Offline stub (mimics the slice of the SDK the agents use) ──────────────────

class _Msg:
    def __init__(self, content=None, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls
        self.role = "assistant"

class _Choice:
    def __init__(self, message): self.message = message

class _Resp:
    def __init__(self, message): self.choices = [_Choice(message)]

class _Completions:
    def create(self, **kwargs):
        # Always answer "Yes" with no tool call — enough to exercise the harness
        # plumbing (data, scoring, logging) without a real model.
        return _Resp(_Msg(content="Reasoning omitted (stub).\nANSWER: Yes"))

class _Chat:
    def __init__(self): self.completions = _Completions()

class StubClient:
    def __init__(self): self.chat = _Chat()
