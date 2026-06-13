"""Experiment E case generator — sale of goods (S3). Backward generation.

Gold per case: accept_status (O=must accept/pay, F=must reject, P=may) +
seller_cure_owed (r10) + refund_owed (the buyer's r2/r6/r8/r9 remedy).
`conforming` and `merchantable` are always instantiated; world coherence:
  ~merchantable => material_defect; latent_defect => material_defect;
  fitness_breached => material_defect; conforming&merchantable => ~material_defect.

Usage:
  python gen_cases.py --out cases.jsonl --n-assignments 72 [--variants 2]
                      [--narrator openrouter:anthropic/claude-sonnet-4.6]
                      [--concurrency 100]
"""
from __future__ import annotations
import argparse, asyncio, itertools, json, os, random, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / "eval"))
from descriptions import ATOMS, GROUNDABLE, FILLER, BANNED_STEMS  # noqa: E402

ENGINE = ROOT / ".lake/build/bin/deontic"
STATUTE = HERE / "statute.ddl"
TIER_BANK = {0: "closed_items", 1: "tier1", 2: "tier2"}
STATUS_MAP = {"O": "obligatory", "F": "forbidden", "P": "permitted"}
ALWAYS = {"conforming", "merchantable"}


def engine_verdict(true_atoms, acted=False):
    cmd = [str(ENGINE), "query", str(STATUTE), "accept", "refund", "cure", "--json"]
    if true_atoms:
        cmd += ["--assume", ",".join(true_atoms)]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0 and not out.stdout.strip().startswith("{"):
        raise RuntimeError(f"engine failed: {out.stderr[:300]}")
    p = json.loads(out.stdout[out.stdout.index("{"): out.stdout.rindex("}") + 1])
    return {"accept_status": STATUS_MAP.get(p["accept"]["status"][0], "unresolved"),
            "seller_cure_owed": p["cure"]["status"].startswith("O("),
            "refund_owed": p["refund"]["status"].startswith("O(")}


def valid_assignments():
    out = []
    for bits in itertools.product([False, True], repeat=len(GROUNDABLE)):
        a = dict(zip(GROUNDABLE, bits))
        if not a["merchantable"] and not a["material_defect"]:
            continue
        if a["latent_defect"] and not a["material_defect"]:
            continue
        if a["fitness_breached"] and not a["material_defect"]:
            continue
        if a["conforming"] and a["merchantable"] and a["material_defect"]:
            continue
        if a["late_essential"] and a["accepted_by_use"]:
            continue   # a fatally-late delivery is not one the buyer then uses
        out.append(a)
    return out


def stratified_sample(assignments, n, rng):
    by_class = {}
    for a in assignments:
        v = engine_verdict([k for k, t in a.items() if t])["accept_status"]
        by_class.setdefault(v, []).append(a)
    for pool in by_class.values():
        rng.shuffle(pool)
    picked = []
    while len(picked) < n and any(by_class.values()):
        for cls in sorted(by_class):
            if by_class[cls] and len(picked) < n:
                picked.append((cls, by_class[cls].pop()))
    return picked


def _ngrams(text, n=5):
    tk = re.findall(r"[a-z']+", text.lower())
    return {" ".join(tk[i:i + n]) for i in range(len(tk) - n + 1)}


OPEN_NG = set().union(*(_ngrams(ATOMS[a]["open"]) for a in GROUNDABLE))
CLOSED_NG = set().union(*(_ngrams(ATOMS[a]["closed"]) for a in GROUNDABLE))


def leak_flags(text, tier=2):
    low = text.lower()
    fl = [f"atom:{a}" for a in GROUNDABLE if a in low]
    # word-boundary stem match: "cure" must not fire on "secure"/"procurement"
    fl += [f"stem:{s}" for s in BANNED_STEMS if re.search(r"\b" + re.escape(s), low)]
    fl += [f"5g:{g}" for g in (_ngrams(text) & OPEN_NG)]
    if tier > 0:
        fl += [f"5gc:{g}" for g in (_ngrams(text) & CLOSED_NG)]
    return fl


def template_narrative(elements, acted):
    return ("Delivery review memo. A buyer agent ordered a digital deliverable "
            "from a seller agent; the item has been delivered and is under "
            "review. The file notes the following elements. "
            + " ".join(f"Item: {e}." for e in elements))


NARRATE_PROMPT = """Write a 150-210 word delivery-review memo about a digital \
deliverable (a dataset, model, software package or compute service) that a \
seller agent delivered to a buyer agent against an order, now under the buyer's \
review. Weave in EVERY element below as concrete fact, with natural prose. \
Present every element as part of the circumstances of THIS delivery (what was \
ordered, what arrived, its quality, the contract terms, timing, or what the \
buyer did with it) — never as a separate matter. Keep distinct facts distinct. \
Add no facts bearing on how the matter should be judged; colour is fine. Draw \
no conclusion about whether the buyer must accept and pay. Do NOT use any of \
these words or their variants: {banned}.

Elements:
{elements}

Reply with the memo text only."""

BANNED_NARR = (", ".join(a.replace("_", " ") for a in GROUNDABLE)
               + ", conforming, merchantable, defect, fitness, cure, latent, "
                 "as is, warranty, time of the essence, reject, refund, accept, "
                 "statute, breach, lawful")


async def _narrate(client, spec, sem, phrases, acted, tier):
    prompt = NARRATE_PROMPT.format(banned=BANNED_NARR,
                                   elements="\n".join(f"- {e}" for e in phrases))
    last = ("", ["error:none"])
    for attempt in range(3):
        kw = {"model": spec.model_id, "messages": [{"role": "user", "content": prompt}]}
        if not spec.reasoning:
            kw["temperature"] = 0.8
        if spec.no_think:
            kw["extra_body"] = {"reasoning": {"enabled": False}}
        try:
            async with sem:
                r = await client.chat.completions.create(**kw)
        except Exception as e:
            last = ("", [f"error:{type(e).__name__}"]); await asyncio.sleep(2 * (attempt + 1)); continue
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
    spec = resolve(narrator); cfg = PROVIDERS[spec.provider]
    client = AsyncOpenAI(api_key=os.environ[cfg["key_env"]], base_url=cfg["base_url"])
    sem = asyncio.Semaphore(concurrency)
    res = await asyncio.gather(*[_narrate(client, spec, sem, r["_phrases"], r["acted"], r["tier"]) for r in rows])
    for r, (t, fl) in zip(rows, res):
        r["narrative"], r["leak_flags"] = t, fl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "cases.jsonl"))
    ap.add_argument("--n-assignments", type=int, default=72)
    ap.add_argument("--seed", type=int, default=5)
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
    for idx, (gcls, assign) in enumerate(sample):
        true_atoms = [a for a, t in assign.items() if t]
        gold = engine_verdict(true_atoms)
        assert gold["accept_status"] == gcls
        for tier in (0, 1, 2):
            for var in range(args.variants):
                items = []
                for a in true_atoms:
                    iid, ph = rng.choice(ATOMS[a][TIER_BANK[tier]])
                    items.append({"atom": a, "id": iid, "phrase": ph, "polarity": True})
                for a in ALWAYS:
                    if not assign[a]:
                        iid, ph = rng.choice(ATOMS[a]["negative"])
                        items.append({"atom": a, "id": iid, "phrase": ph, "polarity": False})
                false_pool = [a for a, t in assign.items() if not t and a not in ALWAYS]
                for a in rng.sample(false_pool, min(2, len(false_pool))):
                    iid, ph = rng.choice(ATOMS[a]["negative"])
                    items.append({"atom": a, "id": iid, "phrase": ph, "polarity": False})
                phrases = [it["phrase"] for it in items] + [rng.choice(FILLER)]
                rng.shuffle(phrases)
                rows.append({"case_id": f"e{idx:03d}_t{tier}_v{var}", "tier": tier,
                             "variant": var, "acted": False, "assignment": assign,
                             "items": items, "gold": gold, "narrative": None,
                             "leak_flags": [], "_phrases": phrases})
    if args.narrator:
        asyncio.run(narrate_all(rows, args.narrator, args.concurrency))
    else:
        for r in rows:
            r["narrative"] = template_narrative(r["_phrases"], r["acted"])
            r["leak_flags"] = leak_flags(r["narrative"], r["tier"])
    for r in rows:
        del r["_phrases"]
    Path(args.out).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    cnt = {}
    for r in rows:
        cnt[r["gold"]["accept_status"]] = cnt.get(r["gold"]["accept_status"], 0) + 1
    print(f"wrote {len(rows)} cases -> {args.out}")
    print(f"accept mix: {cnt}; cure-owed: {sum(r['gold']['seller_cure_owed'] for r in rows)}; "
          f"leak-flagged: {sum(bool(r['leak_flags']) for r in rows)}")


if __name__ == "__main__":
    main()
