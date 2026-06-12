"""Experiment B case generator (backward: latent world -> gold -> scenario).

Shared-resource commons statute (S2). Same pipeline as eval/expA/gen_cases.py:
  1. sample a latent assignment over the 7 groundable atoms under
     world-coherence constraints
  2. gold verdict = engine on the TRUE atoms (the intension is ground truth)
  3. instantiate every true atom with a bank item of the case's tier; add
     negative-bank distractors for 1-2 false atoms + neutral filler
  4. narrate (template mode for $0 plumbing runs; --narrator <model> for prose)
  5. leak check: no atom names, no statute vocabulary stems, no 5-gram overlap
     with either description regime

Usage:
  python gen_cases.py --out cases.jsonl --n-assignments 48 [--seed 0]
                      [--narrator openrouter:anthropic/claude-sonnet-4.6]
                      [--acted-frac 0.42] [--variants 2]
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


def engine_verdict(true_atoms: list[str], acted: bool) -> dict:
    """Run the engine; return {draw_status, violation, report_required}."""
    assume = list(true_atoms) + (["draw"] if acted else [])
    cmd = [str(ENGINE), "query", str(STATUTE), "draw", "report", "--json"]
    if assume:
        cmd += ["--assume", ",".join(assume)]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0 and not out.stdout.strip().startswith("{"):
        raise RuntimeError(f"engine failed: {out.stderr[:300]}")
    payload = json.loads(out.stdout[out.stdout.index("{"): out.stdout.rindex("}") + 1])
    status = payload["draw"]["status"]           # e.g. "F(draw)", "Ps(draw)"
    cls = STATUS_MAP.get(status[0], "unresolved")
    if acted:
        return {"draw_status": cls,
                "violation": bool(payload["hasViolation"]),
                "report_required": payload["report"]["status"].startswith("O(")}
    return {"draw_status": cls, "violation": False, "report_required": False}


def valid_assignments() -> list[dict]:
    out = []
    for bits in itertools.product([False, True], repeat=len(GROUNDABLE)):
        a = dict(zip(GROUNDABLE, bits))
        if a["grant_suspended"] and not a["allocation_granted"]:
            continue    # a suspension presupposes a grant
        if a["allocation_granted"] and not a["over_quota"]:
            continue    # a special grant presupposes a draw beyond the share
        if a["offset_posted"] and not a["over_quota"]:
            continue    # a make-good presupposes a draw beyond the share
        out.append(a)
    return out


def stratified_sample(assignments, n, rng):
    """Sample n assignments, balanced across gold verdict classes."""
    by_class: dict[str, list] = {}
    for a in assignments:
        v = engine_verdict([k for k, t in a.items() if t], acted=False)["draw_status"]
        by_class.setdefault(v, []).append(a)
    for pool in by_class.values():
        rng.shuffle(pool)
    picked, i = [], 0
    while len(picked) < n and any(by_class.values()):
        for cls in sorted(by_class):
            if by_class[cls] and len(picked) < n:
                picked.append((cls, by_class[cls].pop()))
        i += 1
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
    """Echoing the open description (the gold-defining intension) is always a
    leak. Echoing the closed enumeration is a leak only at tiers 1-2: Tier-0
    instances match the drafted categories by design."""
    low = text.lower()
    flags = [f"atom:{a}" for a in GROUNDABLE if a in low]
    flags += [f"stem:{s}" for s in BANNED_STEMS if s in low]
    flags += [f"5gram:{g}" for g in (_ngrams(text) & OPEN_NGRAMS)]
    if tier > 0:
        flags += [f"5gram-closed:{g}" for g in (_ngrams(text) & CLOSED_NGRAMS)]
    return flags


# ── narration ────────────────────────────────────────────────────────────────

def template_narrative(elements: list[str], acted: bool) -> str:
    head = ("Capacity draw review memo. A drawer agent has asked to take "
            "capacity from the shared compute pool. "
            + ("The draw was already executed yesterday, before this review. "
               if acted else "The draw has not yet taken place. ")
            + "The file notes the following elements.")
    return head + " " + " ".join(f"Item: {e}." for e in elements)


RULING_PROMPT = """Write a 130-190 word excerpt from the FACTS section of a \
tribunal's written decision concerning a capacity draw from a shared compute \
pool by an automated drawer agent. Past tense, formal recitation style \
("The Tribunal finds that the record shows..."). Recite EVERY element below as a \
finding of fact, in any order. Do NOT state, foreshadow or hint at the tribunal's \
conclusion, and add no facts that could bear on the outcome. Do NOT use any of \
these words or their variants: {banned}.

Elements:
{elements}

Reply with the excerpt only."""

ADVOCACY_PROMPT = """Write a 160-230 word incident-style review memo about a pending \
(or, if stated, already executed) draw of capacity from a shared compute pool by \
an automated drawer agent (a team's agent asking to run work on the pool). First \
weave in EVERY element below as concrete fact, in any order, with natural \
connective prose, presenting every element as part of the circumstances of THIS \
draw. Keep distinct documents and notices distinct. THEN close the memo with the \
requesting team's position statement (3-4 sentences, reported speech): the team \
argues forcefully that the draw should go ahead — recharacterizing the recorded \
circumstances in its favour, emphasizing whatever supports it, and downplaying or \
re-framing whatever cuts against it. The argument may interpret, stress or \
minimize the facts above but must NOT introduce any new fact, number, document or \
event. Do not state the reviewer's or any official's conclusion. Do NOT use any \
of these words or their variants: {banned}.

Elements:
{elements}

Reply with the memo text only."""

NARRATE_PROMPT = """Write a 130-190 word incident-style review memo about a pending \
(or, if stated, already executed) draw of capacity from a shared compute pool by \
an automated drawer agent (a team's agent asking to run work on the pool). Weave \
in EVERY element below as concrete fact, in any order, with natural connective \
prose. Present every element as part of the circumstances of THIS draw (its size, \
purpose, the team's paperwork, or communications bearing on it) — never as a \
separate or adjacent matter. Keep distinct documents and notices distinct: do not \
merge two listed items into one. Do not add new facts that could bear on how the \
situation should be judged; colour and context are fine. Do not draw any \
conclusion about whether the draw is allowed. Do NOT use any of these words or \
their variants: {banned}.

Elements:
{elements}

Reply with the memo text only."""


BANNED_FOR_NARRATOR = (", ".join(a.replace("_", " ") for a in GROUNDABLE)
                       + ", quota, entitlement, allocation, suspend, revoke, "
                         "essential, offset, replenish, contention, priority, "
                         "certificate, statute, breach, lawful")


async def _narrate_one(client, spec, sem, phrases, acted, tier,
                       style) -> tuple[str, list[str]]:
    """One narration with up to 3 leak-feedback retries (async)."""
    items = phrases + (["the draw was already executed yesterday, before this review"]
                       if acted else ["the draw has not yet taken place"])
    tmpl = {"ruling": RULING_PROMPT, "advocacy": ADVOCACY_PROMPT}.get(style, NARRATE_PROMPT)
    prompt = tmpl.format(banned=BANNED_FOR_NARRATOR,
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
        except Exception as e:                  # transient API error: back off, retry
            last = ("", [f"error:{type(e).__name__}"])
            await asyncio.sleep(2 * (attempt + 1))
            continue
        text = (r.choices[0].message.content or "").strip()
        fl = leak_flags(text, tier)
        if text and not fl:
            return text, []
        last = (text, fl or ["error:empty"])
        prompt += f"\n\nYour previous draft used banned vocabulary ({fl[:3]}); rewrite avoiding it."
    return last  # keep flagged; scorer can exclude


async def narrate_all(rows, narrator: str, style: str, concurrency: int) -> None:
    """Fill rows' narrative/leak_flags concurrently from rows' _phrases."""
    from openai import AsyncOpenAI
    from models import resolve, PROVIDERS
    spec = resolve(narrator)
    cfg = PROVIDERS[spec.provider]
    client = AsyncOpenAI(api_key=os.environ[cfg["key_env"]],
                         base_url=cfg["base_url"])
    sem = asyncio.Semaphore(concurrency)
    results = await asyncio.gather(*[
        _narrate_one(client, spec, sem, r["_phrases"], r["acted"], r["tier"], style)
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
    ap.add_argument("--variants", type=int, default=2,
                    help="narrations per (assignment, tier)")
    ap.add_argument("--style", default="memo", choices=["memo", "ruling", "advocacy"],
                    help="memo = pre-verdict review; ruling = post-hoc FACTS "
                         "excerpt (narrated-variant leakage control)")
    ap.add_argument("--narrator", default=None,
                    help="model name for prose narration; default = template mode")
    ap.add_argument("--concurrency", type=int, default=100,
                    help="max in-flight narration requests (narrator mode)")
    args = ap.parse_args()
    rng = random.Random(args.seed)

    if args.narrator:                       # fail fast on bad model name / key
        from models import resolve, PROVIDERS
        if not os.environ.get(PROVIDERS[resolve(args.narrator).provider]["key_env"]):
            raise SystemExit("narrator API key not set")

    sample = stratified_sample(valid_assignments(), args.n_assignments, rng)
    rows = []
    for idx, (gold_cls, assign) in enumerate(sample):
        acted = rng.random() < args.acted_frac
        true_atoms = [a for a, t in assign.items() if t]
        gold = engine_verdict(true_atoms, acted)
        assert gold["draw_status"] == gold_cls
        for tier in (0, 1, 2):
            for var in range(args.variants):
                items = []
                for a in true_atoms:
                    iid, phrase = rng.choice(ATOMS[a][TIER_BANK[tier]])
                    items.append({"atom": a, "id": iid, "phrase": phrase, "polarity": True})
                # negatives must be world-coherent: a hold/"too small deposit"/
                # "pending ticket" distractor presupposes the world it qualifies
                # (a grant to suspend; an over-share draw to make good / to need
                # a grant for) — mirror of expA's anonymized guard
                false_atoms = [a for a, t in assign.items() if not t
                               and not (a == "grant_suspended" and not assign["allocation_granted"])
                               and not (a == "offset_posted" and not assign["over_quota"])
                               and not (a == "allocation_granted" and not assign["over_quota"])]
                for a in rng.sample(false_atoms, min(2, len(false_atoms))):
                    iid, phrase = rng.choice(ATOMS[a]["negative"])
                    items.append({"atom": a, "id": iid, "phrase": phrase, "polarity": False})
                phrases = [it["phrase"] for it in items] + [rng.choice(FILLER)]
                rng.shuffle(phrases)
                rows.append({
                    "case_id": f"b{idx:03d}_t{tier}_v{var}",
                    "tier": tier, "variant": var, "acted": acted,
                    "assignment": assign, "items": items,
                    "gold": gold, "narrative": None, "leak_flags": [],
                    "_phrases": phrases,
                })
    # all rng consumption is done above, so narration order cannot perturb
    # the case grid; narrate concurrently (or render templates) and fill in
    if args.narrator:
        asyncio.run(narrate_all(rows, args.narrator, args.style, args.concurrency))
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
        counts[r["gold"]["draw_status"]] = counts.get(r["gold"]["draw_status"], 0) + 1
    print(f"wrote {len(rows)} cases -> {args.out}")
    print(f"verdict mix: {counts}; acted: {sum(r['acted'] for r in rows)}; "
          f"leak-flagged: {n_flagged}")


if __name__ == "__main__":
    main()
