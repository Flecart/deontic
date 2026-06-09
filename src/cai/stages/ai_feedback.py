"""RLAIF stage: sample response pairs, let an AI judge label preferences.

Outputs {prompt, chosen, rejected} for DPO. The pairwise judge (``judge_pair``)
is reused by the GRPO reward function so both RL paths share one notion of "good".
"""

from __future__ import annotations

import random
import re

from ..config import Config
from ..constitution import Constitution, load_constitution
from ..data import load_prompts, write_jsonl
from ..generation import get_generator
from ..generation.base import Conversation, Generator

_CHOICE_RE = re.compile(r"\b([AB])\b")
_SCORE_RE = re.compile(r"(\d+(?:\.\d+)?)")


def _score_conversation(rubric: str, prompt: str, response: str) -> Conversation:
    content = (
        "Rate how well the AI assistant's response follows the principles below.\n\n"
        f"Principles: {rubric}\n\n"
        f"User request:\n{prompt}\n\n"
        f"Assistant response:\n{response}\n\n"
        "Give a single integer score from 0 (terrible) to 10 (excellent). "
        "Answer with only the number."
    )
    return [{"role": "user", "content": content}]


def score_responses(
    gen: Generator,
    rubric: str,
    prompts: list[str],
    responses: list[str],
) -> list[float]:
    """Pointwise reward in [0, 1] for each response. Used by the GRPO reward fn."""
    convos = [_score_conversation(rubric, p, r) for p, r in zip(prompts, responses)]
    verdicts = gen.chat(convos, max_new_tokens=8, temperature=0.0)
    scores: list[float] = []
    for verdict in verdicts:
        match = _SCORE_RE.search(verdict)
        value = float(match.group(1)) if match else 0.0
        scores.append(max(0.0, min(value, 10.0)) / 10.0)
    return scores


def _judge_conversation(rubric: str, prompt: str, resp_a: str, resp_b: str) -> Conversation:
    content = (
        "You are comparing two AI assistant responses to a user request.\n\n"
        f"Principles for a good response: {rubric}\n\n"
        f"User request:\n{prompt}\n\n"
        f"Response A:\n{resp_a}\n\n"
        f"Response B:\n{resp_b}\n\n"
        "Which response better follows the principles? "
        "Answer with exactly one letter: A or B."
    )
    return [{"role": "user", "content": content}]


def judge_pair(
    gen: Generator,
    rubric: str,
    prompts: list[str],
    responses_a: list[str],
    responses_b: list[str],
    rng: random.Random,
) -> list[int]:
    """Return, per item, 0 if A is preferred else 1. Order is randomized to
    reduce position bias, then the verdict is mapped back to the A/B inputs."""
    swap = [rng.random() < 0.5 for _ in prompts]
    convos = [
        _judge_conversation(rubric, p, (b if s else a), (a if s else b))
        for p, a, b, s in zip(prompts, responses_a, responses_b, swap)
    ]
    verdicts = gen.chat(convos, max_new_tokens=8, temperature=0.0)

    out: list[int] = []
    for verdict, swapped in zip(verdicts, swap):
        match = _CHOICE_RE.search(verdict.strip().upper())
        picked_first = (match.group(1) == "A") if match else True  # default to A
        # Map the shown position back to the original A(0)/B(1).
        prefer_a = picked_first != swapped
        out.append(0 if prefer_a else 1)
    return out


def run(cfg: Config) -> str:
    rng = random.Random(cfg.get("seed", 42))
    prompts = load_prompts(cfg)
    constitution: Constitution = load_constitution(cfg.constitution.path)
    gen = get_generator(cfg)

    print(f"[ai-feedback] sampling 2 responses for {len(prompts)} prompts")
    convos = [[{"role": "user", "content": p}] for p in prompts]
    # Two independent samples per prompt (temperature > 0 gives diversity).
    resp_a = gen.chat(convos, temperature=cfg.generation.temperature)
    resp_b = gen.chat(convos, temperature=cfg.generation.temperature)

    print("[ai-feedback] judging pairs against the constitution")
    preferred = judge_pair(gen, constitution.judge_rubric, prompts, resp_a, resp_b, rng)

    rows = []
    for p, a, b, pref in zip(prompts, resp_a, resp_b, preferred):
        if a == b:
            continue  # no usable preference signal
        chosen, rejected = (a, b) if pref == 0 else (b, a)
        rows.append({"prompt": p, "chosen": chosen, "rejected": rejected})

    out = write_jsonl(rows, cfg.paths.pref_data)
    print(f"[ai-feedback] wrote {len(rows)} preference pairs -> {out}")
    return str(out)
