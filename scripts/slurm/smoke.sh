#!/bin/bash
# Tiny end-to-end smoke test. Run inside a GPU allocation, e.g.:
#   srun --partition=b200 --gres=gpu:1 --cpus-per-task=8 --time=1:00:00 \
#        --pty bash scripts/slurm/smoke.sh
#
# Stages run on the small proxy model (configs/smoke.yaml). Set SKIP_35B=0 to
# also run the bleeding-edge 35B load+generate compatibility check at the end.
set -euo pipefail
cd "$(dirname "$0")/../.."

module load cuda/13.0.2 2>/dev/null || true
export HF_HUB_ENABLE_HF_TRANSFER=1
SKIP_35B="${SKIP_35B:-1}"

echo "=============================================================="
echo "[smoke] 1/5 critique-revise (proxy)"
uv run cai critique-revise --config smoke

echo "[smoke] 2/5 sft (proxy, 2 steps)"
uv run cai sft --config smoke

echo "[smoke] 3/5 ai-feedback (proxy)"
uv run cai ai-feedback --config smoke

echo "[smoke] 4/5 rl -> DPO (proxy, 2 steps)"
uv run cai rl --config smoke --set rl.method=dpo

echo "[smoke] 5/5 rl -> GRPO switch (proxy, 2 steps)"
uv run cai rl --config smoke --set rl.method=grpo

if [[ "$SKIP_35B" == "0" ]]; then
  echo "=============================================================="
  echo "[smoke] 35B compat check: list LoRA target modules"
  uv run cai inspect-modules --config full
  echo "[smoke] 35B compat check: one critique-revise pass (1 prompt)"
  uv run cai critique-revise --config full \
    --set data.max_prompts=1 --set generation.max_new_tokens=64
fi

echo "=============================================================="
echo "[smoke] DONE. Artifacts under outputs/smoke/"
