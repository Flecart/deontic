#!/usr/bin/env python3
"""Fetch a Find Case Law judgment and scaffold a cases/*.md file.

Find Case Law serves every judgment as LegalDocML/Akoma Ntoso XML at
<judgment-url>/data.xml — structured sections with headings, so case intake
needs no PDF parsing. This tool:

  1. fetches and caches the XML (cache/<slug>.xml — also our provenance copy);
  2. splits the body into sections by heading, in document order;
  3. WITHHOLDS the tribunal's own reasoning (headings matching discussion/
     conclusion) into cache/<slug>_reasoning.txt — needed for gold-labelling,
     never prompt material;
  4. writes a draft cases/<slug>.md in the pipeline's format, background
     pre-filled with the kept sections, gold fields left TODO.

The draft is a scaffold: a human must curate the background (it still contains
party submissions and procedural noise) and fill Oracle facts / Gold rules
from the withheld reasoning before the case is usable.

  python docs/experiments/foia_corpus/fetch_case.py ukftt/grc/2024/601
  python docs/experiments/foia_corpus/fetch_case.py \
      https://caselaw.nationalarchives.gov.uk/ukftt/grc/2025/61 --force

Licence note: bulk/programmatic re-use of Find Case Law content may require
TNA's computational-analysis licence — this tool is for hand-picked pilot
cases, one fetch at a time, with an identifying User-Agent.
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = "https://caselaw.nationalarchives.gov.uk"
HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
CASES = HERE / "cases"
USER_AGENT = "deontic-foia-pilot/0.1 (academic research, single-case fetches)"

# Tribunal-reasoning headings: withheld from the background draft (leakage
# control); everything else is kept for human curation.
WITHHOLD = re.compile(r"discussion|conclusion|reasons? and decision", re.I)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def text_of(el: ET.Element) -> str:
    return re.sub(r"\s+", " ", " ".join(el.itertext())).strip()


def norm_path(arg: str) -> str:
    """Accept a full FCL URL or a bare path like ukftt/grc/2024/601."""
    path = re.sub(r"^https?://[^/]+/", "", arg.strip()).strip("/")
    return re.sub(r"/data\.xml$", "", path)


def fetch_xml(path: str, refresh: bool) -> tuple[str, str]:
    slug = re.sub(r"[^a-z0-9]+", "_", path.lower()).strip("_")
    CACHE.mkdir(exist_ok=True)
    cached = CACHE / f"{slug}.xml"
    if cached.exists() and not refresh:
        print(f"  using cached {cached.relative_to(HERE)}")
        return slug, cached.read_text()
    url = f"{BASE}/{path}/data.xml"
    print(f"  fetching {url}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        text = resp.read().decode("utf-8")
    cached.write_text(text)
    return slug, text


def _headingish(el: ET.Element, t: str) -> str | None:
    """FCL's parser marks few real <heading>s; most section titles are styled
    spans inside a short <p>. Return "major" (bold) / "minor" (italic or
    underline — sub-headings) when the whole p is one styled title."""
    if not t or len(t) > 90 or t[0].isdigit():
        return None
    spans = [s for s in el.iter() if local(s.tag) == "span"]
    for s in spans:
        style = s.get("style", "")
        if text_of(s) != t:
            continue
        if "font-weight:bold" in style:
            return "major"
        if "text-decoration" in style or "font-style:italic" in style:
            return "minor"
    return None


def parse_judgment(xml_text: str) -> dict:
    """Header metadata + body sections in document order, each
    `(heading, level, [paragraph texts])` with level major/minor (minor =
    styled sub-heading; inherits its major section's withhold state)."""
    root = ET.fromstring(xml_text)
    header = body = None
    name = cite = None
    for el in root.iter():
        ln = local(el.tag)
        if ln == "header" and header is None:
            header = el
        elif ln == "judgmentBody" and body is None:
            body = el
        elif ln == "FRBRname" and name is None:
            name = el.get("value")
        elif ln in ("cite", "neutralCitation") and cite is None:
            cite = text_of(el) or el.get("value")

    header_text = text_of(header) if header is not None else ""
    if not cite:
        m = re.search(r"\[\d{4}\]\s+\w+\s+\d+\s+\([A-Z]+\)", header_text)
        cite = m.group(0) if m else "?"
    m = re.search(r"[Aa]ppeal is ([A-Za-z][A-Za-z ]*?)[.…]", header_text)
    disposition_hint = m.group(1).strip().lower() if m else None

    # (heading, level, paras) accumulated by an explicit walk: real <heading>s
    # and whole-p styled titles open sections; <paragraph>s (and stray body
    # <p>s) append to the current one. Subtrees of handled nodes are not
    # re-entered, so paragraph-internal <p>/<span>s can't fire as headings.
    sections: list[list] = [["(preamble)", "major", []]]

    def open_section(h: str, level: str) -> None:
        sections.append([h, level, []])

    def walk(el: ET.Element) -> None:
        ln = local(el.tag)
        if ln in ("heading", "crossHeading"):
            h = text_of(el)
            if h:
                open_section(h, "major")
            return
        if ln == "paragraph":
            t = text_of(el)
            if t:
                sections[-1][2].append(t)
            return
        if ln == "p":
            t = text_of(el)
            kind = _headingish(el, t)
            if kind:
                open_section(t, kind)
            elif t:
                sections[-1][2].append(t)
            return
        for child in el:
            walk(child)

    if body is not None:
        walk(body)
    # Empty sections are kept: an umbrella heading ("Discussion and
    # conclusions") owns no paragraphs but must still flip the withhold state.
    return {
        "name": name,
        "cite": cite,
        "header_text": header_text,
        "disposition_hint": disposition_hint,
        "sections": [(h, lvl, ps) for h, lvl, ps in sections],
    }


def split_kept_withheld(sections, withhold_from: str | None = None
                        ) -> tuple[list, list]:
    """Sticky withholding: an FTT decision is facts/law/submissions first,
    discussion last — once a heading triggers, everything to the end is the
    tribunal's own reasoning. The WITHHOLD regex catches the common
    "Discussion and conclusions" umbrella, but decisions without one (e.g.
    Driver: analysis under "Legitimate Interest of the Request") need a manual
    cut: `withhold_from` starts withholding at the first heading containing
    that substring (case-insensitive). ALWAYS eyeball the printed split —
    issue-style headings appear on both the submissions and the analysis side,
    so no heuristic is reliable."""
    kept, withheld = [], []
    withholding = False
    for heading, level, paras in sections:
        if not withholding and withhold_from \
                and withhold_from.lower() in heading.lower():
            withholding = True
        if level == "major" and not withholding:
            withholding = bool(WITHHOLD.search(heading))
        if paras:
            (withheld if withholding else kept).append((heading, paras))
    return kept, withheld


def background_text(kept: list) -> str:
    """The raw kept sections as the case background — deliberately NOT
    summarized or hand-curated: condensing is a selection-bias risk, and
    procedural noise hits every arm equally."""
    return "\n\n".join(f"### {h}\n\n" + "\n\n".join(ps) for h, ps in kept)


def scaffold(path: str, slug: str, j: dict, out: Path,
             labels: dict | None = None,
             withhold_from: str | None = None) -> None:
    kept, withheld = split_kept_withheld(j["sections"], withhold_from)
    for h, ps in kept:
        print(f"    KEEP {h} ({len(ps)} paras)")
    for h, ps in withheld:
        print(f"    HIDE {h} ({len(ps)} paras)")

    reasoning = CACHE / f"{slug}_reasoning.txt"
    reasoning.write_text(
        f"# Withheld tribunal reasoning — {j['cite']}\n"
        "# Gold-labelling material; NEVER include in a prompt.\n\n"
        + "\n\n".join(f"== {h} ==\n" + "\n\n".join(ps) for h, ps in withheld)
        + "\n"
    )

    disp = j["disposition_hint"] or "(not detected)"
    lab = labels or {}
    oracle = ", ".join(lab.get("oracle_facts", [])) or "TODO"
    gold = lab.get("gold", "TODO")
    engaged = ", ".join(lab.get("engaged", [])) if labels else "TODO"
    pi = lab.get("pi", "TODO")
    exemptions = lab.get("exemptions", "TODO")
    notes = (f"\n<!-- label-draft notes ({lab.get('model', '?')}): "
             f"{lab.get('notes', '')} -->\n" if labels else "")
    md = f"""# {j['name'] or 'TODO: case name'}

citation: {j['cite']}
url: {BASE}/{path}
exemptions: {exemptions}
verified: no

<!-- verified: flip to `yes` after a human has checked Oracle facts / Gold /
     Gold rules against cache/{slug}_reasoning.txt. The pipeline skips
     unverified cases unless --allow-unverified. -->

## Background

<!-- RAW kept sections from {path}/data.xml (everything before the tribunal's
     own reasoning) — used as-is; trim only if context length forces it.
     Withheld headings: {', '.join(h for h, _ in withheld) or '(none)'} -->

{background_text(kept)}

## Disputed information

TODO

## Oracle facts

{oracle}

## Gold

{gold}

<!-- header disposition hint: appeal is {disp} -->
{notes}
## Gold rules

engaged: {engaged}
pi: {pi}
"""
    out.write_text(md)
    print(f"  wrote {out.relative_to(HERE)} "
          f"({len(kept)} sections kept, {len(withheld)} withheld)")
    print(f"  reasoning -> {reasoning.relative_to(HERE)}")
    print(f"  disposition hint: appeal is {disp}")


# ── label drafting (model transcribes the tribunal's own findings) ──────────

LABEL_SYSTEM = """\
You are preparing GROUND-TRUTH labels for an eval, from a UK First-tier
Tribunal FOIA decision. You are given the tribunal's reasoning sections (which
state its findings explicitly) and an atom dictionary. TRANSCRIBE the
tribunal's findings — do not judge the case yourself; if the reasoning does
not state a finding, leave it out.

Produce:
1. "oracle_facts": every dictionary atom that holds according to the
   tribunal's findings, as a list. Include the procedural atoms (Request,
   HoldsInfo, ConfirmOrDeny, RefusalNotice) when the decision shows a request
   was made, the information is held, and the authority responded citing an
   exemption. Never include Disclose.
2. "gold": "withhold" if the tribunal upholds the withholding (appeal
   dismissed), "disclose" if it orders disclosure.
3. "engaged": which exemption rules the tribunal found ENGAGED, from:
   {rules}. Empty list if it found none engaged.
4. "pi": the tribunal's s2(2)(b) public-interest conclusion — "maintain",
   "disclose", or "na" if it never reached the balance.
5. "exemptions": the statutory provisions in play, e.g. "s42(1)".
6. "notes": one or two sentences citing the paragraphs that state these
   findings.

Reply with ONLY that JSON object."""


def draft_labels(slug: str, model: str) -> dict:
    """Model-drafted labels from the withheld reasoning. A DRAFT: a human must
    verify against the reasoning file and flip `verified:` to yes. Use a
    different model from the one being evaluated (label noise must not
    correlate with the system under test)."""
    sys.path.insert(0, str(HERE))
    from pipeline import (DDL, ENGAGEMENT, atom_dictionary, call_openai,
                          parse_json_reply,
                          start_run)  # also puts the repo root on sys.path
    from deontic_py import Deontic

    start_run(f"label_{slug}")
    reasoning = (CACHE / f"{slug}_reasoning.txt").read_text()
    d = Deontic()
    user = (f"ATOM DICTIONARY:\n{atom_dictionary(d)}\n\n"
            f"TRIBUNAL REASONING:\n{reasoning}")
    system = LABEL_SYSTEM.format(rules=", ".join(ENGAGEMENT))
    lab = parse_json_reply(call_openai(model, system, user,
                                       {"arm": "label", "slug": slug}))
    # validate against the theory; silently dropping nothing — report instead
    atoms = {e.atom for e in d.atoms(str(DDL))} - {"Disclose"}
    bad = [f for f in lab.get("oracle_facts", []) if f not in atoms]
    if bad:
        print(f"  label draft: dropped unknown atoms {', '.join(bad)}")
    lab["oracle_facts"] = [f for f in lab.get("oracle_facts", []) if f in atoms]
    lab["engaged"] = [r for r in lab.get("engaged", []) if r in ENGAGEMENT]
    lab["model"] = model
    return lab


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("case", help="FCL judgment URL or path (e.g. ukftt/grc/2024/601)")
    ap.add_argument("--out", help="output name (default: cases/<slug>_draft.md)")
    ap.add_argument("--force", action="store_true", help="overwrite existing output")
    ap.add_argument("--refresh", action="store_true", help="re-fetch even if cached")
    ap.add_argument("--label", action="store_true",
                    help="model-draft Oracle facts / Gold / Gold rules from the "
                         "withheld reasoning (human verification still required)")
    ap.add_argument("--label-model", default="gpt-4.1",
                    help="model for --label; use a DIFFERENT model from the one "
                         "you evaluate (default: gpt-4.1)")
    ap.add_argument("--withhold-from", metavar="HEADING",
                    help="start withholding at the first heading containing "
                         "this substring (for decisions without a Discussion "
                         "umbrella heading — check the printed KEEP/HIDE split)")
    args = ap.parse_args()

    path = norm_path(args.case)
    slug, xml_text = fetch_xml(path, args.refresh)
    j = parse_judgment(xml_text)
    print(f"  case: {j['name'] or '?'}  ({j['cite']})")

    CASES.mkdir(exist_ok=True)
    out = CASES / (args.out if args.out else f"{slug}_draft.md")
    if out.suffix != ".md":
        out = out.with_suffix(".md")
    if out.exists() and not args.force:
        print(f"error: {out} exists (use --force to overwrite)", file=sys.stderr)
        return 1
    labels = None
    if args.label:
        # writes cache/<slug>_reasoning.txt first
        scaffold(path, slug, j, out, withhold_from=args.withhold_from)
        labels = draft_labels(slug, args.label_model)
        print(f"  label draft ({args.label_model}): gold={labels.get('gold')}, "
              f"engaged={labels.get('engaged')}, pi={labels.get('pi')}")
    scaffold(path, slug, j, out, labels, withhold_from=args.withhold_from)
    return 0


if __name__ == "__main__":
    sys.exit(main())
