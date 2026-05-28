import Deontic.Theory
import Deontic.ProofTags
import Deontic.ProofConditions

namespace Deontic

/-- Detect atoms where O(a) and O(~a) are both blocked by applicable rules with no ≺ between them. -/
def findUnresolvedObligationConflicts (thy : Theory) (d : Derivation) : List UnresolvedConflict :=
  thy.herbrandBase.filterMap fun a =>
    let q := Lit.pos a
    if d.hasPositive .O q || d.hasPositive .O q.compl then none
    else
      let forQ := applicableObligationRules thy d q
      let forQc := applicableObligationRules thy d q.compl
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
          }

end Deontic
