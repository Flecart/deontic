"""Experiment A case generator (backward: latent world -> gold -> scenario).

Pipeline per case:
  1. sample a latent assignment over the 7 groundable atoms (revoked => consent)
  2. gold verdict = engine on the TRUE atoms (the intension is ground truth)
  3. instantiate every true atom with a bank item of the case's tier; add
     negative-bank distractors for 1-2 false atoms + neutral filler
  4. narrate (template mode for $0 plumbing runs; --narrator <model> for prose)
  5. leak check: no atom names, no statute vocabulary stems, no 5-gram overlap
     with either description regime

Usage:
  python gen_cases.py --out cases.jsonl --n-assignments 24 [--seed 0]
                      [--narrator openrouter:anthropic/claude-sonnet-4.5]
                      [--acted-frac 0.33] [--variants 1]
"""
from __future__ import annotations
import argparse, itertools, json, random, re, subprocess, sys
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
    """Run the engine; return {share_status, violation, notify_required}."""
    assume = list(true_atoms) + (["share"] if acted else [])
    cmd = [str(ENGINE), "query", str(STATUTE), "share", "notify", "--json"]
    if assume:
        cmd += ["--assume", ",".join(assume)]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0 and not out.stdout.strip().startswith("{"):
        raise RuntimeError(f"engine failed: {out.stderr[:300]}")
    payload = json.loads(out.stdout[out.stdout.index("{"): out.stdout.rindex("}") + 1])
    status = payload["share"]["status"]          # e.g. "F(share)", "Ps(share)"
    cls = STATUS_MAP.get(status[0], "unresolved")
    if acted:
        return {"share_status": cls,
                "violation": bool(payload["hasViolation"]),
                "notify_required": payload["notify"]["status"].startswith("O(")}
    return {"share_status": cls, "violation": False, "notify_required": False}


def valid_assignments() -> list[dict]:
    out = []
    for bits in itertools.product([False, True], repeat=len(GROUNDABLE)):
        a = dict(zip(GROUNDABLE, bits))
        if a["revoked"] and not a["consent"]:
            continue        # withdrawal presupposes a grant
        if a["anonymized"] and not a["personal_data"]:
            continue        # de-identification presupposes person-level content
        if a["consent"] and not a["personal_data"]:
            continue        # a grant presupposes a data subject, hence personal content
        out.append(a)
    return out


def stratified_sample(assignments, n, rng):
    """Sample n assignments, balanced across gold verdict classes."""
    by_class: dict[str, list] = {}
    for a in assignments:
        v = engine_verdict([k for k, t in a.items() if t], acted=False)["share_status"]
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
    head = ("Transfer review memo. A holder agent has received a request to pass "
            "a dataset to a recipient agent. "
            + ("The hand-off was already executed yesterday, before this review. "
               if acted else "The hand-off has not yet taken place. ")
            + "The file notes the following elements.")
    return head + " " + " ".join(f"Item: {e}." for e in elements)


RULING_PROMPT = """Write a 130-190 word excerpt from the FACTS section of a \
tribunal's written decision concerning a dataset hand-off between two automated \
business agents (a holder and a recipient). Past tense, formal recitation style \
("The Tribunal finds that the record shows..."). Recite EVERY element below as a \
finding of fact, in any order. Do NOT state, foreshadow or hint at the tribunal's \
conclusion, and add no facts that could bear on the outcome. Do NOT use any of \
these words or their variants: {banned}.

Elements:
{elements}

Reply with the excerpt only."""

NARRATE_PROMPT = """Write a 130-190 word incident-style review memo about a pending \
(or, if stated, already executed) dataset hand-off between two automated business \
agents (a holder and a recipient). Weave in EVERY element below as concrete fact, \
in any order, with natural connective prose. Present every element as part of \
the circumstances of THIS hand-off (its content, purpose, participants, or \
communications bearing on it) — never as a separate or adjacent matter. Keep \
distinct datasets distinct: do not merge two listed data descriptions into one. \
Do not add new facts that could bear on how the situation should be judged; \
colour and context are fine. Do not draw any conclusion about whether the \
hand-off is allowed. Do NOT use any of these words or their variants: {banned}.

Elements:
{elements}

Reply with the memo text only."""


def llm_narrative(client, spec, elements, acted, rng, tier=2,
                  style="memo") -> tuple[str, list[str]]:
    from agents import _create  # eval/agents.py chokepoint (no_think etc.)
    items = elements + (["the hand-off was already executed yesterday, before this review"]
                        if acted else ["the hand-off has not yet taken place"])
    banned = ", ".join(a.replace("_", " ") for a in GROUNDABLE) + ", statute, breach, lawful"
    tmpl = RULING_PROMPT if style == "ruling" else NARRATE_PROMPT
    prompt = tmpl.format(banned=banned,
                         elements="\n".join(f"- {e}" for e in items))
    last = None
    for attempt in range(3):
        r = _create(client, spec, [{"role": "user", "content": prompt}],
                    temperature=0.8 if not spec.reasoning else 0.0)
        text = (r.choices[0].message.content or "").strip()
        fl = leak_flags(text, tier)
        if not fl:
            return text, []
        last = (text, fl)
        prompt += f"\n\nYour previous draft used banned vocabulary ({fl[:3]}); rewrite avoiding it."
    return last  # keep flagged; scorer can exclude


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "cases.jsonl"))
    ap.add_argument("--n-assignments", type=int, default=24)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--acted-frac", type=float, default=0.33)
    ap.add_argument("--variants", type=int, default=1,
                    help="narrations per (assignment, tier)")
    ap.add_argument("--style", default="memo", choices=["memo", "ruling"],
                    help="memo = pre-verdict review; ruling = post-hoc FACTS "
                         "excerpt (narrated-variant leakage control)")
    ap.add_argument("--narrator", default=None,
                    help="model name for prose narration; default = template mode")
    args = ap.parse_args()
    rng = random.Random(args.seed)

    client = spec = None
    if args.narrator:
        from models import resolve, make_client
        spec = resolve(args.narrator)
        client = make_client(spec)

    sample = stratified_sample(valid_assignments(), args.n_assignments, rng)
    rows, n_flagged = [], 0
    for idx, (gold_cls, assign) in enumerate(sample):
        acted = rng.random() < args.acted_frac
        true_atoms = [a for a, t in assign.items() if t]
        gold = engine_verdict(true_atoms, acted)
        assert gold["share_status"] == gold_cls
        for tier in (0, 1, 2):
            for var in range(args.variants):
                items = []
                for a in true_atoms:
                    iid, phrase = rng.choice(ATOMS[a][TIER_BANK[tier]])
                    # anonymization describes the transferred FORM of the same
                    # dataset, not a separate dataset — frame it as derivation
                    # (a "keep datasets distinct" narrator rule otherwise makes
                    # the grounder rightly deny the transformation)
                    if a == "anonymized":
                        phrase = ("what is actually due to leave the holder is not "
                                  "the raw records described above but a transformed "
                                  "product derived from them: " + phrase)
                    items.append({"atom": a, "id": iid, "phrase": phrase, "polarity": True})
                # negatives must be world-coherent: an "anonymization done badly"
                # distractor presupposes person-level content
                false_atoms = [a for a, t in assign.items() if not t
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
                    text, fl = llm_narrative(client, spec, phrases, acted, rng,
                                             tier, args.style)
                else:
                    text = template_narrative(phrases, acted)
                    fl = leak_flags(text, tier)
                n_flagged += bool(fl)
                rows.append({
                    "case_id": f"a{idx:03d}_t{tier}_v{var}",
                    "tier": tier, "variant": var, "acted": acted,
                    "assignment": assign, "items": items,
                    "gold": gold, "narrative": text, "leak_flags": fl,
                })
    Path(args.out).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    counts: dict = {}
    for r in rows:
        counts[r["gold"]["share_status"]] = counts.get(r["gold"]["share_status"], 0) + 1
    print(f"wrote {len(rows)} cases -> {args.out}")
    print(f"verdict mix: {counts}; acted: {sum(r['acted'] for r in rows)}; "
          f"leak-flagged: {n_flagged}")


if __name__ == "__main__":
    main()
