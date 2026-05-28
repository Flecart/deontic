namespace Deontic

abbrev Atom := String

inductive Lit where
  | pos : Atom → Lit
  | neg : Atom → Lit
  deriving BEq, DecidableEq, Repr

def Lit.atom : Lit → Atom
  | .pos a => a
  | .neg a => a

def Lit.compl : Lit → Lit
  | .pos a => .neg a
  | .neg a => .pos a

def Lit.isNeg : Lit → Bool
  | .neg _ => true
  | .pos _ => false

instance : ToString Lit where
  toString
    | .pos a => a
    | .neg a => "~" ++ a

inductive DeonticOp where
  | O   -- obligation
  | F   -- forbidden (= O~)
  | P   -- generic permission
  | Pw  -- weak permission
  | Ps  -- strong permission
  deriving BEq, Repr

instance : ToString DeonticOp where
  toString
    | .O  => "O"
    | .F  => "F"
    | .P  => "P"
    | .Pw => "Pw"
    | .Ps => "Ps"

structure DeonticLit where
  op  : DeonticOp
  lit : Lit
  deriving BEq, Repr

instance : ToString DeonticLit where
  toString dl := s!"{dl.op}({dl.lit})"

inductive Literal where
  | plain   : Lit → Literal
  | deontic : DeonticLit → Literal
  deriving BEq, Repr

instance : ToString Literal where
  toString
    | .plain l  => toString l
    | .deontic d => toString d

-- ⊗-expression: non-empty list of plain literals (a1 * a2 * ... * an)
-- Represents compensatory obligation chains from §2.2
abbrev OExpr := List Lit

def OExpr.toStr (e : OExpr) : String :=
  " * ".intercalate (e.map (fun l => toString l))

end Deontic
