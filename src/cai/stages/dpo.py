"""DPO on AI-feedback preference pairs -> the RL-CAI adapter (TRL DPOTrainer)."""

from __future__ import annotations

from datasets import Dataset

from ..config import Config, resolve_path
from ..data import read_jsonl
from ..models import lora_config, load_model, load_tokenizer


def _dataset(cfg: Config) -> Dataset:
    rows = read_jsonl(cfg.paths.pref_data)
    # Conversational preference format -> TRL applies the chat template.
    examples = [
        {
            "prompt": [{"role": "user", "content": r["prompt"]}],
            "chosen": [{"role": "assistant", "content": r["chosen"]}],
            "rejected": [{"role": "assistant", "content": r["rejected"]}],
        }
        for r in rows
    ]
    return Dataset.from_list(examples)


def run(cfg: Config) -> str:
    from trl import DPOConfig, DPOTrainer

    t = cfg.train
    args = DPOConfig(
        output_dir=str(resolve_path(cfg.paths.rl_model)),
        beta=cfg.rl.get("beta", 0.1),
        per_device_train_batch_size=t.per_device_train_batch_size,
        gradient_accumulation_steps=t.gradient_accumulation_steps,
        num_train_epochs=t.num_train_epochs,
        max_steps=t.get("max_steps", -1),
        learning_rate=float(t.learning_rate),
        logging_steps=t.logging_steps,
        save_steps=t.save_steps,
        bf16=t.get("bf16", True),
        gradient_checkpointing=t.get("gradient_checkpointing", True),
        max_length=t.max_length,
        seed=t.get("seed", 42),
        report_to="none",
    )

    model = load_model(cfg, for_training=True)
    tokenizer = load_tokenizer(cfg)
    peft_cfg = lora_config(cfg) if cfg.lora.get("enabled", True) else None

    # With a PEFT adapter, TRL uses the base model as the frozen reference,
    # so no separate ref model needs loading.
    trainer = DPOTrainer(
        model=model,
        args=args,
        train_dataset=_dataset(cfg),
        processing_class=tokenizer,
        peft_config=peft_cfg,
    )
    trainer.train()
    out = resolve_path(cfg.paths.rl_model)
    trainer.save_model(str(out))
    print(f"[dpo] saved RL-CAI adapter -> {out}")
    return str(out)
