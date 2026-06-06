#!/usr/bin/env python3
"""Tiny BM25 retriever over the full codice penale, for the RAG arm.

Reuses the article-index logic from `tools/gen.py` (same `Art. N.` segmentation)
so the corpus is split into article-sized passages. No external deps — a compact
BM25 over word tokens is plenty at this corpus size (~2.5k articles).
"""
from __future__ import annotations

import math
import os
import re
from collections import Counter

import offences as off

SRC = os.path.join(off.CP, "sources", "codice_penale_full.md")
ART_RE = re.compile(
    r"^\s*Art\.\s*(\d+(?:-(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies))?)\.")
_TOKEN = re.compile(r"[a-zàèéìòùA-ZÀÈÉÌÒÙ]+")

_INDEX: list[tuple[str, str]] | None = None     # [(art_num, body)]
_DOC_TOKENS: list[list[str]] = []
_DF: Counter = Counter()
_AVGDL = 0.0


def _tok(s: str) -> list[str]:
    return [t.lower() for t in _TOKEN.findall(s) if len(t) > 2]


def _build():
    global _INDEX, _DOC_TOKENS, _DF, _AVGDL
    with open(SRC, encoding="utf-8") as f:
        lines = f.readlines()
    starts = [(i, m.group(1)) for i, l in enumerate(lines) if (m := ART_RE.match(l))]
    idx = []
    for k, (i, num) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
        idx.append((num, "".join(lines[i:end]).strip()))
    _INDEX = idx
    _DOC_TOKENS = [_tok(body) for _, body in idx]
    for toks in _DOC_TOKENS:
        for t in set(toks):
            _DF[t] += 1
    _AVGDL = sum(len(t) for t in _DOC_TOKENS) / max(1, len(_DOC_TOKENS))


def search(query: str, k: int = 4) -> list[tuple[str, str]]:
    """Return the top-k (article_number, body) passages by BM25 for `query`."""
    if _INDEX is None:
        _build()
    q = _tok(query)
    N = len(_DOC_TOKENS)
    k1, b = 1.5, 0.75
    scores = []
    for di, toks in enumerate(_DOC_TOKENS):
        if not toks:
            scores.append(0.0)
            continue
        tf = Counter(toks)
        dl = len(toks)
        s = 0.0
        for term in q:
            if term not in tf:
                continue
            df = _DF[term]
            idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
            s += idf * tf[term] * (k1 + 1) / (tf[term] + k1 * (1 - b + b * dl / _AVGDL))
        scores.append(s)
    order = sorted(range(N), key=lambda i: scores[i], reverse=True)[:k]
    return [(_INDEX[i][0], _INDEX[i][1][:1200]) for i in order if scores[i] > 0]


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "impossessamento cosa mobile altrui sottrazione profitto"
    for num, body in search(q):
        print(f"== art. {num}\n{body[:200]}\n")
