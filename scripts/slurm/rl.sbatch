#!/bin/bash
#SBATCH --job-name=cai-rl
#SBATCH --output=/scratch/schmidt/ssci-michael/%x-%j.out
#SBATCH --error=/scratch/schmidt/ssci-michael/%x-%j.err
#SBATCH --partition=b200
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=12:00:00
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$(pwd)}"
module load cuda/13.0.2
export HF_HUB_ENABLE_HF_TRANSFER=1
# RL algorithm chosen by rl.method in configs/full.yaml; override here, e.g.:
#   sbatch scripts/slurm/rl.sbatch --set rl.method=grpo
srun uv run cai rl --config full "$@"
