import Deontic.Theory
import Deontic.ProofTags
import Deontic.Extension

namespace Deontic

-- Run extension and filter all tags for a specific atom
def queryAtom (thy : Theory) (a : Atom) : Extension × List TaggedLit :=
  let ext := computeExtension thy
  (ext, ext.tagsFor a)

-- Run extension and check a specific tagged literal
def queryTagged (thy : Theory) (tl : TaggedLit) : Extension × Bool :=
  let ext := computeExtension thy
  (ext, ext.derivation.has tl)

-- Summarise normative status of an atom as a short string
def normativeStatus (ext : Extension) (a : Atom) : String :=
  let pos := Lit.pos a
  let neg := Lit.neg a
  -- Deontic tags take priority over constitutive, but constitutive facts
  -- (facts derived via constitutive rules) come before weak deontic permissions
  if      ext.derivation.hasPositive .O  pos then s!"O({a})"
  else if ext.derivation.hasPositive .O  neg then s!"F({a})"
  else if ext.derivation.hasPositive .Ps pos then s!"Ps({a})"
  else if ext.derivation.hasPositive .C  pos then s!"fact({a})"
  else if ext.derivation.hasPositive .C  neg then s!"fact(~{a})"
  else if ext.derivation.hasPositive .P  pos then s!"P({a})"
  else if ext.derivation.hasPositive .Pw pos then s!"Pw({a})"
  else "unknown"

end Deontic
