"""Pluggable text generation: vLLM preferred, HF transformers fallback.

The target model's architecture is new enough that vLLM may not support it. The
factory tries the requested backend and transparently falls back to HF so the
pipeline always runs.
"""

from __future__ import annotations

import warnings

from ..config import Config
from .base import Generator


def get_generator(cfg: Config) -> Generator:
    backend = cfg.generation.get("backend", "vllm")

    if backend == "hf":
        from .hf_backend import HFGenerator

        return HFGenerator(cfg)

    if backend == "vllm" and cfg.model.get("adapter"):
        warnings.warn(
            "model.adapter is set; using HF backend (vLLM LoRA serving not wired).",
            stacklevel=2,
        )
        from .hf_backend import HFGenerator

        return HFGenerator(cfg)

    if backend == "vllm":
        try:
            from .vllm_backend import VLLMGenerator

            return VLLMGenerator(cfg)
        except Exception as exc:  # noqa: BLE001 - import or unsupported-arch error
            warnings.warn(
                f"vLLM backend unavailable ({type(exc).__name__}: {exc}); "
                "falling back to HF transformers generation.",
                stacklevel=2,
            )
            from .hf_backend import HFGenerator

            return HFGenerator(cfg)

    raise ValueError(f"Unknown generation.backend: {backend!r}")


__all__ = ["Generator", "get_generator"]
