# Codice Penale italiano in DDL

A defeasible-deontic formalization of the Italian penal code (Regio Decreto
1398/1930), built **article by article** so an LLM judge can reason over it.
The point is decomposition: an offence is not one opaque atom ("did a theft
happen?") but the **conjunction of its constitutive elements**, each a discrete
fact a judge verifies — so when the offence does *not* hold, you see exactly
*which* element failed.

The methodology is written up in [`PRINCIPLES.md`](PRINCIPLES.md); read it
first. Source text (verbatim Italian, stable line numbers for the atom `uri:`
provenance) is in [`sources/`](sources/); the PDF is
<https://uwm.edu.pl/kpkm/uploads/files/codice-penale.pdf>.

## Files

| File | Articles | Role |
|------|----------|------|
| `parte_generale.ddl` | 50, 51, 52, 54, 85/87/88, 97 | the causes that exclude **punibilità** + the `FattoTipico → Sanziona` hinge; the base every offence imports |
| `definizioni.ddl`    | 43, 61, 624 c.2, … | **shared vocabulary**: elements reused across offences (Impossessamento, Sottrazione, Violenza, Dolo…) and shared consequences (`Ergastolo`) |
| `omicidio.ddl`       | 575, 576, 577 | homicide decomposed: `CagionaMorte + Dolo`; aggravanti compose onto the shared `Ergastolo` |
| `furto.ddl`          | 624, 625 | theft: four elements + querela procedibility + two art. 625 aggravanti |
| `rapina.ddl`         | 628 | robbery = furto's four (shared) elements **+** `Violenza`/`Minaccia` — the composition demo |
| `ordine_autorita.ddl`| 51 c.3-4 | a deliberately **unresolved** case → `[JUDGE]` |
| `tests.sh`           | —        | 31 runnable assertions (`bash examples/codice_penale/tests.sh`) |

Import graph: an offence file does `from definizioni.ddl import *`, which itself
re-exports `parte_generale.ddl` — so every offence gets the shared elements,
the shared penalties, and the whole defence system from one line.

## How an offence is modelled

```
# furto, art. 624 — the conduct is the CONJUNCTION of four adjudicable elements:
tipico_624: Impossessamento, CosaMobileAltrui, Sottrazione, FineDiProfitto, O(Procedibile)
            =>O@Giudice FattoTipico
pena_624:   Impossessamento, CosaMobileAltrui, Sottrazione, FineDiProfitto, O(Sanziona)
            =>O@Giudice ReclusioneFurto
```

Drop any one element (e.g. the holder *consented*, so `Sottrazione` is false; or
there was no profit motive, so `FineDiProfitto` is false) and `Sanziona` never
fires — **no offence**, and the trace shows which element is missing. That is
the whole value for an LLM judge: it grounds the case onto these atoms, the
engine does the rest.

## Two bearers, one hinge, shared defences

Every penal norm has two layers carried by two Hohfeldian **bearers**:

```
  precetto   =>O@Chiunque ~CagionaMorte      # norma primaria: chiunque
  tipico     CagionaMorte, Dolo =>O@Giudice FattoTipico
  # once, in parte_generale.ddl, shared by ALL offences:
  sanzione_base  O(FattoTipico) =>O@Giudice Sanziona
  giust_difesa   … =>O@Giudice ~Sanziona     # … salvo le cause di non punibilità
```

`Sanziona` ("the offender ought to be punished") is the generic hinge: every
offence pours into `FattoTipico`, one shared rule turns that into the duty to
punish, and the causes of (non-)punishability — justifications (artt. 50-54),
non-imputability (artt. 85/88/97), the exceptions to those (art. 87 *actio
libera in causa*, art. 54 c.2) — bear on it **once** and apply to every offence
with no per-article wiring. Because the offender's duty (`@Chiunque`) and the
judge's duty (`@Giudice`) live in separate bearer scopes, a justified killing
still *violates the precetto* (reported) while the judge's duty to punish is
switched off. Aggravating circumstances replace the base penalty as *lex
specialis* (premeditazione → `Ergastolo`; art. 625 → heavier reclusion).

## Reference resolution & sharing

Cross-references are pulled in as concrete conditions, and **identical things
share one atom** so facts compose across offences:

- `Ergastolo` is the *same* atom whether art. 576, 577 (or, later, 422/630)
  prescribes it — one life-imprisonment consequence, composed onto.
- `Impossessamento`, `Sottrazione`, `CosaMobileAltrui`, `FineDiProfitto`,
  `Violenza`, `Minaccia` are shared elements: assert the same four furto facts
  and you get **furto** (in `furto.ddl`, with querela) or **rapina** (in
  `rapina.ddl`, once `Violenza` is added).

Sharing is applied only where the identity is obvious; graded penalties
(reclusion *da X a Y*) stay article-specific because the range differs.

## Try it

```bash
lake build deontic
bash examples/codice_penale/tests.sh                       # 31 assertions

B=Impossessamento,CosaMobileAltrui,Sottrazione,FineDiProfitto
deontic query examples/codice_penale/furto.ddl  ReclusioneFurto --assume $B,Querela   # O: furto
deontic query examples/codice_penale/furto.ddl  Sanziona        --assume $B           # P: improcedibile
deontic query examples/codice_penale/rapina.ddl ReclusioneRapina --assume $B,Violenza # O: rapina
deontic query examples/codice_penale/omicidio.ddl Sanziona --assume CagionaMorte,Dolo,PericoloAttuale,DifesaProporzionata  # F: legittima difesa
deontic abduce examples/codice_penale/omicidio.ddl 'F(Sanziona)' --assume CagionaMorte,Dolo --all
#   → the minimal fact-sets that make a dolose killer non-punishable
```

A teaching artefact for an LLM agent society's rulebook, not a tool for real
legal practice. It grows article by article (next: more delitti contro la
persona and contro il patrimonio), depth over breadth.
