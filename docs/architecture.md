# Architecture — index

Concise map of the repo. This is an index, not documentation: it says *where to
look*, not how things work in detail. Open the named file to learn the details.

## Pipeline (data flows top to bottom)
1. **critique-revise** → `src/cai/stages/critique_revise.py` → writes `paths.sft_data`
2. **sft** → `src/cai/stages/sft.py` → writes `paths.sft_model` (SL-CAI adapter)
3. **ai-feedback** → `src/cai/stages/ai_feedback.py` → writes `paths.pref_data`
4. **rl** → `src/cai/stages/dpo.py` or `grpo.py` → writes `paths.rl_model` (RL-CAI)

## Where to look
| Concern | Look in |
|---|---|
| CLI / stage dispatch | `src/cai/cli.py` |
| Config model + YAML merge + `--set` | `src/cai/config.py`, `configs/*.yaml` |
| Constitution principles + loader | `constitution/default.yaml`, `src/cai/constitution.py` |
| Red-team prompt loading (seed/HF) | `src/cai/data.py`, `data/red_team_seed.jsonl` |
| Model + LoRA + adapter loading | `src/cai/models.py` |
| Generation backends (vLLM/HF) | `src/cai/generation/` |
| RLAIF judge (pairwise + pointwise) | `src/cai/stages/ai_feedback.py` |
| SLURM / run scripts | `scripts/slurm/` (`smoke.sh` = e2e) |
| Tests | `tests/test_pipeline.py` |
| Deps / env / torch index | `pyproject.toml` |

## Key conventions
- Everything is config-driven; stage code reads `cfg.*` only.
- Stages communicate via JSONL files named in `cfg.paths`.
- RL algorithm switch: `rl.method: dpo|grpo`.
- Generation works in chat messages; backends apply the chat template.
- Target model is a multimodal MoE driven text-only; see `models.py` auto-class logic.
