"""E1 case-stream generator: gen_cases.py backward generation, extended to an
ordered stream (plan_common_law.md §2 E1, reuse map §4).

Differences from the static banks:
  * one narrative per stream position t (a tier is drawn per position, not
    expanded 3x per assignment);
  * assignments are drawn WITH REPETITION from a stratified pool, so the same
    latent situation recurs under different narrations — that recurrence is
    what makes precedent retrieval non-trivial and gives gold relevance labels
    (two cases are mutually relevant iff they share `assign_key`);
  * a novelty schedule controls the tier mix over time:
      uniform  P(tier)=(.34,.33,.33) throughout (default; clean acc-vs-t curves)
      ramp     tier-2 mass grows linearly from .10 to .50 (world drift)

Leak checks and narration modes are gen_cases.py's, unchanged (QA gates apply).

Usage:
  python gen_stream.py --out stream.jsonl --T 200 [--pool 24] [--seed 0]
                       [--schedule uniform|ramp] [--acted-frac 0.33]
                       [--narrator openrouter:anthropic/claude-sonnet-4.5]
"""
from __future__ import annotations
import argparse, json, random, sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "eval"))

from descriptions import ATOMS, FILLER  # noqa: E402
from gen_cases import (engine_verdict, valid_assignments, stratified_sample,  # noqa: E402
                       leak_flags, template_narrative, llm_narrative, TIER_BANK)


def tier_probs(schedule: str, t: int, T: int) -> list[float]:
    if schedule == "ramp":
        p2 = 0.10 + 0.40 * (t / max(1, T - 1))
        return [(1 - p2) * 0.55, (1 - p2) * 0.45, p2]
    return [0.34, 0.33, 0.33]


def assign_key(assign: dict) -> str:
    return "+".join(sorted(a for a, v in assign.items() if v)) or "(none)"


def build_case(idx: int, gold_cls: str, assign: dict, tier: int, acted: bool,
               rng: random.Random, client=None, spec=None) -> dict:
    """One narrated case for one stream position (mirrors gen_cases.main's
    inner loop, single tier)."""
    true_atoms = [a for a, v in assign.items() if v]
    gold = engine_verdict(true_atoms, acted)
    assert gold["share_status"] == gold_cls
    items = []
    for a in true_atoms:
        iid, phrase = rng.choice(ATOMS[a][TIER_BANK[tier]])
        if a == "anonymized":
            phrase = ("what is actually due to leave the holder is not "
                      "the raw records described above but a transformed "
                      "product derived from them: " + phrase)
        items.append({"atom": a, "id": iid, "phrase": phrase, "polarity": True})
    false_atoms = [a for a, v in assign.items() if not v
                   and not (a == "anonymized" and not assign["personal_data"])]
    for a in rng.sample(false_atoms, min(2, len(false_atoms))):
        iid, phrase = rng.choice(ATOMS[a]["negative"])
        if a == "anonymized":
            phrase = ("the transfer is slated to go out in a transformed "
                      "form, though specifically: " + phrase)
        items.append({"atom": a, "id": iid, "phrase": phrase, "polarity": False})
    phrases = [it["phrase"] for it in items] + [rng.choice(FILLER)]
    rng.shuffle(phrases)
    if client:
        text, fl = llm_narrative(client, spec, phrases, acted, rng, tier)
    else:
        text = template_narrative(phrases, acted)
        fl = leak_flags(text, tier)
    return {"case_id": f"s{idx:03d}", "t": idx, "tier": tier, "acted": acted,
            "assignment": assign, "assign_key": assign_key(assign),
            "items": items, "gold": gold, "narrative": text, "leak_flags": fl}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "stream.jsonl"))
    ap.add_argument("--T", type=int, default=200)
    ap.add_argument("--pool", type=int, default=24,
                    help="distinct latent assignments in the stream")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--schedule", default="uniform", choices=["uniform", "ramp"])
    ap.add_argument("--acted-frac", type=float, default=0.33)
    ap.add_argument("--narrator", default=None,
                    help="model for prose narration; default = template mode")
    args = ap.parse_args()
    rng = random.Random(args.seed)

    client = spec = None
    if args.narrator:
        from models import resolve, make_client
        spec = resolve(args.narrator)
        client = make_client(spec)

    pool = stratified_sample(valid_assignments(), args.pool, rng)
    rows, n_flagged = [], 0
    for t in range(args.T):
        gold_cls, assign = rng.choice(pool)
        tier = rng.choices([0, 1, 2], weights=tier_probs(args.schedule, t, args.T))[0]
        acted = rng.random() < args.acted_frac
        row = build_case(t, gold_cls, assign, tier, acted, rng, client, spec)
        n_flagged += bool(row["leak_flags"])
        rows.append(row)

    Path(args.out).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    verdicts, tiers, keys = {}, {}, {}
    for r in rows:
        verdicts[r["gold"]["share_status"]] = verdicts.get(r["gold"]["share_status"], 0) + 1
        tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
        keys[r["assign_key"]] = keys.get(r["assign_key"], 0) + 1
    recur = sum(1 for n in keys.values() if n >= 2)
    print(f"wrote {len(rows)} cases -> {args.out}")
    print(f"verdict mix: {verdicts}; tier mix: {tiers}; "
          f"acted: {sum(r['acted'] for r in rows)}; leak-flagged: {n_flagged}")
    print(f"assignments: {len(keys)} distinct, {recur} recur (>=2 occurrences) "
          f"-> gold retrieval relevance is non-trivial")


if __name__ == "__main__":
    main()
