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

import os
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .client import Deontic, _find_repo_root
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
      must add superiority, unknown=not addressed. flags=["--why"] -> proof
      certificate: the applicable rules on each side, with superiority defeats.
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


# ── Raw-CLI / bash tool ───────────────────────────────────────────────────────
#
# A shell tool for agents that want to write a .ddl file and run `deontic ...`
# (or compose several commands) rather than go through `run_deontic`. The
# permission model is Anthropic-style and binary at the top level:
#
#   • dangerous=True  → everything is permitted (full shell, any working dir).
#                       Containment is the timeout alone. Trusted evals only.
#   • dangerous=False → a *specification* applies: the executable must be in
#                       `allowed_commands` and the working dir must sit inside
#                       `allowed_dirs`; the command runs WITHOUT a shell, so
#                       pipes / redirection / chaining are rejected.
#
# Default policy: run only `deontic`, only inside the repo — the safe "raw CLI"
# condition (an allowlist, vs the blocklist eval/deontic_tool.py used).

_MAX_OUTPUT = 4000
# Shell control characters that let a single command escape an allowlist.
_SHELL_METACHARS = ";|&<>$`()\n{}*?!"


def _repo_root() -> str:
    root = _find_repo_root(Path(__file__).resolve().parent)
    return str(root) if root else os.getcwd()


@dataclass
class CLIPolicy:
    """What the bash tool is allowed to do (Anthropic-style, all-or-spec).

    Attributes
    ----------
    dangerous:
        If true, **everything** is permitted: any command via a real shell, in
        any directory. If false, the fields below specify what is allowed.
    allowed_commands:
        Executable basenames the model may invoke (ignored when ``dangerous``).
    allowed_dirs:
        Directories the command may run in (and under). Empty → the run's own
        working dir only (which defaults to the repo root).
    deontic_on_path:
        Prepend the built-binary dir and ``~/.elan/bin`` to ``PATH`` so
        ``deontic`` (and ``lake``) are callable as bare commands.
    timeout:
        Per-call wall-clock limit in seconds.
    """

    dangerous: bool = False
    allowed_commands: tuple[str, ...] = ("deontic",)
    allowed_dirs: tuple[str, ...] = ()
    deontic_on_path: bool = True
    timeout: float = 30.0


def _tool_env(policy: CLIPolicy) -> dict[str, str]:
    env = dict(os.environ)
    if policy.deontic_on_path:
        bin_dir = os.path.join(_repo_root(), ".lake", "build", "bin")
        elan = os.path.expanduser("~/.elan/bin")
        env["PATH"] = f"{bin_dir}:{elan}:{env.get('PATH', '')}"
    return env


def _within(path: str, roots: tuple[str, ...]) -> bool:
    rp = os.path.realpath(path)
    for r in roots:
        rr = os.path.realpath(r)
        if rp == rr or rp.startswith(rr + os.sep):
            return True
    return False


def _format_proc(proc: subprocess.CompletedProcess) -> str:
    out = (proc.stdout or "")
    if (proc.stderr or "").strip():
        out += "\n[stderr] " + proc.stderr
    out = out.strip() or "(no output)"
    if len(out) > _MAX_OUTPUT:
        out = out[:_MAX_OUTPUT] + "\n…[truncated]"
    return out


def run_cli(
    command: str, *, cwd: str | None = None, policy: CLIPolicy | None = None
) -> str:
    """Run a shell command under ``policy``. Never raises — errors come back as text.

    In dangerous mode the command runs through a real shell. Otherwise it is
    split with :func:`shlex.split` and executed directly (no shell), with the
    executable and working dir checked against the policy.
    """
    policy = policy or CLIPolicy()
    cmd = (command or "").strip()
    if not cmd:
        return "error: empty command"
    env = _tool_env(policy)
    workdir = cwd or _repo_root()

    if policy.dangerous:
        try:
            proc = subprocess.run(
                cmd, shell=True, cwd=workdir, env=env,
                capture_output=True, text=True, timeout=policy.timeout,
            )
        except subprocess.TimeoutExpired:
            return f"error: command timed out ({policy.timeout}s)."
        except Exception as exc:  # noqa: BLE001
            return f"error running command: {exc}"
        return _format_proc(proc)

    # Restricted mode: allowlisted executable, no shell, confined working dir.
    if any(c in cmd for c in _SHELL_METACHARS):
        return ("refused: shell operators (pipes, redirection, chaining, globs) "
                "are disabled in restricted mode — run one command at a time, "
                "or use a policy with dangerous=True.")
    try:
        argv = shlex.split(cmd)
    except ValueError as exc:
        return f"error: could not parse command: {exc}"
    if not argv:
        return "error: empty command"
    exe = os.path.basename(argv[0])
    if exe not in policy.allowed_commands:
        return (f"refused: '{exe}' is not an allowed command "
                f"{sorted(policy.allowed_commands)}.")
    roots = policy.allowed_dirs or (workdir,)
    if not _within(workdir, roots):
        return (f"refused: working dir '{workdir}' is outside the allowed "
                f"folders {list(roots)}.")
    try:
        proc = subprocess.run(
            argv, shell=False, cwd=workdir, env=env,
            capture_output=True, text=True, timeout=policy.timeout,
        )
    except FileNotFoundError:
        return f"error: command not found on PATH: {argv[0]}"
    except subprocess.TimeoutExpired:
        return f"error: command timed out ({policy.timeout}s)."
    except Exception as exc:  # noqa: BLE001
        return f"error running command: {exc}"
    return _format_proc(proc)


def cli_tool_schema(policy: CLIPolicy | None = None) -> dict[str, Any]:
    """Anthropic-format ``bash`` tool whose description reflects ``policy``.

    The description tells the model exactly what is permitted, so it doesn't
    waste turns probing the boundary.
    """
    policy = policy or CLIPolicy()
    if policy.dangerous:
        scope = ("UNRESTRICTED: any shell command, any directory. Use it to "
                 "write a .ddl file and run `deontic check|query|abduce|atoms`.")
    else:
        cmds = ", ".join(sorted(policy.allowed_commands))
        dirs = ", ".join(policy.allowed_dirs) or "the project root"
        scope = (f"Restricted: only these commands are allowed — {cmds}; only "
                 f"inside {dirs}. One command per call (no pipes, redirection, "
                 f"chaining, or globs). `deontic` is on PATH.")
    return {
        "name": "bash",
        "description": (
            "Run a command line. " + scope + " " + str(int(policy.timeout)) +
            "s timeout.\n\n" + DDL_SYNTAX),
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string",
                            "description": "The command line to run."},
            },
            "required": ["command"],
        },
    }


def cli_tool_schema_openai(policy: CLIPolicy | None = None) -> dict[str, Any]:
    """OpenAI function-calling variant of :func:`cli_tool_schema`."""
    s = cli_tool_schema(policy)
    return {"type": "function", "function": {
        "name": s["name"], "description": s["description"],
        "parameters": s["input_schema"]}}


def dispatch_cli(
    tool_input: dict[str, Any], *, policy: CLIPolicy | None = None
) -> str:
    """Route a ``bash`` tool call (input dict) through :func:`run_cli`."""
    return run_cli(tool_input.get("command", ""), policy=policy)
