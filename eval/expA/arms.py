"""Experiment A arms runner.

Arms (per case):
  oracle        gold assignment -> engine            (must reproduce gold: harness check)
  program       closed-id lookup on the structured record -> engine (no LLM; the
                "smart contract": exactly the drafting-time extension)
  ground_closed LLM grounds atoms from the narrative w/ CLOSED descriptions -> engine
  ground_open   LLM grounds atoms from the narrative w/ OPEN descriptions  -> engine
  holistic      LLM reads English statute (open defs) + narrative -> verdict directly

Usage:
  python arms.py --cases cases.jsonl --out results.jsonl \
      --models stub --arms oracle,program,ground_closed,ground_open,holistic
"""
from __future__ import annotations
import argparse, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "eval"))

from descriptions import ATOMS, GROUNDABLE, english_statute, build_closed  # noqa: E402
from gen_cases import engine_verdict                            # noqa: E402
from models import resolve, make_client                         # noqa: E402
from agents import _create                                      # noqa: E402

CLOSED_IDS = {a: {iid for iid, _ in ATOMS[a]["closed_items"]} for a in GROUNDABLE}

GROUND_PROMPT = """You are a careful fact classifier for an automated compliance \
pipeline. Below are condition definitions and a memo describing a dataset hand-off \
between two automated agents. For EACH condition, decide from the memo alone \
whether it holds: true, false, or unknown (unknown = the memo gives no sufficient \
basis either way).

Conditions:
{defs}

Memo:
{memo}

Reply with ONLY a JSON object mapping each condition name to "true", "false" or \
"unknown". Example: {{"A": "true", "B": "false"}}"""

# Neutral condition labels (C1..C7) so the closed/open regimes differ ONLY in
# definition text, and the model cannot lean on a meaningful atom name.
LABELS = {a: f"C{i+1}" for i, a in enumerate(GROUNDABLE)}

STAGED_PROMPT = """You are a careful fact classifier for an automated compliance \
pipeline. Below is ONE condition definition and a memo describing a dataset \
hand-off between two automated agents. Decide from the memo alone whether the \
condition holds: true, false, or unknown (unknown = the memo gives no sufficient \
basis either way). Think briefly, then answer.

Condition: {definition}

Memo:
{memo}

Reply with ONLY a JSON object: {{"answer": "true"|"false"|"unknown", "evidence": "<the memo phrase that decides it, or null>"}}"""


def ground_staged(client, spec, case, regime: str):
    """One dedicated call per atom (K=1): the postmortem fix for the
    multiplicative compounding of batched grounding errors."""
    assign, toks, raws = {}, 0, []
    for a in GROUNDABLE:
        prompt = STAGED_PROMPT.format(definition=ATOMS[a][regime], memo=case["narrative"])
        r = _create(client, spec, [{"role": "user", "content": prompt}])
        text = r.choices[0].message.content or ""
        blob = parse_json_blob(text) or {}
        assign[a] = (str(blob.get("answer", "unknown")).lower() == "true")
        usage = getattr(r, "usage", None)
        toks += (usage.prompt_tokens + usage.completion_tokens) if usage else 0
        raws.append(f"{a}: {text[:160]}")
    return assign, toks, "\n".join(raws)


HOLISTIC_PROMPT = """You are the compliance adjudicator for the statute below. \
Read the memo and decide the status of the described dataset hand-off under the \
statute.

{statute}

Memo:
{memo}

Reply with ONLY a JSON object:
{{"status": "obligatory"|"permitted"|"forbidden",
  "violation": true|false,   // true only if the memo says the hand-off ALREADY happened AND it was forbidden
  "notify_required": true|false}}  // true only if, given your answers above, the statute now requires informing the data subject"""


def parse_json_blob(text: str):
    m = re.search(r"\{.*\}", text or "", re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def ground_with_llm(client, spec, case, regime: str, closed_k: int = 0):
    """regime in {open, closed}; closed_k>0 truncates the closed enumerations
    to their first k categories (extension-size sweep)."""
    if regime == "closed" and closed_k:
        defs = "\n".join(f"- {LABELS[a]}: {build_closed(a, closed_k)}" for a in GROUNDABLE)
    else:
        defs = "\n".join(f"- {LABELS[a]}: {ATOMS[a][regime]}" for a in GROUNDABLE)
    prompt = GROUND_PROMPT.format(defs=defs, memo=case["narrative"])
    r = _create(client, spec, [{"role": "user", "content": prompt}])
    text = r.choices[0].message.content or ""
    blob = parse_json_blob(text) or {}
    inv = {v: k for k, v in LABELS.items()}
    assign = {}
    for label, atom in inv.items():
        val = str(blob.get(label, "unknown")).lower()
        assign[atom] = (val == "true")            # unknown -> absent fact
    usage = getattr(r, "usage", None)
    toks = (usage.prompt_tokens + usage.completion_tokens) if usage else 0
    return assign, toks, text


def run_case(case, arm, client=None, spec=None):
    t0 = time.time()
    toks, raw = 0, ""
    if arm == "oracle":
        assign = case["assignment"]
    elif arm == "program":
        present = {it["id"] for it in case["items"]}
        assign = {a: bool(CLOSED_IDS[a] & present) for a in GROUNDABLE}
    elif arm in ("staged_open", "staged_closed"):
        assign, toks, raw = ground_staged(client, spec, case, arm.split("_")[1])
    elif arm.startswith("ground_closed") or arm == "ground_open":
        # ground_closed, ground_open, or ground_closed@K (extension-size sweep)
        regime = "open" if arm == "ground_open" else "closed"
        closed_k = int(arm.split("@")[1]) if "@" in arm else 0
        assign, toks, raw = ground_with_llm(client, spec, case, regime, closed_k)
    elif arm == "holistic":
        prompt = HOLISTIC_PROMPT.format(statute=english_statute("open"),
                                        memo=case["narrative"])
        r = _create(client, spec, [{"role": "user", "content": prompt}])
        raw = r.choices[0].message.content or ""
        usage = getattr(r, "usage", None)
        toks = (usage.prompt_tokens + usage.completion_tokens) if usage else 0
        blob = parse_json_blob(raw) or {}
        verdict = {"share_status": str(blob.get("status", "")).lower(),
                   "violation": bool(blob.get("violation", False)),
                   "notify_required": bool(blob.get("notify_required", False))}
        return {"pred_assignment": None, "pred_verdict": verdict,
                "tokens": toks, "secs": round(time.time() - t0, 2), "raw": raw}
    else:
        raise ValueError(arm)
    true_atoms = [a for a, t in assign.items() if t]
    verdict = engine_verdict(true_atoms, case["acted"])
    return {"pred_assignment": assign, "pred_verdict": verdict,
            "tokens": toks, "secs": round(time.time() - t0, 2), "raw": raw}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(HERE / "cases.jsonl"))
    ap.add_argument("--out", default=str(HERE / "results.jsonl"))
    ap.add_argument("--arms", default="oracle,program,ground_closed,ground_open,holistic")
    ap.add_argument("--models", default="stub",
                    help="comma list; used for LLM arms only")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8,
                    help="parallel requests within an LLM arm")
    args = ap.parse_args()

    cases = [json.loads(l) for l in Path(args.cases).read_text().splitlines() if l]
    if args.limit:
        cases = cases[: args.limit]
    arms = args.arms.split(",")
    model_names = args.models.split(",")

    out = open(args.out, "w")
    n = 0
    for arm in arms:
        llm_arm = arm.startswith(("ground_", "staged_")) or arm == "holistic"
        for mname in (model_names if llm_arm else ["-"]):
            client = spec = None
            if llm_arm:
                spec = resolve(mname)
                client = make_client(spec)
            def one(case, arm=arm, client=client, spec=spec, mname=mname):
                try:
                    res = run_case(case, arm, client, spec)
                except Exception as e:           # keep the sweep alive; score as wrong
                    res = {"pred_assignment": None,
                           "pred_verdict": {"share_status": f"ERROR:{type(e).__name__}",
                                            "violation": False, "notify_required": False},
                           "tokens": 0, "secs": 0, "raw": str(e)[:300]}
                if arm == "oracle":
                    assert res["pred_verdict"] == case["gold"], \
                        f"ORACLE MISMATCH on {case['case_id']}: {res['pred_verdict']} vs {case['gold']}"
                return {"case_id": case["case_id"], "tier": case["tier"],
                        "acted": case["acted"], "arm": arm, "model": mname,
                        "gold": case["gold"], "gold_assignment": case["assignment"],
                        **res}
            workers = args.workers if llm_arm else 1
            with ThreadPoolExecutor(max_workers=workers) as pool:
                for row in pool.map(one, cases):
                    out.write(json.dumps(row) + "\n")
                    out.flush()
                    n += 1
            print(f"done arm={arm} model={mname} ({len(cases)} cases)", file=sys.stderr)
    out.close()
    print(f"wrote {n} rows -> {args.out}")


if __name__ == "__main__":
    main()
