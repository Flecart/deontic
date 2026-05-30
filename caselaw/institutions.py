"""Institutions = different ways to accumulate/represent law from a case stream.

- CaseLawInstitution: incrementally synthesizes a *defeasible DDL theory* and
  uses the engine to evaluate it. When a new ruling contradicts precedent it
  carves an exception (a more-specific rule + superiority, lex specialis) and
  minimizes the antecedent against case memory so irrelevant facts drop out
  (Ripple-Down-Rules over a deontic theory). Conflicts the engine can't resolve
  surface as dilemmas.
- NearestNeighborInstitution: precedent-as-memory, k-NN over fact vectors. No
  formal structure, no conflict detection (the "judge + NL precedent" ablation).
- ConstitutionInstitution: a fixed DDL theory that never adapts (constitutional-AI
  analog).

A *judge* supplies the verdict for each presented case (oracle or noisy).
"""
from __future__ import annotations

import random

from . import engine

# rule modalities and how they render to DDL (target T):
#   F  =>O ~T   (forbid)     O  =>O T   (oblige)
#   Pp ~>O T    (permit T, defeats a prohibition)
#   Pn ~>O ~T   (permit ~T, defeats an obligation)
_POS = {"O", "Pp"}   # pushes target toward being done
_NEG = {"F", "Pn"}   # pushes target toward not-done / not-required


def _conflict(m1, m2):
    return (m1 in _POS) != (m2 in _POS)


# ─────────────────────────── judges ────────────────────────────
class Judge:
    def __init__(self, latent_ddl, target, eps=0.0, seed=0, bias_to=None, bias=0.0):
        self.latent, self.target, self.eps = latent_ddl, target, eps
        self.bias_to, self.bias = bias_to, bias   # captured/biased judge
        self.rng = random.Random(seed)

    def truth(self, case):
        return engine.verdict(self.latent, case, self.target)

    def rule(self, case):
        """Issue a verdict (noisy with prob eps; or systematically biased toward
        bias_to with prob bias -- a captured judge)."""
        v = self.truth(case)
        if self.bias_to and self.rng.random() < self.bias:
            return self.bias_to
        if self.eps and self.rng.random() < self.eps:
            alts = [x for x in ("forbidden", "obligatory", "allowed") if x != v]
            return self.rng.choice(alts)
        return v


# ───────────────────── case-law (deontic) ──────────────────────
class CaseLawInstitution:
    def __init__(self, atom_decls, target, fact_atoms):
        self.atom_decls = atom_decls.strip()
        self.target = target
        self.fact_atoms = list(fact_atoms)
        self.rules = []      # list of {id, ant:frozenset, mod:'F'/'O'/'P'}
        self.sup = set()     # (winner_id, loser_id)
        self.memory = []     # (case:frozenset, verdict)
        self._n = 0

    _HEAD = {"F": "~{t}", "O": "{t}", "Pp": "{t}", "Pn": "~{t}"}
    _ARROW = {"F": "=>O", "O": "=>O", "Pp": "~>O", "Pn": "~>O"}

    # -- theory assembly --
    def _theory(self, rules=None, sup=None):
        rules = self.rules if rules is None else rules
        sup = self.sup if sup is None else sup
        lines = [self.atom_decls]
        for r in rules:
            ant = ", ".join(sorted(r["ant"]))
            head = self._HEAD[r["mod"]].format(t=self.target)
            pre = f"{ant} " if ant else ""
            lines.append(f"{r['id']}: {pre}{self._ARROW[r['mod']]} {head}")
        if sup:
            edges = ", ".join(f"{a} > {b}" for a, b in sorted(sup))
            lines.append(f"superiority: {edges}")
        return "\n".join(lines) + "\n"

    def predict(self, case, rules=None, sup=None):
        return engine.verdict(self._theory(rules, sup), case, self.target)

    def _majority(self, case):
        """Denoised verdict for an exact case = majority over its rulings."""
        labs = [v for c, v in self.memory if c == case]
        if not labs:
            return None
        return max(set(labs), key=labs.count)

    def _distinct_memory(self):
        seen = {}
        for c, v in self.memory:               # last write wins as fallback
            seen.setdefault(c, [])
        agg = {}
        for c, _ in self.memory:
            if c not in agg:
                agg[c] = self._majority(c)
        return list(agg.items())

    # -- learning (one ruling) --
    def learn(self, case, verdict):
        case = frozenset(case)
        self.memory.append((case, verdict))
        target = self._majority(case)          # denoise repeated rulings
        covered = self.predict(case) == target
        if not covered:
            self._amend(case, target)
        return covered

    def _mod_for(self, verdict, case):
        if verdict == "forbidden":
            return "F"
        if verdict == "obligatory":
            return "O"
        # "allowed": defeat whatever currently controls the case
        cur = self.predict(case)
        return "Pn" if cur == "obligatory" else "Pp"

    def _new_edges(self, rule, others):
        """lex specialis: a more-specific (superset-antecedent) new rule defeats
        a conflicting existing rule it overlaps."""
        return {(rule["id"], r["id"]) for r in others
                if _conflict(r["mod"], rule["mod"]) and r["ant"] <= rule["ant"]}

    def _amend(self, case, verdict):
        self._n += 1
        rid = f"c{self._n}"
        mod = self._mod_for(verdict, case)
        mem = self._distinct_memory()
        ant = set(case)
        # greedily drop facts (distractors / over-specific) while no regression
        for a in sorted(ant):
            cand = ant - {a}
            r2 = {"id": rid, "ant": frozenset(cand), "mod": mod}
            t2, s2 = self.rules + [r2], set(self.sup) | self._new_edges(r2, self.rules)
            if all(self.predict(c, t2, s2) == v for c, v in mem):
                ant = cand
        rule = {"id": rid, "ant": frozenset(ant), "mod": mod}
        self.sup |= self._new_edges(rule, self.rules)
        self.rules.append(rule)
        if self.predict(case) != verdict:      # still uncontrolled -> dominate all
            self.sup |= {(rid, r["id"]) for r in self.rules
                         if r["id"] != rid and _conflict(r["mod"], mod)}

    def consolidate(self):
        """Codification pass: greedily drop rules whose removal changes no decided
        case (a 'restatement' that compresses bloated case law)."""
        mem = self._distinct_memory()
        changed = True
        while changed:
            changed = False
            for r in list(self.rules):
                if r["id"] in getattr(self, "_seed_ids", set()):
                    continue
                trial = [x for x in self.rules if x["id"] != r["id"]]
                sup = {(a, b) for a, b in self.sup if r["id"] not in (a, b)}
                if all(self.predict(c, trial, sup) == v for c, v in mem):
                    self.rules, self.sup = trial, sup
                    changed = True
                    break
        return self

    def dilemmas(self, all_cases):
        return sum(1 for c in all_cases
                   if engine.has_unresolved_conflict(self._theory(), c, self.target))

    def size(self):
        return len(self.rules)


# ───────────── hybrid: constitution-seeded case law ────────────
# The constitution's applicable provisions (target=act) as seed rules.
_CONST_SEED = [
    {"id": "k1", "ant": frozenset(), "mod": "F"},
    {"id": "k2", "ant": frozenset({"emergency"}), "mod": "Pp"},
    {"id": "k3", "ant": frozenset({"harmful"}), "mod": "F"},
    {"id": "k4", "ant": frozenset({"licensed", "notified"}), "mod": "Pp"},
]
_CONST_SEED_SUP = {("k2", "k1"), ("k4", "k1"), ("k3", "k2"), ("k3", "k4")}


class HybridCaseLaw(CaseLawInstitution):
    """Case law seeded with a fixed constitution. `supreme=True` makes the
    constitution inviolable (it always defeats evolved rules); `supreme=False`
    makes it an overridable default (evolved case law wins on conflict)."""

    def __init__(self, atom_decls, target, fact_atoms, supreme=False):
        super().__init__(atom_decls, target, fact_atoms)
        self.supreme = supreme
        if target == "act":   # constitution only speaks to `act`
            decl_atoms = {l.split(":")[0].split()[1] for l in atom_decls.splitlines()
                          if l.strip().startswith("atom ")}
            seeds = [r for r in _CONST_SEED if r["ant"] <= decl_atoms]
            self.rules = [dict(r) for r in seeds]
            ids = {r["id"] for r in seeds}
            self.sup = {(a, b) for a, b in _CONST_SEED_SUP if a in ids and b in ids}
            self._seed_ids = ids
        else:
            self._seed_ids = set()

    def _new_edges(self, rule, others):
        edges = super()._new_edges(rule, others)
        for r in others:
            if r["id"] in self._seed_ids and _conflict(r["mod"], rule["mod"]):
                if self.supreme:
                    edges.discard((rule["id"], r["id"]))
                    edges.add((r["id"], rule["id"]))      # constitution wins
                else:
                    edges.add((rule["id"], r["id"]))      # evolved law overrides default
        return edges


# ─────────────── nearest-neighbour (NL precedent) ───────────────
class NearestNeighborInstitution:
    def __init__(self, atom_decls, target, fact_atoms, k=1):
        self.fact_atoms = list(fact_atoms)
        self.target = target
        self.k = k
        self.memory = []  # (case:frozenset, verdict)

    def _dist(self, a, b):
        return sum(1 for f in self.fact_atoms if (f in a) != (f in b))

    def predict(self, case):
        if not self.memory:
            return "allowed"
        case = frozenset(case)
        ranked = sorted(range(len(self.memory)),
                        key=lambda i: (self._dist(self.memory[i][0], case), -i))
        votes = {}
        for i in ranked[: self.k]:
            votes[self.memory[i][1]] = votes.get(self.memory[i][1], 0) + 1
        return max(votes, key=votes.get)

    def learn(self, case, verdict):
        covered = self.predict(case) == verdict
        self.memory.append((frozenset(case), verdict))
        return covered

    def self_contradictions(self):
        """Stored precedents with identical facts but conflicting verdicts."""
        seen = {}
        bad = 0
        for c, v in self.memory:
            if c in seen and seen[c] != v:
                bad += 1
            seen[c] = v
        return bad


# ──────────────────── fixed constitution ───────────────────────
class ConstitutionInstitution:
    def __init__(self, ddl, target):
        self.ddl, self.target = ddl, target

    def predict(self, case):
        return engine.verdict(self.ddl, case, self.target)

    def learn(self, case, verdict):
        return self.predict(case) == verdict  # never adapts
