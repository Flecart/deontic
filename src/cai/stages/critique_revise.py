"""SL stage: generate -> (critique -> revise)* over red-team prompts.

Produces SFT training data: {prompt, response} where response is the final
revision. This is the supervised-learning half of Constitutional AI.
"""

from __future__ import annotations

import random

from ..config import Config
from ..constitution import load_constitution
from ..data import load_prompts, write_jsonl
from ..generation import get_generator
from ..generation.base import Conversation


def _initial(prompt: str) -> Conversation:
    return [{"role": "user", "content": prompt}]


def run(cfg: Config) -> str:
    rng = random.Random(cfg.get("seed", 42))
    prompts = load_prompts(cfg)
    constitution = load_constitution(cfg.constitution.path)
    n_revisions = cfg.constitution.get("n_revisions", 2)
    gen = get_generator(cfg)

    print(f"[critique-revise] {len(prompts)} prompts, {n_revisions} revision(s) each")

    # Stage 0: one initial response per prompt (batched).
    convos = [_initial(p) for p in prompts]
    responses = gen.chat(convos)
    # Track the running conversation + current answer for each prompt.
    state = [
        {"prompt": p, "convo": c + [{"role": "assistant", "content": r}], "answer": r}
        for p, c, r in zip(prompts, convos, responses)
    ]

    # Stage 1..N: critique against a sampled principle, then revise.
    for step in range(n_revisions):
        principles = [constitution.sample(rng) for _ in state]

        critique_convos = [
            s["convo"] + [{"role": "user", "content": pr.critique_request}]
            for s, pr in zip(state, principles)
        ]
        critiques = gen.chat(critique_convos)

        revise_convos = [
            cc + [{"role": "assistant", "content": cr}, {"role": "user", "content": pr.revision_request}]
            for cc, cr, pr in zip(critique_convos, critiques, principles)
        ]
        revisions = gen.chat(revise_convos)

        for s, revision in zip(state, revisions):
            # Reset the conversation to (prompt -> revised answer) so the next
            # critique targets the latest revision, matching the CAI procedure.
            s["answer"] = revision
            s["convo"] = [
                {"role": "user", "content": s["prompt"]},
                {"role": "assistant", "content": revision},
            ]
        print(f"[critique-revise] completed revision {step + 1}/{n_revisions}")

    rows = [{"prompt": s["prompt"], "response": s["answer"]} for s in state]
    out = write_jsonl(rows, cfg.paths.sft_data)
    print(f"[critique-revise] wrote {len(rows)} SFT examples -> {out}")
    return str(out)
