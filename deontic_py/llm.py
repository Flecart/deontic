"""LLM tool-call surface for the deontic reasoner.

Hand an agent ``TOOL_SCHEMA`` (Anthropic ``tools`` format) and route its tool
calls through :func:`dispatch`. The model writes a ``.ddl`` theory and picks a
command; ``dispatch`` runs it and returns **human-readable** text — LLMs read the
reasoner's prose (statuses, ``[JUDGE: …]`` reports, violation warnings) better
than JSON. Code that wants structured results should use :class:`deontic_py.Deontic`
directly.

Generalizes ``eval/deontic_tool.py``; the schema and DDL cheat-sheet are the same
ones already proven there.
"""
from __future__ import annotations

from typing import Any

from .client import Deontic
from .errors import DeonticError

_COMMANDS = ("check", "query", "abduce", "atoms")

# DDL cheat-sheet embedded in the tool description so the model writes valid theories.
DDL_SYNTAX = """\
DDL syntax (one statement per line; `#` starts a comment):
  facts: a, b            # ground facts that hold
  atom NAME: description # every atom used MUST be declared (mandatory)
  label: ant1, ant2 =>O conc     # defeasible obligation (prescriptive)
  label: =>O ~x          # prohibition: O(~x)  (empty antecedent = default)
  label: cond ~>O x      # defeater: permits x (use with superiority)
  label: cond => y       # defeasible constitutive (classification)
  label: ant =>O@Party c # directed obligation borne by Party
  superiority: rA > rB   # rA defeats rB when both apply
Commands:
  query  args=["X","Y"]          -> status of atoms: O(X)=obligated, F(X)=forbidden,
      Ps(X)/P(X)/Pw(X)=permitted, fact(X)=constitutively holds, unresolved=judge
      must add superiority, unknown=not addressed.
  abduce args=["P(X)"] flags=["--all"] -> minimal fact sets that make a goal hold.
      Goal tokens: O(a) F(a) P(a) Ps(a) Pw(a) C(a) a ~a ; prefix ! = must NOT hold.
  check                          -> full extension + violations + conflicts.
  atoms  flags=["--resolve"]     -> the atom dictionary (descriptions/provenance).
Patterns: prohibition `=>O ~X` then query X -> F(X); conditional duty `cond =>O X`
with fact cond then query X -> O(X); permission `default =>O ~X` + `cond ~>O X` +
`superiority` then `abduce 'P(X)' --all` -> {cond}."""

TOOL_SCHEMA: dict[str, Any] = {
    "name": "run_deontic",
    "description": (
        "Run a defeasible deontic logic reasoner on a DDL theory you write, to "
        "decide obligations / prohibitions / permissions formally instead of "
        "guessing. Formalize the relevant contract or statute clause as a small "
        "DDL theory, then query it.\n\n" + DDL_SYNTAX
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "ddl": {
                "type": "string",
                "description": "The full DDL theory (atoms + rules + optional facts/superiority).",
            },
            "command": {
                "type": "string",
                "enum": list(_COMMANDS),
                "description": "query, abduce, check, or atoms.",
            },
            "args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "For query: atom names. For abduce: goals like 'P(Disclose)'.",
            },
            "flags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional flags, e.g. ['--all'] for abduce, ['--trace'] for query, ['--assume','a,~b'].",
            },
        },
        "required": ["ddl", "command"],
    },
}

# OpenAI-style {"type":"function","function":{...,"parameters":...}} variant for
# harnesses on that API.
TOOL_SCHEMA_OPENAI: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": TOOL_SCHEMA["name"],
        "description": TOOL_SCHEMA["description"],
        "parameters": TOOL_SCHEMA["input_schema"],
    },
}


def dispatch(
    ddl: str,
    command: str = "check",
    args: list[str] | None = None,
    flags: list[str] | None = None,
    *,
    client: Deontic | None = None,
) -> str:
    """Run one tool call and return human-readable reasoner output.

    Never raises: any failure (unknown command, parse error, missing binary,
    timeout) is returned as a message string so the agent sees it and can react.
    """
    args = list(args or [])
    flags = list(flags or [])
    if command not in _COMMANDS:
        return f"error: unknown command '{command}'. Use one of {list(_COMMANDS)}."
    try:
        client = client or Deontic()
        # Human prose, not JSON: drop any stray --json the model added.
        cli_args = [a for a in (*args, *flags) if a != "--json"]
        out = client._run(command, ddl, cli_args).strip()
        return out or "(no output)"
    except DeonticError as exc:
        return f"error: {exc}"
    except Exception as exc:  # noqa: BLE001 — surface any failure to the model
        return f"error running reasoner: {exc}"


def call_tool(tool_input: dict[str, Any], *, client: Deontic | None = None) -> str:
    """Convenience for Anthropic tool-use: ``dispatch`` from a tool-input dict."""
    return dispatch(
        tool_input.get("ddl", ""),
        tool_input.get("command", "check"),
        tool_input.get("args"),
        tool_input.get("flags"),
        client=client,
    )
