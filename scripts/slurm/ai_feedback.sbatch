#!/bin/bash
#SBATCH --job-name=cai-ai-feedback
#SBATCH --output=/scratch/schmidt/ssci-michael/%x-%j.out
#SBATCH --error=/scratch/schmidt/ssci-michael/%x-%j.err
#SBATCH --partition=b200
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=4:00:00
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$(pwd)}"
module load cuda/13.0.2
export HF_HUB_ENABLE_HF_TRANSFER=1
# Sample from the SL-CAI policy: base model + the trained SFT LoRA adapter.
srun uv run cai ai-feedback --config full --set model.adapter=outputs/full/sl-cai "$@"
