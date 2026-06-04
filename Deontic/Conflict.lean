import Deontic.Theory
import Deontic.ProofTags
import Deontic.ProofConditions

namespace Deontic

/-- Conflicts for a single bearer `b`: atoms where O(a) and O(~a) are both blocked
by `b`'s applicable rules with no ≺ between them. `sthy`/`sv` are the theory and
derivation scoped to `b` (see `Theory.scopedForBearer` / `Derivation.scopeForBearer`),
so only same-bearer rules attack — a different party's opposite duty is no conflict. -/
private def conflictsForBearer (thy sthy : Theory) (sv : Derivation)
    (b : Option String) : List UnresolvedConflict :=
  sthy.herbrandBase.filterMap fun a =>
    let q := Lit.pos a
    if sv.hasPositive .O q || sv.hasPositive .O q.compl then none
    else
      let forQ  := applicableObligationRules sthy sv q
      let forQc := applicableObligationRules sthy sv q.compl
      if forQ.isEmpty || forQc.isEmpty then none
      else
        let pairs : List (String × String) :=
          forQ.foldl (fun acc r =>
            acc ++ forQc.map fun s => (r.label, s.label)) [] |>
          List.filter fun (rl, sl) => !thy.defeats rl sl && !thy.defeats sl rl
        let pairs := pairs.eraseDups
        if pairs == [] then none
        else
          some {
            atom := a
            forO := forQ.map (·.label) |>.eraseDups
            againstO := forQc.map (·.label) |>.eraseDups
            pairs := pairs
            bearer := b
          }

/-- Detect, per bearer, atoms where O(a) and O(~a) are both blocked by that
bearer's applicable rules with no ≺ between them. Obligations of *different*
bearers on the same atom never conflict — they are independent norms. -/
def findUnresolvedObligationConflicts (thy : Theory) (d : Derivation) : List UnresolvedConflict :=
  thy.bearers.flatMap fun b =>
    conflictsForBearer thy (thy.scopedForBearer b) (d.scopeForBearer b) b

end Deontic
