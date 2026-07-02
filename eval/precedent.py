"""Precedent store for E1 (plan: docs/plan_common_law.md §2-3).

A *holding* is one adjudicated case:
    {case_id, t, facts, findings {atom: "true"|"false"|"unknown"},
     verdict, rationale, cites, judge, contested, assign_key}
`assign_key` is the case's latent gold assignment key — never shown to any
model; it exists so the scorer can compute gold retrieval relevance
(two cases are relevant to each other iff they share the latent assignment).

Retrieval is as-of-t (only holdings with holding.t < before_t), in three modes
(the E1 retrieval ablation):
    embed  cosine over facts embeddings (pilot baseline; freight/corpus.py)
    atom   agreement between a provisional atom grounding of the query case
           and each holding's determinate findings
    rule   rule-subsumption: a holding compiles to the DDL rule
           "its determinate findings => its verdict"; it is retrieved when
           that rule *fires* on the provisional atoms (every determinate
           finding matched — Horty's precedential constraint, operationalized;
           the subset test below is exactly DDL body-applicability for these
           fact-only bodies, so no engine round-trip is needed). Firing
           holdings rank first (specific > general), embed-sim backfills.

Embeddings: OpenAI text-embedding-3-small when OPENAI_API_KEY is set, else a
deterministic hashed bag-of-words vector so offline/stub smoke runs work.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from functools import lru_cache
from pathlib import Path

EMBED_MODEL = os.environ.get("E1_EMBED_MODEL", "text-embedding-3-small")
OFFLINE_DIM = 256


# ── embeddings ────────────────────────────────────────────────────────────────

def _offline_embed(text: str) -> list[float]:
    """Deterministic hashed bag-of-words unit vector (no network)."""
    v = [0.0] * OFFLINE_DIM
    for tok in re.findall(r"[a-z']+", text.lower()):
        h = int(hashlib.md5(tok.encode()).hexdigest(), 16)
        v[h % OFFLINE_DIM] += 1.0 if (h >> 16) % 2 else -1.0
    n = sum(x * x for x in v) ** 0.5
    return [x / n for x in v] if n else v


@lru_cache(maxsize=100_000)
def _openai_embed(text: str) -> tuple:
    from openai import OpenAI
    r = OpenAI(api_key=os.environ["OPENAI_API_KEY"]).embeddings.create(
        model=EMBED_MODEL, input=[text])
    return tuple(r.data[0].embedding)


def embed(text: str, provider: str = "auto") -> list[float]:
    if provider == "offline" or (provider == "auto" and not os.environ.get("OPENAI_API_KEY")):
        return _offline_embed(text)
    v = list(_openai_embed(text))
    n = sum(x * x for x in v) ** 0.5
    return [x / n for x in v] if n else v


def _cos(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


# ── the store ─────────────────────────────────────────────────────────────────

class Store:
    def __init__(self, atoms: list[str], embed_provider: str = "auto"):
        self.atoms = atoms
        self.embed_provider = embed_provider
        self.holdings: list[dict] = []

    def __len__(self):
        return len(self.holdings)

    def add(self, holding: dict):
        if "embedding" not in holding:
            holding["embedding"] = embed(holding["facts"], self.embed_provider)
        self.holdings.append(holding)

    # -- retrieval ------------------------------------------------------------

    def retrieve(self, facts: str, k: int, mode: str = "embed",
                 provisional: dict | None = None, before_t: int | None = None) -> list[dict]:
        """Top-k holdings; `provisional` (atom -> "true"/"false"/"unknown") is
        required for atom/rule modes. Each returned holding gets `_score` and,
        in rule mode, `_fired`."""
        pool = [h for h in self.holdings
                if before_t is None or h["t"] < before_t]
        if not pool:
            return []
        q = embed(facts, self.embed_provider)
        sims = {id(h): _cos(q, h["embedding"]) for h in pool}

        if mode == "embed":
            ranked = sorted(pool, key=lambda h: -sims[id(h)])
        elif mode == "atom":
            if provisional is None:
                raise ValueError("atom mode needs a provisional grounding")
            def agree(h):
                return sum(1 for a in self.atoms
                           if h["findings"].get(a) in ("true", "false")
                           and h["findings"][a] == provisional.get(a))
            ranked = sorted(pool, key=lambda h: (-agree(h), -sims[id(h)]))
        elif mode == "rule":
            if provisional is None:
                raise ValueError("rule mode needs a provisional grounding")
            def det(h):
                return {a: v for a, v in h["findings"].items() if v in ("true", "false")}
            def fires(h):
                d = det(h)
                return bool(d) and all(provisional.get(a) == v for a, v in d.items())
            fired = {id(h): fires(h) for h in pool}
            ranked = sorted(pool, key=lambda h: (not fired[id(h)],
                                                 -len(det(h)) if fired[id(h)] else 0,
                                                 -sims[id(h)]))
        else:
            raise ValueError(f"unknown retrieval mode: {mode}")

        out = []
        for h in ranked[:k]:
            c = dict(h)
            c["_score"] = round(sims[id(h)], 4)
            if mode == "rule":
                c["_fired"] = fired[id(h)]
            out.append(c)
        return out

    # -- persistence ----------------------------------------------------------

    def save(self, path: str | Path):
        Path(path).write_text(
            "\n".join(json.dumps(h) for h in self.holdings) + ("\n" if self.holdings else ""))

    @classmethod
    def load(cls, path: str | Path, atoms: list[str], embed_provider: str = "auto") -> "Store":
        st = cls(atoms, embed_provider)
        for line in Path(path).read_text().splitlines():
            if line.strip():
                st.holdings.append(json.loads(line))
        return st

    # -- store-level diagnostics ----------------------------------------------

    def consistency(self) -> dict:
        """Fraction of latent-assignment groups (>=2 holdings) whose holdings
        all reached the same verdict — the store-coherence number the scorer
        reports next to any accuracy claim."""
        groups: dict[str, set] = {}
        for h in self.holdings:
            key = h.get("assign_key")
            if key:
                groups.setdefault(key, set()).add(h["verdict"]["share_status"])
        multi = {k: v for k, v in groups.items() if k}
        rep = [k for k, v in multi.items() if len(v) > 1]
        n = len(multi)
        return {"n_groups": n, "n_incoherent": len(rep),
                "coherence": round(1 - len(rep) / n, 3) if n else 1.0}


# ── rendering for prompts ────────────────────────────────────────────────────

def render_block(holdings: list[dict], labels: dict[str, str],
                 show_rationale: bool = True) -> str:
    """Precedent block for grounder/adjudicator prompts. `labels` maps atom
    names to the neutral condition labels (C1..Cn) used in the prompt, so
    holdings never leak meaningful atom names."""
    if not holdings:
        return "(none yet)"
    parts = []
    for i, h in enumerate(holdings):
        det = [f"{labels[a]}={v}" for a, v in h["findings"].items()
               if a in labels and v in ("true", "false")]
        p = (f"[case P{i+1}] FACTS: {h['facts']}\n"
             f"  FINDINGS: {', '.join(det) if det else '(none determinate)'}")
        if show_rationale and h.get("rationale"):
            p += f"\n  RATIONALE: {h['rationale']}"
        parts.append(p)
    return "\n\n".join(parts)
