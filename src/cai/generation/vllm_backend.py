"""vLLM offline generation backend (guarded import; HF fallback handled upstream).

Construction raises if vLLM is missing or the model architecture is unsupported;
``generation.get_generator`` catches that and falls back to HF.
"""

from __future__ import annotations

from ..config import Config
from ..models import load_tokenizer
from .base import Conversation


class VLLMGenerator:
    def __init__(self, cfg: Config):
        from vllm import LLM  # raises ImportError if extra not installed

        self.cfg = cfg
        self.tokenizer = load_tokenizer(cfg)
        v = cfg.generation.get("vllm", {})
        # Constructing the engine is where an unsupported arch will fail loudly.
        self.llm = LLM(
            model=cfg.model.name,
            dtype=cfg.model.dtype,
            trust_remote_code=cfg.model.get("trust_remote_code", True),
            gpu_memory_utilization=v.get("gpu_memory_utilization", 0.90),
            max_model_len=v.get("max_model_len", 4096),
            tensor_parallel_size=v.get("tensor_parallel_size", 1),
        )

    def chat(
        self,
        conversations: list[Conversation],
        max_new_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
    ) -> list[str]:
        from vllm import SamplingParams

        gen = self.cfg.generation
        params = SamplingParams(
            max_tokens=max_new_tokens or gen.max_new_tokens,
            temperature=gen.temperature if temperature is None else temperature,
            top_p=gen.top_p if top_p is None else top_p,
        )
        prompts = [
            self.tokenizer.apply_chat_template(c, tokenize=False, add_generation_prompt=True)
            for c in conversations
        ]
        results = self.llm.generate(prompts, params)
        return [r.outputs[0].text.strip() for r in results]
