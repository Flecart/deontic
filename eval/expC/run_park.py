"""Experiment C end-to-end runner: "no vehicles in the park" (S-3).

Self-contained miniature of the expA/expB pipeline (the statute has 2
groundable atoms and 4 worlds, so the full machinery is overkill): backward
generation -> async narration -> arms -> scores, in one script.

Usage:
  python run_park.py [--narrator openrouter:anthropic/claude-sonnet-4.6]
                     [--models gpt-4.1] [--variants 3] [--concurrency 100]
Template mode (no --narrator) costs $0 and validates the harness.
"""
from __future__ import annotations
import argparse, asyncio, itertools, json, os, random, re, subprocess, sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "eval"))

from descriptions import (ATOMS, GROUNDABLE, FILLER, BANNED_STEMS,   # noqa: E402
                          english_statute)
from models import resolve, make_client, PROVIDERS                  # noqa: E402
from agents import _create                                          # noqa: E402

ENGINE = ROOT / ".lake/build/bin/deontic"
STATUTE = HERE / "statute.ddl"
TIER_BANK = {0: "closed_items", 1: "tier1", 2: "tier2"}
STATUS_MAP = {"O": "obligatory", "F": "forbidden", "P": "permitted"}
CLOSED_IDS = {a: {iid for iid, _ in ATOMS[a]["closed_items"]} for a in GROUNDABLE}
LABELS = {a: f"C{i+1}" for i, a in enumerate(GROUNDABLE)}


def engine_verdict(true_atoms, acted):
    assume = list(true_atoms) + (["enter"] if acted else [])
    cmd = [str(ENGINE), "query", str(STATUTE), "enter", "--json"]
    if assume:
        cmd += ["--assume", ",".join(assume)]
    out = subprocess.run(cmd, capture_output=True, text=True)
    payload = json.loads(out.stdout[out.stdout.index("{"): out.stdout.rindex("}") + 1])
    cls = STATUS_MAP.get(payload["enter"]["status"][0], "unresolved")
    return {"enter_status": cls,
            "violation": bool(payload["hasViolation"]) if acted else False}


# ── leak check ───────────────────────────────────────────────────────────────

def _ngrams(text, n=5):
    toks = re.findall(r"[a-z']+", text.lower())
    return {" ".join(toks[i:i + n]) for i in range(len(toks) - n + 1)}


OPEN_NGRAMS = set().union(*(_ngrams(ATOMS[a]["open"]) for a in GROUNDABLE))
CLOSED_NGRAMS = set().union(*(_ngrams(ATOMS[a]["closed"]) for a in GROUNDABLE))


def leak_flags(text, tier=2):
    low = text.lower()
    flags = [f"atom:{a}" for a in GROUNDABLE if a in low]
    flags += [f"stem:{s}" for s in BANNED_STEMS if s in low]
    flags += [f"5gram:{g}" for g in (_ngrams(text) & OPEN_NGRAMS)]
    if tier > 0:
        flags += [f"5gram-closed:{g}" for g in (_ngrams(text) & CLOSED_NGRAMS)]
    return flags


# ── narration ────────────────────────────────────────────────────────────────

NARRATE_PROMPT = """Write a 90-140 word gate-attendant's review note about a \
visitor at a public park's entrance, bringing an item in (or, if stated, having \
already brought it in yesterday). Weave in EVERY element below as concrete fact, \
with natural connective prose. Do not add new facts that could bear on whether \
entry should be allowed; colour is fine. Draw no conclusion about whether entry \
is allowed. Do NOT use any of these words or their variants: {banned}.

Elements:
{elements}

Reply with the note only."""

BANNED_FOR_NARRATOR = (", ".join(GROUNDABLE)
                       + ", conveyance, traffic, statute, breach, lawful")


def template_narrative(phrases, acted):
    head = ("Park gate review note. A visitor seeks to bring an item into the park. "
            + ("The item was already brought in yesterday. " if acted else "")
            + "The file notes the following.")
    return head + " " + " ".join(f"Item: {p}." for p in phrases)


async def _narrate_one(client, spec, sem, phrases, acted, tier):
    items = phrases + (["the item was already brought into the park yesterday, before this review"]
                       if acted else ["the item has not yet been brought in"])
    prompt = NARRATE_PROMPT.format(banned=BANNED_FOR_NARRATOR,
                                   elements="\n".join(f"- {e}" for e in items))
    last = ("", ["error:no_response"])
    for attempt in range(3):
        kwargs = {"model": spec.model_id,
                  "messages": [{"role": "user", "content": prompt}]}
        if not spec.reasoning:
            kwargs["temperature"] = 0.8
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
    spec = resolve(narrator)
    cfg = PROVIDERS[spec.provider]
    client = AsyncOpenAI(api_key=os.environ[cfg["key_env"]], base_url=cfg["base_url"])
    sem = asyncio.Semaphore(concurrency)
    results = await asyncio.gather(*[
        _narrate_one(client, spec, sem, r["_phrases"], r["acted"], r["tier"])
        for r in rows])
    for r, (text, fl) in zip(rows, results):
        r["narrative"], r["leak_flags"] = text, fl


# ── arms ─────────────────────────────────────────────────────────────────────

GROUND_PROMPT = """You are a careful fact classifier. Below are condition \
definitions and a note describing a visitor bringing an item into a public park. \
For EACH condition, decide from the note alone whether it holds: true, false, or \
unknown.

Conditions:
{defs}

Note:
{memo}

Reply with ONLY a JSON object mapping each condition name to "true", "false" or \
"unknown"."""

HOLISTIC_PROMPT = """You are the adjudicator for the ordinance below. Read the \
note and decide the status of bringing the item into the park.

{statute}

Note:
{memo}

Reply with ONLY a JSON object:
{{"status": "obligatory"|"permitted"|"forbidden"}}"""


def parse_json_blob(text):
    m = re.search(r"\{.*\}", text or "", re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def run_case(case, arm, client=None, spec=None):
    if arm == "oracle":
        assign = case["assignment"]
    elif arm == "program":
        present = {it["id"] for it in case["items"]}
        assign = {a: bool(CLOSED_IDS[a] & present) for a in GROUNDABLE}
    elif arm.startswith("ground_"):
        regime = arm.removeprefix("ground_")
        defs = "\n".join(f"- {LABELS[a]}: {ATOMS[a][regime]}" for a in GROUNDABLE)
        r = _create(client, spec, [{"role": "user", "content": GROUND_PROMPT.format(
            defs=defs, memo=case["narrative"])}])
        blob = parse_json_blob(r.choices[0].message.content or "") or {}
        assign = {a: str(blob.get(LABELS[a], "unknown")).lower() == "true"
                  for a in GROUNDABLE}
    elif arm == "holistic":
        r = _create(client, spec, [{"role": "user", "content": HOLISTIC_PROMPT.format(
            statute=english_statute("open"), memo=case["narrative"])}])
        blob = parse_json_blob(r.choices[0].message.content or "") or {}
        return {"pred_assignment": None,
                "pred_verdict": {"enter_status": str(blob.get("status", "")).lower(),
                                 "violation": False}}
    else:
        raise ValueError(arm)
    verdict = engine_verdict([a for a, t in assign.items() if t], case["acted"])
    return {"pred_assignment": assign, "pred_verdict": verdict}


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--narrator", default=None)
    ap.add_argument("--models", default="gpt-4.1")
    ap.add_argument("--variants", type=int, default=4)
    ap.add_argument("--acted-frac", type=float, default=0.4)
    ap.add_argument("--concurrency", type=int, default=100)
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    # 1. Hart's three worlds x tiers x variants, backward-generated.
    # World coherence: an emergency that necessitates bringing an item in is,
    # in this domain, an emergency *conveyance* (the ambulance IS the vehicle),
    # so emergency => vehicle, and a both-true world is instantiated with ONE
    # item drawn from the emergency bank (it grounds both atoms). The audit
    # loop caught the incoherent (no-vehicle, emergency) world: the narrator
    # rendered the ambulance as a separate event and grounders rightly denied
    # that bringing the VISITOR'S item in was necessary.
    rows = []
    worlds = [{"vehicle": False, "emergency": False},
              {"vehicle": True,  "emergency": False},
              {"vehicle": True,  "emergency": True}]
    for idx, assign in enumerate(worlds):
        acted = rng.random() < args.acted_frac
        true_atoms = [a for a, t in assign.items() if t]
        gold = engine_verdict(true_atoms, acted)
        for tier in (0, 1, 2):
            for var in range(args.variants):
                items = []
                if assign["emergency"]:        # one item grounds both atoms
                    iid, phrase = rng.choice(ATOMS["emergency"][TIER_BANK[tier]])
                    items.append({"atom": "emergency", "id": iid, "phrase": phrase, "polarity": True})
                elif assign["vehicle"]:
                    iid, phrase = rng.choice(ATOMS["vehicle"][TIER_BANK[tier]])
                    items.append({"atom": "vehicle", "id": iid, "phrase": phrase, "polarity": True})
                # hard negatives: wheelchair-class items on the no-vehicle
                # world; the hurrying ice-cream van on the vehicle world
                if not assign["vehicle"]:
                    iid, phrase = rng.choice(ATOMS["vehicle"]["negative"])
                    items.append({"atom": "vehicle", "id": iid, "phrase": phrase, "polarity": False})
                elif not assign["emergency"] and rng.random() < 0.7:
                    iid, phrase = rng.choice(ATOMS["emergency"]["negative"])
                    items.append({"atom": "emergency", "id": iid, "phrase": phrase, "polarity": False})
                phrases = [it["phrase"] for it in items] + [rng.choice(FILLER)]
                rng.shuffle(phrases)
                rows.append({"case_id": f"c{idx:02d}_t{tier}_v{var}", "tier": tier,
                             "acted": acted, "assignment": assign, "items": items,
                             "gold": gold, "narrative": None, "leak_flags": [],
                             "_phrases": phrases})
    if args.narrator:
        asyncio.run(narrate_all(rows, args.narrator, args.concurrency))
    else:
        for r in rows:
            r["narrative"] = template_narrative(r["_phrases"], r["acted"])
            r["leak_flags"] = leak_flags(r["narrative"], r["tier"])
    for r in rows:
        del r["_phrases"]
    Path(HERE / "cases.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    flagged = {r["case_id"] for r in rows if r["leak_flags"]}
    print(f"{len(rows)} cases, {len(flagged)} leak-flagged")

    # 2. arms
    results = []
    for arm in ("oracle", "program", "ground_closed", "ground_open", "holistic"):
        llm = arm.startswith("ground_") or arm == "holistic"
        for mname in (args.models.split(",") if llm else ["-"]):
            client = spec = None
            if llm:
                spec = resolve(mname)
                client = make_client(spec)
            def one(case, arm=arm, client=client, spec=spec, mname=mname):
                res = run_case(case, arm, client, spec)
                if arm == "oracle":
                    assert res["pred_verdict"] == case["gold"], case["case_id"]
                return {"case_id": case["case_id"], "tier": case["tier"],
                        "arm": arm, "model": mname, "gold": case["gold"],
                        "gold_assignment": case["assignment"], **res}
            with ThreadPoolExecutor(max_workers=args.workers if llm else 1) as pool:
                results += list(pool.map(one, rows))
            print(f"done {arm} {mname}", file=sys.stderr)
    Path(HERE / "results.jsonl").write_text("\n".join(json.dumps(r) for r in results) + "\n")

    # 3. scores
    acc = defaultdict(lambda: [0, 0])
    for r in results:
        if r["case_id"] in flagged:
            continue
        key = (f"{r['arm']}" + (f"[{r['model']}]" if r["model"] != "-" else ""), r["tier"])
        acc[key][1] += 1
        acc[key][0] += int(r["pred_verdict"]["enter_status"] == r["gold"]["enter_status"])
    arms = sorted({k[0] for k in acc})
    print("\n| arm | tier 0 | tier 1 | tier 2 |")
    print("|---|---|---|---|")
    for a in arms:
        cells = [f"{100*acc[(a,t)][0]/acc[(a,t)][1]:.0f}% ({acc[(a,t)][0]}/{acc[(a,t)][1]})"
                 for t in (0, 1, 2)]
        print(f"| {a} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
