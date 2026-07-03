#!/usr/bin/env python3
"""E1/E2 run inspector — single-file, stdlib-only local viewer.

  python3 eval/expA/e1_viewer.py        # then open http://localhost:8052

Reads (preferring runs/, falling back to the committed top-level copies):
  stream.jsonl                          the 200-case stream (gold)
  runs/e1/disputes.jsonl                first-pass tri-states + dispute reasons
  runs/e1/store_precedent*.jsonl        judge holdings v1..v6 (+ uniform)
  runs/e1/results_e1.jsonl              E1 eval rows (arm x model x case)
  runs/e2/results_e2*.jsonl             E2 rows (policy x n x model x case)

Tabs: Cases (filter + per-case drill-down incl. judge rationales and raw
model replies), Stores (holdings vs gold per judge version), E2 grid,
Scores (the two SCORES.md files).
"""
from __future__ import annotations

import json
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
PORT = 8052


def _jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def _first(*paths: Path) -> Path:
    for p in paths:
        if p.exists():
            return p
    return paths[0]


# ── load everything once ─────────────────────────────────────────────────────

STREAM = {c["case_id"]: c for c in _jsonl(_first(HERE / "stream.jsonl"))}
DISPUTES = {d["case_id"]: d for d in _jsonl(
    _first(HERE / "runs/e1/disputes.jsonl", HERE / "disputes_e1.jsonl"))}
E1 = _jsonl(_first(HERE / "runs/e1/results_e1.jsonl", HERE / "results_e1.jsonl"))

STORES: dict[str, list[dict]] = {}
for name, fname in [("v1", "store_precedent.jsonl"), ("v2", "store_precedent_v2.jsonl"),
                    ("v3", "store_precedent_v3.jsonl"), ("v4", "store_precedent_v4.jsonl"),
                    ("v5", "store_precedent_v5.jsonl"), ("v6", "store_precedent_v6.jsonl"),
                    ("uniform", "store_uniform.jsonl")]:
    rows = _jsonl(_first(HERE / "runs/e1" / fname, HERE / fname))
    if rows:
        STORES[name] = rows

E2_FILES = {p.stem.replace("results_e2", "e2") or "e2": p
            for p in sorted((HERE / "runs/e2").glob("results_e2*.jsonl"))} \
    if (HERE / "runs/e2").exists() else {}
E2 = {tag: _jsonl(p) for tag, p in E2_FILES.items()}

ATOMS = list(next(iter(STREAM.values()))["assignment"]) if STREAM else []


def ok(r):  # verdict-correct predicate for result rows
    return r["pred_verdict"]["share_status"] == r["gold"]["share_status"]


def case_gold_findings(c):
    return {a: ("true" if v else "false") for a, v in c["assignment"].items()}


# ── api ──────────────────────────────────────────────────────────────────────

def api_meta():
    armkeys = sorted({f"{r['arm']}|{r['model']}" for r in E1})
    return {"n_cases": len(STREAM), "atoms": ATOMS, "armkeys": armkeys,
            "stores": list(STORES), "e2_files": list(E2)}


def api_cases():
    e1_by_case = defaultdict(dict)
    for r in E1:
        e1_by_case[r["case_id"]][f"{r['arm']}|{r['model']}"] = int(ok(r))
    out = []
    for c in sorted(STREAM.values(), key=lambda c: c["t"]):
        d = DISPUTES.get(c["case_id"], {})
        out.append({
            "case_id": c["case_id"], "t": c["t"], "tier": c["tier"],
            "acted": c["acted"], "gold": c["gold"]["share_status"],
            "assign_key": c["assign_key"],
            "contested": d.get("contested", False),
            "reasons": d.get("reasons", []),
            "leak": bool(c.get("leak_flags")),
            "arm_ok": e1_by_case.get(c["case_id"], {}),
        })
    return out


def api_case(cid: str):
    c = STREAM.get(cid)
    if not c:
        return {"error": f"unknown case {cid}"}
    gold_f = case_gold_findings(c)
    holdings = {}
    for name, rows in STORES.items():
        for h in rows:
            if h["case_id"] == cid:
                holdings[name] = {
                    "findings": h["findings"], "verdict": h["verdict"],
                    "rationale": h.get("rationale", ""), "cites": h.get("cites", []),
                    "retrieved": h.get("retrieved", []),
                    "atom_ok": {a: h["findings"].get(a) == gold_f[a] for a in ATOMS},
                    "verdict_ok": h["verdict"]["share_status"] == c["gold"]["share_status"],
                }
    e1_rows = [{
        "arm": r["arm"], "model": r["model"],
        "pred": r["pred_verdict"]["share_status"], "ok": ok(r),
        "pred_tri": r.get("pred_tri"),
        "atom_ok": ({a: r["pred_tri"].get(a) == gold_f[a] for a in ATOMS}
                    if r.get("pred_tri") else None),
        "retrieved": r.get("retrieved"),
        "n_rel": r.get("n_relevant_retrieved"),
        "n_avail": r.get("n_relevant_available"),
        "tokens": r.get("tokens", 0), "raw": (r.get("raw") or "")[:4000],
    } for r in E1 if r["case_id"] == cid]
    same_key = [x["case_id"] for x in STREAM.values()
                if x["assign_key"] == c["assign_key"] and x["case_id"] != cid]
    return {"case": c, "gold_findings": gold_f, "dispute": DISPUTES.get(cid),
            "holdings": holdings, "e1_rows": e1_rows, "same_assignment": sorted(same_key)}


def api_store(name: str):
    rows = STORES.get(name, [])
    out = []
    for h in rows:
        seed = h["case_id"].startswith("seed_")
        c = STREAM.get(h["case_id"].removeprefix("seed_"))
        gold_f = case_gold_findings(c) if c else {}
        out.append({
            "case_id": h["case_id"], "t": h["t"], "seed": seed,
            "verdict": h["verdict"]["share_status"],
            "gold": c["gold"]["share_status"] if c else "?",
            "verdict_ok": bool(c) and h["verdict"]["share_status"] == c["gold"]["share_status"],
            "n_atom_err": sum(1 for a in ATOMS if gold_f and h["findings"].get(a) != gold_f[a]),
            "wrong_atoms": [a for a in ATOMS if gold_f and h["findings"].get(a) != gold_f[a]],
            "assign_key": h.get("assign_key", ""),
            "rationale": h.get("rationale", ""), "cites": h.get("cites", []),
            "contested": h.get("contested", []),
        })
    # coherence groups: same assign_key, >1 distinct verdict
    groups = defaultdict(set)
    for h in rows:
        if not h["case_id"].startswith("seed_"):
            groups[h.get("assign_key", "")].add(h["verdict"]["share_status"])
    incoherent = {k for k, v in groups.items() if len(v) > 1}
    for o in out:
        o["incoherent_group"] = o["assign_key"] in incoherent
    return {"holdings": out, "n_incoherent_groups": len(incoherent),
            "n_groups": len(groups)}


def api_e2():
    grids = {}
    for tag, rows in E2.items():
        acc = defaultdict(lambda: [0, 0])
        for r in rows:
            k = (r["policy"], r["store_n"], r["model"])
            acc[k][0] += ok(r)
            acc[k][1] += 1
        pooled = defaultdict(lambda: [0, 0])
        for (p, n, _m), (o, t) in acc.items():
            pooled[(p, n)][0] += o
            pooled[(p, n)][1] += t
        grids[tag] = {
            "policies": sorted({k[0] for k in pooled}),
            "sizes": sorted({k[1] for k in pooled}),
            "cells": {f"{p}|{n}": round(100 * o / t, 1)
                      for (p, n), (o, t) in pooled.items()},
            "per_model": {f"{p}|{n}|{m}": round(100 * o / t, 1)
                          for (p, n, m), (o, t) in acc.items()},
        }
    return grids


def api_scores():
    return {name: p.read_text() if p.exists() else "(missing)"
            for name, p in [("E1", HERE / "runs/e1/SCORES.md"),
                            ("E2", HERE / "runs/e2/SCORES.md")]}


# ── html (single page, vanilla js) ───────────────────────────────────────────

PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
<title>E1/E2 inspector</title><style>
body{font:13px/1.45 -apple-system,system-ui,sans-serif;margin:0;background:#f6f7f9;color:#1a1d21}
nav{display:flex;gap:2px;background:#1f2430;padding:6px 10px;position:sticky;top:0;z-index:5}
nav button{background:none;border:0;color:#aeb6c4;padding:6px 12px;cursor:pointer;font-size:13px;border-radius:6px}
nav button.on{background:#3b4356;color:#fff}
#root{padding:14px 18px;max-width:1500px}
table{border-collapse:collapse;background:#fff;font-size:12.5px}
th,td{border:1px solid #e2e5ea;padding:3px 8px;text-align:left;vertical-align:top}
th{background:#eef0f4;position:sticky;top:38px;cursor:pointer}
tr:hover td{background:#f0f6ff}
.ok{color:#0a7d38}.bad{color:#c22f2f}.dim{color:#98a0ac}
.pill{display:inline-block;padding:0 7px;border-radius:9px;font-size:11px;background:#e8ebf0;margin-right:3px}
.pill.c{background:#ffe1e1;color:#a22}.pill.t2{background:#e4dcff}.pill.t1{background:#dcecff}.pill.t0{background:#e2f4e4}
.dot{display:inline-block;width:9px;height:9px;border-radius:5px;margin:0 1px}
.dot.k1{background:#39b26b}.dot.k0{background:#e35d5d}
.narr{background:#fff;border:1px solid #e2e5ea;border-radius:8px;padding:10px 14px;max-width:900px;white-space:pre-wrap}
.box{background:#fff;border:1px solid #e2e5ea;border-radius:8px;padding:10px 14px;margin:10px 0}
.badge{font-weight:600}
details{margin:4px 0}summary{cursor:pointer;color:#4762a8}
pre{white-space:pre-wrap;background:#f2f3f6;padding:8px;border-radius:6px;font-size:12px;max-width:1100px;overflow-x:auto}
input,select{padding:3px 6px;margin-right:8px;border:1px solid #cfd4dc;border-radius:5px}
a{color:#3457a0;cursor:pointer;text-decoration:none}a:hover{text-decoration:underline}
.grid td.num{text-align:right;font-variant-numeric:tabular-nums}
h2{margin:10px 0 8px}h3{margin:14px 0 6px}
.atomtbl td{font-size:11.5px;padding:2px 6px}
</style></head><body>
<nav>
 <button data-tab="cases" class="on">Cases</button>
 <button data-tab="stores">Stores</button>
 <button data-tab="e2">E2</button>
 <button data-tab="scores">Scores</button>
</nav>
<div id="root">loading…</div>
<script>
const $=q=>document.querySelector(q); let META=null, CASES=null, TAB='cases', DETAIL=null;
const esc=s=>String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const get=async p=>{const r=await fetch(p);return r.json()};
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{TAB=b.dataset.tab;DETAIL=null;
 document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('on',x===b));render()});

function tierPill(t){return `<span class="pill t${t}">T${t}</span>`}
function okdots(m,keys){return keys.map(k=>`<span class="dot k${m[k]??''}" title="${esc(k)}: ${m[k]===1?'ok':m[k]===0?'wrong':'-'}"></span>`).join('')}

async function render(){
 if(!META) META=await get('/api/meta');
 if(TAB==='cases') return DETAIL? renderCase(DETAIL): renderCases();
 if(TAB==='stores') return renderStores();
 if(TAB==='e2') return renderE2();
 if(TAB==='scores') return renderScores();
}

async function renderCases(){
 if(!CASES) CASES=await get('/api/cases');
 const f={tier:$('#f_tier')?.value??'',cont:$('#f_cont')?.value??'',gold:$('#f_gold')?.value??'',key:$('#f_key')?.value??''};
 const armkeys=META.armkeys;
 const rows=CASES.filter(c=>
   (f.tier===''||String(c.tier)===f.tier)&&
   (f.cont===''||String(c.contested)===f.cont)&&
   (f.gold===''||c.gold===f.gold)&&
   (f.key===''||c.assign_key.includes(f.key)));
 $('#root').innerHTML=`
 <h2>Cases <span class="dim">(${rows.length}/${CASES.length})</span></h2>
 <p>
  tier <select id="f_tier"><option value="">all</option><option>0</option><option>1</option><option>2</option></select>
  contested <select id="f_cont"><option value="">all</option><option value="true">yes</option><option value="false">no</option></select>
  gold <select id="f_gold"><option value="">all</option><option>obligatory</option><option>forbidden</option><option>permitted</option></select>
  assign_key <input id="f_key" placeholder="substring" value="${esc(f.key)}">
 </p>
 <table><tr><th>t</th><th>case</th><th>tier</th><th>gold</th><th>acted</th><th>disputed</th><th>assignment</th><th title="one dot per arm|model, E1 eval">arm correctness</th></tr>
 ${rows.map(c=>`<tr><td>${c.t}</td><td><a onclick="openCase('${c.case_id}')">${c.case_id}</a></td>
  <td>${tierPill(c.tier)}</td><td>${c.gold}</td><td>${c.acted?'yes':''}</td>
  <td>${c.contested?`<span class="pill c">${esc(c.reasons.join('+'))}</span>`:''}</td>
  <td class="dim" style="max-width:260px">${esc(c.assign_key)}</td>
  <td>${okdots(c.arm_ok,armkeys)}</td></tr>`).join('')}
 </table>`;
 ['f_tier','f_cont','f_gold'].forEach(id=>{const el=$('#'+id);el.value=f[id.slice(2)]??f[id.split('_')[1]];el.onchange=renderCases});
 $('#f_tier').value=f.tier;$('#f_cont').value=f.cont;$('#f_gold').value=f.gold;
 $('#f_key').onchange=renderCases;
}
window.openCase=async cid=>{DETAIL=cid;renderCase(cid)};

function atomRow(label,findings,goldF,cls){
 return `<tr><td class="badge">${esc(label)}</td>`+Object.keys(goldF).map(a=>{
  const v=findings?.[a]??'—',ok=v===goldF[a];
  return `<td class="${findings?(ok?'ok':'bad'):''}">${esc(v)}</td>`}).join('')+`</tr>`}

async function renderCase(cid){
 const d=await get('/api/case/'+cid); const c=d.case;
 const atoms=Object.keys(d.gold_findings);
 const hold=Object.entries(d.holdings);
 $('#root').innerHTML=`
 <p><a onclick="DETAIL=null;render()">&larr; all cases</a></p>
 <h2>${cid} ${tierPill(c.tier)} <span class="pill">gold: ${c.gold.share_status}</span>
  ${c.acted?'<span class="pill">acted</span>':''}
  ${d.dispute?.contested?`<span class="pill c">${esc(d.dispute.reasons.join('+'))}</span>`:'<span class="pill">settled</span>'}</h2>
 <div class="narr">${esc(c.narrative)}</div>
 <p class="dim">same latent assignment: ${d.same_assignment.map(x=>`<a onclick="openCase('${x}')">${x}</a>`).join(' ')||'(none)'}</p>

 <h3>Atom findings vs gold</h3>
 <table class="atomtbl"><tr><th></th>${atoms.map(a=>`<th>${esc(a)}</th>`).join('')}</tr>
 ${atomRow('gold',d.gold_findings,d.gold_findings)}
 ${d.dispute?Object.entries(d.dispute.first_pass).map(([m,tri])=>atomRow('1st-pass '+m,tri,d.gold_findings)).join(''):''}
 ${hold.map(([v,h])=>atomRow('judge '+v,h.findings,d.gold_findings)).join('')}
 </table>

 ${hold.length?`<h3>Judge holdings</h3>`+hold.map(([v,h])=>`
  <div class="box"><b>${v}</b> — verdict <span class="${h.verdict_ok?'ok':'bad'}">${h.verdict.share_status}</span>
   ${h.retrieved?.length?`<span class="dim">retrieved: ${h.retrieved.map(esc).join(', ')}</span>`:''}
   ${h.cites?.length?`<div>cites: ${h.cites.map(x=>`<span class="pill">${esc(x.case)}: ${esc(x.treatment)}</span>`).join('')}</div>`:''}
   <div style="margin-top:4px">${esc(h.rationale)}</div></div>`).join(''):''}

 <h3>E1 eval rows</h3>
 <table><tr><th>arm</th><th>model</th><th>pred</th><th>atoms ok</th><th>retrieval</th><th>tok</th><th>raw</th></tr>
 ${d.e1_rows.map(r=>`<tr><td>${esc(r.arm)}</td><td>${esc(r.model)}</td>
  <td class="${r.ok?'ok':'bad'}">${esc(r.pred)}</td>
  <td>${r.atom_ok?atoms.map(a=>`<span class="dot k${r.atom_ok[a]?1:0}" title="${esc(a)}"></span>`).join(''):'<span class="dim">—</span>'}</td>
  <td>${r.retrieved?`${r.n_rel}/${r.retrieved.length} rel${r.n_avail?` (avail ${r.n_avail})`:''}<div class="dim">${r.retrieved.map(esc).join(', ')}</div>`:''}</td>
  <td class="num">${r.tokens||''}</td>
  <td>${r.raw?`<details><summary>show</summary><pre>${esc(r.raw)}</pre></details>`:''}</td></tr>`).join('')}
 </table>`;
}

async function renderStores(){
 const name=window._store||META.stores[0];
 const d=await get('/api/store/'+name);
 $('#root').innerHTML=`
 <h2>Store <select id="s_sel">${META.stores.map(s=>`<option ${s===name?'selected':''}>${s}</option>`).join('')}</select>
  <span class="dim">${d.holdings.length} holdings, ${d.n_incoherent_groups}/${d.n_groups} incoherent assignment-groups</span></h2>
 <table><tr><th>t</th><th>case</th><th>verdict</th><th>gold</th><th>wrong atoms</th><th>cites</th><th>rationale</th></tr>
 ${d.holdings.map(h=>`<tr ${h.incoherent_group?'style="background:#fff6e5"':''}>
  <td>${h.t}</td><td><a onclick="TAB='cases';openCase('${h.case_id.replace('seed_','')}')">${h.case_id}</a>${h.seed?' <span class="pill">seed</span>':''}</td>
  <td class="${h.verdict_ok?'ok':'bad'}">${h.verdict}</td><td>${h.gold}</td>
  <td>${h.wrong_atoms.map(a=>`<span class="pill c">${esc(a)}</span>`).join('')}</td>
  <td>${(h.cites||[]).map(x=>`<span class="pill">${esc(x.case)}:${esc((x.treatment||'').slice(0,6))}</span>`).join('')}</td>
  <td style="max-width:520px">${esc(h.rationale)}</td></tr>`).join('')}
 </table>
 <p class="dim">orange rows = this holding's latent assignment-group has contradictory verdicts in this store (incoherence)</p>`;
 $('#s_sel').onchange=e=>{window._store=e.target.value;renderStores()};
}

async function renderE2(){
 const grids=await get('/api/e2');
 $('#root').innerHTML='<h2>E2 — verdict accuracy by policy × store size (pooled)</h2>'+
  Object.entries(grids).map(([tag,g])=>`
  <h3>${esc(tag)}</h3>
  <table class="grid"><tr><th>policy</th>${g.sizes.map(n=>`<th>n=${n}</th>`).join('')}</tr>
  ${g.policies.map(p=>`<tr><td>${esc(p)}</td>${g.sizes.map(n=>{
    const v=g.cells[p+'|'+n];
    const models=Object.entries(g.per_model).filter(([k])=>k.startsWith(p+'|'+n+'|'))
      .map(([k,x])=>k.split('|')[2]+': '+x).join('\n');
    return `<td class="num" title="${esc(models)}">${v??''}</td>`}).join('')}</tr>`).join('')}
  </table>`).join('')+
  '<p class="dim">hover a cell for per-model numbers · files under runs/e2/</p>';
}

async function renderScores(){
 const s=await get('/api/scores');
 $('#root').innerHTML=Object.entries(s).map(([k,v])=>`<h2>${k} SCORES.md</h2><pre>${esc(v)}</pre>`).join('');
}
render();
</script></body></html>"""


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _send(self, body: bytes, ctype: str):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        parts = [p for p in u.path.split("/") if p]
        try:
            if not parts:
                return self._send(PAGE.encode(), "text/html; charset=utf-8")
            if parts[0] == "api":
                fn = {"meta": api_meta, "cases": api_cases, "e2": api_e2,
                      "scores": api_scores}.get(parts[1])
                if fn:
                    return self._send(json.dumps(fn()).encode(), "application/json")
                if parts[1] == "case":
                    return self._send(json.dumps(api_case(parts[2])).encode(),
                                      "application/json")
                if parts[1] == "store":
                    return self._send(json.dumps(api_store(parts[2])).encode(),
                                      "application/json")
            self.send_error(404)
        except Exception as e:  # surface errors to the browser, keep serving
            self._send(json.dumps({"error": repr(e)}).encode(), "application/json")


if __name__ == "__main__":
    print(f"loaded: {len(STREAM)} cases, {len(E1)} E1 rows, "
          f"stores {list(STORES)}, e2 files {list(E2)}")
    print(f"open http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
