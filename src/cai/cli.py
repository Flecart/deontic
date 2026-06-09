"""Command-line entrypoint: `cai <stage> [--config ...] [--set k=v ...]`.

Stages:
    critique-revise   SL stage: writes the SFT dataset
    sft               train the SL-CAI LoRA adapter
    ai-feedback       RLAIF labeling: writes the preference dataset
    rl                train the RL-CAI adapter (DPO or GRPO per rl.method)
    inspect-modules   load the model and print LoRA-target candidate modules
"""

from __future__ import annotations

import argparse
import sys

from .config import load_config


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--config", "-c", action="append", default=[],
        help="Profile YAML(s) merged over base.yaml (repeatable; bare names ok).",
    )
    p.add_argument(
        "--set", "-s", dest="overrides", action="append", default=[], metavar="KEY=VALUE",
        help="Override a config value, e.g. --set rl.method=grpo (repeatable).",
    )


def _run_stage(name: str, args) -> None:
    cfg = load_config(profiles=args.config, overrides=args.overrides)

    if name == "critique-revise":
        from .stages import critique_revise
        critique_revise.run(cfg)
    elif name == "sft":
        from .stages import sft
        sft.run(cfg)
    elif name == "ai-feedback":
        from .stages import ai_feedback
        ai_feedback.run(cfg)
    elif name == "rl":
        method = cfg.rl.get("method", "dpo")
        if method == "dpo":
            from .stages import dpo
            dpo.run(cfg)
        elif method == "grpo":
            from .stages import grpo
            grpo.run(cfg)
        else:
            sys.exit(f"Unknown rl.method: {method!r} (expected 'dpo' or 'grpo')")
    elif name == "inspect-modules":
        from .models import list_linear_modules, load_model
        model = load_model(cfg)
        print("Linear modules (LoRA target candidates):")
        for n in list_linear_modules(model):
            print(f"  {n}")
    else:  # pragma: no cover - argparse guards this
        sys.exit(f"Unknown stage: {name}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="cai", description="Constitutional AI training pipeline")
    sub = parser.add_subparsers(dest="stage", required=True)
    for stage in ("critique-revise", "sft", "ai-feedback", "rl", "inspect-modules"):
        sp = sub.add_parser(stage, help=stage)
        _add_common(sp)

    args = parser.parse_args(argv)
    _run_stage(args.stage, args)


if __name__ == "__main__":
    main()
