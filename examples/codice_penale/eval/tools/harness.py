#!/usr/bin/env python3
"""harness — run the three arms over a dataset, write results/predictions.jsonl.

Arms (same base model; same encoded norms in context so LLM-only isn't starved):
  - llm_only : narrative + the offence's atom glosses        -> verdict JSON
  - rag      : + top-k retrieved articles from the full code  -> verdict JSON
  - deontic  : narrative -> atom assignments (grounding), then the ENGINE computes
               the verdict (reuses backward_gen). `pred_atoms` recorded so grounding
               is scored separately from deduction.

Each prediction row: {id, arm, raw, pred_verdict, pred_offence, pred_atoms?,
input_tokens, output_tokens, latency_s}.

Usage:
  python3 harness.py --dataset v0_pilot --arms llm_only,rag,deontic [--limit N]
Requires an API key for the LLM arms (see llm.py). The deontic arm's engine step
needs `lake build deontic`.
"""
from __future__ import annotations

import argparse
import json
import os
import re

import backward_gen as bg
import offences as off
import retrieval

HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = os.path.normpath(os.path.join(HERE, ".."))
PROMPTS = os.path.join(EVAL, "prompts")
RESULTS = os.path.join(EVAL, "results")


def _load_prompt(name: str) -> str:
    with open(os.path.join(PROMPTS, name), encoding="utf-8") as f:
        return f.read()


def _atoms_block(file_rel: str) -> str:
    atoms = off.groundable_atoms_for_file(file_rel)
    return "\n".join(f"- {a}: {g}" for a, g in atoms.items())


def _parse_json(text: str) -> dict | None:
    """Extract the first JSON object from an LLM reply (tolerates code fences)."""
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE)
    start = text.find("{")
    if start < 0:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
        return obj
    except Exception:
        return None


def run_llm_only(item, prompt, llm) -> dict:
    sys = prompt.replace("{atoms}", _atoms_block(item["theory"]))
    user = f"FATTO:\n{item['narrative']}\n\nDOMANDA: {item['question']}"
    c = llm.complete(sys, user)
    obj = _parse_json(c.text) or {}
    return _verdict_row(item, "llm_only", c, obj.get("verdict"), obj.get("offence"))


def run_rag(item, prompt, llm) -> dict:
    arts = retrieval.search(item["narrative"] + " " + item["question"], k=4)
    statute = "\n\n".join(f"[art. {n}]\n{txt}" for n, txt in arts)
    sys = prompt.replace("{atoms}", _atoms_block(item["theory"])).replace("{statute}", statute)
    user = f"FATTO:\n{item['narrative']}\n\nDOMANDA: {item['question']}"
    c = llm.complete(sys, user)
    obj = _parse_json(c.text) or {}
    return _verdict_row(item, "rag", c, obj.get("verdict"), obj.get("offence"))


def run_deontic(item, prompt, llm) -> dict:
    atoms = off.groundable_atoms_for_file(item["theory"])
    sys = prompt.replace("{atoms}", "\n".join(f"- {a}: {g}" for a, g in atoms.items()))
    user = f"FATTO:\n{item['narrative']}"
    c = llm.complete(sys, user)
    obj = _parse_json(c.text) or {}
    pred_atoms = {a: int(bool(obj.get(a, 0))) for a in atoms}
    present = [a for a, v in pred_atoms.items() if v]
    # The engine, not the LLM, computes the verdict from the grounded atoms.
    g = bg.verdict_auto(item["theory"], present, off.penalties_for_file(item["theory"]))
    row = _verdict_row(item, "deontic", c, g["verdict"], g["offence"])
    row["pred_atoms"] = pred_atoms
    return row


def _verdict_row(item, arm, c, verdict, offence) -> dict:
    return {
        "id": item["id"], "arm": arm, "raw": c.text,
        "pred_verdict": verdict, "pred_offence": offence,
        "input_tokens": c.input_tokens, "output_tokens": c.output_tokens,
        "latency_s": round(c.latency_s, 3),
    }


ARMS = {"llm_only": (run_llm_only, "arm_llm_only.md"),
        "rag": (run_rag, "arm_rag.md"),
        "deontic": (run_deontic, "arm_ground.md")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="v0_pilot")
    ap.add_argument("--arms", default="llm_only,rag,deontic")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default=os.path.join(RESULTS, "predictions.jsonl"))
    args = ap.parse_args()

    import llm  # imported here so engine-only tooling needn't have the SDK installed

    path = os.path.join(EVAL, "dataset", f"{args.dataset}.jsonl")
    items = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    if args.limit:
        items = items[:args.limit]
    arms = [a.strip() for a in args.arms.split(",") if a.strip()]

    os.makedirs(RESULTS, exist_ok=True)
    n = 0
    with open(args.out, "w", encoding="utf-8") as fout:
        for item in items:
            for arm in arms:
                fn, pfile = ARMS[arm]
                prompt = _load_prompt(pfile)
                try:
                    row = fn(item, prompt, llm)
                except Exception as ex:
                    row = {"id": item["id"], "arm": arm, "raw": f"ERROR: {ex}",
                           "pred_verdict": None, "pred_offence": None,
                           "input_tokens": 0, "output_tokens": 0, "latency_s": 0.0}
                fout.write(json.dumps(row, ensure_ascii=False) + "\n")
                fout.flush()
                n += 1
                print(f"{item['id']:13} {arm:9} -> {row.get('pred_verdict')}")
    print(f"\nwrote {n} predictions -> {os.path.relpath(args.out, off.REPO)}")


if __name__ == "__main__":
    main()
