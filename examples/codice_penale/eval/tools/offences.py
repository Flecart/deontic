#!/usr/bin/env python3
"""Offence catalogue — the source of truth for *which atoms* an offence has.

Parses the hand-written element-decomposed `.ddl` files (furto, omicidio,
rapina, lesioni, …) and recovers, per offence:

    Offence(art, file, elements[], oneof_groups[], mens, penalty_atom,
            aggravated[], procedibilita[])

The encoding is regular (see CLAUDE.md + docs/architecture.md §Parser):
  - a precondition block `A, B, C { … }` lists the constitutive elements;
  - `pena_<art>: … =>O@Giudice <PenaltyAtom>` gives the base penalty atom;
  - `… overrides <Base>` marks an aggravated penalty (lex specialis);
  - `proc_<art>: <cond> =>O@Giudice Procedibile` gives the procedibilità trigger;
  - `oneof[A, B]` (in a block head or a rule body) is a disjunctive element.

The scriminanti / non-imputability atoms live in `parte_generale.ddl` and apply
to every offence transitively (definizioni.ddl re-exports it); they are returned
by `scriminanti()` so the generator can toggle them on any offence.

This module is intentionally read-only and dependency-free (stdlib re only) so
it can run from a bare checkout.  `python3 offences.py` prints the catalogue.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
CP = os.path.normpath(os.path.join(HERE, "..", ".."))          # examples/codice_penale
REPO = os.path.normpath(os.path.join(CP, "..", ".."))          # repo root

# Offence files we decompose for the eval (hand-written, richer than gen.py output).
OFFENCE_FILES = ["furto.ddl", "omicidio.ddl", "rapina.ddl", "lesioni.ddl"]

ONEOF_RE = re.compile(r"oneof\[([^\]]*)\]")
RULE_RE = re.compile(
    r"^\s*(?P<label>\w+):\s*(?P<body>.*?)=>O(?:@(?P<bearer>\w+))?\s+(?P<head>.+?)\s*$"
)
ATOM_DECL_RE = re.compile(r"^\s*atom\s+(\w+)\s*:")


@dataclass
class Offence:
    art: str                       # rule-label suffix, e.g. "624", "582"
    file: str                      # relative path from repo root
    name: str                      # human label, e.g. "furto"
    elements: list[str] = field(default_factory=list)        # plain conjunctive elements
    oneof_groups: list[list[str]] = field(default_factory=list)  # disjunctive element groups
    mens: str | None = None        # "Dolo" | "Colpa" | None
    penalty_atom: str | None = None
    aggravated: list[tuple[str, list[str]]] = field(default_factory=list)
    # ^ (aggravated_penalty_atom, trigger_atoms) where any trigger flips to it
    procedibilita: list[list[str]] = field(default_factory=list)
    # ^ list of alternative trigger groups (each an OR-group); empty => d'ufficio

    def base_config(self) -> dict[str, int]:
        """The minimal 'offence committed' config: every element + one of each
        oneof group + mens + (if a querela exists) the first procedibilità OR-group."""
        cfg = {a: 1 for a in self.elements}
        for grp in self.oneof_groups:
            cfg[grp[0]] = 1
        if self.mens:
            cfg[self.mens] = 1
        if self.procedibilita:
            for a in self.procedibilita[0]:
                cfg[a] = 1
        return cfg

    def all_atoms(self) -> list[str]:
        out = list(self.elements)
        for grp in self.oneof_groups:
            out += grp
        if self.mens:
            out.append(self.mens)
        for grp in self.procedibilita:
            out += grp
        if self.penalty_atom:
            out.append(self.penalty_atom)
        for pen, trig in self.aggravated:
            out.append(pen)
            out += trig
        # de-dup, preserve order
        seen, res = set(), []
        for a in out:
            if a not in seen:
                seen.add(a)
                res.append(a)
        return res


def _strip_comment(line: str) -> str:
    # naive: a '#' not inside a quote starts a comment (the .ddl quotes use '|', not '#')
    return line.split("#", 1)[0].rstrip()


def _split_top(s: str) -> list[str]:
    """Split a comma list, but keep `oneof[a, b]` together."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def parse_file(path: str) -> list[Offence]:
    """Recover offences from one .ddl file by tracking precondition blocks."""
    with open(path, encoding="utf-8") as f:
        raw = f.readlines()
    rel = os.path.relpath(path, REPO)
    name = os.path.splitext(os.path.basename(path))[0]

    # Pass 1: collect blocks as (head_atoms, [rule_lines]). A block is
    #   <comma list> {
    #     <rules…>
    #   }
    offences: list[Offence] = []
    needs_proc, block_lines = [], []      # offences awaiting file-level procedibilità
    file_proc: list[list[str]] = []       # top-level proc_* trigger OR-groups
    i, n = 0, len(raw)
    while i < n:
        line = _strip_comment(raw[i])
        if line.endswith("{"):
            head_src = line[:-1].strip()
            head = _split_top(head_src)
            body_lines = []
            i += 1
            while i < n and _strip_comment(raw[i]).strip() != "}":
                bl = _strip_comment(raw[i])
                if bl.strip():
                    body_lines.append(bl)
                i += 1
            o = _block_to_offence(name, rel, head, body_lines)
            offences.append(o)
            if not o.procedibilita and any("Procedibile" in bl for bl in body_lines):
                needs_proc.append(o)
        else:
            m = RULE_RE.match(line)
            if m and m.group("label").startswith("proc"):
                grp = _body_triggers(m.group("body").strip().rstrip(",").strip())
                if grp:
                    file_proc.append(grp)
        i += 1
    for o in needs_proc:                  # attach file-level procedibilità triggers
        o.procedibilita = [g for g in file_proc]
    return offences


def _block_to_offence(name, rel, head, body_lines) -> Offence:
    elements, oneof_groups, mens = [], [], None
    for tok in head:
        m = ONEOF_RE.search(tok)
        if m:
            oneof_groups.append([a.strip() for a in m.group(1).split(",")])
        elif tok in ("Dolo", "Colpa"):
            mens = tok
        elif tok:
            elements.append(tok)

    penalty, aggravated, proc = None, [], []
    art = None
    for bl in body_lines:
        m = RULE_RE.match(bl)
        if not m:
            continue
        label, body, headlit = m.group("label"), m.group("body"), m.group("head")
        # `overrides X` clause splits off the conclusion atom
        override = None
        if " overrides " in headlit:
            headlit, override = [s.strip() for s in headlit.split(" overrides ", 1)]
        concl = headlit.strip().lstrip("~")
        body = body.strip().rstrip(",").strip()

        if label.startswith("pena"):
            art = art or re.sub(r"\D+", "", label) or label
            if override:                      # aggravated penalty
                trig = _body_triggers(body)
                aggravated.append((concl, trig))
            else:
                penalty = concl
        elif label.startswith("tipico"):
            # a oneof in the tipico body is also a (disjunctive) constitutive element
            for grp in _body_oneofs(body):
                if grp not in oneof_groups:
                    oneof_groups.append(grp)
        elif label.startswith("proc"):
            grp = _body_triggers(body)
            if grp:
                proc.append(grp)
    # An `overrides` with no plain trigger is the block's BASE penalty under
    # lex specialis (e.g. lesione overrides percosse), not an aggravator.
    if penalty is None:
        for k, (pen, trig) in enumerate(list(aggravated)):
            if not trig:
                penalty = pen
                aggravated.pop(k)
                break
    return Offence(
        art=art or "?", file=rel, name=name, elements=elements,
        oneof_groups=oneof_groups, mens=mens, penalty_atom=penalty,
        aggravated=aggravated, procedibilita=proc,
    )


def _body_triggers(body: str) -> list[str]:
    """Atoms in a rule body that are plain facts (drop O(...) deontic guards)."""
    out = []
    for tok in _split_top(body):
        m = ONEOF_RE.search(tok)
        if m:
            out += [a.strip() for a in m.group(1).split(",")]
        elif tok and not tok.startswith("O(") and not tok.startswith("P("):
            out.append(tok)
    return out


def _body_oneofs(body: str) -> list[list[str]]:
    return [[a.strip() for a in m.split(",")] for m in ONEOF_RE.findall(body)]


def scriminanti() -> dict[str, str]:
    """Atom -> one-line gloss for the parte_generale (non-)punishability causes."""
    out = {}
    pg = os.path.join(CP, "parte_generale.ddl")
    with open(pg, encoding="utf-8") as f:
        for line in f:
            m = ATOM_DECL_RE.match(line)
            if m and m.group(1) not in ("Sanziona", "FattoTipico"):
                gloss = line.split(":", 2)[2].split("|")[0].strip() if line.count(":") >= 2 else ""
                out[m.group(1)] = gloss
    return out


def penalties_for_file(file_rel: str) -> list[str]:
    """All penalty atoms (base + aggravated) for offences encoded in `file_rel`."""
    pens: list[str] = []
    for o in catalogue().values():
        if o.file == file_rel:
            if o.penalty_atom:
                pens.append(o.penalty_atom)
            pens += [p for p, _ in o.aggravated]
    seen, out = set(), []
    for p in pens:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def groundable_atoms_for_file(file_rel: str) -> dict[str, str]:
    """Atom -> gloss for everything the grounding LLM may set true on this offence:
    the constitutive elements (+ oneof + mens + procedibilità) of each offence in
    the file, plus the shared scriminanti / non-imputability causes."""
    out: dict[str, str] = {}
    descs = _atom_descriptions()
    for o in catalogue().values():
        if o.file != file_rel:
            continue
        for a in o.elements + [x for g in o.oneof_groups for x in g] + \
                 [x for g in o.procedibilita for x in g] + ([o.mens] if o.mens else []):
            out.setdefault(a, descs.get(a, ""))
    for a, gloss in scriminanti().items():
        out.setdefault(a, gloss)
    return out


def _atom_descriptions() -> dict[str, str]:
    """Atom -> first-line gloss, scanned across the codice_penale .ddl files."""
    out: dict[str, str] = {}
    for fn in os.listdir(CP):
        if not fn.endswith(".ddl"):
            continue
        with open(os.path.join(CP, fn), encoding="utf-8") as f:
            for line in f:
                m = re.match(r"\s*atom\s+(\w+)\s*:\s*([^|]+)", line)
                if m:
                    out.setdefault(m.group(1), m.group(2).strip())
    return out


def catalogue() -> dict[str, Offence]:
    """All offences keyed by a stable slug (file:art, or file when single block)."""
    cat: dict[str, Offence] = {}
    for fn in OFFENCE_FILES:
        path = os.path.join(CP, fn)
        offs = parse_file(path)
        single = len(offs) == 1
        for o in offs:
            key = o.name if single else f"{o.name}_{o.art}"
            cat[key] = o
    return cat


if __name__ == "__main__":
    cat = catalogue()
    for key, o in cat.items():
        print(f"== {key}  (art {o.art}, {o.file})")
        print(f"   elements:   {o.elements}")
        print(f"   oneof:      {o.oneof_groups}")
        print(f"   mens:       {o.mens}")
        print(f"   penalty:    {o.penalty_atom}")
        print(f"   aggravated: {o.aggravated}")
        print(f"   proc:       {o.procedibilita}")
    print(f"\nscriminanti (apply to all): {list(scriminanti())}")
