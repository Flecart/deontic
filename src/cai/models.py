"""Tokenizer/model loading (multimodal-aware) and LoRA attachment.

The target model (Qwen3.6-35B-A3B) is a multimodal MoE whose class is
``Qwen3_5MoeForConditionalGeneration`` -- it does not load via
``AutoModelForCausalLM``. ``load_model`` therefore tries the configured auto-class
and gracefully falls back, while we always drive it as a text LLM.
"""

from __future__ import annotations

import torch
from transformers import AutoTokenizer

from .config import Config


def _dtype(name: str) -> torch.dtype:
    return {"bfloat16": torch.bfloat16, "float16": torch.float16, "float32": torch.float32}[name]


def load_tokenizer(cfg: Config):
    tok = AutoTokenizer.from_pretrained(
        cfg.model.name, trust_remote_code=cfg.model.get("trust_remote_code", True)
    )
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    return tok


def _auto_classes(name: str):
    """Yield candidate model auto-classes to try, in order."""
    from transformers import AutoModelForCausalLM

    if name == "AutoModelForCausalLM":
        return [AutoModelForCausalLM]
    if name == "AutoModelForImageTextToText":
        from transformers import AutoModelForImageTextToText

        return [AutoModelForImageTextToText]
    # "auto": prefer plain causal LM, fall back to the multimodal class.
    candidates = [AutoModelForCausalLM]
    try:
        from transformers import AutoModelForImageTextToText

        candidates.append(AutoModelForImageTextToText)
    except ImportError:
        pass
    return candidates


def load_model(cfg: Config, for_training: bool = False):
    """Load the model with dtype/device_map from config, trying auto-classes.

    For training we pin the whole model onto the local-rank GPU (35B-A3B fits on
    one B200); ``device_map="auto"`` is for sharded inference, not the Trainer.
    """
    import os

    if for_training:
        device_map = {"": int(os.environ.get("LOCAL_RANK", 0))}
    else:
        device_map = cfg.model.get("device_map", "auto")
    kwargs = dict(
        dtype=_dtype(cfg.model.dtype),
        device_map=device_map,
        trust_remote_code=cfg.model.get("trust_remote_code", True),
    )
    if cfg.model.get("attn_implementation"):
        kwargs["attn_implementation"] = cfg.model.attn_implementation

    errors = []
    model = None
    for cls in _auto_classes(cfg.model.get("auto_class", "auto")):
        try:
            model = cls.from_pretrained(cfg.model.name, **kwargs)
            break
        except Exception as exc:  # noqa: BLE001 - report all attempts together
            errors.append(f"{cls.__name__}: {type(exc).__name__}: {exc}")
    if model is None:
        raise RuntimeError(
            "Failed to load model "
            f"{cfg.model.name!r} with any auto-class.\n  " + "\n  ".join(errors)
        )

    # Optionally apply a previously-trained LoRA adapter (e.g. the SL-CAI model
    # as the policy for the RLAIF sampling/feedback stage).
    adapter = cfg.model.get("adapter")
    if adapter:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, adapter)
    return model


def load_model_and_tokenizer(cfg: Config):
    return load_model(cfg), load_tokenizer(cfg)


def list_linear_modules(model) -> list[str]:
    """Distinct leaf names of nn.Linear modules -- candidates for LoRA targets."""
    import torch.nn as nn

    names = set()
    for full_name, module in model.named_modules():
        if isinstance(module, nn.Linear):
            names.add(full_name.split(".")[-1])
    return sorted(names)


def lora_config(cfg: Config):
    """Build a PEFT LoraConfig from cfg.lora."""
    from peft import LoraConfig

    return LoraConfig(
        r=cfg.lora.r,
        lora_alpha=cfg.lora.alpha,
        lora_dropout=cfg.lora.dropout,
        target_modules=list(cfg.lora.target_modules),
        bias=cfg.lora.get("bias", "none"),
        task_type="CAUSAL_LM",
    )


def attach_lora(model, cfg: Config):
    """Wrap a loaded model with LoRA adapters (no-op if disabled)."""
    if not cfg.lora.get("enabled", True):
        return model
    from peft import get_peft_model

    peft_model = get_peft_model(model, lora_config(cfg))
    peft_model.print_trainable_parameters()
    return peft_model
