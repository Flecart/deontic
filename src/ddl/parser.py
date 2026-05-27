"""Parser for the ``.ddl`` surface syntax (human / test authoring).

Grammar (statement-oriented; statements are separated by newlines or ``.``):

    fact         := literal
    rule         := [label ":"] body arrow head
    superiority  := label "<" label          # left < right  ==>  right is superior
    comment      := "#" ... end-of-line

    arrow        := ("=>" | "~>") [mode]      # => defeasible, ~> defeater
    mode         := "C" | "O"                 # attached to arrow; default C
    body         := [ elem ("," elem)* ]
    head         := literal ("(x)" literal)*  # otimes chain; singleton for C
    elem         := modal | literal
    modal        := ["-"] ("O"|"F"|"P"|"Pw"|"Ps") WS literal
    literal      := ["-"] atom
    atom         := [A-Za-z_][A-Za-z0-9_]*

``F x`` is parsed to ``O(~x)`` (eq. 3). ``r < s`` records ``(r, s)`` meaning s
is superior to r.
"""

from __future__ import annotations

import re

from .syntax import (
    BOTTOM,
    BodyElem,
    Literal,
    ModalLiteral,
    Rule,
    Theory,
    normalize_chain,
)

_BOTTOM_NAMES = {"bottom", "⊥", "_bottom", "_|_"}

_ATOM = r"[A-Za-z_][A-Za-z0-9_]*"
_LITERAL_RE = re.compile(rf"^(-)?({_ATOM})$")
_MODAL_RE = re.compile(rf"^(-)?(O|F|Pw|Ps|P)\s+(-)?({_ATOM})$")
_OPS = ("O", "F", "Pw", "Ps", "P")


class ParseError(ValueError):
    pass


def _parse_literal(text: str) -> Literal:
    text = text.strip()
    if text in _BOTTOM_NAMES:
        return BOTTOM
    m = _LITERAL_RE.match(text)
    if not m:
        raise ParseError(f"invalid literal: {text!r}")
    return Literal(m.group(2), negated=bool(m.group(1)))


def _parse_body_elem(text: str) -> BodyElem:
    text = text.strip()
    m = _MODAL_RE.match(text)
    if m:
        outer_neg = bool(m.group(1))
        op = m.group(2)
        inner = Literal(m.group(4), negated=bool(m.group(3)))
        if op == "F":  # F x == O ~x
            return ModalLiteral("O", inner.complement, negated=outer_neg)
        return ModalLiteral(op, inner, negated=outer_neg)
    return _parse_literal(text)


def _split_arrow(text: str) -> tuple[str, str, str, str]:
    """Return (body_str, strength, mode, head_str)."""
    if "->" in text:
        raise ParseError("strict rules ('->') are not supported")
    for token, strength in (("=>", "defeasible"), ("~>", "defeater")):
        idx = text.find(token)
        if idx == -1:
            continue
        body_str = text[:idx]
        after = text[idx + 2 :]
        mode = "C"
        if after[:1] in ("C", "O") and (len(after) == 1 or after[1].isspace()):
            mode = after[0]
            after = after[1:]
        return body_str, strength, mode, after
    raise ParseError(f"no rule arrow in: {text!r}")


def _parse_head(text: str) -> tuple[Literal, ...]:
    parts = text.split("(x)")
    return normalize_chain(tuple(_parse_literal(p) for p in parts))


def _parse_rule(stmt: str, auto_label: str) -> Rule:
    label = auto_label
    head_side = stmt
    # A label is "id:" appearing before the arrow.
    arrow_pos = min(
        (p for p in (stmt.find("=>"), stmt.find("~>")) if p != -1),
        default=-1,
    )
    colon = stmt.find(":")
    if colon != -1 and (arrow_pos == -1 or colon < arrow_pos):
        label = stmt[:colon].strip()
        head_side = stmt[colon + 1 :]
    body_str, strength, mode, head_str = _split_arrow(head_side)
    body = tuple(
        _parse_body_elem(b) for b in body_str.split(",") if b.strip()
    )
    head = _parse_head(head_str)
    if not head or not head_str.strip():
        raise ParseError(f"rule {label!r} has empty head")
    return Rule(label=label, mode=mode, strength=strength, body=body, head=head)


def _statements(source: str) -> list[str]:
    # Strip comments, then split on newlines and periods (periods not inside
    # a token; our tokens never contain '.', so a plain split is safe).
    lines = []
    for line in source.splitlines():
        line = line.split("#", 1)[0]
        lines.append(line)
    cleaned = "\n".join(lines)
    raw = re.split(r"[.\n]", cleaned)
    return [s.strip() for s in raw if s.strip()]


def parse(source: str) -> Theory:
    theory = Theory()
    auto = 0
    for stmt in _statements(source):
        if ("=>" in stmt) or ("~>" in stmt):
            auto += 1
            rule = _parse_rule(stmt, auto_label=f"_r{auto}")
            theory.rules.append(rule)
        elif "<" in stmt:
            left, right = stmt.split("<", 1)
            theory.superiority.add((left.strip(), right.strip()))
        else:
            theory.facts.add(_parse_literal(stmt))
    _validate(theory)
    return theory


def _validate(theory: Theory) -> None:
    labels = {r.label for r in theory.rules}
    for weaker, stronger in theory.superiority:
        for ref in (weaker, stronger):
            if ref not in labels:
                raise ParseError(
                    f"superiority references unknown rule {ref!r}"
                )


def parse_file(path: str) -> Theory:
    with open(path, "r", encoding="utf-8") as fh:
        return parse(fh.read())
