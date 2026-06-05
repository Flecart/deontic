#!/usr/bin/env python3
"""Spec-driven generator for ELEMENT-DECOMPOSED penal-code articles.

NOT the rejected coarse generator: each article is still hand-decomposed into
its constitutive elements here in `specs.txt`. This script only fills the
mechanical boilerplate — atom-decl formatting, quote/uri provenance looked up
from the source text, and the precetto/tipico/pena scaffolding — so the same
decomposed `.ddl` we used to hand-write is produced from a dense spec.

Spec format (examples/codice_penale/tools/specs.txt), one article per block:

    @<num> <file> [querela] [colpa] [noprec] [agg=<AggAtom>:<overriddenPena>]
    <ElementAtom>: <description>          # one per constitutive element
    oneof[A, B]:                          # a disjunctive element (atoms shared)
    :: <PenaltyAtom>: <penalty description>

Atoms already declared in definizioni.ddl are referenced, not redeclared.
Run:  python3 examples/codice_penale/tools/gen.py
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CP   = os.path.join(HERE, "..")
SRC  = os.path.join(CP, "sources", "codice_penale_full.md")
URI  = "examples/codice_penale/sources/codice_penale_full.md"
SPECS = os.path.join(HERE, "specs.txt")

ART_RE = re.compile(r"^\s*Art\.\s*(\d+(?:-(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies))?)\.(?:\s*\(\d+\))?\s*$")


def shared_atoms():
    names = set()
    with open(os.path.join(CP, "definizioni.ddl"), encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\s*atom ([A-Za-z0-9]+):", line)
            if m:
                names.add(m.group(1))
    return names


def article_index(lines):
    """num -> (start_line_1based, end_line_1based, body_text)."""
    idx, starts = {}, []
    for i, l in enumerate(lines):
        m = ART_RE.match(l)
        if m:
            starts.append((i, m.group(1)))
    for k, (i, num) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
        body = "".join(lines[i + 1:end])
        idx[num] = (i + 1, min(end, i + 9), body)
    return idx


def first_quote(body, limit=120):
    s = re.sub(r"\s+", " ", body).strip()
    s = re.sub(r"\s*\(\d+\)", "", s).replace("|", "/")
    # skip the rubric line: take from first sentence of the operative text
    s = s.split(". ")
    out = ""
    for seg in s:
        if len(seg) > 15:
            out = seg
            break
    out = out or (s[0] if s else "")
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0]
    return out.strip()


def parse_specs(text):
    arts, cur = [], None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("@"):
            if cur:
                arts.append(cur)
            parts = line[1:].split()
            num, fil = parts[0], parts[1]
            flags = parts[2:]
            agg = None
            for fl in flags:
                if fl.startswith("agg="):
                    a, _, p = fl[4:].partition(":")
                    agg = (a, p)
            cur = dict(num=num, file=fil, flags=set(f for f in flags if "=" not in f),
                       agg=agg, elems=[], pena=None, aggdesc=None)
        elif line.startswith("::"):
            name, _, desc = line[2:].strip().partition(":")
            cur["pena"] = (name.strip(), desc.strip())
        elif line.startswith("aggpena::"):
            name, _, desc = line[len("aggpena::"):].strip().partition(":")
            cur["aggdesc"] = (name.strip(), desc.strip())
        elif line.strip() in ("querela", "colpa", "nomens", "noprec"):
            cur["flags"].add(line.strip())     # a flag written on its own line
        else:
            name, _, desc = line.partition(":")
            cur["elems"].append((name.strip(), desc.strip()))
    if cur:
        arts.append(cur)
    return arts


def emit(arts, idx, shared):
    files = {}
    for a in arts:
        files.setdefault(a["file"], []).append(a)
    for fil, group in files.items():
        out = [f"# Codice Penale — {fil} (generato da spec hand-decomposte, tools/gen.py).",
               "# Ogni reato è la congiunzione dei suoi elementi (atomi adiudicabili).",
               "from definizioni.ddl import *", "", "facts:", ""]
        for a in group:
            num = a["num"]
            lbl = num.replace("-", "")        # hyphen-free rule labels
            if num not in idx:
                raise SystemExit(f"article {num} not found in source")
            ls, le, body = idx[num]
            q = first_quote(body)
            prov = f"| quote: {q} | uri: {URI}#L{ls}-L{le}"
            # `def`: a general-part / definitional article — ground its concept(s)
            # as described atom(s) with provenance, no precetto/tipico/pena.
            if "def" in a["flags"]:
                out.append(f"# Art. {num}")
                for name, desc in a["elems"]:
                    if name not in shared and "[" not in name:
                        out.append(f"atom {name}: {desc} (art. {num}) {prov}")
                out.append("")
                continue
            body_atoms = []
            decls = []
            for name, desc in a["elems"]:
                body_atoms.append(name)
                base = re.sub(r"^oneof\[.*\]$", "", name)
                if base and "[" not in name and name not in shared:
                    decls.append(f"atom {name}: {desc} (art. {num}) {prov}")
            mens = "Colpa" if "colpa" in a["flags"] else "Dolo"
            if "nomens" not in a["flags"]:   # contravvenzioni: dolo o colpa (art. 42)
                body_atoms.append(mens)
            pena, pdesc = a["pena"]
            decls.append(f"atom {pena}: {pdesc} (art. {num}) {prov}")
            if a["agg"] and a["aggdesc"]:
                ad_name, ad_desc = a["aggdesc"]
                if ad_name not in shared:
                    decls.append(f"atom {ad_name}: {ad_desc} (art. {num}) {prov}")
            out += decls
            # precetto on first plain element
            first_plain = next((n for n, _ in a["elems"] if "[" not in n), None)
            if "noprec" not in a["flags"] and first_plain:
                out.append(f"precetto_{lbl}: =>O@Chiunque ~{first_plain}")
            head = ", ".join(body_atoms)
            out.append(f"{head} {{")
            if "querela" in a["flags"]:
                out.append(f"  proc_{lbl}:   Querela =>O@Giudice Procedibile")
                out.append(f"  tipico_{lbl}: O(Procedibile) =>O@Giudice FattoTipico")
            else:
                out.append(f"  tipico_{lbl}: =>O@Giudice FattoTipico")
            out.append(f"  pena_{lbl}:   O(Sanziona) =>O@Giudice {pena}")
            if a["agg"]:
                agg_atom, over = a["agg"]
                ad_name = a["aggdesc"][0] if a["aggdesc"] else pena
                out.append(f"  pena_{lbl}a: {agg_atom}, O(Sanziona) =>O@Giudice {ad_name}  overrides {over}")
            out.append("}")
            out.append("")
        path = os.path.join(CP, f"{fil}.ddl")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        print(f"wrote {fil}.ddl  ({len(group)} articles)")


def main():
    with open(SRC, encoding="utf-8") as f:
        lines = f.readlines()
    idx = article_index(lines)
    with open(SPECS, encoding="utf-8") as f:
        arts = parse_specs(f.read())
    emit(arts, idx, shared_atoms())
    print(f"total: {len(arts)} articles")


if __name__ == "__main__":
    main()
