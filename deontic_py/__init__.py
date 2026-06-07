"""``deontic_py`` — a typed, JSON-backed Python client for the deontic reasoner.

    from deontic_py import Deontic
    d = Deontic()
    ext = d.check("examples/ex1_license.ddl")
    ext.verdict("use")                       # "obligatory"
    d.abduce(ddl, ["P(publish)"]).minimal_configs

For agents, hand the model :data:`deontic_py.llm.TOOL_SCHEMA` and route its tool
calls through :func:`deontic_py.llm.dispatch`.
"""
from __future__ import annotations

from .client import Deontic
from .errors import (
    DeonticError,
    DeonticNotBuilt,
    DeonticParseError,
    DeonticTimeout,
)
from .llm import (
    DDL_SYNTAX,
    TOOL_SCHEMA,
    TOOL_SCHEMA_OPENAI,
    call_tool,
    dispatch,
)
from .results import (
    AbduceResult,
    AtomEntry,
    AtomStatus,
    Conflict,
    Extension,
    Provenance,
    QueryResult,
    Tag,
    status_code,
    status_to_verdict,
)

__all__ = [
    "Deontic",
    # results
    "Extension",
    "QueryResult",
    "AtomStatus",
    "Tag",
    "Conflict",
    "AbduceResult",
    "AtomEntry",
    "Provenance",
    "status_code",
    "status_to_verdict",
    # llm surface
    "TOOL_SCHEMA",
    "TOOL_SCHEMA_OPENAI",
    "DDL_SYNTAX",
    "dispatch",
    "call_tool",
    # errors
    "DeonticError",
    "DeonticNotBuilt",
    "DeonticParseError",
    "DeonticTimeout",
]
