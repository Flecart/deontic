"""Expose the `deontic` reasoner CLI as a function-calling tool.

The agentic condition gives the model this tool so it can formalize a clause as
a DDL theory and run the reasoner (check / query / abduce / atoms) for several
rounds before answering — the auditable kernel the project is built around.
"""
from __future__ import annotations
import os
import subprocess
import tempfile

DEONTIC_BIN = os.environ.get("DEONTIC_BIN", "./.lake/build/bin/deontic")
_COMMANDS = {"check", "query", "abduce", "atoms"}


def run_deontic(ddl: str, command: str = "check",
                args: list[str] | None = None, flags: list[str] | None = None) -> str:
    """Write `ddl` to a temp file and run `deontic <command> <file> <args> <flags>`."""
    args = list(args or [])
    flags = list(flags or [])
    if command not in _COMMANDS:
        return f"error: unknown command '{command}'. Use one of {sorted(_COMMANDS)}."
    if not os.path.exists(DEONTIC_BIN):
        return (f"error: reasoner not built at {DEONTIC_BIN}. "
                "Run: export PATH=\"$HOME/.elan/bin:$PATH\" && lake build deontic")
    path = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".ddl", delete=False) as f:
            f.write(ddl)
            path = f.name
        proc = subprocess.run([DEONTIC_BIN, command, path, *args, *flags],
                              capture_output=True, text=True, timeout=30)
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        if err:
            out = (out + "\n[stderr] " + err).strip()
        return out or "(no output)"
    except subprocess.TimeoutExpired:
        return "error: reasoner timed out (30s)."
    except Exception as e:  # noqa: BLE001 - surface any failure to the model
        return f"error running reasoner: {e}"
    finally:
        if path and os.path.exists(path):
            os.unlink(path)


# DDL cheat-sheet handed to the model so it can write valid theories.
DDL_SYNTAX = """\
DDL syntax (one statement per line; `#` starts a comment):
  facts: a, b            # ground facts that hold
  atom NAME: description # every atom used MUST be declared (mandatory)
  label: ant1, ant2 =>O conc     # defeasible obligation (prescriptive)
  label: =>O ~x          # prohibition: O(~x)  (empty antecedent = default)
  label: cond ~>O x      # defeater: permits x (use with superiority)
  label: cond => y       # defeasible constitutive (classification)
  superiority: rA > rB   # rA defeats rB when both apply
Querying:
  command "query" with args=["X"]  -> status of X: O(X)=obligated, F(X)=forbidden,
      Ps(X)/P(X)=permitted, fact(X)=constitutively holds, unknown=not addressed.
  command "abduce" with args=["P(X)","--all"] -> minimal fact sets that make X permitted.
  command "check"  -> full extension + violations.
Patterns: prohibition `=>O ~X` then query X -> F(X); conditional duty `cond =>O X`
with fact cond then query X -> O(X); permission `default =>O ~X` + `cond ~>O X` +
`superiority` then `abduce 'P(X)' --all` -> {cond}."""


# ── Raw-CLI condition: a scoped `bash` tool + the skill doc ────────────────────

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# `deontic` lives in the build dir; `lake` (if needed) in elan. Put both on PATH
# so the model can call `deontic ...` as a bare command.
_BIN_DIR = os.path.join(_REPO_ROOT, ".lake", "build", "bin")
_TOOL_ENV = {**os.environ,
             "PATH": f"{_BIN_DIR}:{os.path.expanduser('~/.elan/bin')}:{os.environ.get('PATH', '')}"}

# Coarse guard — a timeout + repo cwd is the real containment; this just rejects
# obviously destructive one-liners. NOT a sandbox; use only for trusted evals.
_DANGER = ("rm -rf /", "rm -rf ~", "sudo ", "mkfs", "dd if=", ":(){", "shutdown",
           "reboot", "> /dev/sd", "curl http", "wget http", "git push", "ssh ")


def run_shell(command: str) -> str:
    """Run a shell command in the repo (deontic on PATH). For the `cli` condition."""
    cmd = (command or "").strip()
    if not cmd:
        return "error: empty command"
    if any(tok in cmd for tok in _DANGER):
        return "refused: command matched a destructive/networked pattern and was not run."
    try:
        proc = subprocess.run(cmd, shell=True, cwd=_REPO_ROOT, env=_TOOL_ENV,
                              capture_output=True, text=True, timeout=30)
        out = (proc.stdout or "") + (("\n[stderr] " + proc.stderr) if proc.stderr.strip() else "")
        out = out.strip() or "(no output)"
        return out[:4000] + ("\n…[truncated]" if len(out) > 4000 else "")
    except subprocess.TimeoutExpired:
        return "error: command timed out (30s)."
    except Exception as e:  # noqa: BLE001
        return f"error running command: {e}"


def load_skill() -> str:
    with open(os.path.join(os.path.dirname(__file__), "deontic_skill.md")) as f:
        return f.read()


SHELL_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "bash",
        "description": ("Run a shell command in the project root. The `deontic` reasoner "
                        "is on PATH. Use it to write a .ddl file and run `deontic query/"
                        "abduce/check/atoms` (see the skill instructions). 30s timeout."),
        "parameters": {
            "type": "object",
            "properties": {"command": {"type": "string", "description": "The shell command to run."}},
            "required": ["command"],
        },
    },
}

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "run_deontic",
        "description": (
            "Run a defeasible deontic logic reasoner on a DDL theory you write, to "
            "decide obligations/prohibitions/permissions formally. Formalize the "
            "relevant contract/statute clause as a small DDL theory and query it.\n\n"
            + DDL_SYNTAX),
        "parameters": {
            "type": "object",
            "properties": {
                "ddl": {"type": "string",
                        "description": "The full DDL theory (atoms + rules + optional facts/superiority)."},
                "command": {"type": "string", "enum": sorted(_COMMANDS),
                            "description": "query (status of atoms), abduce (fact configs), check (full extension), atoms (dictionary)."},
                "args": {"type": "array", "items": {"type": "string"},
                         "description": "For query: atom names. For abduce: a goal like 'P(Disclose)'."},
                "flags": {"type": "array", "items": {"type": "string"},
                          "description": "Optional flags, e.g. ['--all'] for abduce, ['--trace'] for query."},
            },
            "required": ["ddl", "command"],
        },
    },
}
