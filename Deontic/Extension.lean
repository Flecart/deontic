import Deontic.Theory
import Deontic.ProofTags
import Deontic.ProofConditions
import Deontic.Conflict

namespace Deontic

-- One Jacobi pass over the Herbrand base. Constitutive tags (`C`) are derived on
-- a bearer-neutral *flattened* view; obligation/permission tags are derived once
-- per bearer, each on the slice of the derivation that bearer can see
-- (`scopeForBearer`) under the rules that bearer owns (`scopedForBearer`). Because
-- the proof conditions only ever read those bearer-scoped, rebearered-to-`none`
-- views, `ProofConditions.lean` (the published calculus) is reused verbatim.
private def iterOnce (thy : Theory) (base : List Atom) (d : Derivation) : Derivation :=
  let viewC := d.flattenBearers
  let scopes : List (Option String × Theory × Derivation) :=
    thy.bearers.map fun b => (b, thy.scopedForBearer b, d.scopeForBearer b)
  let tryC (acc : Derivation) (pos : Bool) (q : Lit) : Derivation :=
    let tl : TaggedLit := ⟨pos, .C, none, q⟩
    if acc.has tl then acc
    else
      let derived := if pos then canDerive_C_pos thy viewC q
                            else canDerive_C_neg thy viewC q
      if derived then acc.push tl else acc
  let tryDeontic (acc : Derivation) (b : Option String) (sthy : Theory)
      (sv : Derivation) (pos : Bool) (mod : Modality) (q : Lit) : Derivation :=
    let tl : TaggedLit := ⟨pos, mod, b, q⟩
    if acc.has tl then acc
    else
      let derived := match (pos, mod) with
        | (true,  .O)  => canDerive_O_pos  sthy sv q
        | (false, .O)  => canDerive_O_neg  sthy sv q
        | (true,  .Ps) => canDerive_Ps_pos sthy sv q
        | (false, .Ps) => canDerive_Ps_neg sthy sv q
        | (true,  .Pw) => canDerive_Pw_pos sv q
        | (false, .Pw) => canDerive_Pw_neg sv q
        | (true,  .P)  => canDerive_P_pos  sv q
        | (false, .P)  => canDerive_P_neg  sv q
        | _            => false   -- C is handled bearer-neutrally by tryC
      if derived then acc.push tl else acc
  let deonticMods := [Modality.O, .Ps, .Pw, .P]
  let tryAtom (acc : Derivation) (a : Atom) : Derivation :=
    let lits := [Lit.pos a, Lit.neg a]
    let acc := lits.foldl (fun acc q => tryC (tryC acc true q) false q) acc
    scopes.foldl (fun acc (b, sthy, sv) =>
      lits.foldl (fun acc q =>
        deonticMods.foldl (fun acc mod =>
          tryDeontic (tryDeontic acc b sthy sv true mod q) b sthy sv false mod q)
        acc) acc) acc
  base.foldl tryAtom d

def computeExtension (thy : Theory) : Extension :=
  let base := thy.herbrandBase
  let rec loop (d : Derivation) (fuel : Nat) : Derivation :=
    match fuel with
    | 0 => d
    | fuel + 1 =>
      let d' := iterOnce thy base d
      if d'.size == d.size then d else loop d' fuel
  -- Jacobi passes converge in O(dependency-depth); scale fuel by the bearer count
  -- so multi-party theories have headroom.
  let fuel := (base.length + 1) * (thy.bearers.length + 1) * 20 + 20
  let finalD := loop #[] fuel
  let conflicts := findUnresolvedObligationConflicts thy finalD
  -- A violation is a *specific bearer* failing their duty: check each bearer's
  -- scoped view under its own rules.
  let viols := (thy.bearers.flatMap fun b =>
    botWitnessRules (thy.scopedForBearer b) (finalD.scopeForBearer b))
    |>.eraseDups
  ⟨finalD, !viols.isEmpty, (viols.map (·.label)).eraseDups, conflicts⟩

end Deontic
