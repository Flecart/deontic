import Deontic.Theory
import Deontic.ProofTags
import Deontic.ProofConditions

namespace Deontic

private def iterOnce (thy : Theory) (base : List Atom) (d : Derivation) : Derivation :=
  let tryTag (acc : Derivation) (pos : Bool) (mod : Modality) (q : Lit) : Derivation :=
    let tl : TaggedLit := ⟨pos, mod, q⟩
    if acc.has tl then acc
    else
      let derived := match (pos, mod) with
        | (true,  .C)  => canDerive_C_pos  thy acc q
        | (false, .C)  => canDerive_C_neg  thy acc q
        | (true,  .O)  => canDerive_O_pos  thy acc q
        | (false, .O)  => canDerive_O_neg  thy acc q
        | (true,  .Ps) => canDerive_Ps_pos thy acc q
        | (false, .Ps) => canDerive_Ps_neg thy acc q
        | (true,  .Pw) => canDerive_Pw_pos acc q
        | (false, .Pw) => canDerive_Pw_neg acc q
        | (true,  .P)  => canDerive_P_pos  acc q
        | (false, .P)  => canDerive_P_neg  acc q
      if derived then acc.push tl else acc
  let tryAtom (acc : Derivation) (a : Atom) : Derivation :=
    let lits := [Lit.pos a, Lit.neg a]
    let mods := [Modality.C, .O, .Ps, .Pw, .P]
    lits.foldl (fun acc q =>
      mods.foldl (fun acc mod =>
        tryTag (tryTag acc true mod q) false mod q)
      acc) acc
  base.foldl tryAtom d

def computeExtension (thy : Theory) : Extension :=
  let base := thy.herbrandBase
  let rec loop (d : Derivation) (fuel : Nat) : Derivation :=
    match fuel with
    | 0 => d
    | fuel + 1 =>
      let d' := iterOnce thy base d
      if d'.size == d.size then d else loop d' fuel
  let fuel := base.length * 20 + 10
  let finalD := loop #[] fuel
  ⟨finalD, canDerive_bot thy finalD⟩

end Deontic
