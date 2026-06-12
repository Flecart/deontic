"""Independent intension-membership validation of the instance banks (review M1).

For every bank item of every atom, ask annotator models (families distinct
from the narrator) the bare membership question: does this instance fall under
this description? Items are presented standalone — no scenario, no statute,
no knowledge of which bank (tier or negative) the item came from.

Gold: tier0/1/2 items => member; negative items => non-member.
High annotator agreement = the author's intension-membership labels are not
idiosyncratic; disagreements are printed for adjudication in the paper.

Usage: python validate_banks.py --models gpt-5.4,qwen3.6-plus
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))

from descriptions import ATOMS, GROUNDABLE          # noqa: E402
from arms import parse_json_blob                    # noqa: E402
from models import resolve, make_client             # noqa: E402
from agents import _create                          # noqa: E402

PROMPT = """Concept definition: {definition}

Instance: {phrase}

Does this instance fall under the concept as defined? Consider only the \
definition above. Reply with ONLY a JSON object: {{"member": true|false, \
"reason": "<one short sentence>"}}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="gpt-5.4,qwen3.6-plus")
    ap.add_argument("--out", default=str(HERE / "bank_validation.jsonl"))
    args = ap.parse_args()

    items = []
    for a in GROUNDABLE:
        for bank, gold in (("closed_items", True), ("tier1", True),
                           ("tier2", True), ("negative", False)):
            for iid, phrase in ATOMS[a][bank]:
                items.append((a, bank, iid, phrase, gold))

    rows = []
    for mname in args.models.split(","):
        spec = resolve(mname); client = make_client(spec)
        agree = dis = 0
        for a, bank, iid, phrase, gold in items:
            r = _create(client, spec, [{"role": "user", "content": PROMPT.format(
                definition=ATOMS[a]["open"], phrase=phrase)}])
            blob = parse_json_blob(r.choices[0].message.content or "") or {}
            member = bool(blob.get("member", False))
            ok = member == gold
            agree += ok; dis += (not ok)
            rows.append({"model": mname, "atom": a, "bank": bank, "id": iid,
                         "gold_member": gold, "annot_member": member,
                         "reason": blob.get("reason", "")})
            if not ok:
                print(f"DISAGREE {mname} {a}/{bank}/{iid}: gold={gold} "
                      f"annot={member} — {blob.get('reason','')[:100]}")
        print(f"{mname}: {agree}/{agree+dis} agreement "
              f"({100*agree/(agree+dis):.1f}%)")
    Path(args.out).write_text("\n".join(json.dumps(r) for r in rows) + "\n")


if __name__ == "__main__":
    main()
