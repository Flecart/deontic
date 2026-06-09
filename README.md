# Constitutional AI training

A config-driven, runnable scaffold for **Constitutional AI** (Bai et al. 2022):

1. **SL / critique-revision** — generate answers to red-team prompts, have the
   model critique its answer against a sampled constitutional principle, revise,
   then SFT on the revisions → **SL-CAI** adapter.
2. **RLAIF** — the SL-CAI model samples response pairs, an AI judge labels which
   better follows the constitution, then preference-optimize (**DPO** by default,
   **GRPO** via a one-line config switch) → **RL-CAI** adapter.

LoRA throughout; the default target model is the multimodal MoE
`Qwen/Qwen3.6-35B-A3B`, driven text-only.

## Cheatsheet (this SLURM environment)
```bash
# --- one-time setup (login node has internet) ---
curl -LsSf https://astral.sh/uv/install.sh | sh   # install uv (if missing)
uv sync                      # core deps; torch comes from the cu128 (Blackwell) index
uv sync --extra vllm         # add the vLLM backend (torchvision/torchaudio also cu128)

# --- everyday, no GPU (login node) ---
uv run pytest                                  # CPU unit tests
uv run cai --help                              # list stages
uv run cai inspect-modules --config smoke      # (needs GPU) list LoRA target modules

# --- grab an interactive GPU (B200) for quick tests ---
srun --partition=b200 --gres=gpu:1 --cpus-per-task=8 --time=1:00:00 --pty bash
#   inside it:  module load cuda/13.0.2 ; cd <repo> ; uv run cai <stage> --config smoke

# --- full tiny end-to-end smoke test on one GPU ---
srun --partition=b200 --gres=gpu:1 --cpus-per-task=8 --time=1:00:00 \
     --export=ALL bash scripts/slurm/smoke.sh        # set SKIP_35B=0 to also test the 35B

# --- submit the real pipeline as batch jobs (run in order) ---
sbatch scripts/slurm/critique_revise.sbatch    # -> outputs/full/sft.jsonl
sbatch scripts/slurm/sft.sbatch                # -> outputs/full/sl-cai (adapter)
sbatch scripts/slurm/ai_feedback.sbatch        # -> outputs/full/prefs.jsonl
sbatch scripts/slurm/rl.sbatch                 # -> outputs/full/rl-cai  (add: --set rl.method=grpo)

# --- monitor / inspect ---
squeue -u "$USER"                              # your jobs
sinfo -p b200                                  # GPU partition state
tail -f /scratch/schmidt/ssci-michael/cai-*.out   # sbatch job logs
scancel <jobid>                                # cancel a job
```
Config knobs: `--config <name>` merges `configs/<name>.yaml` over `base.yaml`;
`--set a.b=c` overrides any value (e.g. `--set rl.method=grpo`, `--set data.source=hf`).

## Quickstart
```bash
uv sync                 # core deps (torch cu128 for Blackwell)
uv sync --extra vllm    # optional fast generation backend (best-effort)
uv run pytest           # CPU unit tests

# Tiny end-to-end smoke test on a GPU node:
srun --partition=b200 --gres=gpu:1 --cpus-per-task=8 --time=1:00:00 \
     --pty bash scripts/slurm/smoke.sh
```

## Full run (SLURM, b200)
```bash
sbatch scripts/slurm/critique_revise.sbatch
sbatch scripts/slurm/sft.sbatch
sbatch scripts/slurm/ai_feedback.sbatch
sbatch scripts/slurm/rl.sbatch                 # add: --set rl.method=grpo
```

## Layout
See **`docs/architecture.md`** for the index of where everything lives.
Configuration lives in `configs/` (`base.yaml` ← `smoke.yaml`/`full.yaml` ← `--set`).
The constitution is plain data in `constitution/default.yaml`.
