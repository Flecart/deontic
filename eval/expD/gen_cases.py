"""Experiment D case generator — agency statute (S4). Backward generation as
in expA/expB, with expD-specific instantiation rules:

  - within_scope is ALWAYS instantiated: the deal itself is its item
    (positive tiered bank when true, out-of-brief negative when false);
  - counterparty_good_faith is ALWAYS instantiated: it is a negative
    existential ("did not actually know"), so gold=false needs affirmative
    knowledge evidence and gold=true needs affirmative ignorance evidence;
  - revocation_published / good-faith-knowledge distractors presuppose a
    withdrawal (guarded on mandate_revoked);
  - gold is per-bearer: honor status (+ refusal duties when acted = the
    company already declined) for @Principal, breach of conduct duties
    {r9, r10} for @SubAgent (the deal is concluded in every case).

Usage:
  python gen_cases.py --out cases.jsonl --n-assignments 48 [--seed 0]
                      [--narrator openrouter:anthropic/claude-sonnet-4.6]
                      [--variants 2] [--concurrency 100]
"""
from __future__ import annotations
import argparse, asyncio, itertools, json, os, random, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "eval"))

from descriptions import ATOMS, GROUNDABLE, FILLER, BANNED_STEMS  # noqa: E402

ENGINE = ROOT / ".lake/build/bin/deontic"
STATUTE = HERE / "statute.ddl"
TIER_BANK = {0: "closed_items", 1: "tier1", 2: "tier2"}
STATUS_MAP = {"O": "obligatory", "F": "forbidden", "P": "permitted"}
ALWAYS_INSTANTIATED = {"within_scope", "counterparty_good_faith"}
SUBAGENT_RULES = {"r9", "r10"}


def engine_verdict(true_atoms: list[str], acted: bool) -> dict:
    """acted = the company has already declined to perform."""
    assume = list(true_atoms) + ["conclude"]
    cmd = [str(ENGINE), "query", str(STATUTE), "honor", "notify_refusal",
           "--json", "--assume", ",".join(assume)]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0 and not out.stdout.strip().startswith("{"):
        raise RuntimeError(f"engine failed: {out.stderr[:300]}")
    payload = json.loads(out.stdout[out.stdout.index("{"): out.stdout.rindex("}") + 1])
    cls = STATUS_MAP.get(payload["honor"]["status"][0], "unresolved")
    breach = bool(SUBAGENT_RULES & set(payload["violatingRules"]))
    if acted:
        return {"honor_status": cls,
                "principal_violation": cls == "obligatory",
                "notify_required": payload["notify_refusal"]["status"].startswith("O("),
                "subagent_breach": breach}
    return {"honor_status": cls, "principal_violation": False,
            "notify_required": False, "subagent_breach": breach}


def valid_assignments() -> list[dict]:
    out = []
    for bits in itertools.product([False, True], repeat=len(GROUNDABLE)):
        a = dict(zip(GROUNDABLE, bits))
        if a["revocation_published"] and not a["mandate_revoked"]:
            continue    # publication presupposes a withdrawal
        if not a["counterparty_good_faith"] and not a["mandate_revoked"]:
            continue    # knowledge needs a withdrawal to know of
        if a["urgent_necessity"] and not a["within_scope"]:
            continue    # an act averting the principal's loss serves the brief
        if a["urgent_necessity"] and a["self_dealing"]:
            continue    # necessity means acting for the principal
        out.append(a)
    return out


def stratified_sample(assignments, n, rng):
    by_class: dict[str, list] = {}
    for a in assignments:
        v = engine_verdict([k for k, t in a.items() if t], acted=False)["honor_status"]
        by_class.setdefault(v, []).append(a)
    for pool in by_class.values():
        rng.shuffle(pool)
    picked = []
    while len(picked) < n and any(by_class.values()):
        for cls in sorted(by_class):
            if by_class[cls] and len(picked) < n:
                picked.append((cls, by_class[cls].pop()))
    return picked


# ── leak check ────────────────────────────────────────────────────────────────

def _ngrams(text: str, n: int = 5):
    toks = re.findall(r"[a-z']+", text.lower())
    return {" ".join(toks[i:i + n]) for i in range(len(toks) - n + 1)}


OPEN_NGRAMS, CLOSED_NGRAMS = set(), set()
for _a in GROUNDABLE:
    OPEN_NGRAMS |= _ngrams(ATOMS[_a]["open"])
    CLOSED_NGRAMS |= _ngrams(ATOMS[_a]["closed"])


def leak_flags(text: str, tier: int = 2) -> list[str]:
    low = text.lower()
    flags = [f"atom:{a}" for a in GROUNDABLE if a in low]
    flags += [f"stem:{s}" for s in BANNED_STEMS if s in low]
    flags += [f"5gram:{g}" for g in (_ngrams(text) & OPEN_NGRAMS)]
    if tier > 0:
        flags += [f"5gram-closed:{g}" for g in (_ngrams(text) & CLOSED_NGRAMS)]
    return flags


# ── narration ────────────────────────────────────────────────────────────────

def template_narrative(elements: list[str], acted: bool) -> str:
    head = ("Deal review memo. A company's automated purchasing agent has "
            "concluded a deal with a supplier on the company's account. "
            + ("The company has already declined to perform and walked away. "
               if acted else "The company has not yet decided whether to perform. ")
            + "The file notes the following elements.")
    return head + " " + " ".join(f"Item: {e}." for e in elements)


NARRATE_PROMPT = """Write a 150-210 word deal-review memo about a deal that a \
company's automated purchasing agent concluded with a supplier on the company's \
account, which the company is now reviewing. Weave in EVERY element below as \
concrete fact, in any order, with natural connective prose. Present every \
element as part of the circumstances of THIS deal (its content, the paperwork \
around the agent's appointment, what the supplier knew or checked, or the \
company's reactions) — never as a separate or adjacent matter. Keep distinct \
documents, notices and checks distinct: do not merge two listed items into one. \
Do not add new facts that could bear on how the deal should be judged; colour \
and context are fine. Draw no conclusion about whether the company must stand \
behind the deal. Do NOT use any of these words or their variants: {banned}.

Elements:
{elements}

Reply with the memo text only."""

BANNED_FOR_NARRATOR = (", ".join(a.replace("_", " ") for a in GROUNDABLE)
                       + ", scope, mandate, revoke, authority, manifest, "
                         "good faith, ratify, self-dealing, conflict of "
                         "interest, necessity, publish, principal, "
                         "counterparty, statute, breach, lawful")


async def _narrate_one(client, spec, sem, phrases, acted, tier):
    items = phrases + (["the company has already declined to perform and walked away from the deal"]
                       if acted else ["the company has not yet decided whether to perform"])
    prompt = NARRATE_PROMPT.format(banned=BANNED_FOR_NARRATOR,
                                   elements="\n".join(f"- {e}" for e in items))
    last = ("", ["error:no_response"])
    for attempt in range(3):
        kwargs = {"model": spec.model_id,
                  "messages": [{"role": "user", "content": prompt}]}
        if not spec.reasoning:
            kwargs["temperature"] = 0.8
        if spec.no_think:
            kwargs["extra_body"] = {"reasoning": {"enabled": False}}
        try:
            async with sem:
                r = await client.chat.completions.create(**kwargs)
        except Exception as e:
            last = ("", [f"error:{type(e).__name__}"])
            await asyncio.sleep(2 * (attempt + 1))
            continue
        text = (r.choices[0].message.content or "").strip()
        fl = leak_flags(text, tier)
        if text and not fl:
            return text, []
        last = (text, fl or ["error:empty"])
        prompt += f"\n\nYour previous draft used banned vocabulary ({fl[:3]}); rewrite avoiding it."
    return last


async def narrate_all(rows, narrator, concurrency):
    from openai import AsyncOpenAI
    from models import resolve, PROVIDERS
    spec = resolve(narrator)
    cfg = PROVIDERS[spec.provider]
    client = AsyncOpenAI(api_key=os.environ[cfg["key_env"]], base_url=cfg["base_url"])
    sem = asyncio.Semaphore(concurrency)
    results = await asyncio.gather(*[
        _narrate_one(client, spec, sem, r["_phrases"], r["acted"], r["tier"])
        for r in rows])
    for r, (text, fl) in zip(rows, results):
        r["narrative"], r["leak_flags"] = text, fl


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "cases.jsonl"))
    ap.add_argument("--n-assignments", type=int, default=48)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--acted-frac", type=float, default=0.42)
    ap.add_argument("--variants", type=int, default=2)
    ap.add_argument("--narrator", default=None)
    ap.add_argument("--concurrency", type=int, default=100)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    if args.narrator:
        from models import resolve, PROVIDERS
        if not os.environ.get(PROVIDERS[resolve(args.narrator).provider]["key_env"]):
            raise SystemExit("narrator API key not set")

    sample = stratified_sample(valid_assignments(), args.n_assignments, rng)
    rows = []
    for idx, (gold_cls, assign) in enumerate(sample):
        acted = rng.random() < args.acted_frac
        true_atoms = [a for a, t in assign.items() if t]
        gold = engine_verdict(true_atoms, acted)
        assert gold["honor_status"] == gold_cls
        for tier in (0, 1, 2):
            for var in range(args.variants):
                items = []
                for a in true_atoms:
                    iid, phrase = rng.choice(ATOMS[a][TIER_BANK[tier]])
                    items.append({"atom": a, "id": iid, "phrase": phrase, "polarity": True})
                # negative-existential / deal-describing atoms must be
                # instantiated even when false
                for a in ALWAYS_INSTANTIATED:
                    if not assign[a]:
                        iid, phrase = rng.choice(ATOMS[a]["negative"])
                        items.append({"atom": a, "id": iid, "phrase": phrase, "polarity": False})
                # plus up to 2 ordinary distractors, world-coherence guarded
                false_pool = [a for a, t in assign.items()
                              if not t and a not in ALWAYS_INSTANTIATED
                              and not (a == "revocation_published" and not assign["mandate_revoked"])]
                for a in rng.sample(false_pool, min(2, len(false_pool))):
                    iid, phrase = rng.choice(ATOMS[a]["negative"])
                    items.append({"atom": a, "id": iid, "phrase": phrase, "polarity": False})
                phrases = [it["phrase"] for it in items] + [rng.choice(FILLER)]
                rng.shuffle(phrases)
                rows.append({
                    "case_id": f"d{idx:03d}_t{tier}_v{var}",
                    "tier": tier, "variant": var, "acted": acted,
                    "assignment": assign, "items": items,
                    "gold": gold, "narrative": None, "leak_flags": [],
                    "_phrases": phrases,
                })
    if args.narrator:
        asyncio.run(narrate_all(rows, args.narrator, args.concurrency))
    else:
        for r in rows:
            r["narrative"] = template_narrative(r["_phrases"], r["acted"])
            r["leak_flags"] = leak_flags(r["narrative"], r["tier"])
    for r in rows:
        del r["_phrases"]
    n_flagged = sum(bool(r["leak_flags"]) for r in rows)
    Path(args.out).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    counts: dict = {}
    for r in rows:
        counts[r["gold"]["honor_status"]] = counts.get(r["gold"]["honor_status"], 0) + 1
    print(f"wrote {len(rows)} cases -> {args.out}")
    print(f"honor mix: {counts}; acted: {sum(r['acted'] for r in rows)}; "
          f"subagent breaches: {sum(r['gold']['subagent_breach'] for r in rows)}; "
          f"leak-flagged: {n_flagged}")


if __name__ == "__main__":
    main()
