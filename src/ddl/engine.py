"""The inference engine: computes the extension E(D) of a defeasible theory.

Implements Governatori (2018) pp.18-21: the constitutive tag +/-dC, the
prescriptive obligation/permission tags +/-dO, +/-dPs, +/-dPw, +/-dP over
otimes compensation chains, and the non-compliance tag +/-d_bottom.

Prohibition is not a stored tag: ``F l`` is ``+dO ~l`` (eq. 3).

Notes on faithful-but-pragmatic choices:

* Violation. The "advance past an obligation in an otimes chain" / "violation"
  test in the paper is ``(c_k not in F) or (~c_k in F)``. Read literally that
  marks an un-actioned prohibition as violated, which spuriously triggers
  +d_bottom (e.g. ``O~comment`` with no comment in the facts). Under a
  closed-world reading of the decided atoms the two disjuncts coincide, so we
  use the operative one: ``violated(c) iff ~c in F`` -- the opposite was
  actually brought about. This reproduces the Example 1 / sect. 4 outcomes.

* Algorithm. A monotone fixpoint over the modal Herbrand base: apply every
  constructive +/- proof condition to convergence; a constitutive
  well-foundedness closure resolves positive cycles; a final safety net tags
  anything still undecided negatively. "applicable" and "discarded" always mean
  the *stable* notions (all premises positively proved / some premise refuted),
  never "not yet applicable" -- so a pending rule is mistaken for neither.
"""

from __future__ import annotations

from .proof import MODALITIES, Conclusion, Justification
from .syntax import BOTTOM, Literal, ModalLiteral, Rule, Theory, is_bottom


class Extension:
    """The set of derivable tagged literals, with justifications."""

    def __init__(self) -> None:
        self.proven: dict[Conclusion, Justification] = {}

    def add(self, just: Justification) -> bool:
        c = just.conclusion
        if c in self.proven:
            return False
        self.proven[c] = just
        return True

    def has(self, sign: str, modality: str, literal: Literal) -> bool:
        return Conclusion(sign, modality, literal) in self.proven

    def justification(self, sign: str, modality: str, literal: Literal):
        return self.proven.get(Conclusion(sign, modality, literal))

    def conclusions(self, sign: str | None = None) -> list[Conclusion]:
        return [c for c in self.proven if sign is None or c.sign == sign]

    # --- convenience queries ---
    def provable(self, literal: Literal) -> bool:  # +dC
        return self.has("+", "C", literal)

    def refuted(self, literal: Literal) -> bool:  # -dC
        return self.has("-", "C", literal)

    def obligation(self, literal: Literal) -> bool:  # O l
        return self.has("+", "O", literal)

    def forbidden(self, literal: Literal) -> bool:  # F l == O ~l
        return self.has("+", "O", literal.complement)

    def permitted(self, literal: Literal) -> bool:  # P l
        return self.has("+", "P", literal)

    def strong_permitted(self, literal: Literal) -> bool:  # Ps l
        return self.has("+", "Ps", literal)

    def weak_permitted(self, literal: Literal) -> bool:  # Pw l
        return self.has("+", "Pw", literal)

    def noncompliant(self) -> bool:  # +d_bottom
        return self.has("+", "⊥", BOTTOM)


class Engine:
    def __init__(self, theory: Theory) -> None:
        self.theory = theory
        self.ext = Extension()

    # ===================================================== rule selectors
    def _supports_C(self, l: Literal) -> list[Rule]:
        return [
            r for r in self.theory.rules
            if r.mode == "C" and not r.is_defeater and r.head == (l,)
        ]

    def _head_C(self, l: Literal) -> list[Rule]:
        return [r for r in self.theory.rules if r.mode == "C" and r.head == (l,)]

    def _occurrences(self, l: Literal) -> list[tuple[Rule, int]]:
        """(rule, index) pairs where l is an obligation-head literal of rule."""
        out: list[tuple[Rule, int]] = []
        for r in self.theory.rules:
            if r.mode == "O":
                for i, h in enumerate(r.head):
                    if h == l:
                        out.append((r, i))
            elif r.mode == "C" and r.head == (l,):
                out.append((r, 0))
        return out

    def _supports_O(self, l: Literal) -> list[tuple[Rule, int]]:
        return [(r, i) for (r, i) in self._occurrences(l) if not r.is_defeater]

    def _defeaters_O(self, l: Literal) -> list[tuple[Rule, int]]:
        return [(r, i) for (r, i) in self._occurrences(l) if r.is_defeater]

    # ===================================================== body evaluation
    def _elem_applicable(self, b) -> bool:
        if isinstance(b, ModalLiteral):
            sign = "-" if b.negated else "+"
            return self.ext.has(sign, b.op, b.lit)
        if is_bottom(b):
            return self.ext.has("+", "⊥", BOTTOM)
        return self.ext.provable(b)  # plain literal: +dC (subsumes facts)

    def _elem_discarded(self, b) -> bool:
        if isinstance(b, ModalLiteral):
            sign = "+" if b.negated else "-"
            return self.ext.has(sign, b.op, b.lit)
        if is_bottom(b):
            return self.ext.has("-", "⊥", BOTTOM)
        return self.ext.refuted(b)

    def _body_applicable(self, r: Rule) -> bool:
        return all(self._elem_applicable(b) for b in r.body)

    def _body_discarded(self, r: Rule) -> bool:
        return any(self._elem_discarded(b) for b in r.body)

    def _body_p_applicable(self, r: Rule) -> bool:
        if r.mode == "O":
            return self._body_applicable(r)
        if not r.body or any(isinstance(b, ModalLiteral) for b in r.body):
            return False
        return all(self.ext.has("+", "O", b) for b in r.body)

    def _body_p_discarded(self, r: Rule) -> bool:
        if r.mode == "O":
            return self._body_discarded(r)
        if not r.body or any(isinstance(b, ModalLiteral) for b in r.body):
            return True
        return any(self.ext.has("-", "O", b) for b in r.body)

    def _violated(self, c: Literal) -> bool:
        # The obligation O c is violated iff the opposite was brought about.
        # Facts are fixed, so this is stable.
        return c.complement in self.theory.facts

    def _applicable_at(self, r: Rule, index: int) -> bool:
        """Rule is applicable for its head literal at ``index`` (Prop. pp.18-19):
        body-p-applicable and every prior chain obligation is in force and
        violated."""
        if not self._body_p_applicable(r):
            return False
        for k in range(index):
            ck = r.head[k]
            if not self.ext.has("+", "O", ck) or not self._violated(ck):
                return False
        return True

    def _discarded_at(self, r: Rule, index: int) -> bool:
        """Stable negation of applicable-at: body provably discarded, or a prior
        chain obligation is refuted or not violated."""
        if self._body_p_discarded(r):
            return True
        for k in range(index):
            ck = r.head[k]
            if self.ext.has("-", "O", ck) or not self._violated(ck):
                return True
        return False

    # ===================================================== +/- dC
    def _try_plus_dC(self, l: Literal) -> Justification | None:
        if l in self.theory.facts:
            return Justification(Conclusion("+", "C", l), kind="fact")
        if l.complement in self.theory.facts:
            return None
        winners = [r for r in self._supports_C(l) if self._body_applicable(r)]
        if not winners:
            return None
        defeated: list[tuple[str, str]] = []
        for s in self._head_C(l.complement):
            if self._body_discarded(s):
                defeated.append((s.label, "discarded (a premise is refuted)"))
                continue
            beater = next(
                (t for t in winners if self.theory.beats(t.label, s.label)), None
            )
            if beater is None:
                return None
            defeated.append((s.label, f"defeated by superior rule {beater.label}"))
        return Justification(
            Conclusion("+", "C", l), kind="rule", applied=winners[0].label,
            defeated=defeated,
        )

    def _try_minus_dC(self, l: Literal) -> Justification | None:
        if l in self.theory.facts:
            return None
        if l.complement in self.theory.facts:
            return Justification(
                Conclusion("-", "C", l), kind="refuted",
                detail=f"complement {l.complement} is a fact",
            )
        supports = self._supports_C(l)
        if all(self._body_discarded(r) for r in supports):
            return Justification(
                Conclusion("-", "C", l), kind="refuted",
                detail="no applicable supporting rule",
            )
        for s in self._head_C(l.complement):
            if self._body_discarded(s) or not self._body_applicable(s):
                continue
            if all(
                self._body_discarded(t) or not self.theory.beats(t.label, s.label)
                for t in supports
            ):
                return Justification(
                    Conclusion("-", "C", l), kind="refuted",
                    defeated=[(s.label, "undefeated counter-rule")],
                )
        return None

    # ===================================================== +/- dO
    def _team_handles_attackers(self, q: Literal):
        """+dO/+dPs condition 2: every counter-rule applicable for ~q is beaten
        by a rule applicable for q. Returns (ok, defeated-trace)."""
        defeated: list[tuple[str, str]] = []
        for s, j in self._occurrences(q.complement):
            if self._discarded_at(s, j):
                continue
            beater = next(
                (
                    (t, k)
                    for (t, k) in self._occurrences(q)
                    if self._applicable_at(t, k)
                    and self.theory.beats(t.label, s.label)
                ),
                None,
            )
            if beater is None:
                return False, defeated
            defeated.append((s.label, f"defeated by superior rule {beater[0].label}"))
        return True, defeated

    def _try_plus_dO(self, q: Literal) -> Justification | None:
        winners = [(r, i) for (r, i) in self._supports_O(q) if self._applicable_at(r, i)]
        if not winners:
            return None
        ok, defeated = self._team_handles_attackers(q)
        if not ok:
            return None
        return Justification(
            Conclusion("+", "O", q), kind="obligation", applied=winners[0][0].label,
            defeated=defeated,
        )

    def _try_minus_dO(self, q: Literal) -> Justification | None:
        supports = self._supports_O(q)
        if all(self._discarded_at(r, i) for (r, i) in supports):
            return Justification(
                Conclusion("-", "O", q), kind="refuted",
                detail="no applicable obligation rule",
            )
        for s, j in self._occurrences(q.complement):
            if not self._applicable_at(s, j):
                continue
            if all(
                self._discarded_at(t, k) or not self.theory.beats(t.label, s.label)
                for (t, k) in self._occurrences(q)
            ):
                return Justification(
                    Conclusion("-", "O", q), kind="refuted",
                    defeated=[(s.label, "undefeated counter-obligation")],
                )
        return None

    # ===================================================== +/- dPs (strong)
    def _try_plus_dPs(self, q: Literal) -> Justification | None:
        if self.ext.has("+", "O", q):
            return Justification(
                Conclusion("+", "Ps", q), kind="from-obligation",
                detail="O q entails strong permission (Prop. 1.6)",
            )
        defs = [
            r for (r, i) in self._defeaters_O(q) if self._body_p_applicable(r)
        ]
        if not defs:
            return None
        ok, defeated = self._team_handles_attackers(q)
        if not ok:
            return None
        return Justification(
            Conclusion("+", "Ps", q), kind="strong-permission",
            applied=defs[0].label, defeated=defeated,
        )

    def _try_minus_dPs(self, q: Literal) -> Justification | None:
        if not self.ext.has("-", "O", q):
            return None
        defs = self._defeaters_O(q)
        if all(self._body_p_discarded(r) for (r, i) in defs):
            return Justification(
                Conclusion("-", "Ps", q), kind="refuted",
                detail="-dO q and no applicable permissive defeater",
            )
        for s, j in self._occurrences(q.complement):
            if not self._applicable_at(s, j):
                continue
            if all(
                self._discarded_at(t, k) or not self.theory.beats(t.label, s.label)
                for (t, k) in self._occurrences(q)
            ):
                return Justification(
                    Conclusion("-", "Ps", q), kind="refuted",
                    defeated=[(s.label, "undefeated counter-rule")],
                )
        return None

    # ===================================================== +/- dPw (weak)
    def _try_plus_dPw(self, q: Literal) -> Justification | None:
        if self.ext.has("-", "O", q.complement):
            return Justification(
                Conclusion("+", "Pw", q), kind="weak-permission",
                detail=f"the obligation to the contrary (O {q.complement}) is refuted",
            )
        return None

    def _try_minus_dPw(self, q: Literal) -> Justification | None:
        if self.ext.has("+", "O", q.complement):
            return Justification(
                Conclusion("-", "Pw", q), kind="refuted",
                detail=f"O {q.complement} holds, so q is not weakly permitted",
            )
        return None

    # ===================================================== +/- dP (generic)
    def _try_plus_dP(self, q: Literal) -> Justification | None:
        for src in ("Ps", "Pw"):
            if self.ext.has("+", src, q):
                return Justification(
                    Conclusion("+", "P", q), kind="permission",
                    detail=f"holds via {src}",
                )
        return None

    def _try_minus_dP(self, q: Literal) -> Justification | None:
        if self.ext.has("-", "Ps", q) and self.ext.has("-", "Pw", q):
            return Justification(
                Conclusion("-", "P", q), kind="refuted",
                detail="neither strong nor weak permission holds",
            )
        return None

    # ===================================================== +/- d_bottom
    def _try_plus_bottom(self) -> Justification | None:
        for r in self.theory.rules:
            if r.is_defeater or not self._body_p_applicable(r):
                continue
            if r.head and all(
                self.ext.has("+", "O", c) and self._violated(c) for c in r.head
            ):
                return Justification(
                    Conclusion("+", "⊥", BOTTOM), kind="non-compensable",
                    applied=r.label,
                    detail="every obligation in the chain is in force and violated",
                )
        return None

    def _try_minus_bottom(self) -> Justification | None:
        for r in self.theory.rules:
            if r.is_defeater:
                continue
            if not self._chain_cannot_trigger(r):
                return None  # some rule may still trigger non-compliance
        return Justification(
            Conclusion("-", "⊥", BOTTOM), kind="refuted",
            detail="no rule has a fully in-force, fully violated obligation chain",
        )

    def _chain_cannot_trigger(self, r: Rule) -> bool:
        if self._body_p_discarded(r) or not r.head:
            return True
        for c in r.head:
            if self.ext.has("-", "O", c) or not self._violated(c):
                return True
        return False

    # ===================================================== support closure (C)
    def _support_set_C(self) -> set[Literal]:
        S: set[Literal] = set(self.theory.facts)
        changed = True
        while changed:
            changed = False
            for r in self.theory.rules:
                if r.mode != "C" or r.is_defeater or len(r.head) != 1:
                    continue
                h = r.head[0]
                if h in S:
                    continue
                if h.complement in self.theory.facts and h not in self.theory.facts:
                    continue
                if any(self._elem_discarded(b) for b in r.body):
                    continue
                if all(
                    (b in S) if (isinstance(b, Literal) and not is_bottom(b))
                    else self._elem_applicable(b)
                    for b in r.body
                ):
                    S.add(h)
                    changed = True
        return S

    # ===================================================== main loop
    _PLUS = (
        ("C", "_try_plus_dC"), ("O", "_try_plus_dO"), ("Ps", "_try_plus_dPs"),
        ("Pw", "_try_plus_dPw"), ("P", "_try_plus_dP"),
    )
    _MINUS = (
        ("C", "_try_minus_dC"), ("O", "_try_minus_dO"), ("Ps", "_try_minus_dPs"),
        ("Pw", "_try_minus_dPw"), ("P", "_try_minus_dP"),
    )

    def compute(self) -> Extension:
        hb = self._herbrand_literals()
        outer_changed = True
        while outer_changed:
            outer_changed = False
            inner = True
            while inner:
                inner = False
                for l in hb:
                    for mod, fn in self._PLUS:
                        if not self.ext.has("+", mod, l):
                            j = getattr(self, fn)(l)
                            if j and self.ext.add(j):
                                inner = outer_changed = True
                    for mod, fn in self._MINUS:
                        if not self.ext.has("-", mod, l):
                            j = getattr(self, fn)(l)
                            if j and self.ext.add(j):
                                inner = outer_changed = True
                if not self.ext.has("+", "⊥", BOTTOM):
                    j = self._try_plus_bottom()
                    if j and self.ext.add(j):
                        inner = outer_changed = True
                if not self.ext.has("-", "⊥", BOTTOM):
                    j = self._try_minus_bottom()
                    if j and self.ext.add(j):
                        inner = outer_changed = True
            S = self._support_set_C()
            for l in hb:
                if not self.ext.has("+", "C", l) and not self.ext.has("-", "C", l):
                    if l not in S:
                        self.ext.add(
                            Justification(
                                Conclusion("-", "C", l), kind="refuted",
                                detail="unsupported (no constructive derivation)",
                            )
                        )
                        outer_changed = True
        # safety net for any tag still undecided
        for l in hb:
            for mod in MODALITIES:
                if not self.ext.has("+", mod, l) and not self.ext.has("-", mod, l):
                    self.ext.add(
                        Justification(
                            Conclusion("-", mod, l), kind="refuted",
                            detail="undecided at fixpoint (not provable)",
                        )
                    )
        if not self.ext.has("+", "⊥", BOTTOM) and not self.ext.has("-", "⊥", BOTTOM):
            self.ext.add(
                Justification(
                    Conclusion("-", "⊥", BOTTOM), kind="refuted",
                    detail="undecided at fixpoint (compliant)",
                )
            )
        return self.ext

    def _herbrand_literals(self) -> list[Literal]:
        out: list[Literal] = []
        for atom in sorted(self.theory.herbrand_atoms()):
            if atom == BOTTOM.atom:
                continue  # handled by the dedicated +/-d_bottom tag
            out.append(Literal(atom, False))
            out.append(Literal(atom, True))
        return out


def extension(theory: Theory) -> Extension:
    return Engine(theory).compute()
