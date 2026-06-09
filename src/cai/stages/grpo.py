"""GRPO against an AI-feedback reward -> the RL-CAI adapter (TRL GRPOTrainer).

The reward function reuses the constitution-grounded pointwise scorer from the
ai-feedback stage. A separate judge generator scores rollouts during training.
NOTE: the judge loads its own model copy -- cheap for the smoke proxy, but for
the 35B target point it at a smaller/served judge via a judge-specific config.
"""

from __future__ import annotations

from datasets import Dataset

from ..config import Config, resolve_path
from ..constitution import load_constitution
from ..data import load_prompts
from ..generation import get_generator
from ..models import lora_config, load_tokenizer, load_model
from .ai_feedback import score_responses


def _dataset(cfg: Config) -> Dataset:
    prompts = load_prompts(cfg)
    return Dataset.from_list(
        [{"prompt": [{"role": "user", "content": p}]} for p in prompts]
    )


def _text(item) -> str:
    """Extract assistant/user text from a conversational or plain item."""
    if isinstance(item, str):
        return item
    if isinstance(item, list) and item:
        return item[-1].get("content", "")
    return str(item)


def _make_reward(cfg: Config):
    constitution = load_constitution(cfg.constitution.path)
    judge = get_generator(cfg)  # lazily-used judge generator

    def reward_fn(completions, prompts=None, **kwargs):
        responses = [_text(c) for c in completions]
        questions = [_text(p) for p in (prompts or [""] * len(responses))]
        return score_responses(judge, constitution.judge_rubric, questions, responses)

    reward_fn.__name__ = "constitution_reward"
    return reward_fn


def run(cfg: Config) -> str:
    from trl import GRPOConfig, GRPOTrainer

    t = cfg.train
    # GRPO groups num_generations completions per prompt, so the per-device batch
    # must be a multiple of num_generations; bump it up if the config isn't.
    num_generations = cfg.rl.get("num_generations", 4)
    per_device = t.per_device_train_batch_size
    if per_device % num_generations != 0:
        per_device = num_generations

    args = GRPOConfig(
        output_dir=str(resolve_path(cfg.paths.rl_model)),
        num_generations=num_generations,
        per_device_train_batch_size=per_device,
        gradient_accumulation_steps=t.gradient_accumulation_steps,
        num_train_epochs=t.num_train_epochs,
        max_steps=t.get("max_steps", -1),
        learning_rate=float(t.learning_rate),
        logging_steps=t.logging_steps,
        save_steps=t.save_steps,
        bf16=t.get("bf16", True),
        gradient_checkpointing=t.get("gradient_checkpointing", True),
        max_completion_length=cfg.generation.max_new_tokens,
        seed=t.get("seed", 42),
        report_to="none",
    )

    model = load_model(cfg, for_training=True)
    tokenizer = load_tokenizer(cfg)
    peft_cfg = lora_config(cfg) if cfg.lora.get("enabled", True) else None

    trainer = GRPOTrainer(
        model=model,
        args=args,
        train_dataset=_dataset(cfg),
        reward_funcs=_make_reward(cfg),
        processing_class=tokenizer,
        peft_config=peft_cfg,
    )
    trainer.train()
    out = resolve_path(cfg.paths.rl_model)
    trainer.save_model(str(out))
    print(f"[grpo] saved RL-CAI adapter -> {out}")
    return str(out)
