/-
Defeasible Deontic Logic (DDL) inference engine.

Reference implementation of Governatori (2018), "Practical Normative Reasoning
with Defeasible Deontic Logic", ported to Lean 4 from the Python `src/ddl`.
-/
import Ddl.Syntax
import Ddl.Proof
import Ddl.Engine
import Ddl.Parser
import Ddl.Render
import Ddl.Api
import Ddl.JsonIo
