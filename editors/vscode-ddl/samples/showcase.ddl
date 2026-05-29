# showcase.ddl — exercises every DDL token for grammar maintenance.
# After editing the grammar, open this file and eyeball the colours.

# imports (keyword.control.import) — bare, aliased, and glob
import definitions.ddl
import definitions.ddl as roles
from definitions.ddl import *

# atom declaration: keyword + atom name + provenance keys + line selector
atom Disclose: holds when CI is disclosed | quote: ...source text... | uri: sources/nda.md#L3-L6
atom NeedToKnow: holds when the person needs to know

# sections
facts: license, commission, use

# rule labels + arrows (strict/defeasible/defeater, constitutive/prescriptive)
strict_c:     a        ->   b
strict_o:     a        ->O  b
default_o:               =>O  ~use
classify:     Director  =>   Representative
defeater_o:   license   ~>O  use
defeater_c:   ProblemCall, FirstCall  ~>  complaint

# deontic operators in antecedents/conclusions, compensatory chain
remedy:       =>O  ~publish * remove
perm_guard:   P(publish)  ~>O  comment
roles_ref:    roles.Representative, NeedToKnow  ~>O  Disclose

# superiority relation and a trailing comment
superiority: defeater_o > default_o, classify > default_o   # specific beats general
