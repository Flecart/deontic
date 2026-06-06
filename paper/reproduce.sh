#!/usr/bin/env bash
# Reproduce the experiments in deontic_institutions.tex (E1–E11).
# Offline pieces (engine build, E1 confidence intervals) need no API key.
# Formalization / annotator pieces need an LLM key:
#   export OPENAI_API_KEY=sk-...           # gpt-4.1 arms (E1 regen, E2, E4–E8, E10)
#   export OPENROUTER_API_KEY=sk-or-...    # DeepSeek V3 arms (E9, E11)
# Usage: bash paper/reproduce.sh            (runs what your keys allow; skips the rest)
set -uo pipefail
cd "$(dirname "$0")/.."                      # repo root
export PATH="$HOME/.elan/bin:$PATH"
CL=examples/clauses
EVAL=examples/codice_penale/eval/tools
have_openai=${OPENAI_API_KEY:+yes}
have_or=${OPENROUTER_API_KEY:+yes}
run() { echo; echo "### $1"; shift; "$@"; }
skip() { echo; echo "### SKIP $1 (need $2)"; }

echo "==== build engine ===="
lake build deontic || { echo "engine build failed"; exit 1; }

echo; echo "==== E1: eval metrics + Wilson 95% CIs (offline, uses committed predictions) ===="
( cd "$EVAL" && python3 ci_e1.py )
# To regenerate predictions from scratch (needs OPENAI_API_KEY):
#   ( cd "$EVAL" && python3 harness.py --dataset v0_pilot --arms llm_only,rag,deontic && python3 metrics.py ../results/predictions.jsonl )

echo; echo "==== formalization + annotator experiments ===="
if [ -n "$have_openai" ]; then
  run "E2  independent annotator (gpt-4.1)"        bash -c "cd '$EVAL' && python3 indep_annot.py"
  run "E4  scaffolded formalization"               python3 "$CL/formalize_probe.py"
  run "E5  unscaffolded formalization"             python3 "$CL/formalize_unscaffolded.py"
  run "E6  unscaffolded replication (2 clauses)"   python3 "$CL/replication_probe.py"
  run "E7  few-shot layer isolation"               python3 "$CL/fewshot_probe.py"
  run "E8  out-of-distribution CTD (gpt-4.1)"      python3 "$CL/ood_probe.py"
  run "E10 multi-clause contract"                  python3 "$CL/multiclause_probe.py"
else
  skip "E2/E4/E5/E6/E7/E8/E10" "OPENAI_API_KEY"
fi

if [ -n "$have_or" ]; then
  run "E9  out-of-distribution CTD (DeepSeek V3)" \
      env DEONTIC_LLM_PROVIDER=openrouter DEONTIC_LLM_MODEL=deepseek/deepseek-chat python3 "$CL/ood_probe.py"
  run "E11 cross-family independent annotator (DeepSeek V3)" \
      bash -c "cd '$EVAL' && DEONTIC_LLM_PROVIDER=openrouter DEONTIC_LLM_MODEL=deepseek/deepseek-chat python3 indep_annot.py"
else
  skip "E9/E11" "OPENROUTER_API_KEY"
fi

echo; echo "==== done. Findings are logged in docs/experiments/debate_ledger.md ===="
