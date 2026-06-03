"""The case corpus C and its per-arm accretion rules.

C is the evolving body of law. Each entry is a decided case:
    {facts, ruling in {compliant,breach}, damage, ambiguity, rationale, t, ...}
plus a cached embedding of its `facts` text for retrieval.

Retrieval is cosine top-k over those embeddings (this is what J reads). The four
arms differ ONLY in which cases enter C:

  CL  (common law)      -- only cases that were actually filed (endogenous).
  Civ (civil law)       -- a frozen up-front code generated once at t=0; no accretion.
  US  (uniform sampling) -- every round, with prob q, a random transaction is
                            submitted to J regardless of dispute, and accreted.
  RR  (random rule)     -- at CL's rate, an uncorrelated plausible rule is injected.

We also keep the DDL engine in the loop: holdings are compiled to a defeasible
deontic theory and the `deontic` binary's unresolved-conflict signal is our
overruling / entailment-closure-stability proxy.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from functools import lru_cache

import numpy as np

EMBED_MODEL = os.environ.get("FREIGHT_EMBED_MODEL", "text-embedding-3-small")
BIN = os.environ.get("DEONTIC_BIN",
                     os.path.expanduser("~/Desktop/work/deontic/.lake/build/bin/deontic"))


# --- embeddings -------------------------------------------------------------

def _client():
    from openai import OpenAI
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@lru_cache(maxsize=100_000)
def _embed_cached(text: str) -> tuple:
    r = _client().embeddings.create(model=EMBED_MODEL, input=[text])
    return tuple(r.data[0].embedding)


def embed(text: str) -> np.ndarray:
    v = np.asarray(_embed_cached(text), dtype=np.float32)
    n = np.linalg.norm(v)
    return v / n if n else v


# --- the corpus -------------------------------------------------------------

class Corpus:
    def __init__(self, arm: str):
        self.arm = arm
        self.cases: list[dict] = []
        self._mat: np.ndarray | None = None      # stacked unit embeddings
        self.frozen = False                       # Civ freezes after t=0

    def __len__(self):
        return len(self.cases)

    def add(self, case: dict):
        """Accrete one decided case (no-op if frozen, e.g. Civ after seeding)."""
        if self.frozen:
            return
        if "embedding" not in case:
            case["embedding"] = embed(case["facts"]).tolist()
        self.cases.append(case)
        self._mat = None

    def _matrix(self) -> np.ndarray:
        if self._mat is None:
            if not self.cases:
                self._mat = np.zeros((0, 1), dtype=np.float32)
            else:
                self._mat = np.vstack([np.asarray(c["embedding"], dtype=np.float32)
                                       for c in self.cases])
        return self._mat

    def retrieve(self, facts: str, k: int = 5) -> list[dict]:
        """Top-k precedents by cosine similarity on the facts field."""
        if not self.cases:
            return []
        q = embed(facts)
        sims = self._matrix() @ q
        idx = np.argsort(-sims)[:k]
        out = []
        for i in idx:
            c = dict(self.cases[int(i)])
            c["_sim"] = float(sims[int(i)])
            out.append(c)
        return out

    # --- the overruling / closure-stability proxy via the DDL engine --------

    def closure_conflicts(self) -> dict:
        """Compile holdings to a defeasible deontic theory and ask the engine
        which fact-situations are now *unresolved* (contradictory holdings with
        no superiority to break the tie). A jump in unresolved situations means
        a freshly accreted case overturned an established holding.

        Returns {n_situations, n_conflicted, stability in [0,1]}.
        """
        if not self.cases:
            return {"n_situations": 0, "n_conflicted": 0, "stability": 1.0}
        # one opaque situation-atom per discretised fact signature.
        rules, atoms, sigs = [], {}, {}
        for j, c in enumerate(self.cases):
            sig = _signature(c)
            sigs.setdefault(sig, 0)
            sigs[sig] += 1
            head = "breach" if c["ruling"] == "breach" else "~breach"
            rules.append(f"h{j}: {sig} =>O {head}")
            atoms[sig] = _sig_desc(sig)
        atoms["breach"] = "the seller is held to have breached and owes compensation"
        theory = (
            "\n".join(f"atom {a}: {d}" for a, d in atoms.items())
            + "\n\n" + "\n".join(rules) + "\n"
        )
        conflicted = sum(1 for sig in sigs if _is_unresolved(theory, sig))
        n = len(sigs)
        return {"n_situations": n, "n_conflicted": conflicted,
                "stability": round(1.0 - conflicted / n, 3) if n else 1.0}


def _signature(case: dict) -> str:
    """Discretise a case into an opaque situation atom (the DDL antecedent)."""
    sev = case.get("severity", 0.0)
    perm = case.get("permissiveness", 0.5)
    fm = case.get("fm", 0.0)
    sb = "sevlo" if sev < 0.2 else "sevmid" if sev < 0.5 else "sevhi"
    cb = "perm" if perm >= 0.4 else "strict"
    fb = "fmyes" if fm >= 0.3 else "fmno"
    return f"sit_{sb}_{cb}_{fb}"


def _sig_desc(sig: str) -> str:
    return f"fact-situation {sig.replace('sit_', '').replace('_', '/')}"


@lru_cache(maxsize=20_000)
def _is_unresolved(theory: str, sig: str) -> bool:
    body = f"facts: {sig}\n\n{theory}"
    fd, path = tempfile.mkstemp(suffix=".ddl")
    with os.fdopen(fd, "w") as fh:
        fh.write(body)
    try:
        p = subprocess.run([BIN, "query", path, "breach"],
                           capture_output=True, text=True, timeout=30)
        out = (p.stdout + p.stderr).lower()
    except Exception:
        return False
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    return "unresolved" in out or "judge" in out


# --- seeding the arms -------------------------------------------------------

OMEGA0 = [
    "S must deliver goods conforming to the contract specification.",
    "Deviations that stay within commercial reasonableness are permitted.",
    "Price and quantity terms are crisp: short shipment or non-payment is a breach.",
]


def seed_civ(corpus: Corpus, task_description: str, model: str, n_critique: int = 1):
    """Civil-law arm: generate a comprehensive code at t=0 via a short
    Constitutional-AI-style self-critique loop, store it as one 'code' case, and
    freeze. The code rides along in retrieval as a constitution."""
    from openai import OpenAI
    cli = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def chat(msgs):
        kw = dict(model=model, messages=msgs)
        if not model.startswith(("o", "gpt-5")):
            kw["temperature"] = 0.2
        return cli.chat.completions.create(**kw).choices[0].message.content or ""

    draft = chat([
        {"role": "system", "content": "You are a legislator drafting a freight/sales "
         "code for an agent society, grounded in UCC Article 2 doctrine."},
        {"role": "user", "content": f"{task_description}\n\nSeed principles:\n- "
         + "\n- ".join(OMEGA0) + "\n\nDraft 8-12 concise, operational rules that tell "
         "a judge when a delivery deviation is a breach and how to size damages. "
         "Cover quality, packaging, lateness, shortfall, substitution, and force majeure."}])
    for _ in range(n_critique):
        draft = chat([
            {"role": "system", "content": "You critique and improve a freight code."},
            {"role": "user", "content": f"Here is a draft code:\n\n{draft}\n\n"
             "Critique it for gaps, internal contradictions, and over/under-breadth, "
             "then output the IMPROVED code only."}])
    corpus.add({
        "facts": "GENERAL CODE (civil-law constitution): " + draft[:400],
        "ruling": "code", "damage": 0.0, "ambiguity": 0.5, "severity": 0.5,
        "permissiveness": 0.5, "fm": 0.3, "t": 0, "rationale": draft, "is_code": True,
    })
    corpus.frozen = True
    return draft


@lru_cache(maxsize=1)
def _rule_bank(model: str) -> tuple:
    """RR arm: a bank of plausibly-phrased but uncorrelated freight rules."""
    from openai import OpenAI
    cli = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    kw = dict(model=model, messages=[
        {"role": "user", "content": "Generate 20 plausible-sounding freight/sales "
         "contract rules, one per line, no numbering. They should read like real "
         "legal rules but need not be mutually consistent or correct."}])
    if not model.startswith(("o", "gpt-5")):
        kw["temperature"] = 1.0
    txt = cli.chat.completions.create(**kw).choices[0].message.content or ""
    lines = [l.strip(" -*\t") for l in txt.splitlines() if len(l.strip()) > 15]
    return tuple(lines or ["Deliveries must be inspected within 48 hours of arrival."])


def inject_random_rule(corpus: Corpus, model: str, rng) -> dict:
    bank = _rule_bank(model)
    rule = rng.choice(bank)
    case = {
        "facts": "INJECTED RULE: " + rule,
        "ruling": "breach" if rng.random() < 0.5 else "compliant",
        "damage": 0.0, "ambiguity": 0.5, "severity": rng.random(),
        "permissiveness": rng.random(), "fm": rng.random() * 0.5,
        "rationale": "randomly injected rule", "is_rule": True,
    }
    corpus.add(case)
    return case
