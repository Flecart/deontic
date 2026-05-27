/-
Proof tags, conclusions, and justification records.

A conclusion is a tagged literal `±d_X l` where X is a modality
(C, O, P, Pw, Ps, ⊥) and l a plain literal, following Governatori (2018)
pp.17-21. Prohibition is read off the obligation tag: `+dO ~l` means `Fl`.
-/
import Ddl.Syntax

namespace Ddl

/-- The deontic modalities tracked by the proof theory. `⊥` is handled by its
own dedicated tag. -/
def MODALITIES : List String := ["C", "O", "P", "Pw", "Ps"]

/-- A tagged literal, e.g. `+dC complaint` or `+dO -publish` meaning `F publish`. -/
structure Conclusion where
  sign     : String   -- "+" (provable) or "-" (refuted)
  modality : String   -- one of C, O, P, Pw, Ps, ⊥
  literal  : Literal
deriving BEq, Hashable, Repr, DecidableEq, Inhabited

namespace Conclusion

def positive (c : Conclusion) : Bool := c.sign == "+"

instance : ToString Conclusion where
  toString c := s!"{c.sign}d{c.modality} {c.literal}"

end Conclusion

/-- Why a conclusion holds, for traceability.

`kind` is a short reason code; `applied` is the supporting rule label (if any);
`defeated` lists (counter-rule, why-it-failed); `detail` is free text for the
human/LLM-facing trace. -/
structure Justification where
  conclusion : Conclusion
  kind       : String
  applied    : Option String := none
  defeated   : List (String × String) := []
  detail     : String := ""
deriving Repr, Inhabited

namespace Justification

instance : ToString Justification where
  toString j := Id.run do
    let mut parts : List String := [s!"{j.conclusion}  [{j.kind}]"]
    match j.applied with
    | some a => parts := parts ++ [s!"by {a}"]
    | none => pure ()
    for (label, why) in j.defeated do
      parts := parts ++ [s!"counter {label}: {why}"]
    if j.detail != "" then
      parts := parts ++ [j.detail]
    return String.intercalate "  " parts

end Justification

end Ddl
