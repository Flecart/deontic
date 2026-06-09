"""HF transformers generation backend (batched, chat-template aware)."""

from __future__ import annotations

import torch

from ..config import Config
from ..models import load_model, load_tokenizer
from .base import Conversation


class HFGenerator:
    def __init__(self, cfg: Config, model=None, tokenizer=None):
        self.cfg = cfg
        self.tokenizer = tokenizer or load_tokenizer(cfg)
        self.model = model if model is not None else load_model(cfg)
        self.model.eval()
        self.batch_size = cfg.generation.get("batch_size", 8)

    @torch.no_grad()
    def chat(
        self,
        conversations: list[Conversation],
        max_new_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
    ) -> list[str]:
        gen = self.cfg.generation
        max_new_tokens = max_new_tokens or gen.max_new_tokens
        temperature = gen.temperature if temperature is None else temperature
        top_p = gen.top_p if top_p is None else top_p
        do_sample = temperature is not None and temperature > 0

        tok = self.tokenizer
        prev_side = tok.padding_side
        tok.padding_side = "left"  # required for correct batched generation
        outputs: list[str] = []
        try:
            for start in range(0, len(conversations), self.batch_size):
                batch = conversations[start : start + self.batch_size]
                prompts = [
                    tok.apply_chat_template(c, tokenize=False, add_generation_prompt=True)
                    for c in batch
                ]
                enc = tok(prompts, return_tensors="pt", padding=True, add_special_tokens=False)
                enc = {k: v.to(self.model.device) for k, v in enc.items()}
                out = self.model.generate(
                    **enc,
                    max_new_tokens=max_new_tokens,
                    do_sample=do_sample,
                    temperature=temperature if do_sample else None,
                    top_p=top_p if do_sample else None,
                    pad_token_id=tok.pad_token_id,
                )
                gen_tokens = out[:, enc["input_ids"].shape[1] :]
                outputs.extend(tok.batch_decode(gen_tokens, skip_special_tokens=True))
        finally:
            tok.padding_side = prev_side
        return [o.strip() for o in outputs]
