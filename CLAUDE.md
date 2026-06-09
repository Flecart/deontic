# CLAUDE.md

Constitutional AI training scaffolding (critique-revision SFT + RLAIF via DPO/GRPO).

## Start here
Read `docs/architecture.md` first — it is the index of where everything lives.

## Keep docs current
`docs/architecture.md` MUST stay up to date. Whenever you add/remove/move a module
or stage, or change the pipeline flow or conventions, update that index in the same
change. Keep it a terse index (pointers only) — no deep detail.

## Environment
- Package/env manager: **uv** (system Python 3.9 is too old; uv pins 3.11). Run
  things with `uv run ...`; install with `uv sync` (+ `uv sync --extra vllm`).
- GPUs: SLURM partition `b200` (Blackwell, sm_100) → torch from the **cu128** index
  (already wired in `pyproject.toml`). `module load cuda/13.0.2`.
- Submit jobs with `scripts/slurm/*.sbatch`; quick check: `scripts/slurm/smoke.sh`.

## Commands
```
uv run cai critique-revise --config full      # SL data
uv run cai sft             --config full      # SL-CAI adapter
uv run cai ai-feedback     --config full --set model.adapter=outputs/full/sl-cai
uv run cai rl              --config full      # RL-CAI (rl.method = dpo|grpo)
uv run cai inspect-modules --config full      # list LoRA target candidates
uv run pytest                                 # CPU unit tests
```
`--config` merges `configs/<name>.yaml` over `base.yaml`; `--set k.v=x` overrides.

## Conventions
- Config-driven: stage code reads `cfg.*`; don't hardcode. Defaults in `configs/base.yaml`.
- Stages pass data via JSONL files in `cfg.paths`.
- Default model `Qwen/Qwen3.6-35B-A3B` is a multimodal MoE driven text-only with LoRA.
- Generation: vLLM preferred, auto-falls-back to HF transformers.
