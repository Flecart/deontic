"""The E1 adjudicator: a strong model that decides contested cases.

Statute-agnostic: the caller supplies the neutral-labeled condition definitions
(the same open-regime text the grounders see — labels C1..Cn, never atom
names), the retrieved precedent block, and the case narrative. The adjudicator
returns per-condition findings plus a holding rationale *written for reuse* and
explicit follow/distinguish cites. The deontic verdict is never the model's to
give: the caller runs the engine on the findings (the engine stays the
instrument; unresolved combinations surface as the [JUDGE] verdict class).

Default judge model: claude-sonnet-5 (thinking left on — adjudication is the
one place we pay for deliberation).
"""
from __future__ import annotations

import json
import re

ADJUDICATE_PROMPT = """You are the adjudicator for an automated compliance \
regime. A case has been referred to you because first-pass classifiers \
disagreed or were unsure. Below are the governing condition definitions, the \
prior adjudicated cases retrieved as precedent, and the memo before you.

For EACH condition, decide from the memo's facts whether it holds: true, \
false, or unknown (unknown only if the memo gives no sufficient basis either \
way). Where a prior case is on point, follow it and cite it; where its facts \
differ in a way that matters, distinguish it and say why. Then write a short \
holding rationale for future reuse: 2-4 sentences stating the facts that \
decided the contested conditions and the principle applied. Do not invent \
facts, and do not restate the definitions.

Conditions:
{defs}

Prior adjudicated cases:
{precedents}

Memo:
{memo}

Reply with ONLY a JSON object:
{{"findings": {{"C1": "true"|"false"|"unknown", ...}} (one entry per condition),
  "rationale": "<2-4 sentences>",
  "cites": [{{"case": "P1", "treatment": "followed"|"distinguished"}}]}}"""


def _parse_blob(text: str):
    m = re.search(r"\{.*\}", text or "", re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


class Adjudicator:
    """`labels` maps atom name -> neutral label (C1..Cn); `defs_text` is the
    already-rendered condition list using those labels."""

    def __init__(self, client, spec, labels: dict[str, str], defs_text: str):
        self.client = client
        self.spec = spec
        self.labels = labels
        self.inv = {v: k for k, v in labels.items()}
        self.defs_text = defs_text
        self.calls = 0

    def adjudicate(self, memo: str, precedent_block: str) -> dict:
        """Return {findings (atom-name keyed, tri-state), rationale, cites,
        tokens, raw}. On persistent parse failure: all-unknown findings (the
        row is logged; the stub smoke path lands here by design)."""
        from agents import _create
        prompt = ADJUDICATE_PROMPT.format(defs=self.defs_text,
                                          precedents=precedent_block, memo=memo)
        toks, raw = 0, ""
        for attempt in range(3):
            r = _create(self.client, self.spec, [{"role": "user", "content": prompt}])
            self.calls += 1
            raw = r.choices[0].message.content or ""
            usage = getattr(r, "usage", None)
            toks += (usage.prompt_tokens + usage.completion_tokens) if usage else 0
            blob = _parse_blob(raw)
            if blob and isinstance(blob.get("findings"), dict):
                findings = {}
                for label, atom in self.inv.items():
                    v = str(blob["findings"].get(label, "unknown")).lower()
                    findings[atom] = v if v in ("true", "false") else "unknown"
                return {"findings": findings,
                        "rationale": str(blob.get("rationale", ""))[:600],
                        "cites": blob.get("cites", []) if isinstance(blob.get("cites"), list) else [],
                        "tokens": toks, "raw": raw}
            prompt += "\n\nYour previous reply was not the requested JSON object; reply with ONLY the JSON."
        return {"findings": {a: "unknown" for a in self.labels},
                "rationale": "", "cites": [], "tokens": toks,
                "raw": f"__PARSE_FAIL__ {raw[:300]}"}
